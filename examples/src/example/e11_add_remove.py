#! /usr/bin/env python3
"""Example 11: adding and removing the elements of a list or a dict.

Examples 8 to 10 showed members that hold several of something and let every
one of those be edited. A member is a list or a dict because **how many** of
them there are is a decision of whoever configures the application, so this
example is about the other half: putting one more in, taking one out, and
moving one of them along the list.

The interesting part is not that it works. It is *where* it works and where it
cannot, because the editor never invents a value the application never
mentioned. This one configuration puts every case side by side:

- `stages` — add, remove, move. `LIST_ELEMENT` says every element of it is
  a `StageConfig` object, so the declaration says what a new one is.
- `extra_stages` — add, remove, move. The same declaration over an *empty*
  list, which can still be given an element for exactly that reason.
- `retry_delays` — add, remove, move. The class declares elements for it, so
  the first of them is what a new one is copied from.
- `extra_hosts` — remove and move only. Its declared value is empty and
  nothing declares an element, so there is nothing to copy.
- `runners` — add with a key, remove. `DICT_VALUE` says every value of it is
  a `RunnerConfig` object.
- `limits` — nothing. Its class declares which keys it has.
- `labels` — nothing. `_unchecked_dicts` makes its keys the application's own.
- `hooks` — nothing. `DICT_VALUE_BY_KEY`: one named key of it holds an object
  and the others hold ordinary values.
- `audit` — add and remove. An `OPTIONAL_MEMBER` is given its object, or put
  back to holding none.

## A new element is copied and never invented

There are exactly two places a new element can come from, and both of them are
the application's.

**The nesting declaration.** `LIST_ELEMENT` and `DICT_VALUE` name a class, and
a new element is one object of that class holding the values it declares. That
works for a container that is *empty*, which is what `extra_stages` shows: the
declaration says what an element of it is even though the member holds none.

**The values the class declares for the member.** `retry_delays` starts as
`[1, 5, 15]`, so the editor knows what one element of it looks like: a whole
number, and `1` in particular. A new one is a copy of the first.

`extra_hosts` has neither. Its class declares an empty list and no nesting, so
nothing anywhere says what one host looks like, and the editor says so instead
of guessing at `''` or `'localhost'`. Its elements can still be removed and
moved; there is simply nothing to add. Read a file that holds one, and it can
be extended from then on, because the member now holds an element to copy.

````sh
cd examples/src/example
python3 e11_add_remove.py --ui dump --add stages
python3 e11_add_remove.py --ui dump --add extra_stages --add extra_stages
python3 e11_add_remove.py --ui dump --add retry_delays
python3 e11_add_remove.py --ui dump --add extra_hosts \
    -i ../../data/e11_pipeline.json
````

## An entry of a dict needs a key

`--add runners=nightly` says what the new entry is called, because nothing but
the person configuring the application knows. The two graphical backends ask
for it in a dialog and in a screen; the command line takes it after an equals
sign, exactly as `--set` takes a value.

A dict is written in the sorted order of its keys, so a new entry appears
where that order puts it and not at the end.

````sh
cd examples/src/example
python3 e11_add_remove.py --ui dump --add runners=nightly
python3 e11_add_remove.py --ui dump --remove runners.fast
````

## Three dicts that cannot grow, for three different reasons

Each of them says why below its own row, with the rest of the explanations:

- **`limits`** is an ordinary dict member. `config_as_json` checks such a
  member against the keys its class declares — `Config.check_dict_parse` does
  it while parsing — so a dict that gained or lost one would be refused by the
  configuration class itself. The editor says so rather than offering a
  control that produces a refusal.
- **`labels`** is listed in `_unchecked_dicts`, which is how a class takes that
  check away and defines its key policy with validators of its own instead.
  What those validators allow is the application's to say, and serving it is
  out of scope for version 1.
- **`hooks`** is declared `DICT_VALUE_BY_KEY`: one named key of it holds a
  configuration object and the others hold ordinary values. That is a per-key
  policy as well, and it is out of scope for the same reason.

Nothing is half-supported: none of the three gets a control at all.

````sh
cd examples/src/example
python3 e11_add_remove.py --ui dump --fold stages --fold runners
````

## An optional member is added and removed too

`audit` holds one `StageConfig` or none. No text typed into a field becomes a
configuration object, so giving it one is *adding*, and putting it back to
holding none is *removing*. It works here because this class writes `null` for
that member; a class that listed it in `_omit_none_from_json()` would leave it
out of the file altogether, and a member with no row could never be given an
object again, so the editor does not offer to clear one of those.

````sh
cd examples/src/example
python3 e11_add_remove.py --ui dump --add audit
python3 e11_add_remove.py --ui dump --add audit --set audit.name=cleanup
````

## What the application still decides

Adding an element is not a way round the rules. `StageConfig` refuses a stage
that asks for more than ten hours, `RunnerConfig` refuses a runner that would
run more than sixty-four stages at once, and the class holding the stages
refuses two stages with one name — so adding a second copy of a stage is
accepted by the editor and refused by the application, which is exactly what a
validation pass is for:

````sh
cd examples/src/example
python3 e11_add_remove.py --ui dump --add stages
python3 e11_add_remove.py --ui dump --add stages --set stages.2.name=deploy
````

The first of those adds a stage called `build`, which the pipeline already
has, and the verdict says so. The second renames it and the verdict is clean.

That last rule is written as a **method of the configuration class** and named
in the plan with `CallingWholeConfigValidator`, which is the shorter of the two
ways `config_as_json` offers; examples 9 and 10 write the other one, a
`WholeConfigValidator` subclass. A rule about several members at once usually
wants what the object already knows, and a method has that without being
handed the object. What it does not have is the diagnostics stream, so it
raises rather than printing, and the editor shows what the failure says
wherever nothing was printed.

## Moving an element

The order of a list is part of what the file says, so it is part of what an
editor of that file has to be able to change. A dict has no such question: it
is written in the sorted order of its keys.

````sh
cd examples/src/example
python3 e11_add_remove.py --ui dump --move stages.0=down
python3 e11_add_remove.py --ui dump --move retry_delays.2=up
````

Run this example with one of:

````sh
python3 examples/src/example/e11_add_remove.py --ui dump
python3 examples/src/example/e11_add_remove.py --ui tk
python3 examples/src/example/e11_add_remove.py --ui textual
````

Inside this repository, use the virtual environment that the build creates:
`./venv/bin/python3 examples/src/example/e11_add_remove.py --ui dump`.

There is a file to read in [examples/data/](../../data/), and it holds a
pipeline whose `extra_hosts` is not empty, which is what makes that member
extendable:

````sh
cd examples/src/example
python3 e11_add_remove.py --ui dump -i ../../data/e11_pipeline.json
````
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from pathlib import Path
from typing import Optional, TextIO
import sys
from config_as_json import CallingWholeConfigValidator, Config, \
    ConfigNesting, ConfigNestingKind, InvalidConfiguration, \
    IntFloatValidator, MemberValidationStep, NestedConfigs, PathOrStr, \
    ValidationPlan, WholeConfigValidationStep
from edit_cfg_json import Descriptions

FEWEST_MINUTES = 1
"""Fewest minutes that one stage of this example may be given."""

MOST_MINUTES = 600
"""Most minutes that one stage of this example may be given."""

MOST_PARALLEL = 64
"""Most stages that one runner of this example may run at once."""

REPEAT_REFUSAL = 'Two stages of this pipeline are both called {name}.'
"""What the rule below says when two stages share a name.

