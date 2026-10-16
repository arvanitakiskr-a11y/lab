# Test case
ID: Q01
Απαίτηση και πηγή κανόνα: POST /generate δέχεται instruction ελάχιστου μήκους 1
Προϋποθέσεις / mode / test account: POST /reset, normal mode, alpha-demo
Input: {"site_id":1,"quantity":1,"instruction":"x"}
Αναμενόμενο status και δεδομένα: HTTP 201,επιστρέφει 1 άρθρο με status = "draft"
Έλεγχος τελικής κατάστασης: GET /articles επιστρέφει 1 άρθρο
Καθαρισμός: POST /reset

ID: Q02
Απαίτηση και πηγή κανόνα: POST /generate δέχεται instruction μήκους 80 χαρακτήρων
Προϋποθέσεις / mode / test account: POST /reset, normal mode, alpha-demo
Input: {"site_id":1,"quantity":1,"instruction":"x*80"}
Αναμενόμενο status και δεδομένα: HTTP 201,επιστρέφει 1 άρθρο με status = "draft"
Έλεγχος τελικής κατάστασης: GET /articles επιστρέφει 1 άρθρο
Καθαρισμός: POST /reset

ID: Q03
Απαίτηση και πηγή κανόνα: POST /generate δέχεται instruction μήκους 81 χαρακτήρων
Προϋποθέσεις / mode / test account: POST /reset, normal mode, alpha-demo
Input: {"site_id":1,"quantity":1,"instruction":"x*81"}
Αναμενόμενο status και δεδομένα: HTTP 422 UNPROCESSABLE ENTITY
Έλεγχος τελικής κατάστασης: GET /articles επιστρέφει κενή λίστα
Καθαρισμός: POST /reset

ID: Q04
Απαίτηση και πηγή κανόνα: POST /generate δέχεται instruction ""
Προϋποθέσεις / mode / test account: POST /reset, normal mode, alpha-demo
Input: {"site_id":1,"quantity":1,"instruction":""}
Αναμενόμενο status και δεδομένα: 422 UNPROCESSABLE ENTITY
Έλεγχος τελικής κατάστασης: GET /articles επιστρέφει κενή λίστα
Καθαρισμός: POST /reset

ID: Q05
Απαίτηση και πηγή κανόνα: POST /generate δέχεται instruction "   "
Προϋποθέσεις / mode / test account: POST /reset, normal mode, alpha-demo
Input: {"site_id":1,"quantity":1,"instruction":"   "}
Αναμενόμενο status και δεδομένα: 422 UNPROCESSABLE ENTITY
Έλεγχος τελικής κατάστασης: GET /articles επιστρέφει κενή λίστα
Καθαρισμός: POST /reset

ID: Q06
Απαίτηση και πηγή κανόνα: POST /generate δέχεται instruction " X "
Προϋποθέσεις / mode / test account: POST /reset, normal mode, alpha-demo
Input: {"site_id":1,"quantity":1,"instruction":" X "}
Αναμενόμενο status και δεδομένα: HTTP 201,επιστρέφει 1 άρθρο με status = "draft"
Έλεγχος τελικής κατάστασης: GET /articles επιστρέφει 1 άρθρο
Καθαρισμός: POST /reset
