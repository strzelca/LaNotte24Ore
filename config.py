import os
import dotenv

BASEDIR = os.path.abspath(os.path.dirname(__file__))

dotenv.load_dotenv(os.path.join(BASEDIR, '.env'))
dotenv.load_dotenv(os.path.join(BASEDIR, '.flaskenv'))

class Config(object):
    FLASK_DEBUG = os.environ.get('FLASK_DEBUG')
    DEBUG = False
    TESTING = False
    PORT = os.environ.get('FLASK_RUN_PORT') or 5000
    DATABASE_URI = os.environ.get('DATABASE_URI') or ''
    DATABASE_KEY = os.environ.get('DATABASE_KEY') or ''
    NEWS_API_KEY = os.environ.get('NEWS_API_KEY') or ''
    WEATHER_API_KEY = os.environ.get('WEATHER_API_KEY') or ''
    IPINFO_API_KEY = os.environ.get('IPINFO_API_KEY') or ''

class ProductionConfig(Config):
    # production config
    pass


class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True