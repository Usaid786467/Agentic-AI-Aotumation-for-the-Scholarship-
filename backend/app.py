"""
PhD Application Automator - Main Application

Flask application with REST API for PhD application management
"""

from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate

# Import configuration
from config import get_config

# Import database
from models import db

# Import routes
from routes import (
    auth_bp,
    universities_bp,
    professors_bp,
    applications_bp,
    emails_bp,
    analytics_bp,
    user_bp
)

# Import utilities
from services.utils.logger import setup_logger

# Initialize logger
logger = setup_logger('phd_automator', log_file='logs/app.log')


def create_app(config_name='development'):
    """
    Create and configure Flask application

    Args:
        config_name: Configuration name (development, production, testing)

    Returns:
        Flask application instance
    """
    app = Flask(__name__)

    # Load configuration
    config = get_config()
    app.config.from_object(config)

    # Initialize app with config
    config.init_app(app)

    # Initialize extensions
    db.init_app(app)
    migrate = Migrate(app, db)
    jwt = JWTManager(app)

    # Enable CORS
    CORS(app, resources={
        r"/api/*": {
            "origins": app.config['CORS_ORIGINS'],
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"]
        }
    })

    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(universities_bp, url_prefix='/api/universities')
    app.register_blueprint(professors_bp, url_prefix='/api/professors')
    app.register_blueprint(applications_bp, url_prefix='/api/applications')
    app.register_blueprint(emails_bp, url_prefix='/api/emails')
    app.register_blueprint(analytics_bp, url_prefix='/api/analytics')
    app.register_blueprint(user_bp, url_prefix='/api/user')

    # Health check endpoint
    @app.route('/api/health')
    def health_check():
        """Health check endpoint"""
        return jsonify({
            'status': 'healthy',
            'message': 'PhD Application Automator API is running'
        }), 200

    # Root endpoint
    @app.route('/')
    def index():
        """Root endpoint"""
        return jsonify({
            'message': 'PhD Application Automator API',
            'version': '1.0.0',
            'endpoints': {
                'health': '/api/health',
                'auth': '/api/auth',
                'universities': '/api/universities',
                'professors': '/api/professors',
                'applications': '/api/applications',
                'emails': '/api/emails',
                'analytics': '/api/analytics',
                'user': '/api/user'
            }
        }), 200

    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Not found'}), 404

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        logger.error(f"Internal server error: {str(error)}")
        return jsonify({'error': 'Internal server error'}), 500

    # JWT error handlers
    @jwt.unauthorized_loader
    def unauthorized_callback(callback):
        return jsonify({'error': 'Missing authorization token'}), 401

    @jwt.invalid_token_loader
    def invalid_token_callback(callback):
        return jsonify({'error': 'Invalid token'}), 401

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return jsonify({'error': 'Token has expired'}), 401

    logger.info("Application initialized successfully")

    return app


# Create application instance
app = create_app()


if __name__ == '__main__':
    # Create database tables
    with app.app_context():
        db.create_all()
        logger.info("Database tables created")

    # Run application
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )
