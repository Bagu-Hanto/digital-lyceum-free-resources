---
name: tomd
description: Use when the user provides, attaches, or references a .pdf, .docx, .pptx, or .xlsx file and you need its contents. Converts the document to token-efficient markdown with the tomd CLI and reads the resulting _lean.md instead of the raw binary, saving tokens.
---

# tomd — read documents as token-lean markdown

When a `.pdf`, `.docx`, `.pptx`, or `.xlsx` file is provided or referenced:

1. Run the converter (replace `<tomd-dir>` with wherever you installed tomd, and
   use the absolute path to the document):

   ```bash
   cd <tomd-dir> && uv run tomd --mode skill --for-llm "<absolute-file-path>"
   ```

2. The command prints the path to a `_lean.md` in `~/.tomd_cache/`. **Read that file** with the Read tool — do NOT read the raw document.

3. If the command exits non-zero, tell the user it failed and fall back to reading the file directly.

Encrypted files trigger a native macOS password prompt automatically; if the user cancels, the conversion is skipped.
