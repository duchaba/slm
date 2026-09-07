# QA100 LinkedIn Article Test Results

## Test run

- Date: September 6, 2026
- Test data: `data/qa100-linkedin-article.md`
- Test program: `qa-code/test_linkedin_article.py`
- Command: `python qa-code/test_linkedin_article.py data/qa100-linkedin-article.md`
- Requested length: 1,200–1,500 words
- Requested style: Witty and conversational LinkedIn article
- Required themes: Benefits of small language models and the importance of
  testing with the user's own data instead of relying only on published model
  statistics
- Generation temperature: 0.2
- Maximum generation: 2,600 tokens per model
- Model execution: Sequential

## Executive result

Neither model produced a publishable article without substantial editing.

Phi developed a reasonably organized article but failed to stop, reached the
2,600-token generation ceiling, and repeated its closing sentence many times.
Its 2,187-word response exceeded the requested maximum by 687 words and ended
mid-sentence.

Llama produced the stronger draft. It was concise, readable, conversational,
and grammatically clean, but it stopped at 602 words—598 words below the
requested minimum. It also made a material technical error by implying that
testing a model with user data teaches the model and causes it to improve over
time. Inference and testing do not update model weights unless a separate
training or memory process is implemented.

## Objective measurements

Token counts are approximate. Each rendered prompt and decoded response was
encoded with its model's own tokenizer. Token counts are not perfectly
comparable between models because their tokenizers and chat templates differ.

| Measurement | Microsoft Phi-4 Mini | Meta Llama 3.2 3B |
|---|---:|---:|
| Word count | 2,187 | 602 |
| Length requirement | FAIL: 687 words over maximum | FAIL: 598 words below minimum |
| Input tokens | 153 | 185 |
| Output tokens | 2,600 | 723 |
| Total tokens | 2,753 | 908 |
| Model load time | 1.587 s | 1.122 s |
| Article generation time | 116.695 s | 25.983 s |
| Output speed | 22.280 tokens/s | 27.826 tokens/s |
| Cleanup time | 0.040 s | 0.035 s |
| End-to-end model run | 118.340 s | 27.163 s |
| Accuracy result | Qualitative review required | Qualitative review required |

Combined generation time was 142.678 seconds. Mean generation time was 71.339
seconds per model. Phi consumed approximately three times as many total tokens
and took approximately 4.5 times as long to generate its article as Llama.
Those ratios largely reflect the radically different output lengths and Phi's
repetition, not just differences in model speed.

## Rating method

Each category uses a 1–10 scale:

- **1–2:** Unacceptable; major failure
- **3–4:** Weak; substantial correction required
- **5–6:** Usable foundation; significant editing required
- **7–8:** Good; limited editing required
- **9–10:** Excellent; nearly or fully publishable

The ratings are editorial judgments by the Codex/ChatGPT reviewer, not an
automated ground truth. Accuracy considers whether factual and technical claims
are supportable. Token-use efficiency considers whether the model completed
the requested job without severe under-generation, over-generation, or wasted
repetition. Elapsed-time efficiency is judged relative to the other model in
this local run. Overall effectiveness is a separate holistic rating rather
than a mathematical average.

## Ratings

| Category | Phi rating | Llama rating | Review summary |
|---|---:|---:|---|
| Accuracy | 5/10 | 4/10 | Both contain unsupported generalizations. Llama incorrectly describes ordinary testing as a learning process. |
| Readability | 2/10 | 8/10 | Phi becomes unusable because of extreme repetition. Llama is clear and easy to scan. |
| Requested tone | 4/10 | 7/10 | Both attempt conversational language. Llama is more natural; Phi becomes formulaic and repetitive. |
| Grammatical correctness | 4/10 | 9/10 | Llama is mostly clean. Phi's repeated closing and truncated final sentence severely damage coherence. |
| Token-use efficiency | 1/10 | 4/10 | Phi wastes most of its long ending. Llama is efficient but fails to generate even half the requested minimum length. |
| Elapsed-time efficiency | 2/10 | 8/10 | Phi takes 116.695 seconds because it exhausts the token allowance. Llama finishes in 25.983 seconds. |
| **Overall effectiveness** | **2/10** | **6/10** | Phi requires a rewrite. Llama provides a useful short draft but needs expansion and factual correction. |

