#! /usr/bin/env python3
"""Tests for the search of the Tkinter backend.

What a search is belongs to the core and is tested there. What is tested here
is this backend's half of it: the field, the four controls, the line under
them, and the two things a printout cannot do — bringing what was found into
view and putting the cursor in it.

Every test has a stubbed form and a real Tk form wherever real Tk can answer,
for the reason given in `helpers`: the two fail in opposite directions. The
focus is the exception, because a withdrawn window has none to give.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import tkinter
import pytest
from edit_cfg_json import EditModel, FIND_OPTION_HELP, FindOptions
from edit_cfg_json_tk.tk_editor import EditorWidgets
from edit_cfg_json_tk.tk_find import FIND_FIELD_NAME, FIND_LABEL_TEXT, \
    FIND_NEXT_TEXT, FIND_TICK_LABELS
from edit_cfg_json_tk.tk_tooltip import TOOLTIP_WIDTH
from example.e01_flat_config import FlatConfig
from example.e08_lists_and_dicts import ContainerConfig
from .helpers import FakeCanvas, FakeWidget, WHOLE_VIEW, find_field, \
    real_press, real_texts, real_tick, retype, stub_editor, stub_find_var, \
    stub_flag, stub_keys, stub_press, stub_texts

PATH_TICK, VALUE_TICK, CASE_TICK, WHOLE_TICK = FIND_TICK_LABELS
"""The label of each control that says where a search looks."""

FOUND_MARK = ' (found)'
"""Mark of the member that the search has got to.

It is written out here rather than read from the core, in the same way as every
other text these tests expect: what this backend has to do with it is show it.
"""

LONG_LIST = 'many_labels'
"""The member of the example that the editor opens folded."""

HIDDEN_VALUE = 'label-7'
"""A value inside that member, which nothing on the window shows at first."""

HIDDEN_NAME = '7'
"""The name of the row that value is on, which is where it is in the list.

A value is in a field and a name is in a label, so the name is what the texts
of the window say about a row being back on it.
"""

FIND_KEY = '<Control-f>'
"""Sequence that Tk binds for the key that focuses the search field."""

NEXT_KEY = '<F3>'
"""Sequence that Tk binds for the key that goes to the next member found."""

POINTER_PLACE = (400, 300)
"""Where the pointer is when it arrives on a control, in screen pixels.

