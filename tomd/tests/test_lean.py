from tomd.lean import strip


def test_prose_with_pipes_not_flattened():
    line = "Run `cat x | grep y | wc -l` to count."
    assert strip(line) == line


def test_skill_echo_uses_sink_path(tmp_path, monkeypatch):
    # Note 2 regression: cli must echo the exact path sink.write returns,
    # not a re-derived hash.
    import tomd.cli as cli
    import tomd.sink as sink

    monkeypatch.setattr(sink, "CACHE_DIR", tmp_path / "cache")
    monkeypatch.setattr(sink, "_notify", lambda *a, **k: None)
    monkeypatch.setattr(cli.crypto, "is_encrypted", lambda p: False)
    monkeypatch.setattr(cli.convert, "convert", lambda p: "# Doc\n\nbody")
    src = tmp_path / "deck.pptx"
    src.write_bytes(b"x")
    echoed = []
    monkeypatch.setattr(cli.click, "echo", lambda s, **k: echoed.append(s))
    assert cli.process_file(src, "skill") is True
    assert echoed and echoed[0].endswith("_lean.md")
    assert (tmp_path / "cache" / echoed[0].rsplit("/", 1)[-1]).exists()


def test_collapses_blank_line_runs():
    assert strip("a\n\n\n\nb") == "a\n\nb"


def test_strips_trailing_spaces():
    assert strip("a   \nb\t\n") == "a\nb"


def test_drops_data_uri_images():
    md = "text\n![chart](data:image/png;base64,AAAA)\nmore"
    assert strip(md) == "text\nmore"


def test_strips_horizontal_rules():
    assert strip("a\n---\nb\n===\nc") == "a\nb\nc"


def test_trims_link_to_label():
    assert strip("see [the report](https://x.example/very/long) now") == "see the report now"


def test_flattens_pipe_table_to_tsv():
    md = "| A | B |\n| --- | --- |\n| 1 | 2 |\n| 3 | 4 |"
    assert strip(md) == "A\tB\n1\t2\n3\t4"


def test_dedups_repeated_footer_lines():
    md = "Page 1\nConfidential\nPage 2\nConfidential\nPage 3\nConfidential"
    out = strip(md)
    assert out.count("Confidential") == 1


def test_keeps_headings():
    assert "# Title" in strip("# Title\n\nbody")


def test_never_drops_body_text():
    body = "The quarterly revenue rose 12 percent."
    assert body in strip(f"## Section\n\n{body}\n")
