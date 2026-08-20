#! /usr/bin/env python3
"""Tests for the explanatory text about a configuration and its members.

The three sources are tested separately here, because they are independent: a
class has a docstring or has not, an application describes a member or does
not, and a member has a type that says something or has not, and none of
those says anything about the others.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from config_as_json import ConfigPath, JsonType, ParseConverter
import pytest
from edit_cfg_json import Descriptions
from edit_cfg_json.converting import member_converters
from edit_cfg_json.descriptions import MemberFacts, NOTHING_TEXT, \
    OPTIONAL_TEXT, \
    class_docstring, class_summary, enum_text, member_description, \
    optional_members, optional_paths, path_description
from edit_cfg_json.leaf_value import BOOL_KIND, LeafType, NO_KIND, \
    NUMBER_KIND, TEXT_KIND, WHOLE_NUMBER_KIND, kind_text
from edit_cfg_json.tree import config_nodes
from .container_cfg import OwnedOptionCfg
from .sample_cfg import DocumentedCfg, EnumCfg, FlatCfg, HexCfg, IntEnumCfg, \
    NoDocCfg, OmitCfg, PlainEnumCfg, SampleCfg, WrappedDocCfg

SUMMARY = 'One line that says what this configuration is for.'
"""The summary paragraph of the docstring of `DocumentedCfg`."""

DETAIL = 'A second paragraph that is the detail of this class.'
"""The paragraph below the summary in that docstring."""

WHOLE = f'{SUMMARY}\n\n{DETAIL}'
"""That whole docstring as `inspect.cleandoc` leaves it.

