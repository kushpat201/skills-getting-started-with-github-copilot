"""Tests for DELETE /activities/{activity_name}/participants endpoint."""

import pytest


class TestRemoveParticipant:
    """Test suite for removing participants from activities."""

    def test_remove_participant_successful(self, client):
        """
        Arrange: Participant already in activity
        Act: DELETE /activities/Chess%20Club/participants with existing email
        Assert: Returns 200, removes participant, returns success message
        """
        # Arrange
        email = "michael@mergington.edu"  # In Chess Club
        activity = "Chess Club"

        # Act
        response = client.delete(
            f"/activities/{activity}/participants",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "Removed" in data["message"]
        assert email in data["message"]
        assert activity in data["message"]
        
        # Verify participant was removed
        activities_response = client.get("/activities")
        activities = activities_response.json()
        assert email not in activities[activity]["participants"]

    def test_remove_participant_not_found(self, client):
        """
        Arrange: Email not in activity
        Act: DELETE participant that doesn't exist in activity
        Assert: Returns 404
        """
        # Arrange
        email = "notinactivity@mergington.edu"
        activity = "Chess Club"

        # Act
        response = client.delete(
            f"/activities/{activity}/participants",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 404
        assert "not found" in response.json()["detail"]

    def test_remove_participant_activity_not_found(self, client):
        """
        Arrange: Non-existent activity
        Act: DELETE participant from non-existent activity
        Assert: Returns 404
        """
        # Arrange
        email = "test@mergington.edu"
        activity = "Nonexistent Activity"

        # Act
        response = client.delete(
            f"/activities/{activity}/participants",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 404
        assert "not found" in response.json()["detail"]

    def test_remove_multiple_participants(self, client):
        """
        Arrange: Activity with multiple participants
        Act: Remove one participant at a time
        Assert: Each removal succeeds, others remain
        """
        # Arrange
        activity = "Chess Club"
        email1 = "michael@mergington.edu"
        email2 = "daniel@mergington.edu"

        # Act - Remove first participant
        response1 = client.delete(
            f"/activities/{activity}/participants",
            params={"email": email1}
        )

        # Assert first removal
        assert response1.status_code == 200
        activities_response = client.get("/activities")
        activities = activities_response.json()
        assert email1 not in activities[activity]["participants"]
        assert email2 in activities[activity]["participants"]

        # Act - Remove second participant
        response2 = client.delete(
            f"/activities/{activity}/participants",
            params={"email": email2}
        )

        # Assert second removal
        assert response2.status_code == 200
        activities_response = client.get("/activities")
        activities = activities_response.json()
        assert email1 not in activities[activity]["participants"]
        assert email2 not in activities[activity]["participants"]

    def test_remove_and_add_same_participant(self, client):
        """
        Arrange: Participant exists in activity
        Act: Remove participant, then add them back
        Assert: Both operations succeed
        """
        # Arrange
        email = "michael@mergington.edu"
        activity = "Chess Club"

        # Act - Remove
        delete_response = client.delete(
            f"/activities/{activity}/participants",
            params={"email": email}
        )

        # Assert removed
        assert delete_response.status_code == 200
        activities_response = client.get("/activities")
        activities = activities_response.json()
        assert email not in activities[activity]["participants"]

        # Act - Add back
        signup_response = client.post(
            f"/activities/{activity}/signup",
            params={"email": email}
        )

        # Assert added back
        assert signup_response.status_code == 200
        activities_response = client.get("/activities")
        activities = activities_response.json()
        assert email in activities[activity]["participants"]

    def test_remove_participant_activity_name_with_spaces(self, client):
        """
        Arrange: Activity name with spaces (URL encoded)
        Act: DELETE with properly encoded activity name
        Assert: Works correctly with URL encoding
        """
        # Arrange
        email = "michael@mergington.edu"
        activity_display = "Chess Club"

        # Act
        response = client.delete(
            "/activities/Chess%20Club/participants",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 200
        activities_response = client.get("/activities")
        activities = activities_response.json()
        assert email not in activities[activity_display]["participants"]
