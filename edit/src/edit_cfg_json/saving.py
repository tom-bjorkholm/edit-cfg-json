#! /usr/bin/env python3
"""Writing the edited values to the output file.

Saving is validating and then writing, and it is refused whenever the
validation is. An editor that wrote a file the application would then refuse
to read would have failed at the one thing it exists for.

The file name is whatever the application asked for. This library has no
opinion about the extension: some applications use `.cfg`, some use `.json`,
and others use something else again.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from io import StringIO
from typing import NamedTuple
from config_as_json import Config, PathOrStr

NO_DESTINATION = 'There is no file to save to yet. Save as chooses one.'
"""Message of a save that has nowhere to write to."""

NOT_VALID = 'These values are not valid, so they cannot be saved.'
"""Message of a save refused because the buffer is not a configuration."""

WRITE_FAILED = 'File {name} cannot be written.'
"""Message of a save whose destination could not be written."""

SAVED = 'Saved to {name}.'
"""Message of a save that wrote the output file."""

WRITE_ERRORS = (OSError, KeyError, TypeError, ValueError)
"""Every way in which writing the output file can fail.

`OSError` is the file itself: a folder that does not exist, a name that
cannot be used, a file that may not be written to. The other three are how
`config_as_json` refuses a configuration, and `Config.write()` validates the
object again before it writes anything. The object written here has just been
validated, so those three can only mean a validator that does not give the
same answer twice. That is a defect of the application rather than of the
values, but the editor still reports it as a file it could not write, because
falling over would cost the user the whole session.
"""


class SaveOutcome(NamedTuple):
    """What one attempt to save the edited values did."""

    saved: bool
    """Whether the output file was written."""

    message: str
    """What the user has to be told about this attempt.

    There is always something to say, because a save is something the user
    asked for and an answer is the least it owes them.
    """


def _failed(name: PathOrStr, error: Exception) -> str:
    """Return what a save that could not write the file has to say.

    Args:
        name: File that the save was trying to write.
        error: The failure that writing it reported.

    Returns:
        The message of one refused save.
    """
    return f'{WRITE_FAILED.format(name=name)}\n{type(error).__name__}: {error}'


def write_config(config: Config, out_file: PathOrStr) -> SaveOutcome:
    """Write one validated configuration object to one file.

    `Config.write()` serializes before it opens the destination, and
    serializing validates, so a configuration it refuses leaves the file on
    disk exactly as it was. The editor validates first anyway, which makes
    this the second of two gates rather than the only one.

    What the write says about the configuration is captured rather than
    printed, for the same reason as everywhere else here: these diagnostics
    belong on the screen the editor owns and not in the terminal behind it.
    They are the diagnostics of the validation pass that has just run, so the
    verdict is already showing them and this copy is dropped.

    Args:
        config: Configuration object to write. It has been validated.
        out_file: File to write it to, with whatever extension the
            application chose.

    Returns:
        Whether the file was written, and what to tell the user about it.
    """
    said = StringIO()
    try:
        config.write(to_json_filename=out_file, stderr_file=said)
    except WRITE_ERRORS as error:
        return SaveOutcome(saved=False, message=_failed(name=out_file,
                                                        error=error))
    return SaveOutcome(saved=True, message=SAVED.format(name=out_file))
