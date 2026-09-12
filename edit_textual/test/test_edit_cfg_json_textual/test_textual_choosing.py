#! /usr/bin/env python3
"""Tests for choosing a value in the Textual backend.

A member holding true or false and one holding an enum member have a
pull-down of the values they take beside the field they are typed into, and
exactly one of the two is on the screen. The pull-down offers those values and
nothing else, and holds one of them at every moment. What the switch to it had
to replace is said on a screen of its own, because it is the one change of the
buffer that the user did not make.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import asyncio
from config_as_json import JsonType
from textual.pilot import Pilot
from textual.widgets import Select
from textual.widgets._select import InvalidSelectValueError
from edit_cfg_json import EditModel, Settings
from edit_cfg_json_textual.textual_ask import TellScreen
from edit_cfg_json_textual.textual_editor import EditorApp
from edit_cfg_json_textual.textual_screen import ModelScreen
from edit_cfg_json_textual.textual_words import CHOOSE_COMMAND, TYPE_COMMAND
from example.e01_flat_config import FlatConfig
from example.e02_enum_config import EnumConfig
from example.e12_backup_files import ArchiveConfig
from .helpers import CHOOSE_KEY, ENTER_KEY, ESCAPE_KEY, QUIT_KEY, \
    VALIDATE_KEY, chooser_of, field_of, model_value, panel_of

ENUM_NAMES = ('MECHANICAL', 'ELECTRICAL', 'ELECTRONIC')
"""The values that either member of the enum example takes.

They are written out here rather than read from the example, in the same way
as every other text these tests expect.
"""


def _palette_name(app: EditorApp) -> str:
    """Return what the command palette calls the switch as things stand.

    Args:
        app: Application that is showing the model.

    Returns:
        The name of the entry that switches between the two ways of editing.
    """
    named = [entry.name for entry in panel_of(app).command_entries()
             if entry.name in (CHOOSE_COMMAND, TYPE_COMMAND)]
    assert len(named) == 1
    return named[0]


def _enum_app(typed: bool = False) -> EditorApp:
    """Return an application on the enum example.

    Args:
        typed: Whether the application asks for the values to be typed.

    Returns:
        The application to run headlessly.
    """
    settings = Settings(choose_values=not typed)
    return EditorApp(EditModel(EnumConfig(), settings=settings))


def test_chooser_offered() -> None:
    """Test the pull-down offers every name the enum accepts and no other.

    The control refuses a value that is none of the ones it offers, so setting
    each of them and then one that is not is what asks it what it offers.
    """
    async def run() -> tuple[list[str], bool]:
        app = _enum_app()
        async with app.run_test() as pilot:
            await pilot.pause()
            chooser = chooser_of(app, 'needed')
            held = []
            for name in ENUM_NAMES:
                chooser.value = name
                await pilot.pause()
                held.append(str(chooser.value))
            try:
                chooser.value = 'PLUMBING'
                refused = False
            except InvalidSelectValueError:
                refused = True
            return held, refused
    held, refused = asyncio.run(run())
    assert held == list(ENUM_NAMES)
    assert refused


def test_chooser_at_value() -> None:
    """Test the pull-down opens showing the value the member holds."""
    async def run() -> object:
        app = _enum_app()
        async with app.run_test() as pilot:
            await pilot.pause()
            return chooser_of(app, 'needed').value
    assert asyncio.run(run()) == 'ELECTRICAL'


def test_no_chooser() -> None:
    """Test a member whose values are not a known set gets no pull-down.

    A widget that could never hold anything is a piece of the screen spent on
    nothing, which is the same rule the description of a member follows.
    """
    async def run() -> int:
        app = EditorApp(EditModel(FlatConfig()))
        async with app.run_test() as pilot:
            await pilot.pause()
            return len(app.query(Select))
    assert asyncio.run(run()) == 0


def test_chosen_at_start() -> None:
    """Test the editor opens with the pull-down and not with the field."""
    async def run() -> tuple[bool, bool, str]:
        app = _enum_app()
        async with app.run_test() as pilot:
            await pilot.pause()
            return (chooser_of(app, 'needed').display,
                    field_of(app, 'needed').display,
                    _palette_name(app))
    chosen, typed, named = asyncio.run(run())
    assert chosen
    assert not typed
    assert named == TYPE_COMMAND


def test_typed_at_start() -> None:
    """Test an application that asked for fields opens with the fields."""
    async def run() -> tuple[bool, bool, str]:
        app = _enum_app(typed=True)
        async with app.run_test() as pilot:
            await pilot.pause()
            return (chooser_of(app, 'needed').display,
                    field_of(app, 'needed').display,
                    _palette_name(app))
    chosen, typed, named = asyncio.run(run())
    assert not chosen
    assert typed
    assert named == CHOOSE_COMMAND


def test_key_switches() -> None:
    """Test the key of the action switches which of the two is shown.

    The action is renamed as well, because what it is called says what the
    next press will do.
    """
    async def run() -> tuple[bool, bool, str]:
        app = _enum_app()
        async with app.run_test() as pilot:
            await pilot.press(CHOOSE_KEY)
            await pilot.pause()
            return (chooser_of(app, 'needed').display,
                    field_of(app, 'needed').display,
                    _palette_name(app))
    chosen, typed, named = asyncio.run(run())
    assert not chosen
    assert typed
    assert named == CHOOSE_COMMAND


def test_picking_edits() -> None:
    """Test picking a value from the pull-down writes it into the model."""
    async def run() -> tuple[str, bool]:
        model = EditModel(EnumConfig())
        app = EditorApp(model)
        async with app.run_test() as pilot:
            await pilot.pause()
            chooser_of(app, 'needed').value = 'ELECTRONIC'
            await pilot.pause()
            return str(model.rows[0].value), model.dirty
    assert asyncio.run(run()) == ('ELECTRONIC', True)


def test_no_unselected_state() -> None:
    """Test the pull-down has no unselected state to be put into.

    A member holding an enum takes the members of that enum and nothing else,
    so there is no blank line among the values for the user to pick and no
    way to leave the control holding nothing.
    """
    async def run() -> bool:
        app = _enum_app()
        async with app.run_test() as pilot:
            await pilot.pause()
            try:
                chooser_of(app, 'needed').clear()
                return False
            except InvalidSelectValueError:
                return True
    assert asyncio.run(run())


def test_replaced_told() -> None:
    """Test a screen says what switching to the pull-downs replaced.

    A pull-down shows one of the values its member takes, so a text meaning
    none of them is replaced by the value it most likely meant, and the user
    is told because it is the one change they did not make. `ELECT` is the
    beginning of two of these three names, so it means the first of those two
    and not the first name of all.
    """
    async def run() -> tuple[str, str, str]:
        model = EditModel(EnumConfig())
        app = EditorApp(model)
        async with app.run_test() as pilot:
            await pilot.press(CHOOSE_KEY)
            await pilot.pause()
            field_of(app, 'needed').value = 'ELECT'
            await pilot.pause()
            await pilot.press(CHOOSE_KEY)
            await pilot.pause()
            screen = app.screen
            assert isinstance(screen, TellScreen)
            said = str(screen.query_one('Label').render())
            await pilot.press(ENTER_KEY)
            await pilot.pause()
            return (said, str(model.rows[0].value),
                    app.screen.__class__.__name__)
    said, held, left = asyncio.run(run())
    assert 'ELECT' in said
    assert 'needed' in said
    assert held == ENUM_NAMES[1]
    assert left == ModelScreen.__name__


def test_completed_untold() -> None:
    """Test a text meaning one value is completed and no screen is put."""
    async def run() -> tuple[str, str]:
        model = EditModel(EnumConfig())
        app = EditorApp(model)
        async with app.run_test() as pilot:
            await pilot.press(CHOOSE_KEY)
            await pilot.pause()
            field_of(app, 'needed').value = 'MECH'
            await pilot.pause()
            await pilot.press(CHOOSE_KEY)
            await pilot.pause()
            return app.screen.__class__.__name__, str(model.rows[0].value)
    left, held = asyncio.run(run())
    assert left == ModelScreen.__name__
    assert held == 'MECHANICAL'


BOOL_NAMES = ('true', 'false')
"""The values that a member holding true or false takes.

