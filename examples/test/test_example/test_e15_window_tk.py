#! /usr/bin/env python3
"""Tests for example e15_window_tk.

Here the editor gets a window of its own over the application, so these press
the application's button and then look at the window that appeared, at what it
is named, and at what is left of the application when it closes.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from pathlib import Path
import tkinter
import pytest
from example import e15_window_tk
from example._shared_pipeline import CLOSE_TEXT, EDIT_TEXT, SESSION_NOTHING
from .helpers import PIPELINE_FILE, data_file, run_tk_example, \
    tk_fields, tk_press, written_json

EDITOR_CLOSE = 'Close'
"""Text of the button of the editor itself that ends the session.

The application has one of its own beside it, which says `CLOSE_TEXT` and
calls `close` rather than being a widget of the editor at all.
"""


def _editor_window(window: tkinter.Tk) -> tkinter.Toplevel:
    """Return the window that the editor made for itself over this one.

    It is taken off the screen before anything is done to it, in the same way
    as the window of the application: a test that put a window in front of
    whoever is running it would be a test nobody wants to run.
    """
    windows = [child for child in window.winfo_children()
               if isinstance(child, tkinter.Toplevel)]
    assert len(windows) == 1
    windows[0].withdraw()
    return windows[0]


def _status(window: tkinter.Tk) -> str:
    """Return what the application says on its own status line."""
    label = window.winfo_children()[0]
    assert isinstance(label, tkinter.Label)
    return str(label.cget('text'))


def test_no_window_at_first(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test the application opens no editor until its button is pressed."""
    def look(window: tkinter.Tk) -> None:
        """Check that no window of the editor's own exists yet."""
        assert not [child for child in window.winfo_children()
                    if isinstance(child, tkinter.Toplevel)]
    run_tk_example(e15_window_tk.main, monkeypatch, look)


def test_window_is_opened(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test the editor gets a window of its own, named after the class."""
    def look(window: tkinter.Tk) -> None:
        """Press the button and look at the window that appeared."""
        tk_press(window, EDIT_TEXT)
        editor = _editor_window(window)
        assert str(editor.title()) == 'PipelineConfig'
        assert tk_fields(editor)
    run_tk_example(e15_window_tk.main, monkeypatch, look)


def test_window_is_destroyed(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test closing takes that window away and leaves the application's."""
    def close(window: tkinter.Tk) -> None:
        """Press the editor's own Close and look at both windows."""
        tk_press(window, EDIT_TEXT)
        editor = _editor_window(window)
        tk_press(editor, EDITOR_CLOSE)
        assert not editor.winfo_exists()
        assert window.winfo_exists()
        assert SESSION_NOTHING in _status(window)
    run_tk_example(e15_window_tk.main, monkeypatch, close)


def test_app_closes_editor(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test the application's own button closes the editor's window.

    A user cannot press that button while the editor is modal, which is what
    the example says about it and what a real grab enforces. The grab is
    taken away here, as `run_tk_example` explains, so what is left to check
    is that `close` from the application really takes the window away.
    """
    def close(window: tkinter.Tk) -> None:
        """Press the application's own Close and look at what is left."""
        tk_press(window, EDIT_TEXT)
        editor = _editor_window(window)
        tk_press(window, CLOSE_TEXT)
        assert not editor.winfo_exists()
        assert SESSION_NOTHING in _status(window)
    run_tk_example(e15_window_tk.main, monkeypatch, close)


def test_file_is_read(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    """Test the editor reads the file the example was given, and writes it."""
    out_file = tmp_path / 'pipeline.json'

    def save(window: tkinter.Tk) -> None:
        """Open the editor and press Save in its own window."""
        tk_press(window, EDIT_TEXT)
        tk_press(_editor_window(window), 'Save')
    run_tk_example(e15_window_tk.main, monkeypatch, save, '-i',
                   data_file(PIPELINE_FILE), '-o', str(out_file))
    assert written_json(out_file) == {'name': 'release-candidate',
                                      'workers': 8}
