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