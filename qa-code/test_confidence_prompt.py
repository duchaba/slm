"""Test structured confidence reporting by the two locally hosted SLMs.

Each JSON case specifies the expected HIGH, LOW, or UNKNOWN label. The script
uses one shared prompt template, parses the model's structured response, and
reports exact label/format compliance together with tokens and elapsed time.
Answer quality still requires human review and is documented in the result file.
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
from typing import List, Optional, Sequence

import mlx.core as mx
from mlx_lm import generate, load
from mlx_lm.sample_utils import make_sampler

from ask_models import MODELS


DEFAULT_TEST_FILE = Path("data/qa106-prompt-template.json")
DEFAULT_PROMPT_TEMPLATE_FILE = Path("prompt-template/confidence-answer.txt")
VALID_CONFIDENCE = {"HIGH", "LOW", "UNKNOWN"}


@dataclass(frozen=True)
class ConfidenceCase:
    """Represent one confidence-classification question.

    Attributes:
        case_id: Stable numeric identifier.
        category: Human-readable question category.
        expected_confidence: Required HIGH, LOW, or UNKNOWN label.
        question: Question submitted to the model.
        reference_information: Optional current facts supplied with the prompt.
        expected_answer: Answer or qualitative answer criterion for review.
    """

    case_id: int
    category: str
    expected_confidence: str
    question: str
    reference_information: str
    expected_answer: str


@dataclass(frozen=True)
class ConfidenceResult:
    """Store one generated response and its objective measurements.

    Attributes:
        case: Source test case.
        actual_confidence: Parsed confidence label, if recognized.
        raw_response: Complete unedited model response.
        format_valid: Whether both required fields follow the template.
        label_passed: Whether the parsed label equals the expected label.
        input_tokens: Tokenized prompt length.
        output_tokens: Tokenized response length.
        response_seconds: Wall-clock generation duration.
    """

    case: ConfidenceCase
    actual_confidence: Optional[str]
    raw_response: str
    format_valid: bool
    label_passed: bool
    input_tokens: int
    output_tokens: int
    response_seconds: float


@dataclass(frozen=True)
class ModelRun:
    """Store all results and aggregate timing for one model.

    Attributes:
        results: Results in dataset order.
        load_seconds: Model and tokenizer load duration.
        cleanup_seconds: Model cleanup duration.
        total_seconds: End-to-end duration for the model.
    """

    results: List[ConfidenceResult]
    load_seconds: float
    cleanup_seconds: float
    total_seconds: float


def load_prompt_template(template_path: Path) -> str:
    """Read and validate the external confidence prompt template.

    Args:
        template_path: UTF-8 text file containing the reusable prompt.

    Returns:
        Prompt text with surrounding whitespace removed.

    Raises:
        ValueError: If the template is empty or does not contain exactly one
            ``{question}`` placeholder and one ``{context}`` placeholder.
    """
    template = template_path.read_text(encoding="utf-8").strip()
    required_placeholders = ("{question}", "{context}")
    if not template:
        raise ValueError("Prompt template must not be empty")
    for placeholder in required_placeholders:
        if template.count(placeholder) != 1:
            raise ValueError(
                f"Prompt template must contain exactly one {placeholder} placeholder"
            )
    return template


def load_cases(test_path: Path) -> List[ConfidenceCase]:
    """Load and validate confidence test cases.

    Args:
        test_path: UTF-8 JSON file containing a non-empty list of cases.

    Returns:
        Validated test cases in source order.

    Raises:
        ValueError: If the JSON structure or a required value is invalid.
    """
    payload = json.loads(test_path.read_text(encoding="utf-8"))
    if not isinstance(payload, list) or not payload:
        raise ValueError("Confidence test data must be a non-empty JSON list")
    cases: List[ConfidenceCase] = []
    for index, item in enumerate(payload, start=1):
        if not isinstance(item, dict):
            raise ValueError(f"Case {index} must be a JSON object")
        expected = str(item.get("expected_confidence", "")).strip().upper()
        if expected not in VALID_CONFIDENCE:
            raise ValueError(f"Case {index} has invalid expected_confidence")
        question = str(item.get("question", "")).strip()
        category = str(item.get("category", "")).strip()
        expected_answer = str(item.get("expected_answer", "")).strip()
        if not question or not category or not expected_answer:
            raise ValueError(f"Case {index} has an empty required text field")
        cases.append(ConfidenceCase(
            case_id=int(item.get("id", index)),
            category=category,
            expected_confidence=expected,
            question=question,
            reference_information=str(item.get("reference_information", "")).strip(),
            expected_answer=expected_answer,
        ))
    return cases


def parse_response(response: str) -> tuple[Optional[str], bool]:
    """Parse a confidence label and verify the two-field response format.

    Args:
        response: Complete text generated by the model.

    Returns:
        A pair containing the recognized label and strict format-valid flag.
    """
    confidence_match = re.search(
        r"\bCONFIDENCE:\s*(HIGH|LOW|UNKNOWN)\b", response
    )
    confidence_line = re.search(
        r"^CONFIDENCE:\s*(HIGH|LOW|UNKNOWN)\s*$", response, re.MULTILINE
    )
    answer_match = re.search(r"^ANSWER:\s*\S", response, re.MULTILINE)
    label = confidence_match.group(1) if confidence_match else None
    return label, bool(confidence_line and answer_match)


def test_model(
    model_path: Path,
    cases: Sequence[ConfidenceCase],
    prompt_template: str,
    max_tokens: int,
) -> ModelRun:
    """Run every confidence case against one local model.

    Args:
        model_path: Local MLX model directory.
        cases: Ordered cases to evaluate.
        prompt_template: Validated template containing question and context
            placeholders.
        max_tokens: Maximum new tokens allowed per response.

    Returns:
        Per-case results and model-level timings.
    """
    run_started = time.perf_counter()
    load_started = time.perf_counter()
    model, tokenizer = load(str(model_path))
    load_seconds = time.perf_counter() - load_started
    sampler = make_sampler(temp=0.0)
    results: List[ConfidenceResult] = []
    try:
        for case in cases:
            instruction = prompt_template.format(
                question=case.question,
                context=case.reference_information or "None",
            )
            prompt = tokenizer.apply_chat_template(
                [{"role": "user", "content": instruction}],
                tokenize=False,
                add_generation_prompt=True,
            )
            input_tokens = len(tokenizer.encode(prompt))
            response_started = time.perf_counter()
            raw_response = generate(
                model,
                tokenizer,
                prompt=prompt,
                max_tokens=max_tokens,
                sampler=sampler,
                verbose=False,
            ).strip()
            response_seconds = time.perf_counter() - response_started
            actual, format_valid = parse_response(raw_response)
            results.append(ConfidenceResult(
                case=case,
                actual_confidence=actual,
                raw_response=raw_response,
                format_valid=format_valid,
                label_passed=actual == case.expected_confidence,
                input_tokens=input_tokens,
                output_tokens=len(tokenizer.encode(raw_response)),
                response_seconds=response_seconds,
            ))
    finally:
        cleanup_started = time.perf_counter()
        del model, tokenizer
        gc.collect()
        mx.clear_cache()
        cleanup_seconds = time.perf_counter() - cleanup_started
    return ModelRun(results, load_seconds, cleanup_seconds, time.perf_counter() - run_started)


def print_run(model_name: str, run: ModelRun) -> None:
    """Print exact outputs and aggregate statistics for one model.

    Args:
        model_name: Human-readable model name.
        run: Completed confidence test run.

    Returns:
        None. Output is written to standard output.
    """
    times = [result.response_seconds for result in run.results]
    print(f"\n=== {model_name} ===")
    for result in run.results:
        actual = result.actual_confidence or "UNRECOGNIZED"
        status = "PASS" if result.label_passed else "FAIL"
        print(
            f"\nCASE {result.case.case_id}: {result.case.category}\n"
            f"QUESTION: {result.case.question}\n"
            f"EXPECTED ANSWER: {result.case.expected_answer}\n"
            f"Expected confidence: {result.case.expected_confidence} | "
            f"Actual: {actual} | {status} | Format: "
            f"{'PASS' if result.format_valid else 'FAIL'}\n"
            f"Time: {result.response_seconds:.3f} s | Tokens: "
            f"{result.input_tokens} in + {result.output_tokens} out\n"
            f"RAW RESPONSE:\n{result.raw_response}\nEND RESPONSE"
        )
    print(f"\nLabel accuracy: {sum(r.label_passed for r in run.results)}/{len(run.results)}")
    print(f"Format accuracy: {sum(r.format_valid for r in run.results)}/{len(run.results)}")
    print(f"Load time: {run.load_seconds:.3f} s")
    print(f"Total response time: {sum(times):.3f} s")
    print(f"Average response time: {statistics.fmean(times):.3f} s")
    print(f"Median response time: {statistics.median(times):.3f} s")
    print(f"Tokens: {sum(r.input_tokens for r in run.results)} in + {sum(r.output_tokens for r in run.results)} out")
    print(f"Cleanup time: {run.cleanup_seconds:.3f} s")
    print(f"End-to-end time: {run.total_seconds:.3f} s")


def run_test(test_path: Path, template_path: Path, max_tokens: int) -> None:
    """Evaluate both configured SLMs.

    Args:
        test_path: Confidence-test JSON dataset.
        template_path: Reusable prompt-template text file.
        max_tokens: Maximum generated tokens per answer.

    Returns:
        None. Complete results are printed.

    Raises:
        FileNotFoundError: If a configured model directory is missing.
    """
    cases = load_cases(test_path)
    prompt_template = load_prompt_template(template_path)
    missing = [str(path) for path in MODELS.values() if not path.is_dir()]
    if missing:
        raise FileNotFoundError("Missing model directories: " + ", ".join(missing))
    for model_name, model_path in MODELS.items():
        print_run(
            model_name,
            test_model(model_path, cases, prompt_template, max_tokens),
        )


def main() -> None:
    """Parse command-line options and run the confidence test.

    Args:
        None. Values are read from the command line.

    Returns:
        None. Results are printed to standard output.
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("test_path", nargs="?", type=Path, default=DEFAULT_TEST_FILE)
    parser.add_argument(
        "--prompt-template",
        type=Path,
        default=DEFAULT_PROMPT_TEMPLATE_FILE,
        help=(
            "confidence prompt template "
            f"(default: {DEFAULT_PROMPT_TEMPLATE_FILE})"
        ),
    )
    parser.add_argument("--max-tokens", type=int, default=128)
    args = parser.parse_args()
    run_test(args.test_path, args.prompt_template, args.max_tokens)


if __name__ == "__main__":
    main()
