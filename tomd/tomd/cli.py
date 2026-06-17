"""CLI entry: batch loop, encryption + OCR orchestration, failure isolation."""
import sys
from pathlib import Path

import click

from . import convert, crypto, lean, ocr, sink

ERRORS_LOG = Path.home() / ".tomd_cache" / "errors.log"


def _log_error(path: Path, exc: Exception) -> None:
    ERRORS_LOG.parent.mkdir(parents=True, exist_ok=True)
    with open(ERRORS_LOG, "a") as fh:
        fh.write(f"{path}: {type(exc).__name__}: {exc}\n")


def _page_count(path: Path) -> int:
    if path.suffix.lower() != ".pdf":
        return 1
    try:
        import pikepdf

        with pikepdf.open(path) as pdf:
            return len(pdf.pages)
    except Exception:
        return 1


def process_file(path: Path, mode: str) -> bool:
    path = Path(path)
    temp = None
    try:
        work = path
        if crypto.is_encrypted(path):
            pw = crypto.prompt_password(path.name)
            if pw is None:
                sink._notify("tomd", f"skipped {path.name} (no password)")
                return False
            try:
                temp = crypto.decrypt_to_temp(path, pw)
            except crypto.BadPassword:
                pw = crypto.prompt_password(path.name)  # one retry
                if pw is None:
                    sink._notify("tomd", f"skipped {path.name} (no password)")
                    return False
                temp = crypto.decrypt_to_temp(path, pw)
            work = temp

        faithful = convert.convert(work)
        if work.suffix.lower() == ".pdf" and ocr.needs_ocr(faithful, _page_count(work)):
            faithful = ocr.ocr_pdf(work)
        lean_md = lean.strip(faithful)
        primary = sink.write(path, faithful, lean_md, mode)
        if mode == "skill":
            click.echo(str(primary))
        return True
    except convert.UnsupportedFormat as exc:
        sink._notify("tomd", f"unsupported: {path.suffix}")
        _log_error(path, exc)
        return False
    except Exception as exc:
        sink._notify("tomd", f"failed: {path.name} (see errors.log)")
        _log_error(path, exc)
        return False
    finally:
        if temp is not None:
            temp.unlink(missing_ok=True)


def run(paths: list[str], mode: str) -> tuple[int, int]:
    ok = failed = 0
    for p in paths:
        if process_file(Path(p), mode):
            ok += 1
        else:
            failed += 1
    return ok, failed


@click.command()
@click.argument("files", nargs=-1, required=True)
@click.option("--mode", type=click.Choice(["finder", "skill"]), default="finder")
@click.option("--for-llm", is_flag=True, help="(skill) alias kept for clarity")
def main(files, mode, for_llm):
    # Preflight: deps present?
    try:
        import markitdown  # noqa: F401
    except ImportError:
        click.echo("tomd: missing deps; run `uv sync` in tools/tomd", err=True)
        sys.exit(2)
    ok, failed = run(list(files), mode)
    if len(files) > 1:
        sink._notify("tomd", f"{ok} of {ok + failed} converted, {failed} failed")
    sys.exit(0 if failed == 0 else 1)
