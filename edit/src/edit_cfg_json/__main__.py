#! /usr/bin/env python3
# PYTHON_ARGCOMPLETE_OK
"""The `edit-cfg-json` program, reached through the package it belongs to.

It is `edit_cfg_json.launcher` and nothing else, so that a machine whose
script folder is not on `PATH` can still run the launcher, which is how each
of the two editor programs is reachable through its own package as well.

What answers here is the editor the machine can run, because this name
promises an editor: a user who typed the name of the library and got a
printout would have been misled by the name rather than by anything they
typed. The printout is reached by naming it, as
`python3 -m edit_cfg_json.dump`.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import sys
from edit_cfg_json.launcher import main

if __name__ == '__main__':  # pragma: no cover
    sys.exit(main())
