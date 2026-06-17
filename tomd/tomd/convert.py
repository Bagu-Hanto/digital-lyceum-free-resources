"""Faithful document -> markdown via Microsoft markitdown."""
from pathlib import Path

from markitdown import MarkItDown

SUPPORTED = {".docx", ".pptx", ".xlsx", ".pdf"}


class UnsupportedFormat(Exception):
    pass


def convert(path: Path) -> str:
    path = Path(path)
    if path.suffix.lower() not in SUPPORTED:
        raise UnsupportedFormat(path.suffix)
    result = MarkItDown().convert(str(path))
    return result.text_content or ""
