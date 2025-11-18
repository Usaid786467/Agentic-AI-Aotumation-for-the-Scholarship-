"""
Email Models

Handles email management including:
- Email: Individual email records
- EmailBatch: Batch email management for approval workflow
"""

from . import db
from datetime import datetime


class Email(db.Model):
    """Email model for tracking individual emails"""

    __tablename__ = 'emails'

    # Primary Fields
    id = db.Column(db.Integer, primary_key=True)
    application_id = db.Column(db.Integer, db.ForeignKey('applications.id'), nullable=False, index=True)
    batch_id = db.Column(db.Integer, db.ForeignKey('email_batches.id'), index=True)

    # Email Content
    subject = db.Column(db.String(255), nullable=False)
    body = db.Column(db.Text, nullable=False)
    template_id = db.Column(db.String(100))

    # Status Tracking
    # Possible statuses: draft, pending, approved, scheduled, sending, sent, failed, bounced
    status = db.Column(db.String(50), default='draft', index=True)

    # Scheduling
    scheduled_time = db.Column(db.DateTime)

    # Tracking
    sent_at = db.Column(db.DateTime)
    opened_at = db.Column(db.DateTime)
    replied_at = db.Column(db.DateTime)

    # Error Handling
    error_message = db.Column(db.Text)
    retry_count = db.Column(db.Integer, default=0)

    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, application_id, subject, body, **kwargs):
        """Initialize new email"""
        self.application_id = application_id
        self.subject = subject
        self.body = body
        self.batch_id = kwargs.get('batch_id')
        self.template_id = kwargs.get('template_id')
        self.status = kwargs.get('status', 'draft')

    def mark_as_sent(self):
        """Mark email as sent"""
        self.status = 'sent'
        self.sent_at = datetime.utcnow()

    def mark_as_opened(self):
        """Mark email as opened"""
        self.opened_at = datetime.utcnow()
        # Update application status if exists
        if hasattr(self, 'application'):
            self.application.update_status('opened')

    def mark_as_replied(self):
        """Mark email as replied"""
        self.replied_at = datetime.utcnow()
        # Update application status if exists
        if hasattr(self, 'application'):
            self.application.update_status('replied')

    def mark_as_failed(self, error_msg):
        """Mark email as failed"""
        self.status = 'failed'
        self.error_message = error_msg
        self.retry_count += 1

    def to_dict(self):
        """Convert email to dictionary"""
        return {
            'id': self.id,
            'application_id': self.application_id,
            'batch_id': self.batch_id,
            'subject': self.subject,
            'body': self.body,
            'template_id': self.template_id,
            'status': self.status,
            'scheduled_time': self.scheduled_time.isoformat() if self.scheduled_time else None,
            'sent_at': self.sent_at.isoformat() if self.sent_at else None,
            'opened_at': self.opened_at.isoformat() if self.opened_at else None,
            'replied_at': self.replied_at.isoformat() if self.replied_at else None,
            'error_message': self.error_message,
            'retry_count': self.retry_count,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

    def __repr__(self):
        return f'<Email {self.id} - Status: {self.status}>'


class EmailBatch(db.Model):
    """EmailBatch model for managing batch email operations"""

    __tablename__ = 'email_batches'

    # Primary Fields
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)

    # Batch Information
    name = db.Column(db.String(200))
    total_count = db.Column(db.Integer, default=0)
    approved_count = db.Column(db.Integer, default=0)
    sent_count = db.Column(db.Integer, default=0)

    # Status
    # Possible statuses: draft, pending_approval, approved, sending, completed, failed
    status = db.Column(db.String(50), default='draft', index=True)

    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    approved_at = db.Column(db.DateTime)
    completed_at = db.Column(db.DateTime)

    # Relationships
    emails = db.relationship('Email', backref='batch', lazy='dynamic')

    def __init__(self, user_id, name=None):
        """Initialize new email batch"""
        self.user_id = user_id
        self.name = name or f"Batch {datetime.utcnow().strftime('%Y-%m-%d %H:%M')}"
        self.status = 'draft'

    def update_counts(self):
        """Update email counts"""
        if hasattr(self, 'emails'):
            self.total_count = self.emails.count()
            self.approved_count = self.emails.filter_by(status='approved').count()
            self.sent_count = self.emails.filter_by(status='sent').count()

    def approve(self):
        """Approve batch for sending"""
        self.status = 'approved'
        self.approved_at = datetime.utcnow()
        # Update all draft emails to approved
        if hasattr(self, 'emails'):
            for email in self.emails.filter_by(status='draft').all():
                email.status = 'approved'

    def mark_as_completed(self):
        """Mark batch as completed"""
        self.status = 'completed'
        self.completed_at = datetime.utcnow()

    def to_dict(self):
        """Convert batch to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.name,
            'total_count': self.total_count,
            'approved_count': self.approved_count,
            'sent_count': self.sent_count,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'approved_at': self.approved_at.isoformat() if self.approved_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None
        }

    def __repr__(self):
        return f'<EmailBatch {self.id} - {self.name}>'
