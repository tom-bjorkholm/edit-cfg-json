#! /usr/bin/env python3
"""Which user interface the editor is opened in, on this machine.

`edit_cfg_json.ui_backend` is what a backend package says about itself. This
is what reads every one of those and answers the two questions a program has:
which user interfaces could be asked for here, and which one is opened when
nobody asked.

**Being installed is not the question.** A window needs a display and a
terminal screen needs a terminal, so each registration answers for itself
whether it can run in this context, and this module only puts the answers in
order. The order is the priority each registration reports, with whatever
`Settings.ui_priorities` says about it instead, and the highest of them that
can run is the one that is opened.

**A user interface of the lowest priority is never opened on its own.** It is
asked for by name and at no other time, which is what keeps the backend that
prints once and returns out of the choosing: somebody who asked for an editor
and got a printout would have been misled by the answer rather than by
anything they typed. It is still offered by name, so a machine that can run no
editor at all can be asked for the printout.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from collections.abc import Sequence
from importlib.metadata import EntryPoint, entry_points
from typing import Optional
from edit_cfg_json.settings import LOWEST_PRIORITY, Settings, SettingsSource, \
    current_settings
from edit_cfg_json.ui_backend import NoEditorError, UI_GROUP, UiBackend

UNKNOWN_UI = 'There is no {ui} user interface installed.'
"""Message of the refusal of a `--ui` name that nothing registers."""

CANNOT_RUN = 'The {ui} user interface cannot run here.'
"""Message of the refusal of a user interface that was asked for by name."""

NO_EDITOR = 'No editor can be opened here.'
"""What a program says when nothing it could open is an editor."""

ASK_BY_NAME = (' The user interfaces that can run here are {names}, and one '
               'of them is asked for by name.')
"""What is added to that when something can run, which is normally the case.

