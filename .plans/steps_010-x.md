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
- [Step 11](#step-11--nested-config-objects) — a nested `Config` object as a
  node with a class, a docstring and members of its own, and the ownership of
  everything inside it.
- [Step 12](#step-12--subtree-validation) — every nested object asked whether
  it is a configuration on its own, which both puts a badge on its row and
  names the member inside it that a validator refused.
- [Step 13](#step-13--list_element-and-dict_value-nesting) — a list of
  configuration objects and a dict of them, one description reaching every one
  of them, and the confirmation that step 11 had already built the mechanism.
- [Step 14](#step-14--adding-and-removing-elements) — how many things a member
  holds, where a new element is copied from, and the containers that say why
  they cannot be given one.
- [Step 15](#step-15--confirmation-before-dropping-edits) — closing an editor
  that holds something unsaved asks first, in words the core owns and in a
  dialog or a screen that each backend puts.
- [Step 15B](#step-15b---changed-descriptions-of---ui-dump) — the two
  interactive editors described as the product they are, and `--ui dump` as
  the very limited non-interactive user interface it is.
- [Step 16](#step-16--oldbackup-file-when-overwriting) — the file that a save
  writes over kept under the name the application chose, once per destination
  per session, and a question before it happens.

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
  observed from `examples/src/example/` with `--ui tk` or `--ui textual`,
  it is the wrong step boundary and should be merged into a neighbour or
  split differently.
- Every step touches all three packages where the capability is
  user-visible, so `edit_cfg_json`, `edit_cfg_json_tk` and
  `edit_cfg_json_textual` never drift apart by more than one review.
- Steps 1 to 9 are built, and each is written up in
  [steps_001-009_done.md](steps_001-009_done.md) as what it decided, what it
  found while building it and what came of its review. Steps 10 to 15 are
  built and are written up here, in the same way. Steps 16 onwards are named
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
| M5 Release readiness | 15 to 17 | Closing keeps what was not saved, files are not overwritten unannounced, and v1 is documented, classified and published | steps 15, 15B and 16 done |

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

Status: **Implemented and committed.**

**Observable outcome.** A new example `e09_nested_config.py`, modelled on
`e33_nested_configs.py`, whose configuration holds two nested `Config` objects
of one class. `python3 examples/src/example/e09_nested_config.py --ui dump`
shows each of them as a row saying its class with its own members below it,
`--set participant_output.encoding=latin-1` edits one of those members,
`--fold participant_output` folds the object away and leaves the summary of its
class, and `-i ../../data/e09_with_audit.json` fills the optional object that
the defaults leave empty. `--ui tk` and `--ui textual` show the same tree.

**What it decided.** Four things, decided before the work started.

- **`OPTIONAL_MEMBER` is in scope**, as it falls out. A member holding an
  object is a node like any other; one holding none has no row where the class
  omits it from JSON, and a row saying which class is missing where the class
  writes `null`. That row cannot be edited, because no text becomes a
  configuration object; making one is adding, and stays with step 14. This is
  the open question the plan asked to settle explicitly. Design section 4.1.
- **A nested node shows the summary of its class while it is folded and the
  whole docstring while it is open**, both under the explain toggle. Design
  section 4.3 read literally, and it makes folding do one thing rather than
  two: a node showing less of itself says less about itself.
- **The validity state stays with step 12**, which is what that step is named
  after. This step delivers the class, the docstring, the members and the
  ownership.
- **The mechanism is general**, so `LIST_ELEMENT`, `DICT_VALUE` and
  `DICT_VALUE_BY_KEY` became editable subtrees at the same time as `MEMBER`.
  Refusing them would have cost code rather than saved any. Step 13 is
  therefore smaller than planned: it is its own example, the `'['` descriptions
  across repeated objects, and the tests for them.

**Core.** `tree.config_nodes` walks the configuration object and answers with
every configuration object of the tree by its absolute path, the root under the
empty path; `tree.owner_path` finds the object that owns any node; `flat_values`
walks into a nested object by that object's own declared member order.
`converting.node_converters` and `descriptions.optional_paths` are the
ownership those two questions needed. `rows.built_rows` takes the configuration
object and builds its own `RowContext`, because a validation pass hands back
the object it accepted and the nested objects of *that* one are what own its
values.

The public names it settled:

| Name | Kind |
| --- | --- |
| `MemberRow.config_type` | the class of the object at this node, or None |
| `row_describes` | whether anything can ever be said below one node |

**What building it found.**

- **Ownership is asked of an object, not of a declaration.** Step 10 found
  nested nodes by turning each declaration into a `'['` selector, which was
  right while such a node was one row. `parse_converters()`,
  `_omit_none_from_json()` and the declaration order of the members are all of
  an *instance*, so the declarations are now walked over the real object. That
  also tells the truth where a `factory_function` answered with a subclass, and
  it is what distinguishes an `OPTIONAL_MEMBER` holding an object from one
  holding none. The selector keeps its meaning where it is still the right
  question, which is the description mapping.
- **What is said below a nested node changes when it is folded**, so both
  backends had to write that text again on every fold and not only when the
  explain toggle is pressed. Neither of them did, because until now nothing
  below a row ever changed by itself. `row_describes` came out of the same
  finding: a backend creates no widget where nothing can ever appear, and the
  description a row carries is no longer the whole of what appears.
- **A refusal from inside a nested object is not attributed to its member.**
  Such an object validates itself while the whole configuration is parsed, so
  the object that could be asked which member was refused is one the editor
  never holds — the probe of design section 6.3 subtracts one method from one
  copy, and the nested objects are constructed inside `parse_json` where that
  cannot reach. Validating each subtree on its own is what answers it, which is
  exactly step 12. Until then the message is in the block below the members. A
  value whose *text* means nothing is unaffected and is attributed at the
  member as before, because that is asked of the member alone.
- **`config_as_json` does not scope its parse converters the way it scopes its
  serialize converters.** `Config.parse_json` passes its own object hook to
  `json.loads`, so the root's converters run over every decoded object,
  including the JSON of a nested object, while `serialize_converters()`
  explicitly stops at a child-owned subtree. The editor follows the design and
  asks the owning class. The case where the two differ — an ancestor declaring
  a converter for a key name that a nested class holds unconverted — is a class
  that cannot read back what it writes at all, so the application meets it on
  its own first load and not through the editor.
- **The row helpers of the model tests were factored out** into
  `model_helpers.py`, because a second module asking the same four questions of
  a model tripped the duplicate-code check, which is the check working.

#### Step 12 — Subtree validation

Status: **Implemented and committed.**

**Observable outcome.** `e09_nested_config.py` gains a badge on every nested
object and a rule that relates its two outputs across the boundary between
them. `python3 examples/src/example/e09_nested_config.py --ui dump` says
`participant_output: TableOutputConfig [valid on its own]`;
`--set participant_output.output_format=xml` says *refused on its own* and
names the member it is about, which is the half step 11 could not do; and
`-i ../../data/e09_with_audit.json --set
audit_output.file_name=advanced-participants.csv` shows both objects valid on
their own while the configuration is refused, which is the risk this step was
written to guard against. `--ui tk` and `--ui textual` show the same badges.

**What it decided.** Four things, decided before the work started.

- **Folding an object asks it, and so does opening it**, and every validation
  pass asks all of them. The badge is on the row whether the object is open or
  folded, and an edit anywhere inside it takes the answer back. Design
  sections 4.7 and 6.2.
- **The badge says *valid on its own*.** The qualifying words are the whole
  point: a rule of the class above may refuse the configuration while saying
  nothing against either object, so a badge reading only *valid* would answer
  a question that is not its to answer. Design section 6.2.
- **What a nested object refuses about no member of itself is shown at that
  object**, not in the block below the members. It is about the object, and
  the object is a node with a row. Design sections 6.2 and 6.5.
- **The object is copied and not constructed**, which is design section 6.2
  corrected to what step 9 settled for section 6.1. The object is there to be
  copied, so a class needing a constructor argument this library knows nothing
  about is asked exactly as well as any other, and a `factory_function` that
  answered with a subclass is asked as the subclass it really is.

**Core.** `validation._single_pass` is what step 9's `validate_buffer` became,
and `validate_buffer` is now that pass plus every nested object asked about
the part of the buffer it owns. `subtree_states` and `subtree_verdict` are
what folding asks. Refusals from inside an object are merged into
`ValidationVerdict.refused` under absolute paths, so nothing about how a
refusal is shown or how long it lives had to change.

The public names it settled:

| Name | Kind |
| --- | --- |
| `MemberRow.subtree_valid` | what one object is on its own, None if unasked |
| `row_validates` | whether a node can ever say what it is on its own |
| `row_subtree_text` | what it says, as it is shown |
| `subtree_emphasis` | how that stands out, the same three states as a verdict |

**What building it found.**

- **A pass the class accepted answers for every object at once**, because
  `parse_json` builds and validates each nested object while it reads the
  buffer. So the walk runs only when the whole buffer was refused, which is
  also the only time it has anything to add.
- **The innermost object has to be asked first.** An object holding a refused
  object is refused whatever else is true of it, and asking it again would
  report one mistake once for every object it happens to be inside.
- **Every nested object was reporting itself as changed by a validator.** The
  editor holds the members of such an object in the order its class declares
  them and `config_as_json` writes them sorted, so the first validation pass
  after any edit inside one found a different JSON notation for the same
  values. `values_differ` now compares canonically, which is the rule design
  section 5.3 already stated for the comparison the load makes and for the
  same reason; the two now share `leaf_value.canonical_text`. A defect of step
  11, found because this step gave `e09` a reason to edit inside an object.
- **A file that a cross-boundary rule refuses cannot be opened at all**, so
  the example demonstrates that rule with `--set` rather than with a data
  file of its own. `parse_json` ends in `validate()`, which is design section
  5.2 working as designed and worth saying in the example.
- **The two backend test modules tripped the duplicate-code check**, because
  the badge texts are asserted in both and neither package may import the
  other. The constants were regrouped so that each file states them where it
  reads them, which is what design section 8 asks for before a suppression.

### Milestone 4 — configs in containers

#### Step 13 — `LIST_ELEMENT` and `DICT_VALUE` nesting

Status: **Implemented and committed.**

**Observable outcome.** A new example `e10_config_containers.py`, modelled on
`e34_list_nested_configs.py` and `e35_dict_nested_configs.py`, whose
configuration holds a list of three `ReportOutputConfig` objects and a dict of
two more of them.
`python3 examples/src/example/e10_config_containers.py --ui dump` shows the
list folded and the dict open, each object in the dict a row saying its class
with its own members below it and its own badge;
`--fold reports --set reports.0.file_name=other.csv` opens the list and edits
one member of one element; `--set reports_by_id.audit.max_rows=0` is refused by
the element class's own rule and named as `reports_by_id.audit.max_rows`;
`--fold reports --set reports_by_id.audit.file_name=participants.csv` makes a
report of the dict collide with a report of the list, which the class holding
them both refuses while all five objects say *valid on its own*; and
`-i ../../data/e10_reports.json` holds two reports and three named ones, which
folds the other one of the two containers. `--ui tk` and `--ui textual` show
the same tree.

**What it decided.** Four things, decided before the work started.

- **The core needs no change, and that is the finding rather than a
  disappointment.** The prediction of design section 4.1 — that steps 13 and 14
  change what a nested node offers and never how the tree is built — turned out
  to be empty for this step. Verified against the installed build before any
  code was written: a list and a dict of objects already had one node per
  element with its own badge, `'['` already reached inside repeated objects at
  any depth, a refusal inside one element was already attributed by absolute
  path, and a save already round-tripped. So the step is the example, the
  tests, and the write-ups. Design section 4.1.
- **One class, one list and one dict, in one configuration.** Two examples in
  the shape of `e34` and `e35` would have shown one nesting kind each and
  neither would have shown the thing that matters, which is that the same class
  serves both and that one rule reaches over both.
- **The example is sized so that the two containers open differently.**
  `OPEN_AT_MOST` is eight rows below a container, so three objects of three
  members each opens folded and two opens open. That is the rule of step 10 met
  where a real configuration meets it: a container of configuration objects
  reaches the limit at three of them rather than at a dozen numbers. The data
  file inverts the two counts, so the fold state at the start follows the file
  and not the member.
- **Both kinds of rule, per object and over all of them.** The element class
  refuses a row count out of range, which shows that one plan runs once per
  object without the class holding them saying anything; and the class holding
  them refuses two reports that name one file, which is the rule no object
  could check for itself and the one that makes every object say *valid on its
  own* while the export cannot be written. `DICT_VALUE_BY_KEY` is deliberately
  left to step 14, which is where what can and cannot be added is decided.

**Core.** Nothing. The tests that pin the `'['` selector across repeated
objects went into `test_nested.py`, beside the tests of the containers of
objects that step 11 added: one description for that member of every element of
a list, the same through a dict, one for the object itself, a named step
beating `'['` at that step, and a selector with `'['` at two depths reaching
into a list of objects each holding a dict of more of them.

No public name was added or changed, which is what a step that only exercises
the API should look like.

**What building it found.**

- **A container of configuration objects opens folded much sooner than a
  container of values.** Three objects of three members each is twelve rows,
  and `OPEN_AT_MOST` is eight. That is `OPEN_AT_MOST` working as designed and
  it was worth meeting deliberately in an example, because it is the first
  thing a user of a realistic configuration sees.
- **A `--set` inside a folded container edits the buffer and shows nothing.**
  The dump prints only the rows that are on the screen, and `StandInUser`
  applies the edits before the folds, so `--fold reports` after a `--set`
  inside it is what makes the edit visible. It is the command line standing in
  for a user, and a user would open the container first; the example says so
  rather than leaving the reader to find out.
- **The examples README had never been given `e09`.** Its table ended at
  `e08`, so the example that step 11 added and step 12 extended was reachable
  only by knowing it was there. Both rows are in it now.
- **Nothing in either backend had ever rendered two objects of one class in
  one container**, which is why each of them gained a test over the new class:
  several objects have the same member names, and a backend that identified a
  widget by anything but its place among the rows would have been wrong about
  every one of them. Neither was, which the counts now say.

**What its review found.** Two defects in what folding asks and in what it does
with the answer, both of which only a container of configuration objects could
show — which is what the example this step added was for.

- **A fold kept the answer and threw the sentences away.** A folded object said
  *refused on its own* and nothing said what was wrong with it, so the user had
  to validate the whole configuration to be told the rest of something they had
  just been told half of. The two are one answer with one lifetime, and they
  are now kept together: `SubtreeAnswer` is the state and what that object
  refused, the buffer holds one per object beside the fold state, and `stamped`
  writes both onto the rows. That also removed the carrying over of the state
  through a rebuild, and it fixed a smaller inconsistency of step 12 on the
  way — an edit outside an object used to leave its badge standing while the
  sentence under its member vanished with the verdict. Design section 6.2.
- **Folding a list or a dict asked nothing at all.** `subtree_verdict` asked
  the one node that was folded, and such a member is no configuration, so
  folding the member that holds several objects — the ordinary shape of design
  section 4.1 — found nothing. A fold answers *what is being hidden* rather
  than *what is this node*, so `subtree_answers` asks every object at or inside
  the node, and one function replaced both `subtree_states` and
  `subtree_verdict`. Design section 4.7.
- **A container of objects needed a badge of its own**, because its row is the
  only one a fold leaves on the screen. It says *valid inside* and *refused
  inside*, which cannot be read as a verdict about the container itself, and
  `row_validates` is now `MemberRow.has_objects` so that a backend creates the
  widget for a container of objects and for nothing else. Design section 6.2.
- **The Textual backend did not write the diagnostics again on a fold.** It
  wrote the descriptions and the badges, because until now nothing else below a
  row could change without a key being typed. The Tk backend already did.

The public names the review settled:

| Name | Kind |
| --- | --- |
| `MemberRow.subtree_refusal` | why the object owning this node refused it |
| `MemberRow.has_objects` | whether an object is at this node or inside it |
| `MemberRow.is_object` | whether an object is really at this node |

#### Step 14 — Adding and removing elements

Status: **Implemented and committed.**

**Observable outcome.** A new example `e11_add_remove.py` whose configuration
holds every shape a member with several of something can have.
`python3 examples/src/example/e11_add_remove.py --ui dump --add stages` puts one
more configuration object into a list and the verdict then says that two stages
share a name, which is the application's rule and not the editor's;
`--add extra_stages` grows a declared list that holds nothing, `--add
retry_delays` copies the first element the class declares, `--add runners=nightly`
names a new entry of a dict, `--remove runners.fast` takes one out, `--move
stages.0=down` changes two of them round, and `--add audit` gives the optional
member its object. `--add extra_hosts` is refused, and the member says why below
itself, until `-i ../../data/e11_pipeline.json` puts something in it to copy.
`--ui tk` and `--ui textual` show the same controls on the same rows.

**What it decided.** Four things, decided before the work started:

- **Reordering a list and creating or clearing an `OPTIONAL_MEMBER` object are
  in scope**, beside adding and removing. The first is what the order of a list
  being part of the file asks for; the second is what design section 4.1 already
  called adding. A list or a dict declared to hold configuration objects can be
  given one while it is empty, because what an element is comes from the
  declaration.
- **The user names a new entry of a dict**, in a dialog in Tk and in a modal
  screen in Textual, because nothing else knows what one is called. Inventing a
  placeholder key was rejected: a dictionary key is not editable in this model,
  so the invented name would be the name for good.
- **The controls sit on the row, at the end of the line**, and why a container
  cannot be given an element is a `MUTED` line below it, under the explain
  toggle with every other explanation. Design section 4.9.
- **The pattern for a new element of an ordinary list is the declared values,
  and failing that what the member holds now.** That is one fallback more than
  this document first described, and it earns its place: a member the class
  declares nothing for becomes extendable as soon as a file has put something in
  it, which is the ordinary way such a list gets its first element.

**Core.** `elements` owns what a node offers, where a new element is copied
from and what one change does to the values, to the paths and to the
configuration object of the session; `MemberRow.offer` carries it to the
backends. `tree` gained `member_nestings` and `unchecked_members`, which are the
two questions a declaration and a key policy answer, and `member_values` moved
there from `rows`. `built_rows` is told whether it is refreshing after a
validation pass, because a row the user added is not a row a validator wrote.

The public names it settled:

| Name | Kind |
| --- | --- |
| `ElementOffer` | what one node offers about the elements it holds |
| `MemberRow.offer` | that offer, on the row a backend reads it from |
| `EditModel.add_element` | put one more element into a node |
| `EditModel.remove_element` | take one element out of what holds it |
| `EditModel.move_element` | make one element change places with a neighbour |

**What building it found.**

- **An ordinary dict member can neither gain nor lose a key.**
  `Config.check_dict_parse` matches such a member against the keys its class
  declares, so `config_as_json` itself refuses the next validation pass.
  Confirmed against the implementation in `./venv` before any code was written.
  That is why "uniform dicts" means the declared ones: only a `DICT_VALUE`
  member is a dict of one kind of thing, and the other three kinds each say so
  below themselves in words of their own. Design section 4.9.
- **A new element has to be made as an object and not only as JSON.** The tree
  finds the nested objects by walking the real ones, so an element that existed
  only in the buffer would be shown as the dictionary it serializes to, with
  nobody's member order, nobody's parse converters and no badge. The model's own
  copy of the configuration therefore gains the object with the values.
- **Everything the buffer holds about a node is held under the path of that
  node**, and an element of a list is addressed by where it is. Removing or
  moving one therefore moves the fold state, what each object said about itself
  and what each row is compared against along with the values. Without that,
  removing the first element reported every element after it as edited by a user
  who had touched none of them.
- **A member that a class omits from JSON while it holds no object cannot be
  given one**, because it has no row to press. That follows from design section
  4.1 rather than from this step, and it is why clearing such a member is not
  offered either: the editor would be taking it off the screen for good.
- **Both backend modules had to be split again**, at 1000 lines each:
  `tk_elements` and `textual_elements` hold one row's worth of controls, and
  `textual_ask` holds the one screen that both of this backend's questions are
  asked on — the output file and the new dictionary key — which is what kept the
  second question from being the first one written twice.

### Milestone 5 — release readiness

#### Step 15 — Confirmation before dropping edits

Status: **Implemented and committed.**

If Cancel/Close is asked for in an editor with unsaved changes it should ask
for confirmation before discarding the edits.

**Observable outcome.** Any example, in either graphical backend: edit a value
and press Close, and the editor asks whether the changes may be dropped rather
than dropping them. `python3 examples/src/example/e01_flat_config.py --ui tk`
and `--ui textual` both show it, the answer that keeps the changes is the one
the question opens on, and closing again after a Save asks nothing. `--ui dump`
is unchanged and shows nothing of it, which is the point of the fourth decision
below.

**What it decided.** Four things, decided before the work started.

- **Whether the user is asked and what they are asked belong to the core**, as
  `close_question`, which answers with nothing at all when there is nothing to
  ask about. It is a decision that depends on the state of the model, so it is
  the core's by design section 4.5, and two user interfaces of one application
  that disagreed about whether they warn would be worse than either behaviour.
  How the question is put is each backend's own. Design section 7.2.
- **Every way out asks, including the close button of the window.** Both
  backends route the button, the key and — in Tk — `WM_DELETE_WINDOW` through
  one method, because the one way out that is not a widget of the editor would
  otherwise be the one way out that drops the changes silently. It is set on
  the window `TkEditor` created and on no other.
- **Two answers and not three.** Saving on the way out would have to cope with
  a refused save, with no destination chosen yet, and with the Save-as question
  opening from inside a confirmation, all of which belong to saving rather than
  to closing.
- **No `Settings` attribute.** Whether anything is unsaved the editor knows for
  itself, which design section 9.6 keeps out of `Settings`. Whether
  *overwriting* is confirmed is step 16's, and is the application's to say.

**Core.** `model_text.close_question` and the `CLOSE_QUESTION` it words. The
model needed nothing: `dirty` already answers "the buffer holds something worth
saving", and a save moves the values the buffer is compared with.

| Name | Kind |
| --- | --- |
| `close_question` | what to ask before closing, nothing when nothing |

**What building it found.**

- **Both backend modules were at pylint's thousand-line limit again**, and
  what to move out was already named by the modules themselves. `tk_ask` now
  holds every question this backend asks — the file to write and the key of a
  new entry moved out of `tk_editor` and `tk_elements`, and the new one joined
  them — which is the mirror of `textual_ask`. `textual_look` now holds the
  widget identifiers, the style classes, the sizes and the whole style sheet,
  which is what its own docstring had claimed all along while half of them sat
  in `textual_editor`. Nothing in `textual_look` imports another module of its
  backend, so everything that builds a widget reads its identifier and its
  style class from there.
- **The dump backend is asked nothing at all.** It prints once and returns, so
  there is no session to close and nobody to answer; the question would have
  been printed at a user who could not answer it. That is why this step changes
  no example output and is reviewed by running a window.
- **Textual needed the safe answer to be the one with the focus.** A modal
  screen takes the focus to its first control, which would have been Discard,
  and Enter would then have dropped the changes of a user who pressed it
  without reading. `AUTO_FOCUS` names the other control, which is the same
  answer as the Tk dialog's `default=NO`.

#### Step 15B - Changed descriptions of `--ui dump`

Status: **Implemented and committed.**

Today `--ui dump` is incorrectly described as the main focus in examples
and almost as the preferred user interface. This is incorrect and must
be changed in `./doc/design.md` in docstrings and in the example descriptions.

This repo provides 2 real interactive user interfaces, one based on
Textual and one based on Tkinter. Descriptions of examples should focus
on how the example behaves in the interactive user interfaces.
Descriptions of features shall focus on how the feature behaves and is
usable in an interactive backend.

The `--ui dump` backend provides:

- a way to excercise features over the core/backend API without using
  an interactive backend, useful for quick tests and for testing in
  scripts.

- a way to execute a short sequence of editor actions and getting a
  printout of the results, in a non-interactive way.

This is a very limited non-interactive user interface, but it has its
uses as such. The documentation and design documents should
describe `--ui dump` as this very limited non-interactive user interface,
but it has its uses as such. Never describe it as the main or preferred
user interface.

**Observable outcome.** This is the one step that changes what every example
*says* and nothing about what any of them *does*, so the rule of section 1
about an observable outcome is met by reading rather than by running. What a
review runs is the two editors, on any example, to check that what is now
written about them is true: `python3 examples/src/example/e11_add_remove.py
--ui tk` shows the controls that its docstring now tells the reader to count,
and `--ui textual` shows the same. Every `--ui dump` command line in the
repository still prints exactly what it printed before.

**What it decided.** Four things, decided before the work started.

- **The two interactive editors are the product, and a printout is not one of
  them.** Design section 1.1 is where that is said once, and everything else
  points at it. The reason is not taste: a printout has no field to type into,
  no control to press, no focus to lose and nobody to answer a question, so it
  can show what the model holds and can never show what an editor does. A
  document that taught a feature through a printout was teaching the smaller
  half of it.
- **Being limited is not a fault, and the two real uses are stated wherever
  the backend is named.** Exercising a feature over the core and backend API
  with no display is what a script and every example test need, and printing
  what a short sequence of editor actions left behind is a thing worth being
  able to do. A checker that answers with an exit code is a useful thing to be.
  What was wrong was the ranking and never the claim: `--ui dump` really does
  render the same `model_as_text` that both backends draw.
- **`DumpEditor` and `--ui dump` keep their names**, and the `--ui` help
  strings are left as they were. This step changes what is said about them and
  not what they are, so no application, no script and no test moves.
- **`readme_parts/` and the root `README.md` are in scope**, because the first
  sentence a reader of PyPI meets is in `three_packages.md` and the first they
  meet in the repository is in `README.md`. Everything else about those files
  stays with step 17, which already rewrites them.

**Core.** No code at all: docstrings, `readme_parts/`, `README.md`,
`doc/design.md` and this plan. `doc/*_api.md` and the three `README_pypi.md`
are generated by the build from exactly those sources, so they follow without
being edited, which is the check that the docstrings really are where this
lives.

**What building it found.**

- **`doc/design.md` never wrote `--ui dump` at all**, and its sections 4 to 7
  were already written about a window and a terminal throughout. So the sweep
  it was given added the statement that was missing rather than correcting
  ones that were wrong: section 1.1 names the backend and its two uses,
  section 6.1 says that a validation pass is *asked for* in an editor and that
  validating before printing is what having no user does to that question,
  section 10.1 says that a printout is evidence about the core and never about
  a backend, and sections 7.2 and 8.3 now point at section 1.1 rather than
  describing the backend again in their own words.
- **The ranking lived in the examples**, which is where a reader learns what
  this library is. `cmd_line.py` and the examples README both said "the text
  dump is not a lesser mode", every one of the eleven examples opened its "run
  this example" block with `--ui dump`, and every "inside this repository" line
  named it as well. Each example now leads with the two editors and says what
  there is to *do* in one of them — leave the field in `e02`, press `f1` in
  `e03`, press a fold control in `e08`, count the controls along the rows in
  `e11` — and keeps every `--ui dump` line below that as the way to reach the
  same thing from a script.
- **Two of the sixteen exit codes belong to the non-interactive program
  alone.** `_outcome` in `cli.py` answers `OK` for any interactive backend
  whatever is left in the fields, so `INVALID` and `NOT_WRITTEN` are reachable
  only from `edit-cfg-json`. `readme_parts/program.md` is shared by all three
  programs and had never said so, which made its exit code table read as
  though an editor could refuse to end well.
- **A command line in `e01` named `--ui` twice.**
  `--ui dump --key save=ctrl+w --ui textual` is `argparse` taking the last of
  the two, so what it demonstrated was reached by accident. Moving a key is
  something a user presses, so it is `--ui textual --key save=ctrl+w` now, and
  the two file name settings beside it stay on `--ui dump` because a printout
  can say where it wrote as well as a window can.
- **The two backends were called *graphical* in four places**, and one of them
  draws in a terminal. It was the right word while there was one window and one
  printout to tell apart and it is the wrong one for what this step is about,
  so all four say *interactive* now — which is also the word that puts the two
  editors on one side of the line and the printout on the other.
- **Every `readme_parts` still opens its "what it shows" section with "the
  package is under construction" and a description of a flat configuration**,
  in all three packages, which stopped being true at step 10. It is not about
  `--ui dump`, and step 17 rewrites those files against what was actually
  built, so it is recorded here rather than fixed in passing.

#### Step 16 — Old/backup file when overwriting

Status: **Implemented and committed.**

If the editor is asked to write to a file name where the file exists, it
should create an old/backup file with the previous content (probably by
renaming the existing file to the old/backup file name). This logic only
applies if the file was not previously saved to (written) by the editor in
the current editing session (as we do not want to keep an extra backup file
for every time the user presses save). Design decision to take here: Should
editor also ask for confirmation before over-writing an existing file? Note:
This behaviour should probably be configurable in the Settings dataclass.
We should probably let application choose backup file extension (like
xx.cfg.bak or yy.cfg.old or zz.cfg~) in the Settings dataclass.
We should probably let the application opt in for several numbered backup
files (xx.cfg.bak_1, xx.cfg.bak_2, xx.cfg.bak_3...) in the Settings dataclass.

**Observable outcome.** A new example `e12_backup_files.py`, whose application
has decided how its own files are looked after and says so in a `Settings` of
its own, in Python, as a real application does.
`cp examples/data/e12_archive.cfg /tmp/archive.cfg` and then
`python3 examples/src/example/e12_backup_files.py --ui tk` then change something
in the editor and press `Save`. It writes the file and says that the previous
content is in `/tmp/archive.cfg.old_1`; a second
run with an edit and pressing Save twice and keeps one file, so `old_1` and
`old_2` hold the two configurations that were really there and there is no
`old_3`; editing keep_days to "soon" and then pressing Save, causes save to
be refused and leaves every one of the where it was.
`--ui tk` and `--ui textual` ask before they overwrite, in a
dialog and on a modal screen, with the answer that leaves the file alone
offered first, and ask nothing on the second press of Save.

**What it decided.** Four things, decided before the work started.

- **The user is asked, and it is the application that decides whether they
  are.** `confirm_overwrite` is `True` by default, which is the way a default
  about something that cannot be undone should lean. Whether there is anything
  to ask about is the core's, as `overwrite_question`, which is exactly the
  shape step 15 settled for closing and for the same reason: two user
  interfaces of one application that disagreed about whether they warn would be
  worse than either behaviour.
- **One attribute names the kept file, and it is added to the whole name.**
  `backup_suffix` defaults to `.bak`, so `xx.cfg` is kept as `xx.cfg.bak`, and
  `.old` and `~` are the same attribute rather than three shapes to choose
  between. `None` keeps nothing. Design section 7.3.
- **`backup_count` numbers them from `_1` and rotates.** One is not numbered,
  because a number would say that there are others when there are not; two or
  more are `_1` for the file overwritten last, each save moves every one of
  them one further back, and the oldest falls off the end.
- **The keeping happens after the validation and immediately before the
  write.** That is what makes a refused save keep nothing, which matters: a
  refused save that had pushed the kept files along would cost the user the
  oldest of them for nothing.

**Core.** `saving` gained the naming, the rotation and `keep_previous`, and
`write_config` says where the previous content went whether it then wrote the
file or not. `SaveState.written_files` is what "this session has written that
destination" is, `EditModel.overwritten_file` is what a backend asks before it
saves, and `model_text.overwrite_question` is the question. `Settings` gained
the three attributes, and `_check_backups` beside `_normalize_extension`.

The public names it settled:

| Name | Kind |
| --- | --- |
| `Settings.backup_suffix` | what the overwritten file is kept as, None for none |
| `Settings.backup_count` | how many of them are kept |
| `Settings.confirm_overwrite` | whether the user is asked first |
| `EditModel.overwritten_file` | the file a save would overwrite, None for none |
| `overwrite_question` | what to ask before saving, nothing when nothing |

**What building it found.**

- **A save was reading the settings more than once.** `checked_file` asked for
  them and so did the keeping, and an application that hands over a callable is
  asked again at every point of use — so one save could check the name against
  one answer and keep the previous content according to another. The settings
  are resolved once at the top of `save` and passed down now. Found by the test
  that hands over a callable answering differently every time, which was
  written for step 9 and is why this cost one line rather than a bug report.
- **A `Config` with an empty validation plan accepts a value of the wrong
  type.** `config_as_json` checks the declared type of a member only where the
  application asks it to, so the new example's `keep_days` took the text `soon`
  and would have written it. The example declares one `ValueTypeValidator`, so
  that there is a save it can have refused — which is what shows that a refused
  save keeps nothing either.
- **Tk's own file dialog offers to ask this question.** `asksaveasfilename`
  confirms overwriting by default, which would have meant the Tk backend asking
  where the Textual one did not, and asking twice where the core asks as well.
  It is told `confirmoverwrite=False`: the question is the core's.
- **The question comes before the validation, and that is deliberate.** A user
  who types an invalid value and presses Save is asked about the file and then
  told that the values are refused. Validating first would mean running a pass —
  which rewrites what the user typed and marks it — for a save the user then
  declines, and leaving the buffer changed by something that did not happen is
  worse than one question that was not needed.
- **`ConfirmScreen` needed the words of each answer.** One screen serves both
  questions of this backend, and Discard beside a question about a file would be
  a word to work out rather than read, so the labels are constructor arguments
  and the identifiers are `YES_ID` and `NO_ID` rather than the names of the
  closing answer.
- **`run_example` had to be able to take a `Settings`.** Every example before
  this one gets its settings from the command line, which is right for trying
  an answer without writing a program and wrong for showing what an application
  does. It takes one now, and the command line options fill in the parts they
  name with `dataclasses.replace`.
- **`test_edit_model.py` went over a thousand lines**, so what a model does
  about the file it writes is `test_model_saving.py` now: saving, keeping,
  the destination and the file name settings, which are also the tests of that
  module that have a file system in them.

#### Step 16B - fix UX problem with edit_cfg_json

Users are mislead by the available command `edig_cfg_json`. Users think that
this is a smart program running the best interactive editor with internal
logic to choose between tk and textual. Considering the naming they are
really right to think that.

Move the starting of DumpEditor from `__main__.py` to another file, and
change the code so that DumpEditor is started with
`python3 -m edit_cfg_json.dump`

Adding logic so that command `edig_cfg_json` uses smart logic to run
the best interactive editor, is out of scope for this step, but may be
added in a later step.

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

Make sure all references to examples from `config_as_json` package/repo
references the `config_as_json` repo (not necessary with complete URL
more than first time in document) as future readers will otherwise not
understand that what references refer to.

Remove references to step numbers in `./doc/design.md` and `readme_parts`
and also remove any description of order of implementation, but
information what is implememented and what is planned for future stays.
The future reader of `./doc/design.md` or `README_pypi` will not be
interested in the order things were implemented in, what is
interesting is to know what is implemented and what is only planned.

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

#### Step 21 - Add and remove ommitted members

A member that a class omits from JSON while it holds no object shall also
be possible to add and remove in the editor. Exactly how to achieve this
is the subject of a design investigation in the beginning of this step.

#### Step 22 - Full support for `DICT_VALUE_BY_KEY`

Add full support for adding and deleting values in a dict that are
declared by `DICT_VALUE_BY_KEY`.

## 4. Open questions recorded, not answered

These do not block step 1, and each is scheduled to be answered at the
step that needs it. They are listed here so they are not forgotten.

| Question | Answer needed by |
| --- | --- |
| ~~When does a field report that its text means no value at all, and is that on focus loss?~~ Answered at step 7: it does, on focus loss, through `EditModel.check_field`. See `doc/design.md` sections 4.2 and 6.5. | done |
| ~~Does `Config.write()` validate, making the editor's gate belt and braces?~~ | step 5 done |
| ~~Is `ConfigNestingKind.OPTIONAL_MEMBER` in v1 scope?~~ Answered at step 11: it is. A member holding an object is a node like any other, one the class omits from JSON has no row, and one written as `null` has a row that says which class is missing and cannot be edited. | done |
| ~~Does the Textual headless driver in the pinned 8.2.8 behave as the design assumes?~~ | step 1 done |
| ~~Will the README test summary stop updating on a headless machine, per design section 10.2?~~ | step 1, as a known consequence |
| Which widget does the Tk backend bind its keys on when it shares a window? See `doc/design.md` section 8.2.7. | step 18 |
| Does the core name the mounting contract with a `Protocol` of its own? | step 18, or the first third-party backend that mounts |
| Does `Settings` say whether an embedded editor's bindings are priority bindings? | step 18 |
