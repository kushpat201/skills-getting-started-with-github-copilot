"""Tests for GET /activities endpoint."""

import pytest


class TestGetActivities:
    """Test suite for retrieving activities."""

    def test_get_activities_returns_all_activities(self, client):
        """
        Arrange: No setup needed
        Act: GET /activities
        Assert: Returns 200 with all activities and correct structure
        """
        # Act
        response = client.get("/activities")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "Chess Club" in data
        assert "Programming Class" in data
        assert "Gym Class" in data

    def test_get_activities_includes_activity_details(self, client):
        """
        Arrange: No setup needed
        Act: GET /activities
        Assert: Each activity has required fields
        """
        # Act
        response = client.get("/activities")

        # Assert
        data = response.json()
        activity = data["Chess Club"]
        
        assert "description" in activity
        assert "schedule" in activity
        assert "max_participants" in activity
        assert "participants" in activity
        assert isinstance(activity["participants"], list)

    def test_get_activities_includes_current_participants(self, client):
        """
        Arrange: No setup needed
        Act: GET /activities
        Assert: Participants list matches expected data
        """
        # Act
        response = client.get("/activities")

        # Assert
        data = response.json()
        chess_participants = data["Chess Club"]["participants"]
        
        assert "michael@mergington.edu" in chess_participants
        assert "daniel@mergington.edu" in chess_participants
        assert len(chess_participants) == 2
