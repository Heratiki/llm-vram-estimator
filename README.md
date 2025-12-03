# llm-vram-estimator

## Purpose
The `llm-vram-estimator` is a CLI tool designed to estimate the maximum safe token context length for installed Large Language Models (LLMs). It leverages NVIDIA VRAM information and APIs to provide insights into token limits.

## Features
- Query available GPU VRAM for NVIDIA and AMD GPUs.
- Detect installed models from Ollama and LM Studio.
- Estimate VRAM usage and maximum context length for each model.
- Display results in a formatted table.

## Setup
1. Install dependencies using Poetry:

    ```bash
    poetry install
    ```

2. Run the CLI tool:

    ```bash
    poetry run python -m llm_vram_estimator.cli --help
    # or to run the pipeline directly:
    poetry run python -m llm_vram_estimator.cli --verbose
    ```

## Example Output

| Model         | Params | Quant | Model VRAM | MaxCtx | KV/4k | TotalVRAM |
|---------------|--------|-------|------------|--------|-------|-----------|
| codellama-7b  | 7B     | Q4_0  | 3.5 GB     | 8192   | 1 GB  | 5.5 GB    |

## Supported Platforms
- Windows
- Linux

## How Context is Calculated
- Base model VRAM usage is estimated based on size and quantization level.
- KV-cache VRAM is calculated at 1 GB per 4k tokens for 7B Q4 models, scaled accordingly.
- Maximum context length is derived from available free VRAM.

## How to Run CLI
To use the CLI, run the following command:

```bash
poetry run python -m llm_vram_estimator.cli --help
```

This will display the available options and commands for interacting with the tool.
