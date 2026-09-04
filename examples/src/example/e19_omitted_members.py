#! /usr/bin/env python3
"""Example 19: the members a class leaves out of the file altogether.

`config_as_json` has two ways of writing a member that holds nothing, and a
configuration class chooses between them with `_omit_none_from_json()`:

- **written as `null`**, which is the default. The file holds a key for the
  member, and its value is `null`.
- **left out of the file**, which the members named in
  `_omit_none_from_json()` are. The file holds no key of that name at all.

Example 18 is about the first of them and about the two states that every
optional member has. This example is about the second, because it is the one
where there is nothing in the file to build a row from: a member written as
`null` is a key with a value, and a member left out is not there.

The editor asks the **configuration object** for those members rather than the
values it writes, so every one of them has a row saying that it holds nothing,
with the same add control as any other. That matters for one reason above all
the others: without it, such a member could never be given a value. A file
that has no key for it, opened in an editor that shows only what the file
holds, is a member the person configuring the application cannot reach.

## What is in this configuration

Every member below except the title is named in `_omit_none_from_json()`, and
the input file in [examples/data/](../../data/) holds nothing but the title,
so a run against that file starts with every one of them holding nothing:

- `note` — an `Optional[str]`. Add gives it the empty text, remove puts it
  back to holding nothing.
- `audit` — an `OPTIONAL_MEMBER` holding one `AuditConfig` or none. This is
  the case that had no row at all before this example was written, and it is
  the one worth pressing in an editor: adding it builds an object of that
  class holding its own declared values, and the rows of that object appear
  below it.
- `extra_hosts` — an `Optional[list[str]]`. It takes two presses to get an
  element: the first gives the member the empty list, which is what its class
  says the member holds, and the second gives that list an element, which is
  what `list[str]` says an element of it is. That is not a special case; it is
  the two states of the member and then the ordinary growing of a list.
- `limits` — an `Optional[dict[str, int]]`, and the one member here that
  cannot be given a value. It says why below its own row, which is the section
  after next.
- `legacy` — assigned with no annotation at all. Nothing says what it would
  hold, so it has no second state to move to and is an ordinary field showing
  `null`, which is a value the user can type over and type back.

Run it and press the controls at the end of each row:

````sh
python3 examples/src/example/e19_omitted_members.py --ui tk
python3 examples/src/example/e19_omitted_members.py --ui textual
python3 examples/src/example/e19_omitted_members.py --ui dump
````

Inside this repository, use the virtual environment that the build creates:
`./venv/bin/python3 examples/src/example/e19_omitted_members.py --ui tk`.

## A nested object given to a member that had none

`audit` is the reason this example exists. Making a configuration object is
not something a field can do — no text typed into one becomes an object — so
it is *adding*, exactly as an element of a list is. The class the declaration
names is what one is made of, and the object holds the values that class
declares:

````sh
cd examples/src/example
python3 e19_omitted_members.py --ui dump --add audit
python3 e19_omitted_members.py --ui dump --add audit --set audit.retries=4
python3 e19_omitted_members.py --ui dump --add audit --remove audit
````

The last of those ends where it started, and it is worth doing in an editor
rather than reading: the rows of the object appear and disappear with it.

## The file is where the difference really is

Two saves say the whole of what `_omit_none_from_json()` means. The first
writes a file with no `audit` key; the second writes one holding the object:

````sh
cd examples/src/example
python3 e19_omitted_members.py --ui dump --save -o /tmp/without.json
python3 e19_omitted_members.py --ui dump --add audit \
    --save -o /tmp/with.json
````

Reading either of them back gives the state it was saved in, which is what
makes the two states real rather than a way of showing one:

````sh
cd examples/src/example
python3 e19_omitted_members.py --ui dump -i ../../data/e19_report.json
python3 e19_omitted_members.py --ui tk -i ../../data/e19_report.json
````

## Two presses for a list, and none at all for a dict

`extra_hosts` and `limits` are declared alike — a member that may hold nothing,
holding a container of ordinary values — and one of them can be given a value
while the other cannot. The difference is not the editor's rule; it is what
`config_as_json` does with the file:

````sh
cd examples/src/example
python3 e19_omitted_members.py --ui dump --add extra_hosts
python3 e19_omitted_members.py --ui dump --add extra_hosts --add extra_hosts \
    --set extra_hosts.0=build-01
python3 e19_omitted_members.py --ui dump --add limits
````

A **dict** written for a member that holds none is refused by the
configuration class itself: `Config.check_dict_parse` matches a dict in the
file against the dict the member holds, and a member holding nothing holds no
dict to match it with. So even the empty dict would be refused, and the editor
says so below the row instead of offering a control that produces a refusal.
It is the same check that stops an ordinary dict member gaining a key, which
example 11 is about.

A **list** has no such check, so the empty list reaches the file and the member
can then be grown in the ordinary way. The last command above adds nothing and
says so, because the control it presses does not exist.

## What the application still decides

Nothing here is a way round the rules. `AuditConfig` refuses more than five
retries, so an object the editor made is validated exactly as one the file
held:

````sh
cd examples/src/example
python3 e19_omitted_members.py --ui dump --add audit --set audit.retries=9
````

The editor accepts the number as a number and the application refuses it as a
count of retries, which is the division of labour every example here shows:
the editor knows the shape of the configuration and the application knows what
the values mean.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from pathlib import Path
from typing import Optional, TextIO
import sys
from config_as_json import Config, ConfigNesting, ConfigNestingKind, \
    IntFloatValidator, MemberValidationStep, PathOrStr, ValidationPlan
from edit_cfg_json import Descriptions

MOST_RETRIES = 5
"""How many times the audit trail may be written again after a failure."""

NestedConfigs = dict[str, ConfigNesting | list[ConfigNesting]]
"""What `nested_configs()` answers with, which `config_as_json` names."""


class AuditConfig(Config):
    """The audit trail of one run, which is written only when it is wanted."""

    def __init__(self, from_json_data_text: Optional[str] = None,
                 from_json_filename: Optional[PathOrStr] = None,
                 stderr_file: TextIO = sys.stderr,
                 member_name: Optional[str] = None) -> None:
        """Initialize the audit trail with its default values.

        Args:
            from_json_data_text: Optional JSON text to parse directly.
            from_json_filename: Optional path to a JSON file to read.
            stderr_file: Stream used for user-facing diagnostics.
            member_name: Path for reaching this object from the top level
                configuration, so that a diagnostic about a value inside it
                names the whole path. None for the top level itself.
        """
        self.destination: str = 'audit.log'
        self.retries: int = 2
        super().__init__(from_json_data_text=from_json_data_text,
                         from_json_filename=from_json_filename,
                         stderr_file=stderr_file, member_name=member_name)

    def get_validation_plan(self, stderr_file: TextIO) -> ValidationPlan:
        """Return the rules that one audit trail is checked against.

        They apply to an object the editor made in exactly the way they apply
        to one a file held: a nested configuration object validates itself,
        whoever built it.

        Args:
            stderr_file: Stream used for user-facing diagnostics.

        Returns:
            The one rule this class has.
        """
        _ = stderr_file
        few_enough = IntFloatValidator(min_value=0, max_value=MOST_RETRIES,
                                       allowed_values=None)
        return [MemberValidationStep(member_names=['retries'],
                                     validator=few_enough)]


class ReportConfig(Config):
    """What one report is generated with, and what may be left unsaid.

    Every member of this class but the title is named in
    `_omit_none_from_json()`, so a file of this configuration holds a key for
    each of them only while it holds something to say about it. The editor
    asks this object for those members rather than the file, which is what
    gives every one of them a row to be given a value at.
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
        # The one member that is always in the file, so that there is
        # something to compare the rest with.
        self.title: str = 'Quarterly report'
        # A text that may be left unsaid. Add gives it the empty text.
        self.note: Optional[str] = None
        # One configuration object or none, and the file holds no key for it
        # while there is none. This is the case that had no row at all before
        # the editor asked the object instead of the file.
        self.audit: Optional[AuditConfig] = None
        # A list that may be absent rather than empty. Two presses reach an
        # element: the member takes the empty list, and the list takes text.
        self.extra_hosts: Optional[list[str]] = None
        # Declared exactly like the list above, and the one member here that
        # cannot be given a value: the class refuses a dict written for a
        # member that holds none.
        self.limits: Optional[dict[str, int]] = None
        # The one member with no annotation, so nothing says what it would
        # hold. It has one state rather than two, and shows `null` in a field.
        self.legacy = None
        super().__init__(from_json_data_text=from_json_data_text,
                         from_json_filename=from_json_filename,
                         stderr_file=stderr_file, member_name=member_name)

    def _omit_none_from_json(self) -> list[str]:
        """Return the members left out of the file while they hold nothing.

        A member named here is not written as `null`; the file has no key for
        it. The editor reads this because it decides what a save writes and
        what the line under the member says, and it asks this object for such
        a member so that the member has a row whether the file held it or not.
        """
        return ['note', 'audit', 'extra_hosts', 'limits', 'legacy']

    def nested_configs(self) -> NestedConfigs:
        """Return the one nested configuration object this class declares.

        `OPTIONAL_MEMBER` is what says that the member holds one object of
        that class or none at all, and it is what the editor makes a new one
        from when the member is given an object.
        """
        optional = ConfigNestingKind.OPTIONAL_MEMBER
        declared = ConfigNesting(kind=optional, config_type=AuditConfig)
        return {'audit': declared}

    def get_validation_plan(self, stderr_file: TextIO) -> ValidationPlan:
        """Return the rules that this configuration is checked against.

        There are none of its own. Every rule that matters here belongs to
        `AuditConfig`, which validates itself whoever built it, and that is
        the point: an object the editor made is no more trusted than one a
        file held.

        Args:
            stderr_file: Stream used for user-facing diagnostics.

        Returns:
            No rules at all.
        """
        _ = stderr_file
        return []


DESCRIPTIONS: Descriptions = {
    ('title',): 'What the report is called.',
    ('note',): 'A remark for whoever runs the report, if there is one.',
    ('audit',): ('Where the run records what it did, when a record is '
                 'wanted at all.'),
    ('audit', 'destination'): 'File that the record is written to.',
    ('audit', 'retries'): 'How many times writing it is tried again.',
    ('extra_hosts',): 'Machines to run on beside the ones configured.',
    ('limits',): 'A budget per resource, where this run has budgets.',
    ('legacy',): ('Whatever an older version of this tool put here. It is '
                  'the one member of this class with no annotation.')}
"""What this application says about the members it declares.

The type of each member says the rest, under whatever is written here, so
nothing here repeats what the annotation already says.
"""


def main(args: Optional[list[str]] = None) -> None:
    """Run this example from the command line.

    Args:
        args: Optional replacement for `sys.argv[1:]`, mainly for tests.
    """
    # pylint: disable-next=import-outside-toplevel
    from example.cmd_line import run_example
    run_example(example_name='e19_omitted_members', config=ReportConfig(),
                descriptions=DESCRIPTIONS, args=args)


if __name__ == '__main__':
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    main()
