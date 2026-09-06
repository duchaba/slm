# QA12 Basic Literature Test Results

## Test run

- Date: September 6, 2026
- Test data: `data/qa12-literature.csv`
- Test command: `python qa-code/test_fill_blank.py data/qa12-literature.csv`
- Questions: 10 fill-in-the-blank literature questions
- Maximum generated tokens per answer: 64
- Generation temperature: 0.0 (deterministic)
- Microsoft model: `mlx-community/Phi-4-mini-instruct-4bit`
- Meta model: `mlx-community/Llama-3.2-3B-Instruct-4bit`

## Summary

| Model | Correct | Incorrect | Accuracy |
| --- | ---: | ---: | ---: |
| Microsoft Phi-4 Mini | 7 | 3 | 70.0% |
| Meta Llama 3.2 3B | 10 | 0 | 100.0% |

## Detailed results

| # | Question | Expected | Phi actual | Phi result | Llama actual | Llama result |
| ---: | --- | --- | --- | :---: | --- | :---: |
| 1 | The author of Pride and Prejudice was Jane ___. | Austen | Austen. | PASS | Austen | PASS |
| 2 | The author of the novel 1984 was George ___. | Orwell | Orwell | PASS | Orwell | PASS |
| 3 | The captain obsessed with the white whale in Moby-Dick is Captain ___. | Ahab | Ahab | PASS | Ahab | PASS |
| 4 | In Romeo and Juliet Juliet's family name is ___. | Capulet | Capulet. | PASS | Capulet. | PASS |
| 5 | The hero of Homer's Odyssey is ___. | Odysseus | Odysseus. | PASS | Odysseus. | PASS |
| 6 | The spider in Charlotte's Web is named ___. | Charlotte | Unrecognized | **FAIL** | Charlotte | PASS |
| 7 | The narrator of The Great Gatsby is Nick ___. | Carraway | Carraway | PASS | Carraway | PASS |
| 8 | The lawyer who defends Tom Robinson in To Kill a Mockingbird is Atticus ___. | Finch | Tom. | **FAIL** | Finch | PASS |
| 9 | The author of Alice's Adventures in Wonderland was Lewis ___. | Carroll | Carrol | **FAIL** | Carroll | PASS |
| 10 | The hobbit who is the main character of The Hobbit is Bilbo ___. | Baggins | Baggins | PASS | Baggins | PASS |

## Grading notes

Answers were compared without regard to capitalization or punctuation. The
answer key accepts a requested surname alone or the corresponding full name.
It also accepts `Ulysses`, the standard Latin form of `Odysseus`, for question
5.

`Unrecognized` for Phi question 6 means the response did not contain the
required `ANSWER:` marker, so the evaluator could not extract a gradable final
answer. `Tom` is not Atticus's surname, and `Carrol` is not the correct spelling
of Lewis Carroll's surname; neither was accepted.

## Observations

Microsoft Phi-4 Mini answered seven questions correctly. Its failures consisted
of one output-format failure, one incorrect surname, and one misspelling. Meta
Llama 3.2 3B answered all ten questions correctly and followed the required
answer format throughout the test.

Before this test, the reusable evaluator prompt was corrected from the
subject-specific phrase `world history question` to the neutral phrase
`question`. The grading and generation settings were otherwise unchanged.

## Answer-key references

- [The British Library: Pride and Prejudice](https://www.bl.uk/works/pride-and-prejudice)
  identifies Jane Austen as the novel's creator.
- [The Orwell Foundation: Nineteen Eighty-Four](https://www.orwellfoundation.com/the-orwell-foundation/orwell/books-by-orwell/nineteen-eighty-four/)
  identifies George Orwell and his novel.
- [Library of Congress: Moby-Dick](https://www.loc.gov/item/12006731/)
  catalogs Herman Melville's novel about Captain Ahab and the white whale.
- [Folger Shakespeare Library: Romeo and Juliet character list](https://www.folger.edu/explore/shakespeares-works/romeo-and-juliet/read/characterList/1000/)
  identifies Juliet as a Capulet.
- [British Museum: The adventures of Odysseus](https://www.britishmuseum.org/sites/default/files/2019-12/Large%20print%20guide_Troy.pdf)
  identifies Odysseus and states that his story is told in Homer's *Odyssey*.
- [Encyclopaedia Britannica: The Great Gatsby](https://www.britannica.com/topic/The-Great-Gatsby)
  identifies Nick Carraway as the novel's narrator.
- [Encyclopaedia Britannica: To Kill a Mockingbird](https://www.britannica.com/topic/To-Kill-a-Mockingbird)
  identifies Atticus Finch and Tom Robinson.
- [The British Library: Alice's Adventures in Wonderland](https://www.bl.uk/works/alices-adventures-in-wonderland)
  identifies Lewis Carroll as the book's author.
- [The Tolkien Estate: The Hobbit](https://www.tolkienestate.com/writing/the-hobbit/)
  describes Bilbo Baggins as the central hobbit in the novel.
