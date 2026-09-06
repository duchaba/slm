# QA9 Basic Sports Test Results

## Test run

- Date: September 6, 2026
- Test data: `data/qa9-sport.csv`
- Test command: `python qa-code/test_fill_blank.py data/qa9-sport.csv`
- Questions: 10 fill-in-the-blank sports questions
- Maximum generated tokens per answer: 64
- Generation temperature: 0.0 (deterministic)
- Microsoft model: `mlx-community/Phi-4-mini-instruct-4bit`
- Meta model: `mlx-community/Llama-3.2-3B-Instruct-4bit`

## Summary

| Model | Correct | Incorrect | Accuracy |
| --- | ---: | ---: | ---: |
| Microsoft Phi-4 Mini | 8 | 2 | 80.0% |
| Meta Llama 3.2 3B | 10 | 0 | 100.0% |

## Detailed results

| # | Question | Expected | Phi actual | Phi result | Llama actual | Llama result |
| ---: | --- | --- | --- | :---: | --- | :---: |
| 1 | In association football a team may have a maximum of ___ players on the field. | eleven | 11 | PASS | 11 | PASS |
| 2 | A successful free throw in basketball is worth ___ point. | one | 1 | PASS | 1 | PASS |
| 3 | In baseball a batter receives a strikeout after ___ strikes. | three | three strikes | PASS | three | PASS |
| 4 | In tennis a score of zero is called ___. | love | love game | **FAIL** | Love | PASS |
| 5 | The Olympic symbol contains ___ interlocking rings. | five | Five | PASS | 5 | PASS |
| 6 | A touchdown in American football is worth ___ points. | six | six points | PASS | 6 | PASS |
| 7 | In golf a score of one under par on a hole is called a ___. | birdie | Par | **FAIL** | Birdie | PASS |
| 8 | The object struck by players in ice hockey is called a ___. | puck | puck | PASS | puck | PASS |
| 9 | In indoor volleyball each team has ___ players on the court. | six | 6 | PASS | 6 | PASS |
| 10 | The standard marathon distance in kilometers is ___. | 42.195 | 42.195 | PASS | 42.195 | PASS |

## Grading notes

Answers were compared without regard to capitalization or punctuation. Written
numbers and digits were included as accepted equivalents. Unit-inclusive forms
such as `three strikes`, `six points`, and `42.195 kilometers` were also
accepted because they preserve the correct answer.

`Love game` was not accepted for question 4. In tennis, `love` means a score of
zero, while a love game is a game won without the opponent scoring a point.
`Par` was not accepted for question 7 because one under par on a hole is a
birdie.

## Observations

Meta Llama 3.2 3B answered all ten questions correctly. Microsoft Phi-4 Mini
answered eight correctly, with one terminology error in tennis and one factual
error in golf.

## Answer-key references

- [IFAB Law 3: The Players](https://www.theifab.com/laws/latest/the-players/)
  states that an association-football team has a maximum of eleven players.
- [MLB strikeout glossary](https://www.mlb.com/glossary/standard-stats/strikeout)
  defines a strikeout in terms of three strikes.
- [ITF tennis glossary](https://www.itftennis.com/en/about-us/organisation/tennis-glossary/)
  defines `love` as zero in tennis scoring.
- [IOC Olympic Values Education Programme](https://gstatic.olympics.com/s3/mc2026/documents/Education%20Programme/OVEP/English%20Toolkit/OVEP-Fundamentals-2023%20-%20English.pdf)
  describes the Olympic symbol's five interlaced rings.
- [NFL football terms](https://operations.nfl.com/rules-officiating/nfl-football-basics/football-terms)
  states that a touchdown is worth six points.
- [IIHF ice hockey terminology](https://www.iihf.com/en/events/2026/olympic-w/static/71794/ice_hockey_terminology)
  defines the puck used in ice hockey.
- [FIVB official volleyball rules](https://www.fivb.com/wp-content/uploads/2024/03/FIVB_Volleyball_Rules_2015-2016_EN_V3_20150205.pdf)
  specify six players per team in play.
- [Olympic Studies Centre: marathon history](https://oscnewsletter.olympics.com/article/34/hidden-treasures_lang%3Den.html)
  gives the standard marathon distance as 42.195 kilometers.
