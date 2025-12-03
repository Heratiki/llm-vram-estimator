def _parse_params(params_str: str) -> float:
    """Parse a params string like '7B', '7.5B', or '7000M' into a float representing billions (B).

    Returns the parameter count in billions (e.g., 7.0 for '7B').
    """
    if not params_str:
        return 7.0
    p = params_str.strip()
    try:
        if p.lower().endswith("b"):
            return float(p[:-1])
        if p.lower().endswith("m"):
            return float(p[:-1]) / 1000.0
        return float(p)
    except Exception:
        # Fallback conservative default if parsing fails
        return 7.0


def estimate_context_length(vram_info, ollama_models, lmstudio_models):
    results = []

    models = (ollama_models or []) + (lmstudio_models or [])
    free_vram = sum(gpu.get("free_vram", 0.0) for gpu in (vram_info or []))

    for model in models:
        params_b = _parse_params(model.get("params", "7B"))
        quant = model.get("quant", "Q4_0")

        # Estimate model VRAM footprint in GB (simple multiplier based on quantization)
        model_vram = params_b * 0.5 if "Q4" in quant else params_b * 1.0

        # KV-cache VRAM: GB per 4k tokens (scales with model size)
        kv_cache_per_4k = 1.0 * (params_b / 7.0) if "Q4" in quant else 2.0 * (params_b / 7.0)

        remaining_vram = free_vram - model_vram
        if remaining_vram <= 0 or kv_cache_per_4k <= 0:
            max_context_length = 0
        else:
            max_context_length = int(remaining_vram / kv_cache_per_4k * 4096)
            if max_context_length < 0:
                max_context_length = 0

        results.append({
            "name": model.get("name"),
            "params": model.get("params", "7B"),
            "quant": model.get("quant", "Q4_0"),
            "model_vram": f"{model_vram:.1f} GB",
            "max_context_length": max_context_length,
            "kv_cache_vram": f"{kv_cache_per_4k:.1f} GB",
            "total_vram": f"{(model_vram + kv_cache_per_4k):.1f} GB",
        })

    return results
