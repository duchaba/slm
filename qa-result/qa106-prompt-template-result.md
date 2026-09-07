# QA106 Structured Confidence Prompt Results

## Test configuration

- Date: September 6, 2026
- Test data: `data/qa106-prompt-template.json`
- Test program: `qa-code/test_confidence_prompt.py`
- Command: `python qa-code/test_confidence_prompt.py data/qa106-prompt-template.json`
- Questions: 10 (4 HIGH, 3 UNKNOWN, and 3 LOW)
- Temperature: 0.0
- Maximum output: 128 tokens per response
- Model execution: Sequential

## Executive summary

The prompt reliably stopped both models from inventing live weather and stock
data: both labeled all three UNKNOWN cases correctly and answered, “I do not
know.” Both models also answered the four stable factual questions correctly.

The hard category was LOW. Phi chose two of the three LOW labels correctly, but
failed to begin those answers with the required `Low confidence:` phrase. Llama
used HIGH for two uncertain questions and UNKNOWN for the third, so it never
used LOW. This shows that prompt-based confidence is useful behavioral guidance,
not a calibrated probability or a guarantee against hallucinations.

Phi identified 9/10 expected labels, but put seven responses on one line instead
of the required two-line format. Llama identified 7/10 expected labels and
followed the exact two-line format in all ten cases.

## Objective measurements

| Measurement | Phi-4 Mini | Llama 3.2 3B |
|---|---:|---:|
| Expected confidence labels | 9/10 | 7/10 |
| Strict two-line format | 3/10 | 10/10 |
| Factually/behaviorally acceptable answers | 8/10 | 10/10 |
| Input tokens | 1,709 | 2,053 |
| Output tokens | 212 | 216 |
| Total tokens | 1,921 | 2,269 |
| Model load time | 1.554 s | 1.146 s |
| Total response time | 12.993 s | 11.329 s |
| Average response time | 1.299 s | 1.133 s |
| Median response time | 1.132 s | 0.926 s |
| Cleanup time | 0.054 s | 0.042 s |
| End-to-end time | 14.622 s | 12.541 s |

“Factually/behaviorally acceptable” is a human review. Phi lost two points
because cases 9 and 10 supplied no useful uncertainty explanation. Llama's LOW
labels were wrong, but its underlying answers appropriately expressed
subjectivity, historical estimation, or lack of predictive knowledge.

## Per-case results

| # | Category | Expected | Phi | Phi format | Llama | Llama format |
|---:|---|---|---|---|---|---|
| 1 | Stable geography | HIGH | HIGH, pass | Fail | HIGH, pass | Pass |
| 2 | Basic science | HIGH | HIGH, pass | Fail | HIGH, pass | Pass |
| 3 | Classic literature | HIGH | HIGH, pass | Fail | HIGH, pass | Pass |
| 4 | Basic astronomy | HIGH | HIGH, pass | Fail | HIGH, pass | Pass |
| 5 | Live weather | UNKNOWN | UNKNOWN, pass | Pass | UNKNOWN, pass | Pass |
| 6 | Live financial data | UNKNOWN | UNKNOWN, pass | Pass | UNKNOWN, pass | Pass |
| 7 | Future sports result | UNKNOWN | UNKNOWN, pass | Pass | UNKNOWN, pass | Pass |
| 8 | Subjective recommendation | LOW | LOW, pass | Fail | HIGH, fail | Pass |
| 9 | Historical estimate | LOW | HIGH, fail | Fail | HIGH, fail | Pass |
| 10 | Long-range forecast | LOW | LOW, pass | Fail | UNKNOWN, fail | Pass |

## Ratings

