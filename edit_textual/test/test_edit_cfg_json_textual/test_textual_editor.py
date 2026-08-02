#! /usr/bin/env python3
"""Tests for the Textual backend, driven headlessly.

Textual runs headlessly in process, so the equivalent of a withdrawn Tk
window is available everywhere, including on a machine with no display.
`App.run_test()` is an asynchronous context manager, and it is driven from
an ordinary test function with `asyncio.run`, which keeps the test session
free of an extra asynchronous test plugin.

The configuration class comes from the example rather than from a class of
its own, so that the same flat configuration is used by the core tests, by
both backends and by the example itself.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import asyncio
from textual.widgets import Static
from edit_cfg_json import EditModel, EditorBackend
from edit_cfg_json_textual import TextualEditor
from edit_cfg_json_textual.textual_editor import EditorApp, VALUE_ID_PREFIX
from example.e01_flat_config import FlatConfig

EXPECTED_VALUES = {'name': 'flat example', 'answer': '42'}
"""Value text that the application is expected to show for each member."""


def _value_text(app: EditorApp, member_name: str) -> str:
    """Return the text that the application shows for one member."""
    widget = app.query_one(f'#{VALUE_ID_PREFIX}{member_name}', Static)
    return str(widget.content)


async def _drive_app() -> tuple[str, dict[str, str], bool]:
    """Run the application headlessly and quit it with its key binding.

    Returns:
        The application title, the shown value of every member, and whether
        the application was still running after the quit key was pressed.
    """
    app = EditorApp(EditModel(FlatConfig()))
    async with app.run_test() as pilot:
        title = app.title
        shown = {name: _value_text(app, name) for name in EXPECTED_VALUES}
        await pilot.press('q')
        await pilot.pause()
        return title, shown, app.is_running


def test_app_shows_model() -> None:
    """Test the application is named after the class and shows every row."""
    title, shown, still_running = asyncio.run(_drive_app())
    assert title == 'FlatConfig'
    assert shown == EXPECTED_VALUES
    assert not still_running


def test_is_editor_backend() -> None:
    """Test TextualEditor can be used where an EditorBackend is expected."""
    backend: EditorBackend = TextualEditor()
    assert hasattr(backend, 'run_editor')
