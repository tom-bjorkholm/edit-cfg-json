#! /usr/bin/env python3
# PYTHON_ARGCOMPLETE_OK
"""A small utility for whoever is writing a program on top of this package.

It runs `DumpEditor` over the command line of `edit_cfg_json.cli`, so it needs
no display: it prints what a configuration class makes of a file, with what
the application's own validators say about the values, and with `--save` it
writes the validated file. That is worth having while a program of one's own
is being written, and it is worth having in a continuous integration job,
where an exit code is the whole of what can be read.

**It is no editor, and the editors are `edit-cfg-json-tk` and
`edit-cfg-json-textual`.** They take the very same command line and open a
window and a terminal screen. This utility has no field to type into and
nobody to press Save, which is why it is the one of the three that offers
`--save` at all.

`--unfold` is there for the same reason. A container that would flood a window
opens folded, so a printout of a configuration of any size is mostly a line
saying that it holds more, and there is no control here to open it with. With
`--unfold` every container is open and stays open, which is what says what this
library makes of a whole configuration: every value of it, and the explanation
that every one of its nodes is shown with.

**It reads a settings file of its own, and has no file in the home folder.**
`-c/--cfg` and the environment variable name one, and the shared
`.edit-cfg-json.cfg` is the last thing looked for; the step between those two
is skipped, because that step is there to let the two editors differ and what
they differ about is their keys and their questions, of which this has neither.
What a settings file still says here is what a file is called and what happens
to the one a save writes over.

Run it as `python3 -m edit_cfg_json.dump`. This package installs no command of
its own, and the name `edit-cfg-json` in particular is deliberately free: it
promises the editor this library is for, and a user who typed it and got a
printout would have been misled by the name rather than by anything the
program did.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from collections.abc import Sequence
from typing import Optional
import sys
from edit_cfg_json.backend import DumpEditor
from edit_cfg_json.cli import run_cli
from edit_cfg_json.version_report import EcajVersionReporter

PROGRAM = 'python3 -m edit_cfg_json.dump'
"""How this program is run, which is what its own help text says."""


def main(args: Optional[Sequence[str]] = None) -> int:
    """Run this program and return what it ends with.

    Args:
        args: Optional replacement for `sys.argv[1:]`, mainly for tests.

    Returns:
        What this run ends with, as one of `edit_cfg_json.ExitCode`.
    """
    return run_cli(backend=DumpEditor(), prog=PROGRAM, args=args,
                   version_reporter=EcajVersionReporter(), interactive=False)


if __name__ == '__main__':
    sys.exit(main())
