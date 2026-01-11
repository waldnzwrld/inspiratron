
from rand_quote_fetcher import fetch_quote
def initial_prompt(input_text):
    return f"""You are an AI assistant with access to tools. When you need to use a tool, respond with exactly one tool call in this format:
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

def generate_prompt_from_tools(tool_text):

    quote = ""
    if 'TOOL' in tool_text:
        # strip the tool name from the output
        tool_call = tool_text.split(':')[1].strip()
        if 'fetch_quote' in tool_call:
            quote = fetch_quote()

    combined_prompt = f"""Write a short morning brief (2-3 sentences) that incorporates this quote: "{quote[1]}" by {quote[0]}

    The brief should be friendly and inspirational. Start directly with the message, do not include greetings or introductions.

    Brief:
    """

    return combined_prompt

def generate_judgement_prompt(prompt, response):
    return f"""Given a prompt and response, decide if the response correctly follows the prompt's instructions.

Prompt: {prompt}

Response: {response}

If the response is too long, off-topic, or ignores the prompt's instructions, answer 'fail'.
If the response correctly follows the prompt's instructions, answer 'pass'.

Answer:"""

