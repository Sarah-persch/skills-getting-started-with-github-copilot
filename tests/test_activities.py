"""Tests for the activities endpoint (GET /activities)."""

import pytest


class TestActivitiesEndpoint:
    """Test cases for GET /activities."""

    def test_get_all_activities(self, client):
        """Test that all activities are returned."""
        response = client.get("/activities")
        assert response.status_code == 200
        activities = response.json()
        assert isinstance(activities, dict)
        assert len(activities) > 0

    def test_activities_have_required_fields(self, client):
        """Test that each activity has the required fields."""
        response = client.get("/activities")
        activities = response.json()
        
        for activity_name, activity_details in activities.items():
            assert "description" in activity_details
            assert "schedule" in activity_details
            assert "max_participants" in activity_details
            assert "participants" in activity_details
            assert isinstance(activity_details["participants"], list)

    def test_activities_show_correct_participant_counts(self, client):
        """Test that participant counts are accurate in the activities list."""
        response = client.get("/activities")
        activities = response.json()
        
        # Chess Club should have initial participants
        chess_club = activities.get("Chess Club")
        assert chess_club is not None
        assert len(chess_club["participants"]) == 2
        assert "michael@mergington.edu" in chess_club["participants"]
        assert "daniel@mergington.edu" in chess_club["participants"]

    def test_activities_include_chess_club(self, client, existing_activity):
        """Test that Chess Club activity exists."""
        response = client.get("/activities")
        activities = response.json()
        assert existing_activity in activities
