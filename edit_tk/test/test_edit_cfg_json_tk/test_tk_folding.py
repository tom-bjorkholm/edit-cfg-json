#! /usr/bin/env python3
"""Tests for the tree of rows and the folding of the Tkinter backend.

The stubbed and the real Tk way of asking the same question are side by side
here as everywhere else in this backend, because the two fail in opposite
directions: a stub drifts from what Tk really does, and real Tk hides a wrong
value behind a widget default.

The configuration classes come from the example rather than from classes of
their own, so that the same containers are used by the core tests, by both
backends and by the example itself.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import tkinter
from edit_cfg_json import EditModel
from edit_cfg_json_tk.tk_editor import EditorWidgets, FOLD_ALL_TEXT, \
    FOLD_OPEN_TEXT, FOLD_SHUT_TEXT, OPEN_ALL_TEXT, VALIDATE_TEXT
from edit_cfg_json_tk.tk_look import PADDING, TREE_INDENT
from example.e01_flat_config import FlatConfig
from example.e08_lists_and_dicts import ContainerConfig
from .helpers import FakeVar, FakeWidget, real_buttons, real_press, \
    real_texts, stub_editor, stub_press, stub_texts, stub_window

MANY_LABELS = 'many_labels'
"""The member of the example that the editor opens folded."""

PORTS = 'ports'
"""A member of the example that holds a dict of two values."""

FOLD_KEY = '<F2>'
"""What Tk calls the first key that the fold action is given."""


def _tree_stub() -> EditorWidgets:
    """Build the stubbed widgets of the example with the containers."""
    return stub_editor(EditModel(ContainerConfig()))


def _tree_real(parent: tkinter.Misc) -> EditorWidgets:
    """Build the real widgets of the example with the containers."""
    return EditorWidgets(parent=parent, model=EditModel(ContainerConfig()))


def test_stub_shows_the_tree(stub_tk: None) -> None:
    """Test a value inside a container is a row of its own."""
    _ = stub_tk
    _tree_stub()
    shown = stub_texts(packed_only=True)
    assert 'retry_delays' in shown
    assert '2 elements' in shown
    assert shown.count('0') > 1


def test_real_shows_the_tree(root_or_skip: tkinter.Tk) -> None:
    """Test real Tk shows exactly what the stubbed test expects."""
    _tree_real(root_or_skip)
    shown = real_texts(root_or_skip, packed_only=True)
    assert 'retry_delays' in shown
    assert '2 elements' in shown


def test_stub_indents_a_value(stub_tk: None) -> None:
    """Test a value inside a container is indented once for that container.

    The whole node is indented and not only its name, so that a name inside a
    container is never cut off by the column that the names share.
    """
    _ = stub_tk
    widgets = _tree_stub()
    padding = [widget.packing.get('padx') for widget in FakeWidget.created
               if widget.packed and 'padx' in widget.packing]
    assert (PADDING, PADDING) in padding
    assert (PADDING + TREE_INDENT, PADDING) in padding
    assert widgets.label_text == 'ContainerConfig'


def test_stub_folds_one(stub_tk: None) -> None:
    """Test the control of one container hides the rows below it."""
    _ = stub_tk
    _tree_stub()
    before = stub_texts(packed_only=True)
    _press_stub_fold()
    after = stub_texts(packed_only=True)
    assert PORTS in after
    assert len(after) < len(before)
    assert FOLD_SHUT_TEXT in after


def test_stub_opens_again(stub_tk: None) -> None:
    """Test the same control opens the container it folded away."""
    _ = stub_tk
    _tree_stub()
    before = stub_texts(packed_only=True)
    _press_stub_fold()
    _press_stub_fold(FOLD_SHUT_TEXT)
    assert stub_texts(packed_only=True) == before


def test_stub_long_folded(stub_tk: None) -> None:
    """Test the long list of the example opens folded and says so."""
    _ = stub_tk
    _tree_stub()
    shown = stub_texts(packed_only=True)
    assert MANY_LABELS in shown
    assert '11' not in shown
    assert shown.count(FOLD_SHUT_TEXT) == 1


def test_stub_fold_all(stub_tk: None) -> None:
    """Test the button folds every container and then opens every one.

    Opening every one of them shows more than the editor opened with, because
    the long list of the example started folded.
    """
    _ = stub_tk
    _tree_stub()
    stub_press(FOLD_ALL_TEXT)
    folded = stub_texts(packed_only=True)
    assert 'http' not in folded
    assert OPEN_ALL_TEXT in folded
    stub_press(OPEN_ALL_TEXT)
    opened = stub_texts(packed_only=True)
    assert 'http' in opened
    # The name of the last element of the long list, which no other
    # container of the example is long enough to have.
    assert '11' in opened


def test_stub_fold_key(stub_tk: None) -> None:
    """Test the key of the fold action does what the button does."""
    _ = stub_tk
    _tree_stub()
    stub_window().bindings[FOLD_KEY]()
    assert 'http' not in stub_texts(packed_only=True)


def test_stub_no_fold_button(stub_tk: None) -> None:
    """Test a configuration with nothing to fold is offered no folding.

    A button that could never do anything would be offering something that
    is not there, and the column of the controls would be width taken from
    the values for nothing.
    """
    _ = stub_tk
    stub_editor(EditModel(FlatConfig()))
    shown = stub_texts()
    assert FOLD_ALL_TEXT not in shown
    assert FOLD_OPEN_TEXT not in shown
    assert FOLD_KEY not in stub_window().bindings


def test_stub_rows_rebuilt(stub_tk: None) -> None:
    """Test the rows are made again when a pass leaves the model with others.

    The de-duplicating validator of the example removes a value, so the row
    that held it has to go: a backend that wrote into the widgets it had
    would be showing a value that is not in the buffer any more.
    """
    _ = stub_tk
    widgets = _tree_stub()
    _set_field('html', 'json')
    stub_press(VALIDATE_TEXT)
    shown = stub_texts(packed_only=True)
    assert '1 element' in shown
    assert widgets.verdict_text_shown == 'validation: valid'


def test_real_fold_and_open(root_or_skip: tkinter.Tk) -> None:
    """Test real Tk folds one container away and opens it again."""
    _tree_real(root_or_skip)
    before = real_texts(root_or_skip, packed_only=True)
    _press_real_fold(root_or_skip)
    folded = real_texts(root_or_skip, packed_only=True)
    assert len(folded) < len(before)
    _press_real_fold(root_or_skip, FOLD_SHUT_TEXT)
    assert real_texts(root_or_skip, packed_only=True) == before


def test_real_fold_all(root_or_skip: tkinter.Tk) -> None:
    """Test real Tk folds every container and renames the button."""
    _tree_real(root_or_skip)
    real_press(root_or_skip, FOLD_ALL_TEXT)
    shown = real_texts(root_or_skip, packed_only=True)
    assert 'http' not in shown
    assert OPEN_ALL_TEXT in shown


def _press_stub_fold(text: str = FOLD_OPEN_TEXT) -> None:
    """Press the first stub fold control that shows one text.

    There is one per container, so the one to press is named by its place
    and not by its text: what a control says is what the next press does.

    Args:
        text: What that control shows now.
    """
    controls = [widget for widget in FakeWidget.created
                if widget.packed and widget.options.get('text') == text]
    assert controls
    controls[0].invoke()


def _press_real_fold(parent: tkinter.Misc, text: str = FOLD_OPEN_TEXT) -> None:
    """Press the first real Tk fold control that shows one text.

    Args:
        parent: Widget whose descendants are looked through.
        text: What that control shows now.
    """
    controls = [button for button in real_buttons(parent)
                if str(button.cget('text')) == text]
    assert controls
    controls[0].invoke()


def _set_field(was: str, becomes: str) -> None:
    """Type one text into the one stub field that holds another.

    Args:
        was: Text that the field holds now.
        becomes: Text to type into it.
    """
    fields = [field for field in FakeVar.created if field.get() == was]
    assert len(fields) == 1
    fields[0].set(becomes)
