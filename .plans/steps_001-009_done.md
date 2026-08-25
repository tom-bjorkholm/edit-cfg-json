# The v1 delivery plan: steps 1 to 9, implemented and committed

## Where everything is

Steps 1 to 28 are implemented and committed, step 23 with the corrections its
review asked for. Steps 1 to 9 are written up in
[steps_001-009_done.md](steps_001-009_done.md), steps 10 to 21 in
[steps_010-021_done.md](steps_010-021_done.md) and steps 22 to 28 in
[steps_022-028_done.md](steps_022-028_done.md). The steps still to build are in
[steps_029-x.md](steps_029-x.md). Where any of the four files mentions a
design decision, [`doc/detailed_design.md`](../doc/detailed_design.md) remains the authority and
the plan says only *when* that decision gets built.

- [The decisions the plan is built on][dec] — the seven settled before the
  first step, from example observability to per-step verification.
- [The names introduced in steps 1 to 9][names] — one table of every public
  core name and the step that settled it.
- [Step 1][s1] — the walking skeleton: `EditModel`, `EditorBackend`,
  `model_as_text` and `--ui dump`, both backends showing a flat config
  read-only.
- [Step 2][s2] — the buffer became writable, with dirty tracking, and
  `--set` standing in for a user typing.
- [Step 3][s3] — validation of the buffer, the refusals it catches, and the
  mark for a value a validator rewrote.
- [Step 3B][s3b] — `Enum` and `IntEnum` members, which needed no change to
  the core at all.
- [Step 4][s4] — loading: `LoadPolicy`, `load_config`, the three distinct
  refusals, and the mark for a member a permissive load filled in.
- [Step 5][s5] — saving and `edit()`, which reached milestone 1: a save
  validates, moves the baseline it is compared against, and asks for a
  destination when it has none.
- [Step 6][s6] — descriptions and docstrings, the explain toggle in the
  model, a scrolling body in both backends, and the `Emphasis` vocabulary.
- [Step 7][s7] — field-level diagnostics: a refusal is shown at the member
  it is about, on validation and on focus loss.
- [Step 7B][s7b] — three ready-to-run programs, one per package, opening any
  `Config` class named by `--module` or `--file`, with an exit code for each
  way of refusing.
- [Step 8][s8] — automatic-change visibility: what reading an old-format
  file altered, marked at the member and reported by key.
- [Step 9][s9] — the explicit loader: `ConfigLoader`, `derived_loader`, and
  a save that refuses a file the loader would not read back as the same
  class.
- [Step 10][s10] — lists and dicts as a tree of rows with a field at every
  value, folding, and the rows being built again when a validator changes how
  many of them there are.
- [Step 11][s11] — a nested `Config` object as a node with a class, a
  docstring and members of its own, and the ownership of everything inside it.
- [Step 12][s12] — every nested object asked whether it is a configuration on
  its own, which both puts a badge on its row and names the member inside it
  that a validator refused.
- [Step 13][s13] — a list of configuration objects and a dict of them, one
  description reaching every one of them, and the confirmation that step 11 had
  already built the mechanism.
- [Step 14][s14] — how many things a member holds, where a new element is
  copied from, and the containers that say why they cannot be given one.
- [Step 15][s15] — closing an editor that holds something unsaved asks first,
  in words the core owns and in a dialog or a screen that each backend puts.
- [Step 15B][s15b] — the two interactive editors described as the product they
  are, and `--ui dump` as the very limited non-interactive user interface it
  is.
- [Step 16][s16] — the file that a save writes over kept under the name the
  application chose, once per destination per session, and a question before
  it happens.
- [Step 16B][s16b] — the name `edit-cfg-json` freed for the editor it
  promises, and the backend that prints once reached as the small utility it
  is.
- [Step 17][s17] — every document rewritten against what was actually built,
  the order of the work taken out of all of them but this one, and the release
  readiness of the three packages checked rather than assumed.
- [Step 18][s18] — the editor mounted in a window an application already owns,
  in both toolkits, with its keys reaching the editor and nothing else.
- [Step 18B][s18b] — one call per shape per toolkit, taking the keywords of
  `edit()`, and four examples where there were two.
- [Step 19][s19] — the settings of the editor as a configuration class of
  their own, editable in the editor, declarable inside an application's own
  configuration, and looked for in five places by each program.
- [Step 20][s20] — the command line of a program saying what to edit and which
  files and never how the editor behaves, which is the whole of the answer once
  every setting can be written in a file.
- [Step 21][s21] — `--version` on all three programs, as a fourth thing a run
  does instead of editing, answered by one version reporter per distribution.
- [Step 22][s22] — a member holding true or false entered as an enum member
  already was: any beginning of either word in any case, and a text that means
  neither of them refused at that member.
- [Step 23][s23] — looking for a member of a configuration that does not fit a
  window: a field that stays, four controls that say where it looks, and a match
  inside a folded container opened, brought into view and typed into.
- [Step 24][s24] — the declaration of a member read as well as the value it
  holds, and the open question of section 4.2 answered: a member allowed to
  hold nothing has two states rather than a kind the user can change.
- [Step 25][s25] — the members a class leaves out of the file given a row to be
  given a value at, the buffer written back to the class as the document a save
  would write, and the one kind of value that a member holding nothing cannot
  be given.
- [Step 26][s26] — the dict whose values are of two kinds asked twice: the key
  a declaration names given the two states of a member that may hold no object,
  and every other key of it an entry of an ordinary container after all.
- [Step 27][s27] — the dict whose keys its own class does not check given the
  entry control every other container has, and the key policy left where
  `_unchecked_dicts` put it: with the validators of the application.
- [Step 28][s28] — which dicts can be given an entry became a question about
  where a dict sits rather than about which member it belongs to, which is
  what the check that refuses one actually asks.

[dec]: steps_001-009_done.md#1-decisions-this-plan-is-built-on
[names]: steps_001-009_done.md#2-naming-conventions-used-below
[s1]: steps_001-009_done.md#step-1--walking-skeleton-read-only-view-of-a-flat-config
[s2]: steps_001-009_done.md#step-2--editing-the-buffer
[s3]: steps_001-009_done.md#step-3--validation-of-the-buffer
[s3b]: steps_001-009_done.md#step-3b--enums-as-attributes-in-config
[s4]: steps_001-009_done.md#step-4--loading
[s5]: steps_001-009_done.md#step-5--saving-and-edit--milestone-1
[s6]: steps_001-009_done.md#step-6--descriptions-and-docstrings
[s7]: steps_001-009_done.md#step-7--field-level-diagnostics
[s7b]: steps_001-009_done.md#step-7b--a-ready-to-run-program-in-every-package
[s8]: steps_001-009_done.md#step-8--automatic-change-visibility
[s9]: steps_001-009_done.md#step-9--the-explicit-loader
[s10]: steps_010-021_done.md#step-10--lists-and-dicts-of-scalars
[s11]: steps_010-021_done.md#step-11--nested-config-objects
[s12]: steps_010-021_done.md#step-12--subtree-validation
[s13]: steps_010-021_done.md#step-13--list_element-and-dict_value-nesting
[s14]: steps_010-021_done.md#step-14--adding-and-removing-elements
[s15]: steps_010-021_done.md#step-15--confirmation-before-dropping-edits
[s15b]: steps_010-021_done.md#step-15b---changed-descriptions-of---ui-dump
[s16]: steps_010-021_done.md#step-16--oldbackup-file-when-overwriting
[s16b]: steps_010-021_done.md#step-16b---fix-ux-problem-with-edit_cfg_json
[s17]: steps_010-021_done.md#step-17--first-release-polish
[s18]: steps_010-021_done.md#step-18--embedding-in-an-applications-own-window
[s18b]: steps_010-021_done.md#step-18b---redesign-api-and-examples-for-embedding
[s19]: steps_010-021_done.md#step-19---config_as_jsonconfig-for-storing-the-settings
[s20]: steps_010-021_done.md#step-20--the-rest-of-the-programs-command-line
[s21]: steps_010-021_done.md#step-21---version-command-line-flag
[s22]: steps_022-028_done.md#step-22---better-bool-support
[s23]: steps_022-028_done.md#step-23---finding-a-member
[s24]: steps_022-028_done.md#step-24---more-type-information-and-whether-the-user-may-change-it
[s25]: steps_022-028_done.md#step-25---add-and-remove-omitted-members
[s26]: steps_022-028_done.md#step-26---full-support-for-dict_value_by_key
[s27]: steps_022-028_done.md#step-27---adding-an-entry-to-an-_unchecked_dicts-member
[s28]: steps_022-028_done.md#step-28---an-entry-in-a-dict-the-class-never-checks

