#! /usr/bin/env python3
"""Example 12: an application that looks after the file it overwrites.

Saving writes over whatever the destination holds, and what it holds is a
configuration somebody wrote. It may be the one this session read a minute
ago, and it may be one that was written by another person on another day; the
editor cannot tell the two apart, and it can keep the file either way.

That is the whole of this example: **the file that a save is about to
overwrite is kept first, and the user is asked before it happens**. Neither is
a rule of the editor, because neither is the editor's to decide. Both come out
of one `edit_cfg_json.Settings`, which is where an application says what it has
already decided:

````python
from edit_cfg_json import Settings
saved = edit(config=ArchiveConfig(), backend=TkEditor(),
             settings=Settings(file_extension='.cfg', backup_suffix='.old',
                               backup_count=3))
````

That is what `FILE_SETTINGS` below says, and it says three things:

- **`backup_suffix`** is added to the whole file name, so `archive.cfg` is
  kept as `archive.cfg.old`. Adding rather than replacing is what lets one
  attribute say every shape an application wants: `.bak`, which is the
  default, `.old`, which this example uses, and `~`, which some editors use.
  `None` keeps nothing, for an application that looks after its files itself.
- **`backup_count`** is how many of them are kept. This example keeps three,
  so they are numbered: `archive.cfg.old_1` is the file that was overwritten
  last, and each save moves every one of them one number further back until
  the oldest falls off the end. An application that keeps one, which is the
  default, gets `archive.cfg.old` with no number in it, because a number would
  say that there are others when there are not.
- **`confirm_overwrite`** is whether the user is asked first. It is `True` by
  default, which is what this example uses without saying so.

## What the editor does with them

Open the editor on a file and press Save:

````sh
cd examples/src/example
cp ../../data/e12_archive.cfg /tmp/archive.cfg
python3 e12_backup_files.py --ui tk -i /tmp/archive.cfg
python3 e12_backup_files.py --ui textual -i /tmp/archive.cfg
````

Change `keep_days`, press Save, and the editor asks before it writes:
*File /tmp/archive.cfg already exists. Overwrite it? What it holds now is kept
as /tmp/archive.cfg.old_1.* The answer that leaves the file alone is the one
the question opens on, in the dialog of the Tkinter editor and on the modal
screen of the Textual one, because a user who answers without reading should
keep what they have.

Change something and press Save a second time, and **nothing is asked and
nothing is kept**. The file that a second save writes over is the file that
the first save wrote: it is the user's own work of a minute ago, a backup of
it would push the configuration that was really there one number further from
being found, and a question about it would be a question about nothing. It is
asked once per destination per session, which is also why Save as onto some
other existing file asks again.

Answer *Overwrite* — or *Do not save*, and watch the file stay as it was.

## What is not in this file

The configuration class below is as small as it can be, and deliberately so:
this example is about the file and not about the members. It declares one text
member, one number member and one true-or-false member, hands over no
`Descriptions` mapping at all, and has exactly one rule — the one that makes
the refused save above refusable. Example 1 is where a flat configuration is
really taught, example 3 is where the descriptions are, and examples 8 to 11
are where the shapes a real configuration has are.

The file name extension is in `FILE_SETTINGS` too, and it is example 1 that
teaches what it does. It is here because an application that has an opinion
about what its files are called usually has one about how they are looked
after, and both of them are one object.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from pathlib import Path
from typing import Optional, TextIO
import sys
from config_as_json import Config, MemberValidationStep, PathOrStr, \
    ValidationPlan, ValueTypeValidator
from edit_cfg_json import Settings

FILE_SETTINGS = Settings(file_extension='.cfg', backup_suffix='.old',
                         backup_count=3)
"""What this application has already decided about its own files.

A real application writes this once, from what it knows about itself. Every
attribute has a default, so the two this example says nothing about — whether
the extension is enforced, and whether overwriting is confirmed — are what the
editor would have chosen anyway.
"""


class ArchiveConfig(Config):
    """Where this application archives what it collects.

    The members are three ordinary values and are not what this example is
    about. What it is about is what happens to the file they are written to
    when it already holds an older version of them.
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
        self.archive_folder: str = '/var/lib/collector'
        self.keep_days: int = 30
        self.compress: bool = True
        super().__init__(from_json_data_text=from_json_data_text,
                         from_json_filename=from_json_filename,
                         stderr_file=stderr_file)

    def get_validation_plan(self, stderr_file: TextIO) -> ValidationPlan:
        """Return the one rule this configuration has.

        It is here so that there is a save this example can have refused,
        which is what shows that a refused save keeps nothing either, and it
        is one step rather than none because a plan with no steps refuses
        nothing at all: `config_as_json` checks the declared type of a member
        only where the application asks it to, so `keep_days` would otherwise
        accept the text `soon` and write it to the file. `not_allowed_type`
        is what keeps `true` out of it as well, since a `bool` is an `int` in
        Python; example 1 is where that is really taught.
        """
        _ = stderr_file
        return [MemberValidationStep(
            member_names=['keep_days'],
            validator=ValueTypeValidator(int, not_allowed_type=bool))]


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
    run_example(example_name='e12_backup_files', config=ArchiveConfig(),
                args=args, settings=FILE_SETTINGS)
    # This is the one example that hands over a `Settings` of its own, which
    # is what every application with an opinion about its files does. The
    # other examples take the same answers from the command line instead, so
    # that each of them can be tried without a program per answer.


# The usual guard, so that importing this module from a test runs nothing.
if __name__ == '__main__':
    # Running a file directly puts only that file's own folder on sys.path,
    # so the `example` package this file belongs to would not be importable.
    # Adding the folder above it makes both ways of using this file work:
    # `python3 examples/src/example/e12_backup_files.py` and
    # `from example import e12_backup_files` from a test.
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    main()
