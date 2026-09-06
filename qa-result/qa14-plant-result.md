# QA14 Basic Plant Test Results

## Test run

- Date: September 6, 2026
- Test data: `data/qa14-plant.csv`
- Test command: `python qa-code/test_fill_blank.py data/qa14-plant.csv`
- Questions: 10 fill-in-the-blank plant questions
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
| 1 | The process plants use to convert light energy into chemical energy is called ___. | photosynthesis | photosynthesis. | PASS | Photosynthesis | PASS |
| 2 | The green pigment in plants that absorbs light is called ___. | chlorophyll | chlorophyll. | PASS | Chlorophyll. | PASS |
| 3 | The plant structures that usually absorb water and minerals from soil are the ___. | roots | roots. | PASS | roots | PASS |
| 4 | The vascular tissue that transports water upward from a plant's roots is called ___. | xylem | xylem. | PASS | xylem. | PASS |
| 5 | The tiny pores on leaves that allow gas exchange are called ___. | stomata | Unrecognized | **FAIL** | stomata | PASS |
| 6 | The transfer of pollen from the male part to the female part of a flower is called ___. | pollination | pollination. | PASS | Pollination | PASS |
| 7 | The process by which a seed begins to grow is called ___. | germination | germination. | PASS | germination. | PASS |
| 8 | The reproductive structure of an angiosperm is the ___. | flower | flower. | PASS | flower | PASS |
| 9 | Pine trees produce seeds in structures called ___. | cones | Cones. | PASS | Cones | PASS |
| 10 | Trees that normally shed all their leaves once a year are called ___ trees. | deciduous | deciduous trees. | PASS | Deciduous trees. | PASS |

## Grading notes

Answers were compared without regard to capitalization or punctuation. Singular
and plural forms were accepted for `root`, `stoma`, and `cone`. The complete
phrase `deciduous trees` was accepted as equivalent to the missing word
`deciduous`.

`Unrecognized` for Phi question 5 means the response did not contain the
required `ANSWER:` marker, so the evaluator could not extract a gradable final
answer. It remains a failure even if other generated text may have discussed
the correct concept.

The initial run treated `deciduous trees` as a mismatch for both models. Because
that phrase is factually correct and simply repeats the noun following the
blank, it was added as an accepted equivalent and both models were rerun. This
report contains the final rerun results.

## Observations

Microsoft Phi-4 Mini answered nine questions correctly, with one output-format
failure. Meta Llama 3.2 3B answered all ten correctly and followed the required
format throughout the test. Every answer that the evaluator successfully
extracted from either model was factually correct.

## Answer-key references

- [USDA NRCS: How Does Soil Function?](https://www.nrcs.usda.gov/plantmaterials/idpmctr12529.pdf)
  explains photosynthesis, chlorophyll, and gas exchange through stomata.
- [US Forest Service: Plant Parts and Functions](https://www.fs.usda.gov/wildflowers/teacher/documents/k5_DesertGardeners_plantsandparts.pdf)
  covers the water-absorbing role of roots and the reproductive role of flowers.
- [Encyclopaedia Britannica: Xylem](https://www.britannica.com/science/xylem)
  describes xylem's transport of water and dissolved minerals from roots.
- [US Forest Service: Pollinators](https://www.fs.usda.gov/wildflowers/pollinators/What_is_Pollination/)
  defines pollination as the transfer of pollen within or between flowers.
- [USDA National Agricultural Library: Seed germination](https://www.nal.usda.gov/collections/stories/seed-germination)
  describes germination as the beginning of seed growth.
- [US Forest Service: What is a conifer?](https://www.fs.usda.gov/wildflowers/beauty/conifers/what.shtml)
  explains that conifers such as pines bear seeds in cones.
- [US Forest Service: Deciduous Trees](https://www.fs.usda.gov/media/198962)
  defines a deciduous tree as one that loses its leaves each year.
