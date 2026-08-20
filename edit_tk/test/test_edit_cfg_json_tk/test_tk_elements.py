#! /usr/bin/env python3
"""Tests for the controls that change how many elements a node holds.

The stubbed and the real Tk way of asking the same question are side by side
here as everywhere else in this backend, because the two fail in opposite
directions: a stub drifts from what Tk really does, and real Tk hides a wrong
value behind a widget default.

The configuration class comes from the example rather than from one of its
own, so that the same containers are used by the core tests, by both backends
and by the example itself.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from typing import NamedTuple, Optional
import tkinter
from tkinter import simpledialog
import pytest
from config_as_json import ConfigPath
from edit_cfg_json import EditModel
from edit_cfg_json_tk.tk_editor import EditorWidgets, VALIDATE_TEXT
from edit_cfg_json_tk.tk_elements import ADD_TEXT, EARLIER_TEXT, LATER_TEXT, \
    REMOVE_TEXT
from example.e11_add_remove import PipelineConfig
from example.e18_declared_types import ReportConfig
from .helpers import FakeWidget, real_buttons, real_fields, \
    real_press, retype, stub_editor, stub_field_widgets

NEW_KEY = 'nightly'
"""Key that the stubbed question about a new entry answers with."""

STAGES: ConfigPath = ('stages',)
"""The member of the example that holds a list of configuration objects."""

RUNNERS: ConfigPath = ('runners',)
"""The member of it that holds a dict of them, keyed by a name."""


class Editor(NamedTuple):
    """One editor of the example, and the model it is showing."""

    widgets: EditorWidgets
    """The widgets that were built."""

    model: EditModel
    """The model they were built from, which is what a press changes."""


def _pipeline_stub() -> Editor:
    """Build the stubbed widgets of the example with every container."""
    model = EditModel(PipelineConfig())
    return Editor(widgets=stub_editor(model), model=model)


def _value_of(editor: Editor, path: ConfigPath) -> object:
    """Return what one node of the model of one editor holds now."""
    return {row.path: row.value_text for row in editor.model.rows}[path]


def _controls_of(editor: Editor, path: ConfigPath) -> list[str]:
    """Return what the controls of one node of one editor say."""
    shown = dict(zip([row.path for row in editor.model.rows],
                     editor.widgets.element_texts, strict=True))
    return shown[path]


def _place_of(editor: Editor, path: ConfigPath, text: str) -> int:
    """Return which of the controls saying one text belongs to one node.

    The controls are created in row order, so counting the nodes before this
    one that offer the same action is what says which of them it is.

    Args:
        editor: Editor whose controls are counted.
        path: Path of the node whose control is wanted.
        text: What that control says.

    Returns:
        The place of that control among the ones that say the same thing.
    """
    offering = [row.path for row in editor.model.rows
                if text in _controls_of(editor, row.path)]
    return offering.index(path)


def _press(text: str, place: int = 0) -> None:
    """Press one of the stub controls that show one text.

    There is one per node that offers that action, so the one to press is
    named by its place among them: what a control says is what it does, so
    several of them say the same thing.

    Args:
        text: What that control shows.
        place: Which of the controls showing it to press.
    """
    controls = [widget for widget in FakeWidget.created
                if widget.shown and widget.options.get('text') == text]
    assert len(controls) > place
    controls[place].invoke()


def _answer_key(monkeypatch: pytest.MonkeyPatch, named: Optional[str]) -> None:
    """Make the question about a new dict entry answer with one name.

    Args:
        monkeypatch: The pytest fixture that replaces the dialog.
        named: What the question is answered with, or None for a question
            that was left unanswered.
    """
    monkeypatch.setattr(simpledialog, 'askstring', lambda *args, **kw: named)


def test_stub_offers_controls(stub_tk: None) -> None:
    """Test a list that can grow has the controls its offer names.

    Its first element cannot move up, because there is nothing in front of it
    to change places with, so the control that would do that is not there.
    """
    _ = stub_tk
    editor = _pipeline_stub()
    assert _controls_of(editor, STAGES) == [ADD_TEXT]
    assert _controls_of(editor, (*STAGES, '0')) == [REMOVE_TEXT, LATER_TEXT]
    assert _controls_of(editor, (*STAGES, '1')) == [REMOVE_TEXT, EARLIER_TEXT]


def test_stub_offers_nothing(stub_tk: None) -> None:
    """Test the dicts that cannot grow have no controls at all.

    Nothing is half-supported: such a dict gets no control rather than one
    that refuses every press.
    """
    _ = stub_tk
    editor = _pipeline_stub()
    for path in [('limits',), ('limits', 'cpu'), ('labels',), ('hooks',)]:
        assert _controls_of(editor, path) == []


def test_stub_adds_an_element(stub_tk: None) -> None:
    """Test pressing the control of a list puts one more element in it."""
    _ = stub_tk
    editor = _pipeline_stub()
    _press(ADD_TEXT, place=_place_of(editor, STAGES, ADD_TEXT))
    assert _value_of(editor, STAGES) == '3 elements'


def test_stub_removes_element(stub_tk: None) -> None:
    """Test pressing the control of an element takes it out of the list."""
    _ = stub_tk
    editor = _pipeline_stub()
    _press(REMOVE_TEXT, place=_place_of(editor, (*STAGES, '0'), REMOVE_TEXT))
    assert _value_of(editor, STAGES) == '1 element'


def test_stub_moves_element(stub_tk: None) -> None:
    """Test pressing the control of an element changes its place."""
    _ = stub_tk
    editor = _pipeline_stub()
    _press(LATER_TEXT, place=_place_of(editor, (*STAGES, '0'), LATER_TEXT))
    assert _value_of(editor, (*STAGES, '0', 'name')) == 'test'


def test_stub_asks_a_key(stub_tk: None,
                         monkeypatch: pytest.MonkeyPatch) -> None:
    """Test a dict of objects is given the entry the question named."""
    _ = stub_tk
    _answer_key(monkeypatch, NEW_KEY)
    editor = _pipeline_stub()
    _press(ADD_TEXT, place=_place_of(editor, RUNNERS, ADD_TEXT))
    assert (*RUNNERS, NEW_KEY) in [row.path for row in editor.model.rows]


def test_stub_key_unanswered(stub_tk: None,
                             monkeypatch: pytest.MonkeyPatch) -> None:
    """Test a question about a new entry that is unanswered adds none."""
    _ = stub_tk
    _answer_key(monkeypatch, None)
    editor = _pipeline_stub()
    before = len(editor.model.rows)
    _press(ADD_TEXT, place=_place_of(editor, RUNNERS, ADD_TEXT))
    assert len(editor.model.rows) == before


def test_real_has_controls(root_or_skip: tkinter.Tk) -> None:
    """Test real Tk creates the same controls as the stub reports."""
    EditorWidgets(parent=root_or_skip, model=EditModel(PipelineConfig()))
    texts = [str(button.cget('text')) for button in real_buttons(root_or_skip)]
    assert ADD_TEXT in texts
    assert REMOVE_TEXT in texts
    assert LATER_TEXT in texts


def test_real_adds_an_element(root_or_skip: tkinter.Tk) -> None:
    """Test pressing a real control puts one more element into the list."""
    model = EditModel(PipelineConfig())
    EditorWidgets(parent=root_or_skip, model=model)
    added = [button for button in real_buttons(root_or_skip)
             if str(button.cget('text')) == ADD_TEXT]
    added[0].invoke()
    assert {row.path: row.value_text for row in model.rows}[STAGES] == \
        '3 elements'


NOTHING_HELD: ConfigPath = ('subtitle',)
"""The member of the other example that holds nothing to begin with."""

CLEARED: ConfigPath = ('footer',)
"""The member of it that a validation pass can move to holding nothing.

