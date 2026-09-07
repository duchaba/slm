# QA104 Kids Explanation Test Results

## Test configuration

- Date: September 6, 2026
- Test data: `data/qa104-kids.json`
- Test program: `qa-code/test_kids.py`
- Command: `python qa-code/test_kids.py data/qa104-kids.json`
- Audience: Children ages 10–12
- Tone: Funny, friendly, entertaining, and easy to understand
- Topics: *Great Expectations*, *Star Trek*, chess, and baseball
- Temperature: 0.3
- Maximum output: 300 tokens per explanation
- Model execution: Sequential

The input normalizes the user-provided title “The Great Expectation” to Charles
Dickens's correct book title, *Great Expectations*.

## Executive result

Llama produced the stronger set of explanations, especially for chess and
baseball. Phi used an energetic, child-friendly voice but introduced serious
factual errors in every topic. Both models struggled with *Great Expectations*.

The 300-token ceiling was too restrictive. Phi hit it on three responses and
Llama hit it on all four, leaving seven of eight explanations unfinished. This
reduced readability and entertainment even when the preceding content was
good.

| Measurement | Phi-4 Mini | Llama 3.2 3B |
|---|---:|---:|
| Input tokens | 469 | 603 |
| Output tokens | 1,146 | 1,204 |
| Total tokens | 1,615 | 1,807 |
| Responses ending at token ceiling | 3/4 | 4/4 |
| Model load time | 1.609 s | 1.014 s |
| Total generation time | 34.142 s | 29.082 s |
| Average generation time | 8.535 s | 7.270 s |
| Cleanup time | 0.041 s | 0.046 s |
| End-to-end model run | 35.810 s | 30.161 s |

## Ratings

### Microsoft Phi-4 Mini

| Explanation | Accuracy | Tone | Ease of understanding | Humor | Entertainment | Overall |
|---|---:|---:|---:|---:|---:|---:|
| *Great Expectations* | 2 | 6 | 6 | 4 | 5 | 4/10 |
| *Star Trek* | 3 | 8 | 7 | 6 | 7 | 5/10 |
| Chess | 4 | 7 | 6 | 6 | 6 | 5/10 |
| Baseball | 3 | 7 | 7 | 5 | 6 | 4/10 |
| **Model average** | **3.0** | **7.0** | **6.5** | **5.3** | **6.0** | **5/10** |

### Meta Llama 3.2 3B

| Explanation | Accuracy | Tone | Ease of understanding | Humor | Entertainment | Overall |
|---|---:|---:|---:|---:|---:|---:|
| *Great Expectations* | 2 | 8 | 8 | 5 | 7 | 5/10 |
| *Star Trek* | 6 | 8 | 8 | 6 | 8 | 7/10 |
| Chess | 8 | 8 | 9 | 7 | 8 | 8/10 |
| Baseball | 8 | 8 | 9 | 6 | 8 | 8/10 |
| **Model average** | **6.0** | **8.0** | **8.5** | **6.0** | **7.8** | **7/10** |

## Full unedited responses and analysis

### Microsoft Phi-4 Mini

#### Case 1 — Great Expectations

```text
Welcome to the world of Great Expectations, a story written by Charles Dickens that's packed with adventure, growth, and a whole lot of surprises!

Meet Pip, a poor but curious boy who lives on a farm in England. Pip has a wild dream – he wants to be a gentleman one day! His life takes a surprising turn when a rich man named Miss Havisham asks Pip to look after her jilted (upset and angry) niece, Estella. Pip agrees, hoping it will help him achieve his dream.

Miss Havisham lives in a grand but decaying mansion, and Pip becomes her devoted helper while Estella becomes his close friend (even though Estella isn't really his pal). Pip starts off as a humble blacksmith's apprentice but quickly becomes a gentleman in Miss Havisham's eyes.

But life's a bit like a rollercoaster ride – fast, fun, and full of twists and turns! Pip learns that being rich isn't everything, and that true gentility comes from kindness, courage, and making the right choices.

Goodbye Pip, and good riddance to Great Expectations – a story that reminds us that true nobility comes from treating others well and making a positive difference in the world!
```

Miss Havisham is a woman, not a rich man. Estella is her adopted daughter, not
her niece, and Miss Havisham does not ask Pip to look after Estella. Pip visits
to play and becomes infatuated with her. Miss Havisham is not the person who
makes Pip a gentleman. The moral about character and wealth is directionally
reasonable, but the plot summary is unreliable.

#### Case 2 — Star Trek

