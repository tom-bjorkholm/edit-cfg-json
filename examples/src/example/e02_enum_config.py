#! /usr/bin/env python3
"""Example 2: enum members, and the checking that comes free with them.

An enum is the natural type for a configuration member that has a small
fixed set of values, and `config_as_json` writes one to the file as the
*name* of the member rather than as its number. A file that says
`"needed": "ELECTRICAL"` can be read and edited by a person; a file that
said `"needed": 2` could not.

There is nothing else in this example: two members, both enums, and an
empty validation plan. That is the point of it. The class declares no
validator for either member, and yet a name that is no member of the enum
is refused, with a diagnostic that lists the names that do exist. The check
is not a validator; it is the conversion itself. Turning a name into an
enum member either works or it does not.

## The two hooks, and which of them you have to write

`parse_converters()` is the one an application has to declare. It says how
the text in the file becomes a rich Python value again, and
`Config.get_converter_dict()` builds that recipe for an enum. Leaving it
out is worse than getting an error: the load then quietly succeeds and the
attribute holds the *string* `'ELECTRICAL'` instead of
`NeededCompetence.ELECTRICAL`. Nothing complains until some later part of
the application compares that string with an enum member and finds them
different.

`serialize_converters()` is the one this example does not have to write.
`config_as_json` has a built-in write-side conversion for `Enum` and
`IntEnum` that writes the member name, and it covers both members of this
class. It is still worth knowing why that hook exists at all, and
`available` is the reason: an `IntEnum` *is* an `int`, so Python's own JSON
encoder writes its number and never offers it to anyone who might want to
write something else. The write-side hook runs before `json.dumps()`, which
is how the name reaches the file anyway.

## What that means in the editor

An enum is edited in an ordinary text field, because what the file holds is
the text of a member name and that is what the buffer holds too. The editor
does not need a field of its own for it, and it does not need to be told that
the member is an enum either: `parse_converters()` above already says so, and
the editor reads it there.

Two things follow from reading it, and both are visible below.

- **The member explains itself**, with no description mapping anywhere in
  this example. The enum class is a type, so it says what it is in its own
  docstring and it says which names it accepts by having them. That is the
  same kind of reading as the docstring of the configuration class, and it is
  not the reading of a validator, which this library never does.
- **A name that is no name of a member is refused as this member**, and not
  as JSON. Turning the text into an enum member is the very conversion that
  `parse_converters()` declares, so the editor runs it and shows what it says:
  `ELECT is not one of: MECHANICAL, ELECTRICAL, ELECTRONIC`, beside the field
  that holds `ELECT`. Nothing is invented and nothing is reworded — that
  sentence is the one `config_as_json` raises.

What makes the field more than free text after that is still the validation
pass: it hands the buffer to `EnumConfig` exactly as a file would be handed
to it, so the user is told precisely what the application itself would say.

## Matching is forgiving, and the editor shows that too

`config_as_json` looks for an exact name in the usual case variants first,
and then accepts a *unique* prefix, ignoring case. The three values of
these enums are chosen so that both sides of that are easy to try:

- `MECH` and `mechanical` both mean `MECHANICAL`. The validation pass
  writes the full name back into the buffer, and the row is marked as
  changed by a validator, because the editor never rewrites what the user
  typed without saying so.
- `ELECT` means nothing at all, because `ELECTRICAL` and `ELECTRONIC` both
  begin with it. It is refused, and the diagnostic lists all three names.

The forgiving half of that is why the editor waits before it says anything.
`ELECT` is refused, `ELECTR` is refused, and `ELECTRO` is a member — so a
name that is being typed is no name of a member for most of the time it takes
to type it. The editor therefore asks the question when the user **leaves the
field**, and not on every key, because a field that complained about every
half typed name would be complaining about nothing.

Run this example in one of the two editors, and leaving the field is the
thing to try, because it is what asks the question:

````sh
python3 examples/src/example/e02_enum_config.py --ui tk
python3 examples/src/example/e02_enum_config.py --ui textual
````

Inside this repository, use the virtual environment that the build creates,
because that is where the three packages are installed:
`./venv/bin/python3 examples/src/example/e02_enum_config.py --ui tk`.

Type `ELECT` into `needed` and move to the other field: the refusal appears
below that member, and typing the rest of the name takes it away again,
because what a conversion said is kept until that member is edited again.
That is the half of this example that only an editor has, since a field
losing the focus is not something a printout has to lose.

`--ui dump` is the very limited non-interactive user interface, and it prints
the model once. The four below make the same edits a user would type, and show
a name being accepted, a prefix being completed, a prefix that names two
members being refused, and a number being refused in a member that an
`IntEnum` declares:

````sh
cd examples/src/example
python3 e02_enum_config.py --ui dump --set needed=ELECTRONIC
python3 e02_enum_config.py --ui dump --set needed=MECH
python3 e02_enum_config.py --ui dump --set needed=ELECT
python3 e02_enum_config.py --ui dump --set available=2
````

The third of those is where reading `parse_converters()` earns its keep. A
name that no member has is refused by the conversion and not by a validator,
and `config_as_json` reports a failed conversion as JSON that it could not
load — a sentence about the file possibly being the wrong file, with the
useful line underneath it. That is exactly right for a program reading a
file, and it is wrong for a person editing a field, who did not ask about
JSON and is not looking at a file. So the editor runs the conversion of that
one member first, and shows what it said and nothing else.

## Enum members read from a file

The same three files, run from the folder the examples live in, show an enum
member being read, being filled in from the default, and being refused:

````sh
cd examples/src/example
python3 e02_enum_config.py --ui dump -i ../../data/e02_complete.json
python3 e02_enum_config.py --ui dump -i ../../data/e02_incomplete.json
python3 e02_enum_config.py --ui dump -i ../../data/e02_bad_enum.json
````

The last of the three is the interesting one, and it is where a load differs
from an edit. `ELECT` typed into a *field* is kept, because a name is not a
name of an enum member for most of the time it takes to type it, and leaving
the field is what says so. The same `ELECT` in a *file* means the file cannot
be read as configuration at all, so the file is refused and the editor does
not open. Nothing is half typed in a file, which is also why the message
there is the one `config_as_json` prints and not the one a field gets: a
refusal that the user cannot act on inside the editor is not a field being
edited, and reading the diagnostics of the load is exactly what they have to
do.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from enum import Enum, IntEnum, auto
from pathlib import Path
from typing import Optional, TextIO
import sys
from config_as_json import Config, ParseConverter, PathOrStr, ValidationPlan


# Two enums with the same three names, so that both kinds can be tried in
# the same editor. The names are deliberately chosen so that ELECTRICAL and
# ELECTRONIC share a prefix: a partly typed value is then sometimes enough
# to name a member and sometimes not, which is exactly the situation an
# editor has to handle well.

class NeededCompetence(Enum):
    """The competence that a task needs, as an ordinary enum.

    `auto()` numbers the members, and the numbers never reach the file:
    what is written and read back is the name.
    """

    MECHANICAL = auto()
    ELECTRICAL = auto()
    ELECTRONIC = auto()


class AvailableCompetence(IntEnum):
    """The competence that is available, as an int enum.

    This is the interesting one for the file format. An `IntEnum` member is
    an `int`, so Python's JSON encoder would happily write `1` for it. The
    write-side conversion built into `config_as_json` runs first and writes
    `"MECHANICAL"` instead.
    """

    MECHANICAL = auto()
    ELECTRICAL = auto()
    ELECTRONIC = auto()


class EnumConfig(Config):
    """A configuration whose two members are both enums.

    One is an `Enum` and the other an `IntEnum`, and the editor treats them
    the same way, because in the file they are the same thing: the name of
    a member.
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
        # The members are assigned before super().__init__() is called, and
        # the enum member assigned here is both the default value and the
        # only statement of the type anywhere. There is no annotation to
        # read at runtime, so the value is what tells the editor and the
        # library alike what this member is.
        self.needed: NeededCompetence = NeededCompetence.ELECTRICAL
        self.available: AvailableCompetence = AvailableCompetence.MECHANICAL
        super().__init__(from_json_data_text=from_json_data_text,
                         from_json_filename=from_json_filename,
                         stderr_file=stderr_file)

    def get_validation_plan(self, stderr_file: TextIO) -> ValidationPlan:
        """Return no validation steps at all.

        An empty plan is not an oversight here, it is the lesson. Nothing
        below refuses a wrong value, and a wrong value is refused anyway,
        because a name that is no member of the enum cannot be converted
        into one in the first place.
        """
        _ = stderr_file
        return []

    def parse_converters(self) -> dict[str, ParseConverter]:
        """Return how the name in the file becomes an enum member again.

        This is the one hook an enum member needs. Without it the load
        succeeds and leaves a plain string in the attribute, which is the
        kind of mistake that is found a long way from where it was made.

        There is deliberately no `serialize_converters()` beside it: the
        built-in write-side conversion for `Enum` and `IntEnum` already
        writes the member name, and repeating it here would suggest that an
        application has to.
        """
        return {'needed': self.get_converter_dict(NeededCompetence),
                'available': self.get_converter_dict(AvailableCompetence)}


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
    run_example(example_name='e02_enum_config', config=EnumConfig(), args=args)


# The usual guard, so that importing this module from a test runs nothing.
if __name__ == '__main__':
    # Running a file directly puts only that file's own folder on sys.path,
    # so the `example` package this file belongs to would not be importable.
    # Adding the folder above it makes both ways of using this file work:
    # `python3 examples/src/example/e02_enum_config.py` and
    # `from example import e02_enum_config` from a test.
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    main()
