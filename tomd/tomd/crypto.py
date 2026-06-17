"""Encrypted-document detection, macOS password prompt, decrypt-to-temp."""
import subprocess
import tempfile
from pathlib import Path

import msoffcrypto
import pikepdf

_OFFICE = {".docx", ".pptx", ".xlsx"}


class BadPassword(Exception):
    pass


def is_encrypted(path: Path) -> bool:
    path = Path(path)
    suffix = path.suffix.lower()
    if suffix == ".pdf":
        try:
            with pikepdf.open(path):
                return False
        except pikepdf.PasswordError:
            return True
    if suffix in _OFFICE:
        with open(path, "rb") as fh:
            return msoffcrypto.OfficeFile(fh).is_encrypted()
    return False


def _osa_escape(text: str) -> str:
    """Escape AppleScript string metacharacters (backslash then quote)."""
    return text.replace("\\", "\\\\").replace('"', '\\"')


def prompt_password(filename: str) -> str | None:
    script = (
        f'display dialog "Password for {_osa_escape(filename)}:" '
        'default answer "" with hidden answer '
        'with title "tomd"'
    )
    proc = subprocess.run(["osascript", "-e", script], capture_output=True, text=True)
    if proc.returncode != 0:  # user cancelled
        return None
    for part in proc.stdout.strip().split(", "):
        if part.startswith("text returned:"):
            return part[len("text returned:") :]
    return None


def decrypt_to_temp(path: Path, password: str) -> Path:
    path = Path(path)
    suffix = path.suffix.lower()
    out = Path(tempfile.mkstemp(suffix=suffix, prefix="tomd_")[1])
    if suffix == ".pdf":
        try:
            with pikepdf.open(path, password=password) as pdf:
                pdf.save(out)
        except pikepdf.PasswordError:
            out.unlink(missing_ok=True)
            raise BadPassword(path.name)
        return out
    if suffix in _OFFICE:
        with open(path, "rb") as fh:
            office = msoffcrypto.OfficeFile(fh)
            try:
                office.load_key(password=password)
                with open(out, "wb") as dst:
                    office.decrypt(dst)
            except Exception as exc:  # msoffcrypto raises InvalidKeyError
                out.unlink(missing_ok=True)
                raise BadPassword(path.name) from exc
        return out
    raise BadPassword(path.name)
