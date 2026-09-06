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
python ask_models.py
```

Expected answers should identify Paris as the capital of France. Exact wording
can vary because text generation may sample from multiple valid continuations.

## Usage

Pass a different question as the first argument:

```bash
python ask_models.py "Write a short welcome email."
```

Limit the maximum generated response length when needed:

```bash
python ask_models.py --max-tokens 32 "What is the capital of France?"
```

Display all command-line options:

```bash
python ask_models.py --help
```

## Run the true-or-false QA test

The repository includes `qa1-true-false.csv`, which contains ten factual
statements and their expected `True` or `False` answers. Run the same suite
against both models with:

```bash
python test_models.py
```

The report shows each model's expected and actual answer, pass/fail status, and
overall accuracy. To run another compatible test suite, provide its path:

```bash
python test_models.py path/to/questions.csv
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

`qa5-algebra-solving.csv` contains ten high-school algebra problems with
numeric answers instead of true/false labels. Run it with:

```bash
python test_algebra_solving.py
```

The evaluator asks each model to show brief reasoning and finish with
`ANSWER: <number>`. It grades integers, decimals, and fractions as exact numeric
values. A different compatible CSV can be supplied as the first argument.

## Run the fill-in-the-blank history test

`qa6-world-history.csv` contains ten world-history questions with short text
answers. Run it with:

```bash
python test_fill_blank.py
```

The evaluator compares answers without regard to capitalization or punctuation.
Separate multiple valid answers in a custom CSV with `|`, placing the canonical
answer first, for example `Augustus|Augustus Caesar`.

Run the basic health and medicine fill-in-the-blank suite with:

```bash
python test_fill_blank.py qa7-health.csv
```

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
