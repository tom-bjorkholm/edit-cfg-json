#! /usr/bin/env python3
"""Example 5: saying that reading the file changed it.

An application that has been in use for a while has renamed a member, dropped
one and added one. `config_as_json` reads the old files anyway: a
`ReadOldConfiguration` object says how the old shape becomes the current one,
and the rest of the application never has to know that old files exist.

For an editor that is a problem, and the reason is worth stating plainly. The
values on the screen are then **not** the values in the file, and an editor
that showed them without a word would look broken: a member that says
`monthly-summary` is nowhere to be found in a file that says `title`, and a
member that says `2` is in no version of the file at all. Saving would then
write a file quite unlike the one that was opened, which is exactly what the
user asked for and not at all what they would expect if nobody said so.

## Three ways a load changes a file, and one way of finding all of them

- the rules for an older format rename a key, remove a key, or supply a value
- parsing or validating normalizes a value, as the case change on `owner`
  below does
- the declared defaults fill in what an incomplete file left out, which is
  what example 1 is about

The editor finds all three the same way: it writes the loaded values back to
JSON and compares that with the text of the file, key by key. That needs
nothing at all of the configuration class, which is why it is the mechanism
and not the fallback, and it is exact, because it compares what would be
written with what is there.

## What the load records, and why every class gets it

The comparison can see that the file has no `report_name` and that the values
hold one. It cannot see that `report_name` is what `title` became: a key that
was renamed is simply gone, and nothing in the file says what it turned into.

`config_as_json` records that while it reads. Every automatic change becomes
one `RocfChange`, saying which kind of change it was, which path of the file it
consumed and which path of the configuration it produced, and the editor puts
each of them at the member it produced. So `report_name` says that it was read
from the older key `title`, `format_version` says that it was supplied because
the file is older, and `owner` says only that the load changed it, because a
value a validator normalized is recorded nowhere and the comparison is all
there is for it.

**Your class needs to do nothing to get this.** The records are read from
`Config.auto_change_hook()`, and `Config` gives every configuration object one
of those whether the application asked for one or not. `OldFormatConfig` below
declares `auto_ch_hook` in its own `__init__` and hands it on, which is what an
application does when it wants to read the records itself; `NoHookConfig` below
it is the same configuration by a class that does not. The two report exactly
the same, which is the point of having both of them here.

One thing to know if your own application wants to read those records:
`ConfigAutoChangeHook.check_data_version` is how it says which version of them
it was written for, and a `config_as_json` that records another version then
says so plainly instead of being misread. An application that only wants them
printed calls `print_changes` and needs no such check at all.

Run this example with one of:

````sh
python3 examples/src/example/e05_old_format_config.py --ui dump
python3 examples/src/example/e05_old_format_config.py --ui tk
python3 examples/src/example/e05_old_format_config.py --ui textual
````

Inside this repository, use the virtual environment that the build creates:
`./venv/bin/python3 examples/src/example/e05_old_format_config.py --ui dump`.

These two are the point of the example. The first opens a file in the old
shape and says what reading it did; the second opens the same configuration in
the current shape and says nothing at all, because nothing happened:

````sh
cd examples/src/example
python3 e05_old_format_config.py --ui dump -i ../../data/e05_old_format.json
python3 e05_old_format_config.py --ui dump -i ../../data/e05_current.json
````

And this is the same old file read by the class that declares no hook, through
the program that the core installs, which needs no example at all:

````sh
PYTHONPATH=examples/src edit-cfg-json --module example.e05_old_format_config \
    --class NoHookConfig -i examples/data/e05_old_format.json
````

Every mark is the same and every word is the same, because what the load
recorded belongs to the object it loaded and not to the constructor of the
class. What the message is left with is the one fact that belongs to no member:
`debug_trace` is in the file, this configuration does not use it, and saving
leaves it out.

Migrating the file is then one more option on the same program, because a
program with nobody to press Save is the one that offers `--save`:

````sh
PYTHONPATH=examples/src edit-cfg-json --module example.e05_old_format_config \
    --class OldFormatConfig -i examples/data/e05_old_format.json \
    -o current.json --save
````
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from pathlib import Path
from typing import Optional, TextIO
import sys
from config_as_json import Config, ConfigAutoChangeHook, ConfigPath, \
    MemberValidationStep, PathOrStr, ReadOldConfiguration, RocfKeyRename, \
    StrCaseChangeValidator, StrCaseSpec, StrPositionSpec, ValidationPlan

CURRENT_FORMAT = 2
"""Version number that the current shape of this configuration file has.

