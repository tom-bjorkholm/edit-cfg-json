#! /usr/bin/env python3
"""Tests for what the Tkinter backend makes of a nested configuration object.

The stubbed and the real Tk way of asking the same question are side by side
here as everywhere else in this backend, because the two fail in opposite
directions: a stub drifts from what Tk really does, and real Tk hides a wrong
value behind a widget default.

The configuration class comes from the example rather than from one of its
own, so that the same nesting is used by the core tests, by both backends and
by the example itself.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from typing import Optional
import tkinter
from edit_cfg_json import EditModel
from edit_cfg_json_tk.tk_editor import EditorWidgets, FOLD_SHUT_TEXT
from example.e09_nested_config import CourseExportConfig, TableOutputConfig
from .helpers import FakeVar, real_fields, real_fold, real_texts, \
    stub_editor, stub_fold, stub_texts

OUTPUT_CLASS = TableOutputConfig.__name__
"""What the row of a nested object of the example says instead of a value."""

MISSING_OUTPUT = f'no {OUTPUT_CLASS}'
"""What the row of the optional member that holds no object says."""

INSIDE_MEMBER = 'file_name'
"""A member that only exists inside a nested object of the example."""

OUTPUT_SUMMARY = EditModel(TableOutputConfig()).summary
"""The one line of the nested class that a folded object shows."""

OUTPUT_DETAIL = 'Nothing about this class says'
"""The beginning of the part that only an open object shows."""

OWN_VALID = ' [valid on its own]'
"""What an object that is a configuration on its own says.

