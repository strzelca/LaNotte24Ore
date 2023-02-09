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
import locale

owm = OWM(Config.WEATHER_API_KEY)
mgr = owm.weather_manager()

def create_app(config_filename=None):
    app = Flask(__name__)
    config_type = os.environ.get('CONFIG_TYPE', default='config.DevelopmentConfig')
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
    try :
        api.get_sources()
        return api
    except:
        print("Error: NewsAPI connection failed")
        return None

def get_news():
    api = connect_news_api()
    if api:
        return api.get_top_headlines(language='it',country='it')
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

def register_blueprints(app):
    from web.routes import register_blueprint
    app.register_blueprint(register_blueprint)  