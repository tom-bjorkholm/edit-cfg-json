#! /usr/bin/env python3
"""Tests for what the Textual backend makes of a nested configuration object.

The configuration class comes from the example rather than from one of its
own, so that the same nesting is used by the core tests, by both backends and
by the example itself.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import asyncio
from textual.containers import Vertical
from textual.widgets import Input, Label, Static
from edit_cfg_json import EditModel
from edit_cfg_json_textual.textual_editor import EditorApp, NAME_CLASS
from edit_cfg_json_textual.textual_look import fold_id, member_id, value_id
from example.e09_nested_config import CourseExportConfig, TableOutputConfig
from .helpers import ROOMY_SIZE, description_of, index_of

OUTPUT_CLASS = TableOutputConfig.__name__
"""What the row of a nested object of the example says instead of a value."""

MISSING_OUTPUT = f'no {OUTPUT_CLASS}'
"""What the row of the optional member that holds no object says."""

OBJECT_MEMBER = 'participant_output'
"""The member of the example that holds a nested configuration object."""

MISSING_MEMBER = 'audit_output'
"""The member of the example that holds no object at all."""

INSIDE_MEMBER = 'file_name'
"""A member that only exists inside a nested object of the example."""

OUTPUT_SUMMARY = EditModel(TableOutputConfig()).summary
"""The one line of the nested class that a folded object shows."""

OUTPUT_DETAIL = 'Nothing about this class says'
"""The beginning of the part that only an open object shows."""


def _nested_app() -> EditorApp:
    """Return an application on the example with the nested objects."""
    return EditorApp(EditModel(CourseExportConfig()))


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
