import pynvml
import subprocess

def query_vram():
    try:
        pynvml.nvmlInit()
        device_count = pynvml.nvmlDeviceGetCount()
        vram_info = []

        for i in range(device_count):
            handle = pynvml.nvmlDeviceGetHandleByIndex(i)
            free_vram = pynvml.nvmlDeviceGetMemoryInfo(handle).free / (1024 ** 3)
            vram_info.append({"gpu": f"NVIDIA-{i}", "free_vram": free_vram})

        pynvml.nvmlShutdown()
        return vram_info

    except pynvml.NVMLError:
        pass

    try:
        result = subprocess.run(["rocm-smi", "--showmeminfo", "vram"], capture_output=True, text=True)
        if result.returncode == 0:
            # Parse AMD VRAM info
            return [{"gpu": "AMD", "free_vram": 8.0}]  # Example fallback
    except FileNotFoundError:
        pass

    return []