## 1. Decisions this plan is built on

These were settled before the plan was written and are recorded here so
that they do not have to be re-decided at every step.

| Question | Decision |
| --- | --- |
| Example observability | A non-UI `--ui dump` switch on every example, **and** headless UI smoke tests in `examples/test/`, **and** the fuller headless UI tests in each backend package's own test folder |
| First major milestone | Full round trip for a flat config: load, edit, validate, save, cancel. No descriptions, no docstrings, no field-level attribution, no automatic-change report |
| Backend pacing | Both backends in every step |
| Plan coverage | All of v1, detail front-loaded |
| Example layout | New shared `examples/src/example/cmd_line.py`; `e01_hello.py` retired when the first editor example exists |
| Loading in milestone 1 | Loader derived from `type(config)`, plus `LoadPolicy` with its documented `STRICT_THEN_DEFAULTS` default and the three distinct failure messages of design section 5.2 |
| Per-step verification | Clean build on Python 3.12, 3.13 and 3.14, every step |

## 2. Naming conventions used below

Proposed public core names, all inside the 25-character limit that
`python_layout_max_name_length` enforces. They are proposals; the step
that introduces each one is where the name is finally settled.

| Name | Kind | Introduced in |
| --- | --- | --- |
| `EditModel` | class, the UI-agnostic model | step 1 |
| `EditorBackend` | `Protocol`, phrased against `EditModel` | step 1 |
| `model_as_text` | function, the `--ui dump` rendering | step 1 |
| `LoadPolicy` | `Enum` | step 4 |
| `edit` | function, the modal convenience wrapper | step 5 |
| `Descriptions` | type alias, `Mapping[ConfigPath, str]` | step 6 |
| `run_cli` | function, the program given a backend | step 7B |
| `DumpEditor` | class, the backend that prints the model | step 7B |
| `default_config` | function, the declared defaults of a class | step 7B |
| `ExitCode` | `IntEnum`, what one run of a program ends with | step 7B |
| `add_file_options` | function, the shared file and policy options | step 7B |
| `named_policy` | function, a `--policy` value as a `LoadPolicy` | step 7B |
| `ConfigLoader` | `Protocol` | step 9 |
| `derived_loader` | function, a loader made from one callable | step 9 |

`Descriptions` is the only type alias the design asks for, and
`doc/detailed_design.md` section 2.6 already declares it, so introducing it in step
6 needs no further permission. Any *additional* alias needs permission
first, per `CLAUDE.md`. (Do ask for permission when an alias would improve
code quality - do not see the need for permission as a hint to avoid
all aliases.)

## 3. Milestone 1 — flat round trip, steps 1 to 5

### Step 1 — Walking skeleton: read-only view of a flat config

Status: **Implemented and committed**

**Observable outcome.** A new example `e01_flat_config.py` defines a
`Config` subclass with one `str` and one `int` member.
`python3 examples/src/example/e01_flat_config.py --ui dump` prints both
member names with their default values as JSON-space text.
`--ui textual` opens a Textual screen showing the same two rows and quits
on a key binding. `--ui tk` opens a Tk window showing the same two rows
and closes on a button.

**Core.**

- An internal module holding `EditModel`: constructed from the caller's
  `Config` object, it reads the JSON-space values with
  `config.as_json_string(stderr_file)` and `json.loads`, and exposes an
  ordered sequence of leaf entries `(name, value)`. Flat only; a member
  whose value is not a scalar is out of scope until step 10 and the model
  should say so plainly rather than half-handle it.
- `model_as_text(model) -> str`, the single rendering used by `--ui dump`
  and by tests. Putting it in the core rather than in the examples is
  deliberate: it is UI-agnostic, and it is what makes every later step
  observable without a display.
- `EditorBackend`, a `Protocol` phrased against `EditModel`, never
  against `edit()`. It runs to completion and communicates its outcome
  through the model, so the protocol does not change when saving arrives
  in step 5. This is design section 8; getting it right now is what keeps
  embedding additive later.
- `edit_cfg_json/__init__.py` re-exports `EditModel`, `EditorBackend` and
  `model_as_text`.

**Backends.** Each backend gets one thin widget or screen that renders the
model's rows read-only and exits. No editing, no save. A "quit" button or
similar is used to let the user see the rendered backend before exiting.

**Examples.**

- New `examples/src/example/cmd_line.py`, modelled on
  `dep_lib_doc/config_as_json/example/cmd_line_handling.py`. It owns
  `--ui {tk,textual,dump}`, `-i/--input` and `-o/--output`, and it
  selects and runs the backend. Every/most later example reuses it unchanged,
  which is what keeps the examples about configuration shapes rather than
  about argument parsing.
- New `examples/src/example/e01_flat_config.py`.
- Delete `examples/src/example/e01_hello.py` and
  `examples/test/test_example/test_e01_hello.py`.

**Placeholders removed in this step.** `hello.py` and its test disappear
from all three packages together, because the backend greetings call the
core greeting and cannot outlive it. The
`readme_parts/main_entry_points.md` of each package is rewritten to name
the real entry points instead.

**Tests.**

- Core: `EditModel` construction and `model_as_text` output for a flat
  config, including a config whose only members are a `str` and an `int`,
  a config with a `None` default, and a config with a member whose value
  is not scalar (must be reported, not silently dropped).
- Architecture, per design section 2.4, both in the core's test folder:
  importing `edit_cfg_json` with `tkinter` and `textual` blocked in
  `sys.modules` must succeed; walking the two backends' imports must find
  no import from an internal `edit_cfg_json.*` module.
- Tk, per design section 10.2: stubbed tests as the default category, and
  a `root_or_skip()` fixture giving a withdrawn root for the companion
  tests. Register a `focus_sensitive` marker now even though no test uses
  it yet, and add `excluded_test_markers=['focus_sensitive']` to
  `custom_build_tools/custom_spec.py`, so that category 3 is deselected
  rather than collected from the first day.
- Textual: confirm the headless driver API against the pinned `textual`
  8.2.8 in `./venv` rather than assuming `run_test()` behaves as
  documented elsewhere.
- Examples: `--ui dump` output assertions, plus one headless smoke test per
  backend that launches the example's UI and closes it.

**Risks.** This is the largest step in the plan, because it is the first
one and nothing can be assumed to exist. If it grows beyond a comfortable
review, the split is between the core plus `--ui dump` and the two backends,
in that order.

### Step 2 — Editing the buffer

Status: **Implemented and committed**

**Observable outcome.** `--set name=other --set answer=7 --ui dump` shows the
edited buffer instead of the defaults. In both UIs the two rows are
editable text fields, and the model's dirty indication changes as soon as
a field is edited.

**Core.** The edit buffer becomes writable: set a leaf by path, track
which leaves were edited, and expose a dirty flag for the whole model.
The per-field flags of design section 4.2 get their storage here even
though nothing sets them yet; they belong to the model precisely so the
two backends cannot drift.

**Backends.** Read-only rows become editable fields wired to the model.
Nothing else.

**Examples.** `cmd_line.py` gains `--set member=value`, applied to the
buffer before `--ui dump` or before the UI starts. This is the mechanism that
keeps every later step observable without a display, so it is worth
building properly here.

**Tests.** Core tests for setting, re-setting and dirty tracking; a
headless UI test per backend that types into a field and asserts the model
buffer changed; example `--set` plus `--ui dump` assertions. Edge cases worth
covering: setting a member that does not exist, setting an empty string,
and setting a value whose text is not yet a valid number, because
intermediate invalid states are exactly what design section 4.2 says the
buffer must tolerate.

### Step 3 — Validation of the buffer

Status: **Implemented and committed**

**Observable outcome.** `--set answer=not-a-number --ui dump` prints a
validation verdict and the diagnostics the application itself would
produce at load time. In both UIs a validate action shows the same
verdict, and a value that a validator rewrote is visibly marked.

