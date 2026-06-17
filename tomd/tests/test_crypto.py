import pytest
from tomd.crypto import BadPassword, decrypt_to_temp, is_encrypted


def test_detects_encrypted_pdf(fixtures):
    assert is_encrypted(fixtures / "locked.pdf") is True


def test_plain_docx_not_encrypted(fixtures):
    assert is_encrypted(fixtures / "sample.docx") is False


def test_decrypt_with_right_password(fixtures):
    out = decrypt_to_temp(fixtures / "locked.pdf", "secret")
    assert out.exists() and out.stat().st_size > 0
    out.unlink()


def test_decrypt_wrong_password_raises(fixtures):
    with pytest.raises(BadPassword):
        decrypt_to_temp(fixtures / "locked.pdf", "wrong")
