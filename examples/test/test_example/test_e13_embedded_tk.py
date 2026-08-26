#! /usr/bin/env python3
"""Tests for example e13_embedded_tk.

The editor is built into an area of the application's own window when the
button of the application is pressed, so these press that button and then look
at what appeared, and at what is left when the editor closes.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from pathlib import Path
import tkinter
import pytest
from edit_cfg_json_tk.tk_scope import TAG_PREFIX
from example import e13_embedded_tk
from example._shared_pipeline import CLOSE_TEXT, EDIT_TEXT, SESSION_NOTHING
from .helpers import PIPELINE_FILE, SAVED_PIPELINE, data_file, \
    run_tk_example, tk_fields, tk_press, written_json

EDITOR_CLOSE = 'Close'
"""Text of the button of the editor itself that ends the session.

The application has one of its own beside it, which says `CLOSE_TEXT` and
calls `close` rather than being a widget of the editor at all.
"""


def _status(window: tkinter.Tk) -> str:
    """Return what the application says on its own status line."""
    label = window.winfo_children()[0].winfo_children()[0]
    assert isinstance(label, tkinter.Label)
    return str(label.cget('text'))


def _area(window: tkinter.Tk) -> tkinter.Misc:
    """Return the widget of the application that the editor is mounted in.

    It is the last widget the application packs, and everything before it is
    the application's own, which is what this example is about.
    """
    return window.winfo_children()[-1]


def _editor(window: tkinter.Tk) -> tkinter.Misc:
    """Return the frame that the editor built inside that area."""
    return _area(window).winfo_children()[0]


def test_area_starts_empty(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test the application shows no editor until its button is pressed."""
    def look(window: tkinter.Tk) -> None:
        """Check that the area the editor goes in holds nothing yet."""
        assert not _area(window).winfo_children()
    run_tk_example(e13_embedded_tk.main, monkeypatch, look)


def test_editor_is_mounted(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test pressing the button builds the whole editor into that area."""
    def look(window: tkinter.Tk) -> None:
        """Press the button and check that the editor has fields."""
        tk_press(window, EDIT_TEXT)
        assert tk_fields(_editor(window))
    run_tk_example(e13_embedded_tk.main, monkeypatch, look)


def test_keys_scoped(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test the keys of the editor reach the editor and not the window.

    An editor that had claimed the window would take keys away from the
    widgets the application has beside it.
    """
    def look(window: tkinter.Tk) -> None:
        """Check where the tag of the editor is and where it is not."""
        tk_press(window, EDIT_TEXT)
        assert _editor(window).bindtags()[0].startswith(TAG_PREFIX)
        assert not any(tag.startswith(TAG_PREFIX)
                       for tag in window.bindtags())
    run_tk_example(e13_embedded_tk.main, monkeypatch, look)


def test_closing_clears_area(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test closing the editor empties the area and says what was saved."""
    def close(window: tkinter.Tk) -> None:
        """Press the editor's own Close and look at what is left."""
        tk_press(window, EDIT_TEXT)
        editor = _editor(window)
        tk_press(editor, EDITOR_CLOSE)
        assert not editor.winfo_exists()
        assert not _area(window).winfo_children()
        assert SESSION_NOTHING in _status(window)
    run_tk_example(e13_embedded_tk.main, monkeypatch, close)


def test_app_closes_editor(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test the application's own button closes the editor and is told.

    The editor is not modal here, so a button of the application beside it
    can still be pressed while it runs, which is what `close` is for.
    """
    def close(window: tkinter.Tk) -> None:
        """Press the application's own Close and look at what is left."""
        tk_press(window, EDIT_TEXT)
        tk_press(window, CLOSE_TEXT)
        assert not _area(window).winfo_children()
        assert SESSION_NOTHING in _status(window)
    run_tk_example(e13_embedded_tk.main, monkeypatch, close)


def test_file_is_read(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    """Test the editor reads the file the example was given, and writes it.

    The editor reads the file itself here, which is what the one statement of
    this example says. It writes somewhere else than it read, so that nothing
    is overwritten and the editor has no reason to ask about a file.
    """
    out_file = tmp_path / 'pipeline.json'

    def save(window: tkinter.Tk) -> None:
        """Mount the editor and press Save in it."""
        tk_press(window, EDIT_TEXT)
        tk_press(_editor(window), 'Save')
    run_tk_example(e13_embedded_tk.main, monkeypatch, save, '-i',
                   data_file(PIPELINE_FILE), '-o', str(out_file))
    assert written_json(out_file) == SAVED_PIPELINE
