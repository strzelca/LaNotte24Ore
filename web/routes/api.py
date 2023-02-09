from . import register_blueprint
from supabase.client import create_client as database_client
from config import Config
from datetime import datetime
import json
from flask import make_response

@register_blueprint.route('/api/user')
def api_user():
    client = database_client(Config.DATABASE_URI, Config.DATABASE_KEY)
    user_session = client.auth.get_session()
    if user_session != None and user_session.user != None and user_session.user.last_sign_in_at != None and user_session.expires_at != None:
        data = {
            "id": user_session.user.id,
            "email": user_session.user.email,
            "last_signin": user_session.user.last_sign_in_at.strftime("%d/%m/%Y, %H:%M:%S"),
            "token": user_session.refresh_token,
            "expiries_in": datetime.fromtimestamp(float(user_session.expires_at)).strftime("%d/%m/%Y, %H:%M:%S")
        }
        resp = make_response(json.dumps(data), 200)
        resp.mimetype = "text/json"
        return resp
    else:
        return make_response("Morto", 401)