**Core.** Design section 6.1 exactly: serialize the buffer to JSON text,
construct a candidate config from that text with a captured
`stderr_file`, and catch `KeyError`, `ConfigBadJson`, `TypeError`,
`ValueError`, `InvalidConfiguration`, `InvalidConfigurationValue` and
`InvalidConfigurationType`. On success, refresh the buffer from the
validated object and set the *changed by validator* flag on every leaf the
validation pass rewrote (design section 6.4). Validation is not
read-only, and the model must not pretend otherwise.

**Backends.** A validate action and a place to show the verdict and the
captured diagnostics. The changed-by-validator marking is read from the
model, not computed in the backend.

**Examples.** `e01_flat_config.py` gains a validator on its `int` member
so that there is something to fail, and a `StrCaseChangeValidator` or
similar on its `str` member so that there is something that rewrites.
Without a rewriting validator the section 6.4 behaviour has no example.

**Tests.** One parametrized core test per caught exception type, driven by
a buffer crafted to produce it. A test that a rewriting validator sets the
flag and that the next edit to that field clears it.

### Step 3B — Enums as attributes in Config

Status: **Implemented and committed**

**Observable outcome.** An example is added that has a `Config` class
with 2 enum attributes: one `NeededCompetence(Enum)` and one
`AvailableCompetence(IntEnum)`, both having 3 possible values
`MECHANICAL`, `ELECTRICAL` and `ELECTRONIC` for both
enums. (These values are chosen so that a partly typed value could
be the beginning of more than one enum value.)
The values of these enum attribute is shown in editor and can
be changed in editor.

**Examples.** A new `e02_enum_config.py` holds the 2 enum attributes in a
Config class of its own:

- `needed: NeededCompetence = NeededCompetence.ELECTRICAL`
- `available: AvailableCompetence = AvailableCompetence.MECHANICAL`

There are no explicit validators defined for these 2 attributes,
the teaching story is that there is a validation of enums built into
`config_as_json.Config` and that works in the editor as well,
provided that the `parse_converters()` are set up.

Only `parse_converters()` turns out to need declaring: the write side of
an `Enum` and of an `IntEnum` is a documented built-in fallback of
`config_as_json`, so an explicit `serialize_converters()` would teach that
an application has to write one when it does not. The example says so
instead of declaring a redundant one.

**Core.** Nothing. An enum leaf holds the name of its member, which is
text, so `MemberRow.is_text` already treats it as the text member it is
and both backends already render it. This step is examples and tests only,
and the fact that it needs no core change is itself worth confirming with
tests.

### Step 4 — Loading

Status: **Implemented and committed**

**Decided while building it.**

- `Config.__init__` takes no `ok_to_use_defaults`; it belongs to
  `parse_json()` and `read()`. The derived loader therefore constructs the
  class with no JSON source and then calls `parse_json()` with the policy's
  value. Recorded in `doc/detailed_design.md` section 5.1.
- `Config.read()` ends the process with `sys.exit(1)` for a missing file, so
  the editor reads the file text itself.
- A file whose values a validator refuses **cannot be opened**, because a
  member validator returns the value that is stored back into the member and
  a load that stopped part way through leaves it unknown which values were
  already rewritten. Two further refusals fell out of the work: a file that
  cannot be read at all, and a class the editor cannot construct. All of
  them are recorded in `doc/detailed_design.md` section 5.2.
- Missing and unknown keys are told apart by whether the permissive retry
  rescues the file, which needs no message text and survives ROCF renaming.
  `STRICT` runs the retry too, only to pick which refusal to report.
- New public names: `LoadPolicy`, `load_config`, `LoadedConfig`,
  `LoadReport`, `ConfigLoadError`, and `load_text` beside the other
  renderings. No type alias was needed.
- `cmd_line.py` gained `--policy`, and `examples/data/` holds one input file
  per outcome so that every case can be seen by hand.

**Found in review, and the lesson it carries.** No mark of any member was
visible in the Textual backend, while Tk and `--ui dump` showed all of them.
Textual's `Input` is a full width widget of its own accord, so it took the
whole line and the mark beside it was laid out beyond the right edge of the
screen: present, holding the right text, and visible to nobody. The style
sheet now gives the value what is left over and the marks what they need.

The tests could not see it, because every Textual test asked a widget what
it held rather than where it was. The backend's tests now also assert
**geometry**: that every widget of the editor lies inside the screen, that a
mark is as wide as the mark it shows, and that a terminal too narrow for
both cuts the marks rather than the field. All three fail without the style
rules, which is what makes them worth having. Any later step that adds a
widget to a row should extend them rather than trust the content assertions.

**Observable outcome.** `-i some_file.json --ui dump` shows the values from
the file rather than the defaults, and marks any leaf that a permissive
load filled in from a default. A file with an unknown key and a file that
is not valid JSON each produce their own distinct message and refuse to
open. Both UIs show the loaded values and, when defaults were needed, say
so.

**Core.**

- Derive a loader from `type(config)`, using `inspect.signature()` to
  decide which of the constructor keywords can be passed. Design section
  5.3 explains why the editor must construct the configuration rather
  than receive an already-loaded one.
- `LoadPolicy` with `STRICT`, `DEFAULTS` and `STRICT_THEN_DEFAULTS`,
  defaulting to `STRICT_THEN_DEFAULTS`.
- The three outcomes of design section 5.2 kept distinct: missing keys
  are rescued by the retry and each filled leaf gets the *filled from
  default* flag; an unknown key is not rescued and the file cannot be
  opened; `ConfigBadJson` cannot be opened. `Config.check_key_match()`
  raises `KeyError` for both of the first two cases, so distinguishing
  them is real work and needs its own tests.

**Backends.** Show the filled-from-default marking and the load-level
message. Refusal to open is a message plus an exit, not a silent empty
editor.

**Examples.** `cmd_line.py` wires `-i`. `e01_flat_config.py` documents
the three failure modes in its module docstring, since teaching them is
most of the value of this example.

**Tests.** Parametrized over the three policies crossed with complete,
incomplete, unknown-key and malformed input files. The
`inspect.signature()` branch needs a config class that accepts
`auto_ch_hook` and one that does not. *(That branch is gone: nothing is
passed for the hook any more. See the correction at the end of step 8.)*

**Code and test additions/changes.** It is likely that adding
the enum values to config that is loaded and edited will highlight
incompleteness in design and tests that need to be attended to.

### Step 5 — Saving, and `edit()` — milestone 1

Status: **Implemented and committed.**

**Decided while building it.**

- **`Config.write()` does validate.** It calls `as_json_string()`, whose first
  statement is `self.validate(stderr_file=stderr_file)`, and it opens the
  destination only after the text exists. So the editor's gate is belt and
  braces, and a refused configuration leaves the file on disk untouched. The
  open question of design section 7 is answered there.
- **Saving leaves the editor open.** Save answers "is there anything to
  write"; the session ends when the user closes it. So the Tk button stays
  called Close and the Textual key stays `ctrl+q`: a button called Cancel
  beside values that have already been written would read as an offer to undo
  the writing, which it is not. `edit()` returns what really reached the file.
- **A save moves the baseline.** What has just been written is not waiting to
  be written, so the values that reached the file become the ones the buffer
  is compared against: the title loses its mark and every *edited* mark
  clears. The *changed by validator* mark deliberately stays, because it is
  still true. Recorded in `doc/detailed_design.md` section 4.2.
- **Save with no destination asks.** The model reports that it has none and
  invents nothing; both backends turn that into the Save as question, which
  is what every editor does and what design section 7 asks a backend for.
- `edit()` needs a `backend` argument, which design section 8 had left out:
  the core cannot name a user interface it never imports. Each backend package
  also exports a one-call `edit` of its own. Recorded in section 8.
- New public names: `edit`, `SaveOutcome` and `save_text`, plus
  `EditModel.save`, `out_file`, `set_out_file`, `save_message` and
  `saved_config`. No type alias was needed.
- `cmd_line.py` wires `-o` and gains `--save`, which only means something for
  `--ui dump`: a dump prints once and the run is then over, so there is no
  later moment at which a user could press Save. Every run now ends by saying
  what `edit()` gave back. `--set` moved onto a backend that applies the edits
  and then runs the real one, because `edit()` owns the model and `--set`
  stands in for a user typing into an editor that is already open.
- `EditModel` keeps its rows in a `dict` keyed by `ConfigPath` rather than in
  a list beside an index map. That is what the design already says a leaf is
  addressed by, a dictionary keeps the order it was built in, and it took the
  class back under the instance attribute count that saving pushed it over.

