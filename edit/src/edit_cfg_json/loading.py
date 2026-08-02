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
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from enum import Enum, auto
from io import StringIO
from pathlib import Path
from typing import NamedTuple, Optional
import inspect
import json
from config_as_json import Config, ConfigAutoChangeHook, ConfigBadJson, \
    PathOrStr

HOOK_NAME = 'auto_ch_hook'
"""Name of the constructor keyword that reports automatic changes."""

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


def _takes_hook(config_type: type[Config]) -> bool:
    """Return whether one configuration class takes the change hook.

    `Config.__init__` takes it, but a subclass has to declare it and hand it
    on, and the three keyword constructor that `config_as_json` documents
    does not. Only a class that names the keyword itself counts as taking
    it. A class that collects further keyword arguments could be forwarding
    them or refusing them, and offering the hook to it would turn a load
    that works into one that fails, for a report that is a nicety.

    Args:
        config_type: Class of the configuration that is being loaded.

    Returns:
        Whether the hook can be passed to this class.
    """
    parameters = inspect.signature(config_type).parameters
    return HOOK_NAME in parameters


def _defaults(config_type: type[Config], said: StringIO) -> Config:
    """Return one configuration object holding its declared defaults.

    The hook reaches a class that declares it and is dropped for a class
    that does not, which is what `config_as_json` leaves to the application
    to opt into. Nothing reads the hook yet; forwarding it is what a later
    step needs to explain the automatic changes of an old format file.

    Args:
        config_type: Class of the configuration that is being loaded.
        said: Stream that collects what the class says about itself.

    Returns:
        A configuration object holding only what the class declares.

    Raises:
        ConfigLoadError: The editor cannot construct this class.
    """
    hook = ConfigAutoChangeHook()
    try:
        if _takes_hook(config_type):
            return config_type(from_json_data_text=None,
                               from_json_filename=None, auto_ch_hook=hook,
                               stderr_file=said)
        return config_type(from_json_data_text=None, from_json_filename=None,
                           stderr_file=said)
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
             said: StringIO) -> Config:
    """Try once to build one configuration object from one file text.

    The stream is the caller's, because a key that does not match is
    reported to the caller and what was said about it is needed there.

    Args:
        config_type: Class of the configuration that is being loaded.
        text: The whole text of the input file.
        ok_to_use_defaults: Whether the declared defaults may fill in the
            keys the file does not hold.
        said: Stream that collects what the class says about the file.

    Returns:
        A configuration object holding the values of the file.

    Raises:
        KeyError: The keys of the file do not match the declared members.
        ConfigLoadError: The file cannot be opened for editing.
    """
    try:
        config = _defaults(config_type=config_type, said=said)
        config.parse_json(from_json_text=text, stderr_file=said,
                          ok_to_use_defaults=ok_to_use_defaults)
    except ConfigBadJson as error:
        raise ConfigLoadError(NOT_CONFIG,
                              _explained(said=said, error=error)) from error
    except (TypeError, ValueError) as error:
        raise ConfigLoadError(BAD_VALUES,
                              _explained(said=said, error=error)) from error
    return config


def _declared(config: Config) -> list[str]:
    """Return the names of the public members of one configuration object.

    This is the rule `config_as_json` itself uses to decide what a
    configuration object consists of: every attribute that is public and is
    not a method.

    Args:
        config: Configuration object to read the member names of.

    Returns:
        The name of every member of that object.
    """
    return [name for name in vars(config) if not name.startswith('_')
            and not callable(getattr(config, name))]


def _absent(config: Config, text: str) -> frozenset[str]:
    """Return the declared members that one file text does not hold.

    The names are read from the file text, because a load that was allowed
    to use the defaults cannot afterwards say which of its values came from
    the file. The text has already been read as configuration by the time
    this is asked, so it is JSON and it is an object.

    Args:
        config: Configuration object that was loaded from the text.
        text: The whole text of the input file.

    Returns:
        The names of the members the declared defaults supplied.
    """
    data = json.loads(text)
    assert isinstance(data, dict)
    return frozenset(name for name in _declared(config) if name not in data)


def _filled_report(config: Config, text: str, said: str) -> LoadReport:
    """Return what a load that was allowed to use the defaults did.

    Args:
        config: Configuration object that the load built.
        text: The whole text of the input file.
        said: What the configuration class said about the file.

    Returns:
        The report of one permissive load.
    """
    filled = _absent(config=config, text=text)
    lines = [FILLED_MESSAGE if filled else '', said.strip()]
    return LoadReport(message='\n'.join(line for line in lines if line),
                      filled=filled)


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
    try:
        config = _attempt(config_type=config_type, text=text, said=said,
                          ok_to_use_defaults=True)
    except KeyError as error:
        raise ConfigLoadError(UNKNOWN_KEY,
                              _explained(said=said, error=error)) from error
    return LoadedConfig(config=config,
                        report=_filled_report(config=config, text=text,
                                              said=said.getvalue()))


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
    try:
        config = _attempt(config_type=config_type, text=text, said=said,
                          ok_to_use_defaults=False)
    except KeyError:
        return _rescue(config_type=config_type, text=text, policy=policy,
                       said=said.getvalue())
    return LoadedConfig(config=config,
                        report=LoadReport(message=said.getvalue().strip()))


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
                policy: LoadPolicy = DEFAULT_POLICY) -> LoadedConfig:
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
        in_file: File to read, or None to edit the declared defaults.
        policy: What to do about declared keys the file does not hold.

    Returns:
        The configuration object to edit, and what the load did to its
        values beyond reading them.

    Raises:
        ConfigLoadError: The file cannot be opened for editing.
    """
    if in_file is None:
        return LoadedConfig(config=config, report=LoadReport())
    return _load_text(config_type=type(config), policy=policy,
                      text=_file_text(in_file))
