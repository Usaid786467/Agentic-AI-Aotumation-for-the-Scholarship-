"""
AI Services Package

AI-powered services using Google Gemini:
- Email generation
- Research matching
- Content analysis
"""

from .gemini_service import GeminiService
from .email_generator import EmailGenerator
from .matching_engine import MatchingEngine

__all__ = ['GeminiService', 'EmailGenerator', 'MatchingEngine']
