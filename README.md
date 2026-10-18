# Editorial QA Lab — τοπική αυτομελέτη

Ξεκίνα από το Word. Το εργαστήριο είναι υποθετικό: δεν συνδέεται σε Brainfood, Azure, WordPress ή πραγματικό μοντέλο. Τα tokens alpha-demo/beta-demo είναι δημόσια εκπαιδευτικά strings.

## Windows PowerShell
Αποσυμπίεσε το ZIP. Άνοιξε VS Code > Open Folder > lab, έπειτα Terminal > New Terminal.
```
python -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe -m playwright install chromium
.venv\Scripts\python.exe -m uvicorn app:app --host 127.0.0.1 --port 8000
```
Αν python δεν αναγνωρίζεται αλλά py λειτουργεί, χρησιμοποίησε py -3 -m venv .venv στην πρώτη εντολή.
Σε δεύτερο terminal στον ίδιο φάκελο:
```
.venv\Scripts\python.exe -m pytest -q
.venv\Scripts\python.exe -m pytest tests/browser -q --tracing retain-on-failure
.venv\Scripts\python.exe demonstrate_bugs.py
```

## macOS και Linux
Χρησιμοποίησε python3 -m venv .venv και .venv/bin/python αντί για .venv\Scripts\python.exe στις υπόλοιπες εντολές.
Σε Linux αν λείπουν λειτουργικές βιβλιοθήκες για Chromium: .venv/bin/python -m playwright install --with-deps chromium. Μπορεί να ζητηθούν δικαιώματα διαχειριστή για πακέτα συστήματος.

## Εφαρμογή
http://127.0.0.1:8000 — UI
http://127.0.0.1:8000/docs — Swagger
http://127.0.0.1:8000/health — build/mode
Μην χρησιμοποιήσεις 0.0.0.0 και μην ανεβάσεις το training app σε δημόσιο server.
Τα δεδομένα ζουν στη μνήμη. Χάνονται σε restart/reset. Δεν υπάρχουν πραγματικές ουρές, persistence ή AI παραγωγή. Η /generate δημιουργεί σταθερό εκπαιδευτικό κείμενο.

## Modes
```
.venv\Scripts\python.exe mode.py wrong_feed_bug
.venv\Scripts\python.exe mode.py duplicate_bug
.venv\Scripts\python.exe mode.py provider_down
.venv\Scripts\python.exe mode.py timeout_after_accept
.venv\Scripts\python.exe mode.py normal
```
Η POST /reset διαγράφει μόνο το training state και επαναφέρει normal. Εκτέλεσέ την από Swagger πριν από ανεξάρτητες ασκήσεις.
Τα API tests κάνουν reset σε άλλο in-process app. Δεν αλλάζουν τον server του browser. Τα browser tests κάνουν reset στον ενεργό server: μην εκτελείς παράλληλες χειροκίνητες ασκήσεις.

## Expected
Default pytest: API + data checks μόνο. Browser tests ζητούνται ρητά και απαιτούν ενεργό server. Όλα τα παραδείγματα λύσεων είναι στο tests/ και answers/. Πρώτα γράψε δικά σου expected results.
Το demonstrate_bugs.py εμφανίζει normal True/True, wrong_feed_bug False/True, duplicate_bug True/False και ολοκληρώνεται επιτυχώς επειδή επιβεβαιώνει τις αναμενόμενες εκπαιδευτικές αστοχίες.

## Άλλα αρχεία
bruno/: 3 αρχικά requests. Άνοιξε ως collection και εκτέλεσε generate πριν read.
data/: δεδομένα ημερομηνιών, editorial αξιολόγησης και φανταστικών task reports.
templates/: πρότυπα case/run/bug. Αντέγραψε πριν συμπληρώσεις.
requirements-verified.txt: εκδόσεις του περιβάλλοντος ελέγχου, για αναπαραγωγή αν χρειαστεί. Αρχικά εγκατέστησε requirements.txt· κράτησε και το δικό σου pip freeze.

Για JUnit report: python -m pytest -q --junitxml=reports/api.xml (με τον κατάλληλο interpreter).
Για trace: python -m playwright show-trace test-results/[φάκελος-αποτυχίας]/trace.zip.

## Εμπλουτισμένη εκπαίδευση

Ακολούθησε το αναθεωρημένο Word. Οι κωδικοί BrainfoodGPT και τα στοιχεία εκπαιδευτικού repository δίνονται χωριστά. Οι τοπικές ασκήσεις λειτουργούν ανεξάρτητα, ενώ οι πραγματικές MCP/worker ασκήσεις απαιτούν τις αντίστοιχες προσβάσεις.

Στο exercises γράφεις τη δική σου προσπάθεια. Στο answers/test_beginner_reference.py βρίσκεις πλήρη λυμένα παραδείγματα και το τελικό Beta σενάριο. Τρέξε τα ρητά μόνο αφού δοκιμάσεις τις ασκήσεις:

    .venv\Scripts\python.exe -m pytest answers/test_beginner_reference.py -v

Αντιγραφή templates/brainfood_context.md σε brainfood_context.md: συμπλήρωσε μη απόρρητα στοιχεία περιβάλλοντος. Το templates/qa.yml είναι παράδειγμα Actions που ενεργοποιείται μόνο στο εκπαιδευτικό repo. Δεν έχει εκτελεστεί στο δικό σου GitHub από το πακέτο. Το answers/bruno_tests.js είναι παράδειγμα για το Tests tab του Bruno, όχι αρχείο Python.

## Καθημερινή πρακτική BrainfoodGPT σε πραγματικό project

Η νέα έκδοση του Word περιλαμβάνει ενότητα «BrainfoodGPT σήμερα» σε κάθε ημέρα. Το τοπικό lab παραμένει ελεγχόμενο εκπαιδευτικό σύστημα. Παράλληλα χρησιμοποιείς τα πραγματικά repositories και δεδομένα που θα δοθούν στον λογαριασμό σου, με καταγραφή πραγματικών refs και αποτελεσμάτων.

Δημιούργησε φάκελο real_project στον χώρο εργασίας σου και αντίγραψε εκεί τα templates real_project_context.md, daily_bridge.md, real_observation.md και real_project_final.md. Συμπλήρωσε τα δικά σου στοιχεία μετά από πραγματικές αναγνώσεις και εκτελέσεις. Οι κωδικοί θα σταλούν χωριστά και δεν μπαίνουν σε αυτά τα αρχεία.

Το πρόγραμμα περιλαμβάνει θεωρητική εξήγηση κάθε εργαλείου πριν από τη χρήση του. Οι νέες ενότητες προστίθενται στις υπάρχουσες ασκήσεις και λύσεις.



## Περιβάλλον εκτέλεσης
Python: 3.13.3
OS: Windows

## RESTART
Τα άρθρα, τα CMS posts και τα idempotency keys χάνονται σε κάθε restart γιατί ζουν στη μνήμη.