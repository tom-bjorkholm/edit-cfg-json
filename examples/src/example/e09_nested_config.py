#! /usr/bin/env python3
"""Example 9: a configuration built out of smaller configuration objects.

Example 8 showed lists and dicts: ordinary JSON structure inside one
configuration object. This one is about the other kind of structure, and it is
the kind a real application reaches for first. A group of settings that belongs
together — where a file goes, in which format, in which encoding — is written
once as a `Config` class of its own, and the configuration then holds one of
those objects per output.

`config_as_json` calls that a nested `Config`, and a class declares its nested
objects in `nested_configs()`. This example declares two of them, and both are
of the same class, which is the whole point of writing that class once.

## A nested object is not the dict it is written as

In the file, a nested object is a JSON object like any other. In the editor it
is not, and that is the difference this example is here to show:

````text
participant_output: TableOutputConfig
    file_name = participants.csv
    output_format = CSV
    encoding = utf-8
````

The row says the **class**, not how many entries the dict has, because the
class is what it is. Below it are its own members, in the order that class
declares them — not the sorted order the file has. And the docstring of that
class is shown below the row, exactly as the docstring of the whole
configuration is shown at the top.

Press the fold control on its row and it says less about itself as well as
showing fewer rows: the summary of its docstring while it is folded, the whole
docstring while it is open. That is worth pressing twice in an editor, because
the text below the row changes with every press and not only when the explain
key is used.

Without a display, `--fold` presses the same control:

````sh
cd examples/src/example
python3 e09_nested_config.py --ui dump
python3 e09_nested_config.py --ui dump --fold participant_output
````

## Every object says what it is on its own

A nested object is a configuration, so it can be asked whether it is a valid
one without asking anything about the configuration around it. The editor asks
that whenever the object is folded or opened, and again on every validation
pass, and the answer is on the row:

````text
participant_output: TableOutputConfig [valid on its own]
````

**On its own is the whole of what that claims**, and it is worth being careful
about, because it is the one badge that could be misread. A configuration can
be refused for a reason that is about nothing inside either object — the rule
in `CourseExportConfig` below is exactly that — and both objects then say
*valid on its own* while the file cannot be written at all:

````sh
cd examples/src/example
python3 e09_nested_config.py --ui dump -i ../../data/e09_with_audit.json \
    --set audit_output.file_name=advanced-participants.csv
````

Whether these values could be saved is the line below the members, and that
line is the only thing that answers it.

That has to be typed rather than read from a file, because a file whose values
the application refuses is one the editor will not open at all: `parse_json`
ends in `validate()`, so there is no object to build an editor on. Correcting
such a file is a job for a text editor, and the message says so.

## Everything inside it belongs to its own class

This is the part that is easy to get wrong and impossible to see from the
outside. A nested object parses its own JSON, so:

- its **parse converters** are its own. `TableOutputConfig` below converts
  nothing; if it did, that converter would apply to its members and to no
  member of `CourseExportConfig`.
- which of its members it may **leave out of the file** is its own. That is
  `_omit_none_from_json()`, and the class holding it has no say in it.

The editor asks the object that owns a value, and never the one above it.

## A member is addressed by the path to it

A value inside a nested object is addressed exactly as a value inside a list
or a dict is: by the whole path, with a dot between the steps.

````sh
cd examples/src/example
python3 e09_nested_config.py --ui dump \
    --set participant_output.encoding=latin-1
python3 e09_nested_config.py --ui dump \
    --set participant_output.output_format=txt
````

The second of those is worth running. `output_format` has a validator that
normalizes the case, so validating rewrites `txt` to `TXT`, and both the member
and the object holding it say *changed by validator*.

The description mapping uses those same paths, and it is the one thing here
that deliberately does **not** stop at the boundary of a nested object: an
application explaining its own settings should not have to know where its
nesting boundaries fall.

## Where a refusal inside a nested object is shown

Type something that class will not accept and the refusal appears at the
member it is about, exactly as it does for a member at the top level:

````sh
cd examples/src/example
python3 e09_nested_config.py --ui dump \
    --set participant_output.output_format=xml
python3 e09_nested_config.py --ui dump \
    --set participant_output.encoding=nonsense
````

Asking each object on its own is what makes that possible, and it is the same
question the badge above answers. Reading the whole configuration cannot: a
nested object validates itself while the configuration around it is being
parsed, so by the time anything could ask which member was refused there is no
object left to ask.

A rule that is about **no single member** of an object is shown below that
object rather than at one of its members, because that is what it is about.
The rule of `CourseExportConfig` below is about two objects and therefore
about neither, so it appears below all of them, in the validation line.

A value whose *text* means nothing at all is a third question again, and is
answered at the member without any configuration being built, inside a nested
object as anywhere else.

## An optional nested object

`audit_output` may be there or not. It is `None` here, and this class does not
list it in `_omit_none_from_json()`, so `null` is what reaches the file and the
row says which class is missing:

````text
audit_output: no TableOutputConfig
````

It cannot be edited, because no text typed into a field becomes a
configuration object. Making one is *adding*, which
[e11_add_remove.py](e11_add_remove.py) is about. A class that listed the
member in `_omit_none_from_json()` would write nothing for it at all, and it
would then have no row — which is what any member a class omits already does.

The file in [examples/data/](../../data/) has an audit output, so reading it
shows the same member as a real object with rows of its own:

````sh
cd examples/src/example
python3 e09_nested_config.py --ui dump -i ../../data/e09_with_audit.json
````

## What is deliberately not here

A *list* or a *dict* of nested objects, which is the ordinary shape of a large
configuration. The editor handles them by the very same mechanism as the two
members here — each object inside the container is one node — and
[e10_config_containers.py](e10_config_containers.py) is the example that shows
them.

Run this example in one of the two editors, where the badge on each object row
and the folding of one object are what there is to look at:

````sh
python3 examples/src/example/e09_nested_config.py --ui tk
python3 examples/src/example/e09_nested_config.py --ui textual
````

Inside this repository, use the virtual environment that the build creates:
`./venv/bin/python3 examples/src/example/e09_nested_config.py --ui tk`.

`--ui dump` is the very limited non-interactive user interface, and it is what
every command line above uses: it prints the same rows, the same badges and
the same sentences, which is what lets this example be checked from a script.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from pathlib import Path
from typing import Optional, TextIO
import sys
from config_as_json import CharEncodingValidator, Config, ConfigNesting, \
    ConfigNestingKind, InvalidConfiguration, MemberValidationStep, \
    NestedConfigs, PathOrStr, StrValidator, ValidationPlan, \
    WholeConfigValidationStep, WholeConfigValidator
from edit_cfg_json import Descriptions

OUTPUT_FORMATS = ['CSV', 'TXT']
"""The formats that one table-like output can be written in."""

SAME_FILE_REFUSAL = 'The two outputs would both be written to {name}.'
"""What the rule below says when the two outputs name one file.

