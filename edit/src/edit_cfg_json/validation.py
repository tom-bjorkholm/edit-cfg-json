#! /usr/bin/env python3
"""Running the application's own validation over one edit buffer.

There are four passes here and they answer four different questions. What
the text of each member means is answered first, by the parse converter the
class declared for that member, because a value that does not exist cannot be
validated and the message the configuration class prints for one is about
JSON rather than about the member. What the application makes of the whole
buffer is answered next, by applying it to a candidate configuration, which is
the pass that decides whether the buffer is valid at all. And when that pass
refuses, the plan is walked a third time to say which members it was about,
because `Config.validate()` stops at the first step that refuses and can
therefore report one failure and never say whose it was.

The fourth is every nested configuration object asked on its own, and it
answers what the third one cannot reach. Such an object validates itself while
`parse_json` builds it, so a refusal from inside it keeps the walk above from
ever holding an object to walk: the probe is a copy of the configuration with
one method left out, and the nested objects inside that copy are built by the
library and validate themselves as they always do. Applying one subtree of the
buffer to the object that owns it is what reaches them, and it answers the
other question a nested object raises as well — whether it is a configuration
on its own, which is what its row says while the whole configuration is
refused for a reason that is about something else entirely.
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
from edit_cfg_json.tree import ConfigNode, config_nodes, file_values, \
    flat_values, omitted_paths

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


class SubtreeAnswer(NamedTuple):
    """What asking one nested configuration object about itself found."""

    valid: bool
    """Whether that object is a configuration on its own."""

    refused: Mapping[ConfigPath, str] = NOTHING_REFUSED
    """What it refused, by the absolute path of the node it is about.

    It is a member of that object wherever a member validator refused one, and
    the object itself where its class refused it for a reason that is about no
    member of it. It is empty for an object that was accepted, and empty for
    one that is refused only because an object inside it is: that mistake is
    reported once, at the object it is really about.

    It is kept beside the state rather than thrown away, because the state on
    its own says that something is wrong and never says what, and a user who
    folds an object to be told that much has to open it again and ask a second
    question to find out.
    """


NO_SUBTREES: Mapping[ConfigPath, SubtreeAnswer] = MappingProxyType({})
"""What a pass over a configuration with no nested object at all reports.

It cannot be written to, for the same reason as the mapping above.
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

    subtrees: Mapping[ConfigPath, SubtreeAnswer] = NO_SUBTREES
    """What each nested object is on its own, by the path of its node.

    A subtree can be valid while the whole configuration is not, which is what
    a rule relating two of them across the boundary does, and that is the
    honest state rather than a contradiction. It is a different question from
    the verdict and it is answered separately, so a row can say what its own
    object amounts to without saying anything about the file.

    A member declared to hold an object and holding none is not here, because
    there is nothing to validate; and a pass the class accepted answers for
    every one of them at once, since `parse_json` built and validated each of
    them while it read the buffer.
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
        members: The buffer as a file of this configuration would hold it,
            which is what `file_values` answers with.

    Returns:
        An object holding the buffer, or None when the buffer is not a
        configuration of this class at all.
    """
    try:
        return parsed_config(config, json.dumps(members), stream=StringIO(),
                             replace=PLAN_METHOD, method=_no_plan)
    except BUFFER_ERRORS:
        return None


