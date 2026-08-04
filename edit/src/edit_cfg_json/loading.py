#! /usr/bin/env python3
"""Reading the configuration to edit from one input file.

The editor constructs the configuration object rather than receiving one that
is already loaded. Both of the things a load has to be told are given to a
constructor and to nothing else: the hook that reports the automatic changes
of an old format file, and the policy for declared keys the file does not
contain.

Three things can be wrong with an input file, and `config_as_json` reports
two of them as the same `KeyError`. Which of those two it is follows from
retrying the load with the declared defaults filling in what the file lacks:
that rescues a file which is merely incomplete, and it still refuses a key
the configuration does not declare. So the two are told apart by what the
retry does and never by reading the text of a message.

A file whose values a validator refuses cannot be opened either. That is not
squeamishness: a member validator returns the value that is stored back into
the member, so a load that stopped part way through leaves it unknown which
values were already rewritten and which were not.

A load that succeeded still has something to say when it did not leave the
file as it found it, which happens whenever the class has rules for reading an
older format, and whenever parsing or validating normalized a value. What
changed is found in `auto_change`; the words the user reads for it are here,
beside the words for everything else that one load has to report.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from collections.abc import Iterable
from enum import Enum, auto
from io import StringIO
from pathlib import Path
from typing import NamedTuple, Optional
from config_as_json import Config, ConfigBadJson, PathOrStr
from edit_cfg_json.auto_change import ChangeReport, FileChanges, file_changes
from edit_cfg_json.constructing import built_config
from edit_cfg_json.settings import Settings, SettingsSource, checked_file, \
    current_settings

DEFAULTS_ERRORS = (AttributeError, KeyError, TypeError, ValueError)
"""Every way in which constructing the declared defaults can fail.

A class that needs a constructor argument this library knows nothing about
raises `TypeError`, one that declares no public member raises
`AttributeError`, and defaults that a validator refuses raise a `ValueError`
subclass. `NotImplementedError` is deliberately not one of them, for the same
reason as in the validation of a buffer: it says the configuration class is
incomplete, which is a defect of the application that no file can put right.
"""

NO_FILE = 'File {name} cannot be read.'
"""Message of the refusal of a file that is missing or unreadable."""

NOT_TEXT = 'File {name} is not UTF-8 text.'
"""Message of the refusal of a file that is not text at all."""

NOT_CONFIG = 'This file does not hold configuration that can be read.'
"""Message of the refusal of a file the configuration class cannot read.

This covers text that is not JSON and JSON that cannot be turned into the
values of this configuration, which is what `ConfigBadJson` means. Which of
the two it was is in the diagnostics below the message.
"""

UNKNOWN_KEY = 'This file holds a key that this configuration does not have.'
"""Message of the refusal of a file with a key that is not declared."""

INCOMPLETE = ('This file does not hold every value, and a complete file '
              'is asked for.')
"""Message of the refusal of an incomplete file under a strict policy."""

BAD_VALUES = ('The values in this file are not valid, so it cannot be '
              'opened. Correct the file with a text editor first.')
"""Message of the refusal of a file whose values a validator refuses."""

NO_DEFAULTS = 'The editor cannot construct {name} on its own.'
"""Message of the refusal of a class the editor cannot construct."""

FILLED_MESSAGE = ('This file did not hold every value. What it left out was '
                  'filled in from the defaults, and is marked.')
"""Message that says a load used the declared defaults of the class."""

AUTO_CHANGED = ('Reading this file changed it, so what is shown is not what '
                'the file holds. What the load put there or altered is '
                'marked, and saving writes what is shown.')
"""Message that says the load itself changed the values of the file.

It is one message for all three of the ways that can happen, because the user
is being told one thing: the file on the disk and the values on the screen are
not the same, and it is the screen that a save writes.
"""

DROPPED_FORM = ('This file holds keys that this configuration does not use, '
                'and saving leaves them out: {names}')
"""Form of the line that names the keys of the file that are not used.

None of them is a member of this configuration, so none of them has a row that
could be marked, and this line is the only place they can be reported.
"""

OLD_FORMAT_FORM = ('This file is in an older format. It was read with these '
                   'older keys: {names}')
"""Form of the line that names the older keys that the load accepted.

It says what the line above it says and says why as well, so the two are never
both shown: a class that reported its own automatic changes has explained the
keys of its file, and the editor's own reading of them would only repeat it.
"""

SUPPLIED_FORM = ('These values were supplied because this file is in an older '
                 'format: {names}')
"""Form of the line naming what the rules for an older format supplied.

