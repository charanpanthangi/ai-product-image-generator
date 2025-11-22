"""FastAPI application exposing the image generation endpoint."""
from __future__ import annotations

import tempfile
from pathlib import Path
from typing import Annotated

from fastapi import Depends, FastAPI, File, HTTPException, UploadFile
from fastapi.responses import FileResponse

from .config import settings
from .generator import ImageGenerator
from .utils import STYLES, validate_style

app = FastAPI(title="AI Product Image Generator", version="1.0.0")


def get_generator() -> ImageGenerator:
    try:
        return ImageGenerator(api_key=settings.openai_api_key)
    except ValueError as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@app.post("/generate", summary="Generate a transformed product image")
async def generate_image(
    style: str,
    file: Annotated[UploadFile, File(description="Base product photo")],
    generator: ImageGenerator = Depends(get_generator),
):
    """Generate a new product image based on a style and uploaded image."""
    try:
        validated_style = validate_style(style)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))

    with tempfile.NamedTemporaryFile(delete=False, suffix=Path(file.filename).suffix) as tmp:
        content = await file.read()
        tmp.write(content)
        tmp_path = Path(tmp.name)

    try:
        output_path = generator.generate(tmp_path, validated_style)
    except Exception as exc:  # pragma: no cover - surfaces to API response
        raise HTTPException(status_code=500, detail=str(exc))
    finally:
        tmp_path.unlink(missing_ok=True)

    return FileResponse(
        path=output_path,
        filename=output_path.name,
        media_type="image/png",
    )


@app.get("/styles", summary="List available styles")
async def list_styles():
    return {"styles": sorted(STYLES.keys())}
