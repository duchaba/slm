"""Generate and measure a long-form LinkedIn article with both local SLMs.

The input is a UTF-8 Markdown or text file containing the user's rough draft and
writing instructions. Each configured model receives the same content through
its own tokenizer chat template. Models run sequentially to limit unified-memory
use. The script prints complete articles and objective measurements; qualitative
ratings are added separately through human or documented AI-assisted review.
"""

from __future__ import annotations

import argparse
import gc
import re
import statistics
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence

import mlx.core as mx
from mlx_lm import generate, load
from mlx_lm.sample_utils import make_sampler

from ask_models import MODELS


DEFAULT_TEST_FILE = Path("data/qa100-linkedin-article.md")


@dataclass(frozen=True)
class ArticleResult:
    """Generated article and measurements for one local language model.

    Attributes:
        model_name: Human-readable name of the evaluated model.
        article: Complete decoded article produced by the model.
        word_count: Number of word-like sequences in ``article``.
        character_count: Number of Unicode characters, including whitespace.
        input_tokens: Approximate token count of the rendered input prompt.
        output_tokens: Approximate token count of the decoded article.
        load_seconds: Wall-clock duration for loading model and tokenizer.
        generation_seconds: Wall-clock duration of the generation call.
        cleanup_seconds: Wall-clock duration for releasing model memory.
        total_seconds: End-to-end duration including loading and cleanup.
    """

    model_name: str
    article: str
    word_count: int
    character_count: int
    input_tokens: int
    output_tokens: int
    load_seconds: float
    generation_seconds: float
    cleanup_seconds: float
    total_seconds: float


def read_rough_draft(test_path: Path) -> str:
    """Read and validate the rough-draft test instructions.

    Args:
        test_path: Path to a UTF-8 text or Markdown test file.

    Returns:
        Non-empty rough draft with surrounding whitespace removed.

    Raises:
        FileNotFoundError: If ``test_path`` does not exist.
        ValueError: If the file contains no non-whitespace text.
    """
    rough_draft = test_path.read_text(encoding="utf-8").strip()
    if not rough_draft:
        raise ValueError(f"Test file is empty: {test_path}")
    return rough_draft


def count_words(text: str) -> int:
    """Count human-readable words in generated article text.

    Args:
        text: Article text to measure.

    Returns:
        Number of Unicode word sequences, including contractions and hashtags.
    """
    return len(re.findall(r"(?:#|\b)[\w]+(?:[’'][\w]+)*", text, re.UNICODE))


def generate_article(
    model_name: str,
    model_path: Path,
    rough_draft: str,
    max_tokens: int,
    character_target: bool = False,
) -> ArticleResult:
    """Generate one article and capture token and elapsed-time measurements.

    Args:
        model_name: Human-readable name used in output and results.
        model_path: Directory containing a local MLX model and tokenizer.
        rough_draft: User-supplied article instructions and source material.
        max_tokens: Maximum number of new tokens allowed for the article.
        character_target: Whether the supplied draft uses a character-based
            length requirement instead of the QA100 word-based requirement.

    Returns:
        Generated article plus objective measurements for the complete run.

    Raises:
        FileNotFoundError: If the model directory is missing.
        ValueError: If the model cannot be loaded or its prompt cannot be built.
    """
    run_started = time.perf_counter()
    load_started = time.perf_counter()
    model, tokenizer = load(str(model_path))
    load_seconds = time.perf_counter() - load_started
    cleanup_seconds = 0.0

    # A small nonzero temperature permits natural prose while remaining
    # conservative enough for a repeatable editorial comparison.
    sampler = make_sampler(temp=0.2)
    try:
        length_instruction = (
            "Follow every character limit in the draft. Count all visible text "
            "in the finished article, including headings."
            if character_target
            else "Keep the article between 1,200 and 1,500 words."
        )
        instruction = (
            "Follow the rough draft below. Write the finished LinkedIn article "
            f"only; do not discuss these instructions. {length_instruction} "
            "Do not invent research findings, benchmark numbers, quotations, "
            "or personal experiences that are not in the draft.\n\n"
            f"ROUGH DRAFT:\n{rough_draft}"
        )
        prompt = tokenizer.apply_chat_template(
            [{"role": "user", "content": instruction}],
            tokenize=False,
            add_generation_prompt=True,
        )
        input_tokens = len(tokenizer.encode(prompt))

        generation_started = time.perf_counter()
        article = generate(
            model,
            tokenizer,
            prompt=prompt,
            max_tokens=max_tokens,
            sampler=sampler,
            verbose=False,
        ).strip()
        generation_seconds = time.perf_counter() - generation_started
        output_tokens = len(tokenizer.encode(article))
    finally:
        cleanup_started = time.perf_counter()
        del model, tokenizer
        gc.collect()
        mx.clear_cache()
        cleanup_seconds = time.perf_counter() - cleanup_started

    return ArticleResult(
        model_name=model_name,
        article=article,
        word_count=count_words(article),
        character_count=len(article),
        input_tokens=input_tokens,
        output_tokens=output_tokens,
        load_seconds=load_seconds,
        generation_seconds=generation_seconds,
        cleanup_seconds=cleanup_seconds,
        total_seconds=time.perf_counter() - run_started,
    )


