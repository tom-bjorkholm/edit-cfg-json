#! /usr/bin/env python3
"""What the tests of the Tkinter backend share.

The stubs, the ways of reading a real Tk window and the widget texts that both
of them expect live here, so that the four test modules of this backend test
the same editor and cannot drift apart about what it looks like. The stubbed
and the real way of doing one thing are side by side on purpose: a stub can
drift from what Tk really does, and real Tk can hide a wrong value behind a
widget default, so a difference between the two is itself a finding.

The configuration class comes from the example rather than from a class of its
own, so that the same flat configuration is used by the core tests, by both
backends and by the example itself.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from collections.abc import Callable
from pathlib import Path
from typing import ClassVar, Optional, cast
import json
import tkinter
from tkinter import messagebox
import pytest
from edit_cfg_json import Descriptions, EditModel, LoadReport
from edit_cfg_json_tk.tk_editor import CLOSE_TEXT, EditorWidgets, \
    EXPLAIN_TEXT, FOLD_OPEN_TEXT, SAVE_AS_TEXT, SAVE_TEXT, VALIDATE_TEXT
from edit_cfg_json_tk.tk_find import FIND_FIELD_NAME, FIND_LABEL_TEXT, \
    FIND_NEXT_TEXT, FIND_TICK_LABELS
from example.e01_flat_config import FlatConfig

UNKNOWN_VERDICT = 'validation: not validated'
"""Text the editor shows before anything has been validated."""

TEXT_KIND = 'Text.'
"""What the type of a text member says about it.

The editor says what kind of value every member holds, because that is the one
thing it knows about every member of every configuration without being told.
It is written out here rather than read from an internal module of the core, in
the same way as every other text these tests expect.
"""

WHOLE_KIND = 'A whole number.'
"""What the type of a member holding a whole number says about it."""

ABOUT_NAME = 'What the name of this configuration is for.'
"""Description of the one member that the tests below describe."""

DESCRIPTIONS: Descriptions = {('name',): ABOUT_NAME}
"""What an application says about the members of the example."""

FLAT_DOCSTRING = EditModel(FlatConfig()).docstring
"""The docstring of the example, as the editor shows it in full.

It is read from the model rather than written out here, because what these
tests are about is that the editor has a widget for it and shows it in the
right place. What the text of a docstring becomes is decided in the core and
tested there.
"""

FLAT_SUMMARY = EditModel(FlatConfig()).summary
"""The first paragraph of that docstring, which is what hiding leaves."""

LOAD_MESSAGE = 'the file left something out'
"""Message of the load in the tests that show one."""

FILLED_REPORT = LoadReport(message=LOAD_MESSAGE, filled=frozenset({'answer'}))
"""Report of a load that filled the number member in from the default."""

FILLED_MARK = ' (filled from default)'
"""Mark of a member that the input file did not hold."""

VALID_VERDICT = 'validation: valid'
"""Text the editor shows for a buffer the application would accept."""

REFUSED_VERDICT = 'validation: invalid, see answer'
"""Text the editor shows when the number member of the example is refused.

What was refused is said beside that member, so this line only names it: a
configuration too tall for a window would otherwise leave the user hunting
for the field that the refusal is about.
"""

NO_FILE_TEXT = 'save to: no file chosen yet'
"""Text the editor shows while no output file has been chosen."""

BUTTON_TEXTS = [VALIDATE_TEXT, SAVE_TEXT, SAVE_AS_TEXT, EXPLAIN_TEXT,
                CLOSE_TEXT]
"""Texts of the buttons of the editor, in the order they are created."""

FIND_TEXTS = [FIND_LABEL_TEXT, *FIND_TICK_LABELS, FIND_NEXT_TEXT]
"""Texts of the search row, in the order they are created.

The field itself shows no text of the editor's, and the line that says what the
search has reached is out of the layout while nothing is being looked for, so
what is left is the label, the four controls and the button. They come before
the verdict, because the search is about the rows above them.
"""

EXPECTED_LABELS = ['FlatConfig', FLAT_DOCSTRING, 'name', '', TEXT_KIND,
                   'answer', '', WHOLE_KIND, *FIND_TEXTS, UNKNOWN_VERDICT,
                   NO_FILE_TEXT, *BUTTON_TEXTS]
"""Widget texts that both the stubbed and the real Tk test expect.

