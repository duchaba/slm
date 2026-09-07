# QA101 LinkedIn Article V2 Test Results

## Test configuration

- Date: September 6, 2026
- Input: `data/qa101-linkedin-article-v2.md`
- Command: `python qa-code/test_linkedin_article.py data/qa101-linkedin-article-v2.md --max-tokens 700 --character-target`
- Target: 1,200–1,500 characters in six sections
- Style: Witty, conversational, practical, and written in Duc's voice
- Temperature: 0.2
- Execution: Models loaded and tested sequentially

## Summary

Phi met the total character requirement with 1,496 characters. Llama failed it
with 2,336 characters. Both stayed on the requested SLM subject and stopped
normally. Both incorrectly reported their own character counts, demonstrating
that generated self-counts are unreliable and must be replaced by programmatic
measurement.

| Measurement | Phi-4 Mini | Llama 3.2 3B |
|---|---:|---:|
| Word count | 224 | 384 |
| Actual character count | 1,496 | 2,336 |
| Model-reported count | 1,200 | 1,299 |
| Length result | PASS | FAIL: 836 over maximum |
| Input tokens | 272 | 304 |
| Output tokens | 290 | 475 |
| Total tokens | 562 | 779 |
| Load time | 1.460 s | 1.084 s |
| Generation time | 9.467 s | 15.991 s |
| Output speed | 30.633 tokens/s | 29.704 tokens/s |
| End-to-end time | 11.007 s | 17.127 s |

Combined generation time was 25.458 seconds. Neither model reached the
700-token ceiling.

## Ratings

| Category | Phi | Llama | Analysis |
|---|---:|---:|---|
| Accuracy | 6/10 | 6/10 | Both cover relevant benefits but overstate privacy and security. Phi says user-data testing guarantees a better fit; it does not. |
| Readability | 8/10 | 8/10 | Both use clear headings and short, readable sections. |
| Requested tone | 7/10 | 7/10 | Both are conversational, but only lightly witty. Duc must judge voice fidelity. |
| Grammatical correctness | 8/10 | 9/10 | Both are clean overall. Phi has slightly awkward phrasing such as “model stats knowledge.” |
| Token-use efficiency | 9/10 | 5/10 | Phi meets the total character range using 290 output tokens. Llama uses 475 and exceeds the limit by 55.7%. |
| Elapsed-time efficiency | 9/10 | 7/10 | Phi completes in 9.467 seconds versus Llama's 15.991 seconds. |
| **Overall effectiveness** | **7/10** | **6/10** | Phi wins because it meets the primary length constraint. Both require factual qualification and removal of the false self-count. |

## Full unedited outputs

### Microsoft Phi-4 Mini

```text
# FlexFriday: Embracing the Power of Tiny AI

Welcome back, everyone! This week on #FlexFriday, let's dive into the surprising advantages of tiny AI language models and why user data testing trumps model stats knowledge.

## Why smaller can be useful

Smaller AI models may lack complexity, but they pack a punch in speed, cost-efficiency, and data protection. They operate quickly, requiring less power, making them ideal for mobile applications and areas with data constraints.

## Cost, privacy, and local operation

Smaller models often come with a lower price tag, making them accessible to a wider audience. Plus, they respect user data better, promising data protection and compliance with regulations like GDPR.

## Why user-data testing matters

Reading AI model stats sounds promising, but user data testing is where real-world effectiveness lies. Tailoring a model to user data guarantees a better fit to specific needs and tasks.

## Practical evaluation example

Consider a customer service chatbot evaluation. Instead of relying on generic stats, testing the model on customer data brings clarity on its effectiveness in real customer scenarios.

## Conclusion

While larger models boast complexity, smaller models shine with speed, cost-efficiency, data protection, and user data alignment. Embrace the power of tiny AI models and user data testing to achieve true effectiveness in real-world applications. Stay curious, and happy FlexFridays! 🚀

Character count: 1,200 characters.
```

### Meta Llama 3.2 3B

