# QA2 Basic Science Test Results

## Test run

- Date: September 6, 2026
- Test data: `data/qa2-science.csv`
- Test command: `python qa-code/test_models.py data/qa2-science.csv`
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
| 1 | The Earth revolves around the Sun. | True | True | PASS | False | **FAIL** |
| 2 | Plants use sunlight to make food through photosynthesis. | True | True | PASS | True | PASS |
| 3 | Sound can travel through the vacuum of space. | False | False | PASS | False | PASS |
| 4 | The chemical symbol for oxygen is O. | True | True | PASS | True | PASS |
| 5 | Electrons are larger than atoms. | False | False | PASS | False | PASS |
| 6 | The human heart pumps blood through the body. | True | True | PASS | True | PASS |
| 7 | Water is composed of hydrogen and oxygen. | True | True | PASS | True | PASS |
| 8 | Gravity pushes objects away from the Earth. | False | False | PASS | False | PASS |
| 9 | The Moon produces its own visible light. | False | False | PASS | False | PASS |
| 10 | Most of the Earth's atmosphere is nitrogen. | True | True | PASS | True | PASS |

## Observations

Microsoft Phi-4 Mini answered all ten basic science questions correctly. Meta
Llama 3.2 3B answered nine correctly and incorrectly classified the statement
that the Earth revolves around the Sun as `False`.