```text
Hey there, space explorer-in-the-making! Have you ever wondered what it would be like to travel through space, meeting different aliens, and discovering new worlds? Well, Star Trek does just that – but on TV! Star Trek is a science fiction adventure where a group of people (the crew) jump into a cool spaceship called a Starship and explore different parts of space together.

The Star Trek crew comes from different parts of a faraway place called Earth, but they live on a giant ship called a Starship, which floats through space on a special track named a Space Elevator. Together, they travel to different planets, space stations, and distant galaxies to find new life forms, strange planets, and maybe a new place to live called a colony.

One of Star Trek's coolest parts is that they are part of a giant group called the Federation, which is a collection of different planets and space stations working together as one big happy family. They help each other out, solve problems together, and stand up for what's right – just like friends would do on Earth!

Star Trek is not just about space travel and meeting aliens, though. It tells stories about friendship, bravery, and fighting for a better future. It makes you think about big questions like how we should treat each other, what makes a good leader, and how we can work together to make a difference.

And just so you know, Star Trek has different Star Ships and different crew members in different Star Trek series, but they
```

Starships do not float on a track called a Space Elevator. Crews can include
humans from Earth, aliens, and other beings, depending on the series. The
Federation explanation and themes are broadly suitable, but the invented
technology is a serious error. The response also ends unfinished.

#### Case 3 — Chess

```text
Hey there, future grandmaster! Have you ever seen a battle of black and white pieces on a checkered battlefield? No? Well, that’s called chess, a super cool game where you think ahead and try to beat your opponent.

The chessboard looks like a giant tic-tac-toe grid but way cooler because it has 64 squares (32 black, 32 white) and two teams of pieces (one black, one white). It’s like a giant battlefield covered in a giant blanket covered in black and white stripes.

The main goals are to checkmate (or "checkmate") your opponent's king, which means putting him in a position where he is in check (under threat of capture) and has no legal moves left.

There are different pieces on each color team:
- Kings (one black, one white) are super important because they are the last standers on the battlefield.
- Queens (one black, one white) are super strong and can move like a king but they are just one piece away from breaking down!
- Rooks (one black, one white) are like castle guardians—they stand tall on either side of the battlefield.
- Knights (one black, one white) are a bit weird—they jump around in an L-shape (two squares forward, one square to the side).
- Bishops (one black, one white) slide diagonally across the battlefield, like they are sliding down a slide on one color team and sliding up on
```

The board and checkmate descriptions are broadly correct, but each player has
two rooks, two knights, and two bishops, not one of each color across the whole
game. The queen does not “move like a king”; she moves any unobstructed distance
along ranks, files, or diagonals. The response omits pawns and ends unfinished.

#### Case 4 — Baseball

```text
Hey there, future baseball star! Imagine a giant playground divided into two teams, each trying to beat the other by scoring points. This playground is called a baseball field, and it's where an exciting game called baseball happens.

There are two teams on the field, and each team tries to score runs by getting a player (called a 'batter') to hit a ball and run around a series of bases (like stepping stones on a playground). There are nine of these bases arranged in a diamond shape, and they are labeled first base, second base, third base, and home plate.

A game is divided into parts called 'innings.' Just like you take breaks during recess, baseball teams take breaks too, so they alternate batting (hitting the ball) and fielding (catching and throwing down balls). Each inning has two halves, called 'half-innings.' One team bats first, and then the other team does the same.

When a batter hits the ball, they try to run as fast as possible to different bases, starting from first base and aiming to finish on home plate, collecting points called 'runs' along the way. If they are caught while running, or if they fail to run fast enough, it's called an 'out.' Just like a missed shot during recess, an out is a little setback for a team.

The ultimate goal is to beat your team by reaching more bases (collecting more runs) while avoiding making too many outs. If a team makes
```

A baseball diamond has four bases when home plate is included, not nine. An out
does not occur merely because a runner “fails to run fast enough,” and runs are
scored by safely reaching home rather than collected at each base. The goal is
to beat the other team, not “your team.” The innings description is useful, but
the response ends unfinished.

### Meta Llama 3.2 3B

#### Case 1 — Great Expectations

