| Ενέργεια | Άρθρα | CMS posts | Evidence |
|---|---|---|---|
| Reset | 0 | 0 | GET /cms/posts → [] |
| Generate quantity 1 | 1 | 0 | GET /articles → 1 άρθρο |
| Publish ίδιο key ×2 | 1 | 1 | GET /cms/posts → 1 εγγραφή |
| Publish νέο key | 1 | 2 | GET /cms/posts → 2 εγγραφές |

## BrainfoodGPT — Χαρτογράφηση πραγματικού δείγματος

| Στοιχείο | Τι παρατηρήθηκε | Πηγή |
|---|---|---|
| Site | id:1, Alpha Music, feed_id:10 | GET /sites |
| Feed | id:10 (αναφορά μόνο, χωρίς όνομα/URL) | GET /sites response |
| Articles | κανένα | GET /articles → [] |
| Draft | δεν παρατηρήθηκε | — |
| CMS record | δεν παρατηρήθηκε | — |

**Τι δεν επαληθεύτηκε:** feed name/URL, sources, articles, drafts, CMS records.
Το περιβάλλον ήταν άδειο κατά τη στιγμή της εξέτασης (είχε γίνει reset).