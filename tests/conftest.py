"""Shared test configuration and fixtures."""

import pytest
from fastapi.testclient import TestClient
from src import app as app_module


@pytest.fixture
def client():
    """Provide a FastAPI TestClient instance with fresh app state for each test."""
    # Reload the app module to get fresh in-memory data
    import importlib
    importlib.reload(app_module)
    
    # Create a new TestClient with the reloaded app
    return TestClient(app_module.app)


@pytest.fixture
def sample_email():
    """Provide a sample student email for testing."""
    return "test.student@mergington.edu"


@pytest.fixture
def sample_email_2():
    """Provide another sample student email for testing."""
    return "another.student@mergington.edu"


@pytest.fixture
def existing_activity():
    """Provide an existing activity name for testing."""
    return "Chess Club"


@pytest.fixture
def nonexistent_activity():
    """Provide a non-existent activity name for testing."""
    return "Underwater Basket Weaving"


@pytest.fixture
def full_activity():
    """Provide an activity that is at max capacity."""
    return "Programming Class"  # Has 2 participants, max_participants=20 (adjust if needed)
