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
from edit_cfg_json_textual import EditorPanel, EditorScreen, TextualEditor, edit
````

`edit` is the short way in for an application that has already chosen
Textual. It is `edit_cfg_json.edit` with this package's backend filled in,
and it gives back the configuration object that was saved, or `None` when
nothing was:

````python
from edit_cfg_json_textual import edit

saved = edit(config=config, in_file='my_config.json')
````

`TextualEditor` is the Textual implementation of the `EditorBackend`
protocol of `edit-cfg-json`, for an application that builds the model
itself. It has the one method that protocol asks for:

````python
from edit_cfg_json import EditModel, load_config
from edit_cfg_json_textual import TextualEditor

loaded = load_config(config=config, in_file='my_config.json')
model = EditModel(config=loaded.config, report=loaded.report,
                  out_file='my_config.json')
TextualEditor().run_editor(model)
saved = model.saved_config
````

`EditorPanel` and `EditorScreen` are the same editor for an application that
**already runs Textual**. `edit` and `TextualEditor` cannot serve one of
those: `App.run()` calls `asyncio.run`, so calling it from inside a running
application raises or deadlocks, and `run_editor` promises to run until the
user is done, which an editor in one panel of somebody else's application can
never do. So these two are a separate entry point, and neither of them blocks:

````python
from edit_cfg_json_textual import EditorPanel, EditorScreen

# in the application's own `compose`, for an area of its own screen
yield EditorPanel(config, in_file='my_config.json',
                  on_close=self.editor_gone)

# or pushed as a screen of its own
self.push_screen(EditorScreen(config, in_file='my_config.json',
                              on_close=self.editor_gone))
````

Both read the configuration themselves in exactly the way `edit` does: after
the configuration object they take the keywords of `edit` less the backend —
`descriptions`, `in_file`, `loader`, `out_file`, `policy`, `settings` and
`stderr_file` — which all mean here what they mean there, because the same
`edit_cfg_json.editor_model` reads them.

`EditorPanel` is a widget, so it goes wherever the application puts a widget
and the application keeps its own header, its own footer and its own command
palette. `EditorScreen` is that same panel with a header, a footer and the
palette entries of the editor around it, for an application that wants the
editor to have the terminal for a while; it **takes itself off the
application** when the session ends, so the application's own screen is back
on top by the time it is told, and an application that pushed it pops nothing.

What the application learns is `on_close`, which says that the session has
ended, and `saved_config` on the panel or the screen, which says what came of
it — a widget has no moment at which it could return anything. `model` on
either of them is the whole model of the session, for an application that
wants more than the outcome.

`panel.close(ask_about_unsaved=True)`, and `screen.close(...)` for the other
shape, is how the application closes the editor itself, from a button or a
menu of its own. The editor's own Close and its quit key are that same call
with the default, so the question about what has not been saved is put in the
same words whichever of them ended the session; an application that is
shutting down for reasons of its own passes `False`, because it already has a
question to put and does not want two. Closing again once the session has
ended does nothing.

**The keys of the editor are bound on the panel**, so Textual offers them
while the focus is inside the editor and never while it is elsewhere in the
application. They are priority bindings, so a user who presses Save while
typing into a field means Save;
`edit_cfg_json.Settings.priority_keys` is how an application whose own widget
inside that area already reads one of these combinations says otherwise.

One combination is worth knowing about before it surprises anybody: `ctrl+q`
is the default close key of this editor and also Textual's own key for quitting
an application, and an application's binding is offered the key before a
panel's. An application that wants the editor's close key to work inside it
gives the editor another one, with
`Settings(actions=ActionSettings(quit=...))`, or offers a control of its own
that calls `close`.

## The edit-cfg-json-textual program

Installing this package also installs a program of the same name, so an
application author gets a Textual editor for their own configuration class
without writing a line of code:

````sh
edit-cfg-json-textual --module myapp.config --class AppConfig -i /etc/myapp.json
````

The screen it opens is the one this page describes, on the class that was
named. It is `edit_cfg_json.run_cli` with this package's backend filled in, so
the command line below is the same one that `edit-cfg-json-tk` has; what
differs is which of the two shows the configuration.

### Telling it which class to edit

The class is told and never guessed. `--module` names a module that is
importable, `--file` names a Python file that is not, `--edit-settings` says
that the class is this editor's own settings, exactly one of the three is
required, and `--class` names the class in the first two:

