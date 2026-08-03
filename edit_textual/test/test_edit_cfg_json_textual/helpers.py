#! /usr/bin/env python3
"""What the tests of the Textual backend share.

Textual runs headlessly in process, so the equivalent of a withdrawn Tk window
is available everywhere, including on a machine with no display.
`App.run_test()` is an asynchronous context manager, and it is driven from an
ordinary test function with `asyncio.run`, which keeps the test session free of
an extra asynchronous test plugin.

The keys, the sizes and the ways of asking the application what it is showing
live here, so that the five test modules of this backend drive the same editor
and cannot drift apart about what it looks like.

The configuration class comes from the example rather than from a class of its
own, so that the same flat configuration is used by the core tests, by both
backends and by the example itself.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from pathlib import Path
import json
from config_as_json import JsonType
from textual.widgets import Input, Static
from edit_cfg_json import ActionSettings, Descriptions, EditModel, LoadReport
from edit_cfg_json_textual.textual_editor import DESCRIPTION_ID_PREFIX, \
    DIAGNOSTIC_ID_PREFIX, DOCSTRING_ID, EditorApp, MARK_ID_PREFIX, \
    SAVE_AS_ID, SAVE_ID, VALUE_ID_PREFIX, VERDICT_ID
from example.e01_flat_config import FlatConfig

DEFAULT_ACTIONS = ActionSettings()
"""The keys of the editor for an application with no opinion of its own.

The tests press the keys of the settings rather than keys of their own, so
that a default that moves moves them with it. Which keys those are is
decided in the core and tested there.
"""

QUIT_KEY = DEFAULT_ACTIONS.quit[0]
"""Key that ends the editor."""

VALIDATE_KEY = DEFAULT_ACTIONS.validate[0]
"""Key that validates the buffer, and the one the footer names."""

VALIDATE_ALT_KEY = DEFAULT_ACTIONS.validate[1]
"""The other key that validates the buffer."""

SAVE_KEY = DEFAULT_ACTIONS.save[0]
"""Key that writes the output file."""

SAVE_AS_KEY = DEFAULT_ACTIONS.save_as[0]
"""Key that chooses an output file and then writes it."""

EXPLAIN_KEY = DEFAULT_ACTIONS.explain[0]
"""Key that shows or hides the explanatory text, and the one the footer
names."""

EXPLAIN_ALT_KEY = DEFAULT_ACTIONS.explain[1]
"""The other key that shows or hides the explanatory text."""

ABOUT_NAME = 'What the name of this configuration is for.'
"""Description of the one member that the tests below describe."""

DESCRIPTIONS: Descriptions = {('name',): ABOUT_NAME}
"""What an application says about the members of the example."""

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

REFUSED_VERDICT = 'validation: invalid, see answer'
"""Text the editor shows when the number member of the example is refused.

What was refused is said beside that member, so this line only names it: a
configuration too tall for a terminal would otherwise leave the user hunting
for the field that the refusal is about.
"""

REWRITTEN_MARK = ' (edited) (changed by validator)'
"""Mark of a member that the user changed and a validator then rewrote."""

ROOMY_SIZE = (100, 24)
"""Terminal size with room for the longest mark a member can carry."""

NARROW_SIZE = (40, 24)
"""Terminal size too narrow for the field and the marks together."""

SHORT_SIZE = (100, 12)
"""Terminal size too short for the explanations and the members together."""

NO_FILE_TEXT = 'save to: no file chosen yet'
"""Text the editor shows while no output file has been chosen."""

ENTER_KEY = 'enter'
"""Key that answers the question about the output file."""

ESCAPE_KEY = 'escape'
"""Key that leaves the question about the output file unanswered."""


def field_of(app: EditorApp, member_name: str) -> Input:
    """Return the field that the application shows for one member."""
    return app.query_one(f'#{VALUE_ID_PREFIX}{member_name}', Input)


def mark_of(app: EditorApp, member_name: str) -> str:
    """Return the mark that the application shows for one member."""
    widget = app.query_one(f'#{MARK_ID_PREFIX}{member_name}', Static)
    return str(widget.content)


def verdict_of(app: EditorApp) -> str:
    """Return the validation text that the application shows."""
    return str(app.query_one(f'#{VERDICT_ID}', Static).content)


def saving_of(app: EditorApp) -> str:
    """Return the saving text that the application shows."""
    return str(app.query_one(f'#{SAVE_ID}', Static).content)


def written(out_file: Path) -> object:
    """Return what one output file holds, as JSON space values."""
    return json.loads(out_file.read_text(encoding='UTF-8'))


def model_value(model: EditModel, name: str) -> JsonType:
    """Return the value that the buffer holds for one member."""
    return {row.name: row.value for row in model.rows}[name]


class NoDocConfig(FlatConfig):
    """This docstring is taken away below, so that this class has none."""


# A configuration class written without a docstring is one the editor has to
# handle, and it cannot be written here, because every class in this
# repository has to have one. Taking it away afterwards is the same thing.
NoDocConfig.__doc__ = None


def docstring_of(app: EditorApp) -> str:
    """Return the text that the application shows for the whole class."""
    return str(app.query_one(f'#{DOCSTRING_ID}', Static).content)


def description_of(app: EditorApp, member_name: str) -> Static:
    """Return the widget that the application shows about one member."""
    return app.query_one(f'#{DESCRIPTION_ID_PREFIX}{member_name}', Static)


def wrong_widget(app: EditorApp, member_name: str) -> Static:
    """Return the widget that says what is wrong with one member."""
    return app.query_one(f'#{DIAGNOSTIC_ID_PREFIX}{member_name}', Static)


def wrong_of(app: EditorApp, member_name: str) -> str:
    """Return what the application says is wrong with one member.

    A widget that is not being shown says nothing, whatever it holds, so this
    answers what is on the screen and not what a widget remembers.
    """
    widget = wrong_widget(app, member_name)
    return str(widget.content) if widget.display else ''


def described_app() -> EditorApp:
    """Return an application on a model whose text member is described."""
    return EditorApp(EditModel(FlatConfig(), descriptions=DESCRIPTIONS))


async def save_as(model: EditModel, typed: str, key: str = SAVE_AS_KEY,
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
        return saving_of(app)
