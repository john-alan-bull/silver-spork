import pytest


class TestGetActivities:
    """Tests for GET /activities endpoint"""

    def test_get_activities_returns_all_activities(self, client):
        """Test that GET /activities returns all activities"""
        response = client.get("/activities")
        assert response.status_code == 200
        
        activities = response.json()
        assert "Chess Club" in activities
        assert "Programming Class" in activities
        assert "Gym Class" in activities
        assert len(activities) > 0

    def test_get_activities_returns_activity_details(self, client):
        """Test that each activity has required fields"""
        response = client.get("/activities")
        activities = response.json()
        
        chess_club = activities["Chess Club"]
        assert "description" in chess_club
        assert "schedule" in chess_club
        assert "max_participants" in chess_club
        assert "participants" in chess_club
        assert isinstance(chess_club["participants"], list)

    def test_get_activities_includes_existing_participants(self, client):
        """Test that activities include existing participants"""
        response = client.get("/activities")
        activities = response.json()
        
        chess_club = activities["Chess Club"]
        assert len(chess_club["participants"]) > 0
        assert "michael@mergington.edu" in chess_club["participants"]


class TestSignupForActivity:
    """Tests for POST /activities/{activity_name}/signup endpoint"""

    def test_signup_success(self, client):
        """Test successful signup for an activity"""
        response = client.post(
            "/activities/Chess Club/signup",
            params={"email": "newstudent@mergington.edu"}
        )
        assert response.status_code == 200
        
        result = response.json()
        assert "message" in result
        assert "newstudent@mergington.edu" in result["message"]

    def test_signup_updates_participant_list(self, client):
        """Test that signup adds student to the participants list"""
        # Sign up
        client.post(
            "/activities/Chess Club/signup",
            params={"email": "newstudent@mergington.edu"}
        )
        
        # Verify signup
        response = client.get("/activities")
        activities = response.json()
        assert "newstudent@mergington.edu" in activities["Chess Club"]["participants"]

    def test_signup_activity_not_found(self, client):
        """Test signup for non-existent activity"""
        response = client.post(
            "/activities/Nonexistent Activity/signup",
            params={"email": "newstudent@mergington.edu"}
        )
        assert response.status_code == 404
        
        result = response.json()
        assert "Activity not found" in result["detail"]

    def test_signup_already_registered(self, client):
        """Test signup fails when student is already registered"""
        response = client.post(
            "/activities/Chess Club/signup",
            params={"email": "michael@mergington.edu"}
        )
        assert response.status_code == 400
        
        result = response.json()
        assert "already signed up" in result["detail"]

    def test_signup_multiple_students(self, client):
        """Test multiple students can sign up"""
        # Sign up first student
        client.post(
            "/activities/Chess Club/signup",
            params={"email": "student1@mergington.edu"}
        )
        
        # Sign up second student
        client.post(
            "/activities/Chess Club/signup",
            params={"email": "student2@mergington.edu"}
        )
        
        # Verify both are signed up
        response = client.get("/activities")
        activities = response.json()
        participants = activities["Chess Club"]["participants"]
        assert "student1@mergington.edu" in participants
        assert "student2@mergington.edu" in participants


class TestUnregisterFromActivity:
    """Tests for DELETE /activities/{activity_name}/unregister endpoint"""

    def test_unregister_success(self, client):
        """Test successful unregister from an activity"""
        response = client.delete(
            "/activities/Chess Club/unregister",
            params={"email": "michael@mergington.edu"}
        )
        assert response.status_code == 200
        
        result = response.json()
        assert "message" in result
        assert "Unregistered" in result["message"]

    def test_unregister_removes_participant(self, client):
        """Test that unregister removes student from participants list"""
        # Unregister
        client.delete(
            "/activities/Chess Club/unregister",
            params={"email": "michael@mergington.edu"}
        )
        
        # Verify unregister
        response = client.get("/activities")
        activities = response.json()
        assert "michael@mergington.edu" not in activities["Chess Club"]["participants"]

    def test_unregister_activity_not_found(self, client):
        """Test unregister from non-existent activity"""
        response = client.delete(
            "/activities/Nonexistent Activity/unregister",
            params={"email": "student@mergington.edu"}
        )
        assert response.status_code == 404
        
        result = response.json()
        assert "Activity not found" in result["detail"]

    def test_unregister_not_signed_up(self, client):
        """Test unregister fails when student is not signed up"""
        response = client.delete(
            "/activities/Chess Club/unregister",
            params={"email": "notregistered@mergington.edu"}
        )
        assert response.status_code == 400
        
        result = response.json()
        assert "not signed up" in result["detail"]

    def test_unregister_then_signup(self, client):
        """Test can signup again after unregistering"""
        # Unregister
        client.delete(
            "/activities/Chess Club/unregister",
            params={"email": "michael@mergington.edu"}
        )
        
        # Sign up again
        response = client.post(
            "/activities/Chess Club/signup",
            params={"email": "michael@mergington.edu"}
        )
        assert response.status_code == 200
        
        # Verify
        activities_response = client.get("/activities")
        activities = activities_response.json()
        assert "michael@mergington.edu" in activities["Chess Club"]["participants"]
