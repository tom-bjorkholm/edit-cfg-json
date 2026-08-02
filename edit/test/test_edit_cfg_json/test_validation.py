#! /usr/bin/env python3
"""Tests for running the application's own validation over a buffer.

Every failure the design asks the editor to catch has a case below, and each
of them is produced by a configuration class that refuses in that particular
way rather than by a stubbed exception. That is the point of the design: the
editor has no validation of its own, so a test that raised the exception
itself would test nothing about the editor.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from config_as_json import Config, JsonType
import pytest
from edit_cfg_json.validation import validate_buffer
from .sample_cfg import REFUSAL_MESSAGE, AllowedCfg, EnumCfg, ExtraArgCfg, \
    FlatCfg, IntEnumCfg, ListCfg, OmitCfg, RangeCfg, RefuseCfg, RewriteCfg, \
    TypedCfg

ENUM_NAMES = 'is not one of: LOWEST, LOW, HIGH'
"""What the diagnostics say about text that names no member of `Level`."""

REFUSED_BUFFERS: list[tuple[str, type[Config],
                            dict[str, JsonType], str]] = [
    ('missing key', FlatCfg, {'name': 'text'}, 'No value for answer'),
    ('unknown key', FlatCfg, {'name': 'text', 'answer': 1, 'more': 2},
     'Unexpected parameter more'),
    ('no enum member', EnumCfg, {'colour': 'PURPLE'},
     'PURPLE is not one of: RED, GREEN'),
    ('no int enum member', IntEnumCfg, {'level': 'MIDDLE'}, ENUM_NAMES),
    ('ambiguous name', IntEnumCfg, {'level': 'LO'}, ENUM_NAMES),
    ('enum as a number', IntEnumCfg, {'level': 2}, 'not str as expected'),
    ('outside range', RangeCfg, {'answer': 500},
     'is greater than maximum 100'),
    ('not allowed', AllowedCfg, {'colour': 'blue'}, 'colour'),
    ('wrong type', TypedCfg, {'count': 'text'}, 'is not of type int'),
    ('own validator', RefuseCfg, {'name': 'text'},
     REFUSAL_MESSAGE.format(name='name')),
    ('cannot construct', ExtraArgCfg, {'home': 'here'},
     "missing 1 required positional argument: 'home'")]
"""One buffer per way in which a configuration class refuses a buffer.

The first item of each is the name of the case, which pytest uses to
identify it, and the last is text the diagnostics have to contain.
"""


@pytest.mark.parametrize('name, config_type, members, expected',
                         REFUSED_BUFFERS)
def test_refused_buffer(name: str, config_type: type[Config],
                        members: dict[str, JsonType], expected: str) -> None:
    """Test every way of refusing a buffer becomes a verdict, not a crash."""
    outcome = validate_buffer(config_type=config_type, members=members)
    assert not outcome.verdict.valid, name
    assert expected in outcome.verdict.diagnostics
    assert not outcome.members


def test_silent_refusal_told() -> None:
    """Test a refusal that wrote no diagnostics is still explained.

    An application's own validator is free to raise without writing
    anything, and the user would otherwise be shown that the buffer is
    invalid and nothing at all about why.
    """
    outcome = validate_buffer(config_type=RefuseCfg, members={'name': 'x'})
    assert outcome.verdict.diagnostics.startswith('ValueError: ')


@pytest.mark.parametrize('config_type, members',
                         [(FlatCfg, {'name': 'text', 'answer': 7}),
                          (ListCfg, {'tags': ['one'], 'limits': {'low': 2,
                                                                 'high': 3},
                                     'answer': 3}),
                          (OmitCfg, {'first': 1, 'last': 2}),
                          (EnumCfg, {'colour': 'GREEN'}),
                          (IntEnumCfg, {'level': 'HIGH'}),
                          (RangeCfg, {'answer': 100})])
def test_accepted_buffer(config_type: type[Config],
                         members: dict[str, JsonType]) -> None:
    """Test an accepted buffer is reported as valid and says nothing more."""
    outcome = validate_buffer(config_type=config_type, members=members)
    assert outcome.verdict.valid
    assert outcome.verdict.diagnostics == ''


def test_members_read_back() -> None:
    """Test the members of the accepted configuration object are returned."""
    outcome = validate_buffer(config_type=FlatCfg,
                              members={'name': 'text', 'answer': 7})
    assert outcome.members == {'name': 'text', 'answer': 7}


def test_rewritten_returned() -> None:
    """Test the value a validator stored back is what is returned.

    This is what makes a validation pass anything but read only, and the
    reason the buffer is refreshed from the object that was built rather
    than left holding what the user typed.
    """
    outcome = validate_buffer(config_type=RewriteCfg,
                              members={'name': 'typed text'})
    assert outcome.members == {'name': 'Typed text'}


@pytest.mark.parametrize('typed, whole',
                         [('HIGH', 'HIGH'), ('HI', 'HIGH'), ('low', 'LOW'),
                          ('LOW', 'LOW'), ('lowe', 'LOWEST')])
def test_enum_name_completed(typed: str, whole: str) -> None:
    """Test text that names one enum member comes back as its whole name.

    The matching of `config_as_json` is forgiving: it tries the usual case
    variants of the whole name first and then accepts a prefix that only
    one member has. An exact name is therefore not read as a prefix, which
    is what keeps `LOW` meaning `LOW` and not being ambiguous with
    `LOWEST`. The editor sees the completed name as a value that the pass
    rewrote, which is the same thing that a rewriting validator does.
    """
    outcome = validate_buffer(config_type=IntEnumCfg, members={'level': typed})
    assert outcome.verdict.valid
    assert outcome.members == {'level': whole}


def test_int_enum_is_a_name() -> None:
    """Test an int enum member is read back as its name and not its number.

    Python's own JSON encoder treats an `IntEnum` member as the `int` it
    is, so without the write-side conversion of `config_as_json` the buffer
    would be refreshed with a number that the field could not show as a
    name any more.
    """
    outcome = validate_buffer(config_type=IntEnumCfg,
                              members={'level': 'HIGH'})
    assert outcome.members == {'level': 'HIGH'}


def test_omitted_absent() -> None:
    """Test a member left out of JSON while None is not read back.

    The configuration class does not serialize it, so there is no value to
    read, which is different from a value that changed.
    """
    outcome = validate_buffer(config_type=OmitCfg,
                              members={'first': 1, 'last': 2})
    assert outcome.verdict.valid
    assert 'optional' not in outcome.members
