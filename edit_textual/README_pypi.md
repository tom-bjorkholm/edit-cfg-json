# edit-cfg-json-textual

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

## Project status

**The Alpha period is over.** From version 0.1.0 the three packages follow
semantic versioning: a public name is not removed, and what it means is not
changed, without a major version. That applies to the core and to both
backends.

### What is public

Everything a user of edit-cfg-json-textual needs is re-exported from the top-level
`edit_cfg_json_textual` package, so nothing has to be imported from an internal
module. That re-exported set is the public API, and it is what the promise
above is about. Anything this package holds that is not re-exported is
internal and may change in any release.

The three packages share a version number and are released together, so the
version of one of them says which version of the other two it was built
against.

## What this package does

`edit-cfg-json-textual` is the terminal editor. It is a thin backend on top of
`edit-cfg-json`, which it installs as a dependency together with
`textual`. All the editing, validation and file handling logic lives in
the core; this package only draws it and forwards the user's actions.

Use this backend when the application is used over ssh, in a container,
or anywhere else without a desktop.

## Main entry points

Everything a user of this package needs is re-exported from the top-level
`edit_cfg_json_textual` package:

````python
from edit_cfg_json_textual import EditorPanel, EditorScreen, TextualEditor, edit
````

`edit` is the short way in for an application that has already chosen Textual.
It is `edit_cfg_json.edit` with this package's backend filled in, and it gives
back the configuration object that was saved, or `None` when nothing was:

````python
from edit_cfg_json_textual import edit

saved = edit(config=config, in_file='my_config.json')
````

Every keyword of `edit_cfg_json.edit` except the backend is taken here too:
`descriptions` says what the members are for, `settings` says what the
application has already decided about keys and files, and `loader` is for a
class this library cannot construct on its own.

`EditorPanel` and `EditorScreen` are the same editor for an application that
**already runs Textual**. `edit` and `TextualEditor` cannot serve one of those:
`App.run()` calls `asyncio.run`, so calling it from inside a running
application raises or deadlocks. So these two are a separate entry point, they
read the configuration themselves in exactly the way `edit` does, and neither
of them blocks:

````python
from edit_cfg_json_textual import EditorPanel, EditorScreen

# in the application's own `compose`, for an area of its own screen
yield EditorPanel(config, in_file='my_config.json',
                  on_close=self.editor_gone)

# or pushed as a screen of its own
self.push_screen(EditorScreen(config, in_file='my_config.json',
                              on_close=self.editor_gone))
````

`EditorPanel` is a widget, so it goes wherever the application puts a widget
and the application keeps its own header, footer and command palette.
`EditorScreen` is that same panel with a header, a footer and the palette
entries of the editor around it, and it **takes itself off the application**
when the session ends, so an application that pushed it pops nothing.

What the application learns is `on_close`, which says that the session has
ended, and `saved_config` on the panel or the screen, which says what came of
it — a widget has no moment at which it could return anything.
`panel.close(ask_about_unsaved=True)` is how the application closes the editor
itself, from a button or a menu of its own.

**The keys of the editor are bound on the panel**, so Textual offers them while
the focus is inside the editor and never while it is elsewhere in the
application. They are priority bindings, so a user who presses Save while
typing into a field means Save. One combination is worth knowing about before
it surprises anybody: `ctrl+q` is the default close key of this editor and also
Textual's own key for quitting an application, and an application's binding is
offered the key first — so an application that wants the editor's close key to
work inside it gives the editor another one.

