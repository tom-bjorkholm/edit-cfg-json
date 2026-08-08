#! /usr/bin/env python3
"""Tests for taking one configuration apart into nodes and putting it back."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from config_as_json import ConfigPath, JsonType
import pytest
from edit_cfg_json.tree import OPEN_AT_MOST, assembled, child_values, \
    container_text, dict_nodes, flat_values, is_container, is_nested, \
    nested_selectors, path_text, rows_below, selects, starts_folded, \
    text_path, under_dict
from .container_cfg import ConfigListCfg, NestedCfg, TreeCfg
from .sample_cfg import FlatCfg


@pytest.mark.parametrize('path, text', [(('name',), 'name'),
                                        (('tags', '0'), 'tags.0'),
                                        (('a', 'b', 'c'), 'a.b.c')])
def test_path_text(path: ConfigPath, text: str) -> None:
    """Test a path is written with a dot between its steps."""
    assert path_text(path) == text
    assert text_path(text) == path


@pytest.mark.parametrize('value, held', [([1, 2], True), ({'a': 1}, True),
                                         ('text', False), (3, False),
                                         (None, False), ([], True),
                                         ({}, True)])
def test_is_container(value: JsonType, held: bool) -> None:
    """Test a list and a dict hold other values and nothing else does."""
    assert is_container(value) is held


@pytest.mark.parametrize('value, text', [([], '0 elements'),
                                         (['a'], '1 element'),
                                         (['a', 'b'], '2 elements'),
                                         ({}, '0 entries'),
                                         ({'a': 1}, '1 entry'),
                                         ({'a': 1, 'b': 2}, '2 entries')])
def test_container_text(value: JsonType, text: str) -> None:
    """Test a container says how much it holds, counted the right way."""
    assert container_text(value) == text


def test_list_children() -> None:
    """Test a list element is addressed by its index written out."""
    assert child_values(path=('tags',), value=['a', 'b']) == \
        [(('tags', '0'), 'a'), (('tags', '1'), 'b')]


def test_dict_children() -> None:
    """Test a dict entry is addressed by its key."""
    assert child_values(path=('limits',), value={'low': 1}) == \
        [(('limits', 'low'), 1)]


def test_value_has_no_child() -> None:
    """Test a value that holds nothing has no nodes below it."""
    assert not child_values(path=('name',), value='text')


def test_flat_is_a_tree() -> None:
    """Test a configuration is taken apart depth first, container first."""
    config = TreeCfg()
    members: dict[str, JsonType] = {'rules': [{'low': 1}],
                                    'groups': {'red': ['a']}, 'answer': 3}
    assert [path for path, _ in flat_values(members=members,
                                            order=list(members))] == \
        [('rules',), ('rules', '0'), ('rules', '0', 'low'), ('groups',),
         ('groups', 'red'), ('groups', 'red', '0'), ('answer',)]
    assert config.answer == 3


def test_nested_is_one_node() -> None:
    """Test a declared nested configuration object is not taken apart."""
    members: dict[str, JsonType] = {'inner': {'width': 4},
                                    'limits': {'low': 1}}
    nested = nested_selectors(NestedCfg())
    assert nested == frozenset({('inner',)})
    assert [path for path, _ in flat_values(members=members,
                                            order=list(members),
                                            nested=nested)] == \
        [('inner',), ('limits',), ('limits', 'low')]


def test_list_of_configs() -> None:
    """Test a list of configuration objects is a list of one node each.

    That is the ordinary shape of a real configuration, so the member stays a
    container that can be folded and says how much it holds, and each object
    inside it is one node.
    """
    members: dict[str, JsonType] = {'outputs': [{'encoding': 'utf-8'},
                                                {'encoding': 'latin-1'}]}
    nested = nested_selectors(ConfigListCfg())
    assert nested == frozenset({('outputs', '[')})
    assert [path for path, _ in flat_values(members=members,
                                            order=list(members),
                                            nested=nested)] == \
        [('outputs',), ('outputs', '0'), ('outputs', '1')]


def test_nothing_is_nested() -> None:
    """Test a class that declares no nesting has no nested node at all."""
    assert not nested_selectors(FlatCfg())


@pytest.mark.parametrize('selector, path, about',
                         [((('a',)), ('a',), True),
                          ((('a',)), ('b',), False),
                          ((('a', '[')), ('a', '0'), True),
                          ((('a', '[')), ('a', 'key'), True),
                          ((('a', '[')), ('a',), False),
                          ((('a', '[', 'c')), ('a', '0', 'c'), True),
                          ((('a', 'b')), ('a', 'c'), False)])
def test_selects(selector: ConfigPath, path: ConfigPath, about: bool) -> None:
    """Test a selector addresses a node of the same shape and no other."""
    assert selects(selector=selector, path=path) is about
    assert is_nested(path=path, nested=[selector]) is about


def test_rows_below() -> None:
    """Test what a container would add is every row below it.

    It is counted from the rows there are and not from the value, because a
    declared configuration object inside it is one row however much it holds.
    """
    paths = [('a',), ('a', '0'), ('a', '0', 'x'), ('a', '1'), ('b',)]
    assert rows_below(path=('a',), paths=paths) == 3
    assert rows_below(path=('a', '0'), paths=paths) == 1
    assert rows_below(path=('b',), paths=paths) == 0


def test_long_starts_folded() -> None:
    """Test a container of more rows than the window can spare is folded."""
    many = [('a',)] + [('a', str(index)) for index in range(OPEN_AT_MOST + 1)]
    assert starts_folded(path=('a',), paths=many)
    assert not starts_folded(path=('a',), paths=many[:-1])


def test_dict_nodes_only() -> None:
    """Test only the value of a dictionary key can have a converter.

    `config_as_json` applies a parse converter while it decodes an object, so
    a value inside a list is never converted and a value inside a dict is.
    """
    members: dict[str, JsonType] = {'tags': ['a'], 'limits': {'low': 1}}
    assert [path for path, _ in dict_nodes(members)] == \
        [('tags',), ('limits',), ('limits', 'low')]


def test_under_dict() -> None:
    """Test a member counts as a value of the outermost dictionary."""
    values: dict[ConfigPath, JsonType] = {('tags',): ['a'],
                                          ('limits',): {'low': 1}}
    assert under_dict(path=('tags',), values=values)
    assert under_dict(path=('limits', 'low'), values=values)
    assert not under_dict(path=('tags', '0'), values=values)


@pytest.mark.parametrize('children, as_list, value',
                         [([('0', 'a'), ('1', 'b')], True, ['a', 'b']),
                          ([('low', 1)], False, {'low': 1}),
                          ([], True, []), ([], False, {})])
def test_assembled(children: list[tuple[str, JsonType]], as_list: bool,
                   value: JsonType) -> None:
    """Test a container is put together again from what its children hold."""
    assert assembled(children=children, as_list=as_list) == value