## Microsoft Phi-4 Mini review

### What worked

- Opened with the requested `#FlexFriday` framing.
- Used headings that made the initial portion easy to scan.
- Covered flexibility, specialization, cost, deployment constraints, and the
  importance of testing with the user's own data.
- Used conversational devices, analogies, and direct address.
- Produced enough subject matter to support a properly edited 1,200–1,500-word
  article.

### Accuracy concerns

Phi makes several overly broad claims:

- It says small models can be integrated “effortlessly.” Integration difficulty
  depends on the model, hardware, runtime, security requirements, and product.
- It implies small models necessarily need less training data and can adapt to
  specialized domains quickly. That can be true in some fine-tuning settings,
  but model size alone does not guarantee it.
- It says large models “drown” in data noise while small models focus on data
  quality. This is a rhetorical contrast rather than a reliable technical rule.
- It proposes a healthcare example in which a small model leads to faster
  diagnosis and improved outcomes without evidence. That is an inappropriate
  unsupported claim for a general LinkedIn article.
- It sometimes confuses a language model with a more general data-analysis
  model.

### Readability and generation failure

The article was coherent through its nominal conclusion. It then repeated a
variation of the following closing language over and over:

> Stay data-driven, stay curious, and keep embracing the paradox that sometimes
> smaller does not mean lesser—and sometimes lesser does not mean lesser either.

The repetition continued until the 2,600-token limit and the response stopped
mid-sentence. This is a repetition-loop degeneration, not a deliberate
2,187-word article. Increasing the token ceiling would probably have made the
failure longer rather than solving it.

### Phi verdict

The useful opening and body could be edited into a shorter article, but the raw
response is not suitable for publication. A future prompt should require a
single conclusion, use repetition penalties or stop controls if supported, and
monitor repeated n-grams during generation.

## Meta Llama 3.2 3B review

### What worked

- Produced a clear title and an effective version of the requested opening.
- Maintained a conversational LinkedIn tone throughout.
- Organized the argument logically: efficiency, specialization, user-data
  testing, and practical starting advice.
- Used short paragraphs and a numbered list appropriate for online reading.
- Ended cleanly instead of repeating or hitting the generation ceiling.
- Was faster and used fewer total tokens than Phi.

### Accuracy concerns

The most important problem is this passage:

> When you test a model with your own data, you're essentially teaching it how
> to think like you do. This process, called “in-the-loop” learning, allows the
> model to adapt and improve over time.

That description is incorrect for this project. Testing or inference alone does
not teach either model, change its weights, or cause it to improve. Improvement
requires an explicit mechanism such as fine-tuning, feedback-driven training,
prompt changes, or external memory. “Human-in-the-loop” is a common phrase, but
“in-the-loop learning” is not an adequate explanation of what the current QA
system does.

Other issues include:

- Claiming that small models do not require large amounts of training data is
  too broad. Fine-tuning may need less compute and a smaller focused dataset,
  but pretraining a capable SLM still requires substantial data and resources.
- Saying the answer to whether model statistics matter is simply “no”
  overstates the draft's point. Published statistics are useful for screening
  and understanding constraints; tests with representative user data are more
  decisive for the intended use case.
- The chatbot and nonprofit examples sound like actual success stories but have
  no sources. They should be framed explicitly as hypotheticals or removed.

### Length failure

Llama stopped normally after 602 words and 723 output tokens. It used only
27.8% of the allowed 2,600 output tokens, so the short article was not caused by
the evaluator's maximum. The model did not reliably follow the 1,200–1,500-word
constraint. The draft needs approximately twice as much substance, preferably
through concrete discussion of privacy, local deployment, latency, cost,
testing methodology, and the difference between benchmark scores and
application-specific results—not padding or repetition.

### Llama verdict

Llama produced the better editorial foundation. After correcting the learning
claim and expanding it to the required length, it could become an effective
LinkedIn article. The raw response is not yet compliant or factually dependable
enough to publish.

