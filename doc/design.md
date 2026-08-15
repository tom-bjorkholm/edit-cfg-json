# Design of edit-cfg-json

This document records the design decisions for the folding configuration
editor built on top of
[`config-as-json`](https://pypi.org/project/config-as-json). It is a
design document, not an API reference. Where it states a fact about
`config_as_json`, the source is that project's own documentation, examples and
implementation:
[github.com/tom-bjorkholm/config_as_json](https://github.com/tom-bjorkholm/config_as_json).

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
- a very limited non-interactive backend, shipped by the core, which
  prints the model once and returns

The application supplies its `Config` object, optionally a loader
callable, optionally an input file name, an output file name, and a
mapping of per-attribute descriptions.

The editor shall have no opinion about what the filename extension shall
be for input or output files. Some applications use `.cfg`, some use `.json`,
and also other file name extensions are in use.

### 1.1 The two interactive editors are what this library is for

The Textual editor and the Tkinter editor are the product. Wherever this
document says what a feature does, it says what it does in a window or in a
terminal: which control the user presses, what appears below which member, and
what changes when the focus moves.

The non-interactive backend is neither of those and must never be described as
though it were. It offers no field to type into, no control to press, no focus
to lose and nobody to answer a question, so a printout can show what the model
holds and can never show what an editor does. What it is genuinely good for is
two things:

- exercising a feature over the core and backend API without an interactive
  backend, which is what makes a quick check, a script and an automated test
  possible on a machine with no display
- running a short sequence of editor actions and printing what they left
  behind, in one non-interactive run

It is `DumpEditor` in the core, `--ui dump` in the examples of this repository,
and the backend of the `python3 -m edit_cfg_json.dump` utility (section 8.3).
Being limited is
not a fault of it — a checker that prints a verdict and an exit code is a
useful thing to be — and it is a fault to present it as the way this editor is
seen or judged.

**When describing functionality it must be described focusing only on
interactive editors**. Describing functionality using `DumpEditor` or
`python3 -m edit_cfg_json.dump` is plain wrong.

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
  matrix is trivially one-to-one. The version of each package is in its
  `setup.py`, because `pyproject.toml` declares it `dynamic`, and the build
  refuses a build in which the three differ.
- The UI packages pin the core with a compatible-release constraint and not
  with an exact one, so a core patch release does not strand them.
- After Alpha (section 2.5) the core follows semantic versioning. This
  is a promise third-party backend authors need more than the in-house
  backends do.
- `BuildSpec.package_folders` stays unset; the three `pyproject.toml`
  files are auto-discovered.
- `additional_venv_packages` in `custom_build_tools/custom_spec.py` is unset,
  and it is redundant rather than merely unused. The step that creates `./venv`
  installs the declared dependencies of the discovered packages, minus the
  three that are internal to this repository, so `config-as-json`, `textual`
  and the rest reach the environment because the packages declare them and for
  no other reason. Checked against that step rather than assumed: a clean build
  creates the environment from nothing, and the tests that import
  `config_as_json` and drive `textual` headlessly are what would fail if it
  were not so.
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

The Alpha period is what makes it safe to publish three packages before the
public API of the core has been proven by a backend that somebody else wrote.
The two in-house backends exercise it and cannot test the one thing that
matters most about it, which is whether it is enough for a backend written
without reading the core. Section 2.3's semantic versioning promise starts when
Alpha ends, and the README and the PyPI classifiers say so plainly while it
lasts: `Development Status :: 3 - Alpha` in all three `pyproject.toml`, and
`readme_parts/alpha_status.md` in all three generated readme files.

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

**Ordinary JSON structure is a tree of rows.** A member that
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

**A nested configuration object is a node of its own.** It
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
the shape a list of nested objects needs. What a nesting kind changes is
**what a nested node offers** and never **how the tree is built**.

**One walk over the declarations of an object answers for every nesting
kind.** `LIST_ELEMENT` and `DICT_VALUE` ask nothing that `MEMBER` does not, so
a member holding several objects is editable, foldable, validated per object
and addressable by path through the same mechanism as a member holding one. The
description selectors of section 4.3 read across repeated objects for the same
reason. What does ask something of a node beyond that is a container gaining
and losing elements, which really is about what a node offers: section 4.9.

**The declarations are walked over the object and not matched as selectors.**
Turning each declaration into a selector — `('outputs', '[')` for a list of
them — is enough only while a nested object is one row. It stops being enough
once the object owns the region below it, because *ownership is asked of an
object*: `parse_converters()`, `_omit_none_from_json()` and the declaration
order of the members are all methods and attributes of an instance, and a
declaration says only which class was expected. So the configuration object
itself is asked, and it answers with the absolute path of every nested object
there really is, and with the object at it. That also tells the truth where a
`factory_function` answered with a subclass, and it distinguishes an
`OPTIONAL_MEMBER` that holds an object from one that holds none. The `'['`
selector keeps its meaning where it is still the right question, which is the
description mapping of section 4.3.

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
object on its own.** Such an object validates itself while
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
dataclass pattern — `e04_third_party_class.py` of the
[`config_as_json` examples](https://github.com/tom-bjorkholm/config_as_json/tree/master/example/src/example)
is one — do expose real types through `dataclasses.fields()`. Support both; do
not assume annotations exist.

### 4.2 Edit buffer

The buffer holds JSON-compatible values at the leaves, typed as
`config_as_json.JsonType`. The user edits what will actually land in the
file — an enum is edited as its member name.

The buffer is however not JSON text. For example: in the edit field no
quotation marks are shown around a string. The edit field will show
the digits `1` and `0` as`10` for both the string `'10'` and the
integer `10`. The edit buffer needs to hold additional metadata/flags
with type information for each leaf.

**That type information is shown to the user**, as a line of explanatory text
below the member, in the same place and under the same toggle as everything
else explanatory. Section 4.3 is where it says what. It is not shown as a label
beside the field, because it is text about the value and not part of it, and
because a narrow window would then squeeze the field for it. There is still no
decision to allow
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
the first time anything in it was validated.

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
change would report a failure that is not one yet. It is
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

  **Which of the two a nested node shows is decided by its fold**: the whole
  docstring while the node is open, the summary while it is folded, and both of
  them under the explain toggle of section 4.4 like every
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
  accepts.

  Where it holds anything else, what is said is **what kind of value it is** —
  text, a whole number, a number, or true or false — read from the value the
  member held when the file was last agreed with, which section 4.2 already
  keeps as the only type information there is. A member that may be left out of
  the file says that as well, from the `_omit_none_from_json()` of the class
  that owns it, which section 4.1 lists as a source and nothing else uses.
  It matters most where the application described nothing: without it, a
  program that has been told a class and no description mapping shows its
  members with nothing under them at all, when the editor does know something
  about each of them.

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

**A selector says `'['` at each step it has to**, to the bottom of the shape
this library is written for: a list of objects each holding a dict of more of
them is reached by `('outputs', '[', 'parts', '[',
'width')`, one line for that member of every object at any index and any key.
It crosses two nesting boundaries on the way, which is the divergence the
paragraph above records, and it is what makes a repeated object cost an
application nothing extra to explain. A description that names every step still
wins where both address one node, so one element of a repeated object can be
singled out while every other keeps the general text.

One deliberate divergence from `serialize_converters()`: description
paths **cross nesting boundaries**. Converters stop at child-owned
subtrees because each nested config serializes itself; descriptions have
no such constraint, and the application should not have to know where the
nesting boundaries fall. A second divergence: overlapping selectors
resolve in favour of the more specific one rather than raising. A wrong
description is a cosmetic bug; refusing to open the editor over one is
not.

**Which of two selectors is the more specific one** has to be said, because two
selectors of the same length can both address one member and be equally short.
A step that names a key is more specific than the
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

What the toggle covers:

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
name reaches its command palette. The two answers differ because the two
toolkits offer an action differently, and the question each of them answers is
the same one.

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
left until an application asks for it; what is not left is the
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
  space it asks for in the order they were packed, so packing it last would lay
  the verdict, the saving and the buttons below the bottom edge of any window
  too short for everything, where no scrolling could reach them. It is created
  second, so that the widgets are still created in the order they are read in.
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
it, so that neither of them works out for itself what folding hides. What can
be folded is **a node that holds rows** and not "a container", which is what
makes a nested configuration object one of them as well.

**Folding a node also asks every configuration object at or inside it about
itself**, which is section 6.2 and the one thing folding does beyond deciding
what is on the screen. Opening one asks as well: the answer is the same
question either way, and changing how much of a node is shown is the moment the
user is looking at it.

**A region and not the one node that was folded.** A list and a dict have
nothing to say about themselves, so asking only the node that was folded would
ask nothing at all where the member holds several configuration objects, which
is exactly the shape section 4.1 says a real configuration has. The question a
fold answers is not *what is this node* but *what is being hidden*, and what
such a container hides is every object in it. So it asks all of them, and what
it finds is put on their rows, where it is read as soon as the container is
opened again. A container of plain values is asked nothing, because there is
nothing in it that could be asked.

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

**A backend that shows the model once asks a third thing**, and it is not the
toggle: `open_all` opens every container, because the question the toggle
answers — what does the next press do — belongs to a session that goes on. It
takes `no_more_folding`, which also stops a container that appears later from
being folded away, and such a program is what needs it: it validates the buffer
before it shows it, a pass can create a container (section 4.8), and a new one
that is large is folded the way the editor decides every container. That would
fold something away after the one moment at which anything is shown. Asked for
once it stays on, because there is no later moment to ask again in either. It is
`--unfold` of section 8.3.3, and what it is for is the whole listing of a
configuration: every value, and the explanation each node is shown with.
Folding by hand still works afterwards, because a container the user folded is
what the user asked for and nothing about this says otherwise.

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
that section 4.9 needs when the user adds and removes elements, so it is built
once and here.

### 4.9 How many things a member holds

A member is a list or a dict because **how many** of them there are is a
decision of whoever configures the application. An editor that could change
every one of them and add none would be refusing the decision that the shape of
the member exists to allow, so a container can be given an element, one of its
elements can be taken out, and an element of a list can change places with a
neighbour.

**A new element is copied and never invented**, and there are exactly two
places it can be copied from, both of them the application's. Where the class
declares that every element of a list or every value of a dict is a
configuration object, the declaration names the class and a new element is one
object of it holding the values it declares — which works for a container that
is *empty*, because what an element is comes from the declaration and not from
what the member happens to hold. Where it declares no such thing, the values
the class declares for the member itself are the pattern: the first element of
them, and failing that the first element the member holds now.

A member with neither is the one case section 11 puts permanently out of scope,
and the reason is not that it is difficult: only the application knows what an
element of its own list looks like, and a member it never gave one for has
never said. Such a member says so and offers removing and moving. The fallback
to what the member holds now earns its place: a member the class declares
nothing for becomes extendable as soon as a file has put something in it, which
is the ordinary way such a list gets its first element.

**What cannot be done is said and not left to be discovered.** Three kinds of
dict cannot be given an entry, for three different reasons, and each of them
says which below its own row:

- an ordinary dict member, because `config_as_json` checks such a member
  against the keys its class declares — `Config.check_dict_parse` does it while
  parsing — so a dict that gained or lost one would be refused by the
  configuration class itself. Confirmed against the implementation of
  `config_as_json`, and it is why "uniform dicts" in section 11 means the
  declared ones and not every dict.
- a member of `_unchecked_dicts`, whose key policy the application defines with
  validators of its own. Out of v1 scope.
- a `DICT_VALUE_BY_KEY` member, where one named key holds an object and the
  others hold ordinary values. Out of v1 scope.

That sentence is **explanation and not a refusal to act on**: it says what this
member is, in the same way as the line saying what kind of value a member
holds, so it is `Emphasis.MUTED`, it sits below the member with the
description, and the toggle of section 4.4 covers it. Nothing is
half-supported: a node that cannot be given an element gets no control at all
rather than one that refuses every press.

**A declared member holding no configuration object is grown by being given
one**, which is what section 4.1 already called adding, and cleared by being
put back to holding none. Clearing is offered only where the class writes
`null` for the member: one that lists it in `_omit_none_from_json()` leaves it
out of the file altogether and it then has no row, so a member the editor had
cleared could never be given an object again. That also means such a member
cannot be given its first object through the editor at all, which is a
consequence of section 4.1's decision that an omitted member has no row rather
than a decision of this section.

**Where an object is added, an object is made.** The tree finds the nested
configuration objects by walking the real objects (section 4.1), so an element
that existed only in the edit buffer would be shown as the dictionary it
serializes to, with the member order of nobody, the parse converters of nobody
and no badge of its own — and nothing would ever ask it whether it is a
configuration on its own. So the model's own configuration object, which is
the copy the caller never sees, gains the object as the buffer gains its
values. Principle 5 of section 3 is untouched: it is the editor's copy that is
changed and never the caller's.

**What the editor holds about a node is held under the path of that node**, and
an element of a list is addressed by where it is, so a removal or a move takes
all of it along: what each row is compared against, which containers are
folded, and what each object said about itself. Without that, removing the
first element of a list would leave every element after it comparing itself
with the element that used to be there, and would report every one of them as
edited by a user who touched none of them.

**A change of the elements is not a validation pass**, and the rows say so. The
rows are built again after both, and only one of the two is a validator's work,
so a row that a validation pass created is marked as one a validator wrote and
a row the user added is not. What the application makes of what was added is
the ordinary verdict: the editor copies what the class declares, and a class
that refuses two elements with one name refuses the copy until it is given a
name of its own.

**Where the new entry of a dict is named is the user**, because nothing else
knows. Each backend asks in the way its own toolkit asks a question — a dialog
in Tk, a modal screen in Textual — and a key the dict already holds is asked
about again rather than allowed to take the place of what is there. A list is
never asked, because an element of a list is addressed by where it is.

**The controls sit at the end of the line of the node**, unlike the fold
control, which keeps a column clear on every row. There is no alignment to
keep, so a node that offers none of them costs the values no width at all, and
that is what makes four controls on one row affordable.

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
control, which they cannot get through `ConfigFactory` at all. There is no
parameter for the hook that reports automatic changes, because
`config_as_json` 1.5 makes that hook something every configuration object has
(section 5.3), and what a loader is never asked for is one parameter less to
explain.

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
JSON.

**Reading a file and the declared defaults are what need the loader**, which
is what makes it affordable. Section 6.1 does not construct the class at all,
so an application that has a loader needs it for those two and for nothing
else, and one that has no loader is no worse off anywhere else. The second of
the two is section 4.9's: the values a class declares are what a new element
of an ordinary list is copied from, and a loader is asked for
them with no JSON source, which is exactly what the paragraph below says a
loader answers. A class the editor cannot construct answers with nothing and
loses that one offer.

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
implementation of `config_as_json`: the parameter belongs to
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
  of the two it was. A field that is being *edited* reports the enum case for
  itself (section 4.2), and this one is deliberately left as it is: a file that
  cannot be opened is not a field the user can correct, and reading the
  diagnostics of the load is exactly what they have to do.
- **values a validator refuses** → the file cannot be opened. `parse_json()`
  ends with `validate()`, so there is no valid object to build a model from.
  The reason it is a refusal rather than an editor opened on the file's own
  values: a member validator returns the value that is stored back into the
  member, so a load that stopped part way through leaves it unknown which values
  were already rewritten and which were not, and there is then nothing honest to
  show. The user is told to correct the file in a text editor first.
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
object that is really being edited. Computing the flag from the keys of the file
instead would claim that a renamed member had been filled in from a default,
which is untrue of it.

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

**Nothing is opted into and nothing is passed.** `Config.__init__` creates a
hook when the application names none, keeps by reference the one it is given,
and publishes both through `auto_change_hook()`. So a class that declares
`auto_ch_hook` and hands it on is reported on exactly as fully as the ordinary
three-keyword constructor shape that does not, the editor passes no hook
anywhere, and `ConfigLoader` has no parameter for one (section 5.1). Keeping it
by reference is what `config-as-json` 1.5 promises and is why the editor needs
no rule about reading the hook before anything parses the file again: a copy of
the configuration carries a copy of the hook, so a later parse cannot disturb
what the load recorded.

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

**The pass is asked for and never done for the user.** Tk has a Validate
button and Textual a key, because a user who is halfway through typing a value
has not asked anything, and an editor that answered a question nobody put would
be reporting a mistake that is not one yet. The non-interactive backend of
section 1.1 has no later moment in which to be asked, so it validates once
before it prints — which is a consequence of printing once and returning, and
not a second policy about when to validate.

**The class is not constructed, and it does not have to be.** Constructing it
would add nothing: the declaring of the members is the whole
of what a constructor does before `parse_json`, and a copy has that already.
Even the derived loader of section 5.1 never gives the text to a constructor,
because the load policy belongs to `parse_json` and not to `__init__`.

Copying instead of constructing is what makes two kinds of class editable at
all: one whose constructor needs an argument this library knows
nothing about, and one with no JSON text parameter at all. Both are validated
and saved like any other, and the loader an application supplies is then for
reading a file and for nothing else. Copying is also what keeps a session on
one class where a loader would choose another (section 5.1), and it is what
gives the probe of section 6.3 the object it needs.

### 6.2 Subtree validation, and why folding is the natural trigger

A nested config subtree can be validated **in isolation**, by applying that
subtree's JSON to the nested object itself.

**The object is copied and not constructed**, for the same reason as in
section 6.1: the object is there to be copied, so a class whose constructor
needs an argument this library knows nothing about is asked about itself exactly
as well as any other, a `factory_function` that answered with a subclass is
asked as the subclass it really is, and there is one way of applying a buffer to
an object rather than two.

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
and this one only by an edit inside the object it is about.

**What the object refused is kept with the state and never apart from it.**
Keeping the state and throwing the sentences away would leave a folded object
saying that something was wrong with nothing saying what, and the user asking a
second question, about the whole configuration, to be told something they had
just been told half of. The two are one answer: they are found by one pass, they
are true for exactly as long as each other, and an edit inside the object
takes both back together. That third lifetime is why they are the buffer's and
are stamped onto the rows rather than being carried by them, beside the fold
state and for the same reason: the rows are built again after every validation
pass, and an answer outlives the rows it was given about.

The sentence is shown where section 6.5 puts every other refusal, which is at
the node it is about — a member of the object, or the object itself where it
is about no member of it. A folded object therefore shows the state and not
the sentence, because the member the sentence is about is one of the rows that
folding hid, and opening the object is what shows it.

**A list or a dict of such objects carries the same state, about them.** It is
no configuration and can say nothing about itself, so the words differ: it is
*valid inside* and *refused inside*, refused as soon as one object in it is,
valid once every one of them has been asked and accepted, and unasked while
any of them is unasked and none is refused. That row is the only one a folded
container leaves on the screen, and without it folding a member would hide the
one thing the user has to act on and leave nothing at all in its place. A user
who folds a member to get it out of the way is not asking to be told that
everything in it is fine, and is very much asking to be told that it is not.

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

**The candidate this needs cannot be held the ordinary way.**
`Config.parse_json()` ends in `validate()`, which
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

**The method is left out on the object and not on a class.** It is one
attribute of one copy rather than a throwaway subclass, for two reasons.
It works for a class the editor cannot construct, which
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
be told where to look rather than have to go looking.

**What is refused is addressed by a path and not by a name**,
because a value inside a list or a dict is a node of its own and two of
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

One member can have three things wrong with it, and they are not the same
thing: its text may mean no value of it at all (section 4.2), the application
may have refused the value it holds, or the nested configuration object that
owns it may have refused it when it was asked about itself (section 6.2).
**The first is preferred when more than one is there**, because a value that
does not exist yet is what has to be corrected first, and the verdict comes
before what one object said because a pass over the whole buffer is the more
recent of the two whenever both are there. They also live for three different
lengths of time, which is the reason they are kept apart rather than merged:
the first stays true until that member is edited again, the second is dropped
as soon as anything in the buffer changes, and the third as soon as anything
inside that one object does.

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
- **`Config.write()` does validate.** Confirmed against the implementation of
  `config_as_json`: `write()` calls `as_json_string()`, whose first
  statement is `self.validate(stderr_file=stderr_file)`, and it opens the
  destination only after the text exists. So the editor's own gate is belt
  and braces rather than the only guard, and a configuration that `write()`
  refuses leaves the file on disk exactly as it was.
- A destination that cannot be written — a folder that does not exist, a file
  that may not be written to — is a message and not a crash, for the same
  reason: the alternative costs the user the whole session.
- **What the destination held is kept, and overwriting it is asked about.**
  Section 7.3.
- **Where the application said how it loads, that is asked once more before
  anything is written**, with the very text the file would hold. It is the one
  question a validation pass cannot answer: the pass applies the buffer to the
  class of the session (section 6.1), and a loader that chooses its class by
  looking at the JSON may read the same text back as another class altogether. A
  file the loader refuses, and one it would read as a class the session is not
  about, are both a refused save with a message; `isinstance` is what the second
  of those asks, so a loader that answers with a subclass is answering with the
  class. An application that supplied no loader is asked nothing, and the class
  it edits is the class it gets.

### 7.1 Draft file (room left, not implemented in v1)

"Invalid cannot be saved" means a user with a long, still-invalid editing
session has no way out but to discard it. The escape hatch that preserves
the rule is an editor-owned **draft file** holding the raw JSON buffer —
explicitly not a `config.write()`, explicitly not loadable by the
application, reopened by the editor on next start. Not a v1 priority, but
the model must not be designed in a way that rules it out.

### 7.2 Closing with something unsaved

Closing writes nothing (section 9.1: quitting is the cancel of this design), so
a session closed with something in the buffer that has not reached the file
loses it. The editor is the only thing that knows there is anything to lose, so
it asks first.

**Whether the user is asked, and what they are asked, belongs to the core.** It
is a decision that depends on the state of the model, which is section 4.5's
rule, and it is the same rule that already places the verdict line, the saving
line and the marks there: two user interfaces of one application, one of which
asked and one of which did not, would be worse than either behaviour. **How the
question is put belongs to each backend**, because that is where the toolkits
differ — Tk has a message box and Textual has a modal screen — and it is the
same split as everywhere else.

It is one function and not two. `close_question` answers with the question, and
with nothing at all when there is nothing to ask about, exactly as `load_text`
is empty when the load has nothing to say. Closing then reads as one sentence
in both backends: ask where there is a question, and close where there is not
or where the answer was to discard.

**What it asks is `dirty`**, which is already "the buffer holds something worth
saving": a save moves the values the buffer is compared with (section 4.2), so
a session that saved and typed nothing since is not asked, and a save the
application refused leaves the buffer dirty and is.

**Every way out asks, including the one that is not a widget of the editor.**
The button, the key of the quit action and the close button of the window all
go through one method of the backend, because a way out that dropped the
changes without a word would be the one thing an editor must not do, and one
method for all of them is what keeps any one of them from becoming that. The
window is only ever the one the backend created: the editor never touches a
window it did not create, which is section 8.2.2 holding here as well.

**Both backends offer the answer that keeps the changes first**, as the answer
the dialog opens on and as the control the screen puts the focus on, because a
user who answers without reading should keep what they have. Leaving the
question — the cancel key of section 9.1 — is the same as keeping them.

**The non-interactive backend of section 1.1 is asked nothing.** There is no
session for a user to close and nobody to answer, so `DumpEditor` consults
none of this; where the core is asked, such a backend's answer is to discard,
which is the only answer it ever had. Closing is therefore one of the
behaviours that exist only in a window or a terminal, and one of the plainest
reasons a printout is no measure of this editor.

**Two answers and not three.** Saving on the way out was rejected: it would
have to cope with a save the application refuses, with no destination chosen
yet, and with the Save-as question opening from inside a confirmation, and all
three of those belong to saving rather than to closing. The user presses Save
and then closes, which is one keystroke more and no new state.

**No `Settings` attribute.** Whether there is anything unsaved is something the
editor knows for itself, and section 9.6 keeps `Settings` for what only the
application knows. Whether *overwriting* a file is confirmed is a different
question, because only the application knows how its files are looked after,
and that one is left where section 9.6 leaves it.

### 7.3 The file that a save writes over

A save writes over whatever the destination holds, and what it holds is a
configuration somebody wrote. It may be the one this session read a minute ago,
and it may be one another person wrote on another day; nothing the editor can
look at tells those apart. So the file is **kept** before it is overwritten,
and the user is **asked** before it happens. Both are the application's
decision, for the reason section 9.6 gives about `Settings` as a whole: how its
own configuration files are looked after is something an application knows and
the editor cannot find out.

**It is once per destination per session, and that is what makes it about the
user's own work.** From the second save onwards the file being written over is
the first save of the same session: keeping it would push the configuration
that was really there one number further from being found, and asking about it
would be asking the user about something they did a minute ago. The model
therefore holds every destination it has written, and Save-as onto some other
existing file is asked about again because that is another file.

**Kept by renaming, not by copying**, which is what the file being kept *is*
rather than a second reading of it, and which leaves the previous content whole
under one name or the other whatever happens next. The name is the destination
plus `backup_suffix`, added to the whole name rather than put in place of the
extension: `xx.cfg` becomes `xx.cfg.bak`, and one attribute then expresses
`.old` and `~` as well. `backup_count` above one numbers them from `_1`, which
is the file overwritten last, and each save moves every one of them one number
further back until the oldest falls off the end. One is not numbered, because a
number would say that there are others when there are not.

**Where it happens in a save is the whole of what can go wrong.** It is after
the validation and after the loader has been asked, and immediately before the
write. So a save that is refused for any reason keeps nothing — a refused save
that had pushed the kept files along would cost the user the oldest of them for
nothing — and a save that kept the previous content and then could not write
says where that content is, on the line below its own message. A save that
cannot keep it writes nothing at all: overwriting cannot be undone, so the
moment at which that is found is the last moment at which anything can be done
about it. A destination that is not a regular file, a folder being the case
that arises, is left to the write to refuse in its own words rather than
renamed out of the user's way.

**Whether the user is asked belongs to the core and how they are asked to each
backend**, which is exactly section 7.2's split and for the same reason.
`overwrite_question` answers with the question and with nothing at all when
there is nothing to ask, `EditModel.overwritten_file` is the file it is about,
and each backend puts it in a dialog or on a modal screen with the answer that
leaves the file alone offered first. The Tk file dialog is told **not** to ask
this itself, although it offers to: a question that one backend put and the
other did not would be the one thing the core owning the question exists to
prevent.

**A backend that prints once and returns is asked nothing**, as it is asked
nothing before closing, and it writes what it was asked to write. What it does
*not* skip is keeping the previous content, because that is the model's work
and not a question: a script that saves has exactly the same reason to still
have the configuration that was there.

## 8. The UI backend contract

The editor is embeddable in an application that already runs its own Textual
or Tk event loop. That cost nothing because it was decided before anything was
built, and it would have been a rewrite otherwise; section 8.2.5 is what it
really came to.

- The model is a standalone object. It does no I/O in its constructor
  and owns no event loop.
- `edit()` is a thin convenience wrapper: build the model with
  `editor_model()`, run a backend to completion, return the result.
- The backend `Protocol` is phrased against the **model**, never against
  `edit()`. Embedding is then additive: the mounting entry point of a backend
  package builds the model with the same `editor_model()` and shows it in a
  widget of the application's.

```python
def editor_model(config: Config, *,
                 descriptions: Optional[Descriptions] = None,
                 in_file: Optional[PathOrStr] = None,
                 loader: Optional[ConfigLoader] = None,
                 out_file: Optional[PathOrStr] = None,
                 policy: LoadPolicy = DEFAULT_POLICY,
                 settings: SettingsSource = Settings(),
                 stderr_file: TextIO = sys.stderr) -> EditModel:


def edit(config: Config, backend: EditorBackend, *,
         descriptions: Optional[Descriptions] = None,
         in_file: Optional[PathOrStr] = None,
         loader: Optional[ConfigLoader] = None,
         out_file: Optional[PathOrStr] = None,
         policy: LoadPolicy = DEFAULT_POLICY,
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

`descriptions` is an optional keyword and not a required positional argument.
An application that describes none of its members
is a perfectly good caller: the docstring of its configuration class still
labels the object, and principle 4 of section 3 says that what the editor
cannot be told it does without. Requiring the argument would also make every
call site pass an empty mapping to say nothing. The same
reasoning makes `EditModel`'s arguments after the load
report keyword-only: each of them says one independent thing about the session,
and none of them is worth passing by position.

The `backend` argument has to be there: the core never imports a user interface
library, so it cannot name one. Each backend package therefore also exports an
`edit` of its own that supplies itself and forwards everything else, which is
the shorter door
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
a third-party backend in the wild. The programs of section 8.3 are not
that launcher: each of them supplies its own backend, so none of them has
anything to discover. An `edit-cfg-json` that chose an editor for the machine
it was run on would be that launcher, and the name is kept free for it.

### 8.2 Embedding in an application that already runs a UI

An application that already runs Tk or Textual mounts the editor in a widget
of its own and goes on running its own event loop. It is implemented, and it
was **designed here before it was built**, because two of its questions have
answers that are cheaper to give early than to retrofit: which toolkit
instance the editor attaches to, and where in an existing window it is placed.
What embedding asked of the design that was already here is recorded in
section 8.2.5, and it turned out to be three rules and nothing else;
everything the rest of this section names is an addition.

The first question is the same in both toolkits and so is its answer. The
second was answered twice: step 18 built it, step 18B rebuilt it around what
an application actually writes, and section 8.2.2 records both the answer and
the reversal, because a design document that quietly replaced one is worth
less than one that says which way it went and why.

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
section 8.2.3, and says with it where the editor is to go.

#### 8.2.2 Where in an existing window is it placed?

**In the widget the application names, and the editor destroys only what it
created.** What differs between the two toolkits is what "a window of its own"
even is, so each of them answers the second half of the question in its own
way: Tk is told which of the two the application wants, and Textual has a
class for each.

- **Tk: `parent` or `area`, and never both.** `area` is a widget the editor
  fills — it builds one frame inside it and destroys that frame again.
  `parent` is a widget the editor opens a window *over* — it creates the
  `tkinter.Toplevel` itself, names it after the configuration class, makes it
  transient for the application's window, routes its close button through
  `close`, and destroys it when the session ends. Neither of the two given, or
  both, is a `ValueError`: an application with no Tk of its own uses
  `run_editor`, and one that named both has answered one question twice.
- **Textual: `EditorPanel` or `EditorScreen`.** A widget and a screen are
  different Textual types, so which one it is *is* the class, and there is
  nothing to be told. Section 8.2.4.

**This is a reversal, and it is recorded as one.** Until step 18B the editor
took one widget and filled it, and an application that wanted a window of its
own created the `Toplevel` itself and passed it; section 12 listed the
alternative as rejected, on the grounds that two mutually exclusive arguments
do the work of one and that the title, the geometry, the close protocol and the
grab belong to the application. What that reasoning missed is that **every**
application that wants a window of its own then writes those same five lines,
and writes them against a toolkit rather than against this library — so the
argument that was saved cost every caller a paragraph. `wizard_tk_bridge` had
already answered the same question the other way, with `parent`, `area` and
`modal`, and an application that embeds both should not have to learn two
shapes for one idea. The five lines are the editor's now, and an application
that really wants its own decisions about that window can still pass `area`
after making one.

**`modal` is a third thing the application says**, and it is `True` by default.
It is a Tk word and a Tk argument: the editor asks Tk to hold the events of the
application for the window or the frame it built, and gives the grab back when
it closes. Textual has no equivalent and needs none — a pushed screen already
has the terminal, and a mounted panel already does not. A grab is asked for at
the moment the editor is built, which is before the window it made has been
mapped, and whether Tk allows that is a platform question: Aqua does, and X11
refuses a grab for a window that is not viewable. An editor that opened without
its grab is worth more than one that did not open, so a refused grab is a
non-modal editor rather than an error — which means an application that must
be held on every platform makes its own window, maps it, and passes it as
`area`.

The remaining rejected alternatives are in section 12.

#### 8.2.3 It cannot be `run_editor`, so it is a second entry point

`EditorBackend.run_editor` promises to run until the user is done. An
embedded editor cannot keep that promise. Tk could fake it with a nested
`wait_window`, but Textual has no way to nest a second loop at all, and an
editor mounted in a panel of the application's window should not suspend
the application's call stack in either toolkit.

Embedding is therefore a **separate, non-blocking entry point per backend
package**, additive to the protocol rather than a change to it. Each of them
is *one call*, and it says the same things about a session that `edit()` says,
because an application should not have to learn a second vocabulary to put the
editor somewhere else:

```python
# edit_cfg_json_tk
class TkEditorPanel:
    def __init__(self, config: Config, *,
                 parent: Optional[tkinter.Misc] = None,
                 area: Optional[tkinter.Misc] = None, modal: bool = True,
                 on_close: Optional[Callable[[], None]] = None,
                 descriptions: Optional[Descriptions] = None,
                 in_file: Optional[PathOrStr] = None,
                 loader: Optional[ConfigLoader] = None,
                 out_file: Optional[PathOrStr] = None,
                 policy: LoadPolicy = DEFAULT_POLICY,
                 settings: SettingsSource = Settings(),
                 stderr_file: TextIO = sys.stderr) -> None: ...
    def close(self, ask_about_unsaved: bool = True) -> None: ...
    @property
    def model(self) -> EditModel: ...
    @property
    def saved_config(self) -> Optional[Config]: ...

# edit_cfg_json_textual — the seven session keywords again, and no place
class EditorPanel(Widget):        # mounted into an area
    def __init__(self, config: Config, *,
                 on_close: Optional[Callable[[], None]] = None,
                 ...) -> None: ...
    # close, model and saved_config as above

class EditorScreen(Screen):       # pushed as a screen of its own
    def __init__(self, config: Config, *,
                 on_close: Optional[Callable[[], None]] = None,
                 ...) -> None: ...
    @property
    def panel(self) -> EditorPanel: ...
```

The seven after `on_close` are the keywords of `edit()` less the backend, and
each of the three classes spells them out rather than taking a bundle: a
reader of one signature sees the whole of it, and a type checker sees every
name. The `...` above is this document being brief and is no part of the code.

**The seven keywords are one function, and it is in the core.**
`edit_cfg_json.editor_model` is the first half of `edit()` — read the input
file, build the model — and `edit()` is now that call plus `run_editor`.
Without it the two backend packages would each be reimplementing the loading
rules of section 5 against a `load_config` and an `EditModel` constructor, and
the three ways of opening the editor would drift apart in what an `out_file`
or a `policy` means. It is public rather than internal because an application
that writes a backend of its own wants the same half.

`on_close` is how the application learns the session ended; the outcome is
`saved_config`, which the panel and the screen offer beside the `model` it
comes from, so that an application need not hold a model it did not build.
`edit()` gains no argument: an embedded editor has no moment at which it can
return what was saved, so the wrapper that exists to return it has nothing to
offer here.

**`close` is the application's way out, and it says whether the user is
asked.** The editor's own Close and its quit key are that same call with the
default, so the question of section 7.2 is put in the same words and answered
in the same dialog whichever of the three ended the session. Whether it is put
at all is the *application's* to decide and not the editor's, because only the
application knows what it is closing the editor for: a menu entry that closes
the editor should ask, and an application that is already putting a question
of its own to the user has one question too many. That is the same line
section 9.6 draws — the editor knows for itself whether anything is unsaved,
and the application knows what else it is about to ask.

**It answers with nothing, and `on_close` is the whole answer.** A Tk panel
could say synchronously whether it really closed, and a Textual one could not:
its question is a modal screen with a callback, so there is no moment at which
`close` could know. One answer that both backends can give is worth more than
a return value in one of them.

**Closing again once the session has ended does nothing**, so an application
need not keep track of whether the user has closed the editor already.

**Only what the editor created is destroyed.** The Tk panel destroys the frame
it built inside the given `area`, or the window it opened over the given
`parent`; the Textual panel removes itself, and the Textual screen pops itself
off the application. What the application had on the screen beside the editor
is untouched, which is section 8.2.2 acted on rather than only stated.

**A screen pops itself, and that is not the same decision as the rest of this
section.** Everywhere else the editor destroys what it created and leaves the
application to decide what happens next; a screen it pushed is what it created,
and an application that had to pop it would be left with the editor's own empty
screen on top of its own for as long as it took to be told. The application's
screen is therefore back on top by the time `on_close` runs, which is what
makes reading `saved_config` from there the same in both shapes. A screen that
is the *only* screen — which is what `EditorApp` shows — is not popped, because
there is nothing underneath it.

#### 8.2.4 What Textual has to be split into

The Tk backend already builds below an arbitrary parent widget, so its
panel is a wrapper. The Textual backend is an `App`, and five things live
at App level that an embedded editor cannot have:

| On `EditorApp` | Why it cannot stay there |
| --- | --- |
| `CSS` | Textual ignores `CSS` on a widget and says so; a widget uses `DEFAULT_CSS`. |
| priority bindings on `self._bindings` | App-level priority bindings fire wherever the focus is. Verified against `App._check_bindings` in 8.2.8: the priority pass walks the whole binding chain, so a priority binding on a **widget** still beats the focused `Input`, and only while the focus is inside the editor. That is what embedding wants. |
| `self.title` | It is the application's window title. |
| `get_system_commands` | `COMMANDS` exists on `App` and `Screen`, not on `Widget`. An embedded widget cannot offer palette entries; an embedded screen can. |
| `action_quit` | It ends the application. |

So `EditorApp` splits three ways: `ModelPanel(Widget)` holds the whole
body with its `DEFAULT_CSS` and its instance bindings, `ModelScreen`
adds the header, the footer and the palette entries, and `EditorApp`
composes the screen. One body, so the two backends cannot drift and the
CSS and the bindings exist once. The model title moves from `App.title`
into a label of the panel, which is what the Tk backend already does; the
application title becomes the name of the configuration class, which is what
`TkEditor` puts in the title bar of the window it owns.

**The two the application mounts take a configuration and not a model**, and
that is one subclass each: `EditorPanel(ModelPanel)` and
`EditorScreen(ModelScreen)` call `editor_model` on the seven keywords of
section 8.2.3 and hand the model up. The pair with the model stays because
`EditorApp` has one already — it was given a model by `run_editor`, which is
what `EditorBackend` promises — and because a backend of somebody else's could
want the same. Subclassing is what keeps that from being two constructors with
a flag: nothing in the body knows which of the two doors it was reached
through, and the public names are the short ones. Textual matches a type
selector against every class name in the hierarchy, so the sheet `ModelPanel`
declares for itself reaches the subclass too, which is the one thing this
split had to be true of.

Three things about the split had to be learnt from Textual rather than from a
design, and are recorded because none of them is obvious:

- **A screen offers palette entries through `COMMANDS` and not through
  `get_system_commands`.** That method is `App`'s alone, so the entries become
  a `Provider` of the screen, which asks the panel for them. Asking rather
  than holding a table is what keeps the two entries whose name says what the
  next press will do — Explain and Fold all — true at the moment the palette
  is opened.
- **A widget styles *itself* by its type name.** Textual scopes the style
  sheet a widget declares to that widget and what is inside it, so a class
  selector in it reaches the inside and never the widget the sheet belongs to.
  The sheets therefore leave a mark where a class name belongs and each widget
  fills in its own, which is what `ModalScreen` does with its own name too.
- **The question screens carry their own sheet.** They are screens of the
  application and never a part of the editor widget, so a sheet the panel
  declared could not reach them and an application that mounted the editor
  would have none of the editor's at all.

**What the split costs an application that shows the editor and nothing else
is one thing, and it is deliberate.** The footer names the actions of the
editor while the focus is inside the editor, because that is where the
bindings now are. That is the same rule embedding wants, and Textual focuses
the first focusable widget of a screen, which in this editor is inside the
panel.

#### 8.2.5 What embedding asks of the design that is here

Two rules, and both of them hold for a modal editor as well, so nothing has to
change meaning when the panel is added:

- **`EditorBackend` promises a modal editor**, and it does not promise that an
  application can mount the backend as a widget. Mounting is the separate entry
  point of section 8.2.3, and the docstring that is published in
  `doc/edit-cfg-json_api.md` says exactly that.
- **`EditorWidgets` is told what closing does** rather than deriving it
  from `parent.winfo_toplevel()`. The default is what `TkEditor` needs, and
  stating the rule of section 8.2.2 where the editor acts on it is what makes
  the panel an addition rather than a rewrite.

Everything else is genuinely additive: the public surface of both backend
packages is `TkEditor`, `TextualEditor` and `edit`, none of them changes
meaning under embedding, and every name section 8.2.3 introduces is new. That
is what section 8's decision to phrase the protocol against the model bought.

**Step 18B added a third rule, and it is about the core rather than about a
backend.** `edit()` was the only place that knew how to turn the seven
keywords of a session into a model, and an entry point that could not run to
completion could not reach it. Splitting `editor_model` out is what let the
mounting entry points take the same keywords rather than a model the
application had to build; `edit()` is that call plus `run_editor` and means
exactly what it meant before. Nothing else in the core moved, which is what
section 8.2.5 was written to check.

#### 8.2.6 A Tk variable names its parent

`tkinter.StringVar` built without a `master` is created in the **first**
Tcl interpreter of the process, not in the one its field belongs to —
`tkinter.Variable.__init__` falls back to `_get_default_root`. With an
application's root already present, every field's variable would be
created in the application's interpreter while its `Entry` lived in the
editor's, so the field would show nothing and the callback that writes it
into the model would never run. The fields therefore name their parent. That
is as true of a window the editor owns as of one it shares, so it is not a
rule that waits for embedding.

#### 8.2.7 What the Tk keys are bound on

**A bind tag of the editor's own**, put on the widget the editor was built
below and on every widget it created inside it. That is the answer to a
question this document left open while the keys were bound on the toplevel,
which is right for a window the editor owns and wrong for one it shares: the
editor would claim keys across the whole application window.

It is one rule for both ways of running the editor rather than two, which is
what makes it worth the machinery: **the keys of the editor reach the widget it
was given and everything inside it, and nothing else.** A backend that owns its
window is given the window, so it keeps exactly the keys it always had; a panel
is given the frame it built, so it claims nothing of the application. The
alternatives — binding on each field, or making the panel focusable — were
rejected because the first leaves a key dead the moment the focus is on a
button and the second puts the editor in the application's tab order, which is
a decision about the application's window that section 8.2.2 gives to the
application.

**The mouse wheel is bound the same way, and that is the same answer.** A
wheel event goes to the widget under the pointer, which is usually a field or
a label inside the body rather than the canvas that scrolls, so binding the
canvas alone would leave the wheel working over the empty parts and nowhere
else.

**Where the tag goes in each list is `Settings.priority_keys`.** Tk offers the
tags of a widget in the order they are in and a handler that answers `break`
stops the walk, so the tag first is the editor before the widget with the
focus, and the tag last is the editor after it. Section 9.1.

**The tag is given up when the editor closes**, because a bind tag is a name
in the Tcl interpreter and outlives the widgets that carried it: an editor
that had been taken off a window would otherwise leave its callbacks, and the
model they hold, for as long as the application runs.

Textual needed none of this, because a widget's bindings already dispatch only
from the focused widget upwards.

#### 8.2.7.1 The two questions that are answered with a no

- **The core does not name the mounting contract.** A `Protocol` for it would
  let a third-party backend implement the same shape, as `EditorBackend` does
  for the modal one, and it is additive whenever it is added. There are now
  three implementations and they still do not share a shape: the Tk one is told
  a parent or an area and whether to be modal, and the two Textual ones are a
  widget the application mounts where it likes and a screen it pushes, neither
  of which ever hears of a parent. A protocol over things that differ in what
  they are told would be a protocol over one of them with the others written
  down beside it. What they *do* share is the seven session keywords, and that
  is named in the core, as `editor_model`. The rest waits for the first backend
  somebody else writes.
- **`Settings` gains one attribute and it is not about mounting.**
  `priority_keys` is what an embedded editor really asked for, and it is about
  keys rather than about panels: an application that has taken one of these
  combinations for a widget of its own inside the area the editor is in says so
  with it. Everything else an embedded editor might have wanted from `Settings`
  turned out to be something the editor knows for itself, which section 9.6
  keeps out.

#### 8.2.8 Facts checked against the pinned versions

Checked against `textual` 8.2.8 and the Python 3.14 `tkinter` in `./venv`,
because each of them decides a paragraph above: `App.run` calls
`asyncio.run`/`run_until_complete`; `App._check_bindings` walks
`reversed(screen._binding_chain)` on the priority pass, so widget priority
bindings are honoured; `Screen.refresh_bindings` builds that chain from
`focused.ancestors_with_self`, so a widget's bindings are active only while
the focus is inside it; `active_app` is in `textual._context` and private;
`COMMANDS` is declared on `Screen` and `App` and not on `Widget`, and
`get_system_commands` is declared on `App` alone;
`DOMNode.__init__` gives every widget its own `_bindings`, so the
per-instance binding the App does today works on a widget too;
`DOMNode.check_action` and `DOMNode.refresh_bindings` are on every widget and
not only on the application; `Widget`
warns that a `CSS` class variable is ignored; a scoped `DEFAULT_CSS` matches
the widget it belongs to by its type name and not by a style class the widget
carries, which `ModalScreen.DEFAULT_CSS` relies on as well;
`tkinter.Variable.__init__` calls `_get_default_root('create variable')`
when it is given no master; and `Misc.bindtags`, `Misc.bind_class` and
`Misc.unbind_class` are what section 8.2.7 is built on.

### 8.3 A ready-to-run program in each editor package

An application author should not have to write a program to get an editor for
their own configuration class, so each of the two editor distributions installs
one: `edit-cfg-json-tk` and `edit-cfg-json-textual`. They are a product and not
only a development tool, and the second benefit is what makes them worth the
code: a question about a configuration that is not two members long would
otherwise cost a hand-written example, and any class in reach answers it
instead.

**The core installs no program, and the name it would have installed under is
the reason.** The same command line over the non-interactive backend of section
1.1 is worth having, because it says what a class makes of a file and answers
with an exit code, which is what a continuous integration job can read and what
neither editor can offer. But that is a small utility for whoever is writing a
program on top of this library, and `edit-cfg-json` is the name of the editor
this library is for: a user who typed it and got a printout was misled by the
name rather than by anything the program did, and they were right to expect an
editor, because a command named after a library is taken for that library's
product. So the utility is `python3 -m edit_cfg_json.dump`, which says which
backend it runs, and the name is left free for the launcher that picks the
editor the machine can run.

#### 8.3.1 The command line owns no logic

`edit_cfg_json.cli` holds all of it — the parsing, the two doors to a class, the
construction, one editing session and the exit code — and `run_cli` takes the
backend for exactly the reason `edit()` does: the core names no user interface.
Each package is then a program of a few statements. Without that split the two
interactive programs would be near copies of each other, and section 8 answers
duplicate code between the backends by moving logic into the core rather than by
suppressing the warning. It is also what makes the whole program testable with
no display and no toolkit, by handing `run_cli` a backend that is a stub.

Each editor program is reachable as `python -m` on its own package as well, so
a machine whose script folder is not on `PATH` can still run it, and the
utility of the core is reached that way and no other. All three complete their
own command lines with `argcomplete`: the two installed programs through
`register-python-argcomplete`, and the utility through the global completion,
which finds the `PYTHON_ARGCOMPLETE_OK` marker of the module it is asked to
run.

#### 8.3.2 The class is told, and never guessed

`--module` names an importable module, `--file` names a Python file and
`--edit-settings` says that the class is this library's own settings; exactly
one of the three is required, and section 8.3.6 adds `--version` to the same
group as the one alternative that edits nothing at all. A single `module:Class`
argument reads better and
would have to guess which of the two it was given, which is the decision section
8.2.1 already took for this library as a whole; it would also make a Windows
drive letter a special case, and it would take the refusal of a missing or a
doubled location away from `argparse`.

**`--edit-settings` is a third door and not a mode.** What it answers is the
same question the other two answer — where does the class come from — so it
belongs in the same group of alternatives, and `--class`, `--loader` and
`--descriptions` are refused beside it because it has already said what all
three of them would say. With `-i` it reads a settings file and with no `-i` it
starts from the values the class declares, which is what every class the editor
is given with no input file already does; a second option for making a new file
was considered and rejected for exactly that reason, since it would be a name
for something the command line already expresses.

**What to edit is either a class or a loader**, named by `--class` and
`--loader` in that module or file. At least one is needed and both are allowed:
a class alone is constructed on the values it declares, a loader alone is asked
for a configuration and the class it answers with is the class of the session,
and the two together mean that the loader has to answer with that class or the
program stops. The check is made on the object that is really going to be
edited, so a loader that chose its class from the input file is answered for
that file, and `isinstance` is what it asks.

The class is a named option and not a positional argument, so
that the ways of saying what to edit are symmetric. `argparse` can be asked
for exactly one of a group of options and not for at least one of them, so the
refusal of a command line that names neither a class nor a loader is the one
that is written by hand, and so is the refusal of one that names either beside
`--edit-settings`.

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

`--unfold` belongs to that same program and to no other, for the same kind of
reason: a container that would flood a window opens folded (section 4.7), and a
printout has no control to press on it. It opens every container for good, after
the save and before the backend runs, so that the pass the backend makes before
it prints cannot fold a container it created away again.

That one fact about a backend is what `run_cli` is told, and neither `--save`
nor `--unfold` is then added to the parser at all for the other two, so it is
`argparse` that refuses them rather than a check written by hand.

The other fact each program is told is the name of its own settings file in the
home folder (section 9.9), which is the third step of the lookup and the one
thing about that lookup a program has to say for itself.

#### 8.3.4 What a corpus of real configuration classes shows

Opening the 47 configuration classes of the
[`config_as_json` examples](https://github.com/tom-bjorkholm/config_as_json/tree/master/example/src/example)
shows two things that no example in this repository would have.

- **The constructor has more than one shape.** `Config.__init__` names the JSON
  text `from_json_data_text`; the example classes that `config_as_json` ships
  name it `from_json_text` in the constructors they declare, as does
  `ConfigFactory`. An editor that insisted on the one name that
  `Config.__init__` uses would refuse 32 of those 47 classes over the name of a
  parameter, so the editor reads the signature and passes every parameter it
  knows the meaning of, which is principle 4 of section 3 applied to a
  constructor. No text is passed to a constructor at all
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
to call it with, so the answer cannot differ between them. There are two of
them, the declared defaults and the load, because the validation of a buffer
and the walk that attributes a refusal copy an object rather than construct
one.

#### 8.3.5 The command line names no setting

A program is told **what to edit and which files**, and never how the editor
behaves. Every setting there is is a member of `SettingsConfig` (section 9.8),
so a program reads all of them from a settings file, and the one option the
command line has about them is `-c/--cfg`, which says *which* file this run
behaves according to.

The two that a program could plausibly have been given are the ones an
application knows about its own files — the extension its configuration files
use and whether it is enforced — and an option for either would be a second way
of saying what a settings file already says, inside one run, with nothing to
decide which of the two wins. `--key ACTION=COMBINATIONS` is the same answer
once more, and it is the one that makes the shape plain: an option per setting
is a command line that grows a flag every time `Settings` grows an attribute,
and section 9.1 promises that it will.

**A settings file is per run and not only per user**, which is what makes one
option enough. An extension is a fact about the class being edited, while a
file of the home folder is a fact about whoever is running the program, so
somebody who opens two applications' classes writes a settings file for each
and names one with `-c`. That is the option used for what it is for, and it is
the answer to the one thing the lookup of section 9.9 could not do on its own.

**Asking for the defaults of the editor is naming a file that says nothing.** A
settings file need name only what it changes, so one holding `{}` is the last
step of that lookup written down, and `-c` reaches it past a file of the home
folder that says something else. There is therefore no option for ignoring the
lookup: it would be a name for something the command line already expresses,
which is the reason section 8.3.2 gives for `--edit-settings` having no
companion option for making a new file.

The examples of this repository do have `--extension`, `--enforce-extension`
and `--key`, and that is not the same command line disagreeing with itself. An
example stands in for the application, which decides these things in Python,
and the options are there so that every answer can be tried without writing a
program per answer. A program has no application around it, which is exactly
why it reads a file instead.

#### 8.3.6 What a program says about its own versions

Whoever is about to report a problem, and whoever is about to upgrade, has to
know which versions are really installed and whether newer ones exist. So each
of the three programs answers `--version` with the report that
[`versionreporter`](https://pypi.org/project/versionreporter/) prints: the
installed version of every package the program is built out of and of Python
itself, and then what PyPI has that is newer, told apart into what runs on this
Python version and what would need a newer one. It is one call to a package
that does this rather than a version string of this library's own, for the same
reason as everything else here: the second half of that report is the half
nobody writes for themselves.

**It is a fourth alternative and not an option beside the other three.** Naming
a module, naming a file, editing the settings of this editor and asking what is
installed are four things one run does *instead of* each other, so `--version`
joins the required group of section 8.3.2, where `argparse` refuses it beside
any of the three and accepts it on its own. It is answered before the rest of
the command line is looked at, because a run that reports versions edits
nothing, reads no settings file and opens nothing.

**This is not the setting that section 8.3.5 keeps off a command line.** A
setting says how the editor behaves while it edits, and every one of them is a
member of `SettingsConfig` written in a file. `--version` says that this run
does something other than editing, which is the same line `--save` and
`--unfold` are on the far side of.

**One class per distribution, derived and not configured.** The report begins
with the distribution the program was installed from, because that is the
package whoever runs it has to upgrade, and because `versionreporter` takes the
first name of the list as the one its upgrade instructions name.
`EcajVersionReporter` names the core and what the core declares, and each
editor package derives a class that puts its own name in front of that list and
adds whatever else it alone depends on — `textual` in one of them and nothing
in the other, because Tkinter comes with Python. So a dependency is written
down in the package that declares it and nowhere else.

It has to be a class and cannot be a name handed to one:
`get_main_package_name` and `recommended_python` are class methods of
`versionreporter`, so two instances of one class cannot answer them
differently.

**The reporter reaches `run_cli` as an argument of its own**, rather than being
asked of the backend. A backend is what shows a model, and one of them is
handed to a program, to `edit` and to every example of this repository, so what
it said about a distribution would be right in the first of those and
meaningless in the others; the two mounting entry points are not backends at
all and would be left out of a report that lived there. What a report is about
is the *package the program was installed from*, which is the same kind of fact
as the name a program is installed under and the name of its own settings file
in the home folder — both of which `run_cli` is already told, and for the same
reason. It is a required argument because a program that forgot it would report
another package's name to a user about to upgrade.

**`check_if_unsupported_python` is deliberately not called**, though
`versionreporter` recommends it beside the flag. It prints to standard output
at the start of every run: the Textual editor's own screen would cover it, the
window editor has nobody reading the terminal it was started from, and the
utility of the core would put a paragraph in front of a printout that scripts
read. What it would say is in the report, and a user who wants it asks.

## 9. Settings the application owns

The editor does not run on its own. It runs inside an application that has
already made decisions the editor has no right to overrule: which key
combinations that application's own user interface has taken, and what a
configuration file of that application is called. An editor that decided
either of those for itself would be overruling the application, which is the
one thing a library in this position must not do.

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
    backup_suffix: Optional[str] = '.bak'
    backup_count: int = 1
    priority_keys: bool = True
    confirm_overwrite: bool = True
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
where saying it costs nothing. Section 9.8 is where that was asked again, and
the answer is the same: what would have wanted them unfrozen is impossible for
a different reason.

`explain` is what the promise above was written for: an action added later is
an added attribute, and no application that was written before it breaks. Its
keys are `f1`, because a function key is what asks for help everywhere else and
because a field claims most of the control letters, and `ctrl+g`, because a
terminal or a keyboard that does not deliver a function key would otherwise
leave the action to the button and the command palette.

The last three make the same point about the files: three attributes, three
defaults, and an application that says nothing about them
gets what the editor would have chosen anyway. What they say is section 7.3's;
that they are here is because only an application knows how its own
configuration files are looked after. Two of the three defaults are the answers
that lose nothing — one kept file, and a question before it is written — which
is the right way for a default about something that cannot be undone to lean.

`fold` makes the same point again. Its keys are `f2`, the function key beside
the one that explains, because the two actions are the same kind of thing —
both of them decide how much of the configuration is on the screen — and
`ctrl+t`, for the reason `explain` has a control letter as well and because the
tree is what the action is about. A configuration with no list and no dict in it
is never offered the action at all (section 4.7), so those keys are free
wherever there would be nothing to fold.

**It is deliberately not `ctrl+f`**, which is the one combination that means
find everywhere and is therefore not the editor's to spend.
`ctrl+shift+f` was considered and rejected for the reason
`save_as` already records above: a terminal that encodes a control letter as a
single byte has nowhere to put the shift, so that combination would arrive as
`ctrl+f` and the fold key would run the search. See section 9.7.

`priority_keys` is the one attribute that is not about *which* keys the editor
has but about **how hard it holds them**. True is the default and is what an
editor wants of its own keys: the editor is offered a combination before the
widget that has the focus, so a user who presses Save while typing into a
field means Save. False is for an application that has taken one of these
combinations for a widget of its own inside the part of the window the editor
is in; the widget with the focus is then offered the key first and the editor
gets what is left of it.

It is the one attribute that only an **embedded** editor has a reason to
change (section 8.2), which is why it took until then to be added, and it is
the same promise again: an attribute added later breaks no application. It is
also a different answer from an empty tuple in `ActionSettings` and both are
worth having — that one takes a key away from the editor altogether, and this
one leaves the editor the key it did not get first.

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

Whether an overwritten file is kept, under what name, how many of them, and
whether overwriting is confirmed are application decisions of exactly this
kind, and they are the three attributes section 7.3 is about. Whether there is
anything *unsaved* is not, which is the line between them: the editor knows
that for itself.

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

### 9.8 The same answers, written in a file

An application decides these things in Python. A *program* of section 8.3 has
no application around it to ask, and the person running it is who decides
instead — so the same answers are a `config_as_json.Config` class of their own,
`SettingsConfig`, and can be read from a file. It is also what an application
declares as one member of its own configuration where its own users are the
ones who should decide, which is the second thing it is for and the reason it
is in the core rather than in each program.

**It mirrors `Settings` and does not derive from it**, and the reason is not a
preference. `ActionSettings` declares a member called `validate`, which shadows
`Config.validate()` on every object of a class bridged the way
`config_as_json`'s third-party-parameter pattern bridges one; `config_as_json`
calls that method while it constructs and while it parses, so such a class
cannot be built at all. No `Config` may hold a member of that name. That
settles the question section 9.1 leaves open by making it moot: `Settings` and
`ActionSettings` stay frozen, for the reason section 9.1 already gives.

**The key combinations are a dict member and not a nested object.**
`config_as_json` reads a nested configuration object whole — it constructs one
from its own JSON without the permissive flag of the parse around it — so every
settings file would then have had to name every action. A dict member is filled
in per key instead, its keys are checked against the ones the class declares,
which is the same protection against a misspelled action name that section 9.1
gets from one attribute per action, and a member validator completes what a
file left out so that the editor shows every action whatever the file held.

**Nothing here restates what a valid setting is.** Each member validator hands
the value to what `Settings` and `ActionSettings` already say, which is
principle 1 of section 3 applied to the editor's own settings: there is one
place that says a combination cannot belong to two actions, and it is the place
the editor itself is built on. Two rules that both classes need — whether a
piece of text adds anything to a file name, and what an extension without its
dot becomes — are functions of the settings module that both read, rather than
two statements that could come to disagree.

### 9.9 Where a program finds its settings

A program looks in five places and uses the first that answers: the file that
`-c/--cfg` names, the file that the `CFG_EDIT_CFG_JSON` environment variable
names, a file of that program's own in the home folder, `$HOME/.edit-cfg-json.cfg`
there, and finally nowhere at all, which is the defaults of the editor.

**A file that was named must be there, and a file that was looked for need
not be.** The first two are somebody saying which file to use, so a name that
no file answers to is a refusal with an exit code of its own: running with
other settings than the ones that were asked for is the one thing a lookup must
not do quietly, and falling back would be answering a question that was not
put. The two files of the home folder are the lookup itself, and a step of a
lookup that finds nothing is the lookup working.

**One environment variable for every program, and one file of the home folder
per program above the shared one.** The variable is a machine or a session
deciding how this editor behaves, and an answer that had to be given three
times would come to be given twice. The per-program file is the other half of
the same thought: what the two editors differ about is their keys and their
questions, so a user who wants the window and the terminal to differ writes
one file each and a user who wants one answer writes only the shared file. The
backend that prints once and returns has neither keys nor questions, so it has
no file of its own and reads the shared one or nothing.

**It is read with `LoadPolicy.DEFAULTS`**, because a settings file is written
by hand to change one or two things and what it does not name is what the
editor would have chosen anyway. It is also read **before** anything else the
command line names, because it is what the whole run behaves according to.

**The last step is reachable by name**, which follows from that and is worth
saying because it is what a command line option would otherwise have been asked
for. A file that names nothing is the defaults of the editor, so `-c` naming
one is how a run asks for them past a file of the home folder that says
something else. Section 8.3.5 is where that is the answer to a question.

## 10. Testing strategy

### 10.1 Core

The core needs no UI and no display, and it is where essentially all the
logic lives. If a behaviour can only be tested through a backend, that is
evidence the behaviour is in the wrong package.

**A printout of the model is evidence about the core and never about a
backend.** The non-interactive backend of section 1.1 is a test instrument as
much as it is a user interface, and what it can testify to is what the model
holds. What only a user can reach — a control that is pressed, a field that
loses the focus, a question that is answered — is tested where it exists, which
is sections 10.2 to 10.4.

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

In scope, and implemented:

- read, edit and save with full validation
- lists and dicts as a tree of rows, with a field at every value
- folding with per-subtree validation badges
- add and remove elements of uniform lists and dicts, move an element of a
  list, and give a declared optional member its object or take it away
- descriptions, class docstrings, and a docstring visibility toggle
- automatic-change and filled-default visibility
- a question before closing drops what has not been saved (section 7.2)
- the file a save writes over kept, and a question before it is written
  (section 7.3)
- modal `edit()` with both backends
- the editor mounted in a window an application already owns, in both
  toolkits, with its keys reaching the editor and nothing else (section 8.2)
- the settings of the editor as a configuration class of their own, editable
  in the editor and declarable as one member of an application's own
  configuration, and read from a file by each program (sections 9.8 and 9.9)

Deliberately out of scope for v1, and therefore not implemented:

- **Containers with nothing to copy a new element from.** Only the
  application knows what an element of its own list looks like, and a
  member it neither declares an element for nor holds one of has never
  said. Such members can be reordered and have elements removed, but not
  extended, and the UI says so rather than guessing. Section 4.9.
- **`DICT_VALUE_BY_KEY` members and dicts listed in
  `_unchecked_dicts`.** These have per-key rather than uniform policy.
  An ordinary dict member is not out of scope but out of reach: its keys
  are the ones its class declares and `config_as_json` refuses any other,
  which section 4.9 records.
- **The draft file** of section 7.1.
- **A `Protocol` in the core for the mounting contract**, which section
  8.2.7.1 leaves for a third implementation of it to check against.

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
- **`Settings` unfrozen and bridged into a `Config`**, the way
  `config_as_json` bridges a third-party parameter class. It would have made
  the settings and their configuration class one class rather than two that
  have to agree. It is impossible: `ActionSettings` declares a member called
  `validate`, which shadows `Config.validate()`, and `config_as_json` calls
  that method while it constructs and while it parses. Section 9.8.
- **The key combinations as a nested `Config` object.** It would give them a
  class, a docstring and a member each, which is more than a dict member says
  about itself. `config_as_json` reads a nested object whole, so every settings
  file would then have had to name every action, which is the one thing such a
  file should not have to do. Section 9.8.
- **A second option for making a settings file that does not exist yet.**
  `--edit-settings` with no `-i` already starts from the values the class
  declares, which is what every class the editor is given with no input file
  does, so the option would be a name for something the command line already
  says. Section 8.3.2.
- **A `master` argument beside the parent, with the backend creating the
  `Toplevel`.** Rejected at step 18 and **built at step 18B**, as `parent`
  beside `area`. Two mutually exclusive arguments really are two where one
  would do, and the window decisions really do belong to the application — but
  every application that wanted a window of its own was then writing the same
  five lines of `tkinter` against this library rather than with it, and the
  library it is most likely to be embedded beside had already answered the
  question the other way. An application that wants those five lines back
  passes `area` after making the window itself. Section 8.2.2.
- **Blocking while embedded, with Tk's nested `wait_window`.** It would
  keep `run_editor` honest in one backend and is impossible in the other,
  which is the worst place for a difference between them to be. Section
  8.2.3.
- **Tk key bindings on each field the editor creates.** It scopes the keys
  the way embedding needs, and it leaves a key dead the moment the focus is on
  a button, which is where a Tk focus lands as soon as anything is pressed.
  A bind tag scopes the same way and covers everything the editor built.
  Section 8.2.7.
- **A focusable Tk panel with the bindings on it.** It would put the editor
  into the application's tab order, which is a decision about the
  application's own window that section 8.2.2 gives to the application.
- **`close()` answering whether the editor really closed.** Useful in Tk and
  impossible in Textual, whose question is a modal screen with a callback. One
  answer both backends can give — `on_close` — is worth more than a return
  value in one of them. Section 8.2.3.
