# -*- coding: utf-8 -*-

from . import api
import json
from flask import render_template, request, make_response, redirect
from gotrue import errors
from newsapi import const as newsapi_const
import country_converter as coco
from iso639 import languages as iso_languages
from . import register_blueprint
import ast
from storage3 import utils
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
    location = get_location_from_ip(request.remote_addr)
    session = db.auth.get_session()
        
    if session != None:
        favorites = db.table("favorites").select('id, article').eq('user_id', f'{session.user.id}').execute().data
        articles = {'articles': [], 'id': []}
        for favorite in favorites:
            article_str = favorite['article']
            article_json = ast.literal_eval(json.loads(article_str))
            articles['articles'].append(article_json)
            articles['id'].append(favorite['id'])
    else:
        articles = {'articles': [], 'id': []}

    return render_template('index.html',
                           news=json.loads(json.dumps(get_news(request.remote_addr))),
                           favorites=articles,
                           user_img=get_image(),
                           isLoggedIn=get_full_user(db.auth.get_session()),
                           weather=get_weather_from_location(location),
                           weather_link=get_weather_link(location),
                           weather_icon=get_weather_icon_from_location(
                               location),
                            weather_widget=get_weather_widget(request.remote_addr),
                           categories=newsapi_const.categories
                           )


@register_blueprint.route('/categories')
def categories():
    location = get_location_from_ip(request.remote_addr)
    return render_template('category.html',
                           news=json.loads(json.dumps(
                               get_news_with_category(request.args.get('category'), request.remote_addr))),
                           user_img=get_image(),
                           isLoggedIn=get_full_user(db.auth.get_session()),
                           weather=get_weather_from_location(location),
                           weather_link=get_weather_link(location),
                           weather_icon=get_weather_icon_from_location(
                               location),
                            weather_widget=get_weather_widget(request.remote_addr),
                           categories=newsapi_const.categories
                           )


@register_blueprint.route('/search')
def search():
    location = get_location_from_ip(request.remote_addr)
    return render_template('search.html',
                           news=json.loads(json.dumps(
                               get_news_with_query(request.args.get('search'), request.remote_addr))),
                           query=request.args.get('search'),
                           user_img=get_image(),
                           isLoggedIn=get_full_user(db.auth.get_session()),
                           weather=get_weather_from_location(location),
                           weather_link=get_weather_link(location),
                           weather_icon=get_weather_icon_from_location(
                               location),
                            weather_widget=get_weather_widget(request.remote_addr),
                           categories=newsapi_const.categories
                           )


@register_blueprint.route('/signup', methods=['GET', 'POST'])
def signup():
    location = get_location_from_ip(request.remote_addr)
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
        if language not in ['se', 'en-US', 'cn', 'ud']:
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

        elements = ['name', 'surname', 'country',
                    'lang', 'email', 'password', 'policy']

        err_c = 0

        for key, value in request.form.items():
            if key in elements and value != '':
                err_c = err_c+1

        if err_c < len(elements):
            return render_template('signup.html',
                                   user_img=get_image(),
                                   isLoggedIn=get_full_user(
                                       db.auth.get_session()),
                                   weather=get_weather_from_location(location),
                                   weather_link=get_weather_link(location),
                                   weather_icon=get_weather_icon_from_location(
                                       location),
                                   categories=newsapi_const.categories,
                                   countries=countries,
                                   languages=languages,
                                   error="check all values"
                                   )

        if not bool(request.form.get('policy')):
            return render_template('signup.html',
                                   user_img=get_image(),
                                   isLoggedIn=get_full_user(
                                       db.auth.get_session()),
                                   weather=get_weather_from_location(location),
                                   weather_link=get_weather_link(location),
                                   weather_icon=get_weather_icon_from_location(
                                       location),
                                   categories=newsapi_const.categories,
                                   countries=countries,
                                   languages=languages,
                                   error="privacy policy must be accepted"
                                   )

        data = {}

        for element in elements:
            if element != 'policy':
                data.update({element: request.form.get(element)})

        try:
            res = db.auth.sign_up(
                credentials={
                    'email': f"{data['email']}",
                    'password': f"{data['password']}"
                }
            )
        except errors.AuthInvalidCredentialsError as e:
            return render_template('signup.html',
                                   user_img=get_image(),
                                   isLoggedIn=get_full_user(
                                       db.auth.get_session()),
                                   weather=get_weather_from_location(location),
                                   weather_link=get_weather_link(location),
                                   weather_icon=get_weather_icon_from_location(
                                       location),
                                   categories=newsapi_const.categories,
                                   countries=countries,
                                   languages=languages,
                                   error="user already exist or unvalid"
                                   )

        if res.user != None:
            try:
                db.from_('profiles').insert(
                    {
                        'id': res.user.id, 
                        'name': f"{data['name']}", 
                        'surname': f"{data['surname']}", 
                        'profile_pic': "",
                        'lang': f"{data['lang']}", 
                        'country': f"{data['country']}"
                    }
                ).execute()
            except json.JSONDecodeError as e:
                pass

        return render_template(
            'sent_email.html',
            user_img=get_image(),
            isLoggedIn=get_full_user(db.auth.get_session()),
            weather=get_weather_from_location(location),
            weather_link=get_weather_link(location),
            weather_icon=get_weather_icon_from_location(location),
            categories=newsapi_const.categories
        )

    elif request.method == 'GET':
        return render_template('signup.html',
                               user_img=get_image(),
                               isLoggedIn=get_full_user(db.auth.get_session()),
                               weather=get_weather_from_location(location),
                               weather_link=get_weather_link(location),
                               weather_icon=get_weather_icon_from_location(
                                   location),
                               categories=newsapi_const.categories,
                               countries=countries,
                               languages=languages
                               )
    else:
        return make_response("Not found", 404)


