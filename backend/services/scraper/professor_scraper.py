"""
Professor Scraper Service

Scrapes professor profiles and information
Note: This is a simplified version with sample data for demonstration
"""

from typing import List, Dict, Optional
from services.utils.logger import get_logger

logger = get_logger(__name__)


class ProfessorScraper:
    """Service for scraping professor information"""

    def __init__(self):
        """Initialize professor scraper"""
        pass

    def get_sample_professors(self, university_id: int) -> List[Dict]:
        """
        Get sample professors for a university

        Args:
            university_id: University ID

        Returns:
            List of professor dictionaries
        """
        # Sample professors for demonstration
        professors_data = {
            1: [  # MIT
                {
                    'name': 'Dr. Sarah Chen',
                    'title': 'Professor',
                    'email': 's.chen@mit.edu',
                    'department': 'Department of Mechanical Engineering',
                    'research_interests': ['Deep Learning', 'Robotics', 'Manufacturing Automation', 'Computer Vision'],
                    'h_index': 45,
                    'citations': 8500,
                    'accepting_students': True
                },
                {
                    'name': 'Dr. James Rodriguez',
                    'title': 'Associate Professor',
                    'email': 'j.rodriguez@mit.edu',
                    'department': 'Department of Aeronautics and Astronautics',
                    'research_interests': ['Aerospace Engineering', 'Machine Learning', 'Flight Control Systems'],
                    'h_index': 32,
                    'citations': 4200,
                    'accepting_students': True
                }
            ],
            2: [  # Stanford
                {
                    'name': 'Dr. Emily Zhang',
                    'title': 'Professor',
                    'email': 'ezhang@stanford.edu',
                    'department': 'Department of Computer Science',
                    'research_interests': ['Artificial Intelligence', 'Machine Learning', 'Robotics'],
                    'h_index': 52,
                    'citations': 12000,
                    'accepting_students': True
                }
            ],
            3: [  # Cambridge
                {
                    'name': 'Dr. Oliver Thompson',
                    'title': 'Professor',
                    'email': 'ot@cam.ac.uk',
                    'department': 'Department of Engineering',
                    'research_interests': ['Manufacturing', 'Optimization', 'Machine Learning'],
                    'h_index': 38,
                    'citations': 6700,
                    'accepting_students': True
                }
            ],
            4: [  # ETH Zurich
                {
                    'name': 'Dr. Hans Mueller',
                    'title': 'Professor',
                    'email': 'h.mueller@ethz.ch',
                    'department': 'Department of Mechanical and Process Engineering',
                    'research_interests': ['Robotics', 'Automation', 'Deep Learning'],
                    'h_index': 41,
                    'citations': 7800,
                    'accepting_students': True
                }
            ],
            5: [  # Tsinghua
                {
                    'name': 'Dr. Wei Wang',
                    'title': 'Professor',
                    'email': 'w.wang@tsinghua.edu.cn',
                    'department': 'Department of Automation',
                    'research_interests': ['Aerospace', 'Control Systems', 'AI'],
                    'h_index': 36,
                    'citations': 5900,
                    'accepting_students': True
                }
            ]
        }

        # Return professors for the specified university, or empty list if not found
        profs = professors_data.get(university_id, [])

        # Add university_id to each professor
        for prof in profs:
            prof['university_id'] = university_id

        return profs


# Create singleton instance
professor_scraper = ProfessorScraper()
