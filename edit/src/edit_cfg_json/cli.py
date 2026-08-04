#! /usr/bin/env python3
"""The command line of a program that edits any configuration class.

An application author should get an editor for their own configuration class
without writing a line of user interface code, and every one of the three
distributions therefore ships a program. What differs between the three
programs is the backend and nothing else, so everything else lives here: the
parsing, the two doors to a class, the construction, one editing session and
the exit code. Each package is then a program of a few statements, which is
also what makes this testable with no display and no toolkit, by handing
`run_cli` a backend that is a stub.

`run_cli` takes the backend for exactly the reason `edit` does: this package
never imports a user interface library, so it cannot name one.

**The class is told and never guessed.** `--module` names an importable module,
`--file` names a Python file that is not, exactly one of the two is required,
and the class is a positional argument. A single `module:Class` argument reads
well and would have to guess which of the two it was given, which is what
section 8.2.1 of `doc/design.md` settled for this library as a whole; it would
also make a Windows drive letter a special case, and it would take the refusal
of a missing or a doubled location away from `argparse`.

**Importing a module runs it.** That is the same exposure as running the file
with Python, and it is not guarded against, because a guard could only be a
pretence: a configuration class is Python and reaching it means importing the
module it is in.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from argparse import ArgumentParser, Namespace
from collections.abc import Mapping, Sequence
from enum import IntEnum
from pathlib import Path
from types import ModuleType
from typing import Optional
import importlib
import sys
from config_as_json import Config
import argcomplete
from edit_cfg_json.backend import EditorBackend
from edit_cfg_json.edit_model import EditModel
from edit_cfg_json.loading import DEFAULT_POLICY, ConfigLoadError, \
    LoadPolicy, default_config, load_config

DESCRIPTION = ('Edit one config_as_json configuration class, without '
               'writing a program for it.')
"""What the program says about itself above its own options."""

PYTHON_SUFFIX = '.py'
"""File name extension of the files that the `--file` door accepts."""

POLICY_NAMES: Mapping[str, LoadPolicy] = {
    'strict': LoadPolicy.STRICT,
    'defaults': LoadPolicy.DEFAULTS,
    'strict-then-defaults': LoadPolicy.STRICT_THEN_DEFAULTS}
"""What a `--policy` value on a command line means to the editor."""

NO_MODULE_MESSAGE = 'Module {name} cannot be imported.'
"""Message of the refusal of a `--module` that names no importable module."""

NO_FILE_MESSAGE = 'File {name} cannot be read.'
"""Message of the refusal of a `--file` that names no readable file."""

NOT_PYTHON_MESSAGE = 'File {name} is not Python that can be imported.'
"""Message of the refusal of a `--file` that Python cannot compile.

It covers both a name that is not a `.py` file at all and a `.py` file that
does not compile, because both mean the same thing to whoever ran the program:
what was named is not a Python module.
"""

NOT_IMPORTABLE_MESSAGE = (
    'File {name} cannot be imported on its own. A file that belongs to a '
    'package, or that needs another folder on the path, has to be named '
    'with --module and PYTHONPATH instead.')
"""Message of the refusal of a file that only its own package can import.

A module that uses a relative import is the case that arises in practice, and
there is nothing a bare path can do about it: the import needs the package
that the module belongs to, and a path names no package.
"""

NO_NAME_MESSAGE = 'Module {module} holds no name {name}.'
"""Message of the refusal of a class name that the module does not hold."""

NOT_CONFIG_MESSAGE = ('{module}.{name} is not a class based on '
                      'config_as_json.Config.')
"""Message of the refusal of a name that is not a configuration class."""

NOT_SHOWABLE_MESSAGE = ('The editor cannot show {name}, because the values '
                        'it holds cannot be written as JSON. A member whose '
                        'value is not a JSON value needs a serialize '
                        'converter of its own before anything can edit it.')
"""Message of the refusal of a class that cannot be turned into a buffer.

