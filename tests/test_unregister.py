"""Tests for the unregister endpoint (DELETE /activities/{activity_name}/unregister)."""

import pytest


class TestUnregisterEndpoint:
    """Test cases for DELETE /activities/{activity_name}/unregister."""

    def test_successful_unregister(self, client, existing_activity, sample_email):
        """Test that a student can successfully unregister from an activity."""
        # First, sign up the student
        client.post(
            f"/activities/{existing_activity}/signup",
            params={"email": sample_email}
        )
        
        # Then unregister
        response = client.delete(
            f"/activities/{existing_activity}/unregister",
            params={"email": sample_email}
        )
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert sample_email in data["message"]
        assert existing_activity in data["message"]

    def test_unregister_removes_participant_from_activity(self, client, existing_activity, sample_email):
        """Test that unregister actually removes the participant from the activity."""
        # Sign up the student
        client.post(
            f"/activities/{existing_activity}/signup",
            params={"email": sample_email}
        )
        
        # Verify they are signed up
        response = client.get("/activities")
        activities = response.json()
        assert sample_email in activities[existing_activity]["participants"]
        
        # Unregister
        response = client.delete(
            f"/activities/{existing_activity}/unregister",
            params={"email": sample_email}
        )
        assert response.status_code == 200
        
        # Verify they are no longer signed up
        response = client.get("/activities")
        activities = response.json()
        assert sample_email not in activities[existing_activity]["participants"]

    def test_unregister_nonexistent_activity_returns_404(self, client, nonexistent_activity, sample_email):
        """Test that unregistering from a non-existent activity returns 404."""
        response = client.delete(
            f"/activities/{nonexistent_activity}/unregister",
            params={"email": sample_email}
        )
        assert response.status_code == 404
        data = response.json()
        assert "detail" in data
        assert "not found" in data["detail"].lower()

    def test_unregister_not_signed_up_returns_400(self, client, existing_activity):
        """Test that unregistering a student who isn't signed up returns 400."""
        email = "not.signed.up@mergington.edu"
        response = client.delete(
            f"/activities/{existing_activity}/unregister",
            params={"email": email}
        )
        assert response.status_code == 400
        data = response.json()
        assert "detail" in data
        assert "not signed up" in data["detail"].lower()

    def test_unregister_response_format(self, client, existing_activity, sample_email):
        """Test that the unregister response has the correct format."""
        # First sign up
        client.post(
            f"/activities/{existing_activity}/signup",
            params={"email": sample_email}
        )
        
        # Then unregister
        response = client.delete(
            f"/activities/{existing_activity}/unregister",
            params={"email": sample_email}
        )
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)
        assert "message" in data
        assert isinstance(data["message"], str)