def _unconverted(config: Config, members: dict[str, JsonType],
                 bool_nodes: frozenset[ConfigPath]) -> dict[ConfigPath, str]:
    """Return why each value of the buffer means no value of its node.

    Every node is asked, and the converter that answers for it is the one its
    own owning class declares: a value inside a nested configuration object is
    parsed by that object and not by the one above it. A node that no
    converter reaches is asked with none, which nothing but a member holding
    true or false can refuse.

    Args:
        config: Configuration object of this session, which says which nodes
            are configuration objects of their own. It is not modified.
        members: The edit buffer, as one JSON space value per member.
        bool_nodes: Path of every node that holds true or false.

    Returns:
        One message per node whose text means no value of it, and nothing
        at all for a buffer every value of which means something.
    """
    nodes = config_nodes(config)
    flat = flat_values(members=members, nodes=nodes)
    converters = node_converters(nodes=nodes, flat=flat)
    refused = {path: convert_member(converter=converters.get(path),
                                    value=value,
                                    is_bool_member=path in bool_nodes).message
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
        members: The buffer as a file of this configuration would hold it.

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
        members: The buffer as a file of this configuration would hold it.
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


def _single_pass(config: Config, members: dict[str, JsonType],
                 bool_nodes: frozenset[ConfigPath]) -> ValidationPass:
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
    nothing about is validated here exactly as well as any other. That is also
    what lets one nested object be asked the very same question about the part
    of the buffer it owns: the object is there to be copied, whatever its
    class would have needed to be built from nothing.

    What each value means is settled before that, by running the parse
    converter of its member. A value that means nothing is reported as the
    one member it is about, and the candidate is not built at all: it would
    only report the same thing as text it could not read as JSON, which is
    an answer to a question the user did not ask.

    What the class is asked to read is the buffer as a *file* of it would be
    written, so a member that holds nothing and that this class leaves out of
    its files is left out here too. What is validated is then the document
    that a save writes, which is what keeps the verdict about the file rather
    than about a document with a `null` in it that no save produces.

    The stream the candidate writes to is captured rather than passed on,
    because these diagnostics are the answer to a question the user asked
    and belong on the screen and not in the terminal behind it.

    Args:
        config: Configuration object that the buffer belongs to, which holds
            everything about it that is not a member. It is not modified.
        members: The edit buffer, as one JSON space value per member.
        bool_nodes: Path of every node that holds true or false, which is the
            type information the buffer holds and these values do not.

    Returns:
        What the pass found, and the members of the configuration object it
        built. The members are empty when the buffer was refused.
    """
    unconverted = _unconverted(config=config, members=members,
                               bool_nodes=bool_nodes)
    if unconverted:
        return _no_pass(ValidationVerdict(valid=False, diagnostics='',
                                          refused=unconverted))
    diagnostics = StringIO()
    written = file_values(members=members,
                          omitted=omitted_paths(config_nodes(config)))
    try:
        candidate = parsed_config(config, json.dumps(written),
                                  stream=diagnostics)
        validated = json.loads(
            candidate.as_json_string(stderr_file=diagnostics))
    except BUFFER_ERRORS as error:
        return _no_pass(_refused_verdict(config=config, members=written,
                                         captured=diagnostics.getvalue(),
                                         error=error))
    assert isinstance(validated, dict)
    accepted = ValidationVerdict(valid=True,
                                 diagnostics=diagnostics.getvalue())
    return ValidationPass(verdict=accepted, members=validated,
                          candidate=candidate)


def _deepest_first(nodes: Mapping[ConfigPath, ConfigNode],
                   inside: ConfigPath) -> list[ConfigPath]:
    """Return the path of every nested object of one region, innermost first.

    An object holding a refused object is refused whatever else is true of it,
    so the innermost are asked first and one with a refused object inside it
    is then not asked at all. That is what keeps a single mistake from being
    reported once for every object it happens to be inside.

    Args:
        nodes: Every configuration object of the tree, by its path.
        inside: Path of the node to ask about, the empty path for the whole
            configuration. Every object at or inside it is asked, which is
            what makes one list or dict of objects answerable: such a member
            is no configuration itself and every element of it is one.

    Returns:
        The path of every nested object of that region, the longest paths
        first. The configuration itself is left out: it is the whole
        configuration and not a subtree of one.
    """
    return sorted((path for path in nodes
                   if path and path[:len(inside)] == inside),
                  key=len, reverse=True)


def _refused_inside(path: ConfigPath,
                    answers: Mapping[ConfigPath, SubtreeAnswer]) -> bool:
    """Return whether an object inside one node has already been refused."""
    return any(not answer.valid for other, answer in answers.items()
               if len(other) > len(path) and other[:len(path)] == path)


def _own_refusal(path: ConfigPath,
                 verdict: ValidationVerdict) -> dict[ConfigPath, str]:
    """Return what one nested object refused about no member of itself.

    A rule of its own class that is about no single member is about the
    object, and the object is a node with a row of its own, so it is said
    there rather than in the block below the members: a configuration of any
    size does not fit a window, and a message that names no place sends the
    user looking for one.

    Args:
        path: Path of the node the object is at.
        verdict: What asking that object on its own found.

    Returns:
        What to say at that node, and nothing at all when the object said
        nothing that was not already attributed to a member of it.
    """
    said = verdict.diagnostics.strip()
    return {path: said} if said else {}


def _inside(bool_nodes: frozenset[ConfigPath],
            path: ConfigPath) -> frozenset[ConfigPath]:
    """Return the nodes inside one object, by the path that object knows.

    A nested object is asked about its own part of the buffer, where its own
    members are the outermost nodes, so the path of every node inside it loses
    the steps that reach the object itself.

    Args:
        bool_nodes: Path of every node that holds true or false.
        path: Path of the node the object is at.

    Returns:
        Those of them that are inside it, each without that path in front.
    """
    return frozenset(node[len(path):] for node in bool_nodes
                     if node[:len(path)] == path)


def _record_subtree(path: ConfigPath, node: ConfigNode, value: JsonType,
                    answers: dict[ConfigPath, SubtreeAnswer],
                    bool_nodes: frozenset[ConfigPath]) -> None:
    """Ask one nested object about its own part of the buffer.

    Args:
        path: Path of the node the object is at.
        node: What the class declares there, and what is really there.
        value: What the buffer holds for that node.
        answers: What the objects inside it said, which this adds to.
        bool_nodes: Path of every node of the whole tree that holds true or
            false.
    """
    if node.config is None or not isinstance(value, dict):
        return
    if _refused_inside(path=path, answers=answers):
        answers[path] = SubtreeAnswer(valid=False)
        return
    verdict = _single_pass(config=node.config, members=value,
                           bool_nodes=_inside(bool_nodes=bool_nodes,
                                              path=path)).verdict
    if verdict.valid:
        answers[path] = SubtreeAnswer(valid=True)
        return
    inside = {path + node_path: message
              for node_path, message in verdict.refused.items()}
    answers[path] = SubtreeAnswer(
        valid=False, refused=inside or _own_refusal(path=path,
                                                    verdict=verdict))


def subtree_answers(config: Config, members: dict[str, JsonType],
                    inside: ConfigPath = (),
                    bool_nodes: frozenset[ConfigPath] = frozenset()
                    ) -> dict[ConfigPath, SubtreeAnswer]:
    """Return what every nested object of one region says about itself.

    This is what folding asks, and it is the cheap local question that
    section 6.2 of `doc/design.md` makes folding the trigger for: it needs no
    candidate configuration and says nothing about the file.

    A region and not a single node, because the member that holds several
    configuration objects is a list or a dict and is no configuration itself.
    Folding one of those hides every object in it, so folding one of those has
    to ask every object in it; asking only the node that was folded would
    answer nothing at all for exactly the shape a real configuration has.

    Args:
        config: Configuration object of this session, which says which nodes
            are configuration objects of their own. It is not modified.
        members: The edit buffer, as one JSON space value per member.
        inside: Path of the node being asked about, the empty path for the
            whole configuration. Every object at or inside it is asked.
        bool_nodes: Path of every node that holds true or false, empty for a
            caller that knows of none.

    Returns:
        One answer per nested object of that region that is really there. A
        member declared to hold an object and holding none is not here,
        because there is nothing to ask.
    """
    nodes = config_nodes(config)
    values = dict(flat_values(members=members, nodes=nodes))
    answers: dict[ConfigPath, SubtreeAnswer] = {}
    for path in _deepest_first(nodes=nodes, inside=inside):
        _record_subtree(path=path, node=nodes[path], value=values.get(path),
                        answers=answers, bool_nodes=bool_nodes)
    return answers


def _accepted_subtrees(candidate: Config) -> dict[ConfigPath, SubtreeAnswer]:
    """Return every nested object of an accepted configuration, as valid.

    A pass the class accepted built and validated every nested object inside
    it while it parsed the buffer, so each of them is a configuration on its
    own and none has to be asked again.

    Args:
        candidate: Configuration object that the pass built and accepted. It
            is not modified, and it is the object the buffer is rebuilt from,
            so its paths are the paths the rows will have.

    Returns:
        The path of every nested object of it, each of them valid.
    """
    return {path: SubtreeAnswer(valid=True)
            for path, node in config_nodes(candidate).items()
            if path and node.config is not None}


def _every_refusal(answers: Mapping[ConfigPath, SubtreeAnswer]
                   ) -> dict[ConfigPath, str]:
    """Return what every nested object refused, by the node it is about."""
    return {path: message for answer in answers.values()
            for path, message in answer.refused.items()}


def _with_subtrees(verdict: ValidationVerdict,
                   answers: Mapping[ConfigPath, SubtreeAnswer]
                   ) -> ValidationVerdict:
    """Return one refused verdict with what the nested objects refused in it.

    What the whole pass printed is dropped wherever a nested object explained
    the refusal and the pass itself attributed nothing, because the two then
    say the same thing and the nested one says it at the node it is about. A
    pass that did attribute something reached its own validation plan, so what
    it printed is about something else and is kept.

    Args:
        verdict: What applying the whole buffer found.
        answers: What each nested object said about itself.

    Returns:
        That verdict, with every refusal from inside a nested object in it.
    """
    inside = _every_refusal(answers)
    if not inside:
        return verdict
    refused = dict(inside)
    refused.update(verdict.refused)
    said = verdict.diagnostics if verdict.refused else ''
    return verdict._replace(refused=refused, diagnostics=said)


def validate_buffer(config: Config, members: dict[str, JsonType],
                    bool_nodes: frozenset[ConfigPath] = frozenset()
                    ) -> ValidationPass:
    """Validate one edit buffer, and every nested object of it on its own.

    The whole buffer decides the verdict, by `_single_pass`, which is the
    application's own reading of its own file and the only thing that says
    whether these values could be saved. Each nested configuration object is
    then asked the same question about the part of the buffer it owns, which
    answers the two things that pass cannot.

    It says whether that object is a configuration on its own, which is a
    different state from the verdict and has to be shown as one: a rule of the
    class above relates two objects across the boundary between them, so both
    of them can be valid while the configuration is refused.

    And it says which member of a nested object was refused. Such an object
    validates itself while `parse_json` builds it, so the walk of section 6.3
    of `doc/design.md` never gets an object to walk and would leave the
    message in the block below the members. Applying the subtree to the object
    that owns it is what reaches the member.

    None of that is asked of a pass the class accepted: `parse_json` built and
    validated every nested object while it read the buffer, so all of them are
    valid and there is nothing left to find out.

    Args:
        config: Configuration object of this session, which says which class
            the buffer belongs to and holds everything about it that is not a
            member. It is not modified.
        members: The edit buffer, as one JSON space value per member.
        bool_nodes: Path of every node that holds true or false, empty for a
            caller that knows of none. The values are in JSON space, where
            nothing says which member takes those two and only those two.

    Returns:
        What the pass found, the members of the configuration object it built,
        and what each nested object is on its own.
    """
    outcome = _single_pass(config=config, members=members,
                           bool_nodes=bool_nodes)
    if outcome.verdict.valid:
        assert outcome.candidate is not None
        accepted = _accepted_subtrees(outcome.candidate)
        return outcome._replace(subtrees=accepted)
    answers = subtree_answers(config=config, members=members,
                              bool_nodes=bool_nodes)
    return outcome._replace(
        verdict=_with_subtrees(verdict=outcome.verdict, answers=answers),
        subtrees=answers)
