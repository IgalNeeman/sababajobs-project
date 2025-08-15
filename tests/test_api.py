import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_api_apply_success(client):
    payload = {'name': 'Guy', 'email': 'guy@example.com', 'phone': '0501234567', 'position': 'Software Engineer', 'accept': True}
    res = client.post('/api/apply', json=payload)
    assert res.status_code == 200
    assert res.json['ok'] is True

def test_api_apply_missing(client):
    payload = {'name': 'x'}
    res = client.post('/api/apply', json=payload)
    assert res.status_code == 400
    assert 'missing' in res.json