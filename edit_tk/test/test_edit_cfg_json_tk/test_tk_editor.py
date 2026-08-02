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
from typing import ClassVar, cast
import tkinter
import pytest
from edit_cfg_json import EditModel, EditorBackend
from edit_cfg_json_tk import TkEditor
from edit_cfg_json_tk.tk_editor import EditorWidgets
from example.e01_flat_config import FlatConfig

EXPECTED_LABELS = ['FlatConfig', 'name', 'answer', 'Close']
"""Widget texts that both the stubbed and the real Tk test expect."""

EXPECTED_FIELDS = ['flat example', '42']
"""Field contents that both the stubbed and the real Tk test expect."""


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


def _model_value(model: EditModel, name: str) -> object:
    """Return the value that the buffer holds for one member."""
    return {row.name: row.value for row in model.rows}[name]


def test_stub_widget_texts(stub_tk: None) -> None:
    """Test the stubbed widgets show the class name, the names and a button."""
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
    plain = [widget for widget in FakeWidget.created
             if widget is not root and 'text' not in widget.options]
    frames, fields = plain[::2], plain[1::2]
    assert len(frames) == len(model.rows)
    assert all(frame.parent is root for frame in frames)
    assert [field.parent for field in fields] == frames


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
    field = _real_fields(root_or_skip)[1]
    field.delete(0, 'end')
    field.insert(0, '7')
    assert _model_value(model, 'answer') == 7
    assert widgets.label_text == 'FlatConfig *'


def test_real_typing_undone(root_or_skip: tkinter.Tk) -> None:
    """Test a field typed back to its own value leaves nothing to save."""
    model = EditModel(FlatConfig())
    widgets = EditorWidgets(parent=root_or_skip, model=model)
    field = _real_fields(root_or_skip)[0]
    field.insert('end', ' and more')
    field.delete(len('flat example'), 'end')
    assert not model.dirty
    assert widgets.label_text == 'FlatConfig'


def test_is_editor_backend() -> None:
    """Test TkEditor can be used where an EditorBackend is expected."""
    backend: EditorBackend = TkEditor()
    assert hasattr(backend, 'run_editor')
