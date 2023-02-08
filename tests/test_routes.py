from web import *

def test_index():
    app = create_app('lanotte24ore.test')
    @app.template_filter()
    def format_datetime(value):
        return datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ").strftime("%d %B %Y")
    client = app.test_client()
    response = client.get('/')
    assert response.status_code == 200

def test_login_get():
    app = create_app('lanotte24ore.test')
    client = app.test_client()
    response = client.get('/login')
    assert response.status_code == 200

def test_login_post():
    app = create_app('lanotte24ore.test')
    client = app.test_client()
    response = client.post('/login', json={
        "email": Config.AUTH_TEST_USER,
        "password": Config.AUTH_TEST_PASSWORD
    })
    assert response.status_code == 200

def test_logout():
    app = create_app('lanotte24ore.test')
    client = app.test_client()
    response = client.get('/logout')
    assert response.status_code == 200

