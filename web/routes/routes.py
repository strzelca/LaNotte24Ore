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
        isLoggedIn=get_full_user(db.auth.get_session()),
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
        isLoggedIn=get_full_user(db.auth.get_session()),
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
        query=request.args.get('search'),
        user_img=storage.from_('profiles').get_public_url('default_user_female.png'), 
        isLoggedIn=get_full_user(db.auth.get_session()),
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
                    isLoggedIn=get_full_user(db.auth.get_session()),
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
            isLoggedIn=get_full_user(db.auth.get_session()),
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
    location=get_location_from_ip()
    if request.method == 'POST':
        elements = ['email', 'password']

        err_c = 0
        
        for key, value in request.form.items():
            if key in elements and value != '':
                err_c = err_c+1
        
        if err_c < len(elements):
            return render_template('signin.html',
                    user_img=storage.from_('profiles').get_public_url('default_user_female.png'), 
                    isLoggedIn=get_full_user(db.auth.get_session()),
                    weather=get_weather_from_location(location),
                    weather_link=get_weather_link(location),
                    weather_icon=get_weather_icon_from_location(location),
                    categories=newsapi_const.categories,
                    error="check all values"
            )
        else:
            try:
                response = db.auth.sign_in_with_password(credentials={
                    'email': f"{request.form.get('email')}",
                    'password': f"{request.form.get('password')}"
                })
            except errors.AuthApiError as e:
                print(e)
                return render_template('signin.html',
                    user_img=storage.from_('profiles').get_public_url('default_user_female.png'), 
                    isLoggedIn=get_full_user(db.auth.get_session()),
                    weather=get_weather_from_location(location),
                    weather_link=get_weather_link(location),
                    weather_icon=get_weather_icon_from_location(location),
                    categories=newsapi_const.categories,
                    error="check all values",
                    email=request.form.get('email')
                )
            except errors.AuthInvalidCredentialsError as e:
                print(e)
                return render_template('signin.html',
                    user_img=storage.from_('profiles').get_public_url('default_user_female.png'), 
                    isLoggedIn=get_full_user(db.auth.get_session()),
                    weather=get_weather_from_location(location),
                    weather_link=get_weather_link(location),
                    weather_icon=get_weather_icon_from_location(location),
                    categories=newsapi_const.categories,
                    error="check all values",
                    email=request.form.get('email')
                )
            return redirect('/')
            
        
        return make_response("Error", 500)
    
    elif request.method == 'GET':
        return render_template('signin.html',
            user_img=storage.from_('profiles').get_public_url('default_user_female.png'), 
            isLoggedIn=get_full_user(db.auth.get_session()),
            weather=get_weather_from_location(location),
            weather_link=get_weather_link(location),
            weather_icon=get_weather_icon_from_location(location),
            categories=newsapi_const.categories,
        )
    else:
        return make_response("Not Found", 404)


@register_blueprint.route('/logout')
def logout():
    user_session = db.auth.get_session()
    if user_session != None:
        db.auth.sign_out()
        location=get_location_from_ip()
        return render_template('index.html', 
            news=json.loads(json.dumps(get_news())),
            user_img=storage.from_('profiles').get_public_url('default_user_female.png'),
            isLoggedIn=get_full_user(db.auth.get_session()),
            weather=get_weather_from_location(location),
            weather_link=get_weather_link(location),
            weather_icon=get_weather_icon_from_location(location),
            categories=newsapi_const.categories
        ) 
    else:
        return make_response("No user logged in", 401)


@register_blueprint.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        db.auth.reset_password_email(
            request.form.get('email') or ''
        )
        return render_template('forgot_password_sent.html')
    elif request.method == 'GET':
        return render_template('forgot_password.html')
    else:
        return make_response("Failed", 500)

@register_blueprint.route('/about')
def about():
    location=get_location_from_ip()
    return render_template(
        'about.html',
        isLoggedIn=get_full_user(db.auth.get_session()),
        weather=get_weather_from_location(location),
        weather_link=get_weather_link(location),
        weather_icon=get_weather_icon_from_location(location),
        categories=newsapi_const.categories
    )
from . import api