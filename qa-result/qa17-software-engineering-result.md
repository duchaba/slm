# QA17 Basic Software Engineering Test Results

## Test run

- Date: September 6, 2026
- Test data: `data/qa17-software-engineering.csv`
- Test command: `python qa-code/test_fill_blank.py data/qa17-software-engineering.csv`
- Questions: 10 fill-in-the-blank software engineering questions
- Maximum generated tokens per answer: 64
- Generation temperature: 0.0 (deterministic)
- Microsoft model: `mlx-community/Phi-4-mini-instruct-4bit`
- Meta model: `mlx-community/Llama-3.2-3B-Instruct-4bit`

## Summary

| Model | Correct | Incorrect | Accuracy |
| --- | ---: | ---: | ---: |
| Microsoft Phi-4 Mini | 8 | 2 | 80.0% |
| Meta Llama 3.2 3B | 7 | 3 | 70.0% |

## Detailed results

| # | Question | Expected | Phi actual | Phi result | Llama actual | Llama result |
| ---: | --- | --- | --- | :---: | --- | :---: |
| 1 | A system that records and manages changes to source code is called ___ control. | version | version control. | PASS | source. | PASS |
| 2 | Git is an example of a distributed version control ___. | system | system. | PASS | system | PASS |
| 3 | A test that checks one small component of a program in isolation is a ___ test. | unit | Unit test. | PASS | Unit | PASS |
| 4 | The process of finding and fixing defects in software is called ___. | debugging | Quality Assurance (QA) | **FAIL** | Testing | **FAIL** |
| 5 | A needed capability that a software system must provide is called a ___. | requirement | requirement. | PASS | interface. | **FAIL** |
| 6 | The examination of source code by another developer is called code ___. | review | code review. | PASS | reverse engineering | **FAIL** |
| 7 | The practice of frequently merging and automatically testing code changes is continuous ___. | integration | Unrecognized | **FAIL** | integration | PASS |
| 8 | The acronym API stands for application programming ___. | interface | interface. | PASS | Interface | PASS |
| 9 | Improving the internal structure of code without changing its observable behavior is called ___. | refactoring | refactoring. | PASS | Refactoring. | PASS |
| 10 | The acronym SDLC stands for software development life ___. | cycle | cycle. | PASS | cycle | PASS |

## Grading notes

Answers were compared without regard to capitalization or punctuation. Standard
abbreviations and full phrases were accepted where equivalent. Both `version`
and `source` correctly complete `___ control`, so both were accepted.

Before the final run, `source` was added as an accepted completion for question
1, and question 5 was tightened to ask for a needed software capability rather
than a documented description. This report contains the results of the rerun.

`Quality Assurance (QA)` and `Testing` are broader or different processes than
finding and fixing defects, which is `debugging`. An `interface` is not itself a
needed capability, and `reverse engineering` is not peer examination of source
code. `Unrecognized` for Phi question 7 means its response omitted the required
`ANSWER:` marker.

## Observations

Microsoft Phi-4 Mini answered eight questions correctly, with one conceptual
error and one output-format failure. Meta Llama 3.2 3B answered seven correctly,
with errors on debugging, requirements, and code review. Both models correctly
answered the version control, unit testing, API, refactoring, and SDLC items.

## Answer-key references

- [Git documentation: About Version Control](https://git-scm.com/book/en/v2/Getting-Started-About-Version-Control.html)
  explains version control and identifies Git as a distributed version control
  system.
- [Python documentation: unittest](https://docs.python.org/3/library/unittest.html)
  documents unit-testing support and isolated test cases.
- [GNU Debugger documentation](https://sourceware.org/gdb/current/onlinedocs/gdb.html/)
  describes debugging programs and examining failures.
- [GitHub documentation: About pull request reviews](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/reviewing-changes-in-pull-requests/about-pull-request-reviews)
  describes reviewing and approving code changes.
- [GitHub documentation: About continuous integration](https://docs.github.com/en/actions/get-started/continuous-integration)
  explains automatically building and testing frequent code changes.
- [MDN: API](https://developer.mozilla.org/en-US/docs/Glossary/API) expands API as
  Application Programming Interface.
- [Martin Fowler: Refactoring](https://martinfowler.com/bliki/Refactoring.html)
  defines refactoring as changing internal structure without changing observable
  behavior.
- [NIST: Secure Software Development Framework](https://csrc.nist.gov/pubs/sp/800/218/final)
  places software practices within a development life cycle.
