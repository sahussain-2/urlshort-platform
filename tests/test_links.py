from fastapi.testclient import TestClient

from app.main  import app

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
