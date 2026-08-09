#! /usr/bin/env python3
"""Tests for the explanatory text of the Textual backend, and its colours."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from pathlib import Path
import asyncio
import pytest
from textual.widgets import Static
from edit_cfg_json import EditModel, Emphasis
from edit_cfg_json_textual.textual_editor import EditorApp, \
    EXPLAIN_COMMAND, HIDE_COMMAND
from edit_cfg_json_textual.textual_look import DOCSTRING_ID, \
    EMPHASIS_CLASSES, LOAD_ID, SAVE_ID, VERDICT_ID, description_id, \
    mark_id, value_id
from example.e01_flat_config import FlatConfig
from .helpers import ABOUT_NAME, ANSWER_INDEX, DESCRIPTIONS, \
    EXPLAIN_ALT_KEY, EXPLAIN_KEY, FILLED_REPORT, NAME_INDEX, NoDocConfig, \
    SAVE_KEY, TEXT_KIND, VALIDATE_KEY, WHOLE_KIND, described_app, \
    description_of, docstring_of, field_of


async def _explained(*keys: str) -> tuple[str, bool, str]:
    """Run the described application and press every key it is given.

    Args:
        keys: Keys to press, which are the ones that show or hide the
            explanatory text.

    Returns:
        What the application says about the configuration class, whether the
        description of the member is being shown, and the description itself.
    """
    app = described_app()
    async with app.run_test() as pilot:
        for key in keys:
            await pilot.press(key)
            await pilot.pause()
        widget = description_of(app, 'name')
        return docstring_of(app), widget.display, str(widget.content)


def test_explanations_shown() -> None:
    """Test the editor starts by showing what the configuration is for.

    What the application said comes first and what the type of the member says
    follows it, which is what the editor knows about a member without being
    told anything at all.
    """
    docstring, shown, description = asyncio.run(_explained())
    assert docstring == EditModel(FlatConfig()).docstring
    assert shown
    assert description == f'{ABOUT_NAME}\n{TEXT_KIND}'


@pytest.mark.parametrize('key', [EXPLAIN_KEY, EXPLAIN_ALT_KEY])
def test_explain_hides(key: str) -> None:
    """Test either explain key leaves the summary and hides the rest.

    Both keys are tried because a terminal or a keyboard that does not
    deliver a function key is exactly why there are two.
    """
    docstring, shown, _ = asyncio.run(_explained(key))
    assert docstring == EditModel(FlatConfig()).summary
    assert not shown


def test_explain_shows_again() -> None:
    """Test the same key brings the explanatory text back."""
    docstring, shown, _ = asyncio.run(_explained(EXPLAIN_KEY, EXPLAIN_KEY))
    assert docstring == EditModel(FlatConfig()).docstring
    assert shown


def test_hidden_at_start() -> None:
    """Test a model that was told to hide them opens with them hidden.

    Which of the two states the editor is in belongs to the model, so a model
    that reached this backend already toggled has to be honoured rather than
    overruled.
    """
    model = EditModel(FlatConfig(), descriptions=DESCRIPTIONS)
    model.toggle_explanations()

    async def shown() -> tuple[str, bool]:
        """Run the application and read what it is showing."""
        app = EditorApp(model)
        async with app.run_test():
            return docstring_of(app), description_of(app, 'name').display
    docstring, showing = asyncio.run(shown())
    assert docstring == model.summary
    assert not showing


def test_undescribed_told() -> None:
    """Test a member the application says nothing about says what it holds.

    Every editable member has something to say, because its own type says what
    kind of value it is, so every one of them gets the widget for it. A widget
    is left out only where there is nothing that could ever appear in it, which
    is a member the editor cannot edit yet: its row says which kind of
    container it is where its value would be.
    """
    async def described() -> tuple[str, str]:
        """Run the described application and read both members."""
        app = described_app()
        async with app.run_test():
            return (str(description_of(app, 'name').content),
                    str(description_of(app, 'answer').content))
    about_name, about_answer = asyncio.run(described())
    assert about_name == f'{ABOUT_NAME}\n{TEXT_KIND}'
    assert about_answer == WHOLE_KIND


def test_no_docstring_widget() -> None:
    """Test a class with no docstring of its own gets no widget for one."""
    async def widgets() -> int:
        """Run an application on such a class and look for the widget."""
        app = EditorApp(EditModel(NoDocConfig()))
        async with app.run_test():
            return len(app.query(f'#{DOCSTRING_ID}'))
    assert not asyncio.run(widgets())


async def _explain_named(*keys: str) -> tuple[str, list[str]]:
    """Run the described application and read what the action is called.

    The name is read from the binding rather than from the footer widget that
    shows it, because the binding is what the footer is built from and it is
    the part that is not private to Textual.

    Args:
        keys: Keys to press before looking, which are the ones that show or
            hide the explanatory text.

    Returns:
        What the explain action is called, and what the command palette calls
        the actions of the editor.
    """
    app = described_app()
    async with app.run_test() as pilot:
        await pilot.pause()
        for key in keys:
            await pilot.press(key)
            await pilot.pause()
        named = {binding.action: binding.description
                 for (_, binding, _, _) in app.screen.active_bindings.values()}
        return (named['explain'],
                [command.title
                 for command in app.get_system_commands(app.screen)])


def test_explain_named() -> None:
    """Test the action is named for what the next press of it will do.

    "Explain" beside explanations that are already there would read as an
    offer to do something that has been done. The Tk backend answers the same
    question with a tick-box, which a footer cannot be.
    """
    shown_name, shown_palette = asyncio.run(_explain_named())
    assert shown_name == HIDE_COMMAND
    assert HIDE_COMMAND in shown_palette
    hidden_name, hidden_palette = asyncio.run(_explain_named(EXPLAIN_KEY))
    assert hidden_name == EXPLAIN_COMMAND
    assert EXPLAIN_COMMAND in hidden_palette


async def _emphasis(*keys: str) -> dict[str, set[str]]:
    """Run the application and report which emphasis each part is shown with.

    Args:
        keys: Keys to press before looking.

    Returns:
        The emphasis classes of every widget of the editor that has an
        identifier, by identifier.
    """
    app = EditorApp(EditModel(FlatConfig(), FILLED_REPORT,
                              descriptions=DESCRIPTIONS,
                              out_file='/nowhere/at/all/out.json'))
    async with app.run_test() as pilot:
        await pilot.pause()
        for key in keys:
            await pilot.press(key)
            await pilot.pause()
        wanted = set(EMPHASIS_CLASSES.values())
        return {str(widget.id): set(widget.classes) & wanted
                for widget in app.screen.query('*') if widget.id is not None}


def test_explanations_muted() -> None:
    """Test the text about the values is shown as the secondary text it is."""
    shown = asyncio.run(_emphasis())
    assert shown[DOCSTRING_ID] == {EMPHASIS_CLASSES[Emphasis.MUTED]}
    assert shown[description_id(NAME_INDEX)] == \
        {EMPHASIS_CLASSES[Emphasis.MUTED]}


def test_marks_coloured() -> None:
    """Test a mark and a remark about the file are told apart by colour."""
    shown = asyncio.run(_emphasis())
    assert shown[mark_id(ANSWER_INDEX)] == \
        {EMPHASIS_CLASSES[Emphasis.ATTENTION]}
    assert shown[LOAD_ID] == {EMPHASIS_CLASSES[Emphasis.WARNING]}


def test_values_left_alone() -> None:
    """Test the values and their names are shown in the ordinary colour.

    They are what the user came to change, and they are the most legible
    thing on the screen because nothing has been done to them.
    """
    shown = asyncio.run(_emphasis())
    assert shown[value_id(NAME_INDEX)] == set()


@pytest.mark.parametrize('keys, emphasis',
                         [((), Emphasis.MUTED),
                          ((VALIDATE_KEY,), Emphasis.GOOD)])
def test_verdict_coloured(keys: tuple[str, ...], emphasis: Emphasis) -> None:
    """Test the validation state is coloured for what it says."""
    shown = asyncio.run(_emphasis(*keys))
    assert shown[VERDICT_ID] == {EMPHASIS_CLASSES[emphasis]}


def test_bad_verdict_colour() -> None:
    """Test a refused buffer is coloured as refused."""
    async def refused() -> set[str]:
        """Type a value the application refuses, and validate it."""
        app = EditorApp(EditModel(FlatConfig()))
        async with app.run_test() as pilot:
            field_of(app, 'answer').value = '500'
            await pilot.pause()
            await pilot.press(VALIDATE_KEY)
            await pilot.pause()
            verdict = app.query_one(f'#{VERDICT_ID}', Static)
            return set(verdict.classes) & set(EMPHASIS_CLASSES.values())
    assert asyncio.run(refused()) == {EMPHASIS_CLASSES[Emphasis.BAD]}


def test_saving_coloured(tmp_path: Path) -> None:
    """Test a save that wrote the file and one that could not differ.

    Each of the two writes a file of its own, so that neither of them is
    asked whether it may overwrite what the other one left: the question is
    tested where it belongs and this is about the colour of the answer.
    """
    async def saved(text: str) -> set[str]:
        """Type one value and press Save."""
        out_file = tmp_path / f'out-{text}.json'
        app = EditorApp(EditModel(FlatConfig(), out_file=out_file))
        async with app.run_test() as pilot:
            field_of(app, 'answer').value = text
            await pilot.pause()
            await pilot.press(SAVE_KEY)
            await pilot.pause()
            saving = app.query_one(f'#{SAVE_ID}', Static)
            return set(saving.classes) & set(EMPHASIS_CLASSES.values())
    assert asyncio.run(saved('7')) == {EMPHASIS_CLASSES[Emphasis.GOOD]}
    assert asyncio.run(saved('500')) == {EMPHASIS_CLASSES[Emphasis.BAD]}
