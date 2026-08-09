#! /usr/bin/env python3
# PYTHON_ARGCOMPLETE_OK
"""The `edit-cfg-json` program: say what a configuration file amounts to.

It is the program of the package that imports no user interface library, so it
needs no display: it prints the configuration as text, with what the
application's own validators make of it, and with `--save` it writes the
validated file. That makes it a configuration checker for a terminal or for a
continuous integration job, and not an editor.

**For an editor, run `edit-cfg-json-tk` or `edit-cfg-json-textual`**, which
take the very same command line and open a window and a terminal screen. This
program has no field to type into and nobody to press Save, which is why it is
the one of the three that offers `--save` at all.

Run it as `edit-cfg-json`, or as `python -m edit_cfg_json` on a machine whose
script folder is not on the path.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from collections.abc import Sequence
from typing import Optional
import sys
from edit_cfg_json.backend import DumpEditor
from edit_cfg_json.cli import run_cli

PROGRAM = 'edit-cfg-json'
"""Name that this program is installed under."""


def main(args: Optional[Sequence[str]] = None) -> int:
    """Run this program and return what it ends with.

    Args:
        args: Optional replacement for `sys.argv[1:]`, mainly for tests.

    Returns:
        What this run ends with, as one of `edit_cfg_json.ExitCode`.
    """
    return run_cli(backend=DumpEditor(), prog=PROGRAM, args=args,
                   interactive=False)


if __name__ == '__main__':
    sys.exit(main())
