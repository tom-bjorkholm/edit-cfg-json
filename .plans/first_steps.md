# Delivering the v1 scope in small steps

This document turns section 10 of [`doc/design.md`](doc/design.md) into an
ordered list of small, individually reviewable and individually
committable steps. It is a delivery plan, not a design document: where it
mentions a design decision, `doc/design.md` remains the authority and this
file only says *when* that decision gets built.

## 1. How this plan is meant to be used

- One step is one branch-less unit of work on `master`: implement, verify,
  ask for review, commit. The next step does not start until the previous
  one is committed.
- Every step changes what an example program does. If a step cannot be
  observed from `examples/src/example/`, it is the wrong step boundary and
  should be merged into a neighbour or split differently.
- Every step touches all three packages where the capability is
  user-visible, so `edit_cfg_json`, `edit_cfg_json_tk` and
  `edit_cfg_json_textual` never drift apart by more than one review.
- Steps 1 to 5 are specified in detail. Steps 6 to 15 are specified as
  named steps with their observable outcome and their main risks; they are
  detailed just before they are started, when the core API is real rather
  than imagined.

### 1.1 Decisions this plan is built on

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

### 1.2 Definition of done for one step

A step is finished when all of the following hold.

1. A short design summary was posted before editing, per `CLAUDE.md`.
2. Code, tests and example changes are all in place.
3. `./run_clean_build.py python3.12`, then `./run_clean_build.py
   python3.13`, then `./run_clean_build.py python3.14` each exit 0.
   They run sequentially; there is one `./venv` and the three cannot be
   run in parallel.
4. For each of those three runs, `./reports/index.html` says
   `Build succeeded` with no errors or warnings, and
   `./reports/mypy_errors.txt`, `./reports/flake8_log.txt`,
   `./reports/python_layout_log.txt` and `./reports/pytest_log.txt` are
   clean. Every issue the tools report anywhere in the repository is
   fixed, not triaged as unrelated.
5. A summary of the changes and of any oddities noticed is written up.
6. The step is reviewed and committed.

Note that the last of the three builds leaves `./venv` on that Python
version. Record which one, because the next step's fast iteration with
`./run_static_checks.py` and targeted `pytest` runs uses that venv.

### 1.3 Naming conventions used below

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
| `ConfigLoader` | `Protocol` | step 9 |

`Descriptions` is the only type alias the design asks for, and
`doc/design.md` section 2.6 already declares it, so introducing it in step
6 needs no further permission. Any *additional* alias needs permission
first, per `CLAUDE.md`. (Do ask for permission when an alias would improve
code quality - do not see the need for permission as a hint to avoid
all aliases.)

## 2. Milestones

| Milestone | Steps | What exists at the end |
| --- | --- | --- |
| M1 Flat round trip | 1 to 5 | Both backends edit a `Config` with one `str` and one `int`, validate it and save it |
| M2 Flat, fully explained | 6 to 9 | Descriptions, docstrings, field-level diagnostics, automatic-change visibility, explicit loader |
| M3 Structure and folding | 10 to 12 | Lists, dicts, nested `Config` objects, folding with per-subtree badges |
| M4 Configs in containers | 13 to 14 | `LIST_ELEMENT` and `DICT_VALUE` nesting, adding and removing elements |
| M5 Release readiness | 15 | v1 documented, classified and published |

## 3. Steps 1 to 5, in detail (milestone 1)

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
- Tk, per design section 9.2: stubbed tests as the default category, and
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

### Step 4 — Loading

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
`auto_ch_hook` and one that does not.

### Step 4B - Enums as attributes in Config

**Observable outcome.** An example is added that has a `Config` class
with 2 enum attributes: one NeededCompetence(Enum) and one
AvailableCompetence(IntEnum), both having at least 3 possible values
and 2 of these values should be `ELECTRICAL` and `ELECTRONIC`.
(These values are chosen so that a partly typed value could
 be the beginning of more than one enum value.)
The values of these enum attribute is shown in editor and can
be changed in editor.

**Code and test addictions/changes.** It is likely that adding
the enum values to config that is loaded and edited will highlight
incompleteness in design and tests that need to be attended to.

### Step 5 — Saving, and `edit()` — milestone 1

**Observable outcome.** `-i in.json -o out.json --ui textual` opens the
editor, and Save writes a validated file while Cancel writes nothing.
Save is refused while the buffer is invalid, with the diagnostics from
step 3 shown. `--ui dump` reports what would be saved and where. The same
holds for `--ui tk`.

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
  in `./venv` and record the answer in `doc/design.md`.

**Backends.** Save and Cancel actions, with Save disabled or refused
while invalid.

**Examples.** `e01_flat_config.py` shows the full round trip and prints
what `edit()` returned, so that the "returns the saved object, or `None`"
contract is visible rather than merely documented.

**Tests.** Round trip through a temporary file for both backends
headlessly; save refused while invalid; cancel returns `None` and leaves
the output file untouched; the caller's original `Config` object is
unchanged after a save.

**Milestone 1 is reached here.** Before moving on, re-read
`doc/design.md` section 8 against what was actually built: if either
backend holds logic the other also holds, move it into the core now,
while there are only two small backends to reconcile.

## 4. Steps 6 to 15, as named steps

Each of these is detailed just before it is started. What is fixed now is
the order, the observable outcome and the main risk.

### Milestone 2 — flat config, fully explained

