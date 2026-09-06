# QA15 Basic Chemistry Test Results

## Test run

- Date: September 6, 2026
- Test data: `data/qa15-chemistry.csv`
- Test command: `python qa-code/test_fill_blank.py data/qa15-chemistry.csv`
- Questions: 10 fill-in-the-blank chemistry questions
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
| 1 | The number of protons in an atom is its atomic ___. | number | atomic number. | PASS | number | PASS |
| 2 | The chemical formula H2O represents ___. | water | H2O | **FAIL** | water | PASS |
| 3 | A substance with a pH below 7 is classified as an ___. | acid | Acid. | PASS | acid | PASS |
| 4 | The chemical name for common table salt is sodium ___. | chloride | sodium chloride | PASS | chloride | PASS |
| 5 | The subatomic particle with a negative electric charge is the ___. | electron | electron. | PASS | electron. | PASS |
| 6 | Protons and neutrons are found in an atom's ___. | nucleus | Unrecognized | **FAIL** | nucleus | PASS |
| 7 | A chemical bond formed by sharing electron pairs is called a ___ bond. | covalent | covalent | PASS | Covalent | PASS |
| 8 | The change of state from a gas to a liquid is called ___. | condensation | condensation. | PASS | condensation. | PASS |
| 9 | The chemical symbol for carbon is ___. | C | C | PASS | C | PASS |
| 10 | The scientist widely credited with developing the periodic table was Dmitri ___. | Mendeleev | Mendeleev. | PASS | Mendeleev | PASS |

## Grading notes

Answers were compared without regard to capitalization or punctuation. Complete
phrases that repeat wording around a blank were accepted when equivalent, such
as `atomic number`, `sodium chloride`, and `covalent bond`.

Phi's `H2O` response for question 2 only repeated the formula already supplied
in the question; it did not provide the requested substance name, `water`, and
was not accepted. `Unrecognized` for Phi question 6 means its response omitted
the required `ANSWER:` marker, leaving no extractable final answer.

## Observations

Microsoft Phi-4 Mini answered eight questions correctly. Its two failures were
one nonresponsive repetition and one output-format failure. Meta Llama 3.2 3B
answered all ten correctly and followed the required output format throughout.

## Answer-key references

- [IUPAC Gold Book: atomic number](https://goldbook.iupac.org/terms/view/A00499)
  defines atomic number as the number of protons in an atomic nucleus.
- [IUPAC Gold Book: atom](https://goldbook.iupac.org/terms/view/A00493)
  describes the positively charged nucleus and surrounding electrons.
- [USGS: Water Science School](https://www.usgs.gov/special-topics/water-science-school/science/water-qa-why-water-universal-solvent)
  identifies water by the chemical formula H2O.
- [Chemistry LibreTexts: The pH Scale](https://chem.libretexts.org/Bookshelves/Introductory_Chemistry/Introductory_Chemistry/14%3A_Acids_and_Bases/14.09%3A_The_pH_Scale)
  classifies pH values below 7 as acidic.
- [PubChem: Sodium chloride](https://pubchem.ncbi.nlm.nih.gov/compound/Sodium-Chloride)
  identifies sodium chloride as common table salt.
- [Chemistry LibreTexts: Covalent Bonding](https://chem.libretexts.org/Courses/University_of_Toronto/Chemistry%3A_Physical_Principles/03%3A_Bonding_and_Intermolecular_Forces/3.04%3A_Covalent_Bonding)
  explains that a covalent bond forms when atoms share electrons.
- [NOAA: The Water Cycle](https://www.noaa.gov/education/resource-collections/freshwater/water-cycle)
  describes condensation as the change from water vapor to liquid water.
- [Royal Society of Chemistry: Carbon](https://periodic-table.rsc.org/element/6/carbon)
  lists `C` as carbon's chemical symbol.
- [Royal Society of Chemistry: Development of the periodic table](https://periodic-table.rsc.org/about)
  explains Dmitri Mendeleev's foundational periodic table.
