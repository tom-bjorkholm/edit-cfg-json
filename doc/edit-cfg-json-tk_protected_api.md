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
    * [subtree](#edit_cfg_json_tk.tk_editor.RowWidgets.subtree)
    * [description](#edit_cfg_json_tk.tk_editor.RowWidgets.description)
    * [diagnostic](#edit_cfg_json_tk.tk_editor.RowWidgets.diagnostic)
    * [elements](#edit_cfg_json_tk.tk_editor.RowWidgets.elements)
  * [\_show\_below](#edit_cfg_json_tk.tk_editor._show_below)
  * [EditorWidgets](#edit_cfg_json_tk.tk_editor.EditorWidgets)
    * [\_\_init\_\_](#edit_cfg_json_tk.tk_editor.EditorWidgets.__init__)
    * [close\_editor](#edit_cfg_json_tk.tk_editor.EditorWidgets.close_editor)
    * [label\_text](#edit_cfg_json_tk.tk_editor.EditorWidgets.label_text)
    * [verdict\_text\_shown](#edit_cfg_json_tk.tk_editor.EditorWidgets.verdict_text_shown)
    * [save\_text\_shown](#edit_cfg_json_tk.tk_editor.EditorWidgets.save_text_shown)
    * [wrong\_shown](#edit_cfg_json_tk.tk_editor.EditorWidgets.wrong_shown)
    * [element\_texts](#edit_cfg_json_tk.tk_editor.EditorWidgets.element_texts)
    * [docstring\_shown](#edit_cfg_json_tk.tk_editor.EditorWidgets.docstring_shown)
    * [\_add\_docstring](#edit_cfg_json_tk.tk_editor.EditorWidgets._add_docstring)
    * [\_add\_load\_message](#edit_cfg_json_tk.tk_editor.EditorWidgets._add_load_message)
    * [\_add\_verdict](#edit_cfg_json_tk.tk_editor.EditorWidgets._add_verdict)
    * [\_add\_saving](#edit_cfg_json_tk.tk_editor.EditorWidgets._add_saving)
    * [\_add\_buttons](#edit_cfg_json_tk.tk_editor.EditorWidgets._add_buttons)
    * [\_add\_fold\_all](#edit_cfg_json_tk.tk_editor.EditorWidgets._add_fold_all)
    * [\_bind\_keys](#edit_cfg_json_tk.tk_editor.EditorWidgets._bind_keys)
    * [\_create\_rows](#edit_cfg_json_tk.tk_editor.EditorWidgets._create_rows)
    * [\_build\_rows](#edit_cfg_json_tk.tk_editor.EditorWidgets._build_rows)
    * [\_add\_row](#edit_cfg_json_tk.tk_editor.EditorWidgets._add_row)
    * [\_element\_changed](#edit_cfg_json_tk.tk_editor.EditorWidgets._element_changed)
    * [\_add\_subtree](#edit_cfg_json_tk.tk_editor.EditorWidgets._add_subtree)
    * [\_add\_fold](#edit_cfg_json_tk.tk_editor.EditorWidgets._add_fold)
    * [\_folder](#edit_cfg_json_tk.tk_editor.EditorWidgets._folder)
    * [\_fold\_all](#edit_cfg_json_tk.tk_editor.EditorWidgets._fold_all)
    * [\_show\_rows](#edit_cfg_json_tk.tk_editor.EditorWidgets._show_rows)
    * [\_show\_subtrees](#edit_cfg_json_tk.tk_editor.EditorWidgets._show_subtrees)
    * [\_indent](#edit_cfg_json_tk.tk_editor.EditorWidgets._indent)
    * [\_show\_fold\_all](#edit_cfg_json_tk.tk_editor.EditorWidgets._show_fold_all)
    * [\_show\_row\_texts](#edit_cfg_json_tk.tk_editor.EditorWidgets._show_row_texts)
    * [\_add\_description](#edit_cfg_json_tk.tk_editor.EditorWidgets._add_description)
    * [\_add\_value](#edit_cfg_json_tk.tk_editor.EditorWidgets._add_value)
    * [\_writer](#edit_cfg_json_tk.tk_editor.EditorWidgets._writer)
    * [\_leaver](#edit_cfg_json_tk.tk_editor.EditorWidgets._leaver)
    * [\_validate](#edit_cfg_json_tk.tk_editor.EditorWidgets._validate)
    * [\_save](#edit_cfg_json_tk.tk_editor.EditorWidgets._save)
    * [\_save\_as](#edit_cfg_json_tk.tk_editor.EditorWidgets._save_as)
    * [\_explain](#edit_cfg_json_tk.tk_editor.EditorWidgets._explain)
    * [\_show\_explanations](#edit_cfg_json_tk.tk_editor.EditorWidgets._show_explanations)
    * [\_show\_member\_texts](#edit_cfg_json_tk.tk_editor.EditorWidgets._show_member_texts)
    * [\_refresh](#edit_cfg_json_tk.tk_editor.EditorWidgets._refresh)
    * [\_show\_state](#edit_cfg_json_tk.tk_editor.EditorWidgets._show_state)
  * [TkEditor](#edit_cfg_json_tk.tk_editor.TkEditor)
    * [\_\_init\_\_](#edit_cfg_json_tk.tk_editor.TkEditor.__init__)
    * [run\_editor](#edit_cfg_json_tk.tk_editor.TkEditor.run_editor)
  * [edit](#edit_cfg_json_tk.tk_editor.edit)
* [edit\_cfg\_json\_tk.key\_names](#edit_cfg_json_tk.key_names)
  * [MODIFIERS](#edit_cfg_json_tk.key_names.MODIFIERS)
  * [KEY\_NAMES](#edit_cfg_json_tk.key_names.KEY_NAMES)
  * [\_tk\_key](#edit_cfg_json_tk.key_names._tk_key)
  * [tk\_sequence](#edit_cfg_json_tk.key_names.tk_sequence)
  * [\_key\_handler](#edit_cfg_json_tk.key_names._key_handler)
  * [bind\_key](#edit_cfg_json_tk.key_names.bind_key)
* [edit\_cfg\_json\_tk.tk\_look](#edit_cfg_json_tk.tk_look)
  * [NAME\_COLUMN\_WIDTH](#edit_cfg_json_tk.tk_look.NAME_COLUMN_WIDTH)
  * [LEAST\_FIELD\_WIDTH](#edit_cfg_json_tk.tk_look.LEAST_FIELD_WIDTH)
  * [PADDING](#edit_cfg_json_tk.tk_look.PADDING)
  * [DESCRIPTION\_INDENT](#edit_cfg_json_tk.tk_look.DESCRIPTION_INDENT)
  * [TREE\_INDENT](#edit_cfg_json_tk.tk_look.TREE_INDENT)
  * [FOLD\_WIDTH](#edit_cfg_json_tk.tk_look.FOLD_WIDTH)
  * [ELEMENT\_WIDTH](#edit_cfg_json_tk.tk_look.ELEMENT_WIDTH)
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
* [edit\_cfg\_json\_tk.tk\_elements](#edit_cfg_json_tk.tk_elements)
  * [ADD\_TEXT](#edit_cfg_json_tk.tk_elements.ADD_TEXT)
  * [REMOVE\_TEXT](#edit_cfg_json_tk.tk_elements.REMOVE_TEXT)
  * [EARLIER\_TEXT](#edit_cfg_json_tk.tk_elements.EARLIER_TEXT)
  * [LATER\_TEXT](#edit_cfg_json_tk.tk_elements.LATER_TEXT)
  * [element\_controls](#edit_cfg_json_tk.tk_elements.element_controls)
  * [\_control](#edit_cfg_json_tk.tk_elements._control)
  * [\_adder](#edit_cfg_json_tk.tk_elements._adder)
  * [\_remover](#edit_cfg_json_tk.tk_elements._remover)
  * [\_mover](#edit_cfg_json_tk.tk_elements._mover)
* [edit\_cfg\_json\_tk.scrolling](#edit_cfg_json_tk.scrolling)
  * [BODY\_HEIGHT](#edit_cfg_json_tk.scrolling.BODY_HEIGHT)
  * [BODY\_WIDTH](#edit_cfg_json_tk.scrolling.BODY_WIDTH)
  * [\_wheel\_step](#edit_cfg_json_tk.scrolling._wheel_step)
  * [\_scroll\_by](#edit_cfg_json_tk.scrolling._scroll_by)
  * [\_bind\_wheel](#edit_cfg_json_tk.scrolling._bind_wheel)
  * [\_fit\_body](#edit_cfg_json_tk.scrolling._fit_body)
  * [\_fit\_width](#edit_cfg_json_tk.scrolling._fit_width)
  * [ScrollingArea](#edit_cfg_json_tk.scrolling.ScrollingArea)
    * [area](#edit_cfg_json_tk.scrolling.ScrollingArea.area)
    * [body](#edit_cfg_json_tk.scrolling.ScrollingArea.body)
  * [scrolling\_body](#edit_cfg_json_tk.scrolling.scrolling_body)
* [edit\_cfg\_json\_tk.\_\_main\_\_](#edit_cfg_json_tk.__main__)
  * [PROGRAM](#edit_cfg_json_tk.__main__.PROGRAM)
  * [main](#edit_cfg_json_tk.__main__.main)
* [edit\_cfg\_json\_tk.tk\_ask](#edit_cfg_json_tk.tk_ask)
  * [SAVE\_AS\_TITLE](#edit_cfg_json_tk.tk_ask.SAVE_AS_TITLE)
  * [CONFIG\_FILES](#edit_cfg_json_tk.tk_ask.CONFIG_FILES)
  * [ALL\_FILES](#edit_cfg_json_tk.tk_ask.ALL_FILES)
  * [ADD\_KEY\_TITLE](#edit_cfg_json_tk.tk_ask.ADD_KEY_TITLE)
  * [ADD\_KEY\_PROMPT](#edit_cfg_json_tk.tk_ask.ADD_KEY_PROMPT)
  * [CLOSE\_TITLE](#edit_cfg_json_tk.tk_ask.CLOSE_TITLE)
  * [\_file\_types](#edit_cfg_json_tk.tk_ask._file_types)
  * [asked\_file](#edit_cfg_json_tk.tk_ask.asked_file)
  * [may\_close](#edit_cfg_json_tk.tk_ask.may_close)
  * [asked\_key](#edit_cfg_json_tk.tk_ask.asked_key)

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

Because it writes nothing, it is asked about while there is something in the
buffer that has not reached the file. That question is `tk_ask.may_close`, and
what it asks is the core's.

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

<a id="edit_cfg_json_tk.tk_editor.RowWidgets.subtree"></a>

#### subtree

The widget that says what this object is on its own.

It is None for every node that is not a nested configuration object,
because nothing else is a configuration that can be asked about itself.

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

<a id="edit_cfg_json_tk.tk_editor.RowWidgets.elements"></a>

#### elements

The controls that change how many elements this node holds.

A node is given exactly the ones it offers and nothing at all where it
offers none, because they sit at the end of the line rather than in a
column that every row has to keep clear. Which of them a node offers can
change — the first element of a list cannot move up until something is put
in front of it — and the rows are built again whenever it does.

<a id="edit_cfg_json_tk.tk_editor._show_below"></a>

#### \_show\_below

```python
def _show_below(widgets: RowWidgets, description: str,
                diagnostic: str) -> None
```

Show what belongs below one member, in the order it belongs in.

Both texts are taken out of the layout and put back rather than only the
one that changed, because Tk packs a widget after the ones that are
already there: a description that came back while a diagnostic was
showing would otherwise land below it. Nothing is touched while both
texts are already what they should be, so the ordinary case of typing
into a field does not lay the window out again on every key.

**Arguments**:

- `widgets` - Widgets of the member.
- `description` - What the member is for, empty while that is hidden.
- `diagnostic` - What is wrong with the member, empty when nothing is.

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

<a id="edit_cfg_json_tk.tk_editor.EditorWidgets.close_editor"></a>

#### close\_editor

```python
def close_editor() -> None
```

End the session, asking first where there is something to lose.

This is what every way out of the editor does: the button, the key of
the quit action, and the close button of a window that this backend
owns. A way out that dropped the changes without a word would be the
one thing an editor must not do, and having one method for all of
them is what keeps any of them from becoming that.

What closing itself does is what the caller said it does, which is
destroying the window for a caller that owns one.

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

<a id="edit_cfg_json_tk.tk_editor.EditorWidgets.element_texts"></a>

#### element\_texts

```python
@property
def element_texts() -> list[list[str]]
```

Return what the controls of each node say, in row order.

Most of them are empty, because most nodes offer nothing about how
many things they hold: a value is not something that holds elements,
and the members of a configuration object are the ones its class
declares.

<a id="edit_cfg_json_tk.tk_editor.EditorWidgets.docstring_shown"></a>

#### docstring\_shown

```python
@property
def docstring_shown() -> str
```

Return the text that the label of the configuration class shows.

<a id="edit_cfg_json_tk.tk_editor.EditorWidgets._add_docstring"></a>

#### \_add\_docstring

```python
def _add_docstring(parent: tkinter.Misc) -> Optional[tkinter.Label]
```

Show what the configuration class says about itself, if anything.

The widget is created only when that class has a docstring of its
own. What the explain action changes is how much of a docstring is
shown and not whether there is one, so a class without one would
leave an empty widget taking a line of the window for good.

**Arguments**:

- `parent` - Widget that becomes the parent of the created widget.
  

**Returns**:

  The widget that shows the docstring, or None when the
  configuration class has none.

<a id="edit_cfg_json_tk.tk_editor.EditorWidgets._add_load_message"></a>

#### \_add\_load\_message

```python
def _add_load_message(parent: tkinter.Misc) -> None
```

Show what reading the input file did, when it did anything.

The widget is created only when there is something to say. The file
was read before the model was built, so the message cannot arrive
later, and an empty widget would take a line of the window for a
message that will never come.

<a id="edit_cfg_json_tk.tk_editor.EditorWidgets._add_verdict"></a>

#### \_add\_verdict

```python
def _add_verdict(parent: tkinter.Misc) -> tkinter.Label
```

Create the label that says what the application makes of these.

It is packed below the scrolling part rather than at the end of it, so
that it cannot scroll away: a user who has just asked what the
application makes of these values is looking at it.

<a id="edit_cfg_json_tk.tk_editor.EditorWidgets._add_saving"></a>

#### \_add\_saving

```python
def _add_saving(parent: tkinter.Misc) -> tkinter.Label
```

Create the label that says what saving did, or where it would.

<a id="edit_cfg_json_tk.tk_editor.EditorWidgets._add_buttons"></a>

#### \_add\_buttons

```python
def _add_buttons(parent: tkinter.Misc,
                 explained: tkinter.BooleanVar) -> Optional[tkinter.Button]
```

Create the buttons, the tick-box and the one that ends the run.

They share one row, because six of them stacked above each other
would push the values of a real configuration off the window.

The explanations get a tick-box rather than a button, because the
action is a toggle: a button saying Explain beside explanations that
are already there would be offering something that has been done. The
folding gets a button that is renamed instead, because a partly
folded configuration is neither of the two states a tick could show.

**Arguments**:

- `parent` - Widget that becomes the parent of the button row.
- `explained` - Whether the tick-box of the explanations is ticked.
  

**Returns**:

  The button that folds everything, or None for a configuration
  that has nothing to fold.

<a id="edit_cfg_json_tk.tk_editor.EditorWidgets._add_fold_all"></a>

#### \_add\_fold\_all

```python
def _add_fold_all(parent: tkinter.Misc) -> Optional[tkinter.Button]
```

Create the button that folds or opens every container, if any.

**Arguments**:

- `parent` - Widget that becomes the parent of the created button.
  

**Returns**:

  That button, or None for a configuration with no list and no
  dict in it, which has nothing for the action to do.

<a id="edit_cfg_json_tk.tk_editor.EditorWidgets._bind_keys"></a>

#### \_bind\_keys

```python
def _bind_keys(window: tkinter.Misc) -> None
```

Bind the key combinations that the application chose.

The bindings are made on the window and not on each field, because
a key that a field does not use for itself reaches the window that
the field is in. Nothing is bound for the cancel action: the only
question this backend asks is the toolkit's own file dialog, which
answers that key itself. Nothing is bound for the folding either
where there is nothing to fold, for the same reason as the button.

The keys are read once, here, which is the whole of what a later
answer from a settings callable cannot change.

**Arguments**:

- `window` - Window that the bindings are made on.

<a id="edit_cfg_json_tk.tk_editor.EditorWidgets._create_rows"></a>

#### \_create\_rows

```python
def _create_rows() -> None
```

Create the widgets of every node, replacing the ones there are.

Nothing is put into the layout here, because which of the rows are
shown is what `_show_rows` decides, and because the widgets that do
not scroll have to be packed before these whatever order they are
created in.

<a id="edit_cfg_json_tk.tk_editor.EditorWidgets._build_rows"></a>

#### \_build\_rows

```python
def _build_rows() -> None
```

Make the widgets of every node again and put them on the window.

Two things change how many rows the model has. A validation pass does,
because a validator that normalizes a list changes how many values it
holds, and there the widgets are made again only when the paths no
longer match: every other refresh leaves them alone, which is what
keeps the focus where the user put it. Adding, removing or moving an
element does, and there they are always made again, because which
controls a row offers changes with them.

<a id="edit_cfg_json_tk.tk_editor.EditorWidgets._add_row"></a>

#### \_add\_row

```python
def _add_row(parent: tkinter.Misc, row: core.MemberRow) -> RowWidgets
```

Create the widgets of one node, and its description below them.

The node gets a frame of its own, holding the line that is edited
and the texts under it, so that hiding one of those and showing it
again cannot move it away from the node it belongs to. That frame is
also what folding takes out of the layout, which is why it is not
packed here but by `_show_rows`.

<a id="edit_cfg_json_tk.tk_editor.EditorWidgets._element_changed"></a>

#### \_element\_changed

```python
def _element_changed() -> None
```

Show the rows that the model has after an element changed.

The widgets are always made again, and not only where the paths
differ as a validation pass leaves them: which controls a row offers
changes with the elements, so a row that is still at the same path is
not necessarily still offering the same things.

<a id="edit_cfg_json_tk.tk_editor.EditorWidgets._add_subtree"></a>

#### \_add\_subtree

```python
@staticmethod
def _add_subtree(parent: tkinter.Misc,
                 row: core.MemberRow) -> Optional[tkinter.Label]
```

Create the widget that says what one object is on its own.

A node that is no configuration object gets no widget, by the same
rule as the description below the row: a widget that could never hold
anything is a piece of the window spent on nothing.

It does not wrap, exactly as the mark beside it does not: it belongs
on the line of its node, and a narrow window squeezes the values
rather than this.

**Arguments**:

- `parent` - Line of the node that is being shown.
- `row` - Node to create the widget for.
  

**Returns**:

  The widget that says what that object is on its own, or None for
  a node that is not one.

<a id="edit_cfg_json_tk.tk_editor.EditorWidgets._add_fold"></a>

#### \_add\_fold

```python
def _add_fold(parent: tkinter.Misc,
              row: core.MemberRow) -> Optional[tkinter.Button]
```

Create the control that folds one container, if it is one.

A node that holds nothing gets a label of the same width instead of
no widget at all, so that the names of a container and of a value
beside it begin in the same column. A configuration with nothing to
fold anywhere gets no column at all, because a column that could
never hold anything is width taken from the values for nothing.

**Arguments**:

- `parent` - Line of the node that is being shown.
- `row` - Node to create the control for.
  

**Returns**:

  The control that folds that container, or None for a node that
  is not one.

<a id="edit_cfg_json_tk.tk_editor.EditorWidgets._folder"></a>

#### \_folder

```python
def _folder(path: ConfigPath) -> Callable[[], None]
```

Return the command that folds one container or opens it again.

<a id="edit_cfg_json_tk.tk_editor.EditorWidgets._fold_all"></a>

#### \_fold\_all

```python
def _fold_all() -> None
```

Fold every container away, or open every one of them.

<a id="edit_cfg_json_tk.tk_editor.EditorWidgets._show_rows"></a>

#### \_show\_rows

```python
def _show_rows() -> None
```

Put every node that is shown into the layout, in its order.

Every one of them is taken out first and put back afterwards, because
Tk packs a widget after the ones that are already there: a node that
came back would otherwise land below the ones below it. Nothing here
is created or destroyed, so a field the user was typing into keeps
what is in it while its container is folded and opened again.

What is said below the nodes is shown again as well, because folding a
nested configuration object changes it: an object that is showing less
of itself says less about itself.

<a id="edit_cfg_json_tk.tk_editor.EditorWidgets._show_subtrees"></a>

#### \_show\_subtrees

```python
def _show_subtrees() -> None
```

Say what each nested object is on its own, as the model says now.

It is shown after folding as well as after a validation pass, because
folding a nested object is one of the moments the model asks that
object about itself.

<a id="edit_cfg_json_tk.tk_editor.EditorWidgets._indent"></a>

#### \_indent

```python
@staticmethod
def _indent(row: core.MemberRow) -> int
```

Return how far from the left edge one node begins, in pixels.

<a id="edit_cfg_json_tk.tk_editor.EditorWidgets._show_fold_all"></a>

#### \_show\_fold\_all

```python
def _show_fold_all() -> None
```

Say what the next press of the fold button will do.

<a id="edit_cfg_json_tk.tk_editor.EditorWidgets._show_row_texts"></a>

#### \_show\_row\_texts

```python
def _show_row_texts(row: core.MemberRow, widgets: RowWidgets) -> None
```

Show what the model says belongs below one node.

<a id="edit_cfg_json_tk.tk_editor.EditorWidgets._add_description"></a>

#### \_add\_description

```python
@staticmethod
def _add_description(parent: tkinter.Misc,
                     row: core.MemberRow) -> Optional[tkinter.Label]
```

Create the widget that says what one node is for, if anything.

A node that nothing is said about gets no widget, because there is
nothing that could ever appear in it. Whether anything can be is asked
of the core, because the description the row carries is not the whole
of what is said below a nested configuration object.

**Arguments**:

- `parent` - Frame of the node that is being described.
- `row` - Node to describe.
  

**Returns**:

  The widget that shows the description, or None when nothing is
  said about this node.

<a id="edit_cfg_json_tk.tk_editor.EditorWidgets._add_value"></a>

#### \_add\_value

```python
def _add_value(parent: tkinter.Misc,
               row: core.MemberRow) -> Optional[tkinter.StringVar]
```

Create the value widget of one member and wire it to the model.

A node that the model cannot edit gets a widget that only shows text,
because there is nothing the user could do to it: a list, a dict and a
nested configuration object are each edited through the rows below
them, and a declared member that holds no object holds no text either.

The variable is given the parent as its master, so that it is
created in the same Tcl interpreter as the field that reads it. A
variable constructed without one is created in the first interpreter
of the process instead, which is the wrong one as soon as the editor
is not the only Tk in the application: the field would then show
nothing and the callback below would never run.

<a id="edit_cfg_json_tk.tk_editor.EditorWidgets._writer"></a>

#### \_writer

```python
def _writer(row: core.MemberRow,
            field: tkinter.StringVar) -> Callable[..., None]
```

Return the callback that writes one field into the model.

Tk reports a change of the variable and not of the widget, so the
callback reads the field itself. Every change is written through,
including the ones that no key press caused, such as a paste.

<a id="edit_cfg_json_tk.tk_editor.EditorWidgets._leaver"></a>

#### \_leaver

```python
def _leaver(row: core.MemberRow) -> Callable[..., None]
```

Return the callback that one field runs when it loses the focus.

Leaving a field is when the user has moved on from it, and it is
therefore when the editor says whether what they typed means a value
of that member at all. Nothing is validated here: the whole
configuration is what a validation pass is about, and this is one
field answering for itself.

<a id="edit_cfg_json_tk.tk_editor.EditorWidgets._validate"></a>

#### \_validate

```python
def _validate() -> None
```

Validate the buffer and show what the application would say.

<a id="edit_cfg_json_tk.tk_editor.EditorWidgets._save"></a>

#### \_save

```python
def _save() -> None
```

Write the output file, and say what came of trying.

Saving validates, so it can rewrite a value exactly as validating
can, and the fields are refreshed for the same reason.

A session that has no file to write yet is asked where to write,
which is what every editor does and what the design asks a backend
for. There is no way round to loop back here, because the question
is what gives the session a file.

<a id="edit_cfg_json_tk.tk_editor.EditorWidgets._save_as"></a>

#### \_save\_as

```python
def _save_as() -> None
```

Ask which file to write, and write it when one was named.

The name that comes back is handed to the model, which is what
completes it and what refuses it, so that a user of this backend and
a user of the other one are told the same thing about one name.

<a id="edit_cfg_json_tk.tk_editor.EditorWidgets._explain"></a>

#### \_explain

```python
def _explain() -> None
```

Show or hide what the application says about these values.

<a id="edit_cfg_json_tk.tk_editor.EditorWidgets._show_explanations"></a>

#### \_show\_explanations

```python
def _show_explanations() -> None
```

Show as much of the explanatory text as the model says to show.

The tick-box is set from the model rather than left to Tk, because Tk
only flips it when it is the tick-box that was pressed. The key of the
explain action reaches this method without touching it, and a tick
that disagreed with the window would be worse than no tick at all.

It is not part of `_show_state`, which runs on every key the user
types: nothing the user types into a field can change what this
configuration is for or what one of its members means.

<a id="edit_cfg_json_tk.tk_editor.EditorWidgets._show_member_texts"></a>

#### \_show\_member\_texts

```python
def _show_member_texts() -> None
```

Show what belongs below every node, as the model says it now.

<a id="edit_cfg_json_tk.tk_editor.EditorWidgets._refresh"></a>

#### \_refresh

```python
def _refresh() -> None
```

Write the buffer back into the fields and show the new state.

A pass over the buffer is not read only: a member validator returns
the value that is stored back into the member, so a value can end up
different from the one the user typed. Writing the text the model
already holds into a field is not an edit, so this refresh does not
undo the marks that the pass has just set.

A pass can also leave the model with other rows than it had, which a
validator that normalizes a list does, and the widgets are then made
again rather than written into.

<a id="edit_cfg_json_tk.tk_editor.EditorWidgets._show_state"></a>

#### \_show\_state

```python
def _show_state() -> None
```

Show the label, the verdict, the saving and every member.

The verdict and the saving change colour as well as text, because what
they say is either what the application accepted, what it refused, or
what has not been asked of it yet, and a user who has to read three
lines to tell those apart is reading too much.

What is wrong with a member is shown here too, and not with the
explanations: a description says what a member is for and stays until
the user asks for it to go, while a refusal is answered afresh by
every pass and by every field that is left.

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

The close button of the window is made to do what the Close button of
the editor does, so that the one way out that is not a widget of the
editor cannot be the one way out that drops the changes without
asking. It is set on this window and on no other: the editor never
touches a window it did not create.

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

<a id="edit_cfg_json_tk.key_names._tk_key"></a>

#### \_tk\_key

```python
def _tk_key(key: str, shifted: bool) -> Optional[str]
```

Return the keysym that Tk knows one key by.

A single character is that character, in upper case when the
combination also names the shift, because Tk reads `<Control-S>` as the
shifted key and `<Control-s>` as the unshifted one.

**Arguments**:

- `key` - The part of a combination that is not a modifier.
- `shifted` - Whether the combination also names the shift.
  

**Returns**:

  The keysym of that key, or None when this module does not know it.

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

<a id="edit_cfg_json_tk.key_names._key_handler"></a>

#### \_key\_handler

```python
def _key_handler(command: Callable[[], None]) -> Callable[..., str]
```

Return the callback that runs one command for one key event.

**Arguments**:

- `command` - What that key does.
  

**Returns**:

  A callback that Tk can bind, which stops the event from being
  handled a second time by whatever else the window is bound to.

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

<a id="edit_cfg_json_tk.tk_look.ELEMENT_WIDTH"></a>

#### ELEMENT\_WIDTH

Width in characters of one control that changes how many elements there are.

They sit at the end of the line of the node they belong to, so a row that
offers none of them needs no width held for it and gets none. That is what
makes four of them affordable where the one control that folds a container has
to keep a column clear on every row.

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

<a id="edit_cfg_json_tk.tk_elements"></a>

# edit\_cfg\_json\_tk.tk\_elements

The Tk controls that change how many elements a node holds.

They are here rather than in the module that builds the window for the reason
every other split of this backend was made: one module of a thousand lines is
one nobody reads to the end. What is here is one row's worth of controls, and
nothing else: the question that one of them has to ask is in `tk_ask`, with
the other question this backend asks.

Nothing here decides *whether* a node offers anything. That is
`edit_cfg_json.MemberRow.offer`, which the core works out once so that the two
backends cannot offer different things.

<a id="edit_cfg_json_tk.tk_elements.ADD_TEXT"></a>

#### ADD\_TEXT

Text of the control that puts one more element into a node.

It is a word and not the `+` of the fold control beside it, because the two do
different things and one row can have both: a list of configuration objects
folds away and grows, and two controls saying `+` on one line would be two
offers that could not be told apart.

<a id="edit_cfg_json_tk.tk_elements.REMOVE_TEXT"></a>

#### REMOVE\_TEXT

Text of the control that takes one element out of what holds it.

<a id="edit_cfg_json_tk.tk_elements.EARLIER_TEXT"></a>

#### EARLIER\_TEXT

Text of the control that moves one element towards the front.

<a id="edit_cfg_json_tk.tk_elements.LATER_TEXT"></a>

#### LATER\_TEXT

Text of the control that moves one element towards the back.

<a id="edit_cfg_json_tk.tk_elements.element_controls"></a>

#### element\_controls

```python
def element_controls(parent: tkinter.Misc, row: core.MemberRow,
                     model: core.EditModel,
                     after: Callable[[], None]) -> tuple[tkinter.Button, ...]
```

Create the controls that change how many elements one node holds.

They are put at the end of the line of the node, after the value and the
marks, so a node that offers none of them costs the values no width at
all. That is what makes four of them affordable where the one control
that folds a container has to keep a column clear on every row.

**Arguments**:

- `parent` - Line of the node that is being shown.
- `row` - Node to create the controls for.
- `model` - Model that the change is made in.
- `after` - What to do once the model has changed, which is to make the
  widgets again: a change of the elements changes how many rows
  there are and which controls each of them offers.
  

**Returns**:

  The controls that node offers, and nothing at all for one that offers
  none, which is most nodes of most configurations.

<a id="edit_cfg_json_tk.tk_elements._control"></a>

#### \_control

```python
def _control(parent: tkinter.Misc, text: str,
             command: Callable[[], None]) -> tkinter.Button
```

Create one control that changes how many elements there are.

<a id="edit_cfg_json_tk.tk_elements._adder"></a>

#### \_adder

```python
def _adder(row: core.MemberRow, model: core.EditModel,
           after: Callable[[], None]) -> Callable[[], None]
```

Return the command that puts one more element into one node.

<a id="edit_cfg_json_tk.tk_elements._remover"></a>

#### \_remover

```python
def _remover(row: core.MemberRow, model: core.EditModel,
             after: Callable[[], None]) -> Callable[[], None]
```

Return the command that takes one element out of what holds it.

<a id="edit_cfg_json_tk.tk_elements._mover"></a>

#### \_mover

```python
def _mover(row: core.MemberRow, model: core.EditModel,
           after: Callable[[], None], later: bool) -> Callable[[], None]
```

Return the command that moves one element by one place.

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

<a id="edit_cfg_json_tk.scrolling._wheel_step"></a>

#### \_wheel\_step

```python
def _wheel_step(event: 'tkinter.Event[tkinter.Misc]') -> int
```

Return which way one reported turn of the mouse wheel goes.

The type of the event is written as text here and in the three callbacks
around it, because `tkinter.Event` is a generic class to a type checker and
a plain one at runtime: Python 3.12 and 3.13 evaluate an annotation where
it is written, and subscripting it there is an error.

Only the sign of the delta is used. Its size means different things on
different platforms, and one line per turn is a scroll everyone can
follow.

**Arguments**:

- `event` - The wheel event that Tk reported.
  

**Returns**:

  How far to scroll the body, in lines.

<a id="edit_cfg_json_tk.scrolling._scroll_by"></a>

#### \_scroll\_by

```python
def _scroll_by(canvas: tkinter.Canvas,
               step: Optional[int]) -> Callable[..., str]
```

Return the callback that one turn of the mouse wheel runs.

**Arguments**:

- `canvas` - Canvas that holds the scrolling part of the editor.
- `step` - How far to scroll, or None to read it from the event. X11
  reports a wheel as two buttons and says nothing about how far,
  while every other platform reports a delta whose sign is the
  direction.
  

**Returns**:

  A callback that Tk can bind, which stops the event from being handled
  a second time by whatever else the window is bound to.

<a id="edit_cfg_json_tk.scrolling._bind_wheel"></a>

#### \_bind\_wheel

```python
def _bind_wheel(window: tkinter.Misc, canvas: tkinter.Canvas) -> None
```

Let the mouse wheel scroll the body, however it is reported.

The bindings are made on the window rather than on the canvas, because a
wheel event goes to the widget under the pointer and the pointer is
usually over a field or a label inside the body. That is the same window
the keys are bound on, and it is the same open question for the same
reason: an editor mounted in a window it shares would be claiming the
wheel of a whole application. See section 8.2.7 of `doc/design.md`.

**Arguments**:

- `window` - Window that the bindings are made on.
- `canvas` - Canvas that holds the scrolling part of the editor.

<a id="edit_cfg_json_tk.scrolling._fit_body"></a>

#### \_fit\_body

```python
def _fit_body(canvas: tkinter.Canvas,
              body: tkinter.Frame) -> Callable[..., None]
```

Return the callback that follows the height of the body.

It is what makes the canvas scroll: a canvas shows the part of its
contents that its scroll region says is there, and the contents of this
one grow and shrink as the explanations are shown and hidden. The height
follows too, up to the height of a window, so that showing the
explanations makes the window taller while there is room for it.

**The width is deliberately not followed**, and `BODY_WIDTH` says why it
cannot be.

**Arguments**:

- `canvas` - Canvas that holds the body.
- `body` - Frame that holds everything that scrolls.
  

**Returns**:

  A callback for the event that says the body has been laid out.

<a id="edit_cfg_json_tk.scrolling._fit_width"></a>

#### \_fit\_width

```python
def _fit_width(canvas: tkinter.Canvas, item: int) -> Callable[..., None]
```

Return the callback that gives the body the width of the canvas.

An item on a canvas is as wide as it asks to be, so without this the
fields would keep the width they wanted rather than the width there is.

**Arguments**:

- `canvas` - Canvas that holds the body.
- `item` - The canvas item that the body was put on.
  

**Returns**:

  A callback for the event that says the canvas has been resized.

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

<a id="edit_cfg_json_tk.__main__"></a>

# edit\_cfg\_json\_tk.\_\_main\_\_

The `edit-cfg-json-tk` program: edit any configuration class in a window.

It is the same program as `edit-cfg-json` with this package's backend in place
of the one that prints, so everything about its command line is documented in
`edit_cfg_json.cli`. What it opens is a Tk window with a field per member of
the configuration class it was told to edit.

Run it as `edit-cfg-json-tk`, or as `python -m edit_cfg_json_tk` on a machine
whose script folder is not on the path.

<a id="edit_cfg_json_tk.__main__.PROGRAM"></a>

#### PROGRAM

Name that this program is installed under.

<a id="edit_cfg_json_tk.__main__.main"></a>

#### main

```python
def main(args: Optional[Sequence[str]] = None) -> int
```

Run this program and return what it ends with.

**Arguments**:

- `args` - Optional replacement for `sys.argv[1:]`, mainly for tests.
  

**Returns**:

  What this run ends with, as one of `edit_cfg_json.ExitCode`.

<a id="edit_cfg_json_tk.tk_ask"></a>

# edit\_cfg\_json\_tk.tk\_ask

The questions this backend asks the user, and the words of each of them.

There are three of them — which file to write, what a new entry of a dict is
to be called, and whether the changes that have not been saved may be dropped
— and they are here together rather than in the modules that raise them, for
the reason every other split of this backend was made: one module of a
thousand lines is one nobody reads to the end. Keeping them together is also
what makes it plain that this backend asks the toolkit for all three of its
questions, where the Textual one has to build a screen for them.

Nothing here decides *whether* a question is asked. Which file to write is
asked where the model has no destination, what a new entry is called where
`edit_cfg_json.MemberRow.offer` says a key is needed, and whether there is
anything to lose by closing is `edit_cfg_json.close_question`. All three are
the core's, so that the two backends cannot ask one user something and another
user nothing.

<a id="edit_cfg_json_tk.tk_ask.SAVE_AS_TITLE"></a>

#### SAVE\_AS\_TITLE

Title of the dialog that asks which file to write.

<a id="edit_cfg_json_tk.tk_ask.CONFIG_FILES"></a>

#### CONFIG\_FILES

What the dialog calls the files of the extension the application uses.

<a id="edit_cfg_json_tk.tk_ask.ALL_FILES"></a>

#### ALL\_FILES

What the dialog calls every other file.

<a id="edit_cfg_json_tk.tk_ask.ADD_KEY_TITLE"></a>

#### ADD\_KEY\_TITLE

Title of the dialog that asks what a new entry of a dict is called.

<a id="edit_cfg_json_tk.tk_ask.ADD_KEY_PROMPT"></a>

#### ADD\_KEY\_PROMPT

What that dialog asks, naming the member that is about to grow.

<a id="edit_cfg_json_tk.tk_ask.CLOSE_TITLE"></a>

#### CLOSE\_TITLE

Title of the dialog that asks whether the changes may be dropped.

<a id="edit_cfg_json_tk.tk_ask._file_types"></a>

#### \_file\_types

```python
def _file_types(settings: core.Settings) -> list[tuple[str, str]]
```

Return what the dialog that asks for a file offers to filter by.

An application that enforces its extension has that one filter and no
other, because a name with another extension cannot be saved and a
dialog that offered to look for one would be inviting a refusal. An
application whose extension is a default offers it first and everything
else after it, because a name with another extension can be saved. An
application with no opinion offers nothing, which is what this dialog
did before there were settings at all.

**Arguments**:

- `settings` - What the application has decided about file names.
  

**Returns**:

  The file types of the dialog, empty when it has no opinion.

<a id="edit_cfg_json_tk.tk_ask.asked_file"></a>

#### asked\_file

```python
def asked_file(settings: core.Settings) -> str
```

Ask which file to write, with what the application uses offered first.

What the dialog offers is what the application decided: the extension it
uses for its configuration is the one the dialog adds to a name that has
none, and the one it offers to filter by.

**Arguments**:

- `settings` - What the application has decided about file names.
  

**Returns**:

  The file that was named, and nothing at all where the question was
  left unanswered.

<a id="edit_cfg_json_tk.tk_ask.may_close"></a>

#### may\_close

```python
def may_close(model: core.EditModel) -> bool
```

Return whether the editor may close, asking where there is a question.

Closing writes nothing, so a session with something in the buffer that
has not reached the file loses it. What is asked and whether there is
anything to ask about are the core's; putting the question is this
backend's, and the toolkit has a dialog for exactly this.

The answer that keeps the editor open is the one the dialog starts on, so
that a user who answers without reading keeps their changes. The dialog is
modal, which is what makes the question a question: the editor behind it
cannot be closed a second time while it is up.

**Arguments**:

- `model` - Model that is about to be closed.
  

**Returns**:

  Whether the session may end, which is always so while there is
  nothing that closing would lose.

<a id="edit_cfg_json_tk.tk_ask.asked_key"></a>

#### asked\_key

```python
def asked_key(row: core.MemberRow) -> Optional[str]
```

Ask what a new entry of one dict is to be called.

A new entry of a dict has to be called something, and nothing but the
person configuring the application knows what. A key the dict already
holds is asked about again rather than allowed to take the place of what
is there: the model refuses such a key, and an editor that let the
question be answered with one would be offering to lose an entry.

**Arguments**:

- `row` - Node that is about to be given an entry.
  

**Returns**:

  The key that was named, and None where the question was left
  unanswered or answered with nothing.

