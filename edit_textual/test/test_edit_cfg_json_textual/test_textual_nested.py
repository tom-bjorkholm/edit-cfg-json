#! /usr/bin/env python3
"""Tests for what the Textual backend makes of a nested configuration object.

The configuration classes come from the examples rather than from ones of
their own, so that the same nesting is used by the core tests, by both backends
and by the examples themselves. Two of them are used: one object held by a
member, and a list and a dict whose elements are objects.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import asyncio
from textual.containers import Vertical
from textual.widgets import Input, Label, Static
from edit_cfg_json import EditModel
from edit_cfg_json_textual.textual_editor import EditorApp
from edit_cfg_json_textual.textual_look import NAME_CLASS, SUBTREE_CLASS, \
    fold_id, member_id, subtree_id, value_id
from example.e09_nested_config import CourseExportConfig, TableOutputConfig
from example.e10_config_containers import CourseReportsConfig
from .helpers import ROOMY_SIZE, description_of, index_of, wrong_of

OUTPUT_CLASS = TableOutputConfig.__name__
"""What the row of a nested object of the example says instead of a value."""

MISSING_OUTPUT = f'no {OUTPUT_CLASS}'
"""What the row of the optional member that holds no object says."""

OWN_VALID = ' [valid on its own]'
"""What the row of an object that is a configuration on its own adds.

It is written out here rather than read from an internal module of the core,
in the same way as every other text these tests expect.
"""

OWN_REFUSED = ' [refused on its own]'
"""What the row of an object that its own class refuses adds instead."""

OBJECT_MEMBER = 'participant_output'
"""The member of the example that holds a nested configuration object."""

MISSING_MEMBER = 'audit_output'
"""The member of the example that holds no object at all."""

INSIDE_MEMBER = 'file_name'
"""A member that only exists inside a nested object of the example."""

REFUSED_MEMBER = (OBJECT_MEMBER, 'output_format')
"""A member inside that object, to be given a value its class refuses."""

OUTPUT_SUMMARY = EditModel(TableOutputConfig()).summary
"""The one line of the nested class that a folded object shows."""

OUTPUT_DETAIL = 'Nothing about this class says'
"""The beginning of the part that only an open object shows."""

LIST_MEMBER = 'reports'
"""The member of the other example that holds a list of objects.

Three objects of three members each is more rows than a window can spare, so
that container opens folded.
"""

REPEATED_MEMBER = 'title'
"""A member that every one of those repeated objects has.

Several objects of one class have the same member names, so counting one of
them is what says how many objects are on the screen. Nothing but its place
among the rows tells one of those members from the next, which is exactly what
this backend has to get right.
"""

LIST_REPORTS = 3
"""How many objects the list of that example holds."""

DICT_REPORTS = 2
"""How many objects its dict holds, which is few enough to open open."""

REPORT_CONTAINERS = 2
"""How many members of that example hold objects rather than being one.

A list and a dict of objects each get a badge of their own, because that row
is the only one left on the screen once the container is folded and every
object it is about is hidden.
"""


def _nested_app() -> EditorApp:
    """Return an application on the example with the nested objects."""
    return EditorApp(EditModel(CourseExportConfig()))


def _refused_app() -> EditorApp:
    """Return one whose nested object holds a value its class refuses."""
    model = EditModel(CourseExportConfig())
    model.set_text(path=REFUSED_MEMBER, text='xml')
    return EditorApp(model)


def _own_text(app: EditorApp, member_name: str) -> str:
    """Return what the application says one object is on its own."""
    widget = app.query_one(f'#{subtree_id(index_of(app, member_name))}',
                           Static)
    return str(widget.content)


def _all_names(app: EditorApp) -> list[str]:
    """Return the name of every node, in the order the rows are."""
    return [str(label.content) for label in app.query(Label)
            if label.has_class(NAME_CLASS)]


def _shown_names(app: EditorApp) -> list[str]:
    """Return the name of every node that is on the screen."""
    return [name for index, name in enumerate(_all_names(app))
            if app.query_one(f'#{member_id(index)}', Vertical).display]


def _value_text(app: EditorApp, member_name: str) -> str:
    """Return what the application shows in place of one node's value."""
    widget = app.query_one(f'#{value_id(index_of(app, member_name))}', Static)
    return str(widget.content)


async def _opened() -> tuple[list[str], str, str]:
    """Return the rows and what the two nested members show as values."""
    app = _nested_app()
    async with app.run_test(size=ROOMY_SIZE):
        return (_all_names(app), _value_text(app, OBJECT_MEMBER),
                _value_text(app, MISSING_MEMBER))


def test_object_is_a_node() -> None:
    """Test a nested object says its class and holds its members as rows."""
    names, held, missing = asyncio.run(_opened())
    assert names == ['course_name', OBJECT_MEMBER, INSIDE_MEMBER,
                     'output_format', 'encoding', MISSING_MEMBER]
    assert held == OUTPUT_CLASS
    assert missing == MISSING_OUTPUT


async def _fields() -> int:
    """Return how many editable fields the application created."""
    app = _nested_app()
    async with app.run_test(size=ROOMY_SIZE):
        return len(app.query(Input))


