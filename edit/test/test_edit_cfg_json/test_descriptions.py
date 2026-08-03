#! /usr/bin/env python3
"""Tests for the explanatory text about a configuration and its members.

The two sources are tested separately here, because they are independent: a
class has a docstring or has not, and an application describes a member or
does not, and neither of those says anything about the other.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from config_as_json import ConfigPath
import pytest
from edit_cfg_json import Descriptions
from edit_cfg_json.descriptions import class_docstring, class_summary, \
    path_description
from .sample_cfg import DocumentedCfg, FlatCfg, NoDocCfg, WrappedDocCfg

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
