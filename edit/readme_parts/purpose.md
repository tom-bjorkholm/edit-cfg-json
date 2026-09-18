## What this package does

`{{dist_name}}` is the user interface agnostic core. It holds everything
that is not a widget:

- discovery of the editable structure of a `config_as_json.Config` object
  by introspection, so the application does not describe its schema twice:
  its members, what the declaration of each of them says, the values inside
  its lists and dicts, and the nested configuration objects that own a region
  of the tree
- the edit buffer, its per-field state, the tree of rows, the fold structure,
  what is being looked for and where the search looks, and what a node offers
  about how many things it holds
- validation, by applying the buffer to a copy of the configuration object and
  running the application's own validators rather than by inspecting them
- loading, including making automatic changes to an old format file
  visible to the user, and saving, including what becomes of the file that a
  save writes over
- which user interface an editor is opened in, where the program has not
  chosen one: each installed backend registers itself, says whether it can
  run on this machine, and is opened or passed over accordingly

This package installs the program `{{dist_name}}`, which opens the editor the
machine can run, and has the utility `python3 -m {{import_name}}.dump`, which
runs non-interactively on top of the backend API.

Install this package on its own if you are writing a new user interface
backend, or if your application has no user interface of its own and lets its
users install whichever editor they want. If you want an editor of your own
choosing, install one of the backends instead; they pull this package in.
