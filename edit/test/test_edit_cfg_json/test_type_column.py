#! /usr/bin/env python3
"""Tests for the type every row says it holds, and the column that says it.

What a declaration is read into is the business of the tests of
`type_options`; these are about what a row of a model makes of it: which of
its types it holds, what the column shows, how wide the column is, and what is
said below a row about what the column cannot show.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import pytest
from config_as_json import Config, ConfigPath
from edit_cfg_json import EditModel, model_as_text, row_type_choices, \
    row_type_text, row_type_texts, type_column_width
from edit_cfg_json.descriptions import DECLARED_FORM, INFERRED_TEXT
from edit_cfg_json.type_options import CUT_MARK, TYPE_COLUMN_LIMIT
from .container_cfg import ByKeyCfg, LooseDictCfg, NestedCfg, UnionCfg
from .model_helpers import row_at
from .sample_cfg import FlatCfg, NoneCfg

FORMS_TEXT = 'dict[str, list[dict[str, int]] | dict[str, list[str]]]'
"""The declaration of `UnionCfg` that is longer than the column."""


@pytest.mark.parametrize('path, expected',
                         [(('columns',),
                           'dict[str, list[str] | list[list[str]]]'),
                          (('columns', 'flat'), 'list[str]'),
                          (('columns', 'nested'), 'list[list[str]]'),
                          (('columns', 'nested', '0'), 'list[str]'),
                          (('count',), 'int'), (('maybe',), 'None'),
                          (('ratio',), 'float'), (('items', '0'), 'str')])
def test_held_type(path: ConfigPath, expected: str) -> None:
    """Test each row holds the first of its types that its value fits.

    `ratio` holds `0` and is declared `float`, which is the case the value
    alone gets wrong, and the two values of `columns` hold each of the two
    lists the declaration allows.
    """
    assert row_at(EditModel(UnionCfg()), path).chosen_type.text == expected


def test_typed_value_holds() -> None:
    """Test typing into a row whose type is chosen leaves the type alone.

    The type is the user's choice, so a text that is no number, typed while
    `int` is chosen, is a value of the wrong type and not a choice of `str`.
    The text is read by the type chosen, so digits typed afterwards are a
    number again.
    """
    model = EditModel(UnionCfg())
    model.set_text(path=('count',), text='five')
    row = row_at(model, ('count',))
    assert row.value == 'five' and row.chosen_type.text == 'int'
    model.set_text(path=('count',), text='6')
    row = row_at(model, ('count',))
    assert row.value == 6 and row.chosen_type.text == 'int'


def test_given_value_holds() -> None:
    """Test a member given a value holds the type chosen for it.

    `Optional[int | str]` has the two states of a member that may hold
    nothing, and choosing a type that is not `None` is what gives it a value.
    """
    model = EditModel(UnionCfg())
    assert row_at(model, ('maybe',)).holds_nothing
    model.set_type(path=('maybe',), text='int')
    row = row_at(model, ('maybe',))
    assert row.value == 0 and row.chosen_type.text == 'int'


def test_entries_apart() -> None:
    """Test the named key of a dict holds the class and another key does not.

    An object is written as a dict, so the tree is what says which of the
    entries is one: the declaration allows both of them both types.
    """
    model = EditModel(ByKeyCfg())
    assert row_type_texts(row_at(model, ('hooks', 'main'))) == ('InnerCfg',
                                                                'str')
    assert row_type_text(row_at(model, ('hooks', 'main'))) == 'InnerCfg'
    assert row_type_text(row_at(model, ('hooks', 'note'))) == 'str'


def test_object_has_class() -> None:
    """Test an object row holds its class and says nothing as its value."""
    row = row_at(EditModel(NestedCfg()), ('inner',))
    assert row_type_text(row) == 'InnerCfg'
    assert row.value_text == ''


@pytest.mark.parametrize('path, expected',
                         [(('loose',), 'dict'), (('loose', 'cpu'), 'int'),
                          (('spread', '0'), 'dict')])
def test_inferred_type(path: ConfigPath, expected: str) -> None:
    """Test a row whose declaration says nothing holds what its value is.

    The line below it says so, because that is the one thing the type column
    cannot show about it.
    """
    row = row_at(EditModel(LooseDictCfg()), path)
    assert row.types == ()
    assert row_type_texts(row) == (expected,)
    assert INFERRED_TEXT in row.description


def test_long_type_cut() -> None:
    """Test a type longer than the column is cut and said whole below it."""
    row = row_at(EditModel(UnionCfg()), ('forms',))
    assert len(row_type_text(row)) == TYPE_COLUMN_LIMIT
    assert row_type_text(row).endswith(CUT_MARK)
    assert DECLARED_FORM.format(types=FORMS_TEXT) in row.description


def test_union_said_below() -> None:
    """Test a declaration of two types is said whole below the row.

    The column shows the one type the row holds, which for a member holding
    nothing is `None` and says nothing of what it could hold instead.
    """
    row = row_at(EditModel(NoneCfg()), ('name',))
    assert row_type_texts(row) == ('str', 'None')
    assert row_type_text(row) == 'None'
    assert row.description == DECLARED_FORM.format(types='str | None')


def test_choices_whole_text() -> None:
    """Test each type a pull-down lists is given as shown and as it is.

    The column cuts a long type, so what a pull-down shows is not enough to
    name the type chosen: the whole text is what the model is given.
    """
    row = row_at(EditModel(UnionCfg()), ('forms',))
    ((shown, whole),) = row_type_choices(row)
    assert shown == row_type_text(row) and whole == FORMS_TEXT


@pytest.mark.parametrize('config, expected',
                         [(FlatCfg(), len('str')),
                          (NoneCfg(), len('None')),
                          (UnionCfg(), TYPE_COLUMN_LIMIT)])
def test_column_width(config: Config, expected: int) -> None:
    """Test the column is as wide as the longest type, and no wider.

    Every type a row may hold is counted, and not only the one it holds, so
    that a row holding nothing is as wide as it will be once it holds a value.
    """
    assert type_column_width(EditModel(config)) == expected


def test_column_kept_folded() -> None:
    """Test folding a container away leaves the column as wide as it was."""
    model = EditModel(UnionCfg())
    width = type_column_width(model)
    model.toggle_fold(('columns',))
    assert type_column_width(model) == width


def test_dump_says_the_types() -> None:
    """Test the text rendering says the type of every row before its value."""
    printed = model_as_text(EditModel(UnionCfg()))
    assert 'count: int = 5\n' in printed
    assert 'maybe: None\n' in printed
    assert '    flat: list[str], 1 element\n' in printed
    assert '        0: list[str], 1 element\n' in printed
    assert 'ratio: float = 0\n' in printed


def test_cleared_key_is_none() -> None:
    """Test a named key holding no object holds `None` and offers it.

    The values of the dict are not declared to allow `None`, and the key is
    still one the dict need not have, so `None` is what it holds and the
    pull-down offers it after the types the declaration names.
    """
    model = EditModel(ByKeyCfg())
    model.remove_element(('hooks', 'main'))
    row = row_at(model, ('hooks', 'main'))
    assert row_type_text(row) == 'None'
    assert row_type_texts(row) == ('InnerCfg', 'str', 'None')


def test_inferred_follows() -> None:
    """Test a row with no usable declaration says the type it holds now.

    The text is still read by what the row held when the file was last agreed
    with, so a text that is no number stays a text, and the row says so.
    """
    model = EditModel(LooseDictCfg())
    model.set_text(path=('loose', 'cpu'), text='many')
    assert row_type_texts(row_at(model, ('loose', 'cpu'))) == ('str',)
