import os
from flask import Flask
from supabase.client import create_client as database_client
from storage3 import create_client as storage_client
from pyowm import OWM
from ipinfo import getHandler
from config import Config
from datetime import datetime
import locale

owm = OWM(Config.WEATHER_API_KEY)
mgr = owm.weather_manager()

def create_app(config_filename=None):
    app = Flask(__name__)
    config_type = os.environ.get('CONFIG_TYPE', default='config.DevelopmentConfig')
    app.config.from_object(config_type)

    register_blueprints(app)
    return app

def create_database_client():
    return database_client(Config.DATABASE_URI, Config.DATABASE_KEY)

def create_storage_client():
    return storage_client(
        f"https://{Config.DATABASE_URI}/storage/v1", 
        {
            "apiKey": Config.DATABASE_KEY, 
            "Authorization": f"Bearer {Config.DATABASE_KEY}"
        },
        is_async=False)

def get_weather_from_location(location):
    observation = mgr.weather_at_place(location)
    locale.setlocale(locale.LC_ALL, locale.getdefaultlocale())
    now = datetime.now().strftime("%d %B %Y")
    if observation:
        weather = observation.weather
        return f"{round(weather.temperature('celsius')['temp'])}°C - {location}, {now}"
    return None

def get_weather_icon_from_location(location):
    observation = mgr.weather_at_place(location)
    if observation:
        weather = observation.weather
        return f"https://openweathermap.org/img/wn/{weather.weather_icon_name}.png"
    return None

def get_location_from_ip():
    handler = getHandler(Config.IPINFO_API_KEY)
    details = handler.getDetails()
    return details.city

def register_blueprints(app):
    from web.routes import register_blueprint
    app.register_blueprint(register_blueprint)  