The docstring of the configuration class is below its name, because what the
whole configuration is for is what the members below it are read in the light
of. The two empty strings are the marks of the two members, which say nothing
until the user or a validator has done something to them, and the line below
each member is what the type of that member says about it.
"""

EXPECTED_LOADED = ['FlatConfig', FLAT_DOCSTRING, LOAD_MESSAGE, 'name', '',
                   TEXT_KIND, 'answer', FILLED_MARK, WHOLE_KIND, *FIND_TEXTS,
                   UNKNOWN_VERDICT, NO_FILE_TEXT, *BUTTON_TEXTS]
"""Widget texts of a model whose load filled the number member in.

The message of the load is above the members, because it is what explains
the mark on one of them. The empty string is the mark of the member the file
did hold, which has nothing to say.
"""

DESCRIBED_LABELS = ['FlatConfig', FLAT_DOCSTRING, 'name', '',
                    f'{ABOUT_NAME}\n{TEXT_KIND}', 'answer', '', WHOLE_KIND,
                    *FIND_TEXTS, UNKNOWN_VERDICT, NO_FILE_TEXT,
                    *BUTTON_TEXTS]
"""Widget texts of a model whose text member the application describes.

The description is below the member it belongs to, with what the type of that
member says under it. An application that describes half of its configuration
gets half of it explained, and the other half still says what kind of value it
holds, because that is the editor's own to say.
"""

HIDDEN_LABELS = ['FlatConfig', FLAT_SUMMARY, 'name', '', 'answer', '',
                 *FIND_TEXTS, UNKNOWN_VERDICT, NO_FILE_TEXT, *BUTTON_TEXTS]
"""Widget texts of that same model with the explanations hidden.

What is left of the docstring is its summary, which is one line for the whole
configuration, and the description of the member is out of the layout.
"""

EXPECTED_FIELDS = ['Flat example', '42']
"""Field contents that both the stubbed and the real Tk test expect."""


class NoDocConfig(FlatConfig):
    """This docstring is taken away below, so that this class has none."""


# A configuration class written without a docstring is one the editor has to
# handle, and it cannot be written here, because every class in this
# repository has to have one. Taking it away afterwards is the same thing.
NoDocConfig.__doc__ = None

REWRITTEN_MARK = ' (edited) (changed by validator)'
"""Mark of a member that the user changed and a validator then rewrote."""

STUB_BODY_HEIGHT = 1000
"""Height that the stub reports for the scrolling part of the editor.

It is taller than the height that part is allowed to have, so that the stubbed
tests see what the editor does with a configuration too tall for a window.
"""

STUB_BODY_WIDTH = 500
"""Width that the stub reports for the scrolling part of the editor.

It is narrower than the width the editor opens at, which is what makes a
stubbed test able to see whether the width is being followed: an editor that
took this answer would be narrower than the one width it is supposed to have.
"""

WHOLE_VIEW = (0.0, 1.0)
"""The fractions a canvas reports while all of its contents are in view.

It is what the stub answers unless a test says otherwise, so that a search
finds what it was looking for already on the window and scrolls nothing. A test
that is about the scrolling says that only a part is in view instead.
"""

STUB_CANVAS_ITEM = 7
"""Identifier that the stub gives the one item it is asked to create."""


BORN_TAGS = ('widget', 'FakeWidget', 'all')
"""The bind tags a stub widget is born with.

