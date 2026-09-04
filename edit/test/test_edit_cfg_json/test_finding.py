#! /usr/bin/env python3
"""Tests for looking for one node of a configuration.

What is being looked for is state of the model, so it is tested through the
model: the four answers about where a search looks, what each of them reaches,
which node the search has got to, and what has to happen for that node to be
reachable at all.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from typing import Optional
import pytest
from config_as_json import ConfigPath
from edit_cfg_json import EditModel, Emphasis, FindOptions, find_emphasis, \
    find_text
from .container_cfg import BigListCfg, MANY_LABELS, NormalizeCfg, TreeCfg
from .model_helpers import row_at, shown_paths
from .sample_cfg import FlatCfg

PATH_ONLY = FindOptions(in_value=False)
"""Looking in the path of a node and not in its value."""

VALUE_ONLY = FindOptions(in_path=False)
"""Looking in the value of a node and not in its path."""

NOWHERE = FindOptions(in_path=False, in_value=False)
"""The one answer that can never reach a node at all."""


def _found(model: EditModel) -> Optional[ConfigPath]:
    """Return the path of the node the search has got to, or None."""
    reached = [row.path for row in model.rows if row.found]
    assert len(reached) <= 1
    return reached[0] if reached else None


def _matches(model: EditModel, text: str,
             options: FindOptions = FindOptions()) -> list[ConfigPath]:
    """Return every node one text reaches, by looking for it and walking on.

    Args:
        model: Model to look in.
        text: What to look for.
        options: How the text is compared with one node.

    Returns:
        The path of every node the text reaches, in the order the search goes
        to them, which is the order the rows are shown in.
    """
    model.set_find_options(options)
    model.find(text)
    if model.search.total == 0:
        return []
    walked = [_found(model)]
    for _ in range(model.search.total - 1):
        model.find_next()
        walked.append(_found(model))
    return [path for path in walked if path is not None]


def test_nothing_looked_for() -> None:
    """Test a model nobody has searched in says nothing about a search."""
    model = EditModel(FlatCfg())
    assert model.search.text == ''
    assert model.search.total == 0
    assert model.search.place == 0
    assert find_text(model) == ''
    assert find_emphasis(model) is Emphasis.MUTED
    assert _found(model) is None


def test_default_options() -> None:
    """Test the search opens looking in both places, in either case, in part.

    They are the defaults a person looking for a member wants without being
    asked anything, and a user who knows the whole name of what they want is
    the user who least needs a search.
    """
    options = EditModel(FlatCfg()).search.options
    assert options == FindOptions(in_path=True, in_value=True, cased=False,
                                  whole=False)


def test_found_in_path() -> None:
    """Test the path of a node is looked in, whatever its case."""
    model = EditModel(FlatCfg())
    assert model.find('ANSW') is False
    assert _found(model) == ('answer',)
    assert model.search.place == 1
    assert model.search.total == 1
    assert find_text(model) == 'find ANSW: 1 of 1'
    assert find_emphasis(model) is Emphasis.ATTENTION


def test_whole_path_looked_in() -> None:
    """Test the whole path is looked in and not the name of the node alone.

    It is the notation the verdict names a refused node in, so what a user has
    just read is what they can type. A path that is the beginning of another
    reaches both, because a part of a path is enough: naming the dict entry
    reaches the entry and the two values inside it.
    """
    model = EditModel(TreeCfg())
    assert _matches(model, 'groups[red]') == [('groups', 'red'),
                                              ('groups', 'red', '0'),
                                              ('groups', 'red', '1')]
    assert _matches(model, 'red][') == [('groups', 'red', '0'),
                                        ('groups', 'red', '1')]


def test_found_in_value() -> None:
    """Test the value of a node is looked in, as its field shows it."""
    model = EditModel(FlatCfg())
    assert _matches(model, 'flat text', VALUE_ONLY) == [('name',)]
    assert _matches(model, '42', VALUE_ONLY) == [('answer',)]


def test_container_no_value() -> None:
    """Test only a node with a value of its own is looked in for one.

    A list, a dict and a nested configuration object each have their value on
    the rows below them, so there is nothing of their own to look in. What such
    a row shows in the place of a value — how much it holds — is therefore not
    something a search reaches.
    """
    model = EditModel(TreeCfg())
    assert _matches(model, 'elements', VALUE_ONLY) == []
    assert row_at(model, ('rules',)).value_text == '2 elements'


def test_case_matched() -> None:
    """Test the case has to match once that has been asked for."""
    model = EditModel(FlatCfg())
    assert _matches(model, 'FLAT', VALUE_ONLY) == [('name',)]
    assert _matches(model, 'FLAT', VALUE_ONLY._replace(cased=True)) == []
    assert _matches(model, 'flat', VALUE_ONLY._replace(cased=True)) == \
        [('name',)]


def test_whole_matched() -> None:
    """Test the whole of a path or a value has to match once asked for."""
    model = EditModel(TreeCfg())
    whole = FindOptions(whole=True)
    assert _matches(model, 'groups[red]', whole) == [('groups', 'red')]
    assert _matches(model, 'red', whole) == []
    assert _matches(model, 'groups', whole) == [('groups',)]


def test_looks_nowhere() -> None:
    """Test a search with nowhere to look says so rather than finding nothing.

    Nothing was compared with anything, so saying that no member matches would
    be untrue.
    """
    model = EditModel(FlatCfg())
    model.set_find_options(NOWHERE)
    model.find('answer')
    assert model.search.total == 0
    assert _found(model) is None
    assert find_text(model) == \
        'find answer: looking in neither the path nor the value'
    assert find_emphasis(model) is Emphasis.BAD


def test_nothing_matches() -> None:
    """Test a text that reaches no node at all says so."""
    model = EditModel(FlatCfg())
    model.find('nowhere')
    assert model.search.total == 0
    assert _found(model) is None
    assert find_text(model) == 'find nowhere: no member matches'
    assert find_emphasis(model) is Emphasis.BAD


def test_empty_text_clears() -> None:
    """Test clearing the field is a search that has not been made.

    Empty is not a text that matches everything: nothing is being looked for,
    nothing is reached and nothing is said about it.
    """
    model = EditModel(FlatCfg())
    model.find('answer')
    model.find('')
    assert _found(model) is None
    assert find_text(model) == ''
    assert find_emphasis(model) is Emphasis.MUTED


def test_next_wraps_round() -> None:
    """Test the next match after the last one is the first one again."""
    model = EditModel(TreeCfg())
    model.find('rules')
    reached = [_found(model)]
    for _ in range(model.search.total):
        model.find_next()
        reached.append(_found(model))
    assert reached[0] == reached[-1]
    assert model.search.place == 1


def test_place_of_several() -> None:
    """Test the line says which of the matches the search has got to."""
    model = EditModel(TreeCfg())
    model.find('rules')
    assert find_text(model) == f'find rules: 1 of {model.search.total}'
    model.find_next()
    assert find_text(model) == f'find rules: 2 of {model.search.total}'


def test_option_starts_again() -> None:
    """Test changing where the search looks starts it from the top.

    What the earlier search reached was reached by asking a different
    question, so going on from it would be going on from an answer to
    something else.
    """
    model = EditModel(TreeCfg())
    model.find('rules')
    model.find_next()
    assert model.search.place == 2
    model.set_find_options(PATH_ONLY)
    assert model.search.place == 1


def test_folded_opens() -> None:
    """Test a match inside a folded container makes that container open.

    What is found has to be reachable, and the long list of this class opens
    folded, so a search that left it folded would have found something the
    user cannot see.
    """
    model = EditModel(BigListCfg())
    assert ('many', '7') not in shown_paths(model)
    assert model.find('label-7') is True
    assert ('many', '7') in shown_paths(model)
    assert _found(model) == ('many', '7')
    assert not row_at(model, ('many',)).folded


def test_open_only_what_hides() -> None:
    """Test a search that hides nothing opens nothing, and says so.

    The answer is what a backend lays its rows out again for, so a search that
    changed nothing about what is shown has to say that it changed nothing.
    """
    model = EditModel(BigListCfg())
    assert model.find('few') is False
    assert model.find('label-3') is True
    assert model.find('label-4') is False


def test_found_fold_stays() -> None:
    """Test a folded container that is itself found is left folded.

    Only what hides the node is opened. A folded container is a row of its
    own, and it is the row the user presses to open it.
    """
    model = EditModel(BigListCfg())
    assert model.find('many') is False
    assert _found(model) == ('many',)
    assert row_at(model, ('many',)).folded


def test_survives_a_pass() -> None:
    """Test a validation pass that keeps the node keeps the search at it."""
    model = EditModel(BigListCfg())
    model.find('label-7')
    model.validate()
    assert _found(model) == ('many', '7')
    assert find_text(model) == 'find label-7: 1 of 1'


def test_pass_takes_the_node() -> None:
    """Test a pass that leaves no node for the search says what is left.

    The validator of this class sorts the list and throws its duplicates away,
    so the second of the two values that were found is gone. What the text
    still reaches is said as what it is, and the next press starts again from
    the top rather than saying nothing at all.
    """
    model = EditModel(NormalizeCfg())
    model.set_text(path=('words', '0'), text='beta')
    model.set_find_options(VALUE_ONLY)
    model.find('beta')
    model.find_next()
    assert _found(model) == ('words', '1')
    model.validate()
    assert _found(model) is None
    assert find_text(model) == 'find beta: 1 matches'
    assert find_emphasis(model) is Emphasis.ATTENTION
    model.find_next()
    assert _found(model) == ('words', '0')


def test_moved_taken_along() -> None:
    """Test the search follows an element that changed places.

    An element of a list is addressed by where it is, so an element that moved
    is the same node under another path, exactly as its fold state is.
    """
    model = EditModel(BigListCfg())
    model.find('one')
    assert _found(model) == ('few', '0')
    model.move_element(path=('few', '0'), later=True)
    assert _found(model) == ('few', '1')
    assert row_at(model, ('few', '1')).value == 'one'


def test_removed_dropped() -> None:
    """Test the search is at no node once the one it reached is gone."""
    model = EditModel(BigListCfg())
    model.find('two')
    assert _found(model) == ('few', '1')
    model.remove_element(('few', '1'))
    assert _found(model) is None
    assert find_text(model) == 'find two: no member matches'


def test_keeps_the_verdict() -> None:
    """Test looking for something is not a change of the buffer.

    A search changes no value, so what the application made of these values is
    as true as it was and the editor goes on saying it.
    """
    model = EditModel(FlatCfg())
    verdict = model.validate()
    assert verdict.valid
    model.find('answer')
    model.find_next()
    assert model.verdict is verdict
    assert not model.dirty


@pytest.mark.parametrize('text, total', [('label', MANY_LABELS),
                                         ('label-1', 3),
                                         ('many', MANY_LABELS + 1),
                                         ('few', 3)])
def test_how_many_matched(text: str, total: int) -> None:
    """Test how many nodes each text of the long list example reaches.

    `label-1` reaches three of them, because a part of the text is enough:
    `label-1`, `label-10` and `label-11` all begin with it. The name of a
    member reaches the member and every value inside it, for the same reason:
    the path of each of those begins with the name.
    """
    model = EditModel(BigListCfg())
    model.find(text)
    assert model.search.total == total
