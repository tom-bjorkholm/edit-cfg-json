#! /usr/bin/env python3
"""The widgets of every row of the editor, and which node each belongs to.

Every message about a widget of a row arrives at the panel, which is what
having one body for both ways of running the editor means, and the panel then
has to know which node the widget is about. That is what this keeps: the rows
are made here, and each widget that a message can arrive from is remembered by
its identifier together with the node it belongs to.

It is apart from the panel because the panel is the actions of the editor, and
the widgets of the rows are a thing of their own that the actions look up:
`textual_member` makes the widgets of one row, and this makes all of them and
remembers whose each one is.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from collections.abc import Mapping
from typing import Optional
from config_as_json import ConfigPath
from textual.containers import Horizontal, Vertical
from textual.widget import Widget
from textual.widgets import Label
import edit_cfg_json as core
from edit_cfg_json_textual.textual_elements import element_id, \
    offered_actions
from edit_cfg_json_textual.textual_look import MARK_CLASS, MEMBER_CLASS, \
    NAME_CLASS, ROW_CLASS, TREE_INDENT, choice_id, fold_id, mark_id, \
    member_id, plain_widget, type_id, value_id
from edit_cfg_json_textual.textual_member import description_widgets, \
    TypeChooser, diagnostic_widget, element_widgets, fold_widget, \
    subtree_widgets, value_widgets


class PanelRows:
    """The widgets of every node of one model, and whose each of them is.

    The maps are made afresh whenever the widgets are, because the rows are
    mounted afresh after a validation pass that changed them and after every
    change of how many elements a container holds.
    """

    def __init__(self, model: core.EditModel) -> None:
        """Remember the model whose rows these are.

        Args:
            model: Model to show and to edit.
        """
        self._model = model
        self._fields: dict[str, core.MemberRow] = {}
        self._choosers: dict[str, int] = {}
        self._types: dict[str, int] = {}
        self._folds: dict[str, core.MemberRow] = {}
        self._elements: dict[str, tuple[core.MemberRow, str]] = {}
        self._built: tuple[tuple[ConfigPath, bool, bool], ...] = ()

    @property
    def fields(self) -> Mapping[str, core.MemberRow]:
        """Return the node of every field, by the identifier of the field."""
        return self._fields

    @property
    def choosers(self) -> Mapping[str, int]:
        """Return the place of the node of every pull-down of the values."""
        return self._choosers

    @property
    def types(self) -> Mapping[str, int]:
        """Return the place of the node of every active pull-down of types."""
        return self._types

    @property
    def folds(self) -> Mapping[str, core.MemberRow]:
        """Return the node of every control that folds a container."""
        return self._folds

    @property
    def elements(self) -> Mapping[str, tuple[core.MemberRow, str]]:
        """Return the node and the action of every element control."""
        return self._elements

    @property
    def built(self) -> tuple[tuple[ConfigPath, bool, bool], ...]:
        """Return what the rows were made for, as `rows_shape` says it."""
        return self._built

    def widgets(self) -> list[Widget]:
        """Return the widgets of every node, and forget the ones before.

        The model is asked to settle the values first, because a pull-down
        holds one of the values its member takes and is made holding it. That
        is a question and never an answer here: while the values are typed it
        does nothing, and while they are chosen every such member already
        holds one of its own values, so it has nothing to do either.

        Returns:
            One widget per node of the model, in the order it reports them.
        """
        self._model.settle_choices()
        self._fields = {}
        self._choosers = {}
        self._types = {}
        self._folds = {}
        self._elements = {}
        self._built = core.rows_shape(self._model)
        width = core.type_column_width(self._model)
        return [self._member_widget(index=index, row=row, width=width)
                for index, row in enumerate(self._model.rows)]

    def _member_widget(self, index: int, row: core.MemberRow,
                       width: int) -> Widget:
        """Return everything one node owns, as one widget.

        The node is indented once for every container it is inside, which is
        what makes the rows a tree, and it is hidden while any of those
        containers is folded away. Its type stands between its name and its
        value, which reads as Python's `name: type = value`.

        Args:
            index: Place of the node among the rows, which its widgets are
                identified by.
            row: Node to show.
            width: Width in characters of the column of the types.

        Returns:
            A widget holding the line of that node and what is said below it.
        """
        marks = plain_widget(core.row_marks(row), mark_id(index), MARK_CLASS,
                             core.MEMBER_MARK)
        beside = [Label(row.name, classes=NAME_CLASS),
                  self._added_types(index=index, row=row, width=width),
                  *self._added_values(index=index, row=row), marks,
                  *subtree_widgets(index=index, row=row),
                  *self._added_elements(index=index, row=row)]
        folding = self._added_fold(index=index, row=row)
        line = Horizontal(*([folding] if folding is not None else []), *beside,
                          classes=ROW_CLASS)
        below = list(description_widgets(model=self._model, index=index,
                                         row=row))
        below.append(diagnostic_widget(model=self._model, index=index,
                                       row=row))
        member = Vertical(line, *below, id=member_id(index),
                          classes=MEMBER_CLASS)
        member.styles.padding = (0, 0, 0, row.depth * TREE_INDENT)
        member.display = row.shown
        return member

    def _added_elements(self, index: int, row: core.MemberRow) -> list[Widget]:
        """Create the controls of one node, and remember whose they are.

        Args:
            index: Place of the node among the rows.
            row: Node to create the controls for.

        Returns:
            The controls that node offers, and none at all for one that
            offers none, which is most nodes of most configurations.
        """
        for action in offered_actions(row):
            self._elements[element_id(index=index, action=action)] = (row,
                                                                      action)
        return list(element_widgets(index=index, row=row))

    def _added_types(self, index: int, row: core.MemberRow,
                     width: int) -> Widget:
        """Create the pull-down of the types of one node, and remember it.

        Only an active one is remembered, because only an active one posts a
        message that is about anything: a disabled one posts it as well, when
        it is given the type the node holds.

        Args:
            index: Place of the node among the rows.
            row: Node to create the pull-down for.
            width: Width in characters of the column of the types.

        Returns:
            The pull-down of the types of that node.
        """
        if core.row_chooses_type(row):
            self._types[type_id(index)] = index
        return TypeChooser(index=index, row=row, width=width)

    def _added_values(self, index: int, row: core.MemberRow) -> list[Widget]:
        """Create the ways of editing one value, and remember whose they are.

        Args:
            index: Place of the node among the rows.
            row: Node to create the widgets for.

        Returns:
            The widgets that show or edit the value of that node.
        """
        if row.editable:
            self._fields[value_id(index)] = row
        if core.row_chooses(row):
            self._choosers[choice_id(index)] = index
        return list(value_widgets(index=index, row=row,
                                  chosen=self._model.choices_shown))

    def _added_fold(self, index: int, row: core.MemberRow) -> Optional[Widget]:
        """Create the control that folds one node, and remember whose it is.

        Args:
            index: Place of the node among the rows.
            row: Node to create the control for.

        Returns:
            The control that folds that container, an empty space of the same
            width for every other node of a configuration that has one, and
            None for a configuration with nothing to fold.
        """
        foldable = core.can_fold(self._model)
        if foldable and row.foldable:
            self._folds[fold_id(index)] = row
        return fold_widget(index=index, row=row, foldable=foldable)
