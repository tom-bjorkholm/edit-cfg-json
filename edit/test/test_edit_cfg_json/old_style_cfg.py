#! /usr/bin/env python3
"""A configuration whose validation step was written before paths existed.

`config_as_json` added `member_name` to `ValidationStep.apply` after
applications had been written against the version without it, and it calls
such a step without the argument while warning that it should be changed.
The editor applies the very steps of the application's own plan, so it has to
call one the same way. A step called with an argument it does not take raises
`TypeError`, and the editor reports a raise from a step as a refused buffer,
so the user would be told that these values are no configuration when there
is nothing wrong with them at all.

The step here therefore has the old signature on purpose. It does not derive
from `ValidationStep`, because a subclass whose signature disagrees with its
base is a defect wherever it is not this, and it is `cast` into one where the
plan asks for a step. That cast is the one thing this module is for.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from typing import Optional, TextIO, cast
import sys
from config_as_json import Config, InvalidConfiguration, PathOrStr, \
    ValidationPlan, ValidationStep

OLD_STYLE_MESSAGE = 'The two numbers are not the same, and have to be.'
"""What the old style step says when it refuses a configuration."""


class _OldStyleStep:  # pylint: disable=too-few-public-methods
    """One validation step of an application written before paths existed."""

    def apply(self, config: Config, stderr_file: TextIO = sys.stderr) -> None:
        """Refuse a configuration whose two numbers differ.

        It is about both members and therefore about neither, which is what
        makes it a step of its own rather than a member validator.

        Args:
            config: The configuration object that this rule is about.
            stderr_file: Stream that the refusal is written to before it is
                raised.

        Raises:
            InvalidConfiguration: The two numbers differ.
        """
        if getattr(config, 'first', 0) != getattr(config, 'second', 0):
            print(OLD_STYLE_MESSAGE, file=stderr_file)
            raise InvalidConfiguration(OLD_STYLE_MESSAGE)


class OldStyleCfg(Config):
    """A configuration with one rule of the shape an old application wrote."""

    def __init__(self, from_json_data_text: Optional[str] = None,
                 from_json_filename: Optional[PathOrStr] = None,
                 stderr_file: TextIO = sys.stderr,
                 member_name: Optional[str] = None) -> None:
        """Declare the two numbers and then apply the JSON."""
        self.first: int = 1
        self.second: int = 1
        super().__init__(from_json_data_text=from_json_data_text,
                         from_json_filename=from_json_filename,
                         stderr_file=stderr_file, member_name=member_name)

    def get_validation_plan(self, stderr_file: TextIO) -> ValidationPlan:
        """Return the one step, which takes no path."""
        _ = stderr_file
        return [cast(ValidationStep, _OldStyleStep())]
