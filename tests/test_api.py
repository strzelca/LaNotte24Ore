from newsapi import NewsApiClient
from pyowm import OWM
from ipinfo import getHandler
from config import Config

def test_api_connection():
    newsapi = NewsApiClient(api_key=Config.NEWS_API_KEY)
    assert newsapi.get_sources() is not None

def test_weather_api_connection():
    owm = OWM(Config.WEATHER_API_KEY)
    assert owm.weather_manager() is not None

def test_ipinfo_api_connection():
    handler = getHandler(Config.IPINFO_API_KEY)
    assert handler.getDetails() is not None