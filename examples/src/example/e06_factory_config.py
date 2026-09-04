#! /usr/bin/env python3
"""Example 6: a configuration class that the editor cannot construct.

Every example before this one has a configuration class that the editor can
construct for itself: it takes the keyword arguments that `config_as_json`
documents and nothing else, so the editor reads the signature and calls it.

Plenty of real classes are not like that. This one is told which teams exist,
because only the application knows that — it comes from a directory, a
database, or a file that has nothing to do with the configuration — and the
rule that `team` has to name one of them is written with that list in hand. The
editor knows nothing about teams and never will, so it cannot construct this
class at all.

## The loader is how an application says how its class is built

`edit_cfg_json.ConfigLoader` is a callable with four keyword arguments, and
those four are the only things the editor has to give: the JSON text, a file
name it never uses, whether the declared values may fill in what the text
leaves out, and the stream for diagnostics. **Everything else is bound before
the callable reaches the editor.** That is what keeps the editor from needing
to know what a team is, and it is why the protocol never grows a parameter for
one more application.

`edit_cfg_json.derived_loader` is the short way to write one. It is what the
editor does for a class it is given no loader for, offered with an argument of
your own bound into it:

````python
team_loader = derived_loader(partial(TeamConfig, KNOWN_TEAMS))
````

A loader written out by hand is the door for anything that cannot express, and
[e07_chosen_class.py](e07_chosen_class.py) is the example of one.

## What the loader is and is not needed for

It is needed for **reading a file**, which is the one thing that needs an
object that did not exist before. It is not needed for editing, for validating
or for saving: those work on the object the editor already has, by copying it
and applying the buffer with `Config.parse_json`, which runs everything the
class runs while it reads a file. That is worth knowing, because it is why the
list of teams is still there when a validation pass runs: the copy has it.

Run this example in one of the two editors, on the file of teams, and type
into the `team` field to see the rule that only this application could have
written:

````sh
cd examples/src/example
python3 e06_factory_config.py --ui tk -i ../../data/e06_teams.json
python3 e06_factory_config.py --ui textual -i ../../data/e06_teams.json
````

Inside this repository, use the virtual environment that the build creates:
`./venv/bin/python3 examples/src/example/e06_factory_config.py --ui tk`.

Typing `alp` and validating rewrites the field to `alpha` and marks it as a
value a validator changed; typing `delta` is refused with the three names that
exist. Both happen in the fields, because the loader is only about how the
object was made and not about how it is edited.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from collections.abc import Sequence
from functools import partial
from pathlib import Path
from typing import Optional, TextIO
import sys
from config_as_json import Config, ConfigAutoChangeHook, \
    MemberValidationStep, PathOrStr, StrValidator, ValidationPlan
from edit_cfg_json import Descriptions, derived_loader

KNOWN_TEAMS = ('alpha', 'beta', 'gamma')
"""The teams that this application knows about.

A real application reads this from wherever it keeps such a thing. The point of
the example is that it is not in the configuration file and not in the editor:
it is the application's, and the configuration class is told it.
"""


class TeamConfig(Config):
    """Which team does one job, and how many people it needs.

    The list of teams that exist is a constructor argument, because the
    application knows it and neither this class nor the editor could work it
    out. That one argument is what makes this a class the editor cannot
    construct on its own, and therefore a class that is edited through a
    loader.
    """

    # The four keyword arguments are the constructor shape that
    # `config_as_json` documents, and the argument of the application is the
    # fifth. A class the editor can construct on its own has one fewer, and
    # is what every example but this one and example 7 shows.
    # pylint: disable-next=too-many-arguments,too-many-positional-arguments
    def __init__(self, known_teams: Sequence[str],
                 from_json_data_text: Optional[str] = None,
                 from_json_filename: Optional[PathOrStr] = None,
                 auto_ch_hook: Optional[ConfigAutoChangeHook] = None,
                 stderr_file: TextIO = sys.stderr,
                 member_name: Optional[str] = None) -> None:
        """Initialize the configuration with the teams that exist.

        Args:
            known_teams: The teams that the application has. This is the
                argument that the editor knows nothing about, and everything
                this example teaches follows from it being here.
            from_json_data_text: Optional JSON text to parse directly.
            from_json_filename: Optional path to a JSON file to read.
            auto_ch_hook: Hook notified about what reading an older file did.
            stderr_file: Stream used for user-facing diagnostics.
            member_name: Path for reaching this object from the top level
                configuration, so that a diagnostic about a value inside it
                names the whole path. None for the top level itself.
        """
        self.team: str = known_teams[0]
        self.head_count: int = 3
        # A private member is no part of the configuration: `config_as_json`
        # counts the attributes that do not begin with an underscore. So this
        # is remembered for the validation plan below and is neither written
        # to the file nor shown as a row in the editor.
        self._known_teams: tuple[str, ...] = tuple(known_teams)
        super().__init__(from_json_data_text=from_json_data_text,
                         from_json_filename=from_json_filename,
                         auto_ch_hook=auto_ch_hook, stderr_file=stderr_file,
                         member_name=member_name)

    def get_validation_plan(self, stderr_file: TextIO) -> ValidationPlan:
        """Return the one rule, which only the application could have written.

        `best_match=True` is what makes it rewrite rather than refuse where it
        can: `alp` is a unique beginning of `alpha`, so the validator returns
        `alpha` and the editor marks the member as one a validator changed. A
        name that begins no team at all is refused, and the message lists the
        teams that exist.
        """
        _ = stderr_file
        team_rule = StrValidator(allowed_values=self._known_teams,
                                 ignore_case=True, best_match=True)
        return [MemberValidationStep(member_names=['team'],
                                     validator=team_rule)]


team_loader = derived_loader(partial(TeamConfig, KNOWN_TEAMS))
"""How this application constructs its configuration.

`functools.partial` binds the argument that the editor knows nothing about, and
`derived_loader` makes the four keyword arguments of
`edit_cfg_json.ConfigLoader` out of what is left. It is a module level name so
that the programs of this library can be told it with `--loader`.
"""

DESCRIPTIONS: Descriptions = {
    ('team',): 'Which team does this job. The teams are the ones this '
               'installation has, so the editor was told them rather than '
               'reading them from anywhere.',
    ('head_count',): 'How many people the job needs.'}
"""What this example says about the two members it declares."""


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
    run_example(example_name='e06_factory_config', args=args,
                config=TeamConfig(KNOWN_TEAMS), descriptions=DESCRIPTIONS,
                loader=team_loader)


# The usual guard, so that importing this module from a test runs nothing.
if __name__ == '__main__':
    # Running a file directly puts only that file's own folder on sys.path,
    # so the `example` package this file belongs to would not be importable.
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    main()
