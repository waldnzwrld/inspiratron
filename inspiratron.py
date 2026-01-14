from prompts import initial_prompt, generate_prompt_from_tools
from task import generate_response, generate_tool_calls, judge_response

# get input from command line
input_text = "give me some inspirational motivation based on famous quotes to help me navigate the current events in the news headlines today"
tool_prompt = initial_prompt(input_text)
tool_calls = generate_tool_calls(tool_prompt)

combined_prompt = generate_prompt_from_tools(tool_calls)

generated_text = generate_response(combined_prompt, 100, 0.7, 0.9, 1.2, ["\n\n", "Quote:"])
if not judge_response(combined_prompt, generated_text):
    generated_text = generate_response(combined_prompt, 100, 0.7, 0.9, 1.2, ["\n\n", "Quote:"])

print(generated_text)

