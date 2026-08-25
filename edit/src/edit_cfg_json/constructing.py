#! /usr/bin/env python3
"""Building the configuration objects that the editor works with.

There are two of them, and only one of them asks the class for anything.

**An object that did not exist before.** The declared defaults and the values
of an input file both need one, and only the class can make one. More than one
constructor shape is in use, so every parameter this module knows the meaning
of is passed when the class declares it and left out when it does not, which is
principle 4 of section 3 of `doc/detailed_design.md` applied to a constructor:
what cannot be said is not said, and the editor is then only less pleasant
rather than unusable.

**An object holding the edit buffer.** Validating the buffer, and saying which
member of a refused buffer was refused, both need an object holding the values
that are on the screen. There the class is not asked at all: the object the
editor already has is copied, and `Config.parse_json` applies the buffer to the
copy. That runs the whole chain the class runs while it reads a file — the keys
are matched, the dict shapes are checked against the defaults, the parse
converters run, the nested configuration objects are built and the validation
plan is applied — and it needs nothing whatever of the constructor. So a class
that needs an argument this library knows nothing about is edited, validated
and saved exactly as well as any other, and only reading a file needs the
loader that the application supplies for it.

**The JSON text is therefore never given to a constructor**, which is what
makes that true. It would gain nothing if it were: `Config.__init__` passes the
text straight to `parse_json` itself, and the one thing that has to go with it
is the load policy, which `__init__` does not take.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from collections.abc import Callable, Mapping
from copy import deepcopy
from typing import Optional, TextIO
import inspect
from config_as_json import Config

STREAM_NAME = 'stderr_file'
"""Name of the constructor parameter that takes the diagnostics stream."""

FILE_NAME = 'from_json_filename'
"""Name of the constructor parameter that names a file to read."""

JSON_TEXT_NAMES = ('from_json_data_text', 'from_json_text')
"""Every name a configuration class gives its JSON text parameter.

`Config.__init__` names it `from_json_data_text`, and the example
configuration classes that `config_as_json` ships name it `from_json_text` in
the constructors they declare, as does `ConfigFactory`. Both names are
therefore in use in practice, so both are looked for. Nothing is ever passed
under either of them but `None`: a class that declares the parameter without a
default of its own has to be given one, and a class that declares none is
constructed without it.
"""


def _arguments(factory: Callable[..., Config],
               stream: TextIO) -> dict[str, object]:
    """Return what to call one configuration class with.

    The values are a stream and `None`, and which parameter each of them
    belongs to differs from class to class, so there is no one type that they
    share.

    Args:
        factory: Class, or callable with its own arguments already bound,
            that constructs the configuration.
        stream: Stream that collects what the class says about itself.

    Returns:
        The keyword arguments for one construction of that class.
    """
    parameters: Mapping[str, inspect.Parameter] = \
        inspect.signature(factory).parameters
    arguments: dict[str, object] = {}
    if STREAM_NAME in parameters:
        arguments[STREAM_NAME] = stream
    if FILE_NAME in parameters:
        arguments[FILE_NAME] = None
    text_name = next((name for name in JSON_TEXT_NAMES if name in parameters),
                     None)
    if text_name is not None:
        arguments[text_name] = None
    return arguments


def built_config(factory: Callable[..., Config], *, stream: TextIO) -> Config:
    """Construct one configuration holding the values that its class declares.

    Nothing is passed for the automatic changes of an old format file, and
    nothing needs to be: `Config` gives every configuration object a hook of
    its own where the application named none, and `Config.auto_change_hook`
    is where the load that used it is read afterwards. A class that declares
    the parameter is constructed exactly like one that does not.

    Args:
        factory: Class to construct, or a callable that constructs it with
            arguments of its own already bound. A signature is all this needs,
            and `functools.partial` over a class has one.
        stream: Stream that collects what the class says about itself. It is
            passed only to a class that declares it; one that does not writes
            wherever it writes, which is less pleasant and not a refusal.

    Returns:
        A configuration object holding only what the class declares.

    Raises:
        TypeError: The class cannot be constructed this way, which a class
            whose constructor needs an argument this library knows nothing
            about is.
        ValueError: The declared values are ones the class refuses. Every
            refusal of `config_as_json` is a subclass of this.
        AttributeError: The class declares no public member at all.
    """
    return factory(**_arguments(factory=factory, stream=stream))


def parsed_config(config: Config, text: str, *, stream: TextIO,
                  replace: str = '',
                  method: Optional[Callable[..., object]] = None) -> Config:
    """Return a copy of one configuration object holding one JSON text.

    This is how an edit buffer becomes a configuration object. The copy is what
    keeps the editor from ever modifying the object it was given, and
    `parse_json` is what applies the buffer, with everything the configuration
    class does while it reads a file. The hook that records the automatic
    changes of a parse is copied with the object, so what the load of the input
    file recorded stays as the load left it however often a buffer is parsed.

    One method of the copy can be replaced, on the object and not on the class,
    which is how the editor reaches a state that the class does not offer: a
    parse that validates nothing, so that the plan can be walked step by step
    afterwards, and a parse that stops at the key check, so that what the
    declared defaults filled in can be read off it. Replacing it on the object
    leaves the class of the application untouched, and `parse_json` does not
    mistake the replacement for a member, because it counts only the attributes
    that are not callable.

    Args:
        config: Configuration object whose class and copy are used. It is not
            modified.
        text: JSON text holding one value per member, which is the edit buffer
            or the text of an input file.
        stream: Stream that collects what the class says about the text.
        replace: Name of the method to replace on the copy, empty for none.
        method: What to replace that method with, None to replace nothing. It
            is called as the method is called and without the object, because
            an attribute of the object is not a bound method.

    Returns:
        A copy of that configuration object holding the values of the text.

    Raises:
        KeyError: The keys of the text do not match the declared members.
        TypeError: A value of the text is of a type the class refuses.
        ValueError: A value of the text is one the class refuses. Every
            refusal of `config_as_json` is a subclass of this, and text that
            is not JSON at all raises `ConfigBadJson`, which is one of them.
    """
    parsed = deepcopy(config)
    if method is not None:
        setattr(parsed, replace, method)
    parsed.parse_json(from_json_text=text, stderr_file=stream)
    return parsed
