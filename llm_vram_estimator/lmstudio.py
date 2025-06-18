import requests

def query_lmstudio_models():
    try:
        response = requests.get("http://localhost:1234/v1/models")
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
