article = {"site_id": 1, "status": "draft"}
articles = [article,article,article] 
print(article["status"]) 
print(len(articles)) 
assert article["site_id"] == 1
for item in articles:
    assert item["status"]=="draft"