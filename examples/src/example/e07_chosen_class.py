#! /usr/bin/env python3
"""Example 7: the file decides which configuration class is edited.

An application can have more than one mode, and the file it is started with can
be the file that says which mode. A CAD program in a two dimensional drawing
mode and the same program modelling in three dimensions is the case
`config_as_json` teaches with `config_factory_from_json`, and the two
configurations below are that case written small: the same three members, and
different rules about them, because a drawing may be laid out on a finer grid
than a model may.

A loader is what the editor is told for this, exactly as in
[e06_factory_config.py](e06_factory_config.py), but written by hand instead of
made by `derived_loader` alone: the class is not known until the JSON has been
looked at, which nothing but the application can do. Choosing it is the only
thing this loader adds, so it hands the rest over to `derived_loader` for the
class it chose.

## Two rules that make this work

**A loader answers a call with no JSON source.** The editor asks for one when
it is started on the declared values rather than on a file, and there is
nothing to look at then. So a loader like this one names the class it uses for
a configuration that does not exist yet, which is `Cad2DConfig` here.

**The class is chosen when the file is loaded, and the session then edits that
class.** The rows are that class's members, the label is its docstring, and
nothing asks the loader again while the user types. A save does ask, once, with
the text the file would hold, and that is where a value which would select
another class is caught — before the file is written and not after it, when it
would be the application meeting it.

Those two together are the whole of what a class-choosing loader costs.

Run this example in one of the two editors, once per file, and read the title
of each: the same program opens two different configuration classes, and the
title is where it says which one it opened.

````sh
cd examples/src/example
python3 e07_chosen_class.py --ui tk -i ../../data/e07_drawing.json
python3 e07_chosen_class.py --ui textual -i ../../data/e07_model.json
````

Inside this repository, use the virtual environment that the build creates:
`./venv/bin/python3 examples/src/example/e07_chosen_class.py --ui tk`.

Change `mode` in either of them and press Save, and the save is refused with
the message that says why: the file that would be written is one this
application would read back as the other class. That refusal is worth meeting
where a user meets it, which is at the Save button.

`--ui dump` is the very limited non-interactive user interface. These two
print the two classes:

````sh
cd examples/src/example
python3 e07_chosen_class.py --ui dump -i ../../data/e07_drawing.json
python3 e07_chosen_class.py --ui dump -i ../../data/e07_model.json
````

And these two are the same two refusals as at the Save button above, reached
without one. The first would write a file that this application reads as the
other class, and says so; the second would write one it could not read at all,
and says what its own rule said about it:

````sh
cd examples/src/example
python3 e07_chosen_class.py --ui dump -i ../../data/e07_model.json \
    --set mode=2D -o /tmp/out.json --save
python3 e07_chosen_class.py --ui dump -i ../../data/e07_drawing.json \
    --set mode=3D -o /tmp/out.json --save
````

The same through the small non-interactive utility of the core package, where
`--class` is how a script says which of the two classes it is prepared to go
on with. The first opens whichever class the file selects, the second insists
on that class and opens it, and the third insists on the other one and stops
with a message and an exit code of its own:

````sh
export PYTHONPATH=examples/src
python3 -m edit_cfg_json.dump --module example.e07_chosen_class \
    --loader chosen_config -i examples/data/e07_model.json
python3 -m edit_cfg_json.dump --module example.e07_chosen_class \
    --class Cad3DConfig --loader chosen_config -i examples/data/e07_model.json
python3 -m edit_cfg_json.dump --module example.e07_chosen_class \
    --class Cad2DConfig --loader chosen_config -i examples/data/e07_model.json
````
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from pathlib import Path
from typing import Optional, TextIO
import json
import sys
from config_as_json import Config, ConfigAutoChangeHook, \
    IntFloatValidator, MemberValidationStep, PathOrStr, StrValidator, \
    ValidationPlan
from edit_cfg_json import Descriptions, derived_loader

MODE_KEY = 'mode'
"""Member that says which of the two configurations one file holds."""

MODE_2D = '2D'
"""Value of that member for a drawing configuration."""

MODE_3D = '3D'
"""Value of that member for a model configuration."""

FINEST_DRAWING_GRID = 0.05
"""Finest grid that a two dimensional drawing may use, in millimetres."""

FINEST_MODEL_GRID = 1.0
"""Finest grid that a three dimensional model may use, in millimetres.

