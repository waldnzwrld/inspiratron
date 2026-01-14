
from urllib.request import urlopen, Request
import json
import os

NEWS_API_KEY = os.environ["NWSKY"]
def fetch_quote() -> tuple[str, str]:
    url = 'http://api.quotable.io/quotes/random'
    res = urlopen(url)
    data = json.loads(res.read().decode('utf-8'))[0]

    return (data['author'], data['content'])

def fetch_news_headlines() -> list[dict]:
    url = f'https://newsapi.org/v2/top-headlines?country=us&apiKey={NEWS_API_KEY}'
    res = urlopen(url)
    data = json.loads(res.read().decode('utf-8'))
    articles = data['articles']
    return articles
