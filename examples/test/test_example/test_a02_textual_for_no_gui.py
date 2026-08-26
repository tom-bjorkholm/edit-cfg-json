#! /usr/bin/env python3
"""Tests for example a02_textual_for_no_gui.

The editor owns the terminal and the event loop here, so what stands in for
the user is `App.run`: the run opens the editor, the stand-in presses keys in
it, and the call comes back. What the run then prints is the whole of what
this example is about, because the outcome of such a session is the return
value of `edit`.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from pathlib import Path
import pytest
from example import a02_textual_for_no_gui
from example._shared_pipeline import RUN_UNCHANGED, SESSION_NOTHING, \
    SESSION_SAVED
from .helpers import PIPELINE_FILE, QUIT_KEY, SAVED_PIPELINE, SAVE_KEY, \
    data_file, editor_titles, refusal_of, written_json

CLASS_TITLE = 'PipelineConfig'
"""What the editor calls the configuration this example edits."""

SAVED_VALUES = 'Running release-candidate with 8 workers.'
"""What the command says it runs with after saving the shared input file."""


def test_opens_and_returns(monkeypatch: pytest.MonkeyPatch,
                           capsys: pytest.CaptureFixture[str]) -> None:
    """Test the call comes back, with nothing saved, once the editor closes.

    Nothing saved is an ordinary outcome and not an error: the user quit the
    editor without saving, so the command keeps the values it had.
    """
    assert editor_titles(a02_textual_for_no_gui.main,
                         monkeypatch) == [CLASS_TITLE]
    printed = capsys.readouterr().out
    assert SESSION_NOTHING in printed
    assert RUN_UNCHANGED in printed


def test_reads_the_file(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test the editor is given the input file the command line named.

    The label is unmarked, because reading a file is not an edit: what the
    editor opened on is what the file holds.
    """
    assert editor_titles(a02_textual_for_no_gui.main, monkeypatch, '-i',
                         data_file(PIPELINE_FILE)) == [CLASS_TITLE]


def test_saved_comes_back(monkeypatch: pytest.MonkeyPatch,
                          capsys: pytest.CaptureFixture[str],
                          tmp_path: Path) -> None:
    """Test a save writes the file and hands the object back to the command.

    The command goes on with the object `edit` answered with, which is what
    the last line says: the object the command constructed is untouched, so
    the values named here can only have come from the return value.
    """
    out_file = tmp_path / 'pipeline.json'
    editor_titles(a02_textual_for_no_gui.main, monkeypatch, '-i',
                  data_file(PIPELINE_FILE), '-o', str(out_file),
                  keys=(SAVE_KEY, QUIT_KEY))
    printed = capsys.readouterr().out
    assert SESSION_SAVED.format(name=CLASS_TITLE) in printed
    assert SAVED_VALUES in printed
    assert written_json(out_file) == SAVED_PIPELINE


def test_refuses_bad_file(monkeypatch: pytest.MonkeyPatch,
                          capsys: pytest.CaptureFixture[str],
                          tmp_path: Path) -> None:
    """Test an input file that cannot be read ends the run with a message.

    No editor is started at all, which is the point: a user who named a file
    must not be given the declared defaults without being told.
    """
    missing = tmp_path / 'not_there.json'
    said = refusal_of(lambda: editor_titles(a02_textual_for_no_gui.main,
                                            monkeypatch, '-i', str(missing)))
    assert str(missing) in said
    assert SESSION_NOTHING not in capsys.readouterr().out
