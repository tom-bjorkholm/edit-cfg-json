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

The editor has no idea that either of these members is an enum, and needs
none. What it sees is the value as the file holds it, which is the text of
a member name, so an enum is edited in an ordinary text field like any
other piece of text. What makes that field more than free text is the
validation pass: it hands the buffer to `EnumConfig` exactly as a file
would be handed to it, so the user is told precisely what the application
itself would say.

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

Run this example with one of:

````sh
python3 examples/src/example/e02_enum_config.py --ui dump
python3 examples/src/example/e02_enum_config.py --ui tk
python3 examples/src/example/e02_enum_config.py --ui textual
````

Inside this repository, use the virtual environment that the build creates,
because that is where the three packages are installed:
`./venv/bin/python3 examples/src/example/e02_enum_config.py --ui dump`.

These four, run from the folder the examples live in, show a name being
accepted, a prefix being completed, a prefix that names two members being
refused, and a number being refused in a member that an `IntEnum` declares:

````sh
cd examples/src/example
python3 e02_enum_config.py --ui dump --set needed=ELECTRONIC
python3 e02_enum_config.py --ui dump --set needed=MECH
python3 e02_enum_config.py --ui dump --set needed=ELECT
python3 e02_enum_config.py --ui dump --set available=2
````

One thing to be ready for in the diagnostics: `config_as_json` reports a
name it cannot turn into an enum member as JSON that it failed to load, so
the useful line arrives after a sentence about the file possibly being the
wrong file. The editor shows what the application says, word for word, and
does not rewrite it into something friendlier. Inventing a better message
would mean guessing at what went wrong, and a guess that is wrong is worse
than a sentence too many.

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
name of an enum member for most of the time it takes to type it, and the
validation pass is what says so. The same `ELECT` in a *file* means the file
cannot be read as configuration at all, so the file is refused and the editor
does not open. Nothing is half typed in a file.
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