**Found while building it, and the lesson it carries.** The Textual Save as
question was not modal, although it is a `ModalScreen`. Textual dispatches a
**priority** binding from `reversed(screen._binding_chain)`, the whole chain,
while everything else uses `_modal_binding_chain`, which stops at the last
modal screen. The editor's keys are priority bindings, so they went on acting
on the editor underneath: one more `ctrl+s` stacked a second question on the
first, and `ctrl+q` would have abandoned the question altogether. The fix is
`App.check_action`, which turns the editor's own actions off while the
question is up and greys them in the footer. The lesson is the one step 4
already taught in its own way: a Textual screen has to be driven, not
inspected. A test that had only asked the modal what it held would have found
nothing wrong.

The same modal also had to stop its own `Input` messages. They bubble, and the
editor writes every field change into the model, so the name of a file was
being looked for among the members of the configuration.

**Observable outcome.** `-i in.json -o out.json --ui textual` opens the
editor, and Save writes a validated file while Cancel writes nothing.
Save is refused while the buffer is invalid, with the diagnostics from
step 3 shown. `--ui dump` reports what would be saved and where. The same
holds for `--ui tk`.

The editor shall have no opinion about what the filename extension shall
be for input or output files. Some applications use `.cfg`, some use `.json`,
and also other file name extensions are in use.

**Core.**

- Saving is: validate the candidate, and on success call `write()` on it.
  An invalid configuration cannot be saved (design section 7).
- `out_file` defaults to `in_file`. When both are `None` the editor
  starts from defaults and must obtain a destination before it can save;
  for v1 the backends ask for one.
- `edit()` as the thin modal wrapper: build the model, run a backend to
  completion, return the saved `Config` or `None`. The caller's object is
  never mutated.
- Confirm the open question in design section 7: `Config.write()`
  documents a `stderr_file` "used for user-facing diagnostics during
  validation", which suggests it validates too. Check the implementation
  in `./venv` and record the answer in `doc/detailed_design.md`.

**Backends.** Save and Cancel actions, with Save disabled or refused
while invalid. Both backends shall offer both "Save" and "Save as",
the difference is that "Save as" first changes the out_file name and path.

**Examples.** `e01_flat_config.py` shows the full round trip and prints
what `edit()` returned, so that the "returns the saved object, or `None`"
contract is visible rather than merely documented.

**Tests.** Round trip through a temporary file for both backends
headlessly; save refused while invalid; cancel returns `None` and leaves
the output file untouched; the caller's original `Config` object is
unchanged after a save.

**Milestone 1 is reached here.** Before moving on, re-read
`doc/detailed_design.md` section 8 against what was actually built: if either
backend holds logic the other also holds, move it into the core now,
while there are only two small backends to reconcile.

## 4. Milestone 2 — flat config, fully explained, steps 6 to 9

### Step 6 — Descriptions and docstrings

Status: **Implemented and committed.**

**Decided while building it.**

- **The toggle covers all of the explanatory text, and the summary survives
  it.** Shown is the whole class docstring plus a description under every
  described member; hidden is the summary of that docstring and nothing else.
  One line for the whole configuration is worth keeping, and the per-member
  lines are the real cost. The editor starts with the explanations shown,
  because an application that wrote a description mapping wrote it to be read.
  Recorded in `doc/detailed_design.md` section 4.4.
- **Which of two selectors is more specific** had to be settled: a named step
  beats the `'['` step and an earlier step decides before a later one, so no
  two selectors can tie. Recorded in section 4.3.
- **`descriptions` is an optional keyword** and not the required positional
  argument that design section 8 gave it. An application that describes
  nothing is a good caller, and the alternative was every existing call site
  passing an empty mapping to say nothing. `EditModel`'s arguments after the
  load report became keyword-only in the same move, which is what they already
  were at every call site.
- **`model_as_text` gained a head**: the label of the configuration, and then
  as much of the docstring as is being shown. The docstring is the label of the
  configuration object, so it needed the object to be labelled first, and the
  dump had not been showing that label at all.
- New public names: `Descriptions`, `docstring_text`, `row_description`, plus
  `EditModel.summary`, `docstring`, `explanations_shown` and
  `toggle_explanations`, and `MemberRow.description`. `ActionSettings` gained
  `explain`, with `('f1', 'ctrl+g')`. The review added `Emphasis`,
  `EXPLANATION`, `MEMBER_MARK`, `LOAD_REMARK`, `verdict_emphasis`,
  `save_emphasis` and `EditModel.save_outcome`.
- `cmd_line.py` gained `--toggle-explain`, which stands in for the explain key
  as `--set` stands in for typing, and `run_example` gained a `descriptions`
  argument. `SetEditor` became `StandInUser`, since it now does two things a
  user would do.
- The Tk backend gained an Explain button and the Textual one an Explain
  palette entry, so an action whose key a terminal will not deliver is still
  reachable. Both create no widget at all for a member the application said
  nothing about, and none for a class with no docstring.

**Found while building it, and the lesson it carries.** The tests of the Tk
backend went over the 1000 line limit, so they were split: `helpers.py` holds
the stubs, the ways of reading a real Tk window and the widget texts that both
of them expect, `conftest.py` holds the fixture that both need, and the tests
are now `test_tk_editor.py`, `test_tk_saving.py`, `test_tk_keys.py`,
`test_tk_explaining.py` and `test_tk_looks.py`. The tests of the Textual
backend went the same way for the same reason, into `helpers.py` and five test
modules. That was worth doing rather than compacting: the shared expectations
are now in one place, so the modules cannot drift apart about what the editor
looks like.

**Found in review, and what came of it.** Four things that only a window
shows, and one lesson worth keeping.

- **An action that is a toggle has to say which way it goes.** A button called
  Explain that hides the explanations is the wrong reading, and the two
  toolkits need two answers: Tk has a button row, so it gets a tick-box, and
  Textual has a footer of key bindings, so its action is renamed between
  "Explain" and "Hide explanation". Recorded in `doc/detailed_design.md` section 4.4.
- **A configuration of any size does not fit a window**, and with the
  explanations shown it fits one even less. Both backends now scroll the
  label, the docstring, the load message and the members, and keep the
  verdict, the saving and the buttons or footer where they are. Textual gives
  the body the height that is left over; Tk has no scrolling frame and needs a
  canvas, a scrollbar and a frame on the canvas, plus the mouse wheel bound
  where the keys are. Recorded in section 4.6, and the wheel is added to the
  open question of section 8.2.7.
- **A white field on a white window is invisible.** The fields now state their
  own background, text and caret colour, so what can be typed into can be told
  from what only says something.
- **With the explanations there is a great deal of text**, and it is not all
  the same kind of thing. `Emphasis` is the vocabulary the core now has for
  that, `verdict_emphasis` and `save_emphasis` are the two answers that depend
  on the state of the model, and each backend has one table from a kind to
  what its own toolkit understands. Recorded in section 4.5.

**The lesson.** A window is not a text rendering, and the tests that only read
what a widget holds could see none of these four. The Tk tests now read
colours and drive the scrolling, and the Textual tests read the binding that
the footer is built from and scroll the body — which is the same lesson steps 4
and 5 each learnt once already, in their own way.

**Found in the second review, from screenshots of the window.** The scrolling
and the sizes were wrong in three ways that only a real window shows, and all
three are recorded in `doc/detailed_design.md` section 4.6.

- **The part that does not scroll has to be packed first.** Tk gives each child
  the space it asks for in the order they were packed, so a window too short
  for everything laid the verdict, the saving and the buttons out below its
  bottom edge, where no scrolling reached them. The frame is created second, so
  that the widgets are still created in the order they are read in.
- **The size the editor opens at has to be said.** A canvas asks for a width of
  its own that has nothing to do with what is on it, so the window opened 430
  pixels wide and cut off every paragraph. The canvas now asks for what the
  body asks for, up to the size of a window.
- **A Tk label neither wraps nor shrinks.** Every paragraph now follows the
  width it is given, and the mark of a member is the one text that does not:
  a narrow window squeezes the field instead, which is the direction the
  Textual style sheet already gave way in.

