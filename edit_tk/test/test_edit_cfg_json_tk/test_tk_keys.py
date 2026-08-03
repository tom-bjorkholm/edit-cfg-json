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
from edit_cfg_json_tk.tk_editor import CLOSE_TEXT, EditorWidgets, SAVE_TEXT
from example.e01_flat_config import FlatConfig
from .helpers import FakeVar, FakeWidget, real_press, stub_editor, \
    stub_press, stub_texts, stub_window, written


def key_settings(actions: ActionSettings) -> Settings:
    """Return the settings of an application that chose these keys."""
    return Settings(actions=actions)


def test_stub_default_keys(stub_tk: None) -> None:
    """Test the default keys of the editor are bound on the window."""
    _ = stub_tk
    stub_editor(EditModel(FlatConfig()))
    assert set(stub_window().bindings) == {'<Control-q>', '<Control-r>',
                                           '<F5>', '<Control-s>',
                                           '<Control-Shift-S>', '<F12>',
                                           '<F1>', '<Control-g>'}


def test_real_default_keys(root_or_skip: tkinter.Tk) -> None:
    """Test real Tk accepts every sequence the stubbed test expects."""
    EditorWidgets(parent=root_or_skip, model=EditModel(FlatConfig()))
    assert set(root_or_skip.bind()) == {'<Control-Key-q>', '<Control-Key-r>',
                                        '<Key-F5>', '<Control-Key-s>',
                                        '<Control-Shift-Key-S>', '<Key-F12>',
                                        '<Key-F1>', '<Control-Key-g>'}


def test_stub_key_saves(stub_tk: None, tmp_path: Path) -> None:
    """Test the key of the save action writes the output file."""
    _ = stub_tk
    out_file = tmp_path / 'out.json'
    widgets = stub_editor(EditModel(FlatConfig(), out_file=out_file))
    FakeVar.created[1].set('7')
    assert stub_window().bindings['<Control-s>']() == 'break'
    assert widgets.save_text_shown == f'Saved to {out_file}.'
    assert written(out_file) == {'name': 'Flat example', 'answer': 7}


def test_stub_chosen_key(stub_tk: None, tmp_path: Path) -> None:
    """Test a save key the application chose is the one that is bound."""
    _ = stub_tk
    out_file = tmp_path / 'out.json'
    widgets = stub_editor(EditModel(FlatConfig(), out_file=out_file,
                                    settings=key_settings(ActionSettings(
                                        save=('ctrl+w',)))))
    bindings = stub_window().bindings
    assert '<Control-s>' not in bindings
    bindings['<Control-w>']()
    assert widgets.save_text_shown == f'Saved to {out_file}.'


def test_stub_key_taken_away(stub_tk: None) -> None:
    """Test an action the application gave no key keeps its button."""
    _ = stub_tk
    stub_editor(EditModel(FlatConfig(),
                          settings=key_settings(ActionSettings(save=()))))
    assert '<Control-s>' not in stub_window().bindings
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
    assert not [key for key in stub_window().bindings if 'w' in key.lower()]
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
    assert '<Control-Key-s>' not in set(root_or_skip.bind())


def _close_by_button() -> None:
    """Close the stubbed editor with its button."""
    stub_press(CLOSE_TEXT)


def _close_by_key() -> None:
    """Close the stubbed editor with the key of the quit action."""
    stub_window().bindings['<Control-q>']()


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
