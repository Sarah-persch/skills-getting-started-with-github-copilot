"""Tests for the signup endpoint (POST /activities/{activity_name}/signup)."""

import pytest


class TestSignupEndpoint:
    """Test cases for POST /activities/{activity_name}/signup."""

    def test_successful_signup(self, client, existing_activity, sample_email):
        """Test that a student can successfully sign up for an activity."""
        response = client.post(
            f"/activities/{existing_activity}/signup",
            params={"email": sample_email}
        )
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert sample_email in data["message"]
        assert existing_activity in data["message"]

    def test_signup_adds_participant_to_activity(self, client, existing_activity, sample_email):
        """Test that signup actually adds the participant to the activity's participant list."""
        # Sign up the student
        response = client.post(
            f"/activities/{existing_activity}/signup",
            params={"email": sample_email}
        )
        assert response.status_code == 200
        
        # Verify participant was added by checking activities list
        response = client.get("/activities")
        activities = response.json()
        activity = activities[existing_activity]
        assert sample_email in activity["participants"]

    def test_signup_nonexistent_activity_returns_404(self, client, nonexistent_activity, sample_email):
        """Test that signing up for a non-existent activity returns 404."""
        response = client.post(
            f"/activities/{nonexistent_activity}/signup",
            params={"email": sample_email}
        )
        assert response.status_code == 404
        data = response.json()
        assert "detail" in data
        assert "not found" in data["detail"].lower()

    def test_duplicate_signup_returns_400(self, client, existing_activity):
        """Test that signing up twice for the same activity returns 400."""
        # First signup should succeed
        email = "duplicate.test@mergington.edu"
        response1 = client.post(
            f"/activities/{existing_activity}/signup",
            params={"email": email}
        )
        assert response1.status_code == 200
        
        # Second signup with same email should fail
        response2 = client.post(
            f"/activities/{existing_activity}/signup",
            params={"email": email}
        )
        assert response2.status_code == 400
        data = response2.json()
        assert "detail" in data
        assert "already signed up" in data["detail"].lower()

    def test_signup_returns_error_when_activity_full(self, client):
        """Test that signing up for a full activity returns 400."""
        # Create an activity with limited capacity for testing
        activity_name = "Basketball Team"  # max_participants: 15, currently has 1
        
        # Fill the activity to max capacity
        for i in range(14):  # Add 14 more to reach the current 1 = 15
            email = f"filler{i}@mergington.edu"
            client.post(
                f"/activities/{activity_name}/signup",
                params={"email": email}
            )
        
        # Now try to sign up one more - should fail
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": "overflow@mergington.edu"}
        )
        assert response.status_code == 400
        data = response.json()
        assert "detail" in data
        assert "full" in data["detail"].lower()

    def test_signup_response_format(self, client, existing_activity, sample_email):
        """Test that the signup response has the correct format."""
        response = client.post(
            f"/activities/{existing_activity}/signup",
            params={"email": sample_email}
        )
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)
        assert "message" in data
        assert isinstance(data["message"], str)
