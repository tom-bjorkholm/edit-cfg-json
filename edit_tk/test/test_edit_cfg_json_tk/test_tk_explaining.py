#! /usr/bin/env python3
"""Tests for the explanatory text of the Tkinter backend.

What is asserted is mostly the whole list of widget texts rather than the one
that was added, because that is also how a member the application says nothing
about is shown to have no description and no empty label in place of one.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import tkinter
import pytest
from edit_cfg_json import EditModel
from edit_cfg_json_tk.tk_editor import EditorWidgets, EXPLAIN_TEXT
from example.e01_flat_config import FlatConfig
from .helpers import DESCRIBED_LABELS, DESCRIPTIONS, FakeFlag, \
    FLAT_DOCSTRING, FLAT_SUMMARY, HIDDEN_LABELS, NoDocConfig, real_press, \
    real_texts, real_ticks, stub_editor, stub_keys, stub_press, stub_texts


def _described_stub() -> EditorWidgets:
    """Build the stubbed widgets of a model whose one member is described."""
    return stub_editor(EditModel(FlatConfig(), descriptions=DESCRIPTIONS))


def _described_real(parent: tkinter.Misc) -> EditorWidgets:
    """Build the real widgets of a model whose one member is described."""
    return EditorWidgets(parent=parent,
                         model=EditModel(FlatConfig(),
                                         descriptions=DESCRIPTIONS))


def test_stub_described_texts(stub_tk: None) -> None:
    """Test a described member is shown with its description below it.

    The whole list of texts is asserted rather than the one that was added,
    because it is also how the member the application said nothing about is
    shown to have no description and no empty label in place of one.
    """
    _ = stub_tk
    widgets = _described_stub()
    assert stub_texts(packed_only=True) == DESCRIBED_LABELS
    assert widgets.docstring_shown == FLAT_DOCSTRING


def test_real_described_texts(root_or_skip: tkinter.Tk) -> None:
    """Test real Tk shows exactly what the stubbed test expects."""
    widgets = _described_real(root_or_skip)
    assert real_texts(root_or_skip, packed_only=True) == DESCRIBED_LABELS
    assert widgets.docstring_shown == FLAT_DOCSTRING


def test_stub_explain_hides(stub_tk: None) -> None:
    """Test the Explain button takes the explanations away and back.

    A description leaves the layout rather than being emptied, because an
    empty label would still take the height of a line and would have hidden
    nothing at all.
    """
    _ = stub_tk
    _described_stub()
    stub_press(EXPLAIN_TEXT)
    assert stub_texts(packed_only=True) == HIDDEN_LABELS
    stub_press(EXPLAIN_TEXT)
    assert stub_texts(packed_only=True) == DESCRIBED_LABELS


def test_real_explain_hides(root_or_skip: tkinter.Tk) -> None:
    """Test the real Explain button hides and shows exactly the same."""
    _described_real(root_or_skip)
    real_press(root_or_skip, EXPLAIN_TEXT)
    assert real_texts(root_or_skip, packed_only=True) == HIDDEN_LABELS
    real_press(root_or_skip, EXPLAIN_TEXT)
    assert real_texts(root_or_skip, packed_only=True) == DESCRIBED_LABELS


@pytest.mark.parametrize('sequence', ['<F1>', '<Control-g>'])
def test_stub_explain_key(stub_tk: None, sequence: str) -> None:
    """Test either key of the explain action does what its button does."""
    _ = stub_tk
    _described_stub()
    assert stub_keys()[sequence]() == 'break'
    assert stub_texts(packed_only=True) == HIDDEN_LABELS


def test_stub_hidden_at_start(stub_tk: None) -> None:
    """Test a model that was told to hide them opens with them hidden.

    Which of the two states the editor is in belongs to the model, so a model
    that reached this backend already toggled has to be honoured rather than
    overruled.
    """
    _ = stub_tk
    model = EditModel(FlatConfig(), descriptions=DESCRIPTIONS)
    model.toggle_explanations()
    stub_editor(model)
    assert stub_texts(packed_only=True) == HIDDEN_LABELS


def test_stub_no_docstring(stub_tk: None) -> None:
    """Test a configuration class with no docstring gets no widget for one."""
    _ = stub_tk
    widgets = stub_editor(EditModel(NoDocConfig()))
    assert widgets.docstring_shown == ''
    assert FLAT_SUMMARY not in stub_texts()


def test_real_no_docstring(root_or_skip: tkinter.Tk) -> None:
    """Test real Tk leaves out exactly the same widget."""
    widgets = EditorWidgets(parent=root_or_skip,
                            model=EditModel(NoDocConfig()))
    assert widgets.docstring_shown == ''
    assert FLAT_SUMMARY not in real_texts(root_or_skip)


def test_stub_tick_follows(stub_tk: None) -> None:
    """Test the tick-box says which of the two states the editor is in.

    A button would have had to be called Explain in both states, and beside
    explanations that are already there that reads as an offer to do
    something that has been done.
    """
    _ = stub_tk
    _described_stub()
    assert len(FakeFlag.created) == 1
    tick = FakeFlag.created[0]
    assert tick.get()
    stub_press(EXPLAIN_TEXT)
    assert not tick.get()
    stub_press(EXPLAIN_TEXT)
    assert tick.get()


def test_stub_tick_after_key(stub_tk: None) -> None:
    """Test the key of the explain action moves the tick as well.

    Tk flips the tick itself only when it was the tick-box that was pressed,
    so a tick that was left to Tk would disagree with the window as soon as
    the key was used.
    """
    _ = stub_tk
    _described_stub()
    stub_keys()['<F1>']()
    assert not FakeFlag.created[0].get()
    assert stub_texts(packed_only=True) == HIDDEN_LABELS


def test_real_tick_follows(root_or_skip: tkinter.Tk) -> None:
    """Test the real tick-box is ticked while the explanations are shown."""
    _described_real(root_or_skip)
    assert real_ticks(root_or_skip) == [True]
    real_press(root_or_skip, EXPLAIN_TEXT)
    assert real_ticks(root_or_skip) == [False]
    real_press(root_or_skip, EXPLAIN_TEXT)
    assert real_ticks(root_or_skip) == [True]
