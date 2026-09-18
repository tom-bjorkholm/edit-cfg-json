#! /usr/bin/env python3
"""One editing session, from the input file to what was saved.

`editor_model` reads the input file and returns the model of one session.
`edit` is that model run in a backend that owns a window, and the embedding
entry points of the two backend packages are that model mounted in a window
an application owns. All three take the same few keywords, so an application
says the same things about a session however it opens the editor.

`edit_in_ui` is `edit` for a caller with no user interface of its own and
therefore no reason to have chosen one: it names no backend and the editor
opens in whichever of the installed ones this machine can run.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from typing import Optional, TextIO
import sys
from config_as_json import Config, PathOrStr
from edit_cfg_json.backend import EditorBackend
from edit_cfg_json.descriptions import Descriptions
from edit_cfg_json.edit_model import EditModel
from edit_cfg_json.loader import ConfigLoader
from edit_cfg_json.loading import DEFAULT_POLICY, LoadPolicy, load_config
from edit_cfg_json.settings import Settings, SettingsSource
from edit_cfg_json.ui_choice import chosen_ui


# Every argument after the configuration is an optional keyword, and each of
# them is one independent thing an application may want to say about a
# session. Bundling them into an object to satisfy the count would make the
# entry points of this library harder to use than what they save.
# pylint: disable-next=too-many-arguments
def editor_model(config: Config, *,
                 descriptions: Optional[Descriptions] = None,
                 in_file: Optional[PathOrStr] = None,
                 loader: Optional[ConfigLoader] = None,
                 out_file: Optional[PathOrStr] = None,
                 policy: LoadPolicy = DEFAULT_POLICY,
                 settings: SettingsSource = Settings(),
                 stderr_file: TextIO = sys.stderr) -> EditModel:
    """Read one configuration from a file and return the model to edit it.

    Args:
        config: Configuration object saying which class to edit and what its
            declared defaults are. It is never modified.
        descriptions: What the application says about the members it
            declares, or None when it says nothing.
        in_file: File to read, or None to start from the declared defaults.
        loader: How this application constructs its configuration, or None for
            a class the editor can construct from the signature it declares.
        out_file: File to write, or None to write the input file.
        policy: What to do about declared keys the input file does not hold.
        settings: What the application around the editor has already decided,
            or a callable that answers with it.
        stderr_file: Stream used for user-facing diagnostics.

    Returns:
        The model of one editing session, ready to be shown.

    Raises:
        ConfigLoadError: The input file cannot be opened for editing.
    """
    loaded = load_config(config=config, in_file=in_file, policy=policy,
                         settings=settings, loader=loader)
    model = EditModel(config=loaded.config, report=loaded.report,
                      descriptions=descriptions, loader=loader,
                      out_file=in_file, settings=settings,
                      stderr_file=stderr_file)
    # A destination this call names is one that was chosen for this session,
    # so it gets the extension of the application when it has none of its
    # own. The input file is inherited rather than chosen, and is taken
    # exactly as it is: reading one file while writing another because the
    # two names differ by an extension would be a surprise.
    if out_file is not None:
        model.set_out_file(out_file)
    return model


# See the disable above: the keywords of a session are the same here.
# pylint: disable-next=too-many-arguments
def edit(config: Config, backend: EditorBackend, *,
         descriptions: Optional[Descriptions] = None,
         in_file: Optional[PathOrStr] = None,
         loader: Optional[ConfigLoader] = None,
         out_file: Optional[PathOrStr] = None,
         policy: LoadPolicy = DEFAULT_POLICY,
         settings: SettingsSource = Settings(),
         stderr_file: TextIO = sys.stderr) -> Optional[Config]:
    """Edit one configuration and return the object that was saved.

    The backend is a parameter because the core never imports a user
    interface library, so it cannot name one. Each backend package also has
    an `edit` of its own that supplies itself, which is the shorter door for
    an application that has already chosen its user interface. An application
    that already runs that user interface mounts the editor instead, with the
    entry point of its backend package, and `editor_model` is what those two
    ways of opening the editor have in common.

    Without an output file the input file is written, which is what an
    editor is normally asked to do. With neither, there is nowhere to write
    and the backend asks the user for a destination before it can save.

    Args:
        config: Configuration object saying which class to edit and what its
            declared defaults are. It is never modified, which is why the
            saved object is handed back rather than expected to be found in
            this one.
        backend: User interface to run this session in.
        descriptions: What the application says about the members it
            declares, or None when it says nothing. A configuration explains
            itself as far as it can without this — the docstring of its class
            labels the object — and a member no description reaches is shown
            without one.
        in_file: File to read, or None to start from the declared defaults.
        loader: How this application constructs its configuration, or None for
            a class the editor can construct from the signature it declares.
            An application whose class needs a constructor argument this
            library knows nothing about says it here, and
            `edit_cfg_json.derived_loader` is the shortest way to say it.
        out_file: File to write, or None to write the input file. A name
            that has no extension gets the one the application uses for its
            configuration; the input file never does.
        policy: What to do about declared keys the input file does not hold.
        settings: What the application around the editor has already
            decided, or a callable that answers with it. The default is an
            application with no opinion, which is what this library had of
            its own before there were settings at all.
        stderr_file: Stream used for user-facing diagnostics.

    Returns:
        The configuration object that was written, or None when the session
        ended without anything being saved.

    Raises:
        ConfigLoadError: The input file cannot be opened for editing.
    """
    model = editor_model(config, descriptions=descriptions, in_file=in_file,
                         loader=loader, out_file=out_file, policy=policy,
                         settings=settings, stderr_file=stderr_file)
    backend.run_editor(model)
    return model.saved_config


# See the same disable above: this takes the keywords of a session, and the
# one thing it says instead of naming a backend.
# pylint: disable-next=too-many-arguments
def edit_in_ui(config: Config, *, ui_name: Optional[str] = None,
               descriptions: Optional[Descriptions] = None,
               in_file: Optional[PathOrStr] = None,
               loader: Optional[ConfigLoader] = None,
               out_file: Optional[PathOrStr] = None,
               policy: LoadPolicy = DEFAULT_POLICY,
               settings: SettingsSource = Settings(),
               stderr_file: TextIO = sys.stderr) -> Optional[Config]:
    """Edit one configuration in a user interface this machine can run.

    This is `edit` for an application that has no user interface of its own
    and therefore no reason to have chosen one: instead of naming a backend it
    names nothing, and the editor opens in the best of the user interfaces
    that are installed and can run in this context. A command that lets its
    own user say which builds the choices of that option with
    `edit_cfg_json.available_uis`, so that it offers exactly the ones that
    would work.

    Everything else it does is `edit`, and every keyword means there what it
    means here.

    Args:
        config: Configuration object saying which class to edit and what its
            declared defaults are. It is never modified.
        ui_name: Name of the user interface to open the editor in, or None
            to open the one this machine can best run. The names are the ones
            `edit_cfg_json.available_uis` answers with.
        descriptions: What the application says about the members it
            declares, or None when it says nothing.
        in_file: File to read, or None to start from the declared defaults.
        loader: How this application constructs its configuration, or None for
            a class the editor can construct on its own.
        out_file: File to write, or None to write the input file.
        policy: What to do about declared keys the input file does not hold.
        settings: What the application around the editor has already decided,
            or a callable that answers with it. `ui_priorities` is the one of
            them this call reads before anything is opened.
        stderr_file: Stream used for user-facing diagnostics.

    Returns:
        The configuration object that was written, or None when the session
        ended without anything being saved.

    Raises:
        ConfigLoadError: The input file cannot be opened for editing.
        NoEditorError: The user interface that was named cannot run here, or
            none was named and this machine can open no editor at all.
    """
    chosen = chosen_ui(ui_name=ui_name, settings=settings)
    return edit(config, backend=chosen.backend(), descriptions=descriptions,
                in_file=in_file, loader=loader, out_file=out_file,
                policy=policy, settings=settings, stderr_file=stderr_file)
