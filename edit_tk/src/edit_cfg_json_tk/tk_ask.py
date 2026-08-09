#! /usr/bin/env python3
"""The questions this backend asks the user, and the words of each of them.

There are four of them — which file to write, what a new entry of a dict is to
be called, whether an existing file may be overwritten, and whether the changes
that have not been saved may be dropped — and they are here together rather
than in the modules that raise them, for the reason every other split of this
backend was made: one module of a thousand lines is one nobody reads to the
end. Keeping them together is also what makes it plain that this backend asks
the toolkit for all four of its questions, where the Textual one has to build a
screen for them.

Nothing here decides *whether* a question is asked. Which file to write is
asked where the model has no destination, what a new entry is called where
`edit_cfg_json.MemberRow.offer` says a key is needed, whether a file may be
overwritten is `edit_cfg_json.overwrite_question`, and whether there is
anything to lose by closing is `edit_cfg_json.close_question`. All four are
the core's, so that the two backends cannot ask one user something and another
user nothing.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from tkinter import filedialog, messagebox, simpledialog
from typing import Optional
import edit_cfg_json as core

SAVE_AS_TITLE = 'Save the configuration as'
"""Title of the dialog that asks which file to write."""

CONFIG_FILES = 'Configuration files ({extension})'
"""What the dialog calls the files of the extension the application uses."""

ALL_FILES = 'All files'
"""What the dialog calls every other file."""

ADD_KEY_TITLE = 'Add an entry'
"""Title of the dialog that asks what a new entry of a dict is called."""

ADD_KEY_PROMPT = 'Key of the new entry of {name}:'
"""What that dialog asks, naming the member that is about to grow."""

CLOSE_TITLE = 'Close the editor'
"""Title of the dialog that asks whether the changes may be dropped."""

OVERWRITE_TITLE = 'Overwrite the file'
"""Title of the dialog that asks whether an existing file may be written."""


def _file_types(settings: core.Settings) -> list[tuple[str, str]]:
    """Return what the dialog that asks for a file offers to filter by.

    An application that enforces its extension has that one filter and no
    other, because a name with another extension cannot be saved and a
    dialog that offered to look for one would be inviting a refusal. An
    application whose extension is a default offers it first and everything
    else after it, because a name with another extension can be saved. An
    application with no opinion offers nothing, which is what this dialog
    did before there were settings at all.

    Args:
        settings: What the application has decided about file names.

    Returns:
        The file types of the dialog, empty when it has no opinion.
    """
    extension = settings.file_extension
    if extension is None:
        return []
    named = (CONFIG_FILES.format(extension=extension), f'*{extension}')
    if settings.extension_enforced:
        return [named]
    return [named, (ALL_FILES, '*')]


def asked_file(settings: core.Settings) -> str:
    """Ask which file to write, with what the application uses offered first.

    What the dialog offers is what the application decided: the extension it
    uses for its configuration is the one the dialog adds to a name that has
    none, and the one it offers to filter by.

    Args:
        settings: What the application has decided about file names.

    Returns:
        The file that was named, and nothing at all where the question was
        left unanswered.
    """
    return filedialog.asksaveasfilename(
        title=SAVE_AS_TITLE, filetypes=_file_types(settings),
        defaultextension=settings.file_extension or '', confirmoverwrite=False)


def _answered_yes(title: str, question: str) -> bool:
    """Put one question of the editor, and return what was answered.

    The answer that changes nothing is the one the dialog starts on, so that a
    user who answers without reading keeps what they have. The dialog is
    modal, which is what makes a question a question: what is behind it cannot
    be asked a second time while it is up.

    Args:
        title: What the window of the dialog is called.
        question: What the core says is to be asked.

    Returns:
        Whether the user answered yes.
    """
    return messagebox.askyesno(title=title, message=question,
                               default=messagebox.NO)


def may_close(model: core.EditModel) -> bool:
    """Return whether the editor may close, asking where there is a question.

    Closing writes nothing, so a session with something in the buffer that
    has not reached the file loses it. What is asked and whether there is
    anything to ask about are the core's; putting the question is this
    backend's, and the toolkit has a dialog for exactly this.

    Args:
        model: Model that is about to be closed.

    Returns:
        Whether the session may end, which is always so while there is
        nothing that closing would lose.
    """
    question = core.close_question(model)
    return not question or _answered_yes(title=CLOSE_TITLE, question=question)


def may_overwrite(model: core.EditModel) -> bool:
    """Return whether the save may write, asking where there is a question.

    A save writes over whatever the destination holds, and what it holds may
    be a configuration this session never read. Whether that is asked about at
    all is the application's decision and whether there is anything to ask is
    the model's; this puts the question the same way as the one above it.

    The dialog that asks for a file is told not to ask this itself. The
    toolkit offers to, and a question that one backend put and the other did
    not would be exactly what the core owning the question exists to prevent.

    Args:
        model: Model that is about to be saved.

    Returns:
        Whether the file may be written, which is always so where saving
        overwrites nothing that this session did not write itself.
    """
    question = core.overwrite_question(model)
    return not question or _answered_yes(title=OVERWRITE_TITLE,
                                         question=question)


def asked_key(row: core.MemberRow) -> Optional[str]:
    """Ask what a new entry of one dict is to be called.

    A new entry of a dict has to be called something, and nothing but the
    person configuring the application knows what. A key the dict already
    holds is asked about again rather than allowed to take the place of what
    is there: the model refuses such a key, and an editor that let the
    question be answered with one would be offering to lose an entry.

    Args:
        row: Node that is about to be given an entry.

    Returns:
        The key that was named, and None where the question was left
        unanswered or answered with nothing.
    """
    held = row.value if isinstance(row.value, dict) else {}
    while True:
        named = simpledialog.askstring(
            ADD_KEY_TITLE,
            ADD_KEY_PROMPT.format(name=core.path_text(row.path)))
        if not named:
            return None
        if named not in held:
            return named
