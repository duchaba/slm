"""Compare local Phi-4 Mini and Llama 3.2 3B responses.

The script loads one Small Language Model (SLM) at a time, formats the supplied
question with that model's chat template, generates an answer, and releases the
model before loading the next one. Sequential loading makes the comparison
practical on machines with limited unified memory.

Run the script from the project root after completing the model-download steps
in ``README.md``::

    python qa-code/ask_models.py "What is the capital of France?"
"""

from __future__ import annotations

import argparse
import gc
from pathlib import Path

import mlx.core as mx
from mlx_lm import generate, load


# Associate a human-readable display name with each downloaded model directory.
# Paths are relative to the project root, where this script is intended to run.
MODELS = {
    "Microsoft Phi-4 Mini": Path("models/phi-4-mini-instruct-4bit"),
    "Meta Llama 3.2 3B": Path("models/llama-3.2-3b-instruct-4bit"),
}


def ask(model_path: Path, question: str, max_tokens: int) -> str:
    """Generate an answer with one locally downloaded model.

    Args:
        model_path: Directory containing the MLX model weights, configuration,
            and tokenizer files.
        question: User message to submit to the model.
        max_tokens: Maximum number of new tokens the model may generate.

    Returns:
        The generated answer with leading and trailing whitespace removed.

    Raises:
        FileNotFoundError: If MLX cannot find required files in ``model_path``.
        ValueError: If the model configuration, tokenizer, or prompt is invalid.
    """
    # Loading returns both the neural-network model and its matching tokenizer.
    model, tokenizer = load(str(model_path))

    # Each instruction-tuned model expects its own control tokens. The tokenizer
    # owns that format, so applying its chat template avoids hard-coded syntax.
    prompt = tokenizer.apply_chat_template(
        [{"role": "user", "content": question}],
        tokenize=False,
        add_generation_prompt=True,
    )

    # Temperature and other sampling settings use MLX-LM defaults. Limiting the
    # output protects this command-line comparison from unbounded generation.
    answer = generate(
        model,
        tokenizer,
        prompt=prompt,
        max_tokens=max_tokens,
        verbose=False,
    )

    # Explicit cleanup is important on unified-memory Macs. It ensures the first
    # model does not remain allocated when the second model starts loading.
    del model, tokenizer
    gc.collect()
    mx.clear_cache()

    return answer.strip()


def main() -> None:
    """Parse command-line arguments and print an answer from each model.

    Args:
        None. Arguments are read from the process command line.

    Returns:
        None. Model names and answers are written to standard output.

    Raises:
        SystemExit: If argument parsing fails or a model directory is missing.
    """
    # The module documentation also serves as the command's help description.
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "question",
        nargs="?",
        default="What is the capital of France?",
    )
    parser.add_argument("--max-tokens", type=int, default=64)
    args = parser.parse_args()

    # Report every missing model in one actionable error instead of failing only
    # after MLX begins initialization.
    missing = [str(path) for path in MODELS.values() if not path.is_dir()]
    if missing:
        raise SystemExit("Missing model directories: " + ", ".join(missing))

    # Dictionary insertion order gives stable Phi-then-Llama output on Python 3.9.
    for name, path in MODELS.items():
        print(f"\n{name}\n{'-' * len(name)}")
        print(ask(path, args.question, args.max_tokens))


# Importing this module exposes ``ask`` without unexpectedly running inference.
if __name__ == "__main__":
    main()
