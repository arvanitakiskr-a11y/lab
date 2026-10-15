"""In-process deterministic fault demonstration. Does not change the browser server."""
from fastapi.testclient import TestClient
from app import app
A={'X-Demo-Token':'alpha-demo'}
with TestClient(app) as c:
    for mode in ['normal','wrong_feed_bug','duplicate_bug']:
        c.post('/reset'); c.post('/training/mode',json={'mode':mode})
        a=c.post('/generate',json={'site_id':1,'quantity':1,'instruction':'QA'},headers=A).json()['articles'][0]
        checks={'correct_feed':a['feed_id']==10}
        h={**A,'Idempotency-Key':'demo'}
        c.post('/publish',json={'article_id':a['id']},headers=h)
        c.post('/publish',json={'article_id':a['id']},headers=h)
        checks['single_cms_post']=len(c.get('/cms/posts',headers=A).json())==1
        print(mode,checks)
        expected={'normal':{'correct_feed':True,'single_cms_post':True},
                  'wrong_feed_bug':{'correct_feed':False,'single_cms_post':True},
                  'duplicate_bug':{'correct_feed':True,'single_cms_post':False}}
        assert checks==expected[mode]
    c.post('/reset')
