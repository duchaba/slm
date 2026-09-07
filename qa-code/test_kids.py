"""Generate child-friendly explanations with both local SLMs.

The input JSON contains self-contained topics and constraints for readers aged
10 to 12. Each model produces a short explanation in a funny, friendly tone.
Models run sequentially to limit unified-memory use. The script records full
unedited output, approximate token use, and elapsed time for later review.
"""

from __future__ import annotations

import argparse
import gc
import json
import re
import statistics
import time
from dataclasses import dataclass
from pathlib import Path
from typing import List, Sequence, Tuple

import mlx.core as mx
from mlx_lm import generate, load
from mlx_lm.sample_utils import make_sampler

from ask_models import MODELS


DEFAULT_TEST_FILE = Path("data/qa104-kids.json")
DEFAULT_TOKEN_LIMITS = (300, 450, 600)


@dataclass(frozen=True)
class KidsCase:
    """One child-friendly explanation task.

    Attributes:
        case_id: Stable numeric identifier.
        topic: Subject of the explanation.
        task: Detailed content and accuracy constraints.
    """

    case_id: int
    topic: str
    task: str


@dataclass(frozen=True)
class KidsResult:
    """Generated explanation and objective measurements.

    Attributes:
        case: Source explanation task.
        response: Complete unedited model output.
        word_count: Number of word-like sequences in the output.
        input_tokens: Approximate rendered-prompt token count.
        output_tokens: Approximate decoded-output token count.
        response_seconds: Wall-clock generation duration.
        attempted_limits: Token ceilings tried in generation order.
        generated_tokens_total: Approximate output tokens consumed across all
            attempts, including discarded truncated responses.
    """

    case: KidsCase
    response: str
    word_count: int
    input_tokens: int
    output_tokens: int
    response_seconds: float
    attempted_limits: Tuple[int, ...]
    generated_tokens_total: int


@dataclass(frozen=True)
class ModelKidsRun:
    """Complete explanation results and model-level timing.

    Attributes:
        results: Ordered explanation results.
        load_seconds: Model-and-tokenizer loading duration.
        cleanup_seconds: Model cleanup duration.
        total_seconds: End-to-end duration for the model run.
    """

    results: List[KidsResult]
    load_seconds: float
    cleanup_seconds: float
    total_seconds: float


def load_cases(test_path: Path) -> List[KidsCase]:
    """Read and validate child-friendly explanation tasks.

    Args:
        test_path: Path to a UTF-8 JSON list of task objects.

    Returns:
        Validated tasks in source order.

    Raises:
        FileNotFoundError: If the input file is missing.
        ValueError: If the JSON structure or a required field is invalid.
    """
    payload = json.loads(test_path.read_text(encoding="utf-8"))
    if not isinstance(payload, list) or not payload:
        raise ValueError("Kids test data must be a non-empty JSON list")

    cases: List[KidsCase] = []
    for index, item in enumerate(payload, start=1):
        if not isinstance(item, dict):
            raise ValueError(f"Case {index} must be a JSON object")
        topic = str(item.get("topic", "")).strip()
        task = str(item.get("task", "")).strip()
        if not topic or not task:
            raise ValueError(f"Case {index} has an empty topic or task")
        cases.append(
            KidsCase(
                case_id=int(item.get("id", index)),
                topic=topic,
                task=task,
            )
        )
    return cases


def count_words(text: str) -> int:
    """Count word-like sequences in generated text.

    Args:
        text: Explanation text to measure.

    Returns:
        Count of Unicode words, including contractions.
    """
    return len(re.findall(r"\b[\w]+(?:[’'][\w]+)*", text, re.UNICODE))


def parse_token_limits(value: str) -> Tuple[int, ...]:
    """Parse an increasing comma-separated token-limit sequence.

    Args:
        value: Text such as ``300,450,600`` from the command line.

    Returns:
        Strictly increasing positive token limits.

    Raises:
        argparse.ArgumentTypeError: If values are invalid or not increasing.
    """
    try:
        limits = tuple(int(item.strip()) for item in value.split(","))
    except ValueError as error:
        raise argparse.ArgumentTypeError(
            "token limits must be comma-separated integers"
        ) from error
    if not limits or any(limit <= 0 for limit in limits):
        raise argparse.ArgumentTypeError("token limits must be positive")
    if any(later <= earlier for earlier, later in zip(limits, limits[1:])):
        raise argparse.ArgumentTypeError("token limits must strictly increase")
    return limits


def probably_reached_token_limit(output_tokens: int, token_limit: int) -> bool:
    """Estimate whether generation stopped because it exhausted its allowance.

    Args:
        output_tokens: Response size obtained by re-encoding decoded text.
        token_limit: Maximum new tokens supplied to the generator.

    Returns:
        ``True`` when the approximate count is within two tokens of the limit.

    Notes:
        Decoding may omit an end token or alter whitespace, so a tolerance is
        safer than requiring exact equality. A future MLX API that exposes a
        native stop reason should replace this approximation.
    """
    return output_tokens >= token_limit - 2


