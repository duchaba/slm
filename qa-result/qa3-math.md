# QA3 Basic Math Test Results

## Test run

- Date: September 6, 2026
- Test data: `data/qa3-math.csv`
- Test command: `python qa-code/test_models.py data/qa3-math.csv`
- Questions: 10
- Generation temperature: 0.0 (deterministic)
- Microsoft model: `mlx-community/Phi-4-mini-instruct-4bit`
- Meta model: `mlx-community/Llama-3.2-3B-Instruct-4bit`

## Summary

| Model | Correct | Incorrect | Accuracy |
| --- | ---: | ---: | ---: |
| Microsoft Phi-4 Mini | 8 | 2 | 80.0% |
| Meta Llama 3.2 3B | 5 | 5 | 50.0% |

## Detailed results

| # | Statement | Expected | Phi actual | Phi result | Llama actual | Llama result |
| ---: | --- | :---: | :---: | :---: | :---: | :---: |
| 1 | Two plus three equals five. | True | True | PASS | False | **FAIL** |
| 2 | Ten minus four equals seven. | False | False | PASS | False | PASS |
| 3 | Six multiplied by seven equals forty-two. | True | False | **FAIL** | False | **FAIL** |
| 4 | Twenty divided by five equals four. | True | True | PASS | False | **FAIL** |
| 5 | The square root of eighty-one is nine. | True | False | **FAIL** | False | **FAIL** |
| 6 | One half is greater than three quarters. | False | False | PASS | False | PASS |
| 7 | A triangle has four sides. | False | False | PASS | False | PASS |
| 8 | The sum of the interior angles of a triangle is 180 degrees. | True | True | PASS | True | PASS |
| 9 | Eleven is an even number. | False | False | PASS | False | PASS |
| 10 | Five squared equals twenty-five. | True | True | PASS | False | **FAIL** |

## Observations

Microsoft Phi-4 Mini answered eight of the ten basic math questions correctly.
It incorrectly classified the multiplication and square-root statements as
`False`.

Meta Llama 3.2 3B answered five questions correctly. It answered `False` for
nine of the ten statements, including five statements whose expected answer
was `True`. This result indicates a response bias or instruction-following
issue worth investigating in a later QA iteration; it should not be interpreted
as a general measurement of the model's mathematical capability.
