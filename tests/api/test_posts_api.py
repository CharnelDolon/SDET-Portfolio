import pytest
import requests
from utils.config import API_BASE_URL


BASE = API_BASE_URL


@pytest.mark.api
@pytest.mark.smoke
class TestPostsAPI:

    def test_get_all_posts_returns_200(self):
        """GET /posts returns HTTP 200."""
        r = requests.get(f"{BASE}/posts")
        assert r.status_code == 200

    def test_get_all_posts_returns_list(self):
        """GET /posts returns a non-empty list."""
        r = requests.get(f"{BASE}/posts")
        data = r.json()
        assert isinstance(data, list)
        assert len(data) > 0

    def test_get_single_post(self):
        """GET /posts/1 returns the correct post structure."""
        r = requests.get(f"{BASE}/posts/1")
        assert r.status_code == 200
        post = r.json()
        assert "id" in post
        assert "title" in post
        assert "body" in post
        assert "userId" in post

    def test_create_post(self):
        """POST /posts returns 201 and echoes back the payload."""
        payload = {"title": "Test post", "body": "Test body", "userId": 1}
        r = requests.post(f"{BASE}/posts", json=payload)
        assert r.status_code == 201
        data = r.json()
        assert data["title"] == payload["title"]
        assert "id" in data

    def test_update_post(self):
        """PUT /posts/1 returns 200 and the updated title."""
        payload = {"id": 1, "title": "Updated title", "body": "Updated body", "userId": 1}
        r = requests.put(f"{BASE}/posts/1", json=payload)
        assert r.status_code == 200
        assert r.json()["title"] == "Updated title"

    def test_delete_post(self):
        """DELETE /posts/1 returns 200."""
        r = requests.delete(f"{BASE}/posts/1")
        assert r.status_code == 200

    def test_post_not_found(self):
        """GET /posts/99999 returns 404."""
        r = requests.get(f"{BASE}/posts/99999")
        assert r.status_code == 404


@pytest.mark.api
@pytest.mark.regression
class TestPostsSchema:

    def test_post_schema(self):
        """Every post in /posts has the required fields and correct types."""
        r = requests.get(f"{BASE}/posts")
        posts = r.json()
        for post in posts:
            assert isinstance(post["id"], int)
            assert isinstance(post["userId"], int)
            assert isinstance(post["title"], str)
            assert isinstance(post["body"], str)
            assert len(post["title"]) > 0

    def test_filter_posts_by_user(self):
        """GET /posts?userId=1 returns only posts for that user."""
        r = requests.get(f"{BASE}/posts", params={"userId": 1})
        posts = r.json()
        assert all(p["userId"] == 1 for p in posts)
