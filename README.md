# AI Product Image Generator

Generate styled product shots with OpenAI's Images API from the command line or a FastAPI endpoint.

## Features
- Upload a base product image and transform it into marketing-ready visuals.
- Styles: cyberpunk, Christmas, neon glow, studio product photo, cartoon / 3D look.
- FastAPI endpoint: `POST /generate` to receive a PNG.
- CLI usage: `python app/main.py --input image.jpg --style cyberpunk`.

## Setup
1. **Install dependencies**
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Configure environment**
   Create a `.env` file with your OpenAI key:
   ```bash
   OPENAI_API_KEY=sk-...
   ```

## Usage
### CLI
Generate an image from the terminal:
```bash
python app/main.py --input examples/sample_product.jpg --style "cyberpunk"
```
Specify an output path:
```bash
python app/main.py --input examples/sample_product.jpg --style "studio product photo" --output outputs/product_studio.png
```

### API
Start the API server:
```bash
python app/main.py --serve --host 0.0.0.0 --port 8000
```
Then call the endpoint:
```bash
curl -X POST "http://localhost:8000/generate?style=neon%20glow" \
  -H "accept: application/octet-stream" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@examples/sample_product.jpg;type=image/jpeg" \
  --output outputs/neon_glow.png
```
List available styles:
```bash
curl http://localhost:8000/styles
```

## Tests
Run the pytest suite:
```bash
pytest
```

## Examples
Example input and output images can be generated locally. Run the helper script to create lightweight placeholders:
```bash
python examples/create_sample_images.py
```
This writes `examples/sample_product.jpg` and `examples/sample_generated.png` without committing binary assets to the repository.

## Notes
- The OpenAI Images API requires sufficient quota. Ensure your key is set and billing enabled.
- Generated images are saved to the `outputs/` directory by default.
