"""Helper utilities for the image generator."""
from __future__ import annotations

from pathlib import Path
from typing import Dict

STYLES: Dict[str, str] = {
    "cyberpunk": "a neon-drenched cyberpunk city backdrop with reflective lighting",
    "christmas": "a warm, holiday-themed setting with festive lights and snow",
    "neon glow": "a bold neon glow aesthetic with vibrant rim lighting",
    "studio product photo": "a high-end studio product photo with soft shadows",
    "cartoon": "a playful cartoon 3D render with clean outlines and depth",
    "3d": "a stylized 3D product render with soft reflections",
}


ALLOWED_STYLE_KEYS = {
    "cyberpunk",
    "christmas",
    "neon glow",
    "studio product photo",
    "cartoon",
    "3d",
    "cartoon / 3d look",
}


def normalize_style(style: str) -> str:
    normalized = style.strip().lower()
    if normalized == "cartoon / 3d look":
        return "cartoon"
    return normalized


def validate_style(style: str) -> str:
    normalized = normalize_style(style)
    if normalized not in STYLES:
        raise ValueError(
            f"Unsupported style '{style}'. Choose from: {', '.join(sorted(STYLES.keys()))}."
        )
    return normalized


def ensure_directory(path: str | Path) -> Path:
    path = Path(path)
    path.mkdir(parents=True, exist_ok=True)
    return path


def default_output_path(input_path: str | Path, style: str) -> Path:
    base = Path(input_path).stem
    output_dir = ensure_directory("outputs")
    normalized = normalize_style(style).replace(" ", "_")
    return output_dir / f"{base}_{normalized}.png"


def resolve_file_path(file_path: str | Path) -> Path:
    path = Path(file_path).expanduser().resolve()
    if not path.exists():
        raise FileNotFoundError(f"Input image not found at {path}")
    return path


__all__ = [
    "STYLES",
    "validate_style",
    "default_output_path",
    "resolve_file_path",
]