An old file has no `format_version` at all, and the rules below supply this
number for it. That is the value the editor marks as one the file did not
hold: it came from the migration rules and from nowhere else.
"""


class OldFormatRules(ReadOldConfiguration):
    """How a file written by an older version becomes a current one.

    All three kinds of rule this example needs are here, and each of them is
    something the editor has to be able to report: a key that changed its
    name, a key that is gone, and a value that only the current shape has.

    Both configuration classes below return an object of this class, so the
    two of them really are the same configuration read the same way. What
    differs between them is only whether the reading can be reported.
    """

    def get_json_key_renames(self) -> list[RocfKeyRename]:
        """Return the key of the old shape that has a new name today."""
        # A rename is what leaves the editor with nothing to go on: the value
        # is the one the file holds, and it is held under a name that is not
        # in the file. Only the hook can say that `title` became this.
        return [RocfKeyRename(old='title', new='report_name')]

    def get_keys_to_prune(self) -> list[str]:
        """Return the key of the old shape that no longer exists."""
        # This one the editor can see for itself, because the key is in the
        # file and is in nothing the configuration writes back.
        return ['debug_trace']

    def get_missing_path_values(self) -> dict[ConfigPath, object]:
        """Return the value that only the current shape of the file has."""
        # Note that this is not the declared default of `format_version`,
        # although it happens to be the same number. This value comes from
        # the migration rules, which is why it is reported as one of them.
        return {('format_version',): CURRENT_FORMAT}


class OldFormatConfig(Config):
    """A report configuration that can be read from an older file too.

    Its constructor declares `auto_ch_hook` and hands it on, which is what an
    application does when it wants to read the records of a load from a hook
    object of its own. The editor needs none of that: it reads them from the
    object the load produced, so `NoHookConfig` below reports the same.
    """

    def __init__(self, from_json_data_text: Optional[str] = None,
                 from_json_filename: Optional[PathOrStr] = None,
                 auto_ch_hook: Optional[ConfigAutoChangeHook] = None,
                 stderr_file: TextIO = sys.stderr) -> None:
        """Initialize the configuration with its default values.

        Args:
            from_json_data_text: Optional JSON text to parse directly.
            from_json_filename: Optional path to a JSON file to read.
            auto_ch_hook: Hook notified about what reading an older file did.
                An application declares this when it wants to read those
                records from an object of its own. The editor asks the
                configuration object instead, so a class without this
                parameter is reported on exactly as well, which is what
                `NoHookConfig` below is here to show.
            stderr_file: Stream used for user-facing diagnostics.
        """
        self.format_version: int = CURRENT_FORMAT
        self.report_name: str = 'daily-summary'
        self.owner: str = 'Ada Lovelace'
        self.refresh_seconds: int = 300
        super().__init__(from_json_data_text=from_json_data_text,
                         from_json_filename=from_json_filename,
                         auto_ch_hook=auto_ch_hook, stderr_file=stderr_file)

    def _get_read_old_config(self) -> ReadOldConfiguration:
        """Return the rules that turn an older file into a current one."""
        # `Config.parse_json()` calls this while it reads, before it checks
        # that the keys of the file are the keys this class declares. That is
        # why an old file is accepted at all rather than refused for holding
        # a key called `title` that this class does not have.
        return OldFormatRules()

    def get_validation_plan(self, stderr_file: TextIO) -> ValidationPlan:
        """Return the one rule, which rewrites rather than refuses.

        A member validator returns the value that is stored back into the
        member, so this one changes what the file held instead of complaining
        about it. That is the second of the three ways a load changes a file,
        and the editor reports it exactly as it reports the others: `owner`
        was not this in the file, so `owner` is marked.
        """
        _ = stderr_file
        capitalize = StrCaseChangeValidator(
            special_position=StrPositionSpec.FIRST_IN_WORD,
            special_position_case=StrCaseSpec.UPPER,
            other_position_case=StrCaseSpec.ORIGINAL)
        return [MemberValidationStep(member_names=['owner'],
                                     validator=capitalize)]


class NoHookConfig(OldFormatConfig):
    """The same configuration, by a class that takes no change hook.

    Everything about this configuration is inherited, so the two classes hold
    the same members, read the same older files by the same rules and rewrite
    the same value. The one difference is the constructor below, which has
    nowhere to put a hook.

    That is on purpose, and it is what most configuration classes look like:
    the three keyword arguments that `config_as_json` documents, and no more.
    Such a class is edited exactly as well **and reported on exactly as
    fully**, because `Config` gives it a hook of its own and the editor reads
    that one. Nothing an application has to opt into is needed for any of this.
    """

    def __init__(self, from_json_data_text: Optional[str] = None,
                 from_json_filename: Optional[PathOrStr] = None,
                 stderr_file: TextIO = sys.stderr) -> None:
        """Initialize the configuration, with no hook to be given.

        Args:
            from_json_data_text: Optional JSON text to parse directly.
            from_json_filename: Optional path to a JSON file to read.
            stderr_file: Stream used for user-facing diagnostics.
        """
        # Leaving the hook out here used to be what made this class the one
        # that could not report the older keys of a file. It no longer costs
        # anything at all, and running the two classes over the same file is
        # what shows that.
        super().__init__(from_json_data_text=from_json_data_text,
                         from_json_filename=from_json_filename,
                         stderr_file=stderr_file)


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
    run_example(example_name='e05_old_format_config', args=args,
                config=OldFormatConfig())


# The usual guard, so that importing this module from a test runs nothing.
if __name__ == '__main__':
    # Running a file directly puts only that file's own folder on sys.path,
    # so the `example` package this file belongs to would not be importable.
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    main()
