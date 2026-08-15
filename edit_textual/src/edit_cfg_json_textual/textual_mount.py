#! /usr/bin/env python3
"""The editor in an area, or on a screen, of an application that runs Textual.

An application with no Textual of its own calls `edit_cfg_json_textual.edit`,
which owns the terminal and runs until the user is done. An application that
already runs Textual cannot use that: `App.run` calls `asyncio.run`, so
calling it from inside a running application raises or deadlocks. It mounts
`EditorPanel` in an area of its own screen, or pushes `EditorScreen` to give
the editor the terminal for a while.

Both read the configuration themselves and take the keywords of
`edit_cfg_json.edit`, so an application says the same things about a session
whichever way it opens the editor.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from collections.abc import Callable
from typing import Optional, TextIO
import sys
from config_as_json import Config, PathOrStr
import edit_cfg_json as core
from edit_cfg_json_textual.textual_panel import ModelPanel
from edit_cfg_json_textual.textual_screen import ModelScreen


class EditorPanel(ModelPanel):
    """One editor of a configuration, as a widget to mount.

    The application mounts it where it likes and keeps its own header, its own
    footer and its own command palette. Mounting never blocks: `on_close` says
    that the session has ended, and `saved_config` says what came of it.
    """

    # Every keyword says one independent thing about the session, exactly as
    # `edit_cfg_json.edit` takes them.
    # pylint: disable-next=too-many-arguments
    def __init__(self, config: Config, *,
                 on_close: Optional[Callable[[], None]] = None,
                 descriptions: Optional[core.Descriptions] = None,
                 in_file: Optional[PathOrStr] = None,
                 loader: Optional[core.ConfigLoader] = None,
                 out_file: Optional[PathOrStr] = None,
                 policy: core.LoadPolicy = core.DEFAULT_POLICY,
                 settings: core.SettingsSource = core.Settings(),
                 stderr_file: TextIO = sys.stderr) -> None:
        """Read the configuration and show it in this widget.

        Args:
            config: Configuration object to edit. It is never modified.
            on_close: What the application does once the session has ended,
                or None for one that reads `saved_config` some other way.
            descriptions: What the application says about the members it
                declares, or None when it says nothing.
            in_file: File to read, or None to start from the declared
                defaults.
            loader: How this application constructs its configuration, or
                None for a class the editor can construct on its own.
            out_file: File to write, or None to write the input file.
            policy: What to do about declared keys the input file does not
                hold.
            settings: What this application has already decided about key
                combinations and file names, or a callable answering with it.
            stderr_file: Stream used for user-facing diagnostics.

        Raises:
            ConfigLoadError: The input file cannot be opened for editing.
        """
        super().__init__(core.editor_model(config, descriptions=descriptions,
                                           in_file=in_file, loader=loader,
                                           out_file=out_file, policy=policy,
                                           settings=settings,
                                           stderr_file=stderr_file),
                         on_close=on_close)


class EditorScreen(ModelScreen):
    """One editor of a configuration, as a screen to push.

    It is `EditorPanel` with a header, a footer and the palette entries of the
    editor around it, and it takes itself off the application when the session
    ends. Pushing it never blocks: `on_close` says that the session has ended,
    and `saved_config` says what came of it.
    """

    # See the disable in `EditorPanel`: the keywords of a session are the same.
    # pylint: disable-next=too-many-arguments
    def __init__(self, config: Config, *,
                 on_close: Optional[Callable[[], None]] = None,
                 descriptions: Optional[core.Descriptions] = None,
                 in_file: Optional[PathOrStr] = None,
                 loader: Optional[core.ConfigLoader] = None,
                 out_file: Optional[PathOrStr] = None,
                 policy: core.LoadPolicy = core.DEFAULT_POLICY,
                 settings: core.SettingsSource = core.Settings(),
                 stderr_file: TextIO = sys.stderr) -> None:
        """Read the configuration and show it on this screen.

        Args:
            config: Configuration object to edit. It is never modified.
            on_close: What the application does once the session has ended,
                or None for one that reads `saved_config` some other way. The
                screen has taken itself off the application by then.
            descriptions: What the application says about the members it
                declares, or None when it says nothing.
            in_file: File to read, or None to start from the declared
                defaults.
            loader: How this application constructs its configuration, or
                None for a class the editor can construct on its own.
            out_file: File to write, or None to write the input file.
            policy: What to do about declared keys the input file does not
                hold.
            settings: What this application has already decided about key
                combinations and file names, or a callable answering with it.
            stderr_file: Stream used for user-facing diagnostics.

        Raises:
            ConfigLoadError: The input file cannot be opened for editing.
        """
        super().__init__(core.editor_model(config, descriptions=descriptions,
                                           in_file=in_file, loader=loader,
                                           out_file=out_file, policy=policy,
                                           settings=settings,
                                           stderr_file=stderr_file),
                         on_close=on_close)
