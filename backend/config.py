"""
Configuration Management for PhD Application Automator

This module handles all application configuration including:
- Database settings
- API keys (Gemini AI, SendGrid, etc.)
- Email configuration
- Scraping settings
- Security settings
"""

import os
from datetime import timedelta
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Base configuration class with common settings"""

    # Flask Configuration
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'

    # Database Configuration
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///phd_applications.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False  # Set to True for SQL query debugging

    # JWT Configuration
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'jwt-secret-key-change-this')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(seconds=int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES', '3600')))
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(seconds=int(os.getenv('JWT_REFRESH_TOKEN_EXPIRES', '2592000')))

    # Gemini AI Configuration
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', '')

    # Email Configuration
    MAIL_SERVER = os.getenv('SMTP_HOST', 'smtp.gmail.com')
    MAIL_PORT = int(os.getenv('SMTP_PORT', '587'))
    MAIL_USE_TLS = os.getenv('SMTP_USE_TLS', 'True').lower() == 'true'
    MAIL_USERNAME = os.getenv('SMTP_USERNAME', '')
    MAIL_PASSWORD = os.getenv('SMTP_PASSWORD', '')
    MAIL_DEFAULT_SENDER = os.getenv('EMAIL_FROM', '')

    # SendGrid (alternative email provider)
    SENDGRID_API_KEY = os.getenv('SENDGRID_API_KEY', '')

    # Redis Configuration (for Celery)
    REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')

    # Celery Configuration
    CELERY_BROKER_URL = REDIS_URL
    CELERY_RESULT_BACKEND = REDIS_URL

    # Web Scraping Configuration
    USER_AGENT = os.getenv('USER_AGENT', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
    SCRAPING_DELAY = float(os.getenv('SCRAPING_DELAY', '2'))
    MAX_RETRIES = int(os.getenv('MAX_RETRIES', '3'))
    REQUEST_TIMEOUT = int(os.getenv('REQUEST_TIMEOUT', '30'))

    # Email Sending Limits
    DAILY_EMAIL_LIMIT = int(os.getenv('DAILY_EMAIL_LIMIT', '10000'))
    HOURLY_EMAIL_LIMIT = int(os.getenv('HOURLY_EMAIL_LIMIT', '500'))
    BATCH_SIZE = int(os.getenv('BATCH_SIZE', '50'))

    # Logging Configuration
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE = os.getenv('LOG_FILE', 'logs/app.log')

    # CORS Configuration
    CORS_ORIGINS = os.getenv('FRONTEND_URL', 'http://localhost:3000').split(',')

    # Upload Configuration
    MAX_CONTENT_LENGTH = int(os.getenv('MAX_UPLOAD_SIZE', '5242880'))  # 5MB default
    UPLOAD_FOLDER = 'uploads'
    ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx'}

    # Pagination
    RESULTS_PER_PAGE = int(os.getenv('RESULTS_PER_PAGE', '20'))

    @staticmethod
    def init_app(app):
        """Initialize application with this configuration"""
        # Create necessary directories
        os.makedirs('logs', exist_ok=True)
        os.makedirs('uploads', exist_ok=True)
        os.makedirs('data', exist_ok=True)


class DevelopmentConfig(Config):
    """Development environment configuration"""
    DEBUG = True
    SQLALCHEMY_ECHO = True  # Show SQL queries in development


class ProductionConfig(Config):
    """Production environment configuration"""
    DEBUG = False
    # Use PostgreSQL in production
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', '').replace('postgres://', 'postgresql://')

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)

        # Log to syslog in production
        import logging
        from logging.handlers import SysLogHandler
        syslog_handler = SysLogHandler()
        syslog_handler.setLevel(logging.WARNING)
        app.logger.addHandler(syslog_handler)


class TestingConfig(Config):
    """Testing environment configuration"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'  # In-memory database for tests
    WTF_CSRF_ENABLED = False


# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}


def get_config():
    """Get configuration based on FLASK_ENV environment variable"""
    env = os.getenv('FLASK_ENV', 'development')
    return config.get(env, config['default'])
