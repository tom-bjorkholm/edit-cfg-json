#! /usr/bin/env python3
"""Example a03: the editor the machine can run, for a command with no UI.

The `a` series belongs to the
[programmer's guide](../../../doc/application_programmers_guide.md) for an
application that offers this editor to its own users. Examples a01 and a02 are
the two cases where the command has already chosen: a01 imports
`edit_cfg_json_tk` and always opens a window, a02 imports
`edit_cfg_json_textual` and always opens a terminal screen. This is the third
case, and it is the one most commands are really in: **the command has no user
interface of its own, so it has no reason to have chosen one either.**

The whole of it is one call, and it names no backend at all:

````python
from edit_cfg_json import edit_in_ui
saved = edit_in_ui(PipelineConfig(), in_file='pipeline.json')
````

What that opens, and who decided
--------------------------------
Every installed package that supplies a user interface registers itself, and
`edit_in_ui` opens the best of the ones that can run **here**: a window on a
machine with a display, a terminal screen on a machine without one. So the
same command, with the same line of code, gives a user at a desk a window and
a user over a plain remote shell the terminal editor.

Three people have a say in that, in this order:

1. **The backend author**, who reports a priority for the user interface they
   wrote. The window editor of this repository reports 10, the terminal editor
   5, and the backend that only prints reports 0, which means "never unless
   asked for by name".
2. **Whoever runs the command**, through the `ui_priorities` setting: a user
   who prefers the terminal on a machine that has a display writes
   `{"ui_priorities": {"textual": 20}}` in a settings file, and every program
   of this library opens the one they meant. Section 1.4 of the guide is about
   settings files.
3. **This command's own user, for one run**, through the option below.

What this command adds: an option of its own
--------------------------------------------
`available_uis()` answers with the user interfaces that can run in this
context, which is exactly the list an option like this should accept:

````python
parser.add_argument('--ui', default=None, choices=available_uis())
````

**It is built from the answer and not written out**, and that is the point of
the function. A command with a hand-written list of two would offer `tk` on a
machine with no display, offer nothing at all for a user interface somebody
installs later, and have to be edited every time either changes. The list here
is what this machine can really do, now.

`None` is the default, which is the command saying nothing and letting the
library choose. That is worth keeping as an option: a user who does not care
should not have to.

The two ways a run can end before the editor opens
--------------------------------------------------
- `edit_cfg_json.ConfigLoadError` says that the input file cannot be read as
  this configuration class, exactly as in a01 and a02.
- `edit_cfg_json.NoEditorError` is this example's own: **there is no editor
  here to open.** A machine with no display and without the terminal editor
  installed is such a machine, and so is one where every user interface has
  been given priority 0. It replaces the `tkinter.TclError` that a01 catches
  and the toolkit import that a02 needs, and it is one exception whatever the
  user interfaces happen to be — which is what a command that names no
  toolkit wants, since it cannot catch an exception of a package it does not
  import.

Note that it is an exception and not a `None` answer. `None` already means a
session that ended without saving anything, and a command that could not tell
the two apart would report that its user changed nothing.

Running it
----------
::

    python3 a03_chosen_ui.py
    python3 a03_chosen_ui.py --ui dump
    python3 a03_chosen_ui.py -i ../../data/e13_pipeline.json -o /tmp/p.json
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from pathlib import Path
from typing import NamedTuple, Optional
import argparse
import sys
# Running this file directly puts only its own folder on sys.path, so the
# `example` package it belongs to would not be importable. Adding the folder
# above it makes both ways of using this file work: as a script, and imported
# by a test.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
# pylint: disable-next=wrong-import-position
from edit_cfg_json import ConfigLoadError, NoEditorError, available_uis, \
    edit_in_ui  # noqa: E402
# pylint: disable-next=wrong-import-position
from example._shared_pipeline import DESCRIPTIONS, PipelineConfig, \
    add_editor_files, report_run  # noqa: E402

EXAMPLE = 'a03_chosen_ui'
"""Name this example is run under, which is what its help text says."""

UI_HELP = ('User interface to edit in, instead of the best one for this '
           'machine.')
"""What this command says about the one option it has of its own."""


class ChosenRun(NamedTuple):
    """What one run of this example was told on its command line."""

    ui_name: Optional[str]
    """User interface to open, or None to let the library choose."""

    in_file: Optional[str]
    """File the editor reads, or None for the declared defaults."""

    out_file: Optional[str]
    """File the editor writes, or None for the input file."""


def command_line(args: Optional[list[str]]) -> ChosenRun:
    """Return what one run of this example was told.

    The two file options are the ones every example of this series has, so
    they come from the module the series shares. The third is this example's
    subject, and its accepted values are asked of the library rather than
    written out here: a list written out would offer a window on a machine
    with no display, and would say nothing about a user interface that is
    installed later.

    Args:
        args: Command line of the run, or None for `sys.argv[1:]`.

    Returns:
        The three answers, each None where the command line said nothing.
    """
    parser = argparse.ArgumentParser(prog=EXAMPLE)
    # This is the line the example is about. `available_uis()` asks every
    # registered user interface whether it can run in this context, so on a
    # machine with no display `tk` is not offered at all, and `--ui` accepts
    # exactly what would work.
    parser.add_argument('--ui', default=None, choices=available_uis(),
                        help=UI_HELP)
    # The two file options of the whole series, which are not this example's
    # subject. a01 and a02 get their whole command line from that module.
    add_editor_files(parser)
    parsed = parser.parse_args(args)
    return ChosenRun(ui_name=parsed.ui, in_file=parsed.input,
                     out_file=parsed.output)


def main(args: Optional[list[str]] = None) -> None:
    """Edit the configuration in some editor, then run with what was saved.

    Args:
        args: Optional replacement for `sys.argv[1:]`, mainly for tests.
    """
    chosen = command_line(args)
    try:
        # The one call. There is no backend argument and no user interface
        # package imported anywhere in this file, which is the whole
        # difference between this example and a01 and a02.
        saved = edit_in_ui(PipelineConfig(), ui_name=chosen.ui_name,
                           descriptions=DESCRIPTIONS, in_file=chosen.in_file,
                           out_file=chosen.out_file)
    except ConfigLoadError as refusal:
        sys.exit(str(refusal))
    except NoEditorError as refusal:
        # A message beats a traceback, exactly as it does for the machine
        # with no display in a01. The difference is that this command does not
        # have to know which toolkit was missing in order to say so.
        sys.exit(str(refusal))
    report_run(saved)


# The usual guard, so that importing this module from a test runs nothing.
if __name__ == '__main__':
    main()
