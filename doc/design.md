# Design of edit-cfg-json

This document records the design decisions for the folding configuration
editor built on top of
[`config-as-json`](https://pypi.org/project/config-as-json). It is a
design document, not an API reference. Where it states a fact about
`config_as_json`, the source is the documentation and examples in
`dep_lib_doc/config_as_json/`.

## 1. Purpose and scope

An application whose configuration is a `config_as_json.Config` object
should be able to hand that object to this library and get a usable
folding editor, without writing any UI code and without describing its
configuration schema a second time.

The library provides:

- a UI-agnostic core that discovers the editable structure by
  introspection and owns all editing, validation and file handling
- a Textual (terminal) editor
- a Tkinter (desktop) editor

The application supplies its `Config` object, optionally a loader
callable, optionally an input file name, an output file name, and a
mapping of per-attribute descriptions.

The editor shall have no opinion about what the filename extension shall
be for input or output files. Some applications use `.cfg`, some use `.json`,
and also other file name extensions are in use.

## 2. Repository and package structure

Three folder trees in this repository, each building its own package.

| Distribution | Import name | Depends on |
| --- | --- | --- |
| `edit-cfg-json` | `edit_cfg_json` | `config-as-json` |
| `edit-cfg-json-tk` | `edit_cfg_json_tk` | `edit-cfg-json` |
| `edit-cfg-json-textual` | `edit_cfg_json_textual` | `edit-cfg-json`, `textual` |

### 2.1 Why three distributions

The deciding reason is that the core is intended as a base for
third-party UI implementations. A third party needs a package to depend
on, a version to pin, and a published API contract. Reinforcing reasons:

- A Qt or web backend is a likely later extension, and a third-party
  backend named `edit-cfg-json-qt` is then symmetric with the two
  in-house ones.
- The Tk editor must be absent, not merely unimported, in environments
  without Tk support, and it is likely to gain pip-installable
  dependencies of its own over time.

### 2.2 Naming

Flat sibling distribution names, not a PEP 420 namespace package. A
namespace package would allow `edit_cfg_json.qt`, but flat names give the
same symmetry for third parties without the namespace-package pitfalls
(no top-level `__init__.py`, so no re-exports; a stray `__init__.py`
silently breaks resolution; mypy and pylint handling is fragile, which
matters under this repository's strict checker configuration).

### 2.3 Versioning and build configuration

- `BuildSpec.identical_versions` stays at its default `True`, so the
  three packages release in lockstep and the in-house compatibility
  matrix is trivially one-to-one. Each `pyproject.toml` carries the same
  version and the build verifies it.
- The UI packages pin the core with a compatible-release constraint
  (`~=`), not `==`, so a core patch release does not strand them.
- After Alpha (section 2.5) the core follows semantic versioning. This
  is a promise third-party backend authors need more than the in-house
  backends do.
- `BuildSpec.package_folders` stays unset; the three `pyproject.toml`
  files are auto-discovered.
- Once the packages declare `config-as-json` and `textual` as real
  dependencies, the corresponding entries in `additional_venv_packages`
  in `custom_build_tools/custom_spec.py` should become redundant. Verify
  against the install step rather than assuming.
- Tk tests are split into three categories with different display
  requirements. See section 10.

### 2.4 The public API contract

- Everything a UI backend needs is re-exported from
  `edit_cfg_json/__init__.py`. Everything else is internal and may
  change without a major version bump.
- The two in-house backends import only from the top-level
  `edit_cfg_json`, never from its internal modules. If we allow
  ourselves the shortcut, the public API will be under-designed and the
  first real third-party backend will discover it. Enforced by a test
  that walks the backends' imports.
- The core must never import `tkinter` or `textual`. Enforced by a test
  that imports the core with both blocked in `sys.modules`. Separate
  wheels do not catch a wrong-direction import on their own, because all
  three packages are installed into the same venv at test time.

### 2.5 Alpha status

The first iterations are released as Alpha. **While Alpha, no API
stability or backward compatibility is offered**, for the core or for
either backend. The public/internal split of section 2.4 still applies —
it is how we keep the eventual contract small and deliberate — but
crossing a major version is not required to change a public name during
Alpha.

The Alpha period is what makes it safe to publish three packages before
the model has been proven by two real backends. Section 2.3's semantic
versioning promise starts when Alpha ends, and the README and PyPI
classifiers must say so plainly while it lasts.

### 2.6 Shared type aliases

Aliases use the `type` keyword. Two rules keep them from multiplying:

1. **Never alias what `config_as_json` already exports.** `JsonType`,
   `PathOrStr`, `ConfigPath`, `ValidationPlan` and `NestedConfigs` are
   public there and are used under those names here.
2. **Each alias is declared exactly once**, in one module of the core,
   re-exported from `edit_cfg_json`, and imported from there by both
   backends. An alias for the same type declared again in another file
   is a defect, not a style preference.

The aliases the design needs so far:

```python
type Descriptions = Mapping[ConfigPath, str]
```

Buffer leaf values are `config_as_json.JsonType` under rule 1.

## 3. Design principles

1. **Validate by running validators, never by introspecting them.**
   Any application may define its own `MemberValidator` subclass with
   arbitrary rules. Reading constraints out of a known set of validator
   classes would work for those classes and silently fail for the rest.
   Running the real validation plan is correct for every validator that
   exists or will ever exist.
2. **The default instance is the schema.** A `Config` constructed with
   no JSON source holds its declared defaults. That is the same source
   the library itself uses when it checks parsed dictionaries.
3. **Ownership segments the tree.** The fold boundary, the validation
   boundary and the serialization boundary are the same line: the edge
   of a nested `Config` object.
4. **Incompleteness is safe.** Anything the introspection cannot infer
   degrades to a free-text field plus validate-on-demand. The editor
   stays correct and becomes only less pleasant. This is what makes
   principle 1 affordable.
5. **The editor never mutates the caller's `Config` object.**

## 4. The model

### 4.1 Node tree

The model is a tree of nodes segmented by config ownership. A nested
`Config` object is a first-class node with its own type, docstring and
validity state; ordinary JSON structure (dicts, lists, scalars) lives
inside the ownership region of the config object that owns it.

This mirrors what `config_as_json` already does internally with
`child_owned_paths` and the `serialize_converters()` ownership rule
("converters apply only to data owned by this object; declared nested
`Config` objects serialize themselves"). Reusing the library's own
segmentation is what makes section 6.2 work.

Sources of structural information, in order of authority:

| Source | Provides |
| --- | --- |
| `nested_configs()` | Which members are nested configs, their `ConfigNestingKind`, their `config_type`, any `factory_function` |
| Default instance | Every attribute name, its default value, and therefore its type |
| `parse_converters()` | Which keys become rich Python types, and the expected parsed type |
| `serialize_converters()` | Which values need explicit conversion on write |
| `_unchecked_dicts` | Which dict members have relaxed key policy |
| `_omit_none_from_json()` | Which members are genuinely optional |

**Ordinary JSON structure is a tree of rows**, built at step 10. A member that
holds a list or a dict is one row, and every value inside it is a row of its
own, indented once for each container it is inside, with a field at every
value. The container row has no field, because it has no value of its own:
its value is what its rows hold, and it says how many of them there are
instead. Every value it holds is kept as its rows hold it, so a change inside
a container is a change of the member whether the container is folded or not.

**A value inside a container is addressed by the path to it**, which is what
section 4.2 already asks of every leaf. A list element is addressed by its
index written out, so `('retry_delays', '0')` is a path and
`('retry_delays', '[')` is the selector that describes every element of that
list. `config_as_json` has no notation for one specific element — `'['` is its
step for all of them — so this is the editor's own, and it is the reason a
dictionary key that begins with `'['` is reserved there and never a path step
here.

**What a container holds is shown in the order the file has it**, which is the
order a list holds its elements and the sorted order of a dictionary's keys.
Section 4.1's declaration order is about the members, because a member has a
declaration to be read from; a dictionary key has none, and the order that a
save writes is the order that is shown.

**A nested configuration object is a node of its own**, built at step 11. It
serializes as a dict and it is not one: it has a class and a docstring of its
own, its members are the rows below it in the order that class declares them,
and showing it as the dict it writes would be showing it as something it is
not. Its row says the class rather than how many entries the dict has, for the
same reason.

**Where those objects are is asked as a path and not as a member name**, and
that is the decision this section exists to record, because a configuration
worth editing is not a handful of scalars. A member that holds one nested
object is the least interesting shape there is. The ordinary shape is a
*list* of nested objects, each of which holds a dict of more of them, and
`ConfigNestingKind` says exactly that: `LIST_ELEMENT` and `DICT_VALUE` declare
that every value *inside* a member is an object, and `DICT_VALUE_BY_KEY`
declares one named key of it.

The member that holds them is then an ordinary container of the tree — it
folds, it says how much it holds, and its rows are its elements — and each
object inside it is one node with rows of its own. So the paths, the fold
state, the rebuild of section 4.8 and the addressing of every description are
already the shape a list of nested objects needs, and steps 13 and 14 change
**what a nested node offers** and never **how the tree is built**.

**The declarations are walked over the object and not matched as selectors.**
Step 10 found those nodes by turning each declaration into a selector —
`('outputs', '[')` for a list of them — which was right while a nested object
was one row. It stops being enough once the object owns the region below it,
because *ownership is asked of an object*: `parse_converters()`,
`_omit_none_from_json()` and the declaration order of the members are all
methods and attributes of an instance, and a declaration says only which class
was expected. So step 11 asks the configuration object itself, which answers
with the absolute path of every nested object there really is, and with the
object at it. That also tells the truth where a `factory_function` answered
with a subclass, and it distinguishes an `OPTIONAL_MEMBER` that holds an object
from one that holds none. The `'['` selector keeps its meaning where it is
still the right question, which is the description mapping of section 4.3.

**Ownership is the rule for everything inside such a node.** A converter
belongs to the class that owns the subtree, exactly as `serialize_converters()`
does on the way out; which members may be left out of a file is that class's to
say; and the members are ordered as that class declares them and not as the
sorted dictionary it writes. What does *not* stop at the boundary is the
description mapping, for the reason section 4.3 gives.

**A declared member that holds no object is a row that says so**, where the
class writes `null` for it rather than leaving it out. It says which class is
missing, and it cannot be edited, because no text typed into a field becomes a
configuration object; making one is adding, and belongs with adding an element
of a list. A class that lists such a member in `_omit_none_from_json()` writes
nothing for it and it then has no row at all, which is what any omitted member
already does.

**What a validator inside a nested object refuses is attributed by asking that
object on its own**, built at step 12. Such an object validates itself while
the whole configuration is parsed, so the object that could say which member
was refused is one the editor never holds — the same problem section 6.3
solved at the top level, and the same answer does not reach inside, because
the nested objects are constructed by `parse_json` and not by the editor.
Applying the subtree of the buffer to the object that owns it is what does
reach it, and that is section 6.2. A value whose *text* means nothing is a
different question and was already answered at the member, inside a nested
object as anywhere else, because it is asked of the member alone.

A trivial configuration has scalar values, or maybe individual nested
`Config`s. A realistic configuration has a number of lists and dicts
of nested `Config`s. We should keep this in mind during design.
A configuration with a list of nested `Config`s, each having a dict of
nested `Config`s is the normal case, not a special case.

**Runtime type information caveat.** `self.story_points: int = 5` inside
`__init__` is a PEP 526 annotation on an instance attribute, and Python
records it nowhere at runtime. `typing.get_type_hints()` therefore
returns nothing useful for the ordinary `Config` pattern, and the type of
the *default value* is the only type source. Config classes built on the
dataclass pattern (see `e04_third_party_class.py`) do expose real types
through `dataclasses.fields()`. Support both; do not assume annotations
exist.

### 4.2 Edit buffer

The buffer holds JSON-compatible values at the leaves, typed as
`config_as_json.JsonType`. The user edits what will actually land in the
file — an enum is edited as its member name.

The buffer is however not JSON text. For example: in the edit field no
quotation marks are shown around a string. The edit field will show
the digits `1` and `0` as`10` for both the string `'10'` and the
integer `10`. The edit buffer needs to hold additional metadata/flags
with type information for each leaf.

**Whether that type information is shown to the user** was left open here and
is answered at step 9: it is, as a line of explanatory text below the member,
in the same place and under the same toggle as everything else explanatory.
Section 4.3 is where it says what. It is not shown as a label beside the field,
because it is text about the value and not part of it, and because a narrow
window would then squeeze the field for it. There is still no decision to allow
the user of the editor to try to change this type metadata (which in many cases
would trigger an error at validation, but might be useful for separating between
a None value and an empty string value of an `Optional[str]`.)

The type metadata of a leaf is **derived from the value that leaf held
when the file was last agreed with**, which is when the model was built and
again after every save, kept beside the value the user is editing.
Deriving the kind from the current value instead does not work: a number
member that is half typed holds text for as long as its text is not a
number yet, and it would stop being a number member for the rest of the
session. The value the model started with also answers the other question
the editor asks about a leaf, which is whether the user changed it. That
comparison is now made on the JSON notation rather than with `==`, because
Python considers `True` equal to `1` and `1` equal to `1.0` while a file
writes all three of them differently, and any of those changes changes
the file. Future versions will probably add more type information on
more focus on attribute types.

The one thing that comparison ignores is **the order of the keys of a
dictionary**, for the reason section 5.3 gives about the other comparison in
this library: `config_as_json` writes them sorted, so a file cannot hold two
orders and two values that differ only in one are the same value. The editor
really does hold another order — the members of a nested configuration object
are kept in the order its class declares them, which is section 4.1 — so
without this every nested object would report itself as changed by a validator
the first time anything in it was validated. Found and fixed at step 12, where
the example that shows a nested object being edited showed it.

A successful save moves that value to what was written, which is what makes
the second question keep answering itself: what has just reached the file is
not waiting to reach it, so the editor stops reporting unsaved changes and
the *edited* mark of every leaf clears. Moving it is safe for the first
question as well, because only a validated configuration is ever written, so
the value moved to has the type the configuration class gave it. The *changed
by validator* mark is deliberately not cleared by a save: that a value is not
literally the one the user typed stays true after it has been written.

Text that is not JSON at all is kept as a string rather than refused, which
is what makes a value typable at all: it is invalid for most of the time it
takes to type it. The string that a number member then holds is not hidden,
it is simply the wrong type, and section 6.1 reports it as one.

A field writes into the buffer on **every change and not when it loses the
focus**, because a commit on focus loss would lose the last edit whenever
saving is reached without leaving the field — from the keyboard, or through
a button that does not take the focus.

Losing the focus is however the moment at which the **conversion of one
field** reports itself, because that is when the user has moved on from that
field. It arises with the leaves that `parse_converters()` turns into rich
Python types, an enum being the obvious one: its member name is not a member
of the enum for most of the time it takes to type it, so converting on every
change would report a failure that is not one yet. **Built at step 7**, as
`EditModel.check_field`, which each backend calls from the event its own
toolkit has for a field losing the focus — `<FocusOut>` in Tk and
`Input.Blurred` in Textual.

Per-field conversion feedback on focus loss is **not** the validation of
section 6. It is local, it needs no candidate configuration, and it answers
a different question — whether this text means a value at all, rather than
whether the configuration is one the application would accept. Both are
needed, and both reach the user through the same line below the member; which
of the two is shown when both have something to say is settled in section 6.5.

The answer of the conversion is **kept per member and cleared by the next edit
of that member**, which is what makes it a different thing from what a
validation pass says. Whether this text means a value of this member is
answered by the member alone, so it stays true however the rest of the buffer
changes, while what a validator refused is only known for as long as the rest
of the buffer stands still, because a member validator receives the whole
configuration and may look at any of it.

**The converter is run rather than read.** Whether a name is a member of an
enum is decided by calling the `ParseConverter` the class declared, which is
what `config_as_json` calls while it parses, so an application that declared a
converter of its own is answered by its own converter. That is principle 1 of
section 3 applied to conversion, and it is also why nothing here knows what an
enum is.

Rewriting the text a field shows is a third, separate matter, and belongs
where validation rewrites values (section 6.4).

**A conversion that fails is reported for the member and not as JSON.**
`config_as_json` reports a failed conversion inside the message it prints for
JSON it could not load, because the conversion runs inside `json.loads()`.
That message is right for a program reading a file and wrong for a person
editing a field, who did not ask about JSON and is not looking at a file. So
the conversion of every member is run *before* the candidate configuration of
section 6.1 is built, and a member whose text means nothing is reported as
that one member, with what its own converter said and nothing else. The
candidate is not built at all in that case: it could only report the same
thing as text it could not read. The load path of section 5.2 is deliberately
left as it was, because a refusal the user cannot act on inside the editor is
not a field being edited.

Each leaf is addressed by a `config_as_json.ConfigPath`, so that a member
inside a list, a dict or a nested config needs no second way of naming it.

Editing a live `Config` object attribute by attribute was considered and
rejected: a value being typed passes through intermediate states that are
not valid, rich Python values exist only after `parse_converters()` runs,
and a half-edited object cannot be validated meaningfully. JSON-space
leaves also make the validation round-trip in section 6.1 exact.

Notice that the mental model presented to the user should as much as
possible center around the `Config` objects, and JSON encoding is
only a way to show and edit individual leaf values.

Per-field flags carried by the model, not by the backends, so that the
two UIs cannot drift:

- **changed by validator** — set when a validation pass rewrote the
  value, cleared when the user next edits that field
- **filled from default** — set when a permissive load supplied a value
  the input file did not contain
- **changed by the load** — what reading the input file did to this value,
  which is what an older format and a normalization during parsing both do
  (section 5.3). It is text rather than a flag, because the load records which
  rule put the value there and at which older key it found it, and a member
  that says it was read from `title` says more than one that says only that
  something happened to it. A member that only the comparison found says that
  much and no more, which is all that can be known about it. It is never set
  together with the mark above it: that one says the same thing more precisely,
  and one member carrying two marks about one fact would be worse than either
  alone.

### 4.3 Descriptions and docstrings

Two complementary, independently optional sources of explanatory text:

- **Class docstrings** label config-object nodes. Read with
  `cls.__doc__`, cleaned with `inspect.cleandoc()`, split at the first
  blank line into a summary for the folded row and full text for the
  expanded view. A show/hide toggle belongs in the model.

  The summary is collapsed to a single line, because where a docstring is
  broken is a fact about the width of a source file and not about the text,
  and a label of one row has one line.

  **Which of the two a nested node shows is decided by its fold**, settled at
  step 11: the whole docstring while the node is open, the summary while it is
  folded, and both of them under the explain toggle of section 4.4 like every
  other explanation. An object that is showing less of itself says less about
  itself, which is the same thing folding already does to the values. The root
  configuration is the one that is never folded, so its summary stays on its
  label line and its docstring is what the toggle covers.

  A consequence worth stating, because it is what a backend has to do about it:
  what is said below a nested node **changes when it is folded**, so a backend
  writes that text again on every fold and not only when the toggle is pressed.
  It is put together by `row_description` rather than carried by the row, since
  what a row says about itself cannot depend on a fold state that is stamped
  onto it afterwards; `row_describes` is what a backend asks before it creates
  the widget at all, because the description a row carries is no longer the
  whole of what appears below it.

  Use `cls.__doc__`, **not** `inspect.getdoc(cls)`. `getdoc()` inherits
  from base classes, so a nested config class without its own docstring
  would silently display `Config`'s docstring — actively misleading in
  an editor. Check `cls.__doc__ is not None` and show nothing otherwise.

- **The description mapping** labels individual attributes, because
  per-attribute docstrings do not exist at runtime: a string literal
  after an assignment is discarded, and PEP 526 annotations are not
  recorded.

- **The type of a member** says the rest, and it always says something. Where
  the member holds an enum, `parse_converters()` is what says so, because it is
  what turns the name in the file back into a member of it, and the enum class
  then says the rest itself: the summary of its own docstring and the names it
  accepts. Settled at step 7.

  Where it holds anything else, what is said is **what kind of value it is** —
  text, a whole number, a number, or true or false — read from the value the
  member held when the file was last agreed with, which section 4.2 already
  keeps as the only type information there is. A member that may be left out of
  the file says that as well, from the `_omit_none_from_json()` of the class
  that owns it, which section 4.1 lists as a source and nothing else uses.
  Added at step 9, after a review found a program that had been told a class
  and no description mapping showing its members with nothing under them at
  all, when the editor did know something about each of them.

  It is the least that can be said and it is worth saying, because it answers
  the one question a value cannot answer about itself: whether `10` in a field
  is the number or the text. A node that is not a value says nothing here,
  because its row already says what it is — which kind of container, or which
  class — where its value would be. What it may still say is that the class
  above it can leave it out of the file, which is true of a nested object as of
  any other member.

  What a validator would have added — a range, a set of allowed values — stays
  out, permanently, for the reason section 11 gives. That is the difference
  between the names of an enum and the bounds of a number: the first is the type
  of the member and the second is a rule about it.

  This is **not** the reading of a validator that section 11 permanently rules
  out. The names an enum has are its type, as true as the name of the member
  itself, and reading them is the same kind of reading as the docstring of the
  configuration class above. A range, by contrast, lives inside a validator
  and is therefore explained by the application in words or not at all.

  It is **appended** to what the application said rather than used where the
  application said nothing: the names are true whatever the application wrote,
  and an application that explains what its members mean should not have to
  list the names as well. Writing them in two places is how one of the two
  comes to be wrong.

  The **summary** of the enum docstring and not the whole of it, which is the
  one place where a class is treated differently from the class of the
  configuration. The reason is what the rest of an enum docstring usually is:
  notes for whoever writes the application, about how the members are numbered
  or how they reach the file, which is not what somebody choosing between them
  needs.

The description mapping is `Descriptions` (section 2.6), that is
`Mapping[ConfigPath, str]`. `ConfigPath` is a tuple of `str` and is
hashable, so a mapping is the natural type rather than a list of pairs.
Absolute paths only; no recursive plain-string key selector. The literal
`'['` step keeps its `config_as_json` meaning of
"every list element or every dictionary value at this point", which is
what keeps repeated `LIST_ELEMENT` and `DICT_VALUE` nested configs from
forcing the application to repeat itself per index or per key.

One deliberate divergence from `serialize_converters()`: description
paths **cross nesting boundaries**. Converters stop at child-owned
subtrees because each nested config serializes itself; descriptions have
no such constraint, and the application should not have to know where the
nesting boundaries fall. A second divergence: overlapping selectors
resolve in favour of the more specific one rather than raising. A wrong
description is a cosmetic bug; refusing to open the editor over one is
not.

**Which of two selectors is the more specific one** is settled at step 6, and
it has to be, because two selectors of the same length can both address one
member and be equally short. A step that names a key is more specific than the
`'['` step, and an earlier step decides before a later one, so
`('a', 'b', '[')` wins over `('a', '[', 'c')` for the member `('a', 'b', 'c')`:
the selector that agrees with the member sooner is the one that is about it
more nearly. Two *different* selectors can never tie, because two selectors
with the same pattern of named steps that both address one member are the same
selector. Nothing is validated: a selector that addresses no member of this
configuration is simply never used, which is the same decision as the
paragraph above and for the same reason.

### 4.4 Showing and hiding the explanations

Explanatory text costs a line per member, and a user who knows this
configuration by heart wants it back. So there is one toggle for all of it,
its state belongs to the model, and both backends read it there — the same
rule that already holds for the marks, the title and the messages, and for the
same reason: two user interfaces that disagreed about whether they were
explaining themselves would be worse than either behaviour.

What the toggle covers, settled at step 6:

- **shown** — the whole class docstring, and the description of every
  described member below that member
- **hidden** — the summary of the class docstring, and nothing else

The summary survives hiding because it is one line for the whole
configuration, so hiding it would save nothing worth the loss. The editor
**starts with the explanations shown**: an application that took the trouble
to write a description mapping wrote it to be read, and a user who does not
want it presses one key.

A member the application said nothing about is shown without a description
rather than with an empty one, and a class with no docstring of its own is
shown without a label rather than with `Config`'s. Both are principle 4 of
section 3 rather than incompleteness to be fixed later, and both mean the
backends create no widget at all for what can never have anything in it.

**The toggle is one action, and each backend says so in its own way.** A
button that said "Explain" while the explanations were already there would be
offering something that has been done, which is the one thing the wording must
not do. Tk has a button row, so it gets a tick-box: one text, true in both
states, and the tick says which state it is in. Textual has a footer of key
bindings and no button row, so its action is *renamed* instead — "Explain"
while they are hidden, "Hide explanation" while they are shown — and the same
name reaches its command palette. Settled at step 6 after review: the two
answers differ because the two toolkits offer an action differently, and the
question each of them answers is the same one.

### 4.5 Telling the kinds of text apart

Once the explanations are on the screen, most of what is there is not the
values. A value is what the user came to change, a description is text about
that value, and a refused validation is something to act on, and a user who has
to read all three to tell them apart is reading too much. They are therefore
told apart by colour.

**What kind each piece of text is belongs to the core, and what colour a kind
is belongs to each backend.** `Emphasis` is that vocabulary: `MUTED` for text
about the values and for a state that has not been reached, `ATTENTION` for
something that has happened to a member, `WARNING` for a remark about the input
file, and `GOOD` and `BAD` for what the application accepted and refused. There
is deliberately no member for ordinary text: the values and their names are left
alone, which is what makes them the most legible thing on the screen.

What is wrong with one member is `BAD` and not `MUTED`, and that pair is the
one that earns the vocabulary: a description and a refusal sit one below the
other under the same member, and the one that has to be acted on has to be
told from the one that only explains. Section 6.5.

The decisions that depend on the state of the model — what the validation, the
saving and what one nested object is on its own are shown as — are functions
of the core rather than of a backend, because they are the ones a backend
could otherwise answer differently. Whether a save succeeded is also not
readable from its message, which is why `EditModel.save_outcome` exists beside
`save_message`. All three have the same three states, and `MUTED` for the one
that has not been reached is what makes them read as the same kind of answer
about three different things.

Colour itself cannot be in the core: Textual names colours of its terminal's
theme and follows it into a dark mode, Tk has no theme to ask and needs colour
values, and neither can be expressed in the other. Each backend therefore has
one table from `Emphasis` to what its own toolkit understands, and that table is
the only place a colour is written down.

**What a light or a dark background does to that** is answered for Textual and
open for Tk. Textual's theme colours are right in both, because the terminal
decides which theme is in use. Tk gets colour values chosen for the light window
it is given, and a Tk that a platform has put into a dark mode would want other
values. That is a theming decision of exactly the kind section 9 is for and is
left to the step that has an application asking for it; what is not left is the
legibility of a **field**, which states its own background, text and caret
colour so that it cannot end up as light text on a light field.

### 4.6 A configuration bigger than the window

A configuration of any interesting size does not fit a window, and with the
explanations shown it fits one even less. So the editor scrolls, and what
scrolls is **the label, the docstring, the load message and the members**. The
validation verdict, the saving line and the buttons or the footer stay where
they are, because they are what a user reaches for after editing rather than
something to be scrolled to.

Both backends do that, and the size of a window is the one thing neither of
them can leave to the model: Textual gives the body the height that is left
over, and Tk has no scrolling frame at all and needs the canvas, the scrollbar
and the frame on the canvas that this amounts to.

Three things about the Tk side had to be learnt from a window rather than from
a design, and are recorded because none of them is obvious:

- **The part that does not scroll is packed first.** Tk gives each child the
  space it asks for in the order they were packed, so the verdict, the saving
  and the buttons were laid out below the bottom edge of any window too short
  for everything, where no scrolling could reach them. It is created second,
  so that the widgets are still created in the order they are read in.
- **The size the editor opens at has to be said.** A canvas asks for a width
  and a height of its own that have nothing to do with what is on it, so the
  body is measured and the canvas asks for that, up to the size of a window.
  A configuration smaller than that limit opens a window smaller than it.
- **A paragraph has to be told to wrap.** A Tk label neither wraps nor shrinks
  of its own accord: text wider than the window is simply cut off. Every text
  of the editor that is a paragraph follows the width it is given; the mark of
  a member is the one that does not, because it belongs beside its field on one
  line, and a narrow window squeezes the field rather than the mark — which is
  the same direction the Textual style sheet gives way in.

Textual needs none of those three: it wraps, it shrinks, and its footer is
docked. What the two backends share is which part scrolls, and that is what
this section is about.

**Testing this needs a window that is on the screen.** Tk lays out the widgets
*inside* a frame only once the window has been mapped, so a withdrawn window
can say where the frames are and not what is in them. The rules above are
therefore tested where they are decided — the packing order, the size the
canvas asks for, the line width a label follows — and one test that maps a real
window and measures the lot belongs to category 3 of section 10.2, deselected
by the build and run by hand.

### 4.7 Folding a node away

A configuration of any size does not fit a window (section 4.6), and a list of
two hundred elements fills one on its own. So a node that holds rows can be
folded to its one summary line and opened again, and **which of them are folded
belongs to the model**, by the same rule as the explain toggle of section 4.4
and for the same reason: two user interfaces of one application that were
folded differently would be worse than either behaviour. Every row carries
whether it is folded and whether it is shown, which is where a backend reads
it, so that neither of them works out for itself what folding hides. Settled at
step 10 for a list and a dict, and step 11 made a nested configuration object
one of them without changing anything here — which is what settling it as "a
node that holds rows" rather than "a container" bought.

**Folding a nested configuration object also asks it about itself**, which is
section 6.2 and the one thing folding does beyond deciding what is on the
screen. Opening one asks as well: the answer is the same question either way,
and changing how much of an object is shown is the moment the user is looking
at it. A list and a dict are asked nothing, because neither is a configuration
that has anything to say about itself.

**The editor opens with a container open unless opening it would flood the
window.** That is the same decision as section 4.4's, made once more where it
stops being obvious: what an application put in its configuration was put there
to be read, and a list that fills the window before the user has seen the
members below it is where that stops being true. So a container is folded at
the start when the rows it would add are more than `OPEN_AT_MOST`, counting
everything inside it and not only its direct children, because that is what
fills a window. It is a number the editor chooses for itself and not a setting,
by section 9.6: it is not something the application knows and the editor
cannot.

**Two ways of asking for it, and they answer different questions.** A control
on the row of each container folds that one, which is what a tree has always
offered; and one action of `Settings` folds or opens all of them at once, which
is what a key is worth. The action folds while anything is open and opens
everything once nothing is, so a press always changes something, and each
backend names it for what the next press will do — the Textual backend by
renaming the action, as it already does for the explanations, and the Tk
backend by renaming a button rather than by a tick-box, because a partly folded
configuration is neither of the two states a tick could show.

**A configuration with nothing to fold is offered nothing**: no action, no key
and no column for the controls. A control that could never do anything would be
offering something that is not there, and the column would be width taken from
the values for nothing.

### 4.8 A validation pass can change how many rows there are

`ListOrderingValidator` sorts a list and removes its duplicates, and a member
validator returns the value that is stored back into the member (section 6.4).
So a pass can leave the model with other rows than it had: the value the user
typed into may be gone. The model therefore **builds its rows again** from the
values the pass accepted rather than writing into the ones it had, carrying
over what each row that is still there knew — what it is compared against, what
a validator did to it, and whether its container is folded.

**Both backends check the paths and build their widgets again when they
differ.** Neither of them can write into a widget for a value that is not in
the buffer any more, and neither may keep one. They leave the widgets alone
whenever the paths match, which is every ordinary refresh, and that is what
keeps the focus in the field the user is typing into. It is also the machinery
that step 14 needs when the user adds and removes elements, so it is built once
and here.

## 5. Loading

### 5.1 The loader protocol

The application may need to pass constructor arguments this library
knows nothing about. The loader protocol solves that by having a
**closed** signature: the editor passes only the four things it owns, all
keyword-only, and anything else is bound before the callable reaches the
editor, with a closure or `functools.partial`.

```python
class ConfigLoader(Protocol):
    """Construct the application's Config object for the editor."""

    def __call__(self, *, from_json_data_text: Optional[str] = None,
                 from_json_filename: Optional[PathOrStr] = None,
                 ok_to_use_defaults: bool = False,
                 stderr_file: TextIO = sys.stderr) -> Config:
        """Construct one Config object from the given JSON source."""
```

This is `config_as_json.ConfigFactory` plus the one parameter it lacks.
Adding it here means factory-constructed configurations get load-policy
control, which they cannot get through `ConfigFactory` today. It had a fifth
parameter for the hook that reports automatic changes until `config_as_json`
1.5 made that hook something every configuration object has (section 5.3);
what a loader is never asked for is one parameter less to explain.

When no loader is supplied, the editor derives one from `type(config)`,
reading `inspect.signature()` to decide what that class can be told. The name
of the JSON text is what that is for, because more than one name for it is in
use; section 8.3.4 is where that was found and why it is answered from the
signature rather than from one documented shape.

**The derived loader is published**, as `derived_loader`, because an
application that needs one usually needs exactly this with one argument of its
own bound into it, and a hand-written loader for that would be six lines of
what the editor already does:

```python
loader = derived_loader(partial(TeamConfig, KNOWN_TEAMS))
```

It reads the signature of whatever it is given, and `functools.partial` over a
class has one. Writing the protocol out by hand stays the door for anything
this cannot express, which in practice means a class chosen by looking at the
JSON. Settled at step 9.

**Loading is the only thing that needs the loader**, which is what makes it
affordable. Section 6.1 does not construct the class at all, so an application
that has a loader needs it for reading a file and for nothing else, and one
that has no loader is no worse off anywhere else.

**A loader answers a call with no JSON source.** That answer is the
configuration the editor edits when it was given no file, so the protocol asks
for it, and a loader that chooses its class by looking at the JSON has to name
the class it uses for a configuration that does not exist yet.

**A loader may choose the class**, and one rule makes that work: the class is
chosen when the file is loaded, and the session then edits that class. Nothing
asks the loader again while the user types, because the rows, the descriptions
and the marks are that one class's. What a save asks is section 7's question,
and it is where a value that would select another class is caught.

**A loader that ends the process is turned into a refusal.**
`config_as_json` ends the process for a file it cannot make sense of —
`config_factory_from_json` does it when no matcher accepts the JSON — so a
loader written around it does too, and inside an editor that would cost the
user the whole session. Every call the editor makes to a loader goes through
one function, which turns `SystemExit` into the `ValueError` that every caller
already reports as values the configuration would not accept.

**`Config.__init__` takes no `ok_to_use_defaults`.** Confirmed against the
implementation in `./venv` at step 4: the parameter belongs to
`Config.parse_json()` and `Config.read()`, and `__init__` calls both of them
with the default `False`. So the derived loader has one path for both
policies: construct the class with no JSON source, which leaves it holding
its declared defaults, and then call `parse_json()` with the
`ok_to_use_defaults` the policy asks for. What that parse records about an
older file is on the object afterwards, because the hook it records into is
the object's own.

The editor also reads the file itself rather than passing a file name on to
`Config.read()`, which calls `file_must_exist()` and therefore ends the
process with `sys.exit(1)` when the file is missing. An editor has to say so
and stay alive. Reading the text here is also what section 5.3 needs for its
diff, and what section 5.2 needs to know which keys the file contained.

Nested configs need nothing from the application: `nested_configs()`
already provides each nested `config_type` and its optional
`factory_function`. One root loader is the whole contract.

### 5.2 Load policy

```python
class LoadPolicy(Enum):
    """Policy for declared keys missing from the input file."""

    STRICT = auto()
    DEFAULTS = auto()
    STRICT_THEN_DEFAULTS = auto()
```

`STRICT_THEN_DEFAULTS` is the default: load strictly, and on failure
retry with `ok_to_use_defaults=True` and tell the user that defaults were
needed. The application can override, because whether a partially
specified file is acceptable is an application decision.

**The retry rescues only one of two failures.** `ok_to_use_defaults`
governs *missing* keys only. `Config.check_key_match()` raises `KeyError`
both for a missing required key and for an **unknown** key in the file,
and the retry does not help the second case — nor should it, since an
unknown key is a typo or a file from a newer version and discarding it
would lose data.

**That is also how the two are told apart.** The retry decides it: a retry
that succeeds says the file was merely incomplete, and a retry that raises
`KeyError` again says there is an unknown key. Nothing reads the text of a
diagnostic to classify a failure, so the classification is unaffected by
ROCF renaming a key before the check runs. `STRICT` runs the retry as well,
because it needs the same distinction to pick a message; there the retry
only decides which refusal to report and never opens the file.

The outcomes, each with a message of its own:

- missing keys → "your file was incomplete; these values were filled in
  from defaults" (plus the per-field *filled from default* flag). Under
  `STRICT` the same file is refused, with its own wording.
- unknown key → "your file contains a key I do not recognise"; the file
  cannot be opened
- `ConfigBadJson` → the file cannot be read as configuration; the file
  cannot be opened. This covers text that is not JSON *and* JSON whose
  values cannot be converted, an enum name that names no member being the
  case that arises in practice, since `parse_converters()` runs inside
  `json.loads()`. The message says that much and the diagnostics say which
  of the two it was. Step 7 improved the enum case for a field being *edited*
  and deliberately left this one alone: a file that cannot be opened is not a
  field the user can correct, and reading the diagnostics of the load is
  exactly what they have to do. See section 4.2.
- **values a validator refuses** → the file cannot be opened. `parse_json()`
  ends with `validate()`, so there is no valid object to build a model from.
  Settled at step 4, and the reason it is a refusal rather than an editor
  opened on the file's own values: a member validator returns the value that
  is stored back into the member, so a load that stopped part way through
  leaves it unknown which values were already rewritten and which were not,
  and there is then nothing honest to show. The user is told to correct the
  file in a text editor first.
- **a file that cannot be read, or that is not UTF-8 text** → the file
  cannot be opened. This is the editor's own message, because
  `Config.read()` would end the process (section 5.1).
- **a class the editor cannot construct** → the file cannot be opened, and
  the message names the class. An application whose constructor needs
  arguments this library knows nothing about supplies the explicit loader of
  section 5.1 instead.

The per-field *filled from default* flag is what the key check of the parse
was not given, which is exactly what the declared defaults supplied. A load
that was allowed to use them cannot be asked afterwards, and the keys of the
file do not answer it either, because ROCF may have renamed a key of the file
into a member or supplied a value for one the file never held. So the parse is
asked, by a copy of the loaded object whose `check_key_match` records what it
was given and stops the parse there — the same borrowing as section 6.3, and
stopping is what keeps the application's own validators running once, on the
object that is really being edited. Settled at step 8, where computing the flag
from the keys of the file turned out to claim that a renamed member had been
filled in from a default, which is untrue of it.

### 5.3 Making automatic changes visible

Reading an old-format file applies `ReadOldConfiguration` rules, so the
data presented for editing can differ substantially from the file on
disk. The user must be told, or the editor looks broken.

**The comparison is the mechanism**: load the file, re-serialize the resulting
config, and diff that against the raw file text. Any difference means the load
changed something. It needs nothing at all of the configuration class and it
covers all three sources of surprise:

- ROCF migration of an old-format file
- normalization during parsing
- values filled in by a permissive load

It is the mechanism rather than a fallback because the second of those three is
recorded nowhere: a value a member validator rewrote is not an automatic change
of the kind `config_as_json` reports, and only a comparison finds it.

**What the load recorded says why.** `Config.auto_change_hook()` is the hook of
the most recent parse, and `hook.changes` holds one `RocfChange` per automatic
change, saying what kind of change it was, which path of the file it consumed
and which path of the configuration it produced. That is what no comparison can
know: a renamed key is simply gone from the file, and nothing in the file says
what it became.

The editor must still **construct** the configuration rather than receive an
already-loaded one, because the load policy of section 5.2 is decided while the
file is read; but the records reach it whatever it constructs.

Built at step 8 and rebuilt against `config_as_json` 1.5, which is what settled
the first two of the five things below.

**Nothing is opted into and nothing is passed.** `Config.__init__` creates a
hook when the application names none, keeps by reference the one it is given,
and publishes both through `auto_change_hook()`. So a class that declares
`auto_ch_hook` and hands it on is reported on exactly as fully as the ordinary
three-keyword constructor shape that does not, the editor passes no hook
anywhere, and `ConfigLoader` has no parameter for one (section 5.1). Until 1.5
`Config.__init__` deep copied the hook it was given and recorded into the copy,
so the editor's own hook had to say that a copy of it was itself; that
work-around is gone, and with it the rule that the hook had to be read before
anything parsed the file again — a copy of the configuration now carries a copy
of the hook, so a later parse cannot disturb what the load recorded.

**A record reaches a member or it reaches the message.** That one rule places
all of them. A record that produced a member of this configuration explains
that member and is shown at it, so the mark says *read from the older key
`title`* rather than only that something happened. A record that produced no
member consumed a key of the file that nothing here holds, and joins the keys
the message says saving leaves out — and a key that a member did receive is
taken *out* of that list, because the comparison put it there and the record
knows better. A record that did neither supplied a value this configuration
does not write, which has no row at all, so the message names it and the value
it carries.

**The records are versioned, and the fallback is text.** `config_as_json` steps
`DATA_STRUCTURE_VERSION` whenever what it records changes, and asks a reader of
the records to declare the version it was written for. A future version that
records something else is not worth refusing a file over: the comparison still
finds every changed member, and what the records would have added is taken from
`print_changes`, the library's own report, which is version independent by
contract. That text is shown as it stands and is never parsed — parsing it
would be a second way of depending on the version it exists to avoid.

**The comparison is canonical.** `config_as_json` writes the keys of a
dictionary sorted while a file is written by hand, so the values are compared
with their dictionary keys sorted. Everything else is compared as it is
written, which is what tells `1` from `1.0` and from `true`, exactly as
section 4.2 requires of the *edited* mark.

**A class that cannot write itself is left as it was.** The comparison reads
what the load would write, so such a class has nothing to compare — and it
cannot be shown at all, for the same reason. The comparison then reports
nothing and the refusal stays where section 8.3.4 put it.

## 6. Validation

### 6.1 Whole-configuration validation

`Config.parse_json` runs the entire chain: key matching, recursive
dict-shape checks against defaults, `parse_converters()`, nested-config
construction, and then `get_validation_plan()`. So a validation pass is:

> serialize the edit buffer to JSON text, apply it with `parse_json` to a deep
> copy of the configuration object of this session with a captured
> `stderr_file`, and catch `KeyError`, `ConfigBadJson`, `TypeError`,
> `ValueError`, `InvalidConfiguration`, `InvalidConfigurationValue` and
> `InvalidConfigurationType`.

The user sees exactly the diagnostics the application would see at load
time. There is no second validation implementation and no way for the
editor to accept something the application later rejects.

**The class is not constructed, and it does not have to be.** This document
first said "construct a candidate config from that text", and step 9 found
that the construction adds nothing: the declaring of the members is the whole
of what a constructor does before `parse_json`, and a copy has that already.
Even the derived loader of section 5.1 never gives the text to a constructor,
because the load policy belongs to `parse_json` and not to `__init__`.

Copying instead of constructing is what makes two classes editable that were
refused before: one whose constructor needs an argument this library knows
nothing about, and one with no JSON text parameter at all. Both are validated
and saved like any other, and the loader an application supplies is then for
reading a file and for nothing else. Copying is also what keeps a session on
one class where a loader would choose another (section 5.1), and it is what
gives the probe of section 6.3 the object it needs.

### 6.2 Subtree validation, and why folding is the natural trigger

A nested config subtree can be validated **in isolation**, by applying that
subtree's JSON to the nested object itself. Built at step 12.

**The object is copied and not constructed**, which is the same correction
step 9 made to section 6.1 and for the same reason: the object is there to be
copied, so a class whose constructor needs an argument this library knows
nothing about is asked about itself exactly as well as any other, a
`factory_function` that answered with a subclass is asked as the subclass it
really is, and there is one way of applying a buffer to an object rather than
two. This document first said "constructing `config_type` from that subtree's
JSON", which was written before that correction and would have been the second
way.

That makes folding and validating the same operation: when the user folds a
nested config away — or opens it again, since changing how much of an object
is on the screen is the moment the user is looking at it — the editor asks
that object about itself and shows the result as a badge on its row.

Two validity levels result, and the UI must distinguish them:

- **subtree-valid** — this nested config is internally consistent;
  cheap, local, available on fold
- **config-valid** — the whole tree passes, including
  `WholeConfigValidator` and `ProjectedWholeConfigValidator` steps on a
  parent that relate members *across* a nesting boundary; obtainable
  only at the root

A subtree can be valid while the root is not. That is the honest state
and both should be shown.

**The badge is worded so that it cannot be read as the other one.** It says
*valid on its own*, and the words that qualify it are the whole point: a rule
of the class above relating two objects across the boundary between them
refuses the configuration while saying nothing against either object, so a
badge that said only *valid* would be answering a question nobody may ask of
it. Whether the file can be written is the verdict line of section 6.5, and
that line is the only thing that answers it. The other direction needs no
qualification, because an object its own class refuses cannot be part of a
configuration that is saved.

**A pass the class accepted answers for every object at once**, so none of
them is asked again: `parse_json` builds and validates each nested object
while it reads the buffer, so a whole configuration that was accepted has
every subtree in it accepted already. The walk therefore runs only when the
whole buffer was refused, which is also the only time it has anything to add.

**The innermost object is asked first, and one holding a refused one is not
asked at all.** It is refused whatever else is true of it, and asking it again
would report one mistake once for every object it happens to be inside.

**What a nested object refuses about no member of itself is shown at that
object**, and not in the block below the members. It is about the object, the
object is a node with a row, and section 6.5's reason for naming a place
applies: a configuration of any size does not fit a window. The block keeps
what is about no node at all, which is where a rule relating two objects
across a boundary belongs.

**A state that has not been asked for is shown as nothing**, the third state
that `verdict` and `save_outcome` already have. It is taken back whenever
anything inside that object is edited, which is a different lifetime from the
verdict of the whole configuration: that one is dropped by an edit anywhere,
and this one only by an edit inside the object it is about. That difference is
why it is carried by the row rather than by the verdict.

### 6.3 Field-level attribution

Whole-config validation alone would present the user with one block of
diagnostics. Better attribution is available without introspecting any
validator's constraints, because two things are public:

- `MemberValidationStep` is a dataclass with public `member_names` and
  `validator`
- `MemberValidator.validate_member(config, member_name, member_value,
  stderr_file)` is a public abstract method

So, given a complete candidate config, the editor can run an individual
member's validators and attribute each failure to a specific field.
Custom application validators work identically, since no knowledge of any
specific validator class is required.

Note that `validate_member` receives the whole `config` object and may
inspect other members, so a complete candidate must be built first;
individual fields cannot be validated in isolation.

**The candidate this needs cannot be held the ordinary way**, and that is
what step 7 had to solve. `Config.parse_json()` ends in `validate()`, which
raises at the first step that refuses — so the object that could say which
member was refused is exactly the object that a refusal keeps the editor from
ever holding. A copy whose `get_validation_plan` returns nothing is that
object: everything else the parse does still happens, and only the plan is left
out, which is what the walk then applies itself. The plan is asked of the class
and not of the object, because it is the object that has none, so what is
applied is the application's own plan and not the empty one.

**The reason the buffer is parsed and not assigned** is that the whole parse
chain runs on the way in: the keys are matched, the dict shapes are checked
against the defaults, the parse converters run, and from section 4.1's step
onwards the nested configuration objects are built. Assigning the buffer onto
an object member by member would mean the editor applying the converters
itself, which is a second implementation of something `config_as_json` already
does, and it would put a plain `dict` where a nested `Config` object belongs.
The subtraction of one method is the whole of what this borrows; everything
else is the library's.

**The method is left out on the object and not on a class.** Step 7 built this
as a throwaway subclass, and step 9 replaced that with one attribute of one
copy, for two reasons. It works for a class the editor cannot construct, which
a subclass of it does not: the loader an application supplies constructs the
application's class and not the editor's subclass of it. And it leaves the real
method where the walk needs it, because the class of the copy is untouched.
`parse_json` does not mistake the replacement for a member, because it counts
the attributes of the object that are not callable. The same borrowing answers
what the declared defaults filled in (section 5.2), where the method left out
is the key check.

**The walk differs from `Config.validate()` in two deliberate ways.** A member
that is refused is recorded and the walk goes on, so that every member the
user has to correct is named at once rather than one per pass; and a step that
is about no single member is applied only while no member has been refused,
because that is the only case in which the real pass would have reached it. An
editor that reported a rule the application never applied would be inventing.

A member that is already refused is left alone by a later step that names it,
so what is reported about it is the first thing that was wrong with it, which
is also what the real pass would have reported.

### 6.5 Where a refusal is shown

What is refused about one member is shown **at that member**, and what is
refused about no single member stays in the block below them. The verdict line
names the members it was about, because a configuration of any size does not
fit a window (section 4.6) and a user who has just asked what is wrong should
be told where to look rather than have to go looking. Settled at step 7.

**What is refused is addressed by a path and not by a name**, settled at step
10, because a value inside a list or a dict is a node of its own and two of
them can share a name: a dictionary key called `cpu` must not be told what the
application said about a member of that name. The verdict line writes the whole
path of each of them, so a value the user has to correct can be found.

**What a member validator refused is about the whole member**, because the
whole member is what it is given, so it is shown at the member and never at one
value inside it. That is not a limitation of the editor: `validate_member`
receives one member name, and an editor that guessed which value inside it the
validator meant would be inventing. What one *value* can be refused for on its
own is the conversion of section 4.2, and that is shown where it was typed.

The same sentence is therefore not on the screen twice: what the attribution
explained is taken out of the block, and the block keeps what it could not
explain — a whole-configuration validator, a key that does not match, text
that is not JSON, a class the editor cannot construct.

One member can have two things wrong with it, and they are not the same thing:
its text may mean no value of it at all (section 4.2), or the application may
have refused the value it holds. **The first is preferred when both are
there**, because a value that does not exist yet is what has to be corrected
first. The two also live for different lengths of time, which is the reason
they are kept apart rather than merged: the first stays true until that member
is edited again, and the second is dropped as soon as anything in the buffer
changes.

A refusal is **not** covered by the explanations toggle of section 4.4. A
description says what a member is for and is what a user who knows the
configuration wants out of the way; a refusal is the one thing on the row that
has to be read. It is shown *below* the description of the same member, so
that a line which comes and goes moves nothing that is above it, and it is
`Emphasis.BAD` where the description is `Emphasis.MUTED`, so that the two
cannot be mistaken for each other.

### 6.4 Validation mutates

`Config.validate()` documents that "a member validator returns the value
that shall be stored back into the member, even if that returned value is
`None`". Validators such as `StrValidator(best_match=True)` and
`StrCaseChangeValidator` rewrite what the user typed.

A validation pass is therefore **not read-only**. After every pass the
editor refreshes its buffer from the validated object and sets the
*changed by validator* flag on each rewritten field. The rewrite is
accepted silently but is visibly highlighted; silently altering text the
user just entered without showing it would be the worst available
behaviour.

## 7. Saving

- **An invalid configuration cannot be saved.** Saving is: validate the
  candidate, and on success call `write()` on it. It is the *same* pass the
  user asks for with Validate, so a validator that rewrites a value rewrites
  it on the way to the file too and the editor shows what was written rather
  than what was typed.
- `edit()` returns the saved `Config` object, or `None` if the user
  cancelled. The caller's own object is never mutated and would
  otherwise be stale.
- `out_file` defaults to `in_file`. If both are `None` the editor starts
  from defaults and must obtain a destination before it can save. The model
  reports that it has none and the backends ask the user for one; the model
  invents nothing, because a file name is not something a library can guess.
- **Saving leaves the editor open.** A save is not the end of a session, so
  Save answers "is there anything to write" and the session ends only when
  the user closes it. `edit()` then returns the object that really reached
  the file, whatever was typed afterwards and not saved.
- **`Config.write()` does validate.** Confirmed against the implementation in
  `./venv` at step 5: `write()` calls `as_json_string()`, whose first
  statement is `self.validate(stderr_file=stderr_file)`, and it opens the
  destination only after the text exists. So the editor's own gate is belt
  and braces rather than the only guard, and a configuration that `write()`
  refuses leaves the file on disk exactly as it was.
- A destination that cannot be written — a folder that does not exist, a file
  that may not be written to — is a message and not a crash, for the same
  reason: the alternative costs the user the whole session.
- **Where the application said how it loads, that is asked once more before
  anything is written**, with the very text the file would hold. It is the one
  question a validation pass cannot answer: the pass applies the buffer to the
  class of the session (section 6.1), and a loader that chooses its class by
  looking at the JSON may read the same text back as another class altogether. A
  file the loader refuses, and one it would read as a class the session is not
  about, are both a refused save with a message; `isinstance` is what the second
  of those asks, so a loader that answers with a subclass is answering with the
  class. An application that supplied no loader is asked nothing, and the class
  it edits is the class it gets. Settled at step 9.

### 7.1 Draft file (room left, not implemented in v1)

"Invalid cannot be saved" means a user with a long, still-invalid editing
session has no way out but to discard it. The escape hatch that preserves
the rule is an editor-owned **draft file** holding the raw JSON buffer —
explicitly not a `config.write()`, explicitly not loadable by the
application, reopened by the editor on next start. Not a v1 priority, but
the model must not be designed in a way that rules it out.

## 8. The UI backend contract

The end goal is an editor embeddable in an application that already runs
its own Textual or Tk event loop. That costs nothing if it is decided
now, and is a rewrite if it is not.

- The model is a standalone object. It does no I/O in its constructor
  and owns no event loop.
- `edit()` is a thin convenience wrapper: build the model, run a backend
  to completion, return the result.
- The backend `Protocol` is phrased against the **model**, never against
  `edit()`. Embedding is then additive: the host application builds the
  model itself and mounts the backend as a widget.

```python
def edit(config: Config, backend: EditorBackend, *,
         descriptions: Optional[Descriptions] = None,
         in_file: Optional[PathOrStr] = None,
         loader: Optional[ConfigLoader] = None,
         out_file: Optional[PathOrStr] = None,
         policy: LoadPolicy = LoadPolicy.STRICT_THEN_DEFAULTS,
         settings: SettingsSource = Settings(),
         stderr_file: TextIO = sys.stderr) -> Optional[Config]:
```

The `config` argument serves as the schema and defaults source and stays
the ergonomic front door; `loader` is the door for applications with
constructor arguments we do not know about. It stays required when a loader is
given, because the protocol says a loader answers a call with no JSON source
(section 5.1), so an application that has one has an object of its class as
well; `load_config` and `EditModel` take the loader for the same reason and on
the same terms.

`descriptions` is an optional keyword and not the required positional argument
this document first gave it. An application that describes none of its members
is a perfectly good caller: the docstring of its configuration class still
labels the object, and principle 4 of section 3 says that what the editor
cannot be told it does without. Requiring the argument would also have made
every existing call site pass an empty mapping to say nothing. Settled at
step 6, where the same reasoning made `EditModel`'s arguments after the load
report keyword-only: each of them says one independent thing about the session,
and none of them is worth passing by position.

The `backend` argument is one this document originally left out, and it has
to be there: the core never imports a user interface library, so it cannot
name one. Each backend package therefore also exports an `edit` of its own
that supplies itself and forwards everything else, which is the shorter door
for an application that has already chosen its user interface. Those wrappers
are a signature and one call, so section 8's warning about logic drifting into
the backends does not apply to them; if either of them ever grows a decision
of its own, that decision belongs here instead.

A practical consequence of the split: the backends must stay thin. All
three packages share a single pylint invocation, and this repository
forbids file-level `duplicate-code` disables. If the Tk and Textual trees
start tripping R0801, the correct response is to move logic into the core
— tree flattening, fold state, edit dispatch, dirty tracking and
diagnostic presentation all belong there. The linter will keep us honest
about the layering we are paying three packages for.

### 8.1 Entry points (deferred)

An `edit_cfg_json.ui` entry-point group would let backends register
themselves for discovery (`--ui=auto`). It is additive and breaks
nothing, and is only worth building once there is a generic launcher or
a third-party backend in the wild. The three programs of section 8.3 are not
that launcher: each of them supplies its own backend, so none of them has
anything to discover.

### 8.2 Embedding in an application that already runs a UI

Embedding is out of v1 scope (section 11) and is **designed here before it
is built**, because two of its questions have answers that are cheaper to
give now than to retrofit: which toolkit instance the editor attaches to,
and where in an existing window it is placed. What that costs today is
recorded in section 8.2.5; everything else is additive.

The two questions are the same in both toolkits, and so are the answers.

#### 8.2.1 Which instance does the editor attach to?

**It is told, and it never guesses.** Neither toolkit offers a supported
way to ask.

- **Tk.** `TkEditor.run_editor` creates a `tkinter.Tk`, which is a Tcl
  interpreter. A second one in the same process is a second interpreter,
  and widgets, variables, fonts and images cannot cross between them. The
  toolkit's own rule is one `Tk` per process and `Toplevel` for every
  further window. Detecting an existing one means reading
  `tkinter._default_root`, a private name, and then guessing what the
  application meant by not saying.
- **Textual.** There is one `App` per event loop. `App.run()` calls
  `asyncio.run()` or `loop.run_until_complete()`, so calling it from
  inside a running app raises or deadlocks. `textual._context.active_app`
  would answer the question and is private.

So `run_editor` stays what it is — the editor that owns a window and a
loop — and it is documented as being for an application that runs neither
yet. An application that runs one already uses the entry point of
section 8.2.3, and hands over the parent it wants.

#### 8.2.2 Where in an existing window is it placed?

**Inside the widget the application names, and the editor destroys only
what it created.** One rule, one argument, both toolkits.

An application that wants the editor in a window of its own creates that
window itself — `tkinter.Toplevel(root)`, or a Textual `Screen` — and
passes it. This is one line in the application, and it buys three things:
the library never has to guess whether a given widget was meant as a
container or as a master; the window title, geometry, `WM_DELETE_WINDOW`,
`transient` and `grab_set` stay with the application, which is where they
belong; and the editor can state one rule about closing instead of two.

The rejected alternatives are in section 12.

#### 8.2.3 It cannot be `run_editor`, so it is a second entry point

`EditorBackend.run_editor` promises to run until the user is done. An
embedded editor cannot keep that promise. Tk could fake it with a nested
`wait_window`, but Textual has no way to nest a second loop at all, and an
editor mounted in a panel of the application's window should not suspend
the application's call stack in either toolkit.

Embedding is therefore a **separate, non-blocking entry point per backend
package**, additive to the protocol rather than a change to it:

```python
# edit_cfg_json_tk
class TkEditorPanel:
    def __init__(self, parent: tkinter.Misc, model: EditModel, *,
                 on_close: Optional[Callable[[], None]] = None) -> None: ...
    def close(self) -> None: ...

# edit_cfg_json_textual
class EditorPanel(Widget): ...    # mounted into an area
class EditorScreen(Screen): ...   # pushed as a screen of its own
```

`on_close` is how the application learns the session ended; the outcome is
`model.saved_config`, which is where `run_editor` already leaves it
(section 8). Neither `edit()` gains an argument: an embedded editor has no
moment at which it can return what was saved, so the wrapper that exists to
return it has nothing to offer here.

#### 8.2.4 What Textual has to be split into

The Tk backend already builds below an arbitrary parent widget, so its
panel is a wrapper. The Textual backend is an `App`, and five things live
at App level that an embedded editor cannot have:

| On `EditorApp` today | Why it cannot stay there |
| --- | --- |
| `CSS` | Textual ignores `CSS` on a widget and says so; a widget uses `DEFAULT_CSS`. |
| priority bindings on `self._bindings` | App-level priority bindings fire wherever the focus is. Verified against `App._check_bindings` in 8.2.8: the priority pass walks the whole binding chain, so a priority binding on a **widget** still beats the focused `Input`, and only while the focus is inside the editor. That is what embedding wants. |
| `self.title` | It is the application's window title. |
| `get_system_commands` | `COMMANDS` exists on `App` and `Screen`, not on `Widget`. An embedded widget cannot offer palette entries; an embedded screen can. |
| `action_quit` | It ends the application. |

So `EditorApp` splits three ways: `EditorPanel(Widget)` holds the whole
body with its `DEFAULT_CSS` and its instance bindings, `EditorScreen`
adds the header, the footer and the palette entries, and `EditorApp`
composes the screen. One body, so the two backends cannot drift and the
CSS and the bindings exist once. The model title moves from `App.title`
into a label of the panel, which is what the Tk backend already does.

#### 8.2.5 What this costs today, and why

Only what would otherwise become a change to a published promise:

- **`EditorBackend`'s docstring** said an application could "mount the
  backend as a widget". It cannot, and that sentence is published in
  `doc/edit-cfg-json_api.md`. It now says what section 8.2.3 settles.
- **`EditorWidgets` is told what closing does** rather than deriving it
  from `parent.winfo_toplevel()`. The default is unchanged and is what
  `TkEditor` needs, but the rule of section 8.2.2 is now stated where the
  editor acts on it, so the panel is an addition rather than a rewrite.

Everything else is genuinely additive: the public surface of both backend
packages is `TkEditor`, `TextualEditor` and `edit`, none of them changes
meaning, and every name section 8.2.3 introduces is new. That is what
section 8's decision to phrase the protocol against the model already
bought.

#### 8.2.6 A defect this uncovered, fixed now

`tkinter.StringVar` built without a `master` is created in the **first**
Tcl interpreter of the process, not in the one its field belongs to —
`tkinter.Variable.__init__` falls back to `_get_default_root`. With an
application's root already present, every field's variable would be
created in the application's interpreter while its `Entry` lived in the
editor's, so the field would show nothing and the callback that writes it
into the model would never run. The fields now name their parent. This is
a defect today and not only under embedding, which is why it is not
waiting for the step.

#### 8.2.7 Left open for the step that builds it

- **Which widget the Tk key bindings are made on.** They are made on the
  toplevel, which is right for a window the editor owns and wrong for one
  it shares: the editor would claim keys across the whole application
  window. A Tk `Frame` does not take the focus, so the answer is one of
  binding on each field, giving the panel a `bindtag` of its own, or
  making it focusable. Textual has no equivalent question, because a
  widget's bindings already dispatch only from the focused widget upwards.

  **The mouse wheel is bound on the same widget and is the same question.** A
  wheel event goes to the widget under the pointer, which is usually a field or
  a label inside the body rather than the canvas that scrolls, so binding the
  canvas alone would leave the wheel working over the empty parts and nowhere
  else. Whatever answers the keys answers this too.
- **Whether the core names the mounting contract.** A `Protocol` for it
  would let a third-party backend implement the same shape, as
  `EditorBackend` does for the modal one. It is additive whenever it is
  added, so it waits until there is a second implementation to check it
  against — a protocol with one implementation is a guess.
- **Whether `Settings` gains anything.** An embedded editor may want its
  bindings not to be priority bindings. That is an application decision of
  exactly the kind section 9 is for, and it is an added attribute, which
  breaks no application.

#### 8.2.8 Facts checked against the pinned versions

Checked against `textual` 8.2.8 and the Python 3.14 `tkinter` in `./venv`,
because each of them decides a paragraph above: `App.run` calls
`asyncio.run`/`run_until_complete`; `App._check_bindings` walks
`reversed(screen._binding_chain)` on the priority pass, so widget priority
bindings are honoured; `active_app` is in `textual._context` and private;
`COMMANDS` is declared on `Screen` and `App` and not on `Widget`;
`DOMNode.__init__` gives every widget its own `_bindings`, so the
per-instance binding the App does today works on a widget too; `Widget`
warns that a `CSS` class variable is ignored; and
`tkinter.Variable.__init__` calls `_get_default_root('create variable')`
when it is given no master.

### 8.3 A ready-to-run program in every package

An application author should not have to write a program to get an editor for
their own configuration class, so each of the three distributions installs one:
`edit-cfg-json`, `edit-cfg-json-tk` and `edit-cfg-json-textual`. They are a
product and not only a development tool, and the second benefit is what built
them at step 7B: every question about a configuration that is not two members
long used to cost a hand-written example, and now any class in reach answers it.

#### 8.3.1 The command line owns no logic

`edit_cfg_json.cli` holds all of it — the parsing, the two doors to a class, the
construction, one editing session and the exit code — and `run_cli` takes the
backend for exactly the reason `edit()` does: the core names no user interface.
Each package is then a program of a few statements. Without that split the two
graphical programs would be near copies of each other, and section 8 answers
duplicate code between the backends by moving logic into the core rather than by
suppressing the warning. It is also what makes the whole program testable with
no display and no toolkit, by handing `run_cli` a backend that is a stub.

Each program is reachable as `python -m` on its own package as well, so a
machine whose script folder is not on `PATH` can still run it, and all three
complete their own command lines with `argcomplete`.

#### 8.3.2 The class is told, and never guessed

`--module` names an importable module and `--file` names a Python file, exactly
one of the two is required. A single `module:Class` argument reads better and
would have to guess which of the two it was given, which is the decision section
8.2.1 already took for this library as a whole; it would also make a Windows
drive letter a special case, and it would take the refusal of a missing or a
doubled location away from `argparse`.

**What to edit is either a class or a loader**, named by `--class` and
`--loader` in that module or file. At least one is needed and both are allowed:
a class alone is constructed on the values it declares, a loader alone is asked
for a configuration and the class it answers with is the class of the session,
and the two together mean that the loader has to answer with that class or the
program stops. The check is made on the object that is really going to be
edited, so a loader that chose its class from the input file is answered for
that file, and `isinstance` is what it asks.

The class was a positional argument until step 9 and is a named option now, so
that the two ways of saying what to edit are symmetric. `argparse` can be asked
for exactly one of two options and not for at least one of them, so the refusal
of a command line that names neither is the one that is written by hand.

**A loader cannot be finished off from a command line**, and the refusal says
so: whatever it needs beyond the four keyword arguments of `ConfigLoader` has
to be bound where the loader is written, because a command line cannot supply
an argument this library knows nothing about. That refusal, a name that cannot
be called at all, and a loader that answered with the wrong class each have a
number of their own, for the reason section 8.3.3 gives.

The file door puts the folder of the file at the front of `sys.path` and imports
it by its own stem, so a module that imports its neighbours works, and it puts
both back afterwards: a second file of the same stem must really be read rather
than found among the modules of the first. A module that belongs to a package
and uses a relative import cannot be loaded from a bare path at all, and is
refused with a message naming `--module` with `PYTHONPATH` instead.

**Importing a module runs it.** The help text and the readme say so. It is not
guarded against, because it is the same exposure as `python somefile.py` and a
guard could only be a pretence.

#### 8.3.3 What the program answers with

`ExitCode` gives each way of refusing a number of its own, because a program of
this library is meant to be usable from a script and from a continuous
integration job. A program whose backend prints once and returns is the one that
`--save` belongs to — there is no later moment at which a user could press Save
— and it is also the one whose exit code answers with the verdict of the buffer,
because there is nobody to read one. A program that gives the user a session
ends with success when the user closes it, whatever is left in the fields:
closing an editor is not a failure.

That one fact about a backend is what `run_cli` is told, and `--save` is then not
added to the parser at all for the other two, so it is `argparse` that refuses
it rather than a check written by hand.

#### 8.3.4 What the corpus showed, which is why the step exists

Opening the 47 configuration classes of `dep_lib_doc/config_as_json/example/`
found two things that no example in this repository would have.

- **The constructor has more than one shape.** `Config.__init__` names the JSON
  text `from_json_data_text`; the example classes that `config_as_json` ships
  name it `from_json_text` in the constructors they declare, as does
  `ConfigFactory`. 32 of those classes were refused by the editor over the name
  of a parameter. The editor now reads the signature and passes every parameter
  it knows the meaning of, which is principle 4 of section 3 applied to a
  constructor. Step 7B answered that by passing the text under whichever name
  the class declares, and refusing a class that declares neither, because a
  buffer validated against the declared defaults would be accepted whatever the
  user typed. Step 9 removed both: no text is passed to a constructor at all
  (sections 5.1 and 6.1), so a class with nowhere to put it is edited like any
  other, and the names are looked for only to pass `None` under one that has no
  default of its own.
- **A class may not be able to serialize itself.** The editor reads the values
  it shows with `as_json_string()`, so a class that leaves part of its own
  writing to code outside itself has nothing for the editor to show at all. That
  is a refusal of the program with a message and a number, and the exception
  that `EditModel` already documents for an application that builds the model
  itself and knows its own class.

The places that construct the application's class ask one internal module what
to call it with, so the answer cannot differ between them. Step 7B had four of
them; two are left after step 9, the declared defaults and the load, because
the validation of a buffer and the walk that attributes a refusal now copy an
object rather than construct one.

## 9. Settings the application owns

The editor does not run on its own. It runs inside an application that has
already made decisions the editor has no right to overrule: which key
combinations that application's own user interface has taken, and what a
configuration file of that application is called. The first steps of this
library made both of those decisions inside the editor. That was the right
size of decision for a walking skeleton and the wrong one for a library.

`Settings` is what the application says about them. Every attribute has a
default, so an application with no opinion passes nothing at all and gets
what the editor would have chosen anyway.

### 9.1 The shape

```python
@dataclass(frozen=True)
class ActionSettings:
    quit: tuple[str, ...] = ('ctrl+q',)
    validate: tuple[str, ...] = ('ctrl+r', 'f5')
    save: tuple[str, ...] = ('ctrl+s',)
    save_as: tuple[str, ...] = ('ctrl+shift+s', 'f12')
    cancel: tuple[str, ...] = ('escape',)
    explain: tuple[str, ...] = ('f1', 'ctrl+g')
    fold: tuple[str, ...] = ('f2', 'ctrl+t')


@dataclass(frozen=True)
class Settings:
    actions: ActionSettings = ActionSettings()
    file_extension: Optional[str] = None
    extension_enforced: bool = False
```

One attribute per action rather than a mapping keyed by an action enum. The
attribute *is* the default, so an action the application says nothing about
needs no merge rule to be written down and no merge rule to be explained; a
misspelled action name is a `TypeError` where the mistake was made rather
than a key nobody ever reads; and the reason for a default lives in the
docstring of the attribute that holds it, which is where the next reader
will look for it. An action added later is an added attribute, which breaks
no application.

Both classes are frozen. The editor is given what an application decided and
has no business changing it, and a frozen dataclass says so in the one place
where saying it costs nothing.

`explain` is the attribute that step 6 added, and it is what the promise above
was written for: an action added later is an added attribute, and no
application that was written before it breaks. Its keys are `f1`, because a
function key is what asks for help everywhere else and because a field claims
most of the control letters, and `ctrl+g`, because a terminal or a keyboard
that does not deliver a function key would otherwise leave the action to the
button and the command palette.

`fold` is the attribute that step 10 added, and it makes the same point a
second time. Its keys are `f2`, the function key beside the one that explains,
because the two actions are the same kind of thing — both of them decide how
much of the configuration is on the screen — and `ctrl+t`, for the reason
`explain` has a control letter as well and because the tree is what the action
is about. A configuration with no list and no dict in it is never offered the
action at all (section 4.7), so those keys are free wherever there would be
nothing to fold.

**It is deliberately not `ctrl+f`**, which was its second key until the review
of step 10 asked why the editor was spending the one combination that means
find everywhere. `ctrl+shift+f` was considered and rejected for the reason
`save_as` already records above: a terminal that encodes a control letter as a
single byte has nowhere to put the shift, so that combination would arrive as
`ctrl+f` and the fold key would run the search. See section 9.7.

### 9.2 Key combinations

Each action holds a tuple and not a single key, because an action can have
more than one: the first is the one a footer or a menu names, and the rest
work without being named. That is exactly the `('ctrl+r', 'f5')` of the
Textual backend, expressed without a second attribute for the alternate.

An empty tuple takes the key away and not the action. Tk shows a button and
Textual offers a command palette entry, and both stay. An application whose
own `ctrl+s` is spoken for empties that tuple, and its users still save.

Combinations are written in Textual's key names, in lower case: the
modifiers `ctrl`, `shift`, `alt` and `meta` joined with `+`, and then a
single character, `f1` to `f12`, or a name such as `escape`, `enter`, `tab`,
`space`, `backspace`, `delete`, `insert`, `home`, `end`, `pageup`,
`pagedown`, `up`, `down`, `left` or `right`. The core has to name some
vocabulary, and this one is published, complete, and used unchanged by one
of the two backends. Tk needs a translation whatever vocabulary is chosen,
because `<Control-Shift-S>` is a notation no other toolkit shares; the
translation lives in the Tk package, since nothing else can use it. A
combination that the translation does not know leaves that action without
that key rather than without an editor — the button is still there. This is
principle 4 of section 3 applied to keys.

One key combination given to two actions raises `ValueError` where the
`Settings` is constructed. Only one of the two can ever run, which one it is
depends on the toolkit, and the symptom is an action that mysteriously does
nothing. A refusal at the point of the mistake is worth a great deal more.

### 9.3 The file name extension

`file_extension` is `None` by default, which is the "no opinion" this
document has stated since section 1 — with the difference that it is now the
application's opinion that is absent, rather than the editor's opinion being
imposed on an application that has one. A value is normalized to begin with
a dot, so `cfg` and `.cfg` mean the same thing, and text that names no
extension at all is refused.

`extension_enforced` then decides how hard the extension is:

| | a file to write | a file to read |
| --- | --- | --- |
| no extension set | taken as given | taken as given |
| default extension | added to a name that has none | taken as given |
| enforced extension | added to a name that has none, refused when the name has another | refused unless the name has it |

**The two directions differ on purpose.** A name to write does not name an
existing file, so completing it is a service. A name to read does name one,
so completing it would open a different file from the one that was asked
for; there the setting can only refuse. And a default extension says nothing
at all about reading, because a default is about what the editor writes when
the user did not say.

**Completing applies to a name that is chosen, not to one that is
inherited.** `out_file` defaults to `in_file` (section 7), and a session that
read `settings` must not save to `settings.cfg` because the two names differ
by an extension. A destination is chosen when the user answers Save as, when
the application calls `EditModel.set_out_file`, and when it names `out_file`
in the `edit()` call; it is inherited only when it is the input file. So
`edit()` completes the one it was given and never the one it fell back to,
and the model completes what `set_out_file` chooses and takes what it is
constructed with. Both are checked against an enforced extension at every
save, whatever their origin.

A refusal is a message and never a crash, for the reason section 7 already
gives: `load_config` raises the `ConfigLoadError` the application already
handles, and a refused save is a `SaveOutcome` carrying the message that
says why, exactly like every other refused save.

### 9.4 Settings, or a way to get them

```python
type SettingsSource = Settings | Callable[[], Settings]
```

Every entry point takes one of these, and the model resolves it at each
point of use, so a callable really is asked again.

What that buys, stated plainly, because it is less than it looks:

- **Key combinations are read once**, when the backend builds its bindings.
  Textual copies a class's bindings into the instance when the instance is
  constructed, and offers no supported way to change the key of a binding
  afterwards. Tk binds to the window when the widgets are created.
- **The file name settings are read at every save** and at every choice of a
  destination, so a later answer does take effect there immediately.
- **The gain that matters is neither.** It is that an application need not
  have its settings ready at the moment it calls. Under embedding
  (section 8) the model may be built long before the editor is shown, and a
  callable defers the read to the moment the answer is used.

Resolving a callable once and keeping the answer was rejected: an
application that can answer at that moment can pass the `Settings` object
itself, so that variant buys nothing that the plain object does not.

### 9.5 Where the settings enter

`edit()`, `load_config()` and `EditModel()` each take a `settings` keyword
that defaults to `Settings()`. The backends take none: they read
`model.settings`, which is the same rule that already holds for the marks,
the title and the messages. One source per session is what stops the two
backends from binding different keys or offering different file names.

### 9.6 What `Settings` is not for

- **The load policy.** It is already a parameter of its own, and it is a
  decision about one file rather than about the application.
- **Wording.** Button text, footer descriptions and palette entries stay in
  the backends. An application that wants its own wording is asking for
  translation, which is a larger thing than this and should be designed as
  one rather than arrived at through a growing dataclass.
- **Anything the editor can find out for itself.** `Settings` is for what
  the application knows and the editor cannot.

Room is deliberately left here for step 16 of the delivery plan, where
whether an overwritten file keeps a backup, and whether overwriting is
confirmed, become application decisions of exactly this kind.

### 9.7 Keys that are kept free

`RESERVED_KEYS` is `('ctrl+f', 'f3')`, and no default of this editor takes
either of them. Finding a member of a configuration that does not fit a window
(section 4.6) is something this editor is likely to be asked for, `ctrl+f`
opens a search everywhere and `f3` finds the next one.

The promise of section 9.1 — that an action added later is an added attribute
and breaks no application — is about the *attribute*. A **key** that moved
would break every user who had learnt it, and no version number protects a
habit. So the two combinations a search will want are kept free from the start
rather than taken back afterwards, and a test says so about the defaults.

Nothing here refuses these keys to an application. Which combinations its own
user interface has already taken is the application's to say, and this whole
section exists so that the editor does not overrule it; an application that
has no search of its own is welcome to give `ctrl+f` to Save. What is reserved
is what the editor itself may take.

## 10. Testing strategy

### 10.1 Core

The core needs no UI and no display, and it is where essentially all the
logic lives. If a behaviour can only be tested through a backend, that is
evidence the behaviour is in the wrong package.

### 10.2 Tkinter: three categories

Experience with other Tkinter applications says one category is not
enough. Tk tests fall into three groups with genuinely different
requirements:

1. **Stubbed** — real Tk is never called; widgets are monkey-patched or
   otherwise replaced. Runs anywhere, fast, no display. This is the
   default category and should hold most Tk tests.
2. **`root_or_skip()`** — a fixture returning a *withdrawn* Tk root, or
   skipping when no display is available. Real Tk, no visible window,
   still automatable. Most stubbed tests should have a companion test
   in this category.
3. **Focus sensitive** — must run on a real display, and any user
   activity that changes what has focus disturbs them. These cannot run
   automatically. They are run manually, by a person who knows no other
   display activity is happening.

Category 3 maps directly onto `BuildSpec.excluded_test_markers`, whose
own docstring uses `focus_sensitive` as its example and notes such tests
are **deselected** rather than collected — so they never appear in the
summary as skipped, and are run on demand with
`pytest -m focus_sensitive`. The build system already anticipated this
category.

**Interaction to be aware of**: `BuildSpec.readme_summary_max_skipped`
defaults to `0`, so the README test summary is updated only when nothing
was skipped. On a machine with a display, category 2 runs and the
summary updates. On a headless machine, category 2 skips and the summary
is not updated. That is defensible — a summary should not be published
from an incomplete run — but it should be a known consequence rather
than a surprise.

### 10.3 Test the same code both ways

Where it is affordable, the same code path gets a stubbed test *and* a
real-Tk (withdrawn) test. This is deliberate duplication, because the two
fail in opposite directions:

- Stubs drift from real Tk behaviour and quietly stop being evidence of
  anything.
- Real Tk masks logic errors behind widget defaults and silent
  coercions, so a wrong value can still produce a passing assertion.

A discrepancy between the two runs is itself a finding, and usually a
more interesting one than either test failing alone.

### 10.4 Textual

Textual can be driven headlessly in-process, so it does not need the
three-way split — the equivalent of the withdrawn root runs everywhere,
including in CI. The stubbed-versus-real duality of section 10.3 still
applies where it is cheap. The exact headless driver API should be
confirmed against the pinned `textual` version rather than assumed.

## 11. Version 1 scope

In scope:

- read, edit and save with full validation
- lists and dicts as a tree of rows, with a field at every value
- folding with per-subtree validation badges
- add and remove elements of uniform lists and dicts
- descriptions, class docstrings, and a docstring visibility toggle
- automatic-change and filled-default visibility
- modal `edit()` with both backends

Deliberately out of scope for v1:

- **Containers whose default is empty and which have no nesting
  declaration.** There is no template for a new element and no way to
  invent one. Such members can be reordered and have elements removed,
  but not extended. The UI must say so rather than guess.
- **`DICT_VALUE_BY_KEY` members and dicts listed in
  `_unchecked_dicts`.** These have per-key rather than uniform policy.
- **Embedding.** The model is designed for it and section 8.2 designs the
  rest of it; only the modal wrapper ships first.
- **The draft file** of section 7.1.

Not a limitation but a permanent decision: no introspection of validator
constraints, so no automatically generated dropdowns or spin ranges.
Fields are edited as text and correctness comes from running the real
validators.

## 12. Rejected alternatives

- **One distribution with `[tk]` and `[textual]` extras.** Simpler
  releases and no compatibility matrix, but it cannot give a
  third-party backend author a package to depend on, and `tkinter` is
  not installable from PyPI, so a `[tk]` extra would install nothing.
- **PEP 420 namespace package.** See section 2.2.
- **One repository per package.** Correct only if a backend gets a
  separate maintainer. Today it would mean releasing the core to PyPI
  before either backend could test against it, while the core API is
  still moving.
- **Read-only constraint accessors on `config_as_json` validators.**
  Rejected because applications may define arbitrary validator
  subclasses, so this would work for known classes and silently fail for
  the rest. Running validators is correct for all of them.
- **Editing a live `Config` object.** See section 4.2.
- **A `parent` argument on the backend classes.** `TkEditor(parent=...)`
  reads well until `run_editor` has to mean "run to completion" with no
  parent and "mount and return" with one. One method with two meanings
  makes `edit()` return `None` before the user has done anything, and the
  protocol's one sentence stops being true. Section 8.2.3 instead.
- **A backend that detects the toolkit instance for itself.** Shortest for
  the application, and it rests on `tkinter._default_root` and
  `textual._context.active_app`, both private, to guess something the
  application could simply have said. Section 8.2.1.
- **A `master` argument beside the parent, with the backend creating the
  `Toplevel`.** Two arguments where one does, mutually exclusive, and it
  gives the editor window decisions — title, geometry, the close protocol,
  grab — that belong to the application. Section 8.2.2.
- **Blocking while embedded, with Tk's nested `wait_window`.** It would
  keep `run_editor` honest in one backend and is impossible in the other,
  which is the worst place for a difference between them to be. Section
  8.2.3.
