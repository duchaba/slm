# Local SLM project

This project runs Microsoft Phi-4 Mini Instruct and Meta Llama 3.2 3B
Instruct locally on Apple Silicon with MLX. The downloaded checkpoints are
4-bit MLX conversions of the models hosted on Hugging Face, which keeps memory
use practical on a 16 GB Mac.

The current command-line comparison loads the models sequentially, asks both
the same question, and prints their answers. Local API serving and fine-tuning
will be added in later phases.

## Requirements

- An Apple Silicon Mac (M1 or newer)
- macOS with Metal support
- At least 16 GB of unified memory recommended
- Approximately 4 GB free for model files, plus space for Python dependencies
- Git and Python 3.9 or newer
- An internet connection for the initial installation and model downloads

## Download and install

### 1. Clone the repository

```bash
git clone https://github.com/duchaba/slm.git
cd slm
```

### 2. Create and activate a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

All remaining commands assume the virtual environment is active and the
current directory is the repository root.

### 3. Install the Python dependencies

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

This installs MLX-LM for local inference and Hugging Face Hub's `hf` download
command.

### 4. Download both models from Hugging Face

```bash
hf download mlx-community/Phi-4-mini-instruct-4bit \
  --local-dir models/phi-4-mini-instruct-4bit

hf download mlx-community/Llama-3.2-3B-Instruct-4bit \
  --local-dir models/llama-3.2-3b-instruct-4bit
```

The model sources are:

- `mlx-community/Phi-4-mini-instruct-4bit`
- `mlx-community/Llama-3.2-3B-Instruct-4bit`

Model files are intentionally excluded from Git because they total about
3.7 GB and can be reproduced with the commands above.

### 5. Verify the installation

```bash
python qa-code/ask_models.py
```

Expected answers should identify Paris as the capital of France. Exact wording
can vary because text generation may sample from multiple valid continuations.

## Usage

Pass a different question as the first argument:

```bash
python qa-code/ask_models.py "Write a short welcome email."
```

Limit the maximum generated response length when needed:

```bash
python qa-code/ask_models.py --max-tokens 32 "What is the capital of France?"
```

Display all command-line options:

```bash
python qa-code/ask_models.py --help
```

## Run the command-line SLM app

Run `ask_slm.py` from the repository root. Activate the project's virtual
environment first so the command uses the installed MLX dependencies:

```bash
cd /Users/duchaba/Documents/slm
source .venv/bin/activate
```

The command syntax is:

```text
python qa-code/ask_slm.py "QUESTION" MODEL [PROMPT_TEMPLATE] [OPTIONS]
```

The arguments are:

- `QUESTION`: The complete question or writing request, enclosed in quotes.
- `MODEL`: Use `phi` for Microsoft Phi-4 Mini or `llama` for Meta Llama 3.2
  3B. The alias `llamda` is also accepted.
- `PROMPT_TEMPLATE`: Optional path to another prompt-template file. When this
  argument is omitted, the app uses `prompt-template/confidence-answer.txt`.

For example, ask Phi a stable factual question:

```bash
python qa-code/ask_slm.py "What is the capital of France?" phi
```

An expected response is:

```text
CONFIDENCE: HIGH
ANSWER: Paris.

Output: 12 tokens | attempted limits: 300

Elapsed time: 4.307 seconds
```

Exact wording, token count, and elapsed time can vary. Ask Llama a writing
question by changing the final model argument:

```bash
python qa-code/ask_slm.py "Write me a short love poem." llama
```

The default confidence template tells the local model to identify uncertain or
unavailable answers. Because the app has no internet connection or live-data
tool, a question about current weather should return `UNKNOWN` with a reason:

```bash
python qa-code/ask_slm.py "What is the current weather in Fremont, CA?" phi
```

Use a custom prompt by supplying its path as the third positional argument:

```bash
python qa-code/ask_slm.py "Your question" llama path/to/custom-template.txt
```

Templates must contain one `{question}` placeholder and one `{context}`
placeholder. This command has no live-data source, so `{context}` is currently
filled with `None`.

The app automatically starts with a 300-token output allowance. If the response
reaches that limit, it retries from the original prompt with 450 and then 600
tokens. This bounded retry prevents most cut-off poems and articles without
allowing generation to grow indefinitely. Customize the retry sequence with:

```bash
python qa-code/ask_slm.py "Write me a love poem." phi --token-limits 400,600,800
```

To disable automatic retries and use one fixed allowance:

```bash
python qa-code/ask_slm.py "Explain photosynthesis." phi --max-tokens 256
```

Display the complete usage guide, including model names, prompt templates, and
token options:

```bash
python qa-code/ask_slm.py --help
```

## Run the true-or-false QA test

The repository includes `data/qa1-true-false.csv`, which contains ten factual
statements and their expected `True` or `False` answers. Run the same suite
against both models with:

```bash
python qa-code/test_models.py
```

The report shows each model's expected and actual answer, pass/fail status, and
overall accuracy. To run another compatible test suite, provide its path:

