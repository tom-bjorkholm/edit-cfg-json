#! /usr/bin/env python3
# PYTHON_ARGCOMPLETE_OK
"""The `edit-cfg-json-tk` program: edit any configuration class in a window.

It is the command line of `edit_cfg_json.cli` with this package's backend
written into it, so everything about that command line is documented there.
What it opens is a Tk window with a field per member of the configuration
class it was told to edit.

**It is the window editor and nothing else**, which is the difference between
it and `edit-cfg-json`: that one opens whichever editor the machine can run,
and this one is how a user who wants the window says so once and for all,
whatever else is installed. Everything the two differ about beside that is
read from `TK_UI`, so this program and a session the launcher opens in this
editor behave alike down to the settings file they read.

Run it as `edit-cfg-json-tk`, or as `python -m edit_cfg_json_tk` on a machine
whose script folder is not on the path.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from collections.abc import Sequence
from typing import Optional
import sys
from edit_cfg_json import run_cli
from edit_cfg_json_tk.tk_ui import TK_UI
from edit_cfg_json_tk.tk_version import TkVersionReporter

PROGRAM = 'edit-cfg-json-tk'
"""Name that this program is installed under."""


def main(args: Optional[Sequence[str]] = None) -> int:
    """Run this program and return what it ends with.

    Args:
        args: Optional replacement for `sys.argv[1:]`, mainly for tests.

    Returns:
        What this run ends with, as one of `edit_cfg_json.ExitCode`.
    """
    return run_cli(backend=TK_UI.backend(), prog=PROGRAM, args=args,
                   version_reporter=TkVersionReporter(),
                   interactive=TK_UI.interactive,
                   home_settings=TK_UI.home_settings)


if __name__ == '__main__':  # pragma: no cover
    sys.exit(main())
