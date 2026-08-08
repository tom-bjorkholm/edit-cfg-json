#! /usr/bin/env python3
"""Tests for what the Textual editor says is wrong with one member.

There are two ways for a member to be told that something is wrong with it,
and they are separate: leaving its field asks whether its text means a value
of it at all, and a validation pass asks what the whole application makes of
the buffer. Both end up below the same member and both are read from the
core, which is what stops the two backends from disagreeing about either.

Leaving a field costs Textual nothing that it costs Tk. Focus is a matter of
the application and not of the operating system here, so the headless driver
moves it and the editor is really told about it, which is what these tests do.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from pathlib import Path
import asyncio
from textual.containers import Vertical
from edit_cfg_json import EditModel
from edit_cfg_json_textual.textual_editor import EditorApp
from edit_cfg_json_textual.textual_look import description_id, \
    diagnostic_id, member_id
from example.e02_enum_config import EnumConfig
from example.e04_validated_config import DESCRIPTIONS, ValidatedConfig
from .helpers import EXPLAIN_KEY, SAVE_AS_KEY, VALIDATE_KEY, description_of, \
    field_of, index_of, save_as, verdict_of, wrong_of

RETRIES_INDEX = 1
"""Place among the rows of the number member of the validated example.

The widgets of a node are identified by where it is among the rows, and that
example declares its enum member first and its number member second.
"""

NO_MEMBER = 'MIDDLE is not one of: MECHANICAL, ELECTRICAL, ELECTRONIC'
"""What the converter of the example says about a name no member has."""

TOO_MANY = ('Invalid configuration: Value 9 for retries is greater than '
            'maximum 5.')
"""What the example says about a number that is above its limit."""

SPACED_NAME = 'Invalid configuration: job_name may not contain a space.'
"""What the validator of the example writes about a name with a space."""


def _described() -> EditorApp:
    """Return an application on the example with its descriptions on it."""
    return EditorApp(EditModel(ValidatedConfig(), descriptions=DESCRIPTIONS))


async def _leaving_field(typed: str) -> tuple[str, str]:
    """Type into the enum field, leave it, and report what the editor says.

    Args:
        typed: Text to put into the field of the first member.

    Returns:
        What the editor says about that member, and its validation text.
    """
    app = EditorApp(EditModel(EnumConfig()))
    async with app.run_test() as pilot:
        field_of(app, 'needed').value = typed
        field_of(app, 'needed').focus()
        await pilot.pause()
        field_of(app, 'available').focus()
        await pilot.pause()
        return wrong_of(app, 'needed'), verdict_of(app)


def test_leaving_reports() -> None:
    """Test leaving a field says the text names no member of the enum.

    Nothing has been validated, because leaving one field is not a question
    about the whole configuration and the editor does not pretend it is.
    """
    wrong, verdict = asyncio.run(_leaving_field('MIDDLE'))
    assert wrong == NO_MEMBER
    assert verdict == 'validation: not validated'


def test_leaving_accepts() -> None:
    """Test leaving a field whose text names a member says nothing."""
    assert asyncio.run(_leaving_field('MECH'))[0] == ''


async def _refusals(app: EditorApp) -> dict[str, str]:
    """Break two rules of the example, validate, and report every message.

    Args:
        app: Application to drive.

    Returns:
        What the editor says about each member, and its validation text
        under the empty name.
    """
    async with app.run_test() as pilot:
        field_of(app, 'job_name').value = 'a b'
        field_of(app, 'retries').value = '9'
        await pilot.pause()
        await pilot.press(VALIDATE_KEY)
        await pilot.pause()
        return {name: wrong_of(app, name)
                for name in ('job_name', 'retries', 'timeout_seconds')} | \
            {'': verdict_of(app)}


def test_every_bad_member() -> None:
    """Test a validation pass marks every member that was refused.

    `Config.validate()` stops at the first step that refuses, so a user who
    saw only that one would correct one member per press of the key.
    """
    shown = asyncio.run(_refusals(EditorApp(EditModel(ValidatedConfig()))))
    assert shown == {'job_name': SPACED_NAME, 'retries': TOO_MANY,
                     'timeout_seconds': '',
                     '': 'validation: invalid, see job_name, retries'}


async def _whole_rule() -> tuple[dict[str, str], str]:
    """Break the rule that is about no single member, and report the editor."""
    app = EditorApp(EditModel(ValidatedConfig()))
    async with app.run_test() as pilot:
        field_of(app, 'retries').value = '5'
        field_of(app, 'timeout_seconds').value = '400'
        await pilot.pause()
        await pilot.press(VALIDATE_KEY)
        await pilot.pause()
        return ({name: wrong_of(app, name)
                 for name in ('job_name', 'retries', 'timeout_seconds')},
                verdict_of(app))


def test_whole_rule_below() -> None:
    """Test a rule about no single member stays with the verdict.

    Neither number is wrong on its own, so there is no member this could
    honestly be put beside.
    """
    shown, verdict = asyncio.run(_whole_rule())
    assert set(shown.values()) == {''}
    assert 'longest run' in verdict
    assert verdict.startswith('validation: invalid\n')


async def _hiding() -> tuple[bool, bool]:
    """Refuse a member, hide the explanations, and report what is left."""
    app = _described()
    async with app.run_test() as pilot:
        field_of(app, 'retries').value = '9'
        await pilot.pause()
        await pilot.press(VALIDATE_KEY)
        await pilot.pause()
        assert description_of(app, 'retries').display
        assert wrong_of(app, 'retries') == TOO_MANY
        await pilot.press(EXPLAIN_KEY)
        await pilot.pause()
        return (description_of(app, 'retries').display,
                wrong_of(app, 'retries') == TOO_MANY)


def test_wrong_survives() -> None:
    """Test hiding the explanations leaves what is wrong on the screen.

    A description is what a user who knows the configuration wants out of the
    way; a refusal is the one thing that has to be read.
    """
    assert asyncio.run(_hiding()) == (False, True)


async def _wrong_order(app: EditorApp) -> list[str]:
    """Return the identifiers of the widgets below one refused member."""
    async with app.run_test() as pilot:
        field_of(app, 'retries').value = '9'
        await pilot.pause()
        await pilot.press(VALIDATE_KEY)
        await pilot.pause()
        index = index_of(app, 'retries')
        member = app.query_one(f'#{member_id(index)}', Vertical)
        return [str(child.id) for child in member.children]


def test_description_first() -> None:
    """Test the description is above what is wrong with the member.

    The description is part of the member and a refusal comes and goes, so a
    line that appears at the bottom moves nothing that is above it.
    """
    assert asyncio.run(_wrong_order(_described())) == \
        ['None', description_id(RETRIES_INDEX), diagnostic_id(RETRIES_INDEX)]


def test_save_as_field(tmp_path: Path) -> None:
    """Test leaving the field of the Save as question reaches no member.

    That field is the name of a file and no member of the configuration, so
    a message from it that reached the editor would be looked for among the
    members and found nowhere. The question is answered here, which is what
    takes the focus away from it.
    """
    out_file = tmp_path / 'chosen.json'
    saving = asyncio.run(save_as(EditModel(ValidatedConfig()), str(out_file),
                                 key=SAVE_AS_KEY))
    assert saving == f'Saved to {out_file}.'
