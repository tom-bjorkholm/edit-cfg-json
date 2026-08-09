#! /usr/bin/env python3
"""The protocol that every user interface backend implements.

The one backend this package ships is here as well, because it is the one
that needs no user interface library: it prints the model and returns. That
makes it the backend of a program that judges a configuration file on a
machine with no display, and it is also the shortest thing there is to read
for anybody writing a backend of their own.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from typing import Protocol
from edit_cfg_json.edit_model import EditModel
from edit_cfg_json.model_text import model_as_text


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

        A backend that offers the user a way out asks `close_question` on
        every one of them before it takes it, because closing writes nothing
        and a session that is closed with something in the buffer loses it.
        What is asked is the model's to say and how it is asked is the
        backend's, which is the same split as everything else here.

        Args:
            model: Model to show. The backend reads and edits the model, and
                never touches the caller's configuration object.
        """


class DumpEditor:  # pylint: disable=too-few-public-methods
    """A backend that prints the model instead of opening a window.

    It satisfies `EditorBackend` and is not a special case beside a real
    backend, which is worth noticing: the protocol asks for one method, so
    anything with that method can be handed to `edit`. That is also how an
    application writes a backend of its own.

    It runs to completion in the sense the protocol asks for, and there is
    simply nothing for the user to do while it runs: it prints once and
    returns. So it is the backend of a program that says what a configuration
    file amounts to rather than one that offers to change it, and whoever runs
    such a program has no later moment at which to press Save. Saving is
    therefore the caller's to ask for, before the model is handed over.

    For the same reason it asks nothing before it ends. There is no session
    for a user to close and nobody to answer a question, so what a session
    that ends here does with a buffer that was never saved is settled: it
    ends, which is the only thing it could ever have done.
    """

    def run_editor(self, model: EditModel) -> None:
        """Validate the buffer and print the model as text.

        Validating is what makes the printed model say what the application
        itself would make of the values in it, which is the whole point of
        printing them. A save that the caller already asked for has validated
        them too, and says so on the line about saving.

        Args:
            model: Model to print.
        """
        model.validate()
        print(model_as_text(model))
