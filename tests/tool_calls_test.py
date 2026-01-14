from unittest.mock import patch, MagicMock
import tool_calls

def test_fetch_quote(): 
    with patch('tool_calls.urlopen') as mock_urlopen:
        mock_response = MagicMock()
        mock_response.read.return_value = b'[{"author": "John Doe", "content": "Inspirational quote"}]'
        mock_urlopen.return_value = mock_response

        res = tool_calls.fetch_quote()
        assert isinstance(res, tuple)
        assert res == ("John Doe", "Inspirational quote")
        mock_urlopen.assert_called_with('http://api.quotable.io/quotes/random')

def test_fetch_news_headlines():
    with patch('tool_calls.urlopen') as mock_urlopen:
        mock_response = MagicMock()
        mock_response.read.return_value = b'{"articles": [{"title": "Inspirational headline 1", "content": "Inspirational content 1"}, {"title": "Inspirational headline 2", "content": "Inspirational content 2"}]}'
        mock_urlopen.return_value = mock_response

        res = tool_calls.fetch_news_headlines()
        assert isinstance(res, list)
        assert len(res) == 2
        assert res[0]['title'] == "Inspirational headline 1"
        assert res[0]['content'] == "Inspirational content 1"
        assert res[1]['title'] == "Inspirational headline 2"
        assert res[1]['content'] == "Inspirational content 2"
        mock_urlopen.assert_called_with(f'https://newsapi.org/v2/top-headlines?country=us&apiKey={tool_calls.NEWS_API_KEY}')
