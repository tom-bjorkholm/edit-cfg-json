# Delivering the remaining scope in small steps

## Where everything is

Steps 1 to 28 are implemented and committed, step 23 with the corrections its
review asked for, and step 29 is implemented and awaiting its review. Steps 1 to 9 are written up in
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
- [Step 29](#step-29---pull-down-selection-of-enum-and-bool-values) — a member
  whose values the editor knows the whole of offered as a pull-down of them,
  one switch for all of them, and the first value it takes given to a text
  that means none.

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

## 1. How this plan is meant to be used

This document turns the scope recorded in
[`doc/detailed_design.md`](../doc/detailed_design.md) into an ordered list of small,
individually reviewable and individually committable steps. It is a delivery
plan, not a design document: where it mentions a design decision,
`doc/detailed_design.md` remains the authority and this file only says *when* that
decision gets built.

- One step is one branch-less unit of work on `master`: implement, verify,
  ask for review, commit. The next step does not start until the previous
  one is committed.
- Every step changes what an example program does. If a step cannot be
  observed from `examples/src/example/` with `--ui tk` or `--ui textual`,
  it is the wrong step boundary and should be merged into a neighbour or
  split differently.
- Every step touches all three packages where the capability is
  user-visible, so `edit_cfg_json`, `edit_cfg_json_tk` and
  `edit_cfg_json_textual` never drift apart by more than one review.
- Steps 1 to 28 are built, and each is written up in
  [steps_001-009_done.md](steps_001-009_done.md), in
  [steps_010-021_done.md](steps_010-021_done.md) or in
  [steps_022-028_done.md](steps_022-028_done.md) as what it decided, what it
  found while building it and what came of its review. Steps 29 onwards are
  named steps with their observable outcome and their main risks; they are
  detailed just before they are started, when the core API is real rather than
  imagined.

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
| M3 Structure and folding | 10 to 12 | Lists, dicts, nested `Config` objects, folding with per-subtree badges | done |
| M4 Configs in containers | 13 to 14 | `LIST_ELEMENT` and `DICT_VALUE` nesting, adding and removing elements | done |
| M5 Release readiness | 15 to 17 | Closing keeps what was not saved, files are not overwritten unannounced, and first release is documented, classified and published | done |
| First release 0.0.2 | release on PyPI.org | [https://pypi.org/project/edit-cfg-json/](https://pypi.org/project/edit-cfg-json/) | done |
| Second release 0.0.4 | 18 to 21 | Release 0.0.4 | done |
| Third release 0.1.0 | 22 to 28 | Release 0.1.0 | done |
| Fourth release 0.2.0 | none | Release 0.2.0, the paths that `config-as-json` 1.7 reports | done |
| Fifth release | 29 onwards | in progress | step 29 implemented, awaiting review |

## 3. Steps 29 onwards, as named steps

Each of these is detailed just before it is started. What is fixed now is
the order, the observable outcome and the main risk.

### Step 29 - Pull-down selection of enum and bool values

Status: **Implemented, committed.**

When the type of an attribute have a well defined set of possible
values that we know from type discovered by introspection we shall
offer the user to select the value instead of typing the value.
This is the case for bool, and for enums.

The end user shall be able to switch between typing in a text field
and pull-down selection of values for enums, in a way similar to how
the end user shows and hides the explanations. The initial state
(text field or pull-down) shall be defined in Settings, with the
default value in settings as pull-down.

**Observable outcome.** `e02_enum_config.py --ui tk` and `--ui textual` open
with both enum members as a pull-down of `MECHANICAL`, `ELECTRICAL`,
`ELECTRONIC` where they were fields; `F4`, or the new `Choose values` tick-box
in the window, turns them back into fields; and `F4` again with `ELECT` in a
field replaces it with `MECHANICAL` and says so in a dialog, where `MECH` is
completed silently because it is the beginning of exactly one member name of
*that* enum. `--type-values` opens the same example the other way
round. `e12_backup_files.py --ui tk` shows the same thing for a member holding
true or false, and `e17_settings_config.py --ui tk -i ../../data/e17_tool.json`
shows the four true-or-false settings of the editor as pull-downs, one of
which is the setting that says which way the editor opens.

**What it decided.** Six things.

- **The values are read from what the row already carries**, so
  `MemberRow.choices` is a property and not something the buffer computes:
  `is_bool` for the two words of step 22, and `descriptions.enum_names` for
  the names of an enum, which is the reading `enum_text` already made for the
  line that lists them below the row. One reading, so the list offered and the
  list written cannot come to disagree.
- **One answer for the whole editor, switched by the user**, which is the
  explain toggle of section 4.4 applied to a second question, with the
  tick-box of one backend and the renamed action of the other. What the
  application decides is only which way the editor *opens*, as
  `Settings.choose_values`, and that answer is read until the user gives one
  of their own — a third thing a settings callable can change, beside the keys
  read once and the file names read at every save.
- **A pull-down offers the values its member takes and nothing else, and holds
  one of them at every moment.** There is no unselected state, no blank line
  among the values and no way for the user to reach either: a member holding an
  enum takes the members of that enum, one holding true or false takes those
  two words, and offering anything else would be offering to write what the
  class cannot read back. Tk's menu lists the values alone, and Textual's
  control is declared `allow_blank=False`, which takes its unselected state
  away and with it the blank line it would otherwise list.
- **Switching to a pull-down is a third moment at which a member's text is
  answered for**, beside a field losing the focus and a validation pass,
  because typing is what the field is for and the pull-down has to hold a
  value its member takes. `matched_choice` runs the converter the class
  declared: the case is ignored and a beginning that only one member of *that*
  enum has is that member, which is a fact about the enum the application
  declared and about no other. Such a text is completed with nothing said about
  it; a text meaning none of them, or more than one, leaves the member holding
  the first value it takes, and the user is told in a dialog because it is the
  one change of the buffer they did not make.
- **The rule holds by construction and not by tolerant widgets.** Each backend
  asks `settle_choices()` where it builds the widgets of its rows, which is
  what makes every pull-down be *made* holding one of its own values. It does
  nothing while the values are typed and nothing a second time, so it is a
  question rather than a change: what it guards against is an application that
  wrote into the model between building it and showing it, which
  `EditModel.set_text` allows and the examples do for `--set`.
- **The Tk pull-down and the Tk field share one variable.** A menu entry writes
  the value that was picked into the variable it is given, so the callback that
  writes the model is the one the field already had and picking a value is the
  same edit as typing one. It is built from the `Menubutton` and `Menu` that
  `tkinter.OptionMenu` is, which is plain Tk rather than `ttk` and keeps every
  widget of this backend configurable with `background` and `foreground` — what
  step 31 will need.

**Core.** `leaf_value` gained `BOOL_NAMES` beside `BOOL_CHOICES`,
`descriptions` gained `enum_names`, `rows` gained `MemberRow.choices`,
`converting` gained `matched_choice` and the words of a replaced text, `buffer`
gained `choose_values`, `edit_model` gained the state, the switch and
`settle_choices`, and `model_text` gained `row_chooses`. `Settings` gained
`choose_values` and `ActionSettings` gained `choose`, which `SettingsConfig`
mirrors and `ADDED_ACTIONS` and the new `ADDED_SETTINGS` make an older settings
file readable past.

The public names it settled:

| Name | Kind |
| --- | --- |
| `Settings.choose_values` | which way the editor opens |
| `ActionSettings.choose` | keys that switch, `('f4',)` |
| `SettingsConfig.choose_values` | the same setting, written in a file |
| `ADDED_SETTINGS` | members no released version wrote into a file |
| `MemberRow.choices` | the values this node takes |
| `EditModel.choices_shown` | whether they are chosen rather than typed |
| `EditModel.toggle_choices` | the switch |
| `EditModel.settle_choices` | give every such member a value it takes |
| `row_chooses` | whether this node is chosen from rather than typed into |

**What building it found.**

- **The review found the whole of this step's worst mistake in one place.**
  The first version left Textual's control at its default `allow_blank=True`
  and used its unselected state for a member whose text was none of its values,
  which put a blank line into the list of every enum and let the user pick it.
  It was built to tolerate a state the editor should simply not have, and the
  one path that produced that state — an application writing into the model
  before the editor is shown — is closed by settling where the widgets are
  built. `allow_blank=False` now takes the state and the blank line away
  together, and `Select.NULL` appears nowhere in this package.
- **`tkinter.OptionMenu` cannot be given a Tk name before Python 3.14.** Its
  `__init__` passes only its own options to the widget, and the `name` keyword
  was added to those in 3.14 alone, so a 3.12 build failed with *unknown option
  -name*. The pull-down is built from the `Menubutton` and the `Menu` that
  class is, which is ten lines, keeps the widget name that tells it from its
  field, and works on all three supported versions.
- **Two modules had to be split**, both of which were one step from too long
  before this one: `tk_editor` gave up the two ways of editing one value to a
  new `tk_values`, and `textual_panel` gave up the widgets of one member row
  and what they show to a new `textual_member`. The Tk test helpers went the
  same way, with the stand-ins moving to a `stubs` module of their own.
  `textual_panel` is still within a hundred lines of the limit, and the next
  step that touches it will have to split the actions of the panel from the
  widgets of it.
- **`rows_shape` does not track the values a node takes**, and one exotic case
  can therefore leave a row without the pull-down it has become entitled to: a
  member with no annotation the editor can read, whose value changes kind
  across a save, in a session that stays open. Nothing wrong is shown and no
  wrong value can be written — the row simply keeps its field until the editor
  is opened again — so the public shape of `rows_shape` was left as it is.
- **`e17_tool.json` had to gain the new action and the new setting.** A
  settings block inside another configuration is read whole, so the data file
  of that example is a current-format file by definition, and the old-format
  file beside it now differs by three actions and one member rather than by
  two actions.

### Step 30 - The launcher the name `edit-cfg-json` is kept for

Status: **Not started.**

Section 8.1 of the design is headed "planned, not implemented": an
`edit_cfg_json.ui` entry-point group would let backends register themselves for
discovery, which is what `--ui auto` needs. Section 8.3 keeps the command name
`edit-cfg-json` free for the launcher that picks the editor the machine can
run, and step 16B freed that name and said the logic for choosing "may be added
in a later step". This is that step: both editor packages register themselves,
the core installs the launcher it has never installed a program for, and a
machine with no display or without `textual` gets the editor it can actually
run, with a refusal and an exit code of its own where it can run none.

When the backends register (or are discovered) they each provide a named tuple
or frozen dataclass describing them. This named tuple has members for:

- priority: an integer that is 0 or greater. DumpEditor has priority 0,
  textual priority 5 and Tk priority 10.
- the string that specifies the value this editor uses for the argument of
  the `--ui` switch.
- a callable `Callable[[], bool]` that determines if this editor can run
  in this context. (This includes checking if dependencies are installed,
  if a stdout/stdin are attched to a terminal, ...)
- a callable to start the editor.

`edit-cfg-json` takes an optional command line switch `--ui` with possible
arguments determined by the registered/discovered backends. (Member from the
named tuple they provide at registration/discovery).
If the switch `--ui` is missing the backends are probed if they can run in
order, starting with the highest priority. When the first backend answers
that it can run, it is started and no other backend is probed.
However, backends whith priority 0 are never probed and are never started
unless explictly requested as the argument of the `--ui` command line switch.

Other possible future editors (like a Qt editor) can register or be discovered
just as the backends provided by this repo. The programmer of a backend
determines which priority to report for that backend.

The Settings and configuration file gains a `dict[str, int]` that can be
used to override the priorities the backend report at registration/discovery.
It is a dict from `--ui` argument string to priority.
The default Settings has an empty dict for this priority override.

### Step 31 - Selectable dark mode

Up until now the `edit-cfg-json-tk` has only had a hard coded light mode.
Add to the Settings an enum value that selects between light mode and
dark mode for the Tk UI.

Add also 2 configuration sets as sub-configurations under Settings
that specify the individual colors of all UI parts as optional Tk hex colors.
Each color that is specified as None, shall use the Tk default color for
kind of UI element.

There shall be `config_as_json.Config` derived configuration for selecting
between light and dark mode and for selecting color of individual UI element
types. Use `Optional[config_as_json.HexadecimalNumber]` for the individaul
UI element type colors.

Evaluate to which extent the Tk UI mode settings and colors can also
be applied to the textual UI.

### Step 32 - Raw JSON for a subtree the editor cannot show

Step 25's early idea included a raw JSON editing surface for a sub-object whose
class nothing says anything about, and step 25 found that the case it was
proposed for does not need it: the class of a nested object is named by its
declaration, and one the editor cannot construct says so rather than offering a
control that refuses every press. Section 11 of the design records that it is
kept as a step rather than rejected, because what would make it worth having is
a different question from the one it was proposed for.

That question is an editing surface for a *subtree*, which nothing in the
editor has: a text area holding the JSON of one node, validated by the class on
the next pass, which would also serve pasting a whole section from somewhere
else and repairing a shape no row can express. The risks are the two that
belong to any second way of editing the same thing — which of the two wins
while both are open, and what a validation pass does to text the user is half
way through typing — and they are the reason this is late rather than cheap.

### Step 33 — The program asks for what the command line left out

A wizard: the program opens with no location, no class name and no files,
and asks for them in the toolkit it was started in. What has been chosen,
what is still missing and whether the class could be loaded is state, and by
the lesson of step 6 about the explanation toggle it belongs in the core so
that the two backends cannot drift about it. Each backend then contributes a
dialog or a screen, and a file chooser, which is where the two toolkits
differ most and where neither has a headless test that is worth much.

When we get here investigate if using
[https://pypi.org/project/wizard-ui-bridge/](https://pypi.org/project/wizard-ui-bridge/)
and
[https://pypi.org/project/wizard-tk-bridge/](https://pypi.org/project/wizard-tk-bridge/)
makes implementing the wizards simpler.

Alternatively, consider if we should use the menubar and menu items like
File - Open. (Using the menubar may feel very natural in the Tk version.)

## 4. Relative effort of the steps still to build

The relative effort of the remaining steps is listed in effort order.

| Step | Effort | What the number is mostly |
| --- | --- | --- |
| 30 The launcher | 4 | Little logic, spread over all three packages: an entry-point group, a script the core has never installed, discovery, and what a machine that can run neither editor is told. |
| 32 Raw JSON for a subtree | 8 | An editing surface the editor does not have at all yet, in both backends, and two rules about a second way of editing one thing. |
| 33 The wizard | 10 | Two toolkits' dialogs and file choosers, two bridge libraries to weigh against the menubar alternative, and no headless test worth much. |

## 5. Open questions recorded, not answered

These do not block current development, and each is scheduled to be answered at the
step that needs it. They are listed here so they are not forgotten.

| Question      | Answer needed by |
| ------------- | ---------------- |
| (nothing yet) |                  |
