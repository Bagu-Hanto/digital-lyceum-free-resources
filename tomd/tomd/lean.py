"""Deterministic markdown -> token-lean markdown. Pure, no I/O."""
import re
from collections import Counter

_DATA_URI_IMG_LINE = re.compile(r"^!\[[^\]]*\]\(data:[^)]*\)\n?", re.MULTILINE)
_ANY_IMG_LINE = re.compile(r"^!\[[^\]]*\]\([^)]*\)\n?", re.MULTILINE)
_DATA_URI_IMG = re.compile(r"!\[[^\]]*\]\(data:[^)]*\)")
_ANY_IMG = re.compile(r"!\[[^\]]*\]\([^)]*\)")
_RULE = re.compile(r"^\s*([-=*])\1{2,}\s*$")
_TABLE_SEP = re.compile(r"^\s*\|?\s*:?-{2,}.*$")
_LINK = re.compile(r"\[([^\]]+)\]\([^)]+\)")
_TRAILING_WS = re.compile(r"[ \t]+$", re.MULTILINE)


def _flatten_table_line(line: str) -> str:
    cells = [c.strip() for c in line.strip().strip("|").split("|")]
    return "\t".join(cells)


def strip(md: str) -> str:
    # 2: drop image refs (data URIs first, then any remaining image syntax)
    md = _DATA_URI_IMG_LINE.sub("", md)
    md = _ANY_IMG_LINE.sub("", md)
    md = _DATA_URI_IMG.sub("", md)
    md = _ANY_IMG.sub("", md)
    # 6: trim links to their label
    md = _LINK.sub(r"\1", md)
    # 1: kill trailing whitespace
    md = _TRAILING_WS.sub("", md)

    out_lines = []
    for line in md.split("\n"):
        # 3: decorative horizontal rules
        if _RULE.match(line):
            continue
        # 5: table separator rows vanish; pipe rows become TSV
        if "|" in line and _TABLE_SEP.match(line):
            continue
        # 5: only true pipe-bounded table rows flatten — prose/code with
        # internal pipes (e.g. "cat x | grep y") must survive untouched.
        stripped = line.strip()
        if stripped.startswith("|") and stripped.endswith("|") and stripped.count("|") >= 2:
            line = _flatten_table_line(line)
        out_lines.append(line)

    # 4: dedup lines that repeat 3+ times (page furniture), keep first
    counts = Counter(l.strip() for l in out_lines if l.strip())
    seen = set()
    deduped = []
    for line in out_lines:
        key = line.strip()
        if key and counts[key] >= 3:
            if key in seen:
                continue
            seen.add(key)
        deduped.append(line)
    md = "\n".join(deduped)

    # 1: collapse runs of blank lines to a single blank line; trim ends
    md = re.sub(r"\n{3,}", "\n\n", md)
    return md.strip("\n")