It is far enough to the right and down that a tooltip put beside it would hang
outside the window that the stub stands in for, which is what the test about
keeping the whole of one inside the window reads.
"""


def _flat_stub() -> EditorWidgets:
    """Build the stubbed widgets of the flat example."""
    return stub_editor(EditModel(FlatConfig()))


def _tree_stub() -> EditorWidgets:
    """Build the stubbed widgets of the example with the containers."""
    return stub_editor(EditModel(ContainerConfig()))


def _canvas() -> FakeCanvas:
    """Return the stub canvas that the scrolling part of the editor is on.

    It is the one widget the editor tells how much of its contents is in view,
    which is what a search reads before it decides whether to scroll.
    """
    canvases = [widget for widget in FakeWidget.created
                if 'yscrollcommand' in widget.options]
    assert len(canvases) == 1
    return canvases[0]


def test_ticks_all_explained() -> None:
    """Test every answer about where a search looks has a control and a tip.

    Two of the labels are one or two characters, so the tooltip is the only
    place their meaning is said. A control without one would be a control
    nobody can read.
    """
    assert len(FIND_TICK_LABELS) == len(FindOptions()._fields)
    assert len(FIND_OPTION_HELP) == len(FIND_TICK_LABELS)
    assert all(FIND_TICK_LABELS) and all(FIND_OPTION_HELP)


def test_stub_search_row(stub_tk: None) -> None:
    """Test the search is a label, four controls and a button on one row.

    The line that says what the search has reached is not on the window,
    because nothing is being looked for yet.
    """
    _ = stub_tk
    _flat_stub()
    shown = stub_texts(packed_only=True)
    assert FIND_LABEL_TEXT in shown
    assert FIND_NEXT_TEXT in shown
    assert set(FIND_TICK_LABELS) <= set(shown)
    assert not [text for text in shown if text.startswith('find ')]


def test_real_search_row(root_or_skip: tkinter.Tk) -> None:
    """Test real Tk shows exactly what the stubbed test expects."""
    EditorWidgets(parent=root_or_skip, model=EditModel(FlatConfig()))
    shown = real_texts(root_or_skip, packed_only=True)
    assert FIND_LABEL_TEXT in shown
    assert FIND_NEXT_TEXT in shown
    assert set(FIND_TICK_LABELS) <= set(shown)
    assert not [text for text in shown if text.startswith('find ')]


def test_stub_ticks_default(stub_tk: None) -> None:
    """Test the editor opens with the four answers the core chose."""
    _ = stub_tk
    _flat_stub()
    assert stub_flag(PATH_TICK).get()
    assert stub_flag(VALUE_TICK).get()
    assert not stub_flag(CASE_TICK).get()
    assert not stub_flag(WHOLE_TICK).get()


def test_real_ticks_default(root_or_skip: tkinter.Tk) -> None:
    """Test the real controls start in exactly the same four states."""
    EditorWidgets(parent=root_or_skip, model=EditModel(FlatConfig()))
    assert real_tick(root_or_skip, PATH_TICK)
    assert real_tick(root_or_skip, VALUE_TICK)
    assert not real_tick(root_or_skip, CASE_TICK)
    assert not real_tick(root_or_skip, WHOLE_TICK)


def test_stub_tooltips(stub_tk: None) -> None:
    """Test each control too small for a word answers the pointer on it.

    Tk has no tooltip, so what says that a control explains itself is the two
    bindings the editor put on it. The button is one of these controls now that
    it carries the arrow instead of the two words the arrow stands for.
    """
    _ = stub_tk
    _flat_stub()
    labels = {*FIND_TICK_LABELS, FIND_NEXT_TEXT}
    boxes = [widget for widget in FakeWidget.created
             if widget.options.get('text') in labels]
    assert len(boxes) == len(labels)
    assert all({'<Enter>', '<Leave>'} <= set(box.bindings) for box in boxes)


def _pointer(place: tuple[int, int]) -> 'tkinter.Event[tkinter.Misc]':
    """Return the event that says where the pointer has just arrived."""
    event: 'tkinter.Event[tkinter.Misc]' = tkinter.Event()
    event.x_root, event.y_root = place
    return event


def _stub_control(label: str) -> FakeWidget:
    """Return the stub control of the search that carries one label."""
    boxes = [widget for widget in FakeWidget.created
             if widget.options.get('text') == label]
    assert len(boxes) == 1
    return boxes[0]


def _stub_tips() -> list[FakeWidget]:
    """Return the stub widgets that show an explanation of the search."""
    said = {' '.join(text.split()) for text in FIND_OPTION_HELP}
    return [widget for widget in FakeWidget.created
            if ' '.join(str(widget.options.get('text', '')).split()) in said]


def _hovered(label: str) -> FakeWidget:
    """Build the editor, rest the pointer on one control, return the tooltip.

    Args:
        label: Label of the control the pointer rests on.

    Returns:
        The one widget that the tooltip amounts to.
    """
    _flat_stub()
    _stub_control(label).bindings['<Enter>'](_pointer(POINTER_PLACE))
    tips = _stub_tips()
    assert len(tips) == 1
    return tips[0]


def test_stub_tip_shown(stub_tk: None) -> None:
    """Test the pointer resting on a control puts its explanation up.

    What it says is the core's sentence and not a shorter one of this
    backend's, and it is laid out in lines that fit beside the control rather
    than in the one line that a sentence would otherwise be.
    """
    _ = stub_tk
    shown = str(_hovered(CASE_TICK).options['text'])
    assert ' '.join(shown.split()) == FIND_OPTION_HELP[2]
    assert max(len(line) for line in shown.splitlines()) <= TOOLTIP_WIDTH


def test_stub_tip_inside(stub_tk: None) -> None:
    """Test a tooltip that would hang outside the window is moved into it.

    It is put over the window the control is in and not in a window of its own,
    which is what gives it sharp corners on every platform and every version of
    Tk, so a tooltip reaching past an edge would be cut off there. The stub
    answers that the window is exactly as big as the tooltip needs, so the only
    place the whole of it fits is the corner.
    """
    _ = stub_tk
    assert _hovered(WHOLE_TICK).packing == {'x': 0, 'y': 0}


def test_stub_tip_taken_away(stub_tk: None) -> None:
    """Test the pointer leaving a control takes its explanation away again."""
    _ = stub_tk
    tip = _hovered(PATH_TICK)
    _stub_control(PATH_TICK).bindings['<Leave>']()
    assert tip not in FakeWidget.created
    assert not _stub_tips()


def test_stub_typing_finds(stub_tk: None) -> None:
    """Test typing into the field looks for that text as it is typed.

    Nothing is pressed to ask: the field stays on the window and the answer
    moves under it, which is what a field that is a part of the editor is for.
    """
    _ = stub_tk
    _flat_stub()
    stub_find_var().set('answer')
    shown = stub_texts(packed_only=True)
    assert 'find answer: 1 of 1' in shown
    assert FOUND_MARK in shown


def test_real_typing_finds(root_or_skip: tkinter.Tk) -> None:
    """Test real Tk searches as the field is typed into, and says the same."""
    EditorWidgets(parent=root_or_skip, model=EditModel(FlatConfig()))
    retype(find_field(root_or_skip), 'answer')
    shown = real_texts(root_or_skip, packed_only=True)
    assert 'find answer: 1 of 1' in shown
    assert FOUND_MARK in shown


def test_stub_line_clears(stub_tk: None) -> None:
    """Test clearing the field takes the line off the window again."""
    _ = stub_tk
    _flat_stub()
    field = stub_find_var()
    field.set('answer')
    field.set('')
    assert not [text for text in stub_texts(packed_only=True)
                if text.startswith('find ')]


def test_stub_no_match(stub_tk: None) -> None:
    """Test a text that reaches no member says so on that line."""
    _ = stub_tk
    _flat_stub()
    stub_find_var().set('nowhere')
    assert 'find nowhere: no member matches' in \
        stub_texts(packed_only=True)


def test_stub_opens_fold(stub_tk: None) -> None:
    """Test a match inside a folded container puts that container's rows back.

    What is found has to be reachable, and the long list of the example opens
    folded, so a search that left it folded would have found something the
    user cannot see.
    """
    _ = stub_tk
    _tree_stub()
    assert HIDDEN_NAME not in stub_texts(packed_only=True)
    stub_find_var().set(HIDDEN_VALUE)
    shown = stub_texts(packed_only=True)
    assert HIDDEN_NAME in shown
    assert f'find {HIDDEN_VALUE}: 1 of 1' in shown


def test_real_opens_fold(root_or_skip: tkinter.Tk) -> None:
    """Test real Tk puts the rows of that container back in the same way."""
    EditorWidgets(parent=root_or_skip, model=EditModel(ContainerConfig()))
    assert HIDDEN_NAME not in real_texts(root_or_skip, packed_only=True)
    retype(find_field(root_or_skip), HIDDEN_VALUE)
    assert HIDDEN_NAME in real_texts(root_or_skip, packed_only=True)


def test_stub_next_button(stub_tk: None) -> None:
    """Test the button goes to the next member the search reaches."""
    _ = stub_tk
    _tree_stub()
    stub_find_var().set('port')
    assert 'find port: 1 of 6' in stub_texts(packed_only=True)
    stub_press(FIND_NEXT_TEXT)
    assert 'find port: 2 of 6' in stub_texts(packed_only=True)


def test_real_next_button(root_or_skip: tkinter.Tk) -> None:
    """Test the real button does exactly the same."""
    EditorWidgets(parent=root_or_skip, model=EditModel(ContainerConfig()))
    retype(find_field(root_or_skip), 'port')
    real_press(root_or_skip, FIND_NEXT_TEXT)
    assert 'find port: 2 of 6' in real_texts(root_or_skip, packed_only=True)


def test_stub_next_key(stub_tk: None) -> None:
    """Test the key of the find next action does what the button does."""
    _ = stub_tk
    _tree_stub()
    stub_find_var().set('port')
    assert stub_keys()[NEXT_KEY]() == 'break'
    assert 'find port: 2 of 6' in stub_texts(packed_only=True)


def test_stub_find_key(stub_tk: None) -> None:
    """Test the find key puts the cursor in the field, leaving its text.

    A user who has found one member and wants another comes back to text that
    is worth changing rather than text that is worth typing again.
    """
    _ = stub_tk
    _flat_stub()
    stub_find_var().set('answ')
    assert stub_keys()[FIND_KEY]() == 'break'
    assert FakeWidget.focused[-1].options.get('name') == FIND_FIELD_NAME
    assert stub_find_var().get() == 'answ'


def test_stub_next_focus(stub_tk: None) -> None:
    """Test going to the next member puts the cursor in its field.

    Typing in the search field does not move the cursor, because the user is
    typing there. This is the press that says they have found what they were
    looking for and want to edit it.
    """
    _ = stub_tk
    _flat_stub()
    stub_find_var().set('answer')
    assert not FakeWidget.focused
    stub_keys()[NEXT_KEY]()
    assert FakeWidget.focused[-1].options.get('name') != FIND_FIELD_NAME
    assert 'textvariable' in FakeWidget.focused[-1].options


def test_stub_return_enters(stub_tk: None) -> None:
    """Test pressing Return in the field goes into the member that was found.

    Typing does not move the cursor, because the user is typing in the search
    field. Return is the press that says they have found what they were
    looking for and want to edit it, which is the same thing the button and
    the find next key do.
    """
    _ = stub_tk
    _flat_stub()
    stub_find_var().set('answer')
    assert not FakeWidget.focused
    _stub_find_field().bindings['<Return>']()
    assert FakeWidget.focused[-1].options.get('name') != FIND_FIELD_NAME
    assert 'textvariable' in FakeWidget.focused[-1].options


def _stub_find_field() -> FakeWidget:
    """Return the stub field that a search is typed into."""
    fields = [widget for widget in FakeWidget.created
              if widget.options.get('name') == FIND_FIELD_NAME]
    assert len(fields) == 1
    return fields[0]


def test_real_return_enters(root_or_skip: tkinter.Tk) -> None:
    """Test the real field is bound to answer Return the same way."""
    EditorWidgets(parent=root_or_skip, model=EditModel(FlatConfig()))
    assert find_field(root_or_skip).bind('<Return>')


def test_stub_no_focus(stub_tk: None) -> None:
    """Test a member that is not edited in a field is only brought into view.

    A list, a dict and a nested configuration object are each edited through
    the rows below them, so there is nothing there to type into. The whole
    path has to match for the container to be the only member reached, since
    the path of every value inside it begins with its name.
    """
    _ = stub_tk
    _tree_stub()
    stub_find_var().set('retry_delays')
    stub_flag(WHOLE_TICK).set(True)
    stub_press(WHOLE_TICK)
    assert 'find retry_delays: 1 of 1' in stub_texts(packed_only=True)
    stub_keys()[NEXT_KEY]()
    assert not FakeWidget.focused


def test_stub_scrolls(stub_tk: None) -> None:
    """Test what was found is scrolled to when it is off the window.

    Nothing is scrolled while it is already in view, which is what keeps a
    search that is being typed from moving the window on every key.
    """
    _ = stub_tk
    _tree_stub()
    canvas = _canvas()
    assert canvas.view == WHOLE_VIEW
    stub_find_var().set('ports')
    assert canvas.moved == []
    canvas.view = (0.5, 0.6)
    stub_find_var().set('ports[http]')
    assert canvas.moved == [0.0]


NO_MATCH_FORM = 'find {text}: no member matches'
"""What the line says about a text that reaches no member at all."""


@pytest.mark.parametrize('label, text', [(PATH_TICK, 'ports'),
                                         (VALUE_TICK, 'html'),
                                         (CASE_TICK, 'PORTS'),
                                         (WHOLE_TICK, 'port')])
def test_stub_tick_again(stub_tk: None, label: str, text: str) -> None:
    """Test each control changes where the search looks and says what it finds.

    The two that name a place are turned off and the two that make the
    comparison harder are turned on, so every one of the four is a text that
    reached a member before it was pressed and reaches none afterwards. The
    stub does not flip its own tick, which real Tk does, so the state is set
    here and the control is then pressed.
    """
    _ = stub_tk
    _tree_stub()
    said = NO_MATCH_FORM.format(text=text)
    stub_find_var().set(text)
    assert said not in stub_texts(packed_only=True)
    stub_flag(label).set(label in (CASE_TICK, WHOLE_TICK))
    stub_press(label)
    assert said in stub_texts(packed_only=True)


def test_stub_nowhere_said(stub_tk: None) -> None:
    """Test a search with nowhere left to look says so, and not that it failed.

    Nothing was compared with anything, so saying that no member matches would
    be untrue.
    """
    _ = stub_tk
    _tree_stub()
    stub_find_var().set('ports')
    for label in (PATH_TICK, VALUE_TICK):
        stub_flag(label).set(False)
        stub_press(label)
    assert 'find ports: looking in neither the path nor the value' in \
        stub_texts(packed_only=True)


def test_real_tick_again(root_or_skip: tkinter.Tk) -> None:
    """Test pressing a real control changes where the search looks.

    Real Tk flips the tick itself, unlike the stub, so this is one press and
    the state that follows it is the toolkit's own answer.
    """
    EditorWidgets(parent=root_or_skip, model=EditModel(ContainerConfig()))
    retype(find_field(root_or_skip), 'ports')
    assert 'find ports: 3 of 3' not in real_texts(root_or_skip)
    real_press(root_or_skip, PATH_TICK)
    assert not real_tick(root_or_skip, PATH_TICK)
    assert 'find ports: no member matches' in \
        real_texts(root_or_skip, packed_only=True)