## Representative output excerpts

### Phi opening

> Welcome, new readers and old friends, to our weekly series of #FlexFriday,
> where, on occasion, smaller does not mean lesser—and today, I'm thrilled to
> share a transformative tale about tiny AI language models and their surprising
> benefits.

### Llama opening

> Welcome, new readers and old friends, to our weekly series of #FlexFriday,
> where, on occasion, smaller does not mean lesser. Today, I want to share with
> you a transformative tale about the benefits of using a small AI language
> model. Yes, you read that right—small.

### Llama conclusion

> In the world of AI, size isn't everything. Sometimes, it's the smallest models
> that make the biggest impact.

## Recommendations for the next long-form test

1. Preserve this run as the QA100 baseline; do not overwrite its scores with a
   prompt-tuned run.
2. Add detection for repeated n-grams and stop Phi when a paragraph or sentence
   begins looping.
3. Ask the model to create a short outline and allocate approximate word counts
   to sections before drafting.
4. Restate the length requirement at both the beginning and end of the prompt.
5. Require a word-count check followed by one revision pass when the response
   is outside 1,200–1,500 words.
6. Explicitly state that testing data does not update model weights and that
   benchmark statistics remain useful but are secondary to representative
   application testing.
7. Request hypothetical labels or sources for examples, and prohibit medical,
   financial, or performance claims without evidence.
8. Save exact raw generations as separate machine-readable artifacts in future
   runs so repetition, stop reason, and editorial scoring remain fully auditable.
9. Add a deterministic evaluation pass while retaining a separate creative
   temperature for the article-generation pass.
10. Have Duc score tone and overall effectiveness independently because those
    categories ultimately depend on Duc's intended voice.

## Overall conclusion

Llama wins this first long-form comparison despite failing the required length
and making a significant technical error. Its 6/10 overall rating represents a
usable short draft, not a finished article. Phi's 2/10 reflects a generation
control failure severe enough to overwhelm its otherwise serviceable opening
and body.

QA100 also demonstrates why application-specific testing is more informative
than model specifications alone. The smaller token count, faster response, or
published model capabilities could not predict the most consequential observed
behaviors: Phi's repetition loop, Llama's premature completion, and Llama's
incorrect description of testing as learning.

## Verbatim article capture rerun

The original scored run printed its articles to a terminal but did not persist
the raw text. The test was therefore rerun with the same input, models,
temperature, and 2,600-token ceiling to create the verbatim record below.
Temperature 0.2 permits sampling, so these are newly generated articles and not
reconstructions of the first run. They demonstrate the same two principal
behaviors: Phi entered a repetition loop and Llama stopped well below the
requested length.

| Capture-run measurement | Microsoft Phi-4 Mini | Meta Llama 3.2 3B |
|---|---:|---:|
| Word count | 2,322 | 669 |
| Input tokens | 153 | 185 |
| Output tokens | 2,600 | 794 |
| Total tokens | 2,753 | 979 |
| Generation time | 116.214 s | 28.835 s |
| Output speed | 22.373 tokens/s | 27.536 tokens/s |
| End-to-end time | 117.629 s | 29.964 s |

### Microsoft Phi-4 Mini — full unedited output

