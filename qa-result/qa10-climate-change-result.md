# QA10 Basic Climate Change Test Results

## Test run

- Date: September 6, 2026
- Test data: `data/qa10-climate-change.csv`
- Test command: `python qa-code/test_fill_blank.py data/qa10-climate-change.csv`
- Questions: 10 fill-in-the-blank climate change questions
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

| # | Question | Expected | Phi actual | Phi result | Llama actual | Llama result |
| ---: | --- | --- | --- | :---: | --- | :---: |
| 1 | The long-term average pattern of weather in a region is called its ___. | climate | climate | PASS | Climate | PASS |
| 2 | The greenhouse gas whose atmospheric increase is driven largely by burning fossil fuels is ___. | carbon dioxide | carbon dioxide (CO2) | PASS | Carbon dioxide (CO2) | PASS |
| 3 | The natural process by which gases in the atmosphere trap heat is called the ___. | greenhouse effect | greenhouse effect | PASS | greenhouse effect | PASS |
| 4 | Coal, oil, and natural gas are collectively known as ___. | fossil fuels | Fossil fuels | PASS | Fossil fuels | PASS |
| 5 | The main component of natural gas that is also a potent greenhouse gas is ___. | methane | methane | PASS | Methane | PASS |
| 6 | The part of the Earth system that stores most of the excess heat from global warming is the ___. | ocean | Ocean | PASS | oceans | PASS |
| 7 | The large-scale clearing or removal of forests is called ___. | deforestation | Deforestation | PASS | Deforestation | PASS |
| 8 | The process in which warming seawater expands and raises sea level is called ___. | thermal expansion | thermal expansion | PASS | Thermohaline circulation | **FAIL** |
| 9 | Energy generated from sunlight is called ___ energy. | solar | solar energy | PASS | Solar energy | PASS |
| 10 | The international climate treaty adopted in 2015 is the ___. | Paris Agreement | Paris Agreement | PASS | Paris | **FAIL** |

## Grading notes

Answers were compared without regard to capitalization or punctuation. Common
scientific abbreviations and equivalent forms were accepted, including
`carbon dioxide`, `CO2`, and `carbon dioxide (CO2)`, as well as singular and
plural forms of `ocean`.

`Thermohaline circulation` was not accepted for question 8 because it refers to
large-scale ocean circulation driven by density differences, not the expansion
of seawater as it warms. `Paris` was not accepted for question 10 because it is
a location, while the requested treaty name is the `Paris Agreement`.

## Observations

Microsoft Phi-4 Mini answered all ten questions correctly. Meta Llama 3.2 3B
answered eight correctly, with one incorrect climate-process term and one
incomplete treaty name.

## Answer-key references

- [NASA: What is climate change?](https://science.nasa.gov/climate-change/what-is-climate-change/)
  defines climate change through long-term average weather patterns and
  identifies fossil-fuel burning as the principal driver of current warming.
- [NASA: Causes of climate change](https://science.nasa.gov/climate-change/causes/)
  explains the greenhouse effect and the roles of carbon dioxide, methane,
  fossil fuels, and deforestation.
- [EPA: Basics of climate change](https://www.epa.gov/climatechange-science/basics-climate-change)
  covers greenhouse gases, fossil-fuel combustion, forest clearing, and the
  heat-trapping greenhouse effect.
- [NASA: Evidence for climate change](https://science.nasa.gov/climate-change/evidence/)
  reports that the ocean stores about 90% of the extra energy in the climate
  system.
- [NASA: Rising waters and thermal expansion](https://science.nasa.gov/science-research/earth-science/rising-waters/)
  explains that seawater expands as it warms and contributes to sea-level rise.
- [UNFCCC: The Paris Agreement](https://www.unfccc.int/process-and-meetings/the-paris-agreement)
  identifies the treaty and its adoption in Paris on December 12, 2015.
