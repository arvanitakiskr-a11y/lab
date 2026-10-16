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