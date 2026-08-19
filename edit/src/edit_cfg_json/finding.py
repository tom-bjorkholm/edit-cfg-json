#! /usr/bin/env python3
"""Looking for one node of a configuration that does not fit a window.

A configuration of any interesting size does not fit a window (section 4.6 of
`doc/design.md`), so the node a user wants is often one they cannot see. This
module is the whole of what looking for it means: what is being looked for, how
a piece of text is compared with one node, which nodes that reaches and which
of them the search has got to.

Nothing here opens a folded container, gives a field the focus or scrolls
anything. What is being looked for is state of the model, by the same rule as
the explain toggle of section 4.4, and reaching what was found is the buffer's
and each backend's: this module answers only which nodes the text is about.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from collections.abc import Mapping, Sequence
from typing import NamedTuple, Optional
from config_as_json import ConfigPath
from edit_cfg_json.rows import MemberRow
from edit_cfg_json.tree import path_text


class FindOptions(NamedTuple):
    """How the text being looked for is compared with one node.

    Four independent answers, each of which the user changes with a control of
    its own, and the defaults are what a person looking for a member wants
    without being asked anything: both of the texts a node has, the case
    ignored, and a part of one of them enough.

    They belong to the model rather than to a backend for the same reason the
    fold state does: two user interfaces of one application that looked in
    different places would each be right about a different search.
    """

    in_path: bool = True
    """Whether the path of the node is looked in.

    The whole path and not the name alone, so that `ports.http` finds that one
    value and `ports` finds the member and everything in it. It is also the
    notation the verdict names a refused node in and the one an example
    program's command line writes, so what a user has just read can be typed
    straight in.
    """

    in_value: bool = True
    """Whether the value of the node is looked in.

    It is the text a field shows, which is what the user is looking at, and it
    is only a node that *has* one: a list, a dict and a nested configuration
    object each have their value on the rows below them, so there is nothing
    of their own to look in.
    """

    cased: bool = False
    """Whether the case of the text has to match.

    Ignoring it is the default because a member name is written in one case
    and remembered in another, and it is the comparison `config_as_json` makes
    for the name of an enum member.
    """

    whole: bool = False
    """Whether the text has to be the whole of what it is compared with.

    A part of it is the default, because a user who knows the whole name of
    what they are looking for is the user who least needs a search.
    """


class FindState(NamedTuple):
    """What is being looked for, and which node the search has got to."""

    text: str = ''
    """What is being looked for, empty while nothing is.

    Empty is not a text that matches everything but a search that has not been
    made: nothing is reached and nothing is said about it, which is what a
    cleared field means.
    """

    reached: Optional[ConfigPath] = None
    """Path of the node the search has got to, None when it is at none.

    It is a path and not a place among the matches, because a validation pass
    can leave the model with other rows than it had (section 4.8): a place
    would then be a different node, and a path that is gone is simply gone.
    """

    options: FindOptions = FindOptions()
    """How the text is compared with one node."""


class FindReport(NamedTuple):
    """What the editor says about the search, for a user to read."""

    text: str
    """What is being looked for, empty while nothing is."""

    options: FindOptions
    """How the text is being compared, which is what the controls show."""

    total: int
    """How many nodes the text reaches.

    It is not called a count, because a `NamedTuple` is a tuple and `count` is
    a method of every one of them.
    """

    place: int
    """Which of them the search has got to, counting from one.

    It is zero where the search is at no node at all, which is a search that
    reaches nothing and a search whose node a validation pass has taken away.
    """


LOOKS_IN_PATH = ('Look in the path of the member, so that ports.http finds '
                 'that one value and ports finds the member and everything '
                 'in it.')
"""What looking in the path of a node means, for a user to read."""

LOOKS_IN_VALUE = ('Look in the value of the member, which is the text that '
                  'its field shows.')
"""What looking in the value of a node means."""

MATCHES_CASE = 'Match the case of the text instead of ignoring it.'
"""What matching the case means."""

MATCHES_WHOLE = ('Match the whole path or the whole value instead of any part '
                 'of it.')
"""What matching the whole of one of them means."""

FIND_OPTION_HELP = (LOOKS_IN_PATH, LOOKS_IN_VALUE, MATCHES_CASE,
                    MATCHES_WHOLE)
"""What each answer of `FindOptions` means, in the order of its members.

