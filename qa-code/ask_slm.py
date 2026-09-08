"""Ask one local SLM a question using a reusable prompt template.

The command accepts a question, a model selector, and an optional prompt file.
Run it from the repository root after installing and downloading the models::

    python qa-code/ask_slm.py "What is the capital of France?" phi
    python qa-code/ask_slm.py "What is the weather now?" llama custom.txt
"""

from __future__ import annotations

import argparse
import gc
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Sequence, Tuple

DEFAULT_PROMPT_TEMPLATE = Path("prompt-template/confidence-answer.txt")
DEFAULT_TOKEN_LIMITS = (300, 450, 600)
MODELS: Dict[str, Path] = {
    "Microsoft Phi-4 Mini": Path("models/phi-4-mini-instruct-4bit"),
    "Meta Llama 3.2 3B": Path("models/llama-3.2-3b-instruct-4bit"),
}
MODEL_ALIASES: Dict[str, str] = {
    "phi": "Microsoft Phi-4 Mini",
    "llama": "Meta Llama 3.2 3B",
    "llamda": "Meta Llama 3.2 3B",
}
HELP_DESCRIPTION = """Ask Microsoft Phi-4 Mini or Meta Llama 3.2 3B a question.

The app inserts the question into a reusable prompt template and runs only the
selected local model. Run this command from the repository root."""
HELP_EPILOG = """examples:
  Default confidence template and automatic 300,450,600 retries:
    python qa-code/ask_slm.py "What is the capital of France?" phi

  Select Llama:
    python qa-code/ask_slm.py "Write me a love poem." llama

  Use a custom prompt template:
    python qa-code/ask_slm.py "Explain gravity." phi path/to/template.txt

  Use larger automatic retry allowances:
    python qa-code/ask_slm.py "Write a long article." llama --token-limits 500,1000,2000

  Disable retries and allow at most 800 generated tokens:
    python qa-code/ask_slm.py "Write a long poem." phi --max-tokens 800

token options:
  --token-limits starts with the first allowance and retries from the original
  prompt at each larger allowance only when the previous output reaches its cap.
  --max-tokens uses one fixed allowance and overrides --token-limits.
  A maximum is an allowance, not a required response length. Input tokens plus
  output tokens must fit within the model's total context window.

knowledge cutoffs:
  Llama: Treat events after December 2023 as unknown.
  Phi: Treat events after June 2024 as unknown.
  A date before the cutoff does not guarantee that the model learned the fact.
  Live weather, prices, news, scores, and schedules require current external
  data regardless of the cutoff."""


@dataclass(frozen=True)
class GenerationResult:
    """Store the final response and bounded-retry measurements.

    Attributes:
        response: Final complete or highest-limit generated response.
        output_tokens: Approximate token count of the final response.
        attempted_limits: Output-token limits attempted in order.
        reached_final_limit: Whether the final response probably exhausted the
            largest configured allowance and may still be incomplete.
    """

    response: str
    output_tokens: int
    attempted_limits: Tuple[int, ...]
    reached_final_limit: bool