The indentation of the source file is gone, and the blank line that separates
the summary from the detail is not.
"""

FLAT_SUMMARY = 'A configuration with one text member and one number member.'
"""The whole docstring of `FlatCfg`, which is a summary and nothing else."""

WRAPPED_SUMMARY = ('A summary that is long enough to have been written on two '
                   'lines of the source file.')
"""The summary of `WrappedDocCfg`, as the one line that it becomes."""

ABOUT_LOW = 'What the low limit is for.'
"""Description of one specific member of a dict."""

ABOUT_ANY = 'What any one of these limits is for.'
"""Description of every member of a dict at once."""

ABOUT_COLOUR = 'What this colour is used for.'
"""Description that an application writes about an enum member."""

COLOUR_SUMMARY = 'The values that the enum member of `EnumCfg` can hold.'
"""The whole docstring of `Colour`, which is a summary and nothing else."""

LEVEL_SUMMARY = 'The values that the int enum member of `IntEnumCfg` can hold.'
"""The summary of the docstring of `Level`, which has a detail as well."""


def test_exact_selector() -> None:
    """Test a selector that names a member describes that member."""
    descriptions: Descriptions = {('name',): 'What the name is for.'}
    assert path_description(descriptions, ('name',)) == 'What the name is for.'


def test_other_member() -> None:
    """Test a member that no selector names has no description."""
    descriptions: Descriptions = {('name',): 'What the name is for.'}
    assert path_description(descriptions, ('answer',)) == ''


def test_no_descriptions() -> None:
    """Test an application that describes nothing describes nothing."""
    assert path_description({}, ('name',)) == ''


def test_every_element() -> None:
    """Test the `'['` step describes every value at that point.

    That is the meaning `config_as_json` gives the step, and it is what keeps
    an application from having to repeat one description per key.
    """
    descriptions: Descriptions = {('limits', '['): ABOUT_ANY}
    assert path_description(descriptions, ('limits', 'low')) == ABOUT_ANY
    assert path_description(descriptions, ('limits', 'high')) == ABOUT_ANY


def test_wrong_length() -> None:
    """Test a selector describes the member it addresses and nothing above."""
    descriptions: Descriptions = {('limits', '['): ABOUT_ANY}
    assert path_description(descriptions, ('limits',)) == ''
    assert path_description(descriptions, ('limits', 'low', 'deep')) == ''


@pytest.mark.parametrize('order', [[('limits', '['), ('limits', 'low')],
                                   [('limits', 'low'), ('limits', '[')]])
def test_specific_wins(order: list[ConfigPath]) -> None:
    """Test the more specific of two selectors describes the member.

    Both insertion orders are tried, because a rule that depended on which
    selector the application happened to write first would be no rule.
    """
    texts: dict[ConfigPath, str] = {('limits', '['): ABOUT_ANY,
                                    ('limits', 'low'): ABOUT_LOW}
    descriptions: Descriptions = {key: texts[key] for key in order}
    assert path_description(descriptions, ('limits', 'low')) == ABOUT_LOW
    assert path_description(descriptions, ('limits', 'high')) == ABOUT_ANY


def test_earlier_step_wins() -> None:
    """Test an earlier named step is more specific than a later one.

    Two selectors can name the same number of steps and still not be equally
    specific. Which of them wins has to be decided rather than left to the
    order the application wrote them in, and the one that agrees with the
    member sooner is the one that is about it more nearly.
    """
    descriptions: Descriptions = {('a', 'b', '['): 'named sooner',
                                  ('a', '[', 'c'): 'named later'}
    assert path_description(descriptions, ('a', 'b', 'c')) == 'named sooner'


def test_whole_docstring() -> None:
    """Test the docstring of a class is read without its indentation."""
    assert class_docstring(DocumentedCfg) == WHOLE


def test_summary_paragraph() -> None:
    """Test the summary is the first paragraph and not the whole docstring."""
    assert class_summary(DocumentedCfg) == SUMMARY


def test_summary_is_one_line() -> None:
    """Test a summary written on two source lines becomes one line.

    Where a docstring is broken is a fact about the width of a source file
    and not about the text, and a label of one row has one line.
    """
    assert class_summary(WrappedDocCfg) == WRAPPED_SUMMARY


def test_summary_only_doc() -> None:
    """Test a docstring that is only a summary is its own summary."""
    assert class_docstring(FlatCfg) == FLAT_SUMMARY
    assert class_summary(FlatCfg) == FLAT_SUMMARY


def test_no_inherited_doc() -> None:
    """Test a class without a docstring is labelled with nothing.

    `inspect.getdoc` would supply the docstring of the base class here, which
    in an editor would label this configuration with a description of
    something else.
    """
    assert class_docstring(NoDocCfg) == ''
    assert class_summary(NoDocCfg) == ''


def _converter(config: SampleCfg, name: str) -> ParseConverter:
    """Return the parse converter of one member of one configuration."""
    return member_converters(config)[name]


def test_enum_names_listed() -> None:
    """Test the names an enum accepts are read from the enum class.

    They are a fact about the type of the member and not a constraint read
    out of a validator, which this library never reads, so the editor can
    say them and an application does not have to write them twice.
    """
    assert enum_text(_converter(EnumCfg(), 'colour')) == \
        f'{COLOUR_SUMMARY}\nOne of: RED, GREEN.'


def test_enum_summary_only() -> None:
    """Test the detail of an enum docstring is left out.

    The rest of an enum docstring is usually notes for whoever writes the
    application, about how the members are numbered or how they reach the
    file, which is not what somebody choosing between them needs.
    """
    text = enum_text(_converter(IntEnumCfg(), 'level'))
    assert text == f'{LEVEL_SUMMARY}\nOne of: LOWEST, LOW, HIGH.'
    assert 'begin with the same' not in text


def test_enum_without_doc() -> None:
    """Test an enum with no docstring of its own still lists its names."""
    assert enum_text(_converter(PlainEnumCfg(), 'level')) == \
        'One of: QUIET, LOUD.'


@pytest.mark.parametrize('config, name',
                         [(FlatCfg(), 'name'), (HexCfg(), 'mask')])
def test_no_enum_text(config: SampleCfg, name: str) -> None:
    """Test a member that holds no enum has nothing said about its type.

    The second of the two has a converter and it is about no enum, which is
    what says that the text comes from the type and not from having one.
    """
    assert enum_text(member_converters(config).get(name)) == ''


def test_description_appended() -> None:
    """Test what the type says is appended to what the application says.

    Appended and not used instead: the names an enum accepts are true
    whatever the application wrote about the member, and an application that
    explains what its members mean should not have to list the names too.
    """
    descriptions: Descriptions = {('colour',): ABOUT_COLOUR}
    converter = _converter(EnumCfg(), 'colour')
    facts = MemberFacts(value='RED', converter=converter)
    assert member_description(descriptions=descriptions, path=('colour',),
                              facts=facts) == \
        f'{ABOUT_COLOUR}\n{COLOUR_SUMMARY}\nOne of: RED, GREEN.'


def test_type_describes_alone() -> None:
    """Test a member the application says nothing about is still explained."""
    converter = _converter(EnumCfg(), 'colour')
    facts = MemberFacts(value='RED', converter=converter)
    assert member_description(descriptions={}, path=('colour',),
                              facts=facts) == \
        f'{COLOUR_SUMMARY}\nOne of: RED, GREEN.'


def test_kind_describes_alone() -> None:
    """Test a member with no enum and no description says what it holds.

    That is the least the editor can say about any member of any
    configuration, and it is what a program that is told a class and no
    description mapping shows.
    """
    assert member_description(descriptions={}, path=('name',),
                              facts=MemberFacts(value='text')) == TEXT_KIND


@pytest.mark.parametrize('value,expected',
                         [('text', TEXT_KIND), (42, WHOLE_NUMBER_KIND),
                          (1.5, NUMBER_KIND), (True, BOOL_KIND),
                          (None, NO_KIND), ([1], ''), ({'a': 1}, '')])
def test_kind_of_value(value: JsonType, expected: str) -> None:
    """Test what each kind of value says about itself.

    `True` is the case the order of the answers exists for, because `bool` is
    a subclass of `int` in Python. A list and a dict say nothing, because a
    member the editor cannot edit yet says which of the two it is where its
    value would be.
    """
    assert kind_text(declared=LeafType(), value=value) == expected


def test_optional_is_said() -> None:
    """Test a member the class may leave out of the file says so.

    `_omit_none_from_json()` is the only thing that answers this, and a member
    holding nothing is not the answer: a member that holds nothing may be one
    that has to hold something.
    """
    said = member_description(descriptions={}, path=('optional',),
                              facts=MemberFacts(value=None, optional=True))
    assert said == f'{NO_KIND} {OPTIONAL_TEXT}'


def test_nothing_is_said() -> None:
    """Test a member declared to allow no value says so under itself.

    It is a different question from the one above: that member is one the
    class leaves out of the file, and this one is written as `null`.
    """
    said = member_description(
        descriptions={}, path=('title',),
        facts=MemberFacts(value=None,
                          declared=LeafType(kind=str, nothing=True)))
    assert said == f'{TEXT_KIND} {NOTHING_TEXT}'


def test_omitted_says_more() -> None:
    """Test a member that is both says only the one that says more.

    A member left out of the file is a member holding nothing, written the
    way that class writes it, so saying both would say the same thing twice.
    """
    said = member_description(
        descriptions={}, path=('title',),
        facts=MemberFacts(value=None, optional=True,
                          declared=LeafType(kind=str, nothing=True)))
    assert said == f'{TEXT_KIND} {OPTIONAL_TEXT}'


def test_optional_asked() -> None:
    """Test the class is what says which of its members are optional."""
    assert optional_members(OmitCfg()) == frozenset({'optional'})
    assert optional_members(FlatCfg()) == frozenset()


def test_optional_by_path() -> None:
    """Test each object of a tree says which of its own members it omits.

    The nested object leaves `note` out of its own JSON and the class holding
    it does not leave out the member of that name, which is what says that
    `_omit_none_from_json()` belongs to the class that owns the subtree.
    """
    assert optional_paths(config_nodes(OwnedOptionCfg())) == \
        frozenset({('inner', 'note')})


def test_nested_says_no_kind() -> None:
    """Test a nested configuration object says no kind of value.

    It holds no value of its own: its class is on its row and its docstring
    is below it, and calling it text or a number would be untrue.
    """
    facts = MemberFacts(value={'width': 4}, nested=True)
    assert member_description(descriptions={}, path=('inner',),
                              facts=facts) == ''
    assert member_description(descriptions={}, path=('inner',),
                              facts=facts._replace(optional=True)) == \
        OPTIONAL_TEXT


def test_nothing_to_describe() -> None:
    """Test a member whose kind is said elsewhere is described by nothing.

    A list and a dict are the two, because the row of such a member says which
    of them it is where its value would be, and saying it twice would be
    worse than saying it once.
    """
    assert member_description(descriptions={}, path=('tags',),
                              facts=MemberFacts(value=['one'])) == ''
