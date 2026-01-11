from prompts import initial_prompt, generate_prompt_from_tools
from task import generate_response, judge_response


# get input from command line
input_text = "Inspire me"
tool_prompt = initial_prompt(input_text)
tool_text = generate_response(tool_prompt, 20, 0.2, 0.9, 1.2, ["]", "\n"])

combined_prompt = generate_prompt_from_tools(tool_text)

generated_text = generate_response(combined_prompt, 200, 0.7, 0.9, 1.2)
if not judge_response(combined_prompt, generated_text ):
    generated_text = generate_response(combined_prompt, 200, 0.7, 0.9, 1.2)

print(generated_text)

