## Main entry points

Everything a user of this package needs is re-exported from the top-level
`{{import_name}}` package:

````python
from {{import_name}} import TkEditor, TkEditorPanel, edit
````

`edit` is the short way in for an application that has already chosen Tkinter.
It is `edit_cfg_json.edit` with this package's backend filled in, and it gives
back the configuration object that was saved, or `None` when nothing was:

````python
from {{import_name}} import edit

saved = edit(config=config, in_file='my_config.json')
````

Every keyword of `edit_cfg_json.edit` except the backend is taken here too:
`descriptions` says what the members are for, `settings` says what the
application has already decided about keys and files, and `loader` is for a
class this library cannot construct on its own.

`TkEditorPanel` is the same editor for an application that **already runs Tk**.
`edit` and `TkEditor` cannot serve one of those: each of them creates a
`tkinter.Tk`, a second one in a process is a second Tcl interpreter, and no
widget, variable, font or image crosses between two of them. So this is a
separate entry point, it reads the configuration itself in exactly the way
`edit` does, and it does not block:

````python
from {{import_name}} import TkEditorPanel

# a window of its own, over the application's, holding the application
panel = TkEditorPanel(config, parent=self.window, in_file='my_config.json',
                      on_close=self.editor_gone)

# or filling a frame of a window the application also uses for other things
panel = TkEditorPanel(config, area=self.frame, modal=False,
                      in_file='my_config.json', on_close=self.editor_gone)
````

**`parent` or `area`, and never both**, is the one decision this entry point
asks of the application. `parent` is a widget the editor opens a window *over*:
it creates that `tkinter.Toplevel` itself, names it after the configuration
class, makes it transient and destroys it again when the session ends. `area`
is a widget the editor *fills* instead, building one frame inside it and
touching nothing else. `modal` says whether the editor holds the application
for the session, and is `True` by default.

What the application learns is `on_close`, which says that the session has
ended, and `panel.saved_config`, which says what came of it — an editor that
returns at once has no moment at which it could return anything.
`panel.close(ask_about_unsaved=True)` is how the application closes the editor
itself, from a button or a menu of its own.

`TkEditor` is the Tkinter implementation of the `EditorBackend` protocol of
`edit-cfg-json`, for an application that builds the model itself. Every public
name of this package, that one included, is described in
[the api document](https://github.com/tom-bjorkholm/edit-cfg-json/blob/master/doc/{{dist_name}}_api.md).

## The {{dist_name}} program

Installing this package also installs a program of the same name, so an
application author gets a Tk editor for their own configuration class without
writing a line of code. The window it opens is the one this page describes, on
the class that was named. It is `edit_cfg_json.run_cli` with this package's
backend filled in, so the command line below is the same one that
`edit-cfg-json-textual` has; what differs is which of the two shows the
configuration.

{{include: program.md}}

## What the window shows

The window holds the label of the configuration, what the class says about
itself, what reading the input file did, and then one row per node of the
configuration. Below those, in a part of the window that does not scroll, are
the search, the validation verdict, the saving line, and the buttons:
Validate, Save, Save as..., a tick-box for Explain, a button that folds or
opens every container, and Close. Every one of them has a key as well:

| Key | What it does |
| --- | --- |
| `ctrl+r`, or `f5` | Validate |
| `ctrl+s` | Save |
| `ctrl+shift+s` or `f12` | Save as |
| `f1`, or `ctrl+g` | Explain |
| `f2`, or `ctrl+t` | Fold all, or unfold all |
| `ctrl+f` | Find |
| `f3` | Find next |
| `ctrl+q` | Close |

Those are the defaults of `edit_cfg_json.ActionSettings`, and an application
that needs one of these combinations for itself moves it, or empties it, in the
`actions` of its own `edit_cfg_json.Settings`. Every action has a button as
well, so an action with no key at all stays reachable. The bindings are made on
a bind tag of the editor's own, which the widget the editor was built below and
every widget inside it carry, so an editor that owns its window gets the keys
of all of it and an embedded one never claims a key of the application.

**Every change of a field goes straight into the model**, and the label above
the rows is marked while the model holds a change worth saving.

**A container is a row and not a field.** The rows of what it holds are
indented below it, there is a field at every value, and the container row says
how many things it holds — or which class the object at it is — where a value
would be. A control at the left of the row folds it away, `Fold all` below the
rows does the same to all of them at once, and its text says what the next
press will do. A configuration with nothing to fold gets neither the button nor
the column that the controls sit in, so the values keep that width.

**A member of a configuration too big for the window is looked for** in
the `Find:` field below the rows, which searches as it is typed. The
four tick-boxes beside it say where it looks — in the path of a member,
in its value, matching the case, and matching the whole of one of them
instead of any part — and each of them says what it means when the
pointer rests on it. The defaults are the path and the value, the case
ignored, and a part enough. What is found is opened if folding hid it,
brought into view and marked *(found)*; `f3` and the `►` button go on to
the next one, and pressing Enter in the field puts the cursor in what
was found, so it can be typed into at once.

**At the end of the line of a node are its element controls**: `Add`, `Del`,
`Up` and `Down`, and only the ones that node really offers. Adding an entry to
a dict opens a small dialog for the key, because nothing but the person
configuring the application knows what a new entry is called. A container that
can be given nothing gets no `Add` at all and says why below itself instead.

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

**Validate** shows what the application's own configuration class would say
about the values that are in the fields, below the node each remark is about.
**Leaving a field** asks the smaller question of whether what was typed into it
means a value of that member at all, which is what an enum member name answers
only once it is fully typed. **Save** writes the output file and refuses to
write values the application would not accept, leaving the file on disk exactly
as it was; it asks first before writing over a file this session has not
written, and says where the previous content was kept. **Save as** asks with
the ordinary system dialog, offering the extension the application named in its
`Settings`. **Close** writes nothing, and asks whether unsaved changes may be
dropped, with the answer that keeps them as the one the dialog opens on.

**Explain** shows or hides what the application says about these values: the
class docstring, the docstring of each nested object, the description of each
described member below its own field, what kind of value each member holds, and
why a container cannot be given an element. The editor opens with them shown,
and what is left when they are hidden is the first paragraph of the class
docstring. It is a tick-box rather than a button, because a button saying
Explain beside explanations that are already there would be offering something
that has been done.

**A configuration bigger than the window** is scrolled through rather than cut
off: the rows are on a canvas that scrolls while the verdict, the saving line
and the buttons stay where they are, and every paragraph wraps to the width
there is. The window opens at the size the configuration asks for, up to the
size of a window.

**Each kind of text has a colour**, so that the explanations do not read as
loudly as the values and a refused validation does not read like an accepted
one. Which kind each piece of text is comes from `edit_cfg_json.Emphasis`, so
it is the same here as in the Textual backend; the colours are this package's
own and are chosen for the light window that Tk gives this editor.
