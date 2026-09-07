# QA105 Kids Explanation Post-Fix Results

## Test configuration

- Date: September 6, 2026
- Test data: `data/qa105-kids-fixed.json`
- Test program: `qa-code/test_kids.py`
- Command: `python qa-code/test_kids.py data/qa105-kids-fixed.json`
- Audience: Children ages 10–12
- Tone: Funny, friendly, entertaining, and easy to understand
- Automatic token sequence: 300, 450, then 600 if still capped
- Temperature: 0.3
- Model execution: Sequential

## Executive result

The automatic retry fixed seven of the eight truncations observed in QA104.
Phi completed Star Trek, chess, and baseball at the 450-token attempt. Llama
completed all four topics at 450. Phi's *Great Expectations* response exhausted
all three limits, entered a repetition loop, and still ended unfinished at 600
tokens.

Completion improved, but accuracy did not improve consistently. More output
room allowed both models to finish their explanations, while also giving them
room to produce additional incorrect details. Token retries solve capacity
cutoffs, not knowledge or reasoning errors.

| Measurement | Phi-4 Mini | Llama 3.2 3B |
|---|---:|---:|
| Final responses completed | 3/4 | 4/4 |
| Total generation attempts | 9 | 8 |
| Input tokens across attempts | 1,052 | 1,206 |
| Output tokens across attempts | 3,319 | 2,609 |
| Total consumed tokens | 4,371 | 3,815 |
| Model load time | 1.420 s | 1.122 s |
| Total generation time | 99.491 s | 65.485 s |
| Average time per final topic | 24.873 s | 16.371 s |
| Cleanup time | 0.053 s | 0.042 s |
| End-to-end model run | 101.002 s | 66.677 s |

## Retry results

| Topic | Phi attempts | Phi final tokens | Phi completed | Llama attempts | Llama final tokens | Llama completed |
|---|---:|---:|---|---:|---:|---|
| *Great Expectations* | 3: 300, 450, 600 | 600 | No | 2: 300, 450 | 364 | Yes |
| *Star Trek* | 2: 300, 450 | 327 | Yes | 2: 300, 450 | 310 | Yes |
| Chess | 2: 300, 450 | 416 | Yes | 2: 300, 450 | 360 | Yes |
| Baseball | 2: 300, 450 | 326 | Yes | 2: 300, 450 | 371 | Yes |

## Ratings

### Microsoft Phi-4 Mini

| Explanation | Accuracy | Tone | Ease of understanding | Humor | Entertainment | Overall |
|---|---:|---:|---:|---:|---:|---:|
| *Great Expectations* | 1 | 5 | 4 | 3 | 3 | 2/10 |
| *Star Trek* | 7 | 8 | 8 | 6 | 8 | 7/10 |
| Chess | 4 | 7 | 7 | 6 | 6 | 5/10 |
| Baseball | 2 | 7 | 6 | 5 | 6 | 4/10 |
| **Model average** | **3.5** | **6.8** | **6.3** | **5.0** | **5.8** | **4/10** |

### Meta Llama 3.2 3B

| Explanation | Accuracy | Tone | Ease of understanding | Humor | Entertainment | Overall |
|---|---:|---:|---:|---:|---:|---:|
| *Great Expectations* | 4 | 8 | 8 | 5 | 7 | 6/10 |
| *Star Trek* | 7 | 9 | 9 | 7 | 9 | 8/10 |
| Chess | 8 | 9 | 9 | 7 | 8 | 8/10 |
| Baseball | 6 | 8 | 8 | 6 | 8 | 7/10 |
| **Model average** | **6.3** | **8.5** | **8.5** | **6.3** | **8.0** | **7/10** |

## Full final unedited responses

Only the final attempt for each topic appears below. Token and timing totals
above include discarded capped attempts as well.

### Microsoft Phi-4 Mini

#### Great Expectations