It is here rather than in each backend for the reason the type of a member is:
what a piece of the model *means* is the model's to say, and two backends
explaining one control two ways would be explaining two different controls.
What each backend owns is the label on it — one or two characters, since the
width of that row belongs to the field — and where the explanation is put,
which is a tooltip in both toolkits and the only place a label that short has
to say what it is.
"""


def _texts_of(row: MemberRow, options: FindOptions) -> list[str]:
    """Return the texts of one node that a search is compared with.

    Args:
        row: Node to look at.
        options: Which of its texts are being looked in.

    Returns:
        The texts to compare with, empty for a node that has none of them.
    """
    texts = [path_text(row.path)] if options.in_path else []
    if options.in_value and row.editable:
        texts.append(row.value_text)
    return texts


def _reaches(row: MemberRow, text: str, options: FindOptions) -> bool:
    """Return whether one text is about one node.

    Args:
        row: Node to compare with.
        text: What is being looked for.
        options: How the comparison is made.

    Returns:
        Whether the text is about that node.
    """
    wanted = text if options.cased else text.casefold()
    for held in _texts_of(row=row, options=options):
        candidate = held if options.cased else held.casefold()
        if candidate == wanted if options.whole else wanted in candidate:
            return True
    return False


def looks_nowhere(options: FindOptions) -> bool:
    """Return whether these options leave nothing at all to look in.

    A user who unticks both of the places a search looks has asked for
    something that can never reach a node, and telling them that no member
    matches would be untrue: nothing was compared with anything.

    Args:
        options: How the comparison would be made.

    Returns:
        Whether neither the path nor the value is being looked in.
    """
    return not (options.in_path or options.in_value)


def matched(rows: Mapping[ConfigPath, MemberRow],
            state: FindState) -> tuple[ConfigPath, ...]:
    """Return the path of every node that the search is about, in row order.

    Args:
        rows: The rows of the configuration, by path.
        state: What is being looked for and how.

    Returns:
        The nodes the text reaches, in the order they are shown, and none at
        all for a search that has not been made or has nowhere to look.
    """
    if not state.text or looks_nowhere(state.options):
        return ()
    return tuple(path for path, row in rows.items()
                 if _reaches(row=row, text=state.text, options=state.options))


def next_match(matches: Sequence[ConfigPath],
               reached: Optional[ConfigPath]) -> Optional[ConfigPath]:
    """Return the match after one node, wrapping round to the first.

    A search that is at no node at all, and one whose node is not a match any
    more, both go to the first: that is a search starting from the top, which
    is what a new text and a changed option ask for and what is left of a
    search whose node a validation pass took away.

    Args:
        matches: The nodes the text reaches, in the order they are shown.
        reached: Node the search has got to, or None when it is at none.

    Returns:
        The node to go to, and None when the text reaches none.
    """
    if not matches:
        return None
    if reached is None or reached not in matches:
        return matches[0]
    return matches[(matches.index(reached) + 1) % len(matches)]


def find_report(state: FindState, matches: Sequence[ConfigPath]) -> FindReport:
    """Return what the editor says about one search.

    Args:
        state: What is being looked for and where the search has got to.
        matches: The nodes that text reaches, in the order they are shown.

    Returns:
        What is being looked for, how, how many nodes it reaches and which of
        them the search is at.
    """
    place = matches.index(state.reached) + 1 \
        if state.reached in matches else 0
    return FindReport(text=state.text, options=state.options,
                      total=len(matches), place=place)
