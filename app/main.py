"""Command-line interface for generating images and running the API server."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import uvicorn
from dotenv import load_dotenv

from .api import app
from .generator import ImageGenerator
from .utils import STYLES, validate_style


load_dotenv()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="AI Product Image Generator")
    parser.add_argument("--input", required=False, help="Path to the input product image")
    parser.add_argument("--style", required=False, help="Transformation style")
    parser.add_argument(
        "--output",
        required=False,
        help="Optional output path for the generated image (defaults to outputs/<name>_<style>.png)",
    )
    parser.add_argument(
        "--serve",
        action="store_true",
        help="Start the FastAPI server instead of running the CLI generation",
    )
    parser.add_argument(
        "--host",
        default="0.0.0.0",
        help="Host for the API server",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="Port for the API server",
    )
    return parser.parse_args()


def run_cli(input_path: str, style: str, output: str | None = None) -> None:
    generator = ImageGenerator()
    validated_style = validate_style(style)
    output_path = generator.generate(input_path, validated_style, output_path=output)
    print(f"Generated image saved to {output_path}")


def main() -> None:
    args = parse_args()

    if args.serve:
        uvicorn.run(app, host=args.host, port=args.port)
        return

    if not args.input or not args.style:
        print("Error: --input and --style are required when not running the server.")
        print("Available styles:", ", ".join(sorted(STYLES.keys())))
        sys.exit(1)

    run_cli(args.input, args.style, args.output)


if __name__ == "__main__":
    main()