```text
"Great Expectations" is a story about a boy named Pip who lives in England in the 1800s. Pip starts off as a poor boy who lives on a farm with his sister and her husband, Mr. Joe. Pip wants more than just farm life, so he saves up money to go to a big city called London to be a gentleman.

One night, a mysterious woman offers Pip a fortune, promising him great things in life. Pip gets a scholarship to a special school called Magwitch School, but he struggles with his rough background and the snobbery of his new schoolmates.

Pip meets a scruffy boy named Estella, who is supposed to be a snob but secretly wants Pip to love her just like she wants him to love Estella. Estella is Mr. Misses' daughter, and Mr. Misses is a nasty man who uses Estella to mistreat people.

Pip learns that Mr. Misses is really Estella's benefactor, who saved her money so Estella could be mistreated by Mr. Misses. Pip decides to help Mr. Misses secretly, but Estella accidentally hurts Pip badly.

Pip becomes rich but unhappy because he misses Estella and Mr. Misses. Estella tries to be nice to Pip but is just pretending to be nice.

Finally, Pip meets Mr. Misses again, but Mr. Misses tells Pip that Estella is just a snob and not really a nice person. Pip realizes Estella isn't really nice, just like Mr. Misses says.

Pip decides Estella isn't really a snob and they are friends, but Estella is just pretending to be nice to Pip.

Pip learns that true gentility isn't just money and snobbery, but treating people fairly and not mistreating anyone just like Mr. Misses does.

Pip decides Estella isn't really a snob and they are friends, but Estella is just pretending to be nice to Pip.

Pip learns that true gentility isn't just money and snobbery, but treating people fairly and not mistreating anyone just like Mr. Misses does.

Pip decides Estella isn't really a snob and they are friends, but Estella is just pretending to be nice to Pip.

Pip learns that true gentility isn't just money and snobbery, but treating people fairly and not mistreating anyone just like Mr. Misses does.

Pip decides Estella isn't really a snob and they are friends, but Estella is just pretending to be nice to Pip.

Pip learns that true gentility isn't just money and snobbery, but treating people fairly and not mistreating anyone just like Mr. Misses does.

Pip decides Estella isn't really a snob and they are friends, but Estella is just pretending to be nice to Pip.

Pip learns that true gentility isn't just money and snobbery, but
```

This response is largely fabricated. Pip does not save money to attend a
“Magwitch School,” Estella is not a boy or “Mr. Misses' daughter,” and the plot
described does not represent the novel. It also repeats two paragraphs and hits
the final 600-token ceiling.

#### Star Trek

```text
Hello future space explorers! Imagine a world far away from Earth, where a group of brave people travel on a ship called a Starship, like a Star Wars Tatooine junket but way cooler because they go to different parts of space to explore and make new friends! This Star Trek adventure is all about space travel, meeting different aliens, and learning how to work together as a crew on a mission.

The Star Trek crew consists of different people who each have a special role on the ship, just like a school class has different teachers and students with different jobs. Some crew members are doctors who look after everyone, while others are engineers who fix things or pilot spaceships like a video game.

One really important part of Star Trek is the Federation, a group of different planets and peoples who live together in peace and work on making new discoveries together. It’s like a giant school project where everyone brings different skills and knowledge to solve problems and explore space together.

The Star Trek stories often talk about treating everyone fairly, sharing discoveries, and making new friends from different parts of space. It’s a mix of adventure, science (like learning how things work on different planets), and teaching us how to be better friends on Earth and far away in space.

And just so you know, Star Trek is a lot like a dream come true for people who love science, space travel, and making new friends from different parts of the universe! So, next time you look up at the night sky, just think – maybe one day, you’ll be on a Star Trek mission visiting distant planets and making friends among the stars! 🚀✨
```

This response is complete and broadly accurate. The Star Wars/Tatooine analogy
is distracting and “junket” is not child-friendly vocabulary. The Federation
description is simplified but useful.

#### Chess

```text
Hey there, future grandmaster! Have you ever seen a battle of tiny warriors on a cheezy battlefield? Well, that battle is called chess, and it's a super fun game that people play all over the world!

The battlefield is a square board divided into 64 smaller squares (like a giant tic-tac-toe grid). There are two armies on each side, each led by a king (one king per color, black or white).

The first player (let's say black) starts by setting up their pieces on their side of the battlefield, while the second player (let's say white) does the same on their side.

The main goals are to checkmate (or "checkmate") the opponent's king, which means putting him in a position where he is in check (under threat of capture) and cannot escape to safety.

The black army has a King, Queen, Rooks (two different shaped pieces called rooks), Knights (those L-shaped pieces), and Bishops (those pieces that slide diagonally). The white army has the same pieces but different colors (like black and white).

The black Queen is a real powerhouse (she can move any number of spaces forward, backward, left, or right). She has a couple of close buddies on her team, too: her black King (who just wants to stand guard on his tiny throne), black Rooks (who stand tall on their corners, ready to jump forward or slide diagonally), black Knights (who jump around L-shaped), and black Bishops (who slide diagonally).

The white King (who just wants to stand guard on his tiny throne), white Rooks (who stand tall on their corners, ready to jump forward or slide diagonally), white Knights (who jump around L-shaped), and white Bishops (who slide diagonally).

The black and white armies clash on this cheezy battlefield, each trying to checkmate the other king while avoiding getting checkmated themselves!

Good luck, future grandmaster, and may the cheezy battle begin!
```