**And the lesson that goes with them.** Tk lays out the widgets *inside* a
frame only once the window is mapped, so the withdrawn window of category 2 can
say where the frames are and not what is in them. The three rules are therefore
tested where they are decided — the packing order, the size the canvas asks
for, the line width a label follows — and one test that maps a real window and
measures the lot is the first `focus_sensitive` test in the repository, which
is the category design section 10.2 reserved for exactly this and which the
build has been deselecting since step 1.

**Two things the checkers found in that work, and what they cost.**

- `tkinter.Event[tkinter.Misc]` is a generic class to a type checker and a
  plain one at runtime. Python 3.14 defers an annotation and 3.12 and 3.13
  evaluate it where it is written, so the four wheel and resize callbacks
  write that type as text. Found by the 3.12 build and by pylint, and not by
  mypy or by the 3.14 build, which is the whole reason for the three version
  sweep.
- The two backends had come to import the same twenty names from the core,
  which pylint reported as duplicate code — rightly, and with nothing to
  factor out, because neither backend may import the other. They now reach the
  core through `import edit_cfg_json as core`, which removes the duplication
  rather than hiding it and says at every call site that this is the published
  API of the core and not something local. A local suppression was tried first
  and does not work: pylint reports `duplicate-code` against a module and not
  against a line.

**Observable outcome.** `e03_described_config.py --ui dump` prints the
docstring of the configuration class, one line per member, and the description
of every described member below its member. `--toggle-explain` prints the same
model with the summary and the values alone. Both graphical backends show the
same and hide it again on `f1`, on `ctrl+g`, or with the Explain button or
palette entry.

**What it was planned to be.** Introduce the `Descriptions`
alias, absolute `ConfigPath` keys only, with the more specific selector
winning over the less specific rather than raising. Read class docstrings
with `cls.__doc__` and never `inspect.getdoc(cls)`, so that a nested class
without its own docstring shows nothing instead of showing `Config`'s.
Split at the first blank line into a folded-row summary and an expanded
full text, and put the show/hide toggle in the model. A new example
`e03_described_config.py` shows the same flat config with a description
mapping; `--ui dump` includes the descriptions, and both UIs toggle them.
Risk: the toggle is state that both backends will want to own; it belongs
to the model.

### Step 7 — Field-level diagnostics

Status: **Implemented and committed.**

**Decided while building it.**

- **The candidate that attribution needs cannot be built the ordinary way.**
  `Config.__init__` ends in `parse_json()`, which ends in `validate()`, which
  raises at the first refusal, so the object that could say which member was
  refused is the one a refusal keeps the editor from holding. A throwaway
  subclass whose `get_validation_plan` returns nothing is that object, and the
  plan is then asked of the real class and applied step by step. Recorded in
  `doc/detailed_design.md` section 6.3.
- **It is a subclass rather than a default instance with the buffer assigned
  onto it**, because the subclass gets the whole parse chain for nothing: key
  matching, the dict shape checks, the parse converters, and the nested
  configuration objects that step 11 brings. Assigning would put a copy of
  `_json_parse_obj_hook`'s rule in the editor and a plain dict where a nested
  `Config` belongs. Reviewed at step 7 after a first justification that
  claimed it also rescued a configuration whose declared defaults are invalid;
  that claim was wrong, and it is worth recording why. Such a class cannot
  reach the editor at all — `load_config` constructs it with no JSON source
  and `edit()` is handed an object the caller already constructed, so both
  doors validate the defaults first. `RefuseCfg` in the core tests is exactly
  that class, and it is a test fixture and not a configuration any application
  could use.
- **The walk does not stop at the first refusal**, so every member the user
  has to correct is named at once; and a step that is about no single member
  is applied only while no member has been refused, because that is the only
  case in which `Config.validate()` would have reached it.
- **Where a refusal is shown** is settled in a new section 6.5: at the member
  when it is about one, in the block below the members when it is about none,
  and the verdict line names the members so that a configuration too tall for
  a window does not leave the user hunting. What was attributed is taken out
  of the block, so the same sentence is not on the screen twice.
- **The focus-loss question of design section 4.2 is answered by building
  it.** `EditModel.check_field` is what a backend calls when a field loses the
  focus, from `<FocusOut>` in Tk and `Input.Blurred` in Textual. It is a
  different question from validation and its answer lives for a different
  length of time: per member, cleared by the next edit of that member, while
  what a validator refused is dropped as soon as anything in the buffer
  changes.
- **The converter is run and not read.** `parse_converters()` gives a
  `ParseConverter` whose `func` is what `config_as_json` itself calls, so the
  enum pre-check is that call and nothing about enums is hard coded. An
  application that declared a converter of its own is answered by its own
  converter, which the `HexCfg` of the core tests is there to show.
- **Part C was built, appending rather than replacing.** The enum class of a
  member says the summary of its own docstring and the names it accepts, below
  whatever the application said. Recorded in section 4.3, with the reason it
  is not the validator reading that section 11 rules out permanently. The
  description of `priority` in `e03` was reworded, because it listed the three
  names by hand and that is now the editor's job.
- New public names: `row_diagnostic` and `MEMBER_DIAGNOSTIC`, plus
  `EditModel.check_field`, `MemberRow.converter`, `MemberRow.conversion` and
  `ValidationVerdict.refused`. New internal modules `converting.py` in the
  core and `scrolling.py` in the Tk package. No type alias was needed.
- **The load path is deliberately unchanged.** A file with a bad enum name is
  still refused with the message `config_as_json` prints, because a refusal
  the user cannot act on inside the editor is not a field being edited.

**Found while building it, and the lessons they carry.**

- **`tk_editor.py` went over the 1000 line limit**, so the scrolling body — the
  canvas, the scrollbar, the frame on it, the wheel and the two resize
  callbacks — moved into `scrolling.py`. It is a clean split rather than a cut
  to fit a number: none of it is about an edit model.
- **Two texts under one member cannot both be packed and unpacked freely.** Tk
  packs a widget after the ones that are already there, so a description that
  came back while a refusal was showing landed below it. Both are now taken
  out and put back together, and only when either of them has really changed,
  so typing into a field does not lay the window out again on every key.
- **A withdrawn Tk window swallows a generated focus event.** `event_generate`
  does not stand in for one, so the real companion to the stubbed focus test
  is the second `focus_sensitive` test of the repository. Textual costs
  nothing here: focus is the application's own, so the headless driver moves
  it and the editor is really told.

**Observable outcome.** A new example `e04_validated_config.py` carries a
validator the application wrote and a `ProjectedWholeConfigValidator` over two
members. `--set job_name='a b' --set retries=9` names both members on the
verdict line and puts a sentence under each of them, with nothing left in the
block; `--set retries=5 --set timeout_seconds=400` refuses neither member and
says so in the block alone. `e02_enum_config.py --set needed=ELECT` now shows
`ELECT is not one of: MECHANICAL, ELECTRICAL, ELECTRONIC` under that member
instead of the wrapper about JSON that could not be loaded, and its two
members explain themselves although that example passes no descriptions at
all. Both graphical backends show the same, and say the same as soon as a
field loses the focus.

**What it was planned to be.** Attribute failures to individual fields by
running `MemberValidationStep.validator.validate_member()` for one member of a
complete candidate config, per design section 6.3. A new example
`e04_validated_config.py` carries a custom validator and a projected
validator; the failure now appears on the offending row in both UIs rather
than in one block. Risk: this must work for an application's own
`MemberValidator` subclass, so no test may rely on a validator class that
ships with `config_as_json` being recognised by type. Also: make the enum
validation error message nicer by pre-checking the value against what
`parse_converters()` says the member holds; and evaluate whether the same
introspection can describe an enum member from its class, deciding whether to
build that now, later, or not at all.

### Step 7B — A ready-to-run program in every package

Status: **Implemented and committed.**

Numbered `7B` rather than `8` for the same reason as step 3B: the steps
after it are cross-referenced by number from this file and from
`doc/detailed_design.md`, and renumbering them would be churn with no content in
it. It was the next step because the corpus it unlocks is what steps 8 to
14 need, not because it belongs to milestone 2 by subject.

**Decided while building it.**

- **`run_cli` owns `--save`, and `DumpEditor` does not.** The dump backend
  became a class with no arguments that validates and prints, and the one fact
  `run_cli` is told about a backend is whether it gives the user a session. A
  program whose backend prints once and returns is the one that offers `--save`
  and the one whose exit code answers with the verdict, because both follow
  from there being no user. `--save` is then not added to the parser at all for
  the other two, so it is `argparse` that refuses it rather than a check
  written by hand — which is one refusal fewer than `cmd_line.py` has. In the
  examples the saving moved to `StandInUser`, where it belongs beside `--set`
  and `--toggle-explain`: pressing Save is one more thing a user does.
