from app import app

app.testing = True


def test_hello_world():
    response = app.test_client().get('/')
    assert response.status_code == 200
    assert response.data.decode('utf-8') == '<p>Hello, World!</p>'
