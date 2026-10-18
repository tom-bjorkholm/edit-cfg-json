#! /usr/bin/env python3
"""Tests for the column of the names in the Textual backend.

Every row says its name in a label as wide as the longest name of the editor,
and never wider than the column always was. How wide that is, is the core's;
what is tested here is that this backend gives every label that width.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import asyncio
from textual.widgets import Label
from edit_cfg_json import EditModel
from edit_cfg_json_textual.textual_editor import EditorApp
from edit_cfg_json_textual.textual_look import NAME_CLASS
from example.e20_union_types import ExportConfig
from .helpers import ROOMY_SIZE


def test_names_fitted() -> None:
    """Test every name is as wide as the longest, at every depth.

    The names of a terminal are one cell per character, so the longest name
    of the example of the complaint is the width of every one of them.
    """
    model = EditModel(ExportConfig())

    async def run() -> tuple[list[str], set[int]]:
        app = EditorApp(model)
        async with app.run_test(size=ROOMY_SIZE) as pilot:
            await pilot.pause()
            found = list(app.query(f'.{NAME_CLASS}').results(Label))
            return ([str(label.content) for label in found],
                    {label.size.width for label in found})
    names, widths = asyncio.run(run())
    assert names == [row.name for row in model.rows]
    assert widths == {len('jira_column_map')}