The editor reads the values it edits by serializing the configuration object,
so a class that cannot serialize itself has no values to show. A class that
leaves part of its own writing to code outside itself is the case that arises
in practice, and there is nothing the editor can do with one.
"""


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


class _Refusal(Exception):
    """Refusal to run, with what to say about it and what to exit with.

    It is internal because it exists only to carry the two together from
    wherever the refusal is decided out to the one place that reports it.
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


def _default_policy_name() -> str:
    """Return the `--policy` value that the editor uses when none is named.

    It is looked up rather than written out, so that the default of the
    editor stays the one and only source of it.

    Returns:
        The name of the default load policy.
    """
    return next(name for name, policy in POLICY_NAMES.items()
                if policy is DEFAULT_POLICY)


def named_policy(name: str) -> LoadPolicy:
    """Return the load policy that one `--policy` value asks for.

    Args:
        name: One of the values that `add_file_options` accepts.

    Returns:
        What the editor makes of that value.

    Raises:
        KeyError: The name is not one of the accepted values. It cannot come
            from a command line, because `argparse` refuses it first.
    """
    return POLICY_NAMES[name]


def add_file_options(parser: ArgumentParser) -> None:
    """Add the file and policy options that every program of this library has.

    The three of them say the same thing wherever they appear — which file to
    read, which to write, and what to do about a value the file leaves out —
    so they are declared here once rather than per program. The examples of
    this repository use this as well, which is what keeps the one meaning
    from becoming two.

    Args:
        parser: Parser that the options are added to.
    """
    parser.add_argument('--policy', default=_default_policy_name(),
                        choices=tuple(POLICY_NAMES),
                        help='What to do about values the file leaves out.')
    parser.add_argument('-i', '--input', default=None,
                        help='Configuration file to read.')
    parser.add_argument('-o', '--output', default=None,
                        help='Configuration file to write, or the input file.')


def _create_parser(prog: str, interactive: bool) -> ArgumentParser:
    """Return the parser of one program of this library.

    `--save` belongs to a program whose backend prints once and returns,
    because there is then no later moment at which a user could press Save.
    A program that opens an editor does not offer the option at all, so it is
    `argparse` that refuses it rather than a check written by hand; the
    default is set instead, so that the rest of this module can read it
    either way.

    Args:
        prog: Name that this program is installed under.
        interactive: Whether the backend of this program gives the user a
            session in which they could ask for a save themselves.

    Returns:
        The parser for one program.
    """
    parser = ArgumentParser(prog=prog, description=DESCRIPTION)
    where = parser.add_mutually_exclusive_group(required=True)
    where.add_argument('--module', default=None, metavar='MODULE',
                       help='Importable module that holds the class.')
    where.add_argument('--file', default=None, metavar='PATH',
                       help='Python file that holds the class.')
    parser.add_argument('class_name', metavar='CLASS',
                        help='Name of the config_as_json.Config class.')
    add_file_options(parser)
    if interactive:
        parser.set_defaults(save=False)
    else:
        parser.add_argument('--save', action='store_true',
                            help='Write the output file, since this program '
                                 'has no Save to press.')
    return parser


def _said(message: str, error: Exception) -> str:
    """Return one refusal with what Python said about it below it.

    Args:
        message: What the program has to tell the user.
        error: The failure that Python reported.

    Returns:
        The message, and the failure below it.
    """
    return f'{message}\n{type(error).__name__}: {error}'


def _imported_module(name: str) -> ModuleType:
    """Return one importable module, or refuse to run.

    Args:
        name: Name of the module, as an import statement would write it.

    Returns:
        That module, imported.

    Raises:
        _Refusal: The module cannot be imported.
    """
    try:
        return importlib.import_module(name)
    except ImportError as error:
        raise _Refusal(_said(NO_MODULE_MESSAGE.format(name=name), error),
                       ExitCode.NO_MODULE) from error