Real Tk gives every widget its own name, its class, its window and `all`, in
that order. What the editor does with them is add a tag of its own at one end
or the other, so what the stub needs of them is that there are some and that
their order can be read.
"""


class FakeWindow:
    """The part of the stand-in that stands in for a Tkinter window.

    A window is asked things no other widget is asked — its name, what its
    close button does, which window it belongs over and whether it holds the
    events of the application — and those are here so that what a stub widget
    is stays readable beside them.
    """

    def __init__(self) -> None:
        """Start with a window that is named nothing and grabs nothing."""
        self.window_title = ''
        self.protocols: dict[str, Callable[[], None]] = {}
        self.transient_to: object = None
        self.grabbed = False

    def title(self, text: str) -> None:
        """Name this window, as a real Tk toplevel is named."""
        self.window_title = text

    def protocol(self, name: str, callback: Callable[[], None]) -> None:
        """Record what one window manager protocol of this window does."""
        self.protocols[name] = callback

    def transient(self, parent: object) -> None:
        """Record which window this one is a transient of."""
        self.transient_to = parent

    def grab_set(self) -> None:
        """Take the events of the application for this widget."""
        self.grabbed = True

    def grab_release(self) -> None:
        """Give the events of the application back."""
        self.grabbed = False


class FakeCanvas(FakeWindow):
    """The part of the stand-in that stands in for a Tkinter canvas.

    One stub serves every widget class the editor creates, and the scrolling
    part of the editor is the one place where the methods of a particular
    class are really used. They are here so that what a stub widget is stays
    readable beside them.
    """

    def __init__(self) -> None:
        """Start with a canvas that has not been scrolled."""
        super().__init__()
        self.scrolled = 0
        self.moved: list[float] = []
        self.view = WHOLE_VIEW

    def create_window(self, *place: int, **options: object) -> int:
        """Put a widget on this canvas, as a real Tk canvas does.

        The widget counts as being in the layout afterwards, because that is
        what a canvas item is: the scrolling part of the editor is on a
        canvas and not packed, and everything in it would otherwise be
        reported as hidden.
        """
        _ = place
        window = options.get('window')
        if isinstance(window, FakeWidget):
            window.packed = True
        return STUB_CANVAS_ITEM

    def itemconfigure(self, item: int, **options: object) -> None:
        """Change options of one item of this canvas."""
        _ = (item, options)

    def bbox(self, *what: str) -> tuple[int, int, int, int]:
        """Return the area the contents of this canvas take up."""
        _ = what
        return (0, 0, 0, STUB_BODY_HEIGHT)

    def yview(self, *arguments: str) -> tuple[float, float]:
        """Scroll this canvas, or say how much of it is in view.

        Real Tk answers with the two fractions when it is asked without
        arguments, which is what a search reads before it decides whether it
        has to scroll at all.
        """
        _ = arguments
        return self.view

    def yview_moveto(self, fraction: float) -> None:
        """Record where a search asked this canvas to look."""
        self.moved.append(fraction)

    def update_idletasks(self) -> None:
        """Lay out what is waiting to be laid out, as real Tk does."""

    def yview_scroll(self, number: int, what: str) -> None:
        """Record how far the wheel scrolled this canvas."""
        assert what == 'units'
        self.scrolled += number

    def set(self, *fractions: str) -> None:
        """Show how much of the contents is visible, as a scrollbar does."""
        _ = fractions


class FakeWidget(FakeCanvas):
    """Recording stand-in for a Tkinter widget in the stubbed tests."""

    created: ClassVar[list['FakeWidget']] = []
    """Every stub widget created since the list was last cleared."""

    tag_bindings: ClassVar[dict[str, dict[str, Callable[..., object]]]] = {}
    """What is bound on each bind tag, standing in for the interpreter.

    A bind tag is a name in the Tcl interpreter and not a widget, which is why
    this is one table for the whole process and not an attribute of a widget.
    """

    focused: ClassVar[list['FakeWidget']] = []
    """Every widget that has been given the keyboard focus, in order.

    The focus belongs to the interpreter and not to a widget in real Tk
    either: exactly one widget has it, and it is the last one that asked.
    """

    def __init__(self, parent: object = None, **options: object) -> None:
        """Record this widget together with its parent and its options."""
        self.parent = parent
        self.options = options
        self.bindings: dict[str, Callable[..., object]] = {}
        self.tags: tuple[str, ...] = BORN_TAGS
        self.packed = False
        self.packing: dict[str, object] = {}
        super().__init__()
        FakeWidget.created.append(self)

    def bindtags(self, tags: Optional[tuple[str, ...]] = None
                 ) -> Optional[tuple[str, ...]]:
        """Read or replace the bind tags of this widget, as Tk does.

        Args:
            tags: The tags this widget is to carry, or None to read them.

        Returns:
            The tags this widget carries, and None when it was given some.
        """
        if tags is None:
            return self.tags
        self.tags = tuple(tags)
        return None

    def bind_class(self, tag: str, sequence: str,
                   callback: Callable[..., object]) -> str:
        """Record one binding made on a bind tag, as a real widget does."""
        FakeWidget.tag_bindings.setdefault(tag, {})[sequence] = callback
        return 'stub class binding'

    def unbind_class(self, tag: str, sequence: str) -> None:
        """Take one binding off a bind tag, as a real widget does."""
        FakeWidget.tag_bindings.get(tag, {}).pop(sequence, None)

    def focus_set(self) -> None:
        """Record that this widget has been given the keyboard focus."""
        FakeWidget.focused.append(self)

    @property
    def shown(self) -> bool:
        """Return whether this widget is really on the window.

        A widget inside a frame that has been taken out of the layout is not
        on the window, whatever the widget itself was told: that is how the
        editor folds a container away, and a stub that answered only for the
        widget would say that a folded value is shown.

        The widget the editor was built below is the one this stops at. It is
        the test's own stand-in for a window, so it is never packed and
        everything inside it would otherwise be hidden.
        """
        if self is FakeWidget.created[0]:
            return True
        if not self.packed:
            return False
        parent = self.parent
        return not isinstance(parent, FakeWidget) or parent.shown

    def bind(self, sequence: str, callback: Callable[..., object]) -> str:
        """Record one key binding, as a real Tk widget accepts one."""
        self.bindings[sequence] = callback
        return 'stub binding'

    def pack(self, **options: object) -> None:
        """Record that this widget is in the layout, and how it was put there.

        Where a widget ends up on the screen is what the real Tk tests are
        for. Whether it is in the layout at all is what tells a hidden
        description from a shown one, and how far from the left edge it was
        asked to be is what tells a value inside a container from a member,
        and a stub can answer both of those.
        """
        self.packed = True
        self.packing = dict(options)

    def pack_forget(self) -> None:
        """Record that this widget is out of the layout."""
        self.packed = False

    def config(self, **options: object) -> None:
        """Change options of this widget, as a real Tk widget does."""
        self.options.update(options)

    def cget(self, name: str) -> object:
        """Return one option of this widget, as a real Tk widget does."""
        return self.options[name]

    def configure(self, **options: object) -> None:
        """Change options of this widget, as a real Tk widget does."""
        self.options.update(options)

    def winfo_toplevel(self) -> 'FakeWidget':
        """Return this widget, standing in for the enclosing window."""
        return self

    def winfo_children(self) -> list['FakeWidget']:
        """Return the stub widgets that were created below this one."""
        return [widget for widget in FakeWidget.created
                if widget.parent is self]

    def winfo_rooty(self) -> int:
        """Return where this widget is on the screen, standing in for Tk."""
        return 0

    def winfo_height(self) -> int:
        """Return a height, standing in for one that Tk would lay out."""
        return STUB_BODY_HEIGHT

    def winfo_reqheight(self) -> int:
        """Return a height, standing in for one that Tk would have laid out."""
        return STUB_BODY_HEIGHT

    def winfo_reqwidth(self) -> int:
        """Return a width, standing in for one that Tk would have laid out."""
        return STUB_BODY_WIDTH

    def destroy(self) -> None:
        """Forget this widget and everything below it, as Tk does.

        The editor destroys the rows it built when a validation pass leaves
        the model with other rows than it had, and a stub that remembered the
        destroyed ones would let a test read a window that is not there.
        """
        for child in self.winfo_children():
            child.destroy()
        if self in FakeWidget.created:
            FakeWidget.created.remove(self)

    def invoke(self) -> None:
        """Call the command of this widget, as a real Tk button does."""
        command = self.options['command']
        assert callable(command)
        command()


class FakeFlag:
    """Recording stand-in for a `tkinter.BooleanVar` in the stubbed tests.

    A tick-box shows its state through one of these, and Tk flips it itself
    when the box is pressed. This stub does neither of those things: it holds
    what it is told, which is what shows that the editor keeps the tick and
    the window saying the same thing.
    """

    created: ClassVar[list['FakeFlag']] = []
    """Every stub flag created since the list was last cleared."""

    def __init__(self, master: object = None, value: bool = False) -> None:
        """Record this flag, its master and the state it starts in."""
        self.master = master
        self.value = value
        FakeFlag.created.append(self)

    def get(self) -> bool:
        """Return the state this flag holds."""
        return self.value

    def set(self, value: bool) -> None:
        """Change the state this flag holds."""
        self.value = value


class FakeVar:
    """Recording stand-in for a `tkinter.StringVar` in the stubbed tests."""

    created: ClassVar[list['FakeVar']] = []
    """Every stub variable created since the list was last cleared."""

    def __init__(self, master: object = None, value: str = '') -> None:
        """Record this variable, its master and the text it starts with."""
        self.master = master
        self.value = value
        self.callbacks: list[Callable[..., None]] = []
        FakeVar.created.append(self)

    def get(self) -> str:
        """Return the text this variable holds."""
        return self.value

    def set(self, value: str) -> None:
        """Change the text and tell everyone who traced this variable."""
        self.value = value
        for callback in self.callbacks:
            callback()

    def trace_add(self, mode: str, callback: Callable[..., None]) -> str:
        """Record a callback that a change of this variable calls."""
        assert mode == 'write'
        self.callbacks.append(callback)
        return 'stub trace'


def stub_editor(model: EditModel) -> EditorWidgets:
    """Build the stubbed widgets of one model below a stub parent."""
    return EditorWidgets(parent=cast(tkinter.Misc, FakeWidget()), model=model)


def stub_texts(packed_only: bool = False) -> list[str]:
    """Return the text of every stub widget that was given one.

    Args:
        packed_only: Whether to leave out the widgets that are not in the
            layout, which is how the editor hides a description.

    Returns:
        The text of every stub widget that has one.
    """
    return [str(widget.options['text']) for widget in FakeWidget.created
            if 'text' in widget.options and (widget.shown or not packed_only)]


def stub_press(button_text: str) -> None:
    """Press the one stub button that shows the given text."""
    buttons = [widget for widget in FakeWidget.created
               if widget.options.get('text') == button_text]
    assert len(buttons) == 1
    buttons[0].invoke()


def stub_fold(text: str = FOLD_OPEN_TEXT) -> None:
    """Press the first stub fold control that shows one text.

    There is one per node that holds rows, so the one to press is named by
    its place among them and not by its text: what a control says is what the
    next press of it does, so several of them say the same thing.

    Args:
        text: What that control shows now.
    """
    controls = [widget for widget in FakeWidget.created
                if widget.packed and widget.options.get('text') == text]
    assert controls
    controls[0].invoke()


def _shows_text(widget: tkinter.Misc, packed_only: bool) -> bool:
    """Return whether one real Tk widget counts as showing text.

    A widget that a geometry manager has been told nothing about is not in
    the layout, which is how the editor hides a description. That is asked
    here rather than `winfo_ismapped`, which is false for every widget of a
    window that has not been shown, and the tests use a withdrawn one.

    Args:
        widget: Widget to look at.
        packed_only: Whether a widget out of the layout is left out.

    Returns:
        Whether the text of that widget is one of the texts of the editor.
    """
    if 'text' not in widget.keys():
        return False
    return bool(widget.winfo_manager()) or not packed_only


def real_texts(widget: tkinter.Misc, packed_only: bool = False) -> list[str]:
    """Return the text of every real Tk widget below one widget.

    The order is the order the widgets were created in, which the editor keeps
    the same as the order they are read in: the part that does not scroll is
    *packed* before the part that does, so that a window too short for
    everything still has room for it, and it is created afterwards.

    Args:
        widget: Widget whose descendants are read.
        packed_only: Whether to leave out the widgets that are not in the
            layout, which is how the editor hides a description.

    Returns:
        The text of every widget below that widget that has one.
    """
    texts: list[str] = []
    for child in widget.winfo_children():
        if packed_only and not child.winfo_manager():
            # A widget inside a frame that is out of the layout is not on the
            # window either, and it still has a geometry manager of its own.
            # That is how the editor folds a container away.
            continue
        if _shows_text(child, packed_only=packed_only):
            texts.append(str(child.cget('text')))
        texts.extend(real_texts(child, packed_only=packed_only))
    return texts


def real_fields(widget: tkinter.Misc) -> list[tkinter.Entry]:
    """Return every real Tk field of a member below one widget, in row order.

    The field that a search is typed into is left out, because it holds no
    member of the configuration: it is told from the others by its Tk name,
    which is what that name is for.
    """
    return [field for field in _all_fields(widget)
            if field.winfo_name() != FIND_FIELD_NAME]


def _all_fields(widget: tkinter.Misc) -> list[tkinter.Entry]:
    """Return every real Tk edit field below one widget, in creation order."""
    fields: list[tkinter.Entry] = []
    for child in widget.winfo_children():
        if isinstance(child, tkinter.Entry):
            fields.append(child)
        fields.extend(_all_fields(child))
    return fields


def find_field(widget: tkinter.Misc) -> tkinter.Entry:
    """Return the one real Tk field that a search is typed into."""
    fields = [field for field in _all_fields(widget)
              if field.winfo_name() == FIND_FIELD_NAME]
    assert len(fields) == 1
    return fields[0]


def stub_fields() -> list[FakeVar]:
    """Return the variable of every stub field of a member, in row order.

    `FakeVar.created` holds one more than these: the field that a search is
    typed into, created after the rows. It is left out here for the same reason
    as in `real_fields`, and it is reached by `stub_find_var`.
    """
    return [variable for widget, variable in _stub_fields()
            if widget.options.get('name') != FIND_FIELD_NAME]


def stub_field_widgets() -> list[FakeWidget]:
    """Return every stub field of a member, in row order.

    It is the widgets where `stub_fields` is the variables, and the field that
    a search is typed into is left out of both.
    """
    return [widget for widget, _ in _stub_fields()
            if widget.options.get('name') != FIND_FIELD_NAME]


def stub_find_var() -> FakeVar:
    """Return the variable of the stub field that a search is typed into."""
    found = [variable for widget, variable in _stub_fields()
             if widget.options.get('name') == FIND_FIELD_NAME]
    assert len(found) == 1
    return found[0]


def _stub_fields() -> list[tuple[FakeWidget, FakeVar]]:
    """Return every stub field and its variable, in creation order."""
    return [(widget, variable) for widget in FakeWidget.created
            if isinstance(variable := widget.options.get('textvariable'),
                          FakeVar)]


def stub_flag(label: str) -> FakeFlag:
    """Return the variable of the one stub tick-box showing one label.

    The editor has five tick-boxes now — the four that say where a search
    looks and the one that shows or hides the explanations — so a test says
    which of them it means by the label on it.

    Args:
        label: Text on the tick-box.

    Returns:
        The variable that holds whether it is ticked.
    """
    boxes = [widget for widget in FakeWidget.created
             if widget.options.get('text') == label
             and 'variable' in widget.options]
    assert len(boxes) == 1
    flag = boxes[0].options['variable']
    assert isinstance(flag, FakeFlag)
    return flag


def real_tick(widget: tkinter.Misc, label: str) -> bool:
    """Return whether the one real tick-box showing one label is ticked.

    Args:
        widget: Widget whose descendants are read.
        label: Text on the tick-box.

    Returns:
        Whether it is ticked.
    """
    boxes = [box for box in real_buttons(widget)
             if isinstance(box, tkinter.Checkbutton)
             and str(box.cget('text')) == label]
    assert len(boxes) == 1
    return _is_ticked(boxes[0])


def real_buttons(widget: tkinter.Misc
                 ) -> list[tkinter.Button | tkinter.Checkbutton]:
    """Return everything below one widget that can be pressed.

    A tick-box counts as one: it is what this backend offers for the action
    that is a toggle, and pressing it is what a user does to it.
    """
    buttons: list[tkinter.Button | tkinter.Checkbutton] = []
    for child in widget.winfo_children():
        if isinstance(child, (tkinter.Button, tkinter.Checkbutton)):
            buttons.append(child)
        buttons.extend(real_buttons(child))
    return buttons


def real_press(widget: tkinter.Misc, button_text: str) -> None:
    """Press the one real Tk button below one widget that shows the text."""
    buttons = [button for button in real_buttons(widget)
               if str(button.cget('text')) == button_text]
    assert len(buttons) == 1
    buttons[0].invoke()


def real_fold(parent: tkinter.Misc, text: str = FOLD_OPEN_TEXT) -> None:
    """Press the first real Tk fold control that shows one text.

    Args:
        parent: Widget whose descendants are looked through.
        text: What that control shows now.
    """
    controls = [button for button in real_buttons(parent)
                if str(button.cget('text')) == text]
    assert controls
    controls[0].invoke()


def retype(field: tkinter.Entry, text: str) -> None:
    """Replace the whole content of one real Tk field."""
    field.delete(0, 'end')
    field.insert(0, text)


def model_value(model: EditModel, name: str) -> object:
    """Return the value that the buffer holds for one member."""
    return {row.name: row.value for row in model.rows}[name]


def written(out_file: Path) -> object:
    """Return what one output file holds, as JSON space values."""
    return json.loads(out_file.read_text(encoding='UTF-8'))


def answer_question(monkeypatch: pytest.MonkeyPatch,
                    answer: bool) -> list[str]:
    """Make every yes or no question answer itself, and record each of them.

    Both of the questions this backend answers this way — whether the changes
    may be dropped and whether a file may be overwritten — go to the one
    dialog of the toolkit, so one stand-in serves both and neither test module
    holds a copy of it.

    Args:
        monkeypatch: The pytest fixture that replaces the dialog.
        answer: What the user answers, for every question that is put.

    Returns:
        A list that gets the question every time one is put.
    """
    asked: list[str] = []

    def ask(**options: object) -> bool:
        """Stand in for the system dialog that asks a yes or no question."""
        asked.append(str(options['message']))
        return answer
    monkeypatch.setattr(messagebox, 'askyesno', ask)
    return asked


def stub_window() -> FakeWidget:
    """Return the stub widget that the editor was built below."""
    return FakeWidget.created[0]


def stub_tags(widget: FakeWidget) -> tuple[str, ...]:
    """Return the bind tags of one stub widget.

    Reading them is what a stubbed test does about the keys of the editor
    reaching one widget and not another, and the stub answers with None when
    it is being *given* tags, which is what this asks away.
    """
    tags = widget.bindtags()
    assert tags is not None
    return tags


def stub_keys() -> dict[str, Callable[..., object]]:
    """Return what the editor bound in the part of the window it reaches.

    The keys and the mouse wheel are bound on a bind tag of the editor's own
    rather than on a widget, so that an editor mounted in a window an
    application owns does not claim the keys of the whole window. This is
    what a test presses instead of a widget.
    """
    assert FakeWidget.tag_bindings
    return list(FakeWidget.tag_bindings.values())[-1]


def real_ticks(widget: tkinter.Misc) -> list[bool]:
    """Return the state of every real Tk tick-box below one widget.

    Tk keeps the state in a variable of its own rather than in the widget, so
    it is read the way a user reads it: a tick-box whose value equals its
    `onvalue` is ticked.

    Args:
        widget: Widget whose descendants are read.

    Returns:
        Whether each tick-box below that widget is ticked, in creation order.
    """
    return [_is_ticked(box) for box in real_buttons(widget)
            if isinstance(box, tkinter.Checkbutton)]


def _is_ticked(box: tkinter.Checkbutton) -> bool:
    """Return whether one real Tk tick-box is ticked.

    Args:
        box: Tick-box to read.

    Returns:
        Whether its variable holds the value it holds when it is ticked.
    """
    held = box.getvar(str(box.cget('variable')))
    return str(held) == str(box.cget('onvalue'))
