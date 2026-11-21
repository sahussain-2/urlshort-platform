from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_create_link_returns_code():
    response = client.post("/links", json={"url": "https://example.com/page"})
    assert response.status_code == 200
    data = response.json()
    assert "code" in data
    assert data["url"] == "https://example.com/page"


def test_follow_link_redirects_to_original_url():
    created = client.post("/links", json={"url": "https://example.com/page"})
    code = created.json()["code"]

    response = client.get(f"/{code}", follow_redirects=False)
    assert response.status_code == 307
    assert response.headers["location"] == "https://example.com/page"


def test_stats_counts_clicks():
    created = client.post("/links", json={"url": "https://example.com/page"})
    code = created.json()["code"]

    client.get(f"/{code}", follow_redirects=False)
    client.get(f"/{code}", follow_redirects=False)

    response = client.get(f"/links/{code}/stats")
    assert response.status_code == 200
    assert response.json()["clicks"] == 2


def test_unknown_code_returns_404():
    response = client.get("/doesnotexist", follow_redirects=False)
    assert response.status_code == 404


def test_create_link_without_url_returns_422():
    response = client.post("/links", json={})
    assert response.status_code == 422


def test_create_link_returns_short_url():
    response = client.post("/links", json={"url": "https://example.com/page"})
    data = response.json()
    assert data["short_url"].endswith("/" + data["code"])
