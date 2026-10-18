#! /usr/bin/env python3
"""Tests for the column of the types in the Tkinter backend.

Every row says the type it holds between its name and its value, in a
pull-down that is active where the type is the user's to choose. What a row
holds, how the column is spelled and what choosing a type does are the core's;
what is tested here is that this backend shows what the core says, on every
row and in one column, and that picking a type in the pull-down is what
chooses it. Both are asserted the stubbed way and the real way, because a stub
can drift from what Tk really does.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from collections.abc import Callable
import operator
import tkinter
from config_as_json import ConfigPath
from edit_cfg_json import EditModel, row_chooses_type, row_type_text, \
    row_type_texts, type_column_widths
from edit_cfg_json_tk.tk_editor import EditorWidgets
from edit_cfg_json_tk.tk_elements import ADD_TEXT
from edit_cfg_json_tk.tk_look import BLANK_WIDTH, TREE_INDENT, row_font
from example.e11_add_remove import PipelineConfig
from example.e18_declared_types import ReportConfig
from example.e19_omitted_members import ReportConfig as OmittedReport
from example.e20_union_types import ExportConfig
from .helpers import TwoTypesConfig, model_value, real_fields, real_types, \
    retype, stub_choices, stub_editor, stub_field_widgets, stub_pick, \
    stub_type_of, stub_types
from .stubs import FakeVar

SUBTITLE: ConfigPath = ('subtitle',)
"""The member of the example declared `Optional[str]` and holding nothing."""

FOOTER: ConfigPath = ('footer',)
"""The member of the example declared `Optional[str]` and holding a value."""

HOSTS: ConfigPath = ('extra_hosts',)
"""The member of example 19 declared `Optional[list[str]]`."""

AUDIT: ConfigPath = ('audit',)
"""The member of example 11 declared to hold one `StageConfig` or none."""


def _report() -> EditModel:
    """Return a model of the example that is about declared types."""
    return EditModel(ReportConfig())


def _states(model: EditModel) -> list[str]:
    """Return the state that each pull-down of the types is to be in."""
    return ['normal' if row_chooses_type(row) else 'disabled'
            for row in model.rows]


def _widths(model: EditModel, measure: Callable[[str], int]) -> list[int]:
    """Return how wide each pull-down of the types is to be, in pixels.

    That is the width of its text, which is narrower the deeper the row is,
    and of the blank image that makes its width one in pixels.
    """
    widths = type_column_widths(model, measure=measure, indent=TREE_INDENT)
    return [width + BLANK_WIDTH for width in widths]


def test_stub_every_row(stub_tk: None) -> None:
    """Test every row has a pull-down of its types, saying the one it holds.

    Each is as wide as the core says in the font they are written in, which
    the stub measures one pixel per character, so that the column ends in one
    place and the values beside it begin in one place. Only those of a row
    whose type is the user's to choose can be opened.
    """
    _ = stub_tk
    model = _report()
    stub_editor(model)
    found = stub_types()
    assert [widget.options['text'] for widget in found] == [
        row_type_text(row) for row in model.rows]
    assert [widget.options['width'] for widget in found] == _widths(model, len)
    assert [widget.options['state'] for widget in found] == _states(model)
    assert 'normal' in _states(model) and 'disabled' in _states(model)


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
    font = row_font(root_or_skip)
    assert [int(widget.cget('width')) for widget in found] == _widths(
        model, font.measure)
    assert [str(widget.cget('state')) for widget in found] == _states(model)


def test_real_column_end(root_or_skip: tkinter.Tk) -> None:
    """Test the column of real Tk ends in one place, with no space to spare.

    The example of the complaint has a long type on its member and short ones
    inside it, and containers beside values at every depth. Every pull-down
    ends where the others do, as Tk lays the window out, which both the
    indentation and the control that folds a container decide: an empty
    space beside a value has to be exactly as wide as that control. A
    pull-down is never narrower than Tk makes it on its own, which is what
    width 0 asks for, and one of them is exactly that wide: Tk counts a width
    given in characters in widths of `0`, and the column it gave this example
    was nearly twice as wide as its longest type.
    """
    model = EditModel(ExportConfig())
    EditorWidgets(parent=root_or_skip, model=model)
    root_or_skip.update_idletasks()
    found = real_types(root_or_skip)
    ends = {widget.winfo_rootx() + widget.winfo_width() for widget in found}
    given = [widget.winfo_reqwidth() for widget in found]
    for widget in found:
        widget.config(width=0)
    natural = [widget.winfo_reqwidth() for widget in found]
    assert len(ends) == 1
    assert all(map(operator.ge, given, natural))
    assert any(map(operator.eq, given, natural))


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


def test_stub_typing_keeps(stub_tk: None) -> None:
    """Test typing into a row whose type is chosen leaves the type alone.

    The member may hold a number or a text, and which of the two is the
    user's choice: a text that is no number is a value of the wrong type.
    """
    _ = stub_tk
    stub_editor(EditModel(TwoTypesConfig()))
    FakeVar.created[0].set('five')
    assert stub_types()[0].options['text'] == 'int'


def test_real_typing_keeps(root_or_skip: tkinter.Tk) -> None:
    """Test real Tk leaves the type alone in exactly the same way."""
    EditorWidgets(parent=root_or_skip, model=EditModel(TwoTypesConfig()))
    retype(real_fields(root_or_skip)[0], 'five')
    assert str(real_types(root_or_skip)[0].cget('text')) == 'int'


def test_stub_type_picked(stub_tk: None) -> None:
    """Test picking a type in the pull-down is what chooses it.

    The number the member held is a text of the same digits afterwards, and
    the row is made again, saying the type chosen.
    """
    _ = stub_tk
    model = EditModel(TwoTypesConfig())
    stub_editor(model)
    stub_pick(stub_types()[0], 'str')
    assert model_value(model, 'count') == '5'
    assert stub_types()[0].options['text'] == 'str'


def test_real_type_picked(root_or_skip: tkinter.Tk) -> None:
    """Test picking a type in a real menu chooses it in the same way."""
    model = EditModel(TwoTypesConfig())
    EditorWidgets(parent=root_or_skip, model=model)
    menu = root_or_skip.nametowidget(
        str(real_types(root_or_skip)[0].cget('menu')))
    assert isinstance(menu, tkinter.Menu)
    menu.invoke(1)
    assert model_value(model, 'count') == '5'
    assert str(real_types(root_or_skip)[0].cget('text')) == 'str'


def test_stub_none_no_field(stub_tk: None) -> None:
    """Test a member holding nothing has no field and nothing to press.

    Its type says `None`, which is the whole of what is shown about it, and
    choosing a type is how it is given a value: there is no control at the
    end of its row.
    """
    _ = stub_tk
    model = _report()
    widgets = stub_editor(model)
    controls = dict(zip([row.path for row in model.rows],
                        widgets.element_texts, strict=True))
    assert controls[SUBTITLE] == [] and controls[FOOTER] == []
    assert len(stub_field_widgets()) == \
        len([row for row in model.rows if row.editable])


def test_stub_value_by_type(stub_tk: None) -> None:
    """Test choosing `str` gives a field, and choosing `None` takes one."""
    _ = stub_tk
    model = _report()
    stub_editor(model)
    before = len(stub_field_widgets())
    stub_pick(stub_type_of(model, SUBTITLE), 'str')
    assert model_value(model, 'subtitle') == ''
    assert len(stub_field_widgets()) == before + 1
    stub_pick(stub_type_of(model, FOOTER), 'None')
    assert model_value(model, 'footer') is None
    assert len(stub_field_widgets()) == before


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


def _controls(model: EditModel, widgets: EditorWidgets,
              path: ConfigPath) -> list[str]:
    """Return what the controls at the end of one row of one model say."""
    return dict(zip([row.path for row in model.rows], widgets.element_texts,
                    strict=True))[path]


def test_stub_list_by_type(stub_tk: None) -> None:
    """Test choosing a list gives the row a list, and `None` takes it away.

    The row is made again as a container, with the control that adds an
    element to it, and choosing `None` takes the list and that control away.
    """
    _ = stub_tk
    model = EditModel(OmittedReport())
    widgets = stub_editor(model)
    assert _controls(model, widgets, HOSTS) == []
    stub_pick(stub_type_of(model, HOSTS), 'list[str]')
    assert model_value(model, 'extra_hosts') == []
    assert _controls(model, widgets, HOSTS) == [ADD_TEXT]
    stub_pick(stub_type_of(model, HOSTS), 'None')
    assert model_value(model, 'extra_hosts') is None
    assert _controls(model, widgets, HOSTS) == []


def test_real_list_by_type(root_or_skip: tkinter.Tk) -> None:
    """Test choosing a list in a real menu makes the row a container."""
    model = EditModel(OmittedReport())
    widgets = EditorWidgets(parent=root_or_skip, model=model)
    index = [row.path for row in model.rows].index(HOSTS)
    menu = root_or_skip.nametowidget(
        str(real_types(root_or_skip)[index].cget('menu')))
    assert isinstance(menu, tkinter.Menu)
    assert menu.entrycget(0, 'label') == 'list[str]'
    menu.invoke(0)
    assert model_value(model, 'extra_hosts') == []
    assert str(real_types(root_or_skip)[index].cget('text')) == 'list[str]'
    assert _controls(model, widgets, HOSTS) == [ADD_TEXT]


def test_stub_object_by_type(stub_tk: None) -> None:
    """Test choosing a class gives the row an object, and `None` takes it.

    The rows of the object appear below the row, and choosing `None` takes
    them away again; neither has a control at the end of the row.
    """
    _ = stub_tk
    model = EditModel(PipelineConfig())
    widgets = stub_editor(model)
    stub_pick(stub_type_of(model, AUDIT), 'StageConfig')
    assert (*AUDIT, 'name') in [row.path for row in model.rows]
    assert _controls(model, widgets, AUDIT) == []
    stub_pick(stub_type_of(model, AUDIT), 'None')
    assert model_value(model, 'audit') is None
    assert (*AUDIT, 'name') not in [row.path for row in model.rows]


def test_real_object_by_type(root_or_skip: tkinter.Tk) -> None:
    """Test choosing a class in a real menu gives the row an object."""
    model = EditModel(PipelineConfig())
    EditorWidgets(parent=root_or_skip, model=model)
    index = [row.path for row in model.rows].index(AUDIT)
    menu = root_or_skip.nametowidget(
        str(real_types(root_or_skip)[index].cget('menu')))
    assert isinstance(menu, tkinter.Menu)
    assert menu.entrycget(0, 'label') == 'StageConfig'
    menu.invoke(0)
    assert (*AUDIT, 'name') in [row.path for row in model.rows]
    assert str(real_types(root_or_skip)[index].cget('text')) == 'StageConfig'
