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
from config_as_json import JsonType
import pytest
from textual.app import App, ComposeResult
from textual.widgets import Input, Static
from edit_cfg_json import EditModel, EditorBackend
from edit_cfg_json_textual import TextualEditor
from edit_cfg_json_textual.textual_editor import EditorApp, MARK_ID_PREFIX, \
    QUIT_KEY, VALIDATE_ALT_KEY, VALIDATE_KEY, VALUE_ID_PREFIX, VERDICT_ID, \
    plain_widget
from example.e01_flat_config import FlatConfig

EXPECTED_VALUES = {'name': 'Flat example', 'answer': '42'}
"""Value text that the application is expected to show for each member."""

UNKNOWN_VERDICT = 'validation: not validated'
"""Text the editor shows before anything has been validated."""

VALID_VERDICT = 'validation: valid'
"""Text the editor shows for a buffer the application would accept."""

REWRITTEN_MARK = ' (edited) (changed by validator)'
"""Mark of a member that the user changed and a validator then rewrote."""

MARKUP_TEXT = 'value [red on blue]here[/] is refused'
"""Text of a configuration that happens to look like console markup."""


class MarkupProbe(App[None]):
    """An application showing one text that looks like console markup."""

    def compose(self) -> ComposeResult:
        """Create the one widget that is under test."""
        yield plain_widget(MARKUP_TEXT, 'probe')


def _field(app: EditorApp, member_name: str) -> Input:
    """Return the field that the application shows for one member."""
    return app.query_one(f'#{VALUE_ID_PREFIX}{member_name}', Input)


def _mark(app: EditorApp, member_name: str) -> str:
    """Return the mark that the application shows for one member."""
    widget = app.query_one(f'#{MARK_ID_PREFIX}{member_name}', Static)
    return str(widget.content)


def _verdict(app: EditorApp) -> str:
    """Return the validation text that the application shows."""
    return str(app.query_one(f'#{VERDICT_ID}', Static).content)


def _model_value(model: EditModel, name: str) -> JsonType:
    """Return the value that the buffer holds for one member."""
    return {row.name: row.value for row in model.rows}[name]


async def _drive_app() -> tuple[str, dict[str, str], str, bool]:
    """Run the application headlessly and quit it with its key binding.

    Returns:
        The application title, the shown value of every member, the shown
        validation text, and whether the application was still running after
        the quit key was pressed.
    """
    app = EditorApp(EditModel(FlatConfig()))
    async with app.run_test() as pilot:
        title = app.title
        shown = {name: _field(app, name).value for name in EXPECTED_VALUES}
        verdict = _verdict(app)
        await pilot.press(QUIT_KEY)
        await pilot.pause()
        return title, shown, verdict, app.is_running


async def _type_into_answer(key: str) -> tuple[JsonType, str]:
    """Run the application headlessly and type one key into a field.

    Args:
        key: Key to press while the field of the answer member has focus.

    Returns:
        The value the buffer holds for that member, and the title.
    """
    model = EditModel(FlatConfig())
    app = EditorApp(model)
    async with app.run_test() as pilot:
        _field(app, 'answer').focus()
        await pilot.pause()
        await pilot.press(key)
        await pilot.pause()
        return _model_value(model, 'answer'), app.title


async def _validate_with(member_name: str, text: str,
                         key: str = VALIDATE_KEY) -> tuple[str, str, str]:
    """Run the application headlessly, set one field and validate.

    Args:
        member_name: Member whose field is written into.
        text: Text to put in that field, replacing what is there.
        key: Key that is pressed to validate.

    Returns:
        The validation text, the text the field shows afterwards, and the
        mark of that member.
    """
    app = EditorApp(EditModel(FlatConfig()))
    async with app.run_test() as pilot:
        _field(app, member_name).value = text
        # The field keeps the focus while the key is pressed, which is the
        # situation the editor is really in: a user validates what has just
        # been typed without leaving the field first.
        _field(app, member_name).focus()
        await pilot.pause()
        await pilot.press(key)
        await pilot.pause()
        return (_verdict(app), _field(app, member_name).value,
                _mark(app, member_name))


async def _edit_after_validate() -> str:
    """Run the application headlessly, validate and then edit a field.

    Returns:
        The validation text the application shows after the edit.
    """
    app = EditorApp(EditModel(FlatConfig()))
    async with app.run_test() as pilot:
        await pilot.press(VALIDATE_KEY)
        await pilot.pause()
        _field(app, 'answer').value = '7'
        await pilot.pause()
        return _verdict(app)


def test_app_shows_model() -> None:
    """Test the application is named after the class and shows every row."""
    title, shown, verdict, still_running = asyncio.run(_drive_app())
    assert title == 'FlatConfig'
    assert shown == EXPECTED_VALUES
    assert verdict == UNKNOWN_VERDICT
    assert not still_running


def test_typing_edits_model() -> None:
    """Test a key typed into a field reaches the model as a value."""
    value, title = asyncio.run(_type_into_answer('7'))
    assert value == 427
    assert title == 'FlatConfig *'


def test_typing_not_a_number() -> None:
    """Test a field that is not a number yet is still kept by the model."""
    value, title = asyncio.run(_type_into_answer('x'))
    assert value == '42x'
    assert title == 'FlatConfig *'


@pytest.mark.parametrize('key', [VALIDATE_KEY, VALIDATE_ALT_KEY])
def test_validate_accepts(key: str) -> None:
    """Test either validate key reports a buffer the application accepts.

    Both keys are tried because a keyboard or a terminal that does not
    deliver one of them is exactly why there are two.
    """
    verdict, shown, mark = asyncio.run(_validate_with('answer', '7', key))
    assert verdict == VALID_VERDICT
    assert shown == '7'
    assert mark == ' (edited)'


@pytest.mark.parametrize('key', [VALIDATE_KEY, VALIDATE_ALT_KEY])
def test_key_not_typed(key: str) -> None:
    """Test a validate key is not typed into the field that has the focus."""
    verdict, shown, mark = asyncio.run(_validate_with('name', 'Typed', key))
    assert shown == 'Typed'
    assert verdict == VALID_VERDICT
    assert mark == ' (edited)'


def test_validate_refuses() -> None:
    """Test the validate key shows why the application refused a value."""
    verdict, shown, mark = asyncio.run(_validate_with('answer', '500'))
    assert 'validation: invalid' in verdict
    assert 'greater than maximum 100' in verdict
    assert shown == '500'
    assert mark == ' (edited)'


def test_validate_rewrites() -> None:
    """Test a value a validator rewrote reaches the field and the mark."""
    verdict, shown, mark = asyncio.run(_validate_with('name', 'other'))
    assert verdict == VALID_VERDICT
    assert shown == 'Other'
    assert mark == REWRITTEN_MARK


def test_edit_after_validate() -> None:
    """Test an edit puts the editor back to not having been validated."""
    assert asyncio.run(_edit_after_validate()) == UNKNOWN_VERDICT


async def _shown_markup() -> str:
    """Run the probe application and return what its widget really shows."""
    app = MarkupProbe()
    async with app.run_test():
        return str(app.query_one('#probe', Static).visual)


def test_markup_shown_as_text() -> None:
    """Test text that looks like console markup is shown as it is.

    A configuration value or a diagnostic may contain square brackets, and
    Textual would otherwise read them as a style and quietly drop both the
    brackets and the text between them.
    """
    assert asyncio.run(_shown_markup()) == MARKUP_TEXT


def test_is_editor_backend() -> None:
    """Test TextualEditor can be used where an EditorBackend is expected."""
    backend: EditorBackend = TextualEditor()
    assert hasattr(backend, 'run_editor')