```text
# FlexFriday: Embracing the Power of Tiny AI Language Models

Hello, everyone! Welcome back to our #FlexFriday series, where we explore different angles on a flexible mindset and how it impacts our professional growth and personal lives. This week, I want to share a personal journey that led me to a surprising revelation about the effectiveness of tiny AI language models versus larger counterparts. Trust me, it was a game-changer—and I hope you’ll find it just as compelling as I did.

For those who don’t already follow this series, #FlexFriday is an opportunity to delve into different flexible approaches to professional challenges, personal growth, and everyday tasks. This week, I want to discuss a specific area where embracing a smaller scale solution proved immensely beneficial: AI language models.

To set the stage, I first want to introduce you to a tiny AI language model I recently discovered called Phi (pronounced “fee”). Phi is a cutting-edge model that brings a fresh perspective on how we can leverage AI in everyday tasks. Despite its relatively modest size, Phi offers a compelling blend of speed, efficiency, and effectiveness.

One of the first things I noticed about Phi was its speed. Larger models like GPT-3 and Phi-13 take considerable time to process requests, while Phi operates on a different speed spectrum altogether. This speed advantage is a game-changer in situations where quick response times are crucial, such as customer support or real-time data analysis.

Moreover, Phi offers a remarkably user-friendly interface, making it easier to integrate into different workflows and applications. This simplicity is a breath of fresh air in an increasingly complex AI landscape, where larger models often come with a steep learning curve and complexity challenges.

One of the most compelling advantages I discovered through hands-on experimentation is Phi's effectiveness in specific tasks versus larger models. Larger models tend to be data-hungry and often require extensive fine-tuning to achieve desired results. This process can be time-consuming, labor-intensive, and sometimes impractical, especially in fast-paced environments where quick data-driven decisions are crucial.

Conversely, Phi offers a streamlined solution that requires far less data and fine-tuning to achieve high levels of effectiveness in specific applications. This data-efficiency translates into a more sustainable and cost-effective solution, making it an ideal candidate for organizations looking to balance speed and effectiveness with data and resource constraints.

One of the most compelling advantages I discovered through hands-on experimentation is Phi's effectiveness in specific tasks versus larger models. Larger models tend to be data-hungry and often require extensive fine-tuning to achieve desired results. This process can be time-consuming, labor-intensive, and sometimes impractical, especially in fast-paced environments where quick data-driven decisions are crucial.

To illustrate this point, I recently explored Phi's effectiveness in a customer support chatbot application versus a larger model like Phi-13 and GPT-3. I discovered that Phi was not only faster but also achieved remarkably high levels of customer satisfaction in terms of speed, relevance, and effectiveness in addressing customer queries.

This hands-on experimentation solidified a crucial lesson I had come to realize through this journey: data is king, but data alone does not equate to effectiveness in real-world applications. It is data contextualization and application that truly matter—and here is where tiny AI language models like Phi shine.

To wrap things up, I want to share a final thought on embracing tiny AI language models versus larger counterparts in professional settings.

The first lesson I learned on this journey is data is king, but data alone does not equate to effectiveness in real-world applications. It is data contextualization and application that truly matter—and here is where tiny AI language models like Phi shine.

To wrap things up, I want to share a final thought on embracing tiny AI language models versus larger counterparts in professional settings.

The first lesson I learned on this journey is data is king, but data alone does not equate to effectiveness in real-world applications. It is data contextualization and application that truly matter—and here is where tiny AI language models like Phi shine.

To wrap things up, I want to share a final thought on embracing tiny AI language models versus larger counterparts in professional settings.

The first lesson I learned on this journey is data is king, but data alone does not equate to effectiveness in real-world applications. It is data contextualization and application that truly matter—and here is where tiny AI language models like Phi shine.

To wrap things up, I want to share a final thought on embracing tiny AI language models versus larger counterparts in professional settings.

The first lesson I learned on this journey is data is king, but data alone does not equate to effectiveness in real-world applications. It is data contextualization and application that truly matter—and here is where tiny AI language models like Phi shine.

To wrap things up, I want to share a final thought on embracing tiny AI language models versus larger counterparts in professional settings.

The first lesson I learned on this journey is data is king, but data alone does not equate to effectiveness in real-world applications. It is data contextualization and application that truly matter—and here is where tiny AI language models like Phi shine.

To wrap things up, I want to share a final thought on embracing tiny AI language models versus larger counterparts in professional settings.

The first lesson I learned on this journey is data is king, but data alone does not equate to effectiveness in real-world applications. It is data contextualization and application that truly matter—and here is where tiny AI language models like Phi shine.

To wrap things up, I want to share a final thought on embracing tiny AI language models versus larger counterparts in professional settings.

The first lesson I learned on this journey is data is king, but data alone does not equate to effectiveness in real-world applications. It is data contextualization and application that truly matter—and here is where tiny AI language models like Phi shine.

To wrap things up, I want to share a final thought on embracing tiny AI language models versus larger counterparts in professional settings.

The first lesson I learned on this journey is data is king, but data alone does not equate to effectiveness in real-world applications. It is data contextualization and application that truly matter—and here is where tiny AI language models like Phi shine.

To wrap things up, I want to share a final thought on embracing tiny AI language models versus larger counterparts in professional settings.

The first lesson I learned on this journey is data is king, but data alone does not equate to effectiveness in real-world applications. It is data contextualization and application that truly matter—and here is where tiny AI language models like Phi shine.

To wrap things up, I want to share a final thought on embracing tiny AI language models versus larger counterparts in professional settings.

The first lesson I learned on this journey is data is king, but data alone does not equate to effectiveness in real-world applications. It is data contextualization and application that truly matter—and here is where tiny AI language models like Phi shine.

To wrap things up, I want to share a final thought on embracing tiny AI language models versus larger counterparts in professional settings.

The first lesson I learned on this journey is data is king, but data alone does not equate to effectiveness in real-world applications. It is data contextualization and application that truly matter—and here is where tiny AI language models like Phi shine.

To wrap things up, I want to share a final thought on embracing tiny AI language models versus larger counterparts in professional settings.

The first lesson I learned on this journey is data is king, but data alone does not equate to effectiveness in real-world applications. It is data contextualization and application that truly matter—and here is where tiny AI language models like Phi shine.

To wrap things up, I want to share a final thought on embracing tiny AI language models versus larger counterparts in professional settings.

The first lesson I learned on this journey is data is king, but data alone does not equate to effectiveness in real-world applications. It is data contextualization and application that truly matter—and here is where tiny AI language models like Phi shine.

To wrap things up, I want to share a final thought on embracing tiny AI language models versus larger counterparts in professional settings.

The first lesson I learned on this journey is data is king, but data alone does not equate to effectiveness in real-world applications. It is data contextualization and application that truly matter—and here is where tiny AI language models like Phi shine.

To wrap things up, I want to share a final thought on embracing tiny AI language models versus larger counterparts in professional settings.

The first lesson I learned on this journey is data is king, but data alone does not equate to effectiveness in real-world applications. It is data contextualization and application that truly matter—and here is where tiny AI language models like Phi shine.

To wrap things up, I want to share a final thought on embracing tiny AI language models versus larger counterparts in professional settings.

The first lesson I learned on this journey is data is king, but data alone does not equate to effectiveness in real-world applications. It is data contextualization and application that truly matter—and here is where tiny AI language models like Phi shine.

To wrap things up, I want to share a final thought on embracing tiny AI language models versus larger counterparts in professional settings.

The first lesson I learned on this journey is data is king, but data alone does not equate to effectiveness in real-world applications. It is data contextualization and application that truly matter—and here is where tiny AI language models like Phi shine.

To wrap things up, I want to share a final thought on embracing tiny AI language models versus larger counterparts in professional settings.

The first lesson I learned on this journey is data is king, but data alone does not equate to effectiveness in real-world applications. It is data contextualization and application that truly matter—and here is where tiny AI language models like Phi shine.

To wrap things up, I want to share a final thought on embracing tiny AI language models versus larger counterparts in professional settings.

The first lesson I learned on this journey is data is king, but data alone does not equate to effectiveness in real-world applications. It is data contextualization and application that truly matter—and here is where tiny AI language models like Phi shine.

To wrap things up, I want to share a final thought on embracing tiny AI language models versus larger counterparts in professional settings.

The first lesson I learned on this journey is data is king, but data alone does not equate to effectiveness in real-world applications. It is data contextualization and application that truly matter—and here is where tiny AI language models like Phi shine.

To wrap things up, I want to share a final thought on embracing tiny AI language models versus larger counterparts in professional settings.

The first lesson I learned on this journey is data is king, but data alone does not equate to effectiveness in real-world applications. It is data contextualization and application that truly matter—and here is where tiny AI language models like Phi shine.

To wrap things up, I want to share a final thought on embracing tiny AI language models versus larger counterparts in professional settings.

The first lesson I learned on this journey is data is king, but data alone does not equate to effectiveness in real-world applications. It is data contextualization and application that truly matter—and here is where tiny AI language models like Phi shine.

To wrap things up, I want to share a final thought on embracing tiny AI language models versus larger counterparts in professional settings.

The first lesson I learned on this journey is data is king, but data alone does not equate to effectiveness in real-world applications. It is data contextualization and application that truly matter—and here is where tiny AI language models like Phi shine.

To wrap things up, I want to share a final thought on embracing tiny AI language models versus larger counterparts in professional settings.

The first lesson I learned on this journey is data is king, but data alone does not equate to effectiveness in real-world applications. It is data contextualization and application that truly matter—and here is where tiny AI language models like Phi shine.

To wrap things up, I want to share a final thought on embracing tiny AI language models versus larger counterparts in professional settings.

The first lesson I learned on this journey is data is king, but data alone does not equate to effectiveness in real-world applications. It is data contextualization and application that truly matter—and here is where tiny AI language models like Phi shine.

To wrap things up, I want to share a final thought on embracing tiny AI language models versus larger counterparts in professional settings.

The first lesson I learned on this journey is data is king, but data alone does not equate to effectiveness in real-world applications. It is data contextualization and application that truly matter—and here is where tiny AI language models like Phi shine.

To wrap things up, I want to share a final
```

