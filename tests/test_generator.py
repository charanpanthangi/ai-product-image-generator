import base64
from pathlib import Path
from types import SimpleNamespace

import pytest

openai = pytest.importorskip("openai", reason="openai package is required for generator tests")

from app.generator import ImageGenerator
from app.utils import STYLES, validate_style


def fake_response(tmp_path: Path):
    image_bytes = b"fake image bytes"
    encoded = base64.b64encode(image_bytes).decode("utf-8")
    return SimpleNamespace(data=[SimpleNamespace(b64_json=encoded)])


def test_validate_style_accepts_known_styles():
    for style in STYLES:
        assert validate_style(style) == style


def test_generate_calls_openai_and_saves_file(monkeypatch, tmp_path):
    temp_image = tmp_path / "input.png"
    temp_image.write_bytes(b"test")

    generator = ImageGenerator(api_key="test")

    def fake_generate(**kwargs):
        assert kwargs["model"] == "gpt-image-1"
        assert "prompt" in kwargs
        assert kwargs["image"]
        return fake_response(tmp_path)

    monkeypatch.setattr(generator.client.images, "generate", fake_generate)

    output_path = generator.generate(temp_image, "cyberpunk")
    assert output_path.exists()
    assert output_path.read_bytes() == b"fake image bytes"


def test_generate_rejects_invalid_style(tmp_path):
    temp_image = tmp_path / "input.png"
    temp_image.write_bytes(b"test")

    generator = ImageGenerator(api_key="test")
    with pytest.raises(ValueError):
        generator.generate(temp_image, "invalid-style")
