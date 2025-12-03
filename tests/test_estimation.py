from llm_vram_estimator.estimation import estimate_context_length


def test_estimate_context_for_q4_7b():
    vram_info = [{"gpu": "NVIDIA-0", "free_vram": 4.0}]
    models = [{"name": "test-7b", "params": "7B", "quant": "Q4_0"}]
    results = estimate_context_length(vram_info, models, [])
    assert len(results) == 1
    r = results[0]
    assert r["name"] == "test-7b"
    assert r["params"] == "7B"
    assert r["quant"] == "Q4_0"
    assert r["model_vram"] == "3.5 GB"
    assert r["kv_cache_vram"] == "1.0 GB"
    assert r["max_context_length"] == 2048


def test_estimate_context_insufficient_vram():
    # Free VRAM less than model VRAM -> max_context_length 0
    vram_info = [{"gpu": "NVIDIA-0", "free_vram": 1.0}]
    models = [{"name": "big-7b", "params": "7B", "quant": "none"}]
    results = estimate_context_length(vram_info, models, [])
    assert len(results) == 1
    assert results[0]["max_context_length"] == 0