It names them because the one that can run is then almost always the backend
that prints once, and somebody who has been told that no editor can be opened
has to be told what they can do instead.
"""

NONE_AT_ALL = ' No user interface of this library can run here at all.'
"""What is added instead when even that one is not registered."""


def _registered(entry: EntryPoint) -> Optional[UiBackend]:
    """Return what one entry point registers, or None where it cannot be read.

    An entry point that cannot be imported is the ordinary case of a user
    interface whose library is not installed, and it is the reason a
    registration is skipped rather than refused: a machine with one of the two
    editors installed has an editor, and a refusal about the other one would
    take it away. Something registered under this group that is not a
    `UiBackend` at all is skipped for the same reason.

    Args:
        entry: One entry point of the group that user interfaces register in.

    Returns:
        What it registers, or None where nothing usable can be read from it.
    """
    try:
        registered = entry.load()
    except (AttributeError, ImportError):
        return None
    return registered if isinstance(registered, UiBackend) else None


def _all_registered() -> list[UiBackend]:
    """Return every registration that this installation can read.

    Returns:
        What each entry point of the group registers, in no order and with a
        name possibly registered more than once.
    """
    found = (_registered(entry) for entry in entry_points(group=UI_GROUP))
    return [one for one in found if one is not None]


def discovered_uis() -> list[UiBackend]:
    """Return every user interface this installation registers, once each.

    Two packages registering one `--ui` name is a clash neither of them can
    see, so it is settled rather than refused: the one that reports the higher
    priority is kept, because that is the one whose author believes it is the
    better editor of the two.

    Returns:
        One registration per `--ui` name, in no particular order.
    """
    best: dict[str, UiBackend] = {}
    for one in sorted(_all_registered(), key=lambda found: -found.priority):
        best.setdefault(one.ui_name, one)
    return list(best.values())


def ui_priority(backend: UiBackend, settings: Settings) -> int:
    """Return the priority that this machine gives one user interface.

    Args:
        backend: What one user interface registered about itself.
        settings: What this machine has decided about the editor.

    Returns:
        What the settings say about it, and what it reported where they say
        nothing.
    """
    return settings.ui_priorities.get(backend.ui_name, backend.priority)


def ordered_uis(settings: SettingsSource = Settings()) -> list[UiBackend]:
    """Return every registered user interface, the preferred one first.

    Nothing is asked whether it can run here, because ordering is not
    probing: a caller walks this list and asks, which is what stops a machine
    that can open a window from ever being asked about a terminal.

    Args:
        settings: What this machine has decided about the editor, or a
            callable that answers with it.

    Returns:
        The registrations, by descending priority and then by name, so that
        two user interfaces of one priority are in an order that does not
        depend on which package was installed first.
    """
    now = current_settings(settings)
    return sorted(discovered_uis(),
                  key=lambda one: (-ui_priority(one, now), one.ui_name))


def available_uis(settings: SettingsSource = Settings()) -> list[str]:
    """Return the names of the user interfaces that can run here.

    This is what a program of somebody else's builds the choices of its own
    `--ui` option from, so every name here can be asked for — including one
    whose priority says that it is never opened without being asked for.

    Every registration is asked whether it can run, which is what this is for
    and is more than choosing one costs.

    Args:
        settings: What this machine has decided about the editor, or a
            callable that answers with it.

    Returns:
        The `--ui` name of each user interface that can run in this context,
        the preferred one first.
    """
    return [one.ui_name for one in ordered_uis(settings) if one.can_run()]


def no_editor_message(names: Sequence[str]) -> str:
    """Return what a program says when it can open no editor at all.

    Args:
        names: The user interfaces that can run here, which is normally the
            one that prints and nothing else.

    Returns:
        The whole of what the user is told.
    """
    if not names:
        return NO_EDITOR + NONE_AT_ALL
    return NO_EDITOR + ASK_BY_NAME.format(names=', '.join(names))


def _named_ui(ui_name: str, ordered: Sequence[UiBackend]) -> UiBackend:
    """Return the user interface that was asked for by name.

    A name that was asked for is answered about itself and never with another
    user interface: somebody who typed `--ui tk` on a machine with no display
    is told that, rather than given the terminal editor they did not ask for.

    Args:
        ui_name: The `--ui` name that one run asked for.
        ordered: Every registered user interface.

    Returns:
        The registration of that name.

    Raises:
        NoEditorError: Nothing registers that name, or it cannot run here.
    """
    for one in ordered:
        if one.ui_name == ui_name:
            if one.can_run():
                return one
            raise NoEditorError(CANNOT_RUN.format(ui=ui_name))
    raise NoEditorError(UNKNOWN_UI.format(ui=ui_name))


def _best_ui(ordered: Sequence[UiBackend], settings: Settings) -> UiBackend:
    """Return the first user interface of this machine that can run.

    They are asked in order and the asking stops at the first yes, so a
    machine that can open a window is never asked about anything else. One of
    the lowest priority is not asked at all, because a yes from it would not
    be an editor.

    Args:
        ordered: Every registered user interface, the preferred one first.
        settings: What this machine has decided about the editor.

    Returns:
        The registration to open the editor in.

    Raises:
        NoEditorError: None of them is an editor that can run here.
    """
    for one in ordered:
        if ui_priority(one, settings) > LOWEST_PRIORITY and one.can_run():
            return one
    raise NoEditorError(no_editor_message([one.ui_name for one in ordered
                                           if one.can_run()]))


def chosen_ui(ui_name: Optional[str] = None,
              settings: SettingsSource = Settings()) -> UiBackend:
    """Return the user interface that one run opens the editor in.

    Args:
        ui_name: The `--ui` name that this run asked for, or None to open
            the editor that this machine can run.
        settings: What this machine has decided about the editor, or a
            callable that answers with it.

    Returns:
        The registration to open the editor in.

    Raises:
        NoEditorError: The name that was asked for is not one that can run
            here, or nothing was asked for and this machine can open no
            editor at all.
    """
    now = current_settings(settings)
    ordered = ordered_uis(now)
    if ui_name is not None:
        return _named_ui(ui_name=ui_name, ordered=ordered)
    return _best_ui(ordered=ordered, settings=now)
