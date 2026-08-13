#! /usr/bin/env python3
"""The part of a window that the keys and the wheel of one editor reach.

An editor that owns its window may take the keys of the whole window. An
editor mounted in a window that an application owns may not: the application
has widgets of its own in that window and keys of its own on them. Both are
the same rule once it is said about a *part* of a window — the keys of the
editor and its mouse wheel reach the widget the editor was given and
everything the editor built inside it, and nothing else. A backend that owns
its window is then given the window, and one that is mounted is given the
frame it was mounted in, and neither of them needs a rule of its own.

Tk has one mechanism for exactly that, and it is the bind tag. Every widget
carries a list of them, an event walks that list in order, and a handler that
answers `break` stops the walk. So a tag of this editor's own, put on the
widgets of this editor and on no others, is the part of the window the
paragraph above describes; and where in each list it is put decides whether
the editor or the field that has the focus is offered a key first, which is
what `edit_cfg_json.Settings.priority_keys` says.

Nothing here knows what an edit model is. This is what Tk needs in order to
have a scoped binding at all, in the same way as the scrolling beside it.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from collections.abc import Callable
from itertools import count
import tkinter
from edit_cfg_json_tk.key_names import tk_sequence

TAG_PREFIX = 'edit_cfg_json_keys_'
"""Beginning of the name of the bind tag of one editor.

A bind tag is a name in the Tcl interpreter and not an object, so two editors
in one process would share every binding of a tag they shared. The number
after this prefix is what keeps them apart.
"""

_scope_numbers = count()
"""What makes the name of each tag different from every other one."""


def _key_handler(command: Callable[[], None]) -> Callable[..., str]:
    """Return the callback that runs one command for one key event.

    Args:
        command: What that key does.

    Returns:
        A callback that Tk can bind, which stops the event from being
        handled a second time by whatever else the widget is bound to.
    """
    def run_command(*event: object) -> str:
        """Run the command, and keep the event from being handled again."""
        _ = event
        command()
        return 'break'
    return run_command


class KeyScope:
    """The keys and the mouse wheel of one editor, and where they reach.

    The bindings are made on a bind tag of this scope's own, and the tag is
    put on every widget of the editor by `reach`. A widget the editor did not
    build never gets the tag, which is what keeps an embedded editor from
    claiming keys that belong to the application around it.
    """

    def __init__(self, parent: tkinter.Misc, priority: bool = True) -> None:
        """Make a scope that has nothing bound and reaches nothing yet.

        Args:
            parent: Widget the editor is built below. It is used to reach the
                Tcl interpreter that the bind tag lives in, and is given the
                tag itself by `reach` like every widget inside it.
            priority: Whether the editor is offered a key before the widget
                that has the focus. That is what an editor which owns its
                window wants, and an application that has taken one of these
                combinations for a widget of its own says otherwise.
        """
        self._parent = parent
        self._priority = priority
        self._tag = f'{TAG_PREFIX}{next(_scope_numbers)}'
        self._sequences: list[str] = []

    @property
    def tag(self) -> str:
        """Return the bind tag that the widgets of this editor carry."""
        return self._tag

    def bind_key(self, key: str, command: Callable[[], None]) -> None:
        """Bind one key combination of one action, if Tk can bind it.

        A combination that the translation does not know, or that Tk refuses,
        leaves that action without that key rather than without an editor:
        every action of this backend has a button as well.

        Args:
            key: One key combination, as `ActionSettings` writes them.
            command: What that key does.
        """
        sequence = tk_sequence(key)
        if sequence is not None:
            self.bind_event(sequence, _key_handler(command))

    def bind_event(self, sequence: str, callback: Callable[..., str]) -> None:
        """Bind one event sequence everywhere this scope reaches.

        Args:
            sequence: Event sequence in the notation Tk binds by.
            callback: What that event does, which answers `break` so that the
                event is not handled a second time.
        """
        try:
            self._parent.bind_class(self._tag, sequence, callback)
        except tkinter.TclError:
            # Tk refuses a sequence it cannot parse, and a key the
            # application named is not worth an editor that does not open.
            return
        self._sequences.append(sequence)

    def reach(self) -> None:
        """Make this scope reach the widget it was made for, and its inside.

        It is called again whenever the editor builds its rows again, because
        a widget that was created afterwards carries the tags it was born
        with. A widget that already has the tag is left alone, so calling it
        again costs a walk and changes nothing.
        """
        self._reach(self._parent)

    def _reach(self, widget: tkinter.Misc) -> None:
        """Put the tag of this scope on one widget and everything inside it.

        Args:
            widget: Widget to reach, together with its descendants.
        """
        tags = widget.bindtags()
        if self._tag not in tags:
            widget.bindtags((self._tag, *tags) if self._priority
                            else (*tags, self._tag))
        for child in widget.winfo_children():
            self._reach(child)

    def release(self) -> None:
        """Take every binding of this scope out of the interpreter.

        A bind tag is a name in the interpreter and outlives the widgets that
        carried it, so an editor that was closed would otherwise leave its
        callbacks — and the model they hold — behind for as long as the
        application runs.
        """
        for sequence in self._sequences:
            try:
                self._parent.unbind_class(self._tag, sequence)
            except tkinter.TclError:
                # The window is already gone, which takes the bindings of
                # its interpreter with it and is not a failure to report.
                pass
        self._sequences = []
