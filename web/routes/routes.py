from flask import render_template
from . import register_blueprint

@register_blueprint.route('/')
def index():
    return render_template('index.html')