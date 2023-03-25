import json
from flask import render_template, request, make_response, redirect
from gotrue import errors
from newsapi import const as newsapi_const
import country_converter as coco
from iso639 import languages as iso_languages
from . import register_blueprint
from web import *

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
        weather_link=get_weather_link(location),
        weather_icon=get_weather_icon_from_location(location),
        categories=newsapi_const.categories
    )

@register_blueprint.route('/categories')
def categories():
    location=get_location_from_ip()
    return render_template('category.html', 
        news=json.loads(json.dumps(get_news_with_category(request.args.get('category')))),
        user_img=storage.from_('profiles').get_public_url('default_user_female.png'), 
        weather=get_weather_from_location(location),
        weather_link=get_weather_link(location),
        weather_icon=get_weather_icon_from_location(location),
        categories=newsapi_const.categories
    )

@register_blueprint.route('/search')
def search():
    location=get_location_from_ip()
    return render_template('search.html', 
        news=json.loads(json.dumps(get_news_with_query(request.args.get('search')))),
        user_img=storage.from_('profiles').get_public_url('default_user_female.png'), 
        weather=get_weather_from_location(location),
        weather_link=get_weather_link(location),
        weather_icon=get_weather_icon_from_location(location),
        categories=newsapi_const.categories
    )

@register_blueprint.route('/signup', methods=['GET', 'POST'])
def signup():
    location=get_location_from_ip()
    countries_fullname = []
    languages_fullname = []

    newsapi_countries = []
    for country in newsapi_const.countries:
        if country not in ['zh']:
            newsapi_countries.append(country)

    for country in newsapi_countries:
        countries_fullname.append(coco.convert(names=country, to='name'))

    countries = dict(zip(countries_fullname, newsapi_countries))
    countries = {key: value for key, value in sorted(countries.items())}

    newsapi_languages = []
    for language in newsapi_const.languages:
        if language not in ['se', 'en-US','cn','ud']:
            newsapi_languages.append(language)

    for language in newsapi_languages:
        languages_fullname.append(iso_languages.get(alpha2=language).name)
    
    
    languages = dict(zip(languages_fullname, newsapi_languages))
    languages = {key: value for key, value in sorted(languages.items())}

    # REAL RENDERING

    if request.method == 'POST':
        # Manage POST request
        # Values:
        # * name
        # * surname
        # * country
        # * lang
        # * email
        # * password
        # * privacy policy

        elements = ['name', 'surname', 'country', 'lang', 'email', 'password', 'policy']

        err_c = 0
        
        for key, value in request.form.items():
            if key in elements and value != '':
                err_c = err_c+1
        
        if err_c < len(elements):
            return render_template('signup.html',
                    user_img=storage.from_('profiles').get_public_url('default_user_female.png'), 
                    weather=get_weather_from_location(location),
                    weather_link=get_weather_link(location),
                    weather_icon=get_weather_icon_from_location(location),
                    categories=newsapi_const.categories,
                    countries=countries,
                    languages=languages,
                    error="check all values"
            )

        return make_response("UwU", 200)

        
    elif request.method == 'GET':
        return render_template('signup.html',
            user_img=storage.from_('profiles').get_public_url('default_user_female.png'), 
            weather=get_weather_from_location(location),
            weather_link=get_weather_link(location),
            weather_icon=get_weather_icon_from_location(location),
            categories=newsapi_const.categories,
            countries=countries,
            languages=languages
        )
    else:
        return make_response("Not found", 404)



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