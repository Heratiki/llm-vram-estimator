# Copilot / AI Agent Guidance for llm-vram-estimator

## TL;DR
This repository is a small CLI that queries local GPUs + installed local LLM services (Ollama / LM Studio) to estimate the maximum safe token context length for models based on free VRAM. Keep changes modular: data discovery (GPU, model sources) → estimation → display.

## Big-picture architecture
- Entry point: `llm_vram_estimator/main.py` composes the pipeline:
  - `query_vram()` — discover GPU free VRAM (NVIDIA via pysnvml / AMD via `rocm-smi` fallback).
  - `query_ollama_models()` — query installed Ollama models (shell `ollama list`).
  - `query_lmstudio_models()` — query LM Studio over HTTP (localhost:1234).
  - `estimate_context_length()` — combine VRAM and model info to estimate safe tokens.
  - `display_table()` — render results using `rich.Table`.

## Patterns & conventions
- Small, pure query functions returning lists of dictionaries with a common shape; prefer these fields for each model:
  - `name` (string), `params` (string like `7B`), `quant` (string like `Q4_0`), optional `max_context_length` for reported model value.
- `vram.query_vram()` returns `[{"gpu": "NVIDIA-0", "free_vram": 3.5}, ...]` or `[]` if detection fails.
- `estimation.estimate_context_length()` expects `params` to be a string with trailing `B` and uses `quant` to select factors; be conservative when adding new quantizations or parameter units.
- Avoid printing in query functions: return data and let `display_table` handle console output.
- Error-handling: current code swallows exceptions; prefer returning an empty list to preserve pipeline behavior.

## Key files to reference
- `llm_vram_estimator/main.py` — orchestration
- `llm_vram_estimator/vram.py` — GPU detection and free VRAM values
- `llm_vram_estimator/ollama.py` — Ollama model discovery (CLI-based)
- `llm_vram_estimator/lmstudio.py` — LM Studio model discovery (HTTP API)
- `llm_vram_estimator/estimation.py` — numeric estimator (model VRAM & KV cache calculation)
- `llm_vram_estimator/display.py` — formatting with `rich`
 - `llm_vram_estimator/cli.py` — Typer CLI (with `--verbose` top-level option). Use `python -m llm_vram_estimator.cli --verbose` to run or `python -m llm_vram_estimator.main`.

## Developer workflows / commands
- Install dependencies (Poetry used):

```pwsh
poetry install
```

- Run the app via Poetry:

```pwsh
poetry run python -m llm_vram_estimator.cli --help
# To run the pipeline with verbose output
poetry run python -m llm_vram_estimator.cli --verbose
# or the module entrypoint directly (non-verbose)
poetry run python -m llm_vram_estimator.main
```

- Run tests (if you add them):

```pwsh
poetry run pytest
```

- Lint with flake8:

```pwsh
poetry run flake8
```

## Integration points — what to watch for
- NVIDIA: `pynvml` package. Ensure `pynvml.nvmlInit()` is called and `nvmlShutdown()` after reading values. Unit tests can mock `pynvml` to simulate GPUs.
- AMD: `rocm-smi` run via subprocess; parsing is basic; tests should mock `subprocess.run` for `rocm-smi` and `ollama`.
- Ollama: code relies on a local `ollama` CLI in PATH. Tests should mock `subprocess.run` if `ollama` isn't present.
- LM Studio: HTTP API at `http://localhost:1234/v1/models` — it expects JSON model entries with `name`, `size`, `quant`, `maxContextLength`.

## Helpful change guidelines for contributors
- When adding a new model discovery source, implement a function `query_<source>()` that returns the standard model dicts. Add it to `main.py` to keep the pipeline intact.
- Update `estimation/` when adding new parameter units or quant schemes — make sure to add parsing and fallback behaviors (avoid raising on malformed `params` strings).
- Prefer returning empty lists (no models) rather than raising, so the CLI can still run and report partial results.
- Add unit tests for the new source and for `estimate_context_length()` edge cases (e.g., 0 free VRAM, unknown quantization strings, `params` not ending with `B`).
 - Add unit tests for the new source and for `estimate_context_length()` edge cases (e.g., 0 free VRAM, unknown quantization strings, `params` not ending with `B`). Note: a sample test suite exists under `tests/test_estimation.py` that validates `estimate_context_length()` behavior.

## Examples & quick reference
- Expected model dict example:

```python
{
  "name": "my-7b-model",
  "params": "7B",
  "quant": "Q4_0",
  "max_context_length": 8192  # optional
}
```

- `estimate_context_length()` key behavior:
  - Parses `params` by stripping trailing `B` to int; e.g., `"7B" => 7`
  - Applies different model and KV cache VRAM multipliers for `Q4` variants vs others

## Known gaps / TODOs (useful for PR reviewers)
 - `--verbose` is a top-level option wired into the Typer CLI `llm_vram_estimator/cli.py`. It sets Python `logging` to DEBUG; `llm_vram_estimator/main.py` exposes `run_pipeline(verbose=False)` when called programmatically.
- Replace broad exception swallowing for better diagnostics (return data and log warnings instead).
- Add unit tests for each query function and the estimator.
- Consider a clear config or `Model` dataclass to reduce tight coupling to string-based params.

---
If something in this guide is incomplete or you want more detail (examples for mocking `pynvml`, tests scaffolding, or a contributed `Model` dataclass proposal), tell me which area to expand. ✅
