# QA19 Basic Biology Test Results

## Test run

- Date: September 6, 2026
- Test data: `data/qa19-biology.csv`
- Test command: `python qa-code/test_fill_blank.py data/qa19-biology.csv`
- Questions: 10 fill-in-the-blank biology questions
- Maximum generated tokens per answer: 64
- Generation temperature: 0.0 (deterministic)
- Microsoft model: `mlx-community/Phi-4-mini-instruct-4bit`
- Meta model: `mlx-community/Llama-3.2-3B-Instruct-4bit`

## Summary

| Model | Correct | Incorrect | Accuracy |
| --- | ---: | ---: | ---: |
| Microsoft Phi-4 Mini | 9 | 1 | 90.0% |
| Meta Llama 3.2 3B | 9 | 1 | 90.0% |

## Detailed results

| # | Question | Expected | Phi actual | Phi result | Llama actual | Llama result |
| ---: | --- | --- | --- | :---: | --- | :---: |
| 1 | The basic structural and functional unit of life is the ___. | cell | cell. | PASS | cell | PASS |
| 2 | The molecule that carries hereditary information in most organisms is ___. | DNA | DNA. | PASS | DNA | PASS |
| 3 | The organelle commonly called the powerhouse of the cell is the ___. | mitochondrion | Mitochondria | PASS | Mitochondria | PASS |
| 4 | In eukaryotic cells most genetic material is stored in the ___. | nucleus | nucleus. | PASS | nucleus | PASS |
| 5 | The type of cell division that produces two genetically identical daughter cells is ___. | mitosis | Mitosis. | PASS | Asexual reproduction. | **FAIL** |
| 6 | The maintenance of stable internal conditions in an organism is called ___. | homeostasis | homeostasis. | PASS | Homeostasis. | PASS |
| 7 | The blood cells primarily responsible for transporting oxygen are ___ blood cells. | red | Unrecognized | **FAIL** | Red | PASS |
| 8 | The basic unit of heredity is a ___. | gene | gene. | PASS | gene | PASS |
| 9 | The scientist associated with the theory of evolution by natural selection was Charles ___. | Darwin | Charles Darwin. | PASS | Darwin | PASS |
| 10 | A community of organisms interacting with their nonliving environment forms an ___. | ecosystem | ecosystem. | PASS | ecosystem | PASS |

## Grading notes

Answers were compared without regard to capitalization or punctuation. Standard
scientific equivalents were accepted, including `DNA`/`deoxyribonucleic acid`,
`mitochondrion`/`mitochondria`, and `red`/`red blood cells`/`erythrocytes`.

`Unrecognized` for Phi question 7 means its response omitted the required
`ANSWER:` marker, leaving no extractable final answer. Llama's `Asexual
reproduction` was not accepted for question 5 because it is a mode of
reproduction, while the question asks for the specific cell-division process
that creates two genetically identical daughter cells: `mitosis`.

## Observations

Microsoft Phi-4 Mini and Meta Llama 3.2 3B each answered nine questions
correctly. Phi's only loss was an output-format failure; Llama's only loss was a
conceptual error. The models answered different questions incorrectly, despite
earning the same aggregate score.

## Answer-key references

- [National Human Genome Research Institute: Genetics glossary](https://www.genome.gov/genetics-glossary)
  provides definitions for cells, DNA, genes, heredity, and related concepts.
- [NHGRI: DNA fact sheet](https://www.genome.gov/about-genomics/fact-sheets/Deoxyribonucleic-Acid-Fact-Sheet)
  explains that DNA carries biological instructions and that eukaryotic DNA is
  primarily located in the nucleus.
- [National Institute of General Medical Sciences: Mitosis and meiosis](https://nigms.nih.gov/biobeat/2021/09/make-like-a-cell-and-split-comparing-mitosis-and-meiosis)
  states that mitosis produces two genetically identical daughter cells.
- [MedlinePlus: Red blood cell production](https://medlineplus.gov/ency/anatomyvideos/000104.htm)
  explains that red blood cells transport oxygen to body tissues.
- [NIGMS: Inside the Cell](https://nigms.nih.gov/education/Booklets/inside-the-cell)
  introduces cellular structures including the nucleus and mitochondria.
- [Smithsonian: On the Origin of Species](https://www.si.edu/collections/snapshot/origin-species-charles-darwin)
  connects Charles Darwin with the theory of evolution by natural selection.
- [USGS: Ecosystems](https://www.usgs.gov/programs/ecosystems)
  describes the study of organisms and their interacting environments.
