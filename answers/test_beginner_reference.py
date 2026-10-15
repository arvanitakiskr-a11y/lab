"""Reference solutions: attempt the exercises BEFORE reading this file.
Run explicitly: python -m pytest answers/test_beginner_reference.py -v
"""
import pytest

ALPHA = {"X-Demo-Token": "alpha-demo"}
BETA = {"X-Demo-Token": "beta-demo"}


def test_three_drafts(client):
    # Arrange: fixture resets the application before this test.
    body = {"site_id": 1, "quantity": 3, "instruction": "QA"}
    # Act: use the real local app through TestClient.
    response = client.post("/generate", json=body, headers=ALPHA)
    # Assert: check status before reading the successful response structure.
    assert response.status_code == 201
    articles = response.json()["articles"]
    assert len(articles) == 3
    for article in articles:
        assert article["feed_id"] == 10
        assert article["status"] == "draft"


@pytest.mark.parametrize("quantity", [1, 3])
def test_valid_quantities(client, quantity):
    body = {"site_id": 1, "quantity": quantity, "instruction": "QA"}
    response = client.post("/generate", json=body, headers=ALPHA)
    assert response.status_code == 201
    assert len(response.json()["articles"]) == quantity


def test_missing_instruction(client):
    body = {"site_id": 1, "quantity": 1}
    response = client.post("/generate", json=body, headers=ALPHA)
    assert response.status_code == 422
    assert client.get("/articles", headers=ALPHA).json() == []


def test_beta_isolation(client):
    body = {"site_id": 2, "quantity": 1, "instruction": "QA"}
    created = client.post("/generate", json=body, headers=BETA)
    assert created.status_code == 201
    article_id = created.json()["articles"][0]["id"]
    assert client.get(f"/articles/{article_id}", headers=ALPHA).status_code == 404
    assert client.get("/articles", headers=ALPHA).json() == []
    headers = {**ALPHA, "Idempotency-Key": "foreign-attempt"}
    rejected = client.post("/publish", json={"article_id": article_id}, headers=headers)
    assert rejected.status_code == 404
    assert client.get("/cms/posts", headers=ALPHA).json() == []
    assert client.get("/cms/posts", headers=BETA).json() == []


def test_capstone_beta(client):
    body = {"site_id": 2, "quantity": 3, "instruction": "  Σύντομη είδηση  "}
    response = client.post("/generate", json=body, headers=BETA)
    assert response.status_code == 201
    articles = response.json()["articles"]
    assert len(articles) == 3
    assert {a["source_id"] for a in articles} == {201, 202, 203}
    for article in articles:
        assert article["site_id"] == 2
        assert article["feed_id"] == 20
        assert article["status"] == "draft"
        assert article["instruction"] == "Σύντομη είδηση"
    article_id = articles[1]["id"]
    headers = {**BETA, "Idempotency-Key": "final-beta"}
    first = client.post("/publish", json={"article_id": article_id}, headers=headers)
    second = client.post("/publish", json={"article_id": article_id}, headers=headers)
    assert first.status_code == second.status_code == 200
    assert first.json()["id"] == second.json()["id"]
    posts = client.get("/cms/posts", headers=BETA).json()
    assert len(posts) == 1
    assert posts[0]["article_id"] == article_id
    assert posts[0]["site_id"] == 2
    assert posts[0]["status"] == "draft"
    assert client.get(f"/articles/{article_id}", headers=ALPHA).status_code == 404
