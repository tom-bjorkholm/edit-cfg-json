#! /usr/bin/env python3
"""Tests for the widgets of the Textual backend, and for editing in them."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import asyncio
from config_as_json import JsonType
import pytest
from textual.app import App, ComposeResult
from textual.containers import VerticalScroll
from textual.geometry import Region
from textual.widgets import Static
from edit_cfg_json import EditModel, LoadReport
from edit_cfg_json_textual.textual_editor import BODY_ID, EditorApp, \
    LEAST_VALUE_WIDTH, LOAD_ID, MARK_ID_PREFIX, SAVE_ID, VALUE_ID_PREFIX, \
    plain_widget
from example.e01_flat_config import FlatConfig
from .helpers import DESCRIPTIONS, EXPECTED_VALUES, FILLED_MARK, \
    FILLED_REPORT, LOAD_MESSAGE, NARROW_SIZE, QUIT_KEY, REWRITTEN_MARK, \
    REFUSED_VERDICT, ROOMY_SIZE, SHORT_SIZE, UNKNOWN_VERDICT, \
    VALIDATE_ALT_KEY, VALIDATE_KEY, VALID_VERDICT, field_of, mark_of, \
    model_value, verdict_of

LOAD_REASON = 'supplied for a file of an older format'
"""What the model of the test below says the load did to one member.

