#! /usr/bin/env python3
"""Tests for what the class of a configuration says its members are.

The three sources are tested apart from each other, because each of them
covers a pattern the others do not: a dataclass records real types, a class
level annotation records one without a dataclass around it, and the ordinary
`Config` pattern records nothing at all and is read from the source.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from dataclasses import dataclass, field
from io import StringIO
from typing import Optional
import pytest
from config_as_json import Config, ConfigPath, JsonType
from edit_cfg_json.leaf_value import empty_value
from edit_cfg_json.member_types import KeptTypes, attribute_texts, \
    declared_hints, member_types, node_types, nothing_allowed
from edit_cfg_json.tree import ConfigNode, config_nodes, flat_values, \
    member_values
from edit_cfg_json.type_options import NONE_TYPE, TypeOption, type_options
from .container_cfg import LooseDictCfg, UnionCfg


class WrittenInInit:  # pylint: disable=too-few-public-methods
    """A class in the ordinary pattern, annotating attributes of `self`."""

    def __init__(self) -> None:
        """Assign one member of each kind that a declaration can name."""
        self.name: str = 'written'
        self.answer: int = 7
        self.ratio: float = 0
        self.verbose: bool = False
        self.title: Optional[str] = None
        self.tags: list[str] = []
        self.limits: dict[str, int] = {}


class Unannotated:  # pylint: disable=too-few-public-methods
    """A class assigning a member without saying what it holds."""

    def __init__(self) -> None:
        """Assign the one member that has no annotation at all."""
        self.plain = 'nothing says what this is'


class WrittenElsewhere(WrittenInInit):  # pylint: disable=R0903
    """A class declaring a member in a method that `__init__` calls.

    A class is free to put its declarations in a method of its own, and the
    annotations there are exactly as real as the ones in `__init__`. The
    editor reads the source of the whole class for that reason.
    """

    def __init__(self) -> None:
        """Assign what the base declares and then one member more."""
        super().__init__()
        self._declare_more()

    def _declare_more(self) -> None:
        """Assign the member that is not declared in `__init__`."""
        self.extra: bool = True


class Annotated:  # pylint: disable=too-few-public-methods
    """A class with class level annotations and no `__init__` of its own."""

    name: str = 'annotated'
    answer: Optional[int] = None


@dataclass
class Recorded:  # pylint: disable=too-few-public-methods
    """A dataclass, whose fields record their types at runtime."""

    name: str = 'recorded'
    tags: list[str] = field(default_factory=list)


def _texts(options: tuple[TypeOption, ...]) -> list[str]:
    """Return the text of every type one declaration allows."""
    return [option.text for option in options]


def _tree(config: Config) -> tuple[dict[ConfigPath, ConfigNode],
                                   list[tuple[ConfigPath, JsonType]]]:
    """Return the objects of one configuration and every node of it."""
    nodes = config_nodes(config)
    return nodes, flat_values(members=member_values(config,
                                                    stderr_file=StringIO()),
                              nodes=nodes)


@pytest.mark.parametrize('name, expected',
                         [('name', ['str']), ('answer', ['int']),
                          ('ratio', ['float']), ('verbose', ['bool']),
                          ('title', ['str', 'None']),
                          ('tags', ['list[str]']),
                          ('limits', ['dict[str, int]'])])
def test_read_from_source(name: str, expected: list[str]) -> None:
    """Test each annotation on `self` says what its member holds.

    `ratio` is the case the value cannot answer: its default is written `0`,
    which is a whole number, while the member is declared to hold a number.
    """
    assert _texts(member_types(WrittenInInit)[name]) == expected


def test_unannotated() -> None:
    """Test a member with no annotation is a member nothing says about."""
    assert 'plain' not in member_types(Unannotated)


def test_private_is_no_member() -> None:
    """Test a private attribute is never one of the members."""
    assert not any(name.startswith('_')
                   for name in member_types(WrittenElsewhere))


def test_read_from_any_method() -> None:
    """Test a member declared outside `__init__` is read as well."""
    assert _texts(member_types(WrittenElsewhere)['extra']) == ['bool']


def test_base_is_read_too() -> None:
    """Test the members a base class declares are read with the rest."""
    assert _texts(member_types(WrittenElsewhere)['name']) == ['str']


def test_class_annotation() -> None:
    """Test a class level annotation says what its member holds."""
    found = member_types(Annotated)
    assert _texts(found['name']) == ['str']
    assert _texts(found['answer']) == ['int', 'None']


def test_dataclass_field_read() -> None:
    """Test the fields of a dataclass record the types they declare."""
    found = member_types(Recorded)
    assert _texts(found['name']) == ['str']
    assert _texts(found['tags']) == ['list[str]']


class Quoted:  # pylint: disable=too-few-public-methods
    """A class whose annotation is written in quotation marks."""

    def __init__(self) -> None:
        """Assign the one member whose annotation is a text."""
        self.title: 'Optional[str]' = None


def test_quoted_annotation() -> None:
    """Test an annotation in quotation marks is read as what it names.

    A forward reference is a text in the source, so writing that source out
    again gives a text of a text. It means the same thing as the annotation
    written without the quotation marks.
    """
    assert attribute_texts(Quoted)['title'] == 'Optional[str]'
    assert _texts(member_types(Quoted)['title']) == ['str', 'None']


def test_texts_are_as_written() -> None:
    """Test the annotations are read as the text the source writes."""
    assert attribute_texts(WrittenInInit)['title'] == 'Optional[str]'


def test_unreadable_source() -> None:
    """Test a class with no source to read costs its members nothing worse.

    A class made by `type` has no source anywhere, which is what a class
    defined in an interactive session, by `exec` and in a frozen program all
    amount to. The editor does without what it cannot find out.
    """
    made = type('MadeAtRuntime', (), {})
    assert attribute_texts(made) == {}
    assert not declared_hints(made)


class Unresolvable:  # pylint: disable=too-few-public-methods
    """A class one of whose annotations names nothing that exists."""

    def __init__(self) -> None:
        """Assign one member that resolves and one that cannot."""
        self.name: str = 'here'
        self.other: 'NoSuchTypeAnywhere' = 'there'  # type: ignore[name-defined] # noqa: E501,F821


def test_one_bad_annotation() -> None:
    """Test an annotation that will not resolve leaves the others alone."""
    found = member_types(Unresolvable)
    assert _texts(found['name']) == ['str']
    assert 'other' not in found


class UsesNothing:  # pylint: disable=too-few-public-methods
    """A class whose one annotation names a type the editor cannot use."""

    def __init__(self) -> None:
        """Assign the one member, a pair the editor can make nothing of."""
        self.pair: tuple[int, int] = (1, 2)


def test_unusable_is_left_out() -> None:
    """Test a member declared as nothing usable is one nothing says about."""
    assert 'pair' not in member_types(UsesNothing)


@pytest.mark.parametrize('kind, expected',
                         [(str, ''), (int, 0), (float, 0.0), (bool, False),
                          (list, []), (dict, {}), (None, None)])
def test_empty_value_of_kind(kind: Optional[type], expected: object) -> None:
    """Test the value of each kind that says no more than its kind."""
    assert empty_value(kind) == expected


def test_empty_is_fresh() -> None:
    """Test two empty values of one kind are not the same object.

    A list and a dict are values that the next edit would otherwise reach
    through, so every member given one has to be given one of its own.
    """
    assert empty_value(list) is not empty_value(list)


class BadClassHint:  # pylint: disable=too-few-public-methods
    """A class whose class level annotation names nothing that exists.

    A name imported under `if TYPE_CHECKING` is the way this arises for real:
    it exists while the type checker reads the file and never at runtime. What
    it costs the class is what the class level annotations would have added,
    and the annotations that its source writes are read as usual.
    """

    later: 'NoSuchTypeAnywhere'  # type: ignore[name-defined] # noqa: F821

    def __init__(self) -> None:
        """Assign the one member that the source annotates."""
        self.name: str = 'here'


def test_bad_class_annotation() -> None:
    """Test a class annotation that will not resolve costs only itself.

    `typing.get_type_hints` resolves every annotation of a class at once, so
    one that fails takes all of them with it. The source of the class is a
    separate source and is read afresh, which is what leaves the members that
    it annotates with their declarations.
    """
    found = member_types(BadClassHint)
    assert _texts(found['name']) == ['str']
    assert 'later' not in declared_hints(BadClassHint)


def test_nothing_to_step_into() -> None:
    """Test a value inside a member with no declared type says nothing.

    The declaration of the member is what a node inside it is reached
    through, one step per step of the path, so a member that has no
    declaration has none to step into and every node inside it is one that
    the class said nothing about. The two containers a node can be inside
    answer alike, and so does a node two steps in.
    """
    nodes, flat = _tree(LooseDictCfg())
    assert {('loose', 'cpu'), ('spread', '0'),
            ('spread', '0', 'cpu')} <= set(dict(flat))
    assert node_types(nodes=nodes, flat=flat) == {}


def _union_types() -> dict[ConfigPath, list[str]]:
    """Return what the classes of `UnionCfg` allow each of its nodes."""
    nodes, flat = _tree(UnionCfg())
    return {path: _texts(options)
            for path, options in node_types(nodes=nodes, flat=flat).items()}


@pytest.mark.parametrize('path, expected',
                         [(('columns', 'flat'), ['list[str]',
                                                 'list[list[str]]']),
                          (('columns', 'flat', '0'), ['str']),
                          (('columns', 'nested', '0'), ['list[str]']),
                          (('columns', 'nested', '0', '0'), ['str']),
                          (('count',), ['int', 'str']),
                          (('items', '0'), ['str', 'None'])])
def test_steps_through_union(path: ConfigPath, expected: list[str]) -> None:
    """Test a node inside a union of containers is reached through its own.

    Each value of `columns` may be either list, and the elements of each are
    what the list that value really is holds: text in one of them and a list
    of text in the other.
    """
    assert _union_types()[path] == expected


@pytest.mark.parametrize('path, expected',
                         [(('maybe',), True), (('count',), False),
                          (('colour',), True), (('items', '0'), True),
                          (('columns', 'flat'), False)])
def test_nothing_allowed(path: ConfigPath, expected: bool) -> None:
    """Test which nodes have the two states of a value and of nothing.

    A node whose type the user chooses has them wherever `None` is one of its
    types, which is `Optional[int | str]`, an optional enum, and an element of
    `list[Optional[str]]` as much as a member. A value inside a container
    whose type is not chosen never has them.
    """
    nodes, flat = _tree(UnionCfg())
    options = node_types(nodes=nodes, flat=flat).get(path, ())
    assert nothing_allowed(path=path, options=options, nodes=nodes) is expected


@pytest.mark.parametrize('refreshing, expected',
                         [(False, ['list[str]']), (True, ['str'])])
def test_steps_through_choice(refreshing: bool, expected: list[str]) -> None:
    """Test a container is stepped into through the type the user chose.

    The choice stands while the user edits, whatever the value says, and a
    validation pass that leaves a value the choice does not fit makes the
    value say which type it is, for the rows inside it as well.
    """
    nodes, flat = _tree(UnionCfg())
    chosen = type_options(list[list[str]])[0]
    kept = KeptTypes(chosen={('columns', 'flat'): chosen},
                     refreshing=refreshing)
    found = node_types(nodes=nodes, flat=flat, kept=kept)
    assert _texts(found[('columns', 'flat', '0')]) == expected


def test_only_none_is_state() -> None:
    """Test a node offered `None` and nothing else holds nothing as a state.

    The class would accept nothing else there, so no field is given it.
    """
    nodes, _ = _tree(UnionCfg())
    assert nothing_allowed(path=('count',), options=(NONE_TYPE,), nodes=nodes)
