#! /usr/bin/env python3
"""Example 10: lists and dicts whose elements are configuration objects.

Example 8 showed a member holding a list or a dict of plain values. Example 9
showed a member holding one nested `Config` object. This one puts the two
together, and the result is not a curiosity: **a list of nested objects, and a
dict of them by name, is what a configuration of any real size looks like.**
One nested object per member is the least interesting shape there is; a
configuration worth editing has several of the same kind of thing.

`config_as_json` says which shape a member has with `ConfigNestingKind`:

| Kind | What it declares |
| --- | --- |
| `MEMBER` | the member itself is one object — example 9 |
| `OPTIONAL_MEMBER` | the member is one object or is `None` — example 9 |
| `LIST_ELEMENT` | *every element* of that list is one object |
| `DICT_VALUE` | *every value* of that dict is one object |

This example declares one of each of the last two, with the same
`ReportOutputConfig` class in both, because writing that class once and using
it as often as it is needed is the whole point of nesting.

## The member is a container and each object in it is a node

Nothing new had to be invented for this. A member holding a list of objects is
an ordinary container of the tree: it folds, it says how many elements it
holds, and its rows are its elements. Each element is then a node exactly like
the nested object of example 9 — its class where its value would be, its own
docstring below it, its own members as the rows under that, and its own badge
saying what it is on its own:

````text
reports: 3 elements
    0: ReportOutputConfig [valid on its own]
        title = Registered participants
        file_name = participants.csv
        max_rows = 1000
    1: ReportOutputConfig [valid on its own]
        ...
````

A dict of them is the same thing with keys instead of indices, in the sorted
order the file has, because a dictionary key has no declaration order to read.

## The list opens folded, and that is the point

Three objects of three members each is twelve rows, which is more than a
window can spare for one member, so `reports` opens **folded** and says so.
`reports_by_id` holds two objects and opens open. That is not a rule about
lists and dicts: it is the rule of example 8, counting everything inside a
container, and a container of configuration objects reaches the limit at three
of them rather than at a dozen numbers. It is worth meeting here, because it is
where a real configuration meets it, and it is the first thing an editor shows
of a configuration this size: one member open and one folded, with a control on
each of them.

````sh
cd examples/src/example
python3 e10_config_containers.py --ui dump
python3 e10_config_containers.py --ui dump --fold reports
python3 e10_config_containers.py --ui dump --toggle-fold --toggle-fold
````

## One description for every element

This is what the `'['` step is for, and it is the reason a repeated nested
object costs the application nothing extra to explain. `'['` is
`config_as_json`'s own notation for *every element of this list or every value
of this dict at this point*, and a description written with it reaches into
every one of them:

````python
('reports', '['): 'One report of the list.'
('reports', '[', 'file_name'): 'The file this report is written to. ...'
('reports_by_id', '[', 'max_rows'): 'Most rows this named report may have.'
````

Without it the application would have to write one description per index and
per key, which would be untrue as soon as a list grew or a key was renamed. A
description that names a step exactly still wins over one that says `'['` at
that step, so a single value inside a container can be singled out:
`('reports_by_id', 'audit', 'max_rows')` below describes that one report and
leaves the `'['` line above it to every other.

A description path is the one thing here that **crosses** the boundary of a
nested object. Everything else stops at it, and section 4.3 of
[`doc/design.md`](../../../doc/design.md) says why: an application explaining
its own settings should not have to know where its nesting boundaries fall.

## A value inside one of them is addressed by the path to it

Exactly as a value inside a list of numbers is, and exactly as a member of a
single nested object is. There is one notation and it reaches everywhere:

````sh
cd examples/src/example
python3 e10_config_containers.py --ui dump --fold reports \
    --set reports.0.file_name=all-participants.csv
python3 e10_config_containers.py --ui dump \
    --set reports_by_id.audit.max_rows=250
````

## Every object is checked by its own class, once per object

`ReportOutputConfig` refuses a row count outside its range. That rule belongs
to that class, so it runs for every element of the list and for every value of
the dict, and the editor names the one object it was about:

````sh
cd examples/src/example
python3 e10_config_containers.py --ui dump \
    --set reports_by_id.audit.max_rows=0
````

That object says *refused on its own*, every other object says *valid on its
own*, and the verdict line names `reports_by_id.audit.max_rows`.

## A rule about all of them belongs to the class holding them

No report can check that its file name differs from the other reports' names,
because no report knows the others exist. So that rule is a
`WholeConfigValidator` on the class that holds both containers, and it reaches
over the list and the dict together:

````sh
cd examples/src/example
python3 e10_config_containers.py --ui dump \
    --set reports_by_id.summary.file_name=audit.csv
python3 e10_config_containers.py --ui dump --fold reports \
    --set reports_by_id.audit.file_name=participants.csv
````

The second of those is the interesting one: it makes a report of the dict
collide with a report of the list, and it opens the list so that both of them
can be seen at once. Both objects are perfectly good
`ReportOutputConfig` objects, so both say *valid on its own* while the
configuration cannot be written at all. The badge on a row answers one
question and the validation line answers the other, which is why the badge is
worded *on its own* and never simply *valid*.

## What is deliberately not here

**Adding an element and removing one.** This example edits the objects that
are there; a list that grows and shrinks is
[e11_add_remove.py](e11_add_remove.py).

**`DICT_VALUE_BY_KEY`,** the third repeated shape, which declares that one
named key of a dict is an object. It is edited exactly like the two here, and
what is different about it is that the named key may be given and taken away
while the keys beside it hold ordinary values, so the example that shows what
can be added is where it belongs.

Run this example in one of the two editors. This is the first example whose
configuration is the size a real one is, so it is the first where the fold
controls and the scrolling are doing real work:

````sh
python3 examples/src/example/e10_config_containers.py --ui tk
python3 examples/src/example/e10_config_containers.py --ui textual
````

Inside this repository, use the virtual environment that the build creates:
`./venv/bin/python3 examples/src/example/e10_config_containers.py --ui tk`.

Open `reports`, break one report's `max_rows`, and fold the member again: the
badge on the container row says *refused inside* while everything below it is
hidden, which is why a container of objects has a badge of its own.

`--ui dump` is the very limited non-interactive user interface, and it is what
the command lines above use. There is a file to read in
[examples/data/](../../data/), and it holds two reports in the list and three
in the dict, which folds the other one of the two containers:

````sh
cd examples/src/example
python3 e10_config_containers.py --ui dump -i ../../data/e10_reports.json
python3 e10_config_containers.py --ui tk -i ../../data/e10_reports.json
````
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from pathlib import Path
from typing import Optional, TextIO
import sys
from config_as_json import Config, ConfigNesting, ConfigNestingKind, \
    InvalidConfiguration, IntFloatValidator, MemberValidationStep, \
    NestedConfigs, PathOrStr, ValidationPlan, WholeConfigValidationStep, \
    WholeConfigValidator
from edit_cfg_json import Descriptions

FEWEST_ROWS = 1
"""Fewest rows that one report of this example may be asked for."""

MOST_ROWS = 10000
"""Most rows that one report of this example may be asked for."""

REPEAT_REFUSAL = 'Two reports would both be written to {name}.'
"""What the rule below says when two reports name one file.

