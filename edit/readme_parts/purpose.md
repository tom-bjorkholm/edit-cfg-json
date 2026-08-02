## What this package does

`{{dist_name}}` is the user interface agnostic core. It holds everything
that is not a widget:

- discovery of the editable structure of a `config_as_json.Config` object
  by introspection, so the application does not describe its schema twice
- the edit buffer, its per-field state, and the fold structure
- validation, by constructing a candidate configuration and running the
  application's own validators rather than by inspecting them
- loading, including making automatic changes to an old format file
  visible to the user, and saving

Install this package on its own if you are writing a new user interface
backend. If you just want an editor, install one of the backends instead;
they pull this package in.
