# Design of edit-cfg-json

This document records the design of the folding configuration editor built on
top of [`config-as-json`](https://pypi.org/project/config-as-json). It
describes what is implemented and how it is designed, and what is planned but
not implemented yet. It is a design document, not an API reference. Where it
states a fact about `config_as_json`, the source is that project's own
documentation, examples and implementation:
[github.com/tom-bjorkholm/config_as_json](https://github.com/tom-bjorkholm/config_as_json).

## 1. Purpose and scope

An application whose configuration is a `config_as_json.Config` object should
be able to hand that object to this library and get a usable folding editor,
without writing any UI code and without describing its configuration schema a
second time.

The library provides:

- a UI-agnostic core that discovers the editable structure by
  introspection and owns all editing, validation and file handling
- a Textual (terminal) editor
- a Tkinter (desktop) editor
- a very limited non-interactive backend, shipped by the core, which
  prints the model once and returns

The application supplies its `Config` object, optionally a loader callable,
optionally an input file name, an output file name, and a mapping of
per-attribute descriptions.

The editor has no opinion about what the filename extension shall be for input
or output files. Some applications use `.cfg`, some use `.json`, and other
extensions are in use as well.

### 1.1 The two interactive editors are what this library is for

The Textual editor and the Tkinter editor are the product. Wherever this
document says what a feature does, it says what it does in a window or in a
terminal: which control the user presses, what appears below which member, and
what changes when the focus moves.

The non-interactive backend offers no field to type into, no control to press,
no focus to lose and nobody to answer a question, so a printout can show what
the model holds and can never show what an editor does. It is good for two
things: exercising a feature over the core and backend API on a machine with no
display, and running a short sequence of editor actions and printing what they
left behind. It is `DumpEditor` in the core, `--ui dump` in the examples of
this repository, and the backend of the `python3 -m edit_cfg_json.dump`
utility (section 8.3).

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

The core is a base for third-party UI implementations, and a third party needs
a package to depend on, a version to pin, and a published API contract.
Reinforcing reasons: a Qt or web backend is a likely later extension, and a
third-party `edit-cfg-json-qt` is then symmetric with the two in-house ones;
and the Tk editor must be absent, not merely unimported, where Tk is missing.

### 2.2 Naming

Flat sibling distribution names, not a PEP 420 namespace package. A namespace
package would allow `edit_cfg_json.qt`, but flat names give the same symmetry
without the namespace-package pitfalls (no top-level `__init__.py`, so no
re-exports; a stray `__init__.py` silently breaks resolution; mypy and pylint
handling is fragile, which matters under this repository's strict checkers).

### 2.3 Versioning and build configuration

- `BuildSpec.identical_versions` stays at its default `True`, so the three
  packages release in lockstep and the compatibility matrix is one-to-one. The
  version of each package is in its `setup.py`, because `pyproject.toml`
  declares it `dynamic`, and the build refuses a build in which the three
  differ.
- The UI packages pin the core with a compatible-release constraint and not
  with an exact one, so a core patch release does not strand them.
- After Alpha (section 2.5) the core follows semantic versioning, a promise
  third-party backend authors need more than the in-house backends do.
- `BuildSpec.package_folders` stays unset; the three `pyproject.toml` files are
  auto-discovered.
- `additional_venv_packages` in `custom_build_tools/custom_spec.py` is unset
  and would be redundant: the step that creates `./venv` installs the declared
  dependencies of the discovered packages, minus the three internal ones.
- Tk tests are split into three categories with different display
  requirements. See section 10.

### 2.4 The public API contract

- Everything a UI backend needs is re-exported from
  `edit_cfg_json/__init__.py`. Everything else is internal and may change
  without a major version bump.
- The two in-house backends import only from the top-level `edit_cfg_json`,
  never from its internal modules; otherwise the public API will be
  under-designed and the first real third-party backend will discover it.
  Enforced by a test that walks the backends' imports.
- The core must never import `tkinter` or `textual`. Enforced by a test that
  imports the core with both blocked in `sys.modules`; separate wheels do not
  catch a wrong-direction import on their own, because all three packages are
  installed into the same venv at test time.

### 2.5 Alpha status

The packages are released as Alpha. **While Alpha, no API stability or backward
compatibility is offered**, for the core or for either backend. The
public/internal split of section 2.4 still applies, but crossing a major
version is not required to change a public name during Alpha.

Alpha is what makes it safe to publish three packages before the public API of
the core has been proven by a backend that somebody else wrote: the two
in-house backends exercise it and cannot test whether it is enough for a
backend written without reading the core. The README and the PyPI classifiers
say so plainly while it lasts: `Development Status :: 3 - Alpha` in all three
`pyproject.toml`, and `readme_parts/alpha_status.md` in all three generated
readme files.

### 2.6 Shared type aliases

Aliases use the `type` keyword. Two rules keep them from multiplying:

1. **Never alias what `config_as_json` already exports.** `JsonType`,
   `PathOrStr`, `ConfigPath`, `ValidationPlan` and `NestedConfigs` are
   public there and are used under those names here.
2. **Each alias is declared exactly once**, in one module of the core,
   re-exported from `edit_cfg_json`, and imported from there by both
   backends. An alias for the same type declared again in another file
   is a defect, not a style preference.

The aliases the design needs:

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

The model is a tree of nodes segmented by config ownership. A nested `Config`
object is a first-class node with its own type, docstring and validity state;
ordinary JSON structure lives inside the ownership region of the config object
that owns it. This mirrors `child_owned_paths` and the `serialize_converters()`
ownership rule of `config_as_json`, and reusing the library's own segmentation
is what makes section 6.2 work.

Sources of structural information, in order of authority:

| Source | Provides |
| --- | --- |
| `nested_configs()` | Which members are nested configs, their `ConfigNestingKind`, their `config_type`, any `factory_function` |
| Default instance | Every attribute name and its default value |
| The declaration of each member | Which kind of value that member takes, whether it may hold nothing, and what one value inside it would be |
| `parse_converters()` | Which keys become rich Python types, and the expected parsed type |
| `serialize_converters()` | Which values need explicit conversion on write |
| `_unchecked_dicts` | Which dict members have relaxed key policy |
| `_omit_none_from_json()` | Which members are genuinely optional |

**Ordinary JSON structure is a tree of rows.** A member holding a list or a
dict is one row, and every value inside it is a row of its own, indented once
per container, with a field at every value. The container row has no field,
because it has no value of its own; it says how many rows it holds instead. A
change inside a container is a change of the member whether it is folded or
not.

**A value inside a container is addressed by the path to it.** A list element
is addressed by its index written out, so `('retry_delays', '0')` is a path and
`('retry_delays', '[')` is the selector for every element of that list.
`config_as_json` has no notation for one specific element — `'['` is its step
for all of them — so this is the editor's own, and it is why a dictionary key
beginning with `'['` is reserved there and never a path step here.

**What a container holds is shown in the order the file has it**: the order a
list holds its elements, and the sorted order of a dictionary's keys.
Declaration order is about the members, because a member has a declaration to
be read from and a dictionary key has none.

**A nested configuration object is a node of its own.** It serializes as a dict
and it is not one: it has a class and a docstring of its own, and its members
are the rows below it in the order that class declares them. Its row says the
class rather than how many entries the dict has.

**Where those objects are is asked as a path and not as a member name.** The
ordinary shape is a *list* of nested objects each holding a dict of more of
them, which is what `ConfigNestingKind` says: `LIST_ELEMENT` and `DICT_VALUE`
declare that every value *inside* a member is an object, and
`DICT_VALUE_BY_KEY` declares one named key of it. The member holding them is an
ordinary container of the tree, and each object inside it is one node with rows
of its own. A nesting kind changes **what a nested node offers** and never
**how the tree is built**, so one walk over the declarations answers for every
kind. What does ask more of a node is a container gaining and losing elements:
section 4.9.

**The declarations are walked over the object and not matched as selectors**,
because *ownership is asked of an object*: `parse_converters()`,
`_omit_none_from_json()` and the declaration order of the members are methods
and attributes of an instance, while a declaration says only which class was
expected. So the configuration object itself is asked, and it answers with the
absolute path of every nested object there really is, and with the object at
it. That tells the truth where a `factory_function` answered with a subclass,
and distinguishes an `OPTIONAL_MEMBER` that holds an object from one that holds
none. The `'['` selector keeps its meaning in the description mapping of
section 4.3.

**Ownership is the rule for everything inside such a node.** A converter
belongs to the class that owns the subtree, exactly as `serialize_converters()`
does on the way out; which members may be left out of a file is that class's to
say; and the members are ordered as that class declares them and not as the
sorted dictionary it writes. What does *not* stop at the boundary is the
description mapping (section 4.3).

**A declared member that holds no object is a row that says so.** It says which
class is missing and cannot be edited, because no text typed into a field
becomes a configuration object; making one is adding, and belongs with adding
an element of a list.

**A member that its class leaves out of the file has a row all the same.** A
class that lists a member in `_omit_none_from_json()` writes nothing at all for
it while it holds nothing, so the values one object writes are fewer than the
members it has. The ones it left out are the ones it holds and did not write,
and they are added back, each of them holding nothing. Without that, a file
with no key for such a member would be exactly the file in which the member
could never be given a value, and that is the file the application ships: a
member is optional because it is usually absent.

**So the tree differs from the file in one direction and the buffer in the
other.** Reading adds those members, holding nothing; writing them back to the
class takes them out again, so that what a validation pass is given is the
document a save would write. Passing `null` for one of them instead would be
reaching a verdict about a document no save of this configuration produces, and
a class is free to make something of a key it does not find — the rules of
section 5.3 for reading an older file are given the keys of the document before
anything else looks at them.

**What a validator inside a nested object refuses is attributed by asking that
object on its own.** Such an object validates itself while the whole
configuration is parsed, so the object that could say which member was refused
is one the editor never holds, and the answer of section 6.3 does not reach
inside because the nested objects are constructed by `parse_json`. Applying the
subtree of the buffer to the object that owns it does reach it: section 6.2.

A list of nested `Config`s, each having a dict of nested `Config`s, is the
normal case and not a special case. A trivial configuration of scalars is the
exception.

**Where the declared type of a member is read from.** `self.story_points: int
= 5` inside `__init__` is a PEP 526 annotation on an instance attribute, and
Python records it nowhere at runtime, so `typing.get_type_hints()` returns
nothing useful for the ordinary `Config` pattern. Three sources are asked, in
this order, and each covers a pattern the others do not.

1. **`typing.get_type_hints()` on the class**, which answers for a class built
   on the dataclass pattern — `e04_third_party_class.py` of the
   [`config_as_json` examples](https://github.com/tom-bjorkholm/config_as_json/tree/master/example/src/example)
   is one — and for any class level annotation.
2. **The source of the class**, parsed with `ast`, taking the annotation of
   every `self.x` there is. The whole of the class and not only its
   `__init__`, because a class is free to declare its members in a method of
   its own that `__init__` calls, and the annotations there are just as real.
   A class further up the MRO is asked in its own right, because its own
   module is where the names of its annotations mean something.
3. **The value the member held when the file was last agreed with**, which is
   what section 4.2 has always used and remains the answer wherever the two
   above say nothing.

**Nothing is evaluated by this library.** An annotation read from source is a
text, and the text is handed to `inspect.get_annotations`, which is the
standard library's own resolver for one — the same resolution
`typing.get_type_hints` does, in the namespace of the module the class was
written in. An annotation written in quotation marks is unwrapped first, so a
forward reference resolves to what it names rather than to its own name.

**Every one of the three is optional, and that is the point of having three.**
A class defined in an interactive session, by `exec` or inside a frozen
program has no source to read; an annotation naming something that exists only
while a type checker is running will not resolve; and a member can simply be
assigned without an annotation. Each of those costs that member its
declaration and nothing else, and one annotation that fails leaves every other
member of the class alone.

**What is made of the answer is deliberately little.** A declaration says one
of the kinds a leaf value has — text, a whole number, a number, true or false,
a list or a dict — or it says nothing this library can use. A class of the
application's own is nothing it can use: what the editor does with a kind is
say what it is and make an empty one of it, and it can do neither with a class
it has never seen. Where the member holds a nested configuration object, the
object itself is what answers; where it holds an enum, the parse converter
of the class answers, and it says far more.

### 4.2 Edit buffer

The buffer holds JSON-compatible values at the leaves, typed as
`config_as_json.JsonType`. The user edits what will actually land in the file —
an enum is edited as its member name. It is not JSON text: the edit field shows
no quotation marks around a string, and shows `10` for both the string `'10'`
and the integer `10`. The buffer therefore holds type information beside each
leaf value.

**That type information is shown to the user**, as a line of explanatory text
below the member, in the same place and under the same toggle as everything
else explanatory; section 4.3 says what it says. It is not a label beside the
field, because it is text about the value and not part of it, and because a
narrow window would then squeeze the field for it.

The type metadata of a leaf is **what the class declared for that member**,
and failing that **the value that leaf held when the file was last agreed
with**, which is when the model was built and again after every save. Section
4.1 says where a declaration is read from and how little is made of it.

The declaration wins because the value cannot always answer. `self.threshold:
float = 0` holds a whole number and the member takes a number, and a member
whose default is `None` held nothing, so nothing was learned from it at all.

Deriving the kind from the *current* value does not work either way: a number
member that is half typed holds text until its text is a number, and it would
stop being a number member for the rest of the session. The kept value also
answers whether the user changed the leaf. The comparison is made on the JSON
notation rather than with `==`, because Python considers `True` equal to `1`
and `1` equal to `1.0` while a file writes all three differently.

The one thing that comparison ignores is **the order of the keys of a
dictionary**: `config_as_json` writes them sorted, so a file cannot hold two
orders, while the editor does hold another order for the members of a nested
configuration object (section 4.1). Without this, every nested object would
report itself as changed by a validator the first time it was validated.

A successful save moves the kept value to what was written, so the editor stops
reporting unsaved changes and the *edited* mark of every leaf clears. That is
safe for the type question too, because only a validated configuration is ever
written. The *changed by validator* mark is deliberately not cleared by a save:
that a value is not literally the one the user typed stays true after it has
been written.

Text that is not JSON at all is kept as a string rather than refused, which is
what makes a value typable: it is invalid for most of the time it takes to type
it. The string a number member then holds is simply the wrong type, and section
6.1 reports it as one.

A field writes into the buffer on **every change and not when it loses the
focus**, because a commit on focus loss would lose the last edit whenever
saving is reached without leaving the field.

Losing the focus is however when the **conversion of one field** reports
itself. It arises with the leaves that `parse_converters()` turns into rich
Python types, an enum being the obvious one: its member name is not a member of
the enum for most of the time it takes to type it, so converting on every
change would report a failure that is not one yet. It is
`EditModel.check_field`, which each backend calls from its own toolkit's
focus-loss event — `<FocusOut>` in Tk and `Input.Blurred` in Textual.

This is **not** the validation of section 6: it is local, needs no candidate
configuration, and answers whether this text means a value at all. Both reach
the user through the same line below the member, and section 6.5 settles which
is shown when both have something to say. The answer is **kept per member and
cleared by the next edit of that member**, because it is answered by the member
alone, while what a validator refused is only known for as long as the rest of
the buffer stands still.

**The converter is run rather than read.** Whether a name is a member of an
enum is decided by calling the `ParseConverter` the class declared, so an
application that declared a converter of its own is answered by its own
converter. That is principle 1 of section 3 applied to conversion, and it is
why nothing here knows what an enum is.

**A conversion that fails is reported for the member and not as JSON.**
`config_as_json` reports a failed conversion inside the message it prints for
JSON it could not load, because the conversion runs inside `json.loads()` —
right for a program reading a file and wrong for a person editing a field. So
the conversion of every member is run *before* the candidate configuration of
section 6.1 is built, and a member whose text means nothing is reported as that
one member. The candidate is not built at all in that case. The load path of
section 5.2 is deliberately left as it is, because a refusal the user cannot
act on inside the editor is not a field being edited.

**A member holding true or false is entered like an enum member.** Such a
member has no parse converter — there is nothing to convert `true` into — so
it would otherwise be the one member whose value has to be typed exactly and
in lower case, while `config_as_json` accepts any unambiguous beginning of an
enum member name in any case at all. The two words are read by those same
rules: the case is ignored, a beginning of one of them is that value, and a
beginning of both of them is neither, which only the empty text of a cleared
field is. It is read where every other text becomes a value, on the change and
not on the focus loss, so a validation pass and a save are given the value the
user meant, and the whole word reaches the field with the refresh that follows
a pass.

**What means neither of the two words is refused at that member**, in the words
an enum member name that names no member is refused in: `yes is not one of:
true, false`. It is the one refusal of a leaf that the editor makes itself
instead of running something the class declared, and what it is made from is the
type of the member rather than a rule of the application — the same knowledge
that says *true or false* under it (section 4.3). One consequence is deliberate:
an application that would have accepted something else in a member whose value
was true or false cannot be given one from the editor. The type is what the leaf
held when the file was last agreed with, as everywhere else here, so a member
that held a string is a text member and takes any text, and a member that held
nothing at all is a member whose type nothing says, which is the open question
at the end of this section.

**Which nodes hold one of the two words is therefore part of what a validation
pass is given.** The values it is handed are JSON space values, in which nothing
says which member takes those two values and only those two, and the rows are
where the type of every leaf is kept.

Rewriting the text a field shows is a separate matter, and belongs where
validation rewrites values (section 6.4).

Each leaf is addressed by a `config_as_json.ConfigPath`, so that a member
inside a list, a dict or a nested config needs no second way of naming it. The
mental model presented to the user centres as much as possible on the `Config`
objects; JSON encoding is only a way to show and edit individual leaf values.

Editing a live `Config` object attribute by attribute is rejected: a value
being typed passes through intermediate states that are not valid, rich Python
values exist only after `parse_converters()` runs, and a half-edited object
cannot be validated meaningfully. JSON-space leaves also make the validation
round-trip in section 6.1 exact.

Per-field flags carried by the model, not by the backends, so that the two UIs
cannot drift:

- **changed by validator** — set when a validation pass rewrote the
  value, cleared when the user next edits that field
- **filled from default** — set when a permissive load supplied a value
  the input file did not contain
- **changed by the load** — what reading the input file did to this value
  (section 5.3). It is text rather than a flag, because the load records which
  rule put the value there and at which older key it found it, and a member
  that says it was read from `title` says more than one that says only that
  something happened. A member that only the comparison found says that much
  and no more. It is never set together with the mark above it, which says the
  same thing more precisely.

**The user never changes what kind of value a leaf takes.** That was left open
until the declaration of a member was read, because the one thing it would
have been useful for is telling a `None` apart from an empty text in an
`Optional[str]`, and there was then nothing that said which members those
were. There is now, and it answers that question without letting anybody
change the kind of anything.

**A member the class declared to allow no value has two states.** It holds a
value, or it holds nothing, and both of them are states of the member rather
than texts in a field:

- while it **holds a value** it is an ordinary field, and it offers *removing*,
  which puts it back to holding nothing;
- while it **holds nothing** its row says so where the value would be, has no
  field at all, and offers *adding*, which gives it the value of its kind that
  says no more than which kind it is.

Those are the two controls that section 4.9 already gives a declared member
holding no configuration object. Nothing new is added to either backend, to the
keys or to the command line, which is most of why this is the answer.

**How the class writes such a member decides nothing about the two states.** A
member written as `null` and a member that `_omit_none_from_json()` leaves out
of the file have the same pair of states and the same pair of controls; what
differs is the file, which holds `null` for the first and no key at all for the
second. Both of them have a row while they hold nothing, for the reason section
4.1 gives, and the line under the member says which of the two kinds of
optional it is because that is the difference there is.

**A member declared to hold a dict is the one that cannot be given a value.**
`Config.check_dict_parse` refuses a dict written for a member whose value is not
one — *Unexpected dictionary for X in JSON data* — whatever keys it has and even
where it has none, so the empty dict is the one value of a kind that the editor
cannot give such a member. It is the first bullet of section 4.9 one step up:
the same check refuses a new key of an ordinary dict member, and offering the
control anyway would be offering one that produces a refusal. That member says
so below its own row instead. A list has no such check, so a member declared to
hold one is given the empty list and grown from there in the ordinary way.

**A field can therefore never put a member into that state.** Text that parses
as JSON `null` is kept as the text it is for such a member, exactly as any
other text of the wrong type is. Without that, four characters typed into a
field would take the field away from under the cursor that typed them, and the
state is one the user asks for with a control rather than one they type. A
member with no such state reads `null` as the JSON it is, as it always did.

**A member that holds nothing while its class does not allow it to** is left
exactly as it was: an editable field showing `null`. The two states exist only
where the class said there were two, and a value that the class does not allow
is a wrong value that the user has to be able to type over.

**A member whose kind nothing says is that same field**, for the same reason
one step further back: the two states exist only where the editor can make a
value for one of them, so a member with no annotation at all has one state
however its class writes it. Such a member is still reachable, which is what
matters — the field takes a value and takes `null` back again — and the moral
is the one section 4.1 ends with: annotate the members of a configuration
class.

### 4.3 Descriptions and docstrings

Two complementary, independently optional sources of explanatory text, plus the
type of the member, which always says something.

**Class docstrings** label config-object nodes. They are read with
`cls.__doc__`, cleaned with `inspect.cleandoc()`, and split at the first blank
line into a summary and the full text. The summary is collapsed to a single
line, because where a docstring is broken is a fact about the width of a source
file and not about the text.

Use `cls.__doc__` and **not** `inspect.getdoc(cls)`: `getdoc()` inherits from
base classes, so a nested config class without its own docstring would silently
display `Config`'s — actively misleading in an editor. Check
`cls.__doc__ is not None` and show nothing otherwise.

**Which of the two a nested node shows is decided by its fold**: the whole
docstring while the node is open, the summary while it is folded, and both of
them under the explain toggle of section 4.4. The root configuration is never
folded, so its summary stays on its label line. A backend therefore writes that
text again on every fold and not only when the toggle is pressed: it is put
together by `row_description` rather than carried by the row, and
`row_describes` is what a backend asks before it creates the widget at all.

**The description mapping** labels individual attributes, because per-attribute
docstrings do not exist at runtime: a string literal after an assignment is
discarded, and PEP 526 annotations are not recorded.

**The type of a member** says the rest. Where the member holds an enum,
`parse_converters()` is what says so, and the enum class then says the rest
itself: the summary of its own docstring and the names it accepts. Where it
holds anything else, what is said is **what kind of value it is** — text, a
whole number, a number, or true or false — read from what the class declared
for that member, and failing that from the value the member held when the file
was last agreed with (sections 4.1 and 4.2). It answers the one question a
value cannot answer about itself: whether `10` in a field is the number or the
text. It matters most where the application described nothing.

**A member that need not hold a value says so as well**, and there are two
ways it can be one and they are not said together. A member the class leaves
out of the file while it holds nothing says that, from the
`_omit_none_from_json()` of the class that owns it, and that is the more of
the two: a member left out of the file is a member holding nothing, and it
also says how it is written. Every other member the declaration allows to hold
nothing says that instead. A member that really holds a list or a dict says
nothing about its kind, because its row already says how much it holds; one
that holds nothing does say which of the two it would be, because its row then
says only that it holds nothing.

A node that is not a value says nothing here, because its row already says
which kind of container or which class it is. What it may still say is that the
class above it can leave it out of the file.

What a validator would have added — a range, a set of allowed values — stays
out permanently (section 11). The names of an enum are the type of the member;
a range is a rule about it, lives inside a validator, and is therefore
explained by the application in words or not at all.

The names are **appended** to what the application said rather than used where
it said nothing, because writing them in two places is how one of the two comes
to be wrong. It is the **summary** of the enum docstring and not the whole of
it, because the rest is usually notes for whoever writes the application.

The description mapping is `Descriptions` (section 2.6), that is
`Mapping[ConfigPath, str]`; `ConfigPath` is a hashable tuple of `str`, so a
mapping is the natural type rather than a list of pairs. Absolute paths only;
no recursive plain-string key selector. The literal `'['` step keeps its
`config_as_json` meaning of "every list element or every dictionary value at
this point", which keeps repeated `LIST_ELEMENT` and `DICT_VALUE` nested
configs from forcing the application to repeat itself per index or per key.

**A selector says `'['` at each step it has to**, to the bottom of the shape
this library is written for: a list of objects each holding a dict of more of
them is reached by `('outputs', '[', 'parts', '[', 'width')`. A description
that names every step still wins where both address one node, so one element of
a repeated object can be singled out while every other keeps the general text.

Two deliberate divergences from `serialize_converters()`. Description paths
**cross nesting boundaries**: converters stop at child-owned subtrees because
each nested config serializes itself, while the application should not have to
know where the nesting boundaries fall. And overlapping selectors resolve in
favour of the more specific one rather than raising, because a wrong
description is a cosmetic bug and refusing to open the editor over one is not.

**Which of two selectors is the more specific one** has to be said, because two
selectors of the same length can both address one member. A step that names a
key is more specific than the `'['` step, and an earlier step decides before a
later one, so `('a', 'b', '[')` wins over `('a', '[', 'c')` for the member
`('a', 'b', 'c')`. Two *different* selectors can never tie. Nothing is
validated: a selector that addresses no member is simply never used.

### 4.4 Showing and hiding the explanations

Explanatory text costs a line per member, and a user who knows this
configuration by heart wants it back. So there is one toggle for all of it, its
state belongs to the model, and both backends read it there — the same rule
that holds for the marks, the title and the messages: two user interfaces that
disagreed about whether they were explaining themselves would be worse than
either behaviour.

What the toggle covers:

- **shown** — the whole class docstring, and the description of every
  described member below that member
- **hidden** — the summary of the class docstring, and nothing else

The summary survives hiding because it is one line for the whole configuration.
The editor **starts with the explanations shown**: an application that took the
trouble to write a description mapping wrote it to be read.

A member the application said nothing about is shown without a description
rather than with an empty one, and a class with no docstring of its own is
shown without a label. Both are principle 4 of section 3, and both mean the
backends create no widget at all for what can never have anything in it.

**The toggle is one action, and each backend says so in its own way.** A button
that said "Explain" while the explanations were already there would be offering
something that has been done. Tk has a button row, so it gets a tick-box: one
text, true in both states. Textual has a footer of key bindings and no button
row, so its action is *renamed* — "Explain" while they are hidden, "Hide
explanation" while they are shown — and the same name reaches its palette.

### 4.5 Telling the kinds of text apart

Once the explanations are on the screen, most of what is there is not the
values. A value is what the user came to change, a description is text about
that value, and a refused validation is something to act on. They are told
apart by colour.

**What kind each piece of text is belongs to the core, and what colour a kind
is belongs to each backend.** `Emphasis` is that vocabulary: `MUTED` for text
about the values and for a state that has not been reached, `ATTENTION` for
something that has happened to a member, `WARNING` for a remark about the input
file, and `GOOD` and `BAD` for what the application accepted and refused. There
is deliberately no member for ordinary text: the values and their names are
left alone, which makes them the most legible thing on the screen. The pair
that earns the vocabulary is a description and a refusal sitting one below the
other under the same member (section 6.5).

The decisions that depend on the state of the model — what the validation, the
saving and what one nested object is on its own are shown as — are functions of
the core, because they are the ones a backend could otherwise answer
differently. Whether a save succeeded is not readable from its message, which
is why `EditModel.save_outcome` exists beside `save_message`. All three have
the same three states, and `MUTED` for the one that has not been reached is
what makes them read as the same kind of answer about three different things.

Colour itself cannot be in the core: Textual names colours of its terminal's
theme and follows it into a dark mode, Tk has no theme to ask and needs colour
values, and neither can be expressed in the other. Each backend therefore has
one table from `Emphasis` to what its own toolkit understands.

**What a light or a dark background does to that** is answered for Textual and
open for Tk. Textual's theme colours are right in both, because the terminal
decides which theme is in use. Tk gets colour values chosen for the light
window it is given; a Tk that a platform has put into a dark mode would want
other values, which is a theming decision of the kind section 9 is for and is
left until an application asks for it. What is not left is the legibility of a
**field**, which states its own background, text and caret colour.

### 4.6 A configuration bigger than the window

A configuration of any interesting size does not fit a window, and with the
explanations shown it fits one even less. So the editor scrolls, and what
scrolls is **the label, the docstring, the load message and the members**. The
search of section 4.10, the validation verdict, the saving line and the buttons
or the footer stay where they are, because they are what a user reaches for
after editing — and a search whose field scrolled off the window would be no
use at all to a configuration this section is about.

The size of a window is the one thing neither backend can leave to the model:
Textual gives the body the height that is left over, and Tk has no scrolling
frame at all and needs the canvas, the scrollbar and the frame on the canvas
that this amounts to. Three constraints of the Tk side, none of them obvious:

- **The part that does not scroll is packed first.** Tk gives each child the
  space it asks for in the order they were packed, so packing it last would lay
  the verdict, the saving and the buttons below the bottom edge of any window
  too short for everything, where no scrolling could reach them. It is created
  second, so that the widgets are still created in the order they are read in.
- **The size the editor opens at has to be said.** A canvas asks for a width
  and a height of its own that have nothing to do with what is on it, so the
  body is measured and the canvas asks for that, up to the size of a window.
- **A paragraph has to be told to wrap.** A Tk label neither wraps nor shrinks
  of its own accord: text wider than the window is cut off. Every text of the
  editor that is a paragraph follows the width it is given; the mark of a
  member is the one that does not, because it belongs beside its field on one
  line, and a narrow window squeezes the field rather than the mark.

Textual needs none of those three: it wraps, it shrinks, and its footer is
docked. What it needs instead is that **everything on a row is a compact
widget**: a field of Textual's own accord is three cells high and grows its
border back when it is given the focus, so on a row of one cell the text of the
field the user is typing in would be laid out under the row below it. Compact is
what takes that border away in every state, and what is left to say that the
cursor is in this field and not another is its background.

**Testing this needs a window that is on the screen.** Tk lays out the widgets
*inside* a frame only once the window has been mapped, so a withdrawn window
can say where the frames are and not what is in them. The rules above are
therefore tested where they are decided — the packing order, the size the
canvas asks for, the line width a label follows — and one test that maps a real
window and measures the lot belongs to category 3 of section 10.2.

### 4.7 Folding a node away

A configuration of any size does not fit a window (section 4.6), and a list of
two hundred elements fills one on its own. So a node that holds rows can be
folded to its one summary line and opened again, and **which of them are folded
belongs to the model**, by the same rule as the explain toggle of section 4.4.
Every row carries whether it is folded and whether it is shown, so that neither
backend works out for itself what folding hides. What can be folded is **a node
that holds rows** and not "a container", which makes a nested configuration
object one of them as well.

**Folding a node also asks every configuration object at or inside it about
itself** (section 6.2). Opening one asks as well: changing how much of a node
is shown is the moment the user is looking at it.

**A region and not the one node that was folded.** A list and a dict have
nothing to say about themselves, so asking only the node that was folded would
ask nothing at all where the member holds several configuration objects. What a
fold answers is not *what is this node* but *what is being hidden*, and what
such a container hides is every object in it. What it finds is put on their
rows. A container of plain values is asked nothing.

**The editor opens with a container open unless opening it would flood the
window.** A container is folded at the start when the rows it would add are
more than `OPEN_AT_MOST`, counting everything inside it and not only its direct
children. It is a number the editor chooses for itself and not a setting, by
section 9.6.

**Two ways of asking for it, and they answer different questions.** A control
on the row of each container folds that one; one action of `Settings` folds or
opens all of them at once. The action folds while anything is open and opens
everything once nothing is, so a press always changes something, and each
backend names it for what the next press will do — Textual by renaming the
action and Tk by renaming a button rather than by a tick-box, because a partly
folded configuration is neither of the two states a tick could show.

**A configuration with nothing to fold is offered nothing**: no action, no key
and no column for the controls, because the column would be width taken from
the values for nothing.

**A backend that shows the model once asks a third thing**, and it is not the
toggle: `open_all` opens every container, because what the toggle answers —
what does the next press do — belongs to a session that goes on. It takes
`no_more_folding`, which also stops a container that appears later from being
folded away: such a program validates the buffer before it shows it, a pass can
create a container (section 4.8), and a new large one would otherwise be folded
after the one moment at which anything is shown. It is `--unfold` of section
8.3.3. Folding by hand still works afterwards.

### 4.8 A validation pass can change how many rows there are

`ListOrderingValidator` sorts a list and removes its duplicates, and a member
validator returns the value that is stored back into the member (section 6.4).
So a pass can leave the model with other rows than it had: the value the user
typed into may be gone. The model therefore **builds its rows again** from the
values the pass accepted, carrying over what each surviving row knew — what it
is compared against, what a validator did to it, and whether its container is
folded.

**Both backends check the paths and build their widgets again when they
differ**, because neither can write into a widget for a value that is not in
the buffer any more. They leave the widgets alone whenever the paths match,
which is every ordinary refresh, and that is what keeps the focus in the field
the user is typing into. It is also the machinery section 4.9 needs.

### 4.9 How many things a member holds

A member is a list or a dict because **how many** of them there are is a
decision of whoever configures the application. An editor that could change
every one of them and add none would be refusing the decision that the shape of
the member exists to allow, so a container can be given an element, one of its
elements can be taken out, and an element of a list can change places with a
neighbour.

**A new element is copied and never invented**, from one of exactly two places,
both of them the application's. Where the class declares that every element of
a list or every value of a dict is a configuration object, the declaration
names the class and a new element is one object of it holding the values it
declares — which works for an *empty* container. Where it declares no such
thing, the values the class declares for the member itself are the pattern: the
first element of them, and failing that the first element the member holds now.
That fallback makes a member the class declares nothing for extendable as soon
as a file has put something in it.

**Where no value says, the declared type of the member does.** `list[str]`
says that an element of that list is text, and the empty text is the one value
of that kind that says no more than which kind it is. It is asked last, after
both of the places above, because a value the application wrote says more
about what belongs in that list than its kind does. It is not an element
invented out of nothing: the kind is the application's, read from the
annotation it wrote, and only the *emptiest value of that kind* is this
library's.

A member with none of the three is the one case section 11 puts permanently
out of scope. It is a narrow case now: a list member with no annotation at
all, or one annotated with something the editor cannot make an empty value of.
Such a member says so and offers removing and moving.

**What cannot be done is said and not left to be discovered.** Three kinds of
dict cannot be given an entry, for three different reasons, and each says which
below its own row:

- an ordinary dict member, because `config_as_json` checks such a member
  against the keys its class declares — `Config.check_dict_parse` does it while
  parsing — so a dict that gained or lost one would be refused by the
  configuration class itself. Confirmed against the implementation of
  `config_as_json`, and it is why a dict is offered an entry or not according
  to the key policy its class declares rather than because it is a dict. The
  declared type of the member does not change this and cannot: `dict[str,
  int]` says what a new value would be and nothing at all about whether the
  class would accept the key beside it, and the check is what refuses it. That
  is the whole difference between a dict and a list here, and it is why the
  declared type unlocked the empty list and not the empty dict.
- a member of `_unchecked_dicts`, whose key policy the application defines with
  validators of its own. Out of v1 scope.
- a `DICT_VALUE_BY_KEY` member, where one named key holds an object and the
  others hold ordinary values. Out of v1 scope.

That sentence is **explanation and not a refusal to act on**: it says what this
member is, so it is `Emphasis.MUTED`, it sits below the member with the
description, and the toggle of section 4.4 covers it. Nothing is
half-supported: a node that cannot be given an element gets no control at all
rather than one that refuses every press.

**A member holding nothing is grown by being given a value**, whether that
value is a configuration object or an ordinary one. A declared member holding
no configuration object is given one; a member the declaration allows to hold
nothing is given the value of its kind that says no more than which kind it is
(section 4.2). The two are the same pair of controls, because they are the
same question one step apart.

**How the class writes such a member decides nothing here.** One that
`_omit_none_from_json()` names is left out of the file altogether and keeps a
row all the same (section 4.1), so clearing it is not a way of losing it: the
row then says that the member holds nothing and offers to give it something
again. That is what makes such a member reachable at all, and it is the case
that matters most, because a file the application ships holds no key for a
member that is usually absent.

**A member the editor cannot make a value for is offered nothing**, and there
are two of those. A member whose kind nothing says has one state rather than
two and stays the field it was (section 4.2). A member declared to hold a dict
says why it cannot be given one, which is the first bullet above: the same
check refuses the empty dict written for a member that holds none.

**Where an object is added, an object is made.** The tree finds the nested
configuration objects by walking the real objects (section 4.1), so an element
that existed only in the edit buffer would be shown as the dictionary it
serializes to, with the member order of nobody and the parse converters of
nobody. So the model's own configuration object, which is the copy the caller
never sees, gains the object as the buffer gains its values. Principle 5 of
section 3 is untouched: it is the editor's copy that changes.

**What the editor holds about a node is held under the path of that node**, and
an element of a list is addressed by where it is, so a removal or a move takes
all of it along: what each row is compared against, which containers are
folded, and what each object said about itself. Without that, removing the
first element of a list would report every element after it as edited by a user
who touched none of them.

**A change of the elements is not a validation pass**, and the rows say so: a
row that a validation pass created is marked as one a validator wrote and a row
the user added is not. What the application makes of what was added is the
ordinary verdict.

**Where the new entry of a dict is named is the user**, because nothing else
knows. Each backend asks in the way its own toolkit asks a question — a dialog
in Tk, a modal screen in Textual — and a key the dict already holds is asked
about again rather than allowed to take the place of what is there. A list is
never asked, because an element of a list is addressed by where it is.

**The controls sit at the end of the line of the node**, unlike the fold
control, which keeps a column clear on every row. There is no alignment to
keep, so a node that offers none of them costs the values no width at all.

### 4.10 Looking for a member

A configuration that does not fit a window (section 4.6) is one where folding is
only half the answer: the other half is looking for the member you want. So the
editor has a search, and **what is being looked for is state of the model**, by
the same rule as the explain toggle of section 4.4 and the fold state of section
4.7 — two user interfaces of one application that were looking for different
things, or looking in different places, would each be right about a different
search.

**It is a field that stays, and not a question that is asked and gone.** A
search is a text that is changed a character at a time with the answer moving
under it, and four controls beside it that change what it reaches; a dialog
would have to be reopened for each of those. It searches on every change of the
text, which is what makes the field worth its place.

**What is found is reachable, or it was not found.** A match inside a folded
container opens every container that hides it — the node itself is left as it
is, because a folded container is a row of its own and the row the user presses
— and each backend brings the row into view, which is the canvas in Tk and
`scroll_visible` in Textual. Opening a container is the moment at which the user
is looking at it, so a search that opens one asks every configuration object
there about itself, exactly as folding does (section 4.7); a search that opened
nothing asks nothing.

**Typing brings the answer into view and moves nothing else.** The cursor stays
in the search field while the user is typing in it. Pressing Enter there, and
pressing the find next key, are what say *I have found it*: those put the cursor
in the field of what was found, so it can be typed into at once. A node that is
not edited in a field — a list, a dict, a nested configuration object — is only
brought into view, because there is nothing there to type into.

**Which node the search has got to is held as a path and not as a place among
the matches.** A validation pass can leave the model with other rows than it had
(section 4.8), so a place would be a different node afterwards; a path that is
gone is simply gone, and the next press starts again from the top. An element
that changed places takes the search with it, exactly as it takes its fold state
(section 4.9).

**Four independent answers say where a search looks**, and the defaults are what
a person looking for a member wants without being asked: the path *and* the
value, the case ignored, and a part of one of them enough.

- The **path** is the whole path and not the name alone, so `ports.http` finds
  that one value and `ports` finds the member and everything in it. It is also
  the notation the verdict names a refused node in (section 6.5), so what a user
  has just read is what they can type.
- The **value** is the text the field shows. Only a node that has a value of its
  own is looked in for one: a list, a dict and a nested configuration object
  each have their value on the rows below them.
- The **case** is ignored unless matching it is asked for, which is the
  comparison `config_as_json` makes for the name of an enum member.
- The **whole** of the text has to match once that is asked for.

**What each of the four means is the core's words**, for the reason the type of
a member is: two backends explaining one control two ways would be explaining
two different controls. What each backend owns is the label on that control —
one or two characters, since the width of that row belongs to the field — and
where the explanation is put, which is a tooltip in both toolkits and the only
place a label that short has to say what it is.

**Tk has no tooltip**, so the Tk editor draws one: a label with a line round it,
put over the window the control is in and not in a borderless window of its own.
A window of its own is what a toolkit with a tooltip does, and macOS rounds its
corners and gives it a shadow — with a radius about half the height of a line of
text, those corners eat the first character and the last. A label inside the
window is drawn by Tk and by nothing else, so it is a rectangle with sharp
corners on every platform and every version of Tk, and it cannot outlive the
window it is in. What that costs is that a tooltip cannot reach outside the
window, so it is kept inside it and its text is wrapped. The control that goes
to the next member found explains itself the same way, because it carries the
arrow every editor draws for that rather than the two words it stands for.

Turning both places off is the one combination that can never reach a node, and
it is said as what it is rather than as *no member matches*: nothing was
compared with anything. That is a fourth thing the line about the search says,
beside where the search has got to, how many nodes it reaches and that it
reaches none.

**The four are session state and not `Settings`.** They are what the user is
doing now, not what the application knows and the editor cannot find out, which
is the line section 9.6 draws.

## 5. Loading

### 5.1 The loader protocol

The application may need to pass constructor arguments this library knows
nothing about. The loader protocol solves that by having a **closed**
signature: the editor passes only the four things it owns, all keyword-only,
and anything else is bound before the callable reaches the editor.

```python
class ConfigLoader(Protocol):
    """Construct the application's Config object for the editor."""

    def __call__(self, *, from_json_data_text: Optional[str] = None,
                 from_json_filename: Optional[PathOrStr] = None,
                 ok_to_use_defaults: bool = False,
                 stderr_file: TextIO = sys.stderr) -> Config:
        """Construct one Config object from the given JSON source."""
```

This is `config_as_json.ConfigFactory` plus the one parameter it lacks, which
gives factory-constructed configurations the load-policy control they cannot
get through `ConfigFactory` at all. There is no parameter for the hook that
reports automatic changes, because `config_as_json` 1.5 makes that hook
something every configuration object has (section 5.3).

When no loader is supplied, the editor derives one from `type(config)`, reading
`inspect.signature()` to decide what that class can be told. The name of the
JSON text is what that is for, because more than one name for it is in use
(section 8.3.4).

**The derived loader is published**, as `derived_loader`, because an
application that needs one usually needs exactly this with one argument of its
own bound into it:

```python
loader = derived_loader(partial(TeamConfig, KNOWN_TEAMS))
```

It reads the signature of whatever it is given, and `functools.partial` over a
class has one. Writing the protocol out by hand stays the door for anything
this cannot express, which in practice means a class chosen by looking at the
JSON.

**Reading a file and the declared defaults are what need the loader**, which is
what makes it affordable: section 6.1 does not construct the class at all, so
an application with no loader is no worse off anywhere else. The second of the
two is section 4.9's — the values a class declares are what a new element of an
ordinary list is copied from. A class the editor cannot construct loses that
one offer.

**A loader answers a call with no JSON source.** That answer is the
configuration the editor edits when it was given no file, so a loader that
chooses its class by looking at the JSON has to name the class it uses for a
configuration that does not exist yet.

**A loader may choose the class**, and one rule makes that work: the class is
chosen when the file is loaded, and the session then edits that class, because
the rows, the descriptions and the marks are that one class's. A value that
would select another class is caught by section 7's question at save time.

**A loader that ends the process is turned into a refusal.** `config_as_json`
ends the process for a file it cannot make sense of, so a loader written around
it does too, and inside an editor that would cost the user the whole session.
Every call the editor makes to a loader goes through one function, which turns
`SystemExit` into the `ValueError` that every caller already reports.

**`Config.__init__` takes no `ok_to_use_defaults`.** Confirmed against the
implementation of `config_as_json`: the parameter belongs to
`Config.parse_json()` and `Config.read()`, and `__init__` calls both with the
default `False`. So the derived loader has one path for both policies:
construct the class with no JSON source, which leaves it holding its declared
defaults, then call `parse_json()` with the `ok_to_use_defaults` the policy
asks for.

The editor also reads the file itself rather than passing a file name on to
`Config.read()`, which calls `file_must_exist()` and therefore ends the process
with `sys.exit(1)` when the file is missing; an editor has to say so and stay
alive. Reading the text here is also what section 5.3 needs for its comparison
and what section 5.2 needs to know which keys the file contained.

Nested configs need nothing from the application: `nested_configs()` already
provides each nested `config_type` and its optional `factory_function`. One
root loader is the whole contract.

### 5.2 Load policy

```python
class LoadPolicy(Enum):
    """Policy for declared keys missing from the input file."""

    STRICT = auto()
    DEFAULTS = auto()
    STRICT_THEN_DEFAULTS = auto()
```

`STRICT_THEN_DEFAULTS` is the default: load strictly, and on failure retry with
`ok_to_use_defaults=True` and tell the user that defaults were needed. The
application can override, because whether a partially specified file is
acceptable is an application decision.

**The retry rescues only one of two failures.** `ok_to_use_defaults` governs
*missing* keys only. `Config.check_key_match()` raises `KeyError` both for a
missing required key and for an **unknown** key in the file, and the retry does
not help the second case — nor should it, since an unknown key is a typo or a
file from a newer version and discarding it would lose data.

**That is also how the two are told apart.** A retry that succeeds says the
file was merely incomplete, and a retry that raises `KeyError` again says there
is an unknown key. Nothing reads the text of a diagnostic to classify a
failure, so the classification is unaffected by ROCF renaming a key before the
check runs. `STRICT` runs the retry as well, because it needs the same
distinction to pick a message; there the retry never opens the file.

The outcomes, each with a message of its own:

- missing keys → "your file was incomplete; these values were filled in
  from defaults" (plus the per-field *filled from default* flag). Under
  `STRICT` the same file is refused, with its own wording.
- unknown key → "your file contains a key I do not recognise"; the file
  cannot be opened
- `ConfigBadJson` → the file cannot be read as configuration. This covers text
  that is not JSON *and* JSON whose values cannot be converted, an enum name
  that names no member being the case that arises in practice, since
  `parse_converters()` runs inside `json.loads()`. The diagnostics say which of
  the two it was. A field that is being *edited* reports the enum case for
  itself (section 4.2); a file that cannot be opened is not a field the user
  can correct.
- **values a validator refuses** → the file cannot be opened. `parse_json()`
  ends with `validate()`, so there is no valid object to build a model from. It
  is a refusal rather than an editor opened on the file's own values because a
  member validator returns the value stored back into the member, so a load
  that stopped part way through leaves it unknown which values were already
  rewritten. The user is told to correct the file in a text editor first.
- **a file that cannot be read, or that is not UTF-8 text** → the file cannot
  be opened. This is the editor's own message, because `Config.read()` would
  end the process (section 5.1).
- **a class the editor cannot construct** → the file cannot be opened, and the
  message names the class. Such an application supplies the explicit loader of
  section 5.1 instead.

The per-field *filled from default* flag is what the key check of the parse was
not given. A load that was allowed to use defaults cannot be asked afterwards,
and the keys of the file do not answer it either, because ROCF may have renamed
a key into a member — computing the flag from the keys of the file would claim
that a renamed member had been filled in from a default. So the parse is asked,
by a copy of the loaded object whose `check_key_match` records what it was
given and stops the parse there — the same borrowing as section 6.3, and
stopping is what keeps the application's own validators running once, on the
object that is really being edited.

### 5.3 Making automatic changes visible

Reading an old-format file applies `ReadOldConfiguration` rules, so the data
presented for editing can differ substantially from the file on disk. The user
must be told, or the editor looks broken.

**The comparison is the mechanism**: load the file, re-serialize the resulting
config, and compare that against the raw file text. Any difference means the
load changed something. It needs nothing of the configuration class and covers
all three sources of surprise — ROCF migration, normalization during parsing,
and values filled in by a permissive load. It is the mechanism rather than a
fallback because the second of those is recorded nowhere: a value a member
validator rewrote is not an automatic change of the kind `config_as_json`
reports.

**What the load recorded says why.** `Config.auto_change_hook()` is the hook of
the most recent parse, and `hook.changes` holds one `RocfChange` per automatic
change, saying what kind of change it was, which path of the file it consumed
and which path of the configuration it produced. That is what no comparison can
know: a renamed key is simply gone from the file.

The editor must **construct** the configuration rather than receive an
already-loaded one, because the load policy of section 5.2 is decided while the
file is read; but the records reach it whatever it constructs.

**Nothing is opted into and nothing is passed.** `Config.__init__` creates a
hook when the application names none, keeps by reference the one it is given,
and publishes both through `auto_change_hook()`. So a class that declares
`auto_ch_hook` and hands it on is reported on exactly as fully as the ordinary
three-keyword constructor shape that does not, and `ConfigLoader` has no
parameter for one (section 5.1). Keeping it by reference is what
`config-as-json` 1.5 promises: a copy of the configuration carries a copy of
the hook, so a later parse cannot disturb what the load recorded.

**A record reaches a member or it reaches the message.** That one rule places
all of them. A record that produced a member explains that member and is shown
at it, so the mark says *read from the older key `title`*. A record that
produced no member consumed a key of the file that nothing here holds, and
joins the keys the message says saving leaves out — and a key that a member did
receive is taken *out* of that list, because the comparison put it there and
the record knows better. A record that did neither supplied a value this
configuration does not write, and the row such a member has says that it holds
nothing rather than saying what was supplied, so the message names the value
and it is named nowhere else.

**The records are versioned, and the fallback is text.** `config_as_json` steps
`DATA_STRUCTURE_VERSION` whenever what it records changes, and asks a reader to
declare the version it was written for. A future version that records something
else is not worth refusing a file over: the comparison still finds every
changed member, and what the records would have added is taken from
`print_changes`, which is version independent by contract. That text is shown
as it stands and is never parsed.

**The comparison is canonical.** `config_as_json` writes the keys of a
dictionary sorted, so the values are compared with their dictionary keys
sorted. Everything else is compared as it is written, which is what tells `1`
from `1.0` and from `true`, exactly as section 4.2 requires of the *edited*
mark.

**A class that cannot write itself is left as it is.** The comparison reads
what the load would write, so such a class has nothing to compare — and it
cannot be shown at all. The refusal stays where section 8.3.4 puts it.

## 6. Validation

### 6.1 Whole-configuration validation

`Config.parse_json` runs the entire chain: key matching, recursive dict-shape
checks against defaults, `parse_converters()`, nested-config construction, and
then `get_validation_plan()`. So a validation pass is:

> serialize the edit buffer to JSON text, apply it with `parse_json` to a deep
> copy of the configuration object of this session with a captured
> `stderr_file`, and catch `KeyError`, `ConfigBadJson`, `TypeError`,
> `ValueError`, `InvalidConfiguration`, `InvalidConfigurationValue` and
> `InvalidConfigurationType`.

The user sees exactly the diagnostics the application would see at load time.
There is no second validation implementation and no way for the editor to
accept something the application later rejects.

**The pass is asked for and never done for the user.** Tk has a Validate button
and Textual a key, because an editor that answered a question nobody put would
be reporting a mistake that is not one yet. The non-interactive backend has no
later moment in which to be asked, so it validates once before it prints.

**The class is not constructed, and it does not have to be.** Declaring the
members is the whole of what a constructor does before `parse_json`, and a copy
has that already. Copying instead of constructing is what makes two kinds of
class editable at all: one whose constructor needs an argument this library
knows nothing about, and one with no JSON text parameter at all. Copying is
also what keeps a session on one class where a loader would choose another
(section 5.1), and what gives the probe of section 6.3 the object it needs.

### 6.2 Subtree validation, and why folding is the natural trigger

A nested config subtree can be validated **in isolation**, by applying that
subtree's JSON to the nested object itself. **The object is copied and not
constructed**, for the same reason as in section 6.1, and so a
`factory_function` that answered with a subclass is asked as the subclass it
really is.

That makes folding and validating the same operation: when the user folds a
nested config away — or opens it again — the editor asks that object about
itself and shows the result as a badge on its row.

Two validity levels result, and the UI must distinguish them:

- **subtree-valid** — this nested config is internally consistent;
  cheap, local, available on fold
- **config-valid** — the whole tree passes, including
  `WholeConfigValidator` and `ProjectedWholeConfigValidator` steps on a
  parent that relate members *across* a nesting boundary; obtainable
  only at the root

A subtree can be valid while the root is not. That is the honest state and both
are shown.

**The badge is worded so that it cannot be read as the other one.** It says
*valid on its own*, and the qualification is the whole point: a rule of the
class above relating two objects across the boundary between them refuses the
configuration while saying nothing against either object. Whether the file can
be written is the verdict line of section 6.5. The other direction needs no
qualification, because an object its own class refuses cannot be part of a
configuration that is saved.

**A pass the class accepted answers for every object at once**, so none is
asked again: `parse_json` builds and validates each nested object while it
reads the buffer. The walk therefore runs only when the whole buffer was
refused. **The innermost object is asked first, and one holding a refused one
is not asked at all**, because asking it again would report one mistake once
for every object it happens to be inside.

**What a nested object refuses about no member of itself is shown at that
object**, and not in the block below the members, because it is about the
object and the object is a node with a row. The block keeps what is about no
node at all, which is where a rule relating two objects across a boundary
belongs.

**A state that has not been asked for is shown as nothing**, the third state
that `verdict` and `save_outcome` also have. It is taken back whenever anything
inside that object is edited, which is a different lifetime from the verdict of
the whole configuration: that one is dropped by an edit anywhere.

**What the object refused is kept with the state and never apart from it.**
Keeping the state and throwing the sentences away would leave a folded object
saying that something was wrong with nothing saying what. That third lifetime
is why they are the buffer's and are stamped onto the rows rather than carried
by them, beside the fold state: the rows are built again after every validation
pass, and an answer outlives the rows it was given about. A folded object shows
the state and not the sentence, because the member the sentence is about is one
of the rows that folding hid.

**A list or a dict of such objects carries the same state, about them.** It is
no configuration and can say nothing about itself, so the words differ: it is
*valid inside* and *refused inside*, refused as soon as one object in it is,
valid once every one has been asked and accepted, and unasked while any is
unasked and none is refused. That row is the only one a folded container leaves
on the screen: a user who folds a member to get it out of the way is very much
asking to be told that something in it is wrong.

### 6.3 Field-level attribution

Whole-config validation alone would present the user with one block of
diagnostics. Better attribution is available without introspecting any
validator's constraints, because two things are public:

- `MemberValidationStep` is a dataclass with public `member_names` and
  `validator`
- `MemberValidator.validate_member(config, member_name, member_value,
  stderr_file)` is a public abstract method

So, given a complete candidate config, the editor runs an individual member's
validators and attributes each failure to a specific field. Custom application
validators work identically. `validate_member` receives the whole `config`
object and may inspect other members, so a complete candidate must be built
first; individual fields cannot be validated in isolation.

**The candidate this needs cannot be held the ordinary way.**
`Config.parse_json()` ends in `validate()`, which raises at the first step that
refuses — so the object that could say which member was refused is exactly the
object that a refusal keeps the editor from ever holding. A copy whose
`get_validation_plan` returns nothing is that object: everything else the parse
does still happens, and only the plan is left out, which is what the walk then
applies itself. The plan is asked of the class and not of the object, because
it is the object that has none.

**The buffer is parsed and not assigned**, because the whole parse chain runs
on the way in: the keys are matched, the dict shapes are checked against the
defaults, the parse converters run, and the nested configuration objects are
built. Assigning the buffer member by member would mean the editor applying the
converters itself, and would put a plain `dict` where a nested `Config` object
belongs.

**The method is left out on the object and not on a class.** It is one
attribute of one copy rather than a throwaway subclass, for two reasons: it
works for a class the editor cannot construct, which a subclass of it does not;
and it leaves the real method where the walk needs it. `parse_json` does not
mistake the replacement for a member, because it counts the attributes of the
object that are not callable. The same borrowing answers what the declared
defaults filled in (section 5.2), where the method left out is the key check.

**The walk differs from `Config.validate()` in two deliberate ways.** A member
that is refused is recorded and the walk goes on, so that every member the user
has to correct is named at once; and a step that is about no single member is
applied only while no member has been refused, because that is the only case in
which the real pass would have reached it. A member that is already refused is
left alone by a later step that names it, so what is reported about it is what
the real pass would have reported.

### 6.4 Validation mutates

`Config.validate()` documents that "a member validator returns the value
that shall be stored back into the member, even if that returned value is
`None`". Validators such as `StrValidator(best_match=True)` and
`StrCaseChangeValidator` rewrite what the user typed.

A validation pass is therefore **not read-only**. After every pass the editor
refreshes its buffer from the validated object and sets the *changed by
validator* flag on each rewritten field. The rewrite is accepted silently but
is visibly highlighted; silently altering text the user just entered without
showing it would be the worst available behaviour.

### 6.5 Where a refusal is shown

What is refused about one member is shown **at that member**, and what is
refused about no single member stays in the block below them. The verdict line
names the members it was about, because a configuration of any size does not
fit a window (section 4.6).

**What is refused is addressed by a path and not by a name**, because a value
inside a list or a dict is a node of its own and two of them can share a name:
a dictionary key called `cpu` must not be told what the application said about
a member of that name.

**What a member validator refused is about the whole member**, because the
whole member is what it is given, so it is shown at the member and never at one
value inside it: `validate_member` receives one member name, and an editor that
guessed which value inside it the validator meant would be inventing. What one
*value* can be refused for on its own is the conversion of section 4.2.

The same sentence is therefore not on the screen twice: what the attribution
explained is taken out of the block, and the block keeps what it could not
explain — a whole-configuration validator, a key that does not match, text that
is not JSON, a class the editor cannot construct.

One member can have three things wrong with it: its text may mean no value of
it at all (section 4.2), the application may have refused the value it holds,
or the nested configuration object that owns it may have refused it (section
6.2). **The first is preferred when more than one is there**, because a value
that does not exist yet has to be corrected first, and the verdict comes before
what one object said because it is the more recent of the two. They also live
for three different lengths of time, which is why they are kept apart: the
first stays true until that member is edited again, the second is dropped as
soon as anything in the buffer changes, and the third as soon as anything
inside that one object does.

A refusal is **not** covered by the explanations toggle of section 4.4. A
description is what a user who knows the configuration wants out of the way; a
refusal is the one thing on the row that has to be read. It is shown *below*
the description of the same member, so that a line which comes and goes moves
nothing above it, and it is `Emphasis.BAD` where the description is
`Emphasis.MUTED`.

## 7. Saving

- **An invalid configuration cannot be saved.** Saving is: validate the
  candidate, and on success call `write()` on it. It is the *same* pass the
  user asks for with Validate, so a validator that rewrites a value rewrites it
  on the way to the file too and the editor shows what was written.
- `edit()` returns the saved `Config` object, or `None` if the user cancelled.
  The caller's own object is never mutated and would otherwise be stale.
- `out_file` defaults to `in_file`. If both are `None` the editor starts from
  defaults and must obtain a destination before it can save. The model reports
  that it has none and the backends ask the user for one; the model invents
  nothing, because a file name is not something a library can guess.
- **Saving leaves the editor open.** A save is not the end of a session, so
  Save answers "is there anything to write" and the session ends only when the
  user closes it. `edit()` then returns the object that really reached the
  file, whatever was typed afterwards and not saved.
- **`Config.write()` does validate.** Confirmed against the implementation of
  `config_as_json`: `write()` calls `as_json_string()`, whose first statement
  is `self.validate(stderr_file=stderr_file)`, and it opens the destination
  only after the text exists. So the editor's own gate is belt and braces
  rather than the only guard.
- A destination that cannot be written is a message and not a crash, because
  the alternative costs the user the whole session.
- **What the destination held is kept, and overwriting it is asked about.**
  Section 7.3.
- **Where the application said how it loads, that is asked once more before
  anything is written**, with the very text the file would hold. It is the one
  question a validation pass cannot answer: the pass applies the buffer to the
  class of the session (section 6.1), and a loader that chooses its class by
  looking at the JSON may read the same text back as another class altogether.
  A file the loader refuses, and one it would read as a class the session is
  not about, are both a refused save with a message; `isinstance` is what the
  second asks. An application that supplied no loader is asked nothing.

### 7.1 Draft file (decided against)

This section described an editor-owned **draft file** holding the raw JSON
buffer, as a way out of a long editing session that is still invalid. It has
been decided that no draft file is built, and the reason is the last entry of
section 11.

### 7.2 Closing with something unsaved

Closing writes nothing (section 9.1: quitting is the cancel of this design), so
a session closed with something in the buffer that has not reached the file
loses it. The editor is the only thing that knows there is anything to lose, so
it asks first.

**Whether the user is asked, and what they are asked, belongs to the core**,
because it depends on the state of the model (section 4.5). **How the question
is put belongs to each backend**: Tk has a message box and Textual has a modal
screen.

It is one function and not two. `close_question` answers with the question, and
with nothing at all when there is nothing to ask about, exactly as `load_text`
is empty when the load has nothing to say. Closing then reads as one sentence
in both backends.

**What it asks is `dirty`**, which is already "the buffer holds something worth
saving": a save moves the values the buffer is compared with (section 4.2), so
a session that saved and typed nothing since is not asked, and a save the
application refused leaves the buffer dirty and is.

**Every way out asks**, including the close button of the window: the button,
the quit key and the window all go through one method of the backend, because a
way out that dropped the changes without a word would be the one thing an
editor must not do. The window is only ever the one the backend created
(section 8.2.2).

**Both backends offer the answer that keeps the changes first**, as the answer
the dialog opens on and as the control the screen puts the focus on. Leaving
the question — the cancel key of section 9.1 — is the same as keeping them.

**The non-interactive backend is asked nothing.** There is no session to close
and nobody to answer, so where the core is asked, such a backend's answer is to
discard.

**No `Settings` attribute.** Whether there is anything unsaved is something the
editor knows for itself, and section 9.6 keeps `Settings` for what only the
application knows. Whether *overwriting* a file is confirmed is a different
question (section 7.3).

### 7.3 The file that a save writes over

A save writes over whatever the destination holds, and what it holds is a
configuration somebody wrote. It may be the one this session read a minute ago,
and it may be one another person wrote on another day; nothing the editor can
look at tells those apart. So the file is **kept** before it is overwritten,
and the user is **asked** before it happens. Both are the application's
decision (section 9.6).

**It is once per destination per session.** From the second save onwards the
file being written over is the first save of the same session: keeping it would
push the configuration that was really there one number further from being
found, and asking about it would be asking the user about something they did a
minute ago. The model therefore holds every destination it has written, and
Save-as onto some other existing file is asked about again.

**Kept by renaming, not by copying**, which leaves the previous content whole
under one name or the other whatever happens next. The name is the destination
plus `backup_suffix`, added to the whole name rather than put in place of the
extension: `xx.cfg` becomes `xx.cfg.bak`, and one attribute then expresses
`.old` and `~` as well. `backup_count` above one numbers them from `_1`, which
is the file overwritten last, and each save moves every one of them one number
further back until the oldest falls off the end. One is not numbered, because a
number would say that there are others when there are not.

**Where it happens in a save is the whole of what can go wrong.** It is after
the validation and after the loader has been asked, and immediately before the
write. So a save that is refused for any reason keeps nothing, and a save that
kept the previous content and then could not write says where that content is,
on the line below its own message. A save that cannot keep it writes nothing at
all: overwriting cannot be undone, so the moment at which that is found is the
last moment at which anything can be done about it. A destination that is not a
regular file, a folder being the case that arises, is left to the write to
refuse in its own words rather than renamed out of the user's way.

**Whether the user is asked belongs to the core and how they are asked to each
backend**, which is section 7.2's split. `overwrite_question` answers with the
question and with nothing at all when there is nothing to ask,
`EditModel.overwritten_file` is the file it is about, and each backend puts it
in a dialog or on a modal screen with the answer that leaves the file alone
offered first. The Tk file dialog is told **not** to ask this itself, although
it offers to: a question that one backend put and the other did not would be
the one thing the core owning the question exists to prevent.

**A backend that prints once and returns is asked nothing**, and it writes what
it was asked to write. What it does *not* skip is keeping the previous content,
because that is the model's work and not a question.

## 8. The UI backend contract

The editor is embeddable in an application that already runs its own Textual or
Tk event loop, and the contract is what makes that additive rather than a
rewrite.

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

The `config` argument serves as the schema and defaults source and is the
ergonomic front door; `loader` is the door for applications with constructor
arguments we do not know about. `config` stays required when a loader is given,
because the protocol says a loader answers a call with no JSON source (section
5.1); `load_config` and `EditModel` take the loader on the same terms.

`descriptions` is an optional keyword and not a required positional argument.
An application that describes none of its members is a perfectly good caller,
and requiring the argument would make every call site pass an empty mapping to
say nothing. The same reasoning makes `EditModel`'s arguments after the load
report keyword-only.

The `backend` argument has to be there: the core never imports a user interface
library, so it cannot name one. Each backend package therefore also exports an
`edit` of its own that supplies itself and forwards everything else. Those
wrappers are a signature and one call; if either ever grows a decision of its
own, that decision belongs here instead.

**When a backend has to make its widgets again** is one answer and not two, so
the core gives it: `rows_shape` is the path of every row and whether that row
is a value with a field, and a backend that finds it changed rebuilds instead
of writing the values back. Both halves of it are needed. A validation pass
that normalizes a list changes how many rows there are, and one that answers
`None` for a member allowed to hold nothing leaves the same rows with one of
them no longer a field (section 4.2). A backend comparing the paths alone
would leave a field on the screen for a member that holds nothing, and the
next key typed into it would be refused.

A practical consequence of the split: the backends must stay thin. All three
packages share a single pylint invocation, and this repository forbids
file-level `duplicate-code` disables. If the Tk and Textual trees start
tripping R0801, the correct response is to move logic into the core — tree
flattening, fold state, edit dispatch, dirty tracking and diagnostic
presentation all belong there.

### 8.1 Entry points (planned, not implemented)

An `edit_cfg_json.ui` entry-point group would let backends register themselves
for discovery (`--ui=auto`). It is additive and breaks nothing, and is only
worth building once there is a generic launcher or a third-party backend in the
wild. The programs of section 8.3 are not that launcher: each supplies its own
backend. An `edit-cfg-json` that chose an editor for the machine it was run on
would be that launcher, and the name is kept free for it.

### 8.2 Embedding in an application that already runs a UI

An application that already runs Tk or Textual mounts the editor in a widget of
its own and goes on running its own event loop. Two questions decide the shape:
which toolkit instance the editor attaches to, and where in an existing window
it is placed.

#### 8.2.1 Which instance does the editor attach to?

**It is told, and it never guesses.** Neither toolkit offers a supported
way to ask.

- **Tk.** `TkEditor.run_editor` creates a `tkinter.Tk`, which is a Tcl
  interpreter. A second one in the same process is a second interpreter, and
  widgets, variables, fonts and images cannot cross between them. The toolkit's
  own rule is one `Tk` per process and `Toplevel` for every further window.
  Detecting an existing one means reading `tkinter._default_root`, a private
  name, and then guessing what the application meant by not saying.
- **Textual.** There is one `App` per event loop. `App.run()` calls
  `asyncio.run()` or `loop.run_until_complete()`, so calling it from inside a
  running app raises or deadlocks. `textual._context.active_app` would answer
  the question and is private.

So `run_editor` is the editor that owns a window and a loop, documented as
being for an application that runs neither yet. An application that runs one
already uses the entry point of section 8.2.3.

#### 8.2.2 Where in an existing window is it placed?

**In the widget the application names, and the editor destroys only what it
created.** What differs between the toolkits is what "a window of its own" even
is, so Tk is told which of the two the application wants and Textual has a
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

The editor and not the application creates that `Toplevel`, because otherwise
**every** application that wants a window of its own writes the same five lines
— title, geometry, transient, close protocol, grab — against a toolkit rather
than against this library, and `wizard_tk_bridge`, the library this one is most
likely to be embedded beside, answers the same question with `parent`, `area`
and `modal`. An application that wants its own decisions about that window
makes the window itself and passes it as `area`.

**`modal` is a third thing the application says**, and it is `True` by default.
It is a Tk word and a Tk argument: the editor asks Tk to hold the events of the
application for the window or the frame it built, and gives the grab back when
it closes. Textual has no equivalent and needs none — a pushed screen already
has the terminal, and a mounted panel already does not. A grab is asked for
when the editor is built, which is before the window it made has been mapped,
and whether Tk allows that is a platform question: Aqua does, and X11 refuses a
grab for a window that is not viewable. A refused grab is a non-modal editor
rather than an error, so an application that must be held on every platform
makes its own window, maps it, and passes it as `area`.

The rejected alternatives are in section 11.

#### 8.2.3 It cannot be `run_editor`, so it is a second entry point

`EditorBackend.run_editor` promises to run until the user is done. An embedded
editor cannot keep that promise. Tk could fake it with a nested `wait_window`,
but Textual has no way to nest a second loop at all, and an editor mounted in a
panel of the application's window should not suspend the application's call
stack in either toolkit.

Embedding is therefore a **separate, non-blocking entry point per backend
package**, additive to the protocol rather than a change to it. Each is *one
call*, and it says the same things about a session that `edit()` says:

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
each of the three classes spells them out rather than taking a bundle, so that
a reader of one signature sees the whole of it. The `...` above is this
document being brief and is no part of the code.

**The seven keywords are one function, and it is in the core.**
`edit_cfg_json.editor_model` is the first half of `edit()` — read the input
file, build the model — and `edit()` is that call plus `run_editor`. Without it
the two backend packages would each be reimplementing the loading rules of
section 5, and the three ways of opening the editor would drift apart in what
an `out_file` or a `policy` means. It is public because an application that
writes a backend of its own wants the same half.

`on_close` is how the application learns the session ended; the outcome is
`saved_config`, which the panel and the screen offer beside the `model` it
comes from. `edit()` gains no argument: an embedded editor has no moment at
which it can return what was saved.

**`close` is the application's way out, and it says whether the user is
asked.** The editor's own Close and its quit key are that same call with the
default, so the question of section 7.2 is put in the same words whichever of
the three ended the session. Whether it is put at all is the *application's* to
decide, because only the application knows what it is closing the editor for:
one that is already putting a question of its own has one question too many.

**It answers with nothing, and `on_close` is the whole answer.** A Tk panel
could say synchronously whether it really closed, and a Textual one could not:
its question is a modal screen with a callback. **Closing again once the
session has ended does nothing**, so an application need not track whether the
user has closed the editor already.

**Only what the editor created is destroyed.** The Tk panel destroys the frame
it built inside the given `area`, or the window it opened over the given
`parent`; the Textual panel removes itself, and the Textual screen pops itself
off the application. What the application had on the screen beside the editor
is untouched.

**A screen pops itself**, unlike everything else here, which the editor
destroys and then leaves the application to decide what happens next: an
application that had to pop it would be left with the editor's own empty screen
on top of its own for as long as it took to be told. The application's screen
is therefore back on top by the time `on_close` runs. A screen that is the
*only* screen — which is what `EditorApp` shows — is not popped.

#### 8.2.4 What Textual has to be split into

The Tk backend builds below an arbitrary parent widget, so its panel is a
wrapper. The Textual backend is an `App`, and five things live at App level
that an embedded editor cannot have:

| On `EditorApp` | Why it cannot stay there |
| --- | --- |
| `CSS` | Textual ignores `CSS` on a widget and says so; a widget uses `DEFAULT_CSS`. |
| priority bindings on `self._bindings` | App-level priority bindings fire wherever the focus is. The priority pass walks the whole binding chain (section 8.2.8), so a priority binding on a **widget** still beats the focused `Input`, and only while the focus is inside the editor. That is what embedding wants. |
| `self.title` | It is the application's window title. |
| `get_system_commands` | `COMMANDS` exists on `App` and `Screen`, not on `Widget`. An embedded widget cannot offer palette entries; an embedded screen can. |
| `action_quit` | It ends the application. |

So `EditorApp` splits three ways: `ModelPanel(Widget)` holds the whole body
with its `DEFAULT_CSS` and its instance bindings, `ModelScreen` adds the
header, the footer and the palette entries, and `EditorApp` composes the
screen. One body, so the two backends cannot drift and the CSS and the bindings
exist once. The model title is a label of the panel, which is what the Tk
backend does; the application title is the name of the configuration class.

**The two the application mounts take a configuration and not a model**, and
that is one subclass each: `EditorPanel(ModelPanel)` and
`EditorScreen(ModelScreen)` call `editor_model` on the seven keywords of
section 8.2.3 and hand the model up. The pair with the model stays because
`EditorApp` is given one by `run_editor`. Subclassing keeps that from being two
constructors with a flag, and Textual matches a type selector against every
class name in the hierarchy, so the sheet `ModelPanel` declares for itself
reaches the subclass too.

Three Textual constraints the split rests on, none of them obvious:

- **A screen offers palette entries through `COMMANDS` and not through
  `get_system_commands`.** That method is `App`'s alone, so the entries are a
  `Provider` of the screen, which asks the panel for them. Asking rather than
  holding a table is what keeps the two entries whose name says what the next
  press will do — Explain and Fold all — true when the palette is opened.
- **A widget styles *itself* by its type name.** Textual scopes the style sheet
  a widget declares to that widget and what is inside it, so a class selector
  in it reaches the inside and never the widget the sheet belongs to. The
  sheets therefore leave a mark where a class name belongs and each widget
  fills in its own, which is what `ModalScreen` does with its own name too.
- **The question screens carry their own sheet.** They are screens of the
  application and never a part of the editor widget, so a sheet the panel
  declared could not reach them.

**What the split costs an application that shows the editor and nothing else is
one thing, and it is deliberate.** The footer names the actions of the editor
while the focus is inside the editor, because that is where the bindings are.
Textual focuses the first focusable widget of a screen, which is inside the
panel.

#### 8.2.5 Two rules that hold for both ways of running the editor

- **`EditorBackend` promises a modal editor**, and it does not promise that an
  application can mount the backend as a widget. Mounting is the separate entry
  point of section 8.2.3, and the docstring published in
  `doc/edit-cfg-json_api.md` says exactly that.
- **`EditorWidgets` is told what closing does** rather than deriving it from
  `parent.winfo_toplevel()`. The default is what `TkEditor` needs.

The public surface of both backend packages is `TkEditor`, `TextualEditor` and
`edit`, and none of them means anything different under embedding. That is what
phrasing the protocol against the model buys.

#### 8.2.6 A Tk variable names its parent

`tkinter.StringVar` built without a `master` is created in the **first** Tcl
interpreter of the process, not in the one its field belongs to —
`tkinter.Variable.__init__` falls back to `_get_default_root`. With an
application's root already present, every field's variable would be created in
the application's interpreter while its `Entry` lived in the editor's, so the
field would show nothing and the callback that writes it into the model would
never run. The fields therefore name their parent.

#### 8.2.7 What the Tk keys are bound on

**A bind tag of the editor's own**, put on the widget the editor was built
below and on every widget it created inside it. Binding on the toplevel is
right for a window the editor owns and wrong for one it shares, where the
editor would claim keys across the whole application window.

It is one rule for both ways of running the editor: **the keys of the editor
reach the widget it was given and everything inside it, and nothing else.** A
backend that owns its window is given the window; a panel is given the frame it
built, so it claims nothing of the application.

**The mouse wheel is bound the same way.** A wheel event goes to the widget
under the pointer, which is usually a field or a label inside the body rather
than the canvas that scrolls, so binding the canvas alone would leave the wheel
working over the empty parts and nowhere else.

**Where the tag goes in each list is `Settings.priority_keys`.** Tk offers the
tags of a widget in the order they are in and a handler that answers `break`
stops the walk, so the tag first is the editor before the widget with the
focus, and the tag last is the editor after it. Section 9.1.

**The tag is given up when the editor closes**, because a bind tag is a name in
the Tcl interpreter and outlives the widgets that carried it: an editor taken
off a window would otherwise leave its callbacks, and the model they hold, for
as long as the application runs.

Textual needs none of this, because a widget's bindings already dispatch only
from the focused widget upwards.

#### 8.2.7.1 The two questions that are answered with a no

- **The core does not name the mounting contract.** A `Protocol` for it would
  let a third-party backend implement the same shape, and it is additive
  whenever it is added. The three implementations do not share a shape: the Tk
  one is told a parent or an area and whether to be modal, and the two Textual
  ones are a widget the application mounts where it likes and a screen it
  pushes, neither of which ever hears of a parent. A protocol over things that
  differ in what they are told would be a protocol over one of them with the
  others written down beside it. What they *do* share is the seven session
  keywords, named in the core as `editor_model`. The rest waits for the first
  backend somebody else writes.
- **`Settings` gains no attribute about mounting.** `priority_keys` is what an
  embedded editor really asked for, and it is about keys rather than panels.
  Everything else an embedded editor might have wanted from `Settings` is
  something the editor knows for itself, which section 9.6 keeps out.

#### 8.2.8 Facts checked against the pinned versions

Checked against `textual` 8.2.8 and the Python 3.14 `tkinter` in `./venv`,
because each decides a paragraph above: `App.run` calls
`asyncio.run`/`run_until_complete`; `App._check_bindings` walks
`reversed(screen._binding_chain)` on the priority pass, so widget priority
bindings are honoured; `Screen.refresh_bindings` builds that chain from
`focused.ancestors_with_self`, so a widget's bindings are active only while the
focus is inside it; `active_app` is in `textual._context` and private;
`COMMANDS` is declared on `Screen` and `App` and not on `Widget`, and
`get_system_commands` on `App` alone; `DOMNode.__init__` gives every widget its
own `_bindings`, so a per-instance binding works on a widget too;
`DOMNode.check_action` and `DOMNode.refresh_bindings` are on every widget;
`Widget` warns that a `CSS` class variable is ignored; a scoped `DEFAULT_CSS`
matches the widget it belongs to by its type name and not by a style class the
widget carries, which `ModalScreen.DEFAULT_CSS` relies on as well;
`tkinter.Variable.__init__` calls `_get_default_root('create variable')` when
it is given no master; `Input`, `Button` and `Checkbox` each take a `compact`
keyword, whose rule takes the border away with `!important` and therefore in the
focused state as well; and `Misc.bindtags`, `Misc.bind_class` and
`Misc.unbind_class` are what section 8.2.7 is built on.

### 8.3 A ready-to-run program in each editor package

An application author should not have to write a program to get an editor for
their own configuration class, so each of the two editor distributions installs
one: `edit-cfg-json-tk` and `edit-cfg-json-textual`. They are a product and not
only a development tool: a question about a configuration that is not two
members long would otherwise cost a hand-written example, and any class in
reach answers it instead.

**The core installs no program, and the name it would have installed under is
the reason.** The same command line over the non-interactive backend is worth
having, because it says what a class makes of a file and answers with an exit
code, which a continuous integration job can read. But that is a small utility
for whoever is writing a program on top of this library, and `edit-cfg-json` is
the name of the editor this library is for: a command named after a library is
taken for that library's product. So the utility is
`python3 -m edit_cfg_json.dump`, and the name is left free for the launcher
that picks the editor the machine can run.

#### 8.3.1 The command line owns no logic

`edit_cfg_json.cli` holds all of it — the parsing, the two doors to a class,
the construction, one editing session and the exit code — and `run_cli` takes
the backend for exactly the reason `edit()` does. Each package is then a
program of a few statements. Without that split the two interactive programs
would be near copies of each other, and section 8 answers duplicate code
between the backends by moving logic into the core. It is also what makes the
whole program testable with no display and no toolkit.

Each editor program is reachable as `python -m` on its own package as well, so
a machine whose script folder is not on `PATH` can still run it, and the
utility of the core is reached that way and no other. All three complete their
own command lines with `argcomplete`: the two installed programs through
`register-python-argcomplete`, and the utility through the global completion,
which finds the `PYTHON_ARGCOMPLETE_OK` marker.

#### 8.3.2 The class is told, and never guessed

`--module` names an importable module, `--file` names a Python file and
`--edit-settings` says that the class is this library's own settings; exactly
one of the three is required, and section 8.3.6 adds `--version` to the same
group.

**`--edit-settings` is a third door and not a mode.** It answers the same
question the other two answer — where does the class come from — and `--class`,
`--loader` and `--descriptions` are refused beside it because it has already
said what all three would say. With `-i` it reads a settings file and with no
`-i` it starts from the values the class declares, which is what every class
the editor is given with no input file does.

**What to edit is either a class or a loader**, named by `--class` and
`--loader` in that module or file. At least one is needed and both are allowed:
a class alone is constructed on the values it declares, a loader alone is asked
for a configuration and the class it answers with is the class of the session,
and the two together mean that the loader has to answer with that class or the
program stops. The check is made on the object that is really going to be
edited, and `isinstance` is what it asks.

The class is a named option and not a positional argument, so that the ways of
saying what to edit are symmetric. `argparse` can be asked for exactly one of a
group of options and not for at least one of them, so the refusal of a command
line that names neither a class nor a loader is written by hand, and so is the
refusal of one that names either beside `--edit-settings`.

**A loader cannot be finished off from a command line**, and the refusal says
so: whatever it needs beyond the four keyword arguments of `ConfigLoader` has
to be bound where the loader is written. That refusal, a name that cannot be
called at all, and a loader that answered with the wrong class each have an
exit code of their own (section 8.3.3).

The file door puts the folder of the file at the front of `sys.path` and
imports it by its own stem, so a module that imports its neighbours works, and
it puts both back afterwards: a second file of the same stem must really be
read rather than found among the modules of the first. A module that belongs to
a package and uses a relative import cannot be loaded from a bare path at all,
and is refused with a message naming `--module` with `PYTHONPATH` instead.

**Importing a module runs it.** The help text and the readme say so. It is not
guarded against, because it is the same exposure as `python somefile.py` and a
guard could only be a pretence.

#### 8.3.3 What the program answers with

`ExitCode` gives each way of refusing a number of its own, because a program of
this library is meant to be usable from a script and from a continuous
integration job. A program whose backend prints once and returns is the one
that `--save` belongs to — there is no later moment at which a user could press
Save — and it is also the one whose exit code answers with the verdict of the
buffer. A program that gives the user a session ends with success when the user
closes it, whatever is left in the fields.

`--unfold` belongs to that same program and to no other: a container that would
flood a window opens folded (section 4.7), and a printout has no control to
press on it. It opens every container for good, after the save and before the
backend runs, so that the pass the backend makes before it prints cannot fold a
container it created away again.

That one fact about a backend is what `run_cli` is told, and neither `--save`
nor `--unfold` is added to the parser at all for the other two, so it is
`argparse` that refuses them. The other fact each program is told is the name
of its own settings file in the home folder (section 9.9).

#### 8.3.4 What a corpus of real configuration classes shows

Opening the 47 configuration classes of the
[`config_as_json` examples](https://github.com/tom-bjorkholm/config_as_json/tree/master/example/src/example)
shows two things that no example in this repository would have.

- **The constructor has more than one shape.** `Config.__init__` names the JSON
  text `from_json_data_text`; the example classes that `config_as_json` ships
  name it `from_json_text`, as does `ConfigFactory`. An editor that insisted on
  the one name that `Config.__init__` uses would refuse 32 of those 47 classes
  over the name of a parameter, so the editor reads the signature and passes
  every parameter it knows the meaning of — principle 4 of section 3 applied to
  a constructor. No text is passed to a constructor at all (sections 5.1 and
  6.1), so a class with nowhere to put it is edited like any other.
- **A class may not be able to serialize itself.** The editor reads the values
  it shows with `as_json_string()`, so a class that leaves part of its own
  writing to code outside itself has nothing for the editor to show. That is a
  refusal of the program with a message and a number, and the exception that
  `EditModel` documents for an application that builds the model itself.

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

An option for the extension a program's configuration files use, or for whether
it is enforced, or a `--key ACTION=COMBINATIONS`, would each be a second way of
saying what a settings file already says, inside one run, with nothing to
decide which of the two wins. An option per setting is also a command line that
grows a flag every time `Settings` grows an attribute, and section 9.1 promises
that it will.

**A settings file is per run and not only per user**, which is what makes one
option enough. An extension is a fact about the class being edited, while a
file of the home folder is a fact about whoever is running the program, so
somebody who opens two applications' classes writes a settings file for each
and names one with `-c`.

**Asking for the defaults of the editor is naming a file that says nothing.** A
settings file need name only what it changes, so one holding `{}` is the last
step of the lookup of section 9.9 written down, and `-c` reaches it past a file
of the home folder that says something else. There is therefore no option for
ignoring the lookup.

The examples of this repository do have `--extension`, `--enforce-extension`
and `--key`, and that is not the same command line disagreeing with itself. An
example stands in for the application, which decides these things in Python,
and the options are there so that every answer can be tried without writing a
program per answer.

#### 8.3.6 What a program says about its own versions

Whoever is about to report a problem, and whoever is about to upgrade, has to
know which versions are really installed and whether newer ones exist. So each
of the three programs answers `--version` with the report that
[`versionreporter`](https://pypi.org/project/versionreporter/) prints: the
installed version of every package the program is built out of and of Python
itself, and then what PyPI has that is newer, told apart into what runs on this
Python version and what would need a newer one. It is one call to a package
that does this rather than a version string of this library's own, because the
second half of that report is the half nobody writes for themselves.

**It is a fourth alternative and not an option beside the other three.** Naming
a module, naming a file, editing the settings of this editor and asking what is
installed are four things one run does *instead of* each other, so `--version`
joins the required group of section 8.3.2. It is answered before the rest of
the command line is looked at, because a run that reports versions edits
nothing, reads no settings file and opens nothing. It is not the kind of thing
section 8.3.5 keeps off a command line: a setting says how the editor behaves
while it edits, and `--version` says that this run does something else.

**One class per distribution, derived and not configured.** The report begins
with the distribution the program was installed from, because that is the
package whoever runs it has to upgrade, and because `versionreporter` takes the
first name of the list as the one its upgrade instructions name.
`EcajVersionReporter` names the core and what the core declares, and each
editor package derives a class that puts its own name in front of that list and
adds whatever else it alone depends on — `textual` in one of them and nothing
in the other, because Tkinter comes with Python. So a dependency is written
down in the package that declares it and nowhere else. It has to be a class and
cannot be a name handed to one: `get_main_package_name` and
`recommended_python` are class methods of `versionreporter`.

**The reporter reaches `run_cli` as an argument of its own**, rather than being
asked of the backend. A backend is handed to a program, to `edit` and to every
example of this repository, so what it said about a distribution would be right
in the first of those and meaningless in the others, and the two mounting entry
points are not backends at all. What a report is about is the *package the
program was installed from*, which is the same kind of fact as the name a
program is installed under and the name of its own settings file — both of
which `run_cli` is already told. It is a required argument because a program
that forgot it would report another package's name to a user about to upgrade.

**`check_if_unsupported_python` is deliberately not called**, though
`versionreporter` recommends it beside the flag. It prints to standard output
at the start of every run: the Textual editor's own screen would cover it, the
window editor has nobody reading the terminal it was started from, and the
utility of the core would put a paragraph in front of a printout that scripts
read. What it would say is in the report, and a user who wants it asks.

## 9. Settings the application owns

The editor runs inside an application that has already made decisions the
editor has no right to overrule: which key combinations that application's own
user interface has taken, and what a configuration file of that application is
called. An editor that decided either of those for itself would be overruling
the application, which is the one thing a library in this position must not do.

`Settings` is what the application says about them. Every attribute has a
default, so an application with no opinion passes nothing at all and gets what
the editor would have chosen anyway.

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
needs no merge rule; a misspelled action name is a `TypeError` where the
mistake was made rather than a key nobody ever reads; and the reason for a
default lives in the docstring of the attribute that holds it. **An action
added later is an added attribute, which breaks no application.**

Both classes are frozen. The editor is given what an application decided and
has no business changing it. What would have wanted them unfrozen is impossible
for a different reason: section 9.8.

`explain` has the keys `f1`, because a function key is what asks for help
everywhere else and a field claims most of the control letters, and `ctrl+g`,
because a terminal or a keyboard that does not deliver a function key would
otherwise leave the action to the button and the command palette.

`fold` has `f2`, the function key beside the one that explains, because both
actions decide how much of the configuration is on the screen, and `ctrl+t`,
because the tree is what the action is about. A configuration with no list and
no dict in it is never offered the action at all (section 4.7). **It is
deliberately not `ctrl+f`**, which is the one combination that means find
everywhere and is therefore not the editor's to spend (section 9.7).
`ctrl+shift+f` is rejected for the reason `save_as` records: a terminal that
encodes a control letter as a single byte has nowhere to put the shift, so the
combination would arrive as `ctrl+f` and the fold key would run the search.

The three file attributes make the same point: three defaults, and an
application that says nothing gets what the editor would have chosen anyway.
What they say is section 7.3's; that they are here is because only an
application knows how its own configuration files are looked after. Two of the
three defaults are the answers that lose nothing — one kept file, and a
question before it is written.

`priority_keys` is the one attribute that is not about *which* keys the editor
has but about **how hard it holds them**. True is the default: the editor is
offered a combination before the widget that has the focus, so a user who
presses Save while typing into a field means Save. False is for an application
that has taken one of these combinations for a widget of its own inside the
part of the window the editor is in. It is the one attribute that only an
**embedded** editor has a reason to change (section 8.2), and it is a different
answer from an empty tuple in `ActionSettings`: that one takes a key away from
the editor altogether, and this one leaves the editor the key it did not get
first.

### 9.2 Key combinations

Each action holds a tuple and not a single key, because an action can have more
than one: the first is the one a footer or a menu names, and the rest work
without being named. That is exactly the `('ctrl+r', 'f5')` of the Textual
backend, expressed without a second attribute for the alternate.

An empty tuple takes the key away and not the action. Tk shows a button and
Textual offers a command palette entry, and both stay. An application whose own
`ctrl+s` is spoken for empties that tuple, and its users still save.

Combinations are written in Textual's key names, in lower case: the modifiers
`ctrl`, `shift`, `alt` and `meta` joined with `+`, and then a single character,
`f1` to `f12`, or a name such as `escape`, `enter`, `tab`, `space`,
`backspace`, `delete`, `insert`, `home`, `end`, `pageup`, `pagedown`, `up`,
`down`, `left` or `right`. The core has to name some vocabulary, and this one
is published, complete, and used unchanged by one of the two backends. Tk needs
a translation whatever vocabulary is chosen, because `<Control-Shift-S>` is a
notation no other toolkit shares; the translation lives in the Tk package. A
combination the translation does not know leaves that action without that key
rather than without an editor — the button is still there. This is principle 4
of section 3 applied to keys.

One key combination given to two actions raises `ValueError` where the
`Settings` is constructed. Only one of the two can ever run, which one it is
depends on the toolkit, and the symptom is an action that does nothing.

### 9.3 The file name extension

`file_extension` is `None` by default, which is the "no opinion" of section 1 —
with the difference that it is the application's opinion that is absent, rather
than the editor's being imposed on an application that has one. A value is
normalized to begin with a dot, so `cfg` and `.cfg` mean the same thing, and
text that names no extension at all is refused.

`extension_enforced` then decides how hard the extension is:

| | a file to write | a file to read |
| --- | --- | --- |
| no extension set | taken as given | taken as given |
| default extension | added to a name that has none | taken as given |
| enforced extension | added to a name that has none, refused when the name has another | refused unless the name has it |

**The two directions differ on purpose.** A name to write does not name an
existing file, so completing it is a service. A name to read does name one, so
completing it would open a different file from the one that was asked for;
there the setting can only refuse. And a default extension says nothing at all
about reading, because a default is about what the editor writes when the user
did not say.

**Completing applies to a name that is chosen, not to one that is inherited.**
`out_file` defaults to `in_file` (section 7), and a session that read
`settings` must not save to `settings.cfg`. A destination is chosen when the
user answers Save as, when the application calls `EditModel.set_out_file`, and
when it names `out_file` in the `edit()` call; it is inherited only when it is
the input file. Both are checked against an enforced extension at every save,
whatever their origin.

A refusal is a message and never a crash: `load_config` raises the
`ConfigLoadError` the application already handles, and a refused save is a
`SaveOutcome` carrying the message that says why.

### 9.4 Settings, or a way to get them

```python
type SettingsSource = Settings | Callable[[], Settings]
```

Every entry point takes one of these, and the model resolves it at each point
of use, so a callable really is asked again. What that buys, stated plainly,
because it is less than it looks:

- **Key combinations are read once**, when the backend builds its bindings.
  Textual copies a class's bindings into the instance when the instance is
  constructed, and offers no supported way to change the key of a binding
  afterwards. Tk binds to the window when the widgets are created.
- **The file name settings are read at every save** and at every choice of a
  destination, so a later answer does take effect there immediately.
- **The gain that matters is neither.** It is that an application need not have
  its settings ready at the moment it calls. Under embedding (section 8) the
  model may be built long before the editor is shown.

### 9.5 Where the settings enter

`edit()`, `load_config()` and `EditModel()` each take a `settings` keyword that
defaults to `Settings()`. The backends take none: they read `model.settings`,
which is the same rule that holds for the marks, the title and the messages.
One source per session is what stops the two backends from binding different
keys or offering different file names.

### 9.6 What `Settings` is not for

- **The load policy.** It is already a parameter of its own, and it is a
  decision about one file rather than about the application.
- **Wording.** Button text, footer descriptions and palette entries stay in the
  backends. An application that wants its own wording is asking for
  translation, which is a larger thing and should be designed as one rather
  than arrived at through a growing dataclass.
- **Anything the editor can find out for itself.** `Settings` is for what the
  application knows and the editor cannot.

Whether an overwritten file is kept, under what name, how many of them, and
whether overwriting is confirmed are application decisions of exactly this
kind, and they are the attributes section 7.3 is about. Whether there is
anything *unsaved* is not, which is the line between them.

### 9.7 The two keys used by find

`ctrl+f` and `f3` are what `find` and `find_next` use as default.

### 9.8 The same answers, written in a file

An application decides these things in Python. A *program* of section 8.3 has
no application around it to ask, and the person running it decides instead — so
the same answers are a `config_as_json.Config` class of their own,
`SettingsConfig`, and can be read from a file. It is also what an application
declares as one member of its own configuration where its own users are the
ones who should decide, which is why it is in the core rather than in each
program.

**It mirrors `Settings` and does not derive from it**, and the reason is not a
preference. `ActionSettings` declares a member called `validate`, which shadows
`Config.validate()` on every object of a class bridged the way
`config_as_json`'s third-party-parameter pattern bridges one; `config_as_json`
calls that method while it constructs and while it parses, so such a class
cannot be built at all. No `Config` may hold a member of that name. That is
also what makes unfreezing `Settings` moot (section 9.1).

**The key combinations are a dict member and not a nested object.**
`config_as_json` reads a nested configuration object whole — without the
permissive flag of the parse around it — so every settings file would then have
had to name every action. A dict member is filled in per key instead, its keys
are checked against the ones the class declares, which is the same protection
against a misspelled action name that section 9.1 gets from one attribute per
action, and a member validator completes what a file left out.

**Nothing here restates what a valid setting is.** Each member validator hands
the value to what `Settings` and `ActionSettings` already say — principle 1 of
section 3 applied to the editor's own settings. Two rules that both classes
need — whether a piece of text adds anything to a file name, and what an
extension without its dot becomes — are functions of the settings module that
both read.

### 9.9 Where a program finds its settings

A program looks in five places and uses the first that answers: the file that
`-c/--cfg` names, the file that the `CFG_EDIT_CFG_JSON` environment variable
names, a file of that program's own in the home folder,
`$HOME/.edit-cfg-json.cfg` there, and finally nowhere at all, which is the
defaults of the editor.

**A file that was named must be there, and a file that was looked for need not
be.** The first two are somebody saying which file to use, so a name that no
file answers to is a refusal with an exit code of its own: running with other
settings than the ones that were asked for is the one thing a lookup must not
do quietly. The two files of the home folder are the lookup itself, and a step
of a lookup that finds nothing is the lookup working.

**One environment variable for every program, and one file of the home folder
per program above the shared one.** The variable is a machine or a session
deciding how this editor behaves, and an answer that had to be given three
times would come to be given twice. What the two editors differ about is their
keys and their questions, so a user who wants the window and the terminal to
differ writes one file each and a user who wants one answer writes only the
shared file. The backend that prints once and returns has neither keys nor
questions, so it has no file of its own.

**It is read with `LoadPolicy.DEFAULTS`**, because a settings file is written
by hand to change one or two things. It is also read **before** anything else
the command line names, because it is what the whole run behaves according to.

**The last step is reachable by name**: a file that names nothing is the
defaults of the editor, so `-c` naming one is how a run asks for them past a
file of the home folder that says something else (section 8.3.5).

### 9.10 Changing the settings file format costs a compatibility rule

**An action added to `ActionSettings` is a change of this library's own file
format**, and so is any other change to what `SettingsConfig` declares.
`config_as_json` matches the keys of a dict member against the ones the class
declares while the file is parsed, before any validator of that class is asked
anything, and it does so whatever policy the load was given. So every settings
file written before that action existed is refused — and an application that
declares `SettingsConfig` as one member of its own configuration is refused
whatever policy *it* chose, because a nested configuration object is read whole
(section 9.8). Such an application fails to start over a key of the editor it
embeds, and the refusal names the wrong fault, because a missing declared key
and an undeclared key of the file are told apart by retrying the load and the
retry fails as well (section 5.2).

**So each such change is accompanied by a rule for reading the older file**,
which is `config_as_json`'s Read Old Configuration File support and is what
section 5.3 already makes visible for an application's own classes. Three things
hold for those rules.

- **Only a difference a released version really wrote belongs in them.**
  `ADDED_ACTIONS` names the actions no released version ever put in a file.
  Supplying an action that has always existed would accept a file no version
  ever produced, and would hide a key that somebody removed by hand.
- **What is supplied is read from `ActionSettings` and not written again**, for
  the same reason the declared values of the class are (section 9.8): the
  default of a setting is stated once.
- **They are the declarative rules and nothing else.** A missing-value path
  creates the members above it, so a file with no `actions` at all is given one
  holding those two entries. That is harmless, and deliberately not guarded
  against: a settings file is written by `--edit-settings` saving one, which
  writes every member and every action, so a file without that member is not a
  file any version wrote. Such a file is still refused, because the key check
  then asks for the seven actions the two rules say nothing about.

**A run that needed such a rule says so.** `load_settings` names the file the
lookup used and asks for it to be opened with `--edit-settings` and saved, which
is what writes every value the current version has. The words are printed there
and not by a `config_as_json.MigrateCfgWarnHook`, because a hook prints while
the file is parsed and `load_config` collects what a parse says into diagnostics
that it shows only when the load *failed*; it also builds its own configuration
object, so a hook handed to it is never the one that records anything.

## 10. Testing strategy

### 10.1 Core

The core needs no UI and no display, and it is where essentially all the logic
lives. If a behaviour can only be tested through a backend, that is evidence
the behaviour is in the wrong package.

**A printout of the model is evidence about the core and never about a
backend.** The non-interactive backend is a test instrument as much as it is a
user interface, and what it can testify to is what the model holds. What only a
user can reach — a control that is pressed, a field that loses the focus, a
question that is answered — is tested where it exists, in sections 10.2 to
10.4.

### 10.2 Tkinter: three categories

Experience with other Tkinter applications says one category is not enough. Tk
tests fall into three groups with genuinely different requirements:

1. **Stubbed** — real Tk is never called; widgets are monkey-patched or
   otherwise replaced. Runs anywhere, fast, no display. This is the
   default category and holds most Tk tests.
2. **`root_or_skip()`** — a fixture returning a *withdrawn* Tk root, or
   skipping when no display is available. Real Tk, no visible window,
   still automatable. Most stubbed tests should have a companion test
   in this category.
3. **Focus sensitive** — must run on a real display, and any user
   activity that changes what has focus disturbs them. These cannot run
   automatically. They are run manually, by a person who knows no other
   display activity is happening.

Category 3 maps directly onto `BuildSpec.excluded_test_markers`, whose own
docstring uses `focus_sensitive` as its example and notes such tests are
**deselected** rather than collected — so they never appear in the summary as
skipped, and are run on demand with `pytest -m focus_sensitive`.

**Interaction to be aware of**: `BuildSpec.readme_summary_max_skipped` defaults
to `0`, so the README test summary is updated only when nothing was skipped. On
a machine with a display, category 2 runs and the summary updates. On a
headless machine, category 2 skips and the summary is not updated. That is
defensible — a summary should not be published from an incomplete run — but it
should be a known consequence rather than a surprise.

### 10.3 Test the same code both ways

Where it is affordable, the same code path gets a stubbed test *and* a real-Tk
(withdrawn) test. This is deliberate duplication, because the two fail in
opposite directions: stubs drift from real Tk behaviour and quietly stop being
evidence of anything, and real Tk masks logic errors behind widget defaults and
silent coercions, so a wrong value can still produce a passing assertion. A
discrepancy between the two runs is itself a finding.

One thing a withdrawn root cannot answer is where the pointer is: Tk delivers
`<Enter>` and `<Leave>` to a mapped window only, and `event_generate` does not
change that, so the tooltip of section 4.10 has a stubbed test and no companion
in category 2.

### 10.4 Textual

Textual can be driven headlessly in-process, so it does not need the three-way
split — the equivalent of the withdrawn root runs everywhere, including in CI.
The stubbed-versus-real duality of section 10.3 still applies where it is
cheap. The headless driver API is confirmed against the pinned `textual`
version rather than assumed.

## 11. Rejected alternatives

- **One distribution with `[tk]` and `[textual]` extras.** Simpler releases and
  no compatibility matrix, but it cannot give a third-party backend author a
  package to depend on, and `tkinter` is not installable from PyPI, so a `[tk]`
  extra would install nothing.
- **PEP 420 namespace package.** Section 2.2.
- **One repository per package.** Correct only if a backend gets a separate
  maintainer. Today it would mean releasing the core to PyPI before either
  backend could test against it, while the core API is still moving.
- **Read-only constraint accessors on `config_as_json` validators.** Rejected
  because applications may define arbitrary validator subclasses, so this would
  work for known classes and silently fail for the rest.
- **Editing a live `Config` object.** Section 4.2.
- **An element invented for a member that nothing says anything about.**
  Permanently out of scope rather than not yet built: where a class declares no
  element for a list member, the member holds none, and no declared type says
  what one would be, only the application knows what an element of its own list
  looks like, and a member it never gave one for and never annotated has never
  said. Such a member says so and offers removing and moving instead. What was
  narrowed rather than reversed is *which* members those are: `list[str]` says
  that an element is text, and giving such a member the empty text is reading
  the application's own annotation rather than inventing anything. Sections 4.1
  and 4.9.
- **An entry invented for an empty dict from its declared type.** A dict is not
  a list here. What refuses a new entry of an ordinary dict member is
  `Config.check_dict_parse` matching it against the keys its class declares,
  and `dict[str, int]` says what a new value would be and nothing about whether
  the key beside it would be accepted. Offering the control anyway would be
  offering one that produces a refusal, which section 4.9 rules out. Section
  4.9's first bullet is the whole reason. This limitation does not apply to
  dicts that will not will not be checked, examples of not checked dicts are
  `list[dict[str,str]]` or dict listed as unchecked dicts.
- **The empty dict given to a member declared to allow no value.** The same
  check, one step up: `check_dict_parse` refuses a dict written for a member
  whose value is not a dict, whatever keys that dict has and even where it has
  none, so the member cannot be given the empty dict of its kind. It is the
  one kind of value that the two states of section 4.2 do not reach, and the
  member says so below its own row rather than offering a control that produces
  a refusal. A list is not affected: there is no such check for one.
- **A row only for the omitted members the editor can make a value for.** It
  would have kept the tree closer to the file, and it would have made the
  existence of a row a second thing to explain: some members the class leaves
  out would be there and some would not. Every one of them is a member of the
  configuration, so every one of them has a row, and the one whose kind nothing
  says is an ordinary field holding `null` — which is what section 4.2 already
  says about a member with one state. Sections 4.1 and 4.9.
- **A raw JSON editing surface for a sub-object whose class cannot be read.**
  The early sketch of the work that gave the omitted members their rows
  proposed a text area holding the JSON of one sub-object, for the case where
  nothing says what the object is. It was not needed for that case: the class
  of a nested object is named by its declaration, and one the editor cannot
  construct says so instead of offering a control that refuses every press. It
  is recorded as a step of its own rather than as a rejection, because what
  would make it worth having is a different question — an editing surface for
  a subtree, which nothing in the editor has yet.
- **The user changing the type metadata of a leaf.** It was an open question
  until the declaration of a member was read, and the one thing it would have
  been useful for — telling a `None` apart from an empty text in an
  `Optional[str]` — is answered by the two states of section 4.2 without
  letting anybody change the kind of anything. A kind chosen by the user would
  in most cases produce a value the application then refuses, which is a
  control that produces a refusal by another route.
- **A `parent` argument on the backend classes.** `TkEditor(parent=...)` reads
  well until `run_editor` has to mean "run to completion" with no parent and
  "mount and return" with one. One method with two meanings makes `edit()`
  return `None` before the user has done anything, and the protocol's one
  sentence stops being true. Section 8.2.3 instead.
- **A backend that detects the toolkit instance for itself.** Shortest for the
  application, and it rests on `tkinter._default_root` and
  `textual._context.active_app`, both private, to guess something the
  application could simply have said. Section 8.2.1.
- **One widget argument only, with the application creating any window of its
  own.** One argument instead of two mutually exclusive ones, and the title,
  the geometry, the close protocol and the grab left to the application whose
  window it is — but every application that wants a window of its own then
  writes the same five lines of `tkinter` against this library rather than with
  it, and `wizard_tk_bridge` answers the same question with `parent`, `area`
  and `modal`. An application that wants those five lines back passes `area`
  after making the window itself. Section 8.2.2.
- **Blocking while embedded, with Tk's nested `wait_window`.** It would keep
  `run_editor` honest in one backend and is impossible in the other, which is
  the worst place for a difference between them to be. Section 8.2.3.
- **Tk key bindings on each field the editor creates.** It scopes the keys the
  way embedding needs, and it leaves a key dead the moment the focus is on a
  button, which is where a Tk focus lands as soon as anything is pressed. A
  bind tag scopes the same way and covers everything the editor built. Section
  8.2.7.
- **A focusable Tk panel with the bindings on it.** It would put the editor
  into the application's tab order, which is a decision about the application's
  own window that section 8.2.2 gives to the application.
- **`close()` answering whether the editor really closed.** Useful in Tk and
  impossible in Textual, whose question is a modal screen with a callback. One
  answer both backends can give — `on_close` — is worth more than a return
  value in one of them. Section 8.2.3.
- **Saving on the way out of a session with unsaved changes.** A third answer
  to the closing question would have to cope with a save the application
  refuses, with no destination chosen yet, and with the Save-as question
  opening from inside a confirmation. The user presses Save and then closes,
  which is one keystroke more and no new state. Section 7.2.
- **`Settings` unfrozen and bridged into a `Config`**, the way `config_as_json`
  bridges a third-party parameter class. It would have made the settings and
  their configuration class one class rather than two that have to agree. It is
  impossible: `ActionSettings` declares a member called `validate`, which
  shadows `Config.validate()`, and `config_as_json` calls that method while it
  constructs and while it parses. Section 9.8.
- **The key combinations as a nested `Config` object.** It would give them a
  class, a docstring and a member each, which is more than a dict member says
  about itself. `config_as_json` reads a nested object whole, so every settings
  file would then have had to name every action. Section 9.8.
- **Resolving a `SettingsSource` callable once and keeping the answer.** An
  application that can answer at that moment can pass the `Settings` object
  itself, so the variant buys nothing the plain object does not. Section 9.4.
- **A second option for making a settings file that does not exist yet.**
  `--edit-settings` with no `-i` already starts from the values the class
  declares, so the option would be a name for something the command line
  already says. Section 8.3.2.
- **A single `module:Class` argument instead of `--module`/`--file` with
  `--class`.** It reads better and would have to guess whether it was given a
  module or a path, make a Windows drive letter a special case, and take the
  refusal of a missing or a doubled location away from `argparse`. Section
  8.3.2.
- **An option per setting on the command line.** It would grow a flag every
  time `Settings` grows an attribute, and it would be a second way of saying
  what a settings file says, inside one run, with nothing to decide which of
  the two wins. Section 8.3.5.
- **Draft file** "Invalid cannot be saved" means that in the highly unlikely
  event that a user has a long, still-invalid editing session, there is no
  way out but to discard it. The escape hatch that would preserve the rule
  is an editor-owned **draft file** holding the raw JSON buffer. It has been
  decided that we will **not implement any draft file** saving.
