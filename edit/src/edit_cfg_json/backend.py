#! /usr/bin/env python3
"""The protocol that every user interface backend implements."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from typing import Protocol
from edit_cfg_json.edit_model import EditModel


class EditorBackend(Protocol):  # pylint: disable=too-few-public-methods
    """Show one edit model to the user and return when the user is done.

    The protocol is phrased against the model and not against the `edit`
    convenience wrapper, so that an application that has built the model
    itself can run a backend over it. A backend that implements this owns a
    window and an event loop of its own and runs to completion, which is
    what the one method below promises.

    Mounting the editor inside a window that an application already owns is
    therefore not this protocol. It cannot run to completion, because the
    event loop that is running is the application's own, and Textual offers
    no way to nest a second one at all. It is a separate, non-blocking entry
    point of each backend package, additive to this one, and section 8.2 of
    `doc/design.md` is where it is designed.

    The outcome of the session is read from the model afterwards rather than
    returned here, so that the protocol does not have to change when saving
    is added, and so that both ways of showing the editor report what was
    saved in the same place.
    """

    def run_editor(self, model: EditModel) -> None:
        """Run the user interface for one model until the user is done.

        Args:
            model: Model to show. The backend reads and edits the model, and
                never touches the caller's configuration object.
        """