## Codex/ChatGPT comparison article

The following article was written from the same rough draft supplied to Phi and
Llama. It is included as a comparison, not as another local-model test. The
article is presented as written, followed by a self-review using the same
rating categories. It contains 1,275 words, which is within the requested
1,200–1,500-word range.

### Full article

Welcome, new readers and old friends, to our weekly series of #FlexFriday, where, on occasion, smaller does not mean lesser.

I have a transformative tale to tell.

It begins, as many modern tales do, with a very large number and an even larger marketing department.

In artificial intelligence, we are trained to admire scale. More parameters. More training data. More benchmark wins. More charts with arrows pointing confidently up and to the right. If one model is large, another model with an extra zero must be better. That is how numbers work, right?

Well, sometimes.

But choosing an AI model is less like buying the largest television in the store and more like hiring someone for a specific job. The tallest candidate is not automatically the best accountant. The fastest typist is not necessarily the best editor. And the language model with the most impressive statistics may not be the one that handles your work most effectively.

That is where small language models enter the story.

A small language model, or SLM, contains fewer parameters than the frontier-scale systems that dominate AI headlines. “Small” is relative—the models are still sophisticated pieces of software—but they can often run on a personal computer, a workstation, a phone, or a modest server. That difference changes what becomes practical.

First, smaller models can reduce operating costs. They generally require less memory and computing power, so a business can experiment without immediately reserving a wing of a data center or handing its entire technology budget to a cloud invoice. Lower operating requirements also make it easier to test several ideas, discard the bad ones, and improve the promising ones.

