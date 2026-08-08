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

from collections.abc import Callable, Mapping
from config_as_json import Config, ConfigPath, JsonType
import pytest
from edit_cfg_json.validation import validate_buffer
from .sample_cfg import HIGHEST, REFUSAL_MESSAGE, SUM_LIMIT, \
    TOO_LARGE_MESSAGE, AllowedCfg, EnumCfg, ExtraArgCfg, FlatCfg, HexCfg, \
    IntEnumCfg, ListCfg, OmitCfg, RangeCfg, RefuseCfg, RewriteCfg, RulesCfg, \
    TypedCfg

ENUM_NAMES = 'is not one of: LOWEST, LOW, HIGH'
"""What the diagnostics say about text that names no member of `Level`."""

REFUSED_BUFFERS: list[tuple[str, Callable[[], Config],
                            dict[str, JsonType], str, str]] = [
    ('missing key', FlatCfg, {'name': 'text'}, '', 'No value for answer'),
    ('unknown key', FlatCfg, {'name': 'text', 'answer': 1, 'more': 2}, '',
     'Unexpected parameter more'),
    ('no enum member', EnumCfg, {'colour': 'PURPLE'}, 'colour',
     'PURPLE is not one of: RED, GREEN'),
    ('no int enum member', IntEnumCfg, {'level': 'MIDDLE'}, 'level',
     ENUM_NAMES),
    ('ambiguous name', IntEnumCfg, {'level': 'LO'}, 'level', ENUM_NAMES),
    ('enum as a number', IntEnumCfg, {'level': 2}, 'level',
     'not str as expected'),
    ('own converter', HexCfg, {'mask': 'zz'}, 'mask', 'base 16'),
    ('outside range', RangeCfg, {'answer': 500}, 'answer',
     'is greater than maximum 100'),
    ('not allowed', AllowedCfg, {'colour': 'blue'}, 'colour', 'colour'),
    ('wrong type', TypedCfg, {'count': 'text'}, 'count', 'is not of type int'),
    ('own validator', RefuseCfg, {'name': 'other'}, 'name',
     REFUSAL_MESSAGE.format(name='name')),
    ('rule about both', RulesCfg, {'first': HIGHEST, 'second': HIGHEST}, '',
     TOO_LARGE_MESSAGE.format(total=2 * HIGHEST))]
"""One buffer per way in which a configuration class refuses a buffer.

The first item of each is the name of the case, which pytest uses to identify
it. The fourth is the member the refusal is about, empty for a refusal that
is about no single member, and the last is text that has to appear where the
fourth one says it does.
"""


def _refusal_text(outcome_refused: Mapping[ConfigPath, str], diagnostics: str,
                  member: str) -> str:
    """Return the text of one refusal, from wherever it belongs.

    Args:
        outcome_refused: What the pass said about each node, by path.
        diagnostics: What it said that is about no single member.
        member: Member the refusal is about, empty when it is about none.

    Returns:
        What was said about that member, or what was said about no member.
    """
    if not member:
        assert not outcome_refused
        return diagnostics
    assert set(outcome_refused) == {(member,)}
    return outcome_refused[(member,)]


@pytest.mark.parametrize('name, config_type, members, member, expected',
                         REFUSED_BUFFERS)
def test_refused_buffer(name: str, config_type: Callable[[], Config],
                        members: dict[str, JsonType], member: str,
                        expected: str) -> None:
    """Test every way of refusing a buffer becomes a verdict, not a crash.

    Where the text of the refusal appears is part of what is tested, because
    a refusal that is about one member belongs beside that member and one
    that is about no member has nowhere else to go than the block.
    """
    outcome = validate_buffer(config=config_type(), members=members)
    assert not outcome.verdict.valid, name
    told = _refusal_text(outcome_refused=dict(outcome.verdict.refused),
                         diagnostics=outcome.verdict.diagnostics,
                         member=member)
    assert expected in told, name
    assert not outcome.members


def test_every_bad_member() -> None:
    """Test every member that is refused is named, and not only the first.

    `Config.validate()` stops at the first step that refuses, so a user who
    was told only what that step said would correct one member per pass. The
    walk that attributes the refusals does not stop, which is the whole gain.
    """
    outcome = validate_buffer(config=RulesCfg(),
                              members={'first': 500, 'second': 700})
    assert set(outcome.verdict.refused) == {('first',), ('second',)}
    assert '500' in outcome.verdict.refused[('first',)]
    assert '700' in outcome.verdict.refused[('second',)]


def test_good_member_silent() -> None:
    """Test a member the application accepted is not named."""
    outcome = validate_buffer(config=RulesCfg(),
                              members={'first': 500, 'second': 2})
    assert set(outcome.verdict.refused) == {('first',)}


