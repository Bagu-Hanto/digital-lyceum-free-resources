"""Tesseract OCR fallback for image-only PDFs. Linux-compatible replacement for Apple Vision."""
from pathlib import Path

# ~40 chars/page average is the floor for "this PDF actually has text".
_MIN_CHARS_PER_PAGE = 40


def needs_ocr(text: str, page_count: int) -> bool:
    page_count = max(page_count, 1)
    return len(text.strip()) < _MIN_CHARS_PER_PAGE * page_count


def ocr_pdf(path: Path) -> str:
    import pytesseract
    from pdf2image import convert_from_path

    images = convert_from_path(str(path), dpi=200)
    pages_text = []
    for img in images:
        text = pytesseract.image_to_string(img)
        pages_text.append(text.strip())
    return "\n\n".join(pages_text).strip()