def print_result(result: ArticleResult) -> None:
    """Print one article and its measurements in a reviewable format.

    Args:
        result: Completed generation result to print.

    Returns:
        None. Output is written to standard output.
    """
    total_tokens = result.input_tokens + result.output_tokens
    tokens_per_second = (
        result.output_tokens / result.generation_seconds
        if result.generation_seconds
        else 0.0
    )
    print(f"\n=== {result.model_name} ===")
    print(f"Word count: {result.word_count}")
    print(f"Character count: {result.character_count}")
    print(f"Input tokens: {result.input_tokens}")
    print(f"Output tokens: {result.output_tokens}")
    print(f"Total tokens: {total_tokens}")
    print(f"Model load: {result.load_seconds:.3f} s")
    print(f"Generation: {result.generation_seconds:.3f} s")
    print(f"Output speed: {tokens_per_second:.3f} tokens/s")
    print(f"Cleanup: {result.cleanup_seconds:.3f} s")
    print(f"End-to-end: {result.total_seconds:.3f} s")
    print("\n--- ARTICLE START ---")
    print(result.article)
    print("--- ARTICLE END ---")


def run_test(
    test_path: Path,
    max_tokens: int,
    character_target: bool = False,
) -> Sequence[ArticleResult]:
    """Run the long-form article test against every configured local model.

    Args:
        test_path: Path to the rough-draft test file.
        max_tokens: Maximum new tokens permitted for each generated article.
        character_target: Whether to enforce the draft's character-based
            instructions instead of adding the QA100 word-based instruction.

    Returns:
        Results in the same order as the configured model mapping.

    Raises:
        FileNotFoundError: If the test file or any model directory is missing.
        ValueError: If the input or model prompt is invalid.
    """
    rough_draft = read_rough_draft(test_path)
    missing_models = [str(path) for path in MODELS.values() if not path.is_dir()]
    if missing_models:
        raise FileNotFoundError(
            "Missing model directories: " + ", ".join(missing_models)
        )

    results = []
    for model_name, model_path in MODELS.items():
        result = generate_article(
            model_name=model_name,
            model_path=model_path,
            rough_draft=rough_draft,
            max_tokens=max_tokens,
            character_target=character_target,
        )
        results.append(result)
        print_result(result)

    generation_times = [result.generation_seconds for result in results]
    print("\n=== COMBINED ===")
    print(f"Models tested: {len(results)}")
    print(f"Mean generation time: {statistics.fmean(generation_times):.3f} s")
    print(f"Total generation time: {sum(generation_times):.3f} s")
    return results


def main() -> None:
    """Parse command-line options and run the LinkedIn article test.

    Args:
        None. Values are read from command-line arguments.

    Returns:
        None. Results and articles are written to standard output.
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "test_path",
        nargs="?",
        type=Path,
        default=DEFAULT_TEST_FILE,
        help=f"rough-draft file (default: {DEFAULT_TEST_FILE})",
    )
    parser.add_argument(
        "--max-tokens",
        type=int,
        default=2600,
        help="maximum generated tokens per article (default: 2600)",
    )
    parser.add_argument(
        "--character-target",
        action="store_true",
        help="use character limits from the draft instead of a word target",
    )
    args = parser.parse_args()
    run_test(
        args.test_path,
        max_tokens=args.max_tokens,
        character_target=args.character_target,
    )


if __name__ == "__main__":
    main()