```text
Hey there, young bookworm! Let's talk about Charles Dickens's amazing novel, Great Expectations.

Meet Pip, a young boy who lives with his kind sister, Bessie, and their mean old brother-in-law, Joe. Pip's life is pretty simple: he likes to explore the marshes near his home, where he meets a convict named Abel Magwitch. Magwitch is a mysterious and kind man who asks Pip to do a favor for him. Pip agrees, and his life changes forever.

Pip's great-uncle, a wealthy man named Mr. Jaggers, decides to help Pip and sends him to London to live with a wealthy friend of his. Pip's new life is full of luxury and excitement, but it's also full of surprises and challenges. He meets a beautiful girl named Estella, who is being raised by Mr. Jaggers to be a lady. Pip falls in love with Estella, but she's not interested in him.

As Pip navigates his new life, he learns some important lessons. He realizes that money and wealth aren't everything, and that true friends and family are what truly matter. He also learns that people are not always what they seem, and that appearances can be deceiving. Through his adventures, Pip discovers that his life has been changed forever, and that he must learn to navigate his new reality.

Great Expectations is a classic tale of love, friendship, and self-discovery. It's a story about
```

Bessie is not Pip's sister; Mrs. Joe is his sister, Joe is Pip's kind
brother-in-law, and Bessie is a friend and teacher. Jaggers is a lawyer, not
Pip's great-uncle or the person financing his expectations. Estella is raised
by Miss Havisham, not Jaggers. Magwitch initially frightens and threatens Pip,
so calling him simply kind removes important context. The response is friendly
but factually poor and incomplete.

#### Case 2 — Star Trek

```text
Hey there, young space traveler! Are you ready to explore the galaxy with the crew of Star Trek? This amazing TV franchise is all about space exploration and the adventures of a group of brave and brilliant individuals who travel through the cosmos in search of new worlds and new civilizations.

At the heart of Star Trek is a team of explorers who represent different countries and cultures from the United States. They're all experts in their fields, from science and technology to diplomacy and leadership. The crew is led by a captain, who is like a superhero, but instead of superpowers, they have amazing skills and knowledge that help them navigate the challenges of space travel.

The crew travels on a spaceship called a starship, which is like a giant flying machine that can take them to the farthest reaches of the galaxy. The starship is part of a larger organization called the United Federation of Planets, which is like a team of countries working together to explore and protect the universe. The Federation is all about peace, cooperation, and mutual respect, and its members are united in their quest for knowledge and understanding.

One of the coolest things about Star Trek is that it's not just about the technology or the adventures – it's also about the themes and messages that the show conveys. Star Trek often explores big questions like what it means to be human, how we treat each other, and how we can work together to solve problems and make the universe a better place. It's like a big, cosmic
```

The broad franchise concept, Federation, and themes are described well. The
claim that crews represent cultures “from the United States” is incorrect;
Star Trek crews are internationally and often interplanetarily diverse.
Calling the captain a superhero oversimplifies the role, and protecting “the
universe” overstates the Federation's scope. The explanation ends unfinished.

#### Case 3 — Chess

```text
Hey there, young adventurer! Are you ready to explore one of the coolest games ever - Chess!

Imagine you're a general in a secret mission to save the kingdom. Your goal is to capture your opponent's king, which is like the most powerful person in the kingdom. To do this, you'll need to move your pieces around the board, using strategy and skill to outsmart your opponent.

The board is like a big battlefield, with 64 squares arranged in an 8x8 grid. You'll have 16 pieces to help you on your mission: one king, one queen, two rooks, two knights, two bishops, and eight pawns. Each piece has its own special powers, which we'll explore below.

Let's meet your team! You'll play as White, and your opponent will be Black. You'll take turns moving one piece at a time. The pieces are:

* King: The most important piece, as you want to keep it safe.
* Queen: The most powerful piece, able to move in any direction (up, down, left, right, or diagonally).
* Rook: A strong piece that can move horizontally or vertically.
* Bishop: A piece that can move diagonally.
* Knight: A piece that jumps over other pieces to land on a square.
* Pawn: The foot soldiers, able to move forward one or two squares, but captures diagonally.

That's a basic overview of Chess! It's a game
```

The board, starting piece counts, turns, and movement summaries are mostly
accurate and accessible. Chess ends with checkmate rather than capture of the
king. Pawns may move two squares only from their starting position, and the
knight's L-shaped move is not explained. Assigning the reader White is
unnecessary. The response ends unfinished.

#### Case 4 — Baseball

