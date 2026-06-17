import pytest
from tomd.convert import UnsupportedFormat, convert


def test_converts_docx_text(fixtures):
    out = convert(fixtures / "sample.docx")
    assert "Quarterly revenue rose 12 percent." in out


def test_converts_xlsx_cells(fixtures):
    out = convert(fixtures / "sample.xlsx")
    assert "A" in out and "B" in out


def test_unsupported_raises(tmp_path):
    p = tmp_path / "note.key"
    p.write_text("x")
    with pytest.raises(UnsupportedFormat):
        convert(p)