**Step 6 — Descriptions and docstrings.** Introduce the `Descriptions`
alias, absolute `ConfigPath` keys only, with the more specific selector
winning over the less specific rather than raising. Read class docstrings
with `cls.__doc__` and never `inspect.getdoc(cls)`, so that a nested class
without its own docstring shows nothing instead of showing `Config`'s.
Split at the first blank line into a folded-row summary and an expanded
full text, and put the show/hide toggle in the model. A new example
`e02_described_config.py` shows the same flat config with a description
mapping; `--ui dump` includes the descriptions, and both UIs toggle them.
Risk: the toggle is state that both backends will want to own; it belongs
to the model.

**Step 7 — Field-level diagnostics.** Attribute failures to individual
fields by running `MemberValidationStep.validator.validate_member()` for
one member of a complete candidate config, per design section 6.3. A
complete candidate must be built first, because `validate_member` receives
the whole config and may inspect other members. A new example
`e03_validated_config.py` carries a custom validator and a projected
validator; the failure now appears on the offending row in both UIs rather
than in one block. Risk: this must work for an application's own
`MemberValidator` subclass, so no test may rely on a validator class that
ships with `config_as_json` being recognised by type.

**Step 8 — Automatic-change visibility.** Load the file, re-serialize the
resulting config and diff that against the raw file text; any difference
means the load changed something. Use the structured
`ConfigAutoChangeHook` report to explain the diff when the application's
class accepts a hook, and do without it otherwise. A new example
`e04_old_format_config.py` carries `ReadOldConfiguration` rules, so
opening an old-format file visibly reports the migration. Risk: the
hook-independent diff is the primary mechanism and must be tested with a
config class that does *not* accept a hook.

**Step 9 — The explicit loader.** Add the `ConfigLoader` protocol and the
`loader` parameter, completing the `edit()` signature of design section 8.
A new example `e05_factory_config.py` has a config needing constructor
arguments this library knows nothing about, bound with
`functools.partial` before the callable reaches the editor. Risk: the
protocol signature is closed on purpose; resist adding parameters to it.

### Milestone 3 — structure and folding

**Step 10 — Lists and dicts of scalars.** Ordinary JSON structure inside
one config's ownership region: render as an indented tree and edit the
leaves. No adding, no removing, no nested configs. A new example
`e06_lists_and_dicts.py`. Risk: this is where `model_as_text` and the two
backends stop being trivially parallel; expect to move tree flattening
into the core.

**Step 11 — Nested `Config` objects.** `nested_configs()` becomes the
first-authority source it is in design section 4.1. A nested config is a
first-class node with its own type, docstring and validity state, and it
segments the tree. A new example `e07_nested_config.py`, modelled on
`e33_nested_configs.py`. Open question to settle when this step starts:
`ConfigNestingKind` also has `OPTIONAL_MEMBER`, which design section 10
neither includes nor excludes. Decide it explicitly rather than by
accident.

**Step 12 — Folding and subtree validation.** Fold state in the model,
and folding a nested config validates that subtree by constructing its
`config_type` from that subtree's JSON. Show *subtree-valid* and
*config-valid* as the two distinct states they are; a subtree can be valid
while the root is not, and both should be shown. `e07_nested_config.py`
gains the badges. Risk: a `WholeConfigValidator` on a parent relates
members across a nesting boundary, so a green subtree badge must never be
allowed to read as "the file can be saved".

### Milestone 4 — configs in containers

**Step 13 — `LIST_ELEMENT` and `DICT_VALUE` nesting.** Repeated nested
configs, and the `'['` step in description paths meaning "every list
element or every dictionary value at this point", which is what stops the
application repeating itself per index or per key. A new example
`e08_config_containers.py`, modelled on `e34_list_nested_configs.py` and
`e35_dict_nested_configs.py`.

**Step 14 — Adding and removing elements.** Add and remove elements of
uniform lists and dicts, with the template taken from the default instance
or from the nesting declaration. Where a container's default is empty and
it has no nesting declaration, there is no template and none can be
invented: the UI says so and offers reorder and remove but not extend.
`DICT_VALUE_BY_KEY` members and dicts listed in `_unchecked_dicts` are out
of v1 scope and must be reported as such rather than half-supported. A new
example `e09_add_remove.py` demonstrates all three cases side by side,
including the two that are refused.

### Milestone 5 — release readiness

**Step 15 — v1 polish.** Rewrite the `readme_parts/` of all three
packages against what was actually built; regenerate the API documents in
`doc/`; confirm that the Alpha wording of design section 2.5 and the PyPI
classifiers still say what they should; verify that
`additional_venv_packages` in `custom_build_tools/custom_spec.py` is
genuinely redundant now that the packages declare their real dependencies,
against the install step rather than by assumption; check that
`BuildSpec.identical_versions` still holds across the three
`pyproject.toml` files; and run the three-version sweep one final time
before release.

## 5. Open questions recorded, not answered

These do not block step 1, and each is scheduled to be answered at the
step that needs it. They are listed here so they are not forgotten.

| Question | Answer needed by |
| --- | --- |
| When does a field report that its text means no value at all, and is that on focus loss? See `doc/design.md` section 4.2. | raised at step 3, settled no later than step 7 |
| Does `Config.write()` validate, making the editor's gate belt and braces? | step 5 |
| Is `ConfigNestingKind.OPTIONAL_MEMBER` in v1 scope? | step 11 |
| Does the Textual headless driver in the pinned 8.2.8 behave as the design assumes? | step 1 |
| Will the README test summary stop updating on a headless machine, per design section 9.2? | step 1, as a known consequence |
