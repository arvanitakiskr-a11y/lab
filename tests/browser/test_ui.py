import os
import pytest
import httpx
from playwright.sync_api import expect
BASE=os.environ.get('LAB_URL','http://127.0.0.1:8000')
@pytest.fixture(autouse=True)
def reset_browser_lab():
    r=httpx.post(BASE+'/reset', trust_env=False); r.raise_for_status()
    yield
    httpx.post(BASE+'/reset', trust_env=False).raise_for_status()

def test_create_and_publish(page):
    page.goto(BASE)
    expect(page.get_by_role('status')).to_have_text('Έτοιμο')
    page.get_by_label('Πλήθος άρθρων').fill('2')
    page.get_by_role('button',name='Δημιουργία drafts',exact=True).click()
    expect(page.get_by_test_id('article')).to_have_count(2)
    page.get_by_role('button',name='Αποστολή draft 1',exact=True).click()
    expect(page.get_by_test_id('cms-post')).to_have_count(1)
    expect(page.get_by_test_id('cms-post').first).to_contain_text('site 1 | draft')
    page.get_by_role('button',name='Αποστολή draft 1',exact=True).click()
    expect(page.get_by_role('status')).to_have_text('Το draft στάλθηκε στο test CMS')
    expect(page.get_by_test_id('cms-post')).to_have_count(1)

def test_invalid_input(page):
    page.goto(BASE)
    expect(page.get_by_role('status')).to_have_text('Έτοιμο')
    page.get_by_label('Οδηγία').fill('   ')
    page.get_by_role('button',name='Δημιουργία drafts',exact=True).click()
    expect(page.get_by_role('status')).to_contain_text('HTTP 422')
    expect(page.get_by_test_id('article')).to_have_count(0)

def test_account_switch(page):
    page.goto(BASE)
    expect(page.get_by_role('status')).to_have_text('Έτοιμο')
    page.get_by_role('button',name='Δημιουργία drafts',exact=True).click()
    expect(page.get_by_test_id('article')).to_have_count(1)
    page.get_by_label('Λογαριασμός').select_option('beta-demo')
    expect(page.get_by_label('Site')).to_have_value('2')
    expect(page.get_by_test_id('article')).to_have_count(0)

def test_beta_draft(page):
    page.goto(BASE)
    page.set_viewport_size({"width": 390, "height": 844})
    page.pause()
    expect(page.get_by_role('status')).to_have_text('Έτοιμο')
    page.get_by_label('Λογαριασμός').select_option('beta-demo')
    expect(page.get_by_label('Site')).to_have_value('2')
    page.get_by_label('Πλήθος άρθρων').fill('1')
    page.get_by_role('button',name='Δημιουργία drafts',exact=True).click()
    expect(page.get_by_test_id('article')).to_have_count(1)
    expect(page.get_by_test_id('article')).to_contain_text('feed 20')
    page.get_by_role('button',name='Αποστολή draft 1',exact=True).click()
    expect(page.get_by_test_id('cms-post')).to_have_count(1)
    expect(page.get_by_role('status')).to_have_text('Το draft στάλθηκε στο test CMS')
    
