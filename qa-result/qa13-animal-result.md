# QA13 Basic Animal Test Results

## Test run

- Date: September 6, 2026
- Test data: `data/qa13-animal.csv`
- Test command: `python qa-code/test_fill_blank.py data/qa13-animal.csv`
- Questions: 10 fill-in-the-blank animal questions
- Maximum generated tokens per answer: 64
- Generation temperature: 0.0 (deterministic)
- Microsoft model: `mlx-community/Phi-4-mini-instruct-4bit`
- Meta model: `mlx-community/Llama-3.2-3B-Instruct-4bit`

## Summary

| Model | Correct | Incorrect | Accuracy |
| --- | ---: | ---: | ---: |
| Microsoft Phi-4 Mini | 10 | 0 | 100.0% |
| Meta Llama 3.2 3B | 10 | 0 | 100.0% |

## Detailed results

| # | Question | Expected | Phi actual | Phi result | Llama actual | Llama result |
| ---: | --- | --- | --- | :---: | --- | :---: |
| 1 | The largest animal on Earth is the blue ___. | whale | blue whale. | PASS | blue whale | PASS |
| 2 | The fastest land animal is the ___. | cheetah | cheetah | PASS | cheetah | PASS |
| 3 | The only mammals capable of true sustained flight are ___. | bats | bats | PASS | Bats. | PASS |
| 4 | A giant panda's primary food is ___. | bamboo | bamboo. | PASS | bamboo | PASS |
| 5 | An animal such as a frog that can live on land and in water is an ___. | amphibian | Amphibian | PASS | amphibian | PASS |
| 6 | A baby kangaroo is called a ___. | joey | joey. | PASS | joey | PASS |
| 7 | A social group of lions is called a ___. | pride | pride | PASS | pride | PASS |
| 8 | An octopus has ___ arms. | eight | Eight. | PASS | Eight | PASS |
| 9 | Emperor penguins live naturally on the continent of ___. | Antarctica | Antarctica. | PASS | Antarctica | PASS |
| 10 | The process by which a caterpillar changes into a butterfly is called ___. | metamorphosis | metamorphosis. | PASS | Metamorphosis. | PASS |

## Grading notes

Answers were compared without regard to capitalization or punctuation. The
answer key accepts `blue whale` as well as the missing word `whale`, singular
and plural forms of `bat`, and both `eight` and `8`. Both models followed the
required `ANSWER:` output format for every question.

## Observations

Microsoft Phi-4 Mini and Meta Llama 3.2 3B each answered all ten questions
correctly. No knowledge, formatting, parsing, or grading failures occurred in
this test.

## Answer-key references

- [NOAA Fisheries: Blue Whale](https://www.fisheries.noaa.gov/species/blue-whale/science?page=0)
  identifies the blue whale as the largest animal on Earth.
- [Smithsonian Institution: Bat Facts](https://www.si.edu/spotlight/bats/batfacts)
  explains that bats are the only mammals capable of true powered flight.
- [Smithsonian's National Zoo: Giant Panda FAQs](https://nationalzoo.si.edu/animals/giant-panda-faqs)
  states that wild giant pandas almost exclusively eat bamboo.
- [San Diego Zoo Wildlife Alliance: Cheetah](https://animals.sandiegozoo.org/animals/cheetah)
  identifies the cheetah as the fastest land animal.
- [Smithsonian's National Zoo: Amphibians](https://nationalzoo.si.edu/animals/amphibians)
  describes amphibians and their life in aquatic and terrestrial habitats.
- [Australian Museum: Kangaroos and wallabies](https://australian.museum/learn/animals/mammals/kangaroos-and-wallabies/)
  uses `joey` for a young kangaroo.
- [Smithsonian's National Zoo: Lion](https://nationalzoo.si.edu/animals/lion)
  describes the lion's social group as a pride.
- [Smithsonian Ocean: Octopuses](https://ocean.si.edu/ocean-life/invertebrates/octopuses)
  describes the octopus's eight arms.
- [Australian Antarctic Program: Emperor penguin](https://www.antarctica.gov.au/about-antarctica/animals/penguins/emperor-penguin/)
  documents emperor penguin colonies around Antarctica.
- [USDA: Butterfly metamorphosis](https://www.fs.usda.gov/wildflowers/pollinators/animals/butterflies.shtml)
  describes the complete metamorphosis from egg through caterpillar and pupa to
  adult butterfly.
