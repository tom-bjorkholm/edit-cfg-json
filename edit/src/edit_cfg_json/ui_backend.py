#! /usr/bin/env python3
"""What a user interface says about itself, so that it can be chosen.

The editors of this library live in packages of their own, so a program that
opens "the editor this machine can run" has to find out what is installed
before it can open anything. This module is the half of that which a backend
package writes: one `UiBackend` per user interface, registered in the
`edit_cfg_json.ui` entry point group of the package that supplies it.
`edit_cfg_json.ui_choice` is the half that reads them.

**A third party writes one of these exactly as the two backends of this
repository do.** Nothing here names a user interface library, and the priority
a registration reports is the backend author's own answer to which editor is
the better one where a machine can run more than one. The person running the
program has the last word over that answer, which is `Settings.ui_priorities`.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from collections.abc import Callable
from typing import NamedTuple, Optional
from edit_cfg_json.backend import DumpEditor, EditorBackend
from edit_cfg_json.settings import LOWEST_PRIORITY

UI_GROUP = 'edit_cfg_json.ui'
"""Entry point group that every user interface of this library registers in.

A package that supplies a user interface names one `UiBackend` of its own in
this group, and that is the whole of what it has to do to be discovered:

````toml
[project.entry-points."edit_cfg_json.ui"]
qt = "edit_cfg_json_qt:QT_UI"
````
"""


class NoEditorError(Exception):
    """There is no user interface here to open the editor in.

    It is raised where an editor was asked for and the machine can open none:
    a name that no installed package registers, one whose user interface
    cannot run in this context, and a run that named no user interface at all
    on a machine where nothing but a printout is available.
    """


class UiBackend(NamedTuple):
    """One user interface that an editor of this library can be opened in.

    It is what a backend package registers about itself, and everything a
    program has to know to open an editor in that user interface without
    naming its package: whether it can run here at all, how to make its
    backend, and the two facts about a session in it that the shared command
    line of `edit_cfg_json.cli` is told.
    """

    ui_name: str
    """What `--ui` is given to ask for this user interface.

    It is what the person running a program types, so it is a plain word and
    not an import name: `tk`, `textual`, `dump`.
    """

    priority: int
    """Which user interface is the better one where several can run.

    It is zero or more, and the highest of those that can run is the one a
    program opens when nobody said which. `LOWEST_PRIORITY` is the answer of
    something that is not an editor at all: it is never opened unless it was
    asked for by name.

    The backend author decides it, because it is a statement about the user
    interface rather than about one machine. What overrules it is the person
    running the program, through `Settings.ui_priorities`.
    """

    can_run: Callable[[], bool]
    """Whether this user interface can run in this context.

    It is asked, rather than worked out from the packages that are installed,
    because being installed is not the question: a window needs a display and
    a terminal screen needs a terminal, and neither of those is a fact about
    what was installed. It is asked at most once per user interface per run,
    and only until one of them answers yes.
    """

    backend: Callable[[], EditorBackend]
    """How one backend of this user interface is made.

    It is a callable and not a backend, because making one before it is known
    which will be used would build every user interface of the machine in
    order to open one of them.
    """

    interactive: bool = True
    """Whether the user gets a session they could press Save in.

    True for an editor, which is what nearly every registration is. A backend
    that prints once and returns says False, and its program then offers the
    options that stand in for what the user cannot do and answers with the
    verdict of the buffer in its exit code.
    """

    home_settings: Optional[str] = None
    """Name of this user interface's own settings file in the home folder.

    It is read before the file that every program of this library shares, so
    that a user whose window and terminal editors want different keys writes
    one file each. None is a user interface that has nothing of its own to
    differ about, which is what a backend that prints once and returns is.
    """


def _always() -> bool:
    """Return that a printout can be made, which it always can.

    Returns:
        True, because writing to standard output needs neither a display nor
        a terminal and every process has one.
    """
    return True


DUMP_UI = UiBackend(ui_name='dump', priority=LOWEST_PRIORITY, can_run=_always,
                    backend=DumpEditor, interactive=False)
"""The very limited non-interactive backend, as a user interface to choose.

Its priority is the one that is never chosen on its own, because printing a
configuration once is not an editor and somebody who asked for an editor and
got a printout would have been misled by the answer rather than by anything
they typed. `--ui dump` reaches it, which is what registering it is for: a
machine that can run no editor at all can still be asked for the printout.
"""
