#! /usr/bin/env python3
"""Tests for the editor mounted in a window that an application owns.

What these are about is what makes an embedded editor different from one that
owns its window: it reads the configuration itself, it builds either a window
of its own or the area it was given, it destroys only what it built, and its
keys and its mouse wheel reach only that. Everything else about the editor is
the same editor and is tested where it always was.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from typing import Optional, cast
import tkinter
import pytest
from edit_cfg_json import Settings
from edit_cfg_json_tk import TkEditorPanel
from edit_cfg_json_tk.tk_scope import TAG_PREFIX
from example.e01_flat_config import FlatConfig
from .helpers import FakeVar, FakeWidget, answer_question, real_fields, \
    real_press, retype, stub_keys, stub_press, stub_tags
from .test_tk_keys import real_keys

CLOSE_TEXT = 'Close'
"""Text of the button of the editor that ends the session.

It is written out here rather than imported, because what this module is
about is the panel and pressing that button is how a user reaches it.
"""


def _stub_panel(settings: Optional[Settings] = None,
                modal: bool = False) -> tuple[TkEditorPanel, FakeWidget]:
    """Return a stubbed panel and the widget the application gave it.

    Args:
        settings: What the application decided, or None for no opinion.
        modal: Whether the editor grabs the application for the session.

    Returns:
        The panel, and the stub widget standing in for the area of the
        application's window that the editor was mounted in.
    """
    area = FakeWidget()
    panel = TkEditorPanel(FlatConfig(), area=cast(tkinter.Misc, area),
                          modal=modal, settings=settings or Settings())
    return panel, area


def test_stub_builds_its_own(stub_tk: None) -> None:
    """Test the editor builds inside a frame of its own and not in the area.

    That one frame is what makes both rules of an embedded editor true: it is
    what closing destroys, and it is what the keys reach.
    """
    _ = stub_tk
    _, area = _stub_panel()
    assert len(area.winfo_children()) == 1


def test_stub_keys_scoped(stub_tk: None) -> None:
    """Test the keys reach what the editor built and not what it was given.

    An editor mounted in a window an application owns would otherwise claim
    the keys of that whole window, which is the one thing an application that
    has widgets of its own cannot have.
    """
    _ = stub_tk
    _, area = _stub_panel()
    frame = area.winfo_children()[0]
    assert stub_tags(frame)[0].startswith(TAG_PREFIX)
    assert not any(tag.startswith(TAG_PREFIX) for tag in stub_tags(area))


def test_stub_ordinary_keys(stub_tk: None) -> None:
    """Test an application can ask to be offered a key first.

    Tk offers the bind tags of a widget in the order they are in, so the
    editor going last is the editor being offered what is left of a key.
    """
    _ = stub_tk
    _, area = _stub_panel(settings=Settings(priority_keys=False))
    assert stub_tags(area.winfo_children()[0])[-1].startswith(TAG_PREFIX)


def test_stub_two_panels(stub_tk: None) -> None:
    """Test two editors in one process do not share their bindings.

    A bind tag is a name in the interpreter rather than a widget, so two
    editors sharing one name would each run the other's actions.
    """
    _ = stub_tk
    _, first = _stub_panel()
    _, second = _stub_panel()
    assert stub_tags(first.winfo_children()[0])[0] != \
        stub_tags(second.winfo_children()[0])[0]


def test_stub_click_focuses(stub_tk: None) -> None:
    """Test clicking the editor gives it the focus, so its keys work.

    A Tk frame does not take the focus of its own accord and a label never
    does, so a user who had not yet been in a field would press a key of the
    editor and see nothing happen.
    """
    _ = stub_tk
    _, area = _stub_panel()
    frame = area.winfo_children()[0]
    frame.bindings['<Button-1>']()
    assert FakeWidget.focused == [frame]


def test_stub_close_destroys(stub_tk: None) -> None:
    """Test closing destroys what the editor built and nothing else."""
    _ = stub_tk
    panel, area = _stub_panel()
    frame = area.winfo_children()[0]
    panel.close()
    assert frame not in FakeWidget.created
    assert area in FakeWidget.created


def test_stub_close_tells(stub_tk: None) -> None:
    """Test the application is told once the session has ended."""
    _ = stub_tk
    ended: list[str] = []
    TkEditorPanel(FlatConfig(), area=cast(tkinter.Misc, FakeWidget()),
                  modal=False, on_close=lambda: ended.append('gone'))
    stub_press(CLOSE_TEXT)
    assert ended == ['gone']


def test_stub_close_asks(stub_tk: None,
                         monkeypatch: pytest.MonkeyPatch) -> None:
    """Test the panel asks about what is unsaved, as the editor always did."""
    _ = stub_tk
    asked = answer_question(monkeypatch, answer=False)
    ended: list[str] = []
    panel = TkEditorPanel(FlatConfig(), modal=False,
                          area=cast(tkinter.Misc, FakeWidget()),
                          on_close=lambda: ended.append('gone'))
    FakeVar.created[1].set('7')
    panel.close()
    assert len(asked) == 1
    assert not ended


def test_stub_close_not_asked(stub_tk: None,
                              monkeypatch: pytest.MonkeyPatch) -> None:
    """Test the application can close the editor without a question.

    An application that is shutting down for reasons of its own already has a
    question to put to the user, and a library that put a second one there
    would be deciding something that is the application's.
    """
    _ = stub_tk
    asked = answer_question(monkeypatch, answer=False)
    ended: list[str] = []
    panel = TkEditorPanel(FlatConfig(), modal=False,
                          area=cast(tkinter.Misc, FakeWidget()),
                          on_close=lambda: ended.append('gone'))
    FakeVar.created[1].set('7')
    panel.close(ask_about_unsaved=False)
    assert not asked
    assert ended == ['gone']


def test_stub_close_twice(stub_tk: None) -> None:
    """Test closing an editor that has ended does nothing at all."""
    _ = stub_tk
    ended: list[str] = []
    panel = TkEditorPanel(FlatConfig(), modal=False,
                          area=cast(tkinter.Misc, FakeWidget()),
                          on_close=lambda: ended.append('gone'))
    panel.close()
    panel.close()
    assert ended == ['gone']


def test_stub_keys_released(stub_tk: None) -> None:
    """Test a closed editor leaves no binding of its own behind.

    A bind tag outlives the widgets that carried it, so the callbacks — and
    the model they hold — would otherwise stay for as long as the application
    runs.
    """
    _ = stub_tk
    panel, _ = _stub_panel()
    assert stub_keys()
    panel.close()
    assert not stub_keys()


def test_stub_builds_model(stub_tk: None) -> None:
    """Test the editor builds the model of the configuration it was given.

    An application says what to edit in the same call that says where the
    editor goes, and reads the outcome off the panel afterwards.
    """
    _ = stub_tk
    panel, _ = _stub_panel()
    assert panel.model.config_type_name == 'FlatConfig'
    assert panel.saved_config is None


def test_stub_area_modal(stub_tk: None) -> None:
    """Test a modal editor in an area takes the events for that area.

    An application that wants its own widgets answering beside the editor
    passes modal=False, which is what every other test here does.
    """
    _ = stub_tk
    _, area = _stub_panel(modal=True)
    assert area.winfo_children()[0].grabbed


def _refuse_grab(monkeypatch: pytest.MonkeyPatch) -> None:
    """Make every stub widget refuse the grab, as Tk does on some platforms.

    Tk refuses to grab for a window that is not on the screen yet, and whether
    a window that has just been created counts as one differs between
    platforms. The stub is the test's own stand-in for Tk, so it is where that
    answer is given here.

    Args:
        monkeypatch: The pytest fixture that replaces the method.
    """
    def refused(_: FakeWidget) -> None:
        """Refuse the grab exactly as Tk refuses one."""
        raise tkinter.TclError('grab failed: window not viewable')
    monkeypatch.setattr(FakeWidget, 'grab_set', refused)


def test_stub_grab_refused(stub_tk: None,
                           monkeypatch: pytest.MonkeyPatch) -> None:
    """Test an editor whose grab Tk refuses opens without one.

    An editor that opened without a grab is worth more than one that did not
    open, so the refusal costs it the grab and nothing else. Closing it must
    then not give back a grab it never took.
    """
    _ = stub_tk
    _refuse_grab(monkeypatch)
    panel, area = _stub_panel(modal=True)
    assert not area.winfo_children()[0].grabbed
    assert panel.model.config_type_name == 'FlatConfig'
    panel.close(ask_about_unsaved=False)
    assert not area.winfo_children()


def test_stub_own_window(stub_tk: None) -> None:
    """Test a parent gets the editor a window of its own, named and modal."""
    _ = stub_tk
    parent = FakeWidget()
    TkEditorPanel(FlatConfig(), parent=cast(tkinter.Misc, parent))
    window = parent.winfo_children()[0]
    assert window.window_title == 'FlatConfig'
    assert window.transient_to is parent
    assert window.grabbed


def test_stub_window_closed(stub_tk: None) -> None:
    """Test closing destroys the window the editor made and frees the grab."""
    _ = stub_tk
    ended: list[str] = []
    parent = FakeWidget()
    panel = TkEditorPanel(FlatConfig(), parent=cast(tkinter.Misc, parent),
                          on_close=lambda: ended.append('gone'))
    window = parent.winfo_children()[0]
    panel.close()
    assert not window.grabbed
    assert window not in FakeWidget.created
    assert parent in FakeWidget.created
    assert ended == ['gone']


def test_stub_window_button(stub_tk: None) -> None:
    """Test the close button of that window ends the session as Close does."""
    _ = stub_tk
    ended: list[str] = []
    parent = FakeWidget()
    TkEditorPanel(FlatConfig(), parent=cast(tkinter.Misc, parent),
                  on_close=lambda: ended.append('gone'))
    parent.winfo_children()[0].protocols['WM_DELETE_WINDOW']()
    assert ended == ['gone']


def test_stub_nowhere_refused(stub_tk: None) -> None:
    """Test the editor refuses to guess which window it belongs in.

    An application with no Tk of its own uses `edit_cfg_json_tk.edit`, which
    owns a window and runs until the user is done.
    """
    _ = stub_tk
    with pytest.raises(ValueError):
        TkEditorPanel(FlatConfig())


def test_stub_both_refused(stub_tk: None) -> None:
    """Test naming a parent and an area is two answers to one question."""
    _ = stub_tk
    with pytest.raises(ValueError):
        TkEditorPanel(FlatConfig(), parent=cast(tkinter.Misc, FakeWidget()),
                      area=cast(tkinter.Misc, FakeWidget()))


def test_real_panel_scoped(root_or_skip: tkinter.Tk) -> None:
    """Test real Tk gives the editor its tag and the application none.

    The stub cannot show this, because it does not know what tags a widget is
    born with; only real Tk does.
    """
    area = tkinter.Frame(root_or_skip)
    area.pack()
    TkEditorPanel(FlatConfig(), area=area, modal=False)
    frame = area.winfo_children()[0]
    assert frame.bindtags()[0].startswith(TAG_PREFIX)
    assert not any(tag.startswith(TAG_PREFIX)
                   for tag in root_or_skip.bindtags())
    assert real_keys(frame)


def test_real_field_reaches(root_or_skip: tkinter.Tk) -> None:
    """Test every field the editor built is reached by its keys as well.

    A key is offered the tags of the widget that has the focus, and the focus
    is normally in a field, so a field without the tag would be a key that
    did nothing wherever the user was working.
    """
    area = tkinter.Frame(root_or_skip)
    area.pack()
    TkEditorPanel(FlatConfig(), area=area, modal=False)
    tag = area.winfo_children()[0].bindtags()[0]
    assert all(tag in field.bindtags() for field in real_fields(area))


def test_real_close_keeps(root_or_skip: tkinter.Tk) -> None:
    """Test closing leaves the widget the application named as it was."""
    area = tkinter.Frame(root_or_skip)
    area.pack()
    ended: list[str] = []
    panel = TkEditorPanel(FlatConfig(), area=area, modal=False,
                          on_close=lambda: ended.append('gone'))
    frame = area.winfo_children()[0]
    panel.close()
    assert not frame.winfo_exists()
    assert area.winfo_exists()
    assert ended == ['gone']


def test_real_close_asks(root_or_skip: tkinter.Tk,
                         monkeypatch: pytest.MonkeyPatch) -> None:
    """Test the editor's own Close asks and keeps the editor on refusal."""
    asked = answer_question(monkeypatch, answer=False)
    area = tkinter.Frame(root_or_skip)
    area.pack()
    TkEditorPanel(FlatConfig(), area=area, modal=False)
    frame = area.winfo_children()[0]
    retype(real_fields(area)[1], '7')
    real_press(area, CLOSE_TEXT)
    assert len(asked) == 1
    assert frame.winfo_exists()


def test_real_own_window(root_or_skip: tkinter.Tk) -> None:
    """Test a real window of the editor's own is created and destroyed.

    It is asked for without the grab, and the window is taken off the screen
    as soon as it is there: a test that really grabbed would hold the pointer
    and the keyboard of the machine it runs on, and a window of its own is
    the one part of this editor that a test cannot keep withdrawn from the
    start. That the editor asks for the grab is tested with the stub above.
    """
    ended: list[str] = []
    panel = TkEditorPanel(FlatConfig(), parent=root_or_skip, modal=False,
                          on_close=lambda: ended.append('gone'))
    window = root_or_skip.winfo_children()[0]
    assert isinstance(window, tkinter.Toplevel)
    window.withdraw()
    assert window.title() == 'FlatConfig'
    panel.close()
    assert not window.winfo_exists()
    assert ended == ['gone']
