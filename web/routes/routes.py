import json
from flask import render_template
from . import register_blueprint
from web import create_database_client, create_storage_client, get_news, get_weather_from_location, get_location_from_ip, get_weather_icon_from_location

db = create_database_client()
storage = create_storage_client()

"""
    Application routes

    / - index
    /category/<category> - category
    /signup - signup
    /login - login
    /logout - logout
    /profile - profile
    /profile/edit - edit profile
    /profile/delete - delete profile
"""

@register_blueprint.route('/')
def index():
    location=get_location_from_ip()
    return render_template('index.html', 
        news=json.loads(json.dumps(get_news())),
        user_img=storage.from_('profiles').get_public_url('default_user_female.png'), 
        weather=get_weather_from_location(location),
        weather_icon=get_weather_icon_from_location(location)
    )

@register_blueprint.route('/signup', methods=['GET', 'POST'])
def signup():
    # TODO: implement signup
    return render_template('signup.html')


@register_blueprint.route('/about')
def about():
    return render_template('about.html')