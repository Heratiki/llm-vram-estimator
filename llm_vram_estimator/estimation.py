def estimate_context_length(vram_info, ollama_models, lmstudio_models):
    results = []

    for model in ollama_models + lmstudio_models:
        params = int(model["params"].replace("B", ""))
        quant = model["quant"]

        model_vram = params * 0.5 if "Q4" in quant else params * 1.0
        kv_cache_vram = 1.0 * (params / 7) if "Q4" in quant else 2.0 * (params / 7)

        free_vram = sum(gpu["free_vram"] for gpu in vram_info)
        max_context_length = int((free_vram - model_vram) / kv_cache_vram * 4096)

        results.append({
            "name": model["name"],
            "params": model["params"],
            "quant": model["quant"],
            "model_vram": f"{model_vram:.1f} GB",
            "max_context_length": max_context_length,
            "kv_cache_vram": f"{kv_cache_vram:.1f} GB",
            "total_vram": f"{model_vram + kv_cache_vram:.1f} GB"
        })

    return results
