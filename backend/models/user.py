"""
User Model

Handles user authentication and profile information including:
- User credentials (email, password)
- Research interests
- Target countries
- Preferences
- CV path
"""

from . import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import json


class User(db.Model):
    """User model for authentication and profile management"""

    __tablename__ = 'users'

    # Primary Fields
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(100), nullable=False)

    # Profile Information
    cv_path = db.Column(db.String(255))
    research_interests = db.Column(db.Text)  # JSON string
    target_countries = db.Column(db.Text)  # JSON string
    preferences = db.Column(db.Text)  # JSON string

    # Account Status
    is_active = db.Column(db.Boolean, default=True)
    is_verified = db.Column(db.Boolean, default=False)

    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)

    # Relationships
    applications = db.relationship('Application', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    email_batches = db.relationship('EmailBatch', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    analytics = db.relationship('Analytics', backref='user', lazy='dynamic', cascade='all, delete-orphan')

    def __init__(self, email, password, name):
        """Initialize new user"""
        self.email = email
        self.set_password(password)
        self.name = name
        self.research_interests = json.dumps([])
        self.target_countries = json.dumps([])
        self.preferences = json.dumps({})

    def set_password(self, password):
        """Hash and set user password"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Verify password against hash"""
        return check_password_hash(self.password_hash, password)

    def get_research_interests(self):
        """Get research interests as list"""
        try:
            return json.loads(self.research_interests) if self.research_interests else []
        except:
            return []

    def set_research_interests(self, interests):
        """Set research interests from list"""
        self.research_interests = json.dumps(interests)

    def get_target_countries(self):
        """Get target countries as list"""
        try:
            return json.loads(self.target_countries) if self.target_countries else []
        except:
            return []

    def set_target_countries(self, countries):
        """Set target countries from list"""
        self.target_countries = json.dumps(countries)

    def get_preferences(self):
        """Get preferences as dictionary"""
        try:
            return json.loads(self.preferences) if self.preferences else {}
        except:
            return {}

    def set_preferences(self, prefs):
        """Set preferences from dictionary"""
        self.preferences = json.dumps(prefs)

    def to_dict(self):
        """Convert user to dictionary (exclude password)"""
        return {
            'id': self.id,
            'email': self.email,
            'name': self.name,
            'cv_path': self.cv_path,
            'research_interests': self.get_research_interests(),
            'target_countries': self.get_target_countries(),
            'preferences': self.get_preferences(),
            'is_active': self.is_active,
            'is_verified': self.is_verified,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_login': self.last_login.isoformat() if self.last_login else None
        }

    def __repr__(self):
        return f'<User {self.email}>'
