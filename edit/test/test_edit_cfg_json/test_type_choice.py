#! /usr/bin/env python3
"""Tests for which types the user may choose, and what choosing one does.

These ask `type_choice` itself, one question at a time, with the types read
from real annotations. What a model makes of it is the business of the tests
of `EditModel.set_type`.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from typing import Literal, Optional
import pytest
from config_as_json import Config, JsonType, ParseConverter
from edit_cfg_json.type_choice import NOT_CONVERTED_FORM, chosen_option, \
    kept_choice, offered_types, switched_value
from edit_cfg_json.type_options import NONE_TYPE, type_options
from .sample_cfg import Colour

COLOUR_CONVERTER = Config.get_converter_dict(Colour)
"""The converter `config_as_json` ships for an enum, made for `Colour`."""


def _texts(hint: object, converter: Optional[ParseConverter],
           omitted: bool = False) -> list[str]:
    """Return the text of every type offered for one annotation."""
    offer = offered_types(options=type_options(hint), converter=converter,
                          omitted=omitted)
    return [option.text for option in offer.offered]


@pytest.mark.parametrize('hint, omitted, expected',
                         [(Optional[Colour], False, ['Colour']),
                          (Optional[Colour], True, ['Colour', 'None']),
                          (Colour | int, False, ['Colour']),
                          (Colour | str, False, ['Colour'])])
def test_converter_decides(hint: object, omitted: bool,
                           expected: list[str]) -> None:
    """Test a type whose empty value the converter refuses is not offered.

    The converter of an enum refuses everything that is not text, and the
    empty text is no name of a member. `None` is never converted where the
    class leaves the member out of the file, so it is offered there.
    """
    assert _texts(hint, COLOUR_CONVERTER, omitted=omitted) == expected


def test_refusal_says_why() -> None:
    """Test each type left out is said, with the value it was refused for."""
    offer = offered_types(options=type_options(Colour | int | None),
                          converter=COLOUR_CONVERTER, omitted=False)
    assert offer.refusals == (NOT_CONVERTED_FORM.format(type='int', value='0'),
                              NOT_CONVERTED_FORM.format(type='None',
                                                        value='null'))


@pytest.mark.parametrize('hint', [int | str, Optional[str], list[str] | None])
def test_no_converter_all(hint: object) -> None:
    """Test every declared type is offered where no converter says no."""
    offer = offered_types(options=type_options(hint), converter=None,
                          omitted=False)
    assert offer.offered == type_options(hint) and offer.refusals == ()


def test_not_choosable_kept() -> None:
    """Test a node whose type is not chosen keeps every declared type.

    Its type is what its value is, so nothing is asked of the converter.
    """
    assert _texts(Colour, COLOUR_CONVERTER) == ['Colour']


@pytest.mark.parametrize('hint, value, chosen, refreshing, expected',
                         [(int | float, 5, None, False, 'int'),
                          (int | float, 5, 'float', False, 'float'),
                          (int | str, 'abc', 'int', False, 'int'),
                          (int | str, 'abc', 'int', True, 'str'),
                          (int | float, 5, 'float', True, 'float'),
                          (Optional[str], None, 'str', True, 'None'),
                          (int | float, 'abc', None, False, 'int')])
def test_kept_choice(hint: object, value: JsonType, chosen: Optional[str],
                     refreshing: bool, expected: str) -> None:
    """Test the type a node holds outlives its value until a pass.

    A value that fits two types keeps the one chosen, a value of the wrong
    type keeps it as well until a validation pass leaves such a value, and a
    node with no choice yet holds the first type its value fits.
    """
    options = type_options(hint)
    held = next((option for option in options if option.text == chosen), None)
    assert kept_choice(options=options, value=value, chosen=held,
                       refreshing=refreshing).text == expected


def test_chosen_option() -> None:
    """Test the text of a type names that type among those offered."""
    options = type_options(int | str)
    assert chosen_option(options=options, text='str', name='width') == \
        options[1]


@pytest.mark.parametrize('hint, text', [(int | str, 'float'), (int, 'int'),
                                        (list[str] | None, 'None')])
def test_option_refused(hint: object, text: str) -> None:
    """Test a type not offered, and a node whose type is not chosen, refuse."""
    with pytest.raises(ValueError):
        chosen_option(options=type_options(hint), text=text, name='width')


@pytest.mark.parametrize('hint, value, expected',
                         [(int, '5', 5), (str, 5, '5'), (int, 'abc', 0),
                          (int, 5.5, 0), (float, 5, 5), (bool, 'true', True),
                          (bool, '5', False), (str, True, 'true'),
                          (str, None, ''), (int, None, 0),
                          (Colour, 'GREEN', 'GREEN'), (Colour, 'pink', 'RED'),
                          (Literal['a', 'b'], 'b', 'b'),
                          (Literal['a', 'b'], 'c', 'a'), (None, 'x', None)])
def test_switched_value(hint: object, value: JsonType,
                        expected: JsonType) -> None:
    """Test switching keeps a text that means a value of the new type.

    Everything else, and `None` on either side, is the empty value of the new
    type: the first name of an enum and the first value of a `Literal`.
    """
    option = type_options(hint)[0]
    assert switched_value(option, value) == expected


def test_switched_to_none() -> None:
    """Test choosing `None` takes the value away whatever it was."""
    assert switched_value(NONE_TYPE, 'kept') is None
