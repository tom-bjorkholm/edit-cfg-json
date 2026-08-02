#! /usr/bin/env python3
"""Tests for the plain text rendering of an edit model."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import pytest
from config_as_json import JsonType
from edit_cfg_json import EditModel, MemberRow, model_as_text, row_value_text
from .sample_cfg import FlatCfg, ListCfg, NoneCfg


def test_flat_text() -> None:
    """Test the rendering has one line per member and no trailing break."""
    assert model_as_text(EditModel(FlatCfg())) == \
        'name = flat text\nanswer = 42'


def test_text_has_no_quotes() -> None:
    """Test a string member is shown as the string and not as JSON text."""
    assert '"' not in model_as_text(EditModel(FlatCfg()))


def test_none_text() -> None:
    """Test a member holding None is rendered as JSON null."""
    assert 'name = null' in model_as_text(EditModel(NoneCfg()))


def test_container_text() -> None:
    """Test a list member and a dict member are named as not editable."""
    text = model_as_text(EditModel(ListCfg()))
    assert 'tags = <not editable yet: list>' in text
    assert 'limits = <not editable yet: dict>' in text
    assert 'answer = 3' in text


@pytest.mark.parametrize('value, expected',
                         [(42, '42'), (1.5, '1.5'), (True, 'true'),
                          (False, 'false'), (None, 'null'),
                          ('text', 'text'), ('', ''),
                          ('with "quotes"', 'with "quotes"'),
                          ('Björkholm', 'Björkholm'),
                          ('  spaced  ', '  spaced  '), ('42', '42')])
def test_row_value_text(value: JsonType, expected: str) -> None:
    """Test a string shows as itself and every other scalar as its JSON."""
    assert row_value_text(MemberRow(name='member', value=value)) == expected
