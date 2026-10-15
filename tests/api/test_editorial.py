import pytest
A={'X-Demo-Token':'alpha-demo'}
B={'X-Demo-Token':'beta-demo'}
def generate(client, **overrides):
    body={'site_id':1,'quantity':1,'instruction':'Γράψε στα ελληνικά'}
    body.update(overrides)
    return client.post('/generate',json=body,headers=A)

def test_create_read(client):
    r=generate(client, quantity=2)
    assert r.status_code==201
    rows=r.json()['articles']
    assert len(rows)==2
    assert {a['source_id'] for a in rows}=={101,102}
    for a in rows:
        assert a['site_id']==1 and a['feed_id']==10 and a['status']=='draft'
        stored=client.get('/articles/'+str(a['id']),headers=A)
        assert stored.status_code==200
        assert stored.json()==a
    assert len(client.get('/articles',headers=A).json())==2

@pytest.mark.parametrize('quantity',[0,4,'2',True,None,1.5])
def test_invalid_quantity(client,quantity):
    assert generate(client,quantity=quantity).status_code==422
    assert client.get('/articles',headers=A).json()==[]

@pytest.mark.parametrize('instruction',['','   ','x'*81,None,123])
def test_invalid_instruction(client,instruction):
    assert generate(client,instruction=instruction).status_code==422
    assert client.get('/articles',headers=A).json()==[]

@pytest.mark.parametrize('size',[1,80])
def test_instruction_boundary(client,size):
    r=generate(client,instruction='x'*size)
    assert r.status_code==201
    assert len(r.json()['articles'][0]['instruction'])==size

def test_trim(client):
    assert generate(client,instruction='  QA  ').json()['articles'][0]['instruction']=='QA'

def test_missing_and_extra(client):
    assert client.post('/generate',json={'site_id':1,'quantity':1},headers=A).status_code==422
    assert generate(client,extra='x').status_code==422

def test_access(client):
    assert client.get('/sites').status_code==401
    assert [s['id'] for s in client.get('/sites',headers=A).json()]==[1]
    assert generate(client,site_id=2).status_code==404
    aid=generate(client).json()['articles'][0]['id']
    assert client.get(f'/articles/{aid}',headers=B).status_code==404
    assert client.get('/articles',headers=B).json()==[]
    assert client.post('/publish',json={'article_id':aid},headers={**B,'Idempotency-Key':'b'}).status_code==404

def test_provider_down(client):
    client.post('/training/mode',json={'mode':'provider_down'})
    assert generate(client).status_code==503
    assert client.get('/articles',headers=A).json()==[]

def test_publish_idempotent(client):
    aid=generate(client).json()['articles'][0]['id']
    h={**A,'Idempotency-Key':'retry-1'}
    r1=client.post('/publish',json={'article_id':aid},headers=h)
    r2=client.post('/publish',json={'article_id':aid},headers=h)
    assert r1.status_code==r2.status_code==200
    assert r1.json()['id']==r2.json()['id']
    posts=client.get('/cms/posts',headers=A).json()
    assert len(posts)==1 and posts[0]['status']=='draft' and posts[0]['site_id']==1

def test_lost_response(client):
    aid=generate(client).json()['articles'][0]['id']
    client.post('/training/mode',json={'mode':'timeout_after_accept'})
    h={**A,'Idempotency-Key':'lost-1'}
    assert client.post('/publish',json={'article_id':aid},headers=h).status_code==504
    assert len(client.get('/cms/posts',headers=A).json())==1
    r=client.post('/publish',json={'article_id':aid},headers=h)
    assert r.status_code==200
    assert len(client.get('/cms/posts',headers=A).json())==1

def test_key_conflict(client):
    rows=generate(client,quantity=2).json()['articles']
    h={**A,'Idempotency-Key':'same'}
    assert client.post('/publish',json={'article_id':rows[0]['id']},headers=A).status_code==400
    assert client.post('/publish',json={'article_id':rows[0]['id']},headers=h).status_code==200
    assert client.post('/publish',json={'article_id':rows[1]['id']},headers=h).status_code==409
    assert len(client.get('/cms/posts',headers=A).json())==1

def test_separate_keys_create_separate_posts(client):
    # Contract intentionally deduplicates by key, NOT globally by article.
    aid=generate(client).json()['articles'][0]['id']
    for key in ['one','two']:
        assert client.post('/publish',json={'article_id':aid},headers={**A,'Idempotency-Key':key}).status_code==200
    assert len(client.get('/cms/posts',headers=A).json())==2
