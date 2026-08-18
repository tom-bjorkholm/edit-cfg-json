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

Which class declared it is a question of its own once there are nested
configuration objects, and `node_converters` is where it is answered: a nested
object parses its own JSON, so what is inside it is answered by its own class
and not by the class above it.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from collections.abc import Mapping, Sequence
from typing import NamedTuple, Optional
from config_as_json import Config, ConfigPath, JsonType, ParseConverter
from edit_cfg_json.leaf_value import BOOL_CHOICES, value_as_text
from edit_cfg_json.tree import ConfigNode, owner_path, under_dict

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

NOT_A_BOOL_FORM = '{text} is not one of: {words}'
"""Why the text of a member holding true or false means neither of them.

It is worded as `config_as_json` words the same refusal about the name of an
enum member, because it is the same refusal: the member holds one of a known
set of values and the text names none of them. Such a member has no parse
converter to answer it — there is nothing to convert true into — so this is
the one refusal of a leaf that the editor makes itself, and it makes it about
the type of the member and never about a rule of the application.
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


def node_converters(nodes: Mapping[ConfigPath, ConfigNode],
                    flat: Sequence[tuple[ConfigPath, JsonType]]) \
        -> dict[ConfigPath, ParseConverter]:
    """Return the parse converter of every node of one tree that has one.

    Two things decide it, and each of them is a rule of `config_as_json`
    rather than of this editor. A converter is applied while an object is
    decoded, so it reaches the value of a dictionary key at any depth and
    never an element of a list. And a converter belongs to the class that owns
    the subtree, exactly as a write-side converter does: a nested
    configuration object parses its own JSON and applies its own converters,
    so the converters of the class above it are not the ones that answer for
    what is inside it.

    Args:
        nodes: Every configuration object of the tree, by its path.
        flat: The path and the value of every node, in row order.

    Returns:
        One converter per node that has one, by the path of that node.
    """
    owned = {path: member_converters(node.config)
             for path, node in nodes.items() if node.config is not None}
    values = dict(flat)
    found = ((path, owned.get(owner_path(path=path, nodes=nodes), {})
              .get(path[-1]))
             for path, _ in flat if under_dict(path=path, values=values))
    return {path: converter for path, converter in found
            if converter is not None}


def convert_member(converter: Optional[ParseConverter], value: JsonType,
                   is_bool_member: bool = False) -> Converted:
    """Return one leaf value as its member holds it, or why it cannot.

    A value that already has the type the converter produces is left alone,
    and so is a value that is `None`: a member that its class leaves out of
    JSON while it is None has nothing to convert, and a `None` that is wrong
    is refused by the validation of the whole configuration, which has a
    message of its own for it.

    A member holding true or false is answered without a converter, because
    it has none and needs none: `text_as_value` has already made the value of
    every text that means one of the two words, so a value that is neither
    means neither and is refused here as an enum member name that names no
    member is.

    Args:
        converter: How the text of this member becomes a value, or None for a
            member that holds what the file holds.
        value: JSON space value that the buffer holds for that member.
        is_bool_member: Whether this member held true or false when the file
            was last agreed with, which is what makes those the two values it
            takes.

    Returns:
        The value the configuration would hold, or the reason it would not.
    """
    if value is None:
        return Converted(value=value, message='')
    if converter is None:
        return _converted_bool(value=value, is_bool_member=is_bool_member)
    if isinstance(value, converter.result_type):
        return Converted(value=value, message='')
    try:
        return Converted(value=converter.func(value, **converter.args),
                         message='')
    except CONVERSION_ERRORS as error:
        return Converted(value=value, message=refusal_text(error))


def _converted_bool(value: JsonType, is_bool_member: bool) -> Converted:
    """Return one value of a member that no converter answers for.

    Args:
        value: JSON space value that the buffer holds for that member.
        is_bool_member: Whether that member holds true or false.

    Returns:
        The value, and why it is neither of the two words where it is neither.
    """
    if not is_bool_member or isinstance(value, bool):
        return Converted(value=value, message='')
    said = NOT_A_BOOL_FORM.format(text=value_as_text(value),
                                  words=BOOL_CHOICES)
    return Converted(value=value, message=said)


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
