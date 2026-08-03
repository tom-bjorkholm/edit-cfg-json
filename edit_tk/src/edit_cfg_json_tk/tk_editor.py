#! /usr/bin/env python3
"""Tkinter view of an edit model, with one editable field per member.

Everything this backend takes from the core is reached through `core`, which is
`edit_cfg_json` itself. A backend may use the public API of the core and
nothing else, and naming it at every call site is what makes that visible; it
also keeps the two backends from each holding the same block of twenty
imported names, which is a duplication with nothing to factor out, since
neither backend may import the other.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from collections.abc import Callable
from typing import NamedTuple, Optional, TextIO
import sys
import tkinter
from tkinter import filedialog
from config_as_json import Config, PathOrStr
import edit_cfg_json as core
from edit_cfg_json_tk.key_names import tk_sequence

NAME_COLUMN_WIDTH = 24
"""Width in characters of the column that holds the member names."""

LEAST_FIELD_WIDTH = 8
"""Width in characters that a field asks for, and can be squeezed to.

A field takes every bit of the width that the name and the marks of its member
leave over, so this is not how wide a field is: it is how far a field gives way
when the window is too narrow for all three. The marks are what a narrow window
would otherwise cut off, and a mark that is there and cannot be read is worse
than a field with fewer characters in view. The Textual backend gives way in
the same direction and for the same reason.
"""

PADDING = 4
"""Padding in pixels around the widgets of the editor."""

DESCRIPTION_INDENT = 24
"""Indentation in pixels of the description of one member.

The indentation is what says that the line belongs to the member above it
rather than being a member of its own.
"""

BODY_HEIGHT = 480
"""Largest height in pixels that the scrolling part of the editor is given.

A configuration of any size therefore opens a window that fits a screen, and
what does not fit is scrolled to rather than lost. A configuration smaller
than this gets a window that is smaller than this, because the height is what
the body asks for up to this limit and not this limit.
"""

LEAST_WRAP_WIDTH = 200
"""Narrowest line in pixels that a paragraph of the editor is wrapped to.

A window can be made narrower than any text is readable in, and wrapping to
what is left of it would leave one word per line. Below this the text is cut
off by the window instead, which is the lesser of the two.
"""

BODY_WIDTH = 720
"""Largest width in pixels that the scrolling part of the editor asks for.

A canvas asks for a width of its own that has nothing to do with what is on
it, so the width the editor opens at has to be said here: what the body asks
for, up to this. Wider than this is left to the user, who can make the window
any size, and every text that is a paragraph wraps to whatever width there is.
"""

EMPHASIS_COLOURS = {core.Emphasis.MUTED: '#4b5563',
                    core.Emphasis.ATTENTION: '#0969da',
                    core.Emphasis.WARNING: '#8a6100',
                    core.Emphasis.GOOD: '#1a7f37',
                    core.Emphasis.BAD: '#cf222e'}
"""The colour of every reason the core has to show something differently.

One colour per member of `edit_cfg_json.Emphasis`, chosen to be read on the
light window that Tk gives this editor: a grey that is dark enough for a
paragraph of explanation to be comfortable rather than faint, and a blue, an
amber, a green and a red that carry on a light background.

Tk has no theme to ask, unlike the Textual backend, which names colours of its
terminal's theme and follows it into a dark mode. A Tk that has been put into
a dark mode by its platform would want other values here, and that belongs
with the rest of what an application decides rather than in the middle of a
backend; see section 9 of `doc/design.md`.
"""

FIELD_BACKGROUND = '#eef1f5'
"""Background of a field the user can edit.

The window is white, so a field that kept the white background of its own
accord could not be told from a label: the values were there to be edited and
nothing said so. The tint plus the border below are what say it.
"""

FIELD_FOREGROUND = '#111827'
"""Colour of the text inside a field.

It is stated rather than inherited, because the background above is stated:
a platform that decided the text of a field should be white would otherwise
put white text on a light field.
"""

FIELD_BORDER = '#9aa5b1'
"""Colour of the line around a field the user can edit."""

VALIDATE_TEXT = 'Validate'
"""Text of the button that runs the validation of the application."""

SAVE_TEXT = 'Save'
"""Text of the button that writes the output file."""

SAVE_AS_TEXT = 'Save as...'
"""Text of the button that chooses an output file and then writes it."""

EXPLAIN_TEXT = 'Explain'
"""Text of the tick-box that shows or hides the explanatory text.