A member validator returns the value that is stored back into the member, so
one of them can take a field away from a row that had one. It is the one thing
a backend has to make its widgets again for beyond a pass that changed how
many rows there are.
"""


def _report_stub() -> Editor:
    """Build the stubbed widgets of the example with the two states."""
    model = EditModel(ReportConfig())
    return Editor(widgets=stub_editor(model), model=model)


def test_stub_nothing_adds(stub_tk: None) -> None:
    """Test a member holding nothing has an add control and no field."""
    _ = stub_tk
    editor = _report_stub()
    assert _controls_of(editor, NOTHING_HELD) == [ADD_TEXT]
    assert _value_of(editor, NOTHING_HELD) == 'no value'
    assert len(stub_field_widgets()) == \
        len([row for row in editor.model.rows if row.editable])


def test_stub_value_removes(stub_tk: None) -> None:
    """Test a member holding a value offers being put back to nothing."""
    _ = stub_tk
    editor = _report_stub()
    assert _controls_of(editor, CLEARED) == [REMOVE_TEXT]


def test_stub_add_gives(stub_tk: None) -> None:
    """Test pressing the control gives that member the value of its kind."""
    _ = stub_tk
    editor = _report_stub()
    _press(ADD_TEXT, place=_place_of(editor, NOTHING_HELD, ADD_TEXT))
    assert _value_of(editor, NOTHING_HELD) == ''


def test_stub_pass_clears(stub_tk: None) -> None:
    """Test the widgets are made again when a pass takes a field away.

    The paths are the same before and after, so a backend that compared only
    those would leave a field on the screen for a member holding nothing, and
    the next key typed into it would be refused.
    """
    _ = stub_tk
    editor = _report_stub()
    before = len(stub_field_widgets())
    editor.model.set_text(CLEARED, '')
    _press(VALIDATE_TEXT)
    assert _value_of(editor, CLEARED) == 'no value'
    assert len(stub_field_widgets()) == before - 1


def test_real_pass_clears(root_or_skip: tkinter.Tk) -> None:
    """Test real Tk makes the widgets again for the same reason.

    The fields are the editable rows and not all of them, so the field of
    this member is found by counting the editable rows before it.
    """
    model = EditModel(ReportConfig())
    EditorWidgets(parent=root_or_skip, model=model)
    before = len(real_fields(root_or_skip))
    typed = [row.path for row in model.rows if row.editable]
    retype(real_fields(root_or_skip)[typed.index(CLEARED)], '')
    real_press(root_or_skip, VALIDATE_TEXT)
    assert len(real_fields(root_or_skip)) == before - 1
