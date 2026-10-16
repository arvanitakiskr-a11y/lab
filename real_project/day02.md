## Σκοπός
Ελέγχει το status ενός draft — αν είναι pending, in_progress, draft ή failed.
Δεν αλλάζει τίποτα, μόνο διαβάζει.

## Method / Path
POST /company.all/drafts/status
Χρησιμοποιεί POST παρότι μόνο διαβάζει — δεν αλλάζει τίποτα.

## Input
{
  "company_id": 1,
  "draft_id": 123
}

- company_id: σε ποια εταιρεία ανήκεις
- draft_id: ποιο draft θέλεις να ελέγξεις

## Response
HTTP 200 — η ερώτηση πέτυχε

{
  "draft_id": 123,
  "status": "pending",
  "message": "Draft generation is queued and waiting to be processed.",
  "data": null
}

HTTP 200 ≠ το draft είναι έτοιμο.
Μπορείς να πάρεις 200 με status "failed".

Όταν status = "draft":
{
  "data": {
    "title": "...",
    "summary": "...",
    "lead_text": "...",
    "content": "..."
  }
}
## Πηγή τεκμηρίωσης
Διάβασα το contract — δεν εκτελέστηκε κλήση.

Αρχεία:
- routes/api/member.php
- app/Http/Controllers/Auth/ClusterDraftController.php
- app/Http/Middleware/CompanyMiddleware.php
- Ref: b4bc0b06213d0119d26d5877e9e1071b69c90879

## Authentication
Bearer token — κάθε χρήστης βλέπει μόνο τα δικά του drafts.
Το company_id + token μαζί καθορίζουν την πρόσβαση.
Δεν μπορείς να δεις draft άλλου χρήστη από την ίδια εταιρεία.