#! /usr/bin/env python3
"""Which types the user may choose between, and what choosing one does.

A node whose declaration allows more than one plain type, or a plain type and
`None`, holds the one of them that the user chose (section 4.12 of
`doc/detailed_design.md`). This module answers the three questions choosing
raises: which of the declared types are offered at all, which of them a node
holds as the buffer changes, and what a node holds once another is chosen.

**A type the class would refuse is not offered.** `config_as_json` hands the
value of a member with a parse converter to that converter whenever the value
is not already of the type the converter makes, and the converter it ships for
an enum refuses everything that is not text: `3` beside `Colors`, and the
`null` of an `Optional[Colors]` that its class writes as `null`. So the
converter is run on the value that choosing a type would give, as it is run on
a field losing the focus, and a type whose value it refuses is left out with a
sentence saying why. An application whose own converter takes more is offered
more, which is principle 1 of section 3 of the design.

**The choice outlives the value**, because a value can fit more than one type:
`5` is an `int` and a `float`, and `''` is a `str` and may be a `Literal` of
text. So the type a node holds is first read from its value, then kept, and
read from the value again only where a validation pass left a value that the
kept type does not fit. Typing never changes it: a text that is no number,
typed while `int` is chosen, is a value of the wrong type and not a choice.

**Switching keeps what still fits.** A plain value keeps its text where that
text means a value of the new type, so the text `5` becomes the number `5`
when `str` is changed to `int`, and everything else is given the empty value
of the new type: `''`, `0`, the first name of an enum, the first value of a
`Literal`, or nothing at all.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from collections.abc import Sequence
from typing import NamedTuple, Optional
import json
from config_as_json import JsonType, ParseConverter
from edit_cfg_json.converting import CONVERSION_ERRORS
from edit_cfg_json.leaf_value import text_as_value, value_as_text
from edit_cfg_json.type_options import NONE_TYPE, TypeOption, choosable, \
    empty_option_value, fits, held_option

NOT_CONVERTED_FORM = ('{type} is not offered, because the parse converter of '
                      'this member refuses {value}.')
"""What is said below a node about a declared type the class would refuse.

The value is written in JSON, so that the empty text is `""` and no value at
all is `null`, which is what the converter would be given.
"""

NOT_CHOOSABLE = 'The type of {name} is not one to choose.'
"""Message of the error raised when the type of a node cannot be chosen."""

NOT_OFFERED = '{name} may hold {types}, and not {type}.'
"""Message of the error raised when a node is given a type it is not offered.
"""


class TypeOffer(NamedTuple):
    """The types one node is offered, and why any declared one is not."""

    offered: tuple[TypeOption, ...]
    """The declared types the class would accept, in declared order."""

    refusals: tuple[str, ...] = ()
    """One sentence per declared type that is left out, saying why."""


def offered_types(options: Sequence[TypeOption],
                  converter: Optional[ParseConverter],
                  omitted: bool) -> TypeOffer:
    """Return which of the types one node may hold its class would accept.

    Only a node whose type is the user's to choose is asked, because only
    there would a refused type be something to choose: every other node holds
    what its value is.

    Args:
        options: The types the declaration of that node allows.
        converter: How the text of that node becomes the value it holds, or
            None for a node that holds what the file holds.
        omitted: Whether its class leaves it out of the file while it holds
            nothing, which is when `config_as_json` converts nothing at all.

    Returns:
        The types offered, and why each of the others is not.
    """
    if converter is None or not choosable(options):
        return TypeOffer(offered=tuple(options))
    offered = tuple(option for option in options
                    if _converts(option=option, converter=converter,
                                 omitted=omitted))
    refusals = tuple(NOT_CONVERTED_FORM.format(
        type=option.text, value=json.dumps(empty_option_value(option)))
        for option in options if option not in offered)
    return TypeOffer(offered=offered, refusals=refusals)


def _converts(option: TypeOption, converter: ParseConverter,
              omitted: bool) -> bool:
    """Return whether one converter takes the empty value of one type."""
    value = empty_option_value(option)
    if (value is None and omitted) or \
            isinstance(value, converter.result_type):
        return True
    try:
        converter.func(value, **converter.args)
    except CONVERSION_ERRORS:
        return False
    return True


def kept_choice(options: Sequence[TypeOption], value: JsonType,
                chosen: Optional[TypeOption], refreshing: bool) -> TypeOption:
    """Return the type one node holds once its rows have been built again.

    Args:
        options: The types the user may choose between for that node.
        value: The value it holds now.
        chosen: The type it held before, None for a node that had none.
        refreshing: Whether the rows are what a validation pass left behind,
            which is the one change that gives the value a say again.

    Returns:
        The type it held, where it still may and the value has no say, and
        the first type its value fits otherwise.
    """
    if chosen is not None and chosen in options and \
            (not refreshing or fits(chosen, value)):
        return chosen
    held = held_option(options, value)
    assert held is not None
    return held


def chosen_option(options: Sequence[TypeOption], text: str,
                  name: str) -> TypeOption:
    """Return the type one text names among those one node is offered.

    Args:
        options: The types that node is offered.
        text: The type as a Python type hint spells it.
        name: What the node is called, for the message.

    Returns:
        The type that text names.

    Raises:
        ValueError: The type of that node is not the user's to choose, or the
            text names none of its types.
    """
    if not choosable(options):
        raise ValueError(NOT_CHOOSABLE.format(name=name))
    found = next((option for option in options if option.text == text), None)
    if found is None:
        raise ValueError(NOT_OFFERED.format(
            name=name, type=text,
            types=', '.join(option.text for option in options)))
    return found


def switched_value(option: TypeOption, value: JsonType) -> JsonType:
    """Return what one node holds once the user has chosen one of its types.

    Args:
        option: The type chosen.
        value: The value the node held before.

    Returns:
        That value read again as a value of the new type, where its text
        means one, and the empty value of the new type otherwise.
    """
    if option == NONE_TYPE or value is None or \
            isinstance(value, (list, dict)):
        return empty_option_value(option)
    kept = text_as_value(text=value_as_text(value), kind=option.kind)
    return kept if fits(option, kept) else empty_option_value(option)
