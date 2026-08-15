#! /usr/bin/env python3
"""The editor of this package as a Textual application of its own.

It is the shortest of the three modules that make up this backend, and that is
the point of the split: `textual_panel` holds the whole editor, and
`textual_screen` gives it a header, a footer and a command palette. What is
left here is the one thing only an application may do, which is to own the
terminal and to end the process.

Everything this backend takes from the core is reached through `core`, which is
`edit_cfg_json` itself. A backend may use the public API of the core and
nothing else, and naming it at every call site is what makes that visible; it
also keeps the two backends from each holding the same block of twenty
imported names, which is a duplication with nothing to factor out, since
neither backend may import the other.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from typing import Optional, TextIO
import sys
from config_as_json import Config, PathOrStr
from textual.app import App
from textual.screen import Screen
import edit_cfg_json as core
from edit_cfg_json_textual.textual_ask import QUESTION_SCREENS
from edit_cfg_json_textual.textual_screen import ModelScreen

QUIT_ACTION = 'quit'
"""Name of the action of Textual itself that would end the application.

The editor answers for it as well as for its own, because the command palette
of Textual offers it and a way out that dropped the changes without a word
would be the one thing an editor must not do.
"""


class EditorApp(App[None]):
    """Textual application that edits one edit model and nothing else."""

    def __init__(self, model: core.EditModel) -> None:
        """Remember the model and name the terminal after its class.

        The title is the name of the class and not the label of the model,
        because the label says whether there is something unsaved and belongs
        beside the values that are unsaved. The Tk backend names its window
        the same way and for the same reason.

        Args:
            model: Model to show and to edit.
        """
        super().__init__()
        self._model = model
        self.title = model.config_type_name

    def get_default_screen(self) -> Screen[None]:
        """Return the screen this application shows, which holds the editor.

        Returns:
            One editor on a screen of its own, which ends this application
            when the session ends: there is nothing else for the application
            to show, so an editor that had gone would leave an empty terminal.
        """
        return ModelScreen(self._model, on_close=self.exit)

    async def action_quit(self) -> None:
        """End the session, asking first where there is something to lose.

        This is the action of Textual itself, which its command palette offers
        and which the editor would otherwise have no say in. It is the Close
        of the editor, so that every way out of this application asks the one
        question in the one place.
        """
        screen = self.screen
        if isinstance(screen, ModelScreen):
            screen.panel.close()
            return
        await super().action_quit()

    def check_action(self, action: str,
                     parameters: tuple[object, ...]) -> Optional[bool]:
        """Turn ending the application off while the editor asks something.

        The editor answers the same way for its own actions, and for the same
        reason: a priority binding is offered the key from the whole binding
        chain and not from the part of it above the last modal screen, so a
        question is only really modal if what is under it says so.

        Args:
            action: Name of the action that is about to run.
            parameters: Arguments of that action, of which this has none.

        Returns:
            None while a question of the editor is open and the action is the
            one that would end the application, and True otherwise.
        """
        _ = parameters
        if action == QUIT_ACTION and isinstance(self.screen, QUESTION_SCREENS):
            return None
        return True


class TextualEditor:  # pylint: disable=too-few-public-methods
    """Textual user interface backend for an edit model.

    The class has the single method that `EditorBackend` asks for, and
    deliberately nothing else: everything worth testing without a terminal
    lives in the core.

    It runs an application of its own, which is what that protocol promises
    and what an application that already runs Textual cannot use.
    `edit_cfg_json_textual.EditorPanel` and
    `edit_cfg_json_textual.EditorScreen` are for that one instead.
    """

    def run_editor(self, model: core.EditModel) -> None:
        """Show the model in a Textual screen until the user quits.

        Args:
            model: Model to show and to edit.
        """
        EditorApp(model).run()


# See the same disable in the core: every argument after the first is an
# optional keyword saying one independent thing about the session.
# pylint: disable-next=too-many-arguments
def edit(config: Config, *, descriptions: Optional[core.Descriptions] = None,
         in_file: Optional[PathOrStr] = None,
         loader: Optional[core.ConfigLoader] = None,
         out_file: Optional[PathOrStr] = None,
         policy: core.LoadPolicy = core.DEFAULT_POLICY,
         settings: core.SettingsSource = core.Settings(),
         stderr_file: TextIO = sys.stderr) -> Optional[Config]:
    """Edit one configuration in the terminal, and return what was saved.

    This is `edit_cfg_json.edit` with this package's backend filled in, for
    an application that has already chosen Textual. Everything it does is
    documented there.

    Args:
        config: Configuration object to edit. It is never modified.
        descriptions: What the application says about the members it
            declares, or None when it says nothing.
        in_file: File to read, or None to start from the declared defaults.
        loader: How this application constructs its configuration, or None for
            a class the editor can construct on its own.
        out_file: File to write, or None to write the input file.
        policy: What to do about declared keys the input file does not hold.
        settings: What this application has already decided about key
            combinations and file names, or a callable that answers with it.
        stderr_file: Stream used for user-facing diagnostics.

    Returns:
        The configuration object that was written, or None when nothing was.

    Raises:
        ConfigLoadError: The input file cannot be opened for editing.
    """
    return core.edit(config=config, backend=TextualEditor(),
                     descriptions=descriptions, in_file=in_file, loader=loader,
                     out_file=out_file, policy=policy, settings=settings,
                     stderr_file=stderr_file)
