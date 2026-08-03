# Table of Contents

* [edit\_cfg\_json\_tk.tk\_editor](#edit_cfg_json_tk.tk_editor)
  * [NAME\_COLUMN\_WIDTH](#edit_cfg_json_tk.tk_editor.NAME_COLUMN_WIDTH)
  * [LEAST\_FIELD\_WIDTH](#edit_cfg_json_tk.tk_editor.LEAST_FIELD_WIDTH)
  * [PADDING](#edit_cfg_json_tk.tk_editor.PADDING)
  * [DESCRIPTION\_INDENT](#edit_cfg_json_tk.tk_editor.DESCRIPTION_INDENT)
  * [LEAST\_WRAP\_WIDTH](#edit_cfg_json_tk.tk_editor.LEAST_WRAP_WIDTH)
  * [EMPHASIS\_COLOURS](#edit_cfg_json_tk.tk_editor.EMPHASIS_COLOURS)
  * [FIELD\_BACKGROUND](#edit_cfg_json_tk.tk_editor.FIELD_BACKGROUND)
  * [FIELD\_FOREGROUND](#edit_cfg_json_tk.tk_editor.FIELD_FOREGROUND)
  * [FIELD\_BORDER](#edit_cfg_json_tk.tk_editor.FIELD_BORDER)
  * [VALIDATE\_TEXT](#edit_cfg_json_tk.tk_editor.VALIDATE_TEXT)
  * [SAVE\_TEXT](#edit_cfg_json_tk.tk_editor.SAVE_TEXT)
  * [SAVE\_AS\_TEXT](#edit_cfg_json_tk.tk_editor.SAVE_AS_TEXT)
  * [EXPLAIN\_TEXT](#edit_cfg_json_tk.tk_editor.EXPLAIN_TEXT)
  * [CLOSE\_TEXT](#edit_cfg_json_tk.tk_editor.CLOSE_TEXT)
  * [SAVE\_AS\_TITLE](#edit_cfg_json_tk.tk_editor.SAVE_AS_TITLE)
  * [CONFIG\_FILES](#edit_cfg_json_tk.tk_editor.CONFIG_FILES)
  * [ALL\_FILES](#edit_cfg_json_tk.tk_editor.ALL_FILES)
  * [\_file\_types](#edit_cfg_json_tk.tk_editor._file_types)
  * [\_key\_handler](#edit_cfg_json_tk.tk_editor._key_handler)
  * [\_bind\_key](#edit_cfg_json_tk.tk_editor._bind_key)
  * [\_shown\_text](#edit_cfg_json_tk.tk_editor._shown_text)
  * [\_told](#edit_cfg_json_tk.tk_editor._told)
  * [\_show\_emphasis](#edit_cfg_json_tk.tk_editor._show_emphasis)
  * [\_wrap\_to\_width](#edit_cfg_json_tk.tk_editor._wrap_to_width)
  * [\_label\_text](#edit_cfg_json_tk.tk_editor._label_text)
  * [\_place\_text](#edit_cfg_json_tk.tk_editor._place_text)
  * [StateWidgets](#edit_cfg_json_tk.tk_editor.StateWidgets)
    * [title](#edit_cfg_json_tk.tk_editor.StateWidgets.title)
    * [docstring](#edit_cfg_json_tk.tk_editor.StateWidgets.docstring)
    * [verdict](#edit_cfg_json_tk.tk_editor.StateWidgets.verdict)
    * [saving](#edit_cfg_json_tk.tk_editor.StateWidgets.saving)
    * [explained](#edit_cfg_json_tk.tk_editor.StateWidgets.explained)
  * [RowWidgets](#edit_cfg_json_tk.tk_editor.RowWidgets)
    * [field](#edit_cfg_json_tk.tk_editor.RowWidgets.field)
    * [mark](#edit_cfg_json_tk.tk_editor.RowWidgets.mark)
    * [description](#edit_cfg_json_tk.tk_editor.RowWidgets.description)
    * [diagnostic](#edit_cfg_json_tk.tk_editor.RowWidgets.diagnostic)
  * [\_show\_below](#edit_cfg_json_tk.tk_editor._show_below)
  * [EditorWidgets](#edit_cfg_json_tk.tk_editor.EditorWidgets)
    * [\_\_init\_\_](#edit_cfg_json_tk.tk_editor.EditorWidgets.__init__)
    * [label\_text](#edit_cfg_json_tk.tk_editor.EditorWidgets.label_text)
    * [verdict\_text\_shown](#edit_cfg_json_tk.tk_editor.EditorWidgets.verdict_text_shown)
    * [save\_text\_shown](#edit_cfg_json_tk.tk_editor.EditorWidgets.save_text_shown)
    * [wrong\_shown](#edit_cfg_json_tk.tk_editor.EditorWidgets.wrong_shown)
    * [docstring\_shown](#edit_cfg_json_tk.tk_editor.EditorWidgets.docstring_shown)
    * [\_add\_docstring](#edit_cfg_json_tk.tk_editor.EditorWidgets._add_docstring)
    * [\_add\_load\_message](#edit_cfg_json_tk.tk_editor.EditorWidgets._add_load_message)
    * [\_add\_verdict](#edit_cfg_json_tk.tk_editor.EditorWidgets._add_verdict)
    * [\_add\_saving](#edit_cfg_json_tk.tk_editor.EditorWidgets._add_saving)
    * [\_add\_buttons](#edit_cfg_json_tk.tk_editor.EditorWidgets._add_buttons)
    * [\_bind\_keys](#edit_cfg_json_tk.tk_editor.EditorWidgets._bind_keys)
    * [\_add\_row](#edit_cfg_json_tk.tk_editor.EditorWidgets._add_row)
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

<a id="edit_cfg_json_tk.tk_editor"></a>

# edit\_cfg\_json\_tk.tk\_editor

Tkinter view of an edit model, with one editable field per member.

Everything this backend takes from the core is reached through `core`, which is
`edit_cfg_json` itself. A backend may use the public API of the core and
nothing else, and naming it at every call site is what makes that visible; it
also keeps the two backends from each holding the same block of twenty
imported names, which is a duplication with nothing to factor out, since
neither backend may import the other.

<a id="edit_cfg_json_tk.tk_editor.NAME_COLUMN_WIDTH"></a>

#### NAME\_COLUMN\_WIDTH

Width in characters of the column that holds the member names.

<a id="edit_cfg_json_tk.tk_editor.LEAST_FIELD_WIDTH"></a>

#### LEAST\_FIELD\_WIDTH

Width in characters that a field asks for, and can be squeezed to.

A field takes every bit of the width that the name and the marks of its member
leave over, so this is not how wide a field is: it is how far a field gives way
when the window is too narrow for all three. The marks are what a narrow window
would otherwise cut off, and a mark that is there and cannot be read is worse
than a field with fewer characters in view. The Textual backend gives way in
the same direction and for the same reason.

<a id="edit_cfg_json_tk.tk_editor.PADDING"></a>

#### PADDING

Padding in pixels around the widgets of the editor.

<a id="edit_cfg_json_tk.tk_editor.DESCRIPTION_INDENT"></a>

#### DESCRIPTION\_INDENT

Indentation in pixels of what is written below one member.

The indentation is what says that the line belongs to the member above it
rather than being a member of its own.

<a id="edit_cfg_json_tk.tk_editor.LEAST_WRAP_WIDTH"></a>

#### LEAST\_WRAP\_WIDTH

Narrowest line in pixels that a paragraph of the editor is wrapped to.

A window can be made narrower than any text is readable in, and wrapping to
what is left of it would leave one word per line. Below this the text is cut
off by the window instead, which is the lesser of the two.

<a id="edit_cfg_json_tk.tk_editor.EMPHASIS_COLOURS"></a>

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

<a id="edit_cfg_json_tk.tk_editor.FIELD_BACKGROUND"></a>

#### FIELD\_BACKGROUND

Background of a field the user can edit.

The window is white, so a field that kept the white background of its own
accord could not be told from a label: the values were there to be edited and
nothing said so. The tint plus the border below are what say it.

<a id="edit_cfg_json_tk.tk_editor.FIELD_FOREGROUND"></a>

#### FIELD\_FOREGROUND

Colour of the text inside a field.

It is stated rather than inherited, because the background above is stated:
a platform that decided the text of a field should be white would otherwise
put white text on a light field.

<a id="edit_cfg_json_tk.tk_editor.FIELD_BORDER"></a>

#### FIELD\_BORDER

Colour of the line around a field the user can edit.

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

<a id="edit_cfg_json_tk.tk_editor._file_types"></a>

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

<a id="edit_cfg_json_tk.tk_editor._key_handler"></a>

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

<a id="edit_cfg_json_tk.tk_editor._bind_key"></a>

#### \_bind\_key

```python
def _bind_key(window: tkinter.Misc, key: str, command: Callable[[],
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

<a id="edit_cfg_json_tk.tk_editor._shown_text"></a>

#### \_shown\_text

```python
def _shown_text(parent: tkinter.Misc,
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

<a id="edit_cfg_json_tk.tk_editor._told"></a>

#### \_told

```python
def _told(label: tkinter.Label, text: str, emphasis: core.Emphasis) -> None
```

Show one text of the editor, in the colour its state asks for.

**Arguments**:

- `label` - Label that shows it.
- `text` - Text to show.
- `emphasis` - Why that text stands out from the values.

<a id="edit_cfg_json_tk.tk_editor._show_emphasis"></a>

#### \_show\_emphasis

```python
def _show_emphasis(label: tkinter.Label,
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

<a id="edit_cfg_json_tk.tk_editor._wrap_to_width"></a>

#### \_wrap\_to\_width

```python
def _wrap_to_width(label: tkinter.Label) -> None
```

Make one label wrap its text to the width it is given.

A Tk label does not wrap at all unless it is told how wide a line may be,
and it does not shrink its text either: a paragraph wider than the window
is simply cut off, which is how a description lost its last words. The
width to wrap at is not known until the window has been laid out, and it
changes whenever the user resizes it, so it is followed rather than set.

**Arguments**:

- `label` - Label that holds text which may be longer than a line.

<a id="edit_cfg_json_tk.tk_editor._label_text"></a>

#### \_label\_text

```python
def _label_text(label: Optional[tkinter.Label]) -> str
```

Return the text one label is showing, empty when it is showing none.

A label that is out of the layout holds no text, because that is how this
backend hides one, so this answers what is on the window and not what a
widget happens to remember.

**Arguments**:

- `label` - Widget to read, or None for a widget that was never created.
  

**Returns**:

  The text that widget shows.

<a id="edit_cfg_json_tk.tk_editor._place_text"></a>

#### \_place\_text

```python
def _place_text(label: Optional[tkinter.Label], text: str) -> None
```

Put one text below a member into the layout, or take it out again.

Hiding is taking the widget out of the layout and emptying it, because a
label with text still takes the height of a line and a window with a
blank line under every member would have hidden nothing.

**Arguments**:

- `label` - Widget that shows one text below a member, or None for a text
  that this member can never have.
- `text` - Text to show, empty when there is nothing to show.

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

<a id="edit_cfg_json_tk.tk_editor.RowWidgets"></a>

## RowWidgets Objects

```python
class RowWidgets(NamedTuple)
```

The widgets that one configuration member owns.

<a id="edit_cfg_json_tk.tk_editor.RowWidgets.field"></a>

#### field

The field of an editable member, and None for every other member.

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

The widgets of the members are kept in the order the model reports its
rows in, which is the order they were created in. This version of the
model neither adds nor removes a row, so the two orders stay the same
one and the pairing is checked rather than assumed.

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
def _add_buttons(parent: tkinter.Misc) -> None
```

Create the buttons, the tick-box and the one that ends the run.

They share one row, because five of them stacked above each other
would push the values of a real configuration off the window.

The explanations get a tick-box rather than a button, because the
action is a toggle: a button saying Explain beside explanations that
are already there would be offering something that has been done.

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
answers that key itself.

The keys are read once, here, which is the whole of what a later
answer from a settings callable cannot change.

**Arguments**:

- `window` - Window that the bindings are made on.

<a id="edit_cfg_json_tk.tk_editor.EditorWidgets._add_row"></a>

#### \_add\_row

```python
def _add_row(parent: tkinter.Misc, row: core.MemberRow) -> RowWidgets
```

Create the widgets of one member, and its description below them.

The member gets a frame of its own, holding the line that is edited
and the texts under it, so that hiding one of those and showing it
again cannot move it away from the member it belongs to.

<a id="edit_cfg_json_tk.tk_editor.EditorWidgets._show_row_texts"></a>

#### \_show\_row\_texts

```python
def _show_row_texts(row: core.MemberRow, widgets: RowWidgets) -> None
```

Show what the model says belongs below one member.

<a id="edit_cfg_json_tk.tk_editor.EditorWidgets._add_description"></a>

#### \_add\_description

```python
def _add_description(parent: tkinter.Misc,
                     row: core.MemberRow) -> Optional[tkinter.Label]
```

Create the widget that says what one member is for, if anything.

A member that nothing is said about gets no widget, because there is
nothing that could ever appear in it.

**Arguments**:

- `parent` - Frame of the member that is being described.
- `row` - Member to describe.
  

**Returns**:

  The widget that shows the description, or None when nothing is
  said about this member.

<a id="edit_cfg_json_tk.tk_editor.EditorWidgets._add_value"></a>

#### \_add\_value

```python
def _add_value(parent: tkinter.Misc,
               row: core.MemberRow) -> Optional[tkinter.StringVar]
```

Create the value widget of one member and wire it to the model.

A member that the model cannot edit yet gets a widget that only
shows text, because there is nothing the user could do to it.

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

What the dialog offers is what the application decided: the
extension it uses for its configuration is the one the dialog adds
to a name that has none, and the one it offers to filter by. An
application with no opinion gets a dialog with none, which is what
this dialog had before there were settings at all.

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

Show what belongs below every member, as the model says it now.

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

Translating a key combination into the notation that Tk binds by.

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

Largest width in pixels that the scrolling part of the editor asks for.

A canvas asks for a width of its own that has nothing to do with what is on
it, so the width the editor opens at has to be said here: what the body asks
for, up to this. Wider than this is left to the user, who can make the window
any size, and every text that is a paragraph wraps to whatever width there is.

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
one grow and shrink as the explanations are shown and hidden.

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