```text
Hey there, young baseball fan! Are you ready to learn about America's favorite pastime?

Baseball is a team sport played with a ball and bat. There are two teams: the home team and the visiting team. The home team plays on their own field, and the visiting team plays on the other team's field. Each team has nine players on the field at a time.

The game is divided into innings. Think of an inning like a chapter in a book. Each team gets a chance to bat (hit the ball) and field (catch the ball). The team with the most runs at the end of nine innings wins the game!

When it's your turn to bat, you try to hit the ball thrown by the opposing team's pitcher. If you hit the ball, you can try to run to one or more bases on the field. If you make it around all four bases (first, second, third, and home plate), you score a run! The goal is to score more runs than the other team.

Now, let's talk about some common baseball terms:

- **Outs**: When a player is tagged (touched) with the ball by the opposing team's fielder, or when they hit the ball in the air and a fielder catches it, they are said to be "out."
- **Runs**: When a player scores by running around all four bases, they score a run!

That's a basic overview of baseball! It's a
```

The basic objective, teams, innings, batting, fielding, bases, runs, and two
common kinds of outs are accurate and age-appropriate. The description of the
home and visiting teams is redundant, and the game can extend beyond nine
innings when tied. The response does not need rare exceptions, so that omission
is acceptable. It still ends unfinished.

## Findings and recommendations

The most urgent improvement is raising the output ceiling to about 400 tokens
or explicitly asking for 150–200 words. A completion check should reject any
response that ends mid-sentence. More tokens alone will not fix fabricated
facts, so each topic also needs factual review or a short verified source note.

For child-oriented explanations:

1. Prefer one or two accurate analogies rather than stacking metaphors.
2. Validate names, relationships, counts, objectives, and essential rules.
3. Avoid calling something “cool” or “amazing” repeatedly as a substitute for
   humor.
4. Use short sentences, define necessary terms, and finish with one memorable
   idea.
5. Test comprehension with children or educators rather than relying only on
   an AI reviewer.
6. Score factual accuracy before tone. A friendly false explanation remains a
   poor educational response.

## Truncation investigation

### Root cause

The unfinished responses were caused by the evaluator's **300-new-token output
limit**, not by either model's 128K context-window capacity.

The QA104 evaluator calls `generate()` with `max_tokens=300`. Generation stops
as soon as either:

1. The model emits its end-of-sequence marker, meaning it chose to finish; or
2. The generator produces 300 new tokens, meaning the evaluator forces it to
   stop.

The evidence is visible in the measurements:

| Model and response | Re-encoded output tokens | Ending |
|---|---:|---|
| Phi — *Great Expectations* | 247 | Finished normally |
| Phi — *Star Trek* | 300 | Cut off at “but they” |
| Phi — chess | 300 | Cut off at “sliding up on” |
| Phi — baseball | 299 | Cut off at “If a team makes” |
| Llama — *Great Expectations* | 301 | Cut off at “It's a story about” |
| Llama — *Star Trek* | 301 | Cut off at “It's like a big, cosmic” |
| Llama — chess | 301 | Cut off at “It's a game” |
| Llama — baseball | 301 | Cut off at “It's a” |

Counts of 299 or 301 still indicate the same 300-token internal limit. The
report counts tokens by re-encoding decoded text after generation. Tokenizer
handling of whitespace and an omitted or added special token can move that
approximation by one token.

The input prompts used only 112–161 tokens. Even after adding 300 output tokens,
each request remained far below 1,000 tokens and therefore nowhere near the
131,072-position context limit. Increasing the context window would not resolve
this failure.

The models also received a request for a “short explanation” without a precise
word target. Both frequently planned more material than would fit in 300 tokens:
an introduction, several explanatory paragraphs, piece or rule lists, and a
conclusion. The token ceiling then interrupted that plan. Llama was especially
consistent in using the entire allowance.

### Resolution

The recommended solution has several layers:

1. **Increase the QA104 output allowance to 400–450 tokens.** This should give
   most of these drafts room to complete. A 500-token ceiling provides more
   margin but can encourage unnecessary length.
2. **Set a word target in the prompt.** Ask for approximately 140–180 words and
   no more than three short paragraphs. A model can follow a concrete size more
   reliably than the word “short.”
3. **Tell the model to reserve space for its ending.** Require one final
   sentence that states the main idea and instruct it to stop after that
   sentence.
4. **Detect probable truncation.** Mark a response incomplete when its internal
   generated-token count reaches the configured maximum, regardless of whether
   the final character happens to be punctuation.
5. **Validate completion.** Check for an incomplete final sentence, open list,
   unmatched formatting marker, or phrases such as “It's a” at the end.
6. **Retry with a correction prompt.** If a response is too long or truncated,
   ask for a complete rewrite within the word target. Rewriting is usually
   cleaner than blindly continuing from a broken sentence.
7. **Use continuation only when preservation matters.** A continuation can
   finish an otherwise valuable response, but it may repeat content or produce
   a conclusion that does not fit the earlier text.
