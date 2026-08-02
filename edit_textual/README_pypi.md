# edit-cfg-json-textual

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

`edit-cfg-json-textual` is the terminal editor. It is a thin backend on top of
`edit-cfg-json`, which it installs as a dependency together with
`textual`. All the editing, validation and file handling logic lives in
the core; this package only draws it and forwards the user's actions.

Use this backend when the application is used over ssh, in a container,
or anywhere else without a desktop.

## Main entry points

Everything a user of this package needs is re-exported from the top-level
`edit_cfg_json_textual` package, so it can be imported directly:

````python
from edit_cfg_json_textual import TextualEditor
````

`TextualEditor` is the Textual implementation of the `EditorBackend`
protocol of `edit-cfg-json`. It has the one method that protocol asks for:

````python
from edit_cfg_json import EditModel, load_config
from edit_cfg_json_textual import TextualEditor

loaded = load_config(config=config, in_file='my_config.json')
model = EditModel(config=loaded.config, report=loaded.report)
TextualEditor().run_editor(model)
````

The package is under construction. This version opens a terminal screen with
one edit field per configuration member, validates on `ctrl+r` and quits on
`ctrl+q`. Every change of a field goes straight into the model, and the
title is marked while the model holds a change worth saving. Saving follows.

Validating runs the validation of the application's own configuration class
and shows below the fields what that class would say about the values that
are in them. A pass is not read only: a validator returns the value that is
stored back into the member, so the fields are written back from the model
afterwards, and a member that a validator rewrote says so beside its field.

What reading the input file did is shown above the fields, when it did
anything, because it is what explains the marks below it: a member that the
file did not hold says so beside its field. Both the message and the marks
are read from the model, so the two backends cannot tell the user two
different things about one file.

Neither key is a plain letter, because an unmodified letter belongs to
whichever field has the focus: a user who types it expects to see it appear
in the field. `f5` validates as well, and is left out of the footer so that
one action is not named twice there; a function key is the one of the two
that a keyboard or a terminal is most likely not to deliver, which is why
the footer names `ctrl+r` instead.

## Installing edit-cfg-json-textual

### On macOS and Linux

To install edit-cfg-json-textual on macOS and Linux, run the following command:

````sh
pip3 install --upgrade edit-cfg-json-textual
````

### On Microsoft Windows

To install edit-cfg-json-textual on Microsoft Windows, run the following command:

````sh
pip install --upgrade edit-cfg-json-textual
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

edit-cfg-json-textual is released under the MIT License. See the `LICENSE.txt`
file included in the distribution.

## Test summary

- Test result: 490 passed in 7s
- No flake8 warnings.
- No mypy errors found.
- No pylint warnings.
- No python layout warnings.
- Built version(s): 0.0.1
- Build and test using Python 3.14.6
