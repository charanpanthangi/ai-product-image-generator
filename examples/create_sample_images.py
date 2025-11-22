"""Utility to generate lightweight placeholder sample images."""
from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

EXAMPLES_DIR = Path(__file__).resolve().parent


def _draw_label(draw: ImageDraw.ImageDraw, text: str, position: tuple[int, int]) -> None:
    """Draw a simple label on the image with fallback font."""
    try:
        font = ImageFont.truetype("DejaVuSans.ttf", 20)
    except Exception:
        font = ImageFont.load_default()
    draw.text(position, text, fill=(255, 255, 255), font=font)


def create_product_image(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    image = Image.new("RGB", (512, 512), color=(245, 245, 245))
    draw = ImageDraw.Draw(image)
    draw.rectangle([(156, 156), (356, 356)], fill=(200, 80, 80), outline=(60, 60, 60), width=4)
    _draw_label(draw, "Sample Product", (170, 240))
    image.save(path, format="JPEG")


def create_stylized_image(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    image = Image.new("RGB", (512, 512), color=(18, 18, 26))
    draw = ImageDraw.Draw(image)
    draw.ellipse([(156, 156), (356, 356)], fill=(120, 0, 255), outline=(0, 255, 255), width=6)
    _draw_label(draw, "Generated (neon)", (150, 240))
    image.save(path, format="PNG")


def main() -> None:
    create_product_image(EXAMPLES_DIR / "sample_product.jpg")
    create_stylized_image(EXAMPLES_DIR / "sample_generated.png")
    print("Sample images written to", EXAMPLES_DIR)


if __name__ == "__main__":
    main()
