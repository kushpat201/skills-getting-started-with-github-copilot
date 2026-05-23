"""Tests for POST /activities/{activity_name}/signup endpoint."""

import pytest


class TestSignupForActivity:
    """Test suite for signing up for activities."""

    def test_signup_successful(self, client):
        """
        Arrange: Test email and activity name ready
        Act: POST /activities/Chess%20Club/signup with new email
        Assert: Returns 200, adds participant, returns success message
        """
        # Arrange
        email = "newstudent@mergington.edu"
        activity = "Chess Club"

        # Act
        response = client.post(
            f"/activities/{activity}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "Signed up" in data["message"]
        assert email in data["message"]
        assert activity in data["message"]
        
        # Verify participant was added
        activities_response = client.get("/activities")
        activities = activities_response.json()
        assert email in activities[activity]["participants"]

    def test_signup_duplicate_student_fails(self, client):
        """
        Arrange: Student already signed up for activity
        Act: POST signup for same activity with same email
        Assert: Returns 400, does not add duplicate
        """
        # Arrange
        email = "michael@mergington.edu"  # Already in Chess Club
        activity = "Chess Club"

        # Act
        response = client.post(
            f"/activities/{activity}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 400
        assert "already signed up" in response.json()["detail"]

    def test_signup_activity_not_found(self, client):
        """
        Arrange: Non-existent activity name
        Act: POST signup for non-existent activity
        Assert: Returns 404
        """
        # Arrange
        email = "newstudent@mergington.edu"
        activity = "Nonexistent Activity"

        # Act
        response = client.post(
            f"/activities/{activity}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 404
        assert "not found" in response.json()["detail"]

    def test_signup_multiple_activities(self, client):
        """
        Arrange: Same student, different activities
        Act: POST signup for Chess Club and Programming Class
        Assert: Student appears in both activities
        """
        # Arrange
        email = "multiactivity@mergington.edu"

        # Act - Sign up for first activity
        response1 = client.post(
            "/activities/Chess%20Club/signup",
            params={"email": email}
        )
        
        # Act - Sign up for second activity
        response2 = client.post(
            "/activities/Programming%20Class/signup",
            params={"email": email}
        )

        # Assert
        assert response1.status_code == 200
        assert response2.status_code == 200
        
        # Verify in both activities
        activities_response = client.get("/activities")
        activities = activities_response.json()
        assert email in activities["Chess Club"]["participants"]
        assert email in activities["Programming Class"]["participants"]

    def test_signup_activity_name_with_spaces(self, client):
        """
        Arrange: Activity name with spaces (URL encoded)
        Act: POST signup with properly encoded activity name
        Assert: Works correctly with URL encoding
        """
        # Arrange
        email = "testspaces@mergington.edu"
        activity_display = "Chess Club"

        # Act
        response = client.post(
            "/activities/Chess%20Club/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 200
        activities_response = client.get("/activities")
        activities = activities_response.json()
        assert email in activities[activity_display]["participants"]
