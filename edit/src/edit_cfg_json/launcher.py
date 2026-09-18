#! /usr/bin/env python3
# PYTHON_ARGCOMPLETE_OK
"""The `edit-cfg-json` program: the editor this machine can run.

It is the command line of `edit_cfg_json.cli` with no backend written into it.
What editor it opens is found rather than named: every installed package that
supplies a user interface registers one `edit_cfg_json.ui_backend.UiBackend`,
and this opens the best of those that can run here. `--ui` is how one of them
is asked for instead, and its values are the ones this machine can really run.

**This is the name that promises an editor**, which is why the core has
installed no program under it until now and why
`python3 -m edit_cfg_json.dump` is called what it is. Now that the name opens
one, it is also reachable as `python3 -m edit_cfg_json`, exactly as each of
the two editor programs is reachable through its own package.

**The command line is read twice, and `--ui` is why.** Which options the
parser has depends on the editor: a backend that prints once and returns
offers the two options that stand in for what its user cannot do, and an
editor offers neither. So `--ui` and `-c` are read first, on their own, and
the parser the user sees is built once the answer is known. Both readings
declare the option with the same function of `edit_cfg_json.cli`, so there is
one option and not two that could drift apart.

**The settings that decide which editor are the shared ones.** The file of a
program's own in the home folder is read afterwards, by the session, because
which editor is opened cannot be decided by the settings file belonging to one
of them. That first reading says nothing about a file it cannot read either:
the session reads the same file and refuses the run, and one refusal is
enough.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from argparse import ArgumentParser, Namespace
from collections.abc import Sequence
from typing import NamedTuple, Optional
import io
import sys
from edit_cfg_json.backend import EditorBackend
from edit_cfg_json.cli import add_cfg_option, add_ui_option, run_cli
from edit_cfg_json.loading import ConfigLoadError
from edit_cfg_json.settings import Settings
from edit_cfg_json.settings_file import load_settings
from edit_cfg_json.ui_backend import NoEditorError, UiBackend
from edit_cfg_json.ui_choice import available_uis, chosen_ui
from edit_cfg_json.version_report import EcajVersionReporter

PROGRAM = 'edit-cfg-json'
"""Name that this program is installed under."""


def _pre_parsed(args: Optional[Sequence[str]]) -> Namespace:
    """Return the two options that are needed before the parser is built.

    It reads what it knows and leaves the rest, so the command line is not
    judged here at all: a `--ui` naming something that cannot run is left to
    the parser the user sees, which refuses it beside the names that would
    have worked.

    Args:
        args: Command line of one run, or None for the one this process got.

    Returns:
        What that command line says about the user interface and about the
        settings file, each None when it says nothing.
    """
    parser = ArgumentParser(prog=PROGRAM, add_help=False)
    add_ui_option(parser)
    add_cfg_option(parser)
    known, _ = parser.parse_known_args(args)
    return known


def _launcher_settings(named: Optional[str]) -> Settings:
    """Return the settings that decide which editor this run opens.

    They are looked up without the file of any one program in the home
    folder, because a file belonging to one editor cannot be what decides
    that another editor is opened. The session that follows reads them again
    with the file of the editor that was chosen, which is what the keys and
    the file names of that session come from.

    Args:
        named: Settings file that `-c/--cfg` named, or None for none.

    Returns:
        What that file says, or the defaults of the editor.
    """
    try:
        return load_settings(named=named, stderr_file=io.StringIO())
    except ConfigLoadError:
        # A settings file that cannot be used is a refusal of the run, and
        # the session below makes it with the same lookup and the same words.
        # Choosing an editor for a run that is about to be refused costs a
        # probe and says nothing twice.
        return Settings()


def _chosen_or_none(ui_name: Optional[str],
                    settings: Settings) -> Optional[UiBackend]:
    """Return the user interface this run opens, and None where it has none.

    Refusing here would answer `--help` and `--version` with the refusal, and
    those two are what somebody on a machine with no editor needs most.

    Args:
        ui_name: The `--ui` name this run asked for, or None for none.
        settings: What this machine has decided about the editor.

    Returns:
        The user interface to open the editor in, or None when this machine
        has none that this run can be given.
    """
    try:
        return chosen_ui(ui_name=ui_name, settings=settings)
    except NoEditorError:
        return None


class _EditorFacts(NamedTuple):
    """What the shared command line is told about the editor of one run."""

    backend: Optional[EditorBackend]
    """The backend to run the session in, and None where there is none."""

    interactive: bool
    """Whether that backend gives the user a session to press Save in."""

    home_settings: Optional[str]
    """Name of its own settings file in the home folder, or None."""


NO_EDITOR_FACTS = _EditorFacts(backend=None, interactive=True,
                               home_settings=None)
"""What the command line is told where this machine can open no editor.

They leave it what it would be for an editor, because it is refused once it
has been read and what it offers until then is the same either way.
"""


def _facts_of(chosen: Optional[UiBackend]) -> _EditorFacts:
    """Return what the shared command line is told about one chosen editor.

    A backend is made here and not before, because making one before it is
    known which is used would build every user interface of the machine in
    order to open one of them.

    Args:
        chosen: The user interface this run opens, or None for none.

    Returns:
        The three facts, and `NO_EDITOR_FACTS` where there is no editor.
    """
    if chosen is None:
        return NO_EDITOR_FACTS
    return _EditorFacts(backend=chosen.backend(),
                        interactive=chosen.interactive,
                        home_settings=chosen.home_settings)


def main(args: Optional[Sequence[str]] = None) -> int:
    """Run this program and return what it ends with.

    Args:
        args: Optional replacement for `sys.argv[1:]`, mainly for tests.

    Returns:
        What this run ends with, as one of `edit_cfg_json.ExitCode`.
    """
    parsed = _pre_parsed(args)
    settings = _launcher_settings(parsed.cfg)
    available = available_uis(settings)
    chosen = _chosen_or_none(ui_name=parsed.ui, settings=settings)
    facts = _facts_of(chosen)
    return run_cli(backend=facts.backend, prog=PROGRAM, args=args,
                   version_reporter=EcajVersionReporter(),
                   interactive=facts.interactive, ui_choices=available,
                   home_settings=facts.home_settings)


if __name__ == '__main__':  # pragma: no cover
    sys.exit(main())
