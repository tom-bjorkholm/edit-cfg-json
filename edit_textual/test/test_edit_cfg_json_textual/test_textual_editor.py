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

from pathlib import Path
import asyncio
import json
from config_as_json import JsonType
import pytest
from textual.app import App, ComposeResult
from textual.geometry import Region
from textual.widgets import Input, Static
from edit_cfg_json import EditModel, EditorBackend, LoadReport
from edit_cfg_json_textual import TextualEditor
from edit_cfg_json_textual import edit as textual_edit
from edit_cfg_json_textual.textual_editor import EditorApp, \
    LEAST_VALUE_WIDTH, LOAD_ID, MARK_ID_PREFIX, QUIT_KEY, SAVE_AS_BOX_ID, \
    SAVE_AS_COMMAND, SAVE_AS_ID, SAVE_AS_KEY, SAVE_COMMAND, SAVE_ID, \
    SAVE_KEY, VALIDATE_ALT_KEY, VALIDATE_COMMAND, VALIDATE_KEY, \
    VALUE_ID_PREFIX, VERDICT_ID, plain_widget
from example.e01_flat_config import FlatConfig

EXPECTED_VALUES = {'name': 'Flat example', 'answer': '42'}
"""Value text that the application is expected to show for each member."""

LOAD_MESSAGE = 'the file left something out'
"""Message of the load in the tests that show one."""

FILLED_REPORT = LoadReport(message=LOAD_MESSAGE, filled=frozenset({'answer'}))
"""Report of a load that filled the number member in from the default."""

FILLED_MARK = ' (filled from default)'
"""Mark of a member that the input file did not hold."""

UNKNOWN_VERDICT = 'validation: not validated'
"""Text the editor shows before anything has been validated."""

VALID_VERDICT = 'validation: valid'
"""Text the editor shows for a buffer the application would accept."""

REWRITTEN_MARK = ' (edited) (changed by validator)'
"""Mark of a member that the user changed and a validator then rewrote."""

MARKUP_TEXT = 'value [red on blue]here[/] is refused'
"""Text of a configuration that happens to look like console markup."""

ROOMY_SIZE = (100, 24)
"""Terminal size with room for the longest mark a member can carry."""

NARROW_SIZE = (40, 24)
"""Terminal size too narrow for the field and the marks together."""

NO_FILE_TEXT = 'save to: no file chosen yet'
"""Text the editor shows while no output file has been chosen."""

ENTER_KEY = 'enter'
"""Key that answers the question about the output file."""

ESCAPE_KEY = 'escape'
"""Key that leaves the question about the output file unanswered."""


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


def _saving(app: EditorApp) -> str:
    """Return the saving text that the application shows."""
    return str(app.query_one(f'#{SAVE_ID}', Static).content)


def _written(out_file: Path) -> object:
    """Return what one output file holds, as JSON space values."""
    return json.loads(out_file.read_text(encoding='UTF-8'))


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


async def _load_shown() -> tuple[str, str, str]:
    """Run the application on a model whose load filled a member in.

    Returns:
        What the application says about the load, the mark of the member the
        file did not hold, and the mark of the member it did hold.
    """
    app = EditorApp(EditModel(FlatConfig(), FILLED_REPORT))
    async with app.run_test():
        shown = str(app.query_one(f'#{LOAD_ID}', Static).content)
        return shown, _mark(app, 'answer'), _mark(app, 'name')


async def _no_load_widget() -> bool:
    """Run the application without a load and look for its widget.

    Returns:
        Whether a widget for the load was created anyway.
    """
    app = EditorApp(EditModel(FlatConfig()))
    async with app.run_test():
        return bool(app.query(f'#{LOAD_ID}'))


def test_load_message_shown() -> None:
    """Test the editor shows what reading the input file did, and the mark."""
    shown, filled, held = asyncio.run(_load_shown())
    assert shown == LOAD_MESSAGE
    assert filled == FILLED_MARK
    assert held == ''


