"""
Authentication Tests

Tests for user authentication endpoints
"""

import pytest
from app import create_app, db
from models import User


@pytest.fixture
def client():
    """Create test client"""
    app = create_app('testing')
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.drop_all()


def test_register(client):
    """Test user registration"""
    response = client.post('/api/auth/register', json={
        'name': 'Test User',
        'email': 'test@example.com',
        'password': 'password123'
    })
    assert response.status_code == 201
    data = response.get_json()
    assert 'access_token' in data
    assert data['user']['email'] == 'test@example.com'


def test_login(client):
    """Test user login"""
    # First register a user
    client.post('/api/auth/register', json={
        'name': 'Test User',
        'email': 'test@example.com',
        'password': 'password123'
    })

    # Then login
    response = client.post('/api/auth/login', json={
        'email': 'test@example.com',
        'password': 'password123'
    })
    assert response.status_code == 200
    data = response.get_json()
    assert 'access_token' in data


def test_invalid_login(client):
    """Test login with invalid credentials"""
    response = client.post('/api/auth/login', json={
        'email': 'nonexistent@example.com',
        'password': 'wrongpassword'
    })
    assert response.status_code == 401


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
