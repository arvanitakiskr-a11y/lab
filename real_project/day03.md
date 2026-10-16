## QUERY FIELD

| input        | category | expected status          | article count |
|--------------|----------|--------------------------|---------------|
| "abc"        | BOUNDARY | 201 Created              |1              |
| "ab"         | BELOW    | 422 Unprocessable Entity |0              |
| ""           | BELOW    | 422 Unprocessable Entity |0              |
| "x" × 4000   | BOUNDARY | 201 Created              |1              |
| "x" × 4001   | ABOVE    |422 Unprocessable Entity  |0              |
| null         | OPTIONAL | 201 CREATED              |1              |
| MISSING FIELD| OPTIONAL | 201 CREATED              |1              |
| 123          |wrong type| 422 Unprocessable Entity | 0             |


## Coverage
Κανόνας: `nullable|string|min:3|max:4000` — υπάρχει στον controller.
Test: δεν εντοπίστηκε στα tests/Feature και tests/Unit.
Εύρημα: κενό κάλυψης.
Πηγή: b4bc0b06213d0119d26d5877e9e1071b69c90879