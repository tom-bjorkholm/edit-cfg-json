#! /usr/bin/env python3
"""Example 1: editing a flat configuration.

This is the first example of the editor itself. The configuration class is
as small as a configuration class can be: one text member and one number
member, no validators, no nested structure. That is on purpose, because the
point of this example is not the configuration but the three lines it takes
to get an editor for it:

````python
config = FlatConfig()          # the application's own configuration object
model = EditModel(config)      # what the editor needs to know about it
TkEditor().run_editor(model)   # one of the user interface backends
````

Notice what the application does *not* do. It does not list its members for
the editor, it does not say which of them are text and which are numbers,
and it does not write a single widget. `EditModel` finds all of that by
looking at the configuration object it is handed. The configuration schema
is declared exactly once, in `FlatConfig.__init__`, where it belongs.

The members are shown in the order this class declares them, and the text
member is shown as the text it holds, without the quotation marks that JSON
puts around a string in the file. Both follow from the same idea: what the
editor shows is the configuration object the application declared, and how
that object is written to a file is an implementation detail of saving.

Both members can now be edited. Each of them is a field, and what the user
types goes into the edit buffer of the model as the value it stands for: the
text member keeps whatever is typed, and the number member holds a number as
soon as the text is one. Text that is not a number yet is kept as it was
typed, because a value that is being typed is not valid for most of the time
it takes to type it. Validation, which is what says so, arrives in the next
step.

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
editor observable without a display:

````sh
python3 examples/src/example/e01_flat_config.py --ui dump --set answer=7
````

Reading a file and saving arrive in the following steps, so this example
still starts from the default values and writes nothing.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from pathlib import Path
from typing import Optional, TextIO
import sys
from config_as_json import Config, PathOrStr, ValidationPlan


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
        editor construct the class itself in a later step, without the
        application having to hand over a loader function.

        Args:
            from_json_data_text: Optional JSON text to parse directly.
            from_json_filename: Optional path to a JSON file to read.
            stderr_file: Stream used for user-facing diagnostics.
        """
        # The members are assigned before super().__init__() is called.
        # These assignments are both the schema and the default values, and
        # they are the only description of the configuration that exists.
        self.name: str = 'flat example'
        self.answer: int = 42
        super().__init__(from_json_data_text=from_json_data_text,
                         from_json_filename=from_json_filename,
                         stderr_file=stderr_file)

    def get_validation_plan(self, stderr_file: TextIO) -> ValidationPlan:
        """Return no extra validation steps for this example.

        A later example adds validators, which is where the editor starts
        running them for the user. Here an empty plan keeps the example about
        the editor rather than about validation.
        """
        _ = stderr_file
        return []


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


# The usual guard, so that importing this module from a test runs nothing.
if __name__ == '__main__':
    # Running a file directly puts only that file's own folder on sys.path,
    # so the `example` package this file belongs to would not be importable.
    # Adding the folder above it makes both ways of using this file work:
    # `python3 examples/src/example/e01_flat_config.py` and
    # `from example import e01_flat_config` from a test.
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    main()
