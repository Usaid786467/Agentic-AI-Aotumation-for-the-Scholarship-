"""
Applications Routes

Handles PhD application tracking:
- GET /: Get user's applications
- GET /<id>: Get application details
- POST /: Create new application
- PUT /<id>: Update application
- DELETE /<id>: Delete application
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Application, Professor, University
from services.utils.logger import get_logger
from datetime import datetime

logger = get_logger(__name__)

# Create blueprint
applications_bp = Blueprint('applications', __name__)


@applications_bp.route('/', methods=['GET'])
@jwt_required()
def get_applications():
    """
    Get user's applications

    Query params:
        status: Filter by status

    Returns:
        200: List of applications
    """
    try:
        user_id = get_jwt_identity()
        status = request.args.get('status')

        query = Application.query.filter_by(user_id=user_id)

        if status:
            query = query.filter_by(status=status)

        applications = query.order_by(Application.created_at.desc()).all()
        applications_list = [app.to_dict(include_relations=True) for app in applications]

        return jsonify({
            'applications': applications_list,
            'count': len(applications_list)
        }), 200

    except Exception as e:
        logger.error(f"Get applications error: {str(e)}")
        return jsonify({'error': 'Failed to get applications'}), 500


@applications_bp.route('/<int:application_id>', methods=['GET'])
@jwt_required()
def get_application(application_id):
    """
    Get application details

    Returns:
        200: Application details
        404: Application not found
    """
    try:
        user_id = get_jwt_identity()
        application = Application.query.filter_by(id=application_id, user_id=user_id).first()

        if not application:
            return jsonify({'error': 'Application not found'}), 404

        return jsonify(application.to_dict(include_relations=True)), 200

    except Exception as e:
        logger.error(f"Get application error: {str(e)}")
        return jsonify({'error': 'Failed to get application'}), 500


@applications_bp.route('/', methods=['POST'])
@jwt_required()
def create_application():
    """
    Create new application

    Request body:
        {
            "professor_id": 1,
            "university_id": 1,
            "match_score": 85.5,
            "notes": "Optional notes"
        }

    Returns:
        201: Application created
    """
    try:
        user_id = get_jwt_identity()
        data = request.get_json()

        professor_id = data.get('professor_id')
        university_id = data.get('university_id')

        if not professor_id or not university_id:
            return jsonify({'error': 'Professor and university required'}), 400

        # Create application
        application = Application(
            user_id=user_id,
            professor_id=professor_id,
            university_id=university_id,
            match_score=data.get('match_score'),
            notes=data.get('notes')
        )

        db.session.add(application)
        db.session.commit()

        logger.info(f"Application created: {application.id}")

        return jsonify({
            'message': 'Application created',
            'application': application.to_dict(include_relations=True)
        }), 201

    except Exception as e:
        db.session.rollback()
        logger.error(f"Create application error: {str(e)}")
        return jsonify({'error': 'Failed to create application'}), 500


@applications_bp.route('/<int:application_id>', methods=['PUT'])
@jwt_required()
def update_application(application_id):
    """
    Update application

    Request body:
        {
            "status": "sent",
            "notes": "Updated notes"
        }

    Returns:
        200: Application updated
    """
    try:
        user_id = get_jwt_identity()
        application = Application.query.filter_by(id=application_id, user_id=user_id).first()

        if not application:
            return jsonify({'error': 'Application not found'}), 404

        data = request.get_json()

        # Update fields
        if 'status' in data:
            application.update_status(data['status'])
        if 'notes' in data:
            application.notes = data['notes']
        if 'response_content' in data:
            application.response_content = data['response_content']

        db.session.commit()

        return jsonify({
            'message': 'Application updated',
            'application': application.to_dict(include_relations=True)
        }), 200

    except Exception as e:
        db.session.rollback()
        logger.error(f"Update application error: {str(e)}")
        return jsonify({'error': 'Failed to update application'}), 500
