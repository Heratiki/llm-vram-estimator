

import argparse

  
def parse_args():
    parser = argparse.ArgumentParser(
        description=(
            "Estimate maximum safe token context length for installed "
            "LLMs."
        )
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose output"
    )
    return parser.parse_args()