def _python_file(path: Path) -> Path:
    """Return one path that can be tried as a Python module, or refuse.

    A file that is missing is a different mistake from a file that is not
    Python, so the two are told apart before either of them is imported.

    Args:
        path: Path that `--file` named.

    Returns:
        That path.

    Raises:
        _Refusal: The path is no Python file to import.
    """
    if not path.is_file():
        raise _Refusal(NO_FILE_MESSAGE.format(name=path), ExitCode.NO_FILE)
    if path.suffix != PYTHON_SUFFIX:
        raise _Refusal(NOT_PYTHON_MESSAGE.format(name=path),
                       ExitCode.NOT_PYTHON)
    return path


def _module_from_file(path: Path) -> ModuleType:
    """Return the module of one Python file, and leave no trace of it.

    The folder of the file goes to the front of the path and the file is
    imported by its own stem, so that a module which imports its siblings
    works. Both of those are undone afterwards: the folder is taken off the
    path again, and a module that was not already imported is forgotten, so
    that a second file of the same stem is really imported rather than found
    among the modules of the first. The class that was reached keeps working
    either way, because a class carries the namespace it was defined in.

    Args:
        path: Python file to import, which exists and ends in `.py`.

    Returns:
        That file, imported as a module.

    Raises:
        _Refusal: The file cannot be imported.
    """
    saved_path = list(sys.path)
    was_imported = path.stem in sys.modules
    sys.path.insert(0, str(path.parent.resolve()))
    try:
        return importlib.import_module(path.stem)
    except SyntaxError as error:
        raise _Refusal(_said(NOT_PYTHON_MESSAGE.format(name=path), error),
                       ExitCode.NOT_PYTHON) from error
    except ImportError as error:
        raise _Refusal(_said(NOT_IMPORTABLE_MESSAGE.format(name=path), error),
                       ExitCode.NOT_IMPORTABLE) from error
    finally:
        sys.path[:] = saved_path
        if not was_imported:
            sys.modules.pop(path.stem, None)


def _class_in(module: ModuleType, name: str) -> type[Config]:
    """Return one configuration class of one module, or refuse to run.

    Args:
        module: Module that was named on the command line.
        name: Name of the class that was asked for.

    Returns:
        That class.

    Raises:
        _Refusal: The module holds no such class.
    """
    found = getattr(module, name, None)
    if found is None:
        raise _Refusal(NO_NAME_MESSAGE.format(module=module.__name__,
                                              name=name), ExitCode.NO_NAME)
    if not isinstance(found, type) or not issubclass(found, Config):
        raise _Refusal(NOT_CONFIG_MESSAGE.format(module=module.__name__,
                                                 name=name),
                       ExitCode.NOT_CONFIG)
    return found


def _config_class(parsed: Namespace) -> type[Config]:
    """Return the configuration class that one command line names.

    Args:
        parsed: Parsed command line of one run.

    Returns:
        The class to edit.

    Raises:
        _Refusal: The class cannot be reached.
    """
    if parsed.module is not None:
        module = _imported_module(parsed.module)
    else:
        module = _module_from_file(_python_file(Path(parsed.file)))
    return _class_in(module=module, name=parsed.class_name)


def _constructed(config_type: type[Config]) -> Config:
    """Return the declared defaults of one class, or refuse to run.

    Args:
        config_type: Class that the command line named.

    Returns:
        A configuration object holding what the class declares.

    Raises:
        _Refusal: The editor cannot construct that class. An application
            whose class needs constructor arguments this library knows
            nothing about supplies an explicit loader instead, which is what
            step 9 of the delivery plan is about.
    """
    try:
        return default_config(config_type)
    except ConfigLoadError as error:
        raise _Refusal(str(error), ExitCode.NO_DEFAULTS) from error


