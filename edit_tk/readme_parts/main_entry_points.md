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

## The {{dist_name}} program

Installing this package also installs a program of the same name, so an
application author gets a Tk editor for their own configuration class without
writing a line of code:

````sh
{{dist_name}} --module myapp.config AppConfig -i /etc/myapp.json
````

The window it opens is the one this page describes, on the class that was
named. It is `edit_cfg_json.run_cli` with this package's backend filled in, so
the command line below is the same one that `edit-cfg-json` and
`edit-cfg-json-textual` have; what differs is which of the three shows the
configuration.

{{include: program.md}}

## What the window shows

The package is under construction. This version opens a window with one edit
field per configuration member, four buttons — Validate, Save, Save as and
Close — a tick-box for Explain, and a key for each of them. Every change of a
field goes straight into the model, and the label above the fields is marked
while the model holds a change worth saving.

A field is shown with a background, a border and a caret colour of its own, so
that what can be typed into can be told from what only says something. Those
are stated rather than inherited: the window is white, so a field that kept the
background it was given could not be seen at all.

Validate runs the validation of the application's own configuration class
and shows what that class would say about the values that are in the fields.
What it said about one member is shown **below that member**, and the line
below the fields names the members it was about, so a configuration too tall
for the window does not leave the user hunting for the field. What the class
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

Explain shows or hides what the application says about these values: the
whole docstring of the configuration class above the fields, and the
description of each described member below its own field. The editor opens
with them shown, and what is left when they are hidden is the first paragraph
of that docstring, because one line for the whole configuration is worth
keeping. A member the application described gets a line and one it said
nothing about gets none, rather than an empty one. Which of the two states the
editor is in belongs to the model, so this backend and the Textual one cannot
disagree about it.

It is a tick-box rather than a button, and the tick is what says which of the
two states the window is in: a button saying Explain beside explanations that
are already there would be offering something that has been done. The key of
the action moves the tick with it, because Tk moves it only when it was the
tick-box that was pressed.

Close writes nothing of its own. It is the "cancel" of the editor, and it is
called Close rather than Cancel because saving leaves the editor open: a
button called Cancel beside values that have already been written would read
as an offer to undo the writing, which it is not.

What reading the input file did is shown above the fields, when it did
anything, because it is what explains the marks below it: a member that the
file did not hold says so beside its field. Both the message and the marks
are read from the model, so the two backends cannot tell the user two
different things about one file.

## Scrolling, and the colours

The label, the docstring, the load message and the member rows are on a canvas
that scrolls, and the verdict, the saving line and the buttons are below it and
stay where they are: they are what a user reaches for after editing rather than
something to scroll to. The scrollbar is beside the canvas, and the mouse wheel
scrolls it however the platform reports one.

The window opens at the size the configuration asks for, up to the size of a
window, so a small configuration gets a small window and a large one is
scrolled through rather than cut off. Every text that is a paragraph — the
docstring, a description, a message, what is wrong with a member — wraps to
the width there is, whatever the user resizes the window to. The mark of a
member is the one text that does not wrap, because it belongs beside its
field on one line: a
window too narrow for the name, the field and the mark squeezes the field,
which the user can scroll within, rather than cutting off a mark, which they
could not read at all.

Each kind of text has a colour, so that the explanations do not read as loudly
as the values and a refused validation does not read like an accepted one.
Which kind each piece of text is comes from `edit_cfg_json.Emphasis` and is
therefore the same here as in the Textual backend; what the colours are is this
package's own, in `EMPHASIS_COLOURS`, because Tk has no theme to ask. They are
chosen for the light window that Tk gives this editor. A Tk that a platform has
put into a dark mode would want other values, and that is a theming decision
the library has not been asked for yet.

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
| `f1`, or `ctrl+g` | Explain |

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
