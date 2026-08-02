#! /usr/bin/env python3
"""Tests for the user interface agnostic edit model."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import pytest
from config_as_json import JsonType
from edit_cfg_json import EditModel, MemberRow
from .sample_cfg import FlatCfg, ListCfg, NoneCfg, OmitCfg, RewriteCfg


def _row(model: EditModel, name: str) -> MemberRow:
    """Return the row of one member of a model."""
    return {row.name: row for row in model.rows}[name]


def test_flat_rows() -> None:
    """Test a flat configuration gives one row per member."""
    model = EditModel(FlatCfg())
    assert [row.name for row in model.rows] == ['name', 'answer']
    assert [row.value for row in model.rows] == ['flat text', 42]
    assert all(row.editable for row in model.rows)


def test_row_paths() -> None:
    """Test every member of a flat configuration has a one step path."""
    assert [row.path for row in EditModel(FlatCfg()).rows] == \
        [('name',), ('answer',)]


def test_declaration_order() -> None:
    """Test the rows keep the order the configuration class declares.

    The JSON file has its keys sorted, so a model that took its order from
    the file would show these three members as answer, limits, tags.
    """
    model = EditModel(ListCfg())
    assert [row.name for row in model.rows] == ['tags', 'limits', 'answer']


def test_omitted_none_no_row() -> None:
    """Test a member left out of JSON while it is None gets no row."""
    model = EditModel(OmitCfg())
    assert [row.name for row in model.rows] == ['first', 'last']


def test_type_name() -> None:
    """Test the model reports the class name of the configuration."""
    assert EditModel(FlatCfg()).config_type_name == 'FlatCfg'


def test_none_is_a_value() -> None:
    """Test a member defaulting to None is an editable row holding None."""
    row = _row(EditModel(NoneCfg()), 'name')
    assert row.value is None
    assert row.editable
    assert not row.is_text


def test_containers_reported() -> None:
    """Test a list member and a dict member are rows that are not editable."""
    model = EditModel(ListCfg())
    assert {row.name for row in model.rows} == {'answer', 'limits', 'tags'}
    assert not _row(model, 'tags').editable
    assert not _row(model, 'limits').editable
    assert _row(model, 'answer').editable


def test_text_kept_as_text() -> None:
    """Test a string member is held as a string and not as JSON notation."""
    model = EditModel(FlatCfg())
    assert _row(model, 'name').is_text
    assert _row(model, 'name').value == 'flat text'
    assert not _row(model, 'answer').is_text


def test_caller_not_changed() -> None:
    """Test building a model does not change the caller's own object."""
    config = RewriteCfg()
    config.name = 'raw text'
    model = EditModel(config)
    assert config.name == 'raw text'
    assert model.rows[0].value == 'Raw text'


def test_edit_stays_in_model() -> None:
    """Test editing the buffer does not touch the caller's own object."""
    config = FlatCfg()
    model = EditModel(config)
    model.set_text(path=('name',), text='edited')
    assert config.name == 'flat text'
    assert _row(model, 'name').value == 'edited'


def test_clean_at_start() -> None:
    """Test a model that was just built has nothing worth saving."""
    model = EditModel(FlatCfg())
    assert not model.dirty
    assert not any(row.edited for row in model.rows)


def test_set_text_member() -> None:
    """Test setting a text member keeps exactly what was typed."""
    model = EditModel(FlatCfg())
    model.set_text(path=('name',), text='other text')
    assert _row(model, 'name').value == 'other text'
    assert _row(model, 'name').edited
    assert model.dirty


def test_set_number_member() -> None:
    """Test setting a number member gives a number and not its text."""
    model = EditModel(FlatCfg())
    model.set_text(path=('answer',), text='7')
    assert _row(model, 'answer').value == 7
    assert not _row(model, 'answer').is_text


def test_set_digits_as_text() -> None:
    """Test a text member holding digits stays text and does not become one.

    This is the case the type information of a row exists for. The member is
    a text member because that is what the configuration object declared,
    and not because of what it happens to hold right now.
    """
    model = EditModel(FlatCfg())
    model.set_text(path=('name',), text='10')
    assert _row(model, 'name').value == '10'


def test_set_invalid_number() -> None:
    """Test a number member tolerates text that is not a number yet.

    A value that is being typed is not valid for most of the time it takes
    to type it, so a buffer that refused such a value could not be typed in.
    """
    model = EditModel(FlatCfg())
    model.set_text(path=('answer',), text='not-a-number')
    assert _row(model, 'answer').value == 'not-a-number'
    assert _row(model, 'answer').edited