```bash
python qa-code/test_models.py path/to/questions.csv
```

Compatible CSV files must use this structure:

```csv
question,answer
Paris is the capital of France.,True
Mars is the closest planet to the Sun.,False
```

Answers are case-insensitive when the CSV is loaded, but must be either `True`
or `False`.

## Run the open-ended algebra-solving test

`data/qa5-algebra-solving.csv` contains ten high-school algebra problems with
numeric answers instead of true/false labels. Run it with:

```bash
python qa-code/test_algebra_solving.py
```

The evaluator asks each model to show brief reasoning and finish with
`ANSWER: <number>`. It grades integers, decimals, and fractions as exact numeric
values. A different compatible CSV can be supplied as the first argument.

## Run the fill-in-the-blank history test

`data/qa6-world-history.csv` contains ten world-history questions with short text
answers. Run it with:

```bash
python qa-code/test_fill_blank.py
```

The evaluator compares answers without regard to capitalization or punctuation.
Separate multiple valid answers in a custom CSV with `|`, placing the canonical
answer first, for example `Augustus|Augustus Caesar`.

Run the basic health and medicine fill-in-the-blank suite with:

```bash
python qa-code/test_fill_blank.py data/qa7-health.csv
```

Run the basic finance fill-in-the-blank suite with:

```bash
python qa-code/test_fill_blank.py data/qa8-finance.csv
```

Run the basic sports fill-in-the-blank suite with:

```bash
python qa-code/test_fill_blank.py data/qa9-sport.csv
```

Run the basic climate change fill-in-the-blank suite with:

```bash
python qa-code/test_fill_blank.py data/qa10-climate-change.csv
```

Run the basic entertainment fill-in-the-blank suite with:

```bash
python qa-code/test_fill_blank.py data/qa11-entertainment.csv
```

Run the basic literature fill-in-the-blank suite with:

```bash
python qa-code/test_fill_blank.py data/qa12-literature.csv
```

Run the basic animal fill-in-the-blank suite with:

```bash
python qa-code/test_fill_blank.py data/qa13-animal.csv
```

Run the basic plant fill-in-the-blank suite with:

```bash
python qa-code/test_fill_blank.py data/qa14-plant.csv
```

Run the basic chemistry fill-in-the-blank suite with:

```bash
python qa-code/test_fill_blank.py data/qa15-chemistry.csv
```

Run the basic computer science fill-in-the-blank suite with:

```bash
python qa-code/test_fill_blank.py data/qa16-computer-science.csv
```

Run the basic software engineering fill-in-the-blank suite with:

```bash
python qa-code/test_fill_blank.py data/qa17-software-engineering.csv
```

Run the advanced programming techniques fill-in-the-blank suite with:

```bash
python qa-code/test_fill_blank.py data/qa18-advanced-programming.csv
```

Run the basic biology fill-in-the-blank suite with:

```bash
python qa-code/test_fill_blank.py data/qa19-biology.csv
```

Run the basic gardening fill-in-the-blank suite with:

```bash
python qa-code/test_fill_blank.py data/qa20-gardening.csv
```

Run the standard written English grammar classification suite with:

```bash
python qa-code/test_fill_blank.py data/qa21-grammar.csv
```

## Architecture and findings reports

The `architecture` folder contains the project's higher-level design notes and
cross-test analysis:

- [First Architecture and QA Observation Note](architecture/first-observation-note.md)
  describes the initial local architecture, the roles of Phi, Llama, Duc, and
  the Codex/ChatGPT assistant, the QA workflow, model capacities, grading
  approach, and the system's current limitations.
- [Token, Context Window, and Memory Design Note](architecture/token-context-window-memory.md)
  explains token measurement, response time, input and output context, session
  memory, proposed long-term memory, retrieval, and recommendations for a
  continuously operating Duc assistant.
- [Consolidated QA Findings and Architecture Recommendations](architecture/qa-results-synthesis.md)
  reviews all reports in `qa-result`, compares both models across factual and
  writing tests, analyzes truncation, latency, guardrails, and confidence
  behavior, and proposes a validated production architecture.

## Model storage

After download, the expected directory structure is:

```text
models/
├── phi-4-mini-instruct-4bit/
└── llama-3.2-3b-instruct-4bit/
```

The models are loaded sequentially to keep peak memory low. On the original
16 GB M2 test machine, Phi used approximately 2.2 GB peak memory and Llama used
approximately 1.9 GB.

## Repository layout

```text
slm/
├── architecture/  # Architecture notes and consolidated findings
├── qa-code/       # Python model comparison and QA evaluators
├── data/          # CSV question sets and expected answers
├── prompt-template/ # Reusable model prompt templates
├── qa-result/     # Markdown reports from completed QA runs
├── models/        # Downloaded model weights (excluded from Git)
├── README.md
└── requirements.txt
```
---
# Legal

- GNU Affero General Public License v3.0

Run all Python commands from the repository root so model and data paths resolve
consistently.
