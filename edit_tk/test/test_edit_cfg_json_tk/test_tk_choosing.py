#! /usr/bin/env python3
"""Tests for choosing a value in the Tkinter backend.

A member holding true or false and one holding an enum member have a
pull-down of the values they take beside the field they are typed into, and
exactly one of the two is on the window. Both are asserted the stubbed way
and the real way, because a stub can drift from what Tk really does and real
Tk can hide a wrong value behind a widget default.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from collections.abc import Callable
import tkinter
import pytest
from config_as_json import Config
from edit_cfg_json import EditModel, Settings
from edit_cfg_json_tk.tk_ask import REPLACED_TITLE
from edit_cfg_json_tk.tk_editor import CHOOSE_TEXT, EditorWidgets
from edit_cfg_json_tk.tk_look import MEMBER_CHOICE_NAME, MEMBER_FIELD_NAME
from example.e01_flat_config import FlatConfig
from example.e02_enum_config import EnumConfig
from example.e12_backup_files import ArchiveConfig
from .helpers import model_value, real_choosers, real_press, real_tick, \
    real_ways, stub_choices, stub_choosers, stub_editor, stub_fields, \
    stub_flag, stub_keys, stub_pick, stub_press, stub_ways, told_replaced

ENUM_NAMES = ('MECHANICAL', 'ELECTRICAL', 'ELECTRONIC')
"""The values that either member of the enum example takes.