Neither the file nor the declared defaults gave these values. The
configuration class did, because the file is too old to hold them at all.
"""


class LoadPolicy(Enum):
    """Policy for declared keys that the input file does not contain."""

    STRICT = auto()
    """Refuse a file that does not hold every declared key."""

    DEFAULTS = auto()
    """Fill in what the file leaves out from the declared defaults."""

    STRICT_THEN_DEFAULTS = auto()
    """Load strictly, and on failure fill in and say that it was needed."""


DEFAULT_POLICY = LoadPolicy.STRICT_THEN_DEFAULTS
"""Policy used when the application names none of them.

Loading strictly and retrying with the defaults is the default because
whether a partly specified file is acceptable is an application decision,
and the answer that suits most applications is to open the file and say that
it was incomplete.
"""


class LoadReport(NamedTuple):
    """What one load of an input file did beyond reading the values."""

    message: str = ''
    """What the user has to be told about the load, empty when nothing.

    A load that read a complete file and had nothing remarked about it says
    nothing, so a backend that shows this shows nothing at all.
    """

    filled: frozenset[str] = frozenset()
    """Names of the members the declared defaults supplied.

    These are the members the input file did not hold. The model marks the
    row of each of them, so the user can see which values are not the ones
    the file asked for.
    """

    changed: frozenset[str] = frozenset()
    """Names of the members whose value the load itself put there or altered.

    Reading a file is not always only reading it: the rules a class declares
    for an older format may have supplied a value or renamed a key into a
    member, and parsing or validating may have normalized one. The model marks
    the row of each of these too, so that a value which is not the one in the
    file can be seen to be one. A member the declared defaults filled in is
    not here but in `filled`, which says the same thing more precisely.
    """


class LoadedConfig(NamedTuple):
    """The configuration object to edit, and what its load did."""

    config: Config
    """The object whose values are edited. Never the caller's own object,
    unless there was no input file to read."""

    report: LoadReport
    """What the load did to the values beyond reading them."""


class ConfigLoadError(Exception):
    """Refusal to open one input file for editing."""

    def __init__(self, message: str, diagnostics: str = '') -> None:
        """Say why the file cannot be opened, and what was said about it.

        Args:
            message: What the editor has to tell the user about this file.
            diagnostics: What the configuration class itself said about it.
        """
        self.message = message
        self.diagnostics = diagnostics.strip()
        parts = (message, self.diagnostics)
        super().__init__('\n'.join(part for part in parts if part))


def _defaults(config_type: type[Config], said: StringIO,
              hook: ChangeReport) -> Config:
    """Return one configuration object holding its declared defaults.

    The hook is offered whatever the class does with it, because
    `built_config` drops it for a class that does not declare it. What a class
    that takes it reports through it is what explains the automatic changes of
    a file in an older format.

    Args:
        config_type: Class of the configuration that is being loaded.
        said: Stream that collects what the class says about itself.
        hook: Hook that the class reports its automatic changes through.

    Returns:
        A configuration object holding only what the class declares.

    Raises:
        ConfigLoadError: The editor cannot construct this class.
    """
    try:
        return built_config(config_type, stream=said, hook=hook)
    except DEFAULTS_ERRORS as error:
        raise ConfigLoadError(NO_DEFAULTS.format(name=config_type.__name__),
                              _explained(said=said, error=error)) from error


def _explained(said: StringIO, error: Exception) -> str:
    """Return what a failed load has to say for itself.

    A failure that wrote nothing has only its exception left to report,
    which is better than no explanation at all.

    Args:
        said: Stream that collected what the configuration class said.
        error: The failure that the class reported.

    Returns:
        The diagnostics of one failure.
    """
    return said.getvalue() or f'{type(error).__name__}: {error}'


def _attempt(config_type: type[Config], text: str, ok_to_use_defaults: bool,
             said: StringIO, hook: ChangeReport) -> Config:
    """Try once to build one configuration object from one file text.

    The stream is the caller's, because a key that does not match is
    reported to the caller and what was said about it is needed there. The
    hook is the caller's for the same reason: what it collects is what the
    caller reports about the load that succeeded.

    Args:
        config_type: Class of the configuration that is being loaded.
        text: The whole text of the input file.
        ok_to_use_defaults: Whether the declared defaults may fill in the
            keys the file does not hold.
        said: Stream that collects what the class says about the file.
        hook: Hook that collects the automatic changes of this attempt.

    Returns:
        A configuration object holding the values of the file.

    Raises:
        KeyError: The keys of the file do not match the declared members.
        ConfigLoadError: The file cannot be opened for editing.
    """
    try:
        config = _defaults(config_type=config_type, said=said, hook=hook)
        config.parse_json(from_json_text=text, stderr_file=said,
                          ok_to_use_defaults=ok_to_use_defaults)
    except ConfigBadJson as error:
        raise ConfigLoadError(NOT_CONFIG,
                              _explained(said=said, error=error)) from error
    except (TypeError, ValueError) as error:
        raise ConfigLoadError(BAD_VALUES,
                              _explained(said=said, error=error)) from error
    return config


def _named(names: Iterable[str]) -> str:
    """Return several names as one piece of text, in a settled order.

    The order is the sorted one and not the one they were collected in,
    because a list of names that is read is easier to look something up in
    than one that records the order in which rules happened to run.

    Args:
        names: Names to write out.

    Returns:
        Those names, separated by commas.
    """
    return ', '.join(sorted(names))


def _change_lines(changes: FileChanges) -> list[str]:
    """Return what a load that changed its file has to say about that.

    Args:
        changes: What the load did to the file it read.

    Returns:
        The lines to tell the user, and nothing at all for a load that left
        the file as it found it.
    """
    if not changes.anything:
        return []
    lines = [AUTO_CHANGED]
    if changes.old_keys:
        lines.append(OLD_FORMAT_FORM.format(names=_named(changes.old_keys)))
    elif changes.dropped:
        lines.append(DROPPED_FORM.format(names=_named(changes.dropped)))
    if changes.supplied:
        lines.append(SUPPLIED_FORM.format(names=_named(changes.supplied)))
    return lines


def _report(config: Config, text: str, said: str, hook: ChangeReport,
            permissive: bool) -> LoadReport:
    """Return what one load did beyond reading the values of its file.

    The order of what is said follows the order in which it happened: what the
    file did not hold, then what reading it changed, and then whatever the
    configuration class itself said while it read.

    Args:
        config: Configuration object that the load built.
        text: The whole text of the input file.
        said: What the configuration class said about the file.
        hook: Hook that collected the automatic changes of this load.
        permissive: Whether the load was allowed to fill in what the file
            left out.

    Returns:
        The report of one load.
    """
    changes = file_changes(config=config, text=text, hook=hook,
                           permissive=permissive)
    lines = [FILLED_MESSAGE if changes.filled else ''] + \
        _change_lines(changes) + [said.strip()]
    return LoadReport(message='\n'.join(line for line in lines if line),
                      filled=changes.filled, changed=changes.changed)


def _permissive(config_type: type[Config], text: str) -> LoadedConfig:
    """Load one file text with the defaults filling in what it lacks.

    A key the configuration does not declare is still refused, because
    filling in governs the keys that are missing and nothing else. Dropping
    an unknown key would lose whatever the file meant by it, and such a file
    is either from a newer version or has a misspelled key in it.

    Args:
        config_type: Class of the configuration that is being loaded.
        text: The whole text of the input file.

    Returns:
        The configuration object, and what filling in did to its values.

    Raises:
        ConfigLoadError: The file cannot be opened for editing.
    """
    said = StringIO()
    hook = ChangeReport()
    try:
        config = _attempt(config_type=config_type, text=text, said=said,
                          ok_to_use_defaults=True, hook=hook)
    except KeyError as error:
        raise ConfigLoadError(UNKNOWN_KEY,
                              _explained(said=said, error=error)) from error
    return LoadedConfig(config=config,
                        report=_report(config=config, text=text, hook=hook,
                                       said=said.getvalue(), permissive=True))


def _rescue(config_type: type[Config], text: str, policy: LoadPolicy,
            said: str) -> LoadedConfig:
    """Retry a load that the keys of the file made fail.

    The retry is what tells the two failures apart that `check_key_match`
    reports as the same `KeyError`. A retry that succeeds says the file was
    incomplete, and a retry that fails again says the file holds a key that
    is not declared here. An incomplete file is opened under
    `STRICT_THEN_DEFAULTS` and refused under `STRICT`, which is the whole
    difference between those two policies.

    Args:
        config_type: Class of the configuration that is being loaded.
        text: The whole text of the input file.
        policy: What to do about declared keys the file does not hold.
        said: What the class said about the load that failed.

    Returns:
        The configuration object of the retry, and what the retry did.

    Raises:
        ConfigLoadError: The file cannot be opened for editing.
    """
    rescued = _permissive(config_type=config_type, text=text)
    if policy is LoadPolicy.STRICT:
        raise ConfigLoadError(INCOMPLETE, said)
    return rescued


def _load_text(config_type: type[Config], text: str,
               policy: LoadPolicy) -> LoadedConfig:
    """Load one file text under one policy, or refuse to open the file.

    Args:
        config_type: Class of the configuration that is being loaded.
        text: The whole text of the input file.
        policy: What to do about declared keys the file does not hold.

    Returns:
        The configuration object, and what the load did to its values.

    Raises:
        ConfigLoadError: The file cannot be opened for editing.
    """
    if policy is LoadPolicy.DEFAULTS:
        return _permissive(config_type=config_type, text=text)
    said = StringIO()
    hook = ChangeReport()
    try:
        config = _attempt(config_type=config_type, text=text, said=said,
                          ok_to_use_defaults=False, hook=hook)
    except KeyError:
        return _rescue(config_type=config_type, text=text, policy=policy,
                       said=said.getvalue())
    return LoadedConfig(config=config,
                        report=_report(config=config, text=text, hook=hook,
                                       permissive=False, said=said.getvalue()))


def default_config(config_type: type[Config]) -> Config:
    """Return one configuration object holding the declared defaults.

    This is the door for a caller that has a configuration class and needs
    the object that `edit` and `EditModel` take. A program that is told which
    class to edit is the case it exists for: the class is named on a command
    line, and the editor wants an instance of it.

    It is the same construction that reading an input file starts from, so a
    class the editor cannot construct is refused here in the same words and
    with the same diagnostics, and the hook that reports the automatic changes
    of an old format file reaches a class that declares it. Nothing reads that
    hook here, because there is no file to read and therefore nothing for it to
    report.

    Args:
        config_type: Class to construct with no JSON source, which leaves it
            holding only what it declares.

    Returns:
        A configuration object holding the declared defaults of that class.

    Raises:
        ConfigLoadError: The editor cannot construct this class.
    """
    return _defaults(config_type=config_type, said=StringIO(),
                     hook=ChangeReport())


def _file_text(in_file: PathOrStr) -> str:
    """Return the whole text of one input file, or refuse to open it.

    The file is read here and not by `Config.read()`, which ends the process
    with `sys.exit` when the file is missing. An editor has to say so and
    stay alive.

    Args:
        in_file: File to read.

    Returns:
        The whole text of that file.

    Raises:
        ConfigLoadError: The file cannot be read.
    """
    try:
        return Path(in_file).read_text(encoding='UTF-8')
    except OSError as error:
        raise ConfigLoadError(NO_FILE.format(name=in_file),
                              str(error)) from error
    except UnicodeDecodeError as error:
        raise ConfigLoadError(NOT_TEXT.format(name=in_file),
                              str(error)) from error


def load_config(config: Config, in_file: Optional[PathOrStr] = None,
                policy: LoadPolicy = DEFAULT_POLICY,
                settings: SettingsSource = Settings()) -> LoadedConfig:
    """Read the configuration to edit from one file, or use the defaults.

    The caller's object is the source of the class and of the declared
    defaults, and is not modified. Without an input file it is also the
    object to edit, so that a caller has one code path for both cases.

    What the load says is captured rather than printed, because an
    application that runs the editor has a screen and not a terminal behind
    it: what the load has to say belongs where the editor can show it, which
    is the report or the refusal.

    Args:
        config: Configuration object saying which class to load and what its
            declared defaults are. It is not modified.
        in_file: File to read, or None to edit the declared defaults. It is
            refused when the application enforces an extension that this
            name does not have; it is never completed with one, because it
            names a file that already exists and completing it would open a
            different file from the one that was asked for.
        policy: What to do about declared keys the file does not hold.
        settings: What the application around the editor has already
            decided, or a callable that answers with it. The default is an
            application with no opinion.

    Returns:
        The configuration object to edit, and what the load did to its
        values beyond reading them.

    Raises:
        ConfigLoadError: The file cannot be opened for editing.
    """
    if in_file is None:
        return LoadedConfig(config=config, report=LoadReport())
    checked = checked_file(name=in_file, settings=current_settings(settings))
    if checked.message:
        raise ConfigLoadError(checked.message)
    return _load_text(config_type=type(config), policy=policy,
                      text=_file_text(checked.name))
