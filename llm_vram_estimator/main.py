import logging
from llm_vram_estimator.vram import query_vram
from llm_vram_estimator.ollama import query_ollama_models
from llm_vram_estimator.lmstudio import query_lmstudio_models
from llm_vram_estimator.estimation import estimate_context_length
from llm_vram_estimator.display import display_table


def run_pipeline(verbose: bool = False):
    """Run the CLI pipeline that queries VRAM & models and shows estimates.

    If `verbose` is True, the logging level is set to DEBUG.
    """
    logging.basicConfig(level=logging.DEBUG if verbose else logging.INFO)

    # Query GPU VRAM
    vram_info = query_vram()

    # Query models
    ollama_models = query_ollama_models()
    lmstudio_models = query_lmstudio_models()

    # Estimate context length
    results = estimate_context_length(vram_info, ollama_models, lmstudio_models)

    # Display results
    display_table(results)


if __name__ == "__main__":
    # default behavior (non-verbose)
    run_pipeline()
