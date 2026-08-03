#! /usr/bin/env python3
"""Tests for the Tkinter backend, once stubbed and once with real Tk.

The same widget building is tested both ways on purpose, because the two
ways fail in opposite directions: a stub can drift from what Tk really does,
and real Tk can hide a wrong value behind a widget default. A difference
between the two runs is itself a finding.

The configuration class comes from the example rather than from a class of
its own, so that the same flat configuration is used by the core tests, by
both backends and by the example itself.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from collections.abc import Callable, Iterator
from pathlib import Path
from typing import ClassVar, cast
import json
import tkinter
from tkinter import filedialog
import pytest
from edit_cfg_json import EditModel, EditorBackend, LoadReport
from edit_cfg_json_tk import TkEditor
from edit_cfg_json_tk import edit as tk_edit
from edit_cfg_json_tk.tk_editor import CLOSE_TEXT, EditorWidgets, \
    SAVE_AS_TEXT, SAVE_TEXT, VALIDATE_TEXT
from example.e01_flat_config import FlatConfig

UNKNOWN_VERDICT = 'validation: not validated'
"""Text the editor shows before anything has been validated."""

LOAD_MESSAGE = 'the file left something out'
"""Message of the load in the tests that show one."""

FILLED_REPORT = LoadReport(message=LOAD_MESSAGE, filled=frozenset({'answer'}))
"""Report of a load that filled the number member in from the default."""

FILLED_MARK = ' (filled from default)'
"""Mark of a member that the input file did not hold."""

VALID_VERDICT = 'validation: valid'
"""Text the editor shows for a buffer the application would accept."""

NO_FILE_TEXT = 'save to: no file chosen yet'
"""Text the editor shows while no output file has been chosen."""

BUTTON_TEXTS = [VALIDATE_TEXT, SAVE_TEXT, SAVE_AS_TEXT, CLOSE_TEXT]
"""Texts of the buttons of the editor, in the order they are created."""

EXPECTED_LABELS = ['FlatConfig', 'name', '', 'answer', '', UNKNOWN_VERDICT,
                   NO_FILE_TEXT, *BUTTON_TEXTS]
"""Widget texts that both the stubbed and the real Tk test expect.

The two empty strings are the marks of the two members, which say nothing
until the user or a validator has done something to them.
"""

EXPECTED_LOADED = ['FlatConfig', LOAD_MESSAGE, 'name', '', 'answer',
                   FILLED_MARK, UNKNOWN_VERDICT, NO_FILE_TEXT, *BUTTON_TEXTS]
"""Widget texts of a model whose load filled the number member in.

