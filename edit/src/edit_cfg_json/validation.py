#! /usr/bin/env python3
"""Running the application's own validation over one edit buffer.

There are three passes here and they answer three different questions. What
the text of each member means is answered first, by the parse converter the
class declared for that member, because a value that does not exist cannot be
validated and the message the configuration class prints for one is about
JSON rather than about the member. What the application makes of the whole
buffer is answered next, by applying it to a candidate configuration, which is
the pass that decides whether the buffer is valid at all. And when that pass
refuses, the plan is walked a third time to say which members it was about,
because `Config.validate()` stops at the first step that refuses and can
therefore report one failure and never say whose it was.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from collections.abc import Mapping
from io import StringIO
from types import MappingProxyType
from typing import NamedTuple, Optional, TextIO
import json
from config_as_json import Config, ConfigPath, JsonType, \
    MemberValidationStep, MemberValidator, ValidationPlan, ValidationStep
from edit_cfg_json.constructing import parsed_config
from edit_cfg_json.converting import convert_member, node_converters, \
    refusal_text
from edit_cfg_json.tree import config_nodes, flat_values

BUFFER_ERRORS = (KeyError, TypeError, ValueError)
"""Every way in which a configuration class refuses an edit buffer.

`config_as_json` reports a key that is missing or unknown as `KeyError`,
text that is not JSON as `ConfigBadJson`, and a value that a validator
refuses as `InvalidConfiguration`, `InvalidConfigurationValue` or
`InvalidConfigurationType`. Those four are all `ValueError` subclasses, so
these three classes are exactly those failures and nothing besides them.

`NotImplementedError` is deliberately not one of them. It says that the
configuration class is incomplete, which is a defect of the application that
no edit of the buffer can put right, and hiding it in a verdict would send
the user looking for a mistake that is not theirs.
"""

NOTHING_REFUSED: Mapping[ConfigPath, str] = MappingProxyType({})
"""What a pass that refused no individual member reports.

