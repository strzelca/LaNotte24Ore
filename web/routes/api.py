from . import register_blueprint
from supabase.client import create_client as database_client
from config import Config
from datetime import datetime
import json
from flask import make_response
from web import *

@register_blueprint.route('/api/user')
def api_user():
    client = database_client(Config.DATABASE_URI, Config.DATABASE_KEY)
    user_session = client.auth.get_session()
    if user_session != None and user_session.user != None and user_session.user.last_sign_in_at != None and user_session.expires_at != None:
        query = client.table('profiles').select('name, surname, country, lang').eq('id', f'{user_session.user.id}').execute()
        user_data = query.data[0]
        data = {
            "id": user_session.user.id,
            "name":user_data['name'],
            "surname":user_data['surname'],
            "email": user_session.user.email,
            "country":user_data['country'],
            "language":user_data['lang'],
            "last_signin": user_session.user.last_sign_in_at.strftime("%d/%m/%Y, %H:%M:%S"),
            "token": user_session.refresh_token,
            "expiries_in": datetime.fromtimestamp(float(user_session.expires_at)).strftime("%d/%m/%Y, %H:%M:%S"),
        }

        resp = make_response(json.dumps(data), 200)
        resp.mimetype = "text/json"
        return resp
    else:
        return make_response("Morto", 401)