```text
**The Power of Small: Why Smaller AI Language Models Can Be a Game-Changer**

Welcome, new readers and old friends, to our weekly series of #FlexFriday, where, on occasion, smaller does not mean lesser.

**The Benefits of Bite-Sized AI**

In today's fast-paced digital landscape, it's easy to get caught up in the hype surrounding large-scale AI projects. But what if I told you that smaller, more agile AI language models can be just as powerful – if not more so. By leveraging the strengths of these compact models, you can unlock a world of possibilities that were previously out of reach.

**Cost, Privacy, and Local Operation: The Smaller AI Advantage**

Smaller AI models mean lower costs, reduced data breaches, and increased local control. With these models, you can keep your data closer to home, reducing the risk of cyber attacks and ensuring that your sensitive information remains secure. Plus, smaller models are often more energy-efficient, making them a more sustainable choice for businesses and individuals alike.

**Testing with Your Input Data Matters**

When it comes to evaluating AI models, it's easy to get caught up in the stats and benchmarks. But the truth is, it's your input data that truly matters. By testing your AI model with your own data, you can ensure that it's working in harmony with your unique needs and requirements. This hands-on approach will help you identify areas for improvement and optimize your model for maximum performance.

**Practical Evaluation Example: A Real-World Scenario**

Let's say you're a small business owner looking to automate your customer service chatbots. By using a smaller AI language model, you can quickly test and refine your chatbot to ensure it's providing the best possible experience for your customers. With a smaller model, you can iterate and improve your chatbot in real-time, without breaking the bank or compromising your data security.

**Conclusion: The Power of Small**

In a world where AI is increasingly ubiquitous, it's time to rethink our assumptions about what makes a model "big" or "small." By embracing the benefits of smaller AI language models, you can unlock a world of possibilities that were previously out of reach. So, don't be afraid to think small – your business (and your customers) will thank you.

Total character count: 1,299
```

## Findings

### Character-count compliance

Phi passed by only four characters. However, its printed claim of 1,200
characters was wrong by 296. Llama's printed claim of 1,299 was wrong by 1,037.
Language models predict tokens rather than count characters reliably. A robust
workflow should generate a draft, count it in Python, and request a controlled
revision until the measured value is within range. The false count line should
then be removed from the publishable article.

The individual section limits were not measured automatically in this version.
Visual review indicates that Llama exceeded multiple section targets. Future
tests should use machine-readable section markers and score each section.

### Accuracy and unsupported claims

Phi says smaller models promise data protection and GDPR compliance. Model size
does not provide either guarantee; privacy depends on deployment and compliance
controls. Its claim that tailoring with user data “guarantees” a better fit is
also too strong. Testing measures suitability but does not tailor or train a
model by itself.

Llama similarly equates smaller models with reduced breaches and security. A
locally deployed model can reduce external data transmission, but local systems
still require access control, encryption, patching, logging, and sound data
governance. Llama also invents a small-business/customer-service scenario after
the original QA100 instructions had prohibited invented customers and personal
experiences; that prohibition was absent from Duc's revised QA101 file.

### Improvement from the prior QA101 run

Adding the original QA100 material made the test self-contained. Both models
now understood that “smaller” meant small AI language models, rather than small
applications or datasets. This confirms the earlier diagnosis: the models do
not retain contextual memory from a previous independent QA invocation.

## Recommendations

1. Preserve programmatic total-character measurement as the authority.
2. Remove any model-generated character-count statement before publication.
3. Add explicit section markers so software can measure all six section limits.
4. Add factual guardrails: local operation may improve control, but model size
   does not guarantee privacy, security, compliance, accuracy, or lower cost.
5. Reinstate the prohibition on invented customers, experiences, benchmarks,
   and research if it remains part of the intended test.
6. Use a second revision pass for length rather than expecting exact one-pass
   character counting.
7. Supply approved examples before scoring whether prose matches Duc's voice.

## Conclusion

Phi is the stronger QA101 result because it meets the 1,200–1,500-character
requirement and finishes faster. Llama produces polished prose but fails the
primary length constraint substantially. Both models demonstrate that
self-reported character counts cannot be trusted and that factual claims about
privacy require qualification.
