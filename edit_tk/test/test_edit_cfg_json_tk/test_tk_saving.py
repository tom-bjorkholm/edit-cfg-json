#! /usr/bin/env python3
"""Tests for saving from the Tkinter backend, and for the file it asks for."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from pathlib import Path
import tkinter
from tkinter import filedialog
import pytest
from edit_cfg_json import EditModel, Settings
from edit_cfg_json_tk import edit as tk_edit
from edit_cfg_json_tk.tk_ask import ALL_FILES
from edit_cfg_json_tk.tk_editor import EditorWidgets, SAVE_AS_TEXT, SAVE_TEXT
from example.e01_flat_config import FlatConfig
from .helpers import FakeVar, NO_FILE_TEXT, real_fields, real_press, \
    retype, stub_editor, stub_press, written


def _answer_dialog(monkeypatch: pytest.MonkeyPatch, answer: str) -> list[int]:
    """Make the Save as dialog answer without a display, and count its uses.

    Args:
        monkeypatch: The pytest fixture that replaces the dialog.
        answer: What the dialog gives back. An empty answer is what Tk gives
            back when the user cancelled it.

    Returns:
        A list that gets one entry per time the dialog was opened.
    """
    opened: list[int] = []

    def ask(**options: object) -> str:
        """Stand in for the system dialog that asks for a file name."""
        _ = options
        opened.append(1)
        return answer
    monkeypatch.setattr(filedialog, 'asksaveasfilename', ask)
    return opened


def test_stub_saves(stub_tk: None, tmp_path: Path) -> None:
    """Test the stubbed Save button writes the edited values."""
    _ = stub_tk
    out_file = tmp_path / 'out.json'
    widgets = stub_editor(EditModel(FlatConfig(), out_file=out_file))
    FakeVar.created[1].set('7')
    stub_press(SAVE_TEXT)
    assert widgets.save_text_shown == f'Saved to {out_file}.'
    assert written(out_file) == {'name': 'Flat example', 'answer': 7}


def test_real_saves(root_or_skip: tkinter.Tk, tmp_path: Path) -> None:
    """Test the real Save button writes exactly the same."""
    out_file = tmp_path / 'out.json'
    widgets = EditorWidgets(parent=root_or_skip,
                            model=EditModel(FlatConfig(), out_file=out_file))
    retype(real_fields(root_or_skip)[1], '7')
    real_press(root_or_skip, SAVE_TEXT)
    assert widgets.save_text_shown == f'Saved to {out_file}.'
    assert written(out_file) == {'name': 'Flat example', 'answer': 7}


def test_stub_save_unmarks(stub_tk: None, tmp_path: Path) -> None:
    """Test the label loses its mark once the values have been written."""
    _ = stub_tk
    widgets = stub_editor(EditModel(FlatConfig(),
                                    out_file=tmp_path / 'out.json'))
    FakeVar.created[1].set('7')
    assert widgets.label_text == 'FlatConfig *'
    stub_press(SAVE_TEXT)
    assert widgets.label_text == 'FlatConfig'


def test_real_save_unmarks(root_or_skip: tkinter.Tk, tmp_path: Path) -> None:
    """Test the real label does the same after a save."""
    widgets = EditorWidgets(parent=root_or_skip,
                            model=EditModel(FlatConfig(),
                                            out_file=tmp_path / 'out.json'))
    retype(real_fields(root_or_skip)[1], '7')
    assert widgets.label_text == 'FlatConfig *'
    real_press(root_or_skip, SAVE_TEXT)
    assert widgets.label_text == 'FlatConfig'


def test_stub_save_refused(stub_tk: None, tmp_path: Path) -> None:
    """Test the stubbed editor refuses to write an invalid buffer."""
    _ = stub_tk
    out_file = tmp_path / 'out.json'
    widgets = stub_editor(EditModel(FlatConfig(), out_file=out_file))
    FakeVar.created[1].set('500')
    stub_press(SAVE_TEXT)
    assert 'cannot be saved' in widgets.save_text_shown
    assert 'greater than maximum 100' in widgets.wrong_shown[1]
    assert not out_file.exists()


def test_real_save_refused(root_or_skip: tkinter.Tk, tmp_path: Path) -> None:
    """Test the real editor refuses the same buffer the same way."""
    out_file = tmp_path / 'out.json'
    widgets = EditorWidgets(parent=root_or_skip,
                            model=EditModel(FlatConfig(), out_file=out_file))
    retype(real_fields(root_or_skip)[1], '500')
    real_press(root_or_skip, SAVE_TEXT)
    assert 'cannot be saved' in widgets.save_text_shown
    assert 'greater than maximum 100' in widgets.wrong_shown[1]
    assert not out_file.exists()


def test_stub_save_rewrites(stub_tk: None, tmp_path: Path) -> None:
    """Test a value a validator rewrote is what the file gets.

    Saving validates, so it rewrites what validating would rewrite, and the
    field is refreshed to show what really went into the file.
    """
    _ = stub_tk
    out_file = tmp_path / 'out.json'
    stub_editor(EditModel(FlatConfig(), out_file=out_file))
    FakeVar.created[0].set('other')
    stub_press(SAVE_TEXT)
    assert FakeVar.created[0].get() == 'Other'
    assert written(out_file) == {'name': 'Other', 'answer': 42}


def test_real_save_rewrites(root_or_skip: tkinter.Tk, tmp_path: Path) -> None:
    """Test the real field and the real file show the same rewrite."""
    out_file = tmp_path / 'out.json'
    EditorWidgets(parent=root_or_skip,
                  model=EditModel(FlatConfig(), out_file=out_file))
    retype(real_fields(root_or_skip)[0], 'other')
    real_press(root_or_skip, SAVE_TEXT)
    assert real_fields(root_or_skip)[0].get() == 'Other'
    assert written(out_file) == {'name': 'Other', 'answer': 42}


def test_stub_save_as(stub_tk: None, monkeypatch: pytest.MonkeyPatch,
                      tmp_path: Path) -> None:
    """Test Save as chooses a file, writes it, and says where."""
    _ = stub_tk
    out_file = tmp_path / 'chosen.cfg'
    opened = _answer_dialog(monkeypatch, str(out_file))
    widgets = stub_editor(EditModel(FlatConfig()))
    stub_press(SAVE_AS_TEXT)
    assert opened == [1]
    assert widgets.save_text_shown == f'Saved to {out_file}.'
    assert written(out_file) == {'name': 'Flat example', 'answer': 42}


def test_real_save_as(root_or_skip: tkinter.Tk,
                      monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    """Test the real editor does the same with the dialog answered."""
    out_file = tmp_path / 'chosen.cfg'
    _answer_dialog(monkeypatch, str(out_file))
    widgets = EditorWidgets(parent=root_or_skip, model=EditModel(FlatConfig()))
    real_press(root_or_skip, SAVE_AS_TEXT)
    assert widgets.save_text_shown == f'Saved to {out_file}.'
    assert written(out_file) == {'name': 'Flat example', 'answer': 42}


def test_stub_save_as_left(stub_tk: None,
                           monkeypatch: pytest.MonkeyPatch) -> None:
    """Test a cancelled dialog writes nothing and chooses nothing.

    Tk reports a cancelled dialog as an empty file name, and there is no
    file whose name is nothing.
    """
    _ = stub_tk
    _answer_dialog(monkeypatch, '')
    model = EditModel(FlatConfig())
    widgets = stub_editor(model)
    stub_press(SAVE_AS_TEXT)
    assert model.out_file is None
    assert widgets.save_text_shown == NO_FILE_TEXT


def test_stub_save_asks(stub_tk: None, monkeypatch: pytest.MonkeyPatch,
                        tmp_path: Path) -> None:
    """Test Save asks where to write when the session has no file yet.

    That is what every editor does, and it is the reason the model may be
    built with no destination at all.
    """
    _ = stub_tk
    out_file = tmp_path / 'asked.json'
    opened = _answer_dialog(monkeypatch, str(out_file))
    widgets = stub_editor(EditModel(FlatConfig()))
    stub_press(SAVE_TEXT)
    assert opened == [1]
    assert widgets.save_text_shown == f'Saved to {out_file}.'


def test_real_save_asks(root_or_skip: tkinter.Tk,
                        monkeypatch: pytest.MonkeyPatch,
                        tmp_path: Path) -> None:
    """Test the real Save button asks the same question."""
    out_file = tmp_path / 'asked.json'
    _answer_dialog(monkeypatch, str(out_file))
    widgets = EditorWidgets(parent=root_or_skip, model=EditModel(FlatConfig()))
    real_press(root_or_skip, SAVE_TEXT)
    assert widgets.save_text_shown == f'Saved to {out_file}.'


def test_stub_destination(stub_tk: None, tmp_path: Path) -> None:
    """Test a session that has a file says where it would write."""
    _ = stub_tk
    out_file = tmp_path / 'out.json'
    widgets = stub_editor(EditModel(FlatConfig(), out_file=out_file))
    assert widgets.save_text_shown == f'save to: {out_file}'


def test_stub_edit_after_save(stub_tk: None, tmp_path: Path) -> None:
    """Test an edit after a save is worth saving again."""
    _ = stub_tk
    out_file = tmp_path / 'out.json'
    widgets = stub_editor(EditModel(FlatConfig(), out_file=out_file))
    stub_press(SAVE_TEXT)
    FakeVar.created[1].set('7')
    assert widgets.label_text == 'FlatConfig *'
    assert widgets.save_text_shown == f'save to: {out_file}'


def test_edit_returns_saved(monkeypatch: pytest.MonkeyPatch,
                            tmp_path: Path) -> None:
    """Test the edit of this package saves and gives the object back.

    `Tk.mainloop` is replaced by a save and a close, which is what a user
    who pressed Save and then Close would do.
    """
    out_file = tmp_path / 'out.json'

    def save_and_close(window: tkinter.Tk) -> None:
        """Stand in for Tk.mainloop by saving and closing the window."""
        real_press(window, SAVE_TEXT)
        window.destroy()
    monkeypatch.setattr(tkinter.Tk, 'mainloop', save_and_close)
    try:
        saved = tk_edit(config=FlatConfig(), out_file=out_file)
    except tkinter.TclError:
        pytest.skip('No display available for Tk.')
    assert isinstance(saved, FlatConfig)
    assert written(out_file) == {'name': 'Flat example', 'answer': 42}


def test_edit_returns_none(monkeypatch: pytest.MonkeyPatch,
                           tmp_path: Path) -> None:
    """Test a session that only closes saves nothing and gives back None."""
    out_file = tmp_path / 'out.json'
    monkeypatch.setattr(tkinter.Tk, 'mainloop', tkinter.Tk.destroy)
    try:
        saved = tk_edit(config=FlatConfig(), out_file=out_file)
    except tkinter.TclError:
        pytest.skip('No display available for Tk.')
    assert saved is None
    assert not out_file.exists()


def _dialog_options(monkeypatch: pytest.MonkeyPatch) -> dict[str, object]:
    """Make the Save as dialog answer nothing, and record what it was given.

    Args:
        monkeypatch: The pytest fixture that replaces the dialog.

    Returns:
        A dictionary that gets the options of the dialog when it is opened.
    """
    seen: dict[str, object] = {}

    def ask(**options: object) -> str:
        """Stand in for the system dialog that asks for a file name."""
        seen.update(options)
        return ''
    monkeypatch.setattr(filedialog, 'asksaveasfilename', ask)
    return seen


@pytest.mark.parametrize('settings, extension, types', [
    (Settings(), '', []),
    (Settings(file_extension='.cfg'), '.cfg',
     [('Configuration files (.cfg)', '*.cfg'), (ALL_FILES, '*')]),
    (Settings(file_extension='.cfg', extension_enforced=True), '.cfg',
     [('Configuration files (.cfg)', '*.cfg')])])
def test_dialog_offers(stub_tk: None, monkeypatch: pytest.MonkeyPatch,
                       settings: Settings, extension: str,
                       types: list[tuple[str, str]]) -> None:
    """Test the dialog offers what the application decided about names."""
    _ = stub_tk
    seen = _dialog_options(monkeypatch)
    stub_editor(EditModel(FlatConfig(), settings=settings))
    stub_press(SAVE_AS_TEXT)
    assert seen['defaultextension'] == extension
    assert seen['filetypes'] == types


def test_stub_dialog_name(stub_tk: None, monkeypatch: pytest.MonkeyPatch,
                          tmp_path: Path) -> None:
    """Test the name the dialog gives back is completed by the model."""
    _ = stub_tk
    _answer_dialog(monkeypatch, str(tmp_path / 'chosen'))
    settings = Settings(file_extension='.cfg')
    widgets = stub_editor(EditModel(FlatConfig(), settings=settings))
    stub_press(SAVE_AS_TEXT)
    assert widgets.save_text_shown == f'Saved to {tmp_path / "chosen"}.cfg.'
    assert written(tmp_path / 'chosen.cfg') == {'name': 'Flat example',
                                                'answer': 42}


def test_stub_dialog_refused(stub_tk: None, monkeypatch: pytest.MonkeyPatch,
                             tmp_path: Path) -> None:
    """Test a name that an enforced extension forbids is not written."""
    _ = stub_tk
    out_file = tmp_path / 'chosen.json'
    _answer_dialog(monkeypatch, str(out_file))
    settings = Settings(file_extension='.cfg', extension_enforced=True)
    widgets = stub_editor(EditModel(FlatConfig(), settings=settings))
    stub_press(SAVE_AS_TEXT)
    assert '.cfg extension' in widgets.save_text_shown
    assert not out_file.exists()
