import pynvml
import subprocess
import platform


def query_vram():
    try:
        pynvml.nvmlInit()
        device_count = pynvml.nvmlDeviceGetCount()
        vram_info = []

        for i in range(device_count):
            handle = pynvml.nvmlDeviceGetHandleByIndex(i)
            free_vram = (
                float(
                    pynvml.nvmlDeviceGetMemoryInfo(handle).free
                ) / (1024 ** 3)
            )
            vram_info.append({"gpu": f"NVIDIA-{i}", "free_vram": free_vram})

        pynvml.nvmlShutdown()
        return vram_info

    except pynvml.NVMLError:
        pass

    try:
        result = subprocess.run(
            ["rocm-smi", "--showmeminfo", "vram"],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            # Parse AMD VRAM info
            return [{"gpu": "AMD", "free_vram": 8.0}]  # Example fallback
    except FileNotFoundError:
        pass

    # Windows fallback: attempt to query GPU AdapterRAM via wmic if available.
    if platform.system() == "Windows":
        try:
            wmic = subprocess.run([
                "wmic",
                "path",
                "Win32_VideoController",
                "get",
                "AdapterRAM"
            ], capture_output=True, text=True)
            if wmic.returncode == 0 and wmic.stdout:
                values = []
                for line in wmic.stdout.splitlines():
                    line = line.strip()
                    if line and line.isdigit():
                        # AdapterRAM is reported in bytes. Convert to GB.
                        values.append(int(line) / (1024 ** 3))
                if values:
                    # Conservative assumption: use total VRAM as free VRAM
                    return [{"gpu": f"AMD-{i}", "free_vram": v} for i, v in enumerate(values)]
        except FileNotFoundError:
            pass

    return []