It is a rule about the reports taken together and therefore about none of
them, which is what makes it the rule this example needs: every report can be
a perfectly good configuration on its own while the export holding them is
refused.
"""


class ReportOutputConfig(Config):
    """One generated report: what it is called, where it goes, how big.

    Nothing about this class says that it will be used more than once. It is
    an ordinary configuration class, and what makes it a repeated one is the
    declaration in `CourseReportsConfig` below.
    """

    # The three keyword arguments below are the constructor that
    # `config_as_json` builds a nested object with, whether that object is a
    # member, an element of a list or a value of a dict. It is the same
    # contract in all three cases, which is why one class covers all of them.
    def __init__(self, from_json_data_text: Optional[str] = None,
                 from_json_filename: Optional[PathOrStr] = None,
                 stderr_file: TextIO = sys.stderr) -> None:
        """Initialize one report with its default values.

        Args:
            from_json_data_text: Optional JSON text to parse directly.
            from_json_filename: Optional path to a JSON file to read.
            stderr_file: Stream used for user-facing diagnostics.
        """
        # Three members, shown in this order because this is the order they
        # are assigned in. Three is also what keeps the dict of two reports
        # below open when the editor starts and folds the list of three.
        self.title: str = 'Registered participants'
        self.file_name: str = 'participants.csv'
        self.max_rows: int = 1000
        super().__init__(from_json_data_text=from_json_data_text,
                         from_json_filename=from_json_filename,
                         stderr_file=stderr_file)

    def get_validation_plan(self, stderr_file: TextIO) -> ValidationPlan:
        """Return the one rule that every report of this example obeys.

        It belongs to this class, so it runs once for every object of it: for
        each element of the list and for each value of the dict, without the
        class holding them having to say anything about it.
        """
        _ = stderr_file
        in_range = IntFloatValidator[int](min_value=FEWEST_ROWS,
                                          max_value=MOST_ROWS,
                                          allowed_values=None)
        return [MemberValidationStep(member_names=['max_rows'],
                                     validator=in_range)]


def new_report(title: str, file_name: str, max_rows: int,
               stderr_file: TextIO) -> ReportOutputConfig:
    """Return one report output holding the values it is given.

    The values are assigned after the object is built, because the
    constructor of a configuration class takes JSON and not values. That is
    the same thing `config_as_json` does when it reads a file: build the
    object, then fill it in.

    Args:
        title: Heading that this report is written under.
        file_name: File that this report is written to.
        max_rows: Most rows that this report may hold.
        stderr_file: Stream used for user-facing diagnostics.

    Returns:
        One report output configuration holding those values.
    """
    report = ReportOutputConfig(stderr_file=stderr_file)
    report.title = title
    report.file_name = file_name
    report.max_rows = max_rows
    return report


# A validator has one method, which is fewer than pylint likes to see in a
# class. That is what a validator is, so the check is turned off for this one.
# pylint: disable-next=too-few-public-methods
class ReportsDiffer(WholeConfigValidator):
    """Refuse an export in which two reports write to one file.

    This is the rule that no report could check for itself, because a report
    knows its own file name and does not know that any other report exists. So
    it belongs to the class that holds them all, and it is a
    `WholeConfigValidator` because it is about no single member: it reaches
    over the list and the dict together.
    """

    def validate(self, config: Config,
                 stderr_file: TextIO = sys.stderr) -> None:
        """Refuse two reports that would be written to one file.

        Args:
            config: The whole export, which is what makes the file names of
                every report comparable at all.
            stderr_file: Stream that the refusal is written to before it is
                raised, which is the contract every validator here follows.

        Raises:
            InvalidConfiguration: Two reports name the same file.
        """
        assert isinstance(config, CourseReportsConfig)
        names = [report.file_name for report in config.every_report()]
        repeated = sorted(name for name in set(names) if names.count(name) > 1)
        if not repeated:
            return
        message = REPEAT_REFUSAL.format(name=repeated[0])
        print(message, file=stderr_file)
        raise InvalidConfiguration(message)


def _default_reports(stderr_file: TextIO) -> list[ReportOutputConfig]:
    """Return the reports that this example writes for every course.

    Args:
        stderr_file: Stream used for user-facing diagnostics.

    Returns:
        Three report outputs, which is one more than a window can spare.
    """
    return [new_report('Registered participants', 'participants.csv', 1000,
                       stderr_file),
            new_report('Waiting list', 'waiting-list.csv', 200, stderr_file),
            new_report('Cancellations', 'cancellations.csv', 200, stderr_file)]


def _reports_by_id(stderr_file: TextIO) -> dict[str, ReportOutputConfig]:
    """Return the reports that this example writes when they are asked for.

    Args:
        stderr_file: Stream used for user-facing diagnostics.

    Returns:
        Two report outputs, by the name each of them is asked for under.
    """
    return {'audit': new_report('Administrator audit log', 'audit.csv', 5000,
                                stderr_file),
            'summary': new_report('Course summary', 'summary.csv', 50,
                                  stderr_file)}


class CourseReportsConfig(Config):
    """Every report that one course export writes.

    The two members below hold the same kind of thing in the two ways a
    configuration usually holds several of something: a list, where the order
    is what matters, and a dict, where a stable name is what matters. Both of
    them hold real configuration objects, and the editor shows each of those
    as the object it is.
    """

    def __init__(self, from_json_data_text: Optional[str] = None,
                 from_json_filename: Optional[PathOrStr] = None,
                 stderr_file: TextIO = sys.stderr) -> None:
        """Initialize the course reports with their default values.

        Args:
            from_json_data_text: Optional JSON text to parse directly.
            from_json_filename: Optional path to a JSON file to read.
            stderr_file: Stream used for user-facing diagnostics.
        """
        # One plain member first, so that an ordinary row can be seen beside
        # the two containers of objects.
        self.course_name: str = 'python-intro'
        # A list of objects. The default may be empty or hold ready-made
        # objects; this one holds three, because a real export writes more
        # than one report and because three of them is what fills a window.
        self.reports: list[ReportOutputConfig] = _default_reports(stderr_file)
        # A dict of objects, keyed by the name each is asked for under.
        self.reports_by_id: dict[str, ReportOutputConfig] = \
            _reports_by_id(stderr_file)
        super().__init__(from_json_data_text=from_json_data_text,
                         from_json_filename=from_json_filename,
                         stderr_file=stderr_file)

    def every_report(self) -> list[ReportOutputConfig]:
        """Return every report of this export, however it is held.

        A rule about the reports taken together has to see all of them, and
        which container one is in says nothing about that.

        Returns:
            The reports of the list followed by the reports of the dict.
        """
        return [*self.reports, *self.reports_by_id.values()]

    def nested_configs(self) -> NestedConfigs:
        """Return which members hold configuration objects, and how.

        `LIST_ELEMENT` says that every *element* of `reports` is one, and
        `DICT_VALUE` says that every *value* of `reports_by_id` is one. In
        both cases the member itself is an ordinary list or dict; only what
        is inside it is a configuration object.

        This one declaration is the whole of what the editor needs to show
        every one of those objects as the object it is.
        """
        return {'reports': ConfigNesting(kind=ConfigNestingKind.LIST_ELEMENT,
                                         config_type=ReportOutputConfig),
                'reports_by_id': ConfigNesting(
                    kind=ConfigNestingKind.DICT_VALUE,
                    config_type=ReportOutputConfig)}

    def get_validation_plan(self, stderr_file: TextIO) -> ValidationPlan:
        """Return the one rule that is about all the reports at once.

        Every rule about what is *inside* one report belongs to
        `ReportOutputConfig`, which is the point of nesting: the class that
        owns the values is the class that checks them, and it checks every
        object of itself without being asked once per element.
        """
        _ = stderr_file
        return [WholeConfigValidationStep(validator=ReportsDiffer())]


DESCRIPTIONS: Descriptions = {
    ('course_name',): 'Which course these reports are about.',
    ('reports',): 'The reports that every export of this course writes.',
    ('reports', '['): 'One report of the list.',
    ('reports', '[', 'file_name'): ('The file this report is written to. No '
                                    'two reports may name one file.'),
    ('reports_by_id',): ('The reports that are written when they are asked '
                         'for.'),
    ('reports_by_id', '[', 'max_rows'): ('Most rows this named report may '
                                         'hold.'),
    ('reports_by_id', 'audit', 'max_rows'): ('Most entries kept in the audit '
                                             'log, which is the one report '
                                             'that is normally long.')}
"""What this application says about the members it declares.

Four of these use the `'['` step, and they are what this example is about.
`'['` means every element of that list or every value of that dict, so one
line describes a member of *every* report and the application never repeats
itself per index or per key. Writing one description per index would also be
untrue the moment a report was added or a key was renamed.

`('reports', '[')` describes each object itself rather than a member of it,
which is what appears below the row that says its class.

`('reports_by_id', 'audit', 'max_rows')` is the exception that the rule allows
for: it names every step, so it is the more specific selector and it wins over
the `'['` line above it for that one report. Every other report of that dict
keeps the general description.

`title` is described by nobody, so it is shown with what its type says and
nothing else, which is what any member an application says nothing about is
shown with.
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
    run_example(example_name='e10_config_containers', args=args,
                config=CourseReportsConfig(), descriptions=DESCRIPTIONS)


# The usual guard, so that importing this module from a test runs nothing.
if __name__ == '__main__':
    # Running a file directly puts only that file's own folder on sys.path,
    # so the `example` package this file belongs to would not be importable.
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    main()
