"""
Web Scraping Services Package

Services for scraping university and professor information
"""

from .university_scraper import UniversityScraper
from .professor_scraper import ProfessorScraper

__all__ = ['UniversityScraper', 'ProfessorScraper']
