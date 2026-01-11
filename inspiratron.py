from prompts import initial_prompt, generate_prompt_from_tools
from task import generate_response


# get input from command line
input_text = "Inspire me"

tool_text = generate_response(initial_prompt(input_text), 20, 0.2, 0.9, 1.2, ["]", "\n"])

combined_prompt = generate_prompt_from_tools(tool_text)

generated_text = generate_response(combined_prompt, 200, 0.7, 0.9, 1.2)
print(generated_text)

