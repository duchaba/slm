# QA16 Basic Computer Science Test Results

## Test run

- Date: September 6, 2026
- Test data: `data/qa16-computer-science.csv`
- Test command: `python qa-code/test_fill_blank.py data/qa16-computer-science.csv`
- Questions: 10 fill-in-the-blank computer science questions
- Maximum generated tokens per answer: 64
- Generation temperature: 0.0 (deterministic)
- Microsoft model: `mlx-community/Phi-4-mini-instruct-4bit`
- Meta model: `mlx-community/Llama-3.2-3B-Instruct-4bit`

## Summary

| Model | Correct | Incorrect | Accuracy |
| --- | ---: | ---: | ---: |
| Microsoft Phi-4 Mini | 9 | 1 | 90.0% |
| Meta Llama 3.2 3B | 10 | 0 | 100.0% |

## Detailed results

| # | Question | Expected | Phi actual | Phi result | Llama actual | Llama result |
| ---: | --- | --- | --- | :---: | --- | :---: |
| 1 | The primary component that executes instructions in a computer is the ___. | CPU | Central Processing Unit (CPU) | PASS | CPU | PASS |
| 2 | The two digits used in the binary number system are 0 and ___. | 1 | 1 | PASS | 1 | PASS |
| 3 | The acronym RAM stands for random access ___. | memory | Memory. | PASS | Memory | PASS |
| 4 | A finite sequence of steps for solving a problem is called an ___. | algorithm | algorithm. | PASS | algorithm | PASS |
| 5 | An error or defect in a computer program is commonly called a ___. | bug | Bug. | PASS | bug | PASS |
| 6 | The acronym HTML stands for HyperText Markup ___. | Language | HyperText Markup Language. | PASS | Language | PASS |
| 7 | A data structure that follows last in first out ordering is called a ___. | stack | Unrecognized | **FAIL** | Stack | PASS |
| 8 | The standard language commonly used to query relational databases is ___. | SQL | SQL | PASS | SQL. | PASS |
| 9 | A program that translates source code into machine code is called a ___. | compiler | compiler | PASS | Compiler | PASS |
| 10 | The smallest unit of digital information is a ___. | bit | bit. | PASS | bit | PASS |

## Grading notes

Answers were compared without regard to capitalization or punctuation. Standard
abbreviations, expanded forms, and direct synonyms were accepted where
appropriate. For example, `CPU`, `central processing unit`, `Central Processing
Unit (CPU)`, and `processor` were accepted for question 1.

The initial run did not include the combined form `Central Processing Unit
(CPU)` even though it combined two accepted answers. That form was added and
both models were rerun; this report contains the final results. `Unrecognized`
for Phi question 7 means the response omitted the required `ANSWER:` marker, so
the evaluator could not extract a gradable final answer.

## Observations

Microsoft Phi-4 Mini answered nine questions correctly, with a single
output-format failure. Meta Llama 3.2 3B answered all ten correctly and followed
the required format throughout. Every successfully extracted response from both
models was factually correct.

## Answer-key references

- [NIST Dictionary of Algorithms and Data Structures](https://xlinux.nist.gov/dads/)
  provides standard definitions for algorithms and data structures.
- [Python documentation: Using Lists as Stacks](https://docs.python.org/3/tutorial/datastructures.html#using-lists-as-stacks)
  defines stack behavior as last-in, first-out.
- [MDN: HTML](https://developer.mozilla.org/en-US/docs/Web/HTML) expands HTML as
  HyperText Markup Language.
- [PostgreSQL documentation: The SQL Language](https://www.postgresql.org/docs/current/sql.html)
  documents SQL syntax and its use for querying relational databases.
- [GCC documentation](https://gcc.gnu.org/onlinedocs/gcc/Overall-Options.html)
  describes compilation stages that translate source into assembler and machine
  code.
- [IBM: What is a CPU?](https://www.ibm.com/think/topics/central-processing-unit)
  describes the central processing unit as the computer's instruction-processing
  component.
- [NIST glossary: bit](https://csrc.nist.gov/glossary/term/bit) defines a bit as
  a binary digit represented by zero or one.
