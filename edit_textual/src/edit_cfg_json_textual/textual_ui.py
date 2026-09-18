#! /usr/bin/env python3
"""What this package registers about itself, so that it can be chosen.

A program that opens the editor its machine can run finds this through the
`edit_cfg_json.ui` entry point group, and it is the whole of what this package
says about itself: what `--ui` calls it, how good an editor it is where a
machine can run more than one, whether it can run at all here, and how one of
its backends is made.

**Textual being installed is not the question either.** This editor takes over
the terminal it was started in, so what it needs is a terminal: a run whose
input or output is a pipe or a file has nowhere to draw a screen and nobody to
press a key on it, which is what a build job, a shell pipeline and a test
suite with its output captured all are. Asking costs nothing and touches
nothing, unlike the display of a window, so nothing here is remembered: a
process whose output was redirected halfway through its own run gets the
answer that is true now.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import sys
from edit_cfg_json import UiBackend
from edit_cfg_json_textual.textual_editor import TextualEditor

TEXTUAL_PRIORITY = 5
"""How good an editor this is where the machine can run more than one.

It is below the window editor and above what is not an editor at all. A
machine with a display and a terminal has both, and the window is what a user
of such a machine expects to be given; this is the editor of every machine
that has no display, which is where a terminal is not second best but the
whole of what there is.
"""

HOME_SETTINGS = '.edit-cfg-json-textual.cfg'
"""File of the home folder that this user interface reads its settings from.

It is looked for before the file that every program of this library reads, so
that a user whose terminal and window editors want different answers writes
this one and a user who wants one answer writes only the shared file. It
belongs to the user interface and not to the program, so a session in this
editor reads it whichever program opened that session.
"""


def textual_can_run() -> bool:
    """Return whether a screen of this editor can be shown in this run.

    Returns:
        Whether both ends of this process are a terminal, which is what a
        screen that is drawn on one and typed into needs.
    """
    return sys.stdin.isatty() and sys.stdout.isatty()


TEXTUAL_UI = UiBackend(ui_name='textual', backend=TextualEditor,
                       priority=TEXTUAL_PRIORITY, can_run=textual_can_run,
                       home_settings=HOME_SETTINGS)
"""What this package registers in the `edit_cfg_json.ui` entry point group."""
