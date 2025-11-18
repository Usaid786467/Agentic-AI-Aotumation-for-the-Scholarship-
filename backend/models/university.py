"""
University Model

Stores information about universities including:
- Basic information (name, location, website)
- Scholarship availability
- Application deadlines
- Research areas
- Contact information
"""

from . import db
from datetime import datetime
import json


class University(db.Model):
    """University model for storing university information"""

    __tablename__ = 'universities'

    # Primary Fields
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, index=True)
    country = db.Column(db.String(100), nullable=False, index=True)
    city = db.Column(db.String(100))
    website = db.Column(db.String(255))
    domain = db.Column(db.String(100), index=True)  # e.g., .edu, .cn

    # Ranking & Status
    ranking = db.Column(db.Integer)  # Can be null for unranked universities

    # Scholarship Information
    has_scholarship = db.Column(db.Boolean, default=False, index=True)
    scholarship_details = db.Column(db.Text)

    # Application Information
    application_deadline = db.Column(db.Date)
    research_areas = db.Column(db.Text)  # JSON string

    # Contact Information
    contact_email = db.Column(db.String(120))
    phone = db.Column(db.String(50))
    address = db.Column(db.Text)

    # Additional Information
    logo_url = db.Column(db.String(255))

    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_scraped = db.Column(db.DateTime)

    # Relationships
    professors = db.relationship('Professor', backref='university', lazy='dynamic', cascade='all, delete-orphan')
    applications = db.relationship('Application', backref='university', lazy='dynamic')

    def __init__(self, name, country, **kwargs):
        """Initialize new university"""
        self.name = name
        self.country = country
        self.city = kwargs.get('city')
        self.website = kwargs.get('website')
        self.domain = kwargs.get('domain')
        self.ranking = kwargs.get('ranking')
        self.has_scholarship = kwargs.get('has_scholarship', False)
        self.scholarship_details = kwargs.get('scholarship_details')
        self.research_areas = json.dumps(kwargs.get('research_areas', []))

    def get_research_areas(self):
        """Get research areas as list"""
        try:
            return json.loads(self.research_areas) if self.research_areas else []
        except:
            return []

    def set_research_areas(self, areas):
        """Set research areas from list"""
        self.research_areas = json.dumps(areas)

    def to_dict(self):
        """Convert university to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'country': self.country,
            'city': self.city,
            'website': self.website,
            'domain': self.domain,
            'ranking': self.ranking,
            'has_scholarship': self.has_scholarship,
            'scholarship_details': self.scholarship_details,
            'application_deadline': self.application_deadline.isoformat() if self.application_deadline else None,
            'research_areas': self.get_research_areas(),
            'contact_email': self.contact_email,
            'phone': self.phone,
            'address': self.address,
            'logo_url': self.logo_url,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'last_scraped': self.last_scraped.isoformat() if self.last_scraped else None,
            'professor_count': self.professors.count() if hasattr(self, 'professors') else 0
        }

    def __repr__(self):
        return f'<University {self.name}, {self.country}>'
