from importlib.resources import files
from pathlib import Path

BASE_DIR = Path(__file__).parent

def get_image(filename: str) -> Path:
    return BASE_DIR / "images" / filename

def get_json(filename: str) -> Path:
    return BASE_DIR / "file_json" / filename

