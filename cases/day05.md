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


# Day 05 — Bug Reports & PR Reading

## PR ##104 Analysis — mediasync.ai

PR URL: https://github.com/Brainfood-Media/mediasync.ai/pull/104

**Πρόβλημα:** Η εφαρμογή επέστρεφε `{"message":"..."}` αντί για `{"error":"..."}` σε αποτυχία ταυτοποίησης. Λείπουν βήματα αναπαραγωγής από την περιγραφή του PR — δεν αναφέρεται ποιο endpoint, ποιο token, ή ποια HTTP μέθοδος προκαλεί το πρόβλημα.

**Επίπτωση:** Όταν αποτυγχάνει η ταυτοποίηση, η εφαρμογή πρέπει να επιστρέφει HTTP 401 και κατανοητό μήνυμα στο JSON πεδίο `error`.

**Αλλαγή:** Path: `app/Exceptions/Handler.php`, head branch: `dev-alex`, commit SHA: `cda871e4f4ccf6e42f87b06feeeaf717a4fbc6f2`, μέγεθος: ένα αρχείο, έξι προσθήκες.

**Επαλήθευση:** Check runs στο head commit: 0. Commit statuses: 0, με συνολική ένδειξη pending. Το PR merged χωρίς automated checks και χωρίς review — δεν αποδείχθηκε λειτουργικά ότι το πρόβλημα διορθώθηκε.