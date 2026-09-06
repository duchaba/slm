# QA7 Basic Health and Medicine Test Results

## Test run

- Date: September 6, 2026
- Test data: `data/qa7-health.csv`
- Test command: `python qa-code/test_fill_blank.py data/qa7-health.csv`
- Questions: 10 fill-in-the-blank health and medicine questions
- Maximum generated tokens per answer: 64
- Generation temperature: 0.0 (deterministic)
- Microsoft model: `mlx-community/Phi-4-mini-instruct-4bit`
- Meta model: `mlx-community/Llama-3.2-3B-Instruct-4bit`

## Summary

| Model | Correct | Incorrect | Accuracy |
| --- | ---: | ---: | ---: |
| Microsoft Phi-4 Mini | 10 | 0 | 100.0% |
| Meta Llama 3.2 3B | 9 | 1 | 90.0% |

## Detailed results

| # | Question | Expected | Phi actual | Phi result | Llama actual | Llama result |
| ---: | --- | --- | --- | :---: | --- | :---: |
| 1 | The organ that pumps blood throughout the body is the ___. | heart | Heart | PASS | heart | PASS |
| 2 | The gas taken into the lungs that body cells need to make energy is ___. | oxygen | Oxygen | PASS | Carbon dioxide | **FAIL** |
| 3 | The protein in red blood cells that carries oxygen is ___. | hemoglobin | Hemoglobin | PASS | Hemoglobin | PASS |
| 4 | The largest organ of the human body is the ___. | skin | Skin | PASS | Skin | PASS |
| 5 | The vitamin the body can form in the skin after sunlight exposure is vitamin ___. | D | D | PASS | D | PASS |
| 6 | The bony structure that protects the brain is the ___. | skull | cranium | PASS | Skull | PASS |
| 7 | The hormone that lowers blood glucose by helping glucose enter cells is ___. | insulin | Insulin | PASS | Insulin | PASS |
| 8 | Blood vessels that generally carry blood away from the heart are called ___. | arteries | Arteries | PASS | Arteries | PASS |
| 9 | The organs that filter blood and remove wastes and extra water to make urine are the ___. | kidneys | Kidneys | PASS | kidneys | PASS |
| 10 | The main muscle used for breathing is the ___. | diaphragm | diaphragm | PASS | Diaphragm | PASS |

## Grading notes

Answers were compared without regard to capitalization or punctuation. The
dataset accepts equivalent terms where appropriate, including `hemoglobin` and
`haemoglobin`, `skull` and `cranium`, and `kidneys` and `kidney`.

## Observations

Microsoft Phi-4 Mini answered all ten questions correctly. Meta Llama 3.2 3B
answered nine correctly. Llama incorrectly supplied `Carbon dioxide` for the
gas inhaled into the lungs that cells use to make energy; the expected answer
is `oxygen`. Carbon dioxide is instead a waste gas transferred from the blood
to the lungs and exhaled.

These results are a small factual QA baseline and are not evidence that either
model is suitable for medical diagnosis, treatment, or other clinical use.

## Answer-key references

- [NHLBI: How the lungs work and what breathing does for the body](https://www.nhlbi.nih.gov/health/lungs/breathing-benefits)
  covers oxygen intake, cellular energy, carbon dioxide removal, hemoglobin,
  red blood cells, and circulation.
- [MedlinePlus: Heart and vascular services](https://medlineplus.gov/ency/article/007459.htm)
  describes the heart's pumping role and the general direction of arterial
  blood flow.
- [MedlinePlus: Components of skin](https://medlineplus.gov/ency/anatomyvideos/000029.htm)
  identifies skin as the body's largest organ.
- [MedlinePlus: Vitamin D](https://medlineplus.gov/ency/article/002405.htm)
  explains that the body makes vitamin D when skin is exposed to sunlight.
- [MedlinePlus: Insulin therapy](https://medlineplus.gov/ency/patientinstructions/000965.htm)
  explains how insulin lowers blood glucose by helping it enter cells.
- [NIDDK: Your kidneys and how they work](https://www.niddk.nih.gov/health-information/kidney-disease/kidneys-how-they-work)
  explains that kidneys filter blood and remove wastes and extra water to make
  urine.
- [NHLBI: How the body controls breathing](https://www.nhlbi.nih.gov/health/lungs/body-controls-breathing)
  identifies the diaphragm as the main muscle used for breathing.
