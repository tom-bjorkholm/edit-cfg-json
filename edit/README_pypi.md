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
from edit_cfg_json import ConfigLoadError, EditModel, EditorBackend, \
    LoadPolicy, LoadReport, LoadedConfig, MemberRow, ValidationVerdict, \
    load_config, load_text, model_as_text, model_title, row_marks, \
    row_value_text, verdict_text
````

| Name | What it is |
| --- | --- |
| `EditModel` | The editable state of one `config_as_json.Config` object, discovered by looking at that object. Its members keep the order the configuration class declares them in, their values are held in JSON space, `set_text` writes the text of one edit field into one of them, and `validate` runs the application's own validation over the whole buffer. |
| `MemberRow` | One configuration member of the model: the path that addresses it, the value it holds now, the value it started with, and the flags that say what has happened to it. |
| `ValidationVerdict` | What one validation pass found: whether the application itself would accept the buffer, and the diagnostics it would produce. `EditModel.verdict` is the verdict of the last pass, or `None` while the buffer has not been validated since it last changed. |
| `load_config` | Reads the configuration to edit from one input file, or hands back the caller's own object when there is no file. It constructs the configuration class itself, because a load policy and the reporting of automatic changes are given to a constructor and to nothing else. |
| `LoadPolicy` | What to do about a declared value the input file does not hold: `STRICT`, `DEFAULTS`, or `STRICT_THEN_DEFAULTS`, which is the default. |
| `LoadedConfig` | What `load_config` returns: the object to edit, and the report of its load. |
| `LoadReport` | What one load did beyond reading the values: what the user has to be told, and the names of the members the declared defaults supplied. It is handed to `EditModel`, which marks those members. |
| `ConfigLoadError` | The refusal of an input file that cannot be opened, holding the message for the user and the diagnostics the configuration class produced. |
| `EditorBackend` | The protocol a user interface implements. It is phrased against `EditModel`, so a backend can also be mounted by an application that runs its own event loop. |
| `model_as_text` | The plain text rendering of a whole model, used by the examples and by the tests so that the editor can be observed without a display. It begins with what the load did and ends with the validation state, so a rendering never leaves either of them unsaid. |
| `model_title` | The label of a whole model, marked while the buffer holds a change worth saving. Both backends show it, so neither of them decides on its own how an unsaved change looks. |
| `load_text` | What reading the input file did, as text, and nothing at all when it did nothing worth saying. Both backends show it, so the two of them cannot tell the user two different things about one file. |
| `row_marks` | The marks of one member: that the input file did not hold it, that the user changed it, and that a validation pass then rewrote what the user wrote. All of them can apply at once. |
| `row_value_text` | The value of one member as the text a field shows. A string is shown as the string itself, without the quotation marks that the file format puts around it. Both backends use it, so neither of them formats values itself. |
| `verdict_text` | The validation state of a model as text, with the diagnostics below it. Both backends show it, so the two of them cannot describe one verdict differently. |

The package is under construction. This version reads a flat configuration
from a file, edits it in memory and validates it; saving follows. A member
whose value is a list or a dict is reported as a row that cannot be edited
yet rather than being left out.

## Reading the input file

`load_config` constructs the configuration class rather than taking an
already loaded object, because the two things a load has to be told are given
to a constructor and to nothing else: the policy for declared keys the file
does not hold, and the hook that reports the automatic changes of an old
format file. The hook is passed on only to a class that declares it, since
the constructor that `config_as_json` documents does not.

A value the file leaves out is filled in from the declared default of the
class, and that member is marked, so the user can see which values are not
the ones the file asked for. Every other way in which an input file can be
wrong is a refusal with a message of its own: a key the configuration does
not declare, text that cannot be read as configuration, values a validator
refuses, and a file that cannot be read at all.

`config_as_json` reports a missing key and an unknown key as the same
`KeyError`, and the two are told apart by retrying the load with the defaults
filling in: that rescues a file which is merely incomplete, and it still
refuses an unknown key. Nothing anywhere reads the text of a message to
decide which of the two it was.

A file whose values a validator refuses cannot be opened. A member validator
returns the value that is stored back into the member, so a load that stopped
part way through leaves it unknown which values were already rewritten and
which were not, and there is then nothing honest to show.

Text that is not a valid value yet is kept as it was typed rather than
refused, because a value that is being typed is not valid for most of the
time it takes to type it. What is wrong with it is said by the application's
own configuration class and not by any rule of this package: a validation
pass writes the buffer as JSON, constructs that class from it, and reports
what the class says. There is no second implementation of validation
anywhere, so a validator that an application writes for itself works here
without this package knowing anything about it.

A validation pass is not read only. A member validator returns the value
that is stored back into the member, so a validator such as one that changes
the case of a string rewrites what the user typed. The buffer is refreshed
from the configuration object that was accepted, and every value the pass
rewrote is marked, because changing what the user just typed without showing
it would be the worst of the available behaviours.

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

- Test result: 490 passed in 7s
- No flake8 warnings.
- No mypy errors found.
- No pylint warnings.
- No python layout warnings.
- Built version(s): 0.0.1
- Build and test using Python 3.14.6
