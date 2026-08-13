#! /usr/bin/env python3
"""Tests for example e13_embedded_tk.

This example has no `--ui dump`, and cannot have one: what it teaches is where
the editor is in a window, and a printout has no window to be one part of. So
these run the real thing, with `Tk.mainloop` replaced by what a user would do
next, which is category 2 of design section 10.2 and skips where there is no
display.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from collections.abc import Callable
from pathlib import Path
import json
import tkinter
import pytest
from edit_cfg_json_tk.tk_scope import TAG_PREFIX
from example import e13_embedded_tk
from example.cmd_line import SESSION_NOTHING
from example.e13_embedded_tk import CLOSE_TEXT, DROP_TEXT, PipelineConfig
from .helpers import DATA_FOLDER, NO_DISPLAY

DATA_NAME = 'e13_pipeline.json'
"""Input file of this example, which is copied before it is written over."""


def _run(monkeypatch: pytest.MonkeyPatch, acting: Callable[[tkinter.Tk], None],
         *settings: str) -> None:
    """Run the example, and do one thing to its window instead of looping.

    Args:
        monkeypatch: The pytest fixture that replaces `Tk.mainloop`.
        acting: What is done to the window of the application, which stands
            in for the user of it.
        settings: Command line arguments of the run.
    """
    def instead(window: tkinter.Tk) -> None:
        """Stand in for Tk.mainloop by acting on the window once."""
        window.withdraw()
        window.update_idletasks()
        acting(window)
        window.destroy()
    monkeypatch.setattr(tkinter.Tk, 'mainloop', instead)
    try:
        e13_embedded_tk.main(list(settings))
    except tkinter.TclError:
        pytest.skip(NO_DISPLAY)


def _buttons(window: tkinter.Misc) -> list[tkinter.Button]:
    """Return every button below one widget."""
    found: list[tkinter.Button] = []
    for child in window.winfo_children():
        if isinstance(child, tkinter.Button):
            found.append(child)
        found.extend(_buttons(child))
    return found


def _fields(window: tkinter.Misc) -> list[tkinter.Entry]:
    """Return every edit field below one widget."""
    found: list[tkinter.Entry] = []
    for child in window.winfo_children():
        if isinstance(child, tkinter.Entry):
            found.append(child)
        found.extend(_fields(child))
    return found


def _editor_frame(window: tkinter.Tk) -> tkinter.Misc:
    """Return the frame that the editor built inside the application.

    The editor is mounted in the last widget the application packs, and the
    one frame inside that is the editor's own. Everything above it is the
    application's, which is what this example is about.
    """
    return window.winfo_children()[-1].winfo_children()[0]


def _press(window: tkinter.Misc, text: str) -> None:
    """Press the one button below one widget that shows the given text."""
    buttons = [button for button in _buttons(window)
               if str(button.cget('text')) == text]
    assert len(buttons) == 1
    buttons[0].invoke()


def test_editor_is_mounted(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test the window holds the application's own widgets and the editor."""
    def look(window: tkinter.Tk) -> None:
        """Check that both are there, and that the editor has fields."""
        assert str(window.title()) == e13_embedded_tk.APP_TITLE
        assert _fields(_editor_frame(window))
    _run(monkeypatch, look)


def test_keys_scoped(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test the keys of the editor reach the editor and not the window.

    The application binds the save combination on its own window, so an
    editor that had claimed the window would be running two things on one
    key press.
    """
    def look(window: tkinter.Tk) -> None:
        """Check where the tag of the editor is and where it is not."""
        assert _editor_frame(window).bindtags()[0].startswith(TAG_PREFIX)
        assert not any(tag.startswith(TAG_PREFIX)
                       for tag in window.bindtags())
    _run(monkeypatch, look)


def test_ordinary_keys(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test the flag puts the editor after the widget that has the focus."""
    def look(window: tkinter.Tk) -> None:
        """Check that the tag of the editor is the last of them."""
        assert _editor_frame(window).bindtags()[-1].startswith(TAG_PREFIX)
    _run(monkeypatch, look, '--ordinary-keys')


def test_closing_tells(monkeypatch: pytest.MonkeyPatch,
                       capsys: pytest.CaptureFixture[str]) -> None:
    """Test the application's own control closes the editor and is told."""
    def close(window: tkinter.Tk) -> None:
        """Press the application's own Close editor button."""
        frame = _editor_frame(window)
        _press(window, CLOSE_TEXT)
        assert not frame.winfo_exists()
    _run(monkeypatch, close)
    assert SESSION_NOTHING in capsys.readouterr().out


def test_dropping_is_quiet(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test the control that drops the editor puts no question at all.

    Nothing is unsaved in this run either, so what it really says is that the
    control works; the core is where a question that is not asked is tested.
    """
    def drop(window: tkinter.Tk) -> None:
        """Press the application's own Drop editor button."""
        frame = _editor_frame(window)
        _press(window, DROP_TEXT)
        assert not frame.winfo_exists()
    _run(monkeypatch, drop)


def test_file_is_read(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    """Test the application reads the file it was given and can write it.

    The model is the application's own here, so this is what says that the
    three statements the example shows really do build one. It writes
    somewhere else than it read, so that nothing is overwritten and the editor
    has no reason to ask about a file: what a save does to the file it writes
    over is example 12's, and it is the same editor here.
    """
    out_file = tmp_path / 'pipeline.json'

    def save(window: tkinter.Tk) -> None:
        """Press Save in the editor that the application mounted."""
        _press(_editor_frame(window), 'Save')
    _run(monkeypatch, save, '-i', str(DATA_FOLDER / DATA_NAME), '-o',
         str(out_file))
    assert json.loads(out_file.read_text(encoding='UTF-8')) == \
        {'name': 'release-candidate', 'workers': 8}


def test_class_is_editable() -> None:
    """Test the configuration class of this example is what it says it is."""
    config = PipelineConfig()
    assert config.name == 'nightly'
    assert config.workers == 4
