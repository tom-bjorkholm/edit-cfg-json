#! /usr/bin/env python3
"""Tests for what an application says about how its configuration is built.

Two things are tested here and they are worth telling apart. One is the loader
that the editor makes for itself out of a class, which is what almost every
application gets without saying anything and which is published so that an
application can have the same thing with an argument of its own bound into it.
The other is what the editor does with a loader it is given: it passes the five
keyword arguments and nothing else, and it stays alive whatever the loader does
about a refusal, including ending the process.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from functools import partial
from io import StringIO
from typing import Optional
import json
import pytest
from config_as_json import ConfigAutoChangeHook
from edit_cfg_json import ConfigLoader, derived_loader
from edit_cfg_json.loader import LOADER_EXITED, NO_FILE_NAME, ConfigSource, \
    ask_loader
from .sample_cfg import HOME_VALUE, PICKED_NAME, ExtraArgCfg, FlatCfg, \
    HookCfg, PickedCfg, exiting_loader, extra_arg_loader, picking_loader


def test_declared_values() -> None:
    """Test a derived loader with no JSON source holds the declared values."""
    config = derived_loader(FlatCfg)(stderr_file=StringIO())
    assert getattr(config, 'name') == 'flat text'


def test_text_is_applied() -> None:
    """Test a derived loader applies the JSON text it is given."""
    text = json.dumps({'name': 'from text', 'answer': 7})
    config = derived_loader(FlatCfg)(from_json_data_text=text,
                                     stderr_file=StringIO())
    assert getattr(config, 'name') == 'from text'


@pytest.mark.parametrize('permissive,expected', [(True, 42), (False, None)])
def test_policy_honoured(permissive: bool, expected: Optional[int]) -> None:
    """Test a derived loader fills in what the text leaves out, or refuses.

    The policy belongs to the parse and not to the constructor, which is why
    the loader constructs the class and applies the text afterwards:
    `Config.__init__` takes no `ok_to_use_defaults` at all.
    """
    text = json.dumps({'name': 'partial'})
    loader = derived_loader(FlatCfg)
    if expected is None:
        with pytest.raises(KeyError):
            loader(from_json_data_text=text, stderr_file=StringIO(),
                   ok_to_use_defaults=permissive)
        return
    config = loader(from_json_data_text=text, stderr_file=StringIO(),
                    ok_to_use_defaults=permissive)
    assert getattr(config, 'answer') == expected


def test_file_name_refused() -> None:
    """Test a derived loader refuses a file name rather than ignoring it."""
    with pytest.raises(ValueError) as error_info:
        derived_loader(FlatCfg)(from_json_filename='somewhere.json',
                                stderr_file=StringIO())
    assert str(error_info.value) == NO_FILE_NAME


def test_hook_reaches_class() -> None:
    """Test a derived loader hands the change hook to a class that takes it."""
    hook = ConfigAutoChangeHook()
    config = derived_loader(HookCfg)(auto_ch_hook=hook, stderr_file=StringIO())
    assert isinstance(config, HookCfg)
    assert config.hook_given() is hook


def test_bound_argument() -> None:
    """Test a bound argument reaches a class the editor cannot construct.

    This is what the published helper is for, and it is the whole of what an
    application whose class needs one argument has to write.
    """
    config = extra_arg_loader(stderr_file=StringIO())
    assert isinstance(config, ExtraArgCfg)
    assert config.home == HOME_VALUE


def test_bound_arg_and_text() -> None:
    """Test such a loader applies a JSON text as any other loader does."""
    text = json.dumps({'home': 'from text'})
    config = extra_arg_loader(from_json_data_text=text, stderr_file=StringIO())
    assert getattr(config, 'home') == 'from text'


def test_exit_is_a_refusal() -> None:
    """Test a loader that ends the program is turned into a refusal.

    It becomes a `ValueError`, which is what every caller in this library
    already reports as values the configuration would not accept, so a loader
    of that kind costs a message and never the session.
    """
    with pytest.raises(ValueError) as error_info:
        ask_loader(exiting_loader, stream=StringIO())
    assert str(error_info.value) == LOADER_EXITED


def test_asked_args_reach() -> None:
    """Test what `ask_loader` is given is what the loader is called with."""
    text = json.dumps({'name': 'asked'})
    config = ask_loader(derived_loader(FlatCfg), stream=StringIO(), text=text,
                        ok_to_use_defaults=True)
    assert getattr(config, 'name') == 'asked'
    assert getattr(config, 'answer') == 42


@pytest.mark.parametrize('candidate,is_loader',
                         [(picking_loader, True), (extra_arg_loader, True),
                          (FlatCfg, True), (PICKED_NAME, False)])
def test_runtime_recognised(candidate: object, is_loader: bool) -> None:
    """Test a name from a command line can be told from something else.

    What the check can see is that the name can be called, which is why a
    configuration class passes it and is then refused by being called: it takes
    no `ok_to_use_defaults`. A piece of text is refused before that.
    """
    assert isinstance(candidate, ConfigLoader) is is_loader


def test_source_derives() -> None:
    """Test a session with no loader constructs the class it was given."""
    source = ConfigSource(config=FlatCfg())
    assert source.config_type is FlatCfg
    assert getattr(source.made(stream=StringIO()), 'name') == 'flat text'


def test_source_uses_loader() -> None:
    """Test a session with a loader asks that loader and not the class."""
    source = ConfigSource(config=ExtraArgCfg(home='given'),
                          loader=extra_arg_loader)
    assert getattr(source.made(stream=StringIO()), 'home') == HOME_VALUE


def test_source_can_choose() -> None:
    """Test the class a loader chooses is the class of the object it made."""
    source = ConfigSource(config=FlatCfg(), loader=picking_loader)
    text = json.dumps({'name': PICKED_NAME, 'answer': 1})
    assert isinstance(source.made(stream=StringIO(), text=text), PickedCfg)
    assert isinstance(source.made(stream=StringIO()), FlatCfg)


def test_partial_of_a_class() -> None:
    """Test a partial is all a derived loader needs, and a class is one too.

    `derived_loader` reads a signature, and `functools.partial` over a class
    has one with the bound argument left out of it.
    """
    loader = derived_loader(partial(ExtraArgCfg, home='partly'))
    assert getattr(loader(stderr_file=StringIO()), 'home') == 'partly'
