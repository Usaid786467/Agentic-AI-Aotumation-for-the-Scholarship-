"""
Application Model

Tracks PhD application submissions including:
- Application status
- Important dates
- Email tracking (sent, opened, replied)
- Notes and documents
- Match score
"""

from . import db
from datetime import datetime
import json


class Application(db.Model):
    """Application model for tracking PhD applications"""

    __tablename__ = 'applications'

    # Primary Fields
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    professor_id = db.Column(db.Integer, db.ForeignKey('professors.id'), nullable=False, index=True)
    university_id = db.Column(db.Integer, db.ForeignKey('universities.id'), nullable=False, index=True)

    # Status Tracking
    # Possible statuses: draft, sent, delivered, opened, replied, rejected, accepted, withdrawn
    status = db.Column(db.String(50), default='draft', index=True)

    # Important Dates
    applied_date = db.Column(db.DateTime)
    opened_date = db.Column(db.DateTime)
    replied_date = db.Column(db.DateTime)
    follow_up_date = db.Column(db.DateTime)

    # Response Information
    response_content = db.Column(db.Text)

    # Additional Information
    notes = db.Column(db.Text)
    documents = db.Column(db.Text)  # JSON string with document paths
    match_score = db.Column(db.Float)  # 0-100 match score

    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    emails = db.relationship('Email', backref='application', lazy='dynamic', cascade='all, delete-orphan')

    def __init__(self, user_id, professor_id, university_id, **kwargs):
        """Initialize new application"""
        self.user_id = user_id
        self.professor_id = professor_id
        self.university_id = university_id
        self.status = kwargs.get('status', 'draft')
        self.match_score = kwargs.get('match_score')
        self.notes = kwargs.get('notes')
        self.documents = json.dumps(kwargs.get('documents', []))

    def get_documents(self):
        """Get documents as list"""
        try:
            return json.loads(self.documents) if self.documents else []
        except:
            return []

    def set_documents(self, docs):
        """Set documents from list"""
        self.documents = json.dumps(docs)

    def add_document(self, document_path):
        """Add a document to the application"""
        docs = self.get_documents()
        docs.append(document_path)
        self.set_documents(docs)

    def update_status(self, new_status):
        """Update application status and set appropriate dates"""
        self.status = new_status
        now = datetime.utcnow()

        if new_status == 'sent' and not self.applied_date:
            self.applied_date = now
        elif new_status == 'opened' and not self.opened_date:
            self.opened_date = now
        elif new_status == 'replied' and not self.replied_date:
            self.replied_date = now

    def to_dict(self, include_relations=False):
        """Convert application to dictionary"""
        data = {
            'id': self.id,
            'user_id': self.user_id,
            'professor_id': self.professor_id,
            'university_id': self.university_id,
            'status': self.status,
            'applied_date': self.applied_date.isoformat() if self.applied_date else None,
            'opened_date': self.opened_date.isoformat() if self.opened_date else None,
            'replied_date': self.replied_date.isoformat() if self.replied_date else None,
            'follow_up_date': self.follow_up_date.isoformat() if self.follow_up_date else None,
            'response_content': self.response_content,
            'notes': self.notes,
            'documents': self.get_documents(),
            'match_score': self.match_score,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

        # Include related information if requested
        if include_relations:
            if hasattr(self, 'professor') and self.professor:
                data['professor'] = {
                    'id': self.professor.id,
                    'name': self.professor.name,
                    'email': self.professor.email,
                    'title': self.professor.title
                }
            if hasattr(self, 'university') and self.university:
                data['university'] = {
                    'id': self.university.id,
                    'name': self.university.name,
                    'country': self.university.country
                }
            if hasattr(self, 'emails'):
                data['email_count'] = self.emails.count()

        return data

    def __repr__(self):
        return f'<Application {self.id} - Status: {self.status}>'
