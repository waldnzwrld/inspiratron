
from urllib.request import urlopen, Request

url = 'http://api.quotable.io/quotes/random'

def fetch_quote(url):
    res = urlopen(url)
    data = res.read().decode('utf-8')
    return (data['author'], data['content'])


