"""Write outputs, copy path, notify. Surface-aware (finder vs skill)."""
import hashlib
import shutil
import subprocess
from pathlib import Path

CACHE_DIR = Path.home() / ".tomd_cache"


def estimate_tokens(text: str) -> int:
    return len(text) // 4


def _unique_path(path: Path) -> Path:
    if not path.exists():
        return path
    stem, suffix, parent = path.stem, path.suffix, path.parent
    n = 2
    while (cand := parent / f"{stem}_{n}{suffix}").exists():
        n += 1
    return cand


def _copy_to_clipboard(text: str) -> None:
    # pbcopy (macOS) → xclip/xsel/wl-copy (Linux)
    if shutil.which("pbcopy"):
        subprocess.run(["pbcopy"], input=text, text=True, check=False)
    elif shutil.which("wl-copy"):
        subprocess.run(["wl-copy"], input=text, text=True, check=False)
    elif shutil.which("xclip"):
        subprocess.run(["xclip", "-selection", "clipboard"], input=text, text=True, check=False)
    elif shutil.which("xsel"):
        subprocess.run(["xsel", "--clipboard", "--input"], input=text, text=True, check=False)


def _notify(title: str, message: str) -> None:
    # osascript (macOS) → notify-send (Linux)
    if shutil.which("osascript"):
        esc = message.replace("\\", "\\\\").replace('"', '\\"')
        title_esc = title.replace("\\", "\\\\").replace('"', '\\"')
        script = f'display notification "{esc}" with title "{title_esc}"'
        subprocess.run(["osascript", "-e", script], check=False)
    elif shutil.which("notify-send"):
        subprocess.run(["notify-send", title, message], check=False)


def write(src: Path, faithful: str, lean: str, mode: str) -> Path:
    src = Path(src)
    before = estimate_tokens(faithful)
    after = estimate_tokens(lean)
    pct = round(100 * (before - after) / before) if before else 0

    if mode == "skill":
        CACHE_DIR.mkdir(parents=True, exist_ok=True)
        digest = hashlib.sha1(str(src.resolve()).encode()).hexdigest()[:12]
        primary = CACHE_DIR / f"{digest}_lean.md"
        primary.write_text(lean)
        return primary

    faithful_path = _unique_path(src.with_suffix(".md"))
    lean_path = faithful_path.with_name(faithful_path.stem + "_lean.md")
    faithful_path.write_text(faithful)
    lean_path.write_text(lean)
    _copy_to_clipboard(str(lean_path))
    _notify(
        "tomd",
        f"{src.name}: {before//1000}k -> {after//1000}k tokens (-{pct}%), lean path copied",
    )
    return faithful_path
