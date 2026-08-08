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
from typing import ClassVar, cast
import json
import tkinter
from edit_cfg_json import Descriptions, EditModel, LoadReport
from edit_cfg_json_tk.tk_editor import CLOSE_TEXT, EditorWidgets, \
    EXPLAIN_TEXT, FOLD_OPEN_TEXT, SAVE_AS_TEXT, SAVE_TEXT, VALIDATE_TEXT
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

EXPECTED_LABELS = ['FlatConfig', FLAT_DOCSTRING, 'name', '', TEXT_KIND,
                   'answer', '', WHOLE_KIND, UNKNOWN_VERDICT, NO_FILE_TEXT,
                   *BUTTON_TEXTS]
"""Widget texts that both the stubbed and the real Tk test expect.

The docstring of the configuration class is below its name, because what the
whole configuration is for is what the members below it are read in the light
of. The two empty strings are the marks of the two members, which say nothing
until the user or a validator has done something to them, and the line below
each member is what the type of that member says about it.
"""

EXPECTED_LOADED = ['FlatConfig', FLAT_DOCSTRING, LOAD_MESSAGE, 'name', '',
                   TEXT_KIND, 'answer', FILLED_MARK, WHOLE_KIND,
                   UNKNOWN_VERDICT, NO_FILE_TEXT, *BUTTON_TEXTS]
"""Widget texts of a model whose load filled the number member in.

The message of the load is above the members, because it is what explains
the mark on one of them. The empty string is the mark of the member the file
did hold, which has nothing to say.
"""

DESCRIBED_LABELS = ['FlatConfig', FLAT_DOCSTRING, 'name', '',
                    f'{ABOUT_NAME}\n{TEXT_KIND}', 'answer', '', WHOLE_KIND,
                    UNKNOWN_VERDICT, NO_FILE_TEXT, *BUTTON_TEXTS]
"""Widget texts of a model whose text member the application describes.

The description is below the member it belongs to, with what the type of that
member says under it. An application that describes half of its configuration
gets half of it explained, and the other half still says what kind of value it
holds, because that is the editor's own to say.
"""

HIDDEN_LABELS = ['FlatConfig', FLAT_SUMMARY, 'name', '', 'answer', '',
                 UNKNOWN_VERDICT, NO_FILE_TEXT, *BUTTON_TEXTS]
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

STUB_CANVAS_ITEM = 7
"""Identifier that the stub gives the one item it is asked to create."""


class FakeWidget:
    """Recording stand-in for a Tkinter widget in the stubbed tests."""

    created: ClassVar[list['FakeWidget']] = []
    """Every stub widget created since the list was last cleared."""

    def __init__(self, parent: object = None, **options: object) -> None:
        """Record this widget together with its parent and its options."""
        self.parent = parent
        self.options = options
        self.bindings: dict[str, Callable[..., object]] = {}
        self.packed = False
        self.packing: dict[str, object] = {}
        self.scrolled = 0
        FakeWidget.created.append(self)

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

    def winfo_reqheight(self) -> int:
        """Return a height, standing in for one that Tk would have laid out."""
        return STUB_BODY_HEIGHT

    def winfo_reqwidth(self) -> int:
        """Return a width, standing in for one that Tk would have laid out."""
        return STUB_BODY_WIDTH

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

    def yview(self, *arguments: str) -> None:
        """Scroll this canvas, as its scrollbar asks it to."""
        _ = arguments

    def yview_scroll(self, number: int, what: str) -> None:
        """Record how far the wheel scrolled this canvas."""
        assert what == 'units'
        self.scrolled += number

    def set(self, *fractions: str) -> None:
        """Show how much of the contents is visible, as a scrollbar does."""
        _ = fractions

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
    """Return every real Tk edit field below one widget, in row order."""
    fields: list[tkinter.Entry] = []
    for child in widget.winfo_children():
        if isinstance(child, tkinter.Entry):
            fields.append(child)
        fields.extend(real_fields(child))
    return fields


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


def stub_window() -> FakeWidget:
    """Return the stub widget that the bindings of the editor are made on."""
    return FakeWidget.created[0]


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
