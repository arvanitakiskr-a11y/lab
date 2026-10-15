// Paste into the Tests tab of the Generate request in Bruno.
// Normal mode, site 1, alpha-demo, quantity 1, instruction QA.
test("One Alpha draft", function () {
  expect(res.getStatus()).to.equal(201);
  const rows = res.getBody().articles;
  expect(rows.length).to.equal(1);
  rows.forEach(function (article) {
    expect(article.site_id).to.equal(1);
    expect(article.feed_id).to.equal(10);
    expect(article.status).to.equal("draft");
  });
});
