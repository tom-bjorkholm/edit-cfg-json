#! /usr/bin/env python3
"""Tests for taking one configuration apart into nodes and putting it back."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from io import StringIO
from config_as_json import Config, ConfigPath, JsonType
import pytest
from edit_cfg_json.tree import OPEN_AT_MOST, assembled, child_values, \
    config_nodes, container_text, file_values, flat_values, is_container, \
    member_values, optional_members, optional_paths, ordered_names, \
    owner_path, path_text, rows_below, selects, shown_values, starts_folded, \
    text_path, under_dict
from .container_cfg import ByKeyCfg, ConfigListCfg, DeepConfigCfg, \
    InnerCfg, NestedCfg, NullNestedCfg, OmitNestedCfg, OwnedOptionCfg, TreeCfg
from .sample_cfg import FlatCfg, OmitCfg


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


def _paths(config: Config, members: dict[str, JsonType]) -> list[ConfigPath]:
    """Return the path of every node of one configuration, in row order."""
    return [path for path, _ in
            flat_values(members=members, nodes=config_nodes(config))]


def test_flat_is_a_tree() -> None:
    """Test a configuration is taken apart depth first, container first."""
    members: dict[str, JsonType] = {'rules': [{'low': 1}],
                                    'groups': {'red': ['a']}, 'answer': 3}
    assert _paths(TreeCfg(), members) == \
        [('rules',), ('rules', '0'), ('rules', '0', 'low'), ('groups',),
         ('groups', 'red'), ('groups', 'red', '0'), ('answer',)]


def test_nested_is_walked() -> None:
    """Test a nested configuration object holds rows of its own members."""
    members: dict[str, JsonType] = {'inner': {'height': 6, 'width': 4},
                                    'limits': {'low': 1}}
    assert _paths(NestedCfg(), members) == \
        [('inner',), ('inner', 'width'), ('inner', 'height'), ('limits',),
         ('limits', 'low')]


def test_nested_own_order() -> None:
    """Test a nested object shows its members in its own declared order.

    The dict it writes is sorted, so `height` comes first in the file and
    second in the editor: the class that owns the members is what says in
    which order they are read.
    """
    members: dict[str, JsonType] = {'inner': {'height': 6, 'width': 4},
                                    'limits': {'low': 1}}
    written = members['inner']
    assert isinstance(written, dict)
    assert list(written) == ['height', 'width']
    assert _paths(NestedCfg(), members)[1:3] == \
        [('inner', 'width'), ('inner', 'height')]


def test_list_of_configs() -> None:
    """Test every element of a list of configuration objects is a node.

    That is the ordinary shape of a real configuration, so the member stays a
    container that can be folded and says how much it holds, and each object
    inside it holds rows of its own.
    """
    members: dict[str, JsonType] = {'outputs': [{'width': 4, 'height': 6},
                                                {'width': 1, 'height': 2}],
                                    'answer': 3}
    assert _paths(ConfigListCfg(), members) == \
        [('outputs',), ('outputs', '0'), ('outputs', '0', 'width'),
         ('outputs', '0', 'height'), ('outputs', '1'),
         ('outputs', '1', 'width'), ('outputs', '1', 'height'), ('answer',)]


def test_deep_nesting() -> None:
    """Test a nested object inside a nested object is found as well."""
    inner: JsonType = {'parts': {'one': {'width': 4, 'height': 6}},
                       'label': 'deep'}
    members: dict[str, JsonType] = {'outputs': [inner]}
    assert ('outputs', '0', 'parts', 'one', 'width') in \
        _paths(DeepConfigCfg(), members)


def test_missing_is_a_leaf() -> None:
    """Test a declared member that holds no object holds no rows either."""
    members: dict[str, JsonType] = {'inner': None, 'answer': 3}
    assert _paths(NullNestedCfg(), members) == [('inner',), ('answer',)]


def test_config_nodes_found() -> None:
    """Test every configuration object of a tree is found by its path."""
    nodes = config_nodes(NestedCfg())
    assert set(nodes) == {(), ('inner',)}
    assert nodes[('inner',)].config_type is InnerCfg
    assert nodes[('inner',)].config is not None


def test_absent_declared() -> None:
    """Test a member that holds no object still says which class it wants."""
    nodes = config_nodes(NullNestedCfg())
    assert nodes[('inner',)].config_type is InnerCfg
    assert nodes[('inner',)].config is None


def test_omitted_declared() -> None:
    """Test a member the class leaves out of JSON is declared all the same.

    It has no value to be a row of, so nothing shows it, but where it is is
    still known: what decides whether it has a row is what is written.
    """
    assert config_nodes(OmitNestedCfg())[('inner',)].config is None


def test_keyed_member_emptied() -> None:
    """Test a keyed dict member holding no dict has no node inside it.

    A `DICT_VALUE_BY_KEY` declaration names one key of a dict, so a member
    that holds no dict at all holds no such key either. No configuration that
    `config_as_json` accepts is in that state, and an object whose members were
    assigned by hand can be: the tree answers for the object it is given
    rather than assuming it was validated.
    """
    config = ByKeyCfg()
    setattr(config, 'hooks', None)
    assert set(config_nodes(config)) == {()}


def test_nothing_is_nested() -> None:
    """Test a class that declares no nesting has only itself as a node."""
    assert set(config_nodes(FlatCfg())) == {()}


@pytest.mark.parametrize('path, owner',
                         [(('answer',), ()), (('outputs',), ()),
                          (('outputs', '0'), ()),
                          (('outputs', '0', 'width'), ('outputs', '0'))])
def test_owner_path(path: ConfigPath, owner: ConfigPath) -> None:
    """Test the object owning a node is the innermost one it is inside."""
    assert owner_path(path=path, nodes=config_nodes(ConfigListCfg())) == owner


def test_ordered_names() -> None:
    """Test the members are ordered as declared, and no name is lost."""
    config = TreeCfg()
    members: dict[str, JsonType] = {'answer': 3, 'groups': {}, 'rules': [],
                                    'extra': 1}
    assert ordered_names(config=config, members=members) == \
        ['rules', 'groups', 'answer', 'extra']


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


def test_optional_asked() -> None:
    """Test the class is what says which of its members are optional."""
    assert optional_members(OmitCfg()) == frozenset({'optional'})
    assert optional_members(FlatCfg()) == frozenset()


def test_optional_by_path() -> None:
    """Test each object of a tree says which of its own members it omits.

    The nested object leaves `note` out of its own JSON and the class holding
    it does not leave out the member of that name, which is what says that
    `_omit_none_from_json()` belongs to the class that owns the subtree.
    """
    assert optional_paths(config_nodes(OwnedOptionCfg())) == \
        frozenset({('inner', 'note')})


def test_left_out_shown() -> None:
    """Test the members one object left out of its JSON are added back.

    They hold nothing, which is why the object wrote nothing for them, and
    they are members of it all the same: a member with no row could never be
    given a value.
    """
    config = OmitCfg()
    written = member_values(config=config, stderr_file=StringIO())
    assert 'optional' not in written
    assert shown_values(config=config, members=written) == \
        {'first': 1, 'optional': None, 'last': 2}


def test_left_out_in_place() -> None:
    """Test such a member keeps the place its own declaration gives it."""
    config = OmitCfg()
    held = shown_values(config=config,
                        members=member_values(config=config,
                                              stderr_file=StringIO()))
    assert ordered_names(config=config, members=held) == ['first', 'optional',
                                                          'last']


def test_left_out_has_a_node() -> None:
    """Test a nested member the class leaves out is a node of the tree.

    It is the case that had no row at all before: the class writes nothing for
    it, so nothing about it reached the values the rows are built from.
    """
    config = OmitNestedCfg()
    nodes = config_nodes(config)
    flat = flat_values(members=member_values(config=config,
                                             stderr_file=StringIO()),
                       nodes=nodes)
    assert dict(flat)[('inner',)] is None
    assert nodes[('inner',)].config is None


def test_inner_left_out_shown() -> None:
    """Test a member a nested object leaves out is a node of the tree too.

    The class that may leave a member out is the class that owns it, so this
    has to hold at every depth and not only at the outermost one.
    """
    config = OwnedOptionCfg()
    config.inner.note = None
    flat = flat_values(members=member_values(config=config,
                                             stderr_file=StringIO()),
                       nodes=config_nodes(config))
    assert dict(flat)[('inner', 'note')] is None
    assert dict(flat)[('inner',)] == {'note': None, 'width': 4}


def test_file_leaves_out() -> None:
    """Test the buffer is written as the file holds it.

    A member that holds nothing and that its class leaves out of the file is
    not in the file, so it is not in what that class is asked to read: what a
    validation pass is given is the document that a save would write.
    """
    omitted = optional_paths(config_nodes(OmitCfg()))
    values = {'first': 1, 'optional': None, 'last': 2}
    assert file_values(members=values, omitted=omitted) == {'first': 1,
                                                            'last': 2}


def test_file_keeps_a_value() -> None:
    """Test such a member is written as soon as it holds anything at all."""
    omitted = optional_paths(config_nodes(OmitCfg()))
    values: dict[str, JsonType] = {'first': 1, 'optional': '', 'last': 2}
    assert file_values(members=values, omitted=omitted) == values


def test_file_keeps_plain_key() -> None:
    """Test a key of an ordinary dict is kept whatever it is called.

    Only a member of a configuration object can be left out of the file, and
    the paths asked about are the ones the objects of the tree answered with,
    so a dictionary entry that holds nothing is never mistaken for one.
    """
    omitted = optional_paths(config_nodes(OmitCfg()))
    values: dict[str, JsonType] = {'first': {'optional': None}, 'last': 2}
    assert file_values(members=values, omitted=omitted) == values
