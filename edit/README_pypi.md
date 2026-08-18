# edit-cfg-json

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

The application supplies its own `Config` object and gets a folding
editor for it, without writing any user interface code and without
describing its configuration schema a second time.

The three packages share a version number and are released together. The
first two are the editors: pick the one that matches how your application
is used, and it pulls in the core itself.

## Project status

**Alpha. No API stability and no backward compatibility is offered while
this package is in Alpha.** That applies to the core and to both
backends. Public names may change without a major version bump.

Semantic versioning starts when the Alpha period ends. Until then, pin an
exact version if your build needs to be reproducible.

### Stable exception: Descriptions

A library or a program that only does

```python
from edit_cfg_json import Descriptions
```

and then uses the `Descriptions` type definition can safely use the
latest version of `edit_cfg_json` in its declared dependencies with
`install_requires = [ 'edit_cfg_json >=`...
That type definition will be kept stable (or at least backward
compatible).

## What this package does

`edit-cfg-json` is the user interface agnostic core. It holds everything
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

This package has the utility `python3 -m edit_cfg_json.dump` that
runs non-interactively on top of the backend API.

Install this package on its own if you are writing a new user interface
backend. If you want an editor, install one of the backends instead; they
pull this package in.

## Main entry points

Everything a user of this package needs is re-exported from the top-level
`edit_cfg_json` package, so nothing has to be imported from an internal
module. These are the names an application starts with:

````python
from edit_cfg_json import Descriptions, EditModel, LoadPolicy, Settings, \
    edit, editor_model, load_config
````

| Name | What it is |
| --- | --- |
| `edit` | The whole of an editing session in one call: read the input file, build the model, run a backend to completion, and give back the configuration object that was saved, or `None` when nothing was. The backend is a parameter because this package never imports a user interface library; each backend package exports an `edit` of its own that supplies itself. |
| `editor_model` | The first half of `edit` on its own: read the input file and give back the model of one session, for an application that shows that model itself. It takes every keyword `edit` takes except the backend, so a session is described in the same words whichever way the editor is opened. |
| `EditModel` | The editable state of one `config_as_json.Config` object, discovered by looking at that object: the tree of rows, what has happened to each of them, `validate` over the whole buffer, and `save`. |
| `Descriptions` | What the application says about the members it declares: a mapping from the absolute `config_as_json.ConfigPath` of a member to the text that explains it. It is the one type alias this library declares, and the one name that stays stable through Alpha. |
| `Settings` | What the application around the editor has already decided: the key combinations of its actions, what one of its own configuration files is called, and what becomes of a file that a save writes over. Every attribute has a default, so an application with no opinion passes nothing at all. |
| `load_config`, `LoadPolicy` | Reading the input file into the application's own class, under a policy for declared values the file does not hold. `edit` and `editor_model` do this themselves; this is the door for an application that wants the loaded object first. |

