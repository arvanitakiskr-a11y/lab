Τίτλος: POST /generate return wrong article feed with value 20
Training bug ή πραγματικό εύρημα:training bug(wrong_feed_bug mode)
Έκδοση / mode / περιβάλλον:wrong_feed_bug,localhost:8000
Προϋποθέσεις και δεδομένα:reset -> wrong_feed_bug mode -> alpha-demo token
Βήματα αναπαραγωγής:1./reset 2.wrong_feed_bug mode 3.POST /generate quantity:1 4.GET/articles
Αναμενόμενο:feed_id: 10
Πραγματικό:feed_id: 20
Επίπτωση / severity:article gets connected with wrong feed - probability to be published in wrong site
Αποδεικτικά:response from GET/articles
Υπόθεση αιτίας: Server in wrong_feed_bug mode probably selects feed_id from wrong site during article generation
Retest και νέα έκδοση: mode.py normal → reset → generate → GET /articles → feed_id: 10 confirmed fixed in normal mode.

