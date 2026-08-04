#! /usr/bin/env python3
"""Writing the edited values to the output file.

Saving is validating and then writing, and it is refused whenever the
validation is. An editor that wrote a file the application would then refuse
to read would have failed at the one thing it exists for.

Where the application said how it loads its own configuration, that is asked
once more before anything is written, with the very text the file would hold.
It is the one thing a validation pass cannot answer: the pass applies the
buffer to the class that is being edited, and a loader that chooses its class
by looking at the JSON may read the same text back as another class
altogether. A value that would do that has to be caught here, because after
the file is written it is the application that meets it.

The file name is whatever the application asked for. This library has no
opinion about the extension: some applications use `.cfg`, some use `.json`,
and others use something else again.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from dataclasses import dataclass
from io import StringIO
from typing import NamedTuple, Optional
from config_as_json import Config, PathOrStr
from edit_cfg_json.loader import ConfigLoader, ask_loader

NO_DESTINATION = 'There is no file to save to yet. Save as chooses one.'
"""Message of a save that has nowhere to write to."""

NOT_VALID = 'These values are not valid, so they cannot be saved.'
"""Message of a save refused because the buffer is not a configuration."""

NOT_LOADABLE = ('These values cannot be saved: this application would not be '
                'able to read back the file that they would write.')
"""Message of a save whose file the application's own loader refuses."""

OTHER_CLASS = ('These values cannot be saved: this application would read the '
               'file that they would write as {other} and not as {own}.')
"""Message of a save whose file the loader would read as another class.

Which class a configuration is was settled when the file was opened, and the
session has been about that class ever since: its members are the rows, and
its docstring is the label. A value that would select another class is
therefore not something the editor can follow, and writing the file anyway
would leave the application with one it may not be able to read at all.
"""

RELOAD_ERRORS = (KeyError, TypeError, ValueError)
"""Every way the application's own loader can refuse what would be written.

They are the three ways `config_as_json` refuses anything, which is what a
loader built around it refuses with, and `ask_loader` turns a loader that ends
the process into the third of them. A refusal here is a file that is not
written, exactly like a refused validation, and never an exception the
application has to handle.
"""

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


@dataclass
class SaveState:
    """Where the editor writes, and what has come of writing there.

    The three belong together because each of them moves when the others do:
    choosing a destination drops what an earlier attempt said, and an
    attempt that wrote the file is the only thing there is a written object
    to hand back from.
    """

    out_file: Optional[PathOrStr] = None
    """File that saving writes, None while no destination has been chosen.

    There is none when the editor was started neither on an input file nor
    on an output file, which is what happens when an application offers to
    write its very first configuration file.
    """

    outcome: Optional[SaveOutcome] = None
    """What the last attempt to save did, None when there has been none."""

    written: Optional[Config] = None
    """The configuration object that reached the file, None when none has.

    It is never the caller's own object, which the editor does not modify
    and which would otherwise be stale.
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


def reload_refusal(loader: Optional[ConfigLoader], config: Config) -> str:
    """Return why the application would not read back what is to be written.

    An application that said nothing about how it loads is not asked anything,
    and neither is one whose loader reads back what the editor is showing: both
    of those are the ordinary case, and both answer with nothing at all.

    Args:
        loader: How this application constructs its configuration, or None
            when it did not say and there is nothing to ask.
        config: Validated configuration object that the save would write.

    Returns:
        What to tell the user instead of saving, empty when nothing stands in
        the way of writing the file.
    """
    if loader is None:
        return ''
    said = StringIO()
    try:
        text = config.as_json_string(stderr_file=said)
        reloaded = ask_loader(loader, stream=said, text=text)
    except RELOAD_ERRORS as error:
        told = said.getvalue().strip() or f'{type(error).__name__}: {error}'
        return f'{NOT_LOADABLE}\n{told}'
    if isinstance(reloaded, type(config)):
        return ''
    return OTHER_CLASS.format(other=type(reloaded).__name__,
                              own=type(config).__name__)


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
