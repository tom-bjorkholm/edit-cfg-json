# Delivering the remaining scope in small steps

## Where everything is

Steps 1 to 21 are implemented and committed. Steps 1 to 9 are written up in
[steps_001-009_done.md](steps_001-009_done.md) and steps 10 to 21 in
[steps_010-021.md](steps_010-021.md). The steps still to build are in
[steps_022-x.md](steps_022-x.md). Where any of the three files mentions a
design decision, [`doc/design.md`](../doc/design.md) remains the authority and
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
[s10]: steps_010-021.md#step-10--lists-and-dicts-of-scalars
[s11]: steps_010-021.md#step-11--nested-config-objects
[s12]: steps_010-021.md#step-12--subtree-validation
[s13]: steps_010-021.md#step-13--list_element-and-dict_value-nesting
[s14]: steps_010-021.md#step-14--adding-and-removing-elements
[s15]: steps_010-021.md#step-15--confirmation-before-dropping-edits
[s15b]: steps_010-021.md#step-15b---changed-descriptions-of---ui-dump
[s16]: steps_010-021.md#step-16--oldbackup-file-when-overwriting
[s16b]: steps_010-021.md#step-16b---fix-ux-problem-with-edit_cfg_json
[s17]: steps_010-021.md#step-17--first-release-polish
[s18]: steps_010-021.md#step-18--embedding-in-an-applications-own-window
[s18b]: steps_010-021.md#step-18b---redesign-api-and-examples-for-embedding
[s19]: steps_010-021.md#step-19---config_as_jsonconfig-for-storing-the-settings
[s20]: steps_010-021.md#step-20--the-rest-of-the-programs-command-line
[s21]: steps_010-021.md#step-21---version-command-line-flag

## 1. How this plan is meant to be used

This document turns the scope recorded in
[`doc/design.md`](../doc/design.md) into an ordered list of small,
individually reviewable and individually committable steps. It is a delivery
plan, not a design document: where it mentions a design decision,
`doc/design.md` remains the authority and this file only says *when* that
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
- Steps 1 to 21 are built, and each is written up in
  [steps_001-009_done.md](steps_001-009_done.md) or in
  [steps_010-021.md](steps_010-021.md) as what it decided, what it found
  while building it and what came of its review. Steps 22 onwards are named
  steps with their observable outcome and their main risks; they are detailed
  just before they are started, when the core API is real rather than
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

## 3. Steps 22 onwards, as named steps

Each of these is detailed just before it is started. What is fixed now is
the order, the observable outcome and the main risk.

### Step 22 - Better bool support

When the user enters a bool value they should get the same support as
when entering an enum value. The text in the text field should be
compared to `true` and `false` in a case insensitive way and if the
text in the field matches the beginning of `true` or `false` it should
be expanded to that value.

### Step 23 - Finding a member

Section 9.7 keeps `ctrl+f` and `f3` free from the start, because finding a
member of a configuration that does not fit a window (section 4.6) is something
this editor is likely to be asked for, and a test says the defaults take
neither key. Nothing implements the search they are reserved for. What is found
has to be reachable, so a match inside a folded container opens it, and both
backends have to bring it into view — the canvas in Tk and `scroll_visible` in
Textual. Which member is being looked for is state, and belongs in the core by
the lesson of step 6 about the explanation toggle.

### Step 24 - More type information, and whether the user may change it

Two things the design records and no step claims, both in section 4.2. It is an
open question whether the user may change the type metadata of a leaf, and the
reason it might be wanted is written down: telling a `None` apart from an empty
string in an `Optional[str]`. And later versions are said to be likely to
derive more type information from the attribute types than the type of the
default value, which is all section 4.1 has today. The step answers the
question before it builds what the answer asks for.

Built before step 28 it would give the pull-down a better answer about which
members have a known set of values, and before step 25 it would give that
step's investigation a type model to start from. Neither is forced.

### Step 25 - Add and remove omitted members

A member that a class omits from JSON while it holds no object shall also
be possible to add and remove in the editor. Exactly how to achieve this
is the subject of a design investigation in the beginning of this step.

One possible idea to investigate for how to implement this:
With vars() on the config object we can detect the member variable even
when it has value None.
We should (in most cases) be able to look up the Python code (often in
site-packages). Most of the time the Python code is type and the type hint
tells us what class the attribute should have. We should be able to
create an object of that type, and then get the fields to edit from that
object.
For the cases when this fails, we should be clear to the user that we
failed to discover what the types of the editable fields should be for
this sub-object, but as a fallback we offer the user to type in raw
JSON for this sub-object that the editor can then validate.
This first idea could lead to better spin off ideas.

