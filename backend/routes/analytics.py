"""
Analytics Routes

Handles analytics and statistics:
- GET /dashboard: Get dashboard statistics
- GET /success-rate: Get success rate metrics
"""

from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Application, Email, University, Professor
from sqlalchemy import func
from services.utils.logger import get_logger

logger = get_logger(__name__)

# Create blueprint
analytics_bp = Blueprint('analytics', __name__)


@analytics_bp.route('/dashboard', methods=['GET'])
@jwt_required()
def get_dashboard():
    """
    Get dashboard statistics

    Returns:
        200: Dashboard statistics
    """
    try:
        user_id = get_jwt_identity()

        # Count applications by status
        total_applications = Application.query.filter_by(user_id=user_id).count()
        sent_applications = Application.query.filter_by(user_id=user_id, status='sent').count()
        replied_applications = Application.query.filter_by(user_id=user_id, status='replied').count()

        # Count emails
        app_ids = [app.id for app in Application.query.filter_by(user_id=user_id).all()]
        total_emails = Email.query.filter(Email.application_id.in_(app_ids)).count()
        sent_emails = Email.query.filter(Email.application_id.in_(app_ids), Email.status == 'sent').count()

        # Calculate success rate
        success_rate = (replied_applications / sent_applications * 100) if sent_applications > 0 else 0

        # Count universities and professors
        universities_count = University.query.count()
        professors_count = Professor.query.count()

        return jsonify({
            'applications': {
                'total': total_applications,
                'sent': sent_applications,
                'replied': replied_applications
            },
            'emails': {
                'total': total_emails,
                'sent': sent_emails
            },
            'success_rate': round(success_rate, 2),
            'opportunities': {
                'universities': universities_count,
                'professors': professors_count
            }
        }), 200

    except Exception as e:
        logger.error(f"Dashboard analytics error: {str(e)}")
        return jsonify({'error': 'Failed to get analytics'}), 500


@analytics_bp.route('/by-country', methods=['GET'])
@jwt_required()
def get_by_country():
    """
    Get applications by country

    Returns:
        200: Applications grouped by country
    """
    try:
        user_id = get_jwt_identity()

        # Get applications with university info
        results = db.session.query(
            University.country,
            func.count(Application.id).label('count')
        ).join(
            Application, University.id == Application.university_id
        ).filter(
            Application.user_id == user_id
        ).group_by(
            University.country
        ).all()

        by_country = [{'country': row[0], 'count': row[1]} for row in results]

        return jsonify({
            'by_country': by_country
        }), 200

    except Exception as e:
        logger.error(f"By country analytics error: {str(e)}")
        return jsonify({'error': 'Failed to get analytics'}), 500