````sh
edit-cfg-json-textual --module myapp.config --class AppConfig -i /etc/myapp.json
edit-cfg-json-textual --file ./somewhere/cfg.py --class AppConfig
edit-cfg-json-textual --edit-settings -o ~/.edit-cfg-json-textual.cfg
````

`--module` uses the ordinary import path, so `PYTHONPATH` reaches a package
that is not installed. `--file` puts the folder of the file at the front of the
path and imports the file by its own name, so a file that imports its
neighbours works — but a file that belongs to a package and uses a relative
import cannot be loaded from a bare path at all, and is refused with a message
saying to use `--module` with `PYTHONPATH` instead.

**Importing a module runs it.** That is the same exposure as running the file
with `python`, and it is not guarded against, because a configuration class is
Python and reaching it means importing the module it is in.

### The rest of the command line

| Option | Meaning |
| --- | --- |
| `-i`, `--input` | Configuration file to read. Without it the editor starts from the values the class declares. |
| `-o`, `--output` | Configuration file to write. Without it the input file is written, which is what an editor is normally asked to do. |
| `--policy` | What to do about a declared value the file does not hold: `strict-then-defaults`, which is the default, `strict` or `defaults`. |
| `--descriptions` | Name of an `edit_cfg_json.Descriptions` mapping beside the class, saying what its members are for. Without it the members are shown with whatever their own types say about them, which for most of them is nothing. |

A member has no docstring at runtime, so what a member is for is either in a
mapping like that or nowhere at all, which is why `--descriptions` exists: it is
the one thing an application knows that this program could not otherwise pass
on. The docstring of the configuration class needs no option, because the class
carries it.

**The command line says what to edit and which files, and never how the editor
behaves.** The file name extension a configuration uses, the key combinations
that run the actions of the editor, and what becomes of a file that a save
writes over are settings, and there is no option for any of them: an
application says them in `edit_cfg_json.Settings` and reaches the editor
through `edit`, and this program reads every one of them from a settings file.
That is the next section, and `-c` is the one option about it.

### The settings this program itself runs with

The same answers `edit_cfg_json.Settings` holds are a configuration class of
their own, `edit_cfg_json.SettingsConfig`, so they can be written in a file.
This program looks for one in five steps, and uses the first that answers:

| Step | Where |
| --- | --- |
| 1 | The file that `-c`/`--cfg` names. |
| 2 | The file that the `CFG_EDIT_CFG_JSON` environment variable names. |
| 3 | `~/.edit-cfg-json-textual.cfg`, which only this program reads. |
| 4 | `~/.edit-cfg-json.cfg`, which every program of this library reads. |
| 5 | Nowhere: the values the editor would have chosen anyway. |

A file that was **named** — by `-c` or by the environment — must be there, and
a run whose named file is missing or cannot be read as settings stops with an
exit code of its own. The two files of the home folder are the lookup itself,
so a step that finds nothing is simply the next step.

Such a file need name only what it changes. This one moves Save and keeps three
of the files that a save writes over:

````json
{
    "actions": {"save": ["ctrl+w"]},
    "backup_suffix": ".old",
    "backup_count": 3
}
````

A settings file is what one **run** behaves according to, which is what `-c` is
for. The extension is a fact about the class being edited rather than about
whoever is running the program, so an application whose configuration files are
called `.cfg` gets a file of its own beside the one in the home folder:

````json
{"file_extension": ".cfg", "extension_enforced": true}
````

````sh
edit-cfg-json-textual -c ./myapp-editor.cfg --module myapp.config --class AppConfig \
    -i /etc/myapp.cfg
````

An enforced extension refuses an input file that does not have it, and refuses
a destination that does not have it either, so nothing is written. And a file
holding `{}` names nothing at all, which makes it step 5 of the table written
down: naming it is how a run asks for the values the editor would have chosen
anyway, past a file of the home folder that says something else.

`--edit-settings` is how one is edited in this editor itself. With `-i` it reads
the file that is there; with no `-i` it starts from the values the class
declares, which is how a settings file that does not exist yet is made:

````sh
edit-cfg-json-textual --edit-settings -o ~/.edit-cfg-json-textual.cfg
edit-cfg-json-textual --edit-settings -i ~/.edit-cfg-json-textual.cfg
````

