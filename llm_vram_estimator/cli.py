import logging
import typer
from llm_vram_estimator.main import run_pipeline

app = typer.Typer()


@app.callback(invoke_without_command=True)
def main(verbose: bool = typer.Option(False, "--verbose", help="Enable verbose output")):
    """Run the VRAM estimation pipeline.

    This is the default top-level callback; it supports a --verbose flag. If you want
    to add subcommands later, they can be registered alongside this callback.
    """
    logging.basicConfig(level=logging.DEBUG if verbose else logging.INFO)
    run_pipeline(verbose=verbose)


if __name__ == "__main__":
    app()
