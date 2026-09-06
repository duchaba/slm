"""Load the two local SLMs sequentially and ask each the same question."""

from __future__ import annotations

import argparse
import gc
from pathlib import Path

import mlx.core as mx
from mlx_lm import generate, load


MODELS = {
    "Microsoft Phi-4 Mini": Path("models/phi-4-mini-instruct-4bit"),
    "Meta Llama 3.2 3B": Path("models/llama-3.2-3b-instruct-4bit"),
}


def ask(model_path: Path, question: str, max_tokens: int) -> str:
    """Load one model, apply its chat template, and return its answer."""
    model, tokenizer = load(str(model_path))
    prompt = tokenizer.apply_chat_template(
        [{"role": "user", "content": question}],
        tokenize=False,
        add_generation_prompt=True,
    )
    answer = generate(
        model,
        tokenizer,
        prompt=prompt,
        max_tokens=max_tokens,
        verbose=False,
    )
    del model, tokenizer
    gc.collect()
    mx.clear_cache()
    return answer.strip()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "question",
        nargs="?",
        default="What is the capital of France?",
    )
    parser.add_argument("--max-tokens", type=int, default=64)
    args = parser.parse_args()

    missing = [str(path) for path in MODELS.values() if not path.is_dir()]
    if missing:
        raise SystemExit("Missing model directories: " + ", ".join(missing))

    for name, path in MODELS.items():
        print(f"\n{name}\n{'-' * len(name)}")
        print(ask(path, args.question, args.max_tokens))


if __name__ == "__main__":
    main()
