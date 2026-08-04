#! /usr/bin/env python3
"""Constructing one configuration class the way its own signature allows.

The editor constructs the application's configuration class rather than
receiving an object of it, and it does so in four places: to read the declared
defaults, to read a file, to validate a buffer, and to say which member of a
refused buffer was refused. All four ask the same question — what do I call
this class with — so it is answered here once.

**The signature decides, not one documented shape.** More than one shape is in
use, and a class the editor refused over the name of a parameter would be
refused for no reason a reader of it could see. So every parameter this module
knows the meaning of is passed when the class declares it and left out when it
does not, which is principle 4 of section 3 of `doc/design.md` applied to a
constructor: what cannot be said is not said, and the editor is then only less
pleasant rather than unusable.

The one thing that cannot degrade quietly is the JSON text. A class with
nowhere to put it would be constructed on its declared defaults instead, and a
buffer validated against the defaults would be accepted whatever the user
typed. That is refused with a `TypeError`, which is what every caller here
already reports as a configuration it cannot build.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from collections.abc import Mapping
from typing import Any, Optional, TextIO
import inspect
from config_as_json import Config, ConfigAutoChangeHook

HOOK_NAME = 'auto_ch_hook'
"""Name of the constructor parameter that reports automatic changes."""

STREAM_NAME = 'stderr_file'
"""Name of the constructor parameter that takes the diagnostics stream."""

FILE_NAME = 'from_json_filename'
"""Name of the constructor parameter that names a file to read."""

JSON_TEXT_NAMES = ('from_json_data_text', 'from_json_text')
"""Every name a configuration class gives its JSON text parameter.

`Config.__init__` names it `from_json_data_text`, and the example
configuration classes that `config_as_json` ships name it `from_json_text` in
the constructors they declare, as does `ConfigFactory`. Both names are
therefore in use in practice, so both are looked for, in the order of the one
that `Config` itself documents first.
"""

NO_JSON_TEXT = ('Class {name} declares no parameter for JSON text, so the '
                'editor cannot construct it from the values it holds.')
"""Message of the refusal of a class that cannot be given a buffer."""


def _text_name(parameters: Mapping[str, inspect.Parameter],
               config_type: type[Config],
               text: Optional[str]) -> Optional[str]:
    """Return which parameter of one class takes the JSON text, if any.

    Args:
        parameters: The parameters of the constructor of that class.
        config_type: Class that is being constructed, named in the refusal.
        text: The JSON text that is to be given to it, or None when the
            declared defaults are what is wanted.

    Returns:
        The name to pass the text under, or None when the class declares none
        and none is needed.

    Raises:
        TypeError: There is a text to pass and the class takes none.
    """
    found = next((name for name in JSON_TEXT_NAMES if name in parameters),
                 None)
    if found is None and text is not None:
        raise TypeError(NO_JSON_TEXT.format(name=config_type.__name__))
    return found


def _arguments(config_type: type[Config], stream: TextIO, text: Optional[str],
               hook: Optional[ConfigAutoChangeHook]) -> dict[str, Any]:
    """Return what to call one configuration class with.

    The values are a stream, a hook, a JSON text and `None`, and which
    parameter each of them belongs to differs from class to class, so there is
    no one type that they share.

    Args:
        config_type: Class that is being constructed.
        stream: Stream that collects what the class says about itself.
        text: JSON text to construct it from, or None for the declared
            defaults. A file name is never passed, because the editor reads
            the file itself.
        hook: Hook that reports the automatic changes of an old format file,
            or None when the caller wants none.

    Returns:
        The keyword arguments for one construction of that class.

    Raises:
        TypeError: There is a text to pass and the class takes none.
    """
    parameters = inspect.signature(config_type).parameters
    arguments: dict[str, Any] = {}
    if STREAM_NAME in parameters:
        arguments[STREAM_NAME] = stream
    if FILE_NAME in parameters:
        arguments[FILE_NAME] = None
    text_name = _text_name(parameters=parameters, config_type=config_type,
                           text=text)
    if text_name is not None:
        arguments[text_name] = text
    if hook is not None and HOOK_NAME in parameters:
        arguments[HOOK_NAME] = hook
    return arguments


def built_config(config_type: type[Config], *, stream: TextIO,
                 text: Optional[str] = None,
                 hook: Optional[ConfigAutoChangeHook] = None) -> Config:
    """Construct one configuration class, from JSON text or from nothing.

    Constructing with no JSON text is what leaves a class holding its declared
    defaults, and constructing with text is the whole of what validating a
    buffer amounts to: the keys are matched, the dict shapes are checked
    against the defaults, the parse converters run, the nested configuration
    objects are built, and the validation plan is applied.

    Args:
        config_type: Class to construct.
        stream: Stream that collects what the class says about itself. It is
            passed only to a class that declares it; one that does not writes
            wherever it writes, which is less pleasant and not a refusal.
        text: JSON text to construct the object from, or None to leave it
            holding the values the class declares.
        hook: Hook that reports the automatic changes of an old format file.
            It reaches a class that declares the parameter and is dropped for
            one that does not, which is what `config_as_json` leaves to the
            application to opt into: a class that collects further keyword
            arguments could be forwarding them or refusing them, and offering
            the hook to it would turn a load that works into one that fails,
            for a report that is a nicety.

    Returns:
        A configuration object of that class.

    Raises:
        TypeError: The class cannot be constructed this way. A class whose
            constructor needs an argument this library knows nothing about,
            and a class with nowhere to put the JSON text, are both this.
        KeyError: The keys of the text do not match the declared members.
        ValueError: A value of the text is one the class refuses. Every
            refusal of `config_as_json` is a subclass of this.
        AttributeError: The class declares no public member at all.
    """
    return config_type(**_arguments(config_type=config_type, stream=stream,
                                    text=text, hook=hook))