That freedom to experiment matters. Innovation rarely arrives fully dressed, carrying a business case and a perfect return-on-investment calculation. It usually shows up wearing mismatched socks and asking whether anyone has five minutes to try something strange. A model that is inexpensive and convenient to run gives those strange ideas room to prove themselves.

Second, an SLM can run locally. Local operation may improve privacy because prompts and responses do not have to leave the controlled environment merely to reach a hosted model. It can also help with availability. An internet interruption is inconvenient, but it does not need to silence an assistant running on the machine beside you.

Local does not automatically mean secure, of course. A badly configured local system can leak information with impressive efficiency. Security still requires access controls, encryption, careful logging, software updates, and sensible data-retention rules. The benefit is control, not magic.

Third, smaller models can be fast. For Furiously Important Corporate Questions, such as whether a sentence is true or false, waiting several seconds can feel unnecessary. A compact model can often answer short prompts quickly, especially when it is already loaded. For an interactive assistant, responsiveness is not a decorative feature. It affects whether people enjoy using the tool or quietly return to doing everything by hand.

Fourth, small models can be specialized. A general model must be prepared to discuss everything from algebra to zucchini. Your assistant may have a narrower job: classify support tickets, summarize internal notes, draft a familiar kind of email, or respond in your preferred voice. With appropriate prompting, retrieval, and careful fine-tuning, a smaller model can become effective within that defined territory.

