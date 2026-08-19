#! /usr/bin/env python3
"""Tests for the search of the Textual backend.

What a search is belongs to the core and is tested there. What is tested here
is this backend's half of it: the field, the four controls, the line under
them, and the two things a printout cannot do — bringing what was found into
view and putting the cursor in it.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import asyncio
from textual.containers import Vertical
from textual.widgets import Button, Checkbox, Input, Static
from edit_cfg_json import ActionSettings, EditModel, FIND_OPTION_HELP, \
    FindOptions
from edit_cfg_json_textual.textual_editor import EditorApp
from edit_cfg_json_textual.textual_find import FIND_NEXT_TEXT, \
    FIND_TICK_LABELS
from edit_cfg_json_textual.textual_look import FIND_ID, FIND_LINE_ID, \
    FIND_NEXT_ID, FIND_TICK_IDS, member_id, value_id
from edit_cfg_json_textual.textual_words import FIND_COMMAND, \
    FIND_NEXT_COMMAND
from example.e01_flat_config import FlatConfig
from example.e08_lists_and_dicts import ContainerConfig
from .helpers import ROOMY_SIZE, index_of, mark_of, panel_of

FIND_KEY = ActionSettings().find[0]
"""Key that puts the cursor in the field a search is typed into."""

NEXT_KEY = ActionSettings().find_next[0]
"""Key that goes to the next member the search reaches."""

FOUND_MARK = ' (found)'
"""Mark of the member that the search has got to.

