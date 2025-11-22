"""Configuration utilities for the image generator service."""
from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Optional

from dotenv import load_dotenv


load_dotenv()


@dataclass
class Settings:
    """Application settings loaded from environment variables."""

    openai_api_key: Optional[str] = None
    default_size: str = "1024x1024"

    @classmethod
    def from_env(cls) -> "Settings":
        return cls(openai_api_key=os.getenv("OPENAI_API_KEY"))


settings = Settings.from_env()