The response finishes but contains major rule errors. White moves first, rooks
cannot jump or move diagonally, and queens can also move diagonally. Pawns are
not explained. Completion alone did not make the explanation reliable.

#### Baseball

```text
Hey there, future baseball star! Imagine a giant playground where you and your friends (or teammates) compete to be the champion. This playground is called a baseball field, and it's packed with action, goals, and a whole lot of fun!

First off, a baseball game is like a battle between two teams, each trying to beat the other and score runs faster than they can beat. Each team has nine players who take turns trying different goals on the field.

The game is divided into parts called "innings." Just like rounds on a video game, each team gets a chance to bat (swing a bat) and field (catch and throw or stop the ball from getting passed along). If one team manages to beat all eight teams on their field (that's eight parts of a whole field), they win an inning!

When a team is batting, they try to hit the ball so they can run around a bunch of bases (kind of like a track). Running bases is super fun, right? If they can touch all eight bases before someone throws or catches the ball, they score a run!

Fielders work on catching or throwing the ball to stop or speed up the game. If they stop a runner from reaching a base or stop a passed ball from making a run, they get an "out."

The ultimate goal is to beat your team so badly that they can't beat you back. If one team scores more runs before all eight parts of a whole field are beaten, they win the game!

Keep practicing, and maybe one day you'll be swinging that bat like a champion on a real baseball field! Go team!
```

The response is complete but fundamentally inaccurate. Baseball has two teams,
four bases including home plate, and nine standard innings, not eight teams,
eight bases, or eight parts of a field. Its explanation of an out is also
unreliable.

### Meta Llama 3.2 3B

#### Great Expectations

```text
Hey there, young reader! Let's dive into the amazing world of Charles Dickens's novel, Great Expectations.

Pip is the main character in this story. He's a young boy who lives with his abusive sister and her husband, a blacksmith. Pip's life is pretty tough, but he's lucky to have a kind friend named Joe Gargery, who helps him out. One day, while visiting his parents' graves, Pip meets a convict named Abel Magwitch, who demands that Pip steal food and money for him. Pip does this, and it changes his life forever.

Magwitch is a mysterious character who turns out to be a wealthy man. He hires Pip to be his lawyer and sends him to London to live with a wealthy gentleman named Miss Havisham. Pip's life is now full of excitement and luxury, but he's also very confused. He's not sure what's going on or why he's been treated so differently.

As Pip navigates his new life, he meets a cast of interesting characters, including the beautiful Estella, who's been raised by Miss Havisham to be cold and heartless. Pip falls in love with Estella, but she's not interested in him. He also meets Herbert Pocket, the son of Miss Havisham's brother, who becomes his friend. Through his experiences, Pip learns that money can't buy happiness and that true friends are the most valuable things in life.

Pip's journey is all about self-discovery and learning to appreciate what's truly important. He realizes that his life with Joe Gargery was happy and meaningful, even if it wasn't luxurious. In the end, Pip comes to understand that his experiences have taught him valuable lessons, and he's grateful for the people who care about him.
```

The response finishes but contains major plot errors. Magwitch does not hire Pip
as a lawyer or send him to live with Miss Havisham, who is a woman rather than a
gentleman. Pip steals food and a file, not money. The themes are reasonable, but
the summary is not accurate enough for educational use.

#### Star Trek

```text
Hey there, young space traveler! Are you ready to explore the galaxy with the most awesome crew in the universe? Star Trek is a super cool TV franchise that's all about space exploration, adventure, and making the universe a better place.

Imagine a group of brave and clever people who travel through space in a fancy spaceship called a starship. They're on a mission to explore new worlds, meet new civilizations, and learn new things. The crew is made up of different types of people, like scientists, engineers, and even a captain who leads the team. They work together to solve problems, make new discoveries, and have some serious fun along the way.

The Star Trek universe is actually a group of planets and stars called the Federation. It's like a big team effort, where different planets and civilizations work together to make the universe a better place. The Federation is all about peace, friendship, and exploring the unknown. And, just like you, the crew of the starship is on a quest to learn, grow, and have amazing adventures.

One of the coolest things about Star Trek is that it's not just about the technology or the gadgets – it's about the people and their values. The crew of the starship is all about being kind, respectful, and curious. They're always asking questions, trying new things, and pushing the boundaries of what's possible. And, that's what makes Star Trek so awesome – it's all about exploring the universe and making it a better place, one adventure at a time!
```

