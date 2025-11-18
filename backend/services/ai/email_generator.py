"""
Email Generator Service

Generates personalized PhD application emails using AI
"""

from typing import Dict, Optional
from .gemini_service import gemini_service
from services.utils.logger import get_logger

logger = get_logger(__name__)


class EmailGenerator:
    """Service for generating personalized application emails"""

    def __init__(self):
        """Initialize email generator"""
        self.gemini = gemini_service

    def generate_email(self, user_profile: Dict, professor: Dict, university: Dict) -> Dict[str, str]:
        """
        Generate personalized email for professor

        Args:
            user_profile: User's profile information
                {
                    'name': str,
                    'research_interests': list,
                    'background': str (optional),
                    'experience': str (optional)
                }
            professor: Professor's information
                {
                    'name': str,
                    'research_interests': list,
                    'recent_publications': list (optional)
                }
            university: University information
                {
                    'name': str,
                    'country': str
                }

        Returns:
            Dictionary with 'subject' and 'body' keys
        """
        # Generate subject
        subject = self._generate_subject(professor, university)

        # Generate body
        body = self._generate_body(user_profile, professor, university)

        return {
            'subject': subject,
            'body': body
        }

    def _generate_subject(self, professor: Dict, university: Dict) -> str:
        """Generate email subject line"""
        return self.gemini.generate_email_subject(
            professor.get('name', 'Professor'),
            university.get('name', 'University')
        )

    def _generate_body(self, user_profile: Dict, professor: Dict, university: Dict) -> str:
        """
        Generate email body

        Args:
            user_profile: User's profile
            professor: Professor's profile
            university: University info

        Returns:
            Email body text
        """
        if not self.gemini.model:
            # Fallback to template-based generation
            return self._template_email(user_profile, professor, university)

        # Find common research interests
        user_interests = user_profile.get('research_interests', [])
        prof_interests = professor.get('research_interests', [])
        common_interests = set([i.lower() for i in user_interests]) & set([i.lower() for i in prof_interests])

        # Get recent publications if available
        publications = professor.get('recent_publications', [])
        pub_text = ""
        if publications:
            pub_text = f"I was particularly interested in your recent work on '{publications[0].get('title', 'your research')}'"

        prompt = f"""
        Write a professional PhD application email (200-300 words) with the following details:

        SENDER:
        - Name: {user_profile.get('name', 'Student')}
        - Current status: Master's student in Mechanical Engineering
        - Research interests: {', '.join(user_interests[:3]) if user_interests else 'Deep Learning, Manufacturing, Aerospace'}
        - Background: Specializing in Machine Learning applications in manufacturing and aerospace

        RECIPIENT:
        - Professor {professor.get('name', 'Professor')}
        - {university.get('name', 'University')}, {university.get('country', '')}
        - Research areas: {', '.join(prof_interests[:3]) if prof_interests else 'Engineering'}

        COMMON INTERESTS: {', '.join(list(common_interests)[:2]) if common_interests else 'shared research areas'}

        REQUIREMENTS:
        - Start with "Dear Professor [Last Name],"
        - First paragraph: Briefly introduce yourself and express interest in their research program
        {f'- Mention their recent work: {pub_text}' if pub_text else ''}
        - Second paragraph: Highlight your relevant experience and how it aligns with their research
        - Mention specific shared research interests: {', '.join(list(common_interests)[:2]) if common_interests else 'machine learning in engineering'}
        - Third paragraph: Express interest in PhD position with funding/scholarship
        - Close professionally with "Best regards" or "Sincerely"
        - Mention that CV is attached
        - Keep it concise, professional, and genuine
        - DO NOT use overly flattering language
        - DO NOT make up specific projects or achievements

        Write the email:
        """

        try:
            email_body = self.gemini.generate_text(prompt, max_tokens=600)
            if email_body:
                return email_body.strip()
            else:
                return self._template_email(user_profile, professor, university)
        except Exception as e:
            logger.error(f"Error generating email body: {str(e)}")
            return self._template_email(user_profile, professor, university)

    def _template_email(self, user_profile: Dict, professor: Dict, university: Dict) -> str:
        """
        Fallback template-based email generation

        Args:
            user_profile: User's profile
            professor: Professor's profile
            university: University info

        Returns:
            Email body from template
        """
        prof_name = professor.get('name', 'Professor')
        # Extract last name
        last_name = prof_name.split()[-1] if ' ' in prof_name else prof_name

        user_name = user_profile.get('name', 'Student')
        uni_name = university.get('name', 'your university')

        user_interests = user_profile.get('research_interests', [])
        prof_interests = professor.get('research_interests', [])

        # Find common interests
        user_set = set([i.lower() for i in user_interests])
        prof_set = set([i.lower() for i in prof_interests])
        common = list(user_set & prof_set)

        research_mention = f"particularly in {common[0]}" if common else "in related research areas"

        template = f"""Dear Professor {last_name},

I hope this email finds you well. I am writing to express my strong interest in pursuing a PhD position in your research group at {uni_name}.

I am currently completing my Master's degree in Mechanical Engineering, with a focus on Machine Learning applications in manufacturing and aerospace. I am particularly drawn to your work in {prof_interests[0] if prof_interests else 'engineering research'}, {research_mention}.

During my Master's studies, I have developed expertise in deep learning, model training, and optimization techniques applied to manufacturing processes. I believe my background aligns well with your research focus on {', '.join(prof_interests[:2]) if prof_interests else 'advanced engineering systems'}, and I am eager to contribute to and learn from your team.

I am looking for a fully-funded PhD opportunity and would be grateful if you could inform me about any available positions with scholarship support in your research group. I have attached my CV for your review.

Thank you for considering my application. I look forward to the possibility of discussing this opportunity further.

Best regards,
{user_name}

[CV Attached]"""

        return template


# Create singleton instance
email_generator = EmailGenerator()
