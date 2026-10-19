# Bug Report — Wrong Feed ID on Generate

**Τίτλος:** POST /generate returns wrong feed_id (20) for Alpha site 1  
**Training bug ή πραγματικό εύρημα:** Training bug (wrong_feed_bug mode)  
**Έκδοση / mode / περιβάλλον:** wrong_feed_bug, localhost:8000  
**Προϋποθέσεις και δεδομένα:** reset → mode wrong_feed_bug → alpha-demo token  
**Βήματα αναπαραγωγής:**  
1. POST /reset  
2. .venv\Scripts\python.exe mode.py wrong_feed_bug  
3. POST /generate quantity:1 (X-Demo-Token: alpha-demo)  
4. GET /articles  

**Αναμενόμενο:** feed_id: 10, source_id: 101–103  
**Πραγματικό:** feed_id: 20, source_id: 201–203  
**Επίπτωση / severity:** Άρθρο συνδέεται με λάθος feed — ενδέχεται να δημοσιευτεί σε λάθος site  
**Αποδεικτικά:** Response από GET /articles — feed_id: 20  
**Αιτία (επιβεβαιωμένη από κώδικα):** app.py γραμμή 92:  
`feed_id = 20 if STATE['mode'] == 'wrong_feed_bug' else site['feed_id']`  
Δεν αλλάζει το site — αλλάζει μόνο το feed που χρησιμοποιείται κατά την παραγωγή.  

**Retest:**  
1. .venv\Scripts\python.exe mode.py normal  
2. POST /reset  
3. POST /generate quantity:1  
4. GET /articles → feed_id: 10 ✓ Confirmed fixed in normal mode.

**GitHub MCP / BrainfoodGPT:**  
File: app.py — γραμμές 72–78 (set_mode), γραμμή 92 (feed_id override)
Git ref: δεν επιβεβαιώθηκε μέσω GitHub. Έκδοση εφαρμογής: 1.0-training.