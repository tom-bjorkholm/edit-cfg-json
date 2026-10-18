#! /usr/bin/env python3
"""Example 20: a member that may hold one of two kinds of list.

A real application declared this, and it is the complaint this example is
written to answer:

````python
self.jira_column_map: dict[str, list[str] | list[list[str]]]
````

It says which fields of an issue go into which column of a spreadsheet. A
column is filled from **one** field, written as the path of keys that leads to
it — `['assignee', 'displayName']` — or from **several** fields joined
together, written as a list of such paths. Both are lists, and they are lists
of different things: `list[str]` and `list[list[str]]`.

Example 18 showed a member chosen between `int` and `str`, and between `str`
and `None`, in the pull-down that says the type of every row. This example is
the same pull-down choosing between two **containers**, and that is a bigger
change than choosing between two values: a list of text and a list of lists of
text have different rows below them, so choosing one makes the rows below the
entry again, exactly as adding an element does.

Run it, and choose in the pull-down beside the name of each entry of
`jira_column_map`:

````sh
python3 examples/src/example/e20_union_types.py --ui tk
python3 examples/src/example/e20_union_types.py --ui textual
python3 examples/src/example/e20_union_types.py --ui dump
````

Inside this repository, use the virtual environment that the build creates:
`./venv/bin/python3 examples/src/example/e20_union_types.py --ui tk`.

## Each entry holds the type its value is

`Created` holds one path and `People` holds two, so the first says
`list[str]` and the second `list[list[str]]`, and the line below each of them
says the whole of what it is declared as. Until the user chooses, the type an
entry holds is the first of its types that its value fits.

## A new entry, and choosing what it is

A new entry of a dict is copied from what the dict already holds, as example
11 explains, so a new column is a copy of `Created`: a `list[str]`. Choosing
`list[list[str]]` for it gives it the **empty** list — nothing of a list of
text is a list of lists of text — and the control of that empty list then adds
an empty `list[str]`, because that is what an element of a `list[list[str]]`
is:

````sh
cd examples/src/example
python3 e20_union_types.py --ui dump --add jira_column_map=Status
python3 e20_union_types.py --ui dump --add jira_column_map=Status \
    --set-type 'jira_column_map.Status=list[list[str]]' \
    --add jira_column_map.Status
python3 e20_union_types.py --ui dump --add jira_column_map=Status \
    --set-type 'jira_column_map.Status=list[list[str]]' \
    --add jira_column_map.Status --add jira_column_map.Status.0 \
    --set jira_column_map.Status.0.0=status
````

The quotation marks are for the shell, which would otherwise read the square
brackets as a pattern of file names.

**The choice outlives the value.** An empty list is a `list[str]` and a
`list[list[str]]` alike, so nothing in the value says which of the two the new
entry is; the editor keeps the type the user chose, and that is what the next
element is made of. It keeps it across a validation pass as well, and it gives
way only where a pass leaves a value that the type chosen does not fit.

## Reading the types from a file

There is a file in [examples/data/](../../data/) whose entries say their types
by their values alone. `Labels` holds one path written as a list of paths, so
it holds `list[list[str]]` although one path would have done. `Watchers` holds
the empty list, which is a value of both types, so it holds the first of them
that the declaration writes, `list[str]`, until the user chooses the other:

````sh
cd examples/src/example
python3 e20_union_types.py --ui dump -i ../../data/e20_export.json
python3 e20_union_types.py --ui tk -i ../../data/e20_export.json
````

## Switching gives the empty value

Choosing the other type of an entry that holds something does not try to keep
any of it. A path of keys is not a list of paths, and guessing which of the
two the user meant would be a guess:

````sh
cd examples/src/example
python3 e20_union_types.py --ui dump \
    --set-type 'jira_column_map.People=list[str]'
````

`People` is then an empty `list[str]`, its rows are gone, and anything that was
folded or found inside it went with them.

## What the application still decides

The editor offers the types the class declared and nothing else, and the
values typed into them are still the application's to accept. `ExportConfig`
refuses a separator of no characters, because the fields of a column would run
into one another:

````sh
cd examples/src/example
python3 e20_union_types.py --ui dump --set separator=
````

## Why the keys of this dict are free

`jira_column_map` is named in `_unchecked_dicts`, which is how a class tells
`config_as_json` that the keys of a dict member are the application's own to
decide. Without that, the class would match the keys of the dict in a file
against the keys of its own, and a new column would be refused, as example 11
shows. It matters for the types as well: wherever that check reaches, the class
also refuses a dict in the file where it holds none and anything else where it
holds one, so the editor does not offer a type the class would refuse there.
Below a member named in `_unchecked_dicts` the check reaches nothing, so every
declared type is offered. Example 19 shows the other side of it, with a member
that may hold a dict or nothing and is offered `None` alone.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from pathlib import Path
from typing import Optional, TextIO
import sys
from config_as_json import Config, MemberValidationStep, PathOrStr, \
    StrLenValidator, ValidationPlan
from edit_cfg_json import Descriptions


class ExportConfig(Config):
    """How issues are exported into the columns of a spreadsheet.

    Each column is filled from one field of an issue, or from several fields
    joined with the separator, and each field is written as the path of keys
    that leads to it among the fields of the issue.
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
        # The member of the complaint. Each value is a list either way, and
        # which of the two lists it is, is chosen in the pull-down of its row.
        # `Created` comes first so that a new column, which is a copy of the
        # first entry, is a column filled from one field.
        self.jira_column_map: dict[str, list[str] | list[list[str]]] = {
            'Created': ['created'], 'People': [['assignee'], ['reporter']]}
        # An ordinary text, so that there is something beside the map whose
        # type nothing can change.
        self.separator: str = ', '
        # The keys of the map are the names of columns, which only the person
        # configuring the export knows, so the class does not check them.
        self._unchecked_dicts = ['jira_column_map']
        super().__init__(from_json_data_text=from_json_data_text,
                         from_json_filename=from_json_filename,
                         stderr_file=stderr_file, member_name=member_name)

    def get_validation_plan(self, stderr_file: TextIO) -> ValidationPlan:
        """Return the one rule that this configuration is checked against.

        A separator of no characters would run the fields of a column into
        one another, so it is refused. Nothing is said about the map: every
        value the editor offers there is one the class reads back as it was
        written, which is what this example is about.

        Args:
            stderr_file: Stream used for user-facing diagnostics.

        Returns:
            The rule about the separator.
        """
        _ = stderr_file
        not_empty = StrLenValidator(min_length=1, max_length=None)
        return [MemberValidationStep(member_names=['separator'],
                                     validator=not_empty)]


DESCRIPTIONS: Descriptions = {
    ('jira_column_map',): ('Which fields of an issue fill which column of the '
                           'spreadsheet, by the name of the column.'),
    ('jira_column_map', '['): ('The path of keys to one field, or a list of '
                               'such paths whose fields are joined.'),
    ('separator',): 'What joins the fields of a column filled from several.'}
"""What this application says about the members it declares.

The type of each row says the rest, under whatever is written here, so
nothing here repeats what the annotation already says.
"""


def main(args: Optional[list[str]] = None) -> None:
    """Run this example from the command line.

    Args:
        args: Optional replacement for `sys.argv[1:]`, mainly for tests.
    """
    # pylint: disable-next=import-outside-toplevel
    from example.cmd_line import run_example
    run_example(example_name='e20_union_types', config=ExportConfig(),
                descriptions=DESCRIPTIONS, args=args)


if __name__ == '__main__':
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    main()
