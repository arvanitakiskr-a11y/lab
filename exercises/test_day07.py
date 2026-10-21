import pytest
from app import app
from starlette.testclient import TestClient
A={'X-Demo-Token':'alpha-demo'}







@pytest.mark.parametrize("value",[0,4,"2",True,None,1.5])
def test_bad_quantity(client, value): 
    headers = {"X-Demo-Token": "alpha-demo"} 
    body = {"site_id": 1, "quantity": value, "instruction": "QA"}
    response = client.post("/generate", json=body, headers=headers)
    assert response.status_code == 422
    assert client.get("/articles", headers=headers).json() == []
    
    
@pytest.mark.parametrize("quantity",[1,3])
def test_valid_quantities(client,quantity):
    body = {"site_id":1,"quantity":quantity,"instruction":"QA"}
    r = client.post("/generate",json=body,headers=A)
    assert r.status_code == 201
    assert len(r.json()["articles"]) == quantity