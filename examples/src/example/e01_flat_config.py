#! /usr/bin/env python3
"""Example 1: editing and validating a flat configuration.

This is the first example of the editor itself. The configuration class is
as small as a configuration class can be: one text member and one number
member, no nested structure. That is on purpose, because the point of this
example is not the configuration but the one call it takes to get an editor
for it:

````python
saved = edit(config=FlatConfig(), backend=TkEditor(),
             in_file='my_config.json')
````

That reads the file, opens the editor, and gives back the configuration
object that was written, or `None` when the user saved nothing. An
application that has already chosen its user interface can be even shorter,
because each backend package has an `edit` of its own:

````python
from edit_cfg_json_tk import edit
saved = edit(config=FlatConfig(), in_file='my_config.json')
````

Notice what the application does *not* do. It does not list its members for
the editor, it does not say which of them are text and which are numbers,
and it does not write a single widget. The editor finds all of that by
looking at the configuration object it is handed. The configuration schema
is declared exactly once, in `FlatConfig.__init__`, where it belongs.

Notice also what `edit()` gives back. The editor never modifies the object it
was handed, so the caller's own object is still holding the values it started
with; the object that reached the file is the one that comes back.

The members are shown in the order this class declares them, and the text
member is shown as the text it holds, without the quotation marks that JSON
puts around a string in the file. Both follow from the same idea: what the
editor shows is the configuration object the application declared, and how
that object is written to a file is an implementation detail of saving.

Both members can be edited. Each of them is a field, and what the user types
goes into the edit buffer of the model as the value it stands for: the text
member keeps whatever is typed, and the number member holds a number as soon
as the text is one. Text that is not a number yet is kept as it was typed,
because a value that is being typed is not valid for most of the time it
takes to type it.

Saying what is wrong with such a value is what the validation plan below is
for, and it is the second thing this example teaches. The editor has no
rules of its own: it hands the buffer to `FlatConfig` and reports what
`FlatConfig` says, so the user is told exactly what the application would
say when it read the same values from a file.

The validators show the two sides of that:

- `answer` must be a whole number between 0 and 100, so there is something
  that can fail.
- `name` has its first character upper cased, so there is something that
  rewrites. A validation pass is not read only, and a value that a validator
  rewrote is marked, because changing what the user just typed without
  showing it would be the worst thing the editor could do.

The first of those needs two validators rather than one, and the reason is
worth knowing. In Python `bool` is a subclass of `int`, so `True` really is
a whole number as far as `isinstance` is concerned, and a range check alone
would accept `true` in a field meant for a count.
`ValueTypeValidator` is what `config_as_json` has for exactly that:
`not_allowed_type=bool` says that a `bool` is not one of the whole numbers
this member accepts. Passing `strict=True` instead is the other way to say
it, because that matches `type(value)` exactly rather than by subclass; the
denied type is used here because its diagnostic names `bool` and so teaches
the reader what was rejected.

Run this example with one of:

````sh
python3 examples/src/example/e01_flat_config.py --ui dump
python3 examples/src/example/e01_flat_config.py --ui tk
python3 examples/src/example/e01_flat_config.py --ui textual
````

Inside this repository, use the virtual environment that the build creates,
because that is where the three packages are installed:
`./venv/bin/python3 examples/src/example/e01_flat_config.py --ui dump`.

The `--ui dump` variant needs neither a window nor a terminal, so it is also
what the tests of this example use. The same edit that a user would type
into a field can be made from the command line, which is what makes an
editor observable without a display. These three show the buffer being
accepted, being refused, and being rewritten:

````sh
python3 examples/src/example/e01_flat_config.py --ui dump --set answer=7
python3 examples/src/example/e01_flat_config.py --ui dump --set answer=500
python3 examples/src/example/e01_flat_config.py --ui dump --set name=other
````

In the two graphical backends the same pass is asked for rather than done
for the user: the Tkinter editor has a Validate button and the Textual
editor validates on `ctrl+r`, or on `f5`. Both of them also have Save and
Save as, which the last section below is about.

## Reading the values from a file

`-i` names the file to read. The application says nothing more than which
file it is; the editor constructs `FlatConfig` from it, because that is the
only way to give a load the policy and the automatic change reporting that a
`Config` object takes in its constructor and nowhere else.

There is a file for each outcome in [examples/data/](../../data/), so all of
them can be tried by hand:

````sh
cd examples/src/example
python3 e01_flat_config.py --ui dump -i ../../data/e01_complete.json
python3 e01_flat_config.py --ui dump -i ../../data/e01_incomplete.json
python3 e01_flat_config.py --ui dump -i ../../data/e01_unknown_key.json
python3 e01_flat_config.py --ui dump -i ../../data/e01_not_json.json
python3 e01_flat_config.py --ui dump -i ../../data/e01_bad_value.json
````

Only the first two of those open. The four ways a file can be refused are
worth knowing, because they are four different mistakes:

- **A value the file does not hold** is filled in from the default this class
  declares, and that member is marked, so the user can see which values are
  not the ones the file asked for. This is the default policy, which is
  `--policy strict-then-defaults`: load strictly, and fall back only when the
  strict load shows that the file is incomplete. `--policy strict` refuses
  such a file instead, and `--policy defaults` fills in without trying
  strictly first.
- **A key this configuration does not have** is refused under every policy.
  Filling in governs the keys that are missing and nothing else, and dropping
  an unknown key would lose whatever the file meant by it: such a file is
  either from a newer version of the application or has a misspelling in it.
- **Text that is not configuration** is refused. `config_as_json` reports
  text that is not JSON, and JSON that cannot be turned into these values, as
  the same thing, so the message says that much and the diagnostics below it
  say which of the two it was.
- **Values a validator refuses** are refused as well, which is the one that
  needs a word of explanation. A member validator returns the value that is
  stored back into the member, so a load that stopped part way through leaves
  it unknown which values were already rewritten and which were not. Showing
  that half converted state as if it were the file would be worse than saying
  that the file has to be corrected in a text editor first.

The first two cases are one `KeyError` as far as `config_as_json` is
concerned, and the editor tells them apart by retrying the load with the
defaults filling in: that rescues a file which is merely incomplete, and it
still refuses an unknown key. Nothing anywhere reads the text of a message to
decide which of the two it was.

## Writing the file again

`-o` names the file to write, and defaults to `-i`, which is what an editor
is normally asked to do. In the two graphical backends the user presses Save;
`--ui dump` prints once and the run is then over, so `--save` is what asks it
to really write the file. These four show a round trip, a round trip over the
input file, a save that is refused, and a save with nowhere to go:

````sh
cd examples/src/example
python3 e01_flat_config.py --ui dump -o /tmp/out.json --set answer=7 --save
cp ../../data/e01_complete.json /tmp/round.json
python3 e01_flat_config.py --ui dump -i /tmp/round.json --set answer=11 --save
python3 e01_flat_config.py --ui dump -o /tmp/out.json --set answer=500 --save
python3 e01_flat_config.py --ui dump --save
````

Two things about saving are worth knowing, and both follow from the same
idea: what is written is what the application would read back.

- **An invalid configuration is not written.** Saving is validating and then
  writing, so the third command above writes nothing and says what is wrong
  with the value instead. The file that was already there is untouched: this
  editor cannot leave a user with neither their old configuration nor a new
  one.
- **A validator rewrites on the way to the file too**, because saving runs
  the very same pass. `--set name=other --save` writes `Other`, and the
  editor shows `Other` afterwards rather than the `other` that was typed.

The fourth command is the one case where the editor has to ask something.
With neither `-i` nor `-o` there is nowhere to write, and a file name is not
something a library can guess: the text dump says so, and the two graphical
backends offer their Save as question instead.

## What the application has already decided

The editor does not run on its own. It runs inside an application that took
some key combinations for itself long before the editor was called, and that
knows what one of its own configuration files is called. `Settings` is where
the application says so, and every attribute of it has a default, so an
application with no opinion passes nothing and gets what the editor would
have chosen anyway:

````python
from edit_cfg_json import ActionSettings, Settings
saved = edit(config=FlatConfig(), backend=TkEditor(),
             settings=Settings(actions=ActionSettings(save=('ctrl+w',)),
                               file_extension='.cfg',
                               extension_enforced=True))
````

A real application writes that once, from what it knows. This example takes
the same answers from the command line instead, so that each of them can be
tried without a program per answer:

````sh
cd examples/src/example
python3 e01_flat_config.py --ui dump --key save=ctrl+w --ui textual
python3 e01_flat_config.py --ui dump --extension .cfg -o /tmp/plain --save
python3 e01_flat_config.py --ui dump --extension .cfg --enforce-extension \
    -o /tmp/out.json --save
````

The second of those writes `/tmp/plain.cfg`: a destination that is being
chosen and has no extension at all gets the one the application uses,
because it does not name a file that exists yet. The third writes nothing
and says why, because an enforced extension is what the application uses and
`/tmp/out.json` is not it. Without `--enforce-extension` the same file is
written as asked, which is the whole difference between an extension that is
a default and one that is enforced.

An extension that is enforced also refuses an input file that does not have
it. A name to read is never completed, whatever the setting, because it
names a file that already exists and completing it would open a different
file from the one that was asked for.

The keys of the editor are the same kind of decision. `--key save=ctrl+w`
moves Save, and `--key save_as=` takes the key away from Save as while
leaving the action reachable through the button and the command palette. Two
actions given the same combination are refused where the settings are built,
because only one of the two could ever run.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from pathlib import Path
from typing import Optional, TextIO
import sys
from config_as_json import Config, IntFloatValidator, MemberValidationStep, \
    PathOrStr, StrCaseChangeValidator, StrCaseSpec, StrPositionSpec, \
    ValidationPlan, ValueTypeValidator

LOWEST_ANSWER = 0
"""Smallest number that this configuration accepts as an answer."""

HIGHEST_ANSWER = 100
"""Largest number that this configuration accepts as an answer."""


class FlatConfig(Config):
    """A configuration with one text member and one number member.

    A later step shows this class docstring in the editor as the label of
    the configuration object, which is a good reason to write one.
    """

    def __init__(self, from_json_data_text: Optional[str] = None,
                 from_json_filename: Optional[PathOrStr] = None,
                 stderr_file: TextIO = sys.stderr) -> None:
        """Initialize the configuration with its default values.

        The three keyword arguments are the ones that `config_as_json`
        expects of a configuration class. Keeping to them is what lets the
        editor construct the class itself, which is how it validates: the
        buffer is written as JSON text and handed to this constructor.

        Args:
            from_json_data_text: Optional JSON text to parse directly.
            from_json_filename: Optional path to a JSON file to read.
            stderr_file: Stream used for user-facing diagnostics.
        """
        # The members are assigned before super().__init__() is called.
        # These assignments are both the schema and the default values, and
        # they are the only description of the configuration that exists.
        # The default name starts with an upper case character because the
        # validation plan below would otherwise rewrite the default itself,
        # and an editor that changed a value before the user had done
        # anything would be teaching the wrong lesson.
        self.name: str = 'Flat example'
        self.answer: int = 42
        super().__init__(from_json_data_text=from_json_data_text,
                         from_json_filename=from_json_filename,
                         stderr_file=stderr_file)

    def get_validation_plan(self, stderr_file: TextIO) -> ValidationPlan:
        """Return the validators that refuse and the one that rewrites.

        These are ordinary `config_as_json` validators, declared exactly as
        they would be in an application that had no editor at all. The
        editor runs this plan by constructing this class, so an application
        that adds a validator of its own gets it in the editor for free.

        The type of `answer` is checked before its range, so that a value
        that is no whole number is reported as the wrong type rather than
        as a number outside the range. `not_allowed_type=bool` is what keeps
        `true` out of a member meant for a count, since a `bool` is an `int`
        in Python and a range check on its own would let it through.
        """
        _ = stderr_file
        whole_number = ValueTypeValidator(int, not_allowed_type=bool)
        in_range = IntFloatValidator[int](min_value=LOWEST_ANSWER,
                                          max_value=HIGHEST_ANSWER,
                                          allowed_values=None)
        upper_first = StrCaseChangeValidator(
            special_position=StrPositionSpec.FIRST_IN_STRING,
            special_position_case=StrCaseSpec.UPPER,
            other_position_case=StrCaseSpec.ORIGINAL)
        return [MemberValidationStep(member_names=['answer'],
                                     validator=whole_number),
                MemberValidationStep(member_names=['answer'],
                                     validator=in_range),
                MemberValidationStep(member_names=['name'],
                                     validator=upper_first)]


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
    run_example(example_name='e01_flat_config', config=FlatConfig(), args=args)
    # `run_example` prints what `edit()` gave back, so that the contract of
    # this library is something the reader sees rather than something they
    # have to take on trust: the object that was written, or None.


# The usual guard, so that importing this module from a test runs nothing.
if __name__ == '__main__':
    # Running a file directly puts only that file's own folder on sys.path,
    # so the `example` package this file belongs to would not be importable.
    # Adding the folder above it makes both ways of using this file work:
    # `python3 examples/src/example/e01_flat_config.py` and
    # `from example import e01_flat_config` from a test.
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    main()