def test_no_load_no_widget() -> None:
    """Test a model with nothing to say about a load gets no widget for it.

    The file is read before the model is built, so a message cannot arrive
    later, and an empty widget would take a line of the screen for good.
    """
    assert not asyncio.run(_no_load_widget())


async def _laid_out(size: tuple[int, int]) -> tuple[dict[str, Region], Region]:
    """Run the application and report where each of its widgets ended up.

    Args:
        size: Terminal size to lay the application out in.

    Returns:
        The region of every widget that has an identifier, by identifier,
        and the region of the screen those widgets have to fit inside.
    """
    app = EditorApp(EditModel(FlatConfig(), FILLED_REPORT))
    async with app.run_test(size=size) as pilot:
        await pilot.pause()
        placed = {str(widget.id): widget.region
                  for widget in app.screen.query('*')
                  if widget.id is not None}
        return placed, app.screen.region


def test_all_on_screen() -> None:
    """Test every widget of the editor is laid out where it can be seen.

    This asserts the geometry rather than the text, because that is the
    difference the other tests of this module cannot see. A widget that
    Textual lays out beyond the right edge of the screen still holds its
    text and shows it to nobody, and that is how the marks of a member went
    missing once: `Input` is a full width widget of its own accord, so it
    took the whole line and left the mark beside it nowhere to be.
    """
    placed, screen = asyncio.run(_laid_out(ROOMY_SIZE))
    beyond = [name for name, region in placed.items()
              if not screen.contains_region(region)]
    assert not beyond


def test_mark_width() -> None:
    """Test a mark is given the width of the mark it has to show."""
    placed, _ = asyncio.run(_laid_out(ROOMY_SIZE))
    assert placed[f'{MARK_ID_PREFIX}answer'].width == len(FILLED_MARK)
    assert placed[f'{MARK_ID_PREFIX}name'].width == 0


def test_narrow_keeps_field() -> None:
    """Test a terminal too narrow for both cuts the marks, not the field.

    The field is what the user edits, and `model_as_text` shows every mark
    in full whatever the terminal does to them.
    """
    placed, _ = asyncio.run(_laid_out(NARROW_SIZE))
    assert placed[f'{VALUE_ID_PREFIX}answer'].width == LEAST_VALUE_WIDTH


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
        _field(app, member_name).value = text
        await pilot.pause()
        await pilot.press(SAVE_KEY)
        await pilot.pause()
        return _saving(app), _verdict(app), app.title


def test_save_writes(tmp_path: Path) -> None:
    """Test the save key writes the edited values to the output file."""
    out_file = tmp_path / 'out.json'
    model = EditModel(FlatConfig(), out_file=out_file)
    saving, verdict, title = asyncio.run(_save_with(model))
    assert saving == f'Saved to {out_file}.'
    assert verdict == VALID_VERDICT
    assert title == 'FlatConfig'
    assert _written(out_file) == {'name': 'Flat example', 'answer': 7}


def test_save_refused(tmp_path: Path) -> None:
    """Test an invalid buffer is not written, and the verdict says why."""
    out_file = tmp_path / 'out.json'
    model = EditModel(FlatConfig(), out_file=out_file)
    saving, verdict, title = asyncio.run(_save_with(model, text='500'))
    assert 'cannot be saved' in saving
    assert 'greater than maximum 100' in verdict
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
    assert _written(out_file) == {'name': 'Other', 'answer': 42}


def test_destination_shown(tmp_path: Path) -> None:
    """Test a session with a file says where it would write, before saving."""
    out_file = tmp_path / 'out.json'

    async def shown() -> str:
        """Run the application and read what it says about saving."""
        app = EditorApp(EditModel(FlatConfig(), out_file=out_file))
        async with app.run_test():
            return _saving(app)
    assert asyncio.run(shown()) == f'save to: {out_file}'


def test_no_destination_shown() -> None:
    """Test a session with no file says that rather than saying nothing."""
    async def shown() -> str:
        """Run the application and read what it says about saving."""
        app = EditorApp(EditModel(FlatConfig()))
        async with app.run_test():
            return _saving(app)
    assert asyncio.run(shown()) == NO_FILE_TEXT


