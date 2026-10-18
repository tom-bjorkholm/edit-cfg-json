#! /usr/bin/env python3
"""Tests for the column of the types in the Textual backend.

Every row says the type it holds between its name and its value, in a
pull-down that nothing can be chosen in yet. What a row holds and how the
column is spelled are the core's; what is tested here is that this backend
shows what the core says, on every row and in one column.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import asyncio
from edit_cfg_json import EditModel, row_type_text, row_type_texts, \
    type_column_width
from edit_cfg_json_textual.textual_editor import EditorApp
from edit_cfg_json_textual.textual_look import TYPE_ARROW_WIDTH
from example.e18_declared_types import ReportConfig
from example.e19_omitted_members import ReportConfig as OmittedReport
from .helpers import ROOMY_SIZE, field_of, type_chooser_of, type_of


def test_every_row() -> None:
    """Test every row says the type it holds, inactive and one column wide.

    A type is full of square brackets, which Textual would read as markup:
    `tags` is the row that says `list[str]` and not `list`.
    """
    model = EditModel(ReportConfig())

    async def run() -> tuple[list[str], set[int], set[bool]]:
        app = EditorApp(model)
        async with app.run_test(size=ROOMY_SIZE) as pilot:
            await pilot.pause()
            names = [row.name for row in model.rows]
            choosers = [type_chooser_of(app, name) for name in names]
            return ([type_of(app, name) for name in names],
                    {chooser.size.width for chooser in choosers},
                    {chooser.disabled for chooser in choosers})
    shown, widths, disabled = asyncio.run(run())
    assert shown == [row_type_text(row) for row in model.rows]
    assert 'list[str]' in shown
    assert widths == {type_column_width(model) + TYPE_ARROW_WIDTH}
    assert disabled == {True}


def test_types_listed() -> None:
    """Test the pull-down of a row offers every type that row may hold.

    `subtitle` is declared `Optional[str]` and holds nothing, so it shows
    `None` and offers both.
    """
    model = EditModel(ReportConfig())

    async def run() -> tuple[str, tuple[str, ...]]:
        app = EditorApp(model)
        async with app.run_test(size=ROOMY_SIZE):
            return (type_of(app, 'subtitle'),
                    type_chooser_of(app, 'subtitle').offered)
    subtitle = {row.name: row for row in model.rows}['subtitle']
    assert asyncio.run(run()) == ('None', row_type_texts(subtitle))
    assert row_type_texts(subtitle) == ('str', 'None')


def test_offer_follows() -> None:
    """Test a row whose type only its value says offers what it holds now.

    `legacy` has no annotation and holds nothing, so it offers `None`; a text
    typed into it is a text, and the pull-down says so and offers that.
    """
    async def run() -> tuple[str, str, tuple[str, ...]]:
        app = EditorApp(EditModel(OmittedReport()))
        async with app.run_test(size=ROOMY_SIZE) as pilot:
            await pilot.pause()
            before = type_of(app, 'legacy')
            field_of(app, 'legacy').value = 'kept'
            await pilot.pause()
            return (before, type_of(app, 'legacy'),
                    type_chooser_of(app, 'legacy').offered)
    assert asyncio.run(run()) == ('None', 'str', ('str',))
