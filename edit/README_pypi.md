# edit-cfg-json

There are 3 related packages for editing a `config-as-json`
configuration:

- **[edit-cfg-json](https://pypi.org/project/edit-cfg-json/)** the user
  interface agnostic core. It discovers the editable structure of a
  `config_as_json.Config` object by introspection, and owns all editing,
  validation and file handling. It is also the package a third party
  writes a new user interface backend against.

- **[edit-cfg-json-tk](https://pypi.org/project/edit-cfg-json-tk/)** a
  desktop editor based on Tkinter. It is a thin backend on top of the
  core.

- **[edit-cfg-json-textual](https://pypi.org/project/edit-cfg-json-textual/)**
  a terminal editor based on Textual. It is a thin backend on top of the
  core.

The application supplies its own `Config` object and gets a folding
editor for it, without writing any user interface code and without
describing its configuration schema a second time.

The three packages share a version number and are released together. Pick
the backend that matches how your application is used; both backends pull
in the core themselves.

## Project status

**Alpha. No API stability and no backward compatibility is offered while
this package is in Alpha.** That applies to the core and to both
backends. Public names may change without a major version bump.

Semantic versioning starts when the Alpha period ends. Until then, pin an
exact version if your build needs to be reproducible.

## What this package does

`edit-cfg-json` is the user interface agnostic core. It holds everything
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

## Main entry points

Everything a user of this package needs is re-exported from the top-level
`edit_cfg_json` package, so it can be imported directly:

````python
from edit_cfg_json import EditModel, EditorBackend, MemberRow, \
    model_as_text, row_value_text
````

| Name | What it is |
| --- | --- |
| `EditModel` | The editable state of one `config_as_json.Config` object, discovered by looking at that object. Holds its values in JSON space, that is as they are written to the configuration file. |
| `MemberRow` | One configuration member of the model: its name, its JSON space value, and whether this version can edit it. |
| `EditorBackend` | The protocol a user interface implements. It is phrased against `EditModel`, so a backend can also be mounted by an application that runs its own event loop. |
| `model_as_text` | The plain text rendering of a whole model, used by the examples and by the tests so that the editor can be observed without a display. |
| `row_value_text` | The value of one member as the text a field shows. Both backends use it, so neither of them formats values itself. |

The package is under construction. This first version reads a flat
configuration and shows it; editing, validation, reading a file and saving
follow. A member whose value is a list or a dict is reported as a row that
cannot be edited yet rather than being left out.

## Installing edit-cfg-json

### On macOS and Linux

To install edit-cfg-json on macOS and Linux, run the following command:

````sh
pip3 install --upgrade edit-cfg-json
````

### On Microsoft Windows

To install edit-cfg-json on Microsoft Windows, run the following command:

````sh
pip install --upgrade edit-cfg-json
````

## Documentation

- Design and decisions:
  [doc/design.md](https://github.com/tom-bjorkholm/edit-cfg-json/blob/master/doc/design.md)

- Public API:
  [edit-cfg-json](https://github.com/tom-bjorkholm/edit-cfg-json/blob/master/doc/edit-cfg-json_api.md),
  [edit-cfg-json-tk](https://github.com/tom-bjorkholm/edit-cfg-json/blob/master/doc/edit-cfg-json-tk_api.md),
  [edit-cfg-json-textual](https://github.com/tom-bjorkholm/edit-cfg-json/blob/master/doc/edit-cfg-json-textual_api.md)

- Protected API:
  [edit-cfg-json](https://github.com/tom-bjorkholm/edit-cfg-json/blob/master/doc/edit-cfg-json_protected_api.md),
  [edit-cfg-json-tk](https://github.com/tom-bjorkholm/edit-cfg-json/blob/master/doc/edit-cfg-json-tk_protected_api.md),
  [edit-cfg-json-textual](https://github.com/tom-bjorkholm/edit-cfg-json/blob/master/doc/edit-cfg-json-textual_protected_api.md)

- Worked examples:
  [examples/src/example](https://github.com/tom-bjorkholm/edit-cfg-json/blob/master/examples/src/example)

## License

edit-cfg-json is released under the MIT License. See the `LICENSE.txt`
file included in the distribution.

## Test summary

- Test result: 211 passed in 4s
- No flake8 warnings.
- No mypy errors found.
- No pylint warnings.
- No python layout warnings.
- Built version(s): 0.0.1
- Build and test using Python 3.14.6
