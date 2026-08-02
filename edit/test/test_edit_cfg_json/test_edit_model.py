#! /usr/bin/env python3
"""Tests for the user interface agnostic edit model."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import pytest
from config_as_json import JsonType
from edit_cfg_json import EditModel, MemberRow
from .sample_cfg import FlatCfg, ListCfg, NoneCfg, RewriteCfg


def test_flat_rows() -> None:
    """Test a flat configuration gives one row per member."""
    model = EditModel(FlatCfg())
    assert [row.name for row in model.rows] == ['answer', 'name']
    assert [row.value for row in model.rows] == [42, 'flat text']
    assert all(row.editable for row in model.rows)


def test_type_name() -> None:
    """Test the model reports the class name of the configuration."""
    assert EditModel(FlatCfg()).config_type_name == 'FlatCfg'


def test_none_is_a_value() -> None:
    """Test a member defaulting to None is an editable row holding None."""
    rows = {row.name: row for row in EditModel(NoneCfg()).rows}
    assert rows['name'].value is None
    assert rows['name'].editable


def test_containers_reported() -> None:
    """Test a list member and a dict member are rows that are not editable."""
    rows = {row.name: row for row in EditModel(ListCfg()).rows}
    assert set(rows) == {'answer', 'limits', 'tags'}
    assert not rows['tags'].editable
    assert not rows['limits'].editable
    assert rows['answer'].editable


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