The message of the load is above the members, because it is what explains
the mark on one of them. The empty string is the mark of the member the file
did hold, which has nothing to say.
"""

EXPECTED_FIELDS = ['Flat example', '42']
"""Field contents that both the stubbed and the real Tk test expect."""

REWRITTEN_MARK = ' (edited) (changed by validator)'
"""Mark of a member that the user changed and a validator then rewrote."""


class FakeWidget:
    """Recording stand-in for a Tkinter widget in the stubbed tests."""

    created: ClassVar[list['FakeWidget']] = []
    """Every stub widget created since the list was last cleared."""

    def __init__(self, parent: object = None, **options: object) -> None:
        """Record this widget together with its parent and its options."""
        self.parent = parent
        self.options = options
        FakeWidget.created.append(self)

    def pack(self, **options: object) -> None:
        """Ignore geometry management, which the stubbed tests do not need."""
        _ = options

    def config(self, **options: object) -> None:
        """Change options of this widget, as a real Tk widget does."""
        self.options.update(options)

    def cget(self, name: str) -> object:
        """Return one option of this widget, as a real Tk widget does."""
        return self.options[name]

    def winfo_toplevel(self) -> 'FakeWidget':
        """Return this widget, standing in for the enclosing window."""
        return self

    def destroy(self) -> None:
        """Ignore window destruction, which the stubbed tests do not need."""

    def invoke(self) -> None:
        """Call the command of this widget, as a real Tk button does."""
        command = self.options['command']
        assert callable(command)
        command()


class FakeVar:
    """Recording stand-in for a `tkinter.StringVar` in the stubbed tests."""

    created: ClassVar[list['FakeVar']] = []
    """Every stub variable created since the list was last cleared."""

    def __init__(self, value: str = '') -> None:
        """Record this variable and the text it starts with."""
        self.value = value
        self.callbacks: list[Callable[..., None]] = []
        FakeVar.created.append(self)

    def get(self) -> str:
        """Return the text this variable holds."""
        return self.value

    def set(self, value: str) -> None:
        """Change the text and tell everyone who traced this variable."""
        self.value = value
        for callback in self.callbacks:
            callback()

    def trace_add(self, mode: str, callback: Callable[..., None]) -> str:
        """Record a callback that a change of this variable calls."""
        assert mode == 'write'
        self.callbacks.append(callback)
        return 'stub trace'


@pytest.fixture(name='stub_tk')
def fixture_stub_tk(monkeypatch: pytest.MonkeyPatch) -> Iterator[None]:
    """Replace the Tkinter widget and variable classes with stubs."""
    FakeWidget.created.clear()
    FakeVar.created.clear()
    for widget_name in ('Frame', 'Label', 'Button', 'Entry'):
        monkeypatch.setattr(tkinter, widget_name, FakeWidget)
    monkeypatch.setattr(tkinter, 'StringVar', FakeVar)
    yield
    FakeWidget.created.clear()
    FakeVar.created.clear()


def _stub_editor(model: EditModel) -> EditorWidgets:
    """Build the stubbed widgets of one model below a stub parent."""
    return EditorWidgets(parent=cast(tkinter.Misc, FakeWidget()), model=model)


def _stub_texts() -> list[str]:
    """Return the text of every stub widget that was given one."""
    return [str(widget.options['text']) for widget in FakeWidget.created
            if 'text' in widget.options]


def _stub_press(button_text: str) -> None:
    """Press the one stub button that shows the given text."""
    buttons = [widget for widget in FakeWidget.created
               if widget.options.get('text') == button_text]
    assert len(buttons) == 1
    buttons[0].invoke()


def _real_texts(widget: tkinter.Misc) -> list[str]:
    """Return the text of every real Tk widget below one widget."""
    texts: list[str] = []
    for child in widget.winfo_children():
        if 'text' in child.keys():
            texts.append(str(child.cget('text')))
        texts.extend(_real_texts(child))
    return texts


def _real_fields(widget: tkinter.Misc) -> list[tkinter.Entry]:
    """Return every real Tk edit field below one widget, in row order."""
    fields: list[tkinter.Entry] = []
    for child in widget.winfo_children():
        if isinstance(child, tkinter.Entry):
            fields.append(child)
        fields.extend(_real_fields(child))
    return fields


def _real_buttons(widget: tkinter.Misc) -> list[tkinter.Button]:
    """Return every real Tk button below one widget, in the order created."""
    buttons: list[tkinter.Button] = []
    for child in widget.winfo_children():
        if isinstance(child, tkinter.Button):
            buttons.append(child)
        buttons.extend(_real_buttons(child))
    return buttons


def _real_press(widget: tkinter.Misc, button_text: str) -> None:
    """Press the one real Tk button below one widget that shows the text."""
    buttons = [button for button in _real_buttons(widget)
               if str(button.cget('text')) == button_text]
    assert len(buttons) == 1
    buttons[0].invoke()


def _retype(field: tkinter.Entry, text: str) -> None:
    """Replace the whole content of one real Tk field."""
    field.delete(0, 'end')
    field.insert(0, text)


def _model_value(model: EditModel, name: str) -> object:
    """Return the value that the buffer holds for one member."""
    return {row.name: row.value for row in model.rows}[name]


def test_stub_widget_texts(stub_tk: None) -> None:
    """Test the stubbed widgets show the class name, the names and buttons."""
    _ = stub_tk
    _stub_editor(EditModel(FlatConfig()))
    assert _stub_texts() == EXPECTED_LABELS


def test_real_widget_texts(root_or_skip: tkinter.Tk) -> None:
    """Test real Tk widgets show exactly what the stubbed test expects."""
    widgets = EditorWidgets(parent=root_or_skip, model=EditModel(FlatConfig()))
    assert widgets.label_text == EXPECTED_LABELS[0]
    assert _real_texts(root_or_skip) == EXPECTED_LABELS


def test_stub_field_values(stub_tk: None) -> None:
    """Test the stubbed fields start with the values of the model."""
    _ = stub_tk
    _stub_editor(EditModel(FlatConfig()))
    assert [field.get() for field in FakeVar.created] == EXPECTED_FIELDS


def test_real_field_values(root_or_skip: tkinter.Tk) -> None:
    """Test real Tk fields start with exactly the same values."""
    widgets = EditorWidgets(parent=root_or_skip, model=EditModel(FlatConfig()))
    assert widgets.label_text == EXPECTED_LABELS[0]
    assert [field.get() for field in
            _real_fields(root_or_skip)] == EXPECTED_FIELDS


def test_stub_row_frames(stub_tk: None) -> None:
    """Test each row gets a frame of its own below the given parent."""
    _ = stub_tk
    root = FakeWidget()
    model = EditModel(FlatConfig())
    EditorWidgets(parent=cast(tkinter.Misc, root), model=model)
    fields = [widget for widget in FakeWidget.created
              if 'textvariable' in widget.options]
    assert len(fields) == len(model.rows)
    for field in fields:
        frame = field.parent
        assert isinstance(frame, FakeWidget)
        assert frame.parent is root


def test_stub_typing(stub_tk: None) -> None:
    """Test typing into a stubbed field changes the model and the label."""
    _ = stub_tk
    model = EditModel(FlatConfig())
    widgets = _stub_editor(model)
    FakeVar.created[1].set('7')
    assert _model_value(model, 'answer') == 7
    assert widgets.label_text == 'FlatConfig *'


def test_real_typing(root_or_skip: tkinter.Tk) -> None:
    """Test typing into a real Tk field changes the model and the label."""
    model = EditModel(FlatConfig())
    widgets = EditorWidgets(parent=root_or_skip, model=model)
    _retype(_real_fields(root_or_skip)[1], '7')
    assert _model_value(model, 'answer') == 7
    assert widgets.label_text == 'FlatConfig *'


def test_real_typing_undone(root_or_skip: tkinter.Tk) -> None:
    """Test a field typed back to its own value leaves nothing to save."""
    model = EditModel(FlatConfig())
    widgets = EditorWidgets(parent=root_or_skip, model=model)
    field = _real_fields(root_or_skip)[0]
    field.insert('end', ' and more')
    field.delete(len('Flat example'), 'end')
    assert not model.dirty
    assert widgets.label_text == 'FlatConfig'


def test_stub_accepts(stub_tk: None) -> None:
    """Test the stubbed Validate button reports an accepted buffer."""
    _ = stub_tk
    widgets = _stub_editor(EditModel(FlatConfig()))
    _stub_press(VALIDATE_TEXT)
    assert widgets.verdict_text_shown == VALID_VERDICT


def test_real_accepts(root_or_skip: tkinter.Tk) -> None:
    """Test the real Validate button reports exactly the same."""
    widgets = EditorWidgets(parent=root_or_skip, model=EditModel(FlatConfig()))
    _real_press(root_or_skip, VALIDATE_TEXT)
    assert widgets.verdict_text_shown == VALID_VERDICT


def test_stub_refuses(stub_tk: None) -> None:
    """Test the stubbed editor shows why the application refused a value."""
    _ = stub_tk
    widgets = _stub_editor(EditModel(FlatConfig()))
    FakeVar.created[1].set('500')
    _stub_press(VALIDATE_TEXT)
    assert 'validation: invalid' in widgets.verdict_text_shown
    assert 'greater than maximum 100' in widgets.verdict_text_shown


def test_real_refuses(root_or_skip: tkinter.Tk) -> None:
    """Test the real editor shows the same refusal."""
    widgets = EditorWidgets(parent=root_or_skip, model=EditModel(FlatConfig()))
    _retype(_real_fields(root_or_skip)[1], '500')
    _real_press(root_or_skip, VALIDATE_TEXT)
    assert 'validation: invalid' in widgets.verdict_text_shown
    assert 'greater than maximum 100' in widgets.verdict_text_shown


def test_stub_rewrites(stub_tk: None) -> None:
    """Test a value a validator rewrote reaches the stubbed field and mark."""
    _ = stub_tk
    model = EditModel(FlatConfig())
    widgets = _stub_editor(model)
    FakeVar.created[0].set('other')
    _stub_press(VALIDATE_TEXT)
    assert FakeVar.created[0].get() == 'Other'
    assert _model_value(model, 'name') == 'Other'
    assert REWRITTEN_MARK in _stub_texts()
    assert widgets.verdict_text_shown == VALID_VERDICT


def test_real_rewrites(root_or_skip: tkinter.Tk) -> None:
    """Test the real field and mark show exactly the same rewrite."""
    model = EditModel(FlatConfig())
    widgets = EditorWidgets(parent=root_or_skip, model=model)
    _retype(_real_fields(root_or_skip)[0], 'other')
    _real_press(root_or_skip, VALIDATE_TEXT)
    assert _real_fields(root_or_skip)[0].get() == 'Other'
    assert _model_value(model, 'name') == 'Other'
    assert REWRITTEN_MARK in _real_texts(root_or_skip)
    assert widgets.verdict_text_shown == VALID_VERDICT


def test_stub_edit_after(stub_tk: None) -> None:
    """Test an edit puts the stubbed editor back to not having validated."""
    _ = stub_tk
    widgets = _stub_editor(EditModel(FlatConfig()))
    _stub_press(VALIDATE_TEXT)
    FakeVar.created[1].set('7')
    assert widgets.verdict_text_shown == UNKNOWN_VERDICT


def test_real_edit_after(root_or_skip: tkinter.Tk) -> None:
    """Test the real editor does the same after an edit."""
    widgets = EditorWidgets(parent=root_or_skip, model=EditModel(FlatConfig()))
    _real_press(root_or_skip, VALIDATE_TEXT)
    _retype(_real_fields(root_or_skip)[1], '7')
    assert widgets.verdict_text_shown == UNKNOWN_VERDICT


def test_stub_load_message(stub_tk: None) -> None:
    """Test the stubbed editor shows what reading the input file did.

    The exact list of texts is asserted, so it also says that the message
    comes above the members it explains and that no widget was added for the
    member the file did hold.
    """
    _ = stub_tk
    _stub_editor(EditModel(FlatConfig(), FILLED_REPORT))
    assert _stub_texts() == EXPECTED_LOADED


def test_real_load_message(root_or_skip: tkinter.Tk) -> None:
    """Test the real Tk editor shows exactly the same about the load."""
    EditorWidgets(parent=root_or_skip,
                  model=EditModel(FlatConfig(), FILLED_REPORT))
    assert _real_texts(root_or_skip) == EXPECTED_LOADED


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


def _written(out_file: Path) -> object:
    """Return what one output file holds, as JSON space values."""
    return json.loads(out_file.read_text(encoding='UTF-8'))


def test_stub_saves(stub_tk: None, tmp_path: Path) -> None:
    """Test the stubbed Save button writes the edited values."""
    _ = stub_tk
    out_file = tmp_path / 'out.json'
    widgets = _stub_editor(EditModel(FlatConfig(), out_file=out_file))
    FakeVar.created[1].set('7')
    _stub_press(SAVE_TEXT)
    assert widgets.save_text_shown == f'Saved to {out_file}.'
    assert _written(out_file) == {'name': 'Flat example', 'answer': 7}


def test_real_saves(root_or_skip: tkinter.Tk, tmp_path: Path) -> None:
    """Test the real Save button writes exactly the same."""
    out_file = tmp_path / 'out.json'
    widgets = EditorWidgets(parent=root_or_skip,
                            model=EditModel(FlatConfig(), out_file=out_file))
    _retype(_real_fields(root_or_skip)[1], '7')
    _real_press(root_or_skip, SAVE_TEXT)
    assert widgets.save_text_shown == f'Saved to {out_file}.'
    assert _written(out_file) == {'name': 'Flat example', 'answer': 7}


def test_stub_save_unmarks(stub_tk: None, tmp_path: Path) -> None:
    """Test the label loses its mark once the values have been written."""
    _ = stub_tk
    widgets = _stub_editor(EditModel(FlatConfig(),
                                     out_file=tmp_path / 'out.json'))
    FakeVar.created[1].set('7')
    assert widgets.label_text == 'FlatConfig *'
    _stub_press(SAVE_TEXT)
    assert widgets.label_text == 'FlatConfig'


def test_real_save_unmarks(root_or_skip: tkinter.Tk, tmp_path: Path) -> None:
    """Test the real label does the same after a save."""
    widgets = EditorWidgets(parent=root_or_skip,
                            model=EditModel(FlatConfig(),
                                            out_file=tmp_path / 'out.json'))
    _retype(_real_fields(root_or_skip)[1], '7')
    assert widgets.label_text == 'FlatConfig *'
    _real_press(root_or_skip, SAVE_TEXT)
    assert widgets.label_text == 'FlatConfig'


def test_stub_save_refused(stub_tk: None, tmp_path: Path) -> None:
    """Test the stubbed editor refuses to write an invalid buffer."""
    _ = stub_tk
    out_file = tmp_path / 'out.json'
    widgets = _stub_editor(EditModel(FlatConfig(), out_file=out_file))
    FakeVar.created[1].set('500')
    _stub_press(SAVE_TEXT)
    assert 'cannot be saved' in widgets.save_text_shown
    assert 'greater than maximum 100' in widgets.verdict_text_shown
    assert not out_file.exists()


def test_real_save_refused(root_or_skip: tkinter.Tk, tmp_path: Path) -> None:
    """Test the real editor refuses the same buffer the same way."""
    out_file = tmp_path / 'out.json'
    widgets = EditorWidgets(parent=root_or_skip,
                            model=EditModel(FlatConfig(), out_file=out_file))
    _retype(_real_fields(root_or_skip)[1], '500')
    _real_press(root_or_skip, SAVE_TEXT)
    assert 'cannot be saved' in widgets.save_text_shown
    assert 'greater than maximum 100' in widgets.verdict_text_shown
    assert not out_file.exists()


def test_stub_save_rewrites(stub_tk: None, tmp_path: Path) -> None:
    """Test a value a validator rewrote is what the file gets.

    Saving validates, so it rewrites what validating would rewrite, and the
    field is refreshed to show what really went into the file.
    """
    _ = stub_tk
    out_file = tmp_path / 'out.json'
    _stub_editor(EditModel(FlatConfig(), out_file=out_file))
    FakeVar.created[0].set('other')
    _stub_press(SAVE_TEXT)
    assert FakeVar.created[0].get() == 'Other'
    assert _written(out_file) == {'name': 'Other', 'answer': 42}


def test_real_save_rewrites(root_or_skip: tkinter.Tk, tmp_path: Path) -> None:
    """Test the real field and the real file show the same rewrite."""
    out_file = tmp_path / 'out.json'
    EditorWidgets(parent=root_or_skip,
                  model=EditModel(FlatConfig(), out_file=out_file))
    _retype(_real_fields(root_or_skip)[0], 'other')
    _real_press(root_or_skip, SAVE_TEXT)
    assert _real_fields(root_or_skip)[0].get() == 'Other'
    assert _written(out_file) == {'name': 'Other', 'answer': 42}


def test_stub_save_as(stub_tk: None, monkeypatch: pytest.MonkeyPatch,
                      tmp_path: Path) -> None:
    """Test Save as chooses a file, writes it, and says where."""
    _ = stub_tk
    out_file = tmp_path / 'chosen.cfg'
    opened = _answer_dialog(monkeypatch, str(out_file))
    widgets = _stub_editor(EditModel(FlatConfig()))
    _stub_press(SAVE_AS_TEXT)
    assert opened == [1]
    assert widgets.save_text_shown == f'Saved to {out_file}.'
    assert _written(out_file) == {'name': 'Flat example', 'answer': 42}


def test_real_save_as(root_or_skip: tkinter.Tk,
                      monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    """Test the real editor does the same with the dialog answered."""
    out_file = tmp_path / 'chosen.cfg'
    _answer_dialog(monkeypatch, str(out_file))
    widgets = EditorWidgets(parent=root_or_skip, model=EditModel(FlatConfig()))
    _real_press(root_or_skip, SAVE_AS_TEXT)
    assert widgets.save_text_shown == f'Saved to {out_file}.'
    assert _written(out_file) == {'name': 'Flat example', 'answer': 42}


def test_stub_save_as_left(stub_tk: None,
                           monkeypatch: pytest.MonkeyPatch) -> None:
    """Test a cancelled dialog writes nothing and chooses nothing.

    Tk reports a cancelled dialog as an empty file name, and there is no
    file whose name is nothing.
    """
    _ = stub_tk
    _answer_dialog(monkeypatch, '')
    model = EditModel(FlatConfig())
    widgets = _stub_editor(model)
    _stub_press(SAVE_AS_TEXT)
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
    widgets = _stub_editor(EditModel(FlatConfig()))
    _stub_press(SAVE_TEXT)
    assert opened == [1]
    assert widgets.save_text_shown == f'Saved to {out_file}.'


def test_real_save_asks(root_or_skip: tkinter.Tk,
                        monkeypatch: pytest.MonkeyPatch,
                        tmp_path: Path) -> None:
    """Test the real Save button asks the same question."""
    out_file = tmp_path / 'asked.json'
    _answer_dialog(monkeypatch, str(out_file))
    widgets = EditorWidgets(parent=root_or_skip, model=EditModel(FlatConfig()))
    _real_press(root_or_skip, SAVE_TEXT)
    assert widgets.save_text_shown == f'Saved to {out_file}.'


def test_stub_destination(stub_tk: None, tmp_path: Path) -> None:
    """Test a session that has a file says where it would write."""
    _ = stub_tk
    out_file = tmp_path / 'out.json'
    widgets = _stub_editor(EditModel(FlatConfig(), out_file=out_file))
    assert widgets.save_text_shown == f'save to: {out_file}'


def test_stub_edit_after_save(stub_tk: None, tmp_path: Path) -> None:
    """Test an edit after a save is worth saving again."""
    _ = stub_tk
    out_file = tmp_path / 'out.json'
    widgets = _stub_editor(EditModel(FlatConfig(), out_file=out_file))
    _stub_press(SAVE_TEXT)
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
        _real_press(window, SAVE_TEXT)
        window.destroy()
    monkeypatch.setattr(tkinter.Tk, 'mainloop', save_and_close)
    try:
        saved = tk_edit(config=FlatConfig(), out_file=out_file)
    except tkinter.TclError:
        pytest.skip('No display available for Tk.')
    assert isinstance(saved, FlatConfig)
    assert _written(out_file) == {'name': 'Flat example', 'answer': 42}


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


def test_is_editor_backend() -> None:
    """Test TkEditor can be used where an EditorBackend is expected."""
    backend: EditorBackend = TkEditor()
    assert hasattr(backend, 'run_editor')
