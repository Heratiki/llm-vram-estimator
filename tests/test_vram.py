import subprocess
from llm_vram_estimator.vram import query_vram
import platform


def _mock_subprocess_run_wmic(*args, **kwargs):
    class Result:
        def __init__(self):
            # Example output contains a header then byte values per GPU
            self.stdout = "AdapterRAM\n8589934592\n"
            self.returncode = 0

    return Result()


def test_query_vram_wmic(monkeypatch):
    """Simulate Windows `wmic` output for AdapterRAM and ensure we parse it."""
    monkeypatch.setattr(platform, "system", lambda: "Windows")
    monkeypatch.setattr(subprocess, "run", _mock_subprocess_run_wmic)
    info = query_vram()
    assert isinstance(info, list)
    assert len(info) >= 1
    # The example returns 8589934592 bytes => 8.0 GB
    assert any(round(gpu["free_vram"], 1) == 8.0 for gpu in info)
