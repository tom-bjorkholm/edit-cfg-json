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
  requirements. See section 9.

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
with type information for each leaf. There is not yet any decision
to show the type metadata as a label by the field to the user.
There is not yet any decision to allow the user of the editor to try
to change this type metadata (which in many cases would trigger an
error at validation, but might be useful for separating between
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
field** should report itself, because that is when the user has moved on
from that field. It does not arise yet: the conversions this version has
cannot fail, since text that is not JSON is kept as a string and the wrong
type is something section 6.1 reports later. It arises with the leaves that
`parse_converters()` turns into rich Python types, an enum being the
obvious one: its member name is not a member of the enum for most of the
time it takes to type it, so converting on every change would report a
failure that is not one yet.

Per-field conversion feedback on focus loss is **not** the validation of
section 6. It is local, it needs no candidate configuration, and it answers
a different question — whether this text means a value at all, rather than
whether the configuration is one the application would accept. Both are
needed, and the value conversion is to be revisited with that in mind.

Rewriting the text a field shows is a third, separate matter, and belongs
where validation rewrites values (section 6.4).

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

### 4.3 Descriptions and docstrings

Two complementary, independently optional sources of explanatory text:

- **Class docstrings** label config-object nodes. Read with
  `cls.__doc__`, cleaned with `inspect.cleandoc()`, split at the first
  blank line into a summary for the folded row and full text for the
  expanded view. A show/hide toggle belongs in the model.

  Use `cls.__doc__`, **not** `inspect.getdoc(cls)`. `getdoc()` inherits
  from base classes, so a nested config class without its own docstring
  would silently display `Config`'s docstring — actively misleading in
  an editor. Check `cls.__doc__ is not None` and show nothing otherwise.

- **The description mapping** labels individual attributes, because
  per-attribute docstrings do not exist at runtime: a string literal
  after an assignment is discarded, and PEP 526 annotations are not
  recorded.

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

## 5. Loading

### 5.1 The loader protocol

The application may need to pass constructor arguments this library
knows nothing about. The loader protocol solves that by having a
**closed** signature: the editor passes only the five things it owns, all
keyword-only, and anything else is bound before the callable reaches the
editor, with a closure or `functools.partial`.

```python
class ConfigLoader(Protocol):
    """Construct the application's Config object for the editor."""

    def __call__(self, *, from_json_data_text: Optional[str] = None,
                 from_json_filename: Optional[PathOrStr] = None,
                 ok_to_use_defaults: bool = False,
                 auto_ch_hook: Optional[ConfigAutoChangeHook] = None,
                 stderr_file: TextIO = sys.stderr) -> Config:
        """Construct one Config object from the given JSON source."""
```

This is `config_as_json.ConfigFactory` plus the two parameters it lacks.
Adding them here means factory-constructed configurations get automatic
change reporting and load-policy control, which they cannot get through
`ConfigFactory` today.

When no loader is supplied, the editor derives one from `type(config)`,
using `inspect.signature()` to decide whether `auto_ch_hook` can be
forwarded (see section 5.3).

**`Config.__init__` takes no `ok_to_use_defaults`.** Confirmed against the
implementation in `./venv` at step 4: the parameter belongs to
`Config.parse_json()` and `Config.read()`, and `__init__` calls both of them
with the default `False`. So the derived loader has one path for both
policies: construct the class with no JSON source, which leaves it holding
its declared defaults, and then call `parse_json()` with the
`ok_to_use_defaults` the policy asks for. The hook still reaches the object,
because it is `__init__` that takes it.

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
  of the two it was; step 7 of the delivery plan improves the enum case.
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

The per-field *filled from default* flag is computed from the keys the file
text contained, because a load that was allowed to use the defaults cannot
afterwards say which of its values came from the file. That is exact for
every file the editor can open today. It will over-report a member whose key
ROCF renamed, and section 5.3 with step 8 of the delivery plan is where the
automatic changes of an old-format file get reported properly.

### 5.3 Making automatic changes visible

Reading an old-format file applies `ReadOldConfiguration` rules, so the
data presented for editing can differ substantially from the file on
disk. The user must be told, or the editor looks broken.

`Config.read()` accepts no hook; only `Config.__init__` takes
`auto_ch_hook`. Worse, the application's class must opt in by declaring
`auto_ch_hook` in its own `__init__` and forwarding it (see
`e37_read_old_nested_configuration_file.py`); the standard three-keyword
constructor shape does not. So the editor must **construct** the
configuration rather than receive an already-loaded one, and must detect
hook support with `inspect.signature()`.

Because that support cannot be relied on, the primary mechanism is
hook-independent: **load the file, re-serialize the resulting config, and
diff that against the raw file text.** Any difference means the load
changed something. This single mechanism covers all three sources of
surprise:

- ROCF migration of an old-format file
- normalization during parsing
- values filled in by a permissive load

The structured `ConfigAutoChangeHook` report is used to *explain* the
diff when the application's class accepts a hook, and is simply absent
otherwise.

## 6. Validation

### 6.1 Whole-configuration validation

`Config.__init__` already runs the entire chain: key matching, recursive
dict-shape checks against defaults, `parse_converters()`, nested-config
construction, and then `get_validation_plan()`. So a validation pass is:

> serialize the edit buffer to JSON text, construct a candidate config
> from that text with a captured `stderr_file`, and catch `KeyError`,
> `ConfigBadJson`, `TypeError`, `ValueError`, `InvalidConfiguration`,
> `InvalidConfigurationValue` and `InvalidConfigurationType`.

The user sees exactly the diagnostics the application would see at load
time. There is no second validation implementation and no way for the
editor to accept something the application later rejects.

### 6.2 Subtree validation, and why folding is the natural trigger

Every nested config class is required to be constructible from
`from_json_data_text` alone, or through the `factory_function` declared
in its `ConfigNesting`. A nested-config subtree can therefore be
validated **in isolation** by constructing `config_type` from that
subtree's JSON.

That makes folding and validating the same operation: when the user folds
a nested config away, the editor validates that subtree and shows the
result as a badge on the folded row.

Two validity levels result, and the UI must distinguish them:

- **subtree-valid** — this nested config is internally consistent;
  cheap, local, available on fold
- **config-valid** — the whole tree passes, including
  `WholeConfigValidator` and `ProjectedWholeConfigValidator` steps on a
  parent that relate members *across* a nesting boundary; obtainable
  only at the root

A subtree can be valid while the root is not. That is the honest state
and both should be shown.

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
def edit(config: Config, backend: EditorBackend,
         descriptions: Descriptions, *,
         in_file: Optional[PathOrStr] = None,
         out_file: Optional[PathOrStr] = None,
         loader: Optional[ConfigLoader] = None,
         policy: LoadPolicy = LoadPolicy.STRICT_THEN_DEFAULTS,
         stderr_file: TextIO = sys.stderr) -> Optional[Config]:
```

The `config` argument serves as the schema and defaults source and stays
the ergonomic front door; `loader` is the door for applications with
constructor arguments we do not know about.

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
a third-party backend in the wild.

## 9. Testing strategy

### 9.1 Core

The core needs no UI and no display, and it is where essentially all the
logic lives. If a behaviour can only be tested through a backend, that is
evidence the behaviour is in the wrong package.

### 9.2 Tkinter: three categories

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

### 9.3 Test the same code both ways

Where it is affordable, the same code path gets a stubbed test *and* a
real-Tk (withdrawn) test. This is deliberate duplication, because the two
fail in opposite directions:

- Stubs drift from real Tk behaviour and quietly stop being evidence of
  anything.
- Real Tk masks logic errors behind widget defaults and silent
  coercions, so a wrong value can still produce a passing assertion.

A discrepancy between the two runs is itself a finding, and usually a
more interesting one than either test failing alone.

### 9.4 Textual

Textual can be driven headlessly in-process, so it does not need the
three-way split — the equivalent of the withdrawn root runs everywhere,
including in CI. The stubbed-versus-real duality of section 9.3 still
applies where it is cheap. The exact headless driver API should be
confirmed against the pinned `textual` version rather than assumed.

## 10. Version 1 scope

In scope:

- read, edit and save with full validation
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
- **Embedding.** The model is designed for it; only the modal wrapper
  ships first.
- **The draft file** of section 7.1.

Not a limitation but a permanent decision: no introspection of validator
constraints, so no automatically generated dropdowns or spin ranges.
Fields are edited as text and correctness comes from running the real
validators.

## 11. Rejected alternatives

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
