#! /usr/bin/env python3
"""Example 8: a configuration whose members are lists and dicts.

Every example before this one has a configuration of plain values: a member is
one name and one value, and one row of the editor shows it. That is not what
real configurations look like. A member is very often a list of things or a
dict of settings, and one row and one field could not show either of them.

This example is where the shape stops being flat. Ordinary JSON structure
inside a configuration is a tree of rows, and every value at the bottom of it
is edited in a field of its own.

## What a tree of rows looks like

A member that holds a list or a dict is a row of its own, and what it holds is
on the rows below it, indented once for each container they are inside:

````text
retry_delays: 3 elements
    0 = 1
    1 = 5
    2 = 15
ports: 2 entries
    http = 80
    https = 443
````

The container row uses a colon and says how many values it holds, and a value
row uses an equals sign and shows the value. That is the difference between
them: the container has no value of its own, because its value is the rows
below it.

In an editor every one of those value rows is a field, so `1` and `80` are
typed into exactly as a flat member is. A value inside a container is
addressed by the whole path to it, which is what `--set` writes with a dot
between the steps to reach the same field without a display:

````sh
cd examples/src/example
python3 e08_lists_and_dicts.py --ui dump --set retry_delays.0=2
python3 e08_lists_and_dicts.py --ui dump --set ports.https=8443
````

The same path is what a description in the mapping below is written with, and
`('retry_delays', '[')` is the one that describes *every* element of that list
without naming each index. That `'['` step is `config_as_json`'s own notation
for it, and this library keeps its meaning.

## Folding

A configuration of any size does not fit a window, and a list of a hundred
elements fills one on its own. So a container can be folded away to its single
summary line and opened again: the Tk backend puts a `+` or a `-` control at
the start of the row, the Textual backend puts a button there, and both of
them have one key that folds or opens all of them at once — `f2`, or `ctrl+t`.

The editor opens with every container open, unless opening it would add more
rows than a window can spare; a long one starts folded, and its row says so.
`many_labels` below is what shows that.

Which containers are folded belongs to the model and not to either user
interface, exactly as the explain toggle does, so the two backends cannot
disagree about it. Pressing the control on a row is the way to see this, and
it is worth pressing a few: what a fold really buys is a configuration that
fits the window again.

Without a display, `--fold PATH` presses one control and `--toggle-fold`
presses the key:

````sh
cd examples/src/example
python3 e08_lists_and_dicts.py --ui dump --fold ports
python3 e08_lists_and_dicts.py --ui dump --toggle-fold
python3 e08_lists_and_dicts.py --ui dump --fold many_labels
````

The last of those *opens* `many_labels`, because it starts folded: the control
is a toggle and it does whatever the container is not.

## Finding a member

A configuration that does not fit a window is one where folding is only half
the answer: the other half is being able to *look* for the member you want. The
editor has a search field in the part that does not scroll, with four
tick-boxes beside it and a control that goes to the next member found — the
arrow `►` in the window, the word `next` in the terminal — and `ctrl+f` puts
the cursor in that field while `f3` goes to the next member the search
reaches.

It searches as it is typed, and the member it has got to is marked. **What is
found is always reachable**: a match inside a folded container opens that
container, the row is brought into view, and pressing Enter or `f3` puts the
cursor in its field so it can be typed into straight away. `many_labels` is
what shows that, because it starts folded:

````sh
cd examples/src/example
python3 e08_lists_and_dicts.py --ui dump --find label-7
python3 e08_lists_and_dicts.py --ui dump --find port --find-next
````

The four tick-boxes are where the search looks. Two of them say which text is
compared — the path of the member, the value of it, or both, which is what the
editor opens with — and two say how hard the comparison is: whether the case
has to match, and whether the whole of the text has to rather than a part of
it. Their labels are short and each of them says the rest in a tooltip.

Looking in the *path* is why `--find ports` reaches `ports` and both values
inside it: a part of a path is enough, and the path of every value inside a
member begins with the name of that member. It is also the notation the verdict
line names a refused member in, so what you have just read is what you can
type. Looking in the *value* is what finds `html` without knowing where it is.

````sh
cd examples/src/example
python3 e08_lists_and_dicts.py --ui dump --find ports.http --find-whole
python3 e08_lists_and_dicts.py --ui dump --find HTML --find-in value
python3 e08_lists_and_dicts.py --ui dump --find HTML --find-in value \
    --find-case
````

Turning both places off is the one combination that can never reach anything,
and the editor says that rather than saying that no member matched, because
nothing was compared with anything:

````sh
cd examples/src/example
python3 e08_lists_and_dicts.py --ui dump --find ports --find-in neither
````

What is being looked for and where it looks belong to the model and not to
either user interface, exactly as folding does, so the two backends cannot end
up searching for different things.

## What a validator does to a container

`report_formats` has a `ListOrderingValidator` that sorts its elements and
throws the duplicates away. That is worth seeing, because it is the clearest
case of something design section 6.4 has said since the beginning: **a
validation pass is not read only**. Type a duplicate into it and validate, and
the list comes back shorter than it was, with one row fewer than the row you
typed into:

````sh
cd examples/src/example
python3 e08_lists_and_dicts.py --ui dump --set report_formats.0=json
````

The member is marked *changed by validator*, and this is one to try in an
editor: both backends build their rows again when a pass leaves the model with
other rows than it had, because there is no widget any more for a value that
is gone, and the field that was typed into may be one of them.

## What is refused, and where it is shown

A validator of a list or a dict is given the whole member, so what it refuses
is about the whole member and is shown at the container row rather than at one
value inside it. `retry_delays` has a `ListValueValidator` with a range, and
`ports` has a `DictKeyValueTypesValidator`:

````sh
cd examples/src/example
python3 e08_lists_and_dicts.py --ui dump --set retry_delays.1=500
python3 e08_lists_and_dicts.py --ui dump --set ports.http=eighty
````

The verdict line names the whole path of what was refused, so a configuration
that does not fit the window still says where to look.

## What is deliberately not here

Adding an element and removing one. This example edits what is there, and
[e11_add_remove.py](e11_add_remove.py) is where a list grows and shrinks. A
nested `Config` object is not here either: it serializes as a dict and it is
not one, so [e09_nested_config.py](e09_nested_config.py) is where it becomes a
first-class node of its own.

Run this example in one of the two editors, and press the fold controls and
type into the search field, which is the part of this example that a printout
can only report:

````sh
python3 examples/src/example/e08_lists_and_dicts.py --ui tk
python3 examples/src/example/e08_lists_and_dicts.py --ui textual
````

Inside this repository, use the virtual environment that the build creates:
`./venv/bin/python3 examples/src/example/e08_lists_and_dicts.py --ui tk`.

`--ui dump` is the very limited non-interactive user interface, and it prints
the rows that are on the screen, so a folded container is one line there as
well. There is a file to read in [examples/data/](../../data/):

````sh
cd examples/src/example
python3 e08_lists_and_dicts.py --ui dump -i ../../data/e08_complete.json
python3 e08_lists_and_dicts.py --ui tk -i ../../data/e08_complete.json
````
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from pathlib import Path
from typing import Optional, TextIO
import sys
from config_as_json import Config, DictKeyValueTypesValidator, \
    ListOrderingValidator, ListValueValidator, MemberValidationStep, \
    PathOrStr, ValidationPlan
from edit_cfg_json import Descriptions

SHORTEST_DELAY = 1
"""Fewest seconds that this configuration accepts before a retry."""

LONGEST_DELAY = 60
"""Most seconds that this configuration accepts before a retry."""

LABEL_COUNT = 12
"""How many labels the long list of this example holds.