This is complete, friendly, and mostly accurate. The Federation is an
organization of member worlds, not the Star Trek universe itself. The response
also generalizes one crew and starship across a franchise with many series.

#### Chess

```text
Hey there, young adventurer! Are you ready to explore one of the coolest games ever - Chess!

Imagine you're a detective trying to solve a mystery. You have clues (pieces) that can help you figure out the answer. That's basically what Chess is all about. Your goal is to capture your opponent's king, the most important piece on the board. It's like a big puzzle, and you need to think ahead to outsmart your opponent.

The Chess board is like a big grid, with 64 squares. It's divided into rows and columns, like a big checkerboard. You and your opponent will take turns moving one piece at a time. There are six types of pieces: the king, queen, rook, bishop, knight, and pawn. Each piece has its own special moves and powers.

Let's talk about the pieces:

- The king is the most important piece. You need to protect it at all costs!
- The queen is like a superhero - she can move in any direction (up, down, left, right, or diagonally) any number of squares.
- The rook is like a strong castle wall - it can move horizontally or vertically any number of squares.
- The bishop is like a wise advisor - it can move diagonally any number of squares.
- The knight is like a little horse - it moves in an L-shape (two squares in one direction, then one square to the side).
- The pawn is like a foot soldier - it can move forward one or two squares, but captures diagonally.

That's a basic overview of Chess. It's a game that takes time and practice to master, but it's so much fun. So, grab a friend, set up the board, and start playing!
```

This explanation is complete and mostly accurate. The objective is checkmate,
not capture of the king. A pawn may move two squares only from its starting
position. The movement summaries otherwise suit the intended audience.

#### Baseball

```text
Hey there, young baseball fan! Let's talk about one of the coolest sports out there - baseball!

Imagine you're playing with your friends in a big field. You're all divided into two teams, and your goal is to hit a ball with a bat and run around the four bases on the field. That's basically what baseball is all about. Each team has nine players, and the team with the most players on the field is called the offense. The team with the fewest players is called the defense.

Now, let's talk about innings. An inning is like a round of a game. Each team gets a chance to bat and play defense. The teams take turns playing offense and defense, and the team with the most runs at the end of nine innings wins the game. But here's the thing: you can't score a run if you're not on base. That's where batting and fielding come in.

When you bat, you try to hit the ball with a bat. If you hit the ball, you can try to run to first base, then second, then third, and finally home plate. If you make it around all the bases without getting out, you score a run! But if you get out, you have to go sit down and wait for your next turn. There are three ways to get out: you can strike out (miss the ball three times), you can fly out (hit the ball in the air and someone catches it), or you can ground out (hit the ball on the ground and someone picks it up and throws you out).

The team with the most runs at the end of nine innings wins the game. It's like a big competition to see who can score the most runs. And that's the basic goal of baseball - to score more runs than the other team!
```

The explanation is complete and covers the requested concepts, but offense and
defense are not determined by which team has more players on the field. The
batting team is offense and the fielding team is defense. There are also more
than three ways to record an out, so that sentence should say “three common
ways.”

## Comparison with QA104

| Outcome | QA104 baseline | QA105 automatic retry |
|---|---:|---:|
| Complete final responses | 1/8 | 7/8 |
| Phi generation time | 34.142 s | 99.491 s |
| Llama generation time | 29.082 s | 65.485 s |
| Phi overall rating | 5/10 | 4/10 |
| Llama overall rating | 7/10 | 7/10 |

The retry mechanism improved completion from 12.5% to 87.5%, but increased
generation time and token consumption because capped drafts were discarded.
Phi's quality rating decreased because the longer final outputs exposed severe
fabrication and repetition. Llama retained the same overall rating: completion
improved, while factual errors remained.

## Recommendations

1. Keep the bounded retry sequence; it prevented unlimited generation.
2. Add a repetition detector so Phi's third attempt can stop and fail early.
3. Ask for a concrete 140–180-word target. The completed responses currently
   range from 257 to 320 words, longer than necessary for the audience.
4. Consider starting directly at 400 or 450 tokens. This avoids paying for a
   discarded 300-token attempt when these prompts predictably need more room.
5. Add topic-specific fact sheets or retrieval before generation.
6. Run a factual validator after generation and reject serious errors even when
   the prose is complete and friendly.
7. Record a final status such as `COMPLETE`, `CAPPED`, or `REPETITION_STOPPED`
   rather than inferring success only from token count.

## Conclusion

The automatic token fix works as a completion mechanism, but it is not a quality
mechanism. Llama is the stronger model in QA105 because it completes every
response and provides substantially more accurate explanations. Neither model
is ready for unsupervised educational content without factual review.
