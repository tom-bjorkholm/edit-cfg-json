#! /usr/bin/env python3
"""Tests for saving from the Textual backend, and for the file it asks for."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from pathlib import Path
import asyncio
import pytest
from textual.app import App
from textual.geometry import Region
from textual.widgets import Input
from edit_cfg_json import EditModel, EditorBackend
from edit_cfg_json_textual import TextualEditor
from edit_cfg_json_textual import edit as textual_edit
from edit_cfg_json_textual.textual_ask import NO_ID, YES_ID
from edit_cfg_json_textual.textual_editor import EditorApp
from edit_cfg_json_textual.textual_look import ASK_BOX_ID, SAVE_AS_ID
from example.e01_flat_config import FlatConfig
from .helpers import ESCAPE_KEY, EXPLAIN_KEY, NARROW_SIZE, \
    NO_FILE_TEXT, QUIT_KEY, REFUSED_VERDICT, ROOMY_SIZE, SAVE_AS_KEY, \
    SAVE_KEY, VALIDATE_KEY, VALID_VERDICT, answer_with, described_app, \
    docstring_of, field_of, save_as, saving_of, verdict_of, written


async def _save_with(model: EditModel, member_name: str = 'answer',
                     text: str = '7') -> tuple[str, str, str]:
    """Run the application headlessly, edit one field and press Save.

    Args:
        model: Model to run the application on.
        member_name: Member whose field is written into.
        text: Text to put in that field, replacing what is there.

    Returns:
        The saving text, the validation text, and the title.
    """
    app = EditorApp(model)
    async with app.run_test() as pilot:
        field_of(app, member_name).value = text
        await pilot.pause()
        await pilot.press(SAVE_KEY)
        await pilot.pause()
        return saving_of(app), verdict_of(app), app.title


def test_save_writes(tmp_path: Path) -> None:
    """Test the save key writes the edited values to the output file."""
    out_file = tmp_path / 'out.json'
    model = EditModel(FlatConfig(), out_file=out_file)
    saving, verdict, title = asyncio.run(_save_with(model))
    assert saving == f'Saved to {out_file}.'
    assert verdict == VALID_VERDICT
    assert title == 'FlatConfig'
    assert written(out_file) == {'name': 'Flat example', 'answer': 7}


def test_save_refused(tmp_path: Path) -> None:
    """Test an invalid buffer is not written, and the verdict says why."""
    out_file = tmp_path / 'out.json'
    model = EditModel(FlatConfig(), out_file=out_file)
    saving, verdict, title = asyncio.run(_save_with(model, text='500'))
    assert 'cannot be saved' in saving
    assert verdict == REFUSED_VERDICT
    assert title == 'FlatConfig *'
    assert not out_file.exists()


def test_save_rewrites(tmp_path: Path) -> None:
    """Test a value a validator rewrote is what reaches the file.

    Saving validates, so it rewrites what validating would rewrite, and the
    field is refreshed to show what really went into the file.
    """
    out_file = tmp_path / 'out.json'
    model = EditModel(FlatConfig(), out_file=out_file)
    saving, _, _ = asyncio.run(_save_with(model, 'name', 'other'))
    assert saving == f'Saved to {out_file}.'
    assert written(out_file) == {'name': 'Other', 'answer': 42}


def test_destination_shown(tmp_path: Path) -> None:
    """Test a session with a file says where it would write, before saving."""
    out_file = tmp_path / 'out.json'

    async def shown() -> str:
        """Run the application and read what it says about saving."""
        app = EditorApp(EditModel(FlatConfig(), out_file=out_file))
        async with app.run_test():
            return saving_of(app)
    assert asyncio.run(shown()) == f'save to: {out_file}'


def test_no_destination_shown() -> None:
    """Test a session with no file says that rather than saying nothing."""
    async def shown() -> str:
        """Run the application and read what it says about saving."""
        app = EditorApp(EditModel(FlatConfig()))
        async with app.run_test():
            return saving_of(app)
    assert asyncio.run(shown()) == NO_FILE_TEXT


def test_save_as_writes(tmp_path: Path) -> None:
    """Test Save as asks which file to write and then writes it."""
    out_file = tmp_path / 'chosen.cfg'
    model = EditModel(FlatConfig())
    assert asyncio.run(save_as(model, str(out_file))) == \
        f'Saved to {out_file}.'
    assert model.out_file == str(out_file)
    assert written(out_file) == {'name': 'Flat example', 'answer': 42}


def test_save_as_cancelled(tmp_path: Path) -> None:
    """Test leaving the question unanswered chooses nothing and writes it."""
    out_file = tmp_path / 'chosen.cfg'
    model = EditModel(FlatConfig())
    assert asyncio.run(save_as(model, str(out_file),
                               answer=ESCAPE_KEY)) == NO_FILE_TEXT
    assert model.out_file is None
    assert not out_file.exists()


def test_save_as_empty(tmp_path: Path) -> None:
    """Test an empty answer is the same as no answer at all.

    There is no file whose name is nothing, so an empty field cannot become
    a destination.
    """
    _ = tmp_path
    model = EditModel(FlatConfig())
    assert asyncio.run(save_as(model, '')) == NO_FILE_TEXT
    assert model.out_file is None


def test_save_asks_when_none(tmp_path: Path) -> None:
    """Test Save asks where to write when the session has no file yet.

    That is what every editor does, and it is the reason a model may be
    built with no destination at all.
    """
    out_file = tmp_path / 'asked.json'
    model = EditModel(FlatConfig())
    assert asyncio.run(save_as(model, str(out_file), key=SAVE_KEY)) == \
        f'Saved to {out_file}.'
    assert out_file.exists()


def _there(tmp_path: Path) -> Path:
    """Return an output file that already holds a configuration.

    It is one that this class would accept, so that the save which follows is
    refused by nothing but the answer the test gives to the question.
    """
    out_file = tmp_path / 'out.json'
    out_file.write_text('{"name": "Was there", "answer": 1}', encoding='UTF-8')
    return out_file


async def _save_over(model: EditModel, answer: str,
                     presses: int = 1) -> tuple[str, int]:
    """Run the application, press Save and answer the question about the file.

    Args:
        model: Model to run the application on.
        answer: Selector of the control to press, or the key to press.
        presses: How many times Save is pressed, because the second press of
            one session is the one that is not asked about.

    Returns:
        What the editor says about saving afterwards, and how many times it
        asked.
    """
    app = EditorApp(model)
    asked = 0
    async with app.run_test() as pilot:
        for _ in range(presses):
            await pilot.press(SAVE_KEY)
            await pilot.pause()
            if app.screen.query(f'#{ASK_BOX_ID}'):
                asked += 1
                await answer_with(pilot, answer)
        return saving_of(app), asked


def test_overwrite_writes(tmp_path: Path) -> None:
    """Test the control that agrees writes the file and keeps what it held."""
    out_file = _there(tmp_path)
    saving, asked = asyncio.run(_save_over(
        EditModel(FlatConfig(), out_file=out_file), answer=f'#{YES_ID}'))
    assert asked == 1
    assert saving.startswith(f'Saved to {out_file}.')
    assert written(out_file) == {'name': 'Flat example', 'answer': 42}
    assert written(tmp_path / 'out.json.bak') == {'name': 'Was there',
                                                  'answer': 1}


@pytest.mark.parametrize('answer', [f'#{NO_ID}', ESCAPE_KEY])
def test_overwrite_left(tmp_path: Path, answer: str) -> None:
    """Test the answer that keeps the file leaves it exactly as it was.

    Leaving the question unanswered is the same answer, which is the rule
    every question of this editor follows.
    """
    out_file = _there(tmp_path)
    saving, asked = asyncio.run(_save_over(
        EditModel(FlatConfig(), out_file=out_file), answer=answer))
    assert asked == 1
    assert saving == f'save to: {out_file}'
    assert written(out_file) == {'name': 'Was there', 'answer': 1}
    assert not (tmp_path / 'out.json.bak').exists()


def test_overwrite_asked_once(tmp_path: Path) -> None:
    """Test the second save of one session is not asked about."""
    saving, asked = asyncio.run(_save_over(
        EditModel(FlatConfig(), out_file=_there(tmp_path)),
        answer=f'#{YES_ID}', presses=2))
    assert asked == 1
    assert saving == f'Saved to {tmp_path / "out.json"}.'


def test_no_file_no_question(tmp_path: Path) -> None:
    """Test writing a file that is not there yet asks nothing at all."""
    out_file = tmp_path / 'out.json'
    saving, asked = asyncio.run(_save_over(
        EditModel(FlatConfig(), out_file=out_file), answer=f'#{NO_ID}'))
    assert asked == 0
    assert saving == f'Saved to {out_file}.'


def test_save_as_starts_at(tmp_path: Path) -> None:
    """Test the question starts at the file that would be written now.

    Saving a copy beside the original is then a matter of changing a few
    characters rather than of typing a whole path.
    """
    out_file = tmp_path / 'out.json'

    async def shown() -> str:
        """Ask the question and read what its field starts with."""
        app = EditorApp(EditModel(FlatConfig(), out_file=out_file))
        async with app.run_test() as pilot:
            await pilot.press(SAVE_AS_KEY)
            await pilot.pause()
            return app.screen.query_one(f'#{SAVE_AS_ID}', Input).value
    assert asyncio.run(shown()) == str(out_file)


@pytest.mark.parametrize('size', [ROOMY_SIZE, NARROW_SIZE])
def test_save_as_on_screen(size: tuple[int, int]) -> None:
    """Test the question about the output file is laid out where it is seen.

    A terminal too narrow for it would otherwise lay it out beyond the edge
    of the screen, which is how the marks of a member went missing once.
    """
    async def placed() -> tuple[Region, Region]:
        """Ask the question and report where its box ended up."""
        app = EditorApp(EditModel(FlatConfig()))
        async with app.run_test(size=size) as pilot:
            await pilot.press(SAVE_AS_KEY)
            await pilot.pause()
            box = app.screen.query_one(f'#{ASK_BOX_ID}')
            return box.region, app.screen.region
    region, screen = asyncio.run(placed())
    assert screen.contains_region(region)


def test_question_is_modal() -> None:
    """Test the keys of the editor do nothing while the question is open.

    Textual dispatches a priority binding of an application from the whole
    chain rather than from the part of it above the last modal screen, so it
    goes on offering the editor its keys while the question is up. Without the
    editor turning its own actions off, one more Save would stack a second
    question on the first, and Quit would abandon the question altogether.
    """
    async def pressed() -> tuple[int, bool, str]:
        """Ask the question and then press every key of the editor."""
        app = described_app()
        async with app.run_test() as pilot:
            await pilot.press(SAVE_AS_KEY)
            await pilot.pause()
            for key in (SAVE_KEY, SAVE_AS_KEY, VALIDATE_KEY, EXPLAIN_KEY,
                        QUIT_KEY):
                await pilot.press(key)
                await pilot.pause()
            return len(app.screen_stack), app.is_running, docstring_of(app)
    depth, running, docstring = asyncio.run(pressed())
    assert depth == 2
    assert running
    assert docstring == EditModel(FlatConfig()).docstring


def test_keys_work_after(tmp_path: Path) -> None:
    """Test the keys of the editor work again once the question is gone."""
    out_file = tmp_path / 'out.json'

    async def answered() -> str:
        """Leave the question unanswered and then save the ordinary way."""
        app = EditorApp(EditModel(FlatConfig(), out_file=out_file))
        async with app.run_test() as pilot:
            await pilot.press(SAVE_AS_KEY)
            await pilot.pause()
            await pilot.press(ESCAPE_KEY)
            await pilot.pause()
            await pilot.press(SAVE_KEY)
            await pilot.pause()
            return saving_of(app)
    assert asyncio.run(answered()) == f'Saved to {out_file}.'


def _headless(save: bool) -> object:
    """Return a replacement for App.run that saves or only quits.

    Args:
        save: Whether the stand-in user presses Save before quitting.

    Returns:
        A function that can replace `App.run` for the duration of a test.
    """
    async def drive(app: App[None]) -> None:
        """Start the application headlessly and act as a user would."""
        async with app.run_test() as pilot:
            if save:
                await pilot.press(SAVE_KEY)
                await pilot.pause()
            await pilot.press(QUIT_KEY)

    def run_headless(app: App[None]) -> None:
        """Stand in for App.run, which needs a terminal."""
        asyncio.run(drive(app))
    return run_headless


def test_edit_returns_saved(monkeypatch: pytest.MonkeyPatch,
                            tmp_path: Path) -> None:
    """Test the edit of this package saves and gives the object back."""
    out_file = tmp_path / 'out.json'
    monkeypatch.setattr(App, 'run', _headless(save=True))
    saved = textual_edit(config=FlatConfig(), out_file=out_file)
    assert isinstance(saved, FlatConfig)
    assert written(out_file) == {'name': 'Flat example', 'answer': 42}


def test_edit_returns_none(monkeypatch: pytest.MonkeyPatch,
                           tmp_path: Path) -> None:
    """Test a session that only quits saves nothing and gives back None."""
    out_file = tmp_path / 'out.json'
    monkeypatch.setattr(App, 'run', _headless(save=False))
    assert textual_edit(config=FlatConfig(), out_file=out_file) is None
    assert not out_file.exists()


def test_is_editor_backend() -> None:
    """Test TextualEditor can be used where an EditorBackend is expected."""
    backend: EditorBackend = TextualEditor()
    assert hasattr(backend, 'run_editor')
