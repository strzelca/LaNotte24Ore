import os
from flask import Flask
from supabase.client import create_client as database_client
from storage3 import create_client as storage_client
from config import Config

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

def register_blueprints(app):
    from web.routes import register_blueprint
    app.register_blueprint(register_blueprint)  