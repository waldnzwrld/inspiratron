
from tool_calls import fetch_quote, fetch_news_headlines
def initial_prompt(input_text: str) -> str:
    return f"""You are an AI assistant with access to tools. When you need to use a tool, respond with exactly one tool call in this format:
    [TOOL: tool_name(params)]

Available tools:
    - fetch_quote: Fetches a random quote, there are no params for this tool
    - fetch_headlines: Fetches the top news headlines for the US, there are no params for this tool

Format requirement: You MUST use this exact format: [TOOL: fetch_quote()]

The word "TOOL" followed by colon and space is REQUIRED. The format is [TOOL: fetch_quote()] not [fetch_quote()] or [FETCH_QUOTE()].

Rules:
    - Respond only with the tool call, no other text
    - Use exactly the format: [TOOL: fetch_quote()]
    - Generate exactly one tool call per query
    - Stop immediately after the first closing bracket

Correct: [TOOL: fetch_quote()] or [TOOL: fetch_headlines()]
Incorrect: [fetch_quote()] or [FETCH_QUOTE()] or fetch_quote()

The query is:
{input_text}

Your Answer:
    """

def generate_prompt_from_tools(tool_calls: list) -> str:

    quote = ["", ""]
    for tool in tool_calls:
        print("Tool: ", tool)
        if 'TOOL' in tool:
            # strip the tool name from the output
            tool_call = tool.split(':')[1].strip()
            if 'fetch_quote' in tool_call:
                quote = fetch_quote()
            elif 'fetch_headlines' in tool_call:
                headlines = fetch_news_headlines()
                print(headlines)

    combined_prompt = f"""Quote: "The only way to do great work is to love what you do." - Steve Jobs
Brief: Steve Jobs reminds us that passion fuels excellence. When we love our work, effort becomes joy and greatness follows naturally.

Quote: "{quote[1]}" - {quote[0]}
Brief:"""

    return combined_prompt

def generate_judgement_prompt(prompt: str, response: str) -> str:
    #DO NOT TOUCH THIS, ONLY MAKE CHANGES TO OTHER PROMPTS
    return f"""Given a prompt and response, decide if the response correctly follows the prompt's instructions.

Prompt: {prompt}

Response: {response}

If the response is too long, off-topic, or ignores the prompt's instructions, answer 'fail'.
If the response correctly follows the prompt's instructions, answer 'pass'.

Answer:"""

