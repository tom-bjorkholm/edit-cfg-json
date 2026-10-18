#! /usr/bin/env python3
"""Tests for choosing the type of a node, as a model does it.

A node whose declaration allows more than one plain type, or a plain type and
`None`, holds the one the user chooses with `EditModel.set_type`. A type the
editor cannot make a value of is offered only where the node holds it. These
are about what a model makes of a choice: what the node holds afterwards, how
its text is read, how long the choice lasts, which nodes offer it, and which
types are not offered because the class would refuse them.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from pathlib import Path
from typing import Optional
import pytest
from config_as_json import ConfigPath, JsonType
from edit_cfg_json import EditModel, row_chooses, row_chooses_type, \
    rows_shape
from edit_cfg_json.type_choice import NOT_CONVERTED_FORM, NOT_MADE
from .choice_cfg import ChoiceCfg, ConvertedCfg, LenientCfg, NumberingCfg, \
    UnmadeCfg
from .model_helpers import row_at, type_texts, written

SIZES = ('sizes',)
"""Path of the list of `ChoiceCfg` whose elements may be `int` or `float`."""

PLACE = ('place',)
"""Path of the member of `UnmadeCfg` that may hold a number or a path."""


def _held(model: EditModel, path: ConfigPath) -> str:
    """Return the type one node of one model holds, as Python spells it."""
    return row_at(model, path).chosen_type.text


def _chosen(path: ConfigPath, text: str) -> EditModel:
    """Return a model of `ChoiceCfg` with one type chosen in it."""
    model = EditModel(ChoiceCfg())
    model.set_type(path=path, text=text)
    return model


@pytest.mark.parametrize('path, text, value',
                         [(('width',), 'str', '80'), (('ratio',), 'float', 5),
                          (('flag',), 'str', 'true'),
                          (('maybe',), 'float', 0.0),
                          (('mode',), 'int', 0),
                          (('colour',), 'Colour', 'RED'),
                          (('levels', '1'), 'int', 0),
                          (('notes', '1'), 'str', '')])
def test_switched(path: ConfigPath, text: str, value: JsonType) -> None:
    """Test a node chosen another type holds what still fits, or its empty.

    A text that means a value of the new type is read as one, and everything
    else, `None` among it, is the empty value of the type chosen.
    """
    model = _chosen(path=path, text=text)
    row = row_at(model, path)
    assert row.chosen_type.text == text
    assert row.value == value and type(row.value) is type(value)


def test_text_read_by_choice() -> None:
    """Test the text of a node is read as a value of the type chosen.

    `5` is a number while `int` is chosen and a text while `str` is, and the
    choice is what decides, not what the member held when it was loaded.
    """
    model = _chosen(path=('width',), text='str')
    model.set_text(path=('width',), text='5')
    assert row_at(model, ('width',)).value == '5'
    model.set_type(path=('width',), text='int')
    assert row_at(model, ('width',)).value == 5


def test_choice_outlives() -> None:
    """Test a choice the value cannot say lasts through a validation pass.

    `5` is an `int` and a `float`, so only the choice says which of the two
    the member holds, and a pass that leaves `5` leaves the choice too.
    """
    model = _chosen(path=('ratio',), text='float')
    assert model.validate().valid
    assert _held(model, ('ratio',)) == 'float'


def test_typing_keeps_choice() -> None:
    """Test a text of the wrong type typed into a node changes no choice."""
    model = EditModel(ChoiceCfg())
    model.set_text(path=('width',), text='wide')
    assert row_at(model, ('width',)).value == 'wide'
    assert _held(model, ('width',)) == 'int'


def test_validator_retypes() -> None:
    """Test a validator that changes the type of a value changes the choice.

    A choice lasts until a validation pass leaves a value it does not fit,
    and the editor then shows the type the application made of the value.
    """
    model = EditModel(NumberingCfg())
    model.set_type(path=('width',), text='str')
    model.set_text(path=('width',), text='7')
    assert model.validate().valid
    assert row_at(model, ('width',)).value == 7
    assert _held(model, ('width',)) == 'int'


def test_none_is_a_type() -> None:
    """Test choosing `None` takes the value and the field away, and back.

    The row then says nothing where a value would be, because its type says
    `None`, and choosing a type that is not `None` gives it a field again.
    """
    model = _chosen(path=('maybe',), text='float')
    assert row_at(model, ('maybe',)).editable
    model.set_type(path=('maybe',), text='None')
    row = row_at(model, ('maybe',))
    assert row.holds_nothing and not row.editable and row.value_text == ''


def test_element_nothing() -> None:
    """Test an element whose type is chosen has the state of holding nothing.

    It is still an element, which the control that removes it says, and
    nothing beside choosing a type gives it a value.
    """
    row = row_at(EditModel(ChoiceCfg()), ('notes', '1'))
    assert row.holds_nothing and not row.editable
    assert row.offer.remove and not row.offer.extend


@pytest.mark.parametrize('path, expected',
                         [(('width',), True), (('maybe',), True),
                          (('levels', '0'), True), (('levels',), False),
                          (('hosts',), True)])
def test_who_chooses(path: ConfigPath, expected: bool) -> None:
    """Test which nodes offer their type to be chosen.

    A member declared to allow a list or nothing is one of them, and offers
    no control that adds for its two states.
    """
    row = row_at(EditModel(ChoiceCfg()), path)
    assert row_chooses_type(row) is expected
    assert not (expected and row.offer.extend)


def test_list_member_chosen() -> None:
    """Test a member that may hold a list or nothing is given one by type.

    Choosing `list[str]` gives it the empty list, whose own control then adds
    the element its type says, and choosing `None` takes the list away again.
    """
    model = _chosen(path=('hosts',), text='list[str]')
    assert row_at(model, ('hosts',)).value == []
    model.add_element(path=('hosts',))
    assert row_at(model, ('hosts',)).value == ['']
    model.set_type(path=('hosts',), text='None')
    assert row_at(model, ('hosts',)).holds_nothing
    assert ('hosts', '0') not in [row.path for row in model.rows]


@pytest.mark.parametrize('path, text',
                         [(('width',), 'float'), (('hosts',), 'list[int]'),
                          (('levels',), 'list[int | str]')])
def test_choice_refused(path: ConfigPath, text: str) -> None:
    """Test a type a node is not offered, and a node offering none, refuse."""
    with pytest.raises(ValueError):
        EditModel(ChoiceCfg()).set_type(path=path, text=text)


def test_unknown_node() -> None:
    """Test a path that addresses nothing is refused as such."""
    with pytest.raises(KeyError):
        EditModel(ChoiceCfg()).set_type(path=('nowhere',), text='int')


def test_choice_is_an_edit() -> None:
    """Test choosing another type drops the verdict, as any edit does."""
    model = EditModel(ChoiceCfg())
    model.validate()
    model.set_type(path=('width',), text='str')
    assert model.verdict is None and model.dirty


def test_same_type_no_edit() -> None:
    """Test choosing the type a node already holds changes nothing."""
    model = EditModel(ChoiceCfg())
    verdict = model.validate()
    model.set_type(path=('width',), text='int')
    assert model.verdict is verdict and not model.dirty


def test_values_follow_type() -> None:
    """Test a node chosen to hold true or false is offered the two words.

    That is a different row from one holding text, which the shape of the
    rows says, so a backend makes its widgets again for it.
    """
    model = EditModel(ChoiceCfg())
    before = rows_shape(model)
    model.set_type(path=('flag',), text='str')
    assert not row_chooses(row_at(model, ('flag',)))
    assert rows_shape(model) != before
    model.set_type(path=('flag',), text='bool')
    assert row_at(model, ('flag',)).value is True


def test_choice_moves() -> None:
    """Test a choice goes with the element when it changes places."""
    model = _chosen(path=(*SIZES, '0'), text='float')
    model.move_element(path=(*SIZES, '0'), later=True)
    assert _held(model, (*SIZES, '1')) == 'float'
    assert _held(model, (*SIZES, '0')) == 'int'


def test_choice_leaves() -> None:
    """Test a choice goes with the element that is taken out.

    The element after it moves into its place, and holds the type its own
    value says rather than the type chosen for the one that is gone.
    """
    model = _chosen(path=(*SIZES, '0'), text='float')
    model.remove_element((*SIZES, '0'))
    assert row_at(model, (*SIZES, '0')).value == 2
    assert _held(model, (*SIZES, '0')) == 'int'


def test_choice_saved(tmp_path: Path) -> None:
    """Test the type chosen is the type the file is written with."""
    out_file = tmp_path / 'out.json'
    model = EditModel(ChoiceCfg(), out_file=out_file)
    model.set_type(path=('width',), text='str')
    assert model.save().saved
    saved = written(out_file)
    assert isinstance(saved, dict) and saved['width'] == '80'


@pytest.mark.parametrize('path, types, refused',
                         [(('written',), ['Colour'], ('None', 'null')),
                          (('omitted',), ['Colour', 'None'], None),
                          (('mixed',), ['Colour'], ('int', '0'))])
def test_converter_refuses(path: ConfigPath, types: list[str],
                           refused: Optional[tuple[str, str]]) -> None:
    """Test a type the converter of a member refuses is not offered.

    The line below the row says which type was left out and why, because a
    pull-down cannot say what is not in it.
    """
    row = row_at(EditModel(ConvertedCfg()), path)
    assert type_texts(row) == types
    if refused is not None:
        type_text, value = refused
        assert NOT_CONVERTED_FORM.format(type=type_text,
                                         value=value) in row.description


def test_own_converter_offers() -> None:
    """Test an application whose own converter takes more is offered more."""
    model = EditModel(LenientCfg())
    assert row_chooses_type(row_at(model, ('mixed',)))
    model.set_type(path=('mixed',), text='int')
    assert row_at(model, ('mixed',)).value == 0
    assert model.validate().valid
    assert _held(model, ('mixed',)) == 'int'


def test_unmade_left_out() -> None:
    """Test a type the editor cannot make is not offered beside one it can.

    Choosing it could give the member no value of it, so the member is
    offered the number and nothing, and the line below it says why.
    """
    row = row_at(EditModel(UnmadeCfg()), PLACE)
    assert type_texts(row) == ['int', 'None'] and row.type_choosable
    assert NOT_MADE.format(type='Path') in row.description


def test_unmade_held() -> None:
    """Test a member holding a path keeps it offered, in a field of text.

    Its text is read as the text it was written as, so a text that is JSON
    for a list does not take the field away. Choosing another type is one way,
    because nothing the editor could make is a path.
    """
    model = EditModel(UnmadeCfg(from_json_data_text='{"place": "x/y"}'))
    row = row_at(model, PLACE)
    assert type_texts(row) == ['int', 'Path', 'None']
    assert row.chosen_type.text == 'Path' and row.editable
    model.set_text(path=PLACE, text='[1]')
    assert row_at(model, PLACE).value == '[1]'
    model.set_type(path=PLACE, text='int')
    assert type_texts(row_at(model, PLACE)) == ['int', 'None']
