#! /usr/bin/env python3
"""Tests for what the Tkinter editor says is wrong with one member.

There are two ways for a member to be told that something is wrong with it,
and they are tested separately here because they are separate: leaving its
field asks whether its text means a value of it at all, and a validation pass
asks what the whole application makes of the buffer. Both end up below the
same member and both are read from the core, which is what stops the two
backends from disagreeing about either of them.

Leaving a field is the one thing here that a withdrawn window cannot show. Tk
delivers a focus event to a window that is on the screen and to no other, and
`event_generate` does not stand in for one: a withdrawn window swallows it,
which was worth finding out rather than assuming. So the stubbed test runs
what the field is bound to, and the real one moves the focus of a window that
is really shown, which is the third category of design section 10.2 —
deselected by the build and run by hand with `pytest -m focus_sensitive`.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import tkinter
import pytest
from edit_cfg_json import EditModel, Emphasis
from edit_cfg_json_tk.tk_editor import EMPHASIS_COLOURS, EditorWidgets, \
    EXPLAIN_TEXT, VALIDATE_TEXT
from example.e02_enum_config import EnumConfig
from example.e04_validated_config import DESCRIPTIONS, ValidatedConfig
from .helpers import FakeVar, FakeWidget, real_fields, real_press, \
    real_texts, retype, stub_editor, stub_press, stub_texts

NO_MEMBER = 'MIDDLE is not one of: MECHANICAL, ELECTRICAL, ELECTRONIC'
"""What the converter of the example says about a name no member has."""

TOO_MANY = ('Invalid configuration: Value 9 for retries is greater than '
            'maximum 5.')
"""What the example says about a number that is above its limit."""

SPACED_NAME = 'Invalid configuration: job_name may not contain a space.'
"""What the validator of the example writes about a name with a space."""

ABOUT_RETRIES = ('How many further attempts one failed run gets. From 0 to 5.'
                 '\nA whole number.')
"""What is said about the member whose limit these tests break.