8. **Record the stop reason.** Future evaluator output should distinguish a
   natural end-of-sequence from a maximum-token stop. The current post-generation
   re-encoding is useful evidence but is only an approximation.

A suitable next test configuration is:

```text
Audience: age 10–12
Length: 140–180 words
Structure: two explanatory paragraphs and one short conclusion
Maximum generation: 450 tokens
Completion rule: finish the conclusion, then stop
```

This change should resolve most cutoffs without enlarging the context window.
It will not correct factual errors such as wrong character relationships, chess
piece counts, or baseball bases. Those require better grounding, a verified
fact sheet, retrieval, or a separate factual-review pass.

## Conclusion

Llama wins QA104 with an overall rating of 7/10, largely because its chess and
baseball explanations are clear and mostly accurate. Phi scores 5/10 because
its lively tone is undermined by repeated factual errors. Neither model is
ready to produce unsupervised educational summaries from this configuration,
and both need a larger output allowance plus factual validation.

## Implemented automatic token-limit fix

After the baseline run, `qa-code/test_kids.py` was updated to increase the
output allowance automatically when a response appears to have reached its
token ceiling. The original measurements and ratings above remain unchanged so
QA104 continues to preserve the 300-token baseline.

### Default retry sequence

```python
DEFAULT_TOKEN_LIMITS = (300, 450, 600)
```

For each topic, the evaluator now follows this bounded process:

1. Generate a complete response from the original prompt with a 300-token
   allowance.
2. Re-encode the response with the model's tokenizer.
3. Treat the response as probably capped when its approximate output count is
   within two tokens of the current allowance.
4. If capped, discard that incomplete response and regenerate from the original
   prompt with 450 tokens.
5. If the second response is also capped, regenerate once with 600 tokens.
6. Stop after the 600-token attempt even if the response remains incomplete.

Every retry starts from the original prompt instead of continuing a broken
sentence. This generally produces a more coherent explanation, although a
creative-temperature retry may use different wording.

The upper bound is an important safety and performance control. The evaluator
does not permit the model to increase its own allowance indefinitely. A fixed
sequence limits the time and tokens that can be consumed by repetition or a
model that repeatedly fails to finish.

### Truncation-detection rule

The current `mlx_lm.generate()` use in this evaluator returns decoded text
rather than a recorded stop reason. The code therefore uses this approximation:

```python
output_tokens >= token_limit - 2
```

The two-token tolerance accounts for special end tokens or whitespace that may
appear differently after decoding and re-encoding. This is safer than requiring
exact equality, but it is not perfect. A naturally completed response that
happens to end near the ceiling may be retried unnecessarily, and an unusually
tokenized truncated response could theoretically escape detection. A native
generation stop reason should replace the heuristic if the runtime exposes one
in a future version.

### New reporting fields

The evaluator now records the following for every final response:

- Number of generation attempts
- Token ceilings attempted
- Final response token count
- Approximate tokens generated across all attempts, including discarded drafts
- Total generation time across all attempts

Input tokens are also counted for every attempt when model-level totals are
reported. This prevents a retry from appearing free merely because only the
final response is displayed.

### Commands

Run QA104 with automatic increases:

```bash
.venv/bin/python qa-code/test_kids.py data/qa104-kids.json
```

Choose a different bounded sequence:

```bash
.venv/bin/python qa-code/test_kids.py \
  data/qa104-kids.json \
  --token-limits 300,450,600
```

Disable retries and use one fixed limit:

```bash
.venv/bin/python qa-code/test_kids.py \
  data/qa104-kids.json \
  --max-tokens 450
```

The `--token-limits` values must be positive and strictly increasing. Invalid
or decreasing sequences are rejected before inference.

### What the fix does not solve

The automatic retry addresses probable output truncation only. It does not:

- Correct inaccurate facts
- Guarantee a concise response
- Detect every incomplete sentence
- Prevent repetition inside a response
- Make a larger context window necessary
- Improve humor or age appropriateness automatically

A model could use all three allowances and still fail. Future work should add a
completion validator, repetition detection, the requested 140–180-word target,
and factual review. If the final 600-token attempt is still capped, the test
should report an explicit failure rather than silently treating the response as
complete.

### Verification status

The updated Python file passed syntax and whitespace validation. QA104 has not
yet been rerun with automatic retries, so this section documents the implemented
fix rather than new model results. A follow-up run should be stored separately
or clearly labeled as a post-fix comparison to preserve the original baseline.
