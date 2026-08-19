There are 3 related packages for editing a `config-as-json`
configuration:

- **[edit-cfg-json-tk](https://pypi.org/project/edit-cfg-json-tk/)** a
  desktop editor based on Tkinter. It is a thin backend on top of the
  core.

- **[edit-cfg-json-textual](https://pypi.org/project/edit-cfg-json-textual/)**
  a terminal editor based on Textual. It is a thin backend on top of the
  core.

- **[edit-cfg-json](https://pypi.org/project/edit-cfg-json/)** the user
  interface agnostic core. It discovers the editable structure of a
  `config_as_json.Config` object by introspection, and owns all editing,
  validation and file handling. It is also the package a third party
  writes a new user interface backend against. The only backend it ships
  itself is a very limited non-interactive one that prints the model once
  and returns, for a script, a test or a continuous integration job.

The application supplies its own `Config` object and gets a folding,
searchable editor for it, without writing any user interface code and
without describing its configuration schema a second time.

The three packages share a version number and are released together. The
first two are the editors: pick the one that matches how your application
is used, and it pulls in the core itself.
