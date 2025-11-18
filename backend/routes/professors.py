"""
Professors Routes

Handles professor-related operations:
- GET /search: Search professors
- GET /<id>: Get professor details
- POST /discover: Discover professors for universities
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Professor, University, User
from services.scraper.professor_scraper import professor_scraper
from services.ai.matching_engine import matching_engine
from services.utils.logger import get_logger
from services.utils.helpers import paginate_query

logger = get_logger(__name__)

# Create blueprint
professors_bp = Blueprint('professors', __name__)


@professors_bp.route('/search', methods=['GET'])
@jwt_required()
def search_professors():
    """
    Search professors with filters and matching

    Query params:
        university_id: Filter by university
        match_threshold: Minimum match score (0-100)
        page: Page number
        per_page: Results per page

    Returns:
        200: List of professors with match scores
    """
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)

        # Get query parameters
        university_id = request.args.get('university_id')
        match_threshold = float(request.args.get('match_threshold', 0))
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 20))

        # Build query
        query = Professor.query

        # Apply filters
        if university_id:
            query = query.filter_by(university_id=int(university_id))

        # Get all professors
        all_professors = query.all()

        # Calculate match scores if user has research interests
        user_interests = user.get_research_interests() if user else []

        if user_interests:
            ranked_professors = matching_engine.rank_professors(
                user_interests,
                [prof.to_dict(include_university=True) for prof in all_professors]
            )

            # Filter by match threshold
            if match_threshold > 0:
                ranked_professors = [
                    prof for prof in ranked_professors
                    if prof.get('match_score', 0) >= match_threshold
                ]
        else:
            ranked_professors = [prof.to_dict(include_university=True) for prof in all_professors]

        # Manual pagination
        total = len(ranked_professors)
        start = (page - 1) * per_page
        end = start + per_page
        professors_page = ranked_professors[start:end]

        total_pages = (total + per_page - 1) // per_page

        return jsonify({
            'professors': professors_page,
            'total': total,
            'page': page,
            'per_page': per_page,
            'total_pages': total_pages,
            'has_next': page < total_pages,
            'has_prev': page > 1
        }), 200

    except Exception as e:
        logger.error(f"Professor search error: {str(e)}")
        return jsonify({'error': 'Search failed'}), 500


@professors_bp.route('/<int:professor_id>', methods=['GET'])
@jwt_required()
def get_professor(professor_id):
    """
    Get professor details

    Returns:
        200: Professor details
        404: Professor not found
    """
    try:
        professor = Professor.query.get(professor_id)

        if not professor:
            return jsonify({'error': 'Professor not found'}), 404

        return jsonify(professor.to_dict(include_university=True)), 200

    except Exception as e:
        logger.error(f"Get professor error: {str(e)}")
        return jsonify({'error': 'Failed to get professor'}), 500


@professors_bp.route('/discover', methods=['POST'])
@jwt_required()
def discover_professors():
    """
    Discover professors for universities

    Request body:
        {
            "university_id": 1 (optional)
        }

    Returns:
        200: Discovery completed
    """
    try:
        data = request.get_json() or {}
        university_id = data.get('university_id')

        added_count = 0

        if university_id:
            # Discover for specific university
            universities = [University.query.get(university_id)]
        else:
            # Discover for all universities
            universities = University.query.limit(10).all()

        for university in universities:
            if not university:
                continue

            # Get sample professors
            professors_data = professor_scraper.get_sample_professors(university.id)

            for prof_data in professors_data:
                # Check if professor already exists
                existing = Professor.query.filter_by(
                    email=prof_data.get('email'),
                    university_id=university.id
                ).first()

                if not existing:
                    professor = Professor(
                        name=prof_data['name'],
                        university_id=university.id,
                        **prof_data
                    )
                    db.session.add(professor)
                    added_count += 1

        db.session.commit()

        logger.info(f"Discovered {added_count} new professors")

        return jsonify({
            'message': f'Discovered {added_count} new professors',
            'total': added_count
        }), 200

    except Exception as e:
        db.session.rollback()
        logger.error(f"Professor discovery error: {str(e)}")
        return jsonify({'error': 'Discovery failed'}), 500
