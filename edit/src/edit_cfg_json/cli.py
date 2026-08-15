#! /usr/bin/env python3
"""The command line of a program that edits any configuration class.

An application author should get an editor for their own configuration class
without writing a line of user interface code, and every one of the three
distributions therefore ships a program. What differs between the three
programs is the backend and nothing else, so everything else lives here: the
parsing, one editing session and the exit code. Each package is then a program
of a few statements, which is also what makes this testable with no display and
no toolkit, by handing `run_cli` a backend that is a stub.

`run_cli` takes the backend for exactly the reason `edit` does: this package
never imports a user interface library, so it cannot name one.

**Where the class comes from is `edit_cfg_json.cli_target`**, which owns the
three doors to it — an importable module, a Python file, and this library's own
settings class — and the class, the loader and the descriptions that are named
inside the first two. What every one of them ends with is a `Target`, so this
module is about a session and not about where its configuration came from.

**What settings the program itself runs with is a different question**, and
`-c/--cfg` is the first of the five answers that
`edit_cfg_json.settings_file` gives to it. The settings of a program are read
before anything else the command line names, because they are what the whole
run behaves according to.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from argparse import ArgumentParser, Namespace
from collections.abc import Mapping, Sequence
from typing import Optional
import sys
import argcomplete
from edit_cfg_json.backend import EditorBackend
from edit_cfg_json.cli_target import NOT_SHOWABLE_MESSAGE, NO_TARGET_MESSAGE, \
    OWN_TARGET_MESSAGE, Target, checked_class, explained, target_of
from edit_cfg_json.edit_model import EditModel
from edit_cfg_json.exit_code import ExitCode, Refusal
from edit_cfg_json.loading import DEFAULT_POLICY, ConfigLoadError, \
    LoadPolicy, load_config
from edit_cfg_json.settings import Settings
from edit_cfg_json.settings_file import load_settings

DESCRIPTION = ('Edit one config_as_json configuration class, without '
               'writing a program for it.')
"""What the program says about itself above its own options."""

POLICY_NAMES: Mapping[str, LoadPolicy] = {
    'strict': LoadPolicy.STRICT,
    'defaults': LoadPolicy.DEFAULTS,
    'strict-then-defaults': LoadPolicy.STRICT_THEN_DEFAULTS}
"""What a `--policy` value on a command line means to the editor."""


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
    `--unfold` belongs to one for the same reason: a container that would
    flood a window opens folded, and such a program has no control to press
    on it. A program that opens an editor offers neither option at all, so it
    is `argparse` that refuses them rather than a check written by hand; the
    defaults are set instead, so that the rest of this module can read them
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
    where.add_argument('--edit-settings', action='store_true',
                       help='Edit a settings file of this editor itself, '
                            'reading -i and starting from the defaults '
                            'without one.')
    parser.add_argument('-c', '--cfg', default=None, metavar='PATH',
                        help='Settings file that this program itself runs '
                             'with, instead of the one it would look for.')
    parser.add_argument('--class', dest='class_name', default=None,
                        metavar='CLASS',
                        help='Name of the config_as_json.Config class.')
    parser.add_argument('--loader', default=None, metavar='NAME',
                        help='Name of an edit_cfg_json.ConfigLoader there, '
                             'for a class this editor cannot construct.')
    parser.add_argument('--descriptions', default=None, metavar='NAME',
                        help='Name of an edit_cfg_json.Descriptions mapping '
                             'there, saying what the members are for.')
    add_file_options(parser)
    if interactive:
        parser.set_defaults(save=False, unfold=False)
    else:
        parser.add_argument('--save', action='store_true',
                            help='Write the output file, since this program '
                                 'has no Save to press.')
        parser.add_argument('--unfold', action='store_true',
                            help='Show what every folded container holds, '
                                 'since this program has no control to press.')
    return parser


def _built_model(parsed: Namespace, target: Target,
                 settings: Settings) -> EditModel:
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
        target: What is to be edited, and what says what about it.
        settings: What this program itself runs with, which is what its own
            settings file said.

    Returns:
        The model of one editing session.

    Raises:
        Refusal: The input file cannot be opened, the loaded class is not the
            one that was asked for, or the class cannot be shown at all.
    """
    loader = target.loader
    try:
        loaded = load_config(config=target.config, in_file=parsed.input,
                             policy=named_policy(parsed.policy),
                             settings=settings, loader=loader)
    except ConfigLoadError as error:
        raise Refusal(str(error), ExitCode.LOAD_REFUSED) from error
    checked_class(config=loaded.config, wanted=target.wanted,
                  name=parsed.loader)
    try:
        model = EditModel(config=loaded.config, report=loaded.report,
                          descriptions=target.descriptions, loader=loader,
                          out_file=parsed.input, settings=settings)
    except ValueError as error:
        name = type(loaded.config).__name__
        raise Refusal(explained(NOT_SHOWABLE_MESSAGE.format(name=name),
                                error), ExitCode.NOT_SHOWABLE) from error
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


