#! /usr/bin/env python3
"""One editor mounted in a window that an application already owns.

`TkEditor` runs an editor that owns a window and a Tk of its own, and it
cannot be what an application which already runs Tk uses: a second
`tkinter.Tk` is a second Tcl interpreter, and no widget, variable, font or
image crosses between two of them. `EditorBackend.run_editor` could not serve
such an application either, whatever it created, because that method promises
to run until the user is done and an editor in a panel of somebody else's
window has no such moment.

So this is the other entry point, and it is non-blocking: the application
builds the model, mounts this in a widget of its own, and goes on running its
own event loop. What it gets back is `on_close`, which says the session
ended, and `edit_cfg_json.EditModel.saved_config`, which says what came of it.

Everything this backend takes from the core is reached through `core`, which
is `edit_cfg_json` itself, in the same way as the rest of this package.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from collections.abc import Callable
from typing import Optional
import tkinter
import edit_cfg_json as core
from edit_cfg_json_tk.tk_editor import EditorWidgets


class TkEditorPanel:  # pylint: disable=too-few-public-methods
    """The editor of this package, inside a widget an application owns.

    It creates one frame inside the widget it is given and builds the editor
    in that frame, which is what makes the two rules of this entry point
    true: the editor destroys only what it created, and its keys and its
    mouse wheel reach only the part of the window it built.

    Where that frame goes is the application's decision and is made by
    handing over the widget it belongs in. An application that wants the
    editor in a window of its own creates that window — `tkinter.Toplevel` —
    and passes it, which keeps the title, the geometry, the close protocol
    and the grab where they belong.
    """

    def __init__(self, parent: tkinter.Misc, model: core.EditModel, *,
                 on_close: Optional[Callable[[], None]] = None) -> None:
        """Mount one editor in the widget the application named.

        Args:
            parent: Widget the editor is mounted in. The editor fills it and
                never touches it otherwise: the frame it builds in is its
                own, and closing destroys that frame and not this widget.
            model: Model to show and to edit. The application builds it
                itself, with `edit_cfg_json.load_config` and
                `edit_cfg_json.EditModel`, because reading a file is what an
                application does before it shows an editor at all.
            on_close: What the application does when the session has ended,
                or None for an application that reads the outcome some other
                way. It is called after the editor has taken itself off the
                window, so that `edit_cfg_json.EditModel.saved_config` can be
                read from it.
        """
        self._on_close = on_close
        self._ended = False
        self._frame = tkinter.Frame(parent)
        self._frame.pack(fill='both', expand=True)
        self._frame.bind('<Button-1>', self._take_focus)
        self._widgets = EditorWidgets(parent=self._frame, model=model,
                                      on_close=self._end_session)

    def _take_focus(self, *event: 'tkinter.Event[tkinter.Misc]') -> None:
        """Give the editor the focus when it is clicked on.

        The keys of the editor reach the part of the window it built and
        nothing else, so a user who has not been in the editor yet would
        otherwise press one of them and see nothing happen. A field and a
        button take the focus of their own accord when they are clicked, and
        this is what a click on anything else does.
        """
        _ = event
        self._frame.focus_set()

    def close(self, ask_about_unsaved: bool = True) -> None:
        """End the session and take the editor off the window.

        Whether the user is asked about what has not been saved is the
        application's to decide, because only the application knows what it
        is closing the editor for: a menu entry that closes the editor should
        ask, and an application that is putting a question of its own to the
        user already has one question too many.

        The editor's own Close button and its quit key are this method with
        the default, so the question is put in the same words and answered in
        the same dialog whichever of the three ended the session.

        Calling this again once the session has ended does nothing, so an
        application need not keep track of whether the user has closed the
        editor already.

        Args:
            ask_about_unsaved: Whether the user is asked before a buffer that
                holds something unsaved is dropped. The default asks, which
                is the way a default about something that cannot be undone
                should lean.
        """
        if ask_about_unsaved:
            self._widgets.close_editor()
            return
        self._end_session()

    def _end_session(self) -> None:
        """Take the editor off the window, and say that it has gone.

        Only what the editor created is destroyed, which is the frame it
        built in. The widget the application named is left exactly as it was,
        because an editor that destroyed a window it did not create would be
        deciding something that is not its to decide.
        """
        if self._ended:
            return
        self._ended = True
        self._widgets.release_keys()
        self._frame.destroy()
        if self._on_close is not None:
            self._on_close()
