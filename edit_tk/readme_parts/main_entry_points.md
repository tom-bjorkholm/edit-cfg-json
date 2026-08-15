## Main entry points

Everything a user of this package needs is re-exported from the top-level
`{{import_name}}` package, so it can be imported directly:

````python
from {{import_name}} import TkEditor, TkEditorPanel, edit
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

`TkEditorPanel` is the same editor for an application that **already runs
Tk**. `edit` and `TkEditor` cannot serve one of those: each of them creates a
`tkinter.Tk`, a second one in a process is a second Tcl interpreter, and no
widget, variable, font or image crosses between two of them. `run_editor`
could not serve one either, because it promises to run until the user is done
and an editor in one panel of somebody else's window can never do that. So
this is a separate entry point, it reads the configuration itself in exactly
the way `edit` does, and it does not block:

````python
from {{import_name}} import TkEditorPanel

# a window of its own, over the application's, holding the application
panel = TkEditorPanel(config, parent=self.window, in_file='my_config.json',
                      on_close=self.editor_gone)

# or filling a frame of a window the application also uses for other things
panel = TkEditorPanel(config, area=self.frame, modal=False,
                      in_file='my_config.json', on_close=self.editor_gone)
````

**`parent` or `area`, and never both**, is where the editor goes, and it is
the one decision this entry point asks of the application:

- **`parent`** is a widget of the application's own that the editor opens a
  window *over*. The editor creates that `tkinter.Toplevel` itself, names it
  after the configuration class, makes it transient for the application's
  window and destroys it again when the session ends.
- **`area`** is a widget of the application's own that the editor *fills*
  instead. It builds one frame inside it and touches nothing else, so what the
  application has on the screen beside the editor is untouched.

Everything after that is the session, and it is the keywords of `edit` less
the backend: `descriptions`, `in_file`, `loader`, `out_file`, `policy`,
`settings` and `stderr_file` all mean here exactly what they mean there,
because the same `edit_cfg_json.editor_model` reads them.

`modal` says whether the editor holds the application for the session, and it
is `True` by default, which is what an application that wants its
configuration seen to usually means. An application whose own controls are to
go on answering beside the editor passes `False` — which is the usual answer
for `area` and the unusual one for `parent`.

What the application learns is `on_close`, which says that the session has
ended, and `panel.saved_config`, which says what came of it — an editor that
returns at once has no moment at which it could return anything. `panel.model`
is the whole model of the session, for an application that wants more than the
outcome.

`panel.close(ask_about_unsaved=True)` is how the application closes the editor
itself, from a button or a menu of its own. The editor's own Close button, its
quit key and the close button of a window it made are that same call with the
default, so the question about what has not been saved is put in the same
words whichever of them ended the session; an application that is shutting
down for reasons of its own passes `False`, because it already has a question
to put and does not want two. Closing again once the session has ended does
nothing, so an application need not keep track of whether the user closed the
editor already.

**The keys of the editor and its mouse wheel reach the part of the window it
built and nothing else.** They are bound on a Tk bind tag of the editor's own,
which is put on the widget the editor was given and on every widget inside it,
so an editor that owns its window still gets the keys of all of it and an
embedded one never claims a key of the application. Where that tag goes in the
list of each widget decides whether the editor or the widget with the focus is
offered a key first, which is `edit_cfg_json.Settings.priority_keys`.

## The {{dist_name}} program

Installing this package also installs a program of the same name, so an
application author gets a Tk editor for their own configuration class without
writing a line of code:

````sh
{{dist_name}} --module myapp.config --class AppConfig -i /etc/myapp.json
````

The window it opens is the one this page describes, on the class that was
named. It is `edit_cfg_json.run_cli` with this package's backend filled in, so
the command line below is the same one that `edit-cfg-json-textual` has; what
differs is which of the two shows the configuration.

{{include: program.md}}

## What the window shows

The window holds the label of the configuration, what the class says about
itself, what reading the input file did, and then one row per node of the
configuration. Below those, in a part of the window that does not scroll, are
the validation verdict, the saving line, and the buttons: Validate, Save,
Save as..., a tick-box for Explain, a button that folds or opens every
container, and Close. Every one of them has a key as well.

Every change of a field goes straight into the model, and the label above the
rows is marked while the model holds a change worth saving.

A field is shown with a background, a border and a caret colour of its own, so
that what can be typed into can be told from what only says something. Those
are stated rather than inherited: the window is white, so a field that kept the
background it was given could not be seen at all.

### One row per node

A member that holds a list, a dict or a nested `config_as_json.Config` object
is not one field. It is a row of its own with the rows of what it holds
indented below it, a field at every value, and no field on the row of the
container itself — which says how many things it holds, or which class the
object at it is, where a value would be.

A container has a control at the left of its row, `-` while it is open and `+`
while it is folded, and pressing it hides or shows everything inside it. The
button below the rows does the same to all of them at once, and its text says
what the next press will do: `Fold all` while anything is open, `Unfold all`
once nothing is. A configuration with nothing to fold gets neither the button
nor the column that the controls sit in, so the values keep that width.

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
small dialog for the key, because nothing but the person configuring the
application knows what a new entry is called; a key the dict already holds is
asked about again rather than allowed to take the place of what is there.

A container that cannot be given an element gets no `Add` at all, and says why
below itself instead — an ordinary dict member, for instance, because
`config_as_json` matches such a member against the keys its class declares, so
a dict that gained one would be refused by the configuration class itself. That
line is explanation rather than something to act on, so it is muted and the
Explain tick-box covers it.

### Validating, saving and closing

