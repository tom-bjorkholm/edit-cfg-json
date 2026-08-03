## Main entry points

Everything a user of this package needs is re-exported from the top-level
`{{import_name}}` package, so it can be imported directly:

````python
from {{import_name}} import TkEditor, edit
````

`edit` is the short way in for an application that has already chosen
Tkinter. It is `edit_cfg_json.edit` with this package's backend filled in,
and it gives back the configuration object that was saved, or `None` when
nothing was:

````python
from {{import_name}} import edit

saved = edit(config=config, in_file='my_config.json')
````

`TkEditor` is the Tkinter implementation of the `EditorBackend` protocol of
`edit-cfg-json`, for an application that builds the model itself. It has the
one method that protocol asks for:

````python
from edit_cfg_json import EditModel, load_config
from {{import_name}} import TkEditor

loaded = load_config(config=config, in_file='my_config.json')
model = EditModel(config=loaded.config, report=loaded.report,
                  out_file='my_config.json')
TkEditor().run_editor(model)
saved = model.saved_config
````

The package is under construction. This version opens a window with one edit
field per configuration member, four buttons — Validate, Save, Save as and
Close — and a key for each of them. Every change of a field goes straight
into the model, and the label above the fields is marked while the model
holds a change worth saving.

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

Save as asks for the file with the ordinary system dialog. What that dialog
offers is what the application decided in its `edit_cfg_json.Settings`: the
extension it uses for its configuration is the one the dialog adds to a name
that has none, and the one it offers to filter by, and an application that
enforces its extension gets that filter and no other. An application with no
opinion gets a dialog with none, because this library has none of its own
about what a configuration file is called. Save asks the same question when
the session has no file to write yet, which is what every editor does.

Close writes nothing of its own. It is the "cancel" of the editor, and it is
called Close rather than Cancel because saving leaves the editor open: a
button called Cancel beside values that have already been written would read
as an offer to undo the writing, which it is not.

What reading the input file did is shown above the fields, when it did
anything, because it is what explains the marks below it: a member that the
file did not hold says so beside its field. Both the message and the marks
are read from the model, so the two backends cannot tell the user two
different things about one file.

## About the keys

The keys are the ones the application chose in the `actions` of its
`edit_cfg_json.Settings`, and with an application that chose nothing they
are the defaults of `edit_cfg_json.ActionSettings`:

| Key | What it does |
| --- | --- |
| `ctrl+r`, or `f5` | Validate |
| `ctrl+s` | Save |
| `ctrl+shift+s` or `f12` | Save as |
| `ctrl+q` | Close |

Combinations are written in the notation that `ActionSettings` documents,
which this package translates into the event sequences of Tk: `ctrl+shift+s`
becomes `<Control-Shift-S>`, and `f5` becomes `<F5>`. A combination this
translation does not know, or one that Tk itself refuses, leaves that action
without that key rather than without an editor — every action here has a
button as well, which is also what an action the application gave no key at
all keeps.

The `cancel` action is bound to nothing in this backend. The only question it
asks is the toolkit's own file dialog, which answers that key itself.

The bindings are made on the window, so a key that a field does not use for
itself reaches them wherever the focus is. They are read once, when the
widgets are built, which is the one thing a later answer from a settings
callable cannot change.
