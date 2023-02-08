from supabase.client import create_client as database_client
from storage3 import create_client as storage_client
from web import graphql_query
from gotrue import errors
from config import Config
import json

def test_database_connection():
    client = database_client(Config.DATABASE_URI, Config.DATABASE_KEY)
    assert client is not None

def test_authentication_database_connection():
    client = database_client(Config.DATABASE_URI, Config.DATABASE_KEY)
    try:
        user_session = client.auth.sign_in_with_password(
            credentials={
                "email": Config.AUTH_TEST_USER,
                "password": Config.AUTH_TEST_PASSWORD
            }
        )
    except errors.AuthInvalidCredentialsError as e:
        assert None
    assert user_session is not None
    client.auth.sign_out()

def test_graphql_endpoint():
    query = graphql_query('profiles')
    data = json.loads(query.text)
    for user in data['data']['profilesCollection']['edges']:
        print(json.dumps(user['node'], indent=4))
    assert query.status_code == 200

def test_graphql_user_endpoint():
    client = database_client(Config.DATABASE_URI, Config.DATABASE_KEY)
    try:
        user_session = client.auth.sign_in_with_password(
            credentials={
                "email": Config.AUTH_TEST_USER,
                "password": Config.AUTH_TEST_PASSWORD
            }
        )
    except errors.AuthInvalidCredentialsError as e:
        assert None
    if user_session.user != None:
        args = str("filter: { id: { eq:" + user_session.user.id + " } }")
        query = graphql_query('profiles', args)
        data = json.loads(query.text)
    
        for user in data['data']['profilesCollection']['edges']:
            print(json.dumps(user['node'], indent=4))
        assert query.status_code == 200
    client.auth.sign_out()

def test_storage_connection():
    client = storage_client(
        f"https://{Config.DATABASE_URI}/storage/v1",
        {
            "apiKey": Config.DATABASE_KEY,
            "Authorization": f"Bearer {Config.DATABASE_KEY}"
        },
        is_async=False
    )
    assert client is not None