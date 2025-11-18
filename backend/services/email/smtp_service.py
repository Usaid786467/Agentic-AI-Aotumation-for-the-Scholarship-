"""
SMTP Email Service

Handles sending emails via SMTP
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from typing import Optional, List
import os
from services.utils.logger import get_logger

logger = get_logger(__name__)


class SMTPService:
    """Service for sending emails via SMTP"""

    def __init__(self, host: str = None, port: int = None, username: str = None, password: str = None):
        """
        Initialize SMTP service

        Args:
            host: SMTP server host
            port: SMTP server port
            username: SMTP username
            password: SMTP password
        """
        self.host = host or os.getenv('SMTP_HOST', 'smtp.gmail.com')
        self.port = port or int(os.getenv('SMTP_PORT', '587'))
        self.username = username or os.getenv('SMTP_USERNAME', '')
        self.password = password or os.getenv('SMTP_PASSWORD', '')
        self.from_email = os.getenv('EMAIL_FROM', self.username)

    def send_email(
        self,
        to_email: str,
        subject: str,
        body: str,
        attachments: Optional[List[str]] = None
    ) -> bool:
        """
        Send email

        Args:
            to_email: Recipient email address
            subject: Email subject
            body: Email body (plain text or HTML)
            attachments: List of file paths to attach (optional)

        Returns:
            bool: True if sent successfully, False otherwise
        """
        try:
            # Create message
            msg = MIMEMultipart()
            msg['From'] = self.from_email
            msg['To'] = to_email
            msg['Subject'] = subject

            # Attach body
            msg.attach(MIMEText(body, 'plain'))

            # Attach files if provided
            if attachments:
                for file_path in attachments:
                    if os.path.exists(file_path):
                        with open(file_path, 'rb') as f:
                            part = MIMEApplication(f.read(), Name=os.path.basename(file_path))
                            part['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_path)}"'
                            msg.attach(part)

            # Send email
            with smtplib.SMTP(self.host, self.port) as server:
                server.starttls()
                server.login(self.username, self.password)
                server.send_message(msg)

            logger.info(f"Email sent successfully to {to_email}")
            return True

        except Exception as e:
            logger.error(f"Failed to send email to {to_email}: {str(e)}")
            return False

    def test_connection(self) -> bool:
        """
        Test SMTP connection

        Returns:
            bool: True if connection successful
        """
        try:
            with smtplib.SMTP(self.host, self.port, timeout=10) as server:
                server.starttls()
                server.login(self.username, self.password)
            logger.info("SMTP connection test successful")
            return True
        except Exception as e:
            logger.error(f"SMTP connection test failed: {str(e)}")
            return False


# Create singleton instance
smtp_service = SMTPService()