The example says the first line of it and the type of the member says the
second, which is what the editor knows about every member without being told.
The two are one widget, because they are one thing: what this member is.
"""


def _described() -> EditModel:
    """Return a model of the example with its descriptions on it."""
    return EditModel(ValidatedConfig(), descriptions=DESCRIPTIONS)


def test_stub_leaving(stub_tk: None) -> None:
    """Test leaving a field says the text names no member of the enum."""
    _ = stub_tk
    widgets = stub_editor(EditModel(EnumConfig()))
    FakeVar.created[0].set('MIDDLE')
    assert widgets.wrong_shown[0] == ''
    _left_stub_field(0)
    assert widgets.wrong_shown[0] == NO_MEMBER


def test_stub_leaving_accepts(stub_tk: None) -> None:
    """Test leaving a field whose text names a member says nothing."""
    _ = stub_tk
    widgets = stub_editor(EditModel(EnumConfig()))
    FakeVar.created[0].set('MECH')
    _left_stub_field(0)
    assert widgets.wrong_shown[0] == ''


def test_stub_typing_clears(stub_tk: None) -> None:
    """Test typing on in that field takes the message away again.

    Every name of an enum is text that names no member for as long as it is
    half typed, so the answer about the text before this key says nothing
    true about the text there is now.
    """
    _ = stub_tk
    widgets = stub_editor(EditModel(EnumConfig()))
    FakeVar.created[0].set('MIDDLE')
    _left_stub_field(0)
    FakeVar.created[0].set('MECHANICAL')
    assert widgets.wrong_shown[0] == ''


@pytest.mark.focus_sensitive
def test_real_leaving_field() -> None:
    """Test a real field that loses the focus reports the same thing.

    This is the one test of this backend that needs a window a person can
    see: Tk delivers a focus event to a window that is on the screen and to
    no other, so a withdrawn window can neither be given the focus nor be
    told that it has lost it.
    """
    window = tkinter.Tk()
    try:
        widgets = EditorWidgets(parent=window, model=EditModel(EnumConfig()))
        window.update()
        fields = real_fields(window)
        fields[0].focus_force()
        window.update()
        retype(fields[0], 'MIDDLE')
        fields[1].focus_force()
        window.update()
        assert widgets.wrong_shown[0] == NO_MEMBER
        assert NO_MEMBER in real_texts(window, packed_only=True)
    finally:
        window.destroy()


def _left_stub_field(index: int) -> None:
    """Run what one stubbed field does when it loses the focus."""
    fields = [widget for widget in FakeWidget.created
              if 'textvariable' in widget.options]
    fields[index].bindings['<FocusOut>']()


def test_stub_every_bad(stub_tk: None) -> None:
    """Test a validation pass marks every member that was refused.

    `Config.validate()` stops at the first step that refuses, so a user who
    saw only that one would correct one member per press of the button.
    """
    _ = stub_tk
    widgets = stub_editor(EditModel(ValidatedConfig()))
    FakeVar.created[0].set('a b')
    FakeVar.created[1].set('9')
    stub_press(VALIDATE_TEXT)
    assert widgets.wrong_shown == [SPACED_NAME, TOO_MANY, '']


def test_real_every_bad(root_or_skip: tkinter.Tk) -> None:
    """Test the real editor marks exactly the same members."""
    widgets = EditorWidgets(parent=root_or_skip,
                            model=EditModel(ValidatedConfig()))
    retype(real_fields(root_or_skip)[0], 'a b')
    retype(real_fields(root_or_skip)[1], '9')
    real_press(root_or_skip, VALIDATE_TEXT)
    assert widgets.wrong_shown == [SPACED_NAME, TOO_MANY, '']


def test_stub_whole_rule(stub_tk: None) -> None:
    """Test a rule about no single member stays with the verdict.

    Neither number is wrong on its own, so there is no member this could
    honestly be put beside.
    """
    _ = stub_tk
    widgets = stub_editor(EditModel(ValidatedConfig()))
    FakeVar.created[1].set('5')
    FakeVar.created[2].set('400')
    stub_press(VALIDATE_TEXT)
    assert widgets.wrong_shown == ['', '', '']
    assert 'longest run' in widgets.verdict_text_shown


def test_stub_wrong_colour(stub_tk: None) -> None:
    """Test what is wrong is not shown in the colour of an explanation.

    They sit one below the other under the same member, so the one that has
    to be acted on has to be told from the one that only explains.
    """
    _ = stub_tk
    stub_editor(EditModel(ValidatedConfig()))
    FakeVar.created[1].set('9')
    stub_press(VALIDATE_TEXT)
    wrong = [widget for widget in FakeWidget.created
             if widget.options.get('text') == TOO_MANY]
    assert len(wrong) == 1
    assert wrong[0].options['foreground'] == EMPHASIS_COLOURS[Emphasis.BAD]


def test_stub_wrong_stays(stub_tk: None) -> None:
    """Test hiding the explanations leaves what is wrong on the window.

    A description is what a user who knows the configuration wants out of the
    way; a refusal is the one thing that has to be read.
    """
    _ = stub_tk
    stub_editor(_described())
    FakeVar.created[1].set('9')
    stub_press(VALIDATE_TEXT)
    assert ABOUT_RETRIES in stub_texts(packed_only=True)
    stub_press(EXPLAIN_TEXT)
    shown = stub_texts(packed_only=True)
    assert TOO_MANY in shown
    assert ABOUT_RETRIES not in shown


def test_real_wrong_stays(root_or_skip: tkinter.Tk) -> None:
    """Test the real window keeps it in the same way and in the same order."""
    EditorWidgets(parent=root_or_skip, model=_described())
    retype(real_fields(root_or_skip)[1], '9')
    real_press(root_or_skip, VALIDATE_TEXT)
    shown = real_texts(root_or_skip, packed_only=True)
    assert shown.index(ABOUT_RETRIES) == shown.index('retries') + 2
    assert shown.index(TOO_MANY) == shown.index('retries') + 3
    real_press(root_or_skip, EXPLAIN_TEXT)
    shown = real_texts(root_or_skip, packed_only=True)
    assert shown.index(TOO_MANY) == shown.index('retries') + 2
    assert ABOUT_RETRIES not in shown