That is what an application uses. Writing a user interface backend, or a
program on top of this one, needs the rest of the public API — `EditorBackend`
and `DumpEditor`, the rows and their marks, the `Emphasis` vocabulary, the
questions to ask before closing and before overwriting a file, `ConfigLoader`,
`run_cli` and `ExitCode` — and every public name of this package is described
in
[the api document](https://github.com/tom-bjorkholm/edit-cfg-json/blob/master/doc/edit-cfg-json_api.md).

## What the editor makes of a configuration class

### A tree of rows, and folding

A configuration worth editing is not a handful of scalars. A member may hold a
list, a dict, a nested `config_as_json.Config` object, a list of such objects
or a dict of them, and the model is one tree over all of it: the members in the
order the class declares them, every value inside a container a row of its own
with a field at it, and every node addressed by the absolute
`config_as_json.ConfigPath` to it.

A nested configuration object is a node and not the dict it serializes to: its
row says its class, its own docstring is below it, and its members are the rows
under that in the order *its* class declares them. Any node that holds rows can
be folded away and opened again, and which of them are folded belongs to the
model, so that two user interfaces of one application cannot be folded
differently. A container starts open unless opening it would flood the window.

### How many things a member holds

A member is a list or a dict because **how many** of them there are is a
decision of whoever configures the application, so a container can be given an
element, one can be taken out, and an element of a list can change places with
a neighbour. A new element is copied and never invented: from the class that
the declaration names, or from the values the class declares for the member,
and failing both from the first element the member holds now. A container that
can be given nothing says why below itself rather than offering a control that
would refuse every press.

### Validation, by running the application's own validators

A validation pass writes the buffer as JSON, applies it to a copy of the
configuration object of the session, and reports what the class said. There is
no second implementation of validation anywhere, so a `MemberValidator` an
application wrote for itself works here without this package knowing anything
about it, and the editor cannot accept something the application later rejects.

What was said about one member is shown **below that member**, and every
refused member is named at once rather than one per round. A rule that is about
no single member stays in the verdict below the rows. A nested object is also
asked what it is *on its own*, which is a badge on its row and not the verdict
of the whole configuration: a rule of the class above may relate two objects
across the boundary between them and refuse a configuration in which every
object is valid on its own.

A pass is not read only. A member validator returns the value that is stored
back into the member, so a validator that changes the case of a string rewrites
what the user typed, and every value a pass rewrote is marked.

### Explaining the values to the user

Two sources of explanatory text, independent of each other and both optional.
The docstring of the configuration class labels the configuration and the
docstring of each nested class labels that object — nothing is passed for this,
the class has it and the editor reads it. A `Descriptions` mapping labels the
individual members, because a member has nothing of the kind at runtime:

````python
from edit_cfg_json import Descriptions, edit

DESCRIPTIONS: Descriptions = {
    ('max_items',): 'How many items one report may hold, from 1 to 100.',
    ('limits', '['): 'What every one of these limits means.',
    ('outputs', '[', 'parts', '[', 'width'): 'Width of one part, in columns.'}

saved = edit(config=config, backend=backend, descriptions=DESCRIPTIONS)
````

The `'['` step keeps its `config_as_json` meaning of every list element or
every dictionary value at that point, and it says `'['` at each step it has to,
so one line reaches that member of every object at any index and any key
however deep the shape goes. A selector that addresses no member is never used
and is never an error.

Every member says what kind of value it holds whether the application describes
it or not, and where a member holds an enum the names it accepts are said
instead. What lives inside a validator — a range, a set of allowed values — is
not read and never will be, so a limit is explained by the application in words
or not at all. All of it is under one toggle, because a user who knows this
configuration by heart wants the lines back.

### Reading the input file

`load_config` reads the file itself rather than taking an already loaded
object, because the policy for declared keys the file does not hold is decided
while the file is read. A value the file left out is filled in from the
declared default and that member is marked; every other way a file can be wrong
is a refusal with a message of its own.

**Reading a file is not always only reading it**, and the user has to be told
or the editor looks broken. The rules a class declares for reading an older
format, a normalization during parsing and the defaults filling in what was
missing all change what is on the screen, and one mechanism finds all three:
the values the load produced are written back to JSON and compared with the
text of the file. What the load *recorded* says why — so a member's mark can
say which older key its value was read from — which no comparison could find.

A class that needs a constructor argument of the application's own is told to
`edit` and `load_config` as a `ConfigLoader` instead, and `derived_loader` says
that in one line:

````python
loader = derived_loader(partial(AppConfig, known_teams=TEAMS))
````

### Writing the output file

Saving is validating and then writing, and it is refused wherever the
validation is: an editor that produced a file its own application could not
read would have failed at the one thing it is for. `out_file` defaults to
`in_file`; with neither, the model says there is nowhere to write and invents
nothing, because a file name is not something a library can guess.

The file a save writes over is a configuration somebody wrote, so its previous
content is kept before it is overwritten — under the destination name plus
`backup_suffix`, numbered and rotated where `backup_count` is above one — and
that happens once per destination per session, so that the second press of Save
does not push the configuration that was really there one number further away.
The keeping is after the validation and immediately before the write, so a
refused save keeps nothing.

Closing writes nothing, so an editor closed with something unsaved loses it:
`close_question` is what to ask first, and nothing at all when there is nothing
to lose. Whether the user is asked belongs here and how the question is put
belongs to each backend, which is the split this library makes everywhere.

### What the application has already decided

The editor runs inside an application that took some key combinations for
itself long before the editor was called, that knows what one of its own
configuration files is called, and that has decided how those files are looked
after:

````python
from edit_cfg_json import ActionSettings, Settings, edit

saved = edit(config=config, backend=backend, in_file='my_config.cfg',
             settings=Settings(actions=ActionSettings(save=('ctrl+w',)),
                               file_extension='.cfg',
                               extension_enforced=True,
                               backup_suffix='.old',
                               backup_count=3))
````

`ActionSettings` has one attribute per action of the editor, each holding every
combination that runs it, written in Textual's key names; the Tkinter backend
translates them into the notation of its own toolkit. `file_extension` is
`None` by default, which is no opinion: this library has none of its own about
what a configuration file is called.

The same answers are a configuration class of their own, `SettingsConfig`, so
they can be read from a file, edited in this editor like any other
configuration, and declared as one member of an application's own configuration
class. That is what the two editor programs read their own settings from.

This package installs no program: the editors are `edit-cfg-json-tk` and
`edit-cfg-json-textual`, and `python3 -m edit_cfg_json.dump --help` is a
small utility for whoever is writing a program on top of this one, printing
what a class makes of a file and answering with an exit code.

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

- Test result: 1692 passed, 3 deselected in 48s
- No flake8 warnings.
- No mypy errors found.
- No pylint warnings.
- No python layout warnings.
- Built version(s): 0.0.5
- Build and test using Python 3.14.7
