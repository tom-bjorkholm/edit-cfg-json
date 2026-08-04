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
from edit_cfg_json_textual import TextualEditor, edit
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

The package is under construction. This version opens a terminal screen with
one edit field per configuration member, and the keys the application chose
in the `actions` of its `edit_cfg_json.Settings`. With an application that
chose nothing they are the defaults of `edit_cfg_json.ActionSettings`:

| Key | What it does |
| --- | --- |
| `ctrl+r`, or `f5` | Validate |
| `ctrl+s` | Save |
| `ctrl+shift+s` or `f12` | Save as |
| `ctrl+q` | Quit |
| `f1`, or `ctrl+g` | Explain, or Hide explanation |

Every change of a field goes straight into the model, and the title is marked
while the model holds a change worth saving.

Validating runs the validation of the application's own configuration class
and shows what that class would say about the values that are in the fields.
What it said about one member is shown **below that member**, and the line
below the fields names the members it was about, so a configuration too tall
for the terminal does not leave the user hunting for the field. What the class
said that is about no single member — a whole-configuration rule, a key that
does not match — stays in that line, because there is no field it belongs to.
Every refused member is marked at once, and not only the first one, because
the editor walks the validation plan itself rather than stopping where
`Config.validate()` stops.

A pass is not read only: a validator returns the value that is stored back
into the member, so the fields are written back from the model afterwards, and
a member that a validator rewrote says so beside its field.

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

Explaining shows or hides what the application says about these values: the
whole docstring of the configuration class above the fields, and the
description of each described member below its own field. The editor opens
with them shown, and what is left when they are hidden is the first paragraph
of that docstring, because one line for the whole configuration is worth
keeping. A member the application described gets a line and one it said
nothing about gets none, rather than an empty one. Which of the two states the
editor is in belongs to the model, so this backend and the Tk one cannot
disagree about it.

The action is named for what the next press of it will do: it is "Explain"
while the explanations are hidden and "Hide explanation" while they are shown,
in the footer and in the command palette alike. "Explain" beside explanations
that are already there would be offering something that has been done. The Tk
backend answers the same question with a tick-box, which a footer cannot be.

Quitting writes nothing of its own. It is the "cancel" of the editor; saving
leaves the editor open, and what has been saved has been saved.

## Scrolling, and the colours

The docstring, the load message and the member rows are in the part of the
screen that scrolls, and the verdict, the saving line and the footer are below
it and stay where they are: they are what a user reaches for after editing
rather than something to scroll to. A configuration of any size therefore fits
a terminal of any size.

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
into raw mode.

`f5` validates as well, and is left out of the footer so that one action is
not named twice there; a function key is the one of the two that a keyboard
or a terminal is most likely not to deliver, which is why the footer names
`ctrl+r` instead.

`ctrl+shift+s` needs a word of warning. A legacy terminal encodes a control
letter as a single byte with nowhere to put the shift, so on such a terminal
this key arrives as `ctrl+s` and saves instead of asking where to save.
Textual asks the terminal for the Kitty keyboard protocol at startup, and a
terminal that speaks it reports the two keys apart. That is why **Validate,
Save, Save as and Explain are also in the command palette**, which `ctrl+p`
opens:
every terminal can reach the palette, because it is a letter typed into a
field and not a key combination at all. The palette's own **Keys** entry
lists every binding of the editor, including the ones the footer has no room
for.

An application that needs one of these combinations for itself moves it, or
empties it, in its own `ActionSettings`. An action with no key at all keeps
its command palette entry, so nothing becomes unreachable. The bindings are
made when the application starts, which is the one thing a later answer from
a settings callable cannot change.

What reading the input file did is shown above the fields, when it did
anything, because it is what explains the marks below it: a member that the
file did not hold says so beside its field. Both the message and the marks
are read from the model, so the two backends cannot tell the user two
different things about one file.

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

- Test result: 865 passed, 2 deselected in 19s
- No flake8 warnings.
- No mypy errors found.
- No pylint warnings.
- No python layout warnings.
- Built version(s): 0.0.1
- Build and test using Python 3.14.6
