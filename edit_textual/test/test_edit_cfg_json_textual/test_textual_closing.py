#! /usr/bin/env python3
"""Tests for closing the Textual editor with something left unsaved.

Quitting writes nothing, so a buffer holding something that has not reached
the file loses it. What is asked about that and whether there is anything to
ask about are the core's, and tested there; what is here is that this backend
puts the question, that it stays open until the question is answered, and that
each answer does what it says.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from pathlib import Path
from typing import NamedTuple
import asyncio
from textual.widgets import Label
from edit_cfg_json import EditModel
from edit_cfg_json_textual.textual_ask import NO_ID, YES_ID
from edit_cfg_json_textual.textual_editor import EditorApp
from edit_cfg_json_textual.textual_look import ASK_BOX_ID
from example.e01_flat_config import FlatConfig
from .helpers import ESCAPE_KEY, QUIT_KEY, SAVE_KEY, VALIDATE_KEY, \
    answer_with, field_of, model_value, verdict_of

TYPED_ANSWER = '7'
"""What the stand-in user types into the number member before closing."""


class Closing(NamedTuple):
    """What one attempt to close the editor left behind."""

    asked: bool
    """Whether the question about the changes was on the screen."""

    running: bool
    """Whether the editor was still there afterwards."""


async def _quit_after(app: EditorApp, typed: bool,
                      answers: tuple[str, ...] = ()) -> Closing:
    """Run the application headlessly, edit it, quit it and answer.

    Args:
        app: Application to run.
        typed: Whether the stand-in user changes a value first.
        answers: Selectors of the controls to press, and keys to press, after
            the quit key. A selector is told from a key by its `#`.

    Returns:
        Whether the question was asked and whether the editor is still there.
    """
    async with app.run_test() as pilot:
        if typed:
            field_of(app, 'answer').value = TYPED_ANSWER
            await pilot.pause()
        await pilot.press(QUIT_KEY)
        await pilot.pause()
        asked = bool(app.screen.query(f'#{ASK_BOX_ID}'))
        for answer in answers:
            await answer_with(pilot, answer)
        return Closing(asked=asked, running=app.is_running)


def test_clean_quit_is_quiet() -> None:
    """Test a buffer nobody has touched is closed without a question."""
    closing = asyncio.run(_quit_after(EditorApp(EditModel(FlatConfig())),
                                      typed=False))
    assert not closing.asked
    assert not closing.running


def test_edited_quit_asks() -> None:
    """Test an unsaved change is asked about and leaves the editor open."""
    closing = asyncio.run(_quit_after(EditorApp(EditModel(FlatConfig())),
                                      typed=True))
    assert closing.asked
    assert closing.running


def test_question_says_what() -> None:
    """Test the question is the one the core words, and not this backend."""
    async def asked() -> str:
        """Run the application, quit it, and read what it asks."""
        app = EditorApp(EditModel(FlatConfig()))
        async with app.run_test() as pilot:
            field_of(app, 'answer').value = TYPED_ANSWER
            await pilot.pause()
            await pilot.press(QUIT_KEY)
            await pilot.pause()
            return str(app.screen.query_one(Label).content)
    assert asyncio.run(asked()) == \
        'These changes have not been saved. Close the editor and discard them?'


def test_keeping_stays_open() -> None:
    """Test the control that keeps the changes leaves the editor as it was."""
    model = EditModel(FlatConfig())
    closing = asyncio.run(_quit_after(EditorApp(model), typed=True,
                                      answers=(f'#{NO_ID}',)))
    assert closing.running
    assert model_value(model, 'answer') == int(TYPED_ANSWER)


def test_leaving_stays_open() -> None:
    """Test the key that leaves a question of this editor keeps it too."""
    closing = asyncio.run(_quit_after(EditorApp(EditModel(FlatConfig())),
                                      typed=True, answers=(ESCAPE_KEY,)))
    assert closing.running


def test_discarding_ends_it() -> None:
    """Test the control that drops the changes is what ends the session."""
    closing = asyncio.run(_quit_after(EditorApp(EditModel(FlatConfig())),
                                      typed=True, answers=(f'#{YES_ID}',)))
    assert not closing.running


def test_quiet_after_save(tmp_path: Path) -> None:
    """Test a change that reached the file is not asked about."""
    async def saved_and_quit() -> Closing:
        """Type, save, and then quit."""
        app = EditorApp(EditModel(FlatConfig(),
                                  out_file=tmp_path / 'out.json'))
        async with app.run_test() as pilot:
            field_of(app, 'answer').value = TYPED_ANSWER
            await pilot.pause()
            await pilot.press(SAVE_KEY)
            await pilot.pause()
            await pilot.press(QUIT_KEY)
            await pilot.pause()
            return Closing(asked=bool(app.screen.query(f'#{ASK_BOX_ID}')),
                           running=app.is_running)
    closing = asyncio.run(saved_and_quit())
    assert not closing.asked
    assert not closing.running


def test_question_is_modal() -> None:
    """Test the keys of the editor do nothing while this question is up.

    The editor turns its own actions off while a question is open, because
    Textual goes on offering an application its priority bindings from the
    whole binding chain while a modal screen is up. Without that, one more
    quit would stack a second question on the first.
    """
    async def pressed() -> tuple[int, bool, str]:
        """Ask the question and then press every key of the editor."""
        app = EditorApp(EditModel(FlatConfig()))
        async with app.run_test() as pilot:
            field_of(app, 'answer').value = TYPED_ANSWER
            await pilot.pause()
            for key in (QUIT_KEY, QUIT_KEY, VALIDATE_KEY):
                await pilot.press(key)
                await pilot.pause()
            return len(app.screen_stack), app.is_running, verdict_of(app)
    depth, running, verdict = asyncio.run(pressed())
    assert depth == 2
    assert running
    assert verdict == 'validation: not validated'
