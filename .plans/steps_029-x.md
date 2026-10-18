# Delivering the remaining scope in small steps

## Where everything is

Steps 1 to 30 and 31A to 31C are implemented and committed, step 23 with the
corrections its review asked for. Steps 1 to 9 are written up in
[steps_001-009_done.md](steps_001-009_done.md), steps 10 to 21 in
[steps_010-021_done.md](steps_010-021_done.md) and steps 22 to 28 in
[steps_022-028_done.md](steps_022-028_done.md). Steps 29 to 30 and the steps
still to build are in this file. Where any of the four files mentions a
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
- [Step 29B](#step-29b---the-value-a-mistyped-name-is-given) — the first value
  it takes kept as the last resort it should have been, with the value a
  mistyped or unfinished name most likely meant put in front of it.
- [Step 30](#step-30---the-launcher-the-name-edit-cfg-json-is-kept-for) — each
  user interface registering what it is and whether it can run here, the
  launcher the name was kept for installed at last, and the same choice offered
  to a command that has no user interface of its own.
- [Step 31A](#step-31a---every-row-says-its-type) — every row saying the type
  it holds in the words of a Python type hint, in a column between its name
  and its value, and the prose about the kind of a value gone from below it.
- [Step 31B](#step-31b---choosing-between-the-types-of-a-plain-value) — the
  type of a plain value chosen in that column, `None` among the types instead
  of the add and remove controls, and a type the class would refuse left out.
- [Step 31C](#step-31c---choosing-between-lists-and-dicts) — a list and a dict
  chosen in the same column, the rows below a row made again by a choice, and
  the dict-shape check of the class asked of every row before a type is
  offered.

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
- Steps 1 to 30 and 31A to 31C are built. Steps 1 to 28 are written up in
  [steps_001-009_done.md](steps_001-009_done.md), in
  [steps_010-021_done.md](steps_010-021_done.md) or in
  [steps_022-028_done.md](steps_022-028_done.md), and steps 29 to 30 in
  section 3 below, as what each decided, what it found while building it and
  what came of its review. Steps 31 onwards are named steps with their
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
| M3 Structure and folding | 10 to 12 | Lists, dicts, nested `Config` objects, folding with per-subtree badges | done |
| M4 Configs in containers | 13 to 14 | `LIST_ELEMENT` and `DICT_VALUE` nesting, adding and removing elements | done |
| M5 Release readiness | 15 to 17 | Closing keeps what was not saved, files are not overwritten unannounced, and first release is documented, classified and published | done |
| First release 0.0.2 | release on PyPI.org | [https://pypi.org/project/edit-cfg-json/](https://pypi.org/project/edit-cfg-json/) | done |
| Second release 0.0.4 | 18 to 21 | Release 0.0.4 | done |
| Third release 0.1.0 | 22 to 28 | Release 0.1.0 | done |
| Fourth release 0.2.0 | none | Release 0.2.0, the paths that `config-as-json` 1.7 reports | done |
| Fifth release 0.3.0 | 29 and 29B | Release 0.3.0, a member whose values the editor knows offered to be chosen from | done |
| Sixth release 0.4.0 | corrections and 30 | Release 0.4.0, an editor launcher | done |

## 3. Steps 29 onwards, as named steps

Steps 29 to 30 are built and written up here. Step 31 is detailed already and
split into sub-steps, because the decisions it rests on were settled in a
design discussion before it was planned. Each of the rest is detailed just
before it is started; what is fixed now is the order, the observable outcome
and the main risk.

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
  step 32 will need.

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

### Step 29B - The value a mistyped name is given

Status: **Implemented, committed.**

Step 29 left a text that means none of a member's values holding the **first
value it takes**, which is right as a last resort and blunt as the only rule: a
user who had typed most of a name got the name at the top of the list. This
step puts three questions in front of that one and changes nothing else about
the pull-downs. The two assumptions behind them are that the name was typed as
it was meant, and, failing that, that one character came out wrong.

**Observable outcome.** `e02_enum_config.py --ui tk` with `ELECT` in the
`needed` field and `F4` pressed now holds `ELECTRICAL` where it held
`MECHANICAL`, and the same dialog says so: `ELECT` is the beginning of two of
the three names and the first of those two is taken. `ELEKTRONIC` becomes
`ELECTRONIC`, which is one character changed away from exactly one name.
`ELEKT` becomes `ELECTRICAL`, a beginning of two names once one character is
allowed to be wrong. A text near none of them, and an empty field, still leave
`MECHANICAL`. `e12_backup_files.py --ui tk` shows the same for a member holding
true or false, where `falze` becomes `false` where it became `true`.

**What it decided.** Four things.

- **What a refused text most likely meant is a different question from what a
  name means**, so it is a function of its own. `matched_choice` runs the
  converter the class declared and answers what the class says the text is;
  `nearest_choice` runs no converter and asks the class nothing, because it is
  the editor reading a text the class has already refused. Keeping them apart
  is what keeps a silent change meaning *your text really does name this
  value*: everything the second one answers is announced, the near misses
  among them.
- **One character is one character changed, added or dropped**, which are the
  three ways one is mistyped, and never two of them at once. A transposition is
  two changes, so the rule asked first never answers one — but the rules about
  beginnings answer some of them anyway, because dropping one of the two
  swapped characters can leave a beginning of the name. `fales` reaches `false`
  that way and `flase` does not reach it at all, which is the one place where
  what the rules correct is hard to predict from the outside. Loosening them
  until it was predictable would make every other answer less so, and the field
  is still there for a name the editor guessed wrong.
- **A whole name is worth more than a beginning**, so the changed character is
  asked about before the beginnings are. `LO` among `LOWEST`, `LOW` and `HIGH`
  is therefore `LOW` — one character short of that whole name — and not
  `LOWEST`, which it is equally the beginning of. Two values equally near the
  text answer nothing and the question moves on, so nothing is ever picked
  between two candidates by anything but the order the class declares them in.
- **Where a rule narrows the values down without naming one, the first of what
  it narrowed to is taken**, which is the rule of step 29 applied to a subset
  rather than to all of them. That is the whole of `MEC` meaning `MECHANIC`
  where the values are `ELECTRIC`, `MECHANIC` and `MECHATRONIC`.

**Core.** `converting` gained `nearest_choice` and the three small comparisons
it asks, and `buffer.choose_values` asks it where it used `choices[0]`. No
backend changed at all and no public name of any of them did, which is what
says this is a rule the core owns: the two backend tests that had to change did
so only in the value they expect from typing `ELECT`.

| Name | Kind |
| --- | --- |
| `nearest_choice` | the value a text the class refuses most likely meant |
| `EditorWidgets.least_size` | the size below which something of it is hidden |

**What building it found.**

- **The four rules are one measure asked four ways.** How many characters of
  the typed text differ from the beginning of a name decides all of them, and
  that measure is what the two texts begin with in common plus what the rest of
  them ends with in common — the same comparison for a character changed, one
  added and one dropped, with no alignment to decide and no table to fill in.
  The first draft had a rule per case and was longer than the docstring that
  explains it.
- **A one-character text makes the third rule match every value**, because
  every name begins with a character that one change reaches. It is harmless —
  the answer is then the first value, which is what the fourth rule says
  anyway — but it is worth knowing that the third rule stops narrowing anything
  down at that length.
- **The empty field is answered by the second rule and not by the last one.**
  It is the beginning of every name, so it narrows nothing down and the first
  value is taken, which is exactly what step 29 did with it and what its own
  sentence in `CLEARED_FORM` still says.

**What the review found.** All three tests that
`./run_focus_sensitive_tests.py` runs were failing, and none of the three was
about this step: they are the tests no build runs, so step 29 broke them and
nothing said so until they were run by hand.

- **Two were the step 29 widgets, said twice.** `SETTLED_TICKS` did not know
  about the `Choose values` tick-box, and `test_real_leaving_field` asked a
  field to lose the focus in an editor that now opens with pull-downs, where
  that field exists but is not on the screen and no focus reaches it. It opens
  with the values typed instead, which is what a field losing the focus needs.
- **The third was a real one, and the fix is a rule the design was missing.**
  The `Choose values` tick-box made the button row ask for 555 pixels where it
  had asked for about 430, and the test squeezed the window to 500 and required
  that nothing was cut off — so `Close` went off the edge. Nothing in this
  backend scrolls sideways and a member row cannot wrap, so there is a width
  below which the editor loses text, and no window was ever stopped from
  reaching it. `EditorWidgets.least_size` answers what that size is, `TkEditor`
  sets it as the minimum of the window it owns, and the test now shrinks to the
  size the editor says it needs rather than to a width of its own invention —
  which is what let one more control break it. Section 4.6 of the design has
  the rule as its fourth constraint.
- **A stale `./venv` is what makes these tests crash rather than fail.** They
  import the installed packages, so running them after editing the source and
  before `./run_build.py` aborted the first test on a name that existed only in
  the source, and the Tk window it had already built was destroyed under it —
  which segfaulted the next test when it reached `mainloop()`. Build first, and
  where one of the three does fail, run them one at a time so that an aborted
  test cannot take the next one down with it.

### Step 30 - The launcher the name `edit-cfg-json` is kept for

Status: **Implemented, committed.**

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

`edit-cfg-json` library gains 2 additional exported functions to be used
by command line programs with no GUI of their own that wants to offer
editing of their configuration:

- One is similar to the `edit` function of the backends,
  but take an `ui: Optional[str]`. It selects the backend just like
  what is described above for the `edit-cfg-json` command.
- One returns a list of registered/detected backend strings for
  backends that can run in this context. The return value is intended
  as the allowed values of the `--ui` switch for the configuration
  editor of the command line program.

#### What it decided

The named tuple is `UiBackend` in `edit_cfg_json.ui_backend`, registered in the
`edit_cfg_json.ui` entry point group, and it has **six** members rather than
the four above. The two added are `interactive` and `home_settings`, and the
reason is that the launcher hands its whole session to the same `run_cli` the
other three programs use, which is told both of them: the first decides
`--save` and `--unfold` and what the exit code answers with, and the second is
the settings file of the home folder. Both are facts about the user interface
and not about the program that opened it, so a session the launcher opens in
the window editor reads `~/.edit-cfg-json-tk.cfg` exactly as
`edit-cfg-json-tk` does. The three programs of section 8.3 now read their own
two facts from their own registration as well, so there is one place that says
them.

The "callable to start the editor" is a `Callable[[], EditorBackend]` and not a
call that runs a session. Every way of showing the editor takes a backend —
`edit`, `run_cli`, and an application that built the model itself — so a
factory fits all of them, and it is a factory rather than a backend so that
choosing between the installed user interfaces does not build every one of
them.

**Asking Tk whether it can run happens in a child process**, which is the one
decision here that was made against the obvious implementation. A `Tk()` that
the asking process built and destroyed would be the first of two in the process
that goes on to open the editor, and step 29's own review recorded a Tk
destroyed under an aborted test segfaulting the next one. The child runs
`import tkinter; tkinter.Tk().destroy()` and answers with its exit code, the
answer is cached for the run, and no test of this repository builds a Tk in the
pytest process in order to ask. It costs one Python start-up per run of the
launcher. Textual's answer is `isatty` on both ends of the process and is not
cached, because it costs nothing and can change within one run.

**`--ui` accepts what can run here and nothing else**, so a name that cannot
run is refused by `argparse` beside the names that would have worked. That
costs asking every registration before the command line is parsed. The library
functions still refuse a named user interface about itself —
`edit_in_ui(ui_name='tk')` on a machine with no display says so rather than
opening the terminal editor — because a caller that named one wants that one.

**A machine that can open no editor is refused after the command line is read.**
`--help` is what says that `--ui` exists and `--version` is what a problem
report is written from, and the person who has just been told they have no
editor is the person who most needs both, so `run_cli` took an
`Optional[EditorBackend]` and answers `ExitCode.NO_EDITOR` once those two have
had their chance.

**The launcher reads the settings twice.** The priorities have to be known
before the editor is chosen, and the settings file of the home folder cannot be
known until it has been: the file belongs to the editor. So the launcher makes
the lookup without any program's own file, silently, and the session makes it
again with the file of the editor that was chosen. Silently, because a file
that cannot be read is refused by the session in the same words, and one fault
deserves one message.

#### What it found while building it

- **The priority override cannot be an ordinary dict member of
  `SettingsConfig`.** `config_as_json` matches a dict member's keys against the
  ones the class declares, whatever policy the parse was given, and the class
  declares none of them: a `--ui` name belongs to whatever packages happen to
  be installed, and the same settings file is read on machines that have
  different ones. `_unchecked_dicts` is what takes that check off the member,
  which is what steps 27 and 28 were about for an application's own classes and
  is now used by a class of this library. The shape of the value is still
  checked, so text where a table belongs is still refused, with a `KeyError`
  from `config_as_json` rather than the `InvalidConfiguration` of a validator —
  which is why it is a test of its own rather than another row of the table of
  wrong types.
- **It is a change of this library's own file format**, so `ui_priorities`
  joined `ADDED_SETTINGS`, and the helper that writes "a settings file as an
  earlier release wrote one" in the tests now takes out the added members as
  well as the added actions. That is what made the existing rules for an older
  file exercised by the case they were written for.
- **`ui` is not a name pylint accepts**, since it is two characters and the
  default pattern asks for three. So the member is `ui_name`, and so is the
  keyword of `edit_in_ui` and of `chosen_ui`. It reads better beside
  `available_uis` anyway.
- **`dataclasses` refuses a mutable default**, so the new attribute of
  `Settings` is the one with a `default_factory`. It is worth a test: two
  applications that say nothing about the priorities must not share the dict
  that says it.
- **The example's own `-i` and `-o` tripped R0801 against the module the `a`
  series shares.** The answer was to factor the two options out into
  `add_editor_files` there, which a01 and a02 already reached through
  `editor_files`, and it left a03's parser showing only the option that is its
  subject. The shared helper is deliberately not `edit_cfg_json.add_file_options`:
  that one adds `--policy` too, which this series does not have.
- **Nothing in the launcher can be tested against the real registrations.**
  What they answer depends on the machine, so every test of choosing replaces
  discovery with user interfaces made up for the test, and what the two real
  ones report is tested where each of them lives. The one test that lets the Tk
  child process really run asserts only that an answer came back.

### Step 31 - The type of every row, and choosing between the types allowed

Status: **Split into sub-steps 31A to 31E. 31A to 31C implemented, the
rest planned.**

Two complaints from users, and one answer to both.

- **The type of a value is not said in the words users already know.** Many
  users program in Python, Swift or C++, and they want every row labelled with
  the type it holds in the vocabulary of Python type hints — `int`,
  `list[str]`, `Colors` — and not with *A whole number.* below it.
- **A member that allows two types offers one of them.** An application
  declares `self.jira_column_map: dict[str, list[str] | list[list[str]]]`, and
  a new key of that dict is given a copy of the first entry it holds, which is
  a `list[str]`. Nothing lets the user make it a `list[list[str]]` instead.
  The cause is in `member_types._optional_type`: a union of more than one type
  beside `None` is read as *nothing this editor can use*, so the editor never
  knew there were two.

**The answer is that every row has a set of allowed types**, read from the
declaration: the alternatives of a union, a plain type being a union of one,
and `Optional[X]` being the union of `X` and `None` rather than a state of its
own. The set is shown on the row as a pull-down, and choosing another of its
types is how the user changes what the row holds.

#### What was decided before it was planned

- **A column after the name, always shown.** The pull-down sits between the
  name and the value, which reads as Python's `name: type = value`. The column
  is one width for the whole editor, that of the longest type text up to a
  limit (which rows count is an open question of section 4); a longer text is
  cut with `…`, and then the whole type is said on the explanation line of
  that row. No key, no tick-box and no setting hides it, so `Settings` and
  `SettingsConfig` do not change and no rule for an older settings file is
  needed (design section 9.10).
- **One type is still a pull-down, inactive.** A row whose set has one member
  shows it in the same control, so every row says its type in the same place,
  and nothing can be chosen there.
- **The spelling is Python's, normalized from the resolved hint** and not
  copied from the source text, so a declaration read from source and one read
  with `typing.get_type_hints` are spelled alike. `Optional[int]` and
  `Union[int, None]` are `int | None`, `List[str]` is `list[str]`, a container
  of a union is `dict[str, list[str] | list[list[str]]]`, and an enum or a
  configuration class is its unqualified name. Another class of the
  application's, such as `Path` with a parse converter, is spelled by its own
  name, and what kind of JSON value it holds is still read from the value. The
  alternatives are offered in the order the declaration writes them.
- **`Literal` is a set of values like an enum.** A `Literal` whose values are
  all text, all whole numbers or all booleans is offered as a pull-down of
  those values. A text that means none of them is read by the rules of an enum
  name and of the two words of a boolean — the case ignored, a beginning only
  one of them has completed — and is refused at the member otherwise, in the
  words `yes is not one of: true, false` uses. That makes it the second refusal
  of a leaf that the editor makes itself (design section 4.2). A `Literal` of
  mixed kinds, `tuple`, `set`, `Any` and every other generic are *nothing
  usable*, the rule below.
- **A member whose declaration says nothing usable shows the inferred type,
  inactive.** That is a member with no annotation, one whose annotation will
  not resolve, and one of the kinds just listed. The pull-down shows the kind
  its value has, which is what the field already reads its text by, and the
  explanation line says that it was taken from the value because nothing was
  declared. Principle 4 of design section 3 is unchanged.
- **`None` replaces the two controls of a member that may hold nothing.** Such
  a member has `None` among its types, and choosing it is what *remove* was;
  choosing another type while it holds nothing is what *add* was. That holds
  for a plain value, for an `OPTIONAL_MEMBER` configuration object and for a
  key that `DICT_VALUE_BY_KEY` names, so all three are `StageConfig | None` or
  `str | None` in the same control. The element controls of design section 4.9
  stay for what they are really about: adding an element of a list or an entry
  of a dict, taking one out, and moving one.
- **Switching keeps what still fits.** A plain value keeps its text where that
  text means a value of the new type, so `'5'` becomes `5` when `str` is
  changed to `int`. Everything else — a value whose text does not fit, and
  every list, dict, object and `None` on either side of the switch — is given
  the empty value of the new type: `''`, `0`, `[]`, a new object of the class,
  or nothing. Nothing is remembered per type.
- **A type the class would refuse is not offered.** `config_as_json` refuses
  a dict where the object it parses into holds something else, and the
  reverse, `None` included, wherever its dict-shape check reaches (the facts
  below). Such a type is left out of the pull-down, and the explanation line
  names it and says why. It is left out rather than shown disabled because
  Textual's `Select` cannot disable one option, and the two backends must not
  differ.
- **The prose about the kind goes.** *Text.*, *A whole number.*, *A number.*,
  *True or false.*, *A list.*, *A dict.* and *It may hold no value.* are said
  by the pull-down now. What the pull-down cannot say stays on the explanation
  line: the summary and the names of an enum, that the class leaves the member
  out of the file while it holds nothing, why a type is not offered, the whole
  of a type the column cut, and where the type was inferred.
- **This reverses two sentences of the design**, and says so where they stand:
  *the user never changes what kind of value a leaf takes* in section 4.2, and
  the rejected alternative *the user changing the type metadata of a leaf* in
  section 11. What was rejected was the user choosing a kind; what is built is
  the user choosing among the kinds the application declared, and the worry
  the rejection recorded — a value the application then refuses — is what
  leaving out the refused types answers.

#### Facts checked against `config_as_json` before planning

Checked with a probe class against the `config_as_json` in `./venv`.

- **A list is never checked, so complaint 2 needs nothing from the library.**
  `{"k": [["x"]], "z": []}` parses into a member of `_unchecked_dicts`
  declared `dict[str, list[str] | list[list[str]]]` whose default holds
  `{"k": ["x"]}`.
- **Dict-ness is checked against the object, member by member.**
  `check_dict_parse(getattr(self, i), data[i], ...)` refuses `{"a": 1}` for a
  member that holds `3` (*Unexpected dictionary*) and `null` for a member that
  holds a dict (*Not dictionary*). The check is made *before*
  `_unchecked_dicts` is asked, so a member named there is checked too; it
  recurses only into the keys of a checked dict that the object holds.
- **The object it is checked against is the loaded one, for the whole
  session.** Validation parses into a copy of the model's own object, which is
  the one the load made, and nothing replaces it after a pass or a save. Which
  positions may change between a dict and something else is therefore fixed
  for a session, and is answered from that object rather than from the buffer.
- **A latent defect today:** an `Optional[dict[...]]` member that its class
  writes as `null` (not one `_omit_none_from_json()` names) and that was
  loaded holding a dict is offered *remove*, and the next validation pass is
  refused with *Not dictionary*. 31C removes it by the rule above rather than
  by a special case.

#### The names it is expected to settle

Named here so that the sub-steps can refer to them; each is settled by the
sub-step that builds it, as every step so far has done.

| Name | Kind | Sub-step |
| --- | --- | --- |
| `TypeOption` | one allowed type of a row: its text, its JSON kind, what is inside it, its class or its literal values | 31A |
| `MemberRow.types` | the types this row may hold, the refused ones left out | 31A |
| `MemberRow.chosen_type` | the one of them it holds now | 31A |
| `row_type_text` | the type as the column shows it, cut where it must be | 31A |
| `type_column_width` | how wide the column is for this model | 31A |
| `EditModel.set_type` | change the type of a row | 31B |
| `--set-type PATH=TYPE` | the examples' stand-in for a user choosing a type, as `--set` is for typing | 31B |
| `MemberRow.type_choosable`, `row_chooses_type`, `row_type_choices` | whether a row's type is chosen, and what its pull-down offers | 31B |

`LeafType` and `MemberRow.declared` are replaced by the first three, which is
why 31A is mostly a change of the core with one visible result.

#### Step 31A - Every row says its type

Status: **Implemented, committed.**

**What it does.** A new core module reads a resolved annotation into a tuple
of `TypeOption`, one per alternative, with the spelling decided above, and
`member_types` hands rows that tuple where it handed them a `LeafType`.
Everything that asked `LeafType.kind`, `.nothing` and `.inside` asks the
alternatives instead: `leaf_kind` and `text_as_value` read a text by the type
the row holds now, `_type_at` steps into what is inside each alternative, and
`elements` answers `nothing` from a `None` alternative. Which alternative a row
holds is derived from its value — the first one the value fits, `5` fitting
`float` as well as `int` — so that nothing yet depends on a choice the user
cannot make until 31B. Both backends gain the column, inactive on every row in
this sub-step: Tk a disabled `Menubutton` in a fixed-width column, Textual a
compact `Select(disabled=True)`. The kind prose leaves `descriptions`.
`model_as_text` prints the type of every row.

**Observable outcome.** `e18_declared_types.py --ui tk` and `--ui textual`
show `float` beside `threshold` although it holds `0`, `str | None` beside
`subtitle` and `note`, and the inferred `list` beside `spare` with the line
saying that it was taken from the value; `e11_add_remove.py` shows
`dict[str, StageConfig | str | dict[str, int]]` cut with `…` beside `hooks`,
with the whole of it on the line below; `e02_enum_config.py` shows the name of
the enum class beside each enum member. The *add* and *remove* controls of
optional members are still there, unchanged.

**Main risks.**

- **`textual_panel` has to be split first.** Step 29 left it within a hundred
  lines of the limit and said that the next step touching it splits the actions
  of the panel from its widgets. `tk_editor` is at 937 lines and is likely to
  need the same.
- **Width.** The column makes the Tk button row no wider but every member row
  wider, so `EditorWidgets.least_size` and the test that squeezes the window to
  it have to agree again (step 29B). Run `./run_focus_sensitive_tests.py` after
  a build, one test at a time where one fails.
- **The three ways a union is spelled at runtime.** `typing.Union`,
  `types.UnionType` and, from 3.14, the two being one type; `Optional` inside a
  container; a PEP 695 `type` alias, which is expanded to what it stands for
  and spelled as the expansion. All of it is tested on 3.12 to 3.15.
- **A value of none of its types.** `config_as_json` checks no type against an
  annotation, so a file can hold `"abc"` for an `int`. Such a row keeps the
  first alternative and reads its text by it, as a value of the wrong type is
  read today, and is not refused unless the application's validators refuse it.

**What it decided.** Seven things.

- **The column shows the type the row holds, and the whole declaration goes
  on the line below.** A pull-down shows the option it holds, so `subtitle`
  holding nothing says `None` and not `str | None`, and the line below says
  *Declared as str | None.* wherever there is more than one alternative or the
  one type was cut. The plan's outcome sentence had `str | None` beside
  `subtitle`; that was settled the other way, because a pull-down that showed
  a text none of its options has would need a widget of its own in Textual.
- **The width limit is 40 characters**, counted over every row, so that folding
  moves nothing: that answers the second open question of section 4 for now.
  Making it follow the width the editor can have is step 35.
- **The dump writes `name: type = value`**, and `name: type, 2 elements` for a
  row with no field. A nested configuration object says only its class there:
  its value text is now empty in both backends as well, because its type says
  it and its value is its rows.
- **`LeafType` and `MemberRow.declared` are removed**, not deprecated, and
  `TypeOption` is exported instead, with `MemberRow.types`,
  `MemberRow.chosen_type`, `row_type_text`, `row_type_texts` and
  `type_column_width`. `MemberRow` also gained `nothing_allowed`, because which
  members have the two states of section 4.2 is about a member of a class and
  a row cannot tell that it is one.
- **Which type a row holds and what its text is read by are two answers.** The
  first follows the current value — the first alternative it fits, falling
  back to the first that is not `None` — so the column follows a value typed
  into `int | str`. The second stays tied to the value the file was last agreed
  with, as the kind always was, so half typing cannot change how the next key
  is read.
- **A configuration class is held only where the tree has an object**, because
  an object is written as a dict: without that, `hooks.thresholds` holding
  `{"failures": 3}` read as a `StageConfig`. A place declared for an object
  and holding none holds `None` whether its declaration allows it or not,
  which is the cleared named key of `DICT_VALUE_BY_KEY`.
- **The two states of a member that may hold nothing are where they were.** A
  member has them where `None` is among its types beside a first type the
  editor can make an empty value of; an optional enum or an optional class of
  the application still has one state. That keeps *add* and *remove* unchanged,
  as this sub-step promised, and gives them to `Optional[int | str]`, which had
  none because a union of two was unreadable.

**Core.** A new `type_options` reads a hint into `TypeOption`s and answers
which of them a value fits; `member_types` hands rows those tuples and steps
into a union container through the alternative its value is; `leaf_value` lost
the kind texts, `LeafType`, `leaf_kind` and `kind_text`, and `text_as_value`
takes the kind the row reads by; `descriptions` lost the kind prose and gained
`DECLARED_FORM` and `INFERRED_TEXT`; `rows`, `elements` and `model_text` read
the alternatives. Tk gained `tk_types.TypeWidget`, a disabled `Menubutton` in
the muted colour, and Textual `textual_member.TypeChooser`, a compact disabled
`Select`, after `textual_panel` gave up the widgets of its rows to a new
`textual_rows.PanelRows`.

| Name | Kind |
| --- | --- |
| `TypeOption` | one type a declaration allows: its text, its JSON kind, what is inside it, its class, its literal values |
| `MemberRow.types` | the types its declaration allows, nothing filtered out yet |
| `MemberRow.chosen_type` | the one it holds now |
| `MemberRow.nothing_allowed` | whether it has the two states of a value and of nothing |
| `row_type_text` | the type as the column shows it, cut where it must be |
| `row_type_texts` | every type the pull-down lists, the held one always among them |
| `type_column_width` | how wide the column is for this model |

**What building it found.**

- **Textual reads the text of an option as markup**, so `list[str]` was shown
  as `list`. The options are given as `textual.content.Content`, which is
  plain. The pull-down of the values never met this, because the name of an
  enum member has no square brackets in it.
- **A disabled `Select` still posts `Changed` when it is given its value**, so
  the panel ignores the messages of a pull-down of the types; nothing can be
  chosen in one yet.
- **What a row may hold can change while the editor is open.** A row whose
  type only its value says offers that one type, and a text typed into an
  unannotated member that held `null` is a text: both backends' pull-downs of
  the types therefore remember what they offer and replace it when it
  changes, rather than only moving the selection.
- **Two mistakes of the first version were found by updating the example
  tests**, which is what they are for: an unannotated member showed the type
  it held at load (`legacy: None = kept`), and a cleared named key showed its
  class (`on_failure: StageConfig, no StageConfig`). Both are covered by core
  tests now.
- **`textual_panel` is 849 lines** after the split, and `tk_editor` 945.
- **Under a `DICT_VALUE_BY_KEY` dict every entry says *Declared as …* in
  full**, the same text as the member above it. It is true and it is
  repetitive, and 31D, which takes the configuration class out of what an
  ordinary entry is offered, changes what it says.

#### Step 31B - Choosing between the types of a plain value

Status: **Implemented, committed.**

**What it does.** The type a row holds becomes state of the buffer where the
value cannot answer for it, kept by path the way the fold state is: carried
over when the rows are built again, moved with an element that changes places,
and dropped with one that is taken out (design section 4.9). A value fits more
than one alternative — `5` for `int | float`, `''` for `str` beside a
`Literal` of text — so the user's choice has to outlive the value; a validator
that rewrites the value into one the choice no longer fits makes the value
answer again. `EditModel.set_type` changes it and applies *switching keeps what
still fits*. The pull-down becomes active wherever a row has more than one
type and **every** one of them is a plain value or `None`: `int | str`,
`float | None`, `Colors | None`. Such an optional member loses *add* and
*remove*; one whose types include a list, a dict or an object keeps them until
31C or 31D. `rows_shape` answers the type of every row as well, because a row
that changes type changes which widgets it has. The examples gain
`--set-type`.

**Observable outcome.** `e18_declared_types.py --ui tk`: `subtitle` holds
`None`, says nothing where a value would be and has no `+`; choosing `str`
gives it an empty field, and choosing `None` for `note` takes its text away
with no `-` pressed. A new member of that example declared `int | str` takes
`5` as a number while `int` is chosen and as text while `str` is, and keeps
`5` across the switch. `--ui textual` the same.

**Main risks.**

- **An enum beside another type that is not `None`.** The parse converter is
  per member and `config_as_json` calls it on every value that is not already
  of its result type, so `Colors | int` may be a declaration the class itself
  cannot read. Find out what it does before deciding whether such an enum is
  offered.
- **`settle_choices` and F4.** The type pull-down is not the value pull-down of
  step 29, and F4 switches only the second. A row that changes from `str` to an
  enum while values are being chosen has to be settled as it gets its
  pull-down.
- **Tk focus order** reaches the type before the value, while the focus that
  section 8.2.5 gives the first value at start has to stay on the value.
- A validatator may change both the value and the type of an attribute/field.
  When a validator has changed the type the editor need to show the new type
  resulting from the validation.

**What it decided.** Six things.

- **The type chosen is state for every row whose type is chosen, from the
  start, and typing never changes it.** It is read from the value when the row
  first appears, as the first type the value fits, and kept from then on; the
  text is read by it, so the two answers of 31A are one answer on such a row.
  `wide` typed while `int` is chosen is a value of the wrong type and not a
  choice of `str`. A validation pass that leaves a value the choice does not fit
  makes the value answer again, and since `config_as_json` checks no value
  against its annotation, a pass that accepts `wide` makes the row a `str`.
- **An enum beside another type is offered where the converter of the member
  takes it.** That answers the open question of section 4. The converter is run
  on the empty value of each type, `None` is not converted at all where the
  class leaves the member out of the file, and a type whose value it refuses is
  left out with *X is not offered, because the parse converter of this member
  refuses V.* below the row. Checked against `config_as_json` first: its enum
  converter refuses `3` in `Colors | int`, `"xyz"` in `Colors | str`, and the
  `null` of an `Optional[Colors]` that the class writes as `null` — so that
  last declaration is offered `Colors` alone, and never `None`.
- **A row whose type is chosen has the two states wherever `None` is one of
  its types, an element as much as a member.** An element of
  `list[Optional[str]]` holding `null` has no field and nothing where its value
  would be, and its type says `None`; the rule of section 4.2 that elements
  never have the two states is kept for every other element.
- **A `Literal` is a plain value now.** Switching to one keeps a text that is
  one of its values and gives the first otherwise; 31E adds the pull-down of
  its values and the refusal.
- **An enum is a type the editor can make a value of**, the name of its first
  member, and so is a `Literal`, its first value. That is what gives
  `Optional[Colors]` the two states, and an empty `list[Colors]` an element.
- **The value of a row whose type is chosen and that holds nothing is empty**,
  and the dump writes it `name: None`, because the type says it; a member that
  may hold a list or nothing still says `no value` with its two controls.

**Core.** A new `type_choice` says which declared types a node is offered and
why the others are not, which type it holds after a rebuild, which type a text
names, and what a node holds after a switch. `type_options` gained `choosable`
and `allowed_values`, `fits` takes the names of an enum as its values, and
`empty_option_value` gives the first value of an enum and of a `Literal`.
`elements.tree_facts` filters the declared types through the converter and
keeps the reasons, `member_types.nothing_allowed` gives every chosen row with
`None` the two states, and `elements` offers no *add* or *remove* to one.
`EditBuffer` keeps the chosen types by path and `stamped` writes them onto the
rows as `MemberRow.held`, which `chosen_type` and `kind` read first.
`rows_shape` is now the path, whether the row is a field and whether it has a
pull-down of its values. Tk's `TypeWidget` is active on a chosen row and calls
`set_type` from its menu, whose entries carry the whole type; `menu_of` and
`fill_menu` take pairs of what an entry says and what it hands on. Textual's
`TypeChooser` is enabled on a chosen row with the whole type as the value of
each option, and the panel sends its `Changed` to `set_type`. Both make the
rows again after a choice, as after an element change.

| Name | Kind |
| --- | --- |
| `EditModel.set_type` | make one node hold another of the types it is offered |
| `MemberRow.type_choosable` | whether the type of a node is the user's to choose |
| `MemberRow.held` | the type the buffer keeps for such a node |
| `row_chooses_type` | whether the pull-down of the types of a row is active |
| `row_type_choices` | every type a pull-down offers, as shown and as it is named |
| `--set-type PATH=TYPE` | the examples' stand-in for a user choosing a type |

**What building it found.**

- **A latent defect, fixed on the way:** when an element of a list was taken
  out, the element after it moved into its path and inherited what was held
  for the one taken out — its fold, and what its object had said about itself.
  Removing a folded dict from the front of a list folded the one after it. One
  helper now carries all three, the chosen types among them, and drops what was
  held at a path another node moved into.
- **The Tk focus order needed nothing.** Tk leaves a menu button out of the
  order Tab goes in, as the pull-down of the values already is, so the focus
  goes from value to value and the first one keeps it at start.
- **Textual did need something.** It focuses the first widget that takes the
  focus, which already was the fold control of a configuration whose first row
  is a container, and would now be an active pull-down of types. The panel now
  focuses its first value when it is mounted, as Tk does, and design section
  8.2.5 says so.
- **`settle_choices` has nothing to do after a switch**, because a switch to
  `bool` or an enum gives one of its values; `rows_shape` follows a validator
  that turns a text into `true`, because it says whether a row has a pull-down
  of its values.
- **e18 needed its data file changed.** The new `width` member was missing from
  `examples/data/e18_report.json`, so the load filled in every missing member
  from the defaults, `note` among them. The file now holds `"width": "auto"`,
  which also shows that a member of two types loaded from a file holds the type
  of its value.
- **`ReportConfig` of e18 has eight members now**, one more than pylint likes;
  it says why where pylint is told.

#### Step 31C - Choosing between lists and dicts

Status: **Implemented, committed.**

**What it does.** The types of a row may now include lists and dicts, and
changing between a container and anything else builds the rows again, as an
element added or removed does. The refused types are worked out here: wherever
the dict-shape check reaches — every member, and inside a checked dict every
key the loaded object holds — a dict is offered only where the loaded object
holds a dict there, and only a dict is offered where it does; inside an
`_unchecked_dicts` member, below a list and inside a member `nested_configs()`
names, everything is offered. That is `elements._holds_elements` asked one
question earlier, and it should share its walk rather than repeat it.
`NO_DICT_YET` becomes the reason the explanation line gives, and the latent
defect above goes with it. A new element of a list or a new entry of a dict whose element
type is a union is still copied by the three rules of section 4.9; the last of
them, the empty value of the declared type, takes the first alternative.

**Observable outcome.** A new example, `e20_union_types.py`, is the complaint
itself: `jira_column_map: dict[str, list[str] | list[list[str]]]` with one
entry of each. A new entry is a copy of the first, `list[str]`, and choosing
`list[list[str]]` for it gives it an empty list whose `+` adds an empty
`list[str]` — in both `--ui tk` and `--ui textual`. `e19_omitted_members.py`
shows `extra_hosts` as `list[str] | None` with no `+` or `-` of its own, and
`limits` as `dict[str, int] | None` with `dict[str, int]` left out and the line
saying why.

**Main risks.**

- **The rows below a row that changes type.** Folding, a search that had got to
  a node inside it, and the choices kept for paths inside it have to go the way
  they go when an element is removed, and the paths are what carry them.
- **The column width of nested rows.** A type inside a container is shorter
  than the member's, so the column is decided by the longest *shown* text and
  changes with folding; decide whether it may, or whether it is computed over
  every row.

**What it decided.** Seven things.

- **The dict-shape check is asked of every row, the parse converter only of a
  row whose type is chosen.** The check also decides what the control of a
  member holding nothing would give it, so `NO_DICT_YET` is no longer a
  refusal of that control but the reason a dict type is left out, beside a new
  `DICT_ONLY` for anything else left out where the class holds a dict. A member
  offered `None` alone holds nothing as a state, with no field and no control,
  and its row still says `no value`.
- **The check is mirrored as `config_as_json` makes it**, quirk included: it
  stops below any place whose *last step* is named in `_unchecked_dicts`, so a
  key deeper inside another member that has such a name stops it too.
- **It is read from the objects the rows are built from**, with no object of
  its own passed down. Those are the model's own object or what a validation
  pass accepted, and an accepted one holds a dict at exactly the checked places
  where the object it was matched against does.
- **The column is counted over every row**, which answers the open question of
  section 4: folding moves nothing, and a choice or an element that adds rows
  can widen it, as adding an element always could.
- **The type chosen lives on the rows and is resolved while they are built.**
  The types of the rows inside a container depend on the type it holds, and
  `[]` fits both lists, so the choice is needed during the build and not after
  it. Each build takes it from the row that was at the same path before, which
  moves with an element and goes with one taken out exactly as before, so the
  buffer's own map of chosen types, its `_keep_held` and `BufferState.held` are
  gone, and `kept_choice` moved down to `type_options`, because `member_types`
  steps through it and must not import upwards.
- **A copy is only what fits a container's chosen type.** A default written
  for a `list[str]` entry is no element of the `list[list[str]]` chosen for it,
  so where a container's type is chosen, what the class declares and what the
  container holds are copied only where they are values of what that type
  holds, and the declared type answers otherwise. Every other container copies
  what the application wrote, as before.
- **A node whose type is chosen is edited in a field exactly while it holds a
  plain value**, whatever it held when the file was last agreed with.

**Core.** A new `dict_check` walks the object down a path and answers whether
the check demands a dict there, refuses one, or does not reach it, and whether
the keys of a dict are matched; `elements._holds_elements` is that last answer,
and `_member_path` and `_under_list` are gone. `type_options.choosable` takes
lists and dicts that are not configuration classes, and `kept_choice` lives
there now and answers None where no type is allowed. `type_choice.offered_types`
takes `holds_dict`, gives one reason per type left out, and `switched_value`
gives the empty value to and from a container. `member_types.node_types` takes
`KeptTypes`, the previous choices and whether a pass is being taken in, and
steps into a container through the type it holds; `nothing_allowed` makes
`None` alone a state. `elements.tree_facts` computes the converters, the
omitted paths and the dict check itself, and carries the held types, which
`_typed_element` and the new `_fits_inside` read; `rows.RowContext` reads all
of it from the facts. The two backends needed no change: both already made
their rows again after a choice.

| Name | Kind |
| --- | --- |
| `dict_check.DictCheck`, `dict_check`, `dict_shape`, `keys_checked` | where the dict-shape check of a tree reaches, and what it demands |
| `type_choice.NO_DICT_YET`, `type_choice.DICT_ONLY` | why a dict type, or a type beside a dict, is not offered |
| `member_types.KeptTypes` | the types chosen before a build, and whether it takes in a pass |
| `type_options.kept_choice` | moved from `type_choice` |

**What building it found.**

- **The examples' command line could not say it.** `--add`, `--remove`,
  `--move` and `--set-type` were applied in that fixed order, and a new entry
  given a type and then an element is an add, a choice and an add. They are now
  applied in the order the command line gives them, still all before `--set`.
- **`config_as_json` reads `_unchecked_dicts` by the name of a step**, not of
  a member, because `check_dict_parse` passes the inner key to itself as `key`.
  The editor mirrors it, and `test_dict_check` shows a pass accepting a new key
  of such an inner dict; it looks like a defect of that library worth reporting
  there.
- **The README row of e18 still described 31A's add and remove controls**, and
  now says the pull-down.
- **e20's map opened folded** with paths of two or three keys, because it added
  more than eight rows; its paths are one key each, so the complaint is on the
  screen when it opens.
- **`elements` is 950 lines**, with the walk of the shape check in a module
  of its own rather than in it; `tk_editor` and `textual_panel` did not
  change.

**What its review found.** The column of the types in Tk was far wider than
its types, and ended further to the right on every step into a container,
which e20 made plain: its member is `dict[str, list[str] | list[list[str]]]`
and the rows inside it are `list[str]` and `str`.

- **Tk counts a width in characters in widths of `0`.** A type is mostly
  brackets and narrow letters, so the 38 characters of e20's member measured
  182 pixels in `TkDefaultFont` and the button asked for 378. A menu button
  that shows an image is told its width in pixels instead, so the pull-down
  shows a blank image of one pixel beside its text, written in `ROW_FONT`,
  and is given the width of that text as `tkinter.font.Font.measure` says it.
  Its height is what it was.
- **The column ends in one place.** A row is indented once per container and
  its pull-down is now narrower by as much, so the values of every row begin
  in one column, which is what section 4.12 of the design already said they
  did. The end is where the longest type of any row ends after its
  indentation, so the deepest row decides where it is longest, and every row
  is still counted, so folding moves nothing. Textual does the same in cells.
- **A value's row began 26 pixels left of a container's beside it.** The
  empty space where a value has no control to fold was a label of two
  characters, 24 pixels, and the control is a button of two characters,
  which macOS draws 50 pixels wide; the screenshot of the review shows it at
  `separator`. That is older than this step, and it was found by measuring
  where each pull-down of e20 ends. The space is now `tk_look.fold_space`, an
  empty frame as wide as a fold button made to be measured and destroyed.
- **`type_column_width` became `type_column_widths`**, one width per row,
  given how to measure a text and how far a step indents: a cell for Textual
  and a pixel of the font for Tk. It and the four other functions of the
  column moved from `model_text`, which had passed 1000 lines, to a module
  `type_column` of their own.
- **The name column was too wide in Tk for the same reason**, 24 widths of
  `0` where the names are mostly lower-case letters: a label asked for 222
  pixels where the names of the examples need 44 to 145 with their
  indentation. A second review asked for it, and it is now one width for the
  editor, the longest name of any row as `name_column_width` gives it, still
  stepping into the tree with its rows. It is never wider than the 24
  characters it always was, because a name is often a key of the user's data;
  Tk counts that limit in widths of `0` of `ROW_FONT`, Textual in cells, and a
  longer name is cut off as before. The Tk label shows the blank image for the
  width in pixels, so there is one blank image per editor now, shared by the
  names and the types, and `TYPE_FONT` became `ROW_FONT`. e17 and e20 show it.

| Name | Kind |
| --- | --- |
| `type_column_widths` | the width of the pull-down of the types of each row, replacing `type_column_width` |
| `type_column` | the module of the column of the types, moved out of `model_text` |
| `tk_look.TYPE_FONT` (now `ROW_FONT`), `tk_look.BLANK_WIDTH`, `tk_types.type_widths` | the font the Tk pull-down is measured in, its blank image, and the widths measured in it |
| `name_column_width` | how wide the column of the names is, for one model |
| `tk_look.ROW_FONT`, `tk_look.row_font`, `tk_look.blank_image`, `tk_look.name_label`, `tk_look.MEMBER_LABEL_NAME`, `tk_rows.names_width` | the font names and types are measured in, the shared blank image, the label of a name and its Tk name, and the width measured in that font |
| `tk_look.fold_button`, `tk_look.fold_space` | the Tk control that folds a container, and the space as wide as it on a row with nothing to fold |

#### Step 31D - Choosing between an object and `None`

**What it does.** An `OPTIONAL_MEMBER` and a key that `DICT_VALUE_BY_KEY`
names show `StageConfig | None`, and choosing between the two is what *add*
and *remove* did: `placing.object_added` and `object_removed` are reached
through `set_type` instead, so the model's own object still gains and loses the
object as the buffer does (design section 4.9). A class the editor cannot
construct is a type that is not offered, with `NO_CLASS_FORM` as its reason.
An ordinary entry of a `DICT_VALUE_BY_KEY` member is offered the types of the
declaration less the configuration class, because `config_as_json` refuses an
object beside the named keys; the line says so. After this, `+` and `-` mean
an element or an entry everywhere and nothing else.

**Observable outcome.** `e11_add_remove.py --ui tk`: `audit` is
`StageConfig | None` holding `None`; choosing `StageConfig` gives it an object
whose rows appear below it, and choosing `None` again takes them away. The
named key of `hooks` behaves the same, and an ordinary entry of `hooks` offers
`str | dict[str, int]`. `e19_omitted_members.py` shows the same for its
`audit`. `--ui textual` the same.

**Main risks.**

- **The subtree answers and the verdict.** An object that appears or goes is a
  change of the elements, not a validation pass, and the subtree badge of the
  object and of every container above it has to follow (design section 6.2).
- **The tests of steps 25, 26 and 28** that pressed `+` and `-` on these
  places change shape rather than meaning; check that everything they asserted
  is still asserted through the type pull-down, rather than deleting them.

#### Step 31E - `Literal` values

**What it does.** A one-kind `Literal` is a set of values the editor knows the
whole of, so `MemberRow.choices` answers with its values beside `is_bool` and
the enum converter, and the step 29 machinery — F4, `settle_choices`,
`matched_choice`, `nearest_choice` — applies to it unchanged. Its text is read
by the rules of an enum name, and a text meaning none of the values is refused
at the member as `x is not one of: a, b`, which is a second refusal of the
editor's own and is written into design section 4.2 as one. A `Literal` of
mixed kinds is the *nothing usable* rule, and the explanation says that it is.
A `Literal` among other types is one alternative of the pull-down like any
other.

**Observable outcome.** `e20_union_types.py` gains
`self.layout: Literal['compact', 'wide'] | None = 'compact'`: `--ui tk` shows
its type as `Literal['compact', 'wide'] | None` and its value as a pull-down
of the two words, F4 turns it into a field in which `wi` completes to `wide`
and `tall` is refused at the member, and choosing `None` takes the value away.
`--ui textual` the same.

**Main risks.**

- **The value pull-down and the type pull-down on one row**, both active, need
  the width of two columns where step 29 needed one; recheck `least_size`.
- **A literal value is not a name.** An enum is matched by a converter the
  class declares and a `Literal` by the editor alone, so the matching rule has
  to be the one `bool_word` already is, generalized, rather than a third copy.

#### Documentation, in every sub-step

Each sub-step updates the sections of `doc/detailed_design.md` it changes —
4.1 and 4.2 on what a declaration says, 4.3 and 4.4 on the explanation line,
4.9 on the controls, 4.11 on the values offered, and 11 — and the user's and
the application programmer's guides where what a user sees has changed. That
keeps every sub-step one review, rather than leaving a documentation step at
the end that would change what no example program does.

### Step 32 - Selectable dark mode

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

### Step 33 - Raw JSON for a subtree the editor cannot show

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

### Step 34 — The program asks for what the command line left out

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

### Step 35 - A type column as wide as the editor can afford

Tentative. Step 31A cut every type to a fixed 40 characters, which is a
constant of the core. The width the column can have is a fact about where the
editor runs: for Textual, the width of the terminal it is run in; for Tk, the
width the window could be resized to and still fit on the display. The column
should take what that leaves after the name, a usable field and the marks,
with 40 as the least it is ever given or as a default, and the line below the
row still says the whole of a type that was cut.

## 4. Open questions recorded, not answered

These do not block current development, and each is scheduled to be answered at the
step that needs it. They are listed here so they are not forgotten.

| Question | Answer needed by |
| --- | --- |
| Is an enum offered beside a type that is not `None` (`Colors \| int`), given that the parse converter runs on every value of the member? (31B: the converter of the member is run on the value each type would give, and a type it refuses is not offered, with the reason below the row.) | answered |
| Is the width of the type column decided over the rows on the screen, and so changed by folding, or over every row? (31A counts every row, so that folding moves nothing; 31C confirmed it.) | answered |
| Should the width of the type column change when the Tk window is resized, or only be worked out when the editor opens? | 35 |