@register_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    location = get_location_from_ip(request.remote_addr)
    if request.method == 'POST':
        elements = ['email', 'password']

        err_c = 0

        for key, value in request.form.items():
            if key != 'redirect':
                if key in elements and value != '':
                    err_c = err_c+1

        if err_c < len(elements):
            return render_template('signin.html',
                                   user_img=get_image(),
                                   isLoggedIn=get_full_user(
                                       db.auth.get_session()),
                                   weather=get_weather_from_location(location),
                                   weather_link=get_weather_link(location),
                                   weather_icon=get_weather_icon_from_location(
                                       location),
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
                                       user_img=get_image(),
                                       isLoggedIn=get_full_user(
                                           db.auth.get_session()),
                                       weather=get_weather_from_location(
                                           location),
                                       weather_link=get_weather_link(location),
                                       weather_icon=get_weather_icon_from_location(
                                           location),
                                       categories=newsapi_const.categories,
                                       error="check all values",
                                       email=request.form.get('email')
                                       )
            except errors.AuthInvalidCredentialsError as e:
                print(e)
                return render_template('signin.html',
                                       user_img=get_image(),
                                       isLoggedIn=get_full_user(
                                           db.auth.get_session()),
                                       weather=get_weather_from_location(
                                           location),
                                       weather_link=get_weather_link(location),
                                       weather_icon=get_weather_icon_from_location(
                                           location),
                                       categories=newsapi_const.categories,
                                       error="check all values",
                                       email=request.form.get('email')
                                       )
            if request.form.get('redirect') != None:
                return redirect(f"{request.form.get('redirect')}")
            else:
                return redirect('/')

        return make_response("Error", 500)

    elif request.method == 'GET':
        if request.args.get('redirect') != None:
            return render_template('signin.html',
                               user_img=get_image(),
                               isLoggedIn=get_full_user(db.auth.get_session()),
                               weather=get_weather_from_location(location),
                               weather_link=get_weather_link(location),
                               weather_icon=get_weather_icon_from_location(
                                   location),
                               categories=newsapi_const.categories,
                               redirect=request.args.get('redirect')
                               )
        else:
            return render_template('signin.html',
                               user_img=get_image(),
                               isLoggedIn=get_full_user(db.auth.get_session()),
                               weather=get_weather_from_location(location),
                               weather_link=get_weather_link(location),
                               weather_icon=get_weather_icon_from_location(
                                   location),
                               categories=newsapi_const.categories,
                               )
    else:
        return make_response("Not Found", 404)


@register_blueprint.route('/logout')
def logout():
    user_session = db.auth.get_session()
    if user_session != None:
        db.auth.sign_out()
        location = get_location_from_ip(request.remote_addr)
        return redirect('/')
    else:
        return redirect('/')
    
@register_blueprint.route('/user', methods=['GET', 'POST'])
def user():
    location = get_location_from_ip(request.remote_addr)
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
        if language not in ['se', 'en-US', 'cn', 'ud']:
            newsapi_languages.append(language)

    for language in newsapi_languages:
        languages_fullname.append(iso_languages.get(alpha2=language).name)

    languages = dict(zip(languages_fullname, newsapi_languages))
    languages = {key: value for key, value in sorted(languages.items())}
    session = db.auth.get_session()
    if session != None:
        client = create_app().test_client()
        data = json.loads(client.get('/api/user').text)
        favorites = db.table("favorites").select('id, article').eq('user_id', f'{session.user.id}').execute().data
        articles = {'articles': [], 'id': []}
        for favorite in favorites:
            article_str = favorite['article']
            article_json = ast.literal_eval(json.loads(article_str))
            articles['articles'].append(article_json)
            articles['id'].append(favorite['id'])

        return render_template('user.html',
                            news=articles,
                            user_img=get_image(),
                            user=data,
                            isLoggedIn=get_full_user(session),
                            weather=get_weather_from_location(location),
                            weather_link=get_weather_link(location),
                            weather_icon=get_weather_icon_from_location(
                                   location),
                            categories=newsapi_const.categories,
                            countries=countries,
                            languages=languages
                               )
    else:
        return redirect('/login?redirect=/user')

