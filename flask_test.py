from cgi import test

from flask import request
from main import app

def flask_is_started():
    res = app.test_client().get('/')
    assert res.status_code == 200