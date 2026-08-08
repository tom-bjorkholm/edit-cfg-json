# Delivering the v1 scope in small steps

## Where everything is

Steps 1 to 9 are implemented and committed, and each is written up in
[steps_001-009_done.md](steps_001-009_done.md). The steps still to build are
in [steps_010-x.md](steps_010-x.md). Where either file mentions a design
decision, [`doc/design.md`](../doc/design.md) remains the authority and the
plan says only *when* that decision gets built.

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
- [Step 10](#step-10--lists-and-dicts-of-scalars) — lists and dicts as a tree
  of rows with a field at every value, folding, and the rows being built again
  when a validator changes how many of them there are.

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

## 1. How this plan is meant to be used

This document turns section 11 of [`doc/design.md`](../doc/design.md) into an
ordered list of small, individually reviewable and individually
committable steps. It is a delivery plan, not a design document: where it
mentions a design decision, `doc/design.md` remains the authority and this
file only says *when* that decision gets built.

- One step is one branch-less unit of work on `master`: implement, verify,
  ask for review, commit. The next step does not start until the previous
  one is committed.
- Every step changes what an example program does. If a step cannot be
  observed from `examples/src/example/`, it is the wrong step boundary and
  should be merged into a neighbour or split differently.
- Every step touches all three packages where the capability is
  user-visible, so `edit_cfg_json`, `edit_cfg_json_tk` and
  `edit_cfg_json_textual` never drift apart by more than one review.
- Steps 1 to 9 are built, and each is written up in
  [steps_001-009_done.md](steps_001-009_done.md) as what it decided, what it
  found while building it and what came of its review. Step 10 is built and is
  written up here, in the same way. Steps 11 onwards are named steps with their
  observable outcome and their main risks; they are detailed just before they
  are started, when the core API is real rather than imagined.

### 1.1 Definition of done for one step

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

## 2. Milestones

| Milestone | Steps | What exists at the end | Status |
| --- | --- | --- | --- |
| M1 Flat round trip | 1 to 5 | Both backends edit a `Config` with one `str` and one `int`, validate it and save it | done |
| M2 Flat, fully explained | 6 to 9 | Descriptions, docstrings, field-level diagnostics, automatic-change visibility, explicit loader | done |
| M3 Structure and folding | 10 to 12 | Lists, dicts, nested `Config` objects, folding with per-subtree badges | step 10 done |
| M4 Configs in containers | 13 to 14 | `LIST_ELEMENT` and `DICT_VALUE` nesting, adding and removing elements | to do |
| M5 Release readiness | 15 to 17 | v1 documented, classified and published | to do |

## 3. Steps 10 to 20, as named steps

Each of these is detailed just before it is started. What is fixed now is
the order, the observable outcome and the main risk.

### Milestone 3 — structure and folding

#### Step 10 — Lists and dicts of scalars

Status: **Implemented and committed.**

**Observable outcome.** A new example `e08_lists_and_dicts.py` whose members
hold lists and dicts of values.
`python3 examples/src/example/e08_lists_and_dicts.py --ui dump` prints them as
a tree with a row per value, `--set retry_delays.0=2` edits one of those
values, `--fold ports` folds one container away and `--toggle-fold` folds all
of them. `--ui tk` and `--ui textual` show the same tree with a control on
every container row and one key that folds or opens all of them.

**What it decided.** Four things, decided before the work started and recorded
in `doc/design.md` where each of them belongs.

- **A container opens open unless opening it would flood the window**, which
  is `OPEN_AT_MOST` rows counting everything inside it. Design section 4.7.
- **Two ways of folding**: a control on the row and one new `ActionSettings`
  attribute for all of them at once. Design sections 4.7 and 9.1.
- **A nested `Config` object stays one row** that says the editor cannot edit
  it yet, rather than being shown as the dict it serializes to. Step 11 makes
  it a node of its own. Design section 4.1.
- **Where those objects are is asked as a path and not as a member name.**
  A configuration worth editing is not a handful of scalars, and a *list* of
  nested objects each holding a dict of more of them is the ordinary shape
  rather than a special case. So a nesting declaration becomes a selector,
  `('outputs', '[')` for a list of them, the member that holds them is an
  ordinary container of the tree, and each object inside it is one node.
  Steps 11, 13 and 14 then change what a nested node *is* and not how the
  tree is built. Design section 4.1.
- **A value inside a container is written with a dot between the path
  steps**, which is what `--set` and `--fold` take and what the verdict line
  writes. Design sections 4.1 and 6.5.

**Core.** `tree` takes a configuration apart into nodes and puts it back
together; `rows` owns `MemberRow` and builds the rows of one configuration,
carrying over what an earlier row knew; `buffer` holds the rows, the fold
state and the editing, so that `EditModel` stays the session it always was.
`ValidationVerdict.refused` is keyed by `ConfigPath` rather than by name,
because two values inside two different dicts can share a name.

The public names it settled:

| Name | Kind |
| --- | --- |
| `MemberRow.children` | the paths inside one node, None for a value |
| `MemberRow.depth` | how far inside a member of the configuration it is |
| `MemberRow.foldable` | whether it is a container that can be folded |
| `MemberRow.folded` | whether its rows are hidden |
| `MemberRow.shown` | whether it is on the screen |
| `MemberRow.value_text` | the value as a field shows it |
| `EditModel.toggle_fold` | fold one container, or open it |
| `EditModel.toggle_fold_all` | fold every one of them, or open every one |
| `can_fold` | whether the configuration has anything to fold |
| `fold_hides` | what the next press of the fold action will do |
| `row_fold_text` | what says that one container is folded |
| `path_text`, `text_path` | one path as text, and back |
| `ActionSettings.fold` | the keys of the fold action |
| `RESERVED_KEYS` | the combinations no default of the editor takes |

**What its review found.** The fold action had `ctrl+f` as its second key,
which is find everywhere. It is `ctrl+t` now — the tree is what the action is
about — and `RESERVED_KEYS` records that `ctrl+f` and `f3` are kept free for
the search this editor is likely to be asked for, with a test that no default
takes one of them. `ctrl+shift+f` was considered and rejected for the reason
design section 9.1 already gives about `save_as`: a terminal that has nowhere
to put the shift delivers it as `ctrl+f`, so the fold key would run the search.
Design section 9.7.

**What building it found.**

- **A validation pass can change how many rows there are.** A
  `ListOrderingValidator` that removes duplicates removes a row, so the model
  builds its rows again after every pass and both backends build their widgets
  again when the paths differ. Design section 4.8. This is also the machinery
  that step 14 needs, so it was built here rather than worked around.
- **A parse converter reaches a dictionary key at any depth.**
  `Config._json_parse_obj_hook` runs over every decoded object, so a key named
  after a converted member is converted too, and the editor answers the same
  way: the value of a dictionary key can have a converter and a list element
  never can.
- **A dictionary is shown in the sorted order the file has**, because a
  dictionary key has no declaration order to be read from. Design section 4.1.
- **Both backend modules had to be split**, at 1000 lines each: `tk_look` and
  `textual_look` now hold the sizes, the colours and the widget helpers, and
  `bind_key` moved to `key_names`. `EditorWidgets` builds its rows before the
  part that does not scroll is packed, so that the widgets are still created in
  the order they are read in.
- **The Tk stub had drifted.** A widget inside a frame that is out of the
  layout is still packed itself, so the stubbed tests and `real_texts` both
  reported a folded value as shown until they were taught to stop at a
  container that is not on the window.

#### Step 11 — Nested `Config` objects

`nested_configs()` becomes the first-authority source it is in design
section 4.1. A nested config is a first-class node with its own type,
docstring and validity state, and it segments the tree. A new example
`e09_nested_config.py`, modelled on `e33_nested_configs.py`. Open question
to settle when this step starts: `ConfigNestingKind` also has
`OPTIONAL_MEMBER`, which design section 11 neither includes nor excludes.
Decide it explicitly rather than by accident.

Step 10 left this step less to do than the plan expected. *Where* a nested
object is is already asked as a selector over paths, so a `MEMBER`, a
`LIST_ELEMENT` and a `DICT_VALUE` nesting are already found the same way and
each object is already one node with a row of its own. What is left is what
such a node *is*: its class and docstring, its own members as rows below it,
and the ownership that comes with them — `parse_converters()`,
`_omit_none_from_json()` and the descriptions of a subtree belong to the class
that owns it, and the root's are what the editor uses today because nothing
inside a nested object is a row yet.

#### Step 12 — Folding and subtree validation

Fold state in the model, and folding a nested config validates that subtree
by constructing its `config_type` from that subtree's JSON. Show
*subtree-valid* and *config-valid* as the two distinct states they are; a
subtree can be valid while the root is not, and both should be shown.
`e09_nested_config.py` gains the badges. Risk: a `WholeConfigValidator` on a
parent relates members across a nesting boundary, so a green subtree badge
must never be allowed to read as "the file can be saved".

### Milestone 4 — configs in containers

#### Step 13 — `LIST_ELEMENT` and `DICT_VALUE` nesting

Repeated nested configs, and the `'['` step in description paths meaning
"every list element or every dictionary value at this point", which is what
stops the application repeating itself per index or per key. A new example
`e10_config_containers.py`, modelled on `e34_list_nested_configs.py` and
`e35_dict_nested_configs.py`.

#### Step 14 — Adding and removing elements

Add and remove elements of uniform lists and dicts, with the template taken
from the default instance or from the nesting declaration. Where a
container's default is empty and it has no nesting declaration, there is no
template and none can be invented: the UI says so and offers reorder and
remove but not extend. `DICT_VALUE_BY_KEY` members and dicts listed in
`_unchecked_dicts` are out of v1 scope and must be reported as such rather
than half-supported. A new example `e11_add_remove.py` demonstrates all
three cases side by side, including the two that are refused.

### Milestone 5 — release readiness

#### Step 15 — Confirmation before dropping edits

If Cancel/Close is asked for in an editor with unsaved changes it should ask
for confirmation before discarding the edits.

#### Step 16 — Old/backup file when overwriting

If the editor is asked to write to a file name where the file exists, it
should create an old/backup file with the previous content (probably by
renaming the existing file to the old/backup file name). This logic only
applies if the file was not previously saved to (written) by the editor in
the current editing session (as we do not want to keep an extra backup file
for every time the user presses save). Design decision to take here: Should
editor also ask for confirmation before over-writing an existing file? Note:
This behaviour should probably be configurable in the Settings dataclass.

#### Step 17 — v1 polish

Rewrite the `readme_parts/` of all three packages against what was actually
built; regenerate the API documents in `doc/`; confirm that the Alpha
wording of design section 2.5 and the PyPI classifiers still say what they
should; verify that `additional_venv_packages` in
`custom_build_tools/custom_spec.py` is genuinely redundant now that the
packages declare their real dependencies, against the install step rather
than by assumption; check that `BuildSpec.identical_versions` still holds
across the three `pyproject.toml` files; and run the three-version sweep one
final time before release.

### After v1

#### Step 18 — Embedding in an application's own window

Designed in full in `doc/design.md` section 8.2. The design was recorded
before the code because two of its questions were cheaper to answer while
the backends had no users, not because the code is wanted early. Add
`TkEditorPanel` to the Tk package; split `EditorApp` into
`EditorPanel(Widget)`, `EditorScreen` and `EditorApp` in the Textual
package, moving the CSS to `DEFAULT_CSS`, the bindings to the panel
instance, the model title into a label and the palette entries to the
screen; export the new names from both packages; and answer the three
questions left open in section 8.2.7, of which the Tk key binding target is
the one with real design content. A new example shows one editor inside an
application's own window per backend, which is also what makes the step
observable.

`edit()` gains nothing in either package and no existing name changes
meaning. That is the property section 8.2.5 was written to protect, so
the step is not done until an application written against today's
packages still builds and behaves exactly as it did.

#### Step 19 — The rest of the program's command line

The options step 7B deliberately left out, less the one that step 9 brought
forward: `--extension` and `--enforce-extension` for an application whose
configuration files are not called `.json`, and `--key ACTION=COMBINATIONS`
for one whose users want other keys. `--descriptions NAME` was the
interesting one and is done: a review of step 9 asked why a program showed
no explanations under the members, and the answer was that what an
application says about its own members is the one thing an application can
tell the editor that the program could not pass on. Whether the two parsers
of the repository share their definitions was settled at step 7B rather than
here: `add_file_options` and `named_policy` are shared already, and each
option this step adds is a candidate for the same treatment. Consider if
adding a class derived from `config_as_json.Config` for storing the
`Settings` of the 7B programs instead of passing them as arguments. Using
such a configuration file may be a better idea than a very long command
line.

#### Step 20 — The program asks for what the command line left out

A wizard: the program opens with no location, no class name and no files,
and asks for them in the toolkit it was started in. What has been chosen,
what is still missing and whether the class could be loaded is state, and by
the lesson of step 6 about the explanation toggle it belongs in the core so
that the two backends cannot drift about it. Each backend then contributes a
dialog or a screen, and a file chooser, which is where the two toolkits
differ most and where neither has a headless test that is worth much. This
is a bigger step than the program it completes — roughly the whole of step
7B again per backend — and it is only worth building once the program has
users who would rather not type a module path. It is the reason step 7B puts
the loading and the reporting in the core: a wizard replaces the argument
parsing and nothing else. When we get here investigate if using
https://pypi.org/project/wizard-ui-bridge/ and
https://pypi.org/project/wizard-tk-bridge/ makes implementing the wizards
simpler.

Step 20 also adds version reporting using
https://pypi.org/project/versionreporter/ as a `--version` flag to all
3 programs (created at step 7B). Implement as a class `EcajVersionReporter`
derived from `VersionReporter` in `./edit` and classes derived from
`EcajVersionReporter` in `./edit_tk` and `./edit_textual` so that the
backends get the dependencies of `edit-cfg-json` without repeating
the list of dependencies.

## 4. Open questions recorded, not answered

These do not block step 1, and each is scheduled to be answered at the
step that needs it. They are listed here so they are not forgotten.

| Question | Answer needed by |
| --- | --- |
| ~~When does a field report that its text means no value at all, and is that on focus loss?~~ Answered at step 7: it does, on focus loss, through `EditModel.check_field`. See `doc/design.md` sections 4.2 and 6.5. | done |
| ~~Does `Config.write()` validate, making the editor's gate belt and braces?~~ | step 5 done |
| Is `ConfigNestingKind.OPTIONAL_MEMBER` in v1 scope? | step 11 |
| ~~Does the Textual headless driver in the pinned 8.2.8 behave as the design assumes?~~ | step 1 done |
| ~~Will the README test summary stop updating on a headless machine, per design section 10.2?~~ | step 1, as a known consequence |
| Which widget does the Tk backend bind its keys on when it shares a window? See `doc/design.md` section 8.2.7. | step 18 |
| Does the core name the mounting contract with a `Protocol` of its own? | step 18, or the first third-party backend that mounts |
| Does `Settings` say whether an embedded editor's bindings are priority bindings? | step 18 |
