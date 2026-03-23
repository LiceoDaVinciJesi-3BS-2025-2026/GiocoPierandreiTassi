from importlib.resources import files
from pathlib import Path

def get_image(filename: str) -> Path:
    return files(__package__) / "images" / filename

def get_json(filename: str) -> Path:
    return files(__package__) / "file_json" / filename