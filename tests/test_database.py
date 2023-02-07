from supabase.client import create_client as database_client
from storage3 import create_client as storage_client
from gotrue import errors
from config import Config

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