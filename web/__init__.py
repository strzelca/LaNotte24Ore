import os
from flask import Flask
from supabase.client import create_client as database_client
from storage3 import create_client as storage_client
from pyowm import OWM
from ipinfo import getHandler
from config import Config
from datetime import datetime
from newsapi import NewsApiClient
import json
import requests
import waitress
import locale

owm = OWM(Config.WEATHER_API_KEY)
mgr = owm.weather_manager()

def create_app(config_filename=None):
    app = Flask(__name__)
    config_type = os.environ.get('CONFIG_TYPE') or 'config.DevelopmentConfig'
    app.config.from_object(config_type)

    register_blueprints(app)
    return app

# # # # # # # # # # # # # # # # # # # # # #
# Supabase API Methods

def create_database_client():
    return database_client(Config.DATABASE_URI, Config.DATABASE_KEY)

def create_storage_client():
    return storage_client(
        f"{Config.DATABASE_URI}/storage/v1", 
        {
            "apiKey": Config.DATABASE_KEY, 
            "Authorization": f"Bearer {Config.DATABASE_KEY}"
        },
        is_async=False)

def graphql_query(query_filename, arg=None):
    with open(f'{os.path.dirname(__file__)}/graphql/{query_filename}.gql') as query_file:
        query = query_file.read()
        if arg != None:
            print(query)
            query = query.replace("ARG", arg)
        resp = requests.post(
            f'{Config.DATABASE_URI}/graphql/v1',
            headers={
                'apiKey': Config.DATABASE_KEY,
                'Content-Type': 'application/json'
            },
            json={
                "query": query
            }
        )
        return resp
    
# # # # # # # # # # # # # # # # # # # # # #
# NewsAPI Methods

def connect_news_api():
    api = NewsApiClient(api_key=Config.NEWS_API_KEY)
    try:
        api.get_sources()
        return api
    except:
        print("Error: NewsAPI connection failed")
        return None

def get_news():
    db = create_database_client()
    if announces_bogons():
        return json.loads("""
            {
                "articles": [
                    {
                        "title": "STOP USING TIM",
                        "source": {
                            "name": "A person with IPv6"
                        },
                        "publishedAt": "1914-07-28T00:00:00Z",
                        "description": "You are literally using AS6762 TELECOM ITALIA SPARKLE S.p.A."
                    }
                ]
            }
        """)
    if db.auth.get_session():
        client = create_app().test_client()
        country_code = json.loads(client.get('/api/user').text)['country']
        language = json.loads(client.get('/api/user').text)['language']
    else:
        if get_state_from_ip() in language_dict:
            country_code,language = get_state_from_ip(),language_dict[get_state_from_ip()]
        else:
            country_code = language = get_state_from_ip()
    api = connect_news_api()
    if api:    
        print(f"News For: {f'{country_code}'.lower()}")
        return api.get_everything(language=f'{language}'.lower(),q=f'Italia'.lower(),sort_by='publishedAt')
    else:
        print("No news")
        return "Nothing to see here..."

def get_news_with_category(category):
    db = create_database_client()
    if announces_bogons():
        return json.loads("""
            {
                "articles": [
                    {
                        "title": "STOP USING TIM",
                        "source": {
                            "name": "A person with IPv6"
                        },
                        "publishedAt": "1914-07-28T00:00:00Z",
                        "description": "You are literally using AS6762 TELECOM ITALIA SPARKLE S.p.A."
                    }
                ]
            }
        """)
    if db.auth.get_session():
        client = create_app().test_client()
        country_code = json.loads(client.get('/api/user').text)['country']
        language = json.loads(client.get('/api/user').text)['language']
    else:
        if get_state_from_ip() in language_dict:
            country_code,language = get_state_from_ip(),language_dict[get_state_from_ip()]
        else:
            country_code = language = get_state_from_ip()
    api = connect_news_api()
    if api:    
        print(f"News For: {f'{country_code}'.lower()}")
        return api.get_top_headlines(language=f'{language}'.lower(),country=f'{country_code}'.lower(),category=f'{category}'.lower())
    else:
        print("No news")
        return "Nothing to see here..."

def get_news_with_query(query):
    db = create_database_client()
    if announces_bogons():
        return json.loads("""
            {
                "articles": [
                    {
                        "title": "STOP USING TIM",
                        "source": {
                            "name": "A person with IPv6"
                        },
                        "publishedAt": "1914-07-28T00:00:00Z",
                        "description": "You are literally using AS6762 TELECOM ITALIA SPARKLE S.p.A."
                    }
                ]
            }
        """)
    if db.auth.get_session():
        client = create_app().test_client()
        country_code = json.loads(client.get('/api/user').text)['country']
        language = json.loads(client.get('/api/user').text)['language']
    else:
        if get_state_from_ip() in language_dict:
            country_code,language = get_state_from_ip(),language_dict[get_state_from_ip()]
        else:
            country_code = language = get_state_from_ip()
    api = connect_news_api()
    if api:    
        print(f"News For: {f'{country_code}'.lower()}")
        return api.get_everything(language=f'{language}'.lower(),q=f'{query}'.replace('+', ' '),sort_by='publishedAt')
    else:
        print("No news")
        return "Nothing to see here..."

# # # # # # # # # # # # # # # # # # # # # #
# OpenWeatherAPI Methods

def get_weather_from_location(location):
    observation = mgr.weather_at_place(location)
    now = datetime.now().strftime("%d %B %Y")
    if observation:
        weather = observation.weather
        return f"{round(weather.temperature('celsius')['temp'])}°C - {location}, {now}"
    return None

def get_weather_link(location):
    observation = mgr.weather_at_place(location)
    if observation:
        loc = observation.location
        return f"https://openweathermap.org/city/{loc.id}"

def get_weather_icon_from_location(location):
    observation = mgr.weather_at_place(location)
    if observation:
        weather = observation.weather
        return f"https://openweathermap.org/img/wn/{weather.weather_icon_name}@4x.png"
    return None



# # # # # # # # # # # # # # # # # # # # #
# IP Info API Methods

def get_location_from_ip():
    handler = getHandler(Config.IPINFO_API_KEY)
    details = handler.getDetails()
    return details.city

def get_state_from_ip():
    handler = getHandler(Config.IPINFO_API_KEY)
    details = handler.getDetails()
    return details.country

def announces_bogons():
    handler = getHandler(Config.IPINFO_API_KEY)
    details = handler.getDetails()
    if details.org == "AS6762 TELECOM ITALIA SPARKLE S.p.A.":
        return True
    else:
        return False

def register_blueprints(app):
    from web.routes import register_blueprint
    app.register_blueprint(register_blueprint)  




# Create ad associative array of language codes and language names based on
# IPInfo country codes

language_dict = {
    "US": "en",
    "GB": "en",
    "AU": "en",
    "CA": "en",
    "NZ": "en",
    "IE": "en",
    "ZA": "en",
    "IN": "en",
    "SG": "en",
    "PH": "en",
    "MY": "en",
    "HK": "en",
    "CN": "en",
    "JP": "en",
    "KR": "en",
    "TW": "en",
    "TH": "en",
    "ID": "en",
    "BG": "en",
    "HR": "en",
    "CZ": "en",
    "AL": "en",
    "UA": "ru"
}