#! /usr/bin/env python3
"""The screens this backend asks the user a question on.

There are two shapes of question. One is answered with text — which file to
write, and what a new entry of a dict is to be called — and one is answered
yes or no, which is whether the changes that have not been saved may be
dropped. Each shape is one screen serving every question of that shape,
because two screens differing in a prompt would be the same code twice and the
questions would then be free to drift apart in how they behave.

A question is a screen of its own rather than a field or a row in the editor,
because it is asked, answered and gone: something that was always there would
be one more thing to read in every session, for a question that is asked once
or never.

Neither screen decides *whether* it is asked. Which file to write is what a
backend is asked for when the model has no destination, what a new entry is
called is asked where `edit_cfg_json.MemberRow.offer` says a key is needed,
and whether there is anything to lose by closing is
`edit_cfg_json.close_question`. All three are the core's, so that the two
backends cannot ask one user something and another user nothing.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from collections.abc import Sequence
from typing import ClassVar, Optional
from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical
from textual.screen import ModalScreen
from textual.widgets import Button, Input, Label
from edit_cfg_json_textual.textual_look import ANSWER_CLASS, ASK_BOX_ID, \
    QUESTION_CLASS, bind_action

CANCEL_COMMAND = 'Cancel'
"""Name of the action that leaves a question of the editor unanswered."""

DISCARD_ID = 'discard'
"""Identifier of the control that answers a question with yes."""

KEEP_ID = 'keep'
"""Identifier of the control that answers it with no."""

DISCARD_LABEL = 'Discard'
"""Label of the control that drops the changes and closes the editor."""

KEEP_LABEL = 'Keep editing'
"""Label of the control that leaves the editor as it was.

It says what happens next rather than answering the question with a word, in
the same way as the actions this backend renames: a control saying No beside a
question about closing leaves the user working out what No was about.
"""


class AskScreen(ModalScreen[Optional[str]]):
    """Ask one question, and give back None when it is left unanswered."""

    def __init__(self, prompt: str, field_id: str, cancel_keys: Sequence[str],
                 answer: str = '') -> None:
        """Ask the question, with the field holding what it starts from.

        The keys that leave the question are bound here rather than declared
        as a class variable, because which keys they are is the application's
        decision and not this screen's.

        Args:
            prompt: What this screen asks, as the user reads it.
            field_id: Identifier that the field is found by, which is what
                lets a test and a caller reach the one that is being asked.
            cancel_keys: Key combinations that leave the question unanswered,
                empty when the application gave it none.
            answer: What the field starts out holding, which is what makes
                changing an answer a matter of changing a few characters.
        """
        super().__init__(classes=QUESTION_CLASS)
        self._prompt = prompt
        self._start = answer
        self._field_id = field_id
        self._cancel_keys = tuple(cancel_keys)
        bind_action(self._bindings, keys=self._cancel_keys, action='leave',
                    description=CANCEL_COMMAND)

    def compose(self) -> ComposeResult:
        """Create the question and the field that answers it."""
        with Vertical(id=ASK_BOX_ID):
            yield Label(self._prompt)
            yield Input(value=self._start, id=self._field_id,
                        select_on_focus=False)

    def on_input_changed(self, event: Input.Changed) -> None:
        """Keep what happens in this field to this screen.

        The editor underneath writes every field change into the model, and
        this field is not a member of the configuration: it is the name of a
        file or of a new entry. A message that reached the editor would be
        looked for among the members and found nowhere.
        """
        event.stop()

    def on_input_blurred(self, event: Input.Blurred) -> None:
        """Keep leaving this field to this screen, for the same reason.

        The editor underneath asks the model about the member whose field was
        left, and neither of these fields is a member of the configuration.
        """
        event.stop()

    def on_input_submitted(self, event: Input.Submitted) -> None:
        """Give back what was typed, and leave the screen."""
        event.stop()
        self.dismiss(event.value)

    def action_leave(self) -> None:
        """Leave the screen without answering the question."""
        self.dismiss(None)


class ConfirmScreen(ModalScreen[bool]):
    """Ask one question that is answered by one of two controls.

    It is a screen and not a field, exactly as the question above it is, and
    it is answered with controls rather than with text because what the user
    is being asked for is a decision and not a value.
    """

    AUTO_FOCUS: ClassVar[str] = f'#{KEEP_ID}'
    """The control that the screen opens with, which is the safe one.

    A screen that opened on the control which drops the changes would drop
    them for a user who pressed Enter without reading, and the whole reason
    for asking is that dropping them cannot be undone. The Tk backend opens
    its dialog on the same answer and for the same reason.
    """

    def __init__(self, question: str, cancel_keys: Sequence[str]) -> None:
        """Ask the question, with the keys that leave it unanswered.

        Args:
            question: What this screen asks, as the user reads it.
            cancel_keys: Key combinations that leave the question unanswered,
                which is the same as answering it with no, empty when the
                application gave it none.
        """
        super().__init__(classes=QUESTION_CLASS)
        self._question = question
        bind_action(self._bindings, keys=tuple(cancel_keys), action='leave',
                    description=CANCEL_COMMAND)

    def compose(self) -> ComposeResult:
        """Create the question and the two controls that answer it."""
        with Vertical(id=ASK_BOX_ID):
            yield Label(self._question)
            with Horizontal(classes=ANSWER_CLASS):
                yield Button(DISCARD_LABEL, id=DISCARD_ID)
                yield Button(KEEP_LABEL, id=KEEP_ID)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Give back what was pressed, and leave the screen.

        The message is stopped here because the editor underneath reads every
        press for a control of a row, and neither of these is one.
        """
        event.stop()
        self.dismiss(event.button.id == DISCARD_ID)

    def action_leave(self) -> None:
        """Leave the screen, which is the same as keeping the changes."""
        self.dismiss(False)


QUESTION_SCREENS = (AskScreen, ConfirmScreen)
"""The screens on which this backend asks the user something.

The editor turns its own actions off while one of them is up, because Textual
offers an application's priority bindings the key from the whole binding chain
rather than from the part of it above the last modal screen. What makes a
question modal is therefore the editor answering for its own actions, and this
is what it asks about.
"""
