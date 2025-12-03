import subprocess


def query_ollama_models():
    try:
        result = subprocess.run(["ollama", "list"], capture_output=True, text=True)
        if result.returncode == 0:
            models = []
            for line in result.stdout.splitlines():
                if line.strip():
                    models.append({"name": line.strip(), "params": "7B", "quant": "Q4_0"})  # Example parsing
            return models
    except FileNotFoundError:
        pass

    return []
