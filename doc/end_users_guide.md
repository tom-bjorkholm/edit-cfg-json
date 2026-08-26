# End user's guide to the configuration editor

This guide is for the person who changes the configuration of an application
— which values it runs with, where it writes its results, how many outputs it
produces. The application shows you an editor for those values, and this
guide says what is on the screen, what every control does and what every
message means.

Nothing here is about programming. You do not need to know what the
application is written in or what its configuration file looks like inside.

The editor comes in two forms, and an application uses one of them:

- **a window**, which looks like any other program's window, with buttons
  along the bottom and a scroll bar down the side;
- **the terminal**, which fills the terminal you started the application in
  and has a row of key names along the bottom.

## How to read this guide

- **[Part 1](#part-1--the-editor-in-a-window) is the editor in a window.**
- **[Part 2](#part-2--the-editor-in-the-terminal) is the editor in the
  terminal.**
- **[Part 3](#part-3--the-settings-of-the-editor-itself) is the settings of
  the editor itself**, and it is the same for both.

Part 1 and Part 2 each say the whole story for one of the two editors. Read
the one you have and skip the other; you are not missing anything by doing so.

### If you are copying text from here

A secondary reader of this document is the programmer of an application who
wants to put some of this into their own user guide. Each part is written to
be liftable on its own. Two things to check before you publish any of it:

- **the key combinations** ([1.13](#113-the-keys) and
  [2.13](#213-the-keys)). Every one of them is the application's to choose,
  and yours may have changed or removed some.
- **the name of the configuration file**, which the examples here leave
  general.

## Words used in this guide

| Word | What it means here |
| --- | --- |
| **member** | One named value of the configuration, such as `title` or `retries`. |
| **row** | One line of the editor: a name, a value, and whatever is true of that value. |
| **container** | A member that holds several things — a list or a dict. Each thing in it is a row of its own. |
| **object** | A group of members with a name and rules of its own, shown as one row with its members as the rows below it. |
| **path** | How a value inside a container is named, with dots between the steps: `outputs.0.width` is the `width` of the first element of `outputs`. |
| **the file** | The configuration file the editor reads and writes. Your application decides what it is called. |

---

# Part 1 — The editor in a window

## 1.1 What the editor does, and what it never does

The editor reads the application's configuration file when it opens, shows
you every value in it, checks what you type with the application's **own**
rules, and writes the file back when you press Save.

Two promises are worth having in mind from the start.

- **Nothing is written until you press Save.** Typing changes nothing on the
  disk. Neither does validating, folding, searching, adding or removing.
- **Closing writes nothing.** If you close the editor with changes you have
  not saved, those changes are gone. The editor asks you first
  ([1.12](#112-closing-the-editor)), and that question is the only thing
  standing between you and losing them.

There is also no autosave and no draft file. What you see is what a save
would write.

## 1.2 What is on the screen

```
+---------------------------------------------------------------------+
| PipelineConfig *                                                    |
| The settings of the conversion pipeline.                            |
| This file did not hold every value. What it left out was            |
| filled in from the defaults, and is marked.                         |
|                                                                     |
|    title             [My report        ] (edited)                   |
|        Shown at the top of every page.                              |
|        Text.                                                        |
|    retries           [3                ] (filled from default)      |
|        A whole number.                                              |
|  - outputs           2 elements                     [valid inside]  |
|      - 0             PageOutput                 [valid on its own]  |
|          width       [210             ]                             |
|          height      [297             ]                             |
|      + 1             PageOutput                 [valid on its own]  |
+---------------------------------------------------------------------+
| Find: [report          ] [x] path [x] value [ ] Aa [ ] ==      [►]  |
| find report: 1 of 3                                                 |
| validation: not validated                                           |
| save to: /home/me/report.cfg                                        |
| [Validate] [Save] [Save as...] [x] Explain [Fold all] [Close]       |
+---------------------------------------------------------------------+
```

**The top part scrolls and the bottom part does not.** Everything above the
`Find:` line — the name of the configuration, what it says about itself, what
reading the file did, and all the rows — scrolls with the scroll bar and with
the mouse wheel. Everything from the `Find:` line down stays where it is,
because that is what you reach for once you have finished editing.

Reading from the top:

| Part | What it is |
| --- | --- |
| The first line | What this configuration is called. A `*` after it means there are changes that have not been saved. |
| The line or lines below it | What the application says this whole configuration is for. Only there if the application wrote something. |
| The next paragraph | What reading the file did, if it did anything worth telling you. See [1.14](#114-what-the-editor-says-about-the-file-it-opened). |
| The rows | One per member, one per value inside a container, one per object. This is what you came to change. |
| `Find:` | The search. See [1.9](#19-finding-a-member). |
| The line under it | Where the search has got to. It is not there until you search for something. |
| `validation:` | What the application makes of these values. See [1.10](#110-checking-the-values). |
| `save to:` | Where a save would write, or what the last save did. See [1.11](#111-saving). |
| The buttons | Validate, Save, Save as..., Explain, Fold all, Close. |

Where the editor has a window of its own, that window is named after the
configuration being edited.

## 1.3 Reading one row

A row is read from left to right:

```
  - outputs           2 elements      (edited)  [refused inside]  [Add]
  ^ ^                 ^               ^         ^                 ^
  | name              value           marks     badge             controls
  fold control
```

**The name column** is the same width on every row, so the names line up. A
value inside a container is indented one step further in for every container
it is inside, which is what makes the rows read as a tree.

**The value** is either a field you can type into, or text that says what
this row holds:

| What the value column shows | What it means |
| --- | --- |
| A field with text in it | An ordinary value. Type in it. |
| `3 elements`, `1 element` | A list holding that many things. They are the rows below it. |
| `2 entries`, `1 entry` | A dict holding that many things. They are the rows below it. |
| A class name, such as `PageOutput` | An object. Its own members are the rows below it. |
| `no PageOutput` | A place where an object of that class belongs, holding none. |
| `no value` | A member that is allowed to hold nothing, and holds nothing. This is **not** the same as an empty field. See [1.6](#16-a-member-that-may-hold-nothing). |

**The marks** follow the value and say what has happened to it. More than one
can be there at once, and they are shown in the order in which they can
happen:

| Mark | What it means |
| --- | --- |
| `(filled from default)` | The file did not hold this value, so the application's own default was used. Saving writes it out. |
| `(read from the older key title)` | The file is in an older format. This value came from a key called `title` in it. |
| `(moved here from the older ...)`, `(converted from the older ...)`, `(supplied because this file is in an older format)`, `(kept, and the older ... of this file was dropped)` | The other ways an older file reaches a member. |
| `(changed by the load)` | Reading the file changed this value, and there is nothing more to say about why. |
| `(edited)` | You changed it. It clears when a save writes it. |
| `(changed by validator)` | The application rewrote what you typed — correcting the case of a word, for instance, or completing it. This mark stays after a save, because the value is still not literally the one you typed. |
| `(found)` | The search has got to this row. |

**The badge** is on objects and on containers of objects:

| Badge | What it means |
| --- | --- |
| `[valid on its own]` | This object's own rules accept it. It says nothing about whether the whole configuration can be saved: a rule further up may still refuse the two of them together. |
| `[refused on its own]` | This object's own rules refuse it. It cannot be part of a configuration that gets saved. What is wrong is at the member it is about, or below the object. |
| `[valid inside]` | Every object inside this list or dict has been asked and accepted. |
| `[refused inside]` | At least one object inside is refused. Open the container to find out which. |
| nothing at all | Nobody has asked since something inside it last changed. |

The badges appear when you fold a container away or open it again, and when
you validate. Folding is what asks the question.

**The controls at the end of the row** change how many things a member holds.
See [1.7](#17-changing-how-many-values-a-member-holds).

## 1.4 The explanations under a row

Under a row the editor writes what is known about that member: what the
application said it is for, what kind of value it takes, and — for an object
— what its class says about itself.

```
    retries           [3              ]
        How many times a failed page is tried again.
        A whole number.
```

The **Explain** tick-box turns all of that on and off at once. It starts
ticked, because an application that took the trouble to explain its values
wrote those explanations to be read; untick it once you know this
configuration by heart and want more rows on the screen. The one-line summary
of what the whole configuration is for stays either way.

What the type of a member says is one of these:

| Line | Meaning |
| --- | --- |
| `Text.` | Anything you type is a value. |
| `A whole number.` | `3`, not `3.5`. |
| `A number.` | `3` and `3.5` are both values. |
| `True or false.` | See [1.5](#15-changing-a-value). |
| `A list.`, `A dict.` | Said only about a member that holds nothing yet, so that you can see which of the two it would be. |
| `One of: DAILY, WEEKLY, MONTHLY.` | The value is one of a fixed set of names. |
| `It may be left out of the file.` | The member may hold nothing, and the file then holds no key for it at all. |
| `It may hold nothing at all.` | The member may hold nothing, written as an empty value in the file. |
| `No value, so what kind of value it holds is not known.` | The application never said, and there is no value to tell from. Whatever you type is taken as it is. |

A member that cannot be given more elements says why here as well — see
[1.7](#17-changing-how-many-values-a-member-holds).

**A refusal is never hidden by Explain.** If the application refuses a value,
that sentence is below the member whether the explanations are shown or not,
because it is the one thing on the row that has to be read.

## 1.5 Changing a value

Click into the field and type. There is nothing to press to keep what you
typed: every keystroke is kept as you make it. You do not have to leave the
field before you save, and leaving it does not undo anything.

**A half-typed value is fine.** While you are typing `12` the field holds `1`
for a moment, and that is not treated as a mistake. What a value has to be is
only asked when you validate or save.

Three kinds of value are worth knowing about.

**True or false.** Type any beginning of `true` or of `false`, in any case:
`t`, `TR`, `false` all work. The whole word appears in the field the next
time the editor refreshes it. Anything that means neither is refused below
the member, in these words:

```
    verbose           [yes            ]
        yes is not one of: true, false
```

**One of a fixed set of names.** Type the name. The case does not matter and
any beginning that can only be one of them is enough, so `dai` is `DAILY`.
The name is checked **when you leave the field**, not while you are typing —
a name is not a name yet halfway through. What is refused is said below the
member.

**Everything else** is taken as it is. If a member takes a number and you
type letters, nothing happens until you validate, and the refusal then says
so at that member.

## 1.6 A member that may hold nothing

Some members are allowed to hold nothing at all. Those have two states, and
you move between them with the controls at the end of the row rather than by
typing:

- **holding a value** — an ordinary field. The row offers **Del**, which puts
  the member back to holding nothing.
- **holding nothing** — the row says `no value` where the value would be, has
  no field at all, and offers **Add**, which gives it an empty value of its
  kind for you to type into.

This is why `no value` and an empty field are different things and why you
cannot type your way from one to the other. Typing `null` into a field types
the four letters `null`; it does not empty the member.

The same pair of controls does the same job one step up, for a place where an
**object** belongs: a row saying `no PageOutput` offers **Add**, which puts a
new object of that class there with the values its class declares, and a row
holding one offers **Del**, which takes it away again.

A member that the application never described well enough for the editor to
know what an empty value of it would be stays an ordinary field, and shows
whatever the file holds.

## 1.7 Changing how many values a member holds

How many outputs, how many retries in a list, how many named entries in a
dict — that is your decision, not the application's, so the editor lets you
change it. Up to four controls sit at the end of a row:

| Control | What it does |
| --- | --- |
| **Add** | Puts one more element into this list or dict, or gives this member a value where it holds none. |
| **Del** | Takes this element out of the list or dict it is in, or puts this member back to holding nothing. |
| **Up** | Moves this element one place towards the front of its list. |
| **Down** | Moves this element one place towards the back. |

A row shows only the controls that make sense for it, and most rows show
none.

**A new element is copied, never invented.** It is an object of the class the
application declared for that list, or a copy of the kind of thing the
application already put there, or — failing both — the emptiest value of
the kind the member takes. Whatever it is, you then edit it like anything else.

**A new entry of a dict needs a name.** A small dialog called *Add an entry*
asks for it:

```
    Key of the new entry of limits:
    [                              ]
                        [ OK ] [ Cancel ]
```

Answering with a name the dict already holds asks again rather than replacing
what is there. Cancelling, or answering with nothing, adds nothing. A list
never asks, because an element of a list is named by where it is.

**Some members cannot be given anything, and say why.** The sentence is under
the row, with the rest of the explanations, so **Explain** has to be ticked
to see it. It reads like one of these:

- *The keys of this dict are the ones its class declares, and the
  configuration class checks them while it parses, so a dict that gained or
  lost one would be refused.* — the application fixed the names in this dict;
  you can change the values but not which names are there.
- *Nothing says what an element of this member would be ...* — the
  application never said what belongs in this list and never put anything in
  it, so the editor has nothing to copy. Adding one has to be done in a text
  editor.
- *A dict written for a member that holds none is refused by the
  configuration class itself ...* — this member could hold a dict, but not an
  empty one, so there is no first entry for the editor to make.

The editor says these things instead of offering a control that would fail
every time you pressed it.

## 1.8 Folding

A configuration of any size does not fit a window. Any row that holds other
rows — a list, a dict, an object — can be folded away to its own single
line and opened again.

- **`-` on the row** folds that one container. It becomes `+`, and everything
  inside it goes off the screen.
- **Fold all** folds every one of them. Once everything is folded the button
  reads **Unfold all**, and pressing it opens everything. The button always
  says what the next press will do.

A container that would fill the window on its own **opens folded**. That is
not a setting you have changed; it is the editor keeping two hundred rows out
of your way until you ask for them.

Folding does not change any value, and a field keeps what you typed into it
while its container is folded and opened again.

**Folding is also how you ask an object whether it is all right.** Folding a
row, or opening one, asks every object at it or inside it about itself and
puts the answer on the row as a badge ([1.3](#13-reading-one-row)). That is
the cheap, local check; the whole configuration is checked by **Validate**.

A configuration with nothing to fold has no `+`/`-` column and no **Fold all**
button at all.

## 1.9 Finding a member

```
Find: [width            ] [x] path [x] value [ ] Aa [ ] ==      [►]
find width: 2 of 5
```

Type into the field. The editor searches as you type and the line below says
how many rows the text reaches and which of them it is showing. The cursor
stays in the search field while you type, so you can keep changing the text.

**Going to what was found**: press **Enter** in the search field. That puts
the cursor in the field of the row the search has already got to — the one
marked `(found)` — ready to type in.

**Going to the next one**: press the `►` button, or the find-next key
([1.13](#113-the-keys)). Each press moves on to the next row the text
reaches, puts the cursor in it, and wraps round to the top after the last.

**What is found is always reachable.** A match inside a folded container
opens every container that was hiding it.

A row that has no field of its own — a list, a dict, an object — is only
brought into view, because there is nothing there to type into.

The four tick-boxes say where the search looks. Hold the mouse still over one
and the editor explains it.

| Tick | Ticked to start | What it does |
| --- | --- | --- |
| `path` | yes | Look in the name. It is the whole path, so `ports.http` finds that one value and `ports` finds the member and everything in it. |
| `value` | yes | Look in the value, which is the text the field shows. Rows with no value of their own are not looked in. |
| `Aa` | no | Match upper and lower case exactly. Off, `WIDTH` finds `width`. |
| `==` | no | The text has to be the whole name or the whole value, not a part of it. |

Untick both `path` and `value` and nothing is compared with anything. The
line says so — *looking in neither the path nor the value* — rather than
pretending nothing matched.

The line under the field says one of four things:

| Line | Meaning |
| --- | --- |
| `find width: 2 of 5` | Five rows match; you are at the second. |
| `find width: 5 matches` | Five rows match and you are at none of them, which happens after a validation pass moved things about. The next press starts again from the top. |
| `find width: no member matches` | Nothing matches. |
| `find width: looking in neither the path nor the value` | Both places are turned off. |

## 1.10 Checking the values

Press **Validate**. The editor hands your values to the application's own
rules — the same rules the application would apply if it read the file —
and tells you what they made of them.

Nothing is validated behind your back while you type. The `validation:` line
therefore has three states, not two:

| Line | Meaning |
| --- | --- |
| `validation: not validated` | Nothing has been asked since these values last changed. It is not a complaint. |
| `validation: valid` | The application accepts these values. |
| `validation: invalid` | The application refuses them, for a reason that is about no single member. The reason is on the lines below. |
| `validation: invalid, see outputs.0.width, retries` | The application refuses them, and each named member says why below itself. |

**Where a refusal is written**: at the member it is about, under that
member's own description, in a colour of its own. What is about no single
member — a rule relating two members, a key the configuration does not
have — stays in the block just under `validation:`.

**Validating can change your values.** The application's rules are allowed to
correct what you typed: to fix the case of a word, to complete a name, to
sort a list and drop its duplicates. Whatever they changed is marked
`(changed by validator)`, so it is never done quietly. Sorting a list can
even change how many rows there are.

Saving validates too, so you never need to validate before saving. Validate
is for finding out without writing anything.

## 1.11 Saving

**Save** writes the file. It validates first, and refuses to write values the
application would not accept — an invalid configuration is never written.

**Save leaves the editor open.** A save is not the end of the session: the
`*` after the name at the top goes away, every `(edited)` mark clears, and
you carry on.

**Save as...** opens the usual file dialog, titled *Save the configuration
as*, and writes to the file you choose. If the application uses a particular
file name extension, the dialog offers it and, where the application insists
on it, a name with another extension is refused with a message rather than
written.

If there is nowhere to write yet, pressing **Save** opens that dialog for
you. The `save to:` line says `save to: no file chosen yet` until then.

**Writing over a file you did not write in this session** is asked about
first, in a dialog titled *Overwrite the file*:

```
    File /home/me/report.cfg already exists. Overwrite it?
    What it holds now is kept as /home/me/report.cfg.bak.
                                              [ Yes ] [ No ]
```

The dialog starts on **No**, so answering without reading keeps what you
have. The second sentence is there only if your application keeps the
previous content; if it says nothing, nothing is being kept. You are asked
once per destination per session, not once per press — from the second save
onwards the file being written over is your own save from a minute ago.

The `save to:` line then says what happened:

| Line | Meaning |
| --- | --- |
| `save to: /home/me/report.cfg` | Nothing saved yet. That is where Save would write. |
| `save to: no file chosen yet` | There is nowhere to write. Use Save as... |
| `Saved to /home/me/report.cfg.` | Written. A second line names the file the previous content was kept in, where one was kept. |
| `These values are not valid, so they cannot be saved.` | Validate and read what the members say. |
| `File /home/me/report.cfg cannot be written.` | The name, the folder or the permissions. Nothing was written. |
| `What /home/me/report.cfg holds now cannot be kept as ....bak` | The previous content could not be put safely aside, so **nothing was written at all**. That is deliberate: overwriting cannot be undone. |
| `These values cannot be saved: this application would not be able to read back the file that they would write.` | The values are valid on their own, but the file they make is not one this application can open. |

## 1.12 Closing the editor

Three ways out, and all three do the same thing: the **Close** button, the
close button of the window, and the quit key.

If there is anything unsaved, you are asked first, in a dialog titled *Close
the editor*:

```
    These changes have not been saved. Close the editor and discard them?
                                                      [ Yes ] [ No ]
```

The dialog starts on **No**. Answer **Yes** and the changes are gone; answer
**No** and you are back in the editor with everything as it was.

If there is nothing unsaved you are not asked at all, and that includes a
session in which you saved and typed nothing since.

## 1.13 The keys

Every action also has a key combination. **These are the editor's own
defaults, and your application may have changed or removed any of them** —
they exist so that an application whose own `Ctrl+S` is spoken for can give
the editor something else. The buttons always work, whatever the keys are.

| Action | Default keys | Same as |
| --- | --- | --- |
| Validate | `Ctrl+R`, `F5` | the **Validate** button |
| Save | `Ctrl+S` | the **Save** button |
| Save as | `Ctrl+Shift+S`, `F12` | the **Save as...** button |
| Show or hide the explanations | `F1`, `Ctrl+G` | the **Explain** tick-box |
| Fold or unfold everything | `F2`, `Ctrl+T` | the **Fold all** / **Unfold all** button |
| Find | `Ctrl+F` | clicking in the search field |
| Find next | `F3` | the `►` button |
| Close | `Ctrl+Q` | the **Close** button |

The keys work while you are typing in a field, so `Ctrl+S` in the middle of a
field means Save. They reach only the part of the window the editor is in: if
the editor is one panel of a larger window, the rest of that window keeps its
own keys.

The fold key is not offered at all for a configuration with nothing to fold.

## 1.14 What the editor says about the file it opened

Under the name of the configuration, the editor sometimes says what reading
the file did. It is worth reading, because it tells you that the values on
the screen are not the values in the file — and it is the screen that a save
writes.

| Message | What it means |
| --- | --- |
| *This file did not hold every value. What it left out was filled in from the defaults, and is marked.* | The file was incomplete and was opened anyway. The filled-in members carry `(filled from default)`, and saving writes them out properly. |
| *Reading this file changed it, so what is shown is not what the file holds. What the load put there or altered is marked, and saving writes what is shown.* | The file is in an older format, or a value was normalized while it was read. The changed members carry a mark saying so. |
| *This file holds keys that this configuration does not use, and saving leaves them out: ...* | The named keys are not part of this configuration and will not be in the file after you save. |
| *These values were supplied because this file is in an older format: ...* | The application supplied these values because the file is too old to hold them at all. |

If the file **cannot** be opened at all, the editor does not open on it; the
application tells you instead. The messages are of this kind: the file cannot
be read, it is not text, it does not hold configuration that can be read, it
holds a key this configuration does not have, or the values in it are not
valid. The last two have to be corrected in a text editor before the editor
will open the file, because there is no valid configuration for it to show
you.

---

# Part 2 — The editor in the terminal

## 2.1 What the editor does, and what it never does

The editor reads the application's configuration file when it opens, shows
you every value in it, checks what you type with the application's **own**
rules, and writes the file back when you ask it to save.

Two promises are worth having in mind from the start.

- **Nothing is written until you save.** Typing changes nothing on the disk.
  Neither does validating, folding, searching, adding or removing.
- **Closing writes nothing.** If you close the editor with changes you have
  not saved, those changes are gone. The editor asks you first
  ([2.12](#212-closing-the-editor)), and that question is the only thing
  standing between you and losing them.

There is also no autosave and no draft file. What you see is what a save
would write.

## 2.2 What is on the screen

```
+---------------------------------------------------------------------+
|                          PipelineConfig                             |
+---------------------------------------------------------------------+
| PipelineConfig *                                                    |
| The settings of the conversion pipeline.                            |
| This file did not hold every value. What it left out was            |
| filled in from the defaults, and is marked.                         |
|                                                                     |
|    title             [My report        ] (edited)                   |
|        Shown at the top of every page.                              |
|        Text.                                                        |
|    retries           [3                ] (filled from default)      |
|        A whole number.                                              |
|  - outputs           2 elements                     [valid inside]  |
|      - 0             PageOutput                 [valid on its own]  |
|          width       [210             ]                             |
|          height      [297             ]                             |
|      + 1             PageOutput                 [valid on its own]  |
| Find: [report          ] [X] path [X] value [ ] Aa [ ] ==   [next]  |
| find report: 1 of 3                                                 |
| validation: not validated                                           |
| save to: /home/me/report.cfg                                        |
+---------------------------------------------------------------------+
| ^s Save  ^r Validate  f1 Explain  f2 Fold all  ^f Find  ^q Close    |
+---------------------------------------------------------------------+
```

**The middle part scrolls and the rest does not.** Everything from the name
of the configuration down to the last row scrolls with the mouse wheel and
with the arrow keys, `Page Up` and `Page Down`. The `Find:` row, the
`validation:` line and the `save to:` line stay where they are, because that
is what you reach for once you have finished editing.

Reading from the top:

| Part | What it is |
| --- | --- |
| The bar at the very top | The name of the configuration being edited. Where the editor is one part of a larger program, that program keeps its own bar here instead. |
| The first line of the body | What this configuration is called. A `*` after it means there are changes that have not been saved. |
| The line or lines below it | What the application says this whole configuration is for. Only there if the application wrote something. |
| The next paragraph | What reading the file did, if it did anything worth telling you. See [2.14](#214-what-the-editor-says-about-the-file-it-opened). |
| The rows | One per member, one per value inside a container, one per object. This is what you came to change. |
| `Find:` | The search. See [2.9](#29-finding-a-member). |
| The line under it | Where the search has got to. It is not there until you search for something. |
| `validation:` | What the application makes of these values. See [2.10](#210-checking-the-values). |
| `save to:` | Where a save would write, or what the last save did. See [2.11](#211-saving). |
| The bar at the very bottom | The keys, each with the name of what it does. |

**There are no buttons for Save, Validate, Explain, Fold or Close.** In the
terminal those are keys, and the bottom bar is where you read them. A bar too
narrow for all of them shows what fits; the command palette
([2.13](#213-the-keys)) always lists every one.

**Moving about**: `Tab` and `Shift+Tab` move from one field or control to the
next, and the mouse works too — clicking into a field puts the cursor there,
and clicking a control presses it.

## 2.3 Reading one row

A row is read from left to right:

```
  - outputs           2 elements      (edited)  [refused inside]  [Add]
  ^ ^                 ^               ^         ^                 ^
  | name              value           marks     badge             controls
  fold control
```

**The name column** is the same width on every row, so the names line up. A
value inside a container is indented one step further in for every container
it is inside, which is what makes the rows read as a tree.

**The value** is either a field you can type into, or text that says what
this row holds:

| What the value column shows | What it means |
| --- | --- |
| A field with text in it | An ordinary value. Type in it. |
| `3 elements`, `1 element` | A list holding that many things. They are the rows below it. |
| `2 entries`, `1 entry` | A dict holding that many things. They are the rows below it. |
| A class name, such as `PageOutput` | An object. Its own members are the rows below it. |
| `no PageOutput` | A place where an object of that class belongs, holding none. |
| `no value` | A member that is allowed to hold nothing, and holds nothing. This is **not** the same as an empty field. See [2.6](#26-a-member-that-may-hold-nothing). |

**The marks** follow the value and say what has happened to it. More than one
can be there at once, and they are shown in the order in which they can
happen:

| Mark | What it means |
| --- | --- |
| `(filled from default)` | The file did not hold this value, so the application's own default was used. Saving writes it out. |
| `(read from the older key title)` | The file is in an older format. This value came from a key called `title` in it. |
| `(moved here from the older ...)`, `(converted from the older ...)`, `(supplied because this file is in an older format)`, `(kept, and the older ... of this file was dropped)` | The other ways an older file reaches a member. |
| `(changed by the load)` | Reading the file changed this value, and there is nothing more to say about why. |
| `(edited)` | You changed it. It clears when a save writes it. |
| `(changed by validator)` | The application rewrote what you typed — correcting the case of a word, for instance, or completing it. This mark stays after a save, because the value is still not literally the one you typed. |
| `(found)` | The search has got to this row. |

**The badge** is on objects and on containers of objects:

| Badge | What it means |
| --- | --- |
| `[valid on its own]` | This object's own rules accept it. It says nothing about whether the whole configuration can be saved: a rule further up may still refuse the two of them together. |
| `[refused on its own]` | This object's own rules refuse it. It cannot be part of a configuration that gets saved. What is wrong is at the member it is about, or below the object. |
| `[valid inside]` | Every object inside this list or dict has been asked and accepted. |
| `[refused inside]` | At least one object inside is refused. Open the container to find out which. |
| nothing at all | Nobody has asked since something inside it last changed. |

The badges appear when you fold a container away or open it again, and when
you validate. Folding is what asks the question.

**The controls at the end of the row** change how many things a member holds.
See [2.7](#27-changing-how-many-values-a-member-holds).

## 2.4 The explanations under a row

Under a row the editor writes what is known about that member: what the
application said it is for, what kind of value it takes, and — for an object
— what its class says about itself.

```
    retries           [3              ]
        How many times a failed page is tried again.
        A whole number.
```

The **Explain** key turns all of that on and off at once. It starts on,
because an application that took the trouble to explain its values wrote
those explanations to be read; turn it off once you know this configuration
by heart and want more rows on the screen. The one-line summary of what the
whole configuration is for stays either way.

The bottom bar always says what the next press will do: it reads **Explain**
while the explanations are hidden and **Hide explanation** while they are
shown.

What the type of a member says is one of these:

| Line | Meaning |
| --- | --- |
| `Text.` | Anything you type is a value. |
| `A whole number.` | `3`, not `3.5`. |
| `A number.` | `3` and `3.5` are both values. |
| `True or false.` | See [2.5](#25-changing-a-value). |
| `A list.`, `A dict.` | Said only about a member that holds nothing yet, so that you can see which of the two it would be. |
| `One of: DAILY, WEEKLY, MONTHLY.` | The value is one of a fixed set of names. |
| `It may be left out of the file.` | The member may hold nothing, and the file then holds no key for it at all. |
| `It may hold nothing at all.` | The member may hold nothing, written as an empty value in the file. |
| `No value, so what kind of value it holds is not known.` | The application never said, and there is no value to tell from. Whatever you type is taken as it is. |

A member that cannot be given more elements says why here as well — see
[2.7](#27-changing-how-many-values-a-member-holds).

**A refusal is never hidden by Explain.** If the application refuses a value,
that sentence is below the member whether the explanations are shown or not,
because it is the one thing on the row that has to be read.

## 2.5 Changing a value

Move to the field with `Tab` or with the mouse, and type. There is nothing to
press to keep what you typed: every keystroke is kept as you make it. You do
not have to leave the field before you save, and leaving it does not undo
anything.

**A half-typed value is fine.** While you are typing `12` the field holds `1`
for a moment, and that is not treated as a mistake. What a value has to be is
only asked when you validate or save.

Three kinds of value are worth knowing about.

**True or false.** Type any beginning of `true` or of `false`, in any case:
`t`, `TR`, `false` all work. The whole word appears in the field the next
time the editor refreshes it. Anything that means neither is refused below
the member, in these words:

```
    verbose           [yes            ]
        yes is not one of: true, false
```

**One of a fixed set of names.** Type the name. The case does not matter and
any beginning that can only be one of them is enough, so `dai` is `DAILY`.
The name is checked **when you leave the field**, not while you are typing —
a name is not a name yet halfway through. What is refused is said below the
member.

**Everything else** is taken as it is. If a member takes a number and you
type letters, nothing happens until you validate, and the refusal then says
so at that member.

## 2.6 A member that may hold nothing

Some members are allowed to hold nothing at all. Those have two states, and
you move between them with the controls at the end of the row rather than by
typing:

- **holding a value** — an ordinary field. The row offers **Del**, which puts
  the member back to holding nothing.
- **holding nothing** — the row says `no value` where the value would be, has
  no field at all, and offers **Add**, which gives it an empty value of its
  kind for you to type into.

This is why `no value` and an empty field are different things and why you
cannot type your way from one to the other. Typing `null` into a field types
the four letters `null`; it does not empty the member.

The same pair of controls does the same job one step up, for a place where an
**object** belongs: a row saying `no PageOutput` offers **Add**, which puts a
new object of that class there with the values its class declares, and a row
holding one offers **Del**, which takes it away again.

A member that the application never described well enough for the editor to
know what an empty value of it would be stays an ordinary field, and shows
whatever the file holds.

## 2.7 Changing how many values a member holds

How many outputs, how many retries in a list, how many named entries in a
dict — that is your decision, not the application's, so the editor lets you
change it. Up to four controls sit at the end of a row:

| Control | What it does |
| --- | --- |
| **Add** | Puts one more element into this list or dict, or gives this member a value where it holds none. |
| **Del** | Takes this element out of the list or dict it is in, or puts this member back to holding nothing. |
| **Up** | Moves this element one place towards the front of its list. |
| **Down** | Moves this element one place towards the back. |

Reach them with `Tab` or click them. A row shows only the controls that make
sense for it, and most rows show none.

**A new element is copied, never invented.** It is an object of the class the
application declared for that list, or a copy of the kind of thing the
application already put there, or — failing both — the emptiest value of
the kind the member takes. Whatever it is, you then edit it like anything else.

**A new entry of a dict needs a name.** A small screen opens over the editor
and asks for it:

```
       +--------------------------------------------------+
       | Key of the new entry of limits (Enter adds it,   |
       | escape leaves):                                  |
       | [                                              ] |
       +--------------------------------------------------+
```

Type the name and press `Enter`. Press the key the prompt names — `escape`
unless your application changed it — to leave without adding anything.
Answering with a name the dict already holds asks again rather than replacing
what is there. A list never asks, because an element of a list is named by
where it is.

**Some members cannot be given anything, and say why.** The sentence is under
the row, with the rest of the explanations, so **Explain** has to be on to
see it. It reads like one of these:

- *The keys of this dict are the ones its class declares, and the
  configuration class checks them while it parses, so a dict that gained or
  lost one would be refused.* — the application fixed the names in this dict;
  you can change the values but not which names are there.
- *Nothing says what an element of this member would be ...* — the
  application never said what belongs in this list and never put anything in
  it, so the editor has nothing to copy. Adding one has to be done in a text
  editor.
- *A dict written for a member that holds none is refused by the
  configuration class itself ...* — this member could hold a dict, but not an
  empty one, so there is no first entry for the editor to make.

The editor says these things instead of offering a control that would fail
every time you pressed it.

## 2.8 Folding

A configuration of any size does not fit a terminal. Any row that holds other
rows — a list, a dict, an object — can be folded away to its own single
line and opened again.

- **`-` on the row** folds that one container. It becomes `+`, and everything
  inside it goes off the screen.
- **The fold key** folds every one of them. Once everything is folded, the
  bottom bar reads **Unfold all** and the same key opens everything. The name
  always says what the next press will do.

A container that would fill the screen on its own **opens folded**. That is
not a setting you have changed; it is the editor keeping two hundred rows out
of your way until you ask for them.

Folding does not change any value, and a field keeps what you typed into it
while its container is folded and opened again.

**Folding is also how you ask an object whether it is all right.** Folding a
row, or opening one, asks every object at it or inside it about itself and
puts the answer on the row as a badge ([2.3](#23-reading-one-row)). That is
the cheap, local check; the whole configuration is checked by the validate
key.

A configuration with nothing to fold has no `+`/`-` column, and the fold key
is not offered at all.

## 2.9 Finding a member

```
Find: [width            ] [X] path [X] value [ ] Aa [ ] ==      [next]
find width: 2 of 5
```

Press the find key to put the cursor in the field, and type. The editor
searches as you type and the line below says how many rows the text reaches
and which of them it is showing. The cursor stays in the search field while
you type, so you can keep changing the text.

**Going to what was found**: press **Enter** in the search field. That puts
the cursor in the field of the row the search has already got to — the one
marked `(found)` — ready to type in.

**Going to the next one**: press the `next` control, or the find-next key
([2.13](#213-the-keys)). Each press moves on to the next row the text
reaches, puts the cursor in it, and wraps round to the top after the last.

**What is found is always reachable.** A match inside a folded container
opens every container that was hiding it.

A row that has no field of its own — a list, a dict, an object — is only
brought into view, because there is nothing there to type into.

The four tick-boxes say where the search looks. Hold the mouse still over one
and the editor explains it.

| Tick | Ticked to start | What it does |
| --- | --- | --- |
| `path` | yes | Look in the name. It is the whole path, so `ports.http` finds that one value and `ports` finds the member and everything in it. |
| `value` | yes | Look in the value, which is the text the field shows. Rows with no value of their own are not looked in. |
| `Aa` | no | Match upper and lower case exactly. Off, `WIDTH` finds `width`. |
| `==` | no | The text has to be the whole name or the whole value, not a part of it. |

Untick both `path` and `value` and nothing is compared with anything. The
line says so — *looking in neither the path nor the value* — rather than
pretending nothing matched.

The line under the field says one of four things:

| Line | Meaning |
| --- | --- |
| `find width: 2 of 5` | Five rows match; you are at the second. |
| `find width: 5 matches` | Five rows match and you are at none of them, which happens after a validation pass moved things about. The next press starts again from the top. |
| `find width: no member matches` | Nothing matches. |
| `find width: looking in neither the path nor the value` | Both places are turned off. |

## 2.10 Checking the values

Press the validate key. The editor hands your values to the application's own
rules — the same rules the application would apply if it read the file —
and tells you what they made of them.

Nothing is validated behind your back while you type. The `validation:` line
therefore has three states, not two:

| Line | Meaning |
| --- | --- |
| `validation: not validated` | Nothing has been asked since these values last changed. It is not a complaint. |
| `validation: valid` | The application accepts these values. |
| `validation: invalid` | The application refuses them, for a reason that is about no single member. The reason is on the lines below. |
| `validation: invalid, see outputs.0.width, retries` | The application refuses them, and each named member says why below itself. |

**Where a refusal is written**: at the member it is about, under that
member's own description, in a colour of its own. What is about no single
member — a rule relating two members, a key the configuration does not
have — stays in the block just under `validation:`.

**Validating can change your values.** The application's rules are allowed to
correct what you typed: to fix the case of a word, to complete a name, to
sort a list and drop its duplicates. Whatever they changed is marked
`(changed by validator)`, so it is never done quietly. Sorting a list can
even change how many rows there are.

Saving validates too, so you never need to validate before saving. Validate
is for finding out without writing anything.

## 2.11 Saving

The save key writes the file. It validates first, and refuses to write values
the application would not accept — an invalid configuration is never written.

**Saving leaves the editor open.** A save is not the end of the session: the
`*` after the name at the top goes away, every `(edited)` mark clears, and
you carry on.

**The save-as key** opens a small screen with the current destination already
in the field, so changing where you write is a matter of changing a few
characters:

```
       +--------------------------------------------------+
       | Save as (Enter writes the file, escape leaves    |
       | it):                                             |
       | [/home/me/report.cfg                           ] |
       +--------------------------------------------------+
```

Press `Enter` to write, or the key the prompt names to leave it. If the
application insists on a particular file name extension, a name with another
one is refused with a message rather than written.

If there is nowhere to write yet, the save key opens that screen for you. The
`save to:` line says `save to: no file chosen yet` until then.

**Writing over a file you did not write in this session** is asked about
first:

```
       +--------------------------------------------------+
       | File /home/me/report.cfg already exists.         |
       | Overwrite it? What it holds now is kept as       |
       | /home/me/report.cfg.bak.                         |
       |          [ Overwrite ]  [ Do not save ]          |
       +--------------------------------------------------+
```

The cursor starts on **Do not save**, so answering without reading keeps what
you have. The sentence about keeping is there only if your application keeps
the previous content; if it says nothing, nothing is being kept. You are
asked once per destination per session, not once per press — from the second
save onwards the file being written over is your own save from a minute ago.

The `save to:` line then says what happened:

| Line | Meaning |
| --- | --- |
| `save to: /home/me/report.cfg` | Nothing saved yet. That is where a save would write. |
| `save to: no file chosen yet` | There is nowhere to write. Use save as. |
| `Saved to /home/me/report.cfg.` | Written. A second line names the file the previous content was kept in, where one was kept. |
| `These values are not valid, so they cannot be saved.` | Validate and read what the members say. |
| `File /home/me/report.cfg cannot be written.` | The name, the folder or the permissions. Nothing was written. |
| `What /home/me/report.cfg holds now cannot be kept as ....bak` | The previous content could not be put safely aside, so **nothing was written at all**. That is deliberate: overwriting cannot be undone. |
| `These values cannot be saved: this application would not be able to read back the file that they would write.` | The values are valid on their own, but the file they make is not one this application can open. |

## 2.12 Closing the editor

The close key ends the session. Where the editor is the whole program, the
quit that the terminal offers ends up in the same place, so there is only one
way out and it always asks the same question.

If there is anything unsaved, you are asked first:

```
       +--------------------------------------------------+
       | These changes have not been saved. Close the     |
       | editor and discard them?                         |
       |          [ Discard ]  [ Keep editing ]           |
       +--------------------------------------------------+
```

The cursor starts on **Keep editing**. Press the key the editor uses for
cancel — `escape` unless your application changed it — and that is the same
as **Keep editing**.

If there is nothing unsaved you are not asked at all, and that includes a
session in which you saved and typed nothing since.

## 2.13 The keys

The bottom bar names the keys and what they do. **These are the editor's own
defaults, and your application may have changed or removed any of them** —
they exist so that an application whose own `Ctrl+S` is spoken for can give
the editor something else.

| Action | Default keys | What it does |
| --- | --- | --- |
| Validate | `Ctrl+R`, `F5` | Ask the application what it makes of these values |
| Save | `Ctrl+S` | Write these values to the output file |
| Save as | `Ctrl+Shift+S`, `F12` | Choose the file to write, and write it |
| Explain / Hide explanation | `F1`, `Ctrl+G` | Show or hide what the application says about these values |
| Fold all / Unfold all | `F2`, `Ctrl+T` | Fold every list and dict away, or open every one of them |
| Find | `Ctrl+F` | Type into the field that looks for a member |
| Find next | `F3` | Go to the next member that the search reaches |
| Close | `Ctrl+Q` | End the editing session |
| Cancel | `escape` | Leave a question without answering it |

Where an action has two keys, the bar names the first and the second works
without being named.

**The command palette lists every one of them**, including the ones the
bottom bar is too narrow to show, and lets you run any action without
remembering its key. It is the terminal's own palette — `Ctrl+P` unless your
application says otherwise — and the editor's entries in it are named exactly
as the bar names them, so **Explain** and **Fold all** read there as what the
next press will do too.

The keys work while you are typing in a field, so `Ctrl+S` in the middle of a
field means Save. They are active while the cursor is inside the editor: if
the editor is one part of a larger program, the rest of that program keeps
its own keys.

## 2.14 What the editor says about the file it opened

Under the name of the configuration, the editor sometimes says what reading
the file did. It is worth reading, because it tells you that the values on
the screen are not the values in the file — and it is the screen that a save
writes.

| Message | What it means |
| --- | --- |
| *This file did not hold every value. What it left out was filled in from the defaults, and is marked.* | The file was incomplete and was opened anyway. The filled-in members carry `(filled from default)`, and saving writes them out properly. |
| *Reading this file changed it, so what is shown is not what the file holds. What the load put there or altered is marked, and saving writes what is shown.* | The file is in an older format, or a value was normalized while it was read. The changed members carry a mark saying so. |
| *This file holds keys that this configuration does not use, and saving leaves them out: ...* | The named keys are not part of this configuration and will not be in the file after you save. |
| *These values were supplied because this file is in an older format: ...* | The application supplied these values because the file is too old to hold them at all. |

If the file **cannot** be opened at all, the editor does not open on it; the
application tells you instead. The messages are of this kind: the file cannot
be read, it is not text, it does not hold configuration that can be read, it
holds a key this configuration does not have, or the values in it are not
valid. The last two have to be corrected in a text editor before the editor
will open the file, because there is no valid configuration for it to show
you.

---

# Part 3 — The settings of the editor itself

Some things about the editor are decisions, not facts: which keys it takes,
what a configuration file of your application is called, and what becomes of
the file that a save writes over. The application makes those decisions, and
some applications hand them on to you.

**Whether you can change any of this is your application's decision.** Ask
its own documentation. Where it does let you, the settings arrive in one of
two ways:

- **as part of the application's own configuration** — a member of it holds
  these settings, and you edit them in this same editor, with the same rows,
  the same explanations and the same Save;
- **as a settings file of your own**, which is a small file holding only what
  you want to change.

Either way, the answers are the same and they are named the same.

## 3.1 What can be decided

| Setting | What it decides | If it is not set |
| --- | --- | --- |
| `actions` | Which key combinations run which action of the editor. | The defaults in [1.13](#113-the-keys) and [2.13](#213-the-keys). |
| `file_extension` | What a configuration file of this application is called. `cfg` and `.cfg` mean the same thing. | The editor has no opinion and takes file names exactly as they are given. |
| `extension_enforced` | Whether a file with another extension is refused rather than merely uncompleted. | `false`: the extension is added to a name that has none, and a name with another one is taken as it is. |
| `backup_suffix` | What the previous content of an overwritten file is kept as: `.bak` makes `report.cfg` into `report.cfg.bak`. | `.bak`. Setting it to `null` keeps no previous content at all. |
| `backup_count` | How many of those are kept. Above one they are numbered from `_1`, which is the one overwritten last, and each save pushes the rest one number further back until the oldest falls off the end. | `1`, which is one kept file with no number. |
| `confirm_overwrite` | Whether the editor asks before writing over a file this session did not write. | `true`, which is the answer that loses nothing. |
| `priority_keys` | Whether the editor is offered a key before the field the cursor is in. | `true`, so pressing Save while typing means Save. |

## 3.2 What a settings file looks like

It is a small file, and it need name only what you want to change. Anything
it leaves out keeps the answer the editor would have chosen anyway.

```json
{"actions": {"save": ["ctrl+w"], "find": ["ctrl+f", "f7"]},
 "file_extension": ".cfg",
 "extension_enforced": true,
 "backup_suffix": ".old",
 "backup_count": 3}
```

The names of the actions are these, and no others:

`quit`, `validate`, `save`, `save_as`, `cancel`, `explain`, `fold`, `find`,
`find_next`.

Each holds a **list** of key combinations, and every one of them runs that
action. The first is the one that gets named in the terminal editor's bottom
bar; the rest work without being named. An empty list takes the keys away
from that action without taking the action away: the window editor still has
its button and the terminal editor still has its command palette entry.

**How a key combination is written**: the modifiers `ctrl`, `shift`, `alt`
and `meta` joined with `+`, all in lower case, and then one character, one of
`f1` to `f12`, or a name — `escape`, `enter`, `tab`, `space`, `backspace`,
`delete`, `insert`, `home`, `end`, `pageup`, `pagedown`, `up`, `down`,
`left`, `right`. So `ctrl+w`, `ctrl+shift+s`, `f7`, `escape`.

Two things are worth knowing before you write one:

- **Giving one combination to two actions is refused**, because only one of
  them could ever run and which one it would be is not something you could
  rely on.
- **A combination the editor cannot make sense of costs that action its key
  and nothing else.** The button, the bottom bar entry and the command
  palette entry are all still there.

## 3.3 Where such a file is looked for

Where your application uses this editor's own settings lookup, the first of
these that answers is used:

1. a file named on the command line with `-c` or `--cfg`;
2. the file named by the `CFG_EDIT_CFG_JSON` environment variable;
3. a file of that program's own in your home folder;
4. `$HOME/.edit-cfg-json.cfg`;
5. nothing at all, which is the editor's own defaults.

**A file you name must be there.** The first two are you saying which file to
use, so a name that no file answers to is refused rather than quietly
ignored — running with settings other than the ones you asked for is the one
thing a lookup must not do. The two files in the home folder are the lookup
itself, so a step that finds nothing is simply the next step.

Naming a file that says nothing — one holding `{}` — is how you ask for the
editor's plain defaults past a file in your home folder that says something
else.

## 3.4 A settings file from an older version

The editor gains an action from time to time, and a settings file written
before it existed does not mention it. Such a file is still read: the editor
falls back on the compatibility rules for a file of an earlier version, uses
it, and says so, naming the file and adding that a future version may stop
accepting it.

The fix it asks for is to open that file in the editor and save it again,
which writes every setting the current version has. Nothing you had set is
lost by doing so.