### Step 26 - Full support for `DICT_VALUE_BY_KEY`

Add full support for adding and deleting values in a dict that are
declared by `DICT_VALUE_BY_KEY`.

### Step 27 - Adding an entry to an `_unchecked_dicts` member

Section 4.9 of the design names three kinds of dict that cannot be given an
entry. One of them is permanently impossible, one of them is step 23, and this
is the third: a member of `_unchecked_dicts`, whose key policy the application
defines with validators of its own, which the design marks out of v1 scope and
no step has claimed. Such a member stops saying why it cannot be given an entry
and is offered the controls every other container already has; a key the
application's own validators refuse is then the ordinary verdict.

It shares its mechanism with step 23, because both need a dict that accepts a
key its class does not declare, so whichever is built first makes the other one
cheaper. Neither forces the other's order.

### Step 28 - Pull-down selection of enum and bool values

When the type of an attribute have a well defined set of possible
values that we know from type discovered by introspection we should
offer the user to select the value instead of typing the value.
This is the case for bool, and for enums.

### Step 29 — The program asks for what the command line left out

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

### Step 30 - The launcher the name `edit-cfg-json` is kept for

Section 8.1 of the design is headed "planned, not implemented": an
`edit_cfg_json.ui` entry-point group would let backends register themselves for
discovery, which is what `--ui=auto` needs. Section 8.3 keeps the command name
`edit-cfg-json` free for the launcher that picks the editor the machine can
run, and step 16B freed that name and said the logic for choosing "may be added
in a later step". This is that step: both editor packages register themselves,
the core installs the launcher it has never installed a program for, and a
machine with no display or without `textual` gets the editor it can actually
run, with a refusal and an exit code of its own where it can run none.

## 4. Relative effort of the steps still to build

Best guesses, for judging the order the rest is built in. Step 24 is the
smallest and is 1; every other step is a multiple of it. **The number is the
whole cost of a step** as section 1.1 defines done: the design summary, the
code, the tests, the example, the documentation, three clean builds on 3.12,
3.13 and 3.14, and the review. That floor is why nothing is below 1, and why
the largest step is ten times the smallest rather than thirty times — the steps
differ less in what they cost than in how hard they are. The rows are in effort
order and therefore not in step order.

| Step | Effort | What the number is mostly |
| --- | --- | --- |
| 22 Better bool support | 1 | One rule in the core's conversion path, beside the enum rule that is already there. No backend change. |
| 27 An entry in an `_unchecked_dicts` member | 2 | Step 14's machinery reused: the row stops saying why it cannot, and both backends show controls they already have. |
| 26 Full `DICT_VALUE_BY_KEY` | 3 | The same work, complicated by a member whose values are of two kinds, and by what deleting the named key would mean. |
| 30 The launcher | 4 | Little logic, spread over all three packages: an entry-point group, a script the core has never installed, discovery, and what a machine that can run neither editor is told. |
| 23 Finding a member | 5 | Core state and one field, then bringing a widget into view in two toolkits and opening what folding hid. Partly focus sensitive, so partly category 3. |
| 28 Pull-down for enum and bool | 6 | A second kind of field in both backends, touching every rule written for the first: write on change, focus loss, the rebuild after a pass, and the marks. |
| 24 More type information | 6 | It answers a design question before it builds anything, and the runtime records nothing for the ordinary `Config` pattern (section 4.1). |
| 25 Add and remove omitted members | 8 | Discovering a class the runtime does not record, and then the raw-JSON fallback, which is an editing surface the editor does not have at all yet. |
| 29 The wizard | 10 | Two toolkits' dialogs and file choosers, two bridge libraries to weigh against the menubar alternative, and no headless test worth much. |

Two things the numbers do not say.

- **Effort is not order.** Step 27 shares its mechanism with step 26, and step
  24 would make steps 25 and 28 cheaper, so cheapest first is not
  automatically right.
- **Steps 24, 25, 29 each begin with a question**, so their numbers are the
  three least trustworthy of the nine.

## 5. Open questions recorded, not answered

These do not block current development, and each is scheduled to be answered at the
step that needs it. They are listed here so they are not forgotten.

| Question      | Answer needed by |
| ------------- | ---------------- |
| (nothing yet) |                  |