- **Each way of refusing has an exit code of its own**, twelve of them, in
  `ExitCode`. A program of this library is meant to be usable from a script, so
  a script that wants to tell an uninstalled module from a missing file can.
  `USAGE = 2` is written down there as well although `run_cli` never returns
  it, because it is `argparse` that reports a wrong command line and the number
  is part of the same promise.
- **The shared options were factored out at once** rather than after pylint
  complained. `add_file_options` adds `-i`, `-o` and `--policy` to any parser
  and `named_policy` turns a `--policy` value into a `LoadPolicy`; the examples
  use both, which is what keeps one meaning of those three options from
  becoming two. The name of the default policy is looked up from
  `DEFAULT_POLICY` rather than written twice.
- **`default_config` publishes what `loading._defaults()` already did**, so the
  program does not copy the refusal that names the class or lose the hook.
- **The programs are `[project.scripts]` entries naming each package's
  `__main__:main`**, so the installed script and `python -m` are the same four
  statements. Checked against the install step: the build's package
  consistency step reads only the name, the version, the description, the
  Python requirement and the dependencies, so `[project.scripts]` beside a
  `setup.py` is content, and `venv/bin/` really holds all three programs.
- New public names: `DumpEditor`, `ExitCode`, `run_cli`, `add_file_options`,
  `named_policy` and `default_config`. New modules `cli.py` and
  `constructing.py` in the core, and a `__main__.py` in each of the three
  packages. No type alias was needed.

**What the corpus showed, and why the step was worth having early.** The 47
configuration classes of `dep_lib_doc/config_as_json/example/` found two things
that no example in this repository would have, and both are recorded in
`doc/detailed_design.md` section 8.3.4.

- **32 of the 47 were refused over the name of a constructor parameter.**
  `Config.__init__` names the JSON text `from_json_data_text` and the example
  classes that `config_as_json` ships name it `from_json_text` in the
  constructors they declare, as does `ConfigFactory`. The editor now reads the
  signature and passes every parameter it knows the meaning of, which is
  principle 4 of section 3 applied to a constructor. The one thing that cannot
  degrade quietly is the JSON text: a class with nowhere to put it would be
  constructed on its declared defaults instead, and a buffer validated against
  the defaults would be accepted whatever the user typed, so that is refused
  with a `TypeError`. `NoTextCfg` in the core tests is that class and
  `AltNameCfg` is the other name.
- **One of the 47 cannot serialize itself**, so it crashed the editor with a
  traceback. `ExampleConfig21` leaves part of its own writing to a function
  beside the class, and the editor reads the values it shows with
  `as_json_string()`, so there is nothing for it to show at all. It is now a
  refusal with a message and a number of its own. `NoJsonCfg` in the core tests
  is that class.

**And what came of it.** The four places that construct the application's class
— the declared defaults, the load, the validation of a buffer, and the walk that
attributes a refusal — had three copies of the same constructor call between
them. They now ask `constructing.built_config`, so a fifth shape of constructor
is one edit and not four. After that change 46 of the 47 classes open, and the
one that does not is refused rather than crashing.

**Found while building it, and the lesson it carries.** Written as the plan said
— one subprocess test per package — the two backend program tests were near
copies of each other, and pylint reported `duplicate-code` across them on the
first run. There was nothing to factor out where they were, because neither
backend may import the other, so they became one parametrized table in the
core's test folder, `test_programs.py`, beside the layering tests that are about
all three packages for the same reason. That is the better test as well: one
table names the three programs, their backends and whether each gives the user a
session, and a table cannot drift the way three copies can.

**Observable outcome, as built.** `edit-cfg-json`, `edit-cfg-json-tk` and
`edit-cfg-json-textual` are installed by their packages, each is also
`python -m` on its own package, and all three complete their command lines with
`argcomplete` after one `eval "$(register-python-argcomplete ...)"`.
`PYTHONPATH=examples/src edit-cfg-json --module example.e03_described_config
DescribedConfig` prints that example's configuration with no example being run,
and `PYTHONPATH=dep_lib_doc/config_as_json edit-cfg-json-textual --module
example.e33_nested_configs ExampleConfig33` opens a configuration with nested
objects in it, showing each of them as a row that cannot be edited yet, which is
what step 11 is for.

**What step 16B later changed about that**, so that a command line copied from
this section still runs: the core installs no program, and what
`edit-cfg-json` did is `python3 -m edit_cfg_json.dump` now. The two editor
programs are as this section describes them.

**What it was planned to be.**

**Why it is here and not at the end.** Steps 4, 5, 6 and 7 each recorded a
defect that only a real window holding real content showed: marks laid out
past the right edge of a Textual screen, a Tk canvas that opened 430 pixels
wide, labels that neither wrap nor shrink, a packing order that put the
buttons below the bottom edge, two texts under one member fighting over
pack order. Every one of those is a question about a configuration that is
not two members long, and answering it today costs a hand-written example.
This program answers it with any configuration class in the repository.
`dep_lib_doc/config_as_json/example/` alone holds 37 importable `Config`
classes — 37 of its 39 modules guard their `main` with `__name__`, so
importing them is safe — and they line up with what is left to build:
`e31` and `e37` for old-format reading, `e32` for factories, `e33` to `e35`
for nesting and containers, `e22` for dict key and value types.

**Decided before building it.**

- **It is a product and not only a development tool.** An application
  author gets an editor for their configuration class without writing a
  line of user interface code. The ad-hoc reach during development is a
  second benefit of the same program, not the justification for it.
- **The command line owns no logic.** `edit_cfg_json.cli` holds the
  parsing, the dynamic loading and the reporting, and its entry point takes
  the backend as an argument for exactly the reason `edit()` does: the core
  names no user interface. Each package then ships a program of about four
  statements. Without that split the two backend programs would be near
  identical, and design section 8 answers duplicate code between the
  backends by moving logic into the core rather than by suppressing the
  warning. It is also what makes the program testable with no display and
  no toolkit, by handing `run_cli` a stub backend.
- **Three programs, one per distribution.** `edit-cfg-json` runs the dump
  backend, needs no display, and is a configuration validator for a
  terminal or for CI; `edit-cfg-json-tk` and `edit-cfg-json-textual` open
  the editor. Each is reachable as `python -m` on its package as well, so a
  machine whose script folder is not on `PATH` can still run it.
- **The dump backend becomes public.** `DumpEditor` moves into the core,
  because the core's own program needs it and because `cmd_line.py` holds
  one already. `StandInUser` stays in the examples, and it is what teaches
  that a backend is one method and anything with that method will do.
- **The class is told, and never guessed.** `--module MODULE` or
  `--file PATH`, exactly one of them required, with the class name as a
  positional argument. A single `module:Class` argument reads well and
  would have to guess which of the two it was given; design section 8.2.1
  settled that this library is told and does not guess. It also keeps a
  Windows drive letter from being a special case, and it lets `argparse`
  produce the refusal for a missing or a doubled location.
- **`--policy` now, and the rest at step 19.** A load policy is what a
  generic launcher meeting a half-written file needs first.
  `--extension`, `--enforce-extension`, `--key` and `--descriptions` are
  what the application would know about itself, and they are worth having,
  but not before the corpus is reachable.
- **`--save` for the core's program only**, exactly as in `cmd_line.py`: a
  dump prints once and the run is then over, so there is no later moment at
  which a user could press Save. That is what makes the core's program able
  to normalise a file and not only to judge it.
- **`edit()` takes an object and the program has a class**, so the program
  must construct one. `loading._defaults()` already does that, with the
  `inspect.signature()` hook opt-in and the refusal that names the class,
  so it is published as `default_config` rather than copied. Confirm the
  name at the start of the step; the alternative is four statements in the
  CLI that duplicate the refusal message and lose the hook.
- **The entry-point group of design section 8.1 stays deferred.** Three
  programs that each supply their own backend need no discovery. A
  `--ui auto` launcher is what would, and it is still only worth building
  for a third-party backend.
- **The program does not replace an example.** Rule 2 of section 1 holds
  unchanged: what a step does stays observable from
  `examples/src/example/`.
