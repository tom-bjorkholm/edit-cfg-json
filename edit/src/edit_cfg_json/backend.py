#! /usr/bin/env python3
"""The protocol that every user interface backend implements.

The editors this library is for are the Textual one and the Tkinter one, and
each of them lives in a package of its own, because this package imports no
user interface library.

What is here beside the protocol is `DumpEditor`, which is a very limited
non-interactive backend: it prints the model once and returns. It is the one
backend that needs no user interface library at all, which is what makes it
useful for exercising this API without a display and for printing what a short
sequence of editor actions left behind. It is not an editor and is not the way
to see what one does.
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
    """A very limited non-interactive backend: it prints the model once.

    It is not one of this library's editors and is not how one is looked at.
    The editors are `edit_cfg_json_textual.TextualEditor` and
    `edit_cfg_json_tk.TkEditor`, and everything a user does — typing into a
    field, leaving one, pressing a control on a row, answering a question —
    happens in one of those and in neither this nor any other printout.

    What this is good for is the two things a non-interactive backend can do:
    exercising a feature over this API without a display, which is what a
    quick check, a script and an automated test need, and printing what a
    short sequence of editor actions left behind. Those are real uses, and
    they are the whole of them.

    It satisfies `EditorBackend` and is not a special case beside an
    interactive backend, which is worth noticing: the protocol asks for one
    method, so anything with that method can be handed to `edit`. That is also
    how an application writes a backend of its own, and this is the shortest
    one there is to read.

    It runs to completion in the sense the protocol asks for, and there is
    simply nothing for the user to do while it runs. So whoever runs it has no
    later moment at which to press Save, and saving is the caller's to ask
    for, before the model is handed over.

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

        An interactive backend does the opposite and waits to be asked, with a
        button or a key, because a user halfway through typing a value has not
        asked anything. Validating here is the consequence of having no later
        moment to be asked in, and not a different opinion about when a buffer
        should be validated.

        Args:
            model: Model to print.
        """
        model.validate()
        print(model_as_text(model))
