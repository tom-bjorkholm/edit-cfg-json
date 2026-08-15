#! /usr/bin/env python3
# PYTHON_ARGCOMPLETE_OK
"""The `edit-cfg-json-textual` program: edit any class in the terminal.

It is the same program as `edit-cfg-json` with this package's backend in place
of the one that prints, so everything about its command line is documented in
`edit_cfg_json.cli`. What it opens is a Textual screen with a field per member
of the configuration class it was told to edit.

Run it as `edit-cfg-json-textual`, or as `python -m edit_cfg_json_textual` on
a machine whose script folder is not on the path.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from collections.abc import Sequence
from typing import Optional
import sys
from edit_cfg_json import run_cli
from edit_cfg_json_textual.textual_editor import TextualEditor
from edit_cfg_json_textual.textual_version import TextualVersionReporter

PROGRAM = 'edit-cfg-json-textual'
"""Name that this program is installed under."""

HOME_SETTINGS = '.edit-cfg-json-textual.cfg'
"""File of the home folder that this program reads its own settings from.

It is looked for before the file that every program of this library reads, so
that a user whose terminal and window editors want different answers writes
this one and a user who wants one answer writes only the shared file.
"""


def main(args: Optional[Sequence[str]] = None) -> int:
    """Run this program and return what it ends with.

    Args:
        args: Optional replacement for `sys.argv[1:]`, mainly for tests.

    Returns:
        What this run ends with, as one of `edit_cfg_json.ExitCode`.
    """
    return run_cli(backend=TextualEditor(), prog=PROGRAM, args=args,
                   version_reporter=TextualVersionReporter(),
                   home_settings=HOME_SETTINGS)


if __name__ == '__main__':
    sys.exit(main())
