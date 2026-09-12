#! /usr/bin/env python3
"""What the tests of the Tkinter backend share.

The ways of reading a stubbed editor and a real Tk window, and the widget
texts that both of them expect, live here, so that the test modules of this
backend test the same editor and cannot drift apart about what it looks like.
The stubbed and the real way of doing one thing are side by side on purpose: a
stub can drift from what Tk really does, and real Tk can hide a wrong value
behind a widget default, so a difference between the two is itself a finding.

The stand-ins themselves are in `stubs`, and they are named here as well so
that a test module has one place to import from.

The configuration class comes from the example rather than from a class of its
own, so that the same flat configuration is used by the core tests, by both
backends and by the example itself.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from collections.abc import Callable
from pathlib import Path
from typing import cast
import json
import tkinter
from tkinter import messagebox
import pytest
from edit_cfg_json import Descriptions, EditModel, LoadReport
from edit_cfg_json_tk.tk_editor import CHOOSE_TEXT, CLOSE_TEXT, \
    EditorWidgets, EXPLAIN_TEXT, FOLD_OPEN_TEXT, SAVE_AS_TEXT, SAVE_TEXT, \
    VALIDATE_TEXT
from edit_cfg_json_tk.tk_find import FIND_FIELD_NAME, FIND_LABEL_TEXT, \
    FIND_NEXT_TEXT, FIND_TICK_LABELS
from edit_cfg_json_tk.tk_look import MEMBER_CHOICE_NAME, MEMBER_FIELD_NAME
from example.e01_flat_config import FlatConfig
from .stubs import FakeFlag, FakeVar, FakeWidget, PROBE_TAG, TOUCHPAD

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
                CHOOSE_TEXT, CLOSE_TEXT]
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


def real_choosers(widget: tkinter.Misc) -> list[tkinter.Menubutton]:
    """Return every real Tk pull-down of a member, in row order.

    A member has one where the editor knows the whole set of values it takes,
    and it is told from every other menu button by its Tk name.
    """
    return [found for found in _all_below(widget)
            if isinstance(found, tkinter.Menubutton)
            and found.winfo_name() == MEMBER_CHOICE_NAME]


def real_ways(widget: tkinter.Misc) -> list[str]:
    """Return the Tk name of each way of editing a value that is shown.

    Exactly one of the two ways a member has is on the window, so this is one
    name per member whose value is edited and it says which of the two it is.
    The window is laid out first, because a widget that has been packed is
    not mapped until Tk has got round to it.

    Args:
        widget: Widget the editor was built below.

    Returns:
        The name of the shown way of editing each value, in row order.
    """
    widget.update_idletasks()
    return [found.winfo_name() for found in _all_below(widget)
            if found.winfo_name() in (MEMBER_FIELD_NAME, MEMBER_CHOICE_NAME)
            and found.winfo_ismapped()]


def stub_ways() -> list[str]:
    """Return the same for the stubbed widgets, which are never laid out.

    Returns:
        The name of the shown way of editing each value, in row order.
    """
    return [str(widget.options.get('name')) for widget in FakeWidget.created
            if widget.options.get('name') in (MEMBER_FIELD_NAME,
                                              MEMBER_CHOICE_NAME)
            and widget.shown]


def _all_below(widget: tkinter.Misc) -> list[tkinter.Misc]:
    """Return every real Tk widget below one widget, in creation order."""
    found: list[tkinter.Misc] = []
    for child in widget.winfo_children():
        found.append(child)
        found.extend(_all_below(child))
    return found


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

    Two other stub widgets hold one of these variables: the field that a
    search is typed into, created after the rows, and the pull-down of a
    member whose values the editor knows the whole of, which shares the
    variable of the field of its own member. Both are told apart by the Tk
    name of the widget, and they are reached by `stub_find_var` and by
    `stub_choosers`.
    """
    return _named_fields(MEMBER_FIELD_NAME)[1]


def stub_field_widgets() -> list[FakeWidget]:
    """Return every stub field of a member, in row order.

    It is the widgets where `stub_fields` is the variables, and neither the
    field of the search nor the pull-down of a member is among them.
    """
    return _named_fields(MEMBER_FIELD_NAME)[0]


def stub_choosers() -> list[FakeWidget]:
    """Return every stub pull-down of a member, in row order.

    A member has one where the editor knows the whole set of values it takes,
    which is a member holding true or false and one holding an enum member.
    """
    return _named_fields(MEMBER_CHOICE_NAME)[0]


def stub_choices(widget: FakeWidget) -> tuple[str, ...]:
    """Return the values that one stub pull-down offers.

    A pull-down is a menu button with a menu on it, so the values are the
    entries of the menu that was created below it.

    Args:
        widget: Stub pull-down to read.

    Returns:
        Those values, in the order they are offered.
    """
    return tuple(label for label, _ in _stub_menu(widget).commands)


def stub_pick(widget: FakeWidget, value: str) -> None:
    """Choose one value from the menu of one stub pull-down.

    It runs what the entry of that value is bound to, which is what real Tk
    runs when the entry is chosen.

    Args:
        widget: Stub pull-down to choose in.
        value: Value to choose, which it has to offer.
    """
    chosen = [command for label, command in _stub_menu(widget).commands
              if label == value]
    assert len(chosen) == 1
    picked = chosen[0]
    assert picked is not None
    picked()


def _stub_menu(widget: FakeWidget) -> FakeWidget:
    """Return the menu that was created below one stub pull-down."""
    found = [child for child in FakeWidget.created if child.parent is widget]
    assert len(found) == 1
    return found[0]


def _named_fields(name: str) -> tuple[list[FakeWidget], list[FakeVar]]:
    """Return the stub widgets of one Tk name and their variables.

    Args:
        name: Tk name that says which kind of widget these are.

    Returns:
        Those widgets and their variables, both in creation order.
    """
    found = [(widget, variable) for widget, variable in _stub_fields()
             if widget.options.get('name') == name]
    return ([widget for widget, _ in found],
            [variable for _, variable in found])


def stub_find_var() -> FakeVar:
    """Return the variable of the stub field that a search is typed into."""
    found = _named_fields(FIND_FIELD_NAME)[1]
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


def told_replaced(monkeypatch: pytest.MonkeyPatch) -> list[str]:
    """Make the dialog that says what was replaced record what it said.

    It is the one dialog of this backend that asks nothing, so it has a
    stand-in of its own beside the one that answers a question.

    Args:
        monkeypatch: The pytest fixture that replaces the dialog.

    Returns:
        A list that gets what is said every time it is said.
    """
    said: list[str] = []

    def tell(**options: object) -> None:
        """Stand in for the system dialog that says one thing."""
        said.append(str(options['message']))
    monkeypatch.setattr(messagebox, 'showwarning', tell)
    return said


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


def touchpad_known(parent: tkinter.Misc) -> bool:
    """Return whether this Tk knows the event that a touchpad reports.

    It is asked by binding it and taking the binding away again, rather than
    by reading a version number, because what the editor needs to know is
    exactly whether this interpreter accepts the sequence. A tag of this
    question's own is used, so that nothing the editor bound is touched.

    Args:
        parent: Widget to reach the Tcl interpreter through.

    Returns:
        Whether the editor could bind the touchpad in this interpreter.
    """
    try:
        parent.bind_class(PROBE_TAG, TOUCHPAD, lambda *event: 'break')
    except tkinter.TclError:
        return False
    parent.unbind_class(PROBE_TAG, TOUCHPAD)
    return True


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