It is written out here rather than read from the core, in the same way as every
other text these tests expect: what this backend has to do with it is show it.
"""

HIDDEN_VALUE = 'label-7'
"""A value inside the member that the example opens folded."""

ENTER_KEY = 'enter'
"""Key that goes into the member the search has already reached."""


def _flat_app() -> EditorApp:
    """Return an application on the flat example."""
    return EditorApp(EditModel(FlatConfig()))


def _tree_app() -> EditorApp:
    """Return an application on the example with the containers."""
    return EditorApp(EditModel(ContainerConfig()))


def _find_line(app: EditorApp) -> str:
    """Return what the editor says the search has reached, or nothing.

    A widget that is not being shown says nothing, whatever it holds, so this
    answers what is on the screen and not what a widget remembers.
    """
    widget = app.query_one(f'#{FIND_LINE_ID}', Static)
    return str(widget.content) if widget.display else ''


def _ticked(app: EditorApp) -> list[bool]:
    """Return whether each control that says where a search looks is ticked."""
    return [app.query_one(f'#{tick}', Checkbox).value
            for tick in FIND_TICK_IDS]


async def _typed(app: EditorApp, text: str) -> None:
    """Type one text into the field that a search is typed into."""
    app.query_one(f'#{FIND_ID}', Input).value = text


def test_ticks_all_explained() -> None:
    """Test every answer about where a search looks has a control and a tip.

    Two of the labels are one or two characters, so the tooltip is the only
    place their meaning is said. A control without one would be a control
    nobody can read.
    """
    assert len(FIND_TICK_LABELS) == len(FindOptions()._fields)
    assert len(FIND_TICK_IDS) == len(FIND_TICK_LABELS)
    assert len(FIND_OPTION_HELP) == len(FIND_TICK_LABELS)
    assert all(FIND_TICK_LABELS) and all(FIND_OPTION_HELP)


async def _search_row() -> tuple[list[str], list[str], list[bool], str]:
    """Return what the search row holds when the editor opens."""
    app = _flat_app()
    async with app.run_test(size=ROOMY_SIZE):
        labels = [str(box.label) for box in app.query(Checkbox)]
        tips = [str(box.tooltip) for box in app.query(Checkbox)]
        return labels, tips, _ticked(app), _find_line(app)


def test_search_row_shown() -> None:
    """Test the editor opens with the four controls, ticked as the core says.

    The line that says what the search has reached is not on the screen,
    because nothing is being looked for yet.
    """
    labels, tips, ticked, line = asyncio.run(_search_row())
    assert labels == list(FIND_TICK_LABELS)
    assert tips == list(FIND_OPTION_HELP)
    assert ticked == list(FindOptions())
    assert line == ''


async def _next_control() -> str:
    """Return the label of the control that goes to the next member found."""
    app = _flat_app()
    async with app.run_test(size=ROOMY_SIZE):
        return str(app.query_one(f'#{FIND_NEXT_ID}', Button).label)


def test_next_control_shown() -> None:
    """Test the search offers a control as well as a key.

    A function key is the one thing a terminal is most likely not to deliver,
    and a user who has just typed into the field is looking at this row.
    """
    assert asyncio.run(_next_control()) == FIND_NEXT_TEXT


async def _found_by_typing() -> tuple[str, str, str]:
    """Type into the field and report what the editor says about it."""
    app = _flat_app()
    async with app.run_test(size=ROOMY_SIZE) as pilot:
        await _typed(app, 'answer')
        await pilot.pause()
        return (_find_line(app), mark_of(app, 'answer'),
                mark_of(app, 'name'))


def test_typing_finds() -> None:
    """Test typing into the field looks for that text as it is typed.

    Nothing is pressed to ask: the field stays on the screen and the answer
    moves under it, which is what a field that is a part of the editor is for.
    """
    line, answer, name = asyncio.run(_found_by_typing())
    assert line == 'find answer: 1 of 1'
    assert answer == FOUND_MARK
    assert name == ''


async def _cleared() -> str:
    """Type into the field and then empty it again."""
    app = _flat_app()
    async with app.run_test(size=ROOMY_SIZE) as pilot:
        await _typed(app, 'answer')
        await pilot.pause()
        await _typed(app, '')
        await pilot.pause()
        return _find_line(app)


def test_cleared_says_nothing() -> None:
    """Test clearing the field takes the line off the screen again."""
    assert asyncio.run(_cleared()) == ''


async def _no_match() -> str:
    """Look for a text that reaches no member of the flat example."""
    app = _flat_app()
    async with app.run_test(size=ROOMY_SIZE) as pilot:
        await _typed(app, 'nowhere')
        await pilot.pause()
        return _find_line(app)


def test_nothing_matches() -> None:
    """Test a text that reaches no member says so on that line."""
    assert asyncio.run(_no_match()) == 'find nowhere: no member matches'


async def _find_focus() -> tuple[object, str]:
    """Press the find key and report what has the cursor and what is typed."""
    app = _flat_app()
    async with app.run_test(size=ROOMY_SIZE) as pilot:
        await _typed(app, 'answ')
        await pilot.pause()
        await pilot.press(FIND_KEY)
        await pilot.pause()
        focused = app.focused
        return (None if focused is None else focused.id,
                app.query_one(f'#{FIND_ID}', Input).value)


def test_find_key_focuses() -> None:
    """Test the find key puts the cursor in the field, leaving its text.

    A user who has found one member and wants another comes back to text that
    is worth changing rather than text that is worth typing again.
    """
    focused, typed = asyncio.run(_find_focus())
    assert focused == FIND_ID
    assert typed == 'answ'


async def _reached(key: str) -> tuple[object, int]:
    """Look for a member, press one key and report what has the cursor."""
    app = _flat_app()
    async with app.run_test(size=ROOMY_SIZE) as pilot:
        await _typed(app, 'answer')
        await pilot.pause()
        assert app.focused is None or app.focused.id != value_id(1)
        await pilot.press(FIND_KEY)
        await pilot.pause()
        await pilot.press(key)
        await pilot.pause()
        focused = app.focused
        return (None if focused is None else focused.id,
                index_of(app, 'answer'))


def test_enter_goes_into_it() -> None:
    """Test pressing Enter in the field puts the cursor in what was found.

    Typing does not move the cursor, because the user is typing in the search
    field. This is the press that says they have found what they were looking
    for and want to edit it.
    """
    focused, index = asyncio.run(_reached(ENTER_KEY))
    assert focused == value_id(index)


def test_next_goes_into_it() -> None:
    """Test the find next key does the same as it goes on to the next one."""
    focused, index = asyncio.run(_reached(NEXT_KEY))
    assert focused == value_id(index)


async def _walked() -> list[str]:
    """Look for a text that reaches six members and press the control twice."""
    app = _tree_app()
    async with app.run_test(size=ROOMY_SIZE) as pilot:
        await _typed(app, 'port')
        await pilot.pause()
        said = [_find_line(app)]
        for _ in range(2):
            await pilot.click(f'#{FIND_NEXT_ID}')
            await pilot.pause()
            said.append(_find_line(app))
        return said


def test_control_goes_on() -> None:
    """Test the control goes to the next member the search reaches."""
    assert asyncio.run(_walked()) == ['find port: 1 of 6',
                                      'find port: 2 of 6',
                                      'find port: 3 of 6']


async def _opened() -> tuple[bool, bool, str]:
    """Look for a value inside the container that opens folded."""
    app = _tree_app()
    async with app.run_test(size=ROOMY_SIZE) as pilot:
        shown = app.query_one(f'#{member_id(index_of(app, "7"))}', Vertical)
        before = shown.display
        await _typed(app, HIDDEN_VALUE)
        await pilot.pause()
        return before, shown.display, _find_line(app)


def test_folded_opens() -> None:
    """Test a match inside a folded container puts its rows back on the screen.

    What is found has to be reachable, and the long list of the example opens
    folded, so a search that left it folded would have found something the user
    cannot see.
    """
    before, after, line = asyncio.run(_opened())
    assert not before
    assert after
    assert line == f'find {HIDDEN_VALUE}: 1 of 1'


async def _unticked(ticks: tuple[str, ...]) -> tuple[str, list[bool]]:
    """Look for a text and then press some of the controls."""
    app = _tree_app()
    async with app.run_test(size=ROOMY_SIZE) as pilot:
        await _typed(app, 'ports')
        await pilot.pause()
        for tick in ticks:
            app.query_one(f'#{tick}', Checkbox).toggle()
            await pilot.pause()
        return _find_line(app), _ticked(app)


def test_tick_looks_again() -> None:
    """Test turning off the path leaves a text that only the path reached."""
    line, ticked = asyncio.run(_unticked((FIND_TICK_IDS[0],)))
    assert line == 'find ports: no member matches'
    assert ticked == [False, True, False, False]


def test_nowhere_said() -> None:
    """Test a search with nowhere left to look says so, and not that it failed.

    Nothing was compared with anything, so saying that no member matches would
    be untrue.
    """
    line, ticked = asyncio.run(_unticked(FIND_TICK_IDS[:2]))
    assert line == 'find ports: looking in neither the path nor the value'
    assert ticked == [False, False, False, False]


async def _find_field_height() -> tuple[int, int]:
    """Give the search field the cursor and report how tall it stays."""
    app = _flat_app()
    async with app.run_test(size=ROOMY_SIZE) as pilot:
        field = app.query_one(f'#{FIND_ID}', Input)
        before = field.outer_size.height
        await pilot.press(FIND_KEY)
        await pilot.pause()
        return before, field.outer_size.height


def test_find_field_one_high() -> None:
    """Test the search field is one cell high with the cursor in it too.

    It is the field of a member all over again, so it is compact for the same
    reason: a field that grew a border when it was given the focus would lay
    the text being looked for out under the line that says what it reached.
    """
    before, after = asyncio.run(_find_field_height())
    assert before == 1
    assert after == 1


async def _palette_names() -> list[str]:
    """Return what the command palette of the editor offers."""
    app = _flat_app()
    async with app.run_test(size=ROOMY_SIZE):
        return [entry.name for entry in panel_of(app).command_entries()]


def test_palette_offers() -> None:
    """Test both actions of the search are reachable without their keys.

    Every terminal can reach the palette, because it is opened with one key and
    then typed into, which is what makes it the answer for a function key that
    a terminal does not deliver.
    """
    names = asyncio.run(_palette_names())
    assert FIND_COMMAND in names
    assert FIND_NEXT_COMMAND in names