It cannot be written to, because every verdict that names no member shares
this one mapping and a default that could be changed would be a defect
waiting to happen.
"""


class ValidationVerdict(NamedTuple):
    """What one validation pass over a whole edit buffer found."""

    valid: bool
    """Whether the application itself would accept this buffer."""

    diagnostics: str
    """What the application says that is about no single member.

    A whole-configuration validator that refused, a key that does not match,
    text that is not JSON, or a class the editor cannot construct at all.
    What the application said about one member is under `refused` instead, so
    that the same sentence is not shown twice.

    An accepted buffer can have diagnostics too, because a validator may
    remark on a value without refusing it.
    """

    refused: Mapping[ConfigPath, str] = NOTHING_REFUSED
    """What the application refused about each node, by the path of that node.

    Empty for a buffer that was accepted, and empty for one that was refused
    for a reason that is about no single member. A node is named here when
    its own text means no value of it at all, or when the validators of its
    member refused the value it holds.

    A path and not a name, because a value inside a list or a dict is a node
    of its own and two of them can share a name. What a member validator
    refused is about the whole member, since that is what it is given, so it
    is under the one step path of that member and never under a value inside
    it.
    """


class ValidationPass(NamedTuple):
    """The verdict of one validation pass and what it validated."""

    verdict: ValidationVerdict
    """What the pass found."""

    members: dict[str, JsonType]
    """One JSON space value per member of the accepted configuration.

    A member validator returns the value that is stored back into the
    member, so these are not necessarily the values the pass was given.
    They are empty when the buffer was refused, because there is then no
    configuration object to read them from.
    """

    candidate: Optional[Config]
    """The configuration object the pass built, None when it was refused.

    Saving writes this very object rather than building a second one from
    the same text, so that what reaches the file is what the verdict was
    reached about. It is also what `edit()` gives back to the application,
    which then needs no load of its own to see what was saved.
    """


class Attribution(NamedTuple):
    """What the individual validators of one configuration refused."""

    refused: dict[ConfigPath, str]
    """What the validators of each member said, by the path of that member."""

    remaining: str
    """What a step that is about no single member said, empty when none."""


def _told(captured: str, error: Exception) -> str:
    """Return what one refusal says, and its exception when it said nothing.

    The captured text is what the application itself would have printed, so
    it is what the user is shown. A failure that printed nothing has only
    its exception left to report, which is better than no explanation.

    Args:
        captured: What the refusing code wrote to its diagnostics stream.
        error: The failure that it reported.

    Returns:
        What to tell the user about that refusal.
    """
    return captured.strip() or f'{type(error).__name__}: {refusal_text(error)}'


PLAN_METHOD = 'get_validation_plan'
"""Name of the method that the probe below has replaced with nothing."""


def _no_plan(stderr_file: TextIO) -> ValidationPlan:
    """Return no validation steps at all, for the probe object.

    It is an attribute of one object rather than a method of a class, so it is
    called without the object, exactly as `parse_converters` and the rest of
    the parse call the real method.
    """
    _ = stderr_file
    return []


def _probe(config: Config, members: dict[str, JsonType]) -> Optional[Config]:
    """Return the buffer in an object that has not been validated.

    A configuration object normally cannot hold a buffer without being
    validated: `Config.parse_json` ends in `validate()`, which raises at the
    first step that refuses. So the object that could say which member was
    refused is exactly the object that a refusal keeps the editor from ever
    holding.

    A copy whose validation plan is empty is that object. Everything else the
    parse does still happens — the keys are matched, the dict shapes are
    checked, the parse converters run, the nested configuration objects are
    built — and only the plan is left out, which is what the walk below then
    applies itself, one member at a time.

    That is also why the buffer is parsed rather than assigned onto the object
    member by member. Assigning would mean applying the parse converters here,
    which is a second implementation of what `config_as_json` does while it
    parses, and it would put a plain dict where a nested configuration object
    belongs. The one method left out is the whole of what this borrows.

    Args:
        config: Configuration object of this session. It is not modified.
        members: The edit buffer, as one JSON space value per member.

    Returns:
        An object holding the buffer, or None when the buffer is not a
        configuration of this class at all.
    """
    try:
        return parsed_config(config, json.dumps(members), stream=StringIO(),
                             replace=PLAN_METHOD, method=_no_plan)
    except BUFFER_ERRORS:
        return None


def _unconverted(config: Config,
                 members: dict[str, JsonType]) -> dict[ConfigPath, str]:
    """Return why each value of the buffer means no value of its node.

    Every node is asked, and the converter that answers for it is the one its
    own owning class declares: a value inside a nested configuration object is
    parsed by that object and not by the one above it. A node that no
    converter reaches is asked with none, which nothing can refuse.

    Args:
        config: Configuration object of this session, which says which nodes
            are configuration objects of their own. It is not modified.
        members: The edit buffer, as one JSON space value per member.

    Returns:
        One message per node whose text means no value of it, and nothing
        at all for a buffer every value of which means something.
    """
    nodes = config_nodes(config)
    flat = flat_values(members=members, nodes=nodes)
    converters = node_converters(nodes=nodes, flat=flat)
    refused = {path: convert_member(converter=converters.get(path),
                                    value=value).message
               for path, value in flat}
    return {path: message for path, message in refused.items() if message}


def _attribute_member(validator: MemberValidator, probe: Config, name: str,
                      refused: dict[ConfigPath, str]) -> None:
    """Run one validator over one member, keeping what it refused.

    The value the validator returns is stored back into the member, because
    that is what the real pass does with it and what a later validator of the
    same member is then given.

    Args:
        validator: Validator to run.
        probe: Configuration object holding the buffer. It is modified.
        name: Name of the member to validate.
        refused: What each member has been refused for so far, added to.
    """
    captured = StringIO()
    try:
        value = validator.validate_member(config=probe, member_name=name,
                                          member_value=getattr(probe, name),
                                          stderr_file=captured)
    except BUFFER_ERRORS as error:
        refused[(name,)] = _told(captured=captured.getvalue(), error=error)
        return
    setattr(probe, name, value)


def _attribute_step(step: MemberValidationStep, probe: Config,
                    refused: dict[ConfigPath, str]) -> None:
    """Run one member validator over each of the members that step names.

    A member that has already been refused is left alone, so that what is
    reported about it is the first thing that was wrong with it, which is
    also the one the real pass would have reported.

    Args:
        step: Validation step to apply.
        probe: Configuration object holding the buffer. It is modified.
        refused: What each member has been refused for so far, added to.
    """
    for name in step.member_names:
        if not hasattr(probe, name) or (name,) in refused:
            continue
        _attribute_member(validator=step.validator, probe=probe, name=name,
                          refused=refused)


def _step_refusal(step: ValidationStep, probe: Config) -> str:
    """Return what one step that is about no single member refused, if any.

    Args:
        step: Validation step to apply.
        probe: Configuration object holding the buffer. It is modified, as a
            whole-configuration validator is free to modify one.

    Returns:
        What that step said when it refused, and nothing when it did not.
    """
    captured = StringIO()
    try:
        step.apply(probe, captured)
    except BUFFER_ERRORS as error:
        return _told(captured=captured.getvalue(), error=error)
    return ''


def _plan_failures(probe: Config) -> Attribution:
    """Walk the validation plan far enough to say which members are refused.

    `Config.validate()` stops at the first step that refuses, so the pass
    that decides the verdict can report one failure and cannot say which
    member it was about. This walks the same plan and differs in two ways: a
    member that is refused is recorded and the walk goes on, so that every
    member the user has to correct is named at once, and a step that is about
    no single member is applied only while no member has been refused,
    because that is the only case in which the real pass would have reached
    it.

    No validator class is recognised by type in any of this. What is read is
    `MemberValidationStep.member_names` and `MemberValidationStep.validator`,
    both of which are public, so an application's own `MemberValidator`
    subclass is attributed exactly as the ones `config_as_json` ships are.

    The plan is asked of the class and not of the object, because it is the
    object that has no plan: what was replaced on it is the very method that
    answers this. The class of the probe is the class being edited, so what is
    applied here is the application's own plan, step by step, which is the
    whole point.

    Args:
        probe: Configuration object holding the buffer, not yet validated. It
            is modified: a member validator returns the value that is stored
            back into the member, exactly as the real pass stores it.

    Returns:
        What each member was refused for, and what could not be attributed to
        any member at all.
    """
    refused: dict[ConfigPath, str] = {}
    plan = type(probe).get_validation_plan(probe, stderr_file=StringIO())
    for step in plan:
        if isinstance(step, MemberValidationStep):
            _attribute_step(step=step, probe=probe, refused=refused)
            continue
        if refused:
            break
        remaining = _step_refusal(step=step, probe=probe)
        if remaining:
            return Attribution(refused=refused, remaining=remaining)
    return Attribution(refused=refused, remaining='')


def _attribution(config: Config, members: dict[str, JsonType]) -> Attribution:
    """Return what the validators of one refused buffer were about.

    Args:
        config: Configuration object of this session. It is not modified.
        members: The edit buffer, as one JSON space value per member.

    Returns:
        What each member was refused for, and what could not be attributed.
        Both are empty when the buffer is not a configuration of this class
        at all, which is a refusal about no member and no value.
    """
    probe = _probe(config=config, members=members)
    if probe is None:
        return Attribution(refused={}, remaining='')
    return _plan_failures(probe)


def _refused_verdict(config: Config, members: dict[str, JsonType],
                     captured: str, error: Exception) -> ValidationVerdict:
    """Return the verdict of a pass that the configuration class refused.

    What the class printed is kept only when nothing at all could be
    attributed to a member, which is what happens when the refusal was about
    the shape of the buffer rather than about a value: a key that does not
    match, text that is not JSON, a class that cannot be constructed. What
    the attribution did explain is shown beside the member it is about
    instead, so that the same sentence is not on the screen twice.

    Args:
        config: Configuration object of this session. It is not modified.
        members: The edit buffer, as one JSON space value per member.
        captured: What the refused parse wrote to its stream.
        error: The failure that the parse reported.

    Returns:
        A verdict saying that the buffer is not a configuration, and why.
    """
    found = _attribution(config=config, members=members)
    if found.refused or found.remaining:
        return ValidationVerdict(valid=False, diagnostics=found.remaining,
                                 refused=found.refused)
    return ValidationVerdict(valid=False,
                             diagnostics=_told(captured=captured, error=error))


def _no_pass(verdict: ValidationVerdict) -> ValidationPass:
    """Return the pass of a buffer that never became a configuration."""
    return ValidationPass(verdict=verdict, members={}, candidate=None)


def validate_buffer(config: Config,
                    members: dict[str, JsonType]) -> ValidationPass:
    """Validate one edit buffer by applying it to a candidate configuration.

    The buffer is applied to a copy of the configuration object with
    `Config.parse_json`, which runs the whole chain the application runs when
    it reads its own file: key matching, the recursive check of dict shapes
    against the defaults, the parse converters, the nested configuration
    objects and then the validation plan. So the user sees exactly the
    diagnostics that the application would produce, there is no second
    implementation of validation anywhere, and there is no way for the editor
    to accept something the application would then refuse.

    The class is not constructed, and it is not asked to be. What a
    construction would add is the declaring of the members, which a copy has
    already, so a class that needs a constructor argument this library knows
    nothing about is validated here exactly as well as any other.

    What each value means is settled before that, by running the parse
    converter of its member. A value that means nothing is reported as the
    one member it is about, and the candidate is not built at all: it would
    only report the same thing as text it could not read as JSON, which is
    an answer to a question the user did not ask.

    The stream the candidate writes to is captured rather than passed on,
    because these diagnostics are the answer to a question the user asked
    and belong on the screen and not in the terminal behind it.

    Args:
        config: Configuration object of this session, which says which class
            the buffer belongs to and holds everything about it that is not a
            member. It is not modified.
        members: The edit buffer, as one JSON space value per member.

    Returns:
        What the pass found, and the members of the configuration object it
        built. The members are empty when the buffer was refused.
    """
    unconverted = _unconverted(config=config, members=members)
    if unconverted:
        return _no_pass(ValidationVerdict(valid=False, diagnostics='',
                                          refused=unconverted))
    diagnostics = StringIO()
    try:
        candidate = parsed_config(config, json.dumps(members),
                                  stream=diagnostics)
        validated = json.loads(
            candidate.as_json_string(stderr_file=diagnostics))
    except BUFFER_ERRORS as error:
        return _no_pass(_refused_verdict(config=config, members=members,
                                         captured=diagnostics.getvalue(),
                                         error=error))
    assert isinstance(validated, dict)
    accepted = ValidationVerdict(valid=True,
                                 diagnostics=diagnostics.getvalue())
    return ValidationPass(verdict=accepted, members=validated,
                          candidate=candidate)