async def _save_as(model: EditModel, typed: str, key: str = SAVE_AS_KEY,
                   answer: str = ENTER_KEY) -> str:
    """Run the application headlessly and answer the Save as question.

    Args:
        model: Model to run the application on.
        typed: File name to type into the question.
        key: Key pressed to ask the question.
        answer: Key pressed to finish with it.

    Returns:
        The saving text the editor shows afterwards.
    """
    app = EditorApp(model)
    async with app.run_test() as pilot:
        await pilot.press(key)
        await pilot.pause()
        app.screen.query_one(f'#{SAVE_AS_ID}', Input).value = typed
        await pilot.pause()
        await pilot.press(answer)
        await pilot.pause()
        return _saving(app)


def test_save_as_writes(tmp_path: Path) -> None:
    """Test Save as asks which file to write and then writes it."""
    out_file = tmp_path / 'chosen.cfg'
    model = EditModel(FlatConfig())
    assert asyncio.run(_save_as(model, str(out_file))) == \
        f'Saved to {out_file}.'
    assert model.out_file == str(out_file)
    assert _written(out_file) == {'name': 'Flat example', 'answer': 42}


def test_save_as_cancelled(tmp_path: Path) -> None:
    """Test leaving the question unanswered chooses nothing and writes it."""
    out_file = tmp_path / 'chosen.cfg'
    model = EditModel(FlatConfig())
    assert asyncio.run(_save_as(model, str(out_file),
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
    assert asyncio.run(_save_as(model, '')) == NO_FILE_TEXT
    assert model.out_file is None


def test_save_asks_when_none(tmp_path: Path) -> None:
    """Test Save asks where to write when the session has no file yet.

    That is what every editor does, and it is the reason a model may be
    built with no destination at all.
    """
    out_file = tmp_path / 'asked.json'
    model = EditModel(FlatConfig())
    assert asyncio.run(_save_as(model, str(out_file), key=SAVE_KEY)) == \
        f'Saved to {out_file}.'
    assert out_file.exists()


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
            box = app.screen.query_one(f'#{SAVE_AS_BOX_ID}')
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
    async def pressed() -> tuple[int, bool]:
        """Ask the question and then press every key of the editor."""
        app = EditorApp(EditModel(FlatConfig()))
        async with app.run_test() as pilot:
            await pilot.press(SAVE_AS_KEY)
            await pilot.pause()
            for key in (SAVE_KEY, SAVE_AS_KEY, VALIDATE_KEY, QUIT_KEY):
                await pilot.press(key)
                await pilot.pause()
            return len(app.screen_stack), app.is_running
    depth, running = asyncio.run(pressed())
    assert depth == 2
    assert running


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
            return _saving(app)
    assert asyncio.run(answered()) == f'Saved to {out_file}.'


def test_palette_has_actions() -> None:
    """Test the command palette offers the actions of the editor as well.

    Every terminal can reach the palette, which is what makes it the answer
    for a key combination a terminal cannot encode.
    """
    async def names() -> list[str]:
        """Run the application and read what its palette would offer."""
        app = EditorApp(EditModel(FlatConfig()))
        async with app.run_test():
            return [command.title
                    for command in app.get_system_commands(app.screen)]
    offered = asyncio.run(names())
    assert VALIDATE_COMMAND in offered
    assert SAVE_COMMAND in offered
    assert SAVE_AS_COMMAND in offered


def test_palette_keeps_own() -> None:
    """Test the commands of Textual itself are still there beside them."""
    async def names() -> list[str]:
        """Run the application and read what its palette would offer."""
        app = EditorApp(EditModel(FlatConfig()))
        async with app.run_test():
            return [command.title
                    for command in app.get_system_commands(app.screen)]
    assert 'Quit' in asyncio.run(names())


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
    assert _written(out_file) == {'name': 'Flat example', 'answer': 42}


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
