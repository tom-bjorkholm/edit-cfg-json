#! /usr/bin/env python3
"""Example 3: telling the user what the values are for.

The two examples before this one showed the editor working out *what* the
members of a configuration are. This one is about something the editor
cannot work out at all: what they *mean*. A member called `max_items` has a
type, a default and a validator, and none of those says whether 20 is a lot.

There are two sources of that kind of text, they are independent, and both of
them are optional:

- **The docstring of the configuration class** labels the configuration
  object. Nothing has to be passed for this: the class already has it, and
  the editor reads it.
- **A description mapping** labels the individual members. This one the
  application has to pass, and the reason is worth knowing, because it is not
  laziness on the editor's part.

## Why the members need a mapping and the class does not

Python keeps a class docstring and throws a member docstring away. Writing

````python
self.max_items: int = 20
'''How many items one report may hold.'''
````

is legal and does nothing at all: the string is an expression statement, and
the compiler discards it. The PEP 526 annotation is no better, because an
annotation on an *instance* attribute is recorded nowhere at runtime. So
there is nothing for the editor to read, and the application says it in a
mapping instead:

````python
DESCRIPTIONS: Descriptions = {
    ('max_items',): 'How many items one report may hold, from 1 to 100.',
}
saved = edit(config=DescribedConfig(), backend=TkEditor(),
             descriptions=DESCRIPTIONS)
````

A member is named by the path that addresses it, which is a tuple, and a flat
configuration has one step in every path. The tuple shape is what will let a
member inside a list, a dict or a nested configuration object be described
without a second way of naming it, and it is why the mapping is a mapping:
a path is hashable.

## What is deliberately left out

`report_file` has no description in the mapping below, and that is the point
of it. The editor shows it as an ordinary member with nothing under it. An
application that describes half of its configuration gets half of its
configuration explained, rather than an error at start up, because a missing
description is a cosmetic gap and refusing to open an editor over one would
be a real fault.

## Why the range is in the description and not read out of the validator

`max_items` has to be between 1 and 100, and the description says so in
words. The editor could not have written that sentence: it never reads the
constraints out of a validator, and that is a permanent decision rather than
a thing not built yet. An application may write a validator of its own with
any rule in it, so reading constraints would work for the validators that
`config_as_json` ships and quietly fail for everyone else's. What the editor
does instead is *run* the real validators, which is right for every validator
that exists or ever will.

The consequence for the application is this one: if a rule is worth telling
the user about, tell them in the description. The validator is what enforces
it; the description is what explains it.

## The show and hide key

Explanations take a line per member, and a user who knows this configuration
by heart does not want them. So the editor starts with them shown and `f1`,
or `ctrl+g`, takes them away again — the Tk backend has an Explain button
too, and the Textual command palette an Explain entry. What stays visible
either way is the one line summary of the class, which is the first paragraph
of its docstring: one line for the whole configuration is worth keeping, and
the rest is what gets out of the way.

Which of the two states the editor is in belongs to the model and not to
either user interface, so the two backends cannot end up disagreeing about it.

Run this example in one of the two editors, and press `f1`, which is what
this example is for:

````sh
python3 examples/src/example/e03_described_config.py --ui tk
python3 examples/src/example/e03_described_config.py --ui textual
````

Inside this repository, use the virtual environment that the build creates:
`./venv/bin/python3 examples/src/example/e03_described_config.py --ui tk`.

The Tkinter window offers it as a tick-box in its button row, where the tick
says which of the two states the window is in, and the Textual footer renames
its action for what the next press will do. That is the one place the two
backends deliberately answer the same question differently, because a button
row and a footer of keys offer an action differently.

`--ui dump` is the very limited non-interactive user interface, and
`--toggle-explain` is what stands in for the key there. These two print the
same model with the explanations shown and hidden:

````sh
cd examples/src/example
python3 e03_described_config.py --ui dump
python3 e03_described_config.py --ui dump --toggle-explain
````

And these show that the explanations are text about the members and not a
change to them: a described member is edited, refused and written exactly as
an undescribed one is.

````sh
cd examples/src/example
python3 e03_described_config.py --ui dump -i ../../data/e03_complete.json
python3 e03_described_config.py --ui dump --set max_items=500
python3 e03_described_config.py --ui dump --set priority=HI
````

The last of those is worth trying: `HI` is no prefix of any of the three
names of `Priority`, so it is refused, and the refusal appears below that one
member rather than in the block at the bottom. Example 4 is about why the
editor can say which member a refusal is about, and about the one kind of
rule for which it cannot.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from enum import Enum, auto
from pathlib import Path
from typing import Optional, TextIO
import sys
from config_as_json import Config, IntFloatValidator, MemberValidationStep, \
    ParseConverter, PathOrStr, ValidationPlan, ValueTypeValidator
from edit_cfg_json import Descriptions

FEWEST_ITEMS = 1
"""Smallest number of items that this configuration accepts."""

MOST_ITEMS = 100
"""Largest number of items that this configuration accepts."""


class Priority(Enum):
    """How urgent the work described by a configuration is."""

    LOW = auto()
    ROUTINE = auto()
    URGENT = auto()


class DescribedConfig(Config):
    """A configuration that explains itself to whoever edits it.

    This paragraph is not shown while the explanations are hidden, and the
    line above it is. That is what the first blank line of a docstring is for
    here: the paragraph above it is the summary, which is one line for the
    whole configuration and stays, and everything below it is the detail,
    which goes away with the descriptions of the members. Writing a docstring
    in that shape is worth the trouble, and it is the shape that every style
    guide asks for anyway.
    """

    def __init__(self, from_json_data_text: Optional[str] = None,
                 from_json_filename: Optional[PathOrStr] = None,
                 stderr_file: TextIO = sys.stderr,
                 member_name: Optional[str] = None) -> None:
        """Initialize the configuration with its default values.

        Args:
            from_json_data_text: Optional JSON text to parse directly.
            from_json_filename: Optional path to a JSON file to read.
            stderr_file: Stream used for user-facing diagnostics.
            member_name: Path for reaching this object from the top level
                configuration, so that a diagnostic about a value inside it
                names the whole path. None for the top level itself.
        """
        # These four assignments are the whole schema, as in every other
        # example. What is new here is that three of them are explained in
        # `DESCRIPTIONS` below and the fourth deliberately is not.
        self.project_name: str = 'Example project'
        self.report_file: str = 'report.md'
        self.max_items: int = 20
        self.priority: Priority = Priority.ROUTINE
        super().__init__(from_json_data_text=from_json_data_text,
                         from_json_filename=from_json_filename,
                         stderr_file=stderr_file, member_name=member_name)

    def parse_converters(self) -> Optional[dict[str, ParseConverter]]:
        """Return the converter that turns a member name into a member.

        The enum member is written to the file as its name and has to be
        turned back into a member when it is read, which is the one hook an
        application has to declare for an enum. Example 2 is about that, and
        it is here because a configuration that explains itself is more
        interesting when it has more than one kind of member in it.
        """
        return {'priority': Config.get_converter_dict(Priority)}

    def get_validation_plan(self, stderr_file: TextIO) -> ValidationPlan:
        """Return the validators of the number member.

        The range is the rule that `DESCRIPTIONS` explains in words. The two
        of them are written in two places on purpose: this is what enforces
        the rule, and the description is what tells the user about it, and
        the editor never turns one of them into the other.
        """
        _ = stderr_file
        whole_number = ValueTypeValidator(int, not_allowed_type=bool)
        in_range = IntFloatValidator[int](min_value=FEWEST_ITEMS,
                                          max_value=MOST_ITEMS,
                                          allowed_values=None)
        return [MemberValidationStep(member_names=['max_items'],
                                     validator=whole_number),
                MemberValidationStep(member_names=['max_items'],
                                     validator=in_range)]


DESCRIPTIONS: Descriptions = {
    ('project_name',): 'Name that the reports of this project are headed by.',
    ('max_items',): ('How many items one report may hold. A whole number '
                     f'from {FEWEST_ITEMS} to {MOST_ITEMS}.'),
    ('priority',): ('How urgent this work is. A unique beginning of one of '
                    'the names below will do.')}
"""What this application says about the members it declares.

`report_file` is deliberately absent. A member the mapping says nothing about
is shown without a description, which is the whole of what saying nothing
costs.

The text of `max_items` names the same range that the validation plan
enforces, and it is written here in words because the editor never reads a
range out of a validator.

The text of `priority` deliberately does *not* name the three values, and the
difference between those two members is the point. A range lives inside a
validator, which the editor never reads; the names of an enum are the type of
the member, which the editor does read, from `parse_converters()`. So the
editor lists them below this sentence, and an application that listed them
here as well would be writing them twice and getting them wrong once.
"""


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
    run_example(example_name='e03_described_config', config=DescribedConfig(),
                args=args, descriptions=DESCRIPTIONS)


# The usual guard, so that importing this module from a test runs nothing.
if __name__ == '__main__':
    # Running a file directly puts only that file's own folder on sys.path,
    # so the `example` package this file belongs to would not be importable.
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    main()
