# tomd — documents to token-lean Markdown

`tomd` converts `.pdf`, `.docx`, `.pptx`, and `.xlsx` files into Markdown that's
cheap to feed an LLM. Every conversion produces two files beside the source:

- `name.md` — a faithful Markdown rendering of the document.
- `name_lean.md` — the same content, deterministically stripped to the
  token-minimal version. **This is the one you paste into an LLM.**

---

## Credit

Originally created by [Ari Evergreen](https://www.skool.com/@ari-evergreen?g=cliefnotes) as a macOS-native tool using Apple's Vision framework for OCR. Ported to cross-platform (Linux + macOS) by [Joseph Kemp](https://digitallyceum.netlify.app) by replacing the Apple Vision OCR layer with Tesseract + pdf2image, and swapping macOS-only notification/clipboard calls for cross-platform equivalents (notify-send, xclip/xsel/wl-copy).

---

## Requirements

- **[uv](https://docs.astral.sh/uv/)** — Python package manager
  - macOS: `brew install uv`
  - Linux: `curl -LsSf https://astral.sh/uv/install.sh | sh`
- Python 3.11+ (uv manages its own virtualenv, so system Python version doesn't matter)
- **Linux only:** `tesseract` and `poppler-utils` for scanned-PDF OCR fallback
  - Ubuntu/Debian: `sudo apt install tesseract-ocr poppler-utils`
  - Fedora: `sudo dnf install tesseract poppler-utils`

---

## Install

```bash
cd tomd
uv sync
```

That's it.

---

## Use it

### Command line

```bash
uv run tomd path/to/document.docx
```

Writes `document.md` + `document_lean.md` beside the source file.

Multiple files at once:

```bash
uv run tomd file1.pdf file2.docx file3.xlsx
```

### Claude Code skill

If you use Claude Code, symlink the skill into your skills directory:

```bash
mkdir -p ~/.claude/skills/tomd
ln -sf "$(pwd)/skill/SKILL.md" ~/.claude/skills/tomd/SKILL.md
```

Open `skill/SKILL.md` and replace `<tomd-dir>` with this folder's absolute path.
After that, Claude auto-converts any document you hand it and reads the lean
Markdown instead of the raw binary, saving tokens.

---

## How it works

1. **Convert** — Microsoft's `markitdown` library renders the document to faithful Markdown.
2. **OCR fallback** — if a PDF has less than ~40 characters per page (scanned/image-only), Tesseract OCR extracts the text instead. On macOS, this originally used Apple's Vision framework; the Linux port uses `pytesseract` + `pdf2image`.
3. **Lean pass** — a deterministic set of regex transforms strips images, decorative rules, link URLs, table pipes, and repeated page furniture. The result is the token-minimal `_lean.md`.
4. **Encrypted files** — detected automatically. You'll be prompted for a password; cancel to skip.

---

## Supported formats

- `.pdf` — text-embedded and scanned (OCR fallback)
- `.docx` — Word documents
- `.pptx` — PowerPoint presentations
- `.xlsx` — Excel spreadsheets

---

## Notes

- Run the tests with `uv sync --extra dev && uv run pytest -q`.
- Errors are logged to `~/.tomd_cache/errors.log`.
