# QA11 Basic Entertainment Test Results

## Test run

- Date: September 6, 2026
- Test data: `data/qa11-entertainment.csv`
- Test command: `python qa-code/test_fill_blank.py data/qa11-entertainment.csv`
- Questions: 10 fill-in-the-blank entertainment questions
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
| 1 | The filmmaker who created the Star Wars saga is George ___. | Lucas | Lucas | PASS | Lucas | PASS |
| 2 | Superman's home planet is ___. | Krypton | Krypton. | PASS | Krypton | PASS |
| 3 | Pixar's first feature-length computer-animated film was ___. | Toy Story | Luxo Jr. | **FAIL** | Toy Story. | PASS |
| 4 | The author of the Harry Potter book series is J. K. ___. | Rowling | Rowling. | PASS | Rowling | PASS |
| 5 | The playwright who wrote Hamlet was William ___. | Shakespeare | Shakespeare. | PASS | Shakespeare. | PASS |
| 6 | The band whose members included John Lennon and Paul McCartney was The ___. | Beatles | The Beatles. | PASS | The | **FAIL** |
| 7 | The singer known as the King of Pop was Michael ___. | Jackson | Jackson | PASS | Jackson | PASS |
| 8 | The 1997 film Titanic was directed by James ___. | Cameron | Tommy Lee Jones. | **FAIL** | James Cameron. | PASS |
| 9 | The television sitcom Friends is primarily set in ___ City. | New York | New York City | PASS | Los Angeles | **FAIL** |
| 10 | In The Wizard of Oz Dorothy's destination is the ___ City. | Emerald | Emerald City | PASS | Munchkinland. | **FAIL** |

## Grading notes

Answers were compared without regard to capitalization or punctuation. A model
could supply either the missing word or the complete name or phrase when both
forms conveyed the same answer. For example, both `Cameron` and `James Cameron`
were accepted for question 8.

The incorrect answers were not accepted as variants. `Luxo Jr.` is a Pixar
short, not its first feature-length computer-animated film. Tommy Lee Jones did
not direct *Titanic*. `The` does not identify the Beatles, *Friends* is primarily
set in New York City rather than Los Angeles, and Dorothy travels toward the
Emerald City rather than Munchkinland.

## Observations

Microsoft Phi-4 Mini answered eight questions correctly. Its two errors
confused a Pixar short with a feature film and supplied the wrong person for a
film director. Meta Llama 3.2 3B answered seven correctly. Its three errors
included one incomplete band name and two incorrect fictional or television
locations.

## Answer-key references

- [StarWars.com: Three New Star Wars Movies Announced](https://www.starwars.com/news/swce-2023-new-star-wars-films)
  attributes the creation of *Star Wars* to George Lucas.
- [DC: Superman](https://www.dc.com/characters/superman) identifies Superman as
  the last survivor of Krypton.
- [Pixar: Our Story](https://www.pixar.com/our-story) identifies *Toy Story* as
  the world's first computer-animated feature film and separately identifies
  `Luxo Jr.` as a short film.
- [Folger Shakespeare Library: Hamlet](https://www.folger.edu/explore/shakespeares-works/hamlet/)
  identifies *Hamlet* as a Shakespeare play.
- [The Beatles official site](https://www.thebeatles.com/) identifies the band
  and documents John Lennon and Paul McCartney working together.
- [Oscars: Titanic](https://www.oscars.org/collection-highlights/titanic)
  identifies the 1997 film's director as James Cameron.
