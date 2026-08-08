#! /usr/bin/env python3
"""Tests for building the configuration objects that the editor works with.

Two of them, and only one asks the class for anything. The declared values need
an object that did not exist before, and the shape of a constructor is not the
same for every class that exists: `Config.__init__` names the JSON text
`from_json_data_text`, and the example classes that `config_as_json` ships name
it `from_json_text`. Nothing is ever passed under either name but `None`, and a
class that declares the parameter without a default of its own has to be given
that.

An object holding an edit buffer is the other, and it is a copy of an object
the editor already has with `Config.parse_json` applied to it. These tests are
about what that runs, because it is what makes a class the editor cannot
construct editable all the same, and about the one method that can be replaced
on the copy, because two things the editor has to know are otherwise
unreachable.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from io import StringIO
from typing import Optional, TextIO
import json
import pytest
from config_as_json import Config, ConfigAutoChangeHook, ValidationPlan
from edit_cfg_json.constructing import built_config, parsed_config
from .sample_cfg import AltNameCfg, ExtraArgCfg, FlatCfg, HookCfg, NoTextCfg, \
    RangeCfg


@pytest.mark.parametrize('config_type,name,answer',
                         [(FlatCfg, 'flat text', 42),
                          (AltNameCfg, 'other name', 5),
                          (HookCfg, 'hook text', 42),
                          (NoTextCfg, 'no text', None)])
def test_declared_values(config_type: type[Config], name: str,
                         answer: Optional[int]) -> None:
    """Test a class is constructed holding the values it declares.

    `NoTextCfg` declares no JSON text parameter at all and is constructed
    exactly as well as the rest, because the text is never passed to a
    constructor. It declares no second member either, which is what the
    missing answer stands for.
    """
    config = built_config(config_type, stream=StringIO())
    assert getattr(config, 'name') == name
    assert getattr(config, 'answer', None) == answer


def test_no_hook_is_forced() -> None:
    """Test a class that declares the change hook is offered none.

    The editor has no hook to offer: it reads what a load recorded from the
    object the load produced, so a class that declares the parameter is
    constructed exactly like a class that does not, and the object holds the
    hook that `Config` gave it.
    """
    config = built_config(HookCfg, stream=StringIO())
    assert isinstance(config, HookCfg)
    assert config.hook_given() is None
    assert isinstance(config.auto_change_hook(), ConfigAutoChangeHook)


def test_extra_argument() -> None:
    """Test a class needing an argument of its own cannot be built."""
    with pytest.raises(TypeError):
        built_config(ExtraArgCfg, stream=StringIO())


@pytest.mark.parametrize('config', [FlatCfg(), NoTextCfg(),
                                    ExtraArgCfg(home='here')])
def test_buffer_applied(config: Config) -> None:
    """Test a buffer reaches a copy of any configuration object.

    None of these three is constructed for this, which is the whole point:
    `NoTextCfg` could not be given a text at all and `ExtraArgCfg` could not be
    constructed at all, and both of them hold an edit buffer perfectly well.
    """
    name = type(config).__name__
    text = json.dumps({member: name for member in vars(config)
                       if not member.startswith('_')})
    parsed = parsed_config(config, text, stream=StringIO())
    assert getattr(parsed, 'name', name) == name
    assert parsed is not config


def test_copy_is_not_object() -> None:
    """Test the object the buffer was applied to is left as it was."""
    config = FlatCfg()
    text = json.dumps({'name': 'other', 'answer': 7})
    assert getattr(parsed_config(config, text, stream=StringIO()), 'name') \
        == 'other'
    assert config.name == 'flat text'


def test_refused_buffer() -> None:
    """Test the class refuses a buffer here exactly as it would a file."""
    said = StringIO()
    with pytest.raises(ValueError):
        parsed_config(RangeCfg(), json.dumps({'answer': 5000}), stream=said)
    assert said.getvalue()


def _no_plan(stderr_file: TextIO) -> ValidationPlan:
    """Return no validation steps, standing in for the real method."""
    _ = stderr_file
    return []


def test_replaced_method() -> None:
    """Test a replaced method is used and is no member of the configuration.

    The parse counts the attributes of the object that are not callable, so a
    method replaced on the object is not mistaken for a member. Without the
    replacement `RangeCfg` refuses this value, which is what says that the
    replacement is really what ran.
    """
    parsed = parsed_config(RangeCfg(), json.dumps({'answer': 5000}),
                           stream=StringIO(), replace='get_validation_plan',
                           method=_no_plan)
    assert getattr(parsed, 'answer') == 5000
    assert json.loads(parsed.as_json_string(stderr_file=StringIO())) \
        == {'answer': 5000}


def test_real_plan_reachable() -> None:
    """Test the class of a probe still answers with the real plan.

    That is what the attribution of a refusal walks, so leaving the method out
    on the object rather than on the class is what makes both available.
    """
    parsed = parsed_config(RangeCfg(), json.dumps({'answer': 5000}),
                           stream=StringIO(), replace='get_validation_plan',
                           method=_no_plan)
    assert type(parsed).get_validation_plan(parsed, stderr_file=StringIO())
    assert not parsed.get_validation_plan(stderr_file=StringIO())
