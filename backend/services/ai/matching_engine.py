"""
Matching Engine

Calculates match scores between users and professors based on research interests
"""

from typing import List, Dict
from .gemini_service import gemini_service
from services.utils.helpers import calculate_match_score
from services.utils.logger import get_logger

logger = get_logger(__name__)


class MatchingEngine:
    """Engine for matching users with professors based on research interests"""

    def __init__(self):
        """Initialize matching engine"""
        self.gemini = gemini_service

    def calculate_match(self, user_interests: List[str], prof_interests: List[str]) -> float:
        """
        Calculate match score between user and professor

        Args:
            user_interests: List of user's research interests
            prof_interests: List of professor's research interests

        Returns:
            Match score (0-100)
        """
        if not user_interests or not prof_interests:
            return 0.0

        # Use AI-based matching if available
        if self.gemini.model:
            try:
                return self.gemini.calculate_research_match(user_interests, prof_interests)
            except:
                pass

        # Fallback to traditional matching
        return calculate_match_score(user_interests, prof_interests)

    def rank_professors(self, user_interests: List[str], professors: List[Dict]) -> List[Dict]:
        """
        Rank professors by match score

        Args:
            user_interests: User's research interests
            professors: List of professor dictionaries

        Returns:
            List of professors sorted by match score (highest first)
        """
        scored_professors = []

        for prof in professors:
            prof_interests = prof.get('research_interests', [])
            if isinstance(prof_interests, str):
                import json
                try:
                    prof_interests = json.loads(prof_interests)
                except:
                    prof_interests = []

            match_score = self.calculate_match(user_interests, prof_interests)

            prof_copy = prof.copy() if isinstance(prof, dict) else prof.to_dict()
            prof_copy['match_score'] = match_score
            scored_professors.append(prof_copy)

        # Sort by match score (descending)
        scored_professors.sort(key=lambda x: x.get('match_score', 0), reverse=True)

        return scored_professors

    def find_common_interests(self, user_interests: List[str], prof_interests: List[str]) -> List[str]:
        """
        Find common research interests

        Args:
            user_interests: User's interests
            prof_interests: Professor's interests

        Returns:
            List of common interests
        """
        user_set = set([i.lower().strip() for i in user_interests if i])
        prof_set = set([i.lower().strip() for i in prof_interests if i])

        return list(user_set & prof_set)


# Create singleton instance
matching_engine = MatchingEngine()
