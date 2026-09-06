# QA5 Algebra-Solving Test Results

## Test run

- Date: September 6, 2026
- Test data: `data/qa5-algebra-solving.csv`
- Test command: `python qa-code/test_algebra_solving.py data/qa5-algebra-solving.csv`
- Questions: 10 open-ended numeric algebra problems
- Maximum generated tokens per solution: 256
- Generation temperature: 0.0 (deterministic)
- Microsoft model: `mlx-community/Phi-4-mini-instruct-4bit`
- Meta model: `mlx-community/Llama-3.2-3B-Instruct-4bit`

## Summary

| Model | Correct | Incorrect | Accuracy |
| --- | ---: | ---: | ---: |
| Microsoft Phi-4 Mini | 10 | 0 | 100.0% |
| Meta Llama 3.2 3B | 10 | 0 | 100.0% |

## Detailed results

| # | Question | Expected | Phi actual | Phi result | Llama actual | Llama result |
| ---: | --- | ---: | ---: | :---: | ---: | :---: |
| 1 | Solve for x: x + 5 = 12. | 7 | 7 | PASS | 7 | PASS |
| 2 | Solve for x: 3x = 18. | 6 | 6 | PASS | 6 | PASS |
| 3 | Solve for x: 2x - 4 = 10. | 7 | 7 | PASS | 7 | PASS |
| 4 | Solve for x: 5(x - 2) = 20. | 6 | 6 | PASS | 6 | PASS |
| 5 | Solve for x: x/4 + 3 = 5. | 8 | 8 | PASS | 8 | PASS |
| 6 | Given x + y = 10 and x - y = 2, find x. | 6 | 6 | PASS | 6 | PASS |
| 7 | Find the larger solution of x^2 - 5x + 6 = 0. | 3 | 3 | PASS | 3 | PASS |
| 8 | Solve for x: 4(x + 1) = 2x + 10. | 3 | 3 | PASS | 3 | PASS |
| 9 | Find the slope of the line y = 4x + 2. | 4 | 4 | PASS | 4 | PASS |
| 10 | Evaluate 2x^2 - 3 when x = 3. | 15 | 15 | PASS | 15 | PASS |

## Observations

Both models answered all ten open-ended algebra questions correctly when asked
to show brief reasoning and end with a marked numeric answer.

An initial run used a 128-token output limit. Phi scored 8/10 and Llama scored
8/10 because two responses from each model reached the token limit before
emitting the required `ANSWER:` marker and were therefore unrecognized. After
raising the limit to 256 tokens, all four incomplete responses finished with
correct answers. The 256-token result is the official QA5 result because it
measures completed solutions rather than output truncation.

Llama's 10/10 score also provides more evidence for the QA4 investigation:
Llama can solve these algebra problems when prompted to reason before giving a
numeric answer, despite its all-`False` behavior under QA4's immediate binary
classification prompt.
