#! /usr/bin/env python3
"""Tests for choosing between lists, dicts and the other types of a node.

A node whose declaration allows a list or a dict beside another type holds
the one the user chooses with `EditModel.set_type`, and a container chosen
has rows of its own below it. These are about what is inside such a
container, what is copied into it, how long the choice lasts, what goes with
the rows a switch takes away, and which types the class would refuse.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from pathlib import Path
import pytest
from config_as_json import ConfigPath, JsonType
from edit_cfg_json import EditModel, row_chooses_type
from edit_cfg_json.type_choice import DICT_ONLY, NO_DICT_YET
from .choice_cfg import ContainerChoiceCfg, FlatteningCfg
from .model_helpers import row_at, row_paths, type_texts, written

FLAT = ('columns', 'flat')
"""Path of the entry of `ContainerChoiceCfg` that holds a `list[str]`."""

NESTED = ('columns', 'nested')
"""Path of the entry of `ContainerChoiceCfg` that holds a list of lists."""

LISTS = 'list[list[str]]'
"""The second type an entry of `columns` may hold, as Python spells it."""


def _types(model: EditModel, path: ConfigPath) -> list[str]:
    """Return the text of every type one node of one model is offered."""
    return type_texts(row_at(model, path))


def _held(model: EditModel, path: ConfigPath) -> str:
    """Return the type one node of one model holds, as Python spells it."""
    return row_at(model, path).chosen_type.text


@pytest.mark.parametrize('path, expected',
                         [(FLAT, True), (('either',), True),
                          (('layers', '0'), True), (('columns',), False),
                          (('held',), False), (('empty',), False)])
def test_who_chooses(path: ConfigPath, expected: bool) -> None:
    """Test which nodes offer to choose between containers and the rest.

    A member that the class would accept one type of only, after the dict
    check has had its say, has nothing to choose between.
    """
    assert row_chooses_type(row_at(EditModel(ContainerChoiceCfg()), path)) \
        is expected


@pytest.mark.parametrize('path, expected',
                         [(FLAT, 'list[str]'), (NESTED, LISTS),
                          ((*NESTED, '0'), 'list[str]'),
                          (('layers', '0'), 'list[str]')])
def test_value_says_first(path: ConfigPath, expected: str) -> None:
    """Test a container holds the first type its value fits, at the start."""
    assert _held(EditModel(ContainerChoiceCfg()), path) == expected


def test_complaint_answered() -> None:
    """Test an entry of a list of text can be made a list of lists of text.

    That is the complaint step 31 of the plan answers. The entry is given the
    empty list, and what its control adds is the empty list of text: what
    the class declares for that key is text, which is no element of the type
    the user chose instead.
    """
    model = EditModel(ContainerChoiceCfg())
    model.set_type(path=FLAT, text=LISTS)
    assert row_at(model, FLAT).value == []
    model.add_element(path=FLAT)
    assert row_at(model, FLAT).value == [[]]
    assert _types(model, (*FLAT, '0')) == ['list[str]']
    model.add_element(path=(*FLAT, '0'))
    model.set_text(path=(*FLAT, '0', '0'), text='x')
    assert model.validate().valid
    assert _held(model, FLAT) == LISTS


def test_choice_saved(tmp_path: Path) -> None:
    """Test the container chosen is what the file is written with."""
    out_file = tmp_path / 'out.json'
    model = EditModel(ContainerChoiceCfg(), out_file=out_file)
    model.set_type(path=FLAT, text=LISTS)
    model.add_element(path=FLAT)
    assert model.save().saved
    saved = written(out_file)
    assert isinstance(saved, dict)
    assert saved['columns'] == {'flat': [[]], 'nested': [['b']]}


def test_empty_keeps_choice() -> None:
    """Test an empty container keeps the type chosen through a pass.

    `[]` is a value of both kinds of list, so only the choice says which of
    the two it is, and a pass that leaves it empty leaves the choice too.
    """
    model = EditModel(ContainerChoiceCfg())
    model.set_type(path=FLAT, text=LISTS)
    assert model.validate().valid
    assert _held(model, FLAT) == LISTS
    model.add_element(path=FLAT)
    assert row_at(model, FLAT).value == [[]]


def test_new_entry_copied() -> None:
    """Test a new entry of the dict is a copy of the first, `list[str]`."""
    model = EditModel(ContainerChoiceCfg())
    model.add_element(path=('columns',), key='more')
    assert row_at(model, ('columns', 'more')).value == ['a']
    assert _held(model, ('columns', 'more')) == 'list[str]'


@pytest.mark.parametrize('text, value', [('list[int]', []), ('int', 5)])
def test_scalar_and_list(text: str, value: JsonType) -> None:
    """Test a member moves between a number and a list of numbers.

    A list is given the empty list and nothing of the number, and the number
    it held stays the number while no switch is made.
    """
    model = EditModel(ContainerChoiceCfg())
    model.set_type(path=('either',), text=text)
    assert row_at(model, ('either',)).value == value


def test_list_back_to_scalar() -> None:
    """Test a list chosen away takes its rows with it and gives a field.

    A node that held a container is edited in a field as soon as it holds a
    plain value again, whatever it held when the file was last agreed with.
    """
    model = EditModel(ContainerChoiceCfg())
    model.set_type(path=('either',), text='list[int]')
    model.add_element(path=('either',))
    assert ('either', '0') in row_paths(model)
    model.set_type(path=('either',), text='int')
    row = row_at(model, ('either',))
    assert row.value == 0 and row.editable
    assert ('either', '0') not in row_paths(model)
    assert not row_at(model, ('either',)).foldable


def test_fold_below_goes() -> None:
    """Test what was held for a node inside a switched container is gone.

    The fold of a container inside it and the search that had got to a value
    inside it go the way they go when an element is taken out.
    """
    model = EditModel(ContainerChoiceCfg())
    model.toggle_fold((*NESTED, '0'))
    model.find('b')
    assert row_at(model, (*NESTED, '0', '0')).found
    model.set_type(path=NESTED, text='list[str]')
    model.add_element(path=NESTED)
    assert not any(row.folded or row.found for row in model.rows)


def test_choice_moves() -> None:
    """Test the container chosen for an element goes with it as it moves."""
    model = EditModel(ContainerChoiceCfg())
    model.add_element(path=('layers',))
    model.set_type(path=('layers', '1'), text='dict[str, str]')
    model.move_element(path=('layers', '1'), later=False)
    assert _held(model, ('layers', '0')) == 'dict[str, str]'
    model.remove_element(('layers', '0'))
    assert _held(model, ('layers', '0')) == 'list[str]'


def test_dict_types_refused() -> None:
    """Test the dict check decides what a member may hold or be given.

    A member the class holds a dict in is offered nothing but a dict, which
    takes away the `remove` that produced *Not dictionary*, and one it holds
    no dict in is offered nothing but `None`. Each says why below its row.
    """
    model = EditModel(ContainerChoiceCfg())
    held = row_at(model, ('held',))
    assert _types(model, ('held',)) == ['dict[str, int]']
    assert not held.offer.remove
    assert DICT_ONLY.format(type='None') in held.description
    empty = row_at(model, ('empty',))
    assert _types(model, ('empty',)) == ['None'] and empty.holds_nothing
    assert NO_DICT_YET.format(type='dict[str, int]') in empty.description
    assert model.validate().valid


def test_validator_retypes() -> None:
    """Test a validator that changes a container's type changes the choice.

    A list of lists that a validator flattens is a list of text afterwards,
    and the rows inside it are built by that type rather than by the one the
    user chose before the pass.
    """
    model = EditModel(FlatteningCfg())
    model.set_type(path=('pairs',), text=LISTS)
    model.add_element(path=('pairs',))
    model.add_element(path=('pairs', '0'))
    model.set_text(path=('pairs', '0', '0'), text='x')
    assert model.validate().valid
    assert row_at(model, ('pairs',)).value == ['x']
    assert _held(model, ('pairs',)) == 'list[str]'
    assert _types(model, ('pairs', '0')) == ['str']
