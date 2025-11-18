"""
Combined Test Suite

Runs all backend tests
"""

import pytest
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))


def run_all_tests():
    """Run all tests"""
    print("=" * 50)
    print("Running All Backend Tests")
    print("=" * 50)

    # Run pytest with verbose output
    exit_code = pytest.main([
        'tests/',
        '-v',
        '--tb=short',
        '--color=yes'
    ])

    return exit_code


if __name__ == '__main__':
    exit_code = run_all_tests()
    print("\n" + "=" * 50)
    if exit_code == 0:
        print("✅ All tests passed!")
    else:
        print("❌ Some tests failed")
    print("=" * 50)
    sys.exit(exit_code)
