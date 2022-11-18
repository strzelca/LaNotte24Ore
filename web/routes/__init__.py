from flask import Blueprint

register_blueprint = Blueprint('routes', __name__, template_folder='templates')

from . import routes