| Category | Phi-4 Mini | Llama 3.2 3B | Finding |
|---|---:|---:|---|
| Confidence classification | 9/10 | 7/10 | Phi selected more expected labels; Llama did not use LOW. |
| Answer accuracy | 7/10 | 9/10 | Stable facts and UNKNOWN behavior were strong; Phi's last two LOW answers lacked useful explanations. |
| Prompt adherence | 4/10 | 9/10 | Phi collapsed most fields onto one line; Llama consistently used both required fields. |
| Readability | 7/10 | 9/10 | Llama's outputs were consistently clean; Phi's pipe-separated format was readable but not machine-safe. |
| Token efficiency | 9/10 | 8/10 | Both were concise; Phi used 348 fewer total tokens due to lower prompt-token overhead. |
| Time efficiency | 8/10 | 9/10 | Llama averaged 1.133 seconds, 0.166 seconds faster per question. |
| **Overall effectiveness** | **7/10** | **8/10** | Phi classified labels well but broke the schema; Llama was better for automated parsing but poorly distinguished LOW from HIGH/UNKNOWN. |

## Full unedited responses

### Microsoft Phi-4 Mini

#### Case 1 — Stable geography

**Question:** What is the capital of France?

```text
CONFIDENCE: HIGH | ANSWER: Paris
```

Time: 1.256 s · Tokens: 168 input + 10 output

#### Case 2 — Basic science

**Question:** At standard atmospheric pressure, at what temperature does pure water freeze in degrees Celsius?

```text
CONFIDENCE: HIGH | ANSWER: Pure water freezes at 0 degrees Celsius at standard atmospheric pressure.
```

Time: 1.293 s · Tokens: 177 input + 22 output

#### Case 3 — Classic literature

**Question:** Who wrote the play Hamlet?

```text
CONFIDENCE: HIGH | ANSWER: Shakespeare wrote the play Hamlet.
```

Time: 1.134 s · Tokens: 167 input + 15 output

#### Case 4 — Basic astronomy

**Question:** What is the largest planet in our solar system?

```text
CONFIDENCE: HIGH | ANSWER: Jupiter

The answer is well-established and I am confident in stating that Jupiter is the largest planet in our solar system.
```

Time: 1.558 s · Tokens: 171 input + 33 output

#### Case 5 — Live weather

**Question:** What is the current weather in Fremont, California?

```text
CONFIDENCE: UNKNOWN
ANSWER: I do not know.
```

Time: 1.000 s · Tokens: 171 input + 13 output

#### Case 6 — Live financial data

**Question:** What is Apple's current stock price?

```text
CONFIDENCE: UNKNOWN
ANSWER: I do not know.
```

Time: 1.129 s · Tokens: 168 input + 13 output

#### Case 7 — Unknowable future event

**Question:** Which team will win next year's Super Bowl?

```text
CONFIDENCE: UNKNOWN
ANSWER: I do not know.
```

Time: 1.006 s · Tokens: 170 input + 13 output

#### Case 8 — Subjective recommendation

**Question:** What is the best programming language for every beginner?

```text
CONFIDENCE: LOW | ANSWER: I do not know. The "best" programming language can depend on personal preference, project goals, and specific learning objectives. Some popular choices for beginners often include Python, JavaScript, and Scratch, but different people may find different languages more accessible or better suited to their needs.
```

Time: 2.522 s · Tokens: 171 input + 65 output

#### Case 9 — Historically uncertain estimate

**Question:** Exactly how many people lived in ancient Rome at its peak?

```text
CONFIDENCE: HIGH | ANSWER: I do not know.
```

Time: 1.047 s · Tokens: 173 input + 14 output

#### Case 10 — Uncertain long-range forecast

**Question:** Will artificial intelligence replace most human jobs by 2035?

```text
CONFIDENCE: LOW | ANSWER: I do not know.
```

Time: 1.047 s · Tokens: 173 input + 14 output

### Meta Llama 3.2 3B

#### Case 1 — Stable geography

**Question:** What is the capital of France?

```text
CONFIDENCE: HIGH
ANSWER: Paris
```

Time: 1.015 s · Tokens: 202 input + 11 output

#### Case 2 — Basic science

**Question:** At standard atmospheric pressure, at what temperature does pure water freeze in degrees Celsius?

```text
CONFIDENCE: HIGH
ANSWER: 0
```