It is written out here rather than read from an internal module of the core,
in the same way as every other text these tests expect.
"""

OWN_REFUSED = ' [refused on its own]'
"""What an object that its own class refuses says instead."""

REFUSED_FORMAT = ('participant_output', 'output_format')
"""A member inside a nested object, to be given a value its class refuses."""


def _nested_model(validated: bool = False) -> EditModel:
    """Return a model of the example with the nested objects.

    Args:
        validated: Whether the buffer has been validated already, which is
            what gives every nested object something to say about itself
            before anything has been folded.

    Returns:
        A model of the example configuration.
    """
    model = EditModel(CourseExportConfig())
    if validated:
        model.validate()
    return model


def _refused_model() -> EditModel:
    """Return a model whose nested object holds a value its class refuses."""
    model = EditModel(CourseExportConfig())
    model.set_text(path=REFUSED_FORMAT, text='xml')
    return model


def _nested_stub(model: Optional[EditModel] = None) -> EditorWidgets:
    """Build the stubbed widgets of the example with the nested objects."""
    return stub_editor(model if model is not None else _nested_model())


def _nested_real(parent: tkinter.Misc,
                 model: Optional[EditModel] = None) -> EditorWidgets:
    """Build the real widgets of the example with the nested objects."""
    return EditorWidgets(parent=parent,
                         model=model if model is not None else _nested_model())


def test_stub_shows_the_class(stub_tk: None) -> None:
    """Test the row of a nested object says its class and holds its members."""
    _ = stub_tk
    _nested_stub()
    shown = stub_texts(packed_only=True)
    assert OUTPUT_CLASS in shown
    assert INSIDE_MEMBER in shown
    assert MISSING_OUTPUT in shown


def test_real_shows_the_class(root_or_skip: tkinter.Tk) -> None:
    """Test real Tk shows exactly what the stubbed test expects."""
    _nested_real(root_or_skip)
    shown = real_texts(root_or_skip, packed_only=True)
    assert OUTPUT_CLASS in shown
    assert INSIDE_MEMBER in shown
    assert MISSING_OUTPUT in shown


def test_stub_object_no_field(stub_tk: None) -> None:
    """Test a nested object gets no field, because it holds no value.

    The example has two of them and one holds no object at all, and neither
    is edited in a field: what is edited is the members below them. So there
    is one field for the plain member of the configuration and one for each
    of the three members of the object that is there.
    """
    _ = stub_tk
    _nested_stub()
    assert len(FakeVar.created) == 4
    assert stub_texts(packed_only=True).count(OUTPUT_CLASS) == 1


def test_real_object_no_field(root_or_skip: tkinter.Tk) -> None:
    """Test real Tk creates a field for every value and for nothing else."""
    _nested_real(root_or_skip)
    # Three members of the one nested object that is there, and the plain
    # member of the configuration itself.
    assert len(real_fields(root_or_skip)) == 4


def test_stub_folds_an_object(stub_tk: None) -> None:
    """Test the control of a nested object hides the rows of its members."""
    _ = stub_tk
    _nested_stub()
    assert INSIDE_MEMBER in stub_texts(packed_only=True)
    stub_fold()
    shown = stub_texts(packed_only=True)
    assert OUTPUT_CLASS in shown
    assert INSIDE_MEMBER not in shown


def test_stub_says_less(stub_tk: None) -> None:
    """Test folding a nested object leaves the summary of its class.

    An object that is showing less of itself says less about itself, and the
    text below it has to be shown again when it is folded or nothing would
    say so.
    """
    _ = stub_tk
    _nested_stub()
    assert any(OUTPUT_DETAIL in text for text in stub_texts(packed_only=True))
    stub_fold()
    shown = stub_texts(packed_only=True)
    assert OUTPUT_SUMMARY in shown
    assert not any(OUTPUT_DETAIL in text for text in shown)


def test_stub_opens_again(stub_tk: None) -> None:
    """Test opening it again brings back the members and the whole text.

    The model is validated first, so that every nested object already says
    what it is on its own: folding one asks it that question again, and a
    round trip that started before it had ever been asked would differ by
    that one text and by nothing else.
    """
    _ = stub_tk
    _nested_stub(_nested_model(validated=True))
    before = stub_texts(packed_only=True)
    stub_fold()
    stub_fold(FOLD_SHUT_TEXT)
    assert stub_texts(packed_only=True) == before


def test_real_folds_an_object(root_or_skip: tkinter.Tk) -> None:
    """Test real Tk folds a nested object away and opens it again."""
    _nested_real(root_or_skip, _nested_model(validated=True))
    before = real_texts(root_or_skip, packed_only=True)
    real_fold(root_or_skip)
    folded = real_texts(root_or_skip, packed_only=True)
    assert INSIDE_MEMBER not in folded
    assert OUTPUT_SUMMARY in folded
    real_fold(root_or_skip, FOLD_SHUT_TEXT)
    assert real_texts(root_or_skip, packed_only=True) == before


def test_stub_badge_on_fold(stub_tk: None) -> None:
    """Test folding a nested object says what that object is on its own.

    Nothing has been validated when the editor opens, so the object has not
    been asked and says nothing. Folding it is one of the moments the model
    asks, which is the cheap local question that needs no whole configuration.
    """
    _ = stub_tk
    _nested_stub()
    assert OWN_VALID not in stub_texts(packed_only=True)
    stub_fold()
    assert OWN_VALID in stub_texts(packed_only=True)


def test_real_badge_on_fold(root_or_skip: tkinter.Tk) -> None:
    """Test real Tk shows exactly what the stubbed test expects."""
    _nested_real(root_or_skip)
    assert OWN_VALID not in real_texts(root_or_skip, packed_only=True)
    real_fold(root_or_skip)
    assert OWN_VALID in real_texts(root_or_skip, packed_only=True)


def test_stub_badge_refused(stub_tk: None) -> None:
    """Test an object its own class refuses says so where it is folded."""
    _ = stub_tk
    _nested_stub(_refused_model())
    stub_fold()
    shown = stub_texts(packed_only=True)
    assert OWN_REFUSED in shown
    assert OWN_VALID not in shown


def test_real_badge_refused(root_or_skip: tkinter.Tk) -> None:
    """Test real Tk shows exactly what the stubbed test expects."""
    _nested_real(root_or_skip, _refused_model())
    real_fold(root_or_skip)
    shown = real_texts(root_or_skip, packed_only=True)
    assert OWN_REFUSED in shown
    assert OWN_VALID not in shown


def test_stub_only_objects(stub_tk: None) -> None:
    """Test only the member that holds an object says what it is on its own.

    The example declares two nested members and one of them holds no object,
    so there is nothing there to ask and nothing said about it. A validated
    model is what makes that visible: every object that is there has been
    asked by then.
    """
    _ = stub_tk
    _nested_stub(_nested_model(validated=True))
    shown = stub_texts(packed_only=True)
    assert shown.count(OWN_VALID) == 1
    assert MISSING_OUTPUT in shown
