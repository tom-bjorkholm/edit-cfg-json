#! /usr/bin/env python3
"""Tests for the column of the types in the Textual backend.

Every row says the type it holds between its name and its value, in a
pull-down that is active where the type is the user's to choose. What a row
holds, how the column is spelled and what choosing does are the core's; what
is tested here is that this backend shows what the core says, on every row and
in one column, and that picking a type in the pull-down chooses it.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import asyncio
from textual.widgets import Input
from edit_cfg_json import EditModel, row_chooses_type, row_type_text, \
    row_type_texts, type_column_widths
from edit_cfg_json_textual.textual_editor import EditorApp
from edit_cfg_json_textual.textual_elements import ADD_ACTION, \
    REMOVE_ACTION, element_id
from edit_cfg_json_textual.textual_look import TREE_INDENT, \
    TYPE_ARROW_WIDTH, value_id
from edit_cfg_json_textual.textual_member import TypeChooser
from example.e18_declared_types import ReportConfig
from example.e19_omitted_members import ReportConfig as OmittedReport
from example.e20_union_types import ExportConfig
from .helpers import ROOMY_SIZE, field_of, index_of, model_value, \
    panel_of, type_chooser_of, type_of


def test_every_row() -> None:
    """Test every row says the type it holds, in one column.

    A type is full of square brackets, which Textual would read as markup:
    `tags` is the row that says `list[str]` and not `list`. Each pull-down is
    as wide as the core says, which is narrower the deeper its row is, so
    that every one of them ends in the same column of the screen. Only the
    rows whose type is the user's to choose have an active pull-down.
    """
    model = EditModel(ReportConfig())

    async def run() -> tuple[list[str], list[int], set[int], list[bool]]:
        app = EditorApp(model)
        async with app.run_test(size=ROOMY_SIZE) as pilot:
            await pilot.pause()
            names = [row.name for row in model.rows]
            choosers = [type_chooser_of(app, name) for name in names]
            return ([type_of(app, name) for name in names],
                    [chooser.size.width for chooser in choosers],
                    {chooser.region.right for chooser in choosers},
                    [chooser.disabled for chooser in choosers])
    shown, widths, ends, disabled = asyncio.run(run())
    texts = type_column_widths(model, measure=len, indent=TREE_INDENT)
    assert shown == [row_type_text(row) for row in model.rows]
    assert 'list[str]' in shown
    assert widths == [width + TYPE_ARROW_WIDTH for width in texts]
    assert len(ends) == 1
    assert disabled == [not row_chooses_type(row) for row in model.rows]
    assert True in disabled and False in disabled


def test_column_end() -> None:
    """Test the pull-downs of nested rows end where the member's does.

    The example of the complaint has a long type on its member and short
    ones up to three containers inside it, all of them on the screen when it
    opens.
    """
    model = EditModel(ExportConfig())

    async def run() -> set[int]:
        app = EditorApp(model)
        async with app.run_test(size=ROOMY_SIZE) as pilot:
            await pilot.pause()
            return {chooser.region.right
                    for chooser in app.query(TypeChooser)}
    assert {row.depth for row in model.rows} == {0, 1, 2, 3}
    assert len(asyncio.run(run())) == 1


def _picked(name: str, text: str) -> EditModel:
    """Return the model of the example after one type was picked in it."""
    model = EditModel(ReportConfig())

    async def run() -> None:
        app = EditorApp(model)
        async with app.run_test(size=ROOMY_SIZE) as pilot:
            await pilot.pause()
            type_chooser_of(app, name).value = text
            await pilot.pause()
            await pilot.pause()
    asyncio.run(run())
    return model


def test_type_picked() -> None:
    """Test picking a type in the pull-down is what chooses it.

    The number the member held is a text of the same digits afterwards.
    """
    assert model_value(_picked('width', 'str'), 'width') == '80'


def test_value_by_type() -> None:
    """Test choosing `str` gives a field, and choosing `None` takes one."""
    model = EditModel(ReportConfig())

    async def run() -> list[int]:
        app = EditorApp(model)
        async with app.run_test(size=ROOMY_SIZE) as pilot:
            await pilot.pause()
            counted = [len(app.query('Input'))]
            for name, text in (('subtitle', 'str'), ('footer', 'None')):
                type_chooser_of(app, name).value = text
                await pilot.pause()
                await pilot.pause()
                counted.append(len(app.query('Input')))
            return counted
    counted = asyncio.run(run())
    assert counted == [counted[0], counted[0] + 1, counted[0]]
    assert model_value(model, 'subtitle') == ''
    assert model_value(model, 'footer') is None


def test_none_no_controls() -> None:
    """Test a member holding nothing has no field and nothing to press.

    Its type says `None`, which is the whole of what is shown about it, and
    choosing a type is how it is given a value: there is no control at the
    end of its row.
    """
    async def run() -> int:
        app = EditorApp(EditModel(ReportConfig()))
        async with app.run_test(size=ROOMY_SIZE) as pilot:
            await pilot.pause()
            index = index_of(app, 'subtitle')
            return sum(len(app.query(selector)) for selector in
                       (f'Input#{value_id(index)}',
                        f'#{element_id(index, ADD_ACTION)}',
                        f'#{element_id(index, REMOVE_ACTION)}'))
    assert asyncio.run(run()) == 0


def test_typing_keeps() -> None:
    """Test typing into a row whose type is chosen leaves the type alone."""
    async def run() -> str:
        app = EditorApp(EditModel(ReportConfig()))
        async with app.run_test(size=ROOMY_SIZE) as pilot:
            await pilot.pause()
            field_of(app, 'width').value = 'wide'
            await pilot.pause()
            return type_of(app, 'width')
    assert asyncio.run(run()) == 'int'


def test_first_value_focused() -> None:
    """Test the editor gives its first value the focus, as Tk does.

    Textual on its own gives it to the first widget that takes it, which can
    be the pull-down of the types of the first row, so the focus is put on an
    active one of those first and the panel asked again.
    """
    async def run() -> tuple[object, object, object]:
        app = EditorApp(EditModel(ReportConfig()))
        async with app.run_test(size=ROOMY_SIZE) as pilot:
            await pilot.pause()
            first = app.focused
            type_chooser_of(app, 'subtitle').focus()
            await pilot.pause()
            moved = app.focused
            panel_of(app).on_mount()
            await pilot.pause()
            return first, moved, app.focused
    first, moved, focused = asyncio.run(run())
    assert isinstance(first, Input) and first is focused
    assert isinstance(moved, TypeChooser)


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


def test_list_by_type() -> None:
    """Test choosing a list gives the row a list, and `None` takes it away.

    The row is made again as a container, with the control that adds an
    element to it, and choosing `None` takes the list and that control away.
    """
    model = EditModel(OmittedReport())

    async def run() -> list[int]:
        app = EditorApp(model)
        async with app.run_test(size=ROOMY_SIZE) as pilot:
            await pilot.pause()
            index = index_of(app, 'extra_hosts')
            adding = f'#{element_id(index, ADD_ACTION)}'
            counted = [len(app.query(adding))]
            for text in ('list[str]', 'None'):
                type_chooser_of(app, 'extra_hosts').value = text
                await pilot.pause()
                await pilot.pause()
                counted.append(len(app.query(adding)))
            return counted
    assert asyncio.run(run()) == [0, 1, 0]
    assert model_value(model, 'extra_hosts') is None
