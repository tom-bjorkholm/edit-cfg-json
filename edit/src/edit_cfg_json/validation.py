#! /usr/bin/env python3
"""Running the application's own validation over one edit buffer."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from io import StringIO
from typing import NamedTuple
import json
from config_as_json import Config, JsonType

BUFFER_ERRORS = (KeyError, TypeError, ValueError)
"""Every way in which a configuration class refuses an edit buffer.

`config_as_json` reports a key that is missing or unknown as `KeyError`,
text that is not JSON as `ConfigBadJson`, and a value that a validator
refuses as `InvalidConfiguration`, `InvalidConfigurationValue` or
`InvalidConfigurationType`. Those four are all `ValueError` subclasses, so
these three classes are exactly those failures and nothing besides them.

`NotImplementedError` is deliberately not one of them. It says that the
configuration class is incomplete, which is a defect of the application that
no edit of the buffer can put right, and hiding it in a verdict would send
the user looking for a mistake that is not theirs.
"""


class ValidationVerdict(NamedTuple):
    """What one validation pass over a whole edit buffer found."""

    valid: bool
    """Whether the application itself would accept this buffer."""

    diagnostics: str
    """What the application itself would tell the user about the buffer.

    An accepted buffer can have diagnostics too, because a validator may
    remark on a value without refusing it.
    """


class ValidationPass(NamedTuple):
    """The verdict of one validation pass and what it validated."""

    verdict: ValidationVerdict
    """What the pass found."""

    members: dict[str, JsonType]
    """One JSON space value per member of the accepted configuration.

    A member validator returns the value that is stored back into the
    member, so these are not necessarily the values the pass was given.
    They are empty when the buffer was refused, because there is then no
    configuration object to read them from.
    """


def _refused(captured: str, error: Exception) -> ValidationVerdict:
    """Return the verdict of a pass that the configuration class refused.

    The captured text is what the application itself would have printed, so
    it is what the user is shown. A failure that printed nothing has only
    its exception left to report, which is better than no explanation.

    Args:
        captured: What the candidate wrote to its diagnostics stream.
        error: The failure that the candidate reported.

    Returns:
        A verdict saying that the buffer is not a configuration, and why.
    """
    fallback = f'{type(error).__name__}: {error}'
    return ValidationVerdict(valid=False, diagnostics=captured or fallback)


def validate_buffer(config_type: type[Config],
                    members: dict[str, JsonType]) -> ValidationPass:
    """Validate one edit buffer by constructing a candidate configuration.

    Constructing a configuration object runs the whole chain that the
    application runs when it reads its own file: key matching, the recursive
    check of dict shapes against the defaults, the parse converters, the
    nested configuration objects and then the validation plan. So the user
    sees exactly the diagnostics that the application would produce, there
    is no second implementation of validation anywhere, and there is no way
    for the editor to accept something the application would then refuse.

    The stream the candidate writes to is captured rather than passed on,
    because these diagnostics are the answer to a question the user asked
    and belong on the screen and not in the terminal behind it.

    Args:
        config_type: Class of the configuration that is being edited.
        members: The edit buffer, as one JSON space value per member.

    Returns:
        What the pass found, and the members of the configuration object it
        built. The members are empty when the buffer was refused.
    """
    diagnostics = StringIO()
    try:
        candidate = config_type(from_json_data_text=json.dumps(members),
                                from_json_filename=None,
                                stderr_file=diagnostics)
        validated = json.loads(
            candidate.as_json_string(stderr_file=diagnostics))
    except BUFFER_ERRORS as error:
        return ValidationPass(
            verdict=_refused(captured=diagnostics.getvalue(), error=error),
            members={})
    assert isinstance(validated, dict)
    accepted = ValidationVerdict(valid=True,
                                 diagnostics=diagnostics.getvalue())
    return ValidationPass(verdict=accepted, members=validated)
