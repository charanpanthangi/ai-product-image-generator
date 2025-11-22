"""Core image generation logic using the OpenAI Images API."""
from __future__ import annotations

import base64
from pathlib import Path
from typing import Optional

from openai import OpenAI

from .config import settings
from .utils import STYLES, default_output_path, resolve_file_path, validate_style


class ImageGenerator:
    """Wrapper around the OpenAI Images API for product transformations."""

    def __init__(self, api_key: Optional[str] = None, default_size: str | None = None):
        api_key = api_key or settings.openai_api_key
        if not api_key:
            raise ValueError("OPENAI_API_KEY is required to generate images.")

        self.client = OpenAI(api_key=api_key)
        self.default_size = default_size or settings.default_size

    def build_prompt(self, style: str) -> str:
        validated_style = validate_style(style)
        details = STYLES[validated_style]
        return (
            f"Transform this product photo into a {validated_style} aesthetic. "
            f"Apply the following style description: {details}. Maintain the product's identity,"
            f" crisp edges, and commercial-friendly lighting."
        )

    def generate(
        self,
        input_image: str | Path,
        style: str,
        *,
        size: Optional[str] = None,
        output_path: Optional[str | Path] = None,
    ) -> Path:
        """Generate a transformed image and save it to disk."""
        size = size or self.default_size
        input_path = resolve_file_path(input_image)
        validated_style = validate_style(style)
        output_path = Path(output_path) if output_path else default_output_path(input_path, validated_style)

        with open(input_path, "rb") as f:
            encoded_image = f.read()
        prompt = self.build_prompt(validated_style)

        response = self.client.images.generate(
            model="gpt-image-1",
            prompt=prompt,
            size=size,
            image=encoded_image,
        )

        image_base64 = response.data[0].b64_json
        image_bytes = base64.b64decode(image_base64)

        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "wb") as f:
            f.write(image_bytes)

        return output_path


def generate_product_image(input_image: str | Path, style: str, **kwargs) -> Path:
    generator = ImageGenerator()
    return generator.generate(input_image, style, **kwargs)


__all__ = ["ImageGenerator", "generate_product_image"]