- all 3 program shall use `argcomplete`, which is available in venv

**Observable outcome.**

- `edit-cfg-json-tk --module myapp.config AppConfig -i /etc/myapp.json`
  opens the Tk editor on that application's configuration, with no code
  written by anybody. `--file ./somewhere/cfg.py AppConfig` does the same
  for a class that is not installed.
- `edit-cfg-json --module myapp.config AppConfig -i in.json` prints the
  model as text and the verdict, on a machine with no display, and with
  `--save` writes the validated file.
- `PYTHONPATH=dep_lib_doc/config_as_json edit-cfg-json-textual --module
  example.e33_nested_configs ExampleConfig33` opens a configuration with
  nested configuration objects in it, which this repository has written no
  example for and which the editor does not support yet. Whatever that
  shows is the point of the step.
- Each refusal has its own message and its own exit code: neither location
  given, both given, a module that is not installed, a file that is not
  there or is not Python, a name the module does not hold, a name that is
  not a `Config` subclass, and a class the editor cannot construct.

**Core.**

- New module `edit_cfg_json/cli.py`: the parser, the two doors to a class,
  the construction, one editing session and the exit code. `run_cli` takes
  the backend, the program name and optionally the argument list.
- `default_config`, publishing what `loading._defaults()` already does.
- `DumpEditor`, moved in from `cmd_line.py` and re-exported.
- New `edit_cfg_json/__main__.py`, four statements, running `run_cli` with
  `DumpEditor`.
- **The file door puts the file's own folder at the front of `sys.path`
  and imports by the file's stem**, so a module that imports its siblings
  works. A module inside a package that uses relative imports cannot be
  loaded from a bare path at all, and is refused with a message that says
  to use `--module` with `PYTHONPATH` instead. That is not a corner case:
  `e33` in `dep_lib_doc` is exactly such a file, which is why the
  observable outcome above reaches it through `--module`.
- **Importing a module runs it.** The help text and the readme say so. It
  is not guarded against, because it is the same exposure as
  `python somefile.py` and a guard could only be a pretence.

**Backends.** One `__main__.py` per backend package supplying its own
backend, and `[project.scripts]` in each `pyproject.toml`. No change to
`TkEditor`, to `TextualEditor` or to either package's `edit`.

**Examples.** `cmd_line.py` imports `DumpEditor` from the core instead of
defining one, and says in its docstring that the core ships that backend
and that `StandInUser` below it is one written by hand. Nothing else: the
examples keep their own command line, which is about teaching and not
about launching.

**Tests.**

- Core, parametrized over the refusals: no location, both locations, an
  uninstalled module, a missing file, a file that is not Python, a name the
  module does not hold, a name that is not a `Config` subclass, and
  `ExtraArgCfg` for the class that cannot be constructed. Each asserts the
  message and the exit code, not one or the other.
- The `--module` door through the test package's own
  `test_edit_cfg_json.sample_cfg`, and the `--file` door through a
  self-contained configuration module written into `tmp_path`.
- A round trip with a stub backend that saves, and `--policy` crossed with
  a complete and an incomplete input file.
- `sys.modules` and `sys.path` are left as they were found after a
  `--file` run, because that door mutates both.
- One subprocess test per package that `python -m` really runs and really
  supplies that package's backend. These pass against installed wheels,
  which is what the build tests anyway, and will fail during fast
  iteration until `./run_build.py` has run.

**Risks.** Both are about duplicate code, and neither is answered by a
suppression.

- The core CLI's options overlap `cmd_line.py`'s `-i`, `-o` and
  `--policy`. If pylint reports it on a clean build, the answer is a core
  function that adds the shared options to a parser, which would shrink the
  examples as well.
- The core's `DumpEditor` would overlap the examples' copy, which is why
  the copy goes rather than stays.

Also check that the build's package consistency step is content with
`[project.scripts]` in a `pyproject.toml` whose `name` a `setup.py` also
declares, against the install step rather than by assumption.

### Step 8 — Automatic-change visibility

Status: **Implemented and committed.**

**Decided while building it.**

- **The hook the editor passed could not report anything at all.** *(Corrected
  by `config_as_json` 1.5, see the note at the end of this step.)*
  `Config.__init__` stored `deepcopy(auto_ch_hook)` and recorded into that
  copy, so a hook that was read afterwards answered with nothing. Confirmed
  against `./venv` at the time: after a migrating load the editor's own hook
  was empty. `ConfigAutoChangeHook.auto_changed` writing to a stream is why
  `MigrateCfgWarnHook` never noticed. The editor's hook was a subclass whose
  `__deepcopy__` returned itself, which was the one thing that made the report
  reach the editor.
- **Three facts, and each of them where it can be seen.** A key of the file
  that the configuration does not write back is in the message alone, because
  it is no member and has no row; a member whose value the file does not hold
  is marked on its row; and the older keys that only the class can name are in
  the message where the hook has spoken, in place of the editor's own reading
  of the same keys rather than beside it. *(The third of these is now said at
  the member instead; see the note at the end of this step.)*
- **The `filled from default` flag became exact.** Computing it from the keys
  of the file said that a member ROCF had renamed into was filled in from a
  default, which is untrue of it, and it was untrue for *every* older file
  under `--policy defaults` rather than only for the corner that section 5.2
  had recorded. It is now what the key check of the parse was not given, read
  by a throwaway subclass whose `check_key_match` records and stops. Stopping
  is what keeps the application's validators running once; a test with a
  counting validator says so. `_absent` and `_declared` in `loading.py` are
  gone with it.
- New public names: `LoadReport.changed` and `MemberRow.changed_by_load`, plus
  `LOAD_MARK` in `model_text` and the message forms in `loading`. New internal
  module `auto_change.py`. No type alias was needed, and neither backend
  changed: both already show `core.load_text` and `core.row_marks`.
- The example declares two classes over one set of `ReadOldConfiguration`
  rules: `OldFormatConfig`, which takes the hook and is what `main()` runs, and
  `NoHookConfig`, which does not and is reached through the program of step 7B,
  as its docstring shows. The same file read by both is what says that the
  marks do not depend on the hook.

**Found while building it, and the lesson it carries.** Adding two constants to
the shared `helpers.py` of each backend's tests tripped pylint's
`duplicate-code` across the two packages: the block of load expectations they
already shared was three code lines, which is under the threshold, and it went
over. Attribute docstrings are not docstrings to that checker, so a block that
looks long is counted by its assignments alone. The new expectation now lives in
the one test module of each package that uses it, which is where a constant used
once belongs anyway. A local suppression was not an option: step 6 already found
that `duplicate-code` is reported against a module and not against a line.

**Observable outcome, as corrected.** `e05_old_format_config.py --ui dump -i
examples/data/e05_old_format.json` marks the three members that reading the file
put there or altered and leaves the fourth alone, and each mark says what
happened to that member: supplied for an older file, read from the older key
`title`, changed by the load. The message keeps the one key that became no
member, `debug_trace`. The same file through `edit-cfg-json --module
example.e05_old_format_config --class NoHookConfig` says the same word for word.
`-i examples/data/e05_current.json` says nothing at all. Both graphical backends
show the same, with no change to either of them.

**What it was planned to be.** Load the file, re-serialize the resulting config
and diff that against the raw file text; any difference means the load changed
something. Use the structured `ConfigAutoChangeHook` report to explain the diff
when the application's class accepts a hook, and do without it otherwise. A new
example `e05_old_format_config.py` carries `ReadOldConfiguration` rules, so
opening an old-format file visibly reports the migration. Risk: the
hook-independent diff is the primary mechanism and must be tested with a
config class that does *not* accept a hook.

**Corrected against `config_as_json` 1.5.** Three of the decisions above no
longer hold, and each of them because the library now offers something better.
The re-serialize-and-diff comparison is untouched and is still the mechanism,
for the reason it always was: a value that a member validator rewrote is
recorded nowhere.

- **No hook is passed and none is opted into.** `Config.__init__` keeps the
  hook by reference and creates one where the application named none, and
  `Config.auto_change_hook()` publishes it. So the `__deepcopy__` work-around
  is gone, `built_config` and `ConfigSource.made` no longer take a hook, the
  `auto_ch_hook` parameter is gone from `ConfigLoader` (step 9), and a class
  that declares nothing is reported on exactly as fully as one that declares
  the parameter. `NoHookConfig` in `e05` now says the same as `OldFormatConfig`
  word for word, which is a better teaching point than the old one.
