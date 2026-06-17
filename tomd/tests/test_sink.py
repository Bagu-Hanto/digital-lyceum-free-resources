from tomd.sink import _osa_escape, _unique_path, estimate_tokens, write


def test_osa_escape_neutralizes_quotes_and_backslashes():
    # A filename crafted to break out of the AppleScript string + inject a command.
    evil = 'a" & (do shell script "touch /tmp/pwned") & "'
    escaped = _osa_escape(evil)
    assert '"' not in escaped.replace('\\"', "")  # every quote is backslash-escaped
    assert _osa_escape("c:\\x") == "c:\\\\x"


def test_finder_writes_both_siblings(tmp_path, monkeypatch):
    monkeypatch.setattr("tomd.sink._copy_to_clipboard", lambda p: None)
    monkeypatch.setattr("tomd.sink._notify", lambda *a, **k: None)
    src = tmp_path / "report.pdf"
    src.write_bytes(b"%PDF-1.4")
    primary = write(src, "# Faithful\n\nbody", "Faithful\nbody", "finder")
    assert primary == tmp_path / "report.md"
    assert (tmp_path / "report.md").read_text() == "# Faithful\n\nbody"
    assert (tmp_path / "report_lean.md").read_text() == "Faithful\nbody"


def test_collision_increments(tmp_path):
    (tmp_path / "report.md").write_text("old")
    assert _unique_path(tmp_path / "report.md") == tmp_path / "report_2.md"


def test_skill_writes_to_cache(tmp_path, monkeypatch):
    cache = tmp_path / "cache"
    monkeypatch.setattr("tomd.sink.CACHE_DIR", cache)
    monkeypatch.setattr("tomd.sink._notify", lambda *a, **k: None)
    src = tmp_path / "deck.pptx"
    src.write_bytes(b"x")
    primary = write(src, "faithful", "lean text", "skill")
    assert primary.parent == cache
    assert primary.name.endswith("_lean.md")
    assert primary.read_text() == "lean text"


def test_estimate_tokens_is_chars_over_four():
    assert estimate_tokens("a" * 400) == 100
