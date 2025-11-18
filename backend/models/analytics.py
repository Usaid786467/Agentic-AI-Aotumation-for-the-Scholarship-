"""
Analytics Model

Stores analytics and metrics including:
- User-specific metrics
- Application statistics
- Success rates
- Response times
"""

from . import db
from datetime import datetime
import json


class Analytics(db.Model):
    """Analytics model for tracking metrics and statistics"""

    __tablename__ = 'analytics'

    # Primary Fields
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)

    # Metric Information
    metric_name = db.Column(db.String(100), nullable=False, index=True)
    metric_value = db.Column(db.Float, nullable=False)

    # Date for time-series data
    date = db.Column(db.Date, nullable=False, index=True)

    # Additional metadata
    meta_data = db.Column(db.Text)  # JSON string for additional context

    # Timestamp
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, user_id, metric_name, metric_value, date=None, metadata=None):
        """Initialize new analytics record"""
        self.user_id = user_id
        self.metric_name = metric_name
        self.metric_value = metric_value
        self.date = date or datetime.utcnow().date()
        self.meta_data = json.dumps(metadata) if metadata else None

    def get_metadata(self):
        """Get metadata as dictionary"""
        try:
            return json.loads(self.meta_data) if self.meta_data else {}
        except:
            return {}

    def set_metadata(self, meta):
        """Set metadata from dictionary"""
        self.meta_data = json.dumps(meta)

    def to_dict(self):
        """Convert analytics to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'metric_name': self.metric_name,
            'metric_value': self.metric_value,
            'date': self.date.isoformat() if self.date else None,
            'metadata': self.get_metadata(),
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

    def __repr__(self):
        return f'<Analytics {self.metric_name}: {self.metric_value}>'
