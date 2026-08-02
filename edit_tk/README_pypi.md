# edit-cfg-json-tk

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

`edit-cfg-json-tk` is the Tkinter desktop editor. It is a thin backend on
top of `edit-cfg-json`, which it installs as a dependency. All the
editing, validation and file handling logic lives in the core; this
package only draws it and forwards the user's actions.

Tkinter itself is not installable from PyPI. It comes with most Python
distributions, but on some Linux distributions it is a separate system
package, such as `python3-tk`.

## Main entry points

Everything a user of this package needs is re-exported from the top-level
`edit_cfg_json_tk` package, so it can be imported directly:

````python
from edit_cfg_json_tk import TkEditor
````

`TkEditor` is the Tkinter implementation of the `EditorBackend` protocol of
`edit-cfg-json`. It has the one method that protocol asks for:

````python
from edit_cfg_json import EditModel
from edit_cfg_json_tk import TkEditor

TkEditor().run_editor(EditModel(config))
````

The package is under construction. This first version opens a window
showing the configuration members read-only, with a button to close it.
Editing, validation and saving follow.

## Installing edit-cfg-json-tk

### On macOS and Linux

To install edit-cfg-json-tk on macOS and Linux, run the following command:

````sh
pip3 install --upgrade edit-cfg-json-tk
````

### On Microsoft Windows

To install edit-cfg-json-tk on Microsoft Windows, run the following command:

````sh
pip install --upgrade edit-cfg-json-tk
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

edit-cfg-json-tk is released under the MIT License. See the `LICENSE.txt`
file included in the distribution.

## Test summary

- Test result: 227 passed in 4s
- No flake8 warnings.
- No mypy errors found.
- No pylint warnings.
- No python layout warnings.
- Built version(s): 0.0.1
- Build and test using Python 3.14.6
