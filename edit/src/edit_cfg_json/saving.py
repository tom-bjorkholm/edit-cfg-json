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

A file that is about to be overwritten is kept first, under the name the
application chose for it, so that a session which writes over a configuration
somebody else wrote does not take it away from them. It is kept once per
destination per session: the file that a user is overwriting is their own
earlier save from the second press of Save onwards, and a backup of every
press would be a backup of nothing.

The file name is whatever the application asked for. This library has no
opinion about the extension: some applications use `.cfg`, some use `.json`,
and others use something else again.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from dataclasses import dataclass, field
from io import StringIO
from pathlib import Path
from typing import NamedTuple, Optional
from config_as_json import Config, PathOrStr
from edit_cfg_json.loader import ConfigLoader, ask_loader
from edit_cfg_json.settings import Settings

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

BACKUP_FAILED = 'What {name} holds now cannot be kept as {backup}.'
"""Message of a save that could not keep what the destination held.

Such a save writes nothing. The whole reason for keeping the previous content
is that overwriting it cannot be undone, so a save that has just found it
cannot keep it is the last moment at which anything can be done about that.
"""

SAVED = 'Saved to {name}.'
"""Message of a save that wrote the output file."""

KEPT_FORM = '\nThe previous content is in {name}.'
"""What is added to the message of a save that kept what the file held.

It is said on the way out as well as on the way in: a save that kept the
previous content and then could not write the file has left it under another
name, and a user who was not told would look for it where it no longer is.
"""

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

    written_files: set[Path] = field(default_factory=set)
    """Every destination that this session has already written.

    What a save keeps and what it asks about is what the file held before this
    session reached it, so a destination that is in here is written straight
    over: what would be kept is the user's own earlier save, and what would be
    asked about is a file the user made a minute ago.
    """


class KeptFile(NamedTuple):
    """What keeping what one destination holds now did."""

    name: Optional[Path]
    """Where the previous content went, None when there was none to keep."""

    message: str
    """Why it could not be kept, empty when there was nothing in the way."""


NOTHING_KEPT = KeptFile(name=None, message='')
"""The answer of a save that had nothing to keep, or was not to keep it."""


def _because(message: str, error: Exception) -> str:
    """Return one refusal of a save, with what the failure itself said.

    Args:
        message: What the editor has to say about the file.
        error: The failure that reading, renaming or writing it reported.

    Returns:
        The message of one refused save.
    """
    return f'{message}\n{type(error).__name__}: {error}'


def _numbered(name: PathOrStr, suffix: str, count: int, number: int) -> Path:
    """Return one of the names that a destination is kept under.

    Args:
        name: Destination whose previous content is kept.
        suffix: What the application adds to the name of a kept file.
        count: How many of them the application keeps.
        number: Which of them, 1 being the one that was kept last.

    Returns:
        The name of that kept file, which carries no number at all where
        only one of them is kept.
    """
    kept = f'{name}{suffix}'
    return Path(kept if count == 1 else f'{kept}_{number}')


def kept_file(name: PathOrStr, settings: Settings) -> Optional[Path]:
    """Return where what one destination holds now would be kept.

    Args:
        name: File that a save is about to write.
        settings: What the application has decided about its files.

    Returns:
        The file that the previous content would be kept as, and None where
        there would be none: an application that keeps no backup, and a
        destination that holds no file to keep. A destination that is not a
        file at all, a folder being the case that arises, is left to the
        write to refuse in its own words.
    """
    suffix = settings.backup_suffix
    if suffix is None or not Path(name).is_file():
        return None
    return _numbered(name=name, suffix=suffix, count=settings.backup_count,
                     number=1)


def _rotate(name: PathOrStr, suffix: str, count: int) -> None:
    """Move every kept file one number further back, dropping the oldest.

    The oldest is dropped by being replaced, which is what renaming the one
    before it onto it does. An application that keeps one file numbers none of
    them, so there is then nothing here to move.

    Args:
        name: Destination whose previous content is about to be kept.
        suffix: What the application adds to the name of a kept file.
        count: How many of them the application keeps.
    """
    for number in range(count, 1, -1):
        younger = _numbered(name=name, suffix=suffix, count=count,
                            number=number - 1)
        if younger.is_file():
            younger.replace(_numbered(name=name, suffix=suffix, count=count,
                                      number=number))


def keep_previous(name: PathOrStr, settings: Settings) -> KeptFile:
    """Move what one destination holds now out of the way of a save.

    By renaming and not by copying, so that what is kept is the file that was
    there rather than a second reading of it, and so that a failure leaves the
    previous content whole under one name or the other. A kept file of the
    same name is replaced, which is how the oldest of several falls off the
    end.

    Whether a destination is to be kept at all is the caller's question, and
    the model answers it: a file this session has already written is the
    user's own earlier save.

    Args:
        name: File that a save is about to write.
        settings: What the application has decided about its files.

    Returns:
        Where the previous content went, or why it could not be kept.
    """
    kept = kept_file(name=name, settings=settings)
    if kept is None:
        return NOTHING_KEPT
    suffix = settings.backup_suffix
    assert suffix is not None
    try:
        _rotate(name=name, suffix=suffix, count=settings.backup_count)
        Path(name).replace(kept)
    except OSError as error:
        return KeptFile(name=None, message=_because(
            BACKUP_FAILED.format(name=name, backup=kept), error))
    return KeptFile(name=kept, message='')


def _kept_text(kept: Optional[PathOrStr]) -> str:
    """Return what says where the previous content of the file went.

    Args:
        kept: File it was kept as, or None when there was none to keep.

    Returns:
        The line that says so, and nothing at all when nothing was kept.
    """
    return '' if kept is None else KEPT_FORM.format(name=kept)


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


def write_config(config: Config, out_file: PathOrStr,
                 kept: Optional[PathOrStr] = None) -> SaveOutcome:
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
        kept: File that what this destination held was kept as, or None when
            there was nothing to keep. It is said whether the write succeeds
            or fails, because a user whose file has been moved has to be told
            where it went either way.

    Returns:
        Whether the file was written, and what to tell the user about it.
    """
    said = StringIO()
    try:
        config.write(to_json_filename=out_file, stderr_file=said)
    except WRITE_ERRORS as error:
        return SaveOutcome(
            saved=False,
            message=_because(WRITE_FAILED.format(name=out_file), error)
            + _kept_text(kept))
    return SaveOutcome(saved=True,
                       message=SAVED.format(name=out_file) + _kept_text(kept))
