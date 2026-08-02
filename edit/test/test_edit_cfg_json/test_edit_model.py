#! /usr/bin/env python3
"""Tests for the user interface agnostic edit model."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import pytest
from config_as_json import JsonType
from edit_cfg_json import EditModel, MemberRow
from .sample_cfg import FlatCfg, ListCfg, NoneCfg, OmitCfg, RewriteCfg


def test_flat_rows() -> None:
    """Test a flat configuration gives one row per member."""
    model = EditModel(FlatCfg())
    assert [row.name for row in model.rows] == ['name', 'answer']
    assert [row.value for row in model.rows] == ['flat text', 42]
    assert all(row.editable for row in model.rows)


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
    rows = {row.name: row for row in EditModel(NoneCfg()).rows}
    assert rows['name'].value is None
    assert rows['name'].editable
    assert not rows['name'].is_text


def test_containers_reported() -> None:
    """Test a list member and a dict member are rows that are not editable."""
    rows = {row.name: row for row in EditModel(ListCfg()).rows}
    assert set(rows) == {'answer', 'limits', 'tags'}
    assert not rows['tags'].editable
    assert not rows['limits'].editable
    assert rows['answer'].editable


def test_text_kept_as_text() -> None:
    """Test a string member is held as a string and not as JSON notation."""
    rows = {row.name: row for row in EditModel(FlatCfg()).rows}
    assert rows['name'].is_text
    assert rows['name'].value == 'flat text'
    assert not rows['answer'].is_text


def test_caller_not_changed() -> None:
    """Test building a model does not change the caller's own object."""
    config = RewriteCfg()
    config.name = 'raw text'
    model = EditModel(config)
    assert config.name == 'raw text'
    assert model.rows[0].value == 'Raw text'


@pytest.mark.parametrize('value, editable',
                         [(1, True), (1.5, True), ('text', True),
                          (True, True), (None, True), ([1, 2], False),
                          ({'key': 1}, False), ([], False), ({}, False)])
def test_row_editable(value: JsonType, editable: bool) -> None:
    """Test which kinds of JSON value a row reports as editable."""
    assert MemberRow(name='member', value=value).editable is editable


@pytest.mark.parametrize('value, is_text',
                         [('text', True), ('', True), ('42', True),
                          (42, False), (1.5, False), (True, False),
                          (None, False), (['a'], False), ({'a': 1}, False)])
def test_row_is_text(value: JsonType, is_text: bool) -> None:
    """Test which kinds of JSON value a row reports as text."""
    assert MemberRow(name='member', value=value).is_text is is_text
