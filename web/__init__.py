import os
from flask import Flask
from supabase.client import create_client as database_client
from storage3 import create_client as storage_client
from pyowm import OWM
from ipinfo import getHandler
from config import Config
from datetime import datetime
from newsapi import NewsApiClient, const as newsapi_const
import country_converter as coco
import json
import requests
import airportsdata
import re

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

def get_full_user(user_session):
    if user_session != None:
        client = create_app().test_client()
        data = json.loads(client.get('/api/user').text)
        return data
    else:
        return None
            

def get_image():
    storage = create_storage_client()
    db = create_database_client()
    session = db.auth.get_session()
    url = storage.from_('profiles').get_public_url(
                            'default_user_female.png')
    
    if session != None:
        res = db.from_('profiles').select('profile_pic').match({"id": f'{session.user.id}'}).execute()
        if res.data[0]['profile_pic'] not in ['', None] :
            url = storage.from_('profiles').get_public_url(
                               res.data[0]['profile_pic'])
        else:
            url = storage.from_('profiles').get_public_url(
                               'default_user_female.png') 
    return url

def graphql_query(query_filename, arg=None):
    with open(f'{os.path.dirname(__file__)}/graphql/{query_filename}.gql') as query_file:
        query = query_file.read()
        if arg != None:
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

def get_news(remote_address):
    db = create_database_client()
    if announces_bogons(remote_address):
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
        if get_state_from_ip(remote_address) in newsapi_const.languages:
            country_code,language = get_state_from_ip(remote_address),language_dict[get_state_from_ip(remote_address)]
        elif get_state_from_ip(remote_address) in newsapi_const.countries:
            country_code = language = get_state_from_ip(remote_address)
        else:
            country_code = language = 'it'
    api = connect_news_api()
    if api:    
        print(f"News For: {f'{country_code}'.lower()}")
        return api.get_everything(language=f'{language}'.lower(),q=f"{coco.convert(names=country_code, to='name')}".lower(),sort_by='publishedAt')
    else:
        print("No news")
        return "Nothing to see here..."

def get_news_with_category(category, remote_address):
    db = create_database_client()
    if announces_bogons(remote_address):
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
        if str(remote_address).upper() in language_dict:
            country_code,language = get_state_from_ip(remote_address),language_dict[str(get_state_from_ip(remote_address)).upper()]
        elif get_state_from_ip(remote_address) in newsapi_const.countries:
            country_code = language = get_state_from_ip(remote_address)
        else:
            country_code = language = 'it'
    api = connect_news_api()
    if api:    
        print(f"News For: {f'{country_code}'.lower()}")
        return api.get_top_headlines(language=f'{language}'.lower(),country=f'{country_code}'.lower(),category=f'{category}'.lower())
    else:
        print("No news")
        return "Nothing to see here..."

def get_news_with_query(query, remote_address):
    db = create_database_client()
    if announces_bogons(remote_address):
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
        if str(get_state_from_ip(remote_address)).upper() in language_dict:
            country_code,language = get_state_from_ip(remote_address),language_dict[str(get_state_from_ip(remote_address)).upper()]
        elif get_state_from_ip(remote_address) in newsapi_const.countries:
            country_code = language = get_state_from_ip(remote_address)
        else:
            country_code = language = 'it'
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

def get_weather_widget(remote_address):
    handler = getHandler(Config.IPINFO_API_KEY)
    if remote_address != "127.0.0.1":
        details = handler.getDetails(remote_address)
    else:
        details = handler.getDetails()
    observation = mgr.weather_at_place(details.city)
    try:
        res = requests.get(f"https://www.iata.org/en/publications/directories/code-search/?airport.search={str(details.city).split(' ')[0]}")
        data = res.text
        content = re.findall(r'<td>([A-Z]{3})</td>', data)
        codes = []
        for td in content:
            code = td[:3]
            codes.append(code)
    except Exception as e:
        codes = None
    
    if codes != None:
        airports = airportsdata.load('IATA')
        icao_code = airports[codes[0]].get('icao')
        res = requests.get(f"https://tgftp.nws.noaa.gov/data/observations/metar/stations/{icao_code}.TXT").text
    else:
        codes = ""
    
    if observation:
        weather = observation.weather
        data = {
            'weather': str(weather.detailed_status).capitalize(),
            'temp': f"{round(weather.temperature('celsius')['temp'])}°C",
            'humidity': weather.humidity,
            'wind': weather.wind(unit='knots'),
            'city': details.city,
            'region': details.region,
            'country': details.country,
            'icon': f"https://openweathermap.org/img/wn/{weather.weather_icon_name}@4x.png",
            'metar': res.replace('\n', ' ')
        }
        return data
    return None


# # # # # # # # # # # # # # # # # # # # #
# IP Info API Methods

def get_location_from_ip(remote_address):
    handler = getHandler(Config.IPINFO_API_KEY)
    if remote_address != "127.0.0.1":
        details = handler.getDetails(remote_address)
    else:
        details = handler.getDetails()
    return details.city

def get_state_from_ip(remote_address):
    handler = getHandler(Config.IPINFO_API_KEY)
    if remote_address != "127.0.0.1":
        details = handler.getDetails(remote_address)
    else:
        details = handler.getDetails()
    return details.country

def announces_bogons(remote_address):
    handler = getHandler(Config.IPINFO_API_KEY)
    if remote_address != "127.0.0.1":
        details = handler.getDetails(remote_address)
    else:
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
