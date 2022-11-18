import os

BASEDIR = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    FLASK_DEBUG = os.environ.get('FLASK_DEBUG')
    DEBUG = False
    TESTING = False
    DATABASE_URI = os.environ.get('DB_URI')
    SECRET_KEY = os.environ.get('SECRET_KEY')

class ProductionConfig(Config):
    # production config
    pass


class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True