def test_whole_rule_skipped() -> None:
    """Test a rule about no single member is left alone while one is refused.

    `Config.validate()` would have stopped at the member before it, so an
    editor that reported that rule anyway would be reporting something the
    application never did.
    """
    outcome = validate_buffer(config=RulesCfg(),
                              members={'first': 500, 'second': 500})
    assert outcome.verdict.diagnostics == ''


def test_rule_about_both() -> None:
    """Test a rule about two members is reported for neither of them.

    Both members are values their own validators accept, so there is no
    member this refusal could honestly be put beside.
    """
    outcome = validate_buffer(config=RulesCfg(),
                              members={'first': HIGHEST, 'second': HIGHEST})
    assert not outcome.verdict.refused
    assert TOO_LARGE_MESSAGE.format(total=2 * HIGHEST) in \
        outcome.verdict.diagnostics
    assert 2 * HIGHEST > SUM_LIMIT


def test_silent_refusal_told() -> None:
    """Test a refusal that wrote no diagnostics is still explained.

    An application's own validator is free to raise without writing
    anything, and the user would otherwise be shown that the buffer is
    invalid and nothing at all about why. What is asserted is the exception
    reaching the member.
    """
    outcome = validate_buffer(config=RefuseCfg(), members={'name': 'x'})
    assert outcome.verdict.refused[('name',)].startswith('ValueError: ')


def test_unbuildable_valid() -> None:
    """Test a buffer of a class the editor cannot construct is validated.

    `ExtraArgCfg` needs a constructor argument this library knows nothing
    about, so nothing here could construct one. It does not have to: the
    buffer is applied to a copy of the object that is being edited, which the
    application built, and the class then validates it as it validates
    anything.
    """
    outcome = validate_buffer(config=ExtraArgCfg(home='here'),
                              members={'home': 'elsewhere'})
    assert outcome.verdict.valid
    assert outcome.members == {'home': 'elsewhere'}
    assert isinstance(outcome.candidate, ExtraArgCfg)


@pytest.mark.parametrize('config_type, members',
                         [(FlatCfg, {'name': 'text', 'answer': 7}),
                          (ListCfg, {'tags': ['one'], 'limits': {'low': 2,
                                                                 'high': 3},
                                     'answer': 3}),
                          (OmitCfg, {'first': 1, 'last': 2}),
                          (EnumCfg, {'colour': 'GREEN'}),
                          (IntEnumCfg, {'level': 'HIGH'}),
                          (RangeCfg, {'answer': 100}),
                          (HexCfg, {'mask': 16}),
                          (RulesCfg, {'first': 1, 'second': 2})])
def test_accepted_buffer(config_type: Callable[[], Config],
                         members: dict[str, JsonType]) -> None:
    """Test an accepted buffer is reported as valid and says nothing more."""
    outcome = validate_buffer(config=config_type(), members=members)
    assert outcome.verdict.valid
    assert outcome.verdict.diagnostics == ''
    assert not outcome.verdict.refused


def test_members_read_back() -> None:
    """Test the members of the accepted configuration object are returned."""
    outcome = validate_buffer(config=FlatCfg(),
                              members={'name': 'text', 'answer': 7})
    assert outcome.members == {'name': 'text', 'answer': 7}


def test_rewritten_returned() -> None:
    """Test the value a validator stored back is what is returned.

    This is what makes a validation pass anything but read only, and the
    reason the buffer is refreshed from the object that was built rather
    than left holding what the user typed.
    """
    outcome = validate_buffer(config=RewriteCfg(),
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
    outcome = validate_buffer(config=IntEnumCfg(), members={'level': typed})
    assert outcome.verdict.valid
    assert outcome.members == {'level': whole}


def test_int_enum_is_a_name() -> None:
    """Test an int enum member is read back as its name and not its number.

    Python's own JSON encoder treats an `IntEnum` member as the `int` it
    is, so without the write-side conversion of `config_as_json` the buffer
    would be refreshed with a number that the field could not show as a
    name any more.
    """
    outcome = validate_buffer(config=IntEnumCfg(), members={'level': 'HIGH'})
    assert outcome.members == {'level': 'HIGH'}


def test_omitted_absent() -> None:
    """Test a member left out of JSON while None is not read back.

    The configuration class does not serialize it, so there is no value to
    read, which is different from a value that changed.
    """
    outcome = validate_buffer(config=OmitCfg(),
                              members={'first': 1, 'last': 2})
    assert outcome.verdict.valid
    assert 'optional' not in outcome.members
