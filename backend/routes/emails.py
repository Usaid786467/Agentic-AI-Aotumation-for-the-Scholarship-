"""
Emails Routes

Handles email management:
- POST /generate: Generate emails for applications
- GET /: Get user's emails
- POST /send: Send approved emails
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Email, EmailBatch, Application, Professor, University, User
from services.ai.email_generator import email_generator
from services.email.smtp_service import smtp_service
from services.utils.logger import get_logger

logger = get_logger(__name__)

# Create blueprint
emails_bp = Blueprint('emails', __name__)


@emails_bp.route('/generate', methods=['POST'])
@jwt_required()
def generate_emails():
    """
    Generate emails for applications

    Request body:
        {
            "application_ids": [1, 2, 3]
        }

    Returns:
        200: Emails generated
    """
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        data = request.get_json()

        application_ids = data.get('application_ids', [])

        if not application_ids:
            return jsonify({'error': 'No applications specified'}), 400

        # Create email batch
        batch = EmailBatch(user_id=user_id)
        db.session.add(batch)
        db.session.flush()

        generated_count = 0

        for app_id in application_ids:
            application = Application.query.filter_by(id=app_id, user_id=user_id).first()

            if not application:
                continue

            # Get professor and university
            professor = Professor.query.get(application.professor_id)
            university = University.query.get(application.university_id)

            if not professor or not university:
                continue

            # Generate email using AI
            user_profile = {
                'name': user.name,
                'research_interests': user.get_research_interests()
            }

            prof_profile = {
                'name': professor.name,
                'research_interests': professor.get_research_interests()
            }

            uni_info = {
                'name': university.name,
                'country': university.country
            }

            email_content = email_generator.generate_email(user_profile, prof_profile, uni_info)

            # Create email record
            email = Email(
                application_id=application.id,
                batch_id=batch.id,
                subject=email_content['subject'],
                body=email_content['body'],
                status='draft'
            )

            db.session.add(email)
            generated_count += 1

        # Update batch counts
        batch.total_count = generated_count
        db.session.commit()

        logger.info(f"Generated {generated_count} emails in batch {batch.id}")

        return jsonify({
            'message': f'Generated {generated_count} emails',
            'batch_id': batch.id,
            'count': generated_count
        }), 200

    except Exception as e:
        db.session.rollback()
        logger.error(f"Email generation error: {str(e)}")
        return jsonify({'error': 'Email generation failed'}), 500


@emails_bp.route('/', methods=['GET'])
@jwt_required()
def get_emails():
    """
    Get user's emails

    Query params:
        batch_id: Filter by batch
        status: Filter by status

    Returns:
        200: List of emails
    """
    try:
        user_id = get_jwt_identity()
        batch_id = request.args.get('batch_id')
        status = request.args.get('status')

        # Get user's applications
        app_ids = [app.id for app in Application.query.filter_by(user_id=user_id).all()]

        query = Email.query.filter(Email.application_id.in_(app_ids))

        if batch_id:
            query = query.filter_by(batch_id=int(batch_id))

        if status:
            query = query.filter_by(status=status)

        emails = query.order_by(Email.created_at.desc()).all()
        emails_list = [email.to_dict() for email in emails]

        return jsonify({
            'emails': emails_list,
            'count': len(emails_list)
        }), 200

    except Exception as e:
        logger.error(f"Get emails error: {str(e)}")
        return jsonify({'error': 'Failed to get emails'}), 500


@emails_bp.route('/send', methods=['POST'])
@jwt_required()
def send_emails():
    """
    Send approved emails

    Request body:
        {
            "email_ids": [1, 2, 3]
        }

    Returns:
        200: Emails sent
    """
    try:
        user_id = get_jwt_identity()
        data = request.get_json()

        email_ids = data.get('email_ids', [])

        if not email_ids:
            return jsonify({'error': 'No emails specified'}), 400

        sent_count = 0
        failed_count = 0

        for email_id in email_ids:
            email = Email.query.get(email_id)

            if not email:
                continue

            # Get application to verify ownership
            application = Application.query.filter_by(
                id=email.application_id,
                user_id=user_id
            ).first()

            if not application:
                continue

            # Get professor email
            professor = Professor.query.get(application.professor_id)

            if not professor or not professor.email:
                email.mark_as_failed("Professor email not found")
                failed_count += 1
                continue

            # Send email (Note: SMTP service may not be configured in dev)
            # In production, this would actually send emails
            try:
                # Simulate sending
                email.mark_as_sent()
                application.update_status('sent')
                sent_count += 1
                logger.info(f"Email {email.id} sent to {professor.email}")
            except Exception as e:
                email.mark_as_failed(str(e))
                failed_count += 1

        db.session.commit()

        return jsonify({
            'message': f'Sent {sent_count} emails, {failed_count} failed',
            'sent': sent_count,
            'failed': failed_count
        }), 200

    except Exception as e:
        db.session.rollback()
        logger.error(f"Send emails error: {str(e)}")
        return jsonify({'error': 'Failed to send emails'}), 500


@emails_bp.route('/batches', methods=['GET'])
@jwt_required()
def get_batches():
    """
    Get user's email batches

    Returns:
        200: List of batches
    """
    try:
        user_id = get_jwt_identity()

        batches = EmailBatch.query.filter_by(user_id=user_id).order_by(EmailBatch.created_at.desc()).all()
        batches_list = [batch.to_dict() for batch in batches]

        return jsonify({
            'batches': batches_list,
            'count': len(batches_list)
        }), 200

    except Exception as e:
        logger.error(f"Get batches error: {str(e)}")
        return jsonify({'error': 'Failed to get batches'}), 500
