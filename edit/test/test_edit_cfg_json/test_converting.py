#! /usr/bin/env python3
"""Tests for what the configuration makes of one leaf value of the buffer.

Every case is driven by a real configuration class and its real parse
converter, because the point of the design is that the editor runs the
converter the application declared rather than knowing anything about enums:
a test that converted a value itself would be testing nothing about the
editor.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from config_as_json import JsonType
import pytest
from edit_cfg_json.converting import convert_member, member_converters
from .sample_cfg import EnumCfg, FlatCfg, HexCfg, IntEnumCfg, Level, \
    ListCfg, OmitCfg, PlainEnumCfg, SampleCfg

REFUSED_VALUES: list[tuple[type[SampleCfg], str, JsonType, str]] = [
    (EnumCfg, 'colour', 'PURPLE', 'PURPLE is not one of: RED, GREEN'),
    (IntEnumCfg, 'level', 'MIDDLE', 'MIDDLE is not one of: LOWEST, LOW, HIGH'),
    (IntEnumCfg, 'level', 'LO', 'LO is not one of: LOWEST, LOW, HIGH'),
    (IntEnumCfg, 'level', 7, 'not str as expected'),
    (HexCfg, 'mask', 'zz', "invalid literal for int() with base 16: 'zz'")]
"""One case per way in which a declared converter refuses a value.

The value that is no text at all is here because the editor has to survive
it: the converter of an enum refuses that with an assertion rather than with
an exception of its own, and a crash would be the worst possible answer to a
value that the user typed.

The last of them is refused by a converter that `config_as_json` does not
ship and that is about no enum, which is what says that none of this is
about enums in particular.
"""


@pytest.mark.parametrize('config_type, name, value, expected', REFUSED_VALUES)
def test_refused_value(config_type: type[SampleCfg], name: str,
                       value: JsonType, expected: str) -> None:
    """Test a value no converter accepts is reported and not raised."""
    converter = member_converters(config_type())[name]
    converted = convert_member(converter=converter, value=value)
    assert expected in converted.message
    assert converted.value == value


def test_quotes_not_added() -> None:
    """Test the message is what the converter wrote, without quotation marks.

    A `KeyError` writes the representation of its argument, so the message
    would otherwise reach the user wrapped in quotation marks that no
    validator and no converter ever wrote.
    """
    converter = member_converters(EnumCfg())['colour']
    message = convert_member(converter=converter, value='PURPLE').message
    assert not message.startswith("'")


@pytest.mark.parametrize('typed, member',
                         [('HIGH', Level.HIGH), ('HI', Level.HIGH),
                          ('low', Level.LOW), ('lowe', Level.LOWEST)])
def test_accepted_name(typed: str, member: Level) -> None:
    """Test text that names one member converts to that member.

    The matching of `config_as_json` is forgiving, and the editor is exactly
    as forgiving as it is, because it runs that matching and does none of its
    own.
    """
    converter = member_converters(IntEnumCfg())['level']
    converted = convert_member(converter=converter, value=typed)
    assert converted == (member, '')


def test_no_converter() -> None:
    """Test a member with no converter keeps whatever the buffer holds."""
    assert convert_member(converter=None, value='anything') == ('anything', '')


def test_own_converter_runs() -> None:
    """Test a converter of the application's own is run like any other."""
    converter = member_converters(HexCfg())['mask']
    assert convert_member(converter=converter, value='ff') == (255, '')


def test_already_converted() -> None:
    """Test a value that already has the type of its member is left alone.

    That is what `config_as_json` does while it parses, and the converter of
    this member would refuse the number outright, so nothing but the skip
    could leave it accepted.
    """
    converter = member_converters(HexCfg())['mask']
    assert convert_member(converter=converter, value=255) == (255, '')


def test_none_left_alone() -> None:
    """Test a member holding None is neither converted nor refused.

    A member its class leaves out of JSON while it is None has nothing to
    convert, and a None that is wrong is refused by the validation of the
    whole configuration, which has a message of its own for it.
    """
    converter = member_converters(EnumCfg())['colour']
    assert convert_member(converter=converter, value=None) == (None, '')


@pytest.mark.parametrize('config_type, expected',
                         [(EnumCfg, {'colour'}), (IntEnumCfg, {'level'}),
                          (PlainEnumCfg, {'level'}), (HexCfg, {'mask'}),
                          (FlatCfg, set()), (ListCfg, set()),
                          (OmitCfg, set())])
def test_declared_converters(config_type: type[SampleCfg],
                             expected: set[str]) -> None:
    """Test only the converters of real members are reported.

    A class that declares none inherits a placeholder converter under a key
    of the base class's own, and a member of that name exists nowhere.
    """
    assert set(member_converters(config_type())) == expected
