#! /usr/bin/env python3
"""Tests for the controls that change how many elements a node holds.

Textual runs headlessly in process, so the application is really started and
its controls are really pressed. The configuration class comes from the
example rather than from one of its own, so that the same containers are used
by the core tests, by both backends and by the example itself.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from collections.abc import Awaitable, Callable
from typing import Optional
import asyncio
from textual.pilot import Pilot
from textual.widgets import Button, Input
from config_as_json import ConfigPath
from edit_cfg_json import EditModel
from edit_cfg_json_textual.textual_editor import EditorApp
from edit_cfg_json_textual.textual_look import ASK_BOX_ID, value_id
from edit_cfg_json_textual.textual_elements import ADD_ACTION, ADD_LABEL, \
    ASK_KEY_ID, EARLIER_ACTION, LATER_ACTION, LATER_LABEL, REMOVE_ACTION, \
    REMOVE_LABEL, element_id
from example.e11_add_remove import PipelineConfig
from example.e18_declared_types import ReportConfig
from .helpers import ENTER_KEY, ESCAPE_KEY, ROOMY_SIZE, \
    VALIDATE_KEY

NEW_KEY = 'nightly'
"""Key that the question about a new entry is answered with."""

STAGES: ConfigPath = ('stages',)
"""The member of the example that holds a list of configuration objects."""

RUNNERS: ConfigPath = ('runners',)
"""The member of it that holds a dict of them, keyed by a name."""

HOOKS: ConfigPath = ('hooks',)
"""The member of it whose one named key holds a configuration object."""

NAMED_HOOK: ConfigPath = ('hooks', 'on_failure')
"""That named key, which holds one object or holds nothing."""

UNDER_LIST: ConfigPath = ('stage_limits', '0')
"""A dict of the example that a list holds, so nothing checks its keys."""

HOOK_DICT: ConfigPath = ('hooks', 'thresholds')
"""A dict of it at a key that no declaration names, for the same reason."""


def _index_of(model: EditModel, path: ConfigPath) -> int:
    """Return where among the rows one node of one model is.

    Every widget of a node is identified by that place and not by its name,
    because two values inside two different dicts can have one name.
    """
    return [row.path for row in model.rows].index(path)


def _value_of(model: EditModel, path: ConfigPath) -> str:
    """Return what one node of one model shows where a value would be."""
    return {row.path: row.value_text for row in model.rows}[path]


def _run(model: EditModel,
         driving: Callable[[EditorApp, Pilot[None]],
                           Awaitable[None]]) -> None:
    """Run one application headlessly and drive it with one coroutine.

    Args:
        model: Model to run the application on.
        driving: What to do to the application once it is running.
    """
    async def started() -> None:
        """Start the application and hand it to the coroutine."""
        app = EditorApp(model)
        async with app.run_test(size=ROOMY_SIZE) as pilot:
            await driving(app, pilot)
    asyncio.run(started())


async def _press(app: EditorApp, pilot: Pilot[None], index: int,
                 action: str) -> None:
    """Press one control of one node and let the application settle.

    Args:
        app: Application that is showing the model.
        pilot: What drives that application.
        index: Place of the node among the rows.
        action: Name of the action that control runs.
    """
    named = element_id(index=index, action=action)
    app.query_one(f'#{named}', Button).press()
    await pilot.pause()
    await pilot.pause()


def _presser(model: EditModel, path: ConfigPath, action: str,
             answer: Optional[str] = None
             ) -> Callable[[EditorApp, Pilot[None]], Awaitable[None]]:
    """Return a coroutine that presses one control of one node.

    Args:
        model: Model whose rows say where that node is.
        path: Path of the node whose control is pressed.
        action: Name of the action that control runs.
        answer: What to type into the question about a new dict entry, or
            None for a control that asks nothing.

    Returns:
        A coroutine that presses that control and answers what it asks.
    """
    async def driving(app: EditorApp, pilot: Pilot[None]) -> None:
        """Press the control, and answer the question where there is one."""
        await _press(app=app, pilot=pilot, index=_index_of(model, path),
                     action=action)
        if answer is None:
            return
        app.screen.query_one(f'#{ASK_KEY_ID}', Input).value = answer
        await pilot.pause()
        await pilot.press(ENTER_KEY if answer else ESCAPE_KEY)
        await pilot.pause()
    return driving


def test_controls_are_offered() -> None:
    """Test a list that can grow has the controls its offer names."""
    model = EditModel(PipelineConfig())
    seen: list[str] = []

    async def look(app: EditorApp, pilot: Pilot[None]) -> None:
        """Collect what every control of the application says."""
        _ = pilot
        seen.extend(str(button.label) for button in app.query(Button))
    _run(model, look)
    assert ADD_LABEL in seen
    assert REMOVE_LABEL in seen
    assert LATER_LABEL in seen


def test_added_element() -> None:
    """Test pressing the control of a list puts one more element in it."""
    model = EditModel(PipelineConfig())
    _run(model, _presser(model, STAGES, ADD_ACTION))
    assert _value_of(model, STAGES) == '3 elements'


def test_removed_element() -> None:
    """Test pressing the control of an element takes it out of the list."""
    model = EditModel(PipelineConfig())
    _run(model, _presser(model, (*STAGES, '0'), REMOVE_ACTION))
    assert _value_of(model, STAGES) == '1 element'


def test_moved_element() -> None:
    """Test pressing the control of an element changes its place."""
    model = EditModel(PipelineConfig())
    _run(model, _presser(model, (*STAGES, '0'), LATER_ACTION))
    assert _value_of(model, (*STAGES, '0', 'name')) == 'test'


def test_no_control_at_end() -> None:
    """Test the first element of a list is offered no way of moving up.

    There is nothing in front of it to change places with, so the control
    that would do that is not created at all.
    """
    model = EditModel(PipelineConfig())
    found: list[int] = []

    async def look(app: EditorApp, pilot: Pilot[None]) -> None:
        """Count the controls that would move the first element up."""
        _ = pilot
        widget_id = element_id(index=_index_of(model, (*STAGES, '0')),
                               action=EARLIER_ACTION)
        found.append(len(app.query(f'#{widget_id}')))
    _run(model, look)
    assert found == [0]


def test_named_key_cleared() -> None:
    """Test the named key of a dict of two kinds keeps its row when cleared.

    Its object goes and its row stays, saying which class is missing, so the
    key can be given an object again. Every other key of that dict is an
    ordinary entry and is taken out of it.
    """
    model = EditModel(PipelineConfig())
    _run(model, _presser(model, NAMED_HOOK, REMOVE_ACTION))
    assert _value_of(model, NAMED_HOOK) == 'no StageConfig'
    _run(model, _presser(model, (*HOOKS, 'notify'), REMOVE_ACTION))
    assert _value_of(model, HOOKS) == '2 entries'


def test_named_key_made() -> None:
    """Test pressing the control of a cleared named key makes the object."""
    model = EditModel(PipelineConfig())
    _run(model, _presser(model, NAMED_HOOK, REMOVE_ACTION))
    _run(model, _presser(model, NAMED_HOOK, ADD_ACTION))
    assert _value_of(model, NAMED_HOOK) == 'StageConfig'


def test_dict_under_list() -> None:
    """Test a dict that nothing checks is asked for a key like any other.

    Which dicts the declared-keys check reaches is a question about where a
    dict sits, and neither of these two is somewhere it reaches: one has a
    list between it and its member, and the other is inside a member that
    `config_as_json` reads whole.
    """
    model = EditModel(PipelineConfig())
    _run(model, _presser(model, UNDER_LIST, ADD_ACTION, answer='gpu'))
    assert _value_of(model, UNDER_LIST) == '3 entries'
    _run(model, _presser(model, HOOK_DICT, ADD_ACTION, answer='timeouts'))
    assert _value_of(model, HOOK_DICT) == '2 entries'


def test_key_is_asked() -> None:
    """Test a dict of objects is given the entry that the question named."""
    model = EditModel(PipelineConfig())
    _run(model, _presser(model, RUNNERS, ADD_ACTION, answer=NEW_KEY))
    assert (*RUNNERS, NEW_KEY) in [row.path for row in model.rows]


def test_key_unanswered() -> None:
    """Test a question about a new entry that is left unanswered adds none."""
    model = EditModel(PipelineConfig())
    before = len(model.rows)
    _run(model, _presser(model, RUNNERS, ADD_ACTION, answer=''))
    assert len(model.rows) == before


def test_question_is_a_screen() -> None:
    """Test the question about a new entry is shown on a screen of its own."""
    model = EditModel(PipelineConfig())
    asked: list[int] = []

    async def look(app: EditorApp, pilot: Pilot[None]) -> None:
        """Press the control and see whether the question is up."""
        await _press(app=app, pilot=pilot, action=ADD_ACTION,
                     index=_index_of(model, RUNNERS))
        asked.append(len(app.screen.query(f'#{ASK_BOX_ID}')))
        await pilot.press(ESCAPE_KEY)
        await pilot.pause()
    _run(model, look)
    assert asked == [1]


NOTHING_HELD: ConfigPath = ('subtitle',)
"""The member of the other example that holds nothing to begin with."""

CLEARED: ConfigPath = ('footer',)
"""The member of it that a validation pass can move to holding nothing.

