#! /usr/bin/env python3
"""Tests for example a01_tk_for_no_gui.

The editor owns the window and the event loop here, so what stands in for the
user is `Tk.mainloop`: the run opens the editor, the stand-in acts on the
window once, and the call comes back. What the run then prints is the whole of
what this example is about, because the outcome of such a session is the
return value of `edit`.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from pathlib import Path
import tkinter
import pytest
from example import a01_tk_for_no_gui
from example._shared_pipeline import RUN_UNCHANGED, SESSION_NOTHING, \
    SESSION_SAVED
from .helpers import NO_DISPLAY, PIPELINE_FILE, SAVED_PIPELINE, \
    data_file, open_tk_editor, refusal_of, tk_press, written_json

SAVE_TEXT = 'Save'
"""Text of the button of the editor that writes the output file."""

SAVED_VALUES = 'Running release-candidate with 8 workers.'
"""What the command says it runs with after saving the shared input file."""


def _run(monkeypatch: pytest.MonkeyPatch, *settings: str,
         saving: bool = False) -> None:
    """Run the example with the editor's window acted on once.

    This example catches `tkinter.TclError` itself and ends with a message of
    its own, so a machine with no display never reaches the skip that
    `open_tk_editor` has for one. That message is what is skipped on here.

    Args:
        monkeypatch: The pytest fixture that replaces `Tk.mainloop`.
        settings: The whole command line the example is given.
        saving: Whether the stand-in user presses Save before closing.
    """
    acting = _press_save if saving else None
    try:
        open_tk_editor(a01_tk_for_no_gui.main, monkeypatch, *settings,
                       acting=acting)
    except SystemExit as ended:
        if ended.code != a01_tk_for_no_gui.NO_DISPLAY:
            raise
        pytest.skip(NO_DISPLAY)


def _press_save(window: tkinter.Tk) -> None:
    """Press Save in the editor that owns this window."""
    tk_press(window, SAVE_TEXT)


def test_opens_and_returns(monkeypatch: pytest.MonkeyPatch,
                           capsys: pytest.CaptureFixture[str]) -> None:
    """Test the call comes back, with nothing saved, once the editor closes.

    Nothing saved is an ordinary outcome and not an error: the user closed the
    editor without pressing Save, so the command keeps the values it had.
    """
    _run(monkeypatch)
    printed = capsys.readouterr().out
    assert SESSION_NOTHING in printed
    assert RUN_UNCHANGED in printed


def test_reads_the_file(monkeypatch: pytest.MonkeyPatch,
                        capsys: pytest.CaptureFixture[str]) -> None:
    """Test the editor is given the input file the command line named."""
    _run(monkeypatch, '-i', data_file(PIPELINE_FILE))
    assert SESSION_NOTHING in capsys.readouterr().out


def test_saved_comes_back(monkeypatch: pytest.MonkeyPatch,
                          capsys: pytest.CaptureFixture[str],
                          tmp_path: Path) -> None:
    """Test a save writes the file and hands the object back to the command.

    The command goes on with the object `edit` answered with, which is what
    the last line says: the object the command constructed is untouched, so
    the values named here can only have come from the return value.
    """
    out_file = tmp_path / 'pipeline.json'
    _run(monkeypatch, '-i', data_file(PIPELINE_FILE), '-o', str(out_file),
         saving=True)
    printed = capsys.readouterr().out
    assert SESSION_SAVED.format(name='PipelineConfig') in printed
    assert SAVED_VALUES in printed
    assert written_json(out_file) == SAVED_PIPELINE


def test_refuses_bad_file(monkeypatch: pytest.MonkeyPatch,
                          capsys: pytest.CaptureFixture[str],
                          tmp_path: Path) -> None:
    """Test an input file that cannot be read ends the run with a message.

    No editor is opened at all, which is the point: a user who named a file
    must not be given the declared defaults without being told.
    """
    missing = tmp_path / 'not_there.json'
    said = refusal_of(lambda: _run(monkeypatch, '-i', str(missing)))
    assert str(missing) in said
    assert SESSION_NOTHING not in capsys.readouterr().out
