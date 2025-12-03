import requests


def query_lmstudio_models(timeout: float = 2.0):
    """Query LM Studio's local HTTP API for installed models.

    Uses a small timeout to avoid long blocks if the server isn't running.
    """
    try:
        response = requests.get("http://localhost:1234/v1/models", timeout=timeout)
        if response.status_code == 200:
            models = []
            for model in response.json():
                models.append({
                    "name": model.get("name"),
                    "params": model.get("size", "7B"),
                    "quant": model.get("quant", "Q4_0"),
                    "max_context_length": model.get("maxContextLength", 8192)
                })
            return models
    except requests.RequestException:
        pass

    return []
