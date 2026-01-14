
from huggingface_hub import login
from transformers import AutoTokenizer, AutoModelForCausalLM, StoppingCriteria, StoppingCriteriaList
import os
import torch
from prompts import generate_judgement_prompt
token = os.environ["HFT"]
login(token)

# Model name
model_name = "google/gemma-2b"

NUM_CALLS = 3
# Use local files only to avoid HF API calls after initial download
# Set FORCE_DOWNLOAD=1 in environment to force re-download
force_download = os.environ.get("FORCE_DOWNLOAD", "0") == "1"
use_local_only = not force_download

# Load tokenizer and model
# First try with local_files_only=True, fall back to download if needed
try:
    tokenizer = AutoTokenizer.from_pretrained(
        model_name, 
        local_files_only=use_local_only,
        force_download=force_download
    )
    model = AutoModelForCausalLM.from_pretrained(
        model_name, 
        local_files_only=use_local_only,
        force_download=force_download
    )
except OSError as e:
    if use_local_only:
        # Model not found locally, try downloading it
        print("Model not found in cache. Downloading from Hugging Face...")
        tokenizer = AutoTokenizer.from_pretrained(model_name, local_files_only=False)
        model = AutoModelForCausalLM.from_pretrained(model_name, local_files_only=False)
        print("Model downloaded and cached. Future runs will use local files only.")
    else:
        raise

# Create a custom stopping criteria class that checks decoded text
class StopOnStrings(StoppingCriteria):
    def __init__(self, stop_strings, tokenizer, prompt_length):
        self.stop_strings = stop_strings
        self.tokenizer = tokenizer
        self.prompt_length = prompt_length
    
    def __call__(self, input_ids: torch.LongTensor, scores: torch.FloatTensor, **kwargs) -> bool:
        # Decode only the generated portion (after the prompt)
        generated_text = self.tokenizer.decode(input_ids[0][self.prompt_length:], skip_special_tokens=True)
        # Check if any stop string appears in the generated text
        for stop_str in self.stop_strings:
            if stop_str in generated_text:
                return True
        return False

def generate_response(prompt: str, tokens: int, temperature: float, top_p: float, repetition_penalty: float, stop_strings: list[str] =[]) -> str: 
    
    input_ids = tokenizer.encode(prompt, return_tensors="pt")
    prompt_length = input_ids.shape[1]

    stopping_criteria = StoppingCriteriaList([StopOnStrings(stop_strings, tokenizer, prompt_length)]) if stop_strings else None

    outputs = model.generate(
        input_ids,
        max_new_tokens=tokens,  # Generate up to 20 new tokens
        do_sample=True,      # Enable sampling for more varied outputs
        temperature=temperature,     # Control randomness (lower = more focused)
        top_p=top_p,
        repetition_penalty=repetition_penalty,
        stopping_criteria=stopping_criteria
    )

    # Decode only the newly generated tokens (skip the input prompt)
    generated_text = tokenizer.decode(outputs[0][input_ids.shape[1]:], skip_special_tokens=True)
    return generated_text

def judge_response(prompt: str, response: str) -> bool:
    judgement_prompt = generate_judgement_prompt(prompt, response)
    judgement = generate_response(judgement_prompt, 5, 0.2, 0.9, 1.2, stop_strings=["\n"])
    if judgement.strip().lower() == "pass":
        return True
    else:
        return False

def generate_tool_calls(prompt: str) -> list[str]:
    tool_calls = []
    for _ in range(NUM_CALLS):
        tool_calls.append(generate_response(prompt, 10, 0.2, 0.9, 1.2, stop_strings=["]", "\n"]))
    
    for i, tool_call in enumerate(tool_calls):
        while not judge_response(prompt, tool_call):
            tool_call = generate_response(prompt, 10, 0.2, 0.9, 1.2, stop_strings=["]", "\n"])

        tool_calls[i] = tool_call

    return tool_calls
