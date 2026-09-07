"""Generate and measure four workplace emails with both local SLMs.

The input JSON contains self-contained workplace scenarios. Each local model
receives the same scenario through its own chat template and must return a full
email. Models run sequentially to limit unified-memory use. The script records
unedited text, approximate tokens, and elapsed time; qualitative editorial
ratings are performed separately in the Markdown result report.
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
from typing import List, Sequence

import mlx.core as mx
from mlx_lm import generate, load
from mlx_lm.sample_utils import make_sampler

from ask_models import MODELS


DEFAULT_TEST_FILE = Path("data/qa103-email.json")


@dataclass(frozen=True)
class EmailCase:
    """One workplace email-writing scenario.

    Attributes:
        case_id: Stable numeric identifier.
        scenario: Short description of the communication task.
        recipient: Recipient name supplied to the model.
        subject: Required email subject.
        instructions: Complete content and constraint instructions.
    """

    case_id: int
    scenario: str
    recipient: str
    subject: str
    instructions: str


@dataclass(frozen=True)
class EmailResult:
    """Generated email and objective measurements for one scenario.

    Attributes:
        case: Source email scenario.
        email: Complete unedited model response.
        word_count: Number of word-like sequences in the response.
        input_tokens: Approximate rendered-prompt token count.
        output_tokens: Approximate decoded-response token count.
        response_seconds: Wall-clock generation duration.
    """

    case: EmailCase
    email: str
    word_count: int
    input_tokens: int
    output_tokens: int
    response_seconds: float


@dataclass(frozen=True)
class ModelEmailRun:
    """Complete email results and model-level timing.

    Attributes:
        results: Ordered email results.
        load_seconds: Model-and-tokenizer loading duration.
        cleanup_seconds: Model cleanup duration.
        total_seconds: End-to-end duration for the model run.
    """

    results: List[EmailResult]
    load_seconds: float
    cleanup_seconds: float
    total_seconds: float


def load_cases(test_path: Path) -> List[EmailCase]:
    """Read and validate workplace email scenarios from JSON.

    Args:
        test_path: Path to a UTF-8 JSON list of scenario objects.

    Returns:
        Validated scenarios in input order.

    Raises:
        FileNotFoundError: If the input file does not exist.
        ValueError: If the JSON structure or a required field is invalid.
    """
    payload = json.loads(test_path.read_text(encoding="utf-8"))
    if not isinstance(payload, list) or not payload:
        raise ValueError("Email test data must be a non-empty JSON list")

    cases: List[EmailCase] = []
    for index, item in enumerate(payload, start=1):
        if not isinstance(item, dict):
            raise ValueError(f"Case {index} must be a JSON object")
        fields = {
            key: str(item.get(key, "")).strip()
            for key in ("scenario", "recipient", "subject", "instructions")
        }
        if not all(fields.values()):
            raise ValueError(f"Case {index} has an empty required field")
        cases.append(
            EmailCase(
                case_id=int(item.get("id", index)),
                scenario=fields["scenario"],
                recipient=fields["recipient"],
                subject=fields["subject"],
                instructions=fields["instructions"],
            )
        )
    return cases


def count_words(text: str) -> int:
    """Count word-like sequences in an email response.

    Args:
        text: Generated email text.

    Returns:
        Count of Unicode words, including contractions.
    """
    return len(re.findall(r"\b[\w]+(?:[’'][\w]+)*", text, re.UNICODE))


def test_model(
    model_path: Path,
    cases: Sequence[EmailCase],
    max_tokens: int,
) -> ModelEmailRun:
    """Generate all workplace emails with one local model.

    Args:
        model_path: Local MLX model directory.
        cases: Ordered email-writing scenarios.
        max_tokens: Maximum new tokens permitted per email.

    Returns:
        Generated emails and model-level timing measurements.
    """
    run_started = time.perf_counter()
    load_started = time.perf_counter()
    model, tokenizer = load(str(model_path))
    load_seconds = time.perf_counter() - load_started
    sampler = make_sampler(temp=0.2)
    results: List[EmailResult] = []
    cleanup_seconds = 0.0

    try:
        for case in cases:
            prompt_text = (
                "Write a friendly but professional work email. Return only the "
                "complete email with Subject, greeting, body, closing, and the "
                "sender placeholder [Your Name]. Follow every constraint and "
                "do not discuss the instructions.\n\n"
                f"SCENARIO: {case.scenario}\n"
                f"RECIPIENT: {case.recipient}\n"
                f"REQUIRED SUBJECT: {case.subject}\n"
                f"INSTRUCTIONS: {case.instructions}"
            )
            prompt = tokenizer.apply_chat_template(
                [{"role": "user", "content": prompt_text}],
                tokenize=False,
                add_generation_prompt=True,
            )
            input_tokens = len(tokenizer.encode(prompt))
            response_started = time.perf_counter()
            email = generate(
                model,
                tokenizer,
                prompt=prompt,
                max_tokens=max_tokens,
                sampler=sampler,
                verbose=False,
            ).strip()
            response_seconds = time.perf_counter() - response_started
            results.append(
                EmailResult(
                    case=case,
                    email=email,
                    word_count=count_words(email),
                    input_tokens=input_tokens,
                    output_tokens=len(tokenizer.encode(email)),
                    response_seconds=response_seconds,
                )
            )
    finally:
        cleanup_started = time.perf_counter()
        del model, tokenizer
        gc.collect()
        mx.clear_cache()
        cleanup_seconds = time.perf_counter() - cleanup_started

    return ModelEmailRun(
        results=results,
        load_seconds=load_seconds,
        cleanup_seconds=cleanup_seconds,
        total_seconds=time.perf_counter() - run_started,
    )


def print_run(model_name: str, run: ModelEmailRun) -> None:
    """Print full emails and measurements for one model.

    Args:
        model_name: Human-readable model name.
        run: Completed email results and timing.

    Returns:
        None. Results are written to standard output.
    """
    times = [result.response_seconds for result in run.results]
    input_tokens = sum(result.input_tokens for result in run.results)
    output_tokens = sum(result.output_tokens for result in run.results)
    print(f"\n=== {model_name} ===")
    for result in run.results:
        print(
            f"\nCASE {result.case.case_id}: {result.case.scenario}\n"
            f"Words: {result.word_count} | Time: {result.response_seconds:.3f} s "
            f"| Tokens: {result.input_tokens} in + {result.output_tokens} out\n"
            f"--- EMAIL START ---\n{result.email}\n--- EMAIL END ---"
        )
    print(f"\nLoad time: {run.load_seconds:.3f} s")
    print(f"Total generation time: {sum(times):.3f} s")
    print(f"Average generation time: {statistics.fmean(times):.3f} s")
    print(f"Tokens: {input_tokens} in + {output_tokens} out")
    print(f"Cleanup time: {run.cleanup_seconds:.3f} s")
    print(f"End-to-end time: {run.total_seconds:.3f} s")


def run_test(test_path: Path, max_tokens: int) -> None:
    """Run every email scenario against both configured models.

    Args:
        test_path: Path to the email-scenario JSON file.
        max_tokens: Maximum generated tokens per email.

    Returns:
        None. Full test output is printed.

    Raises:
        FileNotFoundError: If input data or model directories are missing.
    """
    cases = load_cases(test_path)
    missing_models = [str(path) for path in MODELS.values() if not path.is_dir()]
    if missing_models:
        raise FileNotFoundError(
            "Missing model directories: " + ", ".join(missing_models)
        )
    for model_name, model_path in MODELS.items():
        run = test_model(model_path, cases, max_tokens=max_tokens)
        print_run(model_name, run)


def main() -> None:
    """Parse command-line options and run the workplace email test.

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
        help=f"email scenario JSON file (default: {DEFAULT_TEST_FILE})",
    )
    parser.add_argument(
        "--max-tokens",
        type=int,
        default=400,
        help="maximum generated tokens per email (default: 400)",
    )
    args = parser.parse_args()
    run_test(args.test_path, max_tokens=args.max_tokens)


if __name__ == "__main__":
    main()
