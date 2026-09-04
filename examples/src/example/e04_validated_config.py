#! /usr/bin/env python3
"""Example 4: saying which member of a configuration is wrong.

Example 1 showed the editor refusing a buffer and printing what the
application said about it. That is honest and it is not enough: a
configuration of any size gives the user one block of text and leaves them to
work out which of a dozen fields it was about. This example is about the
answer, and about the one case where there is no answer to give.

## Why the editor has to work for it

`Config.validate()` applies the validation plan in order and stops at the
first step that refuses. So the pass that decides whether the buffer is valid
can report exactly one failure, and the exception it raises does not say which
member it was about. There is nothing in `config_as_json` that would say.

What there is, and it is enough, is that a validation plan is public. A
`MemberValidationStep` says which members it is about, in `member_names`, and
holds the validator in `validator`, and `MemberValidator.validate_member()`
takes one member and one value. So the editor walks the same plan a second
time, runs each member's own validators, and puts what each of them says
beside the member it is about. Two things fall out of that, and both of them
are visible below:

- **Every wrong member is named at once**, because this walk does not stop at
  the first refusal. The user corrects one round of mistakes instead of one
  mistake per round.
- **No validator class is recognised by type.** `NoSpacesValidator` below is
  written by this application and `config_as_json` has never heard of it, and
  it is attributed exactly as the `IntFloatValidator` beside it. That is not a
  detail: an editor that only understood the validators of one library would
  be useless to the applications that need one most.

## The case that has no answer, and why it is shown differently

The last step of the plan below is a `ProjectedWholeConfigValidator`. It is
about `retries` and `timeout_seconds` *together* — how long the job can take
in the worst case — and that is about neither of them alone. There is no
member to put it beside, so it stays where the whole configuration is
reported, below the members.

That is the rule the editor follows: what belongs to a member is shown at
that member, and what belongs to no member stays in the block. The line above
the block names the members that were refused, so a configuration too tall
for a window still says where to look.

Notice also that the whole-configuration rule is not even reached while a
member is refused. That is not a shortcut. `Config.validate()` would not have
reached it either, because it would have stopped at the member before it, and
an editor that reported a rule the application never applied would be making
things up.

Run this example in one of the two editors, where a validation pass is asked
for with the Validate button or with `ctrl+r`, or `f5`:

````sh
python3 examples/src/example/e04_validated_config.py --ui tk
python3 examples/src/example/e04_validated_config.py --ui textual
````

Inside this repository, use the virtual environment that the build creates:
`./venv/bin/python3 examples/src/example/e04_validated_config.py --ui tk`.

Break two members at once and ask for the pass, and each of them carries its
own sentence below its own field while the line above the block names both. A
configuration too tall for the window is exactly the case that attribution
exists for, and scrolling to the named member is what makes it worth having.

`--ui dump` is the very limited non-interactive user interface, and it
validates once before it prints, because there is nobody to press Validate.
These four make the same edits and show one member being refused by a
validator this application wrote, one being refused by a validator
`config_as_json` ships, both being refused at once, and the rule that is about
no single member:

````sh
cd examples/src/example
python3 e04_validated_config.py --ui dump --set job_name='nightly backup'
python3 e04_validated_config.py --ui dump --set retries=9
python3 e04_validated_config.py --ui dump --set job_name='a b' --set retries=9
python3 e04_validated_config.py --ui dump --set retries=5 \
    --set timeout_seconds=400
````

The third is the one worth looking at twice. Both members are named on the
verdict line and each of them carries its own sentence, and the block below
is empty, because there was nothing left over that was about no member.

The fourth is the other way round. Neither member is named and neither
carries a sentence, because neither of them is wrong: `5` retries is allowed
and a timeout of `400` seconds is allowed, and it is the six attempts of 400
seconds that are not. So the block below is where it is said, which is the
only place it could honestly be said.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from pathlib import Path
from typing import Optional, TextIO
import sys
from config_as_json import Config, InvalidConfiguration, IntFloatValidator, \
    MemberValidationStep, MemberValidator, PathOrStr, \
    ProjectedWholeConfigValidator, ValidationPlan, WholeConfigValidationStep
from edit_cfg_json import Descriptions

MOST_RETRIES = 5
"""Largest number of retries that this configuration accepts."""

LONGEST_TIMEOUT = 600
"""Longest timeout in seconds that this configuration accepts."""

LONGEST_RUN = 900
"""Longest total time in seconds that one run of the job may take.

