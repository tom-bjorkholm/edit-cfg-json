#! /usr/bin/env python3
"""Tests for the editor mounted in a window that an application owns.

What these are about is the two rules that make an embedded editor different
from one that owns its window: it builds and destroys only its own widgets,
and its keys and its mouse wheel reach only what it built. Everything else
about the editor is the same editor and is tested where it always was.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from typing import cast
import tkinter
import pytest
from edit_cfg_json import EditModel, Settings
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


def _stub_panel(model: EditModel) -> tuple[TkEditorPanel, FakeWidget]:
    """Return a stubbed panel and the widget the application gave it.

    Args:
        model: Model for the panel to show.

    Returns:
        The panel, and the stub widget standing in for the area of the
        application's window that the editor was mounted in.
    """
    area = FakeWidget()
    panel = TkEditorPanel(parent=cast(tkinter.Misc, area), model=model)
    return panel, area


def test_stub_builds_its_own(stub_tk: None) -> None:
    """Test the editor builds inside a frame of its own and not in the area.

    That one frame is what makes both rules of an embedded editor true: it is
    what closing destroys, and it is what the keys reach.
    """
    _ = stub_tk
    _, area = _stub_panel(EditModel(FlatConfig()))
    assert len(area.winfo_children()) == 1


def test_stub_keys_scoped(stub_tk: None) -> None:
    """Test the keys reach what the editor built and not what it was given.

    An editor mounted in a window an application owns would otherwise claim
    the keys of that whole window, which is the one thing an application that
    has widgets of its own cannot have.
    """
    _ = stub_tk
    _, area = _stub_panel(EditModel(FlatConfig()))
    frame = area.winfo_children()[0]
    assert stub_tags(frame)[0].startswith(TAG_PREFIX)
    assert not any(tag.startswith(TAG_PREFIX) for tag in stub_tags(area))


def test_stub_ordinary_keys(stub_tk: None) -> None:
    """Test an application can ask to be offered a key first.

    Tk offers the bind tags of a widget in the order they are in, so the
    editor going last is the editor being offered what is left of a key.
    """
    _ = stub_tk
    _, area = _stub_panel(EditModel(FlatConfig(),
                                    settings=Settings(priority_keys=False)))
    assert stub_tags(area.winfo_children()[0])[-1].startswith(TAG_PREFIX)


def test_stub_two_panels(stub_tk: None) -> None:
    """Test two editors in one process do not share their bindings.

    A bind tag is a name in the interpreter rather than a widget, so two
    editors sharing one name would each run the other's actions.
    """
    _ = stub_tk
    _, first = _stub_panel(EditModel(FlatConfig()))
    _, second = _stub_panel(EditModel(FlatConfig()))
    assert stub_tags(first.winfo_children()[0])[0] != \
        stub_tags(second.winfo_children()[0])[0]


def test_stub_click_focuses(stub_tk: None) -> None:
    """Test clicking the editor gives it the focus, so its keys work.

    A Tk frame does not take the focus of its own accord and a label never
    does, so a user who had not yet been in a field would press a key of the
    editor and see nothing happen.
    """
    _ = stub_tk
    _, area = _stub_panel(EditModel(FlatConfig()))
    frame = area.winfo_children()[0]
    frame.bindings['<Button-1>']()
    assert FakeWidget.focused == [frame]


def test_stub_close_destroys(stub_tk: None) -> None:
    """Test closing destroys what the editor built and nothing else."""
    _ = stub_tk
    panel, area = _stub_panel(EditModel(FlatConfig()))
    frame = area.winfo_children()[0]
    panel.close()
    assert frame not in FakeWidget.created
    assert area in FakeWidget.created


def test_stub_close_tells(stub_tk: None) -> None:
    """Test the application is told once the session has ended."""
    _ = stub_tk
    ended: list[str] = []
    TkEditorPanel(parent=cast(tkinter.Misc, FakeWidget()),
                  model=EditModel(FlatConfig()),
                  on_close=lambda: ended.append('gone'))
    stub_press(CLOSE_TEXT)
    assert ended == ['gone']


def test_stub_close_asks(stub_tk: None,
                         monkeypatch: pytest.MonkeyPatch) -> None:
    """Test the panel asks about what is unsaved, as the editor always did."""
    _ = stub_tk
    asked = answer_question(monkeypatch, answer=False)
    ended: list[str] = []
    panel = TkEditorPanel(parent=cast(tkinter.Misc, FakeWidget()),
                          model=EditModel(FlatConfig()),
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
    panel = TkEditorPanel(parent=cast(tkinter.Misc, FakeWidget()),
                          model=EditModel(FlatConfig()),
                          on_close=lambda: ended.append('gone'))
    FakeVar.created[1].set('7')
    panel.close(ask_about_unsaved=False)
    assert not asked
    assert ended == ['gone']


def test_stub_close_twice(stub_tk: None) -> None:
    """Test closing an editor that has ended does nothing at all."""
    _ = stub_tk
    ended: list[str] = []
    panel = TkEditorPanel(parent=cast(tkinter.Misc, FakeWidget()),
                          model=EditModel(FlatConfig()),
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
    panel, _ = _stub_panel(EditModel(FlatConfig()))
    assert stub_keys()
    panel.close()
    assert not stub_keys()


def test_real_panel_scoped(root_or_skip: tkinter.Tk) -> None:
    """Test real Tk gives the editor its tag and the application none.

    The stub cannot show this, because it does not know what tags a widget is
    born with; only real Tk does.
    """
    area = tkinter.Frame(root_or_skip)
    area.pack()
    TkEditorPanel(parent=area, model=EditModel(FlatConfig()))
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
    TkEditorPanel(parent=area, model=EditModel(FlatConfig()))
    tag = area.winfo_children()[0].bindtags()[0]
    assert all(tag in field.bindtags() for field in real_fields(area))


def test_real_close_keeps(root_or_skip: tkinter.Tk) -> None:
    """Test closing leaves the widget the application named as it was."""
    area = tkinter.Frame(root_or_skip)
    area.pack()
    ended: list[str] = []
    panel = TkEditorPanel(parent=area, model=EditModel(FlatConfig()),
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
    TkEditorPanel(parent=area, model=EditModel(FlatConfig()))
    frame = area.winfo_children()[0]
    retype(real_fields(area)[1], '7')
    real_press(area, CLOSE_TEXT)
    assert len(asked) == 1
    assert frame.winfo_exists()
