import importlib.util

import pytest
from tomd.ocr import needs_ocr


def test_needs_ocr_when_text_tiny():
    assert needs_ocr("", 3) is True
    assert needs_ocr("   \n  \n", 5) is True


def test_no_ocr_when_text_present():
    assert needs_ocr("A paragraph of real content here." * 3, 1) is False


_HAS_VISION = importlib.util.find_spec("Vision") is not None


@pytest.mark.skipif(not _HAS_VISION, reason="pyobjc Vision not available")
def test_ocr_pdf_returns_text(fixtures):
    from tomd.ocr import ocr_pdf

    scanned = fixtures / "scanned.pdf"
    if not scanned.exists():
        pytest.skip("scanned.pdf fixture absent")
    out = ocr_pdf(scanned)
    assert len(out.strip()) > 0
