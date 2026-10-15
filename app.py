"""Local learning app. Bind to loopback only. All tokens and records are fictional."""
import os
from pathlib import Path
from threading import RLock
from fastapi import FastAPI, Header, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, ConfigDict, StrictInt, field_validator

app = FastAPI(title='Editorial QA Lab', version='1.0-training')
lock = RLock()
TOKENS = {'alpha-demo': 'alpha', 'beta-demo': 'beta'}
SITES = {1: {'id': 1, 'owner': 'alpha', 'name': 'Alpha Music', 'feed_id': 10},
         2: {'id': 2, 'owner': 'beta', 'name': 'Beta Culture', 'feed_id': 20}}
SOURCES = {10: [101, 102, 103], 20: [201, 202, 203]}
ARTICLES, POSTS, KEYS = {}, {}, {}
STATE = {'mode': 'normal'}

def owner(token):
    if token not in TOKENS:
        raise HTTPException(401, 'Unknown demo token')
    return TOKENS[token]

def get_site(site_id, account):
    site = SITES.get(site_id)
    if not site or site['owner'] != account:
        raise HTTPException(404, 'Site not found')
    return site

class Generate(BaseModel):
    model_config = ConfigDict(extra='forbid')
    site_id: StrictInt
    quantity: StrictInt
    instruction: str

    @field_validator('quantity')
    @classmethod
    def check_quantity(cls, value):
        if not 1 <= value <= 3:
            raise ValueError('quantity must be 1..3')
        return value

    @field_validator('instruction')
    @classmethod
    def check_instruction(cls, value):
        value = value.strip()
        if not 1 <= len(value) <= 80:
            raise ValueError('instruction must be 1..80 chars after trim')
        return value

class Publish(BaseModel):
    model_config = ConfigDict(extra='forbid')
    article_id: StrictInt

class Mode(BaseModel):
    mode: str

@app.get('/', response_class=HTMLResponse)
def home():
    return Path(__file__).with_name('index.html').read_text(encoding='utf-8')

@app.get('/health')
def health():
    return {'status': 'ok', 'build': '1.0-training', 'mode': STATE['mode']}

@app.post('/reset')
def reset():
    # Local training endpoint only; never deploy this app on a public interface.
    with lock:
        ARTICLES.clear(); POSTS.clear(); KEYS.clear(); STATE['mode'] = 'normal'
    return {'reset': True}

@app.post('/training/mode')
def set_mode(body: Mode):
    if body.mode not in ['normal', 'provider_down', 'timeout_after_accept', 'duplicate_bug', 'wrong_feed_bug']:
        raise HTTPException(422, 'Unknown training mode')
    with lock:
        STATE['mode'] = body.mode
    return STATE.copy()

@app.get('/sites')
def sites(x_demo_token: str = Header(default='')):
    account = owner(x_demo_token)
    return [s for s in SITES.values() if s['owner'] == account]

@app.post('/generate', status_code=201)
def generate(body: Generate, x_demo_token: str = Header(default='')):
    account = owner(x_demo_token)
    site = get_site(body.site_id, account)
    with lock:
        if STATE['mode'] == 'provider_down':
            raise HTTPException(503, 'Training provider unavailable')
        feed_id = 20 if STATE['mode'] == 'wrong_feed_bug' else site['feed_id']
        created = []
        for source_id in SOURCES[feed_id][:body.quantity]:
            aid = max(ARTICLES, default=0) + 1
            item = {'id': aid, 'owner': account, 'site_id': body.site_id,
                    'feed_id': feed_id, 'source_id': source_id,
                    'instruction': body.instruction, 'status': 'draft',
                    'title': f'Άρθρο από την πηγή {source_id}',
                    'body': f'Εκπαιδευτικό κείμενο. Οδηγία: {body.instruction}'}
            ARTICLES[aid] = item
            created.append(item.copy())
        return {'articles': created}

@app.get('/articles')
def articles(x_demo_token: str = Header(default='')):
    account = owner(x_demo_token)
    with lock:
        return [a.copy() for a in ARTICLES.values() if a['owner'] == account]

@app.get('/articles/{article_id}')
def article(article_id: int, x_demo_token: str = Header(default='')):
    account = owner(x_demo_token)
    with lock:
        item = ARTICLES.get(article_id)
        if not item or item['owner'] != account:
            raise HTTPException(404, 'Article not found')
        return item.copy()

@app.post('/publish')
def publish(body: Publish, x_demo_token: str = Header(default=''),
            idempotency_key: str = Header(default='')):
    account = owner(x_demo_token)
    if not idempotency_key.strip():
        raise HTTPException(400, 'Idempotency-Key required')
    with lock:
        item = ARTICLES.get(body.article_id)
        if not item or item['owner'] != account:
            raise HTTPException(404, 'Article not found')
        key = (account, idempotency_key)
        prior = KEYS.get(key)
        if prior and prior['article_id'] != body.article_id:
            raise HTTPException(409, 'Key already used for a different article')
        if prior and STATE['mode'] != 'duplicate_bug':
            return prior.copy()
        pid = max(POSTS, default=0) + 1
        post = {'id': pid, 'article_id': body.article_id, 'site_id': item['site_id'],
                'owner': account, 'status': 'draft'}
        POSTS[pid] = post
        KEYS[key] = post
        if STATE['mode'] == 'timeout_after_accept':
            raise HTTPException(504, 'Training response lost after CMS accepted')
        return post.copy()

@app.get('/cms/posts')
def posts(x_demo_token: str = Header(default='')):
    account = owner(x_demo_token)
    with lock:
        return [x.copy() for x in POSTS.values() if x['owner'] == account]
