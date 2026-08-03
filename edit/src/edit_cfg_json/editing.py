#! /usr/bin/env python3
"""One editing session, from the input file to what was saved.

This is the convenience wrapper and deliberately nothing more. Everything it
does an application can do for itself, in three statements, which is what an
application that already runs its own event loop has to do: read the file,
build the model, mount the backend.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from typing import Optional, TextIO
import sys
from config_as_json import Config, PathOrStr
from edit_cfg_json.backend import EditorBackend
from edit_cfg_json.edit_model import EditModel
from edit_cfg_json.loading import DEFAULT_POLICY, LoadPolicy, load_config


# Every argument after the backend is an optional keyword, and each of them
# is one independent thing an application may want to say about a session.
# Bundling them into an object to satisfy the count would make the one
# ergonomic entry point of this library harder to use than the three
# statements it saves.
# pylint: disable-next=too-many-arguments
def edit(config: Config, backend: EditorBackend, *,
         in_file: Optional[PathOrStr] = None,
         out_file: Optional[PathOrStr] = None,
         policy: LoadPolicy = DEFAULT_POLICY,
         stderr_file: TextIO = sys.stderr) -> Optional[Config]:
    """Edit one configuration and return the object that was saved.

    The backend is a parameter because the core never imports a user
    interface library, so it cannot name one. Each backend package also has
    an `edit` of its own that supplies itself, which is the shorter door for
    an application that has already chosen its user interface.

    Without an output file the input file is written, which is what an
    editor is normally asked to do. With neither, there is nowhere to write
    and the backend asks the user for a destination before it can save.

    Args:
        config: Configuration object saying which class to edit and what its
            declared defaults are. It is never modified, which is why the
            saved object is handed back rather than expected to be found in
            this one.
        backend: User interface to run this session in.
        in_file: File to read, or None to start from the declared defaults.
        out_file: File to write, or None to write the input file.
        policy: What to do about declared keys the input file does not hold.
        stderr_file: Stream used for user-facing diagnostics.

    Returns:
        The configuration object that was written, or None when the session
        ended without anything being saved.

    Raises:
        ConfigLoadError: The input file cannot be opened for editing.
    """
    loaded = load_config(config=config, in_file=in_file, policy=policy)
    model = EditModel(config=loaded.config, report=loaded.report,
                      out_file=in_file if out_file is None else out_file,
                      stderr_file=stderr_file)
    backend.run_editor(model)
    return model.saved_config
