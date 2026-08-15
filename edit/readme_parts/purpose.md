## What this package does

`{{dist_name}}` is the user interface agnostic core. It holds everything
that is not a widget:

- discovery of the editable structure of a `config_as_json.Config` object
  by introspection, so the application does not describe its schema twice:
  its members, the values inside its lists and dicts, and the nested
  configuration objects that own a region of the tree
- the edit buffer, its per-field state, the tree of rows, the fold structure,
  and what a node offers about how many elements it holds
- validation, by applying the buffer to a copy of the configuration object and
  running the application's own validators rather than by inspecting them
- loading, including making automatic changes to an old format file
  visible to the user, and saving, including what becomes of the file that a
  save writes over

This package has the utility `python3 -m {{import_name}}.dump` that
runs non-interactively on top of the backend API.

Install this package on its own if you are writing a new user interface
backend. If you want an editor, install one of the backends instead; they
pull this package in.
