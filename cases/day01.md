# Test case
ID: Q01
Απαίτηση και πηγή κανόνα: POST /generate δέχεται quantity 1 (ελάχιστο όριο)
Προϋποθέσεις / mode / test account: POST /reset, normal mode,alpha-demo
Input:{ "quantity": 2, "instruction": "QA" }
Βήματα: POST/reset , POST/generate με body { "quantity": 2, "instruction": "QA" } και header alpha-demo
Αναμενόμενο status και δεδομένα: HTTP 201, επιστρέφει λίστα με 2 άρθρα, status "draft"
Έλεγχος τελικής κατάστασης:GET /articles επιστρέφει ακριβώς 2 άρθρα
Καθαρισμός: POST/reset

# Test case
ID: Q02
Απαίτηση και πηγή κανόνα: POST /generate δέχεται quantity 3 (μέγιστο όριο)
Προϋποθέσεις / mode / test account: POST /reset , normal mode , alpha-demo
Input: { "quantity": 3, "instruction": "QA" }
Βήματα: POST/reset , POST/generate με body { "quantity": 3, "instruction": "QA" } και header alpha-demo
Αναμενόμενο status και δεδομένα: HTTP 201 ,επιστρέφει λίστα με 3 άρθρα , status draft
Έλεγχος τελικής κατάστασης: GET /articles επιστρέφει ακριβώς 3 άρθρα
Καθαρισμός: POST /reset