The settings a run behaves according to are read before anything else, so a
session that is editing a settings file is not the session that file describes:
the next run reads it.

### A class this editor cannot construct on its own

Most configuration classes take the keyword arguments that `config_as_json`
documents and nothing else, and this program constructs them from the signature
it reads. A class that needs an argument of the application's own — a folder, a
connection, the list of names its own validators accept — is reached through
`--loader NAME` instead, which names an `edit_cfg_json.ConfigLoader` in the same
module or file:

````sh
edit-cfg-json-textual --module myapp.config --loader make_config -i /etc/myapp.json
````

Whatever the loader needs beyond the four keyword arguments of that protocol has
to be bound where the loader is written, for instance with
`functools.partial`, because a command line cannot supply an argument this
library knows nothing about. `edit_cfg_json.derived_loader` is one line for the
ordinary case:

````python
make_config = derived_loader(partial(AppConfig, known_teams=TEAMS))
````

At least one of `--class` and `--loader` is needed and both are allowed. A
loader may choose its class by looking at the file it is given, and `--class`
beside it is then how a script says which class it is prepared to go on with:
the run stops with its own exit code if the loader answers with another one.

### How the run ends

The program is meant to be usable from a script, so each way of refusing has an
exit code of its own:

| Code | What it means |
| --- | --- |
| `0` | Everything the program was asked to do was done. |
| `1` | The input file cannot be opened for editing. |
| `2` | The command line itself is wrong. |
| `3` | The module that `--module` names cannot be imported. |
| `4` | The file that `--file` names cannot be read. |
| `5` | That file is not Python that can be imported. |
| `6` | That file needs the package it belongs to. |
| `7` | The module holds no such name. |
| `8` | That name is not a class based on `config_as_json.Config`. |
| `9` | The editor cannot construct that class on its own. |
| `10` | The values are not ones the application would accept. |
| `11` | The output file was asked for and was not written. |
| `12` | The values of that class cannot be written as JSON, so there is nothing to show. |
| `13` | The name that `--loader` names cannot be called at all. |
| `14` | The loader needs arguments that a command line cannot supply. |
| `15` | The loader did not construct the class that `--class` asked for. |
| `16` | The name that `--descriptions` names is no mapping of any kind. |
| `17` | The settings of the program itself cannot be read. |

The numbers are `edit_cfg_json.ExitCode`, so a program that runs this one can
name them instead of writing them out.

Codes `10` and `11` are never answered by this program. They belong to a run
whose backend prints once and returns, which is the
`python3 -m edit_cfg_json.dump` utility of the core package.
A program that gave the user a session ends with success when the user closes
it, whatever is left in the fields, because closing an editor is not a failure.

### If the script folder is not on the path

This program is also reachable through the package it belongs to, which needs
nothing to be on `PATH`:

````sh
python3 -m edit_cfg_json_textual --module myapp.config --class AppConfig
````

### Completing the command line