def test_set_empty_text() -> None:
    """Test both kinds of member accept an empty field."""
    model = EditModel(FlatCfg())
    model.set_text(path=('name',), text='')
    model.set_text(path=('answer',), text='')
    assert _row(model, 'name').value == ''
    assert _row(model, 'answer').value == ''


def test_set_recovers() -> None:
    """Test a member set to text that is no number can be set to one."""
    model = EditModel(FlatCfg())
    model.set_text(path=('answer',), text='4x')
    model.set_text(path=('answer',), text='4')
    assert _row(model, 'answer').value == 4


def test_set_twice() -> None:
    """Test the last of several edits of one member is what is kept."""
    model = EditModel(FlatCfg())
    for text in ['first', 'second', 'third']:
        model.set_text(path=('name',), text=text)
    assert _row(model, 'name').value == 'third'


def test_set_same_text() -> None:
    """Test setting the text a field already shows is not an edit.

    A field posts a change when it is given its initial text, so a model
    that counted that as an edit would report unsaved changes before the
    user had touched anything.
    """
    model = EditModel(FlatCfg())
    model.set_text(path=('answer',), text='42')
    assert not model.dirty


def test_set_back_to_start() -> None:
    """Test typing a value back to what it was leaves nothing to save."""
    model = EditModel(FlatCfg())
    model.set_text(path=('name',), text='other text')
    model.set_text(path=('name',), text='flat text')
    assert not _row(model, 'name').edited
    assert not model.dirty


def test_dirty_per_model() -> None:
    """Test one edited member is enough to make the whole model dirty."""
    model = EditModel(FlatCfg())
    model.set_text(path=('answer',), text='7')
    assert model.dirty
    assert not _row(model, 'name').edited


def test_set_unknown_member() -> None:
    """Test setting a member that does not exist is refused."""
    model = EditModel(FlatCfg())
    with pytest.raises(KeyError):
        model.set_text(path=('missing',), text='text')
    assert not model.dirty


def test_set_wrong_path() -> None:
    """Test a path with more steps than a flat member has is refused."""
    model = EditModel(FlatCfg())
    with pytest.raises(KeyError):
        model.set_text(path=('name', 'inner'), text='text')


def test_set_container() -> None:
    """Test a member that cannot be edited yet is refused, not half done."""
    model = EditModel(ListCfg())
    with pytest.raises(ValueError):
        model.set_text(path=('tags',), text='[]')
    assert _row(model, 'tags').value == ['first', 'second']
    assert not model.dirty


def test_rows_are_a_snapshot() -> None:
    """Test a row that was read before an edit is not changed by it."""
    model = EditModel(FlatCfg())
    before = _row(model, 'name')
    model.set_text(path=('name',), text='other text')
    assert before.value == 'flat text'
    assert _row(model, 'name').value == 'other text'


@pytest.mark.parametrize('value, editable',
                         [(1, True), (1.5, True), ('text', True),
                          (True, True), (None, True), ([1, 2], False),
                          ({'key': 1}, False), ([], False), ({}, False)])
def test_row_editable(value: JsonType, editable: bool) -> None:
    """Test which kinds of JSON value a row reports as editable."""
    row = MemberRow(path=('member',), value=value, original=value)
    assert row.editable is editable


@pytest.mark.parametrize('value, is_text',
                         [('text', True), ('', True), ('42', True),
                          (42, False), (1.5, False), (True, False),
                          (None, False), (['a'], False), ({'a': 1}, False)])
def test_row_is_text(value: JsonType, is_text: bool) -> None:
    """Test which kinds of member a row reports as holding text."""
    row = MemberRow(path=('member',), value=value, original=value)
    assert row.is_text is is_text


@pytest.mark.parametrize('value, original, edited',
                         [(1, 1, False), (2, 1, True), (1.0, 1, True),
                          (True, 1, True), ('42', 42, True),
                          ('', None, True), (None, None, False)])
def test_row_edited(value: JsonType, original: JsonType, edited: bool) -> None:
    """Test a row is edited when it would be written to the file anew."""
    row = MemberRow(path=('member',), value=value, original=original)
    assert row.edited is edited


def test_row_name_is_last() -> None:
    """Test the name of a member is the last step of its path."""
    row = MemberRow(path=('outer', 'inner'), value=1, original=1)
    assert row.name == 'inner'


def test_row_flags_start_off() -> None:
    """Test the flags that later steps set are off in a new row."""
    row = MemberRow(path=('member',), value=1, original=1)
    assert not row.changed_by_validator
    assert not row.filled_from_default
