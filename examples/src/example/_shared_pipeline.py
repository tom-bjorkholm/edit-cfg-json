#! /usr/bin/env python3
"""The configuration that the four embedding examples all edit.

Examples 13 to 16 are about *where* the editor is: in an area of a window, in
a window of its own, in an area of a Textual screen, or on a screen of its
own. What they edit is beside the point, so they share this one small class
rather than each writing a configuration of its own. Examples 8 to 11 are
where the shapes a real configuration has are taught, and every one of them
works in an embedded editor unchanged.

The command line is shared for the same reason, and it is two options rather
than the three every other example has: `--policy` says what to do about
values a file leaves out, which is example 1's subject and not this one's.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from typing import NamedTuple, Optional, TextIO
import argparse
import sys
from config_as_json import Config, IntFloatValidator, \
    MemberValidationStep, PathOrStr, ValidationPlan
from edit_cfg_json import Descriptions

EDIT_TEXT = 'Edit the configuration'
"""Text of the button with which each example opens the editor."""

CLOSE_TEXT = 'Close the editor'
"""Text of the button an application closes the editor with."""

SESSION_SAVED = 'The session saved a {name} object.'
"""What an example that mounts the editor says about what was written."""

SESSION_NOTHING = 'The session saved nothing.'
"""What it says when the session ended without writing anything."""

DESCRIPTIONS: Descriptions = {
    ('name',): 'What this pipeline is called in the logs.',
    ('workers',): 'How many jobs run at the same time.'}
"""What the application says about the members it declares."""

MOST_WORKERS = 64
"""The largest number of jobs this application will run at the same time."""


class PipelineConfig(Config):
    """How this application runs its pipeline.

    Two ordinary values and one rule, so that the Validate button of an
    embedded editor has something to accept and something to refuse.
    """

    # A configuration class of an example is written out in full, because a
    # reader of one example should not have to read another one first. That
    # makes its shape the same as every other example's, which is what this
    # says is deliberate.
    # pylint: disable=duplicate-code

    def __init__(self, from_json_data_text: Optional[str] = None,
                 from_json_filename: Optional[PathOrStr] = None,
                 stderr_file: TextIO = sys.stderr) -> None:
        """Initialize the configuration with its default values.

        Args:
            from_json_data_text: Optional JSON text to parse directly.
            from_json_filename: Optional path to a JSON file to read.
            stderr_file: Stream used for user-facing diagnostics.
        """
        self.name: str = 'nightly'
        self.workers: int = 4
        super().__init__(from_json_data_text=from_json_data_text,
                         from_json_filename=from_json_filename,
                         stderr_file=stderr_file)

    def get_validation_plan(self, stderr_file: TextIO) -> ValidationPlan:
        """Return the one rule this configuration has.

        Args:
            stderr_file: Stream used for user-facing diagnostics.

        Returns:
            A plan refusing an impossible number of workers. Example 4 is
            where the rules of an application are really taught.
        """
        _ = stderr_file
        return [MemberValidationStep(
            member_names=['workers'],
            validator=IntFloatValidator[int](min_value=1,
                                             max_value=MOST_WORKERS,
                                             allowed_values=None))]


class EditorFiles(NamedTuple):
    """What one run of an embedding example was told about files."""

    in_file: Optional[str]
    """File the editor reads, or None for the declared defaults."""

    out_file: Optional[str]
    """File the editor writes, or None for the input file."""


def editor_files(name: str, args: Optional[list[str]]) -> EditorFiles:
    """Return the file options that one run of an example was given.

    Args:
        name: Name of the example, used in help and error text.
        args: Command line of the run, or None for `sys.argv[1:]`.

    Returns:
        What to pass on to the editor about files.
    """
    parser = argparse.ArgumentParser(prog=name)
    parser.add_argument('-i', '--input', default=None,
                        help='Configuration file to read.')
    parser.add_argument('-o', '--output', default=None,
                        help='Configuration file to write, or the input file.')
    parsed = parser.parse_args(args)
    return EditorFiles(in_file=parsed.input, out_file=parsed.output)


def session_result(saved: Optional[Config]) -> str:
    """Return what one embedded editing session gave back, as a line.

    An editor mounted in a window an application owns has no moment at which
    it could return anything, so the application reads `saved_config` of the
    panel or the screen it mounted.

    Args:
        saved: What that panel or screen holds as its saved object.

    Returns:
        A line naming the saved configuration class, or saying there is none.
    """
    if saved is None:
        return SESSION_NOTHING
    return SESSION_SAVED.format(name=type(saved).__name__)
