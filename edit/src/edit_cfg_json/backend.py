#! /usr/bin/env python3
"""The protocol that every user interface backend implements."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from typing import Protocol
from edit_cfg_json.edit_model import EditModel


class EditorBackend(Protocol):  # pylint: disable=too-few-public-methods
    """Show one edit model to the user and return when the user is done.

    The protocol is phrased against the model and not against a convenience
    wrapper, so that an application that already runs its own event loop can
    build the model itself and mount the backend as a widget. The outcome of
    the session is read from the model afterwards rather than returned here,
    so that the protocol does not have to change when saving is added.
    """

    def run_editor(self, model: EditModel) -> None:
        """Run the user interface for one model until the user is done.

        Args:
            model: Model to show. The backend reads and edits the model, and
                never touches the caller's configuration object.
        """