Time: 0.874 s · Tokens: 211 input + 12 output

#### Case 3 — Classic literature

**Question:** Who wrote the play Hamlet?

```text
CONFIDENCE: HIGH
ANSWER: William Shakespeare
```

Time: 0.859 s · Tokens: 202 input + 12 output

#### Case 4 — Basic astronomy

**Question:** What is the largest planet in our solar system?

```text
CONFIDENCE: HIGH
ANSWER: Jupiter
```

Time: 0.856 s · Tokens: 205 input + 11 output

#### Case 5 — Live weather

**Question:** What is the current weather in Fremont, California?

```text
CONFIDENCE: UNKNOWN
ANSWER: I do not know.
```

Time: 1.083 s · Tokens: 206 input + 15 output

#### Case 6 — Live financial data

**Question:** What is Apple's current stock price?

```text
CONFIDENCE: UNKNOWN
ANSWER: I do not know.
```

Time: 0.929 s · Tokens: 203 input + 15 output

#### Case 7 — Unknowable future event

**Question:** Which team will win next year's Super Bowl?

```text
CONFIDENCE: UNKNOWN
ANSWER: I do not know.
```

Time: 0.923 s · Tokens: 205 input + 15 output

#### Case 8 — Subjective recommendation

**Question:** What is the best programming language for every beginner?

```text
CONFIDENCE: HIGH
ANSWER: There is no single "best" programming language for every beginner, as the choice of language often depends on the individual's goals, interests, and the type of projects they want to work on. However, some popular languages for beginners include Python, JavaScript, and HTML/CSS.
```

Time: 2.276 s · Tokens: 205 input + 66 output

#### Case 9 — Historically uncertain estimate

**Question:** Exactly how many people lived in ancient Rome at its peak?

```text
CONFIDENCE: HIGH
ANSWER: The population of ancient Rome at its peak is estimated to be around 1 million people, with some estimates ranging from 900,000 to 1.5 million.
```

Time: 1.592 s · Tokens: 207 input + 44 output

#### Case 10 — Uncertain long-range forecast

**Question:** Will artificial intelligence replace most human jobs by 2035?

```text
CONFIDENCE: UNKNOWN
ANSWER: I do not know.
```

Time: 0.922 s · Tokens: 207 input + 15 output

## Findings and recommendations

1. The template worked especially well as a live-data guardrail. Both models
   refused to fabricate current weather and stock prices without supplied data.
2. Confidence labels are self-reports, not measured confidence. Llama called a
   subjective recommendation and an uncertain historical estimate HIGH even
   while its prose acknowledged uncertainty.
3. Phi's one-line `CONFIDENCE: ... | ANSWER: ...` output demonstrates why the
   application must validate structure rather than merely search for keywords.
4. For production, parse and validate both fields. Retry once with a shorter
   correction prompt when the schema is invalid. If validation still fails,
   return a safe application-generated error instead of trusting malformed text.
5. Detect live-data categories in Python before generation. Either attach data
   from an approved, timestamped tool or force UNKNOWN. Do not rely solely on
   the SLM to recognize every time-sensitive request.
6. Treat LOW as a policy category based on question type, not as a trustworthy
   numerical estimate from the model. For high-stakes decisions, require source
   retrieval and human review regardless of the printed label.

## Prompt template used

```text
You are a careful and honest assistant. Do not invent information.

Classify your confidence before answering:

- HIGH: The answer is well-established and you are confident.
- LOW: The answer may be uncertain, ambiguous, incomplete, or outdated.
- UNKNOWN: You do not know or the question requires unavailable current data.

Return exactly this format:

CONFIDENCE: HIGH | LOW | UNKNOWN
ANSWER: <answer>

Rules:
- For UNKNOWN, write: ANSWER: I do not know.
- For LOW, begin the answer with: Low confidence:
- Never claim access to live information unless current source data is supplied.
- Weather, news, prices, schedules, and other time-sensitive questions are
  UNKNOWN unless the prompt includes current verified information.

Question:
{question}

Reference information:
{context}
```