A tick-box and not a button, because the action is a toggle and a button
called Explain that hides the explanations reads as the wrong thing entirely.
The tick says which of the two states the editor is in, so one text is true in
both. The Textual backend has no button row to put one in and renames its own
action instead.
"""

CLOSE_TEXT = 'Close'
"""Text of the button that ends the editor.

Closing writes nothing of its own. It is the "cancel" of the design, and it
is called Close because saving leaves the editor open: a button called Cancel
beside values that have already been written would read as an offer to undo
the writing, which it is not.
"""

SAVE_AS_TITLE = 'Save the configuration as'
"""Title of the dialog that asks which file to write."""

CONFIG_FILES = 'Configuration files ({extension})'
"""What the dialog calls the files of the extension the application uses."""

ALL_FILES = 'All files'
"""What the dialog calls every other file."""


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


def _key_handler(command: Callable[[], None]) -> Callable[..., str]:
    """Return the callback that runs one command for one key event.

    Args:
        command: What that key does.

    Returns:
        A callback that Tk can bind, which stops the event from being
        handled a second time by whatever else the window is bound to.
    """
    def run_command(*event: object) -> str:
        """Run the command, and keep the event from being handled again."""
        _ = event
        command()
        return 'break'
    return run_command


def _bind_key(window: tkinter.Misc, key: str,
              command: Callable[[], None]) -> None:
    """Bind one key combination of one action, if Tk can bind it.

    A combination that the translation does not know, or that Tk refuses,
    leaves that action without that key rather than without an editor: every
    action of this backend has a button as well.

    Args:
        window: Window that the binding is made on.
        key: One key combination, as `ActionSettings` writes them.
        command: What that key does.
    """
    sequence = tk_sequence(key)
    if sequence is None:
        return
    try:
        window.bind(sequence, _key_handler(command))
    except tkinter.TclError:
        # Tk refuses an event sequence it cannot parse, and a key the
        # application named is not worth an editor that does not open.
        pass


def _shown_text(parent: tkinter.Misc, text: str,
                emphasis: Optional[core.Emphasis] = None,
                wrapping: bool = True) -> tkinter.Label:
    """Return a label of the editor, in the colour its kind asks for.

    Args:
        parent: Widget that becomes the parent of the created label.
        text: Text to show, left aligned as every text of the editor is.
        emphasis: Why this text stands out from the values, or None for the
            ordinary text colour of the platform.
        wrapping: Whether the text is a paragraph, which wraps to the width
            of the window. The mark of a member is the one text of the editor
            that is not: it belongs beside its field on one line.

    Returns:
        A label showing that text.
    """
    label = tkinter.Label(parent, text=text, anchor='w', justify='left')
    _show_emphasis(label, emphasis)
    if wrapping:
        _wrap_to_width(label)
    return label


def _told(label: tkinter.Label, text: str, emphasis: core.Emphasis) -> None:
    """Show one text of the editor, in the colour its state asks for.

    Args:
        label: Label that shows it.
        text: Text to show.
        emphasis: Why that text stands out from the values.
    """
    label.config(text=text)
    _show_emphasis(label, emphasis)


def _show_emphasis(label: tkinter.Label,
                   emphasis: Optional[core.Emphasis]) -> None:
    """Colour one label in the way one reason to stand out asks for.

    A label with no emphasis is left in the colour of the platform, which is
    what the values and their names are shown in: they are what the user came
    to change, and they are the most legible thing on the screen because
    nothing has been done to them.

    Args:
        label: Label to colour.
        emphasis: Why the text of that label stands out, or None for the
            ordinary text colour.
    """
    if emphasis is not None:
        label.config(foreground=EMPHASIS_COLOURS[emphasis])


def _scroll_by(canvas: tkinter.Canvas, step: Optional[int]
               ) -> Callable[..., str]:
    """Return the callback that one turn of the mouse wheel runs.

    Args:
        canvas: Canvas that holds the scrolling part of the editor.
        step: How far to scroll, or None to read it from the event. X11
            reports a wheel as two buttons and says nothing about how far,
            while every other platform reports a delta whose sign is the
            direction.

    Returns:
        A callback that Tk can bind, which stops the event from being handled
        a second time by whatever else the window is bound to.
    """
    def scroll(*event: 'tkinter.Event[tkinter.Misc]') -> str:
        """Scroll the body by one line, in the direction of the wheel."""
        moved = step if step is not None else _wheel_step(event[0])
        canvas.yview_scroll(moved, 'units')
        return 'break'
    return scroll


def _wheel_step(event: 'tkinter.Event[tkinter.Misc]') -> int:
    """Return which way one reported turn of the mouse wheel goes.

    The type of the event is written as text here and in the three callbacks
    around it, because `tkinter.Event` is a generic class to a type checker and
    a plain one at runtime: Python 3.12 and 3.13 evaluate an annotation where
    it is written, and subscripting it there is an error.

    Only the sign of the delta is used. Its size means different things on
    different platforms, and one line per turn is a scroll everyone can
    follow.

    Args:
        event: The wheel event that Tk reported.

    Returns:
        How far to scroll the body, in lines.
    """
    return -1 if event.delta > 0 else 1


def _bind_wheel(window: tkinter.Misc, canvas: tkinter.Canvas) -> None:
    """Let the mouse wheel scroll the body, however it is reported.

    The bindings are made on the window rather than on the canvas, because a
    wheel event goes to the widget under the pointer and the pointer is
    usually over a field or a label inside the body. That is the same window
    the keys are bound on, and it is the same open question for the same
    reason: an editor mounted in a window it shares would be claiming the
    wheel of a whole application. See section 8.2.7 of `doc/design.md`.

    Args:
        window: Window that the bindings are made on.
        canvas: Canvas that holds the scrolling part of the editor.
    """
    for sequence, step in (('<MouseWheel>', None), ('<Button-4>', -1),
                           ('<Button-5>', 1)):
        try:
            window.bind(sequence, _scroll_by(canvas=canvas, step=step))
        except tkinter.TclError:
            # A platform whose Tk does not know one of these sequences leaves
            # the wheel out and keeps the scrollbar, which is not worth an
            # editor that does not open.
            pass


def _fit_body(canvas: tkinter.Canvas,
              body: tkinter.Frame) -> Callable[..., None]:
    """Return the callback that follows the height of the body.

    It is what makes the canvas scroll: a canvas shows the part of its
    contents that its scroll region says is there, and the contents of this
    one grow and shrink as the explanations are shown and hidden.

    Args:
        canvas: Canvas that holds the body.
        body: Frame that holds everything that scrolls.

    Returns:
        A callback for the event that says the body has been laid out.
    """
    def fitted(*event: 'tkinter.Event[tkinter.Misc]') -> None:
        """Follow the size of the body, up to the size of a window."""
        _ = event
        canvas.configure(scrollregion=canvas.bbox('all'),
                         width=min(body.winfo_reqwidth(), BODY_WIDTH),
                         height=min(body.winfo_reqheight(), BODY_HEIGHT))
    return fitted


def _fit_width(canvas: tkinter.Canvas, item: int) -> Callable[..., None]:
    """Return the callback that gives the body the width of the canvas.

    An item on a canvas is as wide as it asks to be, so without this the
    fields would keep the width they wanted rather than the width there is.

    Args:
        canvas: Canvas that holds the body.
        item: The canvas item that the body was put on.

    Returns:
        A callback for the event that says the canvas has been resized.
    """
    def fitted(event: 'tkinter.Event[tkinter.Misc]') -> None:
        """Make the body as wide as the canvas now is."""
        canvas.itemconfigure(item, width=event.width)
    return fitted


def _wrap_to_width(label: tkinter.Label) -> None:
    """Make one label wrap its text to the width it is given.

    A Tk label does not wrap at all unless it is told how wide a line may be,
    and it does not shrink its text either: a paragraph wider than the window
    is simply cut off, which is how a description lost its last words. The
    width to wrap at is not known until the window has been laid out, and it
    changes whenever the user resizes it, so it is followed rather than set.

    Args:
        label: Label that holds text which may be longer than a line.
    """
    def wrapped(event: 'tkinter.Event[tkinter.Misc]') -> None:
        """Wrap the text of the label at the width it now has."""
        label.configure(wraplength=max(event.width, LEAST_WRAP_WIDTH))
    label.bind('<Configure>', wrapped)


class ScrollingArea(NamedTuple):
    """The part of the editor that scrolls, before it has been placed."""

    area: tkinter.Frame
    """The frame to pack where the scrolling part of the editor belongs."""

    body: tkinter.Frame
    """The frame to build the scrolling part of the editor in."""


def _scrolling_body(parent: tkinter.Misc) -> ScrollingArea:
    """Return the frame that the scrolling part of the editor is built in.

    Tk has no scrolling frame, so this is the one it has: a canvas with a
    scrollbar beside it and a frame on the canvas. What goes in the frame
    scrolls.

    The area is not packed here. Tk gives each child the space it asks for in
    the order they were packed, so the part that does not scroll has to be
    packed before this one to be sure of its space, while this one is created
    first so that the widgets of the editor are created in the order they are
    read in.

    Args:
        parent: Widget that becomes the parent of the created widgets.

    Returns:
        The frame to pack, and the frame to build in.
    """
    area = tkinter.Frame(parent)
    canvas = tkinter.Canvas(area, highlightthickness=0)
    slider = tkinter.Scrollbar(area, orient='vertical', command=canvas.yview)
    canvas.configure(yscrollcommand=slider.set, height=BODY_HEIGHT)
    slider.pack(side='right', fill='y')
    canvas.pack(side='left', fill='both', expand=True)
    body = tkinter.Frame(canvas)
    item = canvas.create_window(0, 0, window=body, anchor='nw')
    body.bind('<Configure>', _fit_body(canvas=canvas, body=body))
    canvas.bind('<Configure>', _fit_width(canvas=canvas, item=item))
    _bind_wheel(window=parent.winfo_toplevel(), canvas=canvas)
    return ScrollingArea(area=area, body=body)


def _show_description(label: Optional[tkinter.Label], text: str) -> None:
    """Show the description of one member, or hide it when there is none.

    The text is what the core says to show for this member, which is nothing
    while the explanations are hidden, so this backend does not decide for
    itself what hiding them means.

    Hiding is taking the widget out of the layout and not emptying its text,
    because a label with no text still takes the height of a line, and a
    window with a blank line under every member would have hidden nothing.
    The widget is the last one inside the frame of its member, so packing it
    again puts it back where it was.

    Args:
        label: Widget that shows the description of one member, or None for a
            member the application said nothing about.
        text: Description to show, empty when it is not being shown.
    """
    if label is None:
        return
    if not text:
        label.pack_forget()
        return
    label.config(text=text)
    label.pack(fill='x', padx=(DESCRIPTION_INDENT, PADDING))


class StateWidgets(NamedTuple):
    """The widgets that say what is true of the whole model.

    They are one object rather than one attribute each, so that the class
    below has a handful of things to hold rather than a dozen.
    """

    title: tkinter.Label
    """The label that names the configuration and marks unsaved changes."""

    docstring: Optional[tkinter.Label]
    """The label that says what the configuration class says about itself.

    It is None for a class with no docstring of its own, because there is then
    nothing that could ever appear in it.
    """

    verdict: tkinter.Label
    """The label that says what the application makes of these values."""

    saving: tkinter.Label
    """The label that says what saving did, or where it would write."""

    explained: tkinter.BooleanVar
    """Whether the tick-box of the explanations is ticked.

    The variable is what a `Checkbutton` shows its state through, and it has
    to be kept for as long as the tick-box lives: a `tkinter.Variable` unsets
    its Tcl variable when it is collected.
    """


class RowWidgets(NamedTuple):
    """The widgets that one configuration member owns."""

    field: Optional[tkinter.StringVar]
    """The field of an editable member, and None for every other member."""

    mark: tkinter.Label
    """The widget that says what has happened to this member."""

    description: Optional[tkinter.Label]
    """The widget that says what this member is for.

    It is None for a member the application said nothing about, because there
    is then nothing that could ever appear in it.
    """


class EditorWidgets:  # pylint: disable=too-few-public-methods
    """The widgets that show one edit model below one parent widget.

    This is a class rather than a function because the fields have to be
    kept: a `tkinter.StringVar` unsets its Tcl variable when it is collected,
    and the field it belongs to would then lose both its text and the
    callback that writes it into the model. Keeping them together also gives
    an application that mounts these widgets in a window of its own a single
    object to hold on to.

    The widgets of the members are kept in the order the model reports its
    rows in, which is the order they were created in. This version of the
    model neither adds nor removes a row, so the two orders stay the same
    one and the pairing is checked rather than assumed.
    """

    def __init__(self, parent: tkinter.Misc, model: core.EditModel, *,
                 on_close: Optional[Callable[[], None]] = None) -> None:
        """Create the labels, one row per member, the verdict and the buttons.

        The parent is a widget and not a window, so that the same rows can
        later be mounted inside a window that an application owns itself.

        Args:
            parent: Widget that becomes the parent of the created widgets.
            model: Model to show and to edit.
            on_close: What closing the editor does, or None to destroy the
                window these widgets are in. None is for a caller that owns
                that window, which is what `TkEditor` does. A caller that
                mounts these widgets in a window of an application says what
                closing does, because the editor must never destroy a window
                it did not create.
        """
        self._model = model
        self._close = on_close or parent.winfo_toplevel().destroy
        scrolling = _scrolling_body(parent)
        # The part that does not scroll is packed first, because Tk gives each
        # child the space it asks for in the order they were packed: a window
        # too short for everything would otherwise leave nothing at all for
        # the verdict, the saving and the buttons, and they are what a user
        # reaches for after editing. It is created second, so that the widgets
        # of the editor are still created in the order they are read in.
        fixed = tkinter.Frame(parent)
        fixed.pack(side='bottom', fill='x')
        scrolling.area.pack(side='top', fill='both', expand=True)
        body = scrolling.body
        title = tkinter.Label(body, text=core.model_title(model))
        title.pack(pady=PADDING)
        docstring = self._add_docstring(body)
        self._add_load_message(body)
        self._rows = [self._add_row(parent=body, row=row)
                      for row in model.rows]
        explained = tkinter.BooleanVar(master=parent,
                                       value=model.explanations_shown)
        self._state = StateWidgets(title=title, docstring=docstring,
                                   verdict=self._add_verdict(fixed),
                                   saving=self._add_saving(fixed),
                                   explained=explained)
        self._add_buttons(fixed)
        self._bind_keys(parent.winfo_toplevel())

    @property
    def label_text(self) -> str:
        """Return the text that the label of the whole model shows."""
        return str(self._state.title.cget('text'))

    @property
    def verdict_text_shown(self) -> str:
        """Return the text that the validation part of the editor shows."""
        return str(self._state.verdict.cget('text'))

    @property
    def save_text_shown(self) -> str:
        """Return the text that the saving part of the editor shows."""
        return str(self._state.saving.cget('text'))

    @property
    def docstring_shown(self) -> str:
        """Return the text that the label of the configuration class shows."""
        if self._state.docstring is None:
            return ''
        return str(self._state.docstring.cget('text'))

    def _add_docstring(self, parent: tkinter.Misc) -> Optional[tkinter.Label]:
        """Show what the configuration class says about itself, if anything.

        The widget is created only when that class has a docstring of its
        own. What the explain action changes is how much of a docstring is
        shown and not whether there is one, so a class without one would
        leave an empty widget taking a line of the window for good.

        Args:
            parent: Widget that becomes the parent of the created widget.

        Returns:
            The widget that shows the docstring, or None when the
            configuration class has none.
        """
        if not self._model.docstring:
            return None
        label = _shown_text(parent, core.docstring_text(self._model),
                            core.EXPLANATION)
        label.pack(fill='x', padx=PADDING)
        return label

    def _add_load_message(self, parent: tkinter.Misc) -> None:
        """Show what reading the input file did, when it did anything.

        The widget is created only when there is something to say. The file
        was read before the model was built, so the message cannot arrive
        later, and an empty widget would take a line of the window for a
        message that will never come.
        """
        message = core.load_text(self._model)
        if message:
            _shown_text(parent, message,
                        core.LOAD_REMARK).pack(fill='x', padx=PADDING)

    def _add_verdict(self, parent: tkinter.Misc) -> tkinter.Label:
        """Create the label that says what the application makes of these.

        It is packed below the scrolling part rather than at the end of it, so
        that it cannot scroll away: a user who has just asked what the
        application makes of these values is looking at it.
        """
        label = _shown_text(parent, core.verdict_text(self._model),
                            core.verdict_emphasis(self._model))
        label.pack(side='top', fill='x', padx=PADDING, pady=PADDING)
        return label

    def _add_saving(self, parent: tkinter.Misc) -> tkinter.Label:
        """Create the label that says what saving did, or where it would."""
        label = _shown_text(parent, core.save_text(self._model),
                            core.save_emphasis(self._model))
        label.pack(side='top', fill='x', padx=PADDING)
        return label

    def _add_buttons(self, parent: tkinter.Misc) -> None:
        """Create the buttons, the tick-box and the one that ends the run.

        They share one row, because five of them stacked above each other
        would push the values of a real configuration off the window.

        The explanations get a tick-box rather than a button, because the
        action is a toggle: a button saying Explain beside explanations that
        are already there would be offering something that has been done.
        """
        line = tkinter.Frame(parent)
        line.pack(side='top', pady=PADDING)
        for text, command in ((VALIDATE_TEXT, self._validate),
                              (SAVE_TEXT, self._save),
                              (SAVE_AS_TEXT, self._save_as)):
            tkinter.Button(line, text=text, command=command).pack(side='left',
                                                                  padx=PADDING)
        tkinter.Checkbutton(line, text=EXPLAIN_TEXT, command=self._explain,
                            variable=self._state.explained).pack(side='left',
                                                                 padx=PADDING)
        tkinter.Button(line, text=CLOSE_TEXT,
                       command=self._close).pack(side='left', padx=PADDING)

    def _bind_keys(self, window: tkinter.Misc) -> None:
        """Bind the key combinations that the application chose.

        The bindings are made on the window and not on each field, because
        a key that a field does not use for itself reaches the window that
        the field is in. Nothing is bound for the cancel action: the only
        question this backend asks is the toolkit's own file dialog, which
        answers that key itself.

        The keys are read once, here, which is the whole of what a later
        answer from a settings callable cannot change.

        Args:
            window: Window that the bindings are made on.
        """
        actions = self._model.settings.actions
        for keys, command in ((actions.quit, self._close),
                              (actions.validate, self._validate),
                              (actions.save, self._save),
                              (actions.save_as, self._save_as),
                              (actions.explain, self._explain)):
            for key in keys:
                _bind_key(window=window, key=key, command=command)

    def _add_row(self, parent: tkinter.Misc,
                 row: core.MemberRow) -> RowWidgets:
        """Create the widgets of one member, and its description below them.

        The member gets a frame of its own, holding the line that is edited
        and the description under it, so that hiding the description and
        showing it again cannot move it away from the member it belongs to.
        """
        frame = tkinter.Frame(parent)
        frame.pack(fill='x', padx=PADDING)
        line = tkinter.Frame(frame)
        line.pack(fill='x')
        tkinter.Label(line, text=row.name, width=NAME_COLUMN_WIDTH,
                      anchor='w').pack(side='left')
        field = self._add_value(parent=line, row=row)
        mark = _shown_text(line, core.row_marks(row), core.MEMBER_MARK,
                           wrapping=False)
        mark.pack(side='left')
        return RowWidgets(field=field, mark=mark,
                          description=self._add_description(parent=frame,
                                                            row=row))

    def _add_description(self, parent: tkinter.Misc,
                         row: core.MemberRow) -> Optional[tkinter.Label]:
        """Create the widget that says what one member is for, if anything.

        A member the application said nothing about gets no widget, because
        there is nothing that could ever appear in it.

        Args:
            parent: Frame of the member that is being described.
            row: Member to describe.

        Returns:
            The widget that shows the description, or None when the
            application said nothing about this member.
        """
        if not row.description:
            return None
        label = _shown_text(parent, '', core.EXPLANATION)
        _show_description(label,
                          text=core.row_description(model=self._model,
                                                    row=row))
        return label

    def _add_value(self, parent: tkinter.Misc,
                   row: core.MemberRow) -> Optional[tkinter.StringVar]:
        """Create the value widget of one member and wire it to the model.

        A member that the model cannot edit yet gets a widget that only
        shows text, because there is nothing the user could do to it.

        The variable is given the parent as its master, so that it is
        created in the same Tcl interpreter as the field that reads it. A
        variable constructed without one is created in the first interpreter
        of the process instead, which is the wrong one as soon as the editor
        is not the only Tk in the application: the field would then show
        nothing and the callback below would never run.
        """
        if not row.editable:
            tkinter.Label(parent, text=core.row_value_text(row),
                          anchor='w').pack(side='left')
            return None
        field = tkinter.StringVar(master=parent,
                                  value=core.row_value_text(row))
        # The window is white, so a field that kept the background it is given
        # could not be told from a label. The tint, the border and the caret
        # colour are what say that this one is edited and the labels are not.
        entry = tkinter.Entry(parent, textvariable=field, relief='flat',
                              width=LEAST_FIELD_WIDTH,
                              background=FIELD_BACKGROUND,
                              foreground=FIELD_FOREGROUND,
                              insertbackground=FIELD_FOREGROUND,
                              highlightbackground=FIELD_BORDER,
                              highlightthickness=1)
        entry.pack(side='left', fill='x', expand=True)
        field.trace_add('write', self._writer(row=row, field=field))
        return field

    def _writer(self, row: core.MemberRow,
                field: tkinter.StringVar) -> Callable[..., None]:
        """Return the callback that writes one field into the model.

        Tk reports a change of the variable and not of the widget, so the
        callback reads the field itself. Every change is written through,
        including the ones that no key press caused, such as a paste.
        """
        def write_field(*trace_arguments: str) -> None:
            """Write the text of the field and show what the model says."""
            _ = trace_arguments
            self._model.set_text(path=row.path, text=field.get())
            self._show_state()
        return write_field

    def _validate(self) -> None:
        """Validate the buffer and show what the application would say."""
        self._model.validate()
        self._refresh()

    def _save(self) -> None:
        """Write the output file, and say what came of trying.

        Saving validates, so it can rewrite a value exactly as validating
        can, and the fields are refreshed for the same reason.

        A session that has no file to write yet is asked where to write,
        which is what every editor does and what the design asks a backend
        for. There is no way round to loop back here, because the question
        is what gives the session a file.
        """
        if self._model.out_file is None:
            self._save_as()
            return
        self._model.save()
        self._refresh()

    def _save_as(self) -> None:
        """Ask which file to write, and write it when one was named.

        What the dialog offers is what the application decided: the
        extension it uses for its configuration is the one the dialog adds
        to a name that has none, and the one it offers to filter by. An
        application with no opinion gets a dialog with none, which is what
        this dialog had before there were settings at all.

        The name that comes back is handed to the model, which is what
        completes it and what refuses it, so that a user of this backend and
        a user of the other one are told the same thing about one name.
        """
        settings = self._model.settings
        chosen = filedialog.asksaveasfilename(
            title=SAVE_AS_TITLE, filetypes=_file_types(settings),
            defaultextension=settings.file_extension or '')
        if chosen:
            self._model.set_out_file(chosen)
            self._save()

    def _explain(self) -> None:
        """Show or hide what the application says about these values."""
        self._model.toggle_explanations()
        self._show_explanations()

    def _show_explanations(self) -> None:
        """Show as much of the explanatory text as the model says to show.

        The tick-box is set from the model rather than left to Tk, because Tk
        only flips it when it is the tick-box that was pressed. The key of the
        explain action reaches this method without touching it, and a tick
        that disagreed with the window would be worse than no tick at all.

        It is not part of `_show_state`, which runs on every key the user
        types: nothing the user types into a field can change what this
        configuration is for or what one of its members means.
        """
        self._state.explained.set(self._model.explanations_shown)
        if self._state.docstring is not None:
            self._state.docstring.config(text=core.docstring_text(self._model))
        for row, widgets in zip(self._model.rows, self._rows, strict=True):
            _show_description(widgets.description,
                              text=core.row_description(model=self._model,
                                                        row=row))

    def _refresh(self) -> None:
        """Write the buffer back into the fields and show the new state.

        A pass over the buffer is not read only: a member validator returns
        the value that is stored back into the member, so a value can end up
        different from the one the user typed. Writing the text the model
        already holds into a field is not an edit, so this refresh does not
        undo the marks that the pass has just set.
        """
        for row, widgets in zip(self._model.rows, self._rows, strict=True):
            if widgets.field is not None:
                widgets.field.set(core.row_value_text(row))
        self._show_state()

    def _show_state(self) -> None:
        """Show the label, the verdict, the saving and every member mark.

        The verdict and the saving change colour as well as text, because what
        they say is either what the application accepted, what it refused, or
        what has not been asked of it yet, and a user who has to read three
        lines to tell those apart is reading too much.
        """
        self._state.title.config(text=core.model_title(self._model))
        _told(self._state.verdict, text=core.verdict_text(self._model),
              emphasis=core.verdict_emphasis(self._model))
        _told(self._state.saving, text=core.save_text(self._model),
              emphasis=core.save_emphasis(self._model))
        for row, widgets in zip(self._model.rows, self._rows, strict=True):
            widgets.mark.config(text=core.row_marks(row))


class TkEditor:  # pylint: disable=too-few-public-methods
    """Tkinter user interface backend for an edit model.

    The class has the single method that `EditorBackend` asks for, and
    deliberately nothing else: everything worth testing without a display
    lives in the core.
    """

    def __init__(self) -> None:
        """Create a backend that has not shown a model yet."""
        self._widgets: Optional[EditorWidgets] = None

    def run_editor(self, model: core.EditModel) -> None:
        """Show the model in a Tk window until the user closes it.

        The widgets are held for as long as the window lives, because they
        own the fields that the Tcl variables belong to. The window is this
        backend's own, which is why closing the editor destroys it.

        This is for an application that has no Tk of its own yet, because a
        second `tkinter.Tk` is a second Tcl interpreter and nothing can be
        shared between the two. An application that already runs Tk gets the
        entry point of section 8.2 of `doc/design.md` instead, which mounts
        the editor in a widget that application owns.

        Args:
            model: Model to show and to edit.
        """
        window = tkinter.Tk()
        window.title(model.config_type_name)
        self._widgets = EditorWidgets(parent=window, model=model)
        window.mainloop()


# See the same disable in the core: every argument after the first is an
# optional keyword saying one independent thing about the session.
# pylint: disable-next=too-many-arguments
def edit(config: Config, *, descriptions: Optional[core.Descriptions] = None,
         in_file: Optional[PathOrStr] = None,
         out_file: Optional[PathOrStr] = None,
         policy: core.LoadPolicy = core.LoadPolicy.STRICT_THEN_DEFAULTS,
         settings: core.SettingsSource = core.Settings(),
         stderr_file: TextIO = sys.stderr) -> Optional[Config]:
    """Edit one configuration in a Tk window, and return what was saved.

    This is `edit_cfg_json.edit` with this package's backend filled in, for
    an application that has already chosen Tkinter. Everything it does is
    documented there.

    Args:
        config: Configuration object to edit. It is never modified.
        descriptions: What the application says about the members it
            declares, or None when it says nothing.
        in_file: File to read, or None to start from the declared defaults.
        out_file: File to write, or None to write the input file.
        policy: What to do about declared keys the input file does not hold.
        settings: What this application has already decided about key
            combinations and file names, or a callable that answers with it.
        stderr_file: Stream used for user-facing diagnostics.

    Returns:
        The configuration object that was written, or None when nothing was.

    Raises:
        ConfigLoadError: The input file cannot be opened for editing.
    """
    return core.edit(config=config, backend=TkEditor(),
                     descriptions=descriptions, in_file=in_file,
                     out_file=out_file, policy=policy, settings=settings,
                     stderr_file=stderr_file)
