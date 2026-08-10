## Main entry points

Everything a user of this package needs is re-exported from the top-level
`{{import_name}}` package, so it can be imported directly:

````python
from {{import_name}} import TextualEditor, edit
````

`edit` is the short way in for an application that has already chosen
Textual. It is `edit_cfg_json.edit` with this package's backend filled in,
and it gives back the configuration object that was saved, or `None` when
nothing was:

````python
from {{import_name}} import edit

saved = edit(config=config, in_file='my_config.json')
````

`TextualEditor` is the Textual implementation of the `EditorBackend`
protocol of `edit-cfg-json`, for an application that builds the model
itself. It has the one method that protocol asks for:

````python
from edit_cfg_json import EditModel, load_config
from {{import_name}} import TextualEditor

loaded = load_config(config=config, in_file='my_config.json')
model = EditModel(config=loaded.config, report=loaded.report,
                  out_file='my_config.json')
TextualEditor().run_editor(model)
saved = model.saved_config
````

## The {{dist_name}} program

Installing this package also installs a program of the same name, so an
application author gets a Textual editor for their own configuration class
without writing a line of code:

````sh
{{dist_name}} --module myapp.config --class AppConfig -i /etc/myapp.json
````

The screen it opens is the one this page describes, on the class that was
named. It is `edit_cfg_json.run_cli` with this package's backend filled in, so
the command line below is the same one that `edit-cfg-json-tk` has; what
differs is which of the two shows the configuration.

{{include: program.md}}

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
