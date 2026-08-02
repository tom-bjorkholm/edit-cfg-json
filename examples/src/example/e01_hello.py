#! /usr/bin/env python3
"""Example 1: greet from all three edit-cfg-json packages.

This is the smallest possible example. It does not edit anything yet. Its
purpose is to show how the three distributions relate to each other, and
which import name belongs to which distribution:

| Distribution            | Import name             | What it is       |
| ----------------------- | ----------------------- | ---------------- |
| `edit-cfg-json`         | `edit_cfg_json`         | the core         |
| `edit-cfg-json-tk`      | `edit_cfg_json_tk`      | Tkinter backend  |
| `edit-cfg-json-textual` | `edit_cfg_json_textual` | Textual backend  |

The distribution name (what you `pip install`) uses hyphens; the import
name (what you `import`) uses underscores. That is the normal Python
convention, and it is worth getting used to before reading the later
examples.

Run this example with:

````sh
python3 examples/src/example/e01_hello.py
````
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

# Import from the top-level package in every case. The public API of each
# package is re-exported from its `__init__.py`, so you never need to know
# which internal module a name actually lives in. Importing from an
# internal module would tie your code to an implementation detail that is
# allowed to move between releases.
from edit_cfg_json import core_greeting
from edit_cfg_json_textual import textual_greeting
from edit_cfg_json_tk import tk_greeting


def show_core() -> None:
    """Print the greeting from the user interface agnostic core.

    Notice that this works without either backend being installed. The
    core never imports `tkinter` or `textual`; that is what makes it
    usable in an application that has no user interface at all.
    """
    print(core_greeting())


def show_backends() -> None:
    """Print the greeting from each of the two user interface backends.

    Each backend greeting starts with the core greeting, because each
    backend calls the core rather than repeating what the core does. That
    is the layering the three packages exist to enforce: the backends stay
    thin, and everything worth testing lives in the core.
    """
    print(tk_greeting())
    print(textual_greeting())


def main() -> None:
    """Print all three greetings."""
    show_core()
    show_backends()


# The usual guard, so that importing this module from a test does not
# print anything, while running the file directly does.
if __name__ == '__main__':
    main()
