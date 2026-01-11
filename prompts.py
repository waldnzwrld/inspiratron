
from tool_calls import fetch_quote, fetch_news_headlines
def initial_prompt(input_text: str) -> str:
    return f"""You are an assistant that responds with exactly one tool call.

Available tools:
- fetch_quote(): Returns an inspirational quote
- fetch_headlines(): Returns current news headlines

Query: I need motivation
Response: [TOOL: fetch_quote()]

Query: What's in the news?
Response: [TOOL: fetch_headlines()]

Query: Give me an inspiring quote
Response: [TOOL: fetch_quote()]

Query: I'm feeling down, help me
Response: [TOOL: fetch_quote()]

Query: Show me today's headlines
Response: [TOOL: fetch_headlines()]

Query: {input_text}
Response:"""

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
                # print(headlines)

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

