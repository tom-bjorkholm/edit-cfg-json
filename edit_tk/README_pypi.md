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
from edit_cfg_json_tk import TkEditor, edit
````

`edit` is the short way in for an application that has already chosen
Tkinter. It is `edit_cfg_json.edit` with this package's backend filled in,
and it gives back the configuration object that was saved, or `None` when
nothing was:

````python
from edit_cfg_json_tk import edit

saved = edit(config=config, in_file='my_config.json')
````

`TkEditor` is the Tkinter implementation of the `EditorBackend` protocol of
`edit-cfg-json`, for an application that builds the model itself. It has the
one method that protocol asks for:

````python
from edit_cfg_json import EditModel, load_config
from edit_cfg_json_tk import TkEditor

loaded = load_config(config=config, in_file='my_config.json')
model = EditModel(config=loaded.config, report=loaded.report,
                  out_file='my_config.json')
TkEditor().run_editor(model)
saved = model.saved_config
````

The package is under construction. This version opens a window with one edit
field per configuration member and four buttons: Validate, Save, Save as and
Close. Every change of a field goes straight into the model, and the label
above the fields is marked while the model holds a change worth saving.

Validate runs the validation of the application's own configuration class
and shows below the fields what that class would say about the values that
are in them. A pass is not read only: a validator returns the value that is
stored back into the member, so the fields are written back from the model
afterwards, and a member that a validator rewrote says so beside its field.

Save writes the output file, and refuses to write values the application
would not accept: the diagnostics then say what is wrong with them and the
file on disk is left exactly as it was. Saving runs the same pass as Validate
does, so it can rewrite a value as well, and the fields show what really
reached the file. What was written is no longer waiting to be written, so the
mark above the fields goes away and the editor stays open.

Save as asks for the file with the ordinary system dialog, with no default
extension and no file type filter, because this library has no opinion about
what a configuration file is called. Save asks the same question when the
session has no file to write yet, which is what every editor does.

Close writes nothing of its own. It is the "cancel" of the editor, and it is
called Close rather than Cancel because saving leaves the editor open: a
button called Cancel beside values that have already been written would read
as an offer to undo the writing, which it is not.

What reading the input file did is shown above the fields, when it did
anything, because it is what explains the marks below it: a member that the
file did not hold says so beside its field. Both the message and the marks
are read from the model, so the two backends cannot tell the user two
different things about one file.

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

- Test result: 573 passed in 10s
- No flake8 warnings.
- No mypy errors found.
- No pylint warnings.
- No python layout warnings.
- Built version(s): 0.0.1
- Build and test using Python 3.14.6
