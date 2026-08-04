#! /usr/bin/env python3
"""Tests for constructing a configuration class from its own signature.

The editor constructs the application's class in four places, and the shape of
the constructor is not the same for every class that exists: `Config.__init__`
names the JSON text `from_json_data_text`, and the example classes that
`config_as_json` ships name it `from_json_text`. These tests are about what is
passed to which class, because getting that wrong is either a class that cannot
be edited at all or, far worse, a buffer that is validated against the declared
defaults and therefore accepted whatever it holds.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from io import StringIO
from typing import Optional
import json
import pytest
from config_as_json import Config, ConfigAutoChangeHook
from edit_cfg_json.constructing import NO_JSON_TEXT, built_config
from .sample_cfg import AltNameCfg, ExtraArgCfg, FlatCfg, HookCfg, NoTextCfg


@pytest.mark.parametrize('config_type,name,answer',
                         [(FlatCfg, 'flat text', 42),
                          (AltNameCfg, 'other name', 5),
                          (HookCfg, 'hook text', 42)])
def test_no_source(config_type: type[Config], name: str, answer: int) -> None:
    """Test a class with no JSON source holds what it declares."""
    config = built_config(config_type, stream=StringIO())
    assert getattr(config, 'name') == name
    assert getattr(config, 'answer') == answer


@pytest.mark.parametrize('config_type', [FlatCfg, AltNameCfg, HookCfg])
def test_text_reaches_class(config_type: type[Config]) -> None:
    """Test JSON text reaches a class whatever it calls that parameter."""
    text = json.dumps({'name': 'from text', 'answer': 7})
    config = built_config(config_type, stream=StringIO(), text=text)
    assert getattr(config, 'name') == 'from text'
    assert getattr(config, 'answer') == 7


def test_no_text_parameter() -> None:
    """Test a class with nowhere to put the text refuses the text.

    Constructing it on its declared defaults instead would accept a buffer
    whatever it held, which is the one degradation that is not safe.
    """
    with pytest.raises(TypeError) as error_info:
        built_config(NoTextCfg, stream=StringIO(), text='{"name": "x"}')
    assert str(error_info.value) == NO_JSON_TEXT.format(name='NoTextCfg')


def test_no_text_needs_none() -> None:
    """Test a class with nowhere to put the text still holds its defaults."""
    config = built_config(NoTextCfg, stream=StringIO())
    assert getattr(config, 'name') == 'no text'


def test_hook_reaches_class() -> None:
    """Test the change hook reaches a class that declares it."""
    hook = ConfigAutoChangeHook()
    config = built_config(HookCfg, stream=StringIO(), hook=hook)
    assert isinstance(config, HookCfg)
    assert config.hook_given() is hook


@pytest.mark.parametrize('hook', [None, ConfigAutoChangeHook()])
def test_hook_dropped(hook: Optional[ConfigAutoChangeHook]) -> None:
    """Test a class that does not declare the hook is built without it."""
    assert isinstance(built_config(FlatCfg, stream=StringIO(), hook=hook),
                      FlatCfg)


def test_stream_is_used() -> None:
    """Test what a class says about a buffer reaches the given stream."""
    said = StringIO()
    with pytest.raises(KeyError):
        built_config(FlatCfg, stream=said, text='{"nowhere": 1}')
    assert said.getvalue()


def test_extra_argument() -> None:
    """Test a class needing an argument of its own cannot be built."""
    with pytest.raises(TypeError):
        built_config(ExtraArgCfg, stream=StringIO())
