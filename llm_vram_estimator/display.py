from rich.table import Table
from rich.console import Console

def display_table(results):
    table = Table(title="LLM VRAM Estimation")

    table.add_column("Model", justify="left")
    table.add_column("Params", justify="right")
    table.add_column("Quant", justify="right")
    table.add_column("Model VRAM", justify="right")
    table.add_column("MaxCtx", justify="right")
    table.add_column("KV/4k", justify="right")
    table.add_column("TotalVRAM", justify="right")

    for result in results:
        table.add_row(
            result["name"],
            result["params"],
            result["quant"],
            result["model_vram"],
            str(result["max_context_length"]),
            result["kv_cache_vram"],
            result["total_vram"]
        )

    console = Console()
    console.print(table)
