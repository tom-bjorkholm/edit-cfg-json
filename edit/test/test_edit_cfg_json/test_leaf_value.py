#! /usr/bin/env python3
"""Tests for the JSON space meaning of one leaf value of the buffer."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import json
import pytest
from config_as_json import JsonType
from edit_cfg_json.leaf_value import BOOL_KIND, LeafType, LIST_KIND, \
    NO_KIND, NUMBER_KIND, TEXT_KIND, WHOLE_NUMBER_KIND, bool_word, \
    canonical_text, kind_text, text_as_value, value_as_text, values_differ

EVERY_KIND = [None, True, False, 0, 42, -1, 1.5, '', 'text', '42',
              'with "quotes"', 'Björkholm', [1, 2], {'key': 1}]
"""One value of every kind that a leaf of the buffer can hold."""

NUMBER_MEMBER = 0
"""A member that kept a number, which is read as JSON and never as text."""

TEXT_MEMBER = ''
"""A member that kept text, which keeps exactly what was typed."""

FLAG_MEMBER = True
"""A member that kept true or false, which takes a beginning of either."""


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
    assert _same(text_as_value(text=text, original=NUMBER_MEMBER), expected)


@pytest.mark.parametrize('text', ['', 'not-a-number', '01', '-', '1.2.3',
                                  'None', 'Yes'])
def test_text_that_is_no_json(text: str) -> None:
    """Test text that is not JSON is kept, so that it can be typed at all.

    A value being typed is not valid for most of the time it takes to type
    it. What is kept is a string in a member that is not a text member,
    which validation reports as the wrong type rather than the editor
    hiding it.
    """
    assert _same(text_as_value(text=text, original=NUMBER_MEMBER), text)


@pytest.mark.parametrize('text', ['', '42', 'true', 'null', 'text',
                                  '  spaced  ', '"quoted"'])
def test_text_member_kept(text: str) -> None:
    """Test the text of a text member is kept exactly as it was typed."""
    assert _same(text_as_value(text=text, original=TEXT_MEMBER), text)


@pytest.mark.parametrize('text, expected',
                         [('true', True), ('True', True), ('TRUE', True),
                          ('t', True), ('tr', True), ('T', True),
                          (' t ', True), ('false', False), ('False', False),
                          ('FALSE', False), ('f', False), ('fal', False),
                          ('F', False)])
def test_bool_word(text: str, expected: bool) -> None:
    """Test the case is ignored and a beginning of either word is enough.

    It is what `config_as_json` does with the name of an enum member, and a
    member holding true or false is entered the same way for the same reason:
    the whole word is not typed yet for most of the time it takes to type it.
    """
    assert bool_word(text) is expected


@pytest.mark.parametrize('text', ['', 'yes', 'no', '1', '0', 'null',
                                  'truely', 'tr ue', 'x'])
def test_no_bool_word(text: str) -> None:
    """Test text that begins neither word means neither of the two values.

    The empty text is the beginning of both of them and is therefore the
    beginning of neither, exactly as an enum member name that two members
    begin with names neither of them. It is what a cleared field holds.
    """
    assert bool_word(text) is None


@pytest.mark.parametrize('text, expected',
                         [('t', True), ('FAL', False), ('true', True),
                          ('false', False)])
def test_flag_member_typed(text: str, expected: bool) -> None:
    """Test a member holding true or false takes a beginning of a word."""
    assert _same(text_as_value(text=text, original=FLAG_MEMBER), expected)


@pytest.mark.parametrize('text, expected', [('', ''), ('yes', 'yes'),
                                            ('1', 1), ('null', None),
                                            ('truely', 'truely')])
def test_flag_member_other(text: str, expected: JsonType) -> None:
    """Test every other text of such a member is read as any other is.

    Nothing is refused here, because a value being typed passes through text
    that means nothing. What such a value is not is a value of that member,
    and `convert_member` is what says so once the user has moved on.
    """
    assert _same(text_as_value(text=text, original=FLAG_MEMBER), expected)


@pytest.mark.parametrize('original', [NUMBER_MEMBER, TEXT_MEMBER, 1.5, None])
def test_only_flag_expands(original: JsonType) -> None:
    """Test no member of another kind reads `t` as one of the two values."""
    assert _same(text_as_value(text='t', original=original), 't')


@pytest.mark.parametrize('value', EVERY_KIND)
def test_text_round_trip(value: JsonType) -> None:
    """Test showing a value and reading it back gives the same value.

    This is what makes an edit field stable. Without it, a value would drift
    every time it was shown and read again, which is what a field does on
    every single key press.
    """
    text = value_as_text(value)
    assert _same(text_as_value(text=text, original=value), value)


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


TEXT_TYPE = LeafType(kind=str)
"""What a member declared to hold text says about itself."""

MAYBE_TEXT = LeafType(kind=str, nothing=True)
"""What a member declared `Optional[str]` says about itself."""


@pytest.mark.parametrize('text', ['42', 'true', 'null', '[1, 2]'])
def test_declared_text_kept(text: str) -> None:
    """Test a member declared to hold text keeps what was typed into it.

    The value it holds says nothing here, because it holds none: without the
    declaration every one of these would be read as the JSON it is.
    """
    assert _same(text_as_value(text=text, original=None,
                               declared=TEXT_TYPE), text)


@pytest.mark.parametrize('text, expected', [('t', True), ('FAL', False)])
def test_declared_flag(text: str, expected: bool) -> None:
    """Test a member declared to hold true or false takes a beginning."""
    assert _same(text_as_value(text=text, original=None,
                               declared=LeafType(kind=bool)), expected)


def test_declared_beats_value() -> None:
    """Test the declaration answers where the value would answer otherwise.

    A member declared to hold text and holding a number is a text member, and
    a member declared to hold a number and holding text is not.
    """
    assert _same(text_as_value(text='42', original=7, declared=TEXT_TYPE),
                 '42')
    assert _same(text_as_value(text='42', original='seven',
                               declared=LeafType(kind=int)), 42)


def test_field_means_no_none() -> None:
    """Test `null` typed into a member that may hold nothing stays text.

    Holding nothing is a state of such a member and has a control of its own,
    so a field never puts the member into it: four characters would otherwise
    take the field away from under the cursor that typed them.
    """
    assert _same(text_as_value(text='null', original=7,
                               declared=LeafType(kind=int, nothing=True)),
                 'null')


def test_null_is_json() -> None:
    """Test a member with no such state reads `null` as the JSON it is."""
    assert text_as_value(text='null', original=7) is None


@pytest.mark.parametrize('declared, value, expected',
                         [(LeafType(), 'text', TEXT_KIND),
                          (LeafType(), None, NO_KIND),
                          (LeafType(kind=float), 0, NUMBER_KIND),
                          (LeafType(kind=str), None, TEXT_KIND),
                          (LeafType(kind=bool), None, BOOL_KIND),
                          (LeafType(kind=int), 7, WHOLE_NUMBER_KIND),
                          (LeafType(kind=list), None, LIST_KIND),
                          (LeafType(kind=list), [1], ''),
                          (LeafType(), {'a': 1}, '')])
def test_kind_text(declared: LeafType, value: JsonType, expected: str) -> None:
    """Test what each node says about the kind of value it holds.

    A member declared `float` whose value is written `0` is the case that the
    value alone gets wrong, and a member holding nothing is the case it
    cannot answer at all. A node that really holds a container says nothing,
    because its row already says how much it holds.
    """
    assert kind_text(declared=declared, value=value) == expected


@pytest.mark.parametrize('value', EVERY_KIND)
def test_declared_round_trip(value: JsonType) -> None:
    """Test a declared text member shows and reads back the same value.

    Every value of every kind is shown as text and read back as the text it
    was shown as, which is what a member declared to hold text does with
    anything that reaches it.
    """
    text = value_as_text(value)
    assert _same(text_as_value(text=text, original=value,
                               declared=MAYBE_TEXT), text)