It is more than a window can spare for one member, which is the point of it:
that list is what shows a container the editor opens folded.
"""


class ContainerConfig(Config):
    """A configuration whose members hold lists and dicts of values.

    Every member below is ordinary JSON structure inside the ownership region
    of this one configuration object. There is no nested `Config` object here
    at all, which is what makes this the example about lists and dicts rather
    than about nesting.
    """

    def __init__(self, from_json_data_text: Optional[str] = None,
                 from_json_filename: Optional[PathOrStr] = None,
                 stderr_file: TextIO = sys.stderr) -> None:
        """Initialize the configuration with its default values.

        Args:
            from_json_data_text: Optional JSON text to parse directly.
            from_json_filename: Optional path to a JSON file to read.
            stderr_file: Stream used for user-facing diagnostics.
        """
        # One plain member first, so that a tree of rows can be seen beside a
        # row that is only a row. Everything after it is a container.
        self.project_name: str = 'Example project'
        # A list of whole numbers, each of which has to be in a range.
        self.retry_delays: list[int] = [1, 5, 15]
        # A list of text that a validator sorts and de-duplicates, which is
        # what makes a validation pass change how many rows there are.
        self.report_formats: list[str] = ['html', 'json']
        # A dict of whole numbers by name.
        self.ports: dict[str, int] = {'http': 80, 'https': 443}
        # A list long enough that the editor opens it folded.
        self.many_labels: list[str] = [f'label-{index}'
                                       for index in range(LABEL_COUNT)]
        super().__init__(from_json_data_text=from_json_data_text,
                         from_json_filename=from_json_filename,
                         stderr_file=stderr_file)

    def get_validation_plan(self, stderr_file: TextIO) -> ValidationPlan:
        """Return the validators of the containers of this configuration.

        Each of them is given the whole member, which is why what one of them
        refuses is shown at the row of that member and not at one value inside
        it. That is not a limitation of the editor: it is what a
        `MemberValidator` is asked about.
        """
        _ = stderr_file
        in_range = ListValueValidator[int](SHORTEST_DELAY, LONGEST_DELAY, None)
        sorted_unique = ListOrderingValidator(str, order=True,
                                              keep_only_unique=True)
        whole_numbers = DictKeyValueTypesValidator(key_type=str,
                                                   value_type=int)
        return [MemberValidationStep(member_names=['retry_delays'],
                                     validator=in_range),
                MemberValidationStep(member_names=['report_formats'],
                                     validator=sorted_unique),
                MemberValidationStep(member_names=['ports'],
                                     validator=whole_numbers)]


DESCRIPTIONS: Descriptions = {
    ('retry_delays',): ('How long to wait before each retry, in seconds. '
                        f'Each of them from {SHORTEST_DELAY} to '
                        f'{LONGEST_DELAY}.'),
    ('retry_delays', '['): 'One wait, in seconds.',
    ('report_formats',): ('Which formats a report is written in. They are '
                          'sorted and de-duplicated when they are validated.'),
    ('ports',): 'Which port each protocol is served on.',
    ('ports', 'https'): 'The one port that is worth saying something about.'}
"""What this application says about the members it declares.

Three of these name a member of the configuration, exactly as every example
before this one does. The other two are what lists and dicts add.

`('retry_delays', '[')` describes *every* element of that list, because `'['`
is the step that means every element or every value at that point. Writing one
description per index would be untrue as soon as the list grew.

`('ports', 'https')` describes one value inside a dict, by the whole path to
it. The other value of that dict says nothing beyond what its type says, which
is the same thing an undescribed member says.

`project_name` and `many_labels` are deliberately absent, so that a row with
nothing said about it can be seen beside the rows that have something.
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
    run_example(example_name='e08_lists_and_dicts', config=ContainerConfig(),
                args=args, descriptions=DESCRIPTIONS)


# The usual guard, so that importing this module from a test runs nothing.
if __name__ == '__main__':
    # Running a file directly puts only that file's own folder on sys.path,
    # so the `example` package this file belongs to would not be importable.
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    main()
