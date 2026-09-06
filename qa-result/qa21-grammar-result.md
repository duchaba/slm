# QA21 Grammar Classification Test Results

## Test run

- Date: September 6, 2026
- Test data: `data/qa21-grammar.csv`
- Test command: `python qa-code/test_fill_blank.py data/qa21-grammar.csv`
- Questions: 10 standard written English grammar classifications
- Expected distribution: 5 correct and 5 incorrect sentences
- Maximum generated tokens per answer: 64
- Generation temperature: 0.0 (deterministic)
- Microsoft model: `mlx-community/Phi-4-mini-instruct-4bit`
- Meta model: `mlx-community/Llama-3.2-3B-Instruct-4bit`

## Summary

| Model | Correct | Incorrect | Accuracy |
| --- | ---: | ---: | ---: |
| Microsoft Phi-4 Mini | 10 | 0 | 100.0% |
| Meta Llama 3.2 3B | 8 | 2 | 80.0% |

## Detailed results

| # | Sentence classified | Expected | Phi actual | Phi result | Llama actual | Llama result |
| ---: | --- | --- | --- | :---: | --- | :---: |
| 1 | She walks to school every day. | correct | correct. | PASS | correct | PASS |
| 2 | They was happy to see us. | incorrect | &lt;Incorrect&gt; | PASS | incorrect | PASS |
| 3 | Neither of the answers is correct. | correct | correct. | PASS | incorrect | **FAIL** |
| 4 | I have went to that store before. | incorrect | &lt;Incorrect&gt; | PASS | incorrect | PASS |
| 5 | The books on the shelf belong to Maya. | correct | correct. | PASS | correct. | PASS |
| 6 | Each of the students have a pencil. | incorrect | incorrect. | PASS | incorrect | PASS |
| 7 | By the time we arrived the film had begun. | correct | grammatically correct. | PASS | correct. | PASS |
| 8 | He don't like cold weather. | incorrect | Incorrect. | PASS | incorrect | PASS |
| 9 | Whom did you invite to the party? | correct | correct. | PASS | correct. | PASS |
| 10 | There is many reasons to study. | incorrect | incorrect. | PASS | correct | **FAIL** |

## Grading notes

The benchmark asks whether each sentence is grammatical in standard written
English; it does not label dialectal constructions as inherently invalid in
their own contexts. Answers were compared without regard to capitalization or
punctuation. Both `correct` and `grammatically correct` were accepted, as were
`incorrect` and `grammatically incorrect`.

The initial run treated Phi's `grammatically correct` as a mismatch even though
it is directly equivalent to `correct`. Those variants were added consistently
to all rows, and both models were rerun. This report contains the final rerun.

Llama's answer to question 3 is incorrect because `neither` is singular in this
standard construction and agrees with `is`. Its answer to question 10 is also
incorrect: the plural noun phrase `many reasons` calls for `are`, yielding
`There are many reasons to study`.

## Observations

Microsoft Phi-4 Mini classified all ten sentences correctly. Meta Llama 3.2 3B
classified eight correctly, with both errors involving subject-verb agreement.
Both models correctly handled the irregular participle, past-perfect sequence,
and objective `whom` examples.

## Answer-key references

- [Purdue OWL: Subject-Verb Agreement](https://owl.purdue.edu/owl/general_writing/grammar/subject_verb_agreement.html)
  explains agreement rules for singular subjects, indefinite pronouns, and
  constructions in which words intervene between subject and verb.
- [Cambridge Grammar: Verbs—basic forms](https://dictionary.cambridge.org/grammar/british-grammar/verbs-basic-forms)
  lists the irregular forms `go`, `went`, and `gone` and explains subject-verb
  agreement.
- [British Council: Past perfect](https://learnenglish.britishcouncil.org/free-resources/grammar/b1-b2/past-perfect)
  explains use of the past perfect for an event completed before another past
  event.
- [MLA Style Center: Who versus whom](https://style.mla.org/who-versus-whom/)
  explains that `whom` is used as a verb's object, as in `whom ... invite`.
