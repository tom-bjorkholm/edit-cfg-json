#! /usr/bin/env python3
"""The editor in a window, or in an area, of an application that runs Tk.

An application with no Tk of its own calls `edit_cfg_json_tk.edit`, which
owns a `tkinter.Tk` and runs until the user is done. An application that
already runs Tk cannot use that: a second `tkinter.Tk` is a second Tcl
interpreter, and no widget, variable, font or image crosses between two of
them. It uses `TkEditorPanel` instead, which builds the editor where it is
told and returns at once.

Everything this backend takes from the core is reached through `core`, which
is `edit_cfg_json` itself, in the same way as the rest of this package.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from collections.abc import Callable
from typing import Optional, TextIO
import sys
import tkinter
from config_as_json import Config, PathOrStr
import edit_cfg_json as core
from edit_cfg_json_tk.tk_editor import EditorWidgets


class TkEditorPanel:
    """One editor of a configuration, in a window or in an area of one.

    Give it `parent` and it builds a window of its own over that widget;
    give it `area` and it fills that widget instead. It never blocks: the
    application's own `mainloop` is already running, `on_close` says that the
    session has ended, and `saved_config` says what came of it.

    Only what the editor created is destroyed when it closes, so the window
    or the area the application named is left as it was.
    """

    # Every keyword after the first says one independent thing about the
    # session, exactly as `edit_cfg_json.edit` takes them.
    # pylint: disable-next=too-many-arguments
    def __init__(self, config: Config, *,
                 parent: Optional[tkinter.Misc] = None,
                 area: Optional[tkinter.Misc] = None, modal: bool = True,
                 on_close: Optional[Callable[[], None]] = None,
                 descriptions: Optional[core.Descriptions] = None,
                 in_file: Optional[PathOrStr] = None,
                 loader: Optional[core.ConfigLoader] = None,
                 out_file: Optional[PathOrStr] = None,
                 policy: core.LoadPolicy = core.DEFAULT_POLICY,
                 settings: core.SettingsSource = core.Settings(),
                 stderr_file: TextIO = sys.stderr) -> None:
        """Read the configuration and build the editor where it was told.

        Args:
            config: Configuration object to edit. It is never modified.
            parent: The widget the editor's own new window is shown over.
                Exactly one of parent and area is given; an application with
                no Tk of its own has neither and uses `edit_cfg_json_tk.edit`.
            area: The existing container the editor fills instead of a window
                of its own. It cannot be given together with parent.
            modal: Whether the editor grabs its window, or the area, for the
                session, so that nothing else of the application answers until
                it closes. Tk refuses a grab for a window that is not on the
                screen yet, and the editor then opens without one rather than
                not opening.
            on_close: What the application does once the session has ended,
                or None for one that reads `saved_config` some other way.
            descriptions: What the application says about the members it
                declares, or None when it says nothing.
            in_file: File to read, or None to start from the declared
                defaults.
            loader: How this application constructs its configuration, or
                None for a class the editor can construct on its own.
            out_file: File to write, or None to write the input file.
            policy: What to do about declared keys the input file does not
                hold.
            settings: What this application has already decided about key
                combinations and file names, or a callable answering with it.
            stderr_file: Stream used for user-facing diagnostics.

        Raises:
            ValueError: Both parent and area were given, or neither was.
            ConfigLoadError: The input file cannot be opened for editing.
        """
        self._model = core.editor_model(config, descriptions=descriptions,
                                        in_file=in_file, loader=loader,
                                        out_file=out_file, policy=policy,
                                        settings=settings,
                                        stderr_file=stderr_file)
        self._on_close = on_close
        self._ended = False
        self._built = _built_widget(parent=parent, area=area,
                                    closer=self.close,
                                    title=self._model.config_type_name)
        self._modal = modal and _grabbed(self._built)
        self._widgets = EditorWidgets(parent=self._built, model=self._model,
                                      on_close=self._end_session)

    @property
    def model(self) -> core.EditModel:
        """Return the model of this session, which the editor built."""
        return self._model

    @property
    def saved_config(self) -> Optional[Config]:
        """Return the configuration this session wrote, None until it does."""
        return self._model.saved_config

    def close(self, ask_about_unsaved: bool = True) -> None:
        """End the session and take the editor off the window.

        Whether the user is asked about what has not been saved is the
        application's to decide: a menu entry that closes the editor should
        ask, and an application that is putting a question of its own already
        has one question too many. The editor's own Close button, its quit
        key and the close button of a window it made are this call with the
        default. Calling it again once the session has ended does nothing.

        Args:
            ask_about_unsaved: Whether the user is asked before a buffer that
                holds something unsaved is dropped.
        """
        if ask_about_unsaved and not self._ended:
            self._widgets.close_editor()
            return
        self._end_session()

    def _end_session(self) -> None:
        """Destroy what the editor built, and say that it has gone."""
        if self._ended:
            return
        self._ended = True
        self._widgets.release_keys()
        if self._modal:
            self._built.grab_release()
        self._built.destroy()
        if self._on_close is not None:
            self._on_close()


def _built_widget(parent: Optional[tkinter.Misc], area: Optional[tkinter.Misc],
                  closer: Callable[[], None], title: str) -> tkinter.Misc:
    """Return the widget the editor builds in, which is its own to destroy.

    Args:
        parent: Widget a new window is shown over, or None.
        area: Widget the editor fills, or None.
        closer: What the close button of such a window does.
        title: Name of the configuration class, for a window of its own.

    Returns:
        The window or the frame that the editor created.

    Raises:
        ValueError: Both parent and area were given, or neither was.
    """
    if (parent is None) == (area is None):
        raise ValueError('Give the editor either a parent or an area.')
    if area is not None:
        frame = tkinter.Frame(area)
        frame.pack(fill='both', expand=True)
        frame.bind('<Button-1>', _focus_taker(frame))
        return frame
    assert parent is not None
    window = tkinter.Toplevel(parent)
    window.title(title)
    window.transient(parent.winfo_toplevel())
    window.protocol('WM_DELETE_WINDOW', closer)
    return window


def _focus_taker(frame: tkinter.Misc) -> Callable[..., None]:
    """Return what a click on the editor's own frame does.

    The keys of the editor reach the part of the window it built and nothing
    else, so a user who has not been in the editor yet would otherwise press
    one of them and see nothing happen. A field and a button take the focus of
    their own accord, and this is what a click on anything else does.

    Args:
        frame: Frame the editor was built in.

    Returns:
        A callback that gives that frame the keyboard focus.
    """
    def take_focus(*event: object) -> None:
        """Give the editor the focus when it is clicked on."""
        _ = event
        frame.focus_set()
    return take_focus


def _grabbed(widget: tkinter.Misc) -> bool:
    """Take the events of the application for one widget, if Tk allows it.

    Args:
        widget: Widget the editor was built in.

    Returns:
        Whether the grab was made, which is what has to be released again. Tk
        refuses to grab for a window that is not on the screen, and an editor
        that opened without a grab is worth more than one that did not open.
    """
    try:
        widget.grab_set()
    except tkinter.TclError:
        return False
    return True