This is the rule that is about no single member: it is the timeout multiplied
by the number of attempts, so neither `retries` nor `timeout_seconds` is wrong
on its own when the product of them is too large.
"""

SPACE_REFUSED = 'Invalid configuration: {name} may not contain a space.'
"""What the validator this application wrote says when it refuses."""


# This is the validator that `config_as_json` has never heard of. It is an
# ordinary class deriving from `MemberValidator`, which is the whole of what
# an application has to do to have a rule of its own, and the editor treats
# what it says exactly as it treats what a validator of the library says.
# pylint: disable-next=too-few-public-methods
class NoSpacesValidator(MemberValidator):
    """Refuse a text value that has a space anywhere in it."""

    def validate_member(self, config: Config, member_name: str,
                        member_value: object,
                        stderr_file: TextIO = sys.stderr) -> Optional[object]:
        """Refuse the value when it holds a space, and keep it when not.

        A member validator returns the value that is stored back into the
        member, so a validator that only checks returns what it was given.
        The message is printed before the exception is raised, which is the
        contract of `config_as_json`, and it is also what the editor shows
        beside the member: what the user reads is what this line writes.
        """
        _ = config
        if isinstance(member_value, str) and ' ' in member_value:
            message = SPACE_REFUSED.format(name=member_name)
            print(message, file=stderr_file)
            raise InvalidConfiguration(message)
        return member_value


class ValidatedConfig(Config):
    """A nightly job, with three rules about it and one about all of it.

    Two of the rules are about one member each, so the editor can say which
    member they are about. The third is about how long the job can take
    altogether, which is neither of the members it is computed from, so it is
    reported for the configuration as a whole.
    """

    def __init__(self, from_json_data_text: Optional[str] = None,
                 from_json_filename: Optional[PathOrStr] = None,
                 stderr_file: TextIO = sys.stderr,
                 member_name: Optional[str] = None) -> None:
        """Initialize the configuration with its default values.

        Args:
            from_json_data_text: Optional JSON text to parse directly.
            from_json_filename: Optional path to a JSON file to read.
            stderr_file: Stream used for user-facing diagnostics.
            member_name: Path for reaching this object from the top level
                configuration, so that a diagnostic about a value inside it
                names the whole path. None for the top level itself.
        """
        self.job_name: str = 'nightly-backup'
        self.retries: int = 2
        self.timeout_seconds: int = 120
        super().__init__(from_json_data_text=from_json_data_text,
                         from_json_filename=from_json_filename,
                         stderr_file=stderr_file, member_name=member_name)

    def get_validation_plan(self, stderr_file: TextIO) -> ValidationPlan:
        """Return two rules about single members and one about all of them.

        The order is what `config_as_json` applies them in, and the editor
        walks the same list: the two member steps first, and the step that is
        about the whole configuration last, because it needs the two members
        it is computed from to be values it can multiply.
        """
        _ = stderr_file
        return [MemberValidationStep(member_names=['job_name'],
                                     validator=NoSpacesValidator()),
                MemberValidationStep(member_names=['retries'],
                                     validator=_at_most(MOST_RETRIES)),
                MemberValidationStep(member_names=['timeout_seconds'],
                                     validator=_at_most(LONGEST_TIMEOUT)),
                WholeConfigValidationStep(validator=_run_length())]


def _at_most(largest: int) -> IntFloatValidator[int]:
    """Return a validator that refuses a whole number above one limit."""
    return IntFloatValidator[int](min_value=0, max_value=largest,
                                  allowed_values=None)


def longest_run(config: Config, stderr_file: TextIO) -> object:
    """Return the longest time one run of the job can take, in seconds.

    This is the projector of the whole-configuration rule. It receives the
    complete configuration object, because the value it computes exists in
    neither of the two members it is computed from.

    Args:
        config: The configuration object to compute the value from.
        stderr_file: Stream used for user-facing diagnostics, unused here.

    Returns:
        The timeout multiplied by the number of attempts.
    """
    _ = stderr_file
    assert isinstance(config, ValidatedConfig)
    return (config.retries + 1) * config.timeout_seconds


def _run_length() -> ProjectedWholeConfigValidator:
    """Return the rule about how long a whole run of the job may take.

    The pseudo-member name is what the message calls the computed value, and
    it is worth choosing well: it is the only thing the user has to go on,
    because there is no field on the screen that this value belongs to.
    """
    return ProjectedWholeConfigValidator(projector=longest_run,
                                         pseudo_member_name='longest run',
                                         validators=[_at_most(LONGEST_RUN)])


DESCRIPTIONS: Descriptions = {
    ('job_name',): 'Name of the job, without spaces in it.',
    ('retries',): ('How many further attempts one failed run gets. From 0 '
                   f'to {MOST_RETRIES}.'),
    ('timeout_seconds',): ('How long one attempt may take, in seconds. From '
                           f'0 to {LONGEST_TIMEOUT}. All the attempts '
                           f'together may take {LONGEST_RUN} seconds.')}
"""What this application says about the members it declares.

The last of the three is where the rule about the whole configuration is
explained, because a rule that is about no single member still has to be
explained at a member: the user reads the description of a field while they
are changing it, and a sentence below the buttons is read after the mistake.
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
    run_example(example_name='e04_validated_config', args=args,
                config=ValidatedConfig(), descriptions=DESCRIPTIONS)


# The usual guard, so that importing this module from a test runs nothing.
if __name__ == '__main__':
    # Running a file directly puts only that file's own folder on sys.path,
    # so the `example` package this file belongs to would not be importable.
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    main()
