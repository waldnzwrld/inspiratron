
from urllib.request import urlopen, Request
import json

def fetch_quote():
    url = 'http://api.quotable.io/quotes/random'
    res = urlopen(url)
    data = json.loads(res.read().decode('utf-8'))[0]

    return (data['author'], data['content'])


