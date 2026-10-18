#! /usr/bin/env python3
"""Tests for how a declaration is read into the types it allows.

Every annotation is resolved here by Python itself, which is what the editor
is given once `member_types` has read a class: these are about what is made of
a resolved hint, and the source of a class is the business of the tests of
that module.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from pathlib import Path
from types import NoneType
from typing import Any, Dict, List, Literal, Optional, Union
import pytest
from config_as_json import JsonType
from edit_cfg_json.type_options import CUT_MARK, NONE_TYPE, \
    TYPE_COLUMN_LIMIT, TypeOption, allowed_values, choosable, \
    cut_type_text, empty_option_value, fits, held_option, inferred_option, \
    node_options, reading_kind, spelled, type_options
from .container_cfg import InnerCfg
from .sample_cfg import Colour

type Pair = list[int]
"""A PEP 695 alias, which is spelled as what it stands for."""


def _texts(hint: object) -> list[str]:
    """Return the text of every type one hint allows."""
    return [option.text for option in type_options(hint)]


@pytest.mark.parametrize('hint, expected',
                         [(int, ['int']), (float, ['float']),
                          (bool, ['bool']), (str, ['str']),
                          (Optional[int], ['int', 'None']),
                          (Union[int, None], ['int', 'None']),
                          (int | None, ['int', 'None']),
                          (Union[str, int], ['str', 'int']),
                          (int | str | None, ['int', 'str', 'None']),
                          (None, ['None']),
                          (list, ['list']), (dict, ['dict']),
                          (List[str], ['list[str]']),
                          (Dict[str, int], ['dict[str, int]']),
                          (list[Optional[str]], ['list[str | None]']),
                          (dict[str, list[str] | list[list[str]]],
                           ['dict[str, list[str] | list[list[str]]]']),
                          (Colour, ['Colour']),
                          (Optional[InnerCfg], ['InnerCfg', 'None']),
                          (Path, ['Path']),
                          (Literal['compact', 'wide'],
                           ["Literal['compact', 'wide']"]),
                          (Literal[1, 2], ['Literal[1, 2]']),
                          (Pair, ['list[int]']),
                          (Pair | None, ['list[int]', 'None']),
                          (list[Pair], ['list[list[int]]']),
                          (list[tuple[int, int]],
                           ['list[tuple[int, int]]'])])
def test_spelled_as_python(hint: object, expected: list[str]) -> None:
    """Test each declaration is spelled as Python spells the resolved hint.

    `Optional[int]` and `Union[int, None]` are `int | None`, an old generic
    alias is the built in type it stands for, an alias of PEP 695 is what it
    stands for, and a class is its own unqualified name. The alternatives are
    in the order the declaration writes them.
    """
    assert _texts(hint) == expected


@pytest.mark.parametrize('hint', [tuple[int, int], set[str], Any, object,
                                  Literal['a', 1], int | tuple[int, int],
                                  Optional[Any]])
def test_nothing_usable(hint: object) -> None:
    """Test a declaration of which any part is unusable allows no type.

    A union is unusable as a whole where one of its alternatives is, because
    a pull-down that left one out would say less than the declaration does.
    A container is not, because what a list is does not depend on what it
    holds, and that is the last case of the test above.
    """
    assert type_options(hint) == ()


def test_inside_unusable() -> None:
    """Test a container of something unusable says nothing about inside."""
    assert type_options(list[tuple[int, int]])[0].inside == ()


@pytest.mark.parametrize('hint, kind', [(Colour, str), (InnerCfg, dict),
                                        (Path, None), (None, NoneType),
                                        (Literal[True], bool)])
def test_kind_of_a_type(hint: object, kind: Optional[type]) -> None:
    """Test which kind of JSON value each type is written as.

    An enum is the name of a member and a configuration class a dict, and a
    class of the application's own is whatever its converters make of it,
    which only the value says.
    """
    assert type_options(hint)[0].kind is kind


def test_union_inside() -> None:
    """Test a union inside a container is one type with two inside it."""
    found = type_options(dict[str, list[str] | list[list[str]]])
    assert [option.text for option in found[0].inside] == ['list[str]',
                                                           'list[list[str]]']


def test_spelled_unusable() -> None:
    """Test a hint the editor cannot use is spelled all the same."""
    assert spelled(tuple[int, ...]) == 'tuple[int, ...]'
    assert spelled(Any) == 'Any'


STR_LIST, NESTED_LIST = type_options(list[str] | list[list[str]])
"""The two alternatives of the declaration the complaint was about."""


@pytest.mark.parametrize('option, value, expected',
                         [(TypeOption('int', kind=int), 5, True),
                          (TypeOption('float', kind=float), 0, True),
                          (TypeOption('int', kind=int), 0.5, False),
                          (TypeOption('int', kind=int), True, False),
                          (TypeOption('str', kind=str), '5', True),
                          (NONE_TYPE, None, True),
                          (NONE_TYPE, '', False),
                          (TypeOption('Path', of_class=Path), 'x', True),
                          (TypeOption('Path', of_class=Path), None, False),
                          (STR_LIST, ['x'], True),
                          (STR_LIST, [['x']], False),
                          (NESTED_LIST, [['x']], True),
                          (NESTED_LIST, [], True),
                          (type_options(Literal['a', 'b'])[0], 'a', True),
                          (type_options(Literal['a', 'b'])[0], 'c', False),
                          (type_options(Literal[1])[0], True, False),
                          (type_options(Colour)[0], 'GREEN', True),
                          (type_options(Colour)[0], 'gr', False)])
def test_value_fits(option: TypeOption, value: JsonType,
                    expected: bool) -> None:
    """Test which values are values of which types.

    A whole number is a number, true is not a whole number, and a container
    fits where everything inside it fits, which is what tells the two lists
    of the complaint apart. The values of an enum are the names of its
    members and nothing else.
    """
    assert fits(option, value) is expected


@pytest.mark.parametrize('hint, value, expected',
                         [(int | float, 5, 'int'), (float | int, 5, 'float'),
                          (Optional[str], None, 'None'),
                          (Optional[str], 'x', 'str'),
                          (Optional[int], 'half typed', 'int'),
                          (None | int, 'x', 'int'),
                          (list[str] | list[list[str]], [['x']],
                           'list[list[str]]')])
def test_held_option(hint: object, value: JsonType, expected: str) -> None:
    """Test the type a value holds is the first one it fits.

    A value that fits none of them holds the first that is not `None`, which
    is what its text is read by.
    """
    held = held_option(type_options(hint), value)
    assert held is not None and held.text == expected


def test_nothing_held() -> None:
    """Test no type is held where no type is allowed."""
    assert held_option((), 5) is None


@pytest.mark.parametrize('hint, original, expected',
                         [(float, 0, float), (Optional[str], None, str),
                          (Optional[int], None, int), (int | str, 'x', str),
                          (int | str, 5, int), (Path, 'x', str),
                          (Colour, 'RED', str), (None, None, None)])
def test_reading_kind(hint: object, original: JsonType,
                      expected: Optional[type]) -> None:
    """Test which kind the text of a node is read as.

    The declaration wins over the value, which is the case of `float` and of
    a member holding nothing. A class whose kind only the value says is read
    by the value, and so is a declaration that allows nothing but `None`.
    """
    assert reading_kind(type_options(hint), original) is expected


def test_reading_undeclared() -> None:
    """Test a node with no usable declaration is read as its value was."""
    assert reading_kind((), 7) is int


def test_objects_apart() -> None:
    """Test a node holds a configuration class only where an object is.

    An object is written as a dict and so is a dict, so the tree is what says
    which of the two a node is, and `None` is either.
    """
    options = type_options(Optional[InnerCfg | dict[str, int]])
    assert [option.text for option in node_options(options, True)] == [
        'InnerCfg', 'None']
    assert [option.text for option in node_options(options, False)] == [
        'dict[str, int]', 'None']


@pytest.mark.parametrize('hint, expected',
                         [(str, ''), (int, 0), (float, 0.0), (bool, False),
                          (list[str], []), (dict[str, int], {}),
                          (Colour, 'RED'), (InnerCfg, None), (Path, None),
                          (Literal['a', 'b'], 'a'), (None, None)])
def test_empty_option_value(hint: object, expected: JsonType) -> None:
    """Test the value of each type that says no more than its type.

    A type whose values are a known set is given the first of them, which is
    the name of the first member of an enum. A class of the application's own
    is a type the editor cannot make a value of on its own.
    """
    found = empty_option_value(type_options(hint)[0])
    assert found == expected and type(found) is type(expected)


@pytest.mark.parametrize('hint, expected',
                         [(Colour, ('RED', 'GREEN')),
                          (Literal['a', 'b'], ('a', 'b')), (str, ()),
                          (InnerCfg, ())])
def test_allowed_values(hint: object, expected: tuple[str, ...]) -> None:
    """Test the values of a type whose values are a known set."""
    assert allowed_values(type_options(hint)[0]) == expected


@pytest.mark.parametrize('hint, expected',
                         [(int | str, True), (Optional[float], True),
                          (Optional[Colour], True), (bool | str, True),
                          (Literal['a'] | int, True), (int, False),
                          (Optional[list[str]], True),
                          (Optional[dict[str, int]], True),
                          (int | list[int], True),
                          (Optional[InnerCfg], False), (Path | None, False),
                          (InnerCfg | dict[str, int], False),
                          (list[str] | list[list[str]], True)])
def test_choosable(hint: object, expected: bool) -> None:
    """Test which declarations leave the type of a node to the user.

    They are those of more than one type, every one of them a plain value, a
    list, a dict or `None`: an enum and a `Literal` are plain values, and a
    configuration class and another class of the application are not, even
    though the first of them is written as a dict.
    """
    assert choosable(type_options(hint)) is expected


@pytest.mark.parametrize('value, expected',
                         [('x', 'str'), (1, 'int'), (1.5, 'float'),
                          (True, 'bool'), ([], 'list'), ({}, 'dict'),
                          (None, 'None')])
def test_inferred_option(value: JsonType, expected: str) -> None:
    """Test the type a value says it is, where nothing else says."""
    assert inferred_option(value).text == expected


def test_short_text_kept() -> None:
    """Test a type that fits the column is shown as it is."""
    text = spelled(dict[str, list[str] | list[list[str]]])
    assert cut_type_text(text) == text


def test_long_text_cut() -> None:
    """Test a type longer than the column is cut, and says that it is."""
    whole = spelled(dict[str, InnerCfg | str | dict[str, int]])
    cut = cut_type_text(whole)
    assert len(cut) == TYPE_COLUMN_LIMIT and cut.endswith(CUT_MARK)
    assert whole.startswith(cut[:-len(CUT_MARK)])
