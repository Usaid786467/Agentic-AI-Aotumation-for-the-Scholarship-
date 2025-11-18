"""
Authentication Routes

Handles user authentication:
- POST /register: User registration
- POST /login: User login
- POST /logout: User logout
- POST /refresh: Refresh access token
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity
)
from models import db, User
from services.utils.validators import validate_email, validate_required_fields
from services.utils.logger import get_logger
from datetime import datetime

logger = get_logger(__name__)

# Create blueprint
auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['POST'])
def register():
    """
    Register a new user

    Request body:
        {
            "email": "user@example.com",
            "password": "password123",
            "name": "John Doe"
        }

    Returns:
        201: User created successfully
        400: Validation error
        409: Email already exists
    """
    try:
        data = request.get_json()

        # Validate required fields
        is_valid, missing = validate_required_fields(data, ['email', 'password', 'name'])
        if not is_valid:
            return jsonify({'error': f'Missing required fields: {", ".join(missing)}'}), 400

        email = data['email'].lower().strip()
        password = data['password']
        name = data['name'].strip()

        # Validate email format
        if not validate_email(email):
            return jsonify({'error': 'Invalid email format'}), 400

        # Check if user already exists
        if User.query.filter_by(email=email).first():
            return jsonify({'error': 'Email already registered'}), 409

        # Create new user
        user = User(email=email, password=password, name=name)
        db.session.add(user)
        db.session.commit()

        logger.info(f"New user registered: {email}")

        # Create tokens
        access_token = create_access_token(identity=user.id)
        refresh_token = create_refresh_token(identity=user.id)

        return jsonify({
            'message': 'User registered successfully',
            'user': user.to_dict(),
            'access_token': access_token,
            'refresh_token': refresh_token
        }), 201

    except Exception as e:
        db.session.rollback()
        logger.error(f"Registration error: {str(e)}")
        return jsonify({'error': 'Registration failed'}), 500


@auth_bp.route('/login', methods=['POST'])
def login():
    """
    User login

    Request body:
        {
            "email": "user@example.com",
            "password": "password123"
        }

    Returns:
        200: Login successful
        400: Validation error
        401: Invalid credentials
    """
    try:
        data = request.get_json()

        # Validate required fields
        is_valid, missing = validate_required_fields(data, ['email', 'password'])
        if not is_valid:
            return jsonify({'error': f'Missing required fields: {", ".join(missing)}'}), 400

        email = data['email'].lower().strip()
        password = data['password']

        # Find user
        user = User.query.filter_by(email=email).first()

        if not user or not user.check_password(password):
            return jsonify({'error': 'Invalid email or password'}), 401

        if not user.is_active:
            return jsonify({'error': 'Account is deactivated'}), 401

        # Update last login
        user.last_login = datetime.utcnow()
        db.session.commit()

        # Create tokens
        access_token = create_access_token(identity=user.id)
        refresh_token = create_refresh_token(identity=user.id)

        logger.info(f"User logged in: {email}")

        return jsonify({
            'message': 'Login successful',
            'user': user.to_dict(),
            'access_token': access_token,
            'refresh_token': refresh_token
        }), 200

    except Exception as e:
        logger.error(f"Login error: {str(e)}")
        return jsonify({'error': 'Login failed'}), 500


@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    """
    Refresh access token

    Returns:
        200: New access token
        401: Invalid refresh token
    """
    try:
        user_id = get_jwt_identity()
        access_token = create_access_token(identity=user_id)

        return jsonify({
            'access_token': access_token
        }), 200

    except Exception as e:
        logger.error(f"Token refresh error: {str(e)}")
        return jsonify({'error': 'Token refresh failed'}), 500


@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    """
    User logout
    Note: With JWT, logout is typically handled client-side by removing the token

    Returns:
        200: Logout successful
    """
    return jsonify({'message': 'Logout successful'}), 200
