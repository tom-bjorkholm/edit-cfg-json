#! /usr/bin/env python3
"""Tests for choosing the user interface that the editor opens in.

**Nothing here asks a real user interface whether it can run**, and the
registrations below are made up for that reason. A real one would answer
according to the machine the tests happen to run on, so a test that used one
would pass on a laptop and fail on a build job while saying nothing about
either. What the two real registrations report is tested where they live; what
is tested here is what is done with the answers.

The one test that does read the real ones asks them what they registered and
never whether they can run, which is a fact about this repository rather than
about the machine.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from typing import Optional
import pytest
from edit_cfg_json import DUMP_UI, DumpEditor, EditModel, NoEditorError, \
    Settings, UiBackend, available_uis, chosen_ui, discovered_uis, \
    ordered_uis, ui_priority
from edit_cfg_json.ui_choice import CANNOT_RUN, NO_EDITOR, UNKNOWN_UI, \
    no_editor_message


class StubEditor:  # pylint: disable=too-few-public-methods
    """A backend that shows nothing, for a registration that is made up."""

    def run_editor(self, model: EditModel) -> None:
        """Do nothing at all with the model it was given."""


def made_up(ui_name: str, priority: int, can_run: bool = True) -> UiBackend:
    """Return one registration that answers what a test wants it to answer.

    Args:
        ui_name: What `--ui` calls it.
        priority: How good an editor it says it is.
        can_run: What it answers about being able to run here.

    Returns:
        A registration of a user interface that does not exist.
    """
    return UiBackend(ui_name=ui_name, priority=priority,
                     can_run=lambda: can_run, backend=StubEditor,
                     home_settings=f'.{ui_name}.cfg')


WINDOW = made_up('window', 10)
"""A registration standing in for the editor of a machine with a display."""

SCREEN = made_up('screen', 5)
"""One standing in for the editor of a machine with a terminal."""

PRINTOUT = made_up('printout', 0)
"""One standing in for what is not an editor and is never chosen."""

NO_DISPLAY = made_up('window', 10, can_run=False)
"""The window editor on a machine that has no display."""


def registry(monkeypatch: pytest.MonkeyPatch, *found: UiBackend) -> None:
    """Make these registrations the ones this installation has.

    Args:
        monkeypatch: What the replacement is undone by.
        found: The registrations that discovery is to answer with.
    """
    monkeypatch.setattr('edit_cfg_json.ui_choice.discovered_uis',
                        lambda: list(found))


def test_real_registrations() -> None:
    """Test the three user interfaces of this repository register themselves.

    They are read through the entry point group, which is what a third party
    registers in as well, so this is the whole mechanism and not only what
    this repository ships. Nothing is asked whether it can run: that is a fact
    about the machine the tests run on and not about the registrations.
    """
    found = {one.ui_name: one for one in discovered_uis()}
    assert set(found) == {'tk', 'textual', 'dump'}
    assert found['tk'].priority > found['textual'].priority
    assert found['textual'].priority > found['dump'].priority
    assert found['dump'] == DUMP_UI


def test_dump_registration() -> None:
    """Test the backend that prints registers as never chosen on its own."""
    assert DUMP_UI.priority == 0
    assert DUMP_UI.can_run()
    assert isinstance(DUMP_UI.backend(), DumpEditor)
    assert not DUMP_UI.interactive
    assert DUMP_UI.home_settings is None


def test_order_is_priority(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test the best editor comes first however they were discovered."""
    registry(monkeypatch, PRINTOUT, SCREEN, WINDOW)
    assert [one.ui_name for one in ordered_uis()] == ['window', 'screen',
                                                      'printout']


