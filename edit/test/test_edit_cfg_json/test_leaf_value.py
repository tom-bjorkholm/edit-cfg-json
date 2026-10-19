#! /usr/bin/env python3
"""Tests for the JSON space meaning of one leaf value of the buffer."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from typing import Optional
import json
import pytest
from config_as_json import JsonType
from edit_cfg_json.leaf_value import BOOL_VALUES, canonical_text, \
    kind_of, known_values, named_value, text_as_value, value_as_text, \
    values_differ

EVERY_KIND = [None, True, False, 0, 42, -1, 1.5, '', 'text', '42',
              'with "quotes"', 'Björkholm', [1, 2], {'key': 1}]
"""One value of every kind that a leaf of the buffer can hold."""


def _same(value: JsonType, expected: JsonType) -> bool:
    """Return whether two values are equal and of the same kind."""
    return not values_differ(value, expected)


@pytest.mark.parametrize('value, expected',
                         [(42, '42'), (1.5, '1.5'), (True, 'true'),
                          (False, 'false'), (None, 'null'),
                          ('text', 'text'), ('', ''), ('42', '42'),
                          ('with "quotes"', 'with "quotes"'),
                          ([1, 2], '[1, 2]'), ({'key': 1}, '{"key": 1}')])
def test_value_as_text(value: JsonType, expected: str) -> None:
    """Test a string shows as itself and every other value as its JSON."""
    assert value_as_text(value) == expected


@pytest.mark.parametrize('text, expected',
                         [('42', 42), ('1.5', 1.5), ('true', True),
                          ('null', None), (' 42 ', 42),
                          ('"quoted"', 'quoted'), ('[1, 2]', [1, 2])])
def test_text_as_json(text: str, expected: JsonType) -> None:
    """Test the text of a member that is not text is read as JSON."""
    assert _same(text_as_value(text=text, kind=int), expected)


@pytest.mark.parametrize('text', ['', 'not-a-number', '01', '-', '1.2.3',
                                  'None', 'Yes'])
def test_text_that_is_no_json(text: str) -> None:
    """Test text that is not JSON is kept, so that it can be typed at all.

    A value being typed is not valid for most of the time it takes to type
    it. What is kept is a string in a member that is not a text member,
    which validation reports as the wrong type rather than the editor
    hiding it.
    """
    assert _same(text_as_value(text=text, kind=int), text)


@pytest.mark.parametrize('text', ['', '42', 'true', 'null', 'text',
                                  '  spaced  ', '"quoted"'])
def test_text_member_kept(text: str) -> None:
    """Test the text of a text member is kept exactly as it was typed."""
    assert _same(text_as_value(text=text, kind=str), text)


@pytest.mark.parametrize('text, expected',
                         [('true', True), ('True', True), ('TRUE', True),
                          ('t', True), ('tr', True), ('T', True),
                          (' t ', True), ('false', False), ('False', False),
                          ('FALSE', False), ('f', False), ('fal', False),
                          ('F', False)])
def test_bool_named(text: str, expected: bool) -> None:
    """Test the case is ignored and a beginning of either word is enough.

    It is what `config_as_json` does with the name of an enum member, and a
    member holding true or false is entered the same way for the same reason:
    the whole word is not typed yet for most of the time it takes to type it.
    """
    assert named_value(text=text, values=BOOL_VALUES) is expected


@pytest.mark.parametrize('text', ['', 'yes', 'no', '1', '0', 'null',
                                  'truely', 'tr ue', 'x'])
def test_no_bool_named(text: str) -> None:
    """Test text that begins neither word means neither of the two values.

    The empty text is the beginning of both of them and is therefore the
    beginning of neither, exactly as an enum member name that two members
    begin with names neither of them. It is what a cleared field holds.
    """
    assert named_value(text=text, values=BOOL_VALUES) is None


@pytest.mark.parametrize('text, expected',
                         [('t', True), ('FAL', False), ('true', True),
                          ('false', False)])
def test_flag_member_typed(text: str, expected: bool) -> None:
    """Test a member holding true or false takes a beginning of a word."""
    assert _same(text_as_value(text=text, kind=bool, values=BOOL_VALUES),
                 expected)


@pytest.mark.parametrize('text, expected', [('', ''), ('yes', 'yes'),
                                            ('1', 1), ('null', None),
                                            ('truely', 'truely')])
def test_flag_member_other(text: str, expected: JsonType) -> None:
    """Test every other text of such a member is read as any other is.

    Nothing is refused here, because a value being typed passes through text
    that means nothing. What such a value is not is a value of that member,
    and `convert_member` is what says so once the user has moved on.
    """
    assert _same(text_as_value(text=text, kind=bool, values=BOOL_VALUES),
                 expected)


@pytest.mark.parametrize('kind', [int, str, float, None])
def test_only_flag_expands(kind: Optional[type]) -> None:
    """Test no member of another kind reads `t` as one of the two values."""
    assert _same(text_as_value(text='t', kind=kind), 't')


WORDS = ('compact', 'wide', 'wider')
"""The values of a `Literal` of text, one of them the beginning of another."""


@pytest.mark.parametrize('text, expected',
                         [('compact', 'compact'), ('c', 'compact'),
                          ('COMP', 'compact'), (' wide ', 'wide'),
                          ('Wide', 'wide'), ('wider', 'wider'),
                          ('wide', 'wide')])
def test_literal_named(text: str, expected: str) -> None:
    """Test a value of a `Literal` is named as a member of an enum is.

    The case is ignored and a beginning is enough, and a text that is a value
    is that value although it begins another one as well.
    """
    assert named_value(text=text, values=WORDS) == expected


@pytest.mark.parametrize('text', ['', 'w', 'wid', 'tall', 'compactly'])
def test_literal_not_named(text: str) -> None:
    """Test a beginning of two values, or of none, names none of them."""
    assert named_value(text=text, values=WORDS) is None


def test_one_value_named() -> None:
    """Test where there is one value, every beginning of it is that value.

    The empty text is one of them, exactly as it is for an enum of one member
    in `config_as_json`.
    """
    assert named_value(text='', values=('only',)) == 'only'


@pytest.mark.parametrize('text', ['80', '8080', '84', ' 8443 '])
def test_number_not_named(text: str) -> None:
    """Test a number is never named by a beginning, nor by its text here.

    A number is the number its text is written as, which `text_as_value`
    reads as the JSON it is, so `80` cannot come to mean `8080`.
    """
    assert named_value(text=text, values=(8080, 8443)) is None


@pytest.mark.parametrize('text, expected',
                         [('wi', 'wide'), ('wide', 'wide'),
                          ('COMP', 'compact'), ('tall', 'tall'), ('', '')])
def test_text_literal_typed(text: str, expected: str) -> None:
    """Test the text of a `Literal` of text is the value it names, if any.

    A text that names none of them is kept as it was typed, for the reason
    every other text is kept: what it is not is a value of that node, and
    `convert_member` says so once the user has moved on.
    """
    values = ('compact', 'wide')
    assert _same(text_as_value(text=text, kind=str, values=values), expected)


@pytest.mark.parametrize('text, expected',
                         [('8080', 8080), (' 8443 ', 8443), ('80', 80),
                          ('84', 84), ('x', 'x')])
def test_number_lit_typed(text: str, expected: JsonType) -> None:
    """Test the text of a `Literal` of numbers is read as the JSON it is."""
    assert _same(text_as_value(text=text, kind=int, values=(8080, 8443)),
                 expected)


@pytest.mark.parametrize('kind, literals, expected',
                         [(bool, (), BOOL_VALUES),
                          (str, ('a', 'b'), ('a', 'b')),
                          (bool, (True,), (True,)), (int, (1, 2), (1, 2)),
                          (int, (), ()), (str, (), ()), (None, (), ())])
def test_known_values(kind: Optional[type], literals: tuple[JsonType, ...],
                      expected: tuple[JsonType, ...]) -> None:
    """Test the values of a `Literal`, or of true or false, are the known set.

    A `Literal` of true alone takes true alone, and not the two of a node
    holding true or false.
    """
    assert known_values(kind=kind, literals=literals) == expected


@pytest.mark.parametrize('value', EVERY_KIND)
def test_text_round_trip(value: JsonType) -> None:
    """Test showing a value and reading it back gives the same value.

    This is what makes an edit field stable. Without it, a value would drift
    every time it was shown and read again, which is what a field does on
    every single key press.
    """
    text = value_as_text(value)
    assert _same(text_as_value(text=text, kind=kind_of(value)), value)


@pytest.mark.parametrize('value, other, differ',
                         [(1, 1, False), (1, 2, True), (1, 1.0, True),
                          (True, 1, True), (False, 0, True),
                          (None, None, False), (None, 'null', True),
                          (42, '42', True), ('a', 'a', False),
                          ([1, 2], [1, 2], False), ([1, 2], [2, 1], True),
                          ({'key': 1}, {'key': 1}, False),
                          ({'a': 1, 'b': 2}, {'b': 2, 'a': 1}, False),
                          ({'a': {'x': 1, 'y': 2}},
                           {'a': {'y': 2, 'x': 1}}, False),
                          ({'a': 1}, {'a': 2}, True)])
def test_values_differ(value: JsonType, other: JsonType, differ: bool) -> None:
    """Test values are compared as a file would show them, not as Python.

    Python considers `True` equal to `1` and `1` equal to `1.0`, while all
    three are written differently to a JSON file. Changing a member from one
    to the other changes the file, so it is a change.

    The order of the keys of a dictionary is the one thing a file cannot
    hold, because `config_as_json` writes them sorted, so two dictionaries
    that differ only in it are the same values. The editor really does hold
    them in another order: the members of a nested configuration object are
    kept in the order its class declares them.
    """
    assert values_differ(value, other) is differ


@pytest.mark.parametrize('value', EVERY_KIND)
def test_canonical_json(value: JsonType) -> None:
    """Test the text a value is compared by is the JSON of that value.

    A list keeps its order, because a file keeps it, and everything else is
    written as it is written. Only the keys of a dictionary are sorted.
    """
    assert canonical_text(value) == json.dumps(value, sort_keys=True)


@pytest.mark.parametrize('text', ['42', 'true', 'null', '[1, 2]'])
def test_declared_text_kept(text: str) -> None:
    """Test a member that takes text keeps what was typed into it.

    Every one of these would be read as the JSON it is by a member of any
    other kind.
    """
    assert _same(text_as_value(text=text, kind=str), text)


@pytest.mark.parametrize('text, expected', [('t', True), ('FAL', False)])
def test_declared_flag(text: str, expected: bool) -> None:
    """Test a member that takes true or false takes a beginning."""
    assert _same(text_as_value(text=text, kind=bool, values=BOOL_VALUES),
                 expected)


def test_field_means_no_none() -> None:
    """Test `null` typed into a member that may hold nothing stays text.

    Holding nothing is a state of such a member and has a control of its own,
    so a field never puts the member into it: four characters would otherwise
    take the field away from under the cursor that typed them.
    """
    assert _same(text_as_value(text='null', kind=int, nothing=True), 'null')


def test_null_is_json() -> None:
    """Test a member with no such state reads `null` as the JSON it is."""
    assert text_as_value(text='null', kind=int) is None


@pytest.mark.parametrize('value', EVERY_KIND)
def test_declared_round_trip(value: JsonType) -> None:
    """Test a text member that may hold nothing reads back what it shows.

    Every value of every kind is shown as text and read back as the text it
    was shown as, which is what a member that takes text does with anything
    that reaches it.
    """
    text = value_as_text(value)
    assert _same(text_as_value(text=text, kind=str, nothing=True), text)