Notice the careful wording: *can become effective*. Smaller does not automatically mean cheaper, safer, faster, more accurate, or easier. It depends on the model, hardware, software, data, and task. This is where the most important lesson arrives.

Test with your input data.

Model cards and benchmark tables are useful. They tell us about architecture, context capacity, memory requirements, supported languages, and performance on standardized evaluations. They can help eliminate models that are plainly unsuitable. Ignoring those facts would be like buying a car without checking whether it has an engine.

But published statistics cannot fully answer your question: “Will this model work for me?”

Your data has its own personality. It contains your terminology, formatting, abbreviations, edge cases, incomplete sentences, recurring mistakes, and wonderfully specific expectations. A benchmark may show that a model performs well on general mathematics. That does not tell you whether it correctly interprets your invoices. A writing benchmark may suggest polished prose. That does not tell you whether the model sounds like you—or like a committee that has just discovered the phrase “thought leadership.”

Representative testing reveals what specifications cannot.

Give the candidate models the same real tasks. Record their complete answers, not just the answers you hoped to see. Measure accuracy, readability, tone, grammar, response time, and token use. Check whether they follow length requirements. Look for repetition. Watch for invented facts delivered with the confidence of someone who has never met a follow-up question.

Then inspect the failures.

A wrong answer may indicate missing knowledge. It may also reveal a confusing prompt, a faulty answer key, a strict parser, or a model that knew the answer but ignored the required format. Those are different problems with different solutions. Buying a larger model to fix a broken test is an expensive way to remain confused.

Long-form writing makes this especially visible. One model may create a strong opening and then repeat its conclusion until the token limit mercifully intervenes. Another may produce clean, readable prose but stop hundreds of words before the requested length. A benchmark score will not warn you about either behavior. A realistic trial will.

Testing also helps establish the right architecture around the model. Perhaps the model needs an outline before drafting. Perhaps long articles should be generated section by section. Perhaps factual claims should come from approved documents through retrieval. Perhaps a repetition detector should stop a looping response. Perhaps a second pass should verify word count and grammar before anything reaches a reader.

The model is only one component. The prompt, memory, retrieval, validation, generation controls, and human review all contribute to the final result.

This point matters when building a personal assistant. A larger context window can hold more material, but filling it with every conversation you have ever had is not the same as creating wisdom. Useful contextual memory should carry the recent discussion and current task. Long-term memory should retrieve approved preferences, decisions, and examples when they are relevant. Fine-tuning can teach stable aspects of writing style. None of these should become a digital attic where every stray sentence is saved forever “just in case.”

Start with the job, not the leaderboard.

Write down what success means. Assemble representative examples. Include routine cases, difficult cases, and the awkward cases everyone hopes will disappear before launch. Run the same tests against each model. Save the outputs and measurements. Let the evidence surprise you.

You may discover that the larger model is worth its additional cost. Excellent. Now you know why.

You may discover that a smaller model performs the required task just as well, runs locally, responds quickly, and gives you more control. Also excellent. You have not settled for less; you have selected more precisely.

And you may discover that neither model is ready. That is not a failed experiment. Finding a weakness before deployment is one of the least expensive successes available in technology.

So, this #FlexFriday, let us make room for a modest proposal: model selection should be an audition, not a beauty contest.

Read the specifications. Understand the limits. Respect the benchmarks. Then bring your own questions, documents, writing samples, constraints, and inconvenient edge cases. Ask each model to do the work you actually need done.

Because the best AI model is not necessarily the one with the biggest number.

It is the one that passes your test.

### Codex/ChatGPT self-review

