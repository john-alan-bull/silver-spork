class TestRootEndpoint:
    """Tests for GET / endpoint"""

    def test_root_redirects_to_index_html(self, client):
        """Test that GET / redirects to /static/index.html"""
        response = client.get("/", follow_redirects=False)
        
        assert response.status_code == 307  # Temporary redirect
        assert response.headers["location"] == "/static/index.html"

    def test_root_redirect_location_is_correct(self, client):
        """Test that the redirect location is exactly /static/index.html"""
        response = client.get("/", follow_redirects=False)
        
        # The location header should point to the index.html
        assert "/static/index.html" in response.headers["location"]