It is the rule that makes adding an element interesting: a new stage is a copy
of what the class declares, so a second one is a stage the pipeline already
has, and the application refuses it until it is given a name of its own.
"""

NAMES_METHOD = 'check_stage_names'
"""Name of the method of the configuration that holds that rule.

`CallingWholeConfigValidator` is what runs a rule that lives as a method of
the configuration class rather than as a validator class of its own, which is
the shorter of the two ways `config_as_json` offers. Examples 9 and 10 write
the other one.
"""

_OPTIONAL = ConfigNestingKind.OPTIONAL_MEMBER
"""What declares that a member holds one configuration object or none."""

_BY_KEY = ConfigNestingKind.DICT_VALUE_BY_KEY
"""What declares that one named key of a dict holds one."""

HOOK_KEY = 'on_failure'
"""The one key of the hooks dict that holds a configuration object.

Every other key of that dict holds an ordinary value, which is what
`DICT_VALUE_BY_KEY` declares and what makes the keys of such a member a policy
of their own.
"""


class StageConfig(Config):
    """One stage of the pipeline: what it is called and what it runs."""

    def __init__(self, from_json_data_text: Optional[str] = None,
                 from_json_filename: Optional[PathOrStr] = None,
                 stderr_file: TextIO = sys.stderr) -> None:
        """Initialize one stage with its default values.

        Args:
            from_json_data_text: Optional JSON text to parse directly.
            from_json_filename: Optional path to a JSON file to read.
            stderr_file: Stream used for user-facing diagnostics.
        """
        # These three values are what a new stage holds when the editor adds
        # one, because a new element of a `LIST_ELEMENT` member is one object
        # of this class holding what this class declares.
        self.name: str = 'build'
        self.command: str = 'make'
        self.minutes: int = 10
        super().__init__(from_json_data_text=from_json_data_text,
                         from_json_filename=from_json_filename,
                         stderr_file=stderr_file)

    def get_validation_plan(self, stderr_file: TextIO) -> ValidationPlan:
        """Return the one rule that every stage of this example obeys."""
        _ = stderr_file
        in_range = IntFloatValidator[int](min_value=FEWEST_MINUTES,
                                          max_value=MOST_MINUTES,
                                          allowed_values=None)
        return [MemberValidationStep(member_names=['minutes'],
                                     validator=in_range)]


class RunnerConfig(Config):
    """One machine that the stages of this pipeline can run on."""

    def __init__(self, from_json_data_text: Optional[str] = None,
                 from_json_filename: Optional[PathOrStr] = None,
                 stderr_file: TextIO = sys.stderr) -> None:
        """Initialize one runner with its default values.

        Args:
            from_json_data_text: Optional JSON text to parse directly.
            from_json_filename: Optional path to a JSON file to read.
            stderr_file: Stream used for user-facing diagnostics.
        """
        self.host: str = 'localhost'
        self.parallel: int = 1
        super().__init__(from_json_data_text=from_json_data_text,
                         from_json_filename=from_json_filename,
                         stderr_file=stderr_file)

    def get_validation_plan(self, stderr_file: TextIO) -> ValidationPlan:
        """Return the one rule that every runner of this example obeys."""
        _ = stderr_file
        at_once = IntFloatValidator[int](min_value=1, allowed_values=None,
                                         max_value=MOST_PARALLEL)
        return [MemberValidationStep(member_names=['parallel'],
                                     validator=at_once)]


def new_stage(name: str, command: str, minutes: int,
              stderr_file: TextIO) -> StageConfig:
    """Return one stage holding the values it is given.

    The values are assigned after the object is built, because the constructor
    of a configuration class takes JSON and not values. That is the same thing
    `config_as_json` does when it reads a file, and the same thing the editor
    does when it adds an element.

    Args:
        name: What this stage is called.
        command: What this stage runs.
        minutes: How long this stage may take.
        stderr_file: Stream used for user-facing diagnostics.

    Returns:
        One stage holding those values.
    """
    stage = StageConfig(stderr_file=stderr_file)
    stage.name = name
    stage.command = command
    stage.minutes = minutes
    return stage


def new_runner(host: str, parallel: int, stderr_file: TextIO) -> RunnerConfig:
    """Return one runner holding the values it is given.

    Args:
        host: Machine that this runner is.
        parallel: How many stages it runs at once.
        stderr_file: Stream used for user-facing diagnostics.

    Returns:
        One runner holding those values.
    """
    runner = RunnerConfig(stderr_file=stderr_file)
    runner.host = host
    runner.parallel = parallel
    return runner


def _default_stages(stderr_file: TextIO) -> list[StageConfig]:
    """Return the stages that this pipeline runs to begin with."""
    return [new_stage('build', 'make', 10, stderr_file),
            new_stage('test', 'make check', 30, stderr_file)]


def _default_runners(stderr_file: TextIO) -> dict[str, RunnerConfig]:
    """Return the runners that this pipeline knows to begin with."""
    return {'fast': new_runner('build-1.example.org', 4, stderr_file),
            'slow': new_runner('build-2.example.org', 1, stderr_file)}


def _default_hooks(stderr_file: TextIO) -> dict[str, StageConfig | str]:
    """Return the hooks dict, one key of which holds a stage.

    `DICT_VALUE_BY_KEY` declares exactly that shape: the value at
    `on_failure` is a configuration object and every other key of the same
    dict holds an ordinary value. It is the shape that makes the keys of such
    a member a policy of their own rather than all one kind of thing.
    """
    hook = new_stage('rollback', 'make rollback', 5, stderr_file)
    return {HOOK_KEY: hook, 'notify': 'ops@example.org'}


# Ten members is more than pylint likes one class to have, and here it is the
# whole point: each of them is one of the shapes a member that holds several
# of something can have, and they are side by side so that what the editor
# offers for each can be read in one window.
# pylint: disable-next=too-many-instance-attributes
class PipelineConfig(Config):
    """Every stage that one build pipeline runs, and where it runs them.

    The members below hold several of something in every way a configuration
    holds several of something, so that what can be added to each of them and
    what cannot can be read side by side.
    """

    def __init__(self, from_json_data_text: Optional[str] = None,
                 from_json_filename: Optional[PathOrStr] = None,
                 stderr_file: TextIO = sys.stderr) -> None:
        """Initialize the pipeline with its default values.

        Args:
            from_json_data_text: Optional JSON text to parse directly.
            from_json_filename: Optional path to a JSON file to read.
            stderr_file: Stream used for user-facing diagnostics.
        """
        self.pipeline_name: str = 'nightly'
        # A list of configuration objects: the declaration below says what an
        # element is, so one can always be added.
        self.stages: list[StageConfig] = _default_stages(stderr_file)
        # The same declaration over an empty list. It is still extendable,
        # because what an element is comes from the declaration and not from
        # what the member happens to hold.
        self.extra_stages: list[StageConfig] = []
        # A list of plain values with elements declared for it, so the first
        # of them is what a new one is copied from.
        self.retry_delays: list[int] = [1, 5, 15]
        # A list of plain values with none declared. Nothing anywhere says
        # what one element of it looks like, so nothing can be added.
        self.extra_hosts: list[str] = []
        # A dict of configuration objects, keyed by the name each is asked for
        # under. A new entry needs a key, which only the user knows.
        self.runners: dict[str, RunnerConfig] = _default_runners(stderr_file)
        # An ordinary dict member. `config_as_json` checks it against the keys
        # declared here, so it can neither gain nor lose one.
        self.limits: dict[str, int] = {'cpu': 2, 'memory': 512}
        # A dict whose key policy this class defines with validators of its
        # own instead of with the check above. Out of scope for version 1.
        self.labels: dict[str, str] = {'team': 'platform'}
        # A dict where one named key holds a configuration object and the rest
        # hold ordinary values. Out of scope for version 1 as well.
        self.hooks: dict[str, StageConfig | str] = _default_hooks(stderr_file)
        # An optional member: one stage or none. Giving it one is adding.
        self.audit: Optional[StageConfig] = None
        # This is what takes the declared-keys check off `labels`, and it has
        # to be assigned before the base class is initialized.
        self._unchecked_dicts = ['labels']
        super().__init__(from_json_data_text=from_json_data_text,
                         from_json_filename=from_json_filename,
                         stderr_file=stderr_file)

    def every_stage(self) -> list[StageConfig]:
        """Return every stage of this pipeline, however it is held.

        A rule about the stages taken together has to see all of them, and
        which member one is in says nothing about that. The hooks are left
        out on purpose: a hook is not a stage of the pipeline.

        Returns:
            The stages of both lists, and the audit stage where there is one.
        """
        found = [*self.stages, *self.extra_stages]
        return found if self.audit is None else [*found, self.audit]

    def check_stage_names(self) -> None:
        """Refuse a pipeline in which two stages share a name.

        This is what makes adding an element worth showing: the editor copies
        what the class declares, so the second stage it adds is called `build`
        like the first, and the application is what says that will not do. The
        editor never checks a rule of its own; it runs the application's.

        The method is not given the diagnostics stream, because
        `CallingWholeConfigValidator` calls it with the arguments the plan
        named and no others, so it raises rather than printing. The editor
        shows what the failure says wherever nothing was printed, which is
        exactly this case.

        Raises:
            InvalidConfiguration: Two stages share a name.
        """
        names = [stage.name for stage in self.every_stage()]
        for name in sorted(set(names)):
            if names.count(name) > 1:
                raise InvalidConfiguration(REPEAT_REFUSAL.format(name=name))

    def nested_configs(self) -> NestedConfigs:
        """Return which members hold configuration objects, and how.

        All five kinds of `ConfigNestingKind` that `config_as_json` has are
        here except `MEMBER`, which example 9 shows, and each of them decides
        what the editor offers for that member.
        """
        return {'stages': ConfigNesting(kind=ConfigNestingKind.LIST_ELEMENT,
                                        config_type=StageConfig),
                'extra_stages': ConfigNesting(
                    kind=ConfigNestingKind.LIST_ELEMENT,
                    config_type=StageConfig),
                'runners': ConfigNesting(kind=ConfigNestingKind.DICT_VALUE,
                                         config_type=RunnerConfig),
                'hooks': ConfigNesting(config_type=StageConfig, kind=_BY_KEY,
                                       discriminator_key=HOOK_KEY),
                'audit': ConfigNesting(config_type=StageConfig,
                                       kind=_OPTIONAL)}

    def get_validation_plan(self, stderr_file: TextIO) -> ValidationPlan:
        """Return the one rule that is about all the stages at once.

        It is written as a method of this class and named here, which is what
        `CallingWholeConfigValidator` is for. A rule about several members at
        once often wants what the object already knows — `every_stage` here —
        and a method has that without being handed the object.
        """
        _ = stderr_file
        named = CallingWholeConfigValidator(method_name=NAMES_METHOD)
        return [WholeConfigValidationStep(validator=named)]


DESCRIPTIONS: Descriptions = {
    ('pipeline_name',): 'Which pipeline these stages belong to.',
    ('stages',): 'The stages this pipeline runs, in the order it runs them.',
    ('stages', '[', 'minutes'): 'How long this stage may take, in minutes.',
    ('extra_stages',): ('Stages that only some runs need. It is empty, and a '
                        'new one can still be added: what an element of it is '
                        'comes from the declaration.'),
    ('retry_delays',): ('How long to wait before each retry, in seconds. A '
                        'new one is a copy of the first.'),
    ('extra_hosts',): ('Machines to build on besides the runners. Nothing '
                       'declares what one looks like, so nothing can be '
                       'added until the member holds one.'),
    ('runners',): 'The machines this pipeline may run its stages on.',
    ('runners', '[', 'parallel'): 'How many stages this machine runs at once.',
    ('limits',): 'What one stage may use.',
    ('labels',): 'Whatever this installation wants to label its builds with.',
    ('hooks',): 'What to do when a run does not go as planned.',
    ('audit',): 'A stage that records what the run did, when it is wanted.'}
"""What this application says about the members it declares.

Every member that holds several of something is described, because the whole
point of this example is what each of them offers, and a member the
application says nothing about would be shown with only what the editor knows.
The line the editor adds below each of them — why nothing can be added there —
is the editor's own and is never in a mapping like this one.
"""


def main(args: Optional[list[str]] = None) -> None:
    """Run this example from the command line.

    Args:
        args: Optional replacement for `sys.argv[1:]`, mainly for tests.
    """
    # The import is inside the function so that running this file directly
    # works. The block at the end of the file puts the examples source folder
    # on sys.path first, and only after that is `example.cmd_line` importable.
    # pylint: disable-next=import-outside-toplevel
    from example.cmd_line import run_example
    run_example(example_name='e11_add_remove', args=args,
                config=PipelineConfig(), descriptions=DESCRIPTIONS)


# The usual guard, so that importing this module from a test runs nothing.
if __name__ == '__main__':
    # Running a file directly puts only that file's own folder on sys.path,
    # so the `example` package this file belongs to would not be importable.
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    main()
