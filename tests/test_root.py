"""Tests for the root endpoint (GET /)."""

import pytest


class TestRootEndpoint:
    """Test cases for GET / redirect."""

    def test_root_redirects_to_index_html(self, client):
        """Test that the root path redirects to /static/index.html."""
        response = client.get("/", follow_redirects=False)
        assert response.status_code == 307
        assert response.headers["location"] == "/static/index.html"

    def test_root_with_follow_redirects(self, client):
        """Test that the root path can be followed to index.html."""
        response = client.get("/", follow_redirects=True)
        assert response.status_code == 200
