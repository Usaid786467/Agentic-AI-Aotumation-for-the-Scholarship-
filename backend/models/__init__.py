"""
Database Models Package

This package contains all SQLAlchemy database models for the PhD Application Automator:
- User: User authentication and profile
- University: University information
- Professor: Professor profiles
- Application: Application tracking
- Email: Email records
- EmailBatch: Email batch management
- Analytics: Analytics and metrics
- ScrapingJob: Scraping job tracking
"""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Initialize SQLAlchemy
db = SQLAlchemy()

# Import all models for easy access
from .user import User
from .university import University
from .professor import Professor
from .application import Application
from .email import Email, EmailBatch
from .analytics import Analytics
from .scraping_job import ScrapingJob

__all__ = [
    'db',
    'User',
    'University',
    'Professor',
    'Application',
    'Email',
    'EmailBatch',
    'Analytics',
    'ScrapingJob'
]
