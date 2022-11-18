import os
from flask import Flask

def create_app(config_filename=None):
    app = Flask(__name__)
    config_type = os.environ.get('CONFIG_TYPE', default='config.DevelopmentConfig')
    app.config.from_object(config_type)

    register_blueprints(app)
    return app


def register_blueprints(app):
    from web.routes import register_blueprint
    app.register_blueprint(register_blueprint)