# QA20 Basic Gardening Test Results

## Test run

- Date: September 6, 2026
- Test data: `data/qa20-gardening.csv`
- Test command: `python qa-code/test_fill_blank.py data/qa20-gardening.csv`
- Questions: 10 fill-in-the-blank gardening questions
- Maximum generated tokens per answer: 64
- Generation temperature: 0.0 (deterministic)
- Microsoft model: `mlx-community/Phi-4-mini-instruct-4bit`
- Meta model: `mlx-community/Llama-3.2-3B-Instruct-4bit`

## Summary

| Model | Correct | Incorrect | Accuracy |
| --- | ---: | ---: | ---: |
| Microsoft Phi-4 Mini | 5 | 5 | 50.0% |
| Meta Llama 3.2 3B | 8 | 2 | 80.0% |

## Detailed results

| # | Question | Expected | Phi actual | Phi result | Llama actual | Llama result |
| ---: | --- | --- | --- | :---: | --- | :---: |
| 1 | Decomposed organic material added to improve garden soil is called ___. | compost | compost. | PASS | compost | PASS |
| 2 | A layer of material spread over soil to conserve moisture and suppress weeds is called ___. | mulch | mulch. | PASS | Mulch. | PASS |
| 3 | The removal of unwanted plants from a garden is called ___. | weeding | Unrecognized | **FAIL** | Weeding. | PASS |
| 4 | Cutting selected branches or stems to improve a plant's growth is called ___. | pruning | Unrecognized | **FAIL** | Pruning. | PASS |
| 5 | A plant that completes its life cycle in one growing season is an ___. | annual | annual | PASS | perennial. | **FAIL** |
| 6 | A plant that lives and grows for more than two years is a ___. | perennial | mature perennial. | **FAIL** | perennial | PASS |
| 7 | Gradually acclimating indoor-grown seedlings to outdoor conditions is called hardening ___. | off | INDOOR. | **FAIL** | offening | **FAIL** |
| 8 | Removing faded or spent flowers from a plant is called ___. | deadheading | Unrecognized | **FAIL** | Deadheading | PASS |
| 9 | Moving a plant from one growing location to another is called ___. | transplanting | transplanting. | PASS | Transplanting. | PASS |
| 10 | On a fertilizer label the letter N represents ___. | nitrogen | Nitrogen. | PASS | nitrogen | PASS |

## Grading notes

Answers were compared without regard to capitalization or punctuation. Complete
phrases were accepted when directly equivalent, including `annual plant`,
`perennial plant`, and `hardening off`.

`Unrecognized` means Phi omitted the required `ANSWER:` marker, so the evaluator
could not extract a final answer for questions 3, 4, and 8. `Mature perennial`
was not accepted because living for more than two years identifies a perennial
but does not establish that the individual plant is mature. `INDOOR` and
`offening` do not correctly complete the established term `hardening off`.
Llama's `perennial` answer for a one-season life cycle is incorrect.

## Observations

Microsoft Phi-4 Mini answered five questions correctly. Three of its five
failures were output-format failures, one added an unsupported qualifier, and
one supplied an incorrect word. Meta Llama 3.2 3B answered eight correctly,
missing the annual and hardening-off questions. Both models correctly answered
compost, mulch, transplanting, and fertilizer-label terminology.

## Answer-key references

- [US EPA: Composting at Home](https://www.epa.gov/recycle/composting-home)
  explains composting organic materials for use as a soil amendment.
- [University of Minnesota Extension: Mulching for soil and garden health](https://extension.umn.edu/garden-and-home/yard-and-garden/gardening-in-minnesota/mulching-for-soil-and-garden-health)
  defines mulch and documents moisture retention and weed suppression.
- [Penn State Extension: Pruning Herbaceous Plants](https://extension.psu.edu/pruning-herbaceous-plants)
  discusses pruning and removing spent flowers through deadheading.
- [Penn State Extension: Perennials](https://extension.psu.edu/programs/master-gardener/counties/chester/how-to-gardening-brochures/perennials-1)
  distinguishes annual and perennial plant life cycles.
- [University of Minnesota Extension: Seed-starting basics](https://extension.umn.edu/about/our-stories/news/yard-and-garden-news/warm-weather-jump-seed-starting)
  describes gradually hardening off seedlings before moving them outdoors.
- [USDA National Agronomy Manual](https://www.nrcs.usda.gov/sites/default/files/2022-10/National-Agronomy-Manual.pdf)
  explains fertilizer labels and their nitrogen designation `N`.
