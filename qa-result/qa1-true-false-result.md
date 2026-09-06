# QA1 True/False Test Results

## Test run

- Date: September 6, 2026
- Test data: `data/qa1-true-false.csv`
- Test command: `python qa-code/test_models.py data/qa1-true-false.csv`
- Questions: 10
- Generation temperature: 0.0 (deterministic)
- Microsoft model: `mlx-community/Phi-4-mini-instruct-4bit`
- Meta model: `mlx-community/Llama-3.2-3B-Instruct-4bit`

## Summary

| Model | Correct | Incorrect | Accuracy |
| --- | ---: | ---: | ---: |
| Microsoft Phi-4 Mini | 10 | 0 | 100.0% |
| Meta Llama 3.2 3B | 9 | 1 | 90.0% |

## Detailed results

| # | Statement | Expected | Phi actual | Phi result | Llama actual | Llama result |
| ---: | --- | :---: | :---: | :---: | :---: | :---: |
| 1 | Paris is the capital of France. | True | True | PASS | True | PASS |
| 2 | The Pacific Ocean is smaller than the Atlantic Ocean. | False | False | PASS | False | PASS |
| 3 | Pure water freezes at 0 degrees Celsius at standard atmospheric pressure. | True | True | PASS | False | **FAIL** |
| 4 | Mars is the closest planet to the Sun. | False | False | PASS | False | PASS |
| 5 | A square has three sides. | False | False | PASS | False | PASS |
| 6 | An adult human body typically has 206 bones. | True | True | PASS | True | PASS |
| 7 | Light travels faster than sound. | True | True | PASS | True | PASS |
| 8 | Australia is both a country and a continent. | True | True | PASS | True | PASS |
| 9 | Mount Everest is the deepest known point in Earth's oceans. | False | False | PASS | False | PASS |
| 10 | The Python programming language was created by Guido van Rossum. | True | True | PASS | True | PASS |

## Observations

Microsoft Phi-4 Mini answered all ten questions correctly. Meta Llama 3.2 3B
answered nine correctly and incorrectly classified the statement about pure
water freezing at 0 degrees Celsius under standard atmospheric pressure as
`False`.
