# Local SLM server project

This project runs Microsoft Phi-4 Mini Instruct and Meta Llama 3.2 3B
Instruct locally on Apple Silicon with MLX. The downloaded checkpoints are
4-bit MLX conversions of the models hosted on Hugging Face, which keeps memory
use practical on a 16 GB Mac.

## Current model sources

- `mlx-community/Phi-4-mini-instruct-4bit`
- `mlx-community/Llama-3.2-3B-Instruct-4bit`

## Run the first comparison

```bash
source .venv/bin/activate
python ask_models.py
```

Pass a different question as the first argument:

```bash
python ask_models.py "Write a short welcome email."
```

The models are loaded sequentially to keep peak memory low.
