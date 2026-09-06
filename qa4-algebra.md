# QA4 High-School Algebra Test Results

## Test run

- Date: September 6, 2026
- Test data: `qa4-algebra.csv`
- Test command: `python test_models.py qa4-algebra.csv`
- Questions: 10
- Generation temperature: 0.0 (deterministic)
- Microsoft model: `mlx-community/Phi-4-mini-instruct-4bit`
- Meta model: `mlx-community/Llama-3.2-3B-Instruct-4bit`

## Summary

| Model | Correct | Incorrect | Accuracy |
| --- | ---: | ---: | ---: |
| Microsoft Phi-4 Mini | 7 | 3 | 70.0% |
| Meta Llama 3.2 3B | 5 | 5 | 50.0% |

## Detailed results

| # | Statement | Expected | Phi actual | Phi result | Llama actual | Llama result |
| ---: | --- | :---: | :---: | :---: | :---: | :---: |
| 1 | If x plus 5 equals 12 then x equals 7. | True | True | PASS | False | **FAIL** |
| 2 | The solution to 3x equals 18 is x equals 5. | False | True | **FAIL** | False | PASS |
| 3 | Expanding 2 times the quantity x plus 3 gives 2x plus 6. | True | True | PASS | False | **FAIL** |
| 4 | The expression x squared minus 9 factors as the quantity x minus 3 times the quantity x plus 3. | True | True | PASS | False | **FAIL** |
| 5 | The slope of the line y equals 4x plus 2 is 2. | False | True | **FAIL** | False | PASS |
| 6 | If 2x minus 4 equals 10 then x equals 7. | True | True | PASS | False | **FAIL** |
| 7 | The equations x plus y equals 10 and x minus y equals 2 have the solution x equals 4 and y equals 6. | False | True | **FAIL** | False | PASS |
| 8 | For every real number x the expression x squared is negative. | False | False | PASS | False | PASS |
| 9 | The quadratic equation x squared minus 5x plus 6 equals zero has solutions x equals 2 and x equals 3. | True | True | PASS | False | **FAIL** |
| 10 | The expression 3x plus 2x squared combines to 5x cubed. | False | False | PASS | False | PASS |

## Observations

Microsoft Phi-4 Mini answered seven of the ten algebra questions correctly. It
incorrectly accepted the proposed answers for `3x = 18`, the slope of
`y = 4x + 2`, and the two-equation system.

Meta Llama 3.2 3B answered `False` for all ten statements. Because the dataset
contains five true and five false answers, it scored 50%. This strong response
bias should be investigated separately from the model's underlying algebra
ability in a later QA iteration.
