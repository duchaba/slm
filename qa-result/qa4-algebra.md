# QA4 High-School Algebra Test Results

## Test run

- Date: September 6, 2026
- Test data: `data/qa4-algebra.csv`
- Test command: `python qa-code/test_models.py data/qa4-algebra.csv`
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

## Investigation of Llama's all-`False` responses

### Checks performed

The investigation used question 1, whose correct result is easy to verify:
`x + 5 = 12` gives `x = 7`. All diagnostic runs used temperature 0.0 and the
same local Llama checkpoint.

| Diagnostic prompt | Observed behavior |
| --- | --- |
| Original prompt: classify immediately and respond with exactly `True` or `False` | Raw model output was `False.` |
| Reason first, then finish with `ANSWER: True` or `ANSWER: False` | Llama subtracted 5 from both sides, obtained `x = 7`, and finished with `ANSWER: True` |
| Two true/false examples followed by the same statement | Llama still selected `False` |
| Rephrased as `7 + 5 = 12` with a yes/no answer | Llama selected `No` |

A second reasoning-first control used the false statement that the slope of
`y = 4x + 2` is 2. Llama correctly explained that slope-intercept form makes
the slope 4 and therefore rejected the statement.

### Findings

1. **The result parser is not the cause.** The evaluator extracts the first
   standalone `True` or `False`, but the raw response to the original prompt
   was literally `False.`. The recorded label therefore matches the generated
   text.
2. **The chat template is being applied.** The local tokenizer contains the
   expected Llama instruction template, and `qa-code/test_models.py` calls
   `apply_chat_template(..., add_generation_prompt=True)` before generation.
3. **Llama can solve the sampled algebra problems.** When required to calculate
   before selecting a label, it correctly solved both a true equation and a
   false slope statement.
4. **The failure is prompt-sensitive shortcut behavior.** The current prompt
   requests an immediate label and allows only eight output tokens. For this
   QA4 dataset, the model falls into a deterministic negative-answer pattern
   instead of performing the calculation. Few-shot labels and a yes/no
   rewording did not remove that pattern, while reasoning-first prompting did.
5. **Quantization remains a possible contributor, not a proven cause.** The
   tested checkpoint is a third-party 4-bit MLX conversion of Meta's model. Its
   [Hugging Face model card](https://huggingface.co/mlx-community/Llama-3.2-3B-Instruct-4bit)
   says it was converted with MLX-LM 0.21.5. Establishing whether quantization
   changes this behavior requires comparison with Meta's original BF16 model
   or a higher-precision conversion; that control was not downloaded for this
   investigation.

### Conclusion

The 50% QA4 score measures a specific instruction-following failure under the
current immediate true/false prompt. It does **not** demonstrate that Llama
lacks basic algebra knowledge. The strongest observed cause is a prompt-induced
`False` response bias in this 4-bit checkpoint.

### Recommended follow-up

- Add a reasoning-first evaluation mode that requires a final marker such as
  `ANSWER: True` or `ANSWER: False`, then parse that final marker.
- Increase the output limit for reasoning-based tests.
- Compare results with an 8-bit or BF16 Llama checkpoint to isolate any
  quantization effect.
- Test multiple semantically equivalent prompt templates and report their
  results separately instead of relying on one forced-choice phrasing.
- Keep the original 5/10 result as the baseline so future prompt or model
  changes can be compared without rewriting history.
