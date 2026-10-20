import pytest

ALPHA = {"X-Demo-Token": "alpha-demo"}
BETA = {"X-Demo-Token": "bta-demo"}


def generate(client, **overrides):
    body = {'site_id': 1, 'quantity': 1, 'instruction': 'Γράψε στα ελληνικά'}
    body.update(overrides)
    return client.post('/generate', json=body, headers=ALPHA)


def test_two_drafts(client):
    body = {"site_id":1,"quantity":2,"instruction":"QA"}
    response = client.post("/generate",json=body,headers=ALPHA)
    assert response.status_code == 201
    articles = response.json()["articles"]
    assert len(articles)==2
    for a in articles:
        assert a["feed_id"] ==10
        assert a["status"] == "draft"
        
        


def test_wrong_authentication(client):
    body = {"site_id":1,"quantity":2,"instruction":"QA"}
    response = client.post("/generate",json=body,headers=BETA) # assigned wrong token and return us 401 UNAUTHORIZED
    assert response.status_code == 401


# path: tests/api/test_my_checks.py | ref: main
def test_get_articles(client):
    generate(client, quantity=2)  # δημιουργούμε 2 άρθρα
    response = client.get("/articles", headers=ALPHA)  # παίρνουμε τη λίστα
    assert response.status_code == 200  # αποδεικνύει ότι το endpoint υπάρχει
    assert len(response.json()['articles']) == 2  # αποδεικνύει ότι επέστρεψε τα 2 που φτιάξαμε