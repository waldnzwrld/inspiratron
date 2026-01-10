from task import generate_response
from rand_quote_fetcher import fetch_quote


# get input from command line
input_text = "Inspire me"
prompt = f"""You are an AI assistant with access to tools. When you need to use a tool, respond with exactly one tool call in this format:
    [TOOL: tool_name(params)]

Available tools:
    - fetch_quote: Fetches a random quote, there are no params for this tool

Format requirement: You MUST use this exact format: [TOOL: fetch_quote()]

The word "TOOL" followed by colon and space is REQUIRED. The format is [TOOL: fetch_quote()] not [fetch_quote()] or [FETCH_QUOTE()].

Rules:
    - Respond only with the tool call, no other text
    - Use exactly the format: [TOOL: fetch_quote()]
    - Generate exactly one tool call per query
    - Stop immediately after the first closing bracket

Correct: [TOOL: fetch_quote()]
Incorrect: [fetch_quote()] or [FETCH_QUOTE()] or fetch_quote()

The query is:
{input_text}

Your Answer:
    """

generated_text = generate_response(prompt, 20, 0.2, 0.9, 1.2, ["]", "\n"])

quote = ""

if 'TOOL' in generated_text:
    # strip the tool name from the output
    tool_call = generated_text.split(':')[1].strip()
    if 'fetch_quote' in tool_call:
        quote = fetch_quote()

print(f"quote: {quote[1]} by {quote[0]}")
combined_prompt = f"""
You are an AI who's purpose is to provide a summary of the following information as an informative and inspirational way to start the day.

The information available to you is:
    quote: {quote[1]} by {quote[0]}

Please return a morning brief in a friendly manner using the information available to you, be sure to include the quote and author in your response.
Morning Brief:
"""


generated_text = generate_response(combined_prompt, 100, 0.7, 0.9, 1.2)
print(generated_text)

