#! /usr/bin/env python3
"""Tests for the part of a window that the keys of one editor reach.

The bind tag is the whole of it: a name in the Tcl interpreter, put on the
widgets of one editor and on no others. Nothing here knows what an edit model
is, so these tests are about the tag, about the two things Tk refuses, and
about what is left in the interpreter once an editor has closed.

Real Tk is what they run on, because what is being tested is what Tk accepts
and what it refuses, and a stub that answered those would be answering the
question itself.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import tkinter
import pytest
from edit_cfg_json_tk.tk_scope import KeyScope, TAG_PREFIX

BAD_SEQUENCE = '<Nonsense>'
"""An event sequence that Tk cannot parse at all.

An application names the key combinations of the editor, so a combination that
Tk refuses is something an application can ask for, and an editor that did not
open because of one would be the wrong answer to it.
"""

REAL_SEQUENCE = '<Control-y>'
"""An event sequence that Tk accepts, for telling the two apart."""


def _bound(scope: KeyScope) -> None:
    """Bind one sequence that Tk accepts, so the scope holds something."""
    scope.bind_event(REAL_SEQUENCE, lambda *event: 'break')


def test_tag_is_its_own(root_or_skip: tkinter.Tk) -> None:
    """Test each scope has a bind tag of its own, named after this editor.

    A bind tag is a name in the interpreter and not an object, so two editors
    in one process would share every binding of a tag they shared.
    """
    first = KeyScope(root_or_skip)
    second = KeyScope(root_or_skip)
    assert first.tag.startswith(TAG_PREFIX)
    assert first.tag != second.tag


def test_tag_reaches_inside(root_or_skip: tkinter.Tk) -> None:
    """Test the tag is put on the widget of the editor and on its children."""
    area = tkinter.Frame(root_or_skip)
    inside = tkinter.Label(area, text='inside')
    scope = KeyScope(area)
    scope.reach()
    assert scope.tag in area.bindtags()
    assert scope.tag in inside.bindtags()
    assert scope.tag not in root_or_skip.bindtags()


@pytest.mark.parametrize('priority, first', [(True, True), (False, False)])
def test_tag_place_chosen(root_or_skip: tkinter.Tk, priority: bool,
                          first: bool) -> None:
    """Test where in the list of tags this editor's own tag is put.

    An event walks the tags of a widget in order, so the place of the tag is
    what decides whether the editor or the widget that has the focus is
    offered a key first.

    Args:
        root_or_skip: A withdrawn Tk root, or a skip where there is no display.
        priority: Whether the editor is offered a key first.
        first: Whether the tag is then the first of the widget's tags.
    """
    area = tkinter.Frame(root_or_skip)
    scope = KeyScope(area, priority=priority)
    scope.reach()
    assert (area.bindtags()[0] == scope.tag) is first


def test_refused_sequence(root_or_skip: tkinter.Tk) -> None:
    """Test a sequence Tk cannot parse costs that binding and nothing else.

    Every action of this backend has a button as well, so an action left
    without a key is an action that can still be reached. An editor that did
    not open at all could not be.
    """
    scope = KeyScope(root_or_skip)
    scope.bind_event(BAD_SEQUENCE, lambda *event: 'break')
    _bound(scope)
    bound = root_or_skip.bind_class(scope.tag)
    assert len(bound) == 1
    assert BAD_SEQUENCE not in bound


def test_refused_combination(root_or_skip: tkinter.Tk) -> None:
    """Test a key combination the translation does not know binds nothing."""
    scope = KeyScope(root_or_skip)
    scope.bind_key('not a key at all', lambda: None)
    scope.release()
    assert not root_or_skip.bind_class(scope.tag)


def test_release_unbinds(root_or_skip: tkinter.Tk) -> None:
    """Test closing an editor takes its bindings out of the interpreter.

    A bind tag outlives the widgets that carried it, so an editor that was
    closed would otherwise leave its callbacks — and the model they hold —
    behind for as long as the application runs.
    """
    scope = KeyScope(root_or_skip)
    _bound(scope)
    assert root_or_skip.bind_class(scope.tag)
    scope.release()
    assert not root_or_skip.bind_class(scope.tag)


def test_release_when_gone(closing_root: tkinter.Tk) -> None:
    """Test releasing the bindings of a window that has gone is no failure.

    The window taking its interpreter with it is what an application closing
    does, and the bindings of that interpreter go with it. There is then
    nothing left to unbind and nothing to report.
    """
    scope = KeyScope(closing_root)
    _bound(scope)
    closing_root.destroy()
    scope.release()
    with pytest.raises(tkinter.TclError):
        closing_root.bind_class(scope.tag)