# Test case
ID:Q03
Απαίτηση και πηγή κανόνα: POST /generate απορρίπτει quantity 0 γιατί είναι κάτω από το ελάχιστο
Προϋποθέσεις / mode / test account: POST/reset,normal mode,alpha-demo
Input:{"quantity":0,"instruction:"QA"}
Βήματα: POST /reset,POST /generate με body {"quantity":0,"instruction:"QA"},και header alpha-demo
Αναμενόμενο status και δεδομένα: HTTP 422 UNPROCESSABLE CONTENT δεν δημιουργήθηκαν δεδομένα
Έλεγχος τελικής κατάστασης: GET/articles επιστρέφη κενή λίστα
Καθαρισμός: POST/reset

# Test case
ID:Q04
Απαίτηση και πηγή κανόνα: POST /generate απορρίπτει quantity 4 γιατί είναι πάνω από το μέγιστο
Προϋποθέσεις / mode / test account: POST/reset,normal mode,alpha-demo
Input:{"quantity":4,"instruction:"QA"}
Βήματα: POST /reset,POST /generate με body {"quantity":4,"instruction:"QA"},και header alpha-demo
Αναμενόμενο status και δεδομένα: HTTP 422 UNPROCESSABLE CONTENT δεν δημιουργήθηκαν δεδομένα
Έλεγχος τελικής κατάστασης: GET/articles επιστρέφη κενή λίστα
Καθαρισμός: POST/reset

# Test case
ID:Q05
Απαίτηση και πηγή κανόνα: POST /generate απορρίπτει quantity "2" γιατί string
Προϋποθέσεις / mode / test account: POST/reset,normal mode,alpha-demo
Input:{"quantity":"2","instruction:"QA"}
Βήματα: POST /reset,POST /generate με body {"quantity":"2","instruction:"QA"},και header alpha-demo
Αναμενόμενο status και δεδομένα: HTTP 422 UNPROCESSABLE CONTENT δεν δημιουργήθηκαν δεδομένα
Έλεγχος τελικής κατάστασης: GET/articles επιστρέφη κενή λίστα
Καθαρισμός: POST/reset

# Test case
ID:Q06
Απαίτηση και πηγή κανόνα: POST /generate απορρίπτει instruction "  " γιατί είναι κενό
Προϋποθέσεις / mode / test account: POST/reset,normal mode,alpha-demo
Input:{"quantity":2,"instruction:"  "}
Βήματα: POST /reset,POST /generate με body {"quantity":2,"instruction:"  "},και header alpha-demo
Αναμενόμενο status και δεδομένα: HTTP 422 UNPROCESSABLE CONTENT δεν δημιουργήθηκαν δεδομένα
Έλεγχος τελικής κατάστασης: GET/articles επιστρέφη κενή λίστα
Καθαρισμός: POST/reset



# BONUS Testcases

ID:Q07
Απαίτηση και πηγή κανόνα: POST /generate απορρίπτει quantity= true γιατί είναι boolean
Προϋποθέσεις / mode / test account: POST/reset,normal mode,alpha-demo
Input:{"quantity":true,"instruction:"QA"}
Βήματα: POST /reset,POST /generate με body {"quantity":true,"instruction:"QA"},και header alpha-demo
Αναμενόμενο status και δεδομένα: HTTP 422 UNPROCESSABLE CONTENT δεν δημιουργήθηκαν δεδομένα
Έλεγχος τελικής κατάστασης: GET/articles επιστρέφη κενή λίστα
Καθαρισμός: POST/reset

ID:Q08
Απαίτηση και πηγή κανόνα: POST /generate απορρίπτει quantity = 1.5 γιατί είναι float
Προϋποθέσεις / mode / test account: POST/reset,normal mode,alpha-demo
Input:{"quantity":1.5,"instruction:"QA"}
Βήματα: POST /reset,POST /generate με body {"quantity":1.5,"instruction:"QA"},και header alpha-demo
Αναμενόμενο status και δεδομένα: HTTP 422 UNPROCESSABLE CONTENT δεν δημιουργήθηκαν δεδομένα
Έλεγχος τελικής κατάστασης: GET/articles επιστρέφη κενή λίστα
Καθαρισμός: POST/reset


# ΑΣΚΗΣΗ ΣΧΕΔΙΑΣΜΟΥ

ID:Q09
Απαίτηση και πηγή κανόνα: POST /generate απορρίπτει instruction = "" γιατί είναι κενό
Προϋποθέσεις / mode / test account: POST/reset,normal mode,alpha-demo
Input:{"quantity":1,"instruction:""}
Βήματα: POST /reset,POST /generate με body {"quantity":1,"instruction:""},και header alpha-demo
Αναμενόμενο status και δεδομένα: HTTP 422 UNPROCESSABLE CONTENT δεν δημιουργήθηκαν δεδομένα
Έλεγχος τελικής κατάστασης: GET/articles επιστρέφη κενή λίστα
Καθαρισμός: POST/reset


ID:Q10
Απαίτηση και πηγή κανόνα: POST /generate δέχεται quantity = 3 γιατί είναι το μέγιστο
Προϋποθέσεις / mode / test account: POST/reset,normal mode,alpha-demo
Input:{"quantity":3,"instruction:"QA"}
Βήματα: POST /reset,POST /generate με body {"quantity":3,"instruction:"QA"},και header alpha-demo
Αναμενόμενο status και δεδομένα: HTTP 201 δημιουργληθηκαν 3 άρθρα
Έλεγχος τελικής κατάστασης: GET/articles επιστρέφη λίστα με 3 άρθρα
Καθαρισμός: POST/reset

ID:Q11
Απαίτηση και πηγή κανόνα: POST /generate απορρίπτει site_id=2 γιατί ο Alpha tenant δεν έχει πρόσβαση σε αυτό το site
Προϋποθέσεις / mode / test account: POST/reset,normal mode,alpha-demo
Input:{"site_id":2,"quantity":1,"instruction:"QA"}
Βήματα: POST /reset,POST /generate με body {"site_id":2,"quantity":1,"instruction:"QA"} και header alpha-demo
Αναμενόμενο status και δεδομένα: HTTP 404 το site δεν βρέθηκε
Έλεγχος τελικής κατάστασης: GET/articles επιστρέφη κενή λίστα
Καθαρισμός: POST/reset