They are written out here rather than read from the example, in the same way
as every other text these tests expect.
"""

BOTH_CHOSEN = [MEMBER_CHOICE_NAME, MEMBER_CHOICE_NAME]
"""What is on the window for the two members of that example."""

BOTH_TYPED = [MEMBER_FIELD_NAME, MEMBER_FIELD_NAME]
"""What is on the window once the user has asked to type them."""


def _typed() -> Settings:
    """Return the settings of an application that opens with fields."""
    return Settings(choose_values=False)


def test_stub_offered(stub_tk: None) -> None:
    """Test each enum member gets a pull-down of the names it accepts."""
    _ = stub_tk
    stub_editor(EditModel(EnumConfig()))
    offered = [stub_choices(widget) for widget in stub_choosers()]
    assert offered == [ENUM_NAMES, ENUM_NAMES]


def test_real_offered(root_or_skip: tkinter.Tk) -> None:
    """Test real Tk creates exactly the same two pull-downs."""
    EditorWidgets(parent=root_or_skip, model=EditModel(EnumConfig()))
    assert len(real_choosers(root_or_skip)) == 2


def test_stub_no_chooser(stub_tk: None) -> None:
    """Test a member whose values are not a known set gets no pull-down.

    A widget that could never hold anything is a piece of the window spent on
    nothing, which is the same rule the description of a member follows.
    """
    _ = stub_tk
    stub_editor(EditModel(FlatConfig()))
    assert stub_choosers() == []


def test_real_no_chooser(root_or_skip: tkinter.Tk) -> None:
    """Test real Tk leaves out exactly the same widget."""
    EditorWidgets(parent=root_or_skip, model=EditModel(FlatConfig()))
    assert real_choosers(root_or_skip) == []


def test_stub_chosen_at_start(stub_tk: None) -> None:
    """Test the editor opens with the pull-downs and not with the fields."""
    _ = stub_tk
    stub_editor(EditModel(EnumConfig()))
    assert stub_ways() == BOTH_CHOSEN
    assert stub_flag(CHOOSE_TEXT).get()


def test_real_chosen_at_start(root_or_skip: tkinter.Tk) -> None:
    """Test real Tk puts exactly the same widget on the window."""
    EditorWidgets(parent=root_or_skip, model=EditModel(EnumConfig()))
    assert real_ways(root_or_skip) == BOTH_CHOSEN
    assert real_tick(root_or_skip, CHOOSE_TEXT)


def test_stub_typed_at_start(stub_tk: None) -> None:
    """Test an application that asked for fields opens with the fields."""
    _ = stub_tk
    stub_editor(EditModel(EnumConfig(), settings=_typed()))
    assert stub_ways() == BOTH_TYPED
    assert not stub_flag(CHOOSE_TEXT).get()


def test_real_typed_at_start(root_or_skip: tkinter.Tk) -> None:
    """Test real Tk opens with exactly the same widget."""
    EditorWidgets(parent=root_or_skip,
                  model=EditModel(EnumConfig(), settings=_typed()))
    assert real_ways(root_or_skip) == BOTH_TYPED
    assert not real_tick(root_or_skip, CHOOSE_TEXT)


def test_stub_tick_switches(stub_tk: None) -> None:
    """Test the tick-box puts the fields on the window and takes them off."""
    _ = stub_tk
    stub_editor(EditModel(EnumConfig()))
    stub_press(CHOOSE_TEXT)
    assert stub_ways() == BOTH_TYPED
    stub_press(CHOOSE_TEXT)
    assert stub_ways() == BOTH_CHOSEN


def test_real_tick_switches(root_or_skip: tkinter.Tk) -> None:
    """Test the real tick-box switches exactly the same widgets."""
    EditorWidgets(parent=root_or_skip, model=EditModel(EnumConfig()))
    real_press(root_or_skip, CHOOSE_TEXT)
    assert real_ways(root_or_skip) == BOTH_TYPED
    real_press(root_or_skip, CHOOSE_TEXT)
    assert real_ways(root_or_skip) == BOTH_CHOSEN


def test_stub_key_switches(stub_tk: None) -> None:
    """Test the key of the action does what the tick-box does.

    The tick has to follow it, because Tk only flips a tick-box when it is
    the tick-box that was pressed and a tick disagreeing with the window
    would be worse than no tick at all.
    """
    _ = stub_tk
    stub_editor(EditModel(EnumConfig()))
    assert stub_keys()['<F4>']() == 'break'
    assert stub_ways() == BOTH_TYPED
    assert not stub_flag(CHOOSE_TEXT).get()


def test_stub_picking_edits(stub_tk: None) -> None:
    """Test picking a value writes it into the model.

    A pull-down shows the variable of the field of its own member, so picking
    a value is the same edit as typing one and the callback that writes the
    model is the one the field already had. What an entry of its menu is bound
    to is what sets that variable, and that is what is run here.
    """
    _ = stub_tk
    model = EditModel(EnumConfig())
    stub_editor(model)
    stub_pick(stub_choosers()[0], 'ELECTRONIC')
    assert model.rows[0].value == 'ELECTRONIC'
    assert model.dirty


def test_stub_replaced_told(stub_tk: None,
                            monkeypatch: pytest.MonkeyPatch) -> None:
    """Test the user is told what switching to the pull-downs replaced.

    A pull-down shows one of the values its member takes, so a text meaning
    none of them is replaced by the value it most likely meant, and that is
    the one change of the buffer the user did not make. `ELECT` is the
    beginning of two of these three names, so it means the first of those
    two and not the first name of all.
    """
    _ = stub_tk
    told = told_replaced(monkeypatch)
    model = EditModel(EnumConfig())
    stub_editor(model)
    stub_press(CHOOSE_TEXT)
    stub_fields()[0].set('ELECT')
    stub_press(CHOOSE_TEXT)
    assert len(told) == 1
    assert 'ELECT' in told[0]
    assert model.rows[0].value == ENUM_NAMES[1]
    assert stub_fields()[0].get() == ENUM_NAMES[1]


def test_stub_completed(stub_tk: None,
                        monkeypatch: pytest.MonkeyPatch) -> None:
    """Test a text meaning one value is completed and nothing is said."""
    _ = stub_tk
    told = told_replaced(monkeypatch)
    model = EditModel(EnumConfig())
    stub_editor(model)
    stub_press(CHOOSE_TEXT)
    stub_fields()[0].set('MECH')
    stub_press(CHOOSE_TEXT)
    assert not told
    assert model.rows[0].value == 'MECHANICAL'
    assert stub_fields()[0].get() == 'MECHANICAL'


def test_replaced_title_said() -> None:
    """Test the dialog that says what was replaced has a title of its own.

    It is told rather than asked, so it is not one of the four questions and
    it says what it is about in its own words.
    """
    assert REPLACED_TITLE


BOOL_NAMES = ('true', 'false')
"""The values that a member holding true or false takes.