def test_object_has_no_field() -> None:
    """Test a nested object gets no field, because it holds no value.

    One field for the plain member of the configuration and one for each of
    the three members of the object that is there, and none for either of the
    two nested members themselves.
    """
    assert asyncio.run(_fields()) == 4


async def _folded_object() -> tuple[list[str], list[str], str, str]:
    """Press the control of the nested object and report what is shown."""
    app = _nested_app()
    async with app.run_test(size=ROOMY_SIZE) as pilot:
        before = _shown_names(app)
        said = str(description_of(app, OBJECT_MEMBER).content)
        await pilot.click(f'#{fold_id(index_of(app, OBJECT_MEMBER))}')
        await pilot.pause()
        return (before, _shown_names(app), said,
                str(description_of(app, OBJECT_MEMBER).content))


def test_control_folds_object() -> None:
    """Test the control of a nested object hides the rows of its members."""
    before, after, _, _ = asyncio.run(_folded_object())
    assert INSIDE_MEMBER in before
    assert INSIDE_MEMBER not in after
    assert OBJECT_MEMBER in after


def test_folded_says_less() -> None:
    """Test folding a nested object leaves the summary of its class.

    An object that is showing less of itself says less about itself, and the
    text below it has to be written again when it is folded or nothing would
    say so.
    """
    _, _, open_text, folded_text = asyncio.run(_folded_object())
    assert OUTPUT_DETAIL in open_text
    assert OUTPUT_DETAIL not in folded_text
    assert OUTPUT_SUMMARY in folded_text


async def _badge_on_fold(app: EditorApp) -> tuple[str, str]:
    """Press the control of the nested object and report what it now says."""
    async with app.run_test(size=ROOMY_SIZE) as pilot:
        before = _own_text(app, OBJECT_MEMBER)
        await pilot.click(f'#{fold_id(index_of(app, OBJECT_MEMBER))}')
        await pilot.pause()
        return before, _own_text(app, OBJECT_MEMBER)


def test_badge_on_fold() -> None:
    """Test folding a nested object says what that object is on its own.

    Nothing has been validated when the editor opens, so the object has not
    been asked and says nothing. Folding it is one of the moments the model
    asks, which is the cheap local question that needs no whole configuration.
    """
    before, after = asyncio.run(_badge_on_fold(_nested_app()))
    assert before == ''
    assert after == OWN_VALID


def test_badge_refused() -> None:
    """Test an object its own class refuses says so where it is folded."""
    _, after = asyncio.run(_badge_on_fold(_refused_app()))
    assert after == OWN_REFUSED


async def _wrong_on_fold() -> tuple[str, str]:
    """Fold the refused object, open it again, and read what is wrong."""
    app = _refused_app()
    async with app.run_test(size=ROOMY_SIZE) as pilot:
        before = wrong_of(app, REFUSED_MEMBER[-1])
        control = f'#{fold_id(index_of(app, OBJECT_MEMBER))}'
        await pilot.click(control)
        await pilot.click(control)
        await pilot.pause()
        return before, wrong_of(app, REFUSED_MEMBER[-1])


def test_wrong_shown_on_fold() -> None:
    """Test folding says why an object was refused and not only that it was.

    Folding asks the object, and what it refused is said at the member it is
    about, which is a row this backend has to write again when the fold
    changes: nothing has been typed and no validation pass has run.
    """
    before, after = asyncio.run(_wrong_on_fold())
    assert before == ''
    assert 'output_format' in after


async def _badge_widgets() -> int:
    """Return how many nodes the application gave a badge widget at all."""
    app = _nested_app()
    async with app.run_test(size=ROOMY_SIZE):
        return len(app.query(f'.{SUBTREE_CLASS}'))


async def _repeated() -> tuple[list[str], list[str], int]:
    """Open the other example and press the control of its folded list."""
    app = EditorApp(EditModel(CourseReportsConfig()))
    async with app.run_test(size=ROOMY_SIZE) as pilot:
        folded = _shown_names(app)
        await pilot.click(f'#{fold_id(index_of(app, LIST_MEMBER))}')
        await pilot.pause()
        return folded, _shown_names(app), len(app.query(f'.{SUBTREE_CLASS}'))


def test_repeated_objects() -> None:
    """Test a list of objects opens folded and opens to one row for each.

    Several objects of one class in one container is what a real configuration
    is made of, and every one of them is a node with the same member names as
    the next, so what a backend has to get right is how many of them there are.
    """
    folded, opened, badges = asyncio.run(_repeated())
    assert folded.count(REPEATED_MEMBER) == DICT_REPORTS
    assert opened.count(REPEATED_MEMBER) == DICT_REPORTS + LIST_REPORTS
    assert badges == DICT_REPORTS + LIST_REPORTS + REPORT_CONTAINERS


def test_only_objects_say() -> None:
    """Test only the member that holds an object is given a widget for it.

    The example declares two nested members and one of them holds no object,
    so there is nothing there to ask and no widget that could ever say
    anything about it.
    """
    assert asyncio.run(_badge_widgets()) == 1
