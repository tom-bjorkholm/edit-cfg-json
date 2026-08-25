#! /usr/bin/env python3
"""What this backend calls the actions of the editor, and what it asks.

The names a footer and a command palette give each action, what the palette
says each of them does, and the words of the one question this backend puts in
a field of its own. They are here rather than in the modules that build the
widgets, for the same reason the identifiers and the sizes are in
`textual_look`: they are what one has to read to know what the editor says, and
two of them are read by two modules — the panel binds the keys and names them,
and the screen offers the same names in the palette.

Section 9.6 of `doc/detailed_design.md` is why wording is a backend's own and
not a setting of the core: an application that wants its own words is asking
for translation, which is a larger thing and should be designed as one.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from collections.abc import Callable
from typing import NamedTuple


CLOSE_COMMAND = 'Close'
"""Name of the action that ends the editing session.

It is Close and not Quit because this editor may be one panel of an
application that goes on running, and because closing writes nothing of its
own: it is the "cancel" of the design, exactly as the button of the Tk
backend that carries the same word.
"""

VALIDATE_COMMAND = 'Validate'
"""Name of the command palette entry that validates the buffer."""

SAVE_COMMAND = 'Save'
"""Name of the command palette entry that writes the output file."""

SAVE_AS_COMMAND = 'Save as'
"""Name of the command palette entry that chooses a file and writes it."""

EXPLAIN_COMMAND = 'Explain'
"""What the explain action is called while the explanations are hidden."""

HIDE_COMMAND = 'Hide explanation'
"""What it is called while they are shown.

The name says what the next press does rather than what the action is about,
because "Explain" beside explanations that are already there reads as an offer
to do something that has been done. The Tk backend answers the same question
with a tick-box, which is what a button row can do and a footer cannot.
"""

VALIDATE_HELP = 'Ask the application what it makes of these values'
"""What the command palette says the validate entry does."""

SAVE_HELP = 'Write these values to the output file'
"""What the command palette says the save entry does."""

SAVE_AS_HELP = 'Choose the file to write, and write it'
"""What the command palette says the save as entry does."""

EXPLAIN_HELP = 'Show or hide what the application says about these values'
"""What the command palette says the explain entry does."""

FOLD_COMMAND = 'Fold all'
"""What the fold action is called while at least one container is open."""

OPEN_COMMAND = 'Unfold all'
"""What it is called once every container is folded.

The name says what the next press does, exactly as the explain action above
is named. The Tk backend answers the same question by renaming its button.
"""

FOLD_HELP = 'Fold every list and dict away, or open every one of them'
"""What the command palette says the fold entry does."""

FIND_COMMAND = 'Find'
"""Name of the entry that puts the cursor in the field of the search."""

FIND_NEXT_COMMAND = 'Find next'
"""Name of the entry that goes to the next member the search reaches."""

FIND_HELP = 'Type into the field that looks for a member'
"""What the command palette says the find entry does."""

FIND_NEXT_HELP = 'Go to the next member that the search reaches'
"""What the command palette says the find next entry does."""

SAVE_AS_PROMPT = 'Save as (Enter writes the file):'
"""What the screen that asks for the output file says."""

SAVE_AS_LEAVE = 'Save as (Enter writes the file, {key} leaves it):'
"""What that screen says while there is a key that leaves it.

The key is named from the settings and not written into the sentence,
because an application that took `escape` for itself would otherwise be
telling its users to press a key that does nothing.
"""


class EditorCommand(NamedTuple):
    """One action of the editor, as a command palette offers it."""

    name: str
    """What the palette calls it, which says what the next press will do."""

    help_text: str
    """What the palette says it does."""

    run: Callable[[], None]
    """What choosing it in the palette runs."""
