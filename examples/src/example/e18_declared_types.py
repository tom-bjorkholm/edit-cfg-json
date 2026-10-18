#! /usr/bin/env python3
"""Example 18: what the type of a member says, and the member holding nothing.

Every example before this one showed the editor working out what a member is
from the *value* it holds. That is a great deal: it tells the digits of a
number from a text that happens to be digits, and it is why a text field never
shows the quotation marks a JSON file puts around a string. There are two
things a value cannot say, and this example is about both of them.

**A value cannot say what a member that holds nothing is for.** A member whose
default is `None` held nothing when the file was last agreed with, so nothing
was learned from it.

**A value can say the wrong thing.** `self.threshold: float = 0` is a member
that holds a number, and `0` is a whole number. Reading the value alone would
call it a whole number for the rest of the session.

So the editor reads the *declaration* as well, and the declaration wins.
Nothing has to be written for it: these are the annotations that a well
written configuration class already has.

## Where the declaration is read from

Three places, and each of them covers a pattern the others do not.

- **A dataclass** records the real type of every field, which
  `dataclasses.fields()` and `typing.get_type_hints()` answer with.
- **A class level annotation** records one in the same way, with no dataclass
  around it.
- **The ordinary `Config` pattern records nothing at all.** `self.title: str =
  'Quarterly report'` inside `__init__` is a PEP 526 annotation on an instance
  attribute, and Python keeps it nowhere: `typing.get_type_hints()` answers
  with nothing useful for the pattern that every other example in this folder
  uses. So the editor reads the *source* of the class and takes the
  annotations from there.

All three are optional, and that is the point of having three. A class defined
in an interactive session, by `exec` or inside a frozen program has no source
to read, an annotation naming something that only exists while a type checker
is running will not resolve, and a member can simply be assigned without an
annotation. Every one of those costs that member its declaration and nothing
else: the value is still there to answer, exactly as before.

Run this example and read the column between the name and the value of each
member, which is where the type of a member is said, spelled the way a Python
type hint spells it:

````sh
python3 examples/src/example/e18_declared_types.py --ui dump
python3 examples/src/example/e18_declared_types.py --ui tk
python3 examples/src/example/e18_declared_types.py --ui textual
````

Inside this repository, use the virtual environment that the build creates:
`./venv/bin/python3 examples/src/example/e18_declared_types.py --ui tk`.

`threshold` says `float` although it holds `0`, and `subtitle` says `None`,
because that is what it holds; the line under it says the whole of what it is
declared as, `str | None`, because the column shows only the type the member
holds now. `spare` says `list`, and the line under it says that this was taken
from its value: it is the one member of this class that was deliberately left
without an annotation, so nothing says what its elements would be.

The column is a pull-down on every row. On most rows it is disabled, because
the declaration allows one type and there is nothing to choose. On `subtitle`,
`footer`, `note` and `width` it is active, because each of them is declared to
allow two types, and choosing one of them is how the user changes what the
member holds. The two sections below are about that.

## A member that may hold nothing has two states

`Optional[str]` says more than what kind of value the member takes. It says
that the member may hold **no value at all**, which is a different thing from
holding an empty text, and a JSON file writes the two of them differently:
`null` and `""`.

Telling those two apart was the open question this library carried from its
first design draft. The answer is that **the user chooses between the types
the class declared**, and `None` is one of them. `Optional[str]` is
`str | None`, and the pull-down of the row offers exactly those two:

- while it **holds a value** the pull-down says `str` and the row is an
  ordinary field;
- while it **holds nothing** the pull-down says `None`, and the row has no
  field at all and nothing where a value would be.

Choosing `str` gives the member the empty text, and choosing `None` takes its
value away. A value is not something that can be typed away, so *nothing* is
chosen and never typed: typing `null` into such a field is text that means no
value of the member, exactly as any other text of the wrong type is.

`subtitle` starts out holding nothing and `footer` starts out holding a value,
so both states are on the screen at once. Without a display, `--set-type`
chooses a type in the same pull-down, and `--set` then types into the field
that choosing `str` gave the member:

````sh
cd examples/src/example
python3 e18_declared_types.py --ui dump --set-type subtitle=str
python3 e18_declared_types.py --ui dump --set-type subtitle=str \
    --set subtitle=Draft
python3 e18_declared_types.py --ui dump --set-type footer=None
````

The two states really are two different files, which is the whole reason for
telling them apart. These two write `"subtitle": null` and `"subtitle": ""`,
and no field could have told them apart:

````sh
cd examples/src/example
python3 e18_declared_types.py --ui dump --save -o /tmp/nothing.json
python3 e18_declared_types.py --ui dump --set-type subtitle=str \
    --save -o /tmp/empty.json
````

## Reading the two states back from a file

There is a file in [examples/data/](../../data/) holding the mirror of the
values above: an empty subtitle and no footer at all. It is what shows that
the two states survive a round trip, because a file is where the difference
between them is really kept.

````sh
cd examples/src/example
python3 e18_declared_types.py --ui dump -i ../../data/e18_report.json
python3 e18_declared_types.py --ui tk -i ../../data/e18_report.json
````

`subtitle` comes back as an ordinary field holding nothing typed into it and
`footer` comes back as `None` with no field, which is the state the file's
`null` put it in. `note` comes back as `None` too, and the file holds no key
of that name at all, which is the section below. `width` comes back holding
`str`, because the file holds the text `auto` for it: until the user chooses,
the type a member of two types holds is the one its value is.

## The other kind of optional, which is also two states

`note` is declared `Optional[str]` like the two above, and its class writes it
differently: `_omit_none_from_json()` names it, so while it holds nothing the
file has no key for it rather than a `null`. Example 19 is about that
difference and about the members it reaches; what matters here is that it does
not change what the editor offers. `note` has the same two states as
`subtitle` and `footer`, chosen between in the same pull-down, and the line
under it says which of the two kinds of optional it is, because the file it
writes is what differs:

````sh
cd examples/src/example
python3 e18_declared_types.py --ui dump --set-type note=None
python3 e18_declared_types.py --ui dump --set-type note=None \
    --save -o /tmp/no_note.json
````

## A member that may hold two kinds of value

`width` is declared `int | str`: a number of characters, or a word such as
`auto` that the report generator understands. Which of the two it holds is
chosen in its pull-down, exactly as `None` is chosen above, and **the text in
its field is read as a value of the type chosen**. So `5` is the number five
while `int` is chosen and the text `5` while `str` is, and the file holds `5`
or `"5"` accordingly.

Switching keeps what still fits. `width` holds the number `80`, and choosing
`str` makes it the text `80`; choosing `int` again makes it the number again.
A text that is no number, such as `auto`, is not a number of any kind, so
choosing `int` for it gives the member `0`:

````sh
cd examples/src/example
python3 e18_declared_types.py --ui dump --set-type width=str
python3 e18_declared_types.py --ui dump --set-type width=str \
    --set width=auto
python3 e18_declared_types.py --ui dump --set-type width=str \
    --set-type width=int
````

The choice is the user's, and typing does not change it: `auto` typed while
`int` is chosen is a value of the wrong type, not a choice of `str`. What the
application accepts is still what decides, though. `config_as_json` checks no
value against its annotation, so a validation pass accepts `auto` all the same,
and the editor then shows the type the application was given — `str` — rather
than a choice the value no longer fits:

````sh
cd examples/src/example
python3 e18_declared_types.py --ui dump --set width=auto
````

## An empty list that can now be given an element

Example 11 has a list whose class declares no element and which holds none, so
that no *value* anywhere says what an element of it looks like. Its declared
type does: `list[str]` says that an element is text, and the empty text is the
one value of that kind which says no more than which kind it is.

That is asked **last**, after the class has been asked for an element to copy
and the member for one of its own, because a value the application wrote says
more about what belongs in that list than its kind does.

`tags` here is such a list. `spare` is the member that still cannot be given
one, and it is worth looking at why: it is assigned without an annotation, so
its class declares no element for it, it holds none, and there is no declared
type to make one of. That is now the only way to reach that state with a
JSON-compatible member, and the moral is the one this whole example teaches —
annotate the members of a configuration class, and the editor will use it.

````sh
cd examples/src/example
python3 e18_declared_types.py --ui dump --add tags --set tags.0=urgent
python3 e18_declared_types.py --ui dump --add spare
````

The second of those adds nothing and says so, because the control it presses
does not exist.

## What the application still decides

Nothing here is a way round the rules. `OptionalMemberValidator` is what
`config_as_json` has for a member that may hold nothing: it lets `None`
through untouched and applies the validator inside it to every other value.
So `footer` is either nothing at all or a text of at least three characters:

````sh
cd examples/src/example
python3 e18_declared_types.py --ui dump --set footer=ab
python3 e18_declared_types.py --ui dump --set-type footer=None
````

The first is refused, because two characters are fewer than three. The second
is accepted, because no footer at all is one of the two states the class
allowed. An application that wanted to refuse the second as well would say so
by not declaring the member optional in the first place — and then the
pull-down on that row would offer `str` alone, and be disabled, because there
would be nothing else to choose.

**A validator can move a member between the two states as well**, which is
worth seeing in one of the two editors rather than in a printout. `footer` has
a second rule that turns a footer of no characters into no footer at all, so
clearing that field and asking for a validation pass takes the field away and
leaves the pull-down of the row saying `None`. The validator changed the type
the member holds, and the editor shows the type it changed it to:

````sh
cd examples/src/example
python3 e18_declared_types.py --ui tk
python3 e18_declared_types.py --ui dump --set footer=
````
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from pathlib import Path
from typing import Optional, TextIO
import sys
from config_as_json import Config, MemberValidator, \
    MemberValidationStep, OptionalMemberValidator, PathOrStr, \
    StrLenValidator, ValidationPlan
from edit_cfg_json import Descriptions

SHORTEST_TEXT = 3
"""How many characters the shortest acceptable subtitle or footer has."""


def _unannotated_list() -> list[str]:
    """Return the empty list of the member that has no declared type.

    The member this is assigned to is deliberately left without an
    annotation, which is what makes it the one member of this class that
    nothing says anything about. It is written this way rather than as
    `self.spare = []` so that a type checker is still told what the member
    holds: what the example is about is what the *editor* can read, and a
    configuration class with a type checking error in it would teach the
    wrong lesson twice over.
    """
    return []


# A validator is a class of the application, and this one is as small as a
# validator gets. It is here because it does something worth seeing in an
# editor: a member validator returns the value that is stored back into the
# member, so one of them can move a member from holding a value to holding
# nothing while the user watches. The row then loses its field, and both
# editors make their widgets again for it.
# pylint: disable-next=too-few-public-methods
class EmptyIsNothing(MemberValidator):
    """Turn a footer of no characters into no footer at all."""

    def validate_member(self, config: Config, member_name: str,
                        member_value: object,
                        stderr_file: TextIO = sys.stderr) -> Optional[object]:
        """Return nothing for an empty text, and the value for anything else.

        Args:
            config: The configuration object that owns the member.
            member_name: Name of the member being validated.
            member_value: What that member holds.
            stderr_file: Stream used for user-facing diagnostics.

        Returns:
            The value that is stored back into the member.
        """
        _ = (config, member_name, stderr_file)
        return None if member_value == '' else member_value


# Eight members is more than pylint likes one class to have, and here each of
# them is one thing a declaration says that a value cannot: they are side by
# side so that the column of the types of all of them can be read at once.
# pylint: disable-next=too-many-instance-attributes
class ReportConfig(Config):
    """What one report is generated with, and where it is written.

    Every member of this class is annotated except one, and the editor reads
    those annotations. Reading them is what lets it say that `threshold` holds
    a number rather than a whole number, what gives `subtitle`, `footer` and
    `note` the two states that an optional member has, and what lets `width`
    hold either of the two types it is declared to hold.

    `note` is the member this class leaves out of the file while it holds
    nothing, and the other two are written as `null`. Example 19 is about that
    difference.
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
        # An ordinary text member. Its value says everything about it, so the
        # annotation adds nothing here — which is the honest baseline for
        # everything below it.
        self.title: str = 'Quarterly report'
        # Declared to allow no value, and holding none. Without the
        # annotation the editor would know nothing at all about this member:
        # a value of None says nothing about what would have been there. It
        # has no validator, so both of its states can be saved and the two
        # files compared.
        self.subtitle: Optional[str] = None
        # Declared to allow no value, and holding one. This is the state that
        # a field can show, and choosing `None` in its pull-down is what takes
        # the value away again.
        self.footer: Optional[str] = 'Confidential'
        # Declared to allow no value as well, and left out of the file while
        # it holds none, which is what `_omit_none_from_json()` below says.
        # It has the same two states as the two above it; the difference is
        # the file, and example 19 is about that difference.
        self.note: Optional[str] = 'Draft, do not circulate'
        # The member whose value says the wrong thing. `0` is a whole number
        # and this member holds a number, which only the annotation says.
        # Writing a whole number for the default of a member that holds a
        # number is ordinary Python, and it is exactly what makes the value
        # an unreliable source of the type.
        self.threshold: float = 0
        # A member that may hold two kinds of value. Which of them it holds is
        # chosen in the pull-down of its row, and the text typed into its
        # field is read as a value of the type chosen: `5` is a number while
        # `int` is chosen and a text while `str` is.
        self.width: int | str = 80
        # An empty list. No value anywhere says what an element of it is, and
        # `list[str]` does.
        self.tags: list[str] = []
        # The one member with no annotation, and therefore the one member
        # that still cannot be given an element.
        self.spare = _unannotated_list()
        super().__init__(from_json_data_text=from_json_data_text,
                         from_json_filename=from_json_filename,
                         stderr_file=stderr_file, member_name=member_name)

    def _omit_none_from_json(self) -> list[str]:
        """Return the members that are left out of the file while empty.

        `config_as_json` writes `null` for an optional member by default, and
        a member named here is left out of the file altogether instead. The
        editor reads this, because it decides what the line under the member
        says and what a save writes, and it asks the object itself for such a
        member so that it has a row whether the file holds it or not.
        """
        return ['note']

    def get_validation_plan(self, stderr_file: TextIO) -> ValidationPlan:
        """Return the rules that this configuration is checked against.

        `OptionalMemberValidator` is what `config_as_json` has for a member
        that may hold nothing: it lets `None` through untouched and applies
        the validator inside it to every other value. That is what makes a
        two character footer refused while no footer at all is accepted.

        `subtitle` deliberately has no rule of its own, so that both of its
        states reach the file and the two files can be compared.

        The two steps for `footer` run in the order they are written, so an
        empty footer becomes no footer at all before the length is looked at,
        and no footer at all is then let through. Anything shorter than three
        characters and not empty is refused.
        """
        _ = stderr_file
        long_enough = StrLenValidator(min_length=SHORTEST_TEXT,
                                      max_length=None)
        optional_text = OptionalMemberValidator(long_enough)
        return [MemberValidationStep(member_names=['footer'],
                                     validator=EmptyIsNothing()),
                MemberValidationStep(member_names=['footer', 'note'],
                                     validator=optional_text)]


