#! /usr/bin/env python3
"""What one run of a program of this library ends with.

The numbers are part of what the programs promise, so they are written down in
one place that everything reporting one reads, and `Refusal` is how a refusal
carries its number out to the one place that prints it.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from enum import IntEnum


class ExitCode(IntEnum):
    """What one run of a program of this library says about how it went.

    A program of this library is meant to be usable from a script and from a
    continuous integration job, so each way of refusing has a number of its
    own rather than sharing one. The numbers are part of what the programs
    promise, so an added way of refusing gets an added number and no existing
    one changes.
    """

    OK = 0
    """Everything the program was asked to do was done."""

    LOAD_REFUSED = 1
    """The input file cannot be opened for editing."""

    USAGE = 2
    """The command line itself is wrong.

    It is `argparse` that reports this and ends the process, so `run_cli`
    never returns it. The number is written down here because it is part of
    the same promise as the rest, and because the tests compare against it.
    """

    NO_MODULE = 3
    """The module that `--module` names cannot be imported."""

    NO_FILE = 4
    """The file that `--file` names cannot be read."""

    NOT_PYTHON = 5
    """The file that `--file` names is not Python that can be imported."""

    NOT_IMPORTABLE = 6
    """The file needs the package it belongs to in order to be imported."""

    NO_NAME = 7
    """The module does not hold the name that was asked for."""

    NOT_CONFIG = 8
    """That name is not a class based on `config_as_json.Config`."""

    NO_DEFAULTS = 9
    """The editor cannot construct that configuration class on its own."""

    INVALID = 10
    """The configuration is not one that the application would accept.

    This is what makes a program with no user interface a check that a script
    or a continuous integration job can run: a file the application would
    refuse is a failure of the run and not merely a remark in the output.
    """

    NOT_WRITTEN = 11
    """The output file was asked for and was not written.

    The values were valid, so what stopped the writing is the destination: a
    name that was not given at all, one the application does not use for its
    configuration, or a file that cannot be written.
    """

    NOT_SHOWABLE = 12
    """The values of that configuration class cannot be written as JSON.

    There is then nothing to edit at all: the editor reads what it shows by
    serializing the configuration object.
    """

    NOT_LOADER = 13
    """The name that `--loader` names cannot be called at all."""

    LOADER_ARGS = 14
    """The loader needs arguments that a command line cannot supply.

    A loader takes the four keyword arguments of `ConfigLoader` and nothing
    else, so whatever it needs besides them is bound where it is written. A
    program cannot bind an argument it knows nothing about, and saying so
    plainly is better than a half answer.
    """

    WRONG_CLASS = 15
    """The loader did not construct the class that `--class` asked for."""

    NOT_DESCRIPTIONS = 16
    """The name that `--descriptions` names is no mapping of any kind."""

    NO_SETTINGS = 17
    """The settings of the program itself cannot be read.

    A file that `-c/--cfg` or the environment named is not there, or the file
    the lookup found does not hold settings of this editor. Running with other
    settings than the ones that were asked for is what this number exists to
    stop, because a user who named a settings file wants that one.
    """


class Refusal(Exception):
    """Refusal to run, with what to say about it and what to exit with.

    It is internal to this package because it exists only to carry the two
    together from wherever the refusal is decided out to the one place that
    reports it.
    """

    def __init__(self, message: str, code: ExitCode) -> None:
        """Say why the program cannot run and how it should end.

        Args:
            message: What the user has to be told.
            code: What this run of the program ends with.
        """
        self.message = message
        self.code = code
        super().__init__(message)
