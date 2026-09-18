#! /usr/bin/env python3
"""What this package registers about itself, so that it can be chosen.

A program that opens the editor its machine can run finds this through the
`edit_cfg_json.ui` entry point group, and it is the whole of what this package
says about itself: what `--ui` calls it, how good an editor it is where a
machine can run more than one, whether it can run at all here, and how one of
its backends is made.

**Tkinter being importable is not the question**, and that is what this module
is really about: Tkinter comes with Python on the machines this library
supports, while the window it opens needs a display that a plain remote shell,
a build job and a machine with no graphical session all lack. So the question
is asked of Tk itself rather than of the import, by building a Tk and throwing
it away.

**It is asked in a process of its own**, which is the one decision here worth
writing down. A Tk that this process built and destroyed would be the first of
two in the process that goes on to open the editor, and a failed one leaves
Tcl state behind that has crashed the next Tk in this repository's own tests.
A child process cannot do that: it answers with its exit code and takes
everything it made with it. The answer is remembered, because the display of a
machine does not appear while one program runs and the child is the expensive
part of asking.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from functools import cache
import subprocess
import sys
from edit_cfg_json import UiBackend
from edit_cfg_json_tk.tk_panel import TkEditor

TK_PRIORITY = 10
"""How good an editor this is where the machine can run more than one.

It is the highest of the user interfaces this repository ships, because a
window is what a user of a machine with a display expects to be given: it
resizes, it scrolls with the pointer, and it is reached by whoever started the
program from somewhere that is not a terminal at all.
"""

HOME_SETTINGS = '.edit-cfg-json-tk.cfg'
"""File of the home folder that this user interface reads its settings from.

It is looked for before the file that every program of this library reads, so
that a user whose window and terminal editors want different answers writes
this one and a user who wants one answer writes only the shared file. It
belongs to the user interface and not to the program, so a session in this
editor reads it whichever program opened that session.
"""

PROBE = 'import tkinter; tkinter.Tk().destroy()'
"""What the child process runs to find out whether there is a display.

Building the Tk is what asks the question, because that is what connects to
the display and what raises where there is none. Nothing is drawn: a window is
mapped when the event loop runs or the window is updated, and this does
neither.
"""


@cache
def tk_can_run() -> bool:
    """Return whether a Tk window can be opened on this machine.

    The answer is worked out once and remembered afterwards. Asking is
    starting a Python, so a program that asks every installed user interface
    what it can do would otherwise pay for it more than once.

    Returns:
        Whether the child process built a Tk and destroyed it again.
    """
    try:
        done = subprocess.run([sys.executable, '-c', PROBE], check=False,
                              capture_output=True)
    except OSError:
        return False
    return done.returncode == 0


TK_UI = UiBackend(ui_name='tk', priority=TK_PRIORITY, backend=TkEditor,
                  can_run=tk_can_run, home_settings=HOME_SETTINGS)
"""What this package registers in the `edit_cfg_json.ui` entry point group."""
