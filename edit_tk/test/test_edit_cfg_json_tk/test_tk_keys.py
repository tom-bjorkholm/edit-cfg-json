#! /usr/bin/env python3
"""Tests for the keys of the Tkinter backend, and for closing the editor."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from collections.abc import Callable
from pathlib import Path
from typing import cast
import tkinter
import pytest
from edit_cfg_json import ActionSettings, EditModel, Settings
from edit_cfg_json_tk import edit as tk_edit
from edit_cfg_json_tk.tk_editor import CLOSE_TEXT, EditorWidgets, SAVE_TEXT
from example.e01_flat_config import FlatConfig
from .helpers import FakeVar, FakeWidget, answer_question, real_fields, \
    real_press, retype, stub_editor, stub_keys, stub_press, stub_texts, \
    written

WHEEL_SEQUENCES = ('<MouseWheel>', '<Button-4>', '<Button-5>')
"""The sequences that the editor binds so that the wheel scrolls the body.

They are in the scope of the editor beside the keys of the actions, because a
wheel event goes to the widget under the pointer and the pointer is usually
over a field.
"""

REAL_WHEEL_SEQUENCES = ('<MouseWheel>', '<Button-4>', '<Button-5>')
"""What real Tk calls those same three sequences.

They are the same, unlike the keys of the actions, which real Tk reports with
a `Key` in them.
"""


def real_keys(parent: tkinter.Misc) -> set[str]:
    """Return every sequence the editor bound in the part it reaches.

    The tag of that part is the first of the tags of the widget the editor
    was built below, because these keys are priority keys and Tk offers the
    tags of a widget in the order they are in.

    Args:
        parent: Widget the editor was built below.

    Returns:
        Every event sequence the editor bound.
    """
    return set(parent.bind_class(parent.bindtags()[0]))


def key_settings(actions: ActionSettings) -> Settings:
    """Return the settings of an application that chose these keys."""
    return Settings(actions=actions)


def test_stub_default_keys(stub_tk: None) -> None:
    """Test the default keys of the editor are bound where it reaches."""
    _ = stub_tk
    stub_editor(EditModel(FlatConfig()))
    assert set(stub_keys()) == {'<Control-q>', '<Control-r>', '<F5>',
                                '<Control-s>', '<Control-Shift-S>', '<F12>',
                                '<F1>', '<Control-g>', '<Control-f>', '<F3>',
                                *WHEEL_SEQUENCES}


def test_real_default_keys(root_or_skip: tkinter.Tk) -> None:
    """Test real Tk accepts every sequence the stubbed test expects."""
    EditorWidgets(parent=root_or_skip, model=EditModel(FlatConfig()))
    assert real_keys(root_or_skip) == {'<Control-Key-q>', '<Control-Key-r>',
                                       '<Key-F5>', '<Control-Key-s>',
                                       '<Control-Shift-Key-S>', '<Key-F12>',
                                       '<Key-F1>', '<Control-Key-g>',
                                       '<Control-Key-f>', '<Key-F3>',
                                       *REAL_WHEEL_SEQUENCES}


def test_stub_key_saves(stub_tk: None, tmp_path: Path) -> None:
    """Test the key of the save action writes the output file."""
    _ = stub_tk
    out_file = tmp_path / 'out.json'
    widgets = stub_editor(EditModel(FlatConfig(), out_file=out_file))
    FakeVar.created[1].set('7')
    assert stub_keys()['<Control-s>']() == 'break'
    assert widgets.save_text_shown == f'Saved to {out_file}.'
    assert written(out_file) == {'name': 'Flat example', 'answer': 7}


def test_stub_chosen_key(stub_tk: None, tmp_path: Path) -> None:
    """Test a save key the application chose is the one that is bound."""
    _ = stub_tk
    out_file = tmp_path / 'out.json'
    widgets = stub_editor(EditModel(FlatConfig(), out_file=out_file,
                                    settings=key_settings(ActionSettings(
                                        save=('ctrl+w',)))))
    bindings = stub_keys()
    assert '<Control-s>' not in bindings
    bindings['<Control-w>']()
    assert widgets.save_text_shown == f'Saved to {out_file}.'


def test_stub_key_taken_away(stub_tk: None) -> None:
    """Test an action the application gave no key keeps its button."""
    _ = stub_tk
    stub_editor(EditModel(FlatConfig(),
                          settings=key_settings(ActionSettings(save=()))))
    assert '<Control-s>' not in stub_keys()
    assert SAVE_TEXT in stub_texts()


def test_stub_unknown_key(stub_tk: None) -> None:
    """Test a combination this backend cannot translate binds nothing.

    The editor opens either way, which is the whole point: an action that
    lost a key still has its button.
    """
    _ = stub_tk
    stub_editor(EditModel(FlatConfig(),
                          settings=key_settings(
                              ActionSettings(save=('super+x',)))))
    assert '<Control-x>' not in stub_keys()
    assert SAVE_TEXT in stub_texts()


def test_real_unknown_key(root_or_skip: tkinter.Tk) -> None:
    """Test real Tk refusing a sequence costs the key and not the editor.

    The stub cannot show this, because it accepts every sequence it is
    given. Only real Tk parses one.
    """
    settings = key_settings(ActionSettings(save=('ctrl+nonsense',)))
    widgets = EditorWidgets(parent=root_or_skip,
                            model=EditModel(FlatConfig(), settings=settings))
    assert widgets.label_text == 'FlatConfig'
    assert '<Control-Key-s>' not in real_keys(root_or_skip)


def _close_by_button() -> None:
    """Close the stubbed editor with its button."""
    stub_press(CLOSE_TEXT)


def _close_by_key() -> None:
    """Close the stubbed editor with the key of the quit action."""
    stub_keys()['<Control-q>']()


@pytest.mark.parametrize('close', [_close_by_button, _close_by_key])
def test_stub_close_told(stub_tk: None, close: Callable[[], None]) -> None:
    """Test both ways of closing run what the caller said closing does."""
    _ = stub_tk
    closed: list[str] = []
    EditorWidgets(parent=cast(tkinter.Misc, FakeWidget()),
                  model=EditModel(FlatConfig()),
                  on_close=lambda: closed.append('closed'))
    close()
    assert closed == ['closed']


def test_real_close_window(root_or_skip: tkinter.Tk) -> None:
    """Test closing destroys the window when the caller said nothing.

    That is what a backend which owns the window needs, and it is why a
    caller that does not own one has to say what closing does instead.
    """
    window = tkinter.Toplevel(root_or_skip)
    EditorWidgets(parent=window, model=EditModel(FlatConfig()))
    real_press(window, CLOSE_TEXT)
    assert not window.winfo_exists()


def _edited_editor() -> EditorWidgets:
    """Return a stubbed editor holding a change that has not been saved."""
    widgets = stub_editor(EditModel(FlatConfig()))
    FakeVar.created[1].set('7')
    return widgets


def test_stub_clean_close(stub_tk: None,
                          monkeypatch: pytest.MonkeyPatch) -> None:
    """Test a buffer nobody has touched is closed without a question."""
    _ = stub_tk
    asked = answer_question(monkeypatch, answer=False)
    closed: list[str] = []
    EditorWidgets(parent=cast(tkinter.Misc, FakeWidget()),
                  model=EditModel(FlatConfig()),
                  on_close=lambda: closed.append('closed'))
    stub_press(CLOSE_TEXT)
    assert not asked
    assert closed == ['closed']


@pytest.mark.parametrize('close', [_close_by_button, _close_by_key])
def test_stub_close_asks(stub_tk: None, monkeypatch: pytest.MonkeyPatch,
                         close: Callable[[], None]) -> None:
    """Test both ways out ask before dropping an unsaved change."""
    _ = stub_tk
    asked = answer_question(monkeypatch, answer=False)
    _edited_editor()
    close()
    assert len(asked) == 1
    assert 'discard' in asked[0]


def test_stub_close_kept(stub_tk: None,
                         monkeypatch: pytest.MonkeyPatch) -> None:
    """Test the editor stays open while the answer is not to discard."""
    _ = stub_tk
    answer_question(monkeypatch, answer=False)
    closed: list[str] = []
    widgets = EditorWidgets(parent=cast(tkinter.Misc, FakeWidget()),
                            model=EditModel(FlatConfig()),
                            on_close=lambda: closed.append('closed'))
    FakeVar.created[1].set('7')
    widgets.close_editor()
    assert not closed


def test_stub_close_discarded(stub_tk: None,
                              monkeypatch: pytest.MonkeyPatch) -> None:
    """Test the answer that drops the changes closes the editor."""
    _ = stub_tk
    answer_question(monkeypatch, answer=True)
    closed: list[str] = []
    widgets = EditorWidgets(parent=cast(tkinter.Misc, FakeWidget()),
                            model=EditModel(FlatConfig()),
                            on_close=lambda: closed.append('closed'))
    FakeVar.created[1].set('7')
    widgets.close_editor()
    assert closed == ['closed']


def test_close_after_save(stub_tk: None, tmp_path: Path,
                          monkeypatch: pytest.MonkeyPatch) -> None:
    """Test a change that reached the file is not asked about."""
    _ = stub_tk
    asked = answer_question(monkeypatch, answer=False)
    closed: list[str] = []
    EditorWidgets(parent=cast(tkinter.Misc, FakeWidget()),
                  model=EditModel(FlatConfig(),
                                  out_file=tmp_path / 'out.json'),
                  on_close=lambda: closed.append('closed'))
    FakeVar.created[1].set('7')
    stub_press(SAVE_TEXT)
    stub_press(CLOSE_TEXT)
    assert not asked
    assert closed == ['closed']


def test_real_close_asks(root_or_skip: tkinter.Tk,
                         monkeypatch: pytest.MonkeyPatch) -> None:
    """Test real Tk asks the same question and keeps the same window."""
    asked = answer_question(monkeypatch, answer=False)
    window = tkinter.Toplevel(root_or_skip)
    EditorWidgets(parent=window, model=EditModel(FlatConfig()))
    retype(real_fields(window)[1], '7')
    real_press(window, CLOSE_TEXT)
    assert len(asked) == 1
    assert window.winfo_exists()


def test_window_close_asks(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test the close button of the window asks what the Close button asks.

    It is the one way out that is not a widget of the editor, and it would
    otherwise be the one way out that drops the changes without a word.
    `Tk.mainloop` is replaced by that button being pressed.
    """
    asked = answer_question(monkeypatch, answer=True)

    def close_window(window: tkinter.Tk) -> None:
        """Stand in for Tk.mainloop by closing the window as Tk would."""
        retype(real_fields(window)[1], '7')
        window.tk.call(window.protocol('WM_DELETE_WINDOW'))
    monkeypatch.setattr(tkinter.Tk, 'mainloop', close_window)
    try:
        assert tk_edit(config=FlatConfig()) is None
    except tkinter.TclError:
        pytest.skip('No display available for Tk.')
    assert len(asked) == 1
