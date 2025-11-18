"""
Professor Model

Stores professor profile information including:
- Basic information (name, title, email)
- Research interests
- Publications
- Academic metrics (h-index, citations)
- Student availability
"""

from . import db
from datetime import datetime
import json


class Professor(db.Model):
    """Professor model for storing professor profiles"""

    __tablename__ = 'professors'

    # Primary Fields
    id = db.Column(db.Integer, primary_key=True)
    university_id = db.Column(db.Integer, db.ForeignKey('universities.id'), nullable=False, index=True)

    # Basic Information
    name = db.Column(db.String(200), nullable=False, index=True)
    title = db.Column(db.String(100))  # e.g., Professor, Associate Professor
    email = db.Column(db.String(120), index=True)
    department = db.Column(db.String(200))

    # Research Information
    research_interests = db.Column(db.Text)  # JSON string
    publications = db.Column(db.Text)  # JSON string with recent publications

    # Academic Metrics
    h_index = db.Column(db.Integer)
    citations = db.Column(db.Integer)

    # Student Information
    accepting_students = db.Column(db.Boolean, default=True)

    # Profile Links
    lab_website = db.Column(db.String(255))
    profile_url = db.Column(db.String(255))
    google_scholar_url = db.Column(db.String(255))

    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_contacted = db.Column(db.DateTime)

    # Relationships
    applications = db.relationship('Application', backref='professor', lazy='dynamic')

    def __init__(self, name, university_id, **kwargs):
        """Initialize new professor"""
        self.name = name
        self.university_id = university_id
        self.title = kwargs.get('title')
        self.email = kwargs.get('email')
        self.department = kwargs.get('department')
        self.research_interests = json.dumps(kwargs.get('research_interests', []))
        self.publications = json.dumps(kwargs.get('publications', []))
        self.h_index = kwargs.get('h_index')
        self.citations = kwargs.get('citations')
        self.accepting_students = kwargs.get('accepting_students', True)
        self.lab_website = kwargs.get('lab_website')
        self.profile_url = kwargs.get('profile_url')
        self.google_scholar_url = kwargs.get('google_scholar_url')

    def get_research_interests(self):
        """Get research interests as list"""
        try:
            return json.loads(self.research_interests) if self.research_interests else []
        except:
            return []

    def set_research_interests(self, interests):
        """Set research interests from list"""
        self.research_interests = json.dumps(interests)

    def get_publications(self):
        """Get publications as list"""
        try:
            return json.loads(self.publications) if self.publications else []
        except:
            return []

    def set_publications(self, pubs):
        """Set publications from list"""
        self.publications = json.dumps(pubs)

    def to_dict(self, include_university=False):
        """Convert professor to dictionary"""
        data = {
            'id': self.id,
            'university_id': self.university_id,
            'name': self.name,
            'title': self.title,
            'email': self.email,
            'department': self.department,
            'research_interests': self.get_research_interests(),
            'publications': self.get_publications(),
            'h_index': self.h_index,
            'citations': self.citations,
            'accepting_students': self.accepting_students,
            'lab_website': self.lab_website,
            'profile_url': self.profile_url,
            'google_scholar_url': self.google_scholar_url,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'last_contacted': self.last_contacted.isoformat() if self.last_contacted else None
        }

        # Include university information if requested
        if include_university and hasattr(self, 'university'):
            data['university'] = {
                'id': self.university.id,
                'name': self.university.name,
                'country': self.university.country,
                'website': self.university.website
            }

        return data

    def __repr__(self):
        return f'<Professor {self.name}>'
