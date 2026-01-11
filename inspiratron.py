from prompts import initial_prompt, generate_prompt_from_tools
from task import generate_response, judge_response

NUM_CALLS = 3
# get input from command line
input_text = "Give me some inspiriational motivation to help me deal with the current state of the world"
tool_prompt = initial_prompt(input_text)
tool_calls = [generate_response(tool_prompt, 20, 0.2, 0.9, 1.2, ["]", "\n"]) for _ in range(NUM_CALLS)]

combined_prompt = generate_prompt_from_tools(tool_calls)

generated_text = generate_response(combined_prompt, 75, 0.7, 0.9, 1.2, ["\n\n", "Quote:"])
if not judge_response(combined_prompt, generated_text):
    generated_text = generate_response(combined_prompt, 75, 0.7, 0.9, 1.2, ["\n\n", "Quote:"])

print(generated_text)

