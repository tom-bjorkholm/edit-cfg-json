#! /usr/bin/env python3
"""Tests for the column of the names in the Tkinter backend.

Every row says its name in a label as wide as the longest name of the editor,
measured in the font it is written in, and never wider than the column always
was. How wide that is, is the core's; what is tested here is that this backend
gives every label that width, and that real Tk then lays the column out with
no space to spare.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import tkinter
from edit_cfg_json import EditModel
from edit_cfg_json_tk.tk_editor import EditorWidgets
from edit_cfg_json_tk.tk_look import BLANK_WIDTH, NAME_COLUMN_WIDTH, row_font
from example.e20_union_types import ExportConfig
from .helpers import OneMemberConfig, real_names, stub_editor, stub_names

LONG_KEY = 'a key of the data that is far longer than the column of the names'
"""A name that the column cannot show the whole of."""


class LongKeyConfig(OneMemberConfig):
    """A configuration whose one dict has a key longer than the column."""

    def declare_members(self) -> None:
        """Assign the dict and its one long key."""
        self.hosts: dict[str, int] = {LONG_KEY: 1}


def test_stub_names_fitted(stub_tk: None) -> None:
    """Test every name is as wide as the longest, measured in its font.

    The stub measures a text one pixel per character, and the blank image
    beside the name is what makes the width one in pixels.
    """
    _ = stub_tk
    model = EditModel(ExportConfig())
    stub_editor(model)
    found = stub_names()
    assert [widget.options['text'] for widget in found] == [
        row.name for row in model.rows]
    assert {widget.options['width'] for widget in found} == {
        len('jira_column_map') + BLANK_WIDTH}


def test_real_names_fitted(root_or_skip: tkinter.Tk) -> None:
    """Test real Tk gives every name one width, with no space to spare.

    The label of the longest name is exactly as wide as Tk makes it on its
    own, which is what width 0 asks for. The width the column had in
    characters was counted in widths of `0`, and left half of it empty.
    """
    EditorWidgets(parent=root_or_skip, model=EditModel(ExportConfig()))
    found = real_names(root_or_skip)
    given = {widget.winfo_reqwidth() for widget in found}
    for widget in found:
        widget.config(width=0)
    natural = [widget.winfo_reqwidth() for widget in found]
    assert given == {max(natural)}


def test_real_long_name_cut(root_or_skip: tkinter.Tk) -> None:
    """Test a name longer than the column is given the column and no more.

    The column is never wider than `NAME_COLUMN_WIDTH` widths of `0`, which
    is what it always was, so one long key of the data does not push the
    values of every row to the right.
    """
    EditorWidgets(parent=root_or_skip, model=EditModel(LongKeyConfig()))
    font = row_font(root_or_skip)
    most = font.measure('0' * NAME_COLUMN_WIDTH)
    assert font.measure(LONG_KEY) > most
    assert {int(widget.cget('width'))
            for widget in real_names(root_or_skip)} == {most + BLANK_WIDTH}
