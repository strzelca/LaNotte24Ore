from newsapi import NewsApiClient
from config import Config

def test_api_connection():
    newsapi = NewsApiClient(api_key=Config.NEWS_API_KEY)
    assert newsapi.get_sources() is not None