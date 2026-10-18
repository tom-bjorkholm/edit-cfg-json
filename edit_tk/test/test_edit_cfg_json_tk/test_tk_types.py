#! /usr/bin/env python3
"""Tests for the column of the types in the Tkinter backend.

Every row says the type it holds between its name and its value, in a
pull-down that nothing can be chosen in yet. What a row holds and how the
column is spelled are the core's; what is tested here is that this backend
shows what the core says, on every row and in one column. Both are asserted
the stubbed way and the real way, because a stub can drift from what Tk really
does.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import tkinter
from edit_cfg_json import EditModel, row_type_text, row_type_texts, \
    type_column_width
from edit_cfg_json_tk.tk_editor import EditorWidgets
from example.e18_declared_types import ReportConfig
from example.e19_omitted_members import ReportConfig as OmittedReport
from .helpers import TwoTypesConfig, real_fields, real_types, retype, \
    stub_choices, stub_editor, stub_types
from .stubs import FakeVar


def _report() -> EditModel:
    """Return a model of the example that is about declared types."""
    return EditModel(ReportConfig())


def test_stub_every_row(stub_tk: None) -> None:
    """Test every row has a pull-down of its types, saying the one it holds.

    They are all as wide as the column, so that the values beside them begin
    in one place, and none of them can be opened yet.
    """
    _ = stub_tk
    model = _report()
    stub_editor(model)
    found = stub_types()
    assert [widget.options['text'] for widget in found] == [
        row_type_text(row) for row in model.rows]
    assert {widget.options['width'] for widget in found} == {
        type_column_width(model)}
    assert {widget.options['state'] for widget in found} == {'disabled'}


def test_stub_types_listed(stub_tk: None) -> None:
    """Test the pull-down of a row lists every type it may hold."""
    _ = stub_tk
    model = _report()
    stub_editor(model)
    assert [stub_choices(widget) for widget in stub_types()] == [
        row_type_texts(row) for row in model.rows]


def test_real_every_row(root_or_skip: tkinter.Tk) -> None:
    """Test real Tk shows exactly the same types, as wide and as inactive."""
    model = _report()
    EditorWidgets(parent=root_or_skip, model=model)
    found = real_types(root_or_skip)
    assert [str(widget.cget('text')) for widget in found] == [
        row_type_text(row) for row in model.rows]
    assert {int(widget.cget('width')) for widget in found} == {
        type_column_width(model)}
    assert {str(widget.cget('state')) for widget in found} == {'disabled'}


def test_real_types_listed(root_or_skip: tkinter.Tk) -> None:
    """Test the menu of a real pull-down lists every type its row may hold.

    `subtitle` is declared `Optional[str]` and holds nothing, so it shows
    `None` and lists both.
    """
    model = _report()
    EditorWidgets(parent=root_or_skip, model=model)
    subtitle = real_types(root_or_skip)[1]
    menu = root_or_skip.nametowidget(str(subtitle.cget('menu')))
    assert isinstance(menu, tkinter.Menu)
    listed = [menu.entrycget(index, 'label') for index in range(2)]
    assert (str(subtitle.cget('text')), listed) == ('None', ['str', 'None'])


def test_stub_type_follows(stub_tk: None) -> None:
    """Test the type shown follows what a value typed into the row is.

    The member may hold a number or a text, so a text that is no number is a
    value of the other type, and the column says so without the row being
    made again.
    """
    _ = stub_tk
    stub_editor(EditModel(TwoTypesConfig()))
    FakeVar.created[0].set('five')
    assert stub_types()[0].options['text'] == 'str'
    FakeVar.created[0].set('6')
    assert stub_types()[0].options['text'] == 'int'


def test_real_type_follows(root_or_skip: tkinter.Tk) -> None:
    """Test real Tk follows the typed value in exactly the same way."""
    EditorWidgets(parent=root_or_skip, model=EditModel(TwoTypesConfig()))
    retype(real_fields(root_or_skip)[0], 'five')
    assert str(real_types(root_or_skip)[0].cget('text')) == 'str'


def test_real_offer_follows(root_or_skip: tkinter.Tk) -> None:
    """Test a row whose type only its value says offers what it holds now.

    `legacy` has no annotation and holds nothing, so it offers `None`; a text
    typed into it is a text, and the menu says so as well as the button.
    """
    EditorWidgets(parent=root_or_skip, model=EditModel(OmittedReport()))
    legacy = real_types(root_or_skip)[-1]
    assert str(legacy.cget('text')) == 'None'
    retype(real_fields(root_or_skip)[-1], 'kept')
    menu = root_or_skip.nametowidget(str(legacy.cget('menu')))
    assert isinstance(menu, tkinter.Menu)
    assert (str(legacy.cget('text')), menu.entrycget(0, 'label'),
            menu.index('end')) == ('str', 'str', 0)
