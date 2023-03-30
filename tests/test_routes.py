from web import *

def test_signup():
    app = create_app('lanotte24ore.test')
    client = app.test_client()
    response = client.get('/signup')
    assert response.status_code == 200

def test_about():
    app = create_app('lanotte24ore.test')
    client = app.test_client()
    response = client.get('/about')
    assert response.status_code == 200

def test_login_get():
    app = create_app('lanotte24ore.test')
    client = app.test_client()
    response = client.get('/login')
    assert response.status_code == 200

def test_login_post():
    app = create_app('lanotte24ore.test')
    client = app.test_client()
    response = client.post('/login', data={
        'email': Config.AUTH_TEST_USER,
        'password': Config.AUTH_TEST_PASSWORD
    })
    assert response.status_code == 302

def test_logout():
    app = create_app('lanotte24ore.test')
    client = app.test_client()
    response = client.get('/logout')
    assert response.status_code == 302
