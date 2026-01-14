
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
    
    Query: Current events
    Response: [TOOL: fetch_headlines()]
    
    Query: {input_text}
    Response:"""

def generate_prompt_from_tools(tool_calls: list) -> str:

    news_resp = None
    headlines = []
    quotes = {} 
    for tool in tool_calls:
        if 'TOOL' in tool:
            # strip the tool name from the output
            tool_call = tool.split(':')[1].strip()
            if 'fetch_quote' in tool_call:
                quotes[fetch_quote()[0]] = fetch_quote()[1]
            elif 'fetch_headlines' in tool_call:
                if news_resp is None:
                    news_resp = fetch_news_headlines()
                index = len(headlines)
                content = news_resp[index]['content']
                # Strip suffix before duplicate check
                if content and '[+' in content:
                   content = content[:content.rfind('[+')]
                while content is None or content in headlines:
                   index += 1
                   content = news_resp[index]['content']
                   if content and '[+' in content:
                      content = content[:content.rfind('[+')]

                headlines.append(content)

    headlines_section = "\n".join(f"- {h}" for h in headlines)
    quotes_section = "\n".join(f'"{q}" - {a}' for a, q in quotes.items())

    print(f"Headlines:\n{headlines_section}\n\nQuotes:\n{quotes_section}\n\n\n")

    combined_prompt = f"""Headlines:
    - Markets drop amid global uncertainty as investors react to trade tensions.
    
    Quotes:
    "In the middle of difficulty lies opportunity." - Albert Einstein
    
    Message: Times of uncertainty can feel overwhelming, but as Einstein reminds us, challenges often reveal new paths forward. Stay steady and look for the opportunities within the turbulence.
    
    Headlines:
    {headlines_section}
    
    Quotes:
    {quotes_section}
    
    Message:"""

    return combined_prompt


def generate_judgement_prompt(prompt: str, response: str) -> str:
    #DO NOT TOUCH THIS, ONLY MAKE CHANGES TO OTHER PROMPTS
    return f"""Given a prompt and response, decide if the response correctly follows the prompt's instructions.

    Prompt: {prompt}
    
    Response: {response}
    
    If the response is too long, off-topic, or ignores the prompt's instructions, answer 'fail'.
    If the response correctly follows the prompt's instructions, answer 'pass'.
    
    Answer:"""

