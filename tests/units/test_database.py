from supabase.client import create_client
from config import Config

def test_database_connection():
    client = create_client(Config.DATABASE_URI, Config.DATABASE_KEY)
    assert client is not None