It is coarser than a drawing's, which is the whole difference between the rules
of the two classes and is what makes a file of one of them a file the other
would refuse.
"""

COARSEST_GRID = 100.0
"""Coarsest grid that either of them may use, in millimetres."""


class CadConfig(Config):
    """What both modes of this application hold, and both modes' rules.

    The two classes below hold the same three members and differ in one rule,
    so everything is here and each of them says what it is. That is ordinary
    Python and nothing the editor knows about: what the editor is given is
    whichever of the two classes the loader answered with.

    Both class attributes below are attributes of the class and not of the
    object, so `config_as_json` does not count them among the members: it
    counts the attributes of the object whose names do not begin with an
    underscore.
    """

    OWN_MODE: str = MODE_2D
    """Which mode this class configures, which the subclasses answer."""

    FINEST_GRID: float = FINEST_DRAWING_GRID
    """Finest grid this mode allows, which the subclasses answer."""

    def __init__(self, from_json_data_text: Optional[str] = None,
                 from_json_filename: Optional[PathOrStr] = None,
                 auto_ch_hook: Optional[ConfigAutoChangeHook] = None,
                 stderr_file: TextIO = sys.stderr) -> None:
        """Initialize the configuration of one mode.

        Args:
            from_json_data_text: Optional JSON text to parse directly.
            from_json_filename: Optional path to a JSON file to read.
            auto_ch_hook: Hook notified about what reading an older file did.
            stderr_file: Stream used for user-facing diagnostics.
        """
        self.mode: str = self.OWN_MODE
        self.project_name: str = 'demo-part'
        self.grid_size_mm: float = FINEST_MODEL_GRID
        super().__init__(from_json_data_text=from_json_data_text,
                         from_json_filename=from_json_filename,
                         auto_ch_hook=auto_ch_hook, stderr_file=stderr_file)

    def get_validation_plan(self, stderr_file: TextIO) -> ValidationPlan:
        """Return the rules of this mode, one of which the subclass says.

        Both modes hold the same members, and it is only the finest grid that
        differs. The mode member is validated against the two names that exist
        and not against this class's own name: what this example is about is a
        file whose mode has been edited to the other one, and a rule that
        refused that outright would hide what the save then does with it.
        """
        _ = stderr_file
        modes = StrValidator(allowed_values=(MODE_2D, MODE_3D),
                             ignore_case=False)
        grid = IntFloatValidator(min_value=self.FINEST_GRID,
                                 max_value=COARSEST_GRID, allowed_values=None)
        return [MemberValidationStep(member_names=[MODE_KEY], validator=modes),
                MemberValidationStep(member_names=['grid_size_mm'],
                                     validator=grid)]


class Cad2DConfig(CadConfig):
    """Settings of the two dimensional drawing mode of this application.

    A drawing is laid out on paper, so it may use a grid as fine as the
    thickness of a line, and nothing in it is seen from an angle. This is also
    the class the editor is given when there is no file at all, because a
    configuration that does not exist yet has to be of some class and a drawing
    is what this application starts with.
    """

    OWN_MODE: str = MODE_2D
    """A drawing configuration is the one this application starts with."""

    FINEST_GRID: float = FINEST_DRAWING_GRID
    """A drawing may be laid out on a grid finer than a model may."""


class Cad3DConfig(CadConfig):
    """Settings of the three dimensional modelling mode of this application.

    A model is measured in the space it will be built in, so the finest grid it
    may use is coarser than a drawing's: a solid positioned to a hundredth of a
    millimetre is a solid nobody can make. Everything else about the two modes
    is the same, which is why a file has to say which of them it holds.
    """

    OWN_MODE: str = MODE_3D
    """A model configuration is what a file with this mode holds."""

    FINEST_GRID: float = FINEST_MODEL_GRID
    """A model may not be laid out on the finest drawing grid."""


def _chosen_class(text: Optional[str]) -> type[CadConfig]:
    """Return the configuration class that one JSON text selects.

    Text that is not JSON at all is answered with the default class rather than
    refused here, so that the configuration class itself produces the message
    about it. That message is the one `config_as_json` writes for a file it
    cannot read, and it says more than a matcher could.

    Args:
        text: JSON text of the file, or None when there is no file. There is
            none when the editor is started on the values the application
            declares, and the class of those is the one for a configuration
            that does not exist yet.

    Returns:
        The class to construct.
    """
    if text is None:
        return Cad2DConfig
    try:
        data = json.loads(text)
    except ValueError:
        return Cad2DConfig
    if isinstance(data, dict) and data.get(MODE_KEY) == MODE_3D:
        return Cad3DConfig
    return Cad2DConfig


def chosen_config(*, from_json_data_text: Optional[str] = None,
                  from_json_filename: Optional[PathOrStr] = None,
                  ok_to_use_defaults: bool = False,
                  stderr_file: TextIO = sys.stderr) -> Config:
    """Construct the configuration class that the JSON selects.

    This is an `edit_cfg_json.ConfigLoader` written out, and the four keyword
    arguments are the whole of the protocol. One of them is what makes it more
    than `config_as_json.ConfigFactory`: the policy for members a file leaves
    out. That is also why a configuration is constructed and the JSON is
    applied to it afterwards rather than being handed to the constructor —
    `Config.__init__` takes no `ok_to_use_defaults`.

    Args:
        from_json_data_text: JSON text to apply, or None for the values that
            the configuration class declares.
        from_json_filename: File to read, which the editor never passes,
            because it reads its own input files.
        ok_to_use_defaults: Whether the declared values may fill in the
            members that the JSON text does not hold.
        stderr_file: Stream used for user-facing diagnostics.

    Returns:
        A drawing configuration or a model configuration, as the JSON says.

    Raises:
        ValueError: A file name was given. The editor reads its own input
            files and never passes one, so a name is a mistake that the loader
            of the core refuses rather than ignoring it.
    """
    # Choosing the class is the whole of what this loader adds, so everything
    # after that is handed over to the loader that the core would have made for
    # that class on its own. Writing the construction and the parse out here
    # again would be writing what `derived_loader` already is, and it is worth
    # seeing that the two halves really are separate.
    chosen = derived_loader(_chosen_class(from_json_data_text))
    return chosen(from_json_data_text=from_json_data_text,
                  from_json_filename=from_json_filename,
                  ok_to_use_defaults=ok_to_use_defaults,
                  stderr_file=stderr_file)


DESCRIPTIONS: Descriptions = {
    (MODE_KEY,): 'Which mode this file configures. It is what the loader of '
                 'this application looks at to decide which configuration '
                 'class a file holds, so changing it here is refused by the '
                 'save rather than followed.',
    ('project_name',): 'Name of the part that is being drawn or modelled.',
    ('grid_size_mm',): 'Spacing of the grid, in millimetres. A drawing may '
                       f'use one as fine as {FINEST_DRAWING_GRID} and a '
                       f'model one as fine as {FINEST_MODEL_GRID}.'}
"""What this example says about the three members that both modes declare."""


def main(args: Optional[list[str]] = None) -> None:
    """Run this example from the command line.

    Args:
        args: Optional replacement for `sys.argv[1:]`, mainly for tests.
    """
    # The import is inside the function so that running this file directly
    # works. The block at the end of the file puts the examples source folder
    # on sys.path first, and only after that is `example.cmd_line` importable.
    # pylint: disable-next=import-outside-toplevel
    from example.cmd_line import run_example
    run_example(example_name='e07_chosen_class', args=args,
                config=Cad2DConfig(), descriptions=DESCRIPTIONS,
                loader=chosen_config)


# The usual guard, so that importing this module from a test runs nothing.
if __name__ == '__main__':
    # Running a file directly puts only that file's own folder on sys.path,
    # so the `example` package this file belongs to would not be importable.
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    main()