def test_same_priority(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test two of one priority are ordered by name and not by chance."""
    registry(monkeypatch, made_up('second', 5), made_up('first', 5))
    assert [one.ui_name for one in ordered_uis()] == ['first', 'second']


@pytest.mark.parametrize('given, expected', [
    ({}, 10), ({'window': 3}, 3), ({'window': 0}, 0), ({'screen': 7}, 10)])
def test_priority_override(given: dict[str, int], expected: int) -> None:
    """Test the machine has the last word over what a backend reported."""
    assert ui_priority(WINDOW, Settings(ui_priorities=given)) == expected


def test_override_reorders(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test a user who prefers the terminal gets it on a machine with both."""
    registry(monkeypatch, WINDOW, SCREEN)
    settings = Settings(ui_priorities={'screen': 20})
    assert chosen_ui(settings=settings).ui_name == 'screen'


def test_available_has_all(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test what can be asked for by name includes what is never chosen.

    The list is what a program builds the choices of its own `--ui` from, so
    leaving out the one that is never chosen on its own would make it the one
    thing that cannot be asked for either.
    """
    registry(monkeypatch, WINDOW, SCREEN, PRINTOUT)
    assert available_uis() == ['window', 'screen', 'printout']


def test_available_leaves_out(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test a user interface that cannot run here is not offered."""
    registry(monkeypatch, NO_DISPLAY, SCREEN)
    assert available_uis() == ['screen']


def test_best_that_can_run(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test a machine with no display is given the editor it can run."""
    registry(monkeypatch, NO_DISPLAY, SCREEN, PRINTOUT)
    assert chosen_ui().ui_name == 'screen'


def test_never_chosen_alone(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test what is not an editor is refused rather than opened.

    It can run, and it is still not what a run that asked for nothing is
    given: somebody who asked for an editor and got a printout would have
    been misled by the answer rather than by anything they typed.
    """
    registry(monkeypatch, NO_DISPLAY, PRINTOUT)
    with pytest.raises(NoEditorError) as refused:
        chosen_ui()
    assert str(refused.value) == no_editor_message(['printout'])


def test_asked_for_by_name(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test the one that is never chosen on its own is given when asked for."""
    registry(monkeypatch, NO_DISPLAY, PRINTOUT)
    assert chosen_ui(ui_name='printout').ui_name == 'printout'


def test_unknown_name(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test a name nothing registers says so rather than opening something."""
    registry(monkeypatch, WINDOW)
    with pytest.raises(NoEditorError) as refused:
        chosen_ui(ui_name='screen')
    assert str(refused.value) == UNKNOWN_UI.format(ui='screen')


def test_named_cannot_run(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test a name that cannot run here is answered about itself.

    It is not answered with another user interface, although one is right
    there and could run: somebody who typed `--ui window` wants that one, and
    being given the terminal instead is a surprise about what they are looking
    at.
    """
    registry(monkeypatch, NO_DISPLAY, SCREEN)
    with pytest.raises(NoEditorError) as refused:
        chosen_ui(ui_name='window')
    assert str(refused.value) == CANNOT_RUN.format(ui='window')


def test_nothing_registered(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test an installation that registers nothing at all says so."""
    registry(monkeypatch)
    with pytest.raises(NoEditorError) as refused:
        chosen_ui()
    assert str(refused.value) == no_editor_message([])


@pytest.mark.parametrize('names', [[], ['printout'], ['printout', 'other']])
def test_no_editor_names_them(names: list[str]) -> None:
    """Test the refusal says what can be asked for, where something can."""
    message = no_editor_message(names)
    assert message.startswith(NO_EDITOR)
    assert all(name in message for name in names)


def test_settings_asked_again(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test a callable settings source really is asked when one is chosen.

    An application that has not got its settings ready at the moment it calls
    passes a callable, and the priorities are one of the answers that is read
    at the moment it is used rather than at the moment it was given.
    """
    registry(monkeypatch, WINDOW, SCREEN)
    asked: list[int] = []

    def source() -> Settings:
        """Answer with the settings, and record that it was asked."""
        asked.append(1)
        return Settings(ui_priorities={'screen': 20})
    assert chosen_ui(settings=source).ui_name == 'screen'
    assert asked


def probe_counter(counted: list[str], ui_name: str,
                  priority: int) -> UiBackend:
    """Return a registration that records every time it is asked.

    It answers that it can run, because what these tests are about is which
    of them were asked at all.

    Args:
        counted: List that the name is appended to on every question.
        ui_name: What `--ui` calls it.
        priority: How good an editor it says it is.

    Returns:
        A registration of a user interface that does not exist.
    """
    def asked() -> bool:
        """Answer yes, having recorded that the question was put."""
        counted.append(ui_name)
        return True
    return UiBackend(ui_name=ui_name, priority=priority, can_run=asked,
                     backend=StubEditor)


def test_asking_stops(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test a machine that can open a window is asked about nothing else.

    Asking costs a display connection or a started process, so the one that
    is opened is the last one asked and the rest are never reached.
    """
    counted: list[str] = []
    registry(monkeypatch, probe_counter(counted, 'first', 10),
             probe_counter(counted, 'second', 5))
    assert chosen_ui().ui_name == 'first'
    assert counted == ['first']


def test_lowest_not_asked(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test one that is never chosen on its own is not even asked.

    Its answer could not change anything, and a question that costs something
    and decides nothing is one worth not putting.
    """
    counted: list[str] = []
    registry(monkeypatch, probe_counter(counted, 'printout', 0),
             made_up('screen', 5))
    assert chosen_ui().ui_name == 'screen'
    assert not counted


def registered_as(monkeypatch: pytest.MonkeyPatch,
                  loaded: list[Optional[object]]) -> None:
    """Make the entry points of the group load to these objects.

    Args:
        monkeypatch: What the replacement is undone by.
        loaded: What each entry point of the group answers with, and a None
            for one that raises `ImportError` instead.
    """
    class _Entry:  # pylint: disable=too-few-public-methods
        """One entry point that answers with what it was made with."""

        def __init__(self, answer: Optional[object]) -> None:
            """Remember what this entry point is to answer with."""
            self._answer = answer

        def load(self) -> object:
            """Return that answer, or raise as a missing package does."""
            if self._answer is None:
                raise ImportError('no such package')
            return self._answer
    entries = [_Entry(answer) for answer in loaded]
    monkeypatch.setattr('edit_cfg_json.ui_choice.entry_points',
                        lambda group: entries)


def test_uninstalled_skipped(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test a registration whose package is not installed takes nothing away.

    A machine with one of the two editors installed has an editor, and a
    refusal about the other one would leave it with none.
    """
    registered_as(monkeypatch, [None, SCREEN])
    assert [one.ui_name for one in discovered_uis()] == ['screen']


def test_wrong_kind_skipped(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test something registered that is no registration is skipped."""
    registered_as(monkeypatch, ['not a registration at all', SCREEN])
    assert [one.ui_name for one in discovered_uis()] == ['screen']


def test_name_twice(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test two packages claiming one name leave the better editor.

    Neither package can see the other, so there is nobody for a refusal to be
    addressed to, and the one whose author believes it is the better editor
    is the one that answers to the name.
    """
    registered_as(monkeypatch, [made_up('screen', 3), made_up('screen', 8)])
    found = discovered_uis()
    assert [one.priority for one in found] == [8]
