#! /usr/bin/env python3
"""The widgets that one member of the configuration owns, and what they show.

One row of the editor is a line holding the value of a node and what has
happened to it, and below that what the node is for and what is wrong with it.
This is where those widgets are made and where each of them is shown again
once the model says something else.

The value is the part of a row with two shapes. A value the editor can edit is
typed into a field, and a value whose whole set the editor knows is picked from
a pull-down of that set instead; both widgets are made and one of them is on
the screen, because a field the user was typing into should still hold what
they typed when they switch back to it.

**A pull-down offers the values its member takes and nothing else**, and one
of them is selected at every moment. There is no unselected state, no blank
line among the values and no way to put a member into either: what a member
holding an enum takes is the members of that enum, and what a member holding
true or false takes is those two words.

Nothing here holds any state. Which node each widget belongs to is the panel's,
because the panel is what every message about a widget arrives at, and this is
a module of functions so that `textual_panel` stays short enough to read.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from typing import Optional
from textual.app import ComposeResult
from textual.content import Content
from textual.widget import Widget
from textual.widgets import Button, Input, Label, Select, Static
import edit_cfg_json as core
from edit_cfg_json_textual.textual_elements import element_button, \
    element_id, offered_actions
from edit_cfg_json_textual.textual_look import DESCRIPTION_CLASS, \
    DIAGNOSTIC_CLASS, FOLD_CLASS, NAME_CLASS, SUBTREE_CLASS, \
    TYPE_ARROW_WIDTH, TYPE_CLASS, VALUE_CLASS, choice_id, description_id, \
    diagnostic_id, fold_glyph, fold_id, plain_widget, show_emphasis, \
    subtree_id, type_id, value_id


class TypeChooser(Select[str]):
    """The pull-down of the types one node may hold.

    It shows the type the node holds now and lists every type it may hold. It
    is active where the type is the user's to choose and disabled everywhere
    else, and every row has one all the same, so that every row says its type
    in the same place.

    It remembers what it offers, because that can change while the editor is
    open: a node whose declaration names nothing usable offers the one type
    its value has, and a value typed into it can be of another type. Each
    type is given as plain content rather than as text, because Textual reads
    text as markup and a type is full of square brackets: `list[str]` would be
    shown as `list`.

    The value of each option is the whole text of its type and not its place
    among them, because a pull-down given new options shows the one it holds
    again only where its value changes: with places for values, the one type
    of `None` replaced by the one type of `str` would both be place 0, and the
    pull-down would go on saying `None`. It is the whole text rather than the
    text shown, because the column cuts a long type and two types can be cut
    to the same text, while the whole text is what the model is given.
    """

    def __init__(self, index: int, row: core.MemberRow, width: int) -> None:
        """Create the pull-down of the types of one node.

        Args:
            index: Place of the node among the rows.
            row: Node to create the pull-down for.
            width: Width in cells of the text of this pull-down, which is
                what `edit_cfg_json.type_column_widths` gives the row, so
                that the column of the types ends in one place and the values
                begin in one column.
        """
        self._offered = core.row_type_choices(row)
        super().__init__(self._options_of(self._offered), allow_blank=False,
                         compact=True, value=row.chosen_type.text,
                         disabled=not core.row_chooses_type(row),
                         id=type_id(index), classes=TYPE_CLASS)
        self.styles.width = width + TYPE_ARROW_WIDTH

    @property
    def offered(self) -> tuple[str, ...]:
        """Return the types this pull-down lists, as the column shows each."""
        return tuple(shown for shown, _ in self._offered)

    @staticmethod
    def _options_of(offered: tuple[tuple[str, str], ...]
                    ) -> list[tuple[Content, str]]:
        """Return the options of a pull-down offering those types."""
        return [(Content(shown), whole) for shown, whole in offered]

    def show(self, row: core.MemberRow) -> None:
        """Show the type the node holds now, among what it may hold now.

        Args:
            row: Node whose type is being shown, as the model holds it now.
        """
        offered = core.row_type_choices(row)
        if offered != self._offered:
            self._offered = offered
            self.set_options(self._options_of(offered))
        self.value = row.chosen_type.text


def value_widgets(index: int, row: core.MemberRow,
                  chosen: bool) -> ComposeResult:
    """Create the ways of editing the value of one node.

    A node that the model cannot edit gets a widget that only shows text,
    because there is nothing the user could do to it: a list, a dict and a
    nested configuration object are each edited through the rows below them,
    and a declared member that holds no object holds no text either.

    A node whose values are a set the editor knows the whole of gets a
    pull-down of those values as well as a field, and `show_way` is what puts
    one of the two on the screen.

    Args:
        index: Place of the node among the rows.
        row: Node to create the widgets for.
        chosen: Whether the values are being chosen rather than typed.

    Returns:
        One widget for a node the model cannot edit, and a field and perhaps
        a pull-down for every other node.
    """
    if not row.editable:
        yield plain_widget(core.row_value_text(row), value_id(index),
                           VALUE_CLASS)
        return
    # A field of its own accord selects all of its text when it is given the
    # focus, so that the first key typed replaces the whole value. That is
    # turned off here, because the two backends would otherwise behave
    # differently: a Tk field puts the cursor in the text and keeps what is
    # there, which is what an editor of existing values should do.
    field = Input(value=core.row_value_text(row), compact=True,
                  id=value_id(index), select_on_focus=False,
                  classes=VALUE_CLASS)
    field.display = not chosen or not row.choices
    yield field
    if core.row_chooses(row):
        yield _choice_widget(index=index, row=row, chosen=chosen)


def _choice_widget(index: int, row: core.MemberRow, chosen: bool) -> Widget:
    """Return the pull-down of the values one node takes.

    It offers those values and nothing else, and it holds one of them at every
    moment: `allow_blank` is false, so the widget has no unselected state to
    list among them and no unselected state to be put into. The value it opens
    with is the one the node holds, which the model has been asked to settle
    before any of these widgets is made.

    Args:
        index: Place of the node among the rows.
        row: Node to create the pull-down for.
        chosen: Whether the values are being chosen rather than typed.

    Returns:
        A pull-down of the values that node takes.
    """
    offered = [(value, value) for value in row.choices]
    chooser: Select[str] = Select(offered, allow_blank=False, compact=True,
                                  value=core.row_value_text(row),
                                  id=choice_id(index), classes=VALUE_CLASS)
    chooser.display = chosen
    return chooser


def show_way(field: Input, chooser: 'Select[str]', chosen: bool) -> None:
    """Put the way of editing one value that the model asks for now.

    The one that is not being used is hidden rather than taken off the screen,
    so that a field the user was typing into still holds what they typed when
    they switch back to it.

    Args:
        field: The field of that node.
        chooser: The pull-down of that node.
        chosen: Whether the values are being chosen rather than typed.
    """
    field.display = not chosen
    chooser.display = chosen


def show_chosen(chooser: 'Select[str]', row: core.MemberRow) -> None:
    """Show the value one pull-down holds, as the model holds it now.

    The value is always one of the ones the pull-down offers, because the
    model is asked to settle the values before a pull-down is made and a
    pull-down offers nothing else.

    Args:
        chooser: The pull-down of that node.
        row: Node whose value is being shown, as the model holds it now.
    """
    chooser.value = core.row_value_text(row)


def element_widgets(index: int, row: core.MemberRow) -> ComposeResult:
    """Create the controls that change how many elements one node holds.

    They are at the end of the line, after the value and the marks, so a node
    that offers none of them costs the values no width at all. That is what
    makes four of them affordable where the one control that folds a container
    has to keep a column clear on every row.

    Args:
        index: Place of the node among the rows.
        row: Node to create the controls for.

    Returns:
        The controls that node offers, and none at all for one that offers
        none, which is most nodes of most configurations.
    """
    for action in offered_actions(row):
        yield element_button(widget_id=element_id(index=index, action=action),
                             action=action)


def name_widget(row: core.MemberRow, width: int) -> Widget:
    """Return the label that says the name of one node.

    Args:
        row: Node to create the label for.
        width: Width in cells of the column of the names, which every name
            is as wide as so that the names line up.

    Returns:
        A label saying the name of that node.
    """
    label = Label(row.name, classes=NAME_CLASS)
    label.styles.width = width
    return label


def fold_widget(index: int, row: core.MemberRow,
                foldable: bool) -> Optional[Widget]:
    """Return the control that folds one container, or an empty space.

    A node that holds nothing gets a widget of the same width rather than no
    widget at all, so that the names of a container and of a value beside it
    begin in the same column. A configuration with nothing to fold anywhere
    gets no column at all, because a column that could never hold anything is
    width taken from the values for nothing.

    Args:
        index: Place of the node among the rows.
        row: Node to create the control for.
        foldable: Whether this configuration has anything to fold at all.

    Returns:
        A button for a container, a label for every other node of a
        configuration that has one, and None for one that has none.
    """
    if not foldable:
        return None
    if not row.foldable:
        return Label('', classes=FOLD_CLASS)
    return Button(fold_glyph(row), id=fold_id(index), classes=FOLD_CLASS,
                  compact=True)


def subtree_widgets(index: int, row: core.MemberRow) -> ComposeResult:
    """Create the widget that says what one object is on its own.

    A node that is no configuration object gets none, by the same rule as the
    description below the row: a widget that could never hold anything is a
    piece of the screen spent on nothing.

    Args:
        index: Place of the node among the rows.
        row: Node to create the widget for.

    Returns:
        One widget for a nested configuration object, and none at all for
        every other node.
    """
    if core.row_validates(row):
        yield plain_widget(core.row_subtree_text(row), subtree_id(index),
                           SUBTREE_CLASS, core.subtree_emphasis(row))


def description_widgets(model: core.EditModel, index: int,
                        row: core.MemberRow) -> ComposeResult:
    """Create the widget that says what one node is for, if anything.

    A node that nothing can ever be said about gets no widget, because there
    is nothing that could ever appear in it. Whether anything can be is asked
    of the core, because the description the row carries is not the whole of
    what is said below a nested configuration object.

    A widget that is created starts out shown or hidden as the model says,
    which is not the same as shown: a model can have been told to hide the
    explanations before the editor was started.

    Args:
        model: Model that says how much is being explained.
        index: Place of the node among the rows.
        row: Node to describe.

    Returns:
        One widget for a node something can be said about, and none at all
        for every other node.
    """
    if core.row_describes(row):
        shown = core.row_description(model=model, row=row)
        widget = plain_widget(shown, description_id(index), DESCRIPTION_CLASS,
                              core.EXPLANATION)
        widget.display = bool(shown)
        yield widget


def diagnostic_widget(model: core.EditModel, index: int,
                      row: core.MemberRow) -> Static:
    """Return the widget that says what is wrong with one node.

    Every node gets one, unlike the description above it: any node can be
    refused, so there is no node for which this could never say anything. It
    starts out hidden unless the model already has something to say about that
    node, which it has when a model that has been validated already reaches
    this backend.

    Args:
        model: Model that says what is wrong with the node.
        index: Place of the node among the rows.
        row: Node to create the widget for.

    Returns:
        The widget that says what is wrong with that node.
    """
    wrong = core.row_diagnostic(model=model, row=row)
    widget = plain_widget(wrong, diagnostic_id(index), DIAGNOSTIC_CLASS,
                          core.MEMBER_DIAGNOSTIC)
    widget.display = bool(wrong)
    return widget


def show_subtrees(panel: Widget, model: core.EditModel) -> None:
    """Say what each nested object is on its own, as the model says now.

    It is shown after folding as well as after a validation pass, because
    folding a nested object is one of the moments the model asks that object
    about itself.

    Args:
        panel: Widget that the rows were built below.
        model: Model that says what each object amounts to now.
    """
    for index, row in enumerate(model.rows):
        if not core.row_validates(row):
            continue
        widget = panel.query_one(f'#{subtree_id(index)}', Static)
        widget.update(core.row_subtree_text(row))
        show_emphasis(widget, core.subtree_emphasis(row))


def show_descriptions(panel: Widget, model: core.EditModel) -> None:
    """Show what belongs below every node, as the model says it now.

    Args:
        panel: Widget that the rows were built below.
        model: Model that says how much is being explained.
    """
    for index, row in enumerate(model.rows):
        if not core.row_describes(row):
            continue
        description = core.row_description(model=model, row=row)
        widget = panel.query_one(f'#{description_id(index)}', Static)
        widget.update(description)
        widget.display = bool(description)


def show_diagnostics(panel: Widget, model: core.EditModel) -> None:
    """Show what is wrong with every node, as the model says it now.

    Args:
        panel: Widget that the rows were built below.
        model: Model that says what is wrong with each node.
    """
    for index, row in enumerate(model.rows):
        wrong = core.row_diagnostic(model=model, row=row)
        widget = panel.query_one(f'#{diagnostic_id(index)}', Static)
        widget.update(wrong)
        widget.display = bool(wrong)
