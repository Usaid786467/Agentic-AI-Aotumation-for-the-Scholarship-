"""
Google Gemini AI Service

Provides interface to Google's Gemini AI for:
- Text generation
- Content analysis
- Research matching
- Email personalization
"""

import google.generativeai as genai
from typing import Optional, Dict, Any
import os
from services.utils.logger import get_logger

logger = get_logger(__name__)


class GeminiService:
    """Service class for interacting with Google Gemini AI"""

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize Gemini service

        Args:
            api_key: Google Gemini API key (optional, will use env var if not provided)
        """
        self.api_key = api_key or os.getenv('GEMINI_API_KEY')

        if not self.api_key:
            logger.warning("Gemini API key not found. AI features will be limited.")
            self.model = None
        else:
            try:
                genai.configure(api_key=self.api_key)
                self.model = genai.GenerativeModel('gemini-pro')
                logger.info("Gemini AI service initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize Gemini AI: {str(e)}")
                self.model = None

    def generate_text(self, prompt: str, max_tokens: int = 1000) -> Optional[str]:
        """
        Generate text using Gemini AI

        Args:
            prompt: Input prompt
            max_tokens: Maximum tokens to generate

        Returns:
            Generated text or None if failed
        """
        if not self.model:
            logger.error("Gemini model not initialized")
            return None

        try:
            response = self.model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    max_output_tokens=max_tokens,
                    temperature=0.7,
                )
            )
            return response.text
        except Exception as e:
            logger.error(f"Error generating text: {str(e)}")
            return None

    def analyze_research_interests(self, text: str) -> list:
        """
        Extract research interests from text using AI

        Args:
            text: Input text (bio, about page, etc.)

        Returns:
            List of research interest keywords
        """
        if not self.model:
            # Fallback to simple extraction
            return self._simple_keyword_extraction(text)

        prompt = f"""
        Analyze the following academic text and extract the main research interests as a comma-separated list of keywords.
        Focus on specific research areas, methodologies, and technologies.
        Return ONLY the comma-separated list, nothing else.

        Text: {text[:2000]}

        Research interests:
        """

        try:
            result = self.generate_text(prompt, max_tokens=200)
            if result:
                # Parse comma-separated list
                interests = [interest.strip() for interest in result.split(',')]
                return [i for i in interests if i][:10]  # Limit to 10 interests
            return []
        except Exception as e:
            logger.error(f"Error analyzing research interests: {str(e)}")
            return self._simple_keyword_extraction(text)

    def _simple_keyword_extraction(self, text: str) -> list:
        """
        Simple fallback method for keyword extraction without AI

        Args:
            text: Input text

        Returns:
            List of keywords
        """
        # Common research keywords
        keywords = [
            'machine learning', 'deep learning', 'artificial intelligence',
            'computer vision', 'natural language processing', 'robotics',
            'data science', 'neural networks', 'manufacturing',
            'aerospace', 'mechanical engineering', 'optimization',
            'simulation', 'modeling', 'automation'
        ]

        text_lower = text.lower()
        found = [kw for kw in keywords if kw in text_lower]
        return found[:5]

    def calculate_research_match(self, user_interests: list, prof_interests: list) -> float:
        """
        Calculate match score between user and professor research interests using AI

        Args:
            user_interests: User's research interests
            prof_interests: Professor's research interests

        Returns:
            Match score (0-100)
        """
        if not user_interests or not prof_interests:
            return 0.0

        if not self.model:
            # Fallback to simple matching
            from services.utils.helpers import calculate_match_score
            return calculate_match_score(user_interests, prof_interests)

        prompt = f"""
        Calculate a research interest match score (0-100) between a PhD applicant and a professor.
        Consider semantic similarity, not just exact keyword matches.

        Applicant's interests: {', '.join(user_interests)}
        Professor's interests: {', '.join(prof_interests)}

        Return ONLY a number between 0 and 100, nothing else.
        Score:
        """

        try:
            result = self.generate_text(prompt, max_tokens=10)
            if result:
                # Extract number from result
                score = float(''.join(filter(str.isdigit, result)))
                return min(score, 100.0)
            return 0.0
        except Exception as e:
            logger.error(f"Error calculating match score: {str(e)}")
            from services.utils.helpers import calculate_match_score
            return calculate_match_score(user_interests, prof_interests)

    def generate_email_subject(self, professor_name: str, university: str) -> str:
        """
        Generate email subject line

        Args:
            professor_name: Professor's name
            university: University name

        Returns:
            Email subject line
        """
        if not self.model:
            return f"PhD Opportunity - Research Collaboration Inquiry"

        prompt = f"""
        Generate a professional email subject line for a PhD application inquiry to Professor {professor_name} at {university}.
        The subject should be concise (5-10 words), professional, and attention-grabbing.
        Focus on PhD position, research opportunity, or collaboration.

        Return ONLY the subject line, without quotes.
        Subject:
        """

        try:
            result = self.generate_text(prompt, max_tokens=50)
            if result:
                # Clean up the result
                subject = result.strip().replace('"', '').replace("'", "")
                return subject
            return f"PhD Research Opportunity Inquiry"
        except Exception as e:
            logger.error(f"Error generating subject: {str(e)}")
            return f"PhD Research Opportunity Inquiry"


# Create singleton instance
gemini_service = GeminiService()
