"""Evaluate both local SLMs on numeric algebra-solving questions.

The input CSV must contain ``question`` and ``answer`` columns. Answers may be
integers, decimals, or fractions. Each model is asked to reason through the
problem and finish with ``ANSWER: <number>`` so its final value can be graded
independently of the wording of its explanation.
"""

from __future__ import annotations

import argparse
import csv
import gc
import re
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path
from typing import List, Optional, Sequence

import mlx.core as mx
from mlx_lm import generate, load
from mlx_lm.sample_utils import make_sampler

from ask_models import MODELS


DEFAULT_TEST_FILE = Path("qa5-algebra-solving.csv")


@dataclass(frozen=True)
class SolvingTestCase:
    """One algebra problem and its expected numeric answer.

    Attributes:
        question: Algebra problem presented to the model.
        expected: Exact expected numeric value.
    """

    question: str
    expected: Fraction


@dataclass(frozen=True)
class SolvingTestResult:
    """Outcome of one model's attempt at one algebra problem.

    Attributes:
        question: Algebra problem presented to the model.
        expected: Correct numeric answer.
        actual: Parsed final numeric answer, or ``None`` when parsing failed.
        raw_response: Complete generated explanation and answer.
        passed: Whether the parsed answer exactly equals the expected answer.
    """

    question: str
    expected: Fraction
    actual: Optional[Fraction]
    raw_response: str
    passed: bool


def parse_number(value: str) -> Fraction:
    """Convert an integer, decimal, or fraction string to an exact value.

    Args:
        value: Numeric text such as ``7``, ``-2.5``, or ``3/4``.

    Returns:
        Exact rational representation of ``value``.

    Raises:
        ValueError: If ``value`` is not a supported number or divides by zero.
    """
    return Fraction(value.strip())


def load_test_cases(csv_path: Path) -> List[SolvingTestCase]:
    """Read and validate numeric algebra cases from a CSV file.

    Args:
        csv_path: UTF-8 CSV path with ``question`` and ``answer`` columns.

    Returns:
        Validated test cases in CSV order.

    Raises:
        FileNotFoundError: If ``csv_path`` does not exist.
        ValueError: If required columns or values are missing or invalid.
    """
    cases: List[SolvingTestCase] = []
    with csv_path.open("r", encoding="utf-8-sig", newline="") as csv_file:
        reader = csv.DictReader(csv_file)
        if reader.fieldnames is None or not {"question", "answer"}.issubset(
            reader.fieldnames
        ):
            raise ValueError("CSV must contain 'question' and 'answer' columns")

        for line_number, row in enumerate(reader, start=2):
            question = (row.get("question") or "").strip()
            answer = (row.get("answer") or "").strip()
            if not question:
                raise ValueError(f"CSV line {line_number} has an empty question")
            try:
                expected = parse_number(answer)
            except (ValueError, ZeroDivisionError) as error:
                raise ValueError(
                    f"CSV line {line_number} has an invalid numeric answer"
                ) from error
            cases.append(SolvingTestCase(question=question, expected=expected))

    if not cases:
        raise ValueError("CSV must contain at least one test case")
    return cases


def parse_final_answer(response: str) -> Optional[Fraction]:
    """Extract the last marked numeric answer from model-generated text.

    Args:
        response: Raw model response expected to contain ``ANSWER: <number>``.

    Returns:
        Exact value from the final answer marker, or ``None`` if absent/invalid.
    """
    # An optional variable assignment supports outputs such as ``ANSWER: x = 7``.
    matches = re.findall(
        r"ANSWER\s*:\s*(?:[A-Za-z]\s*=\s*)?"
        r"(-?(?:\d+(?:\.\d+)?|\.\d+)(?:\s*/\s*-?\d+)?)",
        response,
        flags=re.IGNORECASE,
    )
    if not matches:
        return None
    try:
        return parse_number(matches[-1].replace(" ", ""))
    except (ValueError, ZeroDivisionError):
        return None


