#! /usr/bin/env python3
"""Tests for which types the user may choose, and what choosing one does.

These ask `type_choice` itself, one question at a time, with the types read
from real annotations. What a model makes of it is the business of the tests
of `EditModel.set_type`.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from pathlib import Path
from typing import Literal, Optional
import pytest
from config_as_json import Config, JsonType, ParseConverter
from edit_cfg_json.type_choice import DICT_ONLY, NOT_CONVERTED_FORM, \
    NOT_MADE, NO_DICT_YET, NO_OBJECT_HERE, NodeFacts, chosen_option, \
    offered_types, switched_value
from edit_cfg_json.type_options import NONE_TYPE, kept_choice, type_options
from .container_cfg import InnerCfg
from .sample_cfg import Colour

COLOUR_CONVERTER = Config.get_converter_dict(Colour)
"""The converter `config_as_json` ships for an enum, made for `Colour`."""


def _texts(hint: object, facts: NodeFacts = NodeFacts()) -> list[str]:
    """Return the text of every type offered for one annotation."""
    offer = offered_types(options=type_options(hint), facts=facts)
    return [option.text for option in offer.offered]


def _colour(omitted: bool = False) -> NodeFacts:
    """Return the facts of a node whose converter is the one of `Colour`."""
    converter: ParseConverter = COLOUR_CONVERTER
    return NodeFacts(converter=converter, omitted=omitted)


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
    assert _texts(hint, _colour(omitted=omitted)) == expected


def test_refusal_says_why() -> None:
    """Test each type left out is said, with the value it was refused for."""
    offer = offered_types(options=type_options(Colour | int | None),
                          facts=_colour())
    assert offer.refusals == (NOT_CONVERTED_FORM.format(type='int', value='0'),
                              NOT_CONVERTED_FORM.format(type='None',
                                                        value='null'))


@pytest.mark.parametrize('hint', [int | str, Optional[str], list[str] | None])
def test_no_converter_all(hint: object) -> None:
    """Test every declared type is offered where no converter says no."""
    offer = offered_types(options=type_options(hint), facts=NodeFacts())
    assert offer.offered == type_options(hint) and offer.refusals == ()


def test_not_choosable_kept() -> None:
    """Test a node whose type is not chosen keeps every declared type.

    Its type is what its value is, so nothing is asked of the converter.
    """
    assert _texts(Colour, _colour()) == ['Colour']


@pytest.mark.parametrize('hint, value, chosen, refreshing, expected',
                         [(int | float, 5, None, False, 'int'),
                          (int | float, 5, 'float', False, 'float'),
                          (int | str, 'abc', 'int', False, 'int'),
                          (int | str, 'abc', 'int', True, 'str'),
                          (int | float, 5, 'float', True, 'float'),
                          (Optional[str], None, 'str', True, 'None'),
                          (int | float, 'abc', None, False, 'int'),
                          (list[str] | list[list[str]], [],
                           'list[list[str]]', False, 'list[list[str]]'),
                          (list[str] | list[list[str]], [],
                           'list[list[str]]', True, 'list[list[str]]'),
                          (list[str] | list[list[str]], ['x'],
                           'list[list[str]]', True, 'list[str]')])
def test_kept_choice(hint: object, value: JsonType, chosen: Optional[str],
                     refreshing: bool, expected: str) -> None:
    """Test the type a node holds outlives its value until a pass.

    A value that fits two types keeps the one chosen, a value of the wrong
    type keeps it as well until a validation pass leaves such a value, and a
    node with no choice yet holds the first type its value fits.
    """
    options = type_options(hint)
    held = next((option for option in options if option.text == chosen), None)
    kept = kept_choice(options=options, value=value, chosen=held,
                       refreshing=refreshing)
    assert kept is not None and kept.text == expected


def test_chosen_option() -> None:
    """Test the text of a type names that type among those offered."""
    options = type_options(int | str)
    assert chosen_option(options=options, text='str', name='width') == \
        options[1]


@pytest.mark.parametrize('hint, text', [(int | str, 'float'), (int, 'int'),
                                        (list[str] | None, 'list[int]'),
                                        (Path | None, 'None')])
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
                          (Literal['a', 'b'], 'c', 'a'), (None, 'x', None),
                          (Literal['compact', 'wide'], 'wi', 'wide'),
                          (Literal['compact', 'wide'], 'WIDE', 'wide'),
                          (Literal[8080, 8443], '8443', 8443),
                          (Literal[8080, 8443], '84', 8080), (bool, 't', True),
                          (list[str], ['a'], []), (list[str], 'a', []),
                          (dict[str, int], {'a': 1}, {}), (int, [5], 0),
                          (str, {'a': 'b'}, '')])
def test_switched_value(hint: object, value: JsonType,
                        expected: JsonType) -> None:
    """Test switching keeps a text that means a value of the new type.

    A text means a value of a `Literal` of text, or of true or false, by the
    rules a field of that type reads it by, so `wi` means `wide`; a number is
    the number it is written as. Everything else, and `None`, a list and a
    dict on either side, is the empty value of the new type: the first name
    of an enum, the first value of a `Literal`, and the empty list and dict.
    """
    option = type_options(hint)[0]
    assert switched_value(option, value) == expected


def test_switched_to_none() -> None:
    """Test choosing `None` takes the value away whatever it was."""
    assert switched_value(NONE_TYPE, 'kept') is None


def test_kept_no_types() -> None:
    """Test a node allowed no type at all holds none, rather than failing."""
    assert kept_choice(options=(), value=5, chosen=None,
                       refreshing=False) is None


@pytest.mark.parametrize('holds_dict, expected',
                         [(None, ['dict[str, int]', 'None']),
                          (True, ['dict[str, int]']), (False, ['None'])])
def test_dict_shape_decides(holds_dict: Optional[bool],
                            expected: list[str]) -> None:
    """Test a type of the wrong side of the dict-shape check is not offered.

    The class refuses a dict where it holds none and anything else where it
    holds one, `None` among it, and offers both where its check never asks.
    """
    assert _texts(Optional[dict[str, int]],
                  NodeFacts(holds_dict=holds_dict)) == expected


@pytest.mark.parametrize('holds_dict, form',
                         [(True, DICT_ONLY), (False, NO_DICT_YET)])
def test_shape_says_why(holds_dict: bool, form: str) -> None:
    """Test each type the dict-shape check refuses is said, by its name."""
    offer = offered_types(options=type_options(Optional[dict[str, int]]),
                          facts=NodeFacts(holds_dict=holds_dict))
    left_out = 'None' if holds_dict else 'dict[str, int]'
    assert offer.refusals == (form.format(type=left_out),)


def test_shape_not_chosen() -> None:
    """Test the dict-shape check is asked of a type that is not chosen too.

    A single declared dict where the class holds none is no type at all,
    because the class would refuse any dict written for it.
    """
    assert _texts(dict[str, int], NodeFacts(holds_dict=False)) == []


def test_unknown_kind_kept() -> None:
    """Test a class whose kind only its value says is never shape refused.

    Nothing says whether its converters write it as a dict or not, so the
    dict-shape check cannot be said to refuse it.
    """
    assert _texts(Path | None, NodeFacts(holds_dict=True)) == ['Path']


@pytest.mark.parametrize('placed, expected',
                         [(None, ['None']), (False, ['None']),
                          (True, ['InnerCfg', 'None'])])
def test_object_placed(placed: Optional[bool], expected: list[str]) -> None:
    """Test a configuration class is offered only where it can be placed.

    That is where `nested_configs()` declares an object, and there only where
    one is or the editor can construct one.
    """
    assert _texts(InnerCfg | None, NodeFacts(placed=placed)) == expected


@pytest.mark.parametrize('placed, form',
                         [(None, NO_OBJECT_HERE), (False, NOT_MADE)])
def test_object_says_why(placed: bool, form: str) -> None:
    """Test a configuration class left out is said, with the reason."""
    offer = offered_types(options=type_options(InnerCfg | str),
                          facts=NodeFacts(value='x', placed=placed))
    assert offer.refusals == (form.format(type='InnerCfg'),)


@pytest.mark.parametrize('hint, value, expected',
                         [(Optional[int | Path], 5, ['int', 'None']),
                          (Optional[int | Path], None, ['int', 'None']),
                          (Optional[int | Path], 'x/y',
                           ['int', 'Path', 'None']),
                          (int | Path, 'x/y', ['int', 'Path']),
                          (Path | None, None, ['Path', 'None']),
                          (Path | None, 'x/y', ['Path', 'None'])])
def test_unmade_left_out(hint: object, value: JsonType,
                         expected: list[str]) -> None:
    """Test a type the editor cannot make is offered only where it must be.

    That is where the node holds it, and where nothing besides `None` is
    offered instead: `Path | None` keeps `Path`, because leaving it out
    would leave nothing but `None` to hold.
    """
    assert _texts(hint, NodeFacts(value=value)) == expected


def test_unmade_says_why() -> None:
    """Test a type the editor cannot make is said, by its name."""
    offer = offered_types(options=type_options(Optional[int | Path]),
                          facts=NodeFacts(value=5))
    assert offer.refusals == (NOT_MADE.format(type='Path'),)


def test_unmade_not_converted() -> None:
    """Test no converter is asked about a type the editor cannot make.

    There is no value of it to ask about, so a node that holds one keeps it
    offered: the converter of `Colour` would refuse the `null` that asking
    about the empty value of `Path` would have handed it.
    """
    facts = _colour()._replace(value='x/y')
    assert _texts(Path | Colour, facts) == ['Path', 'Colour']