def _own_settings(parsed: Namespace, home_settings: Optional[str]) -> Settings:
    """Return what this program itself runs with, or refuse to run.

    It is read before anything else the command line names, because it is what
    the whole run behaves according to: which keys the editor holds, what its
    files are called and what happens to the file a save writes over.

    Args:
        parsed: Parsed command line of one run.
        home_settings: Name of this program's own settings file in the home
            folder, or None for a program that has none.

    Returns:
        The settings of this program.

    Raises:
        Refusal: A settings file was named and cannot be used.
    """
    try:
        return load_settings(named=parsed.cfg, home_settings=home_settings)
    except ConfigLoadError as error:
        raise Refusal(str(error), ExitCode.NO_SETTINGS) from error


def _session(backend: EditorBackend, parsed: Namespace, interactive: bool,
             home_settings: Optional[str]) -> ExitCode:
    """Run one editing session and return what it says about the run.

    Saving happens before the backend runs, because a program that is asked
    to save has no user to press Save and the backend has to be able to
    report what the save did. Opening every container happens after the save
    and for the same reason, and it is asked for good: the backend of such a
    program validates the buffer before it shows it, and a container that a
    validation pass creates would otherwise be folded away again.

    Args:
        backend: User interface to run this session in.
        parsed: Parsed command line of one run.
        interactive: Whether the backend gives the user a session.
        home_settings: Name of this program's own settings file in the home
            folder, or None for a program that has none.

    Returns:
        What this run of the program ends with.

    Raises:
        Refusal: The session cannot be started.
    """
    settings = _own_settings(parsed=parsed, home_settings=home_settings)
    model = _built_model(parsed=parsed, target=target_of(parsed),
                         settings=settings)
    if parsed.save:
        model.save()
    if parsed.unfold:
        model.open_all(no_more_folding=True)
    backend.run_editor(model)
    return _outcome(model=model, save_asked=parsed.save,
                    interactive=interactive)


def _check_target(parser: ArgumentParser, parsed: Namespace) -> None:
    """Refuse a command line that says what to edit wrongly, or not at all.

    Neither of the two can be asked of `argparse`: it refuses exactly one of a
    group of options and never at least one of them, and the three names below
    are not alternatives to the group they would have to be in.

    Args:
        parser: Parser used to report the refusal and end the process.
        parsed: Parsed command line of one run.

    Raises:
        SystemExit: The command line says what to edit wrongly or not at all.
            That is `parser.error` reporting it, with `ExitCode.USAGE`.
    """
    named = {'--class': parsed.class_name, '--loader': parsed.loader,
             '--descriptions': parsed.descriptions}
    given = sorted(name for name, value in named.items() if value is not None)
    if parsed.edit_settings:
        if given:
            parser.error(OWN_TARGET_MESSAGE.format(names=', '.join(given)))
        return
    if parsed.class_name is None and parsed.loader is None:
        parser.error(NO_TARGET_MESSAGE)


def run_cli(backend: EditorBackend, prog: str, *,
            args: Optional[Sequence[str]] = None, interactive: bool = True,
            home_settings: Optional[str] = None) -> int:
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
            `--save` and `--unfold` and answers with the verdict in its exit
            code, because there is nobody to press Save, nobody to open a
            container that is folded away and nobody to read a verdict.
        home_settings: Name of this program's own settings file in the home
            folder, which is the third step of the lookup that
            `edit_cfg_json.settings_file` makes. None is a program that has
            none of its own and reads the shared file or nothing.

    Returns:
        What this run of the program ends with, as one of `ExitCode`.

    Raises:
        SystemExit: The command line itself is wrong, or help was asked for.
            That is `argparse` reporting it, with `ExitCode.USAGE`.
    """
    parser = _create_parser(prog=prog, interactive=interactive)
    argcomplete.autocomplete(parser)
    parsed = parser.parse_args(args)
    _check_target(parser=parser, parsed=parsed)
    try:
        return _session(backend=backend, parsed=parsed,
                        interactive=interactive, home_settings=home_settings)
    except Refusal as refusal:
        print(refusal.message, file=sys.stderr)
        return refusal.code
