import pytest
A={'X-Demo-Token':'alpha-demo'}

def generate(client, **overrides):
    body={'site_id':1,'quantity':1,'instruction':'Γράψε στα ελληνικά'}
    body.update(overrides)
    return client.post('/generate',json=body,headers=A)



def test_quantity(client):
    r = generate(client,quantity = 3) # we save the POST /generate with quantity 3 at r variable
    assert r.status_code == 201 # we make an assertion that r will return us HTTP status 201
    assert len(r.json()['articles']) == 4 # we make an assertion that the length of the r.json format with title articles will be equal to 4
                                            # and this is going to return as a FAILED assertion because quantity is equal to 3
                                            # in adittion if the last line is equal to 3 our assertion will be correct and will return PASS
                                            
                                            
@pytest.mark.parametrize("quantity",[1,3])
def test_quantity(client,quantity):
    r = generate(client,quantity=quantity)
    body = {"site_id":1,"instruction":"QA"}
    assert r.status_code == 201
    assert len(r.json()['articles']) == quantity

def test_missing_body(client):
    body = {"site_id":1,"instruction":"QA"}
    response = client.post("/generate", json = body, headers = A)
    assert response.status_code == 422
    
@pytest.mark.parametrize("instruction,expected",[("a"*80,201),("a"*81,422)])
def test_double_values(client,instruction,expected):
    r= generate(client,instruction=instruction)
    assert r.status_code == expected
    
    
    
@pytest.mark.parametrize("header",["fake_token"])
def test_wrong_token(client,header):
    body = {"site_id": 1, "quantity": 1, "instruction": "QA"}
    r = client.post("/generate",json=body,headers={"X-Demo-Token": header})
    assert r.status_code == 401
    
@pytest.mark.parametrize("site_id",[999])
def test_site_id(client,site_id):
    body = {"site_id":site_id,"quantity":1,"instruction":"QA"}
    r = client.post("/generate",json=body,headers = A)
    assert r.status_code == 404
    

@pytest.mark.parametrize("quantity",[2])
def test_articles_quantity(client,quantity):
    body = {"site_id":1,"quantity":quantity,"instruction":"QA"}
    b = client.post("/generate",json=body,headers=A)
    r = client.get("/articles",headers=A)
    assert b.status_code == 201
    assert len(r.json()) == 2
    
@pytest.mark.parametrize("instruction",[""])
def test_empty_instruction(client,instruction):
    body={"site_id":1,"quantity":1,"instruction":instruction}
    r=client.post("/generate",json=body,headers=A)
    assert r.status_code == 422