- **The older keys are said at the member, not in the message.** `hook.changes`
  holds one `RocfChange` per automatic change, with its kind, the path of the
  file it consumed and the path it produced, so `report_name` is marked *read
  from the older key title* and `format_version` *supplied because this file is
  in an older format*. `LoadReport.changed` became `LoadReport.reasons` and
  `MemberRow.changed_by_load` became `MemberRow.load_reason` with it. A key
  that a member received is also taken out of the keys the message says saving
  leaves out, which the comparison alone had wrong.
- **A future version of the records degrades to text.**
  `ConfigAutoChangeHook.check_data_version` is asked first, and a version this
  editor was not written for falls back to the marks the comparison alone gives
  plus the text of `print_changes`, which is version independent by contract
  and is never parsed. Recorded in `doc/detailed_design.md` section 5.3.

### Step 9 — The explicit loader

Status: **Implemented and committed.**

**Found before building it, which decided the shape of the step.** A class the
editor cannot construct was refused in *four* places and not one: the declared
defaults, the load, the candidate that validates a buffer, and the probe that
attributes a refusal to a member. A loader that only fixed the load would have
opened a file into an editor that could never validate or save it.

**Decided while building it.**

- **A buffer becomes a configuration by copying and parsing, not by
  constructing.** `deepcopy` of the object of the session plus the public
  `Config.parse_json` runs the same chain a construction runs — key matching,
  the dict shape checks, the parse converters, the nested objects, the plan —
  and needs nothing of the constructor. The derived loader never gave the text
  to a constructor either, because the load policy belongs to `parse_json`, so
  nothing was lost. Two refusals disappeared with it: a class needing a
  constructor argument this library knows nothing about, and a class with no
  JSON text parameter at all, are now edited, validated and saved like any
  other, with no loader. `built_config` lost its `text` argument and
  `NO_JSON_TEXT` with it. Recorded in `doc/detailed_design.md` sections 5.1, 6.1 and
  8.3.4.
- **The two throwaway subclasses became one method replaced on one copy.** A
  subclass cannot be used where a loader constructs the application's class,
  and replacing the method on the object leaves the real one where the walk of
  section 6.3 needs it. `parse_json` counts the attributes that are not
  callable, so the replacement is no member. `constructing.parsed_config` is
  the one place both probes and the candidate go through.
- **Loading is therefore the only thing the loader is needed for**, which is
  what design section 5 said it was for all along. It reaches `edit`,
  `load_config` and `EditModel`; the model needs it for one thing only, which
  is the save.
- **A save asks the loader whether the file it is about to write would be read
  back**, and refuses when it would not, or when it would be read as another
  class. That is the one question a validation pass cannot answer, because the
  pass applies the buffer to the class of the session. `isinstance` is what the
  class question asks. Recorded in section 7.
- **A class-choosing loader is supported**, with two rules: a loader answers a
  call with no JSON source, and the class is chosen when the file is loaded and
  the session then edits that class. `config_factory_from_json` cannot be a
  loader as it stands — it needs exactly one JSON source and it ends the
  process — so an application wraps it, and every call the editor makes goes
  through `ask_loader`, which turns `SystemExit` into a refusal.
- **`derived_loader` is published**, so that an application with one extra
  constructor argument writes one line instead of a six line wrapper. It reads
  a signature, and `functools.partial` over a class has one.
- **`--class` replaces the positional class name**, symmetric with the new
  `--loader`; at least one of the two is needed, both are allowed, and both
  together check the class of the object that will really be edited. Three exit
  codes were added: 13 for a name that cannot be called, 14 for a loader whose
  own arguments are not bound, 15 for a loader that answered with the wrong
  class.
- New public names: `ConfigLoader`, `derived_loader`, plus `loader` keywords on
  `edit`, `load_config`, `EditModel` and both backends' `edit`. New internal
  module `loader.py` holding the protocol, `derived_loader`, `ask_loader` and
  `ConfigSource`, and `saving.reload_refusal`. No type alias was needed.

**Found while building it, and the lesson it carries.** *(No longer applies:
`config_as_json` 1.5 removed the deep copy this is about, so a copy of the
configuration carries a copy of the hook and no later parse can disturb what
the load recorded. See the correction at the end of step 8.)* The hook that
reports the automatic changes of an old format file said that a copy of itself
was itself, which was the only way its report reached the editor. Once the probe
for the *filled from default* flag became a copy of the loaded object rather
than a fresh subclass, that probe reported into the same hook a second time and
every older key was named twice. `file_changes` therefore read the hook before
anything parsed the file again. The lesson was that a channel back to the editor
is shared by every copy of the object, so what it holds has to be read before
the next parse and not after it.

**Found in review, and what came of it.** Four things, of which the first is
the one that mattered.

- **A Tk window that never settled.** Ticking Explain flickered between two
  window sizes for ever. Measured in a real window: one toggle cost 19099
  resizes in two seconds and never stopped, against about ninety after the fix.
  The canvas followed the width of the body, and a paragraph that has wrapped
  asks for the width of its longest line, which is a little less than the width
  it was given — so the window narrowed, the paragraph wrapped into one more
  line, and asked for something else again. The width the editor opens at is now
  said and not measured, and the height still follows the body. Recorded in
  `doc/detailed_design.md` section 4.6 through `BODY_WIDTH`; the loop is guarded by a
  stubbed test, whose stub now reports a body narrower than the opening width,
  and by a mapped `focus_sensitive` test. Both were checked by reverting the fix.
- **A width that cannot be measured at all.** Two attempts to keep measuring it
  failed before that: the first Configure of the body arrives while it is still
  empty, and Tk delivers the wrap-triggering Configure inside its own idle pass,
  so a body that has been laid out always asks for about the width it already
  has. There is no moment in between, which is why the width is a constant.
- **`--toggle-explain` is a key and can be pressed twice.** It counts now, so
  two of them show the explanations again.
- **A program showed no explanations under its members**, and two things were
  behind that. What the application says about its members needed a door, which
  is `--descriptions NAME`, brought forward from step 19 with exit code 16 for a
  name that is no mapping. And what the *editor* knows about a member needed
  saying at all: every editable member now says what kind of value it holds, and
  whether the class may leave it out of the file. Recorded in sections 4.2 and
  4.3; `leaf_value.value_kind`, `descriptions.type_text` and
  `descriptions.optional_members` are what say it, and every expectation of a
  described member in every test moved with it.
- The two classes of `e07_chosen_class.py` gained a second paragraph in their
  docstrings, because a review that could not see the explanations was looking
  at classes whose docstring was one line.

**Observable outcome.** `e06_factory_config.py` declares a class that is told
which teams exist, so the editor cannot construct it, and hands over
`derived_loader(partial(TeamConfig, KNOWN_TEAMS))`. `--ui dump -i
examples/data/e06_teams.json --set team=alp` completes the name to `alpha` by
the rule that only the application could have written, and the same file through
`edit-cfg-json --module example.e06_factory_config --class TeamConfig` is refused
with the message that names the class, while `--loader team_loader` opens it.
`e07_chosen_class.py` declares two classes of the same shape and a loader
written by hand that picks by the `mode` member: `-i examples/data/e07_model.json`
edits `Cad3DConfig`, `--set mode=2D --save` is refused because the file would be
read as `Cad2DConfig`, and the drawing file with `--set mode=3D --save` is
refused because the model class would not read it back at all. Both graphical
backends show the same.

**What it was planned to be.** Add the `ConfigLoader` protocol and the
`loader` parameter, completing the `edit()` signature of design section 8.
A new example `e06_factory_config.py` has a config needing constructor
arguments this library knows nothing about, bound with
`functools.partial` before the callable reaches the editor. Risk: the
protocol signature is closed on purpose; resist adding parameters to it.

The program of step 7B gains its factory door here, and it is the only
part of this step that is not simply additive. A `--loader NAME` names a
`ConfigLoader` in the same module or file that `--module` or `--file`
already named, and the program calls it with no JSON source to get the
object that `edit()` wants as its `config`. Two things to settle when the
step starts: whether the positional class name stays required when a
loader is named, and what the program does with a loader that a command
line cannot finish binding — because `functools.partial` over arguments
this library knows nothing about is precisely what a command line cannot
supply, and saying so plainly is better than a half-answer.
