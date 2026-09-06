# QA18 Advanced Programming Techniques Test Results

## Test run

- Date: September 6, 2026
- Test data: `data/qa18-advanced-programming.csv`
- Test command: `python qa-code/test_fill_blank.py data/qa18-advanced-programming.csv`
- Questions: 10 fill-in-the-blank advanced programming questions
- Maximum generated tokens per answer: 64
- Generation temperature: 0.0 (deterministic)
- Microsoft model: `mlx-community/Phi-4-mini-instruct-4bit`
- Meta model: `mlx-community/Llama-3.2-3B-Instruct-4bit`

## Summary

| Model | Correct | Incorrect | Accuracy |
| --- | ---: | ---: | ---: |
| Microsoft Phi-4 Mini | 5 | 5 | 50.0% |
| Meta Llama 3.2 3B | 7 | 3 | 70.0% |

## Detailed results

| # | Question | Expected | Phi actual | Phi result | Llama actual | Llama result |
| ---: | --- | --- | --- | :---: | --- | :---: |
| 1 | Caching a function's results so repeated calls can reuse them is called ___. | memoization | Memoization. | PASS | memoization | PASS |
| 2 | An optimization that transforms certain recursive calls into iteration is tail-call ___. | optimization | optimization. | PASS | recursion. | **FAIL** |
| 3 | A function that accepts another function as an argument or returns one is a ___-order function. | higher | first-order | **FAIL** | Higher-order function. | PASS |
| 4 | A function bundled with references to its surrounding lexical environment is a ___. | closure | Unrecognized | **FAIL** | closure | PASS |
| 5 | A function that suspends execution and produces values lazily is commonly called a ___. | generator | Unrecognized | **FAIL** | generator | PASS |
| 6 | The technique of creating new immutable data structures by reusing unchanged parts is structural ___. | sharing | copy | **FAIL** | structural | **FAIL** |
| 7 | The concurrency scheduling technique in which an idle worker takes tasks from another worker is work ___. | stealing | work stealing. | PASS | stealing | PASS |
| 8 | The atomic primitive commonly abbreviated CAS means compare-and-___. | swap | swap. | PASS | swap | PASS |
| 9 | The C++ technique that ties resource lifetime to object lifetime is abbreviated ___. | RAII | RAII | PASS | RAII | PASS |
| 10 | Replacing recursive calls with returned zero-argument functions that a loop invokes is called ___. | trampolining | Tail Call Optimization. | **FAIL** | iterative | **FAIL** |

## Grading notes

Answers were compared without regard to capitalization or punctuation. Standard
abbreviations and complete phrases were accepted where equivalent, including
`TCO`, `higher-order function`, `work stealing`, `compare-and-swap`, and
`resource acquisition is initialization`.

`First-order` is the opposite of the expected higher-order function concept.
`Structural copy` and the incomplete answer `structural` do not mean structural
sharing. Tail-call optimization can eliminate some recursive stack frames, but
it is distinct from trampolining, which repeatedly invokes returned thunks.
`Iterative` describes a broad execution style rather than naming that technique.

`Unrecognized` for Phi questions 4 and 5 means the responses omitted the
required `ANSWER:` marker, leaving no extractable final answer.

## Observations

Microsoft Phi-4 Mini answered five questions correctly, with three conceptual
errors and two output-format failures. Meta Llama 3.2 3B answered seven
correctly, missing tail-call optimization, structural sharing, and
trampolining. Both models correctly answered memoization, work stealing,
compare-and-swap, and RAII.

## Investigation: Why Phi scored 50%

Phi was rerun diagnostically with the same deterministic settings, and the
complete generated text was inspected for all five failures. The low score has
two distinct causes:

| Question | Raw diagnostic response | Primary cause |
| ---: | --- | --- |
| 3 | `A function ... is a first-order function. Answer: first-order` | Concept error: a function that accepts or returns functions is higher-order, not first-order. |
| 4 | `A function ... is a closure. <answer>` | Format error only: the explanation contains the correct term, but the model copied the placeholder and omitted the required `ANSWER:` marker. |
| 5 | `A function ... is commonly called a __ Coroutine. <answer>` | Concept and format errors: coroutine is related but does not specifically name a lazy value-producing generator, and no answer marker was emitted. |
| 6 | `The technique ... is structural __copy__. Answer: copy` | Concept error: copying does not describe reuse of unchanged structure; the term is structural sharing. |
| 10 | `Replacing recursive calls ... is called ___. Answer: Tail Call Optimization.` | Concept error: tail-call optimization and trampolining are different recursion-elimination mechanisms. |

The evidence indicates that advanced terminology is the main cause: four of
the five failed responses contain an incorrect or insufficiently specific
technical term. One failure, question 4, is solely due to strict output-format
compliance. If question 4 were graded for knowledge expressed anywhere in the
response, Phi would score 6/10 rather than 5/10. Question 5 would still fail
because its stated term was `Coroutine`, not `generator`.

The 64-token generation limit did not cause the failures. Every diagnostic
response ended well before the limit, and the failures were reproduced at
temperature 0.0. The pattern is also consistent with the model's documented
constraints: Microsoft's model card describes Phi-4 Mini as a 3.8-billion-
parameter model that remains capacity-limited and says most of its code training
uses Python and common Python packages. This test instead emphasizes specialized,
language-neutral terminology from functional programming, persistent data
structures, concurrency, and C++.

The local checkpoint is 4-bit quantized, while Microsoft's original model card
describes the source weights as BF16. Quantization could affect accuracy, but
this test did not compare 4-bit and BF16 checkpoints, so it cannot establish
quantization as a cause. Likewise, ten questions are too few to support a broad
claim about Phi's overall programming ability. The supported conclusion is
limited to this QA18 question set: terminology confusion caused most lost
points, and exact-format noncompliance caused one additional lost point.

For a follow-up experiment, the clearest next tests would be to use a concrete
output example instead of the literal `<answer>` placeholder, score knowledge
separately from format compliance, and compare the 4-bit checkpoint with the
original-precision model on the same questions.

## Answer-key references

- [Python documentation: `functools.cache`](https://docs.python.org/3/library/functools.html#functools.cache)
  describes caching function results and identifies the technique as
  memoization.
- [MDN: Closures](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Closures)
  defines a closure as a function bundled with its lexical environment.
- [Python language reference: Yield expressions](https://docs.python.org/3/reference/expressions.html#yield-expressions)
  explains generator suspension and resumption.
- [Java ForkJoinPool documentation](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/util/concurrent/ForkJoinPool.html)
  documents work-stealing scheduling.
- [Java AtomicInteger documentation](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/util/concurrent/atomic/AtomicInteger.html#compareAndSet(int,int))
  documents the atomic compare-and-set operation corresponding to the CAS
  family of primitives.
- [Microsoft C++ documentation: RAII](https://learn.microsoft.com/en-us/cpp/cpp/object-lifetime-and-resource-management-modern-cpp)
  explains how RAII ties resource ownership to object lifetime.
- [Scala standard library: TailCalls](https://www.scala-lang.org/api/current/scala/util/control/TailCalls$.html)
  documents trampoline-based tail-call execution.
- [Microsoft Phi-4 Mini model card](https://huggingface.co/microsoft/Phi-4-mini-instruct)
  documents the model's 3.8-billion-parameter size, capacity limitations,
  training focus, and intended use considerations.