Validate runs the validation of the application's own configuration class
and shows what that class would say about the values that are in the fields.
What it said about one node is shown **below that node**, and the line
below the rows names the nodes it was about, by the whole path to each of them,
so a configuration too tall for the window does not leave the user hunting for
the field. What the class said that is about no single node — a
whole-configuration rule, a key that does not match — stays in that line,
because there is no field it belongs to. Every refused node is marked at once,
and not only the first one, because the editor walks the validation plan itself
rather than stopping where `Config.validate()` stops.

A pass is not read only: a validator returns the value that is stored back
into the member, so the fields are written back from the model afterwards, and
a member that a validator rewrote says so beside its field. A pass can also
change how many rows there are — a validator that sorts a list and removes its
duplicates removes one — and the window then builds its rows again rather than
writing into a widget for a value that is no longer there.

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
mark above the rows goes away and the editor stays open.

Save as asks for the file with the ordinary system dialog. What that dialog
offers is what the application decided in its `edit_cfg_json.Settings`: the
extension it uses for its configuration is the one the dialog adds to a name
that has none, and the one it offers to filter by, and an application that
enforces its extension gets that filter and no other. An application with no
opinion gets a dialog with none, because this library has none of its own
about what a configuration file is called. Save asks the same question when
the session has no file to write yet, which is what every editor does.

**A save that would write over a file this session has not written asks
first**, in a dialog whose default answer is the one that leaves the file
alone. The previous content is then kept under the name the application chose,
and the saving line says where it went. Both the question and the name are the
core's, so this backend and the Textual one cannot treat the user's old
configuration differently. The system dialog is told not to ask about
overwriting itself, although it offers to: the question is asked once, and it is
asked by the editor.

Close writes nothing of its own. It is the "cancel" of the editor, and it is
called Close rather than Cancel because saving leaves the editor open: a
button called Cancel beside values that have already been written would read
as an offer to undo the writing, which it is not.

**Closing an editor that holds something unsaved asks whether the changes may
be dropped**, and the answer that keeps them is the one the dialog opens on.
The button, the key and the close button of the window all go through one place,
because the one way out that is not a widget of the editor would otherwise be
the one way out that drops the changes silently. Closing again after a Save asks
nothing, because a save leaves nothing to lose.

Explain shows or hides what the application says about these values: the
whole docstring of the configuration class above the rows, the docstring of
each nested object, the description of each described member below its own
field, what kind of value each member holds, and why a container cannot be
given an element. The editor opens with them shown, and what is left when they
are hidden is the first paragraph of the class docstring, because one line for
the whole configuration is worth keeping. A member the application described
gets a line and one it said nothing about gets none, rather than an empty one.
Which of the two states the editor is in belongs to the model, so this backend
and the Textual one cannot disagree about it.

It is a tick-box rather than a button, and the tick is what says which of the
two states the window is in: a button saying Explain beside explanations that
are already there would be offering something that has been done. The key of
the action moves the tick with it, because Tk moves it only when it was the
tick-box that was pressed.

What reading the input file did is shown above the rows, when it did
anything, because it is what explains the marks below it: a member that the
file did not hold says so beside its field, and so does one whose value the
reading of the file put there or altered — with the older key it was read from,
where the class recorded one. Both the message and the marks are read from the
model, so the two backends cannot tell the user two different things about one
file.

## Scrolling, and the colours

The label, the docstring, the load message and the member rows are on a canvas
that scrolls, and the verdict, the saving line and the buttons are below it and
stay where they are: they are what a user reaches for after editing rather than
something to scroll to. The scrollbar is beside the canvas, and the mouse wheel
scrolls it however the platform reports one.

The window opens at the size the configuration asks for, up to the size of a
window, so a small configuration gets a small window and a large one is
scrolled through rather than cut off. A long list therefore does not decide the
size of the window twice: it opens folded when opening it would add more rows
than the editor opens at, and the window is the size of what is on the screen.

Every text that is a paragraph — the docstring, a description, a message, what
is wrong with a member — wraps to the width there is, whatever the user resizes
the window to. The mark of a member is the one text that does not wrap, because
it belongs beside its field on one line: a window too narrow for the name, the
field and the mark squeezes the field, which the user can scroll within, rather
than cutting off a mark, which they could not read at all.

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
| `f1`, or `ctrl+g` | Explain |
| `f2`, or `ctrl+t` | Fold all, or unfold all |
| `ctrl+q` | Close |

Combinations are written in the notation that `ActionSettings` documents,
which this package translates into the event sequences of Tk: `ctrl+shift+s`
becomes `<Control-Shift-S>`, and `f5` becomes `<F5>`. A combination this
translation does not know, or one that Tk itself refuses, leaves that action
without that key rather than without an editor — every action here has a
button as well, which is also what an action the application gave no key at
all keeps. The fold action is offered at all only to a configuration that has
something to fold, so its keys are free wherever there would be nothing to
fold.

The `cancel` action is bound to nothing in this backend. The questions it would
leave are put in the toolkit's own dialogs, which answer that key themselves.

The bindings are made on a bind tag of the editor's own, which the widget the
editor was built below and every widget inside it carry. For an editor that
owns its window that widget *is* the window, so a key that a field does not
use for itself reaches the editor wherever the focus is; for one mounted in a
window an application owns it is the frame the editor built, which is what
keeps the editor out of the rest of that window. The mouse wheel is bound the
same way and for the same reason, because a wheel event goes to the widget
under the pointer.

The keys are read once, when the widgets are built, which is the one thing a
later answer from a settings callable cannot change.
