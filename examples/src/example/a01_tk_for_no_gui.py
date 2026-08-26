#! /usr/bin/env python3
"""Example a01: the Tk editor for a command with no user interface.

The `a` series belongs to the
[programmer's guide](../../../doc/application_programmers_guide.md) for an
application that offers this editor to its own users. This is its first case:
a command that runs in a terminal, has no graphical user interface of its own,
and wants one window for editing its configuration.

The whole of it is one call:

````python
from edit_cfg_json_tk import edit
saved = edit(PipelineConfig(), in_file='pipeline.json')
````

The editor owns the window and the loop
---------------------------------------
`edit` creates the `tkinter.Tk` of the process, runs its event loop, and
returns when the user closes the editor. That is exactly what a command with
no user interface wants, and it is exactly what an application that *already*
runs Tk must not call: a second `tkinter.Tk` is a second Tcl interpreter, and
no widget, variable, font or image crosses between two of them. Such an
application uses `edit_cfg_json_tk.TkEditorPanel` instead, which is
e15_window_tk.py and e13_embedded_tk.py.

So the rule for this case is a rule about what the command has *not* done: it
created no `tkinter.Tk` before this call and creates none after it.

Blocking is the point
---------------------
Nothing of this command runs while the editor is open, and nothing needs to:
the user is editing, and the command has nothing to do until they have
finished. That is what lets the outcome be a return value rather than a
callback, which is the whole difference between this case and the four that
mount the editor in a window an application already owns.

What comes back, and what does not
----------------------------------
`edit` answers with **the configuration object that was written**, or `None`
when the session ended without a save. Both are ordinary outcomes and neither
is an error.

The object handed in is never modified, so the `PipelineConfig()` this command
constructed is still holding the values it started with even after a save.
What reached the file is the object that comes back, and that is the one to go
on with. `report_run` is where this example does that.

The two ways a run can end before the editor opens
--------------------------------------------------
- `edit_cfg_json.ConfigLoadError` says that the input file cannot be read as
  this configuration class: it is not there, it is not JSON, or the class
  refuses what is in it. A command catches it and says so, rather than letting
  the user get an editor quietly showing default values instead of the file
  they asked for.
- `tkinter.TclError` says that this machine has no display to put a window on,
  which is what a command run over a plain remote shell or from a build job
  meets. It is caught for the same reason: a message beats a traceback.

Running it
----------
::

    python3 a01_tk_for_no_gui.py
    python3 a01_tk_for_no_gui.py -i ../../data/e13_pipeline.json -o /tmp/p.json
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from pathlib import Path
from typing import Optional
import sys
import tkinter
# Running this file directly puts only its own folder on sys.path, so the
# `example` package it belongs to would not be importable. Adding the folder
# above it makes both ways of using this file work: as a script, and imported
# by a test.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
# pylint: disable-next=wrong-import-position
from edit_cfg_json import ConfigLoadError  # noqa: E402
# pylint: disable-next=wrong-import-position
from edit_cfg_json_tk import edit  # noqa: E402
# pylint: disable-next=wrong-import-position
from example._shared_pipeline import DESCRIPTIONS, PipelineConfig, \
    editor_files, report_run  # noqa: E402

NO_DISPLAY = 'This command needs a display to show its editor on.'
"""What this command says on a machine that cannot open a window."""


def main(args: Optional[list[str]] = None) -> None:
    """Edit the configuration in a window, then run with what was saved.

    Args:
        args: Optional replacement for `sys.argv[1:]`, mainly for tests.
    """
    # Both examples of this pair make this one call, because that call is what
    # each of them is about and the import above is the whole difference
    # between them. Keeping each example complete on its own is worth more
    # here than sharing the statement would be.
    # pylint: disable=duplicate-code
    files = editor_files('a01_tk_for_no_gui', args)
    try:
        saved = edit(PipelineConfig(), descriptions=DESCRIPTIONS,
                     in_file=files.in_file, out_file=files.out_file)
    except ConfigLoadError as refusal:
        sys.exit(str(refusal))
    except tkinter.TclError:
        sys.exit(NO_DISPLAY)
    report_run(saved)


# The usual guard, so that importing this module from a test runs nothing.
if __name__ == '__main__':
    main()
