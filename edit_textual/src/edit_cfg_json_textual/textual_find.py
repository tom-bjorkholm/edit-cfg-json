#! /usr/bin/env python3
"""The search of a Textual editor: a field, four controls and a line.

A configuration of any interesting size does not fit a terminal, so the member
a user wants is often one they cannot see. This is what they look for it with,
and it is a part of the editor rather than a screen that is asked and gone: a
search is a text that is changed a character at a time, with the answer moving
under it as it is typed, and four controls beside it that change what it
reaches.

What is being looked for, how it is compared and which node the search has got
to are all state of the model, so nothing here decides any of it. What is here
is the widgets, the words on them and the wiring: this backend's half of a
question the core answers.

It is a widget of its own rather than a part of the panel, so that the messages
of its field stop here: the panel writes every field change into the model as
the value of a member, and this field is no member of the configuration.

Everything this backend takes from the core is reached through `core`, which is
`edit_cfg_json` itself. A backend may use the public API of the core and
nothing else, and naming it at every call site is what makes that visible.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from collections.abc import Callable
from textual.app import ComposeResult
from textual.containers import Horizontal
from textual.widget import Widget
from textual.widgets import Button, Checkbox, Input, Label, Static
import edit_cfg_json as core
from edit_cfg_json_textual.textual_look import FIND_AREA_CLASS, FIND_ID, \
    FIND_LINE_CLASS, FIND_LINE_ID, FIND_NEXT_CLASS, FIND_NEXT_ID, \
    FIND_ROW_CLASS, FIND_TICK_CLASS, FIND_TICK_IDS, plain_widget, \
    show_emphasis

FIND_LABEL_TEXT = 'Find:'
"""Text of the label beside the field that a search is typed into."""

FIND_NEXT_TEXT = 'next'
"""Label of the control that goes to the next member the search reaches.

A control as well as a key, because a function key is the one thing a terminal
is most likely not to deliver, and one word because the row it shares is the
row that the field needs the width of.
"""

FIND_TICK_LABELS = ('path', 'value', 'Aa', '==')
"""The label of each control that says where a search looks.

They are in the order of the members of `edit_cfg_json.FindOptions`, and so are
the identifiers they are created with, because that is what pairs each control
with the answer it shows. A member added there without a label here is refused
where the controls are created rather than being left out in silence.

Two of them are one or two characters, which is what keeps the whole row one
line: the width of that row is what the field is for. What each of them means
is `edit_cfg_json.FIND_OPTION_HELP`, given to the tooltip that the toolkit
offers for exactly this, because what a control means is the core's to say.
"""


class FindRow(Widget):
    """The search of one Textual editor, as the widgets and what they do.

    It holds the model and asks it, rather than reporting keystrokes to the
    panel, because what a search is belongs to the model and this is the one
    widget of this backend that is about a search at all. What it hands back to
    the panel is the two things only the panel can do: show the rows again when
    a container was opened, and bring what was found into view.
    """

    def __init__(self, model: core.EditModel, *,
                 searched: Callable[[bool], None],
                 reached: Callable[[], None]) -> None:
        """Remember the model and what the panel does about a search.

        Args:
            model: Model that the search is of.
            searched: What the panel does once a search has run, told whether a
                container was opened to reach what was found.
            reached: What the panel does to go into what was found, which is
                bringing it into view and typing in it.
        """
        super().__init__(classes=FIND_AREA_CLASS)
        self._model = model
        self._searched = searched
        self._reached = reached

    def compose(self) -> ComposeResult:
        """Create the field, the four controls and the line below them.

        The line is under the row rather than beside it, because what it says
        about a search that has nowhere left to look is a sentence, and the row
        it would share is the row whose width the field wants.
        """
        report = self._model.search
        with Horizontal(classes=FIND_ROW_CLASS):
            yield Label(FIND_LABEL_TEXT)
            yield Input(value=report.text, id=FIND_ID, select_on_focus=False)
            yield from self._tick_widgets(report.options)
            yield Button(FIND_NEXT_TEXT, id=FIND_NEXT_ID,
                         classes=FIND_NEXT_CLASS)
        yield plain_widget('', FIND_LINE_ID, FIND_LINE_CLASS)

    @staticmethod
    def _tick_widgets(options: core.FindOptions) -> ComposeResult:
        """Create the four controls that say where a search looks.

        Args:
            options: How the text being looked for is compared now.

        Yields:
            One control per member of `edit_cfg_json.FindOptions`, in that
            order, each of them ticked as that member says.
        """
        for label, tip, tick, value in zip(FIND_TICK_LABELS,
                                           core.FIND_OPTION_HELP,
                                           FIND_TICK_IDS, options,
                                           strict=True):
            yield Checkbox(label, value=value, id=tick, tooltip=tip,
                           compact=True, classes=FIND_TICK_CLASS)

    def focus_field(self) -> None:
        """Put the cursor in the field that a search is typed into.

        What is in the field is left exactly as it is, because a user who has
        found one member and wants another comes back to text that is worth
        changing rather than text that is worth typing again.
        """
        self.query_one(f'#{FIND_ID}', Input).focus()

    def find_next(self) -> None:
        """Go to the next node the search reaches, and type in it."""
        self._searched(self._model.find_next())
        self._reached()

    def show(self) -> None:
        """Say what the search has reached, and nothing when nothing is.

        The line is hidden while there is nothing to say, because a blank line
        under the search row would otherwise be there in every session that
        nobody searched in.
        """
        shown = core.find_text(self._model)
        widget = self.query_one(f'#{FIND_LINE_ID}', Static)
        widget.update(shown)
        widget.display = bool(shown)
        show_emphasis(widget, core.find_emphasis(self._model))

    def on_input_changed(self, event: Input.Changed) -> None:
        """Look for what the field holds, and show what that reached.

        Every change of the text is a search, because that is what a field
        which stays on the screen is for: the answer moves under it as it is
        typed, and nothing has to be pressed to ask. The cursor stays here,
        unlike the one that a press of Enter or of the control moves.

        The message is stopped because the editor underneath writes every field
        change into the model as the value of a member, and this field is no
        member of the configuration.
        """
        event.stop()
        self._searched(self._model.find(event.value))

    def on_input_submitted(self, event: Input.Submitted) -> None:
        """Go into the node that the search has already reached.

        This is the press that says the user has found what they were looking
        for and wants to edit it, which is why it moves the cursor and typing
        does not.
        """
        event.stop()
        self._reached()

    def on_input_blurred(self, event: Input.Blurred) -> None:
        """Keep leaving this field to this widget.

        The editor underneath asks the model about the member whose field was
        left, and this field is no member of the configuration.
        """
        event.stop()

    def on_checkbox_changed(self, event: Checkbox.Changed) -> None:
        """Look again with the places and the comparison as they are now."""
        event.stop()
        self._searched(self._model.set_find_options(self._options()))

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Go to the next node the search reaches.

        The message is stopped for the same reason the others are: the editor
        underneath reads every press for a control of a row, and this is none.
        """
        event.stop()
        self.find_next()

    def _options(self) -> core.FindOptions:
        """Return what the four controls of the search say now."""
        ticked = tuple(self.query_one(f'#{tick}', Checkbox).value
                       for tick in FIND_TICK_IDS)
        return core.FindOptions(in_path=ticked[0], in_value=ticked[1],
                                cased=ticked[2], whole=ticked[3])