`TextualEditor` is the Textual implementation of the `EditorBackend` protocol
of `edit-cfg-json`, for an application that builds the model itself. Every
public name of this package, that one included, is described in
[the api document](https://github.com/tom-bjorkholm/edit-cfg-json/blob/master/doc/edit-cfg-json-textual_api.md).

## The edit-cfg-json-textual program

Installing this package also installs a program of the same name, so an
application author gets a Textual editor for their own configuration class
without writing a line of code. The screen it opens is the one this page
describes, on the class that was named. It is `edit_cfg_json.run_cli` with this
package's backend filled in, so the command line below is the same one that
`edit-cfg-json-tk` has; what differs is which of the two shows the
configuration.

### Telling it which class to edit

The class is told and never guessed. Exactly one of these says where it comes
from, and `--version` is the one of them that edits nothing:

| Option | Meaning |
| --- | --- |
| `--module MODULE` | Importable module that holds the class. This is the ordinary import path, so `PYTHONPATH` reaches a package that is not installed. |
| `--file PATH` | Python file that is not importable as a module. Its own folder goes to the front of the path, so a file that imports its neighbours works; a file that belongs to a package and uses a relative import is refused, with a message saying to use `--module` instead. |
| `--edit-settings` | The class is this editor's own settings, so a settings file is edited in this editor like any other configuration. |
| `--version` | Report the version of this program and of every package it is built on, and which of them PyPI has a newer release of. |

````sh
edit-cfg-json-textual --module myapp.config --class AppConfig -i /etc/myapp.json
edit-cfg-json-textual --file ./somewhere/cfg.py --class AppConfig
edit-cfg-json-textual --edit-settings -o ~/.edit-cfg-json-textual.cfg
edit-cfg-json-textual --version
````

**Importing a module runs it.** That is the same exposure as running the file
with `python`, and it is not guarded against, because a configuration class is
Python and reaching it means importing the module it is in.

### The rest of the command line

| Option | Meaning |
| --- | --- |
| `--class CLASS` | Name of the `config_as_json.Config` class in that module or file. |
| `--loader NAME` | Name of an `edit_cfg_json.ConfigLoader` there, for a class this editor cannot construct on its own. At least one of `--class` and `--loader` is needed and both are allowed: a loader that chooses its class by looking at the file is held to the one `--class` names. |
| `--descriptions NAME` | Name of an `edit_cfg_json.Descriptions` mapping there, saying what the members are for. Without it the members are shown with whatever their own types say about them. |
| `-i`, `--input` | Configuration file to read. Without it the editor starts from the values the class declares. |
| `-o`, `--output` | Configuration file to write. Without it the input file is written, which is what an editor is normally asked to do. |
| `--policy` | What to do about a declared value the file does not hold: `strict-then-defaults`, which is the default, `strict` or `defaults`. |
| `-c`, `--cfg` | Settings file that this run itself behaves according to, instead of the one the program would look for. |

A member has no docstring at runtime, so what a member is for is either in a
mapping like the one `--descriptions` names or nowhere at all. The docstring of
the configuration class needs no option, because the class carries it.

Whatever a loader needs beyond the four keyword arguments of `ConfigLoader` is
bound where the loader is written, for instance with `functools.partial`,
because a command line cannot supply an argument this library knows nothing
about. `edit_cfg_json.derived_loader` is one line for the ordinary case:

````python
make_config = derived_loader(partial(AppConfig, known_teams=TEAMS))
````

### The settings this program itself runs with

**The command line says what to edit and which files, and never how the editor
behaves.** The extension a configuration uses, the key combinations of the
actions and what becomes of a file that a save writes over are settings, and
`edit_cfg_json.SettingsConfig` is what lets them be written in a file. This
program uses the first of five that answers: the file `-c` names, the file
`$CFG_EDIT_CFG_JSON` names, `~/.edit-cfg-json-textual.cfg`, `~/.edit-cfg-json.cfg`, or
the values the editor would have chosen anyway. A file that was **named** must
be there; the two in the home folder are the lookup itself, so a step that
finds nothing is simply the next step.

Such a file need name only what it changes, and `-c` is what makes it per run
rather than only per user — an extension is a fact about the class being
edited, so an application whose files are called `.cfg` gets one of its own:

````json
{"actions": {"save": ["ctrl+w"]},
 "file_extension": ".cfg", "extension_enforced": true,
 "backup_suffix": ".old", "backup_count": 3}
````

`--edit-settings` is how one is edited in this editor itself: with `-i` it
reads the file that is there, and with no `-i` it starts from the values the
class declares, which is how a file that does not exist yet is made.

### How the run ends, and two smaller things

Each way of refusing has an exit code of its own, so this program is usable
from a script and from a continuous integration job: `0` when everything it was
asked to do was done, `2` for a command line that is wrong, and a number of its
own for each way a module, a file, a class, a loader or a settings file can
refuse to be read. They are `edit_cfg_json.ExitCode`, where each is named.
Closing an editor is not a failure, so a session the user closed ends with `0`
whatever is left in the fields.

The program is also reachable through the package it belongs to, for a machine
whose script folder is not on `PATH`, and it completes its own options and file
names with [argcomplete](https://pypi.org/project/argcomplete):

````sh
python3 -m edit_cfg_json_textual --module myapp.config --class AppConfig
eval "$(register-python-argcomplete edit-cfg-json-textual)"
````

## What the screen shows

The screen holds a header, then the label of the configuration, what the class
says about itself, what reading the input file did, and one row per node of the
configuration. Below those, and not scrolling with them, are the search, the
validation verdict, the saving line and the footer of keys. The label is marked
while the model holds a change worth saving.

| Key | What it does |
| --- | --- |
| `ctrl+r`, or `f5` | Validate |
| `ctrl+s` | Save |
| `ctrl+shift+s` or `f12` | Save as |
| `f1`, or `ctrl+g` | Explain, or Hide explanation |
| `f2`, or `ctrl+t` | Fold all, or Unfold all |
| `ctrl+f` | Find |
| `f3` | Find next |
| `ctrl+q` | Quit |

Those are the defaults of `edit_cfg_json.ActionSettings`, and an application
that needs one of these combinations for itself moves it, or empties it, in the
`actions` of its own `edit_cfg_json.Settings`. **Validate, Save, Save as,
Explain and the fold action are also in the command palette**, which `ctrl+p`
opens, so an action with no key at all stays reachable — and so does one whose
combination the terminal cannot deliver, which `ctrl+shift+s` is on a legacy
terminal that has nowhere to put the shift.

**Every change of a field goes straight into the model.**

**A container is a row and not a field.** The rows of what it holds are
indented below it, there is a field at every value, and the container row says
how many things it holds — or which class the object at it is — where a value
would be. A control at the left of the row folds it away, and the fold action
does the same to all of them at once, named for what the next press will do. A
configuration with nothing to fold is offered neither the action nor the column
that the controls sit in, so the values keep that width.

**A member of a configuration too big for the screen is looked for** in
the `Find:` field below the rows, which searches as it is typed. The
four tick-boxes beside it say where it looks — in the path of a member,
in its value, matching the case, and matching the whole of one of them
instead of any part — and each of them says what it means when the
pointer rests on it. The defaults are the path and the value, the case
ignored, and a part enough. What is found is opened if folding hid it,
scrolled into view and marked *(found)*; `f3` and the `next` control go
on to the next one, and pressing Enter in the field puts the cursor in
what was found, so it can be typed into at once. Both actions are in the
command palette as well.

**At the end of the line of a node are its element controls**: `Add`, `Del`,
`Up` and `Down`, and only the ones that node really offers. Adding an entry to
a dict opens a small screen that asks for the key, because nothing but the
person configuring the application knows what a new entry is called. A
container that can be given nothing gets no `Add` at all and says why below
itself instead.

**The same two controls give a value to a member that holds none**, and take
it away again. A member its class allows to hold nothing has two states rather
than a text in a field: while it holds a value it is an ordinary field offering
`Del`, and while it holds nothing its row says so where the value would be, has
no field, and offers `Add`. A declared place that holds one nested
configuration object or none is the same thing one step up, saying which class
is missing while it holds none. That is what tells an empty text apart from no
value at all, in either direction.

**Beside the class on the row of a nested object is what that object is on its
own**: *valid on its own*, or *refused on its own* with the member it was about
saying why below itself. A list or a dict of such objects says what the objects
in it amount to, because its row is the only one that folding leaves on the
screen. The qualifying words are the whole point — a rule of the class above
may refuse a configuration in which every object is valid on its own — so the
verdict line below the rows is the only thing that answers whether the file can
be saved.

**Validating** shows what the application's own configuration class would say
about the values that are in the fields, below the node each remark is about.
**Leaving a field** asks the smaller question of whether what was typed into it
means a value of that member at all, which is what an enum member name answers
only once it is fully typed. **Saving** writes the output file and refuses to
write values the application would not accept, leaving the file on disk exactly
as it was; it asks first before writing over a file this session has not
written, and says where the previous content was kept. **Save as** asks on a
small screen of its own, starting at the file that would be written now.
**Quitting** writes nothing, and asks whether unsaved changes may be dropped,
with the focus on the answer that keeps them.

**Explaining** shows or hides what the application says about these values: the
class docstring, the docstring of each nested object, the description of each
described member below its own field, what kind of value each member holds, and
why a container cannot be given an element. The editor opens with them shown,
and what is left when they are hidden is the first paragraph of the class
docstring. The action is named for what the next press will do — "Explain"
while they are hidden and "Hide explanation" while they are shown — because
"Explain" beside explanations that are already there would be offering
something that has been done.

**A configuration bigger than the terminal** is scrolled through: the rows
scroll while the verdict, the saving line and the footer stay where they are,
and a container that would add more rows than the editor opens at is folded to
begin with, so a long list does not fill the screen before the user has seen
the members below it.

**Each kind of text has a colour**, so that the explanations do not read as
loudly as the values and a refused validation does not read like an accepted
one. Which kind each piece of text is comes from `edit_cfg_json.Emphasis`, so
it is the same here as in the Tkinter backend; the colours are those of the
terminal's theme rather than colours named here, so the editor follows the
terminal into its light or its dark mode.

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

- For the programmer of an application that offers one of the two editors to
  its own users:
  [doc/application_programmers_guide.md](https://github.com/tom-bjorkholm/edit-cfg-json/blob/master/doc/application_programmers_guide.md)

- For whoever edits a configuration in one of the two editors:
  [doc/end_users_guide.md](https://github.com/tom-bjorkholm/edit-cfg-json/blob/master/doc/end_users_guide.md)

- Design and decisions:
  [doc/detailed_design.md](https://github.com/tom-bjorkholm/edit-cfg-json/blob/master/doc/detailed_design.md)

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

- Test result: 2005 passed, 3 deselected in 78s (0:01:18)
- No flake8 warnings.
- No mypy errors found.
- No pylint warnings.
- No python layout warnings.
- Built version(s): 0.1.0
- Build and test using Python 3.14.7