The program completes its own options and file names with
[argcomplete](https://pypi.org/project/argcomplete), which is installed with
it. Register it once for your shell:

````sh
eval "$(register-python-argcomplete edit-cfg-json-textual)"
````

## What the screen shows

The screen holds a header, then what the configuration class says about itself,
what reading the input file did, and one row per node of the configuration.
Below those, and not scrolling with them, are the validation verdict, the saving
line and the footer of keys. The title is marked while the model holds a change
worth saving.

Every change of a field goes straight into the model. The keys are the ones the
application chose in the `actions` of its `edit_cfg_json.Settings`, and with an
application that chose nothing they are the defaults of
`edit_cfg_json.ActionSettings`:

| Key | What it does |
| --- | --- |
| `ctrl+r`, or `f5` | Validate |
| `ctrl+s` | Save |
| `ctrl+shift+s` or `f12` | Save as |
| `f1`, or `ctrl+g` | Explain, or Hide explanation |
| `f2`, or `ctrl+t` | Fold all, or Unfold all |
| `ctrl+q` | Quit |

### One row per node

A member that holds a list, a dict or a nested `config_as_json.Config` object
is not one field. It is a row of its own with the rows of what it holds
indented below it, a field at every value, and no field on the row of the
container itself — which says how many things it holds, or which class the
object at it is, where a value would be.

A container has a control at the left of its row, `-` while it is open and `+`
while it is folded, and pressing it hides or shows everything inside it. The
fold action does the same to all of them at once, and it is named for what the
next press will do — "Fold all" while anything is open, "Unfold all" once
nothing is — in the footer and in the command palette alike. A configuration
with nothing to fold is offered neither the action nor the column that the
controls sit in, so the values keep that width.

A nested configuration object shows its own docstring below its row and its own
members as the rows under that, in the order *its* class declares them. Folding
it leaves the first paragraph of that docstring, because an object showing less
of itself says less about itself.

### What one nested object is on its own

Beside the class on the row of a nested object is what that object is when it is
asked about itself: *valid on its own* or *refused on its own*. A list or a dict
of such objects says what the objects in it amount to — *valid inside* or
*refused inside* — because its row is the only one that folding leaves on the
screen.

Folding a node asks every object at or inside it, and so does opening one, so
the badge appears as soon as a container is folded out of the way. A member that
one of those objects refused says why below itself, exactly as the verdict of
the whole configuration does; what an object refused about no member of itself
is said at the object.

The words that qualify the badge are the whole point. A rule of the class above
may relate two objects across the boundary between them, and then every object
is valid on its own while the configuration cannot be written. The verdict line
below the rows is the only thing that answers whether the file can be saved.

### Changing how many things a member holds

At the end of the line of a node are the controls for its elements: `Add`,
`Del`, `Up` and `Down`, and only the ones that node really offers. They sit at
the end rather than in a column of their own, so a node that offers none of them
costs the values no width at all, which is what makes four of them affordable.

`Add` copies: a list or a dict whose class declares that its elements are
configuration objects gets one object of that class holding the values it
declares, and any other list gets a copy of the element the class declares for
it, or of the first element it holds now. Adding an entry to a dict opens a
small screen that asks for the key, because nothing but the person configuring
the application knows what a new entry is called; a key the dict already holds
is asked about again rather than allowed to take the place of what is there.

A container that cannot be given an element gets no `Add` at all, and says why
below itself instead — an ordinary dict member, for instance, because
`config_as_json` matches such a member against the keys its class declares, so
a dict that gained one would be refused by the configuration class itself. That
line is explanation rather than something to act on, so it is muted and the
explain action covers it.

### Validating, saving and quitting

Validating runs the validation of the application's own configuration class
and shows what that class would say about the values that are in the fields.
What it said about one node is shown **below that node**, and the line
below the rows names the nodes it was about, by the whole path to each of them,
so a configuration too tall for the terminal does not leave the user hunting for
the field. What the class said that is about no single node — a
whole-configuration rule, a key that does not match — stays in that line,
because there is no field it belongs to. Every refused node is marked at once,
and not only the first one, because the editor walks the validation plan itself
rather than stopping where `Config.validate()` stops.

A pass is not read only: a validator returns the value that is stored back
into the member, so the fields are written back from the model afterwards, and
a member that a validator rewrote says so beside its field. A pass can also
change how many rows there are — a validator that sorts a list and removes its
duplicates removes one — and the screen then builds its rows again rather than
writing into a widget for a value that is no longer there.

**Leaving a field** asks a smaller question of that one member: whether what
was typed into it means a value of that member at all. It is the question a
`parse_converters()` entry answers, an enum being the case that arises in
practice, and it is asked when the field loses the focus rather than on every
key, because a name that is being typed is no name of a member for most of
the time it takes to type it.

Saving writes the output file, and refuses to write values the application
would not accept: the diagnostics then say what is wrong with them and the
file on disk is left exactly as it was. Saving runs the same pass as
validating does, so it can rewrite a value as well, and the fields show what
really reached the file. What was written is no longer waiting to be written,
so the title loses its mark and the editor stays open.

Save as asks for the file in a small screen of its own, where `enter` writes
it and the `cancel` key, `escape` unless the application moved it, leaves the
question unanswered. The screen names that key itself, so it cannot tell the
user to press one that does nothing. `ctrl+s` asks the same question when the
session has no file to write yet, which is what every editor does. The
question starts at the file that would be written now, so saving a copy
beside the original is a matter of changing a few characters.

**A save that would write over a file this session has not written asks
first**, on a modal screen whose focus is on the answer that leaves the file
alone. The previous content is then kept under the name the application chose,
and the saving line says where it went. Both the question and the name are the
core's, so this backend and the Tkinter one cannot treat the user's old
configuration differently.

Quitting writes nothing of its own. It is the "cancel" of the editor; saving
leaves the editor open, and what has been saved has been saved.

**Quitting an editor that holds something unsaved asks whether the changes may
be dropped**, on a modal screen whose focus is on the answer that keeps them, so
that a user who presses `enter` without reading keeps what they have. Quitting
again after a Save asks nothing, because a save leaves nothing to lose.

Explaining shows or hides what the application says about these values: the
whole docstring of the configuration class above the rows, the docstring of
each nested object, the description of each described member below its own
field, what kind of value each member holds, and why a container cannot be
given an element. The editor opens with them shown, and what is left when they
are hidden is the first paragraph of the class docstring, because one line for
the whole configuration is worth keeping. A member the application described
gets a line and one it said nothing about gets none, rather than an empty one.
Which of the two states the editor is in belongs to the model, so this backend
and the Tk one cannot disagree about it.

The action is named for what the next press of it will do: it is "Explain"
while the explanations are hidden and "Hide explanation" while they are shown,
in the footer and in the command palette alike. "Explain" beside explanations
that are already there would be offering something that has been done. The Tk
backend answers the same question with a tick-box, which a footer cannot be.

What reading the input file did is shown above the rows, when it did
anything, because it is what explains the marks below it: a member that the
file did not hold says so beside its field, and so does one whose value the
reading of the file put there or altered — with the older key it was read from,
where the class recorded one. Both the message and the marks are read from the
model, so the two backends cannot tell the user two different things about one
file.

## Scrolling, and the colours

The docstring, the load message and the member rows are in the part of the
screen that scrolls, and the verdict, the saving line and the footer are below
it and stay where they are: they are what a user reaches for after editing
rather than something to scroll to. A configuration of any size therefore fits
a terminal of any size, and a container that would add more rows than the
editor opens at is folded to begin with, so that a long list does not fill the
screen before the user has seen the members below it.

Each kind of text has a colour, so that the explanations do not read as loudly
as the values and a refused validation does not read like an accepted one.
Which kind each piece of text is comes from `edit_cfg_json.Emphasis` and is
therefore the same here as in the Tkinter backend; what the colours are is
this package's own, and they are the colours of the terminal's theme rather
than colours named here, so the editor follows the terminal into its light or
its dark mode.

## About the keys

None of the defaults is a plain letter, because an unmodified letter belongs
to whichever field has the focus: a user who types it expects to see it
appear in the field. Neither `ctrl+s` nor `ctrl+q` is taken for flow control,
because Textual's driver clears `IXON` and `IXOFF` when it puts the terminal
into raw mode. `ctrl+f` and `f3` are taken by no default of this editor,
because a search over a configuration too big for the terminal is something
this editor is likely to be asked for, and no version number protects a key a
user has learnt.

`f5` validates as well, and is left out of the footer so that one action is
not named twice there; a function key is the one of the two that a keyboard
or a terminal is most likely not to deliver, which is why the footer names
`ctrl+r` instead. The same holds for `ctrl+t` beside `f2`.

`ctrl+shift+s` needs a word of warning. A legacy terminal encodes a control
letter as a single byte with nowhere to put the shift, so on such a terminal
this key arrives as `ctrl+s` and saves instead of asking where to save.
Textual asks the terminal for the Kitty keyboard protocol at startup, and a
terminal that speaks it reports the two keys apart. That is why **Validate,
Save, Save as, Explain and the fold action are also in the command palette**,
which `ctrl+p` opens:
every terminal can reach the palette, because it is a letter typed into a
field and not a key combination at all. The palette's own **Keys** entry
lists every binding of the editor, including the ones the footer has no room
for.

An application that needs one of these combinations for itself moves it, or
empties it, in its own `ActionSettings`. An action with no key at all keeps
its command palette entry, so nothing becomes unreachable. The bindings are
made when the application starts, which is the one thing a later answer from
a settings callable cannot change; the two actions that are named for what
they will do next are the exception, because renaming one is making its
bindings afresh.

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

- Test result: 1609 passed, 3 deselected in 45s
- No flake8 warnings.
- No mypy errors found.
- No pylint warnings.
- No python layout warnings.
- Built version(s): 0.0.3
- Build and test using Python 3.14.7
