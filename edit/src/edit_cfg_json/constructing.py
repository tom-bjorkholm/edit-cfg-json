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

**The text of an input file is given to a constructor that takes the load
policy**, which is a constructor declaring both a JSON text parameter and
`ok_to_use_defaults`. Its class then validates once, on the values of the file:
the declared values are never validated on their own, which saves a pass that
may be costly and lets a class whose declared values are not valid on their own
read a file. Any other class is constructed holding its declared values first,
and the text is applied to it with `Config.parse_json`, which is where the load
policy can always be given. That is the rule `config_as_json` follows for the
nested objects it constructs.

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

MEMBER_NAME = 'member_name'
"""Name of the constructor parameter that says where the object is.

It is the path for reaching a nested configuration object from the top level
one, and nothing is ever passed under it but `None`: what is constructed here
is the whole configuration and is a member of nothing. It is passed all the
same, because a class that declares the parameter without a default of its
own has to be given one.
"""

JSON_TEXT_NAMES = ('from_json_data_text', 'from_json_text')
"""Every name a configuration class gives its JSON text parameter.

`Config.__init__` names it `from_json_data_text`, and the example
configuration classes that `config_as_json` ships name it `from_json_text` in
the constructors they declare, as does `ConfigFactory`. Both names are
therefore in use in practice, so both are looked for. The text of an input file
is passed under it only together with the load policy, and `None` is passed
otherwise: a class that declares the parameter without a default of its own has
to be given one, and a class that declares none is constructed without it.
"""

DEFAULTS_NAME = 'ok_to_use_defaults'
"""Name of the constructor parameter that takes the load policy.

`Config.__init__` declares it, and so does a class that passes it on to
`Config.__init__` as `config_as_json` recommends. A class that declares it can
be given the text of an input file, because it can then be told the policy that
the text is to be read with.
"""


def _parameters(factory: Callable[..., Config]
                ) -> Mapping[str, inspect.Parameter]:
    """Return the parameters that one configuration class declares.

    Args:
        factory: Class, or callable with its own arguments already bound,
            that constructs the configuration.

    Returns:
        The parameters of its constructor, by name.
    """
    return inspect.signature(factory).parameters


def _text_name(parameters: Mapping[str, inspect.Parameter]) -> Optional[str]:
    """Return the name a constructor gives its JSON text, None for no name.

    Args:
        parameters: The parameters of the constructor, by name.

    Returns:
        The first name of `JSON_TEXT_NAMES` that the constructor declares.
    """
    return next((name for name in JSON_TEXT_NAMES if name in parameters), None)


def _arguments(parameters: Mapping[str, inspect.Parameter],
               stream: TextIO) -> dict[str, object]:
    """Return what to call one configuration class with for its defaults.

    The values are a stream and `None`, and which parameter each of them
    belongs to differs from class to class, so there is no one type that they
    share.

    Args:
        parameters: The parameters of the constructor, by name.
        stream: Stream that collects what the class says about itself.

    Returns:
        The keyword arguments for one construction of that class.
    """
    arguments: dict[str, object] = {}
    if STREAM_NAME in parameters:
        arguments[STREAM_NAME] = stream
    if FILE_NAME in parameters:
        arguments[FILE_NAME] = None
    if MEMBER_NAME in parameters:
        arguments[MEMBER_NAME] = None
    text_name = _text_name(parameters)
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
    return factory(**_arguments(parameters=_parameters(factory),
                                stream=stream))


def read_config(factory: Callable[..., Config], text: str, *, stream: TextIO,
                ok_to_use_defaults: bool) -> Config:
    """Construct one configuration holding the values of one JSON text.

    A constructor that declares a JSON text parameter and `ok_to_use_defaults`
    is given both, so the class validates once, and only the values of the
    text. Any other class is constructed holding its declared values, which
    are validated on their own, and the text is then applied to it with
    `Config.parse_json`. A constructor that accepts the policy only through
    `**kwargs` is one of the latter, because the signature does not say that
    it passes the policy on.

    Args:
        factory: Class to construct, or a callable that constructs it with
            arguments of its own already bound.
        text: JSON text holding the values of an input file.
        stream: Stream that collects what the class says about the text.
        ok_to_use_defaults: Whether the declared defaults may fill in what the
            text does not hold.

    Returns:
        A configuration object holding the values of the text.

    Raises:
        KeyError: The keys of the text do not match the declared members.
        TypeError: The class cannot be constructed this way.
        ValueError: The values are ones the class refuses.
        AttributeError: The class declares no public member at all.
    """
    parameters = _parameters(factory)
    text_name = _text_name(parameters)
    if text_name is None or DEFAULTS_NAME not in parameters:
        config = built_config(factory, stream=stream)
        config.parse_json(from_json_text=text, stderr_file=stream,
                          ok_to_use_defaults=ok_to_use_defaults)
        return config
    return factory(**_arguments(parameters=parameters, stream=stream)
                   | {text_name: text, DEFAULTS_NAME: ok_to_use_defaults})


# One argument per independent thing about the parse: the object, the text,
# where the diagnostics go, the one method to stand in for, and where the
# object is. Every one after the text is a keyword.
# pylint: disable-next=too-many-arguments
def parsed_config(config: Config, text: str, *, stream: TextIO,
                  replace: str = '',
                  method: Optional[Callable[..., object]] = None,
                  member_name: Optional[str] = None) -> Config:
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
    afterwards. Replacing it on the object leaves the class of the application
    untouched, and `parse_json` does not mistake the replacement for a member,
    because it counts only the attributes that are not callable.

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
        member_name: Path for reaching this object from the top level
            configuration, so that what the class says about a value names
            the whole path to it. None for the whole configuration, which is
            a member of nothing.

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
    parsed.parse_json(from_json_text=text, stderr_file=stream,
                      member_name=member_name)
    return parsed
