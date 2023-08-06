"""
Unit and regression test for the pipit package.
"""

# Import package, test suite, and other packages as needed
import pipit
import pytest
import sys

def test_pipit_imported():
    """Sample test, will always pass so long as import statement worked"""
    assert "pipit" in sys.modules
