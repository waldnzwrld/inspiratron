
from huggingface_hub import login
from transformers import AutoTokenizer, AutoModelForCausalLM, StoppingCriteria, StoppingCriteriaList
import os
import torch
token = os.environ["HFT"]
login(token)

# Model name
model_name = "google/gemma-2b"

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

# Create a custom stopping criteria class
class StopOnTokens(StoppingCriteria):
    def __init__(self, stop_token_ids):
        self.stop_token_ids = stop_token_ids
    
    def __call__(self, input_ids: torch.LongTensor, scores: torch.FloatTensor, **kwargs) -> bool:
        # Check if the last token is in our stop token set
        return input_ids[0][-1].item() in self.stop_token_ids

def generate_response(prompt, tokens, temperature, top_p, repetition_penalty, stop_strings=[]): 
    
    input_ids = tokenizer.encode(prompt, return_tensors="pt")

    # Convert stop strings to token IDs
    stop_token_ids = set()
    for stop_str in stop_strings:
        # Encode the stop string and get the token IDs
        stop_tokens = tokenizer.encode(stop_str, add_special_tokens=False)
        if stop_tokens:
            stop_token_ids.update(stop_tokens)


    stopping_criteria = StoppingCriteriaList([StopOnTokens(stop_token_ids)]) if stop_token_ids else None

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

def judge_response(response, prompt):
    pass