They are written out here rather than read from the core, in the same way as
the names of the enum above, and their order is part of what is expected: it
is the order the pull-down offers them in.
"""

MIXED_WAYS = [MEMBER_FIELD_NAME, MEMBER_FIELD_NAME, MEMBER_CHOICE_NAME]
"""What is on the window for the three members of the backup example.

Its text member and its number member can hold anything of their kind, so
each of them is a field, and the one holding true or false is a pull-down.
The order is the order the example declares them in, which is the order the
editor shows.
"""

PLAIN_WAYS = [MEMBER_FIELD_NAME, MEMBER_FIELD_NAME]
"""What is on the window for the two members of the flat example.

Neither of them has a pull-down, so each of them is a field and stays one
whichever way of editing the user asks for.
"""

SHOWN_WAYS = [(FlatConfig, PLAIN_WAYS), (ArchiveConfig, MIXED_WAYS)]
"""One case per mixture of members with a pull-down and members without.

A member with only one way of editing has to be on the window whatever the
model says about the values that have two, which is what these ask: the flat
example has no pull-down anywhere and the backup example has one among three
members.
"""


def test_stub_flag_offered(stub_tk: None) -> None:
    """Test a member holding true or false gets a pull-down of the two words.

    A member of that kind takes a set of values the editor knows the whole of
    just as an enum member does, and the two kinds read those values from
    different places in the core, so both are asked here.
    """
    _ = stub_tk
    stub_editor(EditModel(ArchiveConfig()))
    offered = [stub_choices(widget) for widget in stub_choosers()]
    assert offered == [BOOL_NAMES]


@pytest.mark.parametrize('config_type, ways', SHOWN_WAYS)
def test_stub_ways_shown(stub_tk: None, config_type: Callable[[], Config],
                         ways: list[str]) -> None:
    """Test every member is edited by a widget that is on the window.

    Which way of editing is used is one answer for the whole editor, and it
    says nothing about a member that has only one way: switching to the fields
    changes the members that had both and leaves the others exactly as they
    were.
    """
    _ = stub_tk
    stub_editor(EditModel(config_type()))
    assert stub_ways() == ways
    stub_press(CHOOSE_TEXT)
    assert stub_ways() == [MEMBER_FIELD_NAME] * len(ways)


@pytest.mark.parametrize('config_type, ways', SHOWN_WAYS)
def test_real_ways_shown(root_or_skip: tkinter.Tk,
                         config_type: Callable[[], Config],
                         ways: list[str]) -> None:
    """Test real Tk puts exactly the same widgets on the window."""
    EditorWidgets(parent=root_or_skip, model=EditModel(config_type()))
    assert real_ways(root_or_skip) == ways
    real_press(root_or_skip, CHOOSE_TEXT)
    assert real_ways(root_or_skip) == [MEMBER_FIELD_NAME] * len(ways)


def test_stub_picking_flag(stub_tk: None) -> None:
    """Test picking one of the two words writes the value it means.

    The pull-down offers the words and the buffer holds true or false, so what
    reaches the model is the value and not the word that named it.
    """
    _ = stub_tk
    model = EditModel(ArchiveConfig())
    stub_editor(model)
    stub_pick(stub_choosers()[0], 'false')
    assert model_value(model, 'compress') is False
    assert model.dirty


def test_stub_picking_held(stub_tk: None) -> None:
    """Test picking the value a member already holds changes nothing.

    A pull-down opens on the value its member holds, so picking that one is
    what a user does who opened it and then thought better of it. There is
    nothing to save afterwards, and an editor that claimed otherwise would be
    telling them something untrue.
    """
    _ = stub_tk
    model = EditModel(EnumConfig())
    stub_editor(model)
    stub_pick(stub_choosers()[0], str(model.rows[0].value))
    assert model.rows[0].value == ENUM_NAMES[1]
    assert not model.dirty


def test_stub_picking_second(stub_tk: None) -> None:
    """Test each pull-down writes its own member and no other.

    Every pull-down of this example offers the same three names, so a
    pull-down wired to the wrong member would show exactly what it should and
    edit the member above it.
    """
    _ = stub_tk
    model = EditModel(EnumConfig())
    stub_editor(model)
    stub_pick(stub_choosers()[1], 'ELECTRONIC')
    assert [row.value for row in model.rows] == ['ELECTRICAL', 'ELECTRONIC']
