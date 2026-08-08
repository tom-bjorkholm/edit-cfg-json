# Table of Contents

* [edit\_cfg\_json\_tk.tk\_editor](#edit_cfg_json_tk.tk_editor)
  * [VALIDATE\_TEXT](#edit_cfg_json_tk.tk_editor.VALIDATE_TEXT)
  * [SAVE\_TEXT](#edit_cfg_json_tk.tk_editor.SAVE_TEXT)
  * [SAVE\_AS\_TEXT](#edit_cfg_json_tk.tk_editor.SAVE_AS_TEXT)
  * [EXPLAIN\_TEXT](#edit_cfg_json_tk.tk_editor.EXPLAIN_TEXT)
  * [FOLD\_ALL\_TEXT](#edit_cfg_json_tk.tk_editor.FOLD_ALL_TEXT)
  * [OPEN\_ALL\_TEXT](#edit_cfg_json_tk.tk_editor.OPEN_ALL_TEXT)
  * [FOLD\_SHUT\_TEXT](#edit_cfg_json_tk.tk_editor.FOLD_SHUT_TEXT)
  * [FOLD\_OPEN\_TEXT](#edit_cfg_json_tk.tk_editor.FOLD_OPEN_TEXT)
  * [CLOSE\_TEXT](#edit_cfg_json_tk.tk_editor.CLOSE_TEXT)
  * [SAVE\_AS\_TITLE](#edit_cfg_json_tk.tk_editor.SAVE_AS_TITLE)
  * [CONFIG\_FILES](#edit_cfg_json_tk.tk_editor.CONFIG_FILES)
  * [ALL\_FILES](#edit_cfg_json_tk.tk_editor.ALL_FILES)
  * [StateWidgets](#edit_cfg_json_tk.tk_editor.StateWidgets)
    * [title](#edit_cfg_json_tk.tk_editor.StateWidgets.title)
    * [docstring](#edit_cfg_json_tk.tk_editor.StateWidgets.docstring)
    * [verdict](#edit_cfg_json_tk.tk_editor.StateWidgets.verdict)
    * [saving](#edit_cfg_json_tk.tk_editor.StateWidgets.saving)
    * [explained](#edit_cfg_json_tk.tk_editor.StateWidgets.explained)
    * [folding](#edit_cfg_json_tk.tk_editor.StateWidgets.folding)
  * [RowWidgets](#edit_cfg_json_tk.tk_editor.RowWidgets)
    * [frame](#edit_cfg_json_tk.tk_editor.RowWidgets.frame)
    * [fold](#edit_cfg_json_tk.tk_editor.RowWidgets.fold)
    * [field](#edit_cfg_json_tk.tk_editor.RowWidgets.field)
    * [mark](#edit_cfg_json_tk.tk_editor.RowWidgets.mark)
    * [description](#edit_cfg_json_tk.tk_editor.RowWidgets.description)
    * [diagnostic](#edit_cfg_json_tk.tk_editor.RowWidgets.diagnostic)
  * [EditorWidgets](#edit_cfg_json_tk.tk_editor.EditorWidgets)
    * [\_\_init\_\_](#edit_cfg_json_tk.tk_editor.EditorWidgets.__init__)
    * [label\_text](#edit_cfg_json_tk.tk_editor.EditorWidgets.label_text)
    * [verdict\_text\_shown](#edit_cfg_json_tk.tk_editor.EditorWidgets.verdict_text_shown)
    * [save\_text\_shown](#edit_cfg_json_tk.tk_editor.EditorWidgets.save_text_shown)
    * [wrong\_shown](#edit_cfg_json_tk.tk_editor.EditorWidgets.wrong_shown)
    * [docstring\_shown](#edit_cfg_json_tk.tk_editor.EditorWidgets.docstring_shown)
  * [TkEditor](#edit_cfg_json_tk.tk_editor.TkEditor)
    * [\_\_init\_\_](#edit_cfg_json_tk.tk_editor.TkEditor.__init__)
    * [run\_editor](#edit_cfg_json_tk.tk_editor.TkEditor.run_editor)
  * [edit](#edit_cfg_json_tk.tk_editor.edit)
* [edit\_cfg\_json\_tk.key\_names](#edit_cfg_json_tk.key_names)
  * [MODIFIERS](#edit_cfg_json_tk.key_names.MODIFIERS)
  * [KEY\_NAMES](#edit_cfg_json_tk.key_names.KEY_NAMES)
  * [tk\_sequence](#edit_cfg_json_tk.key_names.tk_sequence)
  * [bind\_key](#edit_cfg_json_tk.key_names.bind_key)
* [edit\_cfg\_json\_tk.tk\_look](#edit_cfg_json_tk.tk_look)
  * [NAME\_COLUMN\_WIDTH](#edit_cfg_json_tk.tk_look.NAME_COLUMN_WIDTH)
  * [LEAST\_FIELD\_WIDTH](#edit_cfg_json_tk.tk_look.LEAST_FIELD_WIDTH)
  * [PADDING](#edit_cfg_json_tk.tk_look.PADDING)
  * [DESCRIPTION\_INDENT](#edit_cfg_json_tk.tk_look.DESCRIPTION_INDENT)
  * [TREE\_INDENT](#edit_cfg_json_tk.tk_look.TREE_INDENT)
  * [FOLD\_WIDTH](#edit_cfg_json_tk.tk_look.FOLD_WIDTH)
  * [LEAST\_WRAP\_WIDTH](#edit_cfg_json_tk.tk_look.LEAST_WRAP_WIDTH)
  * [EMPHASIS\_COLOURS](#edit_cfg_json_tk.tk_look.EMPHASIS_COLOURS)
  * [FIELD\_BACKGROUND](#edit_cfg_json_tk.tk_look.FIELD_BACKGROUND)
  * [FIELD\_FOREGROUND](#edit_cfg_json_tk.tk_look.FIELD_FOREGROUND)
  * [FIELD\_BORDER](#edit_cfg_json_tk.tk_look.FIELD_BORDER)
  * [shown\_text](#edit_cfg_json_tk.tk_look.shown_text)
  * [told](#edit_cfg_json_tk.tk_look.told)
  * [show\_emphasis](#edit_cfg_json_tk.tk_look.show_emphasis)
  * [wrap\_to\_width](#edit_cfg_json_tk.tk_look.wrap_to_width)
  * [label\_text](#edit_cfg_json_tk.tk_look.label_text)
  * [place\_text](#edit_cfg_json_tk.tk_look.place_text)
* [edit\_cfg\_json\_tk.scrolling](#edit_cfg_json_tk.scrolling)
  * [BODY\_HEIGHT](#edit_cfg_json_tk.scrolling.BODY_HEIGHT)
  * [BODY\_WIDTH](#edit_cfg_json_tk.scrolling.BODY_WIDTH)
  * [ScrollingArea](#edit_cfg_json_tk.scrolling.ScrollingArea)
    * [area](#edit_cfg_json_tk.scrolling.ScrollingArea.area)
    * [body](#edit_cfg_json_tk.scrolling.ScrollingArea.body)
  * [scrolling\_body](#edit_cfg_json_tk.scrolling.scrolling_body)

<a id="edit_cfg_json_tk.tk_editor"></a>

# edit\_cfg\_json\_tk.tk\_editor

Tkinter view of an edit model, with one editable field per member.

Everything this backend takes from the core is reached through `core`, which is
`edit_cfg_json` itself. A backend may use the public API of the core and
nothing else, and naming it at every call site is what makes that visible; it
also keeps the two backends from each holding the same block of twenty
imported names, which is a duplication with nothing to factor out, since
neither backend may import the other.

<a id="edit_cfg_json_tk.tk_editor.VALIDATE_TEXT"></a>

#### VALIDATE\_TEXT

Text of the button that runs the validation of the application.

<a id="edit_cfg_json_tk.tk_editor.SAVE_TEXT"></a>

#### SAVE\_TEXT

Text of the button that writes the output file.

<a id="edit_cfg_json_tk.tk_editor.SAVE_AS_TEXT"></a>

#### SAVE\_AS\_TEXT

Text of the button that chooses an output file and then writes it.

<a id="edit_cfg_json_tk.tk_editor.EXPLAIN_TEXT"></a>

#### EXPLAIN\_TEXT

Text of the tick-box that shows or hides the explanatory text.

A tick-box and not a button, because the action is a toggle and a button
called Explain that hides the explanations reads as the wrong thing entirely.
The tick says which of the two states the editor is in, so one text is true in
both. The Textual backend has no button row to put one in and renames its own
action instead.

<a id="edit_cfg_json_tk.tk_editor.FOLD_ALL_TEXT"></a>

#### FOLD\_ALL\_TEXT

Text of the button while at least one list or dict is open.

A button and not a tick-box, unlike the explanations beside it, because its
two states are not the two states of one thing: a configuration can be partly
folded, and what the button says is what the next press will do to all of it.
That is the same answer the Textual backend gives, which renames its action.

<a id="edit_cfg_json_tk.tk_editor.OPEN_ALL_TEXT"></a>

#### OPEN\_ALL\_TEXT

Text of the same button once every list and dict is folded.

<a id="edit_cfg_json_tk.tk_editor.FOLD_SHUT_TEXT"></a>

#### FOLD\_SHUT\_TEXT

Text of the control of a container that is folded away.

<a id="edit_cfg_json_tk.tk_editor.FOLD_OPEN_TEXT"></a>

#### FOLD\_OPEN\_TEXT

Text of the control of a container that is open.

The two are what a tree has always used for this, and they are one character
wide in every font, which the arrows that a modern tree draws are not.

<a id="edit_cfg_json_tk.tk_editor.CLOSE_TEXT"></a>

#### CLOSE\_TEXT

Text of the button that ends the editor.

Closing writes nothing of its own. It is the "cancel" of the design, and it
is called Close because saving leaves the editor open: a button called Cancel
beside values that have already been written would read as an offer to undo
the writing, which it is not.

<a id="edit_cfg_json_tk.tk_editor.SAVE_AS_TITLE"></a>

#### SAVE\_AS\_TITLE

Title of the dialog that asks which file to write.

<a id="edit_cfg_json_tk.tk_editor.CONFIG_FILES"></a>

#### CONFIG\_FILES

What the dialog calls the files of the extension the application uses.

<a id="edit_cfg_json_tk.tk_editor.ALL_FILES"></a>

#### ALL\_FILES

What the dialog calls every other file.

<a id="edit_cfg_json_tk.tk_editor.StateWidgets"></a>

## StateWidgets Objects

```python
class StateWidgets(NamedTuple)
```

The widgets that say what is true of the whole model.

They are one object rather than one attribute each, so that the class
below has a handful of things to hold rather than a dozen.

<a id="edit_cfg_json_tk.tk_editor.StateWidgets.title"></a>

#### title

The label that names the configuration and marks unsaved changes.

<a id="edit_cfg_json_tk.tk_editor.StateWidgets.docstring"></a>

#### docstring

The label that says what the configuration class says about itself.

It is None for a class with no docstring of its own, because there is then
nothing that could ever appear in it.

<a id="edit_cfg_json_tk.tk_editor.StateWidgets.verdict"></a>

#### verdict

The label that says what the application makes of these values.

<a id="edit_cfg_json_tk.tk_editor.StateWidgets.saving"></a>

#### saving

The label that says what saving did, or where it would write.

<a id="edit_cfg_json_tk.tk_editor.StateWidgets.explained"></a>

#### explained

Whether the tick-box of the explanations is ticked.

The variable is what a `Checkbutton` shows its state through, and it has
to be kept for as long as the tick-box lives: a `tkinter.Variable` unsets
its Tcl variable when it is collected.

<a id="edit_cfg_json_tk.tk_editor.StateWidgets.folding"></a>

#### folding

The button that folds every container away, or opens every one.

It is None for a configuration with no list and no dict in it, because a
button that could never do anything would be offering something that is
not there.

<a id="edit_cfg_json_tk.tk_editor.RowWidgets"></a>

## RowWidgets Objects

```python
class RowWidgets(NamedTuple)
```

The widgets that one node of the configuration owns.

<a id="edit_cfg_json_tk.tk_editor.RowWidgets.frame"></a>

#### frame

The widget that holds the whole node, which is what folding hides.

It is packed and unpacked rather than created and destroyed, so that a
field the user is typing into survives its container being folded and
opened again.

<a id="edit_cfg_json_tk.tk_editor.RowWidgets.fold"></a>

#### fold

The control that folds this container, None for a node with none.

<a id="edit_cfg_json_tk.tk_editor.RowWidgets.field"></a>

#### field

The field of an editable node, and None for every other node.

<a id="edit_cfg_json_tk.tk_editor.RowWidgets.mark"></a>

#### mark

The widget that says what has happened to this member.

<a id="edit_cfg_json_tk.tk_editor.RowWidgets.description"></a>

#### description

The widget that says what this member is for.

It is None for a member that nothing is said about, because there is then
nothing that could ever appear in it.

<a id="edit_cfg_json_tk.tk_editor.RowWidgets.diagnostic"></a>

#### diagnostic

The widget that says what is wrong with this member.

Every member has one, unlike the description above it: any member can be
refused, so there is no member for which this could never say anything.

<a id="edit_cfg_json_tk.tk_editor.EditorWidgets"></a>

## EditorWidgets Objects

```python
class EditorWidgets()
```

The widgets that show one edit model below one parent widget.

This is a class rather than a function because the fields have to be
kept: a `tkinter.StringVar` unsets its Tcl variable when it is collected,
and the field it belongs to would then lose both its text and the
callback that writes it into the model. Keeping them together also gives
an application that mounts these widgets in a window of its own a single
object to hold on to.

The widgets of the nodes are kept in the order the model reports its rows
in, which is the order they were created in. A validation pass can change
how many rows there are, because a validator that normalizes a list
changes how many values it holds, so the paths that were built are kept
and the widgets are made again when they no longer match. Every other
refresh leaves them alone, which is what keeps the focus in the field the
user is typing into.

<a id="edit_cfg_json_tk.tk_editor.EditorWidgets.__init__"></a>

#### \_\_init\_\_

```python
def __init__(parent: tkinter.Misc,
             model: core.EditModel,
             *,
             on_close: Optional[Callable[[], None]] = None) -> None
```

Create the labels, one row per member, the verdict and the buttons.

The parent is a widget and not a window, so that the same rows can
later be mounted inside a window that an application owns itself.

**Arguments**:

- `parent` - Widget that becomes the parent of the created widgets.
- `model` - Model to show and to edit.
- `on_close` - What closing the editor does, or None to destroy the
  window these widgets are in. None is for a caller that owns
  that window, which is what `TkEditor` does. A caller that
  mounts these widgets in a window of an application says what
  closing does, because the editor must never destroy a window
  it did not create.

<a id="edit_cfg_json_tk.tk_editor.EditorWidgets.label_text"></a>

#### label\_text

```python
@property
def label_text() -> str
```

Return the text that the label of the whole model shows.

<a id="edit_cfg_json_tk.tk_editor.EditorWidgets.verdict_text_shown"></a>

#### verdict\_text\_shown

```python
@property
def verdict_text_shown() -> str
```

Return the text that the validation part of the editor shows.

<a id="edit_cfg_json_tk.tk_editor.EditorWidgets.save_text_shown"></a>

#### save\_text\_shown

```python
@property
def save_text_shown() -> str
```

Return the text that the saving part of the editor shows.

<a id="edit_cfg_json_tk.tk_editor.EditorWidgets.wrong_shown"></a>

#### wrong\_shown

```python
@property
def wrong_shown() -> list[str]
```

Return what the editor says about each member, in row order.

A member that nothing is known to be wrong with says nothing, so most
of these are empty most of the time.

<a id="edit_cfg_json_tk.tk_editor.EditorWidgets.docstring_shown"></a>

#### docstring\_shown

```python
@property
def docstring_shown() -> str
```

Return the text that the label of the configuration class shows.

<a id="edit_cfg_json_tk.tk_editor.TkEditor"></a>

## TkEditor Objects

```python
class TkEditor()
```

Tkinter user interface backend for an edit model.

The class has the single method that `EditorBackend` asks for, and
deliberately nothing else: everything worth testing without a display
lives in the core.

<a id="edit_cfg_json_tk.tk_editor.TkEditor.__init__"></a>

#### \_\_init\_\_

```python
def __init__() -> None
```

Create a backend that has not shown a model yet.

<a id="edit_cfg_json_tk.tk_editor.TkEditor.run_editor"></a>

#### run\_editor

```python
def run_editor(model: core.EditModel) -> None
```

Show the model in a Tk window until the user closes it.

The widgets are held for as long as the window lives, because they
own the fields that the Tcl variables belong to. The window is this
backend's own, which is why closing the editor destroys it.

This is for an application that has no Tk of its own yet, because a
second `tkinter.Tk` is a second Tcl interpreter and nothing can be
shared between the two. An application that already runs Tk gets the
entry point of section 8.2 of `doc/design.md` instead, which mounts
the editor in a widget that application owns.

**Arguments**:

- `model` - Model to show and to edit.

<a id="edit_cfg_json_tk.tk_editor.edit"></a>

#### edit

```python
def edit(config: Config,
         *,
         descriptions: Optional[core.Descriptions] = None,
         in_file: Optional[PathOrStr] = None,
         loader: Optional[core.ConfigLoader] = None,
         out_file: Optional[PathOrStr] = None,
         policy: core.LoadPolicy = core.LoadPolicy.STRICT_THEN_DEFAULTS,
         settings: core.SettingsSource = core.Settings(),
         stderr_file: TextIO = sys.stderr) -> Optional[Config]
```

Edit one configuration in a Tk window, and return what was saved.

This is `edit_cfg_json.edit` with this package's backend filled in, for
an application that has already chosen Tkinter. Everything it does is
documented there.

**Arguments**:

- `config` - Configuration object to edit. It is never modified.
- `descriptions` - What the application says about the members it
  declares, or None when it says nothing.
- `in_file` - File to read, or None to start from the declared defaults.
- `loader` - How this application constructs its configuration, or None for
  a class the editor can construct on its own.
- `out_file` - File to write, or None to write the input file.
- `policy` - What to do about declared keys the input file does not hold.
- `settings` - What this application has already decided about key
  combinations and file names, or a callable that answers with it.
- `stderr_file` - Stream used for user-facing diagnostics.
  

**Returns**:

  The configuration object that was written, or None when nothing was.
  

**Raises**:

- `ConfigLoadError` - The input file cannot be opened for editing.

<a id="edit_cfg_json_tk.key_names"></a>

# edit\_cfg\_json\_tk.key\_names

Binding one key combination, in the notation that Tk binds by.

The application writes its key combinations once, in the notation that
`edit_cfg_json.ActionSettings` documents, and each backend translates them
into whatever its own toolkit binds by. Tk needs a translation whatever
notation is chosen, because `<Control-Shift-S>` is a form that no other
toolkit shares.

A combination this module does not know leaves that action without that key
rather than without an editor: every action of this backend has a button as
well.

<a id="edit_cfg_json_tk.key_names.MODIFIERS"></a>

#### MODIFIERS

What Tk calls each modifier that a combination can name.

<a id="edit_cfg_json_tk.key_names.KEY_NAMES"></a>

#### KEY\_NAMES

What Tk calls each named key, where the two notations differ.

The keys of this mapping are the names that `ActionSettings` documents, and
the values are the keysyms of Tk. The two of them agree about nothing but
`Tab`, which is in here anyway so that the mapping answers for every name
the notation has rather than for the ones that happen to differ.

<a id="edit_cfg_json_tk.key_names.tk_sequence"></a>

#### tk\_sequence

```python
def tk_sequence(combination: str) -> Optional[str]
```

Return one key combination as the event sequence that Tk binds by.

**Arguments**:

- `combination` - One key combination, as `ActionSettings` writes them.
  

**Returns**:

  The Tk event sequence of that combination, or None when it names a
  modifier or a key that this module does not know. None is not an
- `error` - the action it belongs to keeps its button and loses only
  this way of reaching it.

<a id="edit_cfg_json_tk.key_names.bind_key"></a>

#### bind\_key

```python
def bind_key(window: tkinter.Misc, key: str, command: Callable[[],
                                                               None]) -> None
```

Bind one key combination of one action, if Tk can bind it.

A combination that the translation does not know, or that Tk refuses,
leaves that action without that key rather than without an editor: every
action of this backend has a button as well.

**Arguments**:

- `window` - Window that the binding is made on.
- `key` - One key combination, as `ActionSettings` writes them.
- `command` - What that key does.

<a id="edit_cfg_json_tk.tk_look"></a>

# edit\_cfg\_json\_tk.tk\_look

How the Tk backend measures and colours the parts of its window.

The sizes, the colours and the labels of this backend are here rather than in
the module that builds the window, because they are what one has to look at
to know how the editor will look and they are what a later theming decision
will change. Nothing here knows what an edit model is: it is given a text, a
reason for that text to stand out, and a widget to put it in.

What each kind of text is stays in the core, as `edit_cfg_json.Emphasis`, and
what colour a kind is belongs here. Tk has no theme to ask, unlike the Textual
backend, which names colours of its terminal's theme and follows it into a
dark mode.

<a id="edit_cfg_json_tk.tk_look.NAME_COLUMN_WIDTH"></a>

#### NAME\_COLUMN\_WIDTH

Width in characters of the column that holds the member names.

<a id="edit_cfg_json_tk.tk_look.LEAST_FIELD_WIDTH"></a>

#### LEAST\_FIELD\_WIDTH

Width in characters that a field asks for, and can be squeezed to.

A field takes every bit of the width that the name and the marks of its member
leave over, so this is not how wide a field is: it is how far a field gives way
when the window is too narrow for all three. The marks are what a narrow window
would otherwise cut off, and a mark that is there and cannot be read is worse
than a field with fewer characters in view. The Textual backend gives way in
the same direction and for the same reason.

<a id="edit_cfg_json_tk.tk_look.PADDING"></a>

#### PADDING

Padding in pixels around the widgets of the editor.

<a id="edit_cfg_json_tk.tk_look.DESCRIPTION_INDENT"></a>

#### DESCRIPTION\_INDENT

Indentation in pixels of what is written below one member.

The indentation is what says that the line belongs to the member above it
rather than being a member of its own.

<a id="edit_cfg_json_tk.tk_look.TREE_INDENT"></a>

#### TREE\_INDENT

Indentation in pixels of each step inside a list or a dict.

The whole member is indented and not only its name, so that a name inside a
container is never cut off by the column that the names share. What that costs
is a value column that steps to the right with the tree, which is what a tree
looks like.

<a id="edit_cfg_json_tk.tk_look.FOLD_WIDTH"></a>

#### FOLD\_WIDTH

Width in characters of the control that folds one container.

Every row has one that wide, and the rows that hold nothing to fold have an
empty one, so that the names of a container and of a value beside it line up.

<a id="edit_cfg_json_tk.tk_look.LEAST_WRAP_WIDTH"></a>

#### LEAST\_WRAP\_WIDTH

Narrowest line in pixels that a paragraph of the editor is wrapped to.

A window can be made narrower than any text is readable in, and wrapping to
what is left of it would leave one word per line. Below this the text is cut
off by the window instead, which is the lesser of the two.

<a id="edit_cfg_json_tk.tk_look.EMPHASIS_COLOURS"></a>

#### EMPHASIS\_COLOURS

The colour of every reason the core has to show something differently.

One colour per member of `edit_cfg_json.Emphasis`, chosen to be read on the
light window that Tk gives this editor: a grey that is dark enough for a
paragraph of explanation to be comfortable rather than faint, and a blue, an
amber, a green and a red that carry on a light background.

Tk has no theme to ask, unlike the Textual backend, which names colours of its
terminal's theme and follows it into a dark mode. A Tk that has been put into
a dark mode by its platform would want other values here, and that belongs
with the rest of what an application decides rather than in the middle of a
backend; see section 9 of `doc/design.md`.

<a id="edit_cfg_json_tk.tk_look.FIELD_BACKGROUND"></a>

#### FIELD\_BACKGROUND

Background of a field the user can edit.

The window is white, so a field that kept the white background of its own
accord could not be told from a label: the values were there to be edited and
nothing said so. The tint plus the border below are what say it.

<a id="edit_cfg_json_tk.tk_look.FIELD_FOREGROUND"></a>

#### FIELD\_FOREGROUND

Colour of the text inside a field.

It is stated rather than inherited, because the background above is stated:
a platform that decided the text of a field should be white would otherwise
put white text on a light field.

<a id="edit_cfg_json_tk.tk_look.FIELD_BORDER"></a>

#### FIELD\_BORDER

Colour of the line around a field the user can edit.

<a id="edit_cfg_json_tk.tk_look.shown_text"></a>

#### shown\_text

```python
def shown_text(parent: tkinter.Misc,
               text: str,
               emphasis: Optional[core.Emphasis] = None,
               wrapping: bool = True) -> tkinter.Label
```

Return a label of the editor, in the colour its kind asks for.

**Arguments**:

- `parent` - Widget that becomes the parent of the created label.
- `text` - Text to show, left aligned as every text of the editor is.
- `emphasis` - Why this text stands out from the values, or None for the
  ordinary text colour of the platform.
- `wrapping` - Whether the text is a paragraph, which wraps to the width
  of the window. The mark of a member is the one text of the editor
  that is not: it belongs beside its field on one line.
  

**Returns**:

  A label showing that text.

<a id="edit_cfg_json_tk.tk_look.told"></a>

#### told

```python
def told(label: tkinter.Label, text: str, emphasis: core.Emphasis) -> None
```

Show one text of the editor, in the colour its state asks for.

**Arguments**:

- `label` - Label that shows it.
- `text` - Text to show.
- `emphasis` - Why that text stands out from the values.

<a id="edit_cfg_json_tk.tk_look.show_emphasis"></a>

#### show\_emphasis

```python
def show_emphasis(label: tkinter.Label,
                  emphasis: Optional[core.Emphasis]) -> None
```

Colour one label in the way one reason to stand out asks for.

A label with no emphasis is left in the colour of the platform, which is
what the values and their names are shown in: they are what the user came
to change, and they are the most legible thing on the screen because
nothing has been done to them.

**Arguments**:

- `label` - Label to colour.
- `emphasis` - Why the text of that label stands out, or None for the
  ordinary text colour.

<a id="edit_cfg_json_tk.tk_look.wrap_to_width"></a>

#### wrap\_to\_width

```python
def wrap_to_width(label: tkinter.Label) -> None
```

Make one label wrap its text to the width it is given.

A Tk label does not wrap at all unless it is told how wide a line may be,
and it does not shrink its text either: a paragraph wider than the window
is simply cut off, which is how a description lost its last words. The
width to wrap at is not known until the window has been laid out, and it
changes whenever the user resizes it, so it is followed rather than set.

**Arguments**:

- `label` - Label that holds text which may be longer than a line.

<a id="edit_cfg_json_tk.tk_look.label_text"></a>

#### label\_text

```python
def label_text(label: Optional[tkinter.Label]) -> str
```

Return the text one label is showing, empty when it is showing none.

A label that is out of the layout holds no text, because that is how this
backend hides one, so this answers what is on the window and not what a
widget happens to remember.

**Arguments**:

- `label` - Widget to read, or None for a widget that was never created.
  

**Returns**:

  The text that widget shows.

<a id="edit_cfg_json_tk.tk_look.place_text"></a>

#### place\_text

```python
def place_text(label: Optional[tkinter.Label], text: str) -> None
```

Put one text below a member into the layout, or take it out again.

Hiding is taking the widget out of the layout and emptying it, because a
label with text still takes the height of a line and a window with a
blank line under every member would have hidden nothing.

**Arguments**:

- `label` - Widget that shows one text below a member, or None for a text
  that this member can never have.
- `text` - Text to show, empty when there is nothing to show.

<a id="edit_cfg_json_tk.scrolling"></a>

# edit\_cfg\_json\_tk.scrolling

The part of a Tkinter editor that scrolls.

A configuration of any interesting size does not fit a window, and with the
explanations shown it fits one even less. Tk has no scrolling frame, so this
is the one it has: a canvas with a scrollbar beside it and a frame on the
canvas. What goes in the frame scrolls, and everything the editor keeps in
view is packed outside it.

It is a module of its own because none of it is about an edit model: it is
what Tk needs in order to have a scrolling area at all, and the editor uses
it the way it uses the toolkit.

<a id="edit_cfg_json_tk.scrolling.BODY_HEIGHT"></a>

#### BODY\_HEIGHT

Largest height in pixels that the scrolling part of the editor is given.

A configuration of any size therefore opens a window that fits a screen, and
what does not fit is scrolled to rather than lost. A configuration smaller
than this gets a window that is smaller than this, because the height is what
the body asks for up to this limit and not this limit.

<a id="edit_cfg_json_tk.scrolling.BODY_WIDTH"></a>

#### BODY\_WIDTH

Width in pixels that the scrolling part of the editor opens at.

A canvas asks for a width of its own that has nothing to do with what is on it,
so the width the editor opens at has to be said, and this is where it is said.

**It is said rather than measured, because the width of the body cannot be
measured.** Every paragraph wraps to the width it is given, so a body that has
been laid out asks for about the width it already has, whatever it would have
liked. Following that answer is what made showing the explanations flicker
between two window sizes for ever: the wrapped paragraph asked for a little
less than it was given, the canvas asked for that, the window narrowed, the
paragraph wrapped into one more line and asked for something else again. Found
at step 9 in a window and measured: one toggle cost 19099 resizes of the window
in two seconds and never stopped.

So the width is this, the height is what the body asks for up to a window's
worth, and a user who wants another width resizes the window — after which
every paragraph wraps to what there is. A small configuration therefore opens
in a window no taller than it needs, and this wide whatever it holds.

<a id="edit_cfg_json_tk.scrolling.ScrollingArea"></a>

## ScrollingArea Objects

```python
class ScrollingArea(NamedTuple)
```

The part of the editor that scrolls, before it has been placed.

<a id="edit_cfg_json_tk.scrolling.ScrollingArea.area"></a>

#### area

The frame to pack where the scrolling part of the editor belongs.

<a id="edit_cfg_json_tk.scrolling.ScrollingArea.body"></a>

#### body

The frame to build the scrolling part of the editor in.

<a id="edit_cfg_json_tk.scrolling.scrolling_body"></a>

#### scrolling\_body

```python
def scrolling_body(parent: tkinter.Misc) -> ScrollingArea
```

Return the frame that the scrolling part of the editor is built in.

The area is not packed here. Tk gives each child the space it asks for in
the order they were packed, so the part that does not scroll has to be
packed before this one to be sure of its space, while this one is created
first so that the widgets of the editor are created in the order they are
read in.

**Arguments**:

- `parent` - Widget that becomes the parent of the created widgets.
  

**Returns**:

  The frame to pack, and the frame to build in.

