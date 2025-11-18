"""
User Routes

Handles user profile management:
- GET /profile: Get user profile
- PUT /profile: Update user profile
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, User
from services.utils.logger import get_logger

logger = get_logger(__name__)

# Create blueprint
user_bp = Blueprint('user', __name__)


@user_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    """
    Get user profile

    Returns:
        200: User profile
    """
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)

        if not user:
            return jsonify({'error': 'User not found'}), 404

        return jsonify(user.to_dict()), 200

    except Exception as e:
        logger.error(f"Get profile error: {str(e)}")
        return jsonify({'error': 'Failed to get profile'}), 500


@user_bp.route('/profile', methods=['PUT'])
@jwt_required()
def update_profile():
    """
    Update user profile

    Request body:
        {
            "name": "John Doe",
            "research_interests": ["Machine Learning", "Robotics"],
            "target_countries": ["USA", "UK"],
            "preferences": {"key": "value"}
        }

    Returns:
        200: Profile updated
    """
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)

        if not user:
            return jsonify({'error': 'User not found'}), 404

        data = request.get_json()

        # Update fields
        if 'name' in data:
            user.name = data['name']

        if 'research_interests' in data:
            user.set_research_interests(data['research_interests'])

        if 'target_countries' in data:
            user.set_target_countries(data['target_countries'])

        if 'preferences' in data:
            user.set_preferences(data['preferences'])

        db.session.commit()

        logger.info(f"Profile updated for user {user_id}")

        return jsonify({
            'message': 'Profile updated successfully',
            'user': user.to_dict()
        }), 200

    except Exception as e:
        db.session.rollback()
        logger.error(f"Update profile error: {str(e)}")
        return jsonify({'error': 'Failed to update profile'}), 500
