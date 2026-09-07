# QA1 True/False Test Results

## Test run

- Date: September 6, 2026
- Test data: `data/qa1-true-false.csv`
- Test command: `python qa-code/test_models.py data/qa1-true-false.csv`
- Questions: 10
- Generation temperature: 0.0 (deterministic)
- Response timing method: Python `time.perf_counter()` around each `generate()` call
- Timing scope: Local prompt evaluation plus answer generation; model loading and
  cleanup are measured separately
- Token-count method: Re-encode the rendered chat prompt and decoded response
  with the tokenizer belonging to the model being tested
- Microsoft model: `mlx-community/Phi-4-mini-instruct-4bit`
- Meta model: `mlx-community/Llama-3.2-3B-Instruct-4bit`

## Summary

| Model | Correct | Incorrect | Accuracy |
| --- | ---: | ---: | ---: |
| Microsoft Phi-4 Mini | 10 | 0 | 100.0% |
| Meta Llama 3.2 3B | 9 | 1 | 90.0% |

## Timing summary

All durations are wall-clock seconds from this run. Average, median, p95,
fastest, and slowest values describe the 10 individual `generate()` calls and
exclude model loading and cleanup. P95 uses linear interpolation.

| Model | Load | Responses total | Average | Median | P95 | Fastest | Slowest | Cleanup | End-to-end |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Microsoft Phi-4 Mini | 1.349 | 5.959 | 0.596 | 0.631 | 0.733 | 0.430 | 0.736 | 0.048 | 7.367 |
| Meta Llama 3.2 3B | 1.033 | 4.746 | 0.475 | 0.446 | 0.558 | 0.425 | 0.587 | 0.027 | 5.821 |

Across both models, the 20 responses took 10.705 seconds in total and averaged
0.535 seconds per question-model response. The two sequential model runs took
13.188 seconds end to end. This combined duration excludes Python process
startup before the first model timer begins.

## Token summary

Token counts are approximate because they are calculated by encoding the
rendered prompt and decoded answer after generation. A decoded answer may omit
an internal special end-of-sequence token. Counts from Phi and Llama are not
directly interchangeable because each model uses its own vocabulary and chat
template.

| Model | Input tokens | Output tokens | Combined tokens | Average per question |
| --- | ---: | ---: | ---: | ---: |
| Microsoft Phi-4 Mini | 313 | 54 | 367 | 36.7 |
| Meta Llama 3.2 3B | 655 | 29 | 684 | 68.4 |
| **Combined** | **968** | **83** | **1,051** | **52.6 per model response** |

## Detailed results

| # | Statement | Expected | Phi actual | Phi result | Phi seconds | Phi tokens in/out/total | Llama actual | Llama result | Llama seconds | Llama tokens in/out/total |
| ---: | --- | :---: | :---: | :---: | ---: | :---: | :---: | :---: | ---: | :---: |
| 1 | Paris is the capital of France. | True | True | PASS | 0.730 | 29/1/30 | True | PASS | 0.587 | 63/3/66 |
| 2 | The Pacific Ocean is smaller than the Atlantic Ocean. | False | False | PASS | 0.430 | 32/2/34 | False | PASS | 0.434 | 66/3/69 |
| 3 | Pure water freezes at 0 degrees Celsius at standard atmospheric pressure. | True | True | PASS | 0.736 | 35/8/43 | False | **FAIL** | 0.520 | 69/3/72 |
| 4 | Mars is the closest planet to the Sun. | False | False | PASS | 0.634 | 31/8/39 | False | PASS | 0.447 | 65/3/68 |
| 5 | A square has three sides. | False | False | PASS | 0.431 | 28/2/30 | False | PASS | 0.446 | 62/3/65 |
| 6 | An adult human body typically has 206 bones. | True | True | PASS | 0.635 | 32/8/40 | True | PASS | 0.425 | 66/3/69 |
| 7 | Light travels faster than sound. | True | True | PASS | 0.629 | 28/8/36 | True | PASS | 0.431 | 62/3/65 |
| 8 | Australia is both a country and a continent. | True | True | PASS | 0.632 | 31/8/39 | True | PASS | 0.438 | 65/3/68 |
| 9 | Mount Everest is the deepest known point in Earth's oceans. | False | False | PASS | 0.615 | 33/8/41 | False | PASS | 0.522 | 68/3/71 |
| 10 | The Python programming language was created by Guido van Rossum. | True | True | PASS | 0.487 | 34/1/35 | True | PASS | 0.495 | 69/2/71 |

