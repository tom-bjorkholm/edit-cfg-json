#! /usr/bin/env python3
"""Tests for the widgets of the Tkinter backend and for editing in them.

Every test here has a stubbed form and a real Tk form, for the reason given in
`helpers`: the two fail in opposite directions.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import tkinter
from typing import cast
from edit_cfg_json import EditModel, EditorBackend
from edit_cfg_json_tk import TkEditor
from edit_cfg_json_tk.tk_editor import EditorWidgets, VALIDATE_TEXT
from example.e01_flat_config import FlatConfig
from .helpers import EXPECTED_FIELDS, EXPECTED_LABELS, EXPECTED_LOADED, \
    FakeVar, FakeWidget, FILLED_REPORT, model_value, real_fields, \
    real_press, real_texts, retype, REWRITTEN_MARK, stub_editor, stub_press, \
    stub_texts, UNKNOWN_VERDICT, VALID_VERDICT


def test_stub_widget_texts(stub_tk: None) -> None:
    """Test the stubbed widgets show the class name, the names and buttons."""
    _ = stub_tk
    stub_editor(EditModel(FlatConfig()))
    assert stub_texts() == EXPECTED_LABELS


def test_real_widget_texts(root_or_skip: tkinter.Tk) -> None:
    """Test real Tk widgets show exactly what the stubbed test expects."""
    widgets = EditorWidgets(parent=root_or_skip, model=EditModel(FlatConfig()))
    assert widgets.label_text == EXPECTED_LABELS[0]
    assert real_texts(root_or_skip) == EXPECTED_LABELS


def test_stub_field_values(stub_tk: None) -> None:
    """Test the stubbed fields start with the values of the model."""
    _ = stub_tk
    stub_editor(EditModel(FlatConfig()))
    assert [field.get() for field in FakeVar.created] == EXPECTED_FIELDS


def test_real_field_values(root_or_skip: tkinter.Tk) -> None:
    """Test real Tk fields start with exactly the same values."""
    widgets = EditorWidgets(parent=root_or_skip, model=EditModel(FlatConfig()))
    assert widgets.label_text == EXPECTED_LABELS[0]
    assert [field.get() for field in
            real_fields(root_or_skip)] == EXPECTED_FIELDS


def below_root(widget: object, root: FakeWidget) -> bool:
    """Return whether one stub widget is inside the frames below one parent.

    A member owns two frames: one for the member, which holds the line that
    is edited and the description below it, and one for that line.

    Args:
        widget: Stub widget to look for.
        root: Parent that the editor was built below.

    Returns:
        Whether that widget is inside the frames of a member of that parent.
    """
    assert isinstance(widget, FakeWidget)
    member = widget.parent
    assert isinstance(member, FakeWidget)
    return member.parent is root


def test_stub_row_frames(stub_tk: None) -> None:
    """Test each row gets a frame of its own below the given parent."""
    _ = stub_tk
    root = FakeWidget()
    model = EditModel(FlatConfig())
    EditorWidgets(parent=cast(tkinter.Misc, root), model=model)
    fields = [widget for widget in FakeWidget.created
              if 'textvariable' in widget.options]
    assert len(fields) == len(model.rows)
    assert all(below_root(field.parent, root) for field in fields)


def test_stub_field_master(stub_tk: None) -> None:
    """Test each field variable is created in the interpreter of its row.

    A variable built without a master is created in the first Tcl
    interpreter of the process, which is the wrong one as soon as the editor
    is not the only Tk in the application.
    """
    _ = stub_tk
    root = FakeWidget()
    model = EditModel(FlatConfig())
    EditorWidgets(parent=cast(tkinter.Misc, root), model=model)
    assert FakeVar.created
    assert all(below_root(variable.master, root)
               for variable in FakeVar.created)


def test_real_second_root(root_or_skip: tkinter.Tk) -> None:
    """Test the fields work in a root that is not the first one made.

    This is what the stubbed test above stands for, seen in real Tk: with
    its variable in the wrong interpreter a field shows nothing, and typing
    into it never reaches the model. The fixture is what makes the root
    below the second one, and it is what skips this without a display.
    """
    _ = root_or_skip
    second = tkinter.Tk()
    second.withdraw()
    try:
        model = EditModel(FlatConfig())
        EditorWidgets(parent=second, model=model)
        assert [field.get()
                for field in real_fields(second)] == EXPECTED_FIELDS
        retype(real_fields(second)[1], '7')
        assert model_value(model, 'answer') == 7
    finally:
        second.destroy()


def test_stub_typing(stub_tk: None) -> None:
    """Test typing into a stubbed field changes the model and the label."""
    _ = stub_tk
    model = EditModel(FlatConfig())
    widgets = stub_editor(model)
    FakeVar.created[1].set('7')
    assert model_value(model, 'answer') == 7
    assert widgets.label_text == 'FlatConfig *'


def test_real_typing(root_or_skip: tkinter.Tk) -> None:
    """Test typing into a real Tk field changes the model and the label."""
    model = EditModel(FlatConfig())
    widgets = EditorWidgets(parent=root_or_skip, model=model)
    retype(real_fields(root_or_skip)[1], '7')
    assert model_value(model, 'answer') == 7
    assert widgets.label_text == 'FlatConfig *'


def test_real_typing_undone(root_or_skip: tkinter.Tk) -> None:
    """Test a field typed back to its own value leaves nothing to save."""
    model = EditModel(FlatConfig())
    widgets = EditorWidgets(parent=root_or_skip, model=model)
    field = real_fields(root_or_skip)[0]
    field.insert('end', ' and more')
    field.delete(len('Flat example'), 'end')
    assert not model.dirty
    assert widgets.label_text == 'FlatConfig'


def test_stub_accepts(stub_tk: None) -> None:
    """Test the stubbed Validate button reports an accepted buffer."""
    _ = stub_tk
    widgets = stub_editor(EditModel(FlatConfig()))
    stub_press(VALIDATE_TEXT)
    assert widgets.verdict_text_shown == VALID_VERDICT


def test_real_accepts(root_or_skip: tkinter.Tk) -> None:
    """Test the real Validate button reports exactly the same."""
    widgets = EditorWidgets(parent=root_or_skip, model=EditModel(FlatConfig()))
    real_press(root_or_skip, VALIDATE_TEXT)
    assert widgets.verdict_text_shown == VALID_VERDICT


def test_stub_refuses(stub_tk: None) -> None:
    """Test the stubbed editor shows why the application refused a value."""
    _ = stub_tk
    widgets = stub_editor(EditModel(FlatConfig()))
    FakeVar.created[1].set('500')
    stub_press(VALIDATE_TEXT)
    assert 'validation: invalid' in widgets.verdict_text_shown
    assert 'greater than maximum 100' in widgets.verdict_text_shown


def test_real_refuses(root_or_skip: tkinter.Tk) -> None:
    """Test the real editor shows the same refusal."""
    widgets = EditorWidgets(parent=root_or_skip, model=EditModel(FlatConfig()))
    retype(real_fields(root_or_skip)[1], '500')
    real_press(root_or_skip, VALIDATE_TEXT)
    assert 'validation: invalid' in widgets.verdict_text_shown
    assert 'greater than maximum 100' in widgets.verdict_text_shown


def test_stub_rewrites(stub_tk: None) -> None:
    """Test a value a validator rewrote reaches the stubbed field and mark."""
    _ = stub_tk
    model = EditModel(FlatConfig())
    widgets = stub_editor(model)
    FakeVar.created[0].set('other')
    stub_press(VALIDATE_TEXT)
    assert FakeVar.created[0].get() == 'Other'
    assert model_value(model, 'name') == 'Other'
    assert REWRITTEN_MARK in stub_texts()
    assert widgets.verdict_text_shown == VALID_VERDICT


def test_real_rewrites(root_or_skip: tkinter.Tk) -> None:
    """Test the real field and mark show exactly the same rewrite."""
    model = EditModel(FlatConfig())
    widgets = EditorWidgets(parent=root_or_skip, model=model)
    retype(real_fields(root_or_skip)[0], 'other')
    real_press(root_or_skip, VALIDATE_TEXT)
    assert real_fields(root_or_skip)[0].get() == 'Other'
    assert model_value(model, 'name') == 'Other'
    assert REWRITTEN_MARK in real_texts(root_or_skip)
    assert widgets.verdict_text_shown == VALID_VERDICT


def test_stub_edit_after(stub_tk: None) -> None:
    """Test an edit puts the stubbed editor back to not having validated."""
    _ = stub_tk
    widgets = stub_editor(EditModel(FlatConfig()))
    stub_press(VALIDATE_TEXT)
    FakeVar.created[1].set('7')
    assert widgets.verdict_text_shown == UNKNOWN_VERDICT


def test_real_edit_after(root_or_skip: tkinter.Tk) -> None:
    """Test the real editor does the same after an edit."""
    widgets = EditorWidgets(parent=root_or_skip, model=EditModel(FlatConfig()))
    real_press(root_or_skip, VALIDATE_TEXT)
    retype(real_fields(root_or_skip)[1], '7')
    assert widgets.verdict_text_shown == UNKNOWN_VERDICT


def test_stub_load_message(stub_tk: None) -> None:
    """Test the stubbed editor shows what reading the input file did.

    The exact list of texts is asserted, so it also says that the message
    comes above the members it explains and that no widget was added for the
    member the file did hold.
    """
    _ = stub_tk
    stub_editor(EditModel(FlatConfig(), FILLED_REPORT))
    assert stub_texts() == EXPECTED_LOADED


def test_real_load_message(root_or_skip: tkinter.Tk) -> None:
    """Test the real Tk editor shows exactly the same about the load."""
    EditorWidgets(parent=root_or_skip,
                  model=EditModel(FlatConfig(), FILLED_REPORT))
    assert real_texts(root_or_skip) == EXPECTED_LOADED


def test_is_editor_backend() -> None:
    """Test TkEditor can be used where an EditorBackend is expected."""
    backend: EditorBackend = TkEditor()
    assert hasattr(backend, 'run_editor')
