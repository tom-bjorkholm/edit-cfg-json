#! /usr/bin/env python3
"""Tests for the JSON space meaning of one leaf value of the buffer."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import json
import pytest
from config_as_json import JsonType
from edit_cfg_json.leaf_value import canonical_text, text_as_value, \
    value_as_text, values_differ

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
    assert _same(text_as_value(text=text, is_text_member=False), expected)


@pytest.mark.parametrize('text', ['', 'not-a-number', '01', '-', '1.2.3',
                                  'None', 'Yes'])
def test_text_that_is_no_json(text: str) -> None:
    """Test text that is not JSON is kept, so that it can be typed at all.

    A value being typed is not valid for most of the time it takes to type
    it. What is kept is a string in a member that is not a text member,
    which validation reports as the wrong type rather than the editor
    hiding it.
    """
    assert _same(text_as_value(text=text, is_text_member=False), text)


@pytest.mark.parametrize('text', ['', '42', 'true', 'null', 'text',
                                  '  spaced  ', '"quoted"'])
def test_text_member_kept(text: str) -> None:
    """Test the text of a text member is kept exactly as it was typed."""
    assert _same(text_as_value(text=text, is_text_member=True), text)


@pytest.mark.parametrize('value', EVERY_KIND)
def test_text_round_trip(value: JsonType) -> None:
    """Test showing a value and reading it back gives the same value.

    This is what makes an edit field stable. Without it, a value would drift
    every time it was shown and read again, which is what a field does on
    every single key press.
    """
    is_text_member = isinstance(value, str)
    text = value_as_text(value)
    assert _same(text_as_value(text=text, is_text_member=is_text_member),
                 value)


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
