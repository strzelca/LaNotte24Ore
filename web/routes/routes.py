import json
from flask import render_template, request, make_response
from gotrue import errors
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



@register_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.json == None:
            return make_response("Empty Request", 404) 
        status_code = 200
        data = request.json
        try:
            response = db.auth.sign_in_with_password(credentials=data)
        except errors.AuthApiError as e:
            print(e)
            status_code = 401
        except errors.AuthInvalidCredentialsError as e:
            print(e)
            status_code = 401
        
        return make_response("Logged In", status_code)
    elif request.method == 'GET':
        return make_response("OwO", 200)
    else:
        return make_response("Not Found", 404)


@register_blueprint.route('/logout')
def logout():
    user_session = db.auth.get_session()
    if user_session != None:
        db.auth.sign_out()
        return make_response("Logged Out", 200)
    else:
        return make_response("No user logged in", 401)

@register_blueprint.route('/about')
def about():
    return render_template('about.html')

from . import api