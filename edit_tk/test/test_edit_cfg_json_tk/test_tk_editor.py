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

from collections.abc import Iterator
from typing import ClassVar, cast
import tkinter
import pytest
from edit_cfg_json import EditModel, EditorBackend
from edit_cfg_json_tk import TkEditor
from edit_cfg_json_tk.tk_editor import build_editor_widgets
from example.e01_flat_config import FlatConfig

EXPECTED_TEXTS = ['FlatConfig', 'answer', '42', 'name', '"flat example"',
                  'Close']
"""Widget texts that both the stubbed and the real Tk test expect."""


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

    def winfo_toplevel(self) -> 'FakeWidget':
        """Return this widget, standing in for the enclosing window."""
        return self

    def destroy(self) -> None:
        """Ignore window destruction, which the stubbed tests do not need."""


@pytest.fixture(name='stub_tk')
def fixture_stub_tk(monkeypatch: pytest.MonkeyPatch) -> Iterator[None]:
    """Replace the Tkinter widget classes with recording stubs."""
    FakeWidget.created.clear()
    for widget_name in ('Frame', 'Label', 'Button'):
        monkeypatch.setattr(tkinter, widget_name, FakeWidget)
    yield
    FakeWidget.created.clear()


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


def test_stub_widget_texts(stub_tk: None) -> None:
    """Test the stubbed widgets show the class name, the rows and a button."""
    _ = stub_tk
    build_editor_widgets(parent=cast(tkinter.Misc, FakeWidget()),
                         model=EditModel(FlatConfig()))
    assert _stub_texts() == EXPECTED_TEXTS


def test_real_widget_texts(root_or_skip: tkinter.Tk) -> None:
    """Test real Tk widgets show exactly what the stubbed test expects."""
    build_editor_widgets(parent=root_or_skip, model=EditModel(FlatConfig()))
    assert _real_texts(root_or_skip) == EXPECTED_TEXTS


def test_stub_row_frames(stub_tk: None) -> None:
    """Test each row gets a frame of its own below the given parent."""
    _ = stub_tk
    root = FakeWidget()
    model = EditModel(FlatConfig())
    build_editor_widgets(parent=cast(tkinter.Misc, root), model=model)
    frames = [widget for widget in FakeWidget.created
              if widget is not root and 'text' not in widget.options]
    assert len(frames) == len(model.rows)
    assert all(frame.parent is root for frame in frames)
    value_parents = [widget.parent for widget in FakeWidget.created
                     if widget.options.get('text') in ('42',
                                                       '"flat example"')]
    assert value_parents == frames


def test_is_editor_backend() -> None:
    """Test TkEditor can be used where an EditorBackend is expected."""
    backend: EditorBackend = TkEditor()
    assert hasattr(backend, 'run_editor')