A member validator returns the value that is stored back into the member, so
one of them can take a field away from a row that had one. It is the one thing
a backend has to mount its widgets afresh for beyond a pass that changed how
many rows there are.
"""


def _fields(app: EditorApp) -> int:
    """Return how many nodes of one application are shown with a field."""
    return len(app.query(Input))


def test_nothing_offers_add() -> None:
    """Test a member holding nothing has an add control and no field."""
    model = EditModel(ReportConfig())
    seen: list[object] = []

    async def look(app: EditorApp, pilot: Pilot[None]) -> None:
        """Collect what that row has and what it says."""
        _ = pilot
        index = _index_of(model, NOTHING_HELD)
        seen.append(len(app.query(f'#{element_id(index, ADD_ACTION)}')))
        seen.append(len(app.query(Input)
                        .filter(f'#{value_id(index)}')))
    _run(model, look)
    assert seen == [1, 0]
    assert _value_of(model, NOTHING_HELD) == 'no value'


def test_add_gives_a_value() -> None:
    """Test pressing the control gives that member the value of its kind."""
    model = EditModel(ReportConfig())
    _run(model, _presser(model, NOTHING_HELD, ADD_ACTION))
    assert _value_of(model, NOTHING_HELD) == ''


def test_value_is_cleared() -> None:
    """Test the control of a member holding a value puts it back to none."""
    model = EditModel(ReportConfig())
    _run(model, _presser(model, CLEARED, REMOVE_ACTION))
    assert _value_of(model, CLEARED) == 'no value'


def test_pass_takes_a_field() -> None:
    """Test the widgets are mounted afresh when a pass takes a field away.

    The paths are the same before and after, so a backend that compared only
    those would leave a field on the screen for a member holding nothing, and
    the next key typed into it would be refused.
    """
    model = EditModel(ReportConfig())
    counted: list[int] = []

    async def clear(app: EditorApp, pilot: Pilot[None]) -> None:
        """Empty that field, validate, and count the fields left."""
        counted.append(_fields(app))
        app.query_one(f'#{value_id(_index_of(model, CLEARED))}',
                      Input).value = ''
        await pilot.pause()
        await pilot.press(VALIDATE_KEY)
        await pilot.pause()
        await pilot.pause()
        counted.append(_fields(app))
    _run(model, clear)
    assert _value_of(model, CLEARED) == 'no value'
    assert counted[1] == counted[0] - 1


HELD_KEY = 'fast'
"""A key that the dict of runners already holds."""


def test_key_already_held() -> None:
    """Test a key the dict already holds is asked about again.

    The model refuses such a key, so an editor that let the question be
    answered with one would be offering to lose the entry that is there. The
    question comes back instead, and nothing has changed underneath it.
    """
    model = EditModel(PipelineConfig())
    before = len(model.rows)
    asked: list[int] = []

    async def answer_twice(app: EditorApp, pilot: Pilot[None]) -> None:
        """Answer with a key that is taken, and then leave the question."""
        await _press(app=app, pilot=pilot, action=ADD_ACTION,
                     index=_index_of(model, RUNNERS))
        app.screen.query_one(f'#{ASK_KEY_ID}', Input).value = HELD_KEY
        await pilot.pause()
        await pilot.press(ENTER_KEY)
        await pilot.pause()
        asked.append(len(app.screen.query(f'#{ASK_KEY_ID}')))
        await pilot.press(ESCAPE_KEY)
        await pilot.pause()
    _run(model, answer_twice)
    assert asked == [1]
    assert len(model.rows) == before


def test_question_field_left() -> None:
    """Test leaving the field of a question is no member being left.

    The editor underneath asks the model about the member whose field was
    left, and the field of a question is no member of the configuration: a
    message that reached the editor would be looked for among the members and
    found nowhere. So the question keeps this to itself.
    """
    model = EditModel(PipelineConfig())
    still_up: list[int] = []

    async def blur_it(app: EditorApp, pilot: Pilot[None]) -> None:
        """Take the focus off the field of the question that is up."""
        await _press(app=app, pilot=pilot, action=ADD_ACTION,
                     index=_index_of(model, RUNNERS))
        app.screen.query_one(f'#{ASK_KEY_ID}', Input).blur()
        await pilot.pause()
        still_up.append(len(app.screen.query(f'#{ASK_KEY_ID}')))
        await pilot.press(ESCAPE_KEY)
        await pilot.pause()
    _run(model, blur_it)
    assert still_up == [1]
    assert model.verdict is None