They are written out here rather than read from the core, in the same way as
the names of the enum above, and their order is part of what is expected: it
is the order the pull-down offers them in.
"""

ARCHIVE_MEMBERS = ('archive_folder', 'keep_days', 'compress')
"""The members of the backup example, in the order it declares them.

Its text member and its number member can hold anything of their kind, so
neither of them has a pull-down, and the one holding true or false has one.
"""

MIXED_FIELDS = [True, True, False]
"""Which members of that example are typed while the values are chosen.

The two that have no pull-down are edited in a field whatever the editor is
set to, because a member with one way of editing has that one on the screen.
"""


async def _reach_told(app: EditorApp, pilot: Pilot[None]) -> None:
    """Bring up the screen that says what switching to a pull-down replaced.

    Args:
        app: Application that is showing the model.
        pilot: Driver of that application.
    """
    await pilot.press(CHOOSE_KEY)
    await pilot.pause()
    field_of(app, 'needed').value = 'ELECT'
    await pilot.pause()
    await pilot.press(CHOOSE_KEY)
    await pilot.pause()
    assert isinstance(app.screen, TellScreen)


def test_cancel_leaves_told() -> None:
    """Test the key that leaves a question leaves the screen that tells.

    There is nothing to answer here, so leaving it is what both ways of
    leaving it do. A user who reaches for the key that dismisses every other
    screen of this editor should not be left with this one still up.
    """
    async def run() -> str:
        app = _enum_app()
        async with app.run_test() as pilot:
            await _reach_told(app, pilot)
            await pilot.press(ESCAPE_KEY)
            await pilot.pause()
            return app.screen.__class__.__name__
    assert asyncio.run(run()) == ModelScreen.__name__


def test_told_is_modal() -> None:
    """Test the keys of the editor do nothing while that screen is up.

    Textual dispatches a priority binding of the editor from the whole chain
    rather than from the part of it above the last modal screen, so it goes on
    offering the editor its keys. Without the editor turning its own actions
    off, one more press of the switch would stack a second of these screens on
    the first, and Quit would leave the user never having read it.
    """
    async def run() -> tuple[int, bool, str]:
        model = EditModel(EnumConfig())
        app = EditorApp(model)
        async with app.run_test() as pilot:
            await _reach_told(app, pilot)
            for key in (CHOOSE_KEY, VALIDATE_KEY, QUIT_KEY):
                await pilot.press(key)
                await pilot.pause()
            return (len(app.screen_stack), app.is_running,
                    str(model.rows[0].value))
    depth, running, held = asyncio.run(run())
    assert depth == 2
    assert running
    assert held == ENUM_NAMES[1]


def test_flag_offered() -> None:
    """Test a member holding true or false offers the two words and no other.

    A member of that kind takes a set of values the editor knows the whole of
    just as an enum member does, and the two kinds read those values from
    different places in the core, so both are asked here.
    """
    async def run() -> tuple[list[str], bool]:
        app = EditorApp(EditModel(ArchiveConfig()))
        async with app.run_test() as pilot:
            await pilot.pause()
            chooser = chooser_of(app, 'compress')
            held = []
            for name in BOOL_NAMES:
                chooser.value = name
                await pilot.pause()
                held.append(str(chooser.value))
            try:
                chooser.value = 'yes'
                refused = False
            except InvalidSelectValueError:
                refused = True
            return held, refused
    held, refused = asyncio.run(run())
    assert held == list(BOOL_NAMES)
    assert refused


def test_mixed_ways() -> None:
    """Test the members that have no pull-down are fields beside the one that.

    Which way of editing is used is one answer for the whole editor, and it
    says nothing about a member that has only one way: switching to the fields
    changes the one member that had both and leaves the other two alone.
    """
    async def run() -> tuple[list[bool], bool, list[bool], bool]:
        app = EditorApp(EditModel(ArchiveConfig()))
        async with app.run_test() as pilot:
            await pilot.pause()
            shown = _ways_shown(app)
            await pilot.press(CHOOSE_KEY)
            await pilot.pause()
            return (*shown, *_ways_shown(app))
    fields, pull_down, typed_fields, typed_pull = asyncio.run(run())
    assert fields == MIXED_FIELDS
    assert pull_down
    assert typed_fields == [True] * len(ARCHIVE_MEMBERS)
    assert not typed_pull


def _ways_shown(app: EditorApp) -> tuple[list[bool], bool]:
    """Return what the backup example has on the screen for its values.

    Args:
        app: Application that is showing the model.

    Returns:
        Whether the field of each member is on the screen, in the order the
        example declares them, and whether the one pull-down is.
    """
    return ([field_of(app, name).display for name in ARCHIVE_MEMBERS],
            chooser_of(app, 'compress').display)


def test_picking_flag() -> None:
    """Test picking one of the two words writes the value it means.

    The pull-down offers the words and the buffer holds true or false, so what
    reaches the model is the value and not the word that named it.
    """
    async def run() -> tuple[JsonType, bool]:
        model = EditModel(ArchiveConfig())
        app = EditorApp(model)
        async with app.run_test() as pilot:
            await pilot.pause()
            chooser_of(app, 'compress').value = 'false'
            await pilot.pause()
            return model_value(model, 'compress'), model.dirty
    assert asyncio.run(run()) == (False, True)


def test_picking_held() -> None:
    """Test picking the value a member already holds changes nothing.

    A pull-down opens on the value its member holds, so picking that one is
    what a user does who opened it and then thought better of it. There is
    nothing to save afterwards, and an editor that claimed otherwise would be
    telling them something untrue.
    """
    async def run() -> tuple[str, bool]:
        model = EditModel(EnumConfig())
        app = EditorApp(model)
        async with app.run_test() as pilot:
            await pilot.pause()
            chooser = chooser_of(app, 'needed')
            chooser.value = str(chooser.value)
            await pilot.pause()
            return str(model.rows[0].value), model.dirty
    assert asyncio.run(run()) == (ENUM_NAMES[1], False)


def test_picking_second() -> None:
    """Test each pull-down writes its own member and no other.

    Every pull-down of this example offers the same three names, so a
    pull-down wired to the wrong member would show exactly what it should and
    edit the member above it.
    """
    async def run() -> list[str]:
        model = EditModel(EnumConfig())
        app = EditorApp(model)
        async with app.run_test() as pilot:
            await pilot.pause()
            chooser_of(app, 'available').value = 'ELECTRONIC'
            await pilot.pause()
            return [str(row.value) for row in model.rows]
    assert asyncio.run(run()) == ['ELECTRICAL', 'ELECTRONIC']
