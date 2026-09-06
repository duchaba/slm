# QA8 Basic Finance Test Results

## Test run

- Date: September 6, 2026
- Test data: `data/qa8-finance.csv`
- Test command: `python qa-code/test_fill_blank.py data/qa8-finance.csv`
- Questions: 10 fill-in-the-blank finance questions
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
| 1 | The original amount of money borrowed on a loan is called the ___. | principal | principal | PASS | Principal | PASS |
| 2 | The price paid for borrowing money is called ___. | interest | interest | PASS | Interest | PASS |
| 3 | A unit of ownership in a corporation is called a ___. | share | Share | PASS | Share | PASS |
| 4 | A debt security that works like an IOU from an issuer is a ___. | bond | Bond | PASS | Bonds | PASS |
| 5 | Spreading money among different investments to reduce risk is called ___. | diversification | Diversification | PASS | Diversification | PASS |
| 6 | A general increase in the overall prices of goods and services is called ___. | inflation | Inflation | PASS | Inflation | PASS |
| 7 | The value of a person's assets minus liabilities is called ___. | net worth | net worth | PASS | Financial Health or Net Worth | **FAIL** |
| 8 | A plan for income, spending, and saving is called a ___. | budget | budget | PASS | Budget | PASS |
| 9 | Earning interest on both principal and previously earned interest is called ___. | compound interest | compound interest | PASS | Compound interest | PASS |
| 10 | The ease with which an investment can be bought or sold is called ___. | liquidity | liquidity | PASS | Liquidity | PASS |

## Grading notes

Answers were compared without regard to capitalization or punctuation. The
dataset accepts clearly equivalent wording such as `bond` and `bonds`, and
`liquidity` and `marketability`.

Llama's answer to question 7 contains the correct term `Net Worth`, but it also
offers `Financial Health` as an alternative. Because the prompt required a
single fill-in-the-blank answer and the first alternative is not the defined
assets-minus-liabilities calculation, the combined response was scored as a
failure under the evaluator's exact accepted-answer policy.

## Observations

Microsoft Phi-4 Mini answered all ten questions correctly. Meta Llama 3.2 3B
answered nine correctly. Llama demonstrated the relevant knowledge in its only
failed response but did not follow the instruction to return one precise term.

This small factual benchmark is educational and does not assess either model's
suitability for investment, credit, tax, or other financial advice.

## Answer-key references

- [CFPB financial terms glossary](https://files.consumerfinance.gov/f/documents/cfpb_building_block_activities_glossary.pdf)
  defines loan principal and other basic personal-finance terms.
- [Investor.gov glossary](https://www.investor.gov/introduction-investing/investing-basics/glossary/all)
  defines interest, assets, liabilities, bonds, and securities.
- [Investor.gov introduction to investing](https://www.investor.gov/introduction-investing)
  explains shares, diversification, and compound growth.
- [Federal Reserve inflation FAQ](https://www.federalreserve.gov/faqs/economy_14419.htm)
  defines inflation as a general increase in prices of goods and services.
- [Investor.gov liquidity glossary](https://www.investor.gov/introduction-investing/investing-basics/glossary/liquidity-or-marketability)
  defines liquidity or marketability in terms of how easily or quickly a
  security can be bought or sold.