## Observations

Microsoft Phi-4 Mini answered all ten questions correctly. Meta Llama 3.2 3B
answered nine correctly and incorrectly classified the statement about pure
water freezing at 0 degrees Celsius under standard atmospheric pressure as
`False`.

Llama's average response was 0.121 seconds faster than Phi's in this run, an
approximately 20.3% reduction relative to Phi's average. Llama used more
counted input tokens because its tokenizer and rendered chat template differ
from Phi's. Phi reached the eight-token generation ceiling on six questions;
the parser still found the requested label at the start of each response.

One short local run is not sufficient for a stable performance benchmark:
background system load,
thermal conditions, prompt length, generated-token count, and first-run model
warm-up can change the timing. Future performance comparisons should repeat
the suite multiple times and report warm and cold runs separately.

## Investigation: Why Llama uses more tokens

### Finding

Llama did not use almost twice as many tokens because the questions contained
more information. The difference is primarily fixed chat-template overhead.
Across the suite, Llama used 34 or 35 more counted input tokens than Phi on
each question:

- Phi input: 313 tokens, or 31.3 per question
- Llama input: 655 tokens, or 65.5 per question
- Difference: 342 tokens overall, or 34.2 per question after averaging the
  question-dependent tokenization

For the first question, the common instruction and statement use 26 tokens
with Phi's tokenizer and 27 with Llama's tokenizer. This one-token difference
shows that ordinary English tokenization is nearly equivalent for this sample.
The complete rendered prompts use approximately 29 Phi tokens and 63 Llama
tokens.

Phi's template is compact. It essentially surrounds the content with a user
marker, an end marker, and an assistant marker. The Llama checkpoint's bundled
template automatically adds all of the following:

- A beginning-of-text marker
- A system-role header, even when the caller supplied no system message
- `Cutting Knowledge Date: December 2023`
- A `Today Date` line
- An end-of-turn marker for the system block
- Longer user and assistant role headers and their end-of-turn marker

For the first question, the injected knowledge-cutoff and date text alone
accounts for approximately 20 Llama tokens. The remaining gap is mostly the
empty system block and Llama's more elaborate role delimiters. The exact
post-generation count also has a small measurement qualification: re-encoding
decoded text may add or omit a special token compared with the internal token
sequence.

Llama actually used fewer output tokens in this run: 29 versus Phi's 54. Phi
reached the configured eight-token output ceiling on six questions, apparently
because it continued beyond the requested label. Therefore, the overall
367-versus-684 difference is an input-template issue partially offset by Phi's
more verbose output behavior.

### Ways Llama could use fewer tokens

These are proposed experiments, not changes applied to the benchmark yet:

1. **Use a minimal Llama chat template.** Preserve Llama's official user,
   assistant, beginning-of-text, and end-of-turn tokens, but omit the empty
   system block and its date metadata. A local tokenization experiment reduced
   the first prompt from approximately 62 to 37 tokens, saving about 25 tokens
   without changing the actual question.
2. **Shorten the task instruction.** For example, `True or False only:` followed
   by the statement reduced the same minimal rendered prompt to approximately
   22 tokens. This saves more input but must be regression-tested because a
   shorter instruction may affect accuracy or output compliance.
3. **Generate only what the grader needs.** Reduce `max_tokens` from 8 to 2 or
   use a stopping condition immediately after `True` or `False`. Llama already
   averaged only 2.9 re-encoded output tokens, so the likely saving is small for
   Llama but potentially larger for Phi.
4. **Batch shared instructions where supported.** A production evaluator could
   place multiple statements in one prompt and request a numbered label list,
   paying the template and instruction overhead once. This changes the task and
   may introduce cross-question influence, parsing errors, and less useful
   per-question latency measurements.
5. **Cache the fixed prompt prefix in a server.** Prefix/KV caching can reduce
   repeated computation and latency, although it does not necessarily reduce
   the logical token count reported for each request.

The recommended first experiment is the minimal official-token template,
followed by a full accuracy rerun. It offers the largest low-risk reduction.
The optimized run should be reported separately from the existing baseline,
because changing only Llama's prompt construction would otherwise make the
comparison less controlled. If both models receive separately optimized
prompts, the project should retain a second shared-prompt benchmark for
fairness.