def _built_model(parsed: Namespace, config: Config) -> EditModel:
    """Return the model of one session, on the files that were named.

    The output file is set only when it was named, because the model already
    writes the input file when nothing else was chosen. Naming it here counts
    as choosing it, so it gets the extension of the application when it has
    none of its own, exactly as `edit` does with the same argument.

    Building the model serializes the configuration object, which is how the
    editor reads the values it shows, and a class that cannot write itself as
    JSON therefore has nothing for the editor to show. That is the class of a
    configuration and not a mistake on the command line, so it is a refusal
    here rather than the exception that `EditModel` documents for an
    application that builds the model itself and knows its own class.

    Args:
        parsed: Parsed command line of one run.
        config: Configuration object holding the declared defaults.

    Returns:
        The model of one editing session.

    Raises:
        _Refusal: The input file cannot be opened, or the class cannot be
            shown at all.
    """
    try:
        loaded = load_config(config=config, in_file=parsed.input,
                             policy=named_policy(parsed.policy))
    except ConfigLoadError as error:
        raise _Refusal(str(error), ExitCode.LOAD_REFUSED) from error
    try:
        model = EditModel(config=loaded.config, report=loaded.report,
                          out_file=parsed.input)
    except ValueError as error:
        name = type(loaded.config).__name__
        raise _Refusal(_said(NOT_SHOWABLE_MESSAGE.format(name=name), error),
                       ExitCode.NOT_SHOWABLE) from error
    if parsed.output is not None:
        model.set_out_file(parsed.output)
    return model


def _outcome(model: EditModel, save_asked: bool,
             interactive: bool) -> ExitCode:
    """Return what one finished session says about how the run went.

    A session the user was given ends when the user closes it, and closing an
    editor is not a failure whatever is left in the fields. A program that
    printed once has nobody to read a verdict for it, so there the verdict is
    the answer.

    Args:
        model: Model of the session that has just ended.
        save_asked: Whether the run was asked to write the output file.
        interactive: Whether the backend gave the user a session.

    Returns:
        What this run of the program ends with.
    """
    if interactive:
        return ExitCode.OK
    verdict = model.verdict
    if verdict is not None and not verdict.valid:
        return ExitCode.INVALID
    if save_asked and model.saved_config is None:
        return ExitCode.NOT_WRITTEN
    return ExitCode.OK


def _session(backend: EditorBackend, parsed: Namespace,
             interactive: bool) -> ExitCode:
    """Run one editing session and return what it says about the run.

    Saving happens before the backend runs, because a program that is asked
    to save has no user to press Save and the backend has to be able to
    report what the save did.

    Args:
        backend: User interface to run this session in.
        parsed: Parsed command line of one run.
        interactive: Whether the backend gives the user a session.

    Returns:
        What this run of the program ends with.

    Raises:
        _Refusal: The session cannot be started.
    """
    config = _constructed(_config_class(parsed))
    model = _built_model(parsed=parsed, config=config)
    if parsed.save:
        model.save()
    backend.run_editor(model)
    return _outcome(model=model, save_asked=parsed.save,
                    interactive=interactive)


def run_cli(backend: EditorBackend, prog: str, *,
            args: Optional[Sequence[str]] = None,
            interactive: bool = True) -> int:
    """Run one program of this library from the command line.

    This is the whole of what each of the three programs does. The backend is
    the only thing that differs between them, and everything that could be
    written twice is therefore here.

    Args:
        backend: User interface to run the session in. Each package supplies
            its own, which is the one thing this package cannot name.
        prog: Name that this program is installed under, used in its help and
            in its refusals.
        args: Optional replacement for `sys.argv[1:]`, mainly for tests.
        interactive: Whether this backend gives the user a session. A backend
            that prints once and returns does not, so its program offers
            `--save` and answers with the verdict in its exit code, because
            there is nobody to press Save and nobody to read a verdict.

    Returns:
        What this run of the program ends with, as one of `ExitCode`.

    Raises:
        SystemExit: The command line itself is wrong, or help was asked for.
            That is `argparse` reporting it, with `ExitCode.USAGE`.
    """
    parser = _create_parser(prog=prog, interactive=interactive)
    argcomplete.autocomplete(parser)
    parsed = parser.parse_args(args)
    try:
        return _session(backend=backend, parsed=parsed,
                        interactive=interactive)
    except _Refusal as refusal:
        print(refusal.message, file=sys.stderr)
        return refusal.code