It is a text of this test and not one of the core's, because what this backend
has to do with it is show it. A backend that put a wording of its own around a
member the load changed would pass a test that used the core's wording.
"""

MARKUP_TEXT = 'value [red on blue]here[/] is refused'
"""Text of a configuration that happens to look like console markup."""


class MarkupProbe(App[None]):
    """An application showing one text that looks like console markup."""

    def compose(self) -> ComposeResult:
        """Create the one widget that is under test."""
        yield plain_widget(MARKUP_TEXT, 'probe')


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
        shown = {name: field_of(app, name).value for name in EXPECTED_VALUES}
        verdict = verdict_of(app)
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
        field_of(app, 'answer').focus()
        await pilot.pause()
        await pilot.press(key)
        await pilot.pause()
        return model_value(model, 'answer'), app.title


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
        field_of(app, member_name).value = text
        # The field keeps the focus while the key is pressed, which is the
        # situation the editor is really in: a user validates what has just
        # been typed without leaving the field first.
        field_of(app, member_name).focus()
        await pilot.pause()
        await pilot.press(key)
        await pilot.pause()
        return (verdict_of(app), field_of(app, member_name).value,
                mark_of(app, member_name))


async def _edit_after_validate() -> str:
    """Run the application headlessly, validate and then edit a field.

    Returns:
        The validation text the application shows after the edit.
    """
    app = EditorApp(EditModel(FlatConfig()))
    async with app.run_test() as pilot:
        await pilot.press(VALIDATE_KEY)
        await pilot.pause()
        field_of(app, 'answer').value = '7'
        await pilot.pause()
        return verdict_of(app)


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
    assert verdict == REFUSED_VERDICT
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
        return shown, mark_of(app, 'answer'), mark_of(app, 'name')


async def _change_shown() -> tuple[str, str]:
    """Run the application on a model whose load changed a value itself.

    A file in an older format is what leaves such a member: its value was in
    the file under another key, or the rules for that format supplied it.

    Returns:
        The mark of the member the load changed, and the mark of the member it
        left alone.
    """
    report = LoadReport(message=LOAD_MESSAGE, reasons={'answer': LOAD_REASON})
    app = EditorApp(EditModel(FlatConfig(), report))
    async with app.run_test():
        return mark_of(app, 'answer'), mark_of(app, 'name')


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


def test_load_change_shown() -> None:
    """Test the editor marks a member whose value the load itself changed.

    Which of the two marks a load leaves is the model's answer. This backend
    shows the marks it is given, so a member the load changed is marked
    exactly where a member the defaults filled in would be.
    """
    changed, held = asyncio.run(_change_shown())
    assert changed == f' ({LOAD_REASON})'
    assert held == ''


def test_no_load_no_widget() -> None:
    """Test a model with nothing to say about a load gets no widget for it.

    The file is read before the model is built, so a message cannot arrive
    later, and an empty widget would take a line of the screen for good.
    """
    assert not asyncio.run(_no_load_widget())


async def _laid_out(size: tuple[int, int]) -> tuple[dict[str, Region], Region]:
    """Run the application and report where each of its widgets ended up.

    The model has everything the editor can show, so that a widget of any
    kind that is laid out where it cannot be seen is found here.

    Args:
        size: Terminal size to lay the application out in.

    Returns:
        The region of every widget that has an identifier, by identifier,
        and the region of the screen those widgets have to fit inside.
    """
    app = EditorApp(EditModel(FlatConfig(), FILLED_REPORT,
                              descriptions=DESCRIPTIONS))
    async with app.run_test(size=size) as pilot:
        await pilot.pause()
        placed = {str(widget.id): widget.region
                  for widget in app.screen.query('*')
                  if widget.id is not None}
        return placed, app.screen.region


def test_all_on_screen() -> None:
    """Test no widget of the editor is laid out beyond the edges of it.

    This asserts the geometry rather than the text, because that is the
    difference the other tests of this module cannot see. A widget that
    Textual lays out beyond the right edge of the screen still holds its
    text and shows it to nobody, and that is how the marks of a member went
    missing once: `Input` is a full width widget of its own accord, so it
    took the whole line and left the mark beside it nowhere to be.

    Only the two sides are asserted. Below the bottom is where the body puts
    what is too tall for the terminal, and it is reached by scrolling to it
    rather than being lost, which the test below is about.
    """
    placed, screen = asyncio.run(_laid_out(ROOMY_SIZE))
    beyond = [name for name, region in placed.items()
              if region.x < screen.x or region.right > screen.right]
    assert not beyond


async def _scrolling(size: tuple[int, int]) -> tuple[int, int, bool]:
    """Run the application and report what its body does about its height.

    Args:
        size: Terminal size to lay the application out in.

    Returns:
        How far the body can be scrolled, how far it went when it was asked
        for all of it, and whether the saving line stayed where it was.
    """
    app = EditorApp(EditModel(FlatConfig(), FILLED_REPORT,
                              descriptions=DESCRIPTIONS))
    async with app.run_test(size=size) as pilot:
        await pilot.pause()
        body = app.query_one(f'#{BODY_ID}', VerticalScroll)
        before = app.query_one(f'#{SAVE_ID}', Static).region
        limit = int(body.max_scroll_y)
        body.scroll_to(y=limit, animate=False)
        await pilot.pause()
        return (limit, int(body.scroll_offset.y),
                app.query_one(f'#{SAVE_ID}', Static).region == before)


def test_body_scrolls() -> None:
    """Test a configuration too tall for the terminal is scrolled to.

    What the application makes of the values and where they would be written
    stay where they are, because they are what a user reaches for after
    editing rather than something to scroll to.
    """
    limit, moved, kept = asyncio.run(_scrolling(SHORT_SIZE))
    assert limit > 0
    assert moved == limit
    assert kept


def test_no_scroll_if_fits() -> None:
    """Test a configuration that fits has nothing to scroll."""
    limit, _, _ = asyncio.run(_scrolling(ROOMY_SIZE))
    assert limit == 0


def test_mark_width() -> None:
    """Test a mark is given the width of the mark it has to show."""
    placed, _ = asyncio.run(_laid_out(ROOMY_SIZE))
    assert placed[f'{MARK_ID_PREFIX}answer'].width == len(FILLED_MARK)
    assert placed[f'{MARK_ID_PREFIX}name'].width == 0


def test_narrow_keepsfield_of() -> None:
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