| Category | Rating | Self-analysis |
|---|---:|---|
| Accuracy | 9/10 | The article distinguishes testing, contextual memory, long-term memory, retrieval, and fine-tuning. Claims are qualified instead of treating every small model as automatically faster, cheaper, or safer. No external benchmark numbers or invented customer results are presented. A point remains deducted because broad statements about typical SLM cost and speed still depend on the deployment. |
| Readability | 9/10 | Short paragraphs, concrete comparisons, transitions, and a clear progression make the article suitable for online reading. A few middle sections could be tightened. |
| Requested tone | 9/10 | The writing is conversational and uses restrained jokes without turning the technical subject into a comedy routine. Duc should make the final judgment about whether it matches his personal voice. |
| Grammatical correctness | 10/10 | The article uses complete sentences, consistent tense, and intentional fragments for rhetorical effect. No known grammatical errors were identified in review. |
| Token-use efficiency | 9/10 | The response uses its length to develop the requested argument rather than padding the conclusion. Exact hosted-model token usage is unavailable from this repository, so this rating reflects editorial efficiency rather than a measured GPT token count. |
| Elapsed-time efficiency | Not scored | The local evaluator did not generate this article and cannot measure the hosted Codex/ChatGPT model's isolated generation time. The elapsed wall time also included document editing and review, making comparison with one local `generate()` call invalid. |
| **Overall effectiveness** | **9/10** | The article fulfills the subject, format, and tone while making the central argument accurately. Human review by Duc is still required before publication. |

The self-rating is not independent evaluation. Codex/ChatGPT wrote the article
and therefore has an obvious evaluation conflict. Its ratings should be treated
as a documented self-assessment, with Duc's blind editorial rating serving as
the meaningful comparison.

### Meta Llama 3.2 3B — full unedited output

```text
The Power of Small: Why Smaller AI Language Models Can Be a Game-Changer

Welcome back to our #FlexFriday series, where we're shaking things up by highlighting the benefits of going small. Today, we're talking about the often-overlooked world of small AI language models. Yes, you read that right – small. But don't let their size fool you. These tiny titans can pack a big punch when it comes to transforming your workflow, boosting productivity, and making your life easier.

My personal journey with small AI language models began when I stumbled upon a tiny model that could generate human-like text in a matter of seconds. I was blown away by its capabilities and couldn't wait to share my discovery with the world. That's when I realized that these small models were not just limited to generating text, but could also be used to improve content creation, writing, and even customer service.

So, what makes small AI language models so special? For starters, they're incredibly fast and agile. Unlike their larger counterparts, small models don't require a lot of computational power, making them perfect for use on low-end devices or in situations where resources are limited. This means that you can use these models to generate content, answer customer queries, or even create chatbots without breaking the bank.

Another benefit of small AI language models is their ability to learn and adapt quickly. These models are trained on vast amounts of data, which enables them to pick up on patterns and nuances that might elude human writers. This means that you can use these models to generate high-quality content, such as blog posts, social media posts, or even entire books, in a fraction of the time it would take a human writer.

But what really sets small AI language models apart is their ability to test and refine their performance. Unlike larger models, which can be slow to adapt to new data, small models can quickly iterate and improve their performance. This means that you can use these models to test and refine your content, answering questions and addressing concerns in real-time.

Now, I know what you're thinking – "But aren't small AI language models limited by their size?" And to that, I say – not necessarily. While it's true that small models may not have the same level of complexity as their larger counterparts, they can still be incredibly powerful.

In fact, some of the most innovative applications of AI language models are being used in small, agile teams. These teams are able to harness the power of these models to generate high-quality content, answer customer queries, and even create chatbots, all while keeping costs low and resources flexible.

So, how can you start using small AI language models in your own workflow? The answer is simple – start by testing them out with your own input data. Don't rely on the stats and benchmarks of these models – instead, use them to generate content, answer questions, and refine your workflow.

To get started, you'll need to choose a small AI language model that's right for you. There are many options available, ranging from simple text generators to more complex models that can handle multiple tasks. Once you've chosen a model, you'll need to input your own data, which will be used to train and refine the model.

From there, it's simply a matter of using the model to generate content, answer questions, and refine your workflow. You can use these models to create chatbots, generate social media posts, or even create entire books. The possibilities are endless, and the results are nothing short of amazing.

In conclusion, small AI language models may not be the most glamorous or high-profile applications of AI, but they're certainly some of the most powerful. By harnessing the power of these models, you can transform your workflow, boost productivity, and make your life easier. So, don't be afraid to go small – you never know what amazing things you might achieve.
```
