import pytest
from app import create_app, db
from app.models import User, Group
import json
import base64
from os import environ as env
from urllib.parse import quote_plus, urlencode

@pytest.fixture
def app():
    app = create_app({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'AUTH0_CLIENT_ID': 'test-client-id',
        'AUTH0_CLIENT_SECRET': 'test-client-secret',
        'AUTH0_DOMAIN': 'test.auth0.com',
        'APP_SECRET_KEY': 'test-secret-key'
    })
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

def test_home_page(client):
    response = client.get('/')
    assert response.status_code == 200

def test_login(client):
    response = client.get('/login')
    assert response.status_code == 302  # Redirect to Auth0
    assert 'auth0.com' in response.location

def test_callback(client):
    # Mock successful Auth0 callback
    with client.session_transaction() as session:
        session['user'] = {
            'access_token': 'test_token',
            'id_token': 'test_id_token',
            'userinfo': {
                'sub': '123',
                'name': 'Test User',
                'email': 'test@example.com'
            }
        }
    
    response = client.get('/callback')
    assert response.status_code == 302  # Redirect to home
    assert response.location == '/'

def test_logout(client):
    response = client.get('/logout')
    assert response.status_code == 302  # Redirect to Auth0 logout
    
    # Verify Auth0 logout URL parameters
    assert 'v2/logout' in response.location
    assert 'returnTo' in response.location
    assert 'client_id' in response.location

def test_protected_route_without_auth(client):
    # Test accessing protected route without authentication
    with client.session_transaction() as session:
        if 'user' in session:
            del session['user']
            
    response = client.get('/protected')
    assert response.status_code == 401  # Unauthorized

def test_protected_route_with_auth(client):
    # Test accessing protected route with authentication
    with client.session_transaction() as session:
        session['user'] = {
            'access_token': 'test_token',
            'id_token': 'test_id_token',
            'userinfo': {
                'sub': '123',
                'name': 'Test User',
                'email': 'test@example.com'
            }
        }
    
    response = client.get('/protected')
    assert response.status_code == 200

def test_callback_error(client):
    # Test callback with error
    response = client.get('/callback')
    assert response.status_code == 302  # Redirect to login
    assert response.location == '/login'

def test_session_persistence(client):
    # Test that user session persists after login
    with client.session_transaction() as session:
        session['user'] = {
            'access_token': 'test_token',
            'id_token': 'test_id_token',
            'userinfo': {
                'sub': '123',
                'name': 'Test User',
                'email': 'test@example.com'
            }
        }
    
    response = client.get('/')
    assert response.status_code == 200
    assert b'Test User' in response.data

def test_session_cleared_after_logout(client):
    # Test that session is cleared after logout
    with client.session_transaction() as session:
        session['user'] = {
            'access_token': 'test_token'
        }
    
    client.get('/logout')
    
    with client.session_transaction() as session:
        assert 'user' not in session