def test_model(
    model_path: Path,
    cases: Sequence[KidsCase],
    token_limits: Sequence[int],
) -> ModelKidsRun:
    """Generate every explanation with one local model.

    Args:
        model_path: Local MLX model directory.
        cases: Ordered child-friendly explanation tasks.
        token_limits: Increasing output ceilings used for bounded retries.

    Returns:
        Generated explanations and model-level timing measurements.

    Raises:
        ValueError: If ``token_limits`` is empty or contains a nonpositive value.
    """
    if not token_limits or any(limit <= 0 for limit in token_limits):
        raise ValueError("token_limits must contain positive values")

    run_started = time.perf_counter()
    load_started = time.perf_counter()
    model, tokenizer = load(str(model_path))
    load_seconds = time.perf_counter() - load_started
    sampler = make_sampler(temp=0.3)
    results: List[KidsResult] = []
    cleanup_seconds = 0.0

    try:
        for case in cases:
            instruction = (
                "Write only a short explanation for a 10- to 12-year-old. "
                "Make it friendly, funny, entertaining, and easy to understand "
                "while remaining accurate. Use a few short paragraphs. Avoid "
                "scary detail, adult language, fake facts, and a quiz at the "
                "end.\n\n"
                f"TOPIC: {case.topic}\nTASK: {case.task}"
            )
            prompt = tokenizer.apply_chat_template(
                [{"role": "user", "content": instruction}],
                tokenize=False,
                add_generation_prompt=True,
            )
            input_tokens = len(tokenizer.encode(prompt))
            response_seconds = 0.0
            generated_tokens_total = 0
            attempted_limits: List[int] = []

            # Every retry starts from the original prompt. This avoids joining
            # a continuation onto a cut-off sentence. The bounded sequence also
            # prevents unlimited automatic expansion.
            for token_limit in token_limits:
                attempted_limits.append(token_limit)
                response_started = time.perf_counter()
                response = generate(
                    model,
                    tokenizer,
                    prompt=prompt,
                    max_tokens=token_limit,
                    sampler=sampler,
                    verbose=False,
                ).strip()
                response_seconds += time.perf_counter() - response_started
                output_tokens = len(tokenizer.encode(response))
                generated_tokens_total += output_tokens
                if not probably_reached_token_limit(output_tokens, token_limit):
                    break
            results.append(
                KidsResult(
                    case=case,
                    response=response,
                    word_count=count_words(response),
                    input_tokens=input_tokens,
                    output_tokens=output_tokens,
                    response_seconds=response_seconds,
                    attempted_limits=tuple(attempted_limits),
                    generated_tokens_total=generated_tokens_total,
                )
            )
    finally:
        cleanup_started = time.perf_counter()
        del model, tokenizer
        gc.collect()
        mx.clear_cache()
        cleanup_seconds = time.perf_counter() - cleanup_started

    return ModelKidsRun(
        results=results,
        load_seconds=load_seconds,
        cleanup_seconds=cleanup_seconds,
        total_seconds=time.perf_counter() - run_started,
    )


def print_run(model_name: str, run: ModelKidsRun) -> None:
    """Print full explanations and measurements for one model.

    Args:
        model_name: Human-readable model name.
        run: Completed explanations and timing.

    Returns:
        None. Results are written to standard output.
    """
    times = [result.response_seconds for result in run.results]
    input_tokens = sum(
        result.input_tokens * len(result.attempted_limits)
        for result in run.results
    )
    output_tokens = sum(result.generated_tokens_total for result in run.results)
    print(f"\n=== {model_name} ===")
    for result in run.results:
        print(
            f"\nCASE {result.case.case_id}: {result.case.topic}\n"
            f"Words: {result.word_count} | Time: {result.response_seconds:.3f} s "
            f"| Final tokens: {result.input_tokens} in + {result.output_tokens} out\n"
            f"Attempts: {len(result.attempted_limits)} | "
            f"Limits tried: {','.join(map(str, result.attempted_limits))} | "
            f"Generated tokens across attempts: {result.generated_tokens_total}\n"
            f"--- RESPONSE START ---\n{result.response}\n--- RESPONSE END ---"
        )
    print(f"\nLoad time: {run.load_seconds:.3f} s")
    print(f"Total generation time: {sum(times):.3f} s")
    print(f"Average generation time: {statistics.fmean(times):.3f} s")
    print(f"Tokens: {input_tokens} in + {output_tokens} out")
    print(f"Cleanup time: {run.cleanup_seconds:.3f} s")
    print(f"End-to-end time: {run.total_seconds:.3f} s")


def run_test(test_path: Path, token_limits: Sequence[int]) -> None:
    """Run all explanation tasks against both configured models.

    Args:
        test_path: Path to the child-friendly task JSON file.
        token_limits: Increasing output ceilings used for bounded retries.

    Returns:
        None. Full test output is printed.

    Raises:
        FileNotFoundError: If test data or model directories are missing.
    """
    cases = load_cases(test_path)
    missing_models = [str(path) for path in MODELS.values() if not path.is_dir()]
    if missing_models:
        raise FileNotFoundError(
            "Missing model directories: " + ", ".join(missing_models)
        )
    for model_name, model_path in MODELS.items():
        run = test_model(model_path, cases, token_limits=token_limits)
        print_run(model_name, run)


def main() -> None:
    """Parse command-line options and run the kids explanation test.

    Args:
        None. Values are read from command-line arguments.

    Returns:
        None. Results are printed to standard output.
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "test_path",
        nargs="?",
        type=Path,
        default=DEFAULT_TEST_FILE,
        help=f"kids task JSON file (default: {DEFAULT_TEST_FILE})",
    )
    parser.add_argument(
        "--max-tokens",
        type=int,
        default=None,
        help="use one fixed token limit and disable automatic retries",
    )
    parser.add_argument(
        "--token-limits",
        type=parse_token_limits,
        default=DEFAULT_TOKEN_LIMITS,
        help="increasing retry limits (default: 300,450,600)",
    )
    args = parser.parse_args()
    token_limits = (
        (args.max_tokens,) if args.max_tokens is not None else args.token_limits
    )
    run_test(args.test_path, token_limits=token_limits)


if __name__ == "__main__":
    main()