DESCRIPTIONS: Descriptions = {
    ('title',): 'What the report is called.',
    ('subtitle',): ('A second line under the title, or no second line at '
                    'all.'),
    ('footer',): 'What is printed at the bottom of every page, if anything.',
    ('note',): ('A remark for whoever runs the report. It is left out of the '
                'file rather than written as null, which is a difference '
                'between two files and not between two rows.'),
    ('threshold',): 'The largest share of a page that one column may take.',
    ('width',): ('How wide a column is: a number of characters, or a word '
                 'the report generator understands, such as auto.'),
    ('tags',): 'Labels for this report. A new one is an empty text.',
    ('spare',): ('Anything else, and nothing says what one of them is: this '
                 'member is the one without an annotation.')}
"""What this application says about the members it declares.

The type of each member says the rest, under whatever is written here, and
saying the same thing in both places is how one of the two comes to be wrong.
So nothing here repeats what the annotation already says.
"""


def main(args: Optional[list[str]] = None) -> None:
    """Run this example from the command line.

    Args:
        args: Optional replacement for `sys.argv[1:]`, mainly for tests.
    """
    # pylint: disable-next=import-outside-toplevel
    from example.cmd_line import run_example
    run_example(example_name='e18_declared_types', config=ReportConfig(),
                descriptions=DESCRIPTIONS, args=args)


if __name__ == '__main__':
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    main()
