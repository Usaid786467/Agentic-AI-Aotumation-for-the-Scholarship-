"""
Universities Routes

Handles university-related operations:
- GET /search: Search universities
- GET /<id>: Get university details
- POST /discover: Trigger university discovery
- GET /<id>/professors: Get professors for a university
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, University, Professor
from services.scraper.university_scraper import university_scraper
from services.utils.logger import get_logger
from services.utils.helpers import paginate_query

logger = get_logger(__name__)

# Create blueprint
universities_bp = Blueprint('universities', __name__)


@universities_bp.route('/search', methods=['GET'])
@jwt_required()
def search_universities():
    """
    Search universities with filters

    Query params:
        country: Filter by country
        has_scholarship: Filter by scholarship availability (true/false)
        page: Page number (default: 1)
        per_page: Results per page (default: 20)

    Returns:
        200: List of universities
    """
    try:
        # Get query parameters
        country = request.args.get('country')
        has_scholarship = request.args.get('has_scholarship')
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 20))

        # Build query
        query = University.query

        # Apply filters
        if country:
            query = query.filter(University.country.ilike(f'%{country}%'))

        if has_scholarship is not None:
            has_scholarship_bool = has_scholarship.lower() == 'true'
            query = query.filter_by(has_scholarship=has_scholarship_bool)

        # Order by created_at descending
        query = query.order_by(University.created_at.desc())

        # Paginate
        result = paginate_query(query, page, per_page)

        # Convert to dict
        universities = [uni.to_dict() for uni in result['items']]

        return jsonify({
            'universities': universities,
            'total': result['total'],
            'page': result['page'],
            'per_page': result['per_page'],
            'total_pages': result['total_pages'],
            'has_next': result['has_next'],
            'has_prev': result['has_prev']
        }), 200

    except Exception as e:
        logger.error(f"University search error: {str(e)}")
        return jsonify({'error': 'Search failed'}), 500


@universities_bp.route('/<int:university_id>', methods=['GET'])
@jwt_required()
def get_university(university_id):
    """
    Get university details

    Returns:
        200: University details
        404: University not found
    """
    try:
        university = University.query.get(university_id)

        if not university:
            return jsonify({'error': 'University not found'}), 404

        return jsonify(university.to_dict()), 200

    except Exception as e:
        logger.error(f"Get university error: {str(e)}")
        return jsonify({'error': 'Failed to get university'}), 500


@universities_bp.route('/discover', methods=['POST'])
@jwt_required()
def discover_universities():
    """
    Trigger university discovery process
    Loads sample universities into database

    Request body:
        {
            "countries": ["USA", "UK", "China"] (optional)
        }

    Returns:
        200: Discovery started
    """
    try:
        # Get sample universities
        sample_universities = university_scraper.get_sample_universities()

        # Add to database
        added_count = 0
        for uni_data in sample_universities:
            # Check if university already exists
            existing = University.query.filter_by(
                name=uni_data['name']
            ).first()

            if not existing:
                university = University(
                    name=uni_data['name'],
                    country=uni_data['country'],
                    **uni_data
                )
                db.session.add(university)
                added_count += 1

        db.session.commit()

        logger.info(f"Discovered {added_count} new universities")

        return jsonify({
            'message': f'Discovered {added_count} new universities',
            'total': added_count
        }), 200

    except Exception as e:
        db.session.rollback()
        logger.error(f"University discovery error: {str(e)}")
        return jsonify({'error': 'Discovery failed'}), 500


@universities_bp.route('/<int:university_id>/professors', methods=['GET'])
@jwt_required()
def get_university_professors(university_id):
    """
    Get professors for a university

    Returns:
        200: List of professors
        404: University not found
    """
    try:
        university = University.query.get(university_id)

        if not university:
            return jsonify({'error': 'University not found'}), 404

        professors = Professor.query.filter_by(university_id=university_id).all()
        professors_list = [prof.to_dict() for prof in professors]

        return jsonify({
            'professors': professors_list,
            'count': len(professors_list)
        }), 200

    except Exception as e:
        logger.error(f"Get professors error: {str(e)}")
        return jsonify({'error': 'Failed to get professors'}), 500
