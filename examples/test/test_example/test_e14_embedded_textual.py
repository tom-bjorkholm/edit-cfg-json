#! /usr/bin/env python3
"""Tests for example e14_embedded_textual.

The editor is mounted in an area of the application's own screen when its
button is pressed, so these press that button headlessly and then look at what
appeared, and at what is left when the editor closes. Textual runs in process,
so they run on a machine with no display at all.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from pathlib import Path
import pytest
from textual.app import App
from textual.pilot import Pilot
from edit_cfg_json_textual import EditorPanel
from example import e14_embedded_textual
from example._shared_pipeline import CLOSE_TEXT, EDIT_TEXT, SESSION_NOTHING
from . import helpers


def test_area_starts_empty(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test the application shows no editor until its button is pressed."""
    async def look(app: App[None], pilot: Pilot[None]) -> None:
        """Check that no editor is on the screen yet."""
        _ = pilot
        assert not app.query(EditorPanel)
    helpers.run_textual_app(e14_embedded_textual.main, monkeypatch, look)


def test_panel_is_mounted(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test pressing the button mounts the editor in the area."""
    async def look(app: App[None], pilot: Pilot[None]) -> None:
        """Press the button and read the label of the editor."""
        await helpers.press_own_button(app, pilot, EDIT_TEXT)
        assert app.query(EditorPanel)
        assert helpers.editor_title(app) == 'PipelineConfig'
    helpers.run_textual_app(e14_embedded_textual.main, monkeypatch, look)


def test_closing_clears_area(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test the application's own control closes the editor and is told.

    `close` is what an application that mounted the editor has for that, and
    an application with a question of its own to put passes False to it.
    """
    async def close(app: App[None], pilot: Pilot[None]) -> None:
        """Close the editor from the application and see the area emptied."""
        await helpers.press_own_button(app, pilot, EDIT_TEXT)
        await helpers.press_own_button(app, pilot, CLOSE_TEXT)
        assert not app.query(EditorPanel)
        assert helpers.own_status(app) == SESSION_NOTHING
    helpers.run_textual_app(e14_embedded_textual.main, monkeypatch, close)


def test_field_gets_key_first(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test the field is offered `ctrl+e` first, and `f1` still explains.

    This application says `priority_keys=False`, and it says it on a
    combination that Textual's own field reads for itself, so the editor is
    offered `ctrl+e` only after the field has had it and never sees it. A key
    no field claims reaches the editor either way.
    """
    async def press(app: App[None], pilot: Pilot[None]) -> None:
        """Press both keys with the focus in a field of the editor."""
        await helpers.press_own_button(app, pilot, EDIT_TEXT)
        await helpers.focus_editor(app, pilot)
        shown = helpers.editor_docstring(app)
        await pilot.press('ctrl+e')
        assert helpers.editor_docstring(app) == shown
        await pilot.press('f1')
        assert helpers.editor_docstring(app) != shown
    helpers.run_textual_app(e14_embedded_textual.main, monkeypatch, press)


def test_file_is_read(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    """Test the editor reads the file the example was given, and writes it.

    It writes somewhere else than it read, so that nothing is overwritten and
    the editor has no reason to ask about a file.
    """
    out_file = tmp_path / 'pipeline.json'

    async def save(app: App[None], pilot: Pilot[None]) -> None:
        """Mount the editor, edit one value and press its save key."""
        await helpers.press_own_button(app, pilot, EDIT_TEXT)
        await helpers.edit_and_save(app, pilot, 'renamed')
    example_main = e14_embedded_textual.main
    in_file = helpers.data_file(helpers.PIPELINE_FILE)
    helpers.run_textual_app(example_main, monkeypatch, save, '-i', in_file,
                            '-o', str(out_file))
    assert helpers.written_json(out_file) == {'name': 'renamed', 'workers': 8}