def test_model(
    model_path: Path,
    test_cases: Sequence[SolvingTestCase],
    max_tokens: int = 256,
) -> List[SolvingTestResult]:
    """Solve every algebra case with one local model.

    Args:
        model_path: Directory containing the local MLX model and tokenizer.
        test_cases: Ordered algebra problems to evaluate.
        max_tokens: Maximum number of generated tokens per solution.

    Returns:
        One graded result for every supplied test case.

    Raises:
        FileNotFoundError: If required model files are unavailable.
        ValueError: If MLX cannot load the model or format a prompt.
    """
    model, tokenizer = load(str(model_path))
    sampler = make_sampler(temp=0.0)
    results: List[SolvingTestResult] = []

    try:
        for test_case in test_cases:
            instruction = (
                "Solve the following high-school algebra problem. Show your "
                "reasoning briefly. On the final line, write only "
                "ANSWER: <number>. The number may be an integer, decimal, or "
                f"fraction.\n\nProblem: {test_case.question}"
            )
            prompt = tokenizer.apply_chat_template(
                [{"role": "user", "content": instruction}],
                tokenize=False,
                add_generation_prompt=True,
            )
            raw_response = generate(
                model,
                tokenizer,
                prompt=prompt,
                max_tokens=max_tokens,
                sampler=sampler,
                verbose=False,
            ).strip()
            actual = parse_final_answer(raw_response)
            results.append(
                SolvingTestResult(
                    question=test_case.question,
                    expected=test_case.expected,
                    actual=actual,
                    raw_response=raw_response,
                    passed=actual == test_case.expected,
                )
            )
    finally:
        del model, tokenizer
        gc.collect()
        mx.clear_cache()

    return results


def format_number(value: Optional[Fraction]) -> str:
    """Create a compact display value for an exact answer.

    Args:
        value: Parsed rational answer or ``None`` for an unparseable response.

    Returns:
        Integer/fraction text, or ``Unrecognized`` when ``value`` is ``None``.
    """
    if value is None:
        return "Unrecognized"
    return str(value.numerator) if value.denominator == 1 else str(value)


def print_report(model_name: str, results: Sequence[SolvingTestResult]) -> None:
    """Print question-level outcomes and aggregate accuracy.

    Args:
        model_name: Human-readable name used as the report heading.
        results: Graded results for one model.

    Returns:
        None. The report is written to standard output.
    """
    passed_count = sum(result.passed for result in results)
    print(f"\n{model_name}\n{'=' * len(model_name)}")
    for index, result in enumerate(results, start=1):
        status = "PASS" if result.passed else "FAIL"
        print(
            f"{index:2}. {status} | Expected: {format_number(result.expected)} "
            f"| Actual: {format_number(result.actual)}\n    {result.question}"
        )

    total_count = len(results)
    accuracy = (passed_count / total_count * 100) if total_count else 0.0
    print(f"\nResult: {passed_count}/{total_count} correct ({accuracy:.1f}%)")


def run_tests(csv_path: Path, max_tokens: int = 256) -> None:
    """Evaluate both configured SLMs with a numeric algebra CSV.

    Args:
        csv_path: Path to the algebra-solving CSV file.
        max_tokens: Maximum number of generated tokens per solution.

    Returns:
        None. One report per model is printed to standard output.

    Raises:
        FileNotFoundError: If the CSV or a model directory is missing.
        ValueError: If CSV data or model input is invalid.
    """
    test_cases = load_test_cases(csv_path)
    missing_models = [str(path) for path in MODELS.values() if not path.is_dir()]
    if missing_models:
        raise FileNotFoundError(
            "Missing model directories: " + ", ".join(missing_models)
        )

    for model_name, model_path in MODELS.items():
        results = test_model(model_path, test_cases, max_tokens=max_tokens)
        print_report(model_name, results)


def main() -> None:
    """Parse command-line options and run the algebra-solving benchmark.

    Args:
        None. Arguments are read from the command line.

    Returns:
        None. Reports are written to standard output.
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "csv_path",
        nargs="?",
        type=Path,
        default=DEFAULT_TEST_FILE,
        help=f"test CSV path (default: {DEFAULT_TEST_FILE})",
    )
    parser.add_argument(
        "--max-tokens",
        type=int,
        default=256,
        help="maximum generated tokens per solution (default: 256)",
    )
    args = parser.parse_args()
    run_tests(args.csv_path, max_tokens=args.max_tokens)


if __name__ == "__main__":
    main()
