import pytest
from app import app
from starlette.testclient import TestClient







@pytest.mark.parametrize("value",[0,4,"2",True,None,1.5])
def test_bad_quantity(client, value): 
    headers = {"X-Demo-Token": "alpha-demo"} 
    body = {"site_id": 1, "quantity": value, "instruction": "QA"}
    response = client.post("/generate", json=body, headers=headers)
    assert response.status_code == 422
    assert client.get("/articles", headers=headers).json() == []
    
    
