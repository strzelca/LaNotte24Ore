from flask import render_template
from . import register_blueprint
from web import create_database_client, create_storage_client, get_weather_from_location, get_location_from_ip

db = create_database_client()
storage = create_storage_client()

@register_blueprint.route('/')
def index():
    return render_template('index.html', 
    user_img=storage.from_('profiles').get_public_url('default_user_female.png'), 
    weather=get_weather_from_location(get_location_from_ip()),
    weather_icon="sun"
)

@register_blueprint.route('/signup', methods=['GET', 'POST'])
def signup():
    return render_template('signup.html')