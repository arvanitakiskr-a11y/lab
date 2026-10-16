## QUANTITY

| input | category | expected status           | article count |
|-------|----------|---------------------------|---------------|
| 0     | below    | 422 Unprocessable Entity  | 0             |
| 1     | boundary | 201 Created               | 1             |
| 3     | boundary | 201 Created               | 3             |
| 4     | above    | 422 Unprocessable Entity  | 0             |

## INSTRUCTIONS

| input       | category | expected status          | article count |
|-------------|----------|--------------------------|---------------|
| "x"         | boundary | 201 Created              | 1             |
| "   "       | below    | 422 Unprocessable Entity | 0             |
| ""          | below    | 422 Unprocessable Entity | 0             |
| "x" × 80   | boundary | 201 Created              | 1             |
| "x" × 81   | above    | 422 Unprocessable Entity | 0             |
