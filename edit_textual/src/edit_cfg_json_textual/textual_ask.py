#! /usr/bin/env python3
"""The one screen this backend asks a question of the user with.

There are two questions so far — which file to write, and what a new entry of
a dict is to be called — and they are the same shape: a sentence, a field, and
an answer that may be left ungiven. One screen serves both, because two
screens differing in a prompt would be the same code twice and the two
questions would then be free to drift apart in how they behave.

The question is a screen of its own rather than a field in the editor, because
it is asked, answered and gone: a field that was always there would be one more
thing to read on every row of every session, for a question that is asked once
or never.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from collections.abc import Sequence
from typing import Optional
from textual.app import ComposeResult
from textual.containers import Vertical
from textual.screen import ModalScreen
from textual.widgets import Input, Label
from edit_cfg_json_textual.textual_look import bind_action

ASK_BOX_ID = 'ask_box'
"""Identifier of the box that holds one question and its field."""

CANCEL_COMMAND = 'Cancel'
"""Name of the action that leaves a question of the editor unanswered."""


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
        super().__init__()
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