@register_blueprint.route('/change_user_settings', methods=['POST'])
def change_user_settings():
    if request.method == "POST":
        session = db.auth.get_session()
        if session != None:
            form_data = f'{request.form.get("name")}'.split(' ')
            res = db.table('profiles').update(
                {
                    'name': f'{form_data[0]}',
                    'surname': f'{form_data[1]}',
                    'lang': f'{request.form.get("lang")}', 
                    'country': f'{request.form.get("country")}'
                }
                ).eq('id', f'{session.user.id}').execute()  
    return redirect('/user')

        
@register_blueprint.route('/favorite', methods=['GET', 'POST'])
def favorite():
    if request.method == 'POST':
        if request.form.get('add') == "1":
            article = json.dumps(request.form.get("article") or '{}').encode('utf-8')
            session = db.auth.get_session()
            if session != None:
                db.table("favorites").insert(
                    {
                        'user_id': f'{session.user.id}',
                        'article': article.decode()
                    }
                ).execute()
        elif request.form.get('remove') == "1":
            session = db.auth.get_session()
            if session != None:
                db.table("favorites").delete().eq('id', f'{request.form.get("id")}').execute()
    return redirect(f"{request.form.get('redirect')}")

@register_blueprint.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    location = get_location_from_ip(request.remote_addr)
    if request.method == 'POST':
        db.auth.reset_password_email(
            request.form.get('email') or ''
        )
        return render_template(
            'forgot_password_sent.html',
            user_img=get_image(),
            isLoggedIn=get_full_user(db.auth.get_session()),
            weather=get_weather_from_location(location),
            weather_link=get_weather_link(location),
            weather_icon=get_weather_icon_from_location(location),
            categories=newsapi_const.categories
        )
    elif request.method == 'GET':
        return render_template(
            'forgot_password.html',
            isLoggedIn=get_full_user(db.auth.get_session()),
            user_img=get_image(),
            weather=get_weather_from_location(location),
            weather_link=get_weather_link(location),
            weather_icon=get_weather_icon_from_location(location),
            categories=newsapi_const.categories
            )
    else:
        return make_response("Failed", 500)

@register_blueprint.route('/about')
def about():
    location = get_location_from_ip(request.remote_addr)
    return render_template(
        'about.html',
        isLoggedIn=get_full_user(db.auth.get_session()),
        user_img=get_image(),
        weather=get_weather_from_location(location),
        weather_link=get_weather_link(location),
        weather_icon=get_weather_icon_from_location(location),
        categories=newsapi_const.categories
    )

@register_blueprint.route('/policy')
def policy():
    location = get_location_from_ip(request.remote_addr)
    return render_template(
        'policy.html',
        isLoggedIn=get_full_user(db.auth.get_session()),
        user_img=get_image(),
        weather=get_weather_from_location(location),
        weather_link=get_weather_link(location),
        weather_icon=get_weather_icon_from_location(location),
        categories=newsapi_const.categories
    )

@register_blueprint.route('/change_pic', methods=['GET', 'POST'])
def change_pic():
    ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
    session = db.auth.get_session()
    if request.method == 'POST':
        if session != None and session.user != None:
            if 'pic' not in request.files:
                return redirect('/user')
            pic = request.files['pic']
            if pic.filename != None:
                if pic.filename.split('.')[1] not in ALLOWED_EXTENSIONS:
                    return redirect('/user')
                path = os.path.join(f'{Config.UPLOAD_FOLDER}', f'{pic.filename}')
                pic.save(path)
                with open(path, 'rb+'):
                    try:
                        storage.from_('profiles').upload(f"{session.user.id}.{pic.filename.split('.')[1]}", os.path.abspath(path))
                    except utils.StorageException:
                        storage.from_('profiles').remove([f"{session.user.id}.{pic.filename.split('.')[1]}"])
                        storage.from_('profiles').upload(f"{session.user.id}.{pic.filename.split('.')[1]}", os.path.abspath(path))
                    db.table('profiles').update({"profile_pic": f"{session.user.id}.{pic.filename.split('.')[1]}"}).eq("id", f'{session.user.id}').execute()
                os.remove(path)
                redirect('/user')
            else:
                return redirect('/user')
        else:
            return redirect('/login?redirect=/user')
    elif request.method == 'GET':
        return redirect('/user')
    else:
        return redirect('/user')
    
    return redirect('/user')
