#! /usr/bin/env python3
"""Tests for where the dict-shape check of `config_as_json` reaches.

`Config.check_dict_parse` refuses a dict where the object holds something else
and anything else where it holds a dict, and matches the keys of the dicts it
reaches. These ask `dict_check` about each kind of place one class has, and
then ask a model that what it answers is what the class itself does.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from typing import Optional
import pytest
from config_as_json import ConfigPath
from edit_cfg_json import EditModel
from edit_cfg_json.dict_check import dict_check, dict_shape, keys_checked
from edit_cfg_json.elements import FIXED_KEYS
from edit_cfg_json.tree import config_nodes
from .choice_cfg import ShapeCfg
from .model_helpers import row_at

CHECK = dict_check(config_nodes(ShapeCfg()))
"""What says where the check of a `ShapeCfg` reaches."""


@pytest.mark.parametrize('path, expected',
                         [(('plain',), False), (('table',), True),
                          (('table', 'row'), True),
                          (('table', 'row', 'a'), False),
                          (('table', 'loose'), True),
                          (('table', 'loose', 'b'), None),
                          (('loose',), True), (('loose', 'x'), None),
                          (('rows',), False), (('rows', '0'), None),
                          (('nothing',), False), (('inner',), None),
                          (('inner', 'sizes'), True),
                          (('inner', 'spare'), False),
                          (('table', 'nowhere'), None)])
def test_dict_shape(path: ConfigPath, expected: Optional[bool]) -> None:
    """Test what the check demands at each kind of place, and where it stops.

    It stops below a place named in `_unchecked_dicts`, at a member that
    `nested_configs()` names, below a list and at a key the object's dict
    does not hold. A nested object answers for its own members.
    """
    assert dict_shape(path=path, check=CHECK) is expected


@pytest.mark.parametrize('path, expected',
                         [(('table',), True), (('table', 'row'), True),
                          (('table', 'loose'), False), (('loose',), False),
                          (('loose', 'x'), False), (('rows', '0'), False),
                          (('inner', 'sizes'), True)])
def test_keys_checked(path: ConfigPath, expected: bool) -> None:
    """Test which dicts have their keys matched against the object's.

    The check returns at a place named in `_unchecked_dicts` after asking
    whether it is a dict, so the keys of that place are the application's.
    """
    assert keys_checked(path=path, check=CHECK) is expected


def test_named_key_grows() -> None:
    """Test a key named like an unchecked member is one the class takes.

    `config_as_json` asks a place by the name of its last step, so the key
    `loose` of `table` can gain a key of its own, and the pass that follows
    accepts it, while the key beside it cannot gain one.
    """
    model = EditModel(ShapeCfg())
    assert row_at(model, ('table', 'row')).offer.refusal == FIXED_KEYS
    model.add_element(path=('table', 'loose'), key='c')
    assert model.validate().valid


def test_pass_keeps_shape() -> None:
    """Test the answer is the same after a pass as before it.

    The rows are then built from the object the pass accepted, which holds a
    dict wherever the object it was matched against does.
    """
    model = EditModel(ShapeCfg())
    assert model.validate().valid
    row = row_at(model, ('nothing',))
    assert [option.text for option in row.types] == ['None']
