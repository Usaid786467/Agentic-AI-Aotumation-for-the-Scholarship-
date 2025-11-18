"""
Scraping Job Model

Tracks web scraping jobs including:
- Job type (universities, professors)
- Status and progress
- Results count
- Error handling
"""

from . import db
from datetime import datetime
import json


class ScrapingJob(db.Model):
    """ScrapingJob model for tracking web scraping operations"""

    __tablename__ = 'scraping_jobs'

    # Primary Fields
    id = db.Column(db.Integer, primary_key=True)

    # Job Information
    # Job types: universities, professors, scholarships
    job_type = db.Column(db.String(50), nullable=False, index=True)

    # Status tracking
    # Possible statuses: pending, running, completed, failed, cancelled
    status = db.Column(db.String(50), default='pending', index=True)

    # Job Parameters (stored as JSON)
    parameters = db.Column(db.Text)  # JSON string with job parameters

    # Progress Tracking
    progress = db.Column(db.Float, default=0.0)  # 0-100 percentage
    results_count = db.Column(db.Integer, default=0)

    # Timestamps
    started_at = db.Column(db.DateTime)
    completed_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Error Information
    error_message = db.Column(db.Text)

    def __init__(self, job_type, parameters=None):
        """Initialize new scraping job"""
        self.job_type = job_type
        self.status = 'pending'
        self.parameters = json.dumps(parameters) if parameters else None
        self.progress = 0.0
        self.results_count = 0

    def get_parameters(self):
        """Get job parameters as dictionary"""
        try:
            return json.loads(self.parameters) if self.parameters else {}
        except:
            return {}

    def set_parameters(self, params):
        """Set job parameters from dictionary"""
        self.parameters = json.dumps(params)

    def start(self):
        """Mark job as started"""
        self.status = 'running'
        self.started_at = datetime.utcnow()

    def complete(self, results_count=None):
        """Mark job as completed"""
        self.status = 'completed'
        self.completed_at = datetime.utcnow()
        self.progress = 100.0
        if results_count is not None:
            self.results_count = results_count

    def fail(self, error_msg):
        """Mark job as failed"""
        self.status = 'failed'
        self.completed_at = datetime.utcnow()
        self.error_message = error_msg

    def update_progress(self, progress, results_count=None):
        """Update job progress"""
        self.progress = min(progress, 100.0)
        if results_count is not None:
            self.results_count = results_count

    def to_dict(self):
        """Convert scraping job to dictionary"""
        return {
            'id': self.id,
            'job_type': self.job_type,
            'status': self.status,
            'parameters': self.get_parameters(),
            'progress': self.progress,
            'results_count': self.results_count,
            'started_at': self.started_at.isoformat() if self.started_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'error_message': self.error_message
        }

    def __repr__(self):
        return f'<ScrapingJob {self.id} - {self.job_type}: {self.status}>'