It is a rule about two objects and therefore about neither of them, which is
what makes it the rule this example needs: both objects can be perfectly good
configurations on their own while the configuration holding them is refused.
"""


class TableOutputConfig(Config):
    """Where one table-like output goes, and how it is written.

    Nothing about this class says that it is meant to be nested. What makes it
    nested is the declaration in the class that holds it, and this one could
    equally well be a configuration file of its own.
    """

    # The one thing a nested class does need is the constructor that
    # `config_as_json` builds a nested object with, which is the three keyword
    # arguments below. That is the whole of the contract, unless the class
    # holding it declares a `factory_function` of its own.
    def __init__(self, from_json_data_text: Optional[str] = None,
                 from_json_filename: Optional[PathOrStr] = None,
                 stderr_file: TextIO = sys.stderr) -> None:
        """Initialize one output section with its default values.

        Args:
            from_json_data_text: Optional JSON text to parse directly.
            from_json_filename: Optional path to a JSON file to read.
            stderr_file: Stream used for user-facing diagnostics.
        """
        # These three are the members of this class, and the editor shows them
        # as the rows below the object. They are shown in this order, because
        # this is the order they are assigned in, and not in the sorted order
        # that the JSON file has.
        self.file_name: str = 'participants.csv'
        self.output_format: str = 'CSV'
        self.encoding: str = 'utf-8'
        super().__init__(from_json_data_text=from_json_data_text,
                         from_json_filename=from_json_filename,
                         stderr_file=stderr_file)

    def get_validation_plan(self, stderr_file: TextIO) -> ValidationPlan:
        """Return the validators of one output section.

        These belong to this class, so they run for every object of it: both
        outputs of the configuration below are checked by these two steps and
        by nothing else.
        """
        _ = stderr_file
        # `normalize=True` makes this validator rewrite what it is given, so
        # `txt` comes back as `TXT`. A validation pass is not read only, and
        # the editor marks a value that a validator rewrote.
        formats = StrValidator(OUTPUT_FORMATS, ignore_case=True,
                               normalize=True)
        return [MemberValidationStep(member_names=['output_format'],
                                     validator=formats),
                MemberValidationStep(member_names=['encoding'],
                                     validator=CharEncodingValidator())]


# A validator has one method, which is fewer than pylint likes to see in a
# class. That is what a validator is, so the check is turned off for this one.
# pylint: disable-next=too-few-public-methods
class OutputsDiffer(WholeConfigValidator):
    """Refuse a configuration whose two outputs write the same file.

    This is a rule that reaches *across* the boundary between two nested
    objects, which is the one kind of rule neither of those objects can check
    for itself: each of them knows its own file name and nothing about the
    other. So it belongs to the class that holds them both, and it is a
    `WholeConfigValidator` because it is about no single member.
    """

    def validate(self, config: Config,
                 stderr_file: TextIO = sys.stderr) -> None:
        """Refuse two outputs that would be written to one file.

        Args:
            config: The whole course export, which is what makes the two file
                names comparable at all.
            stderr_file: Stream that the refusal is written to before it is
                raised, which is the contract every validator here follows.

        Raises:
            InvalidConfiguration: Both outputs name the same file.
        """
        assert isinstance(config, CourseExportConfig)
        audit = config.audit_output
        # There is nothing to compare while the optional output is absent,
        # which is what the declared defaults of this class leave it as.
        if audit is None or \
                audit.file_name != config.participant_output.file_name:
            return
        message = SAME_FILE_REFUSAL.format(name=audit.file_name)
        print(message, file=stderr_file)
        raise InvalidConfiguration(message)


class CourseExportConfig(Config):
    """What one course export writes, and where it writes it.

    The two outputs are the same kind of thing, so they are the same class.
    That is what a nested `Config` object is for: a group of settings that
    belongs together is written once and used as often as it is needed.
    """

    def __init__(self, from_json_data_text: Optional[str] = None,
                 from_json_filename: Optional[PathOrStr] = None,
                 stderr_file: TextIO = sys.stderr) -> None:
        """Initialize the course export with its default values.

        Args:
            from_json_data_text: Optional JSON text to parse directly.
            from_json_filename: Optional path to a JSON file to read.
            stderr_file: Stream used for user-facing diagnostics.
        """
        # One plain member first, so that an ordinary row can be seen beside
        # the two nested objects.
        self.course_name: str = 'python-intro'
        # A mandatory nested object. Its default is a real object of that
        # class, which is what makes the declared defaults a complete
        # configuration.
        self.participant_output: TableOutputConfig = TableOutputConfig(
            stderr_file=stderr_file)
        # An optional nested object. Its default is None, and this class
        # deliberately does not list it in `_omit_none_from_json()`, so `null`
        # is what is written for it and the editor gives it a row saying which
        # class is missing.
        self.audit_output: Optional[TableOutputConfig] = None
        super().__init__(from_json_data_text=from_json_data_text,
                         from_json_filename=from_json_filename,
                         stderr_file=stderr_file)

    def nested_configs(self) -> NestedConfigs:
        """Return which members hold nested configuration objects.

        This is the declaration that turns two ordinary looking members into
        configuration objects. `MEMBER` is one that is always there and
        `OPTIONAL_MEMBER` is one that may be `None`; `config_type` says which
        class to build when JSON holds an object for that member.

        The editor reads this same declaration, which is why it needs nothing
        from the application to show a nested object as what it is.
        """
        return {'participant_output': ConfigNesting(
                    kind=ConfigNestingKind.MEMBER,
                    config_type=TableOutputConfig),
                'audit_output': ConfigNesting(
                    kind=ConfigNestingKind.OPTIONAL_MEMBER,
                    config_type=TableOutputConfig)}

    def get_validation_plan(self, stderr_file: TextIO) -> ValidationPlan:
        """Return the one rule that is about both outputs at once.

        Every rule about what is *inside* an output belongs to
        `TableOutputConfig`, which is the point of nesting: the class that
        owns the values is the class that checks them, and the editor runs the
        real plan of whichever class owns a subtree.

        What is left here is the one rule that neither of those objects could
        check, because it is about the pair of them. That is also what makes a
        green badge on an output mean less than it looks: each of them can be
        a perfectly good `TableOutputConfig` while this rule refuses the
        configuration they are both in.
        """
        _ = stderr_file
        return [WholeConfigValidationStep(validator=OutputsDiffer())]


DESCRIPTIONS: Descriptions = {
    ('course_name',): 'Which course this export is about.',
    ('participant_output',): ('Where the list of registered participants is '
                              'written.'),
    ('participant_output', 'file_name'): ('The file the participants are '
                                          'written to.'),
    ('audit_output',): ('Where the administrator audit log is written, when '
                        'one is wanted at all.'),
    ('audit_output', 'file_name'): ('The file the audit log is written to. '
                                    'It has to differ from the one above.')}
"""What this application says about the members it declares.

Two of these describe a nested object itself, and two describe one member
inside one. That is the one place where a description path differs from
everything else `config_as_json` addresses by path: a description **crosses**
the boundary of a nested object, because an application explaining its own
settings should not have to know where its nesting boundaries fall.

The two `file_name` members are described separately, because in this
application they mean different things. The other members of those objects are
described by neither, and are shown with what their type says and nothing
else — which is what any member an application says nothing about is shown
with.
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
    run_example(example_name='e09_nested_config', args=args,
                config=CourseExportConfig(), descriptions=DESCRIPTIONS)


# The usual guard, so that importing this module from a test runs nothing.
if __name__ == '__main__':
    # Running a file directly puts only that file's own folder on sys.path,
    # so the `example` package this file belongs to would not be importable.
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    main()
