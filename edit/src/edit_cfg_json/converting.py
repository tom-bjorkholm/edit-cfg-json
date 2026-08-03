#! /usr/bin/env python3
"""What the configuration makes of the text of one leaf of the buffer.

The buffer holds JSON space values, and some members do not hold a JSON space
value at all once the configuration class has them: `parse_converters()` says
which of them become a richer Python type and how. An enum is the case that
arises in practice, and it is what makes this worth having. A name that is no
member of an enum cannot be turned into one, and `config_as_json` reports that
inside the message it prints for JSON it could not load — which is right for a
program reading a file and wrong for a person editing a field, who was not
asking about JSON at all.

The converter that the class declared is *run* rather than looked at, exactly
as `config_as_json` runs it while it parses. That is the same rule that
validation follows and for the same reason: an application may declare any
converter it likes, and running the real one is right for every converter that
exists or ever will.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from typing import NamedTuple, Optional
from config_as_json import Config, JsonType, ParseConverter

CONVERSION_ERRORS = (AssertionError, AttributeError, KeyError, TypeError,
                     ValueError)
"""Every way in which a parse converter can refuse one value.

`config_as_json` catches every exception around the parsing it does, so a
converter is not promised to fail in any particular way, and these are the
ways in which the converters it ships do fail: a name that is no member of an
enum raises `KeyError`, and a value that is not text at all trips the
assertion that the enum converter begins with.

`NotImplementedError` is deliberately not one of them, exactly as it is not
one of the failures a validation pass catches: it says that the configuration
class is incomplete, which is a defect of the application that no edit of the
buffer can put right.
"""


class Converted(NamedTuple):
    """One leaf value as the configuration class would hold it."""

    value: object
    """What the converter of that member made of the value, or the value.

    It is the value itself for a member that has no converter, and also for
    one whose converter refused it, so that there is always something to go
    on. The type is genuinely unknown here: a converter may return anything.
    """

    message: str
    """Why the converter refused the value, empty when nothing refused it."""


def member_converters(config: Config) -> dict[str, ParseConverter]:
    """Return the parse converters of the members that one class declares.

    A class that declares none inherits a placeholder converter under a key of
    the base class's own, so the answer is restricted to the members the
    object really has. A converter named after something that is no member of
    the configuration could never be applied to anything in any case.

    Args:
        config: Configuration object to ask. It is not modified.

    Returns:
        One converter per member that has one.
    """
    declared = vars(config)
    return {name: converter
            for name, converter in (config.parse_converters() or {}).items()
            if name in declared}


def convert_member(converter: Optional[ParseConverter],
                   value: JsonType) -> Converted:
    """Return one leaf value as its member holds it, or why it cannot.

    A value that already has the type the converter produces is left alone,
    and so is a value that is `None`: a member that its class leaves out of
    JSON while it is None has nothing to convert, and a `None` that is wrong
    is refused by the validation of the whole configuration, which has a
    message of its own for it.

    Args:
        converter: How the text of this member becomes a value, or None for a
            member that holds what the file holds.
        value: JSON space value that the buffer holds for that member.

    Returns:
        The value the configuration would hold, or the reason it would not.
    """
    if converter is None or value is None or \
            isinstance(value, converter.result_type):
        return Converted(value=value, message='')
    try:
        return Converted(value=converter.func(value, **converter.args),
                         message='')
    except CONVERSION_ERRORS as error:
        return Converted(value=value, message=refusal_text(error))


def refusal_text(error: Exception) -> str:
    """Return what one refusal says, as the user should read it.

    A `KeyError` writes the representation of its argument rather than the
    argument itself, so the message about a name that is no member of an enum
    would otherwise arrive wrapped in quotation marks that nobody wrote.

    Args:
        error: The failure that was reported.

    Returns:
        What that failure says.
    """
    if isinstance(error, KeyError) and error.args:
        return str(error.args[0])
    return str(error)
