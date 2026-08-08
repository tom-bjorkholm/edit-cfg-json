#! /usr/bin/env python3
"""Tests for the tree of rows and the folding of the Textual backend.

The configuration class comes from the example rather than from a class of its
own, so that the same containers are used by the core tests, by both backends
and by the example itself.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import asyncio
from textual.containers import Vertical
from textual.widgets import Button, Input, Label
from edit_cfg_json import EditModel
from edit_cfg_json_textual.textual_editor import EditorApp, FOLD_COMMAND, \
    NAME_CLASS, OPEN_COMMAND, TREE_INDENT
from edit_cfg_json_textual.textual_look import FOLD_OPEN_TEXT, \
    FOLD_SHUT_TEXT, fold_id, member_id, value_id
from example.e01_flat_config import FlatConfig
from example.e08_lists_and_dicts import ContainerConfig
from .helpers import ROOMY_SIZE, VALIDATE_KEY, index_of

FOLD_KEY = 'f2'
"""Key that folds every container away, or opens every one of them."""

DELAYS = 'retry_delays'
"""The member of the example that holds three whole numbers."""

LABELS = 'many_labels'
"""The member of the example that the editor opens folded."""


def _tree_app() -> EditorApp:
    """Return an application on the example with the containers in it."""
    return EditorApp(EditModel(ContainerConfig()))


def _all_names(app: EditorApp) -> list[str]:
    """Return the name of every node, in the order the rows are."""
    return [str(label.content) for label in app.query(Label)
            if label.has_class(NAME_CLASS)]


def _shown_names(app: EditorApp) -> list[str]:
    """Return the name of every node that is on the screen."""
    return [name for index, name in enumerate(_all_names(app))
            if app.query_one(f'#{member_id(index)}', Vertical).display]


def _fold_labels(app: EditorApp) -> list[str]:
    """Return what every fold control of the application shows."""
    return [str(button.label) for button in app.query(Button)]


async def _opened() -> tuple[list[str], list[str], list[str]]:
    """Return the names, the shown names and the fold labels at the start."""
    app = _tree_app()
    async with app.run_test(size=ROOMY_SIZE):
        return _all_names(app), _shown_names(app), _fold_labels(app)


def test_tree_of_rows() -> None:
    """Test a value inside a container is a row of its own."""
    names, _, _ = asyncio.run(_opened())
    assert names[:5] == ['project_name', DELAYS, '0', '1', '2']


def test_long_list_folded() -> None:
    """Test the long list of the example opens folded, and only that one."""
    _, shown, labels = asyncio.run(_opened())
    assert LABELS in shown
    # One for the first element of each of the two lists that opened.
    assert shown.count('0') == 2
    assert labels.count(FOLD_SHUT_TEXT) == 1
    assert labels.count(FOLD_OPEN_TEXT) == 3


async def _folded_one() -> tuple[list[str], list[str]]:
    """Press the control of the first container and report what is shown."""
    app = _tree_app()
    async with app.run_test(size=ROOMY_SIZE) as pilot:
        before = _shown_names(app)
        await pilot.click(f'#{fold_id(index_of(app, DELAYS))}')
        await pilot.pause()
        return before, _shown_names(app)


def test_control_folds_one() -> None:
    """Test the control of one container hides the rows below it."""
    before, after = asyncio.run(_folded_one())
    assert DELAYS in after
    assert len(after) < len(before)
    assert after.count('0') == 1


async def _indent_of(name: str) -> int:
    """Return how far from the left edge one node is laid out."""
    app = _tree_app()
    async with app.run_test(size=ROOMY_SIZE):
        index = index_of(app, name)
        member = app.query_one(f'#{member_id(index)}', Vertical)
        return int(member.styles.padding.left)


def test_value_is_indented() -> None:
    """Test a value inside a container is indented once for that container."""
    assert asyncio.run(_indent_of(DELAYS)) == 0
    assert asyncio.run(_indent_of('http')) == TREE_INDENT


async def _fold_all(key: str) -> tuple[list[str], list[str]]:
    """Press the fold key twice and report what is shown after each press."""
    app = _tree_app()
    async with app.run_test(size=ROOMY_SIZE) as pilot:
        await pilot.press(key)
        await pilot.pause()
        folded = _shown_names(app)
        await pilot.press(key)
        await pilot.pause()
        return folded, _shown_names(app)


def test_fold_key_folds_all() -> None:
    """Test the key folds every container and then opens every one.

    Opening every one of them shows more than the editor opened with, because
    the long list of the example started folded.
    """
    folded, opened = asyncio.run(_fold_all(FOLD_KEY))
    assert 'http' not in folded
    assert folded == ['project_name', DELAYS, 'report_formats', 'ports',
                      LABELS]
    assert 'http' in opened
    assert len(opened) > len(folded)


async def _fold_name(key: str) -> tuple[str, str]:
    """Return what the fold action is called before and after one press."""
    app = _tree_app()
    async with app.run_test(size=ROOMY_SIZE) as pilot:
        before = _named_fold(app)
        await pilot.press(key)
        await pilot.pause()
        return before, _named_fold(app)


def _named_fold(app: EditorApp) -> str:
    """Return what the footer calls the fold action as things stand."""
    return next(binding.description
                for (_, binding, _, _) in app.screen.active_bindings.values()
                if binding.action == 'fold')


def test_fold_action_renamed() -> None:
    """Test the action is named for what the next press of it will do."""
    assert asyncio.run(_fold_name(FOLD_KEY)) == (FOLD_COMMAND, OPEN_COMMAND)


async def _flat_buttons() -> tuple[list[str], bool]:
    """Return the controls and the folding of a configuration with none."""
    app = EditorApp(EditModel(FlatConfig()))
    async with app.run_test(size=ROOMY_SIZE):
        actions = {binding.action for (_, binding, _, _)
                   in app.screen.active_bindings.values()}
        return _fold_labels(app), 'fold' in actions


def test_nothing_to_fold() -> None:
    """Test a configuration of plain values is offered no folding at all.

    A control that could never do anything would be offering something that
    is not there, and the column of the controls would be width taken from
    the values for nothing.
    """
    assert asyncio.run(_flat_buttons()) == ([], False)


async def _rebuilt() -> tuple[list[str], list[str]]:
    """Type a duplicate into the sorted list and validate it."""
    app = _tree_app()
    async with app.run_test(size=ROOMY_SIZE) as pilot:
        first = index_of(app, 'report_formats') + 1
        app.query_one(f'#{value_id(first)}', Input).value = 'json'
        await pilot.pause()
        before = _all_names(app)
        await pilot.press(VALIDATE_KEY)
        await pilot.pause()
        return before, _all_names(app)


def test_rows_mounted_again() -> None:
    """Test the rows are made again when a pass leaves the model with others.

    The de-duplicating validator of the example removes a value, so the row
    that held it has to go: a backend that wrote into the widgets it had
    would be showing a value that is not in the buffer any more.
    """
    before, after = asyncio.run(_rebuilt())
    assert len(after) == len(before) - 1
