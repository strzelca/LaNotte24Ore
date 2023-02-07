from newsapi import NewsApiClient
from pyowm import OWM
from ipinfo import getHandler
from supabase.client import create_client as database_client
from web import create_app
import json
from gotrue import errors
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

################################################
#### INTERNAL API

def test_userinfo_api():
    client = database_client(Config.DATABASE_URI, Config.DATABASE_KEY)
    app = create_app('lanotte24ore.test')
    client_flask = app.test_client()
    try:
        user_session = client.auth.sign_in_with_password(
            credentials={
                "email": Config.AUTH_TEST_USER,
                "password": Config.AUTH_TEST_PASSWORD
            }
        )
    except errors.AuthInvalidCredentialsError as e:
        assert None
    response = client_flask.get('/api/user')
    if response.status_code == 401:
        assert None
    elif response.status_code == 200:
        assert response.status_code == 200
        print(json.dumps(json.loads(response.text), indent=4))
    else:
        assert None
    client.auth.sign_out()