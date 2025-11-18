"""
University Tests

Tests for university-related endpoints
"""

import pytest
from app import create_app, db
from models import User, University


@pytest.fixture
def client():
    """Create test client"""
    app = create_app('testing')
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            # Create test user and get token
            user = User('test@example.com', 'password123', 'Test User')
            db.session.add(user)
            db.session.commit()

            response = client.post('/api/auth/login', json={
                'email': 'test@example.com',
                'password': 'password123'
            })
            token = response.get_json()['access_token']

            yield client, token
            db.drop_all()


def test_search_universities(client):
    """Test university search"""
    test_client, token = client

    response = test_client.get(
        '/api/universities/search',
        headers={'Authorization': f'Bearer {token}'}
    )
    assert response.status_code == 200
    data = response.get_json()
    assert 'universities' in data


def test_discover_universities(client):
    """Test university discovery"""
    test_client, token = client

    response = test_client.post(
        '/api/universities/discover',
        headers={'Authorization': f'Bearer {token}'}
    )
    assert response.status_code == 200
    data = response.get_json()
    assert 'total' in data


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