def parse_token_limits(value: str) -> Tuple[int, ...]:
    """Parse an increasing comma-separated output-token sequence.

    Args:
        value: Text such as ``300,450,600`` from the command line.

    Returns:
        Strictly increasing positive token limits.

    Raises:
        argparse.ArgumentTypeError: If a value is invalid or not increasing.
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
    """Estimate whether generation ended because its allowance was exhausted.

    Args:
        output_tokens: Response size obtained by re-encoding generated text.
        token_limit: Maximum new tokens supplied to the generator.

    Returns:
        ``True`` when the approximate count is within two tokens of the limit.
    """
    return output_tokens >= token_limit - 2


def load_prompt_template(template_path: Path) -> str:
    """Read and validate a question-and-context prompt template.

    Args:
        template_path: UTF-8 text file containing the prompt template.

    Returns:
        Validated template text with surrounding whitespace removed.

    Raises:
        FileNotFoundError: If the template file does not exist.
        ValueError: If the file is empty or lacks one of the required
            ``{question}`` and ``{context}`` placeholders.
    """
    template = template_path.read_text(encoding="utf-8").strip()
    if not template:
        raise ValueError("Prompt template must not be empty")
    for placeholder in ("{question}", "{context}"):
        if template.count(placeholder) != 1:
            raise ValueError(
                f"Prompt template must contain exactly one {placeholder} placeholder"
            )
    return template


def resolve_model(model_name: str) -> tuple[str, Path]:
    """Resolve a short command-line model name to its local directory.

    Args:
        model_name: Case-insensitive selector: ``phi``, ``llama``, or the
            supported misspelling ``llamda``.

    Returns:
        Human-readable model name and corresponding local model path.

    Raises:
        ValueError: If ``model_name`` is not a supported selector.
    """
    normalized_name = model_name.strip().lower()
    display_name = MODEL_ALIASES.get(normalized_name)
    if display_name is None:
        choices = ", ".join(sorted(MODEL_ALIASES))
        raise ValueError(f"Unknown model '{model_name}'. Choose one of: {choices}")
    return display_name, MODELS[display_name]


def ask_slm(
    question: str,
    model_name: str,
    template_path: Path = DEFAULT_PROMPT_TEMPLATE,
    token_limits: Sequence[int] = DEFAULT_TOKEN_LIMITS,
) -> GenerationResult:
    """Generate one template-guided response from the selected local SLM.

    Args:
        question: User question inserted into the prompt template.
        model_name: Short model selector such as ``phi`` or ``llama``.
        template_path: Prompt template file. Defaults to the confidence prompt.
        token_limits: Increasing output allowances used for bounded retries.

    Returns:
        Final response and bounded-retry measurements.

    Raises:
        FileNotFoundError: If the template or selected model is unavailable.
        ValueError: If the model name, prompt, or token limits are invalid.
    """
    if not token_limits or any(limit <= 0 for limit in token_limits):
        raise ValueError("token_limits must contain positive values")
    if any(later <= earlier for earlier, later in zip(token_limits, token_limits[1:])):
        raise ValueError("token_limits must strictly increase")

    display_name, model_path = resolve_model(model_name)
    if not model_path.is_dir():
        raise FileNotFoundError(
            f"The {display_name} model directory does not exist: {model_path}"
        )
    template = load_prompt_template(template_path)
    instruction = template.format(question=question, context="None")

    # Import MLX only when inference begins. This lets ``--help`` and argument
    # validation work in shells that do not have access to the Mac's GPU.
    import mlx.core as mx
    from mlx_lm import generate, load
    from mlx_lm.sample_utils import make_sampler

    model, tokenizer = load(str(model_path))
    try:
        prompt = tokenizer.apply_chat_template(
            [{"role": "user", "content": instruction}],
            tokenize=False,
            add_generation_prompt=True,
        )
        attempted_limits = []
        sampler = make_sampler(temp=0.0)
        for token_limit in token_limits:
            attempted_limits.append(token_limit)
            response = generate(
                model,
                tokenizer,
                prompt=prompt,
                max_tokens=token_limit,
                sampler=sampler,
                verbose=False,
            ).strip()
            output_tokens = len(tokenizer.encode(response))
            reached_limit = probably_reached_token_limit(
                output_tokens,
                token_limit,
            )
            if not reached_limit:
                break
        return GenerationResult(
            response=response,
            output_tokens=output_tokens,
            attempted_limits=tuple(attempted_limits),
            reached_final_limit=reached_limit,
        )
    finally:
        del model, tokenizer
        gc.collect()
        mx.clear_cache()


def create_argument_parser() -> argparse.ArgumentParser:
    """Create the command-line parser and its complete usage guide.

    Args:
        None. The parser configuration uses module-level defaults.

    Returns:
        Argument parser that prints usage, token guidance, and examples when
        the user supplies ``-h`` or ``--help``.
    """
    parser = argparse.ArgumentParser(
        description=HELP_DESCRIPTION,
        epilog=HELP_EPILOG,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("question", help="question to send to the selected SLM")
    parser.add_argument(
        "model",
        choices=sorted(MODEL_ALIASES),
        help="local model selector (llamda is accepted as an alias)",
    )
    parser.add_argument(
        "prompt_template",
        nargs="?",
        type=Path,
        default=DEFAULT_PROMPT_TEMPLATE,
        help=f"prompt file (default: {DEFAULT_PROMPT_TEMPLATE})",
    )
    parser.add_argument(
        "--token-limits",
        type=parse_token_limits,
        default=DEFAULT_TOKEN_LIMITS,
        metavar="N,N,N",
        help="increasing automatic retry allowances (default: 300,450,600)",
    )
    parser.add_argument(
        "--max-tokens",
        type=int,
        metavar="N",
        help="fixed output allowance; disables automatic retries",
    )
    return parser


def main() -> None:
    """Parse command-line arguments, run one SLM, and print its response.

    Args:
        None. Values are read from command-line arguments.

    Returns:
        None. The selected model's answer and elapsed time are printed.
    """
    parser = create_argument_parser()
    args = parser.parse_args()

    if args.max_tokens is not None and args.max_tokens <= 0:
        parser.error("--max-tokens must be greater than zero")

    token_limits = (
        (args.max_tokens,)
        if args.max_tokens is not None
        else args.token_limits
    )

    started = time.perf_counter()
    try:
        result = ask_slm(
            question=args.question,
            model_name=args.model,
            template_path=args.prompt_template,
            token_limits=token_limits,
        )
    except (FileNotFoundError, ValueError) as error:
        parser.error(str(error))
    print(result.response)
    print(
        "\nOutput: "
        f"{result.output_tokens} tokens | "
        f"attempted limits: {', '.join(map(str, result.attempted_limits))}"
    )
    if result.reached_final_limit:
        print("Warning: the response may still be incomplete at the final limit.")
    print(f"\nElapsed time: {time.perf_counter() - started:.3f} seconds")


if __name__ == "__main__":
    main()
