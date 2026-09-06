# QA6 World History Fill-in-the-Blank Test Results

## Test run

- Date: September 6, 2026
- Test data: `qa6-world-history.csv`
- Test command: `python test_fill_blank.py qa6-world-history.csv`
- Questions: 10 fill-in-the-blank world-history questions
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
| 1 | The Great Wall was built primarily in the country of ___. | China | China | PASS | China | PASS |
| 2 | The European Renaissance began in the city-states of modern-day ___. | Italy | Florence | **FAIL** | Italy | PASS |
| 3 | The first emperor of the Roman Empire was ___. | Augustus | Augustus | PASS | Augustus | PASS |
| 4 | The Magna Carta was sealed in 1215 in the kingdom of ___. | England | England | PASS | England | PASS |
| 5 | The French Revolution began in the year ___. | 1789 | 1789 | PASS | 1789 | PASS |
| 6 | The ancient civilization that built the pyramids at Giza was the ___. | Egyptians | Ancient Egypt | PASS | Egyptian | PASS |
| 7 | World War I ended in the year ___. | 1918 | 1918 | PASS | 1918 | PASS |
| 8 | The capital of the Inca Empire was ___. | Cusco | Cusco | PASS | Cuzco | PASS |
| 9 | The European movable-type printing press is associated with Johannes ___. | Gutenberg | Johannes Gutenberg | PASS | Gutenberg | PASS |
| 10 | The capital of the Byzantine Empire was ___. | Constantinople | Constantinople | PASS | Constantinople | PASS |

## Grading notes

Answers were compared without regard to capitalization or punctuation. The
dataset also lists accepted equivalents for answers with common variants:

- `Augustus` and `Augustus Caesar`
- `Egyptians`, `Ancient Egyptians`, `Egypt`, `Ancient Egypt`, `Egyptian`, and
  `Egyptian civilization`
- `Cusco` and `Cuzco`
- `Gutenberg` and `Johannes Gutenberg`

## Observations

Meta Llama 3.2 3B answered all ten questions correctly. Microsoft Phi-4 Mini
answered nine correctly. For the question asking for the modern-day country in
which the Renaissance began, Phi supplied `Florence`, which is a city in the
expected country of Italy and therefore did not satisfy the blank.
