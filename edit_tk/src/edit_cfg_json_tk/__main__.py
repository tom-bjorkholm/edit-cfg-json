#! /usr/bin/env python3
# PYTHON_ARGCOMPLETE_OK
"""The `edit-cfg-json-tk` program: edit any configuration class in a window.

It is the same program as `edit-cfg-json` with this package's backend in place
of the one that prints, so everything about its command line is documented in
`edit_cfg_json.cli`. What it opens is a Tk window with a field per member of
the configuration class it was told to edit.

Run it as `edit-cfg-json-tk`, or as `python -m edit_cfg_json_tk` on a machine
whose script folder is not on the path.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from collections.abc import Sequence
from typing import Optional
import sys
from edit_cfg_json import run_cli
from edit_cfg_json_tk.tk_editor import TkEditor

PROGRAM = 'edit-cfg-json-tk'
"""Name that this program is installed under."""


def main(args: Optional[Sequence[str]] = None) -> int:
    """Run this program and return what it ends with.

    Args:
        args: Optional replacement for `sys.argv[1:]`, mainly for tests.

    Returns:
        What this run ends with, as one of `edit_cfg_json.ExitCode`.
    """
    return run_cli(backend=TkEditor(), prog=PROGRAM, args=args)


if __name__ == '__main__':
    sys.exit(main())
