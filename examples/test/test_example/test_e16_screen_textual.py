#! /usr/bin/env python3
"""Tests for example e16_screen_textual.

Here the editor is pushed as a screen of its own, so these press the button of
the application and then look at the screen stack, at the editor on top of it,
and at the application's own screen being back when the editor closes.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from pathlib import Path
import pytest
from textual.app import App
from textual.pilot import Pilot
from example import e16_screen_textual
from example._shared_pipeline import CLOSE_TEXT, EDIT_TEXT, SESSION_NOTHING
from . import helpers


def test_one_screen_at_first(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test the application pushes nothing until its button is pressed."""
    async def look(app: App[None], pilot: Pilot[None]) -> None:
        """Check that the application's own screen is the only one."""
        _ = pilot
        assert len(app.screen_stack) == 1
    helpers.run_textual_app(e16_screen_textual.main, monkeypatch, look)


def test_screen_is_pushed(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test pressing the button puts the editor on a screen of its own."""
    async def look(app: App[None], pilot: Pilot[None]) -> None:
        """Press the button and read the label of the editor."""
        await helpers.press_own_button(app, pilot, EDIT_TEXT)
        assert len(app.screen_stack) == 2
        assert helpers.editor_title(app) == 'PipelineConfig'
    helpers.run_textual_app(e16_screen_textual.main, monkeypatch, look)


def test_screen_pops_itself(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test closing gives the application its own screen back, and says so.

    The application pops nothing itself: the editor was pushed as a screen, so
    taking that screen off again is the editor's to do.
    """
    async def close(app: App[None], pilot: Pilot[None]) -> None:
        """Close the editor from the application and see its screen go."""
        await helpers.press_own_button(app, pilot, EDIT_TEXT)
        await helpers.press_own_button(app, pilot, CLOSE_TEXT)
        assert len(app.screen_stack) == 1
        assert helpers.own_status(app) == SESSION_NOTHING
    helpers.run_textual_app(e16_screen_textual.main, monkeypatch, close)


def test_file_is_read(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    """Test the editor reads the file the example was given, and writes it."""
    out_file = tmp_path / 'pipeline.json'

    async def save(app: App[None], pilot: Pilot[None]) -> None:
        """Push the editor, edit one value and press its save key."""
        await helpers.press_own_button(app, pilot, EDIT_TEXT)
        await helpers.edit_and_save(app, pilot, 'renamed')
    example_main = e16_screen_textual.main
    in_file = helpers.data_file(helpers.PIPELINE_FILE)
    helpers.run_textual_app(example_main, monkeypatch, save, '-i', in_file,
                            '-o', str(out_file))
    assert helpers.written_json(out_file) == {'name': 'renamed', 'workers': 8}
