#! /usr/bin/env python3
"""Tests for example e14_embedded_textual.

This example has no `--ui dump` either, and for the same reason as example 13:
what it teaches is where the editor is on a screen, and a printout has no
screen to be one part of. Textual runs headlessly in process, so these drive
the real application on a machine with no display at all.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from collections.abc import Awaitable, Callable
from pathlib import Path
import asyncio
import json
import pytest
from textual.app import App
from textual.pilot import Pilot
from textual.widgets import Input, Label, Static
from edit_cfg_json_textual import EditorPanel
from edit_cfg_json_textual.textual_look import DOCSTRING_ID, TITLE_ID, \
    value_id
from example import e14_embedded_textual
from example.cmd_line import SESSION_SAVED
from example.e14_embedded_textual import FIELD_ID, FIELD_KEY, PipelineApp, \
    TOLD_ID
from .helpers import DATA_FOLDER

DATA_NAME = 'e13_pipeline.json'
"""Input file of this example, which is example 13's own."""

APP_SIZE = (100, 40)
"""Terminal size with room for the application and the editor together."""

SAVE_KEY = 'ctrl+s'
"""Key that saves in the editor and that the application also reads."""


def _run(monkeypatch: pytest.MonkeyPatch,
         driving: Callable[[PipelineApp, Pilot[None]], Awaitable[None]],
         *settings: str) -> None:
    """Run the example headlessly and drive the application it started.

    `App.run` is replaced rather than the application being built here, so
    that what is driven is what the example's own `main` puts together.

    Args:
        monkeypatch: The pytest fixture that replaces `App.run`.
        driving: What to do with the application once it is running.
        settings: Command line arguments of the run.
    """
    async def started(app: PipelineApp) -> None:
        """Run one application headlessly and drive it."""
        async with app.run_test(size=APP_SIZE) as pilot:
            await pilot.pause()
            await driving(app, pilot)

    def run_headless(app: App[None]) -> None:
        """Stand in for App.run by running the application headlessly."""
        assert isinstance(app, PipelineApp)
        asyncio.run(started(app))
    monkeypatch.setattr(App, 'run', run_headless)
    e14_embedded_textual.main(list(settings))


def _label(app: PipelineApp) -> str:
    """Return the label that the editor shows for the whole model."""
    return str(app.screen.query_one(f'#{TITLE_ID}', Static).content)


def _told(app: PipelineApp) -> str:
    """Return what the application itself is saying on its own line."""
    return str(app.query_one(f'#{TOLD_ID}', Label).content)


def test_panel_is_mounted(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test the application's screen holds its own widgets and the editor."""
    async def look(app: PipelineApp, pilot: Pilot[None]) -> None:
        """Check that both are there."""
        _ = pilot
        assert app.query(f'#{FIELD_ID}')
        assert app.query(EditorPanel)
        assert _label(app) == 'PipelineConfig'
    _run(monkeypatch, look)


def test_screen_is_pushed(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test the run that asks for a screen gets the editor on one."""
    async def look(app: PipelineApp, pilot: Pilot[None]) -> None:
        """Check that the editor is a screen above the application's."""
        _ = pilot
        assert len(app.screen_stack) == 2
        assert _label(app) == 'PipelineConfig'
    _run(monkeypatch, look, '--mount', 'screen')


def test_application_key(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test a key pressed in the application's own field stays there.

    Textual offers a key from the widget that has the focus upwards, and the
    application's own field is not inside the editor, so the editor never sees
    this one.
    """
    async def press(app: PipelineApp, pilot: Pilot[None]) -> None:
        """Put the focus in the application's field and press its key."""
        app.query_one(f'#{FIELD_ID}', Input).focus()
        await pilot.pause()
        await pilot.press(SAVE_KEY)
        await pilot.pause()
        assert _told(app) == e14_embedded_textual.APP_KEY_TEXT
    _run(monkeypatch, press)


async def _explained(app: PipelineApp, pilot: Pilot[None]) -> bool:
    """Press the fought-over key in a field of the editor and see who won.

    Args:
        app: Application that is running.
        pilot: Driver of that application.

    Returns:
        Whether the editor acted on the key, which is what its explain action
        showing less of the class docstring means.
    """
    app.screen.query_one(f'#{value_id(0)}', Input).focus()
    await pilot.pause()
    docstring = app.screen.query_one(f'#{DOCSTRING_ID}', Static)
    before = str(docstring.content)
    await pilot.press(FIELD_KEY)
    await pilot.pause()
    return str(docstring.content) != before


def test_priority_key_wins(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test the editor is offered its key before the field that has focus."""
    async def press(app: PipelineApp, pilot: Pilot[None]) -> None:
        """Press the key and check that the editor acted on it."""
        assert await _explained(app, pilot)
    _run(monkeypatch, press)


def test_ordinary_key_lost(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test the flag gives that same key to the field that has the focus."""
    async def press(app: PipelineApp, pilot: Pilot[None]) -> None:
        """Press the key and check that the editor did not act on it."""
        assert not await _explained(app, pilot)
    _run(monkeypatch, press, '--ordinary-keys')


def test_closing_tells(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test the application's own key closes the editor and is told."""
    async def close(app: PipelineApp, pilot: Pilot[None]) -> None:
        """Press the application's own close key and look at both."""
        await pilot.press('f8')
        await pilot.pause()
        assert not app.query(EditorPanel)
        assert 'closed' in _told(app)
    _run(monkeypatch, close)


def test_screen_pops(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test closing a pushed editor gives the application its screen back."""
    async def close(app: PipelineApp, pilot: Pilot[None]) -> None:
        """Press the close key and check the stack and the line below."""
        await pilot.press('f8')
        await pilot.pause()
        await pilot.pause()
        assert len(app.screen_stack) == 1
        assert 'closed' in _told(app)
    _run(monkeypatch, close, '--mount', 'screen')


def test_file_is_read(monkeypatch: pytest.MonkeyPatch, tmp_path: Path,
                      capsys: pytest.CaptureFixture[str]) -> None:
    """Test the application reads the file it was given and can write it.

    The model is the application's own here, so this is what says that the
    two statements the example shows really do build one. It writes somewhere
    else than it read, so that nothing is overwritten and the editor has no
    reason to ask about a file: what a save does to the file it writes over is
    example 12's, and it is the same editor here.
    """
    out_file = tmp_path / 'pipeline.json'

    async def save(app: PipelineApp, pilot: Pilot[None]) -> None:
        """Edit one value in the editor and press the save key in it.

        The focus is moved into the editor first, because the application
        itself reads this combination and the application's own field is the
        one the terminal opens on.
        """
        field = app.screen.query_one(f'#{value_id(0)}', Input)
        field.focus()
        await pilot.pause()
        field.value = 'renamed'
        await pilot.pause()
        await pilot.press(SAVE_KEY)
        await pilot.pause()
    _run(monkeypatch, save, '-i', str(DATA_FOLDER / DATA_NAME), '-o',
         str(out_file))
    assert json.loads(out_file.read_text(encoding='UTF-8')) == \
        {'name': 'renamed', 'workers': 8}
    assert SESSION_SAVED.format(
        name='PipelineConfig') in capsys.readouterr().out
