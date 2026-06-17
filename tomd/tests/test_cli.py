from tomd.cli import ERRORS_LOG, process_file


def test_process_unsupported_returns_false(tmp_path, monkeypatch):
    monkeypatch.setattr("tomd.sink._notify", lambda *a, **k: None)
    bad = tmp_path / "note.key"
    bad.write_text("x")
    assert process_file(bad, "finder") is False


def test_process_docx_succeeds(fixtures, tmp_path, monkeypatch):
    monkeypatch.setattr("tomd.sink._copy_to_clipboard", lambda p: None)
    monkeypatch.setattr("tomd.sink._notify", lambda *a, **k: None)
    src = tmp_path / "sample.docx"
    src.write_bytes((fixtures / "sample.docx").read_bytes())
    assert process_file(src, "finder") is True
    assert (tmp_path / "sample.md").exists()
    assert (tmp_path / "sample_lean.md").exists()


def test_batch_isolates_failure(fixtures, tmp_path, monkeypatch):
    from tomd import cli

    monkeypatch.setattr("tomd.sink._copy_to_clipboard", lambda p: None)
    monkeypatch.setattr("tomd.sink._notify", lambda *a, **k: None)
    good = tmp_path / "sample.docx"
    good.write_bytes((fixtures / "sample.docx").read_bytes())
    bad = tmp_path / "broken.key"
    bad.write_text("x")
    ok, failed = cli.run([str(good), str(bad)], "finder")
    assert ok == 1 and failed == 1
    assert (tmp_path / "sample.md").exists()
