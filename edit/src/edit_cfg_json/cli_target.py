#! /usr/bin/env python3
"""What one command line says is to be edited, and how it is reached.

**The class is told and never guessed.** `--module` names an importable
module, `--file` names a Python file that is not, and `--edit-settings` says
that the class is this library's own settings. Exactly one of the three is
required, which is what makes them one group of `argparse` rather than a check
written by hand; a single `module:Class` argument reads well and would have to
guess which of them it was given, which is what section 8.2.1 of
`doc/design.md` settled for this library as a whole.

**What to edit is then either a class or a loader**, and `--class` and
`--loader` name them in the module or file that was reached. At least one of
the two is needed and both are allowed: a class alone is constructed on the
values it declares, a loader alone is asked for a configuration and its class
is whatever it answers with, and the two together mean that the loader has to
answer with that class or the program stops.

**Importing a module runs it.** That is the same exposure as running the file
with Python, and it is not guarded against, because a guard could only be a
pretence: a configuration class is Python and reaching it means importing the
module it is in.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from argparse import Namespace
from collections.abc import Mapping
from io import StringIO
from pathlib import Path
from types import ModuleType
from typing import NamedTuple, Optional
import importlib
import sys
from config_as_json import Config
from edit_cfg_json.descriptions import Descriptions
from edit_cfg_json.exit_code import ExitCode, Refusal
from edit_cfg_json.loader import ConfigLoader, ask_loader
from edit_cfg_json.loading import DEFAULTS_ERRORS, ConfigLoadError, \
    default_config
from edit_cfg_json.settings_config import SETTINGS_DESCRIPTIONS, SettingsConfig

PYTHON_SUFFIX = '.py'
"""File name extension of the files that the `--file` door accepts."""

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

NO_TARGET_MESSAGE = ('Name the class to edit with --class, or a loader that '
                     'constructs it with --loader, or both.')
"""Message of the refusal of a command line that says what to edit nowhere.

`argparse` cannot be asked for at least one of two options, only for exactly
one of them, and either alone is a perfectly good command line here.
"""

OWN_TARGET_MESSAGE = ('--edit-settings says which class to edit and what it '
                      'says about its own members, so {names} cannot be '
                      'given beside it.')
"""Message of the refusal of a class named beside the editor's own class.

`argparse` refuses `--module` and `--file` beside it, because the three of them
are the one place a class comes from. The three that name something inside such
a module cannot be in that group, because they are not alternatives to it, so
this is the refusal that is written by hand.
"""

NOT_LOADER_MESSAGE = '{module}.{name} cannot be called, so it is no loader.'
"""Message of the refusal of a `--loader` that names something else."""

LOADER_ARGS_MESSAGE = (
    'Loader {name} cannot be called by this program: it needs arguments that '
    'a command line cannot supply. Bind them where the loader is written, for '
    'example with functools.partial, so that what is left is the four keyword '
    'arguments of edit_cfg_json.ConfigLoader.')
"""Message of the refusal of a loader whose own arguments are not bound."""

NO_LOADER_CONFIG = ('Loader {name} did not construct a configuration to '
                    'edit.')
"""Message of the refusal of a loader that refused to answer at all.

The editor asks a loader for a configuration with no JSON source, which is what
`edit_cfg_json.ConfigLoader` says a loader answers. A loader that chooses its
class by looking at the JSON has to name the class it uses for a configuration
that does not exist yet, and this is the refusal of one that names none.
"""

WRONG_CLASS_MESSAGE = ('Loader {name} constructed {other} and not {wanted}, '
                       'which --class asked for.')
"""Message of the refusal of a loader that answered with another class.

A loader may choose its class by looking at the JSON, and `--class` beside it
is how a script says which class it is prepared to go on with. The check is
what `isinstance` answers, so a loader that answers with a subclass of the
class that was named is accepted.
"""

NOT_DESCRIPTIONS = ('{module}.{name} is no mapping, so it says nothing about '
                    'any member.')
"""Message of the refusal of a `--descriptions` that names something else.

What the keys and the values of the mapping are is not checked, for the reason
section 4.3 of `doc/design.md` gives: a selector that addresses no member of
this configuration is simply never used, and a wrong description is a cosmetic
mistake that is not worth refusing to open an editor over.
"""

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


def explained(message: str, error: Exception, captured: str = '') -> str:
    """Return one refusal with what Python said about it below it.

    Args:
        message: What the program has to tell the user.
        error: The failure that Python reported.
        captured: What the code that failed wrote to its own diagnostics
            stream, empty when it wrote nothing or was given none.

    Returns:
        The message, whatever was said, and the failure below both.
    """
    parts = (message, captured.strip(), f'{type(error).__name__}: {error}')
    return '\n'.join(part for part in parts if part)


def _imported_module(name: str) -> ModuleType:
    """Return one importable module, or refuse to run.

    Args:
        name: Name of the module, as an import statement would write it.

    Returns:
        That module, imported.

    Raises:
        Refusal: The module cannot be imported.
    """
    try:
        return importlib.import_module(name)
    except ImportError as error:
        raise Refusal(explained(NO_MODULE_MESSAGE.format(name=name), error),
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
        Refusal: The path is no Python file to import.
    """
    if not path.is_file():
        raise Refusal(NO_FILE_MESSAGE.format(name=path), ExitCode.NO_FILE)
    if path.suffix != PYTHON_SUFFIX:
        raise Refusal(NOT_PYTHON_MESSAGE.format(name=path),
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
        Refusal: The file cannot be imported.
    """
    saved_path = list(sys.path)
    was_imported = path.stem in sys.modules
    sys.path.insert(0, str(path.parent.resolve()))
    try:
        return importlib.import_module(path.stem)
    except SyntaxError as error:
        raise Refusal(explained(NOT_PYTHON_MESSAGE.format(name=path), error),
                      ExitCode.NOT_PYTHON) from error
    except ImportError as error:
        raise Refusal(explained(NOT_IMPORTABLE_MESSAGE.format(name=path),
                                error), ExitCode.NOT_IMPORTABLE) from error
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
        Refusal: The module holds no such class.
    """
    found = getattr(module, name, None)
    if found is None:
        raise Refusal(NO_NAME_MESSAGE.format(module=module.__name__,
                                             name=name), ExitCode.NO_NAME)
    if not isinstance(found, type) or not issubclass(found, Config):
        raise Refusal(NOT_CONFIG_MESSAGE.format(module=module.__name__,
                                                name=name),
                      ExitCode.NOT_CONFIG)
    return found


def _loader_in(module: ModuleType, name: str) -> ConfigLoader:
    """Return one configuration loader of one module, or refuse to run.

    What can be checked here is that the name can be called at all. Whether it
    takes the four keyword arguments of a loader is answered by calling it,
    which is what `_loader_config` below does and reports.

    Args:
        module: Module that was named on the command line.
        name: Name of the loader that was asked for.

    Returns:
        That loader.

    Raises:
        Refusal: The module holds no such name, or it is nothing to call.
    """
    found = getattr(module, name, None)
    if found is None:
        raise Refusal(NO_NAME_MESSAGE.format(module=module.__name__,
                                             name=name), ExitCode.NO_NAME)
    if not isinstance(found, ConfigLoader):
        raise Refusal(NOT_LOADER_MESSAGE.format(module=module.__name__,
                                                name=name),
                      ExitCode.NOT_LOADER)
    return found


def _descriptions_in(module: ModuleType,
                     name: Optional[str]) -> Optional[Descriptions]:
    """Return what one module says about the members of its configuration.

    Args:
        module: Module that was named on the command line.
        name: Name of the mapping that was asked for, or None when the command
            line named none and the members explain themselves as far as their
            own types allow.

    Returns:
        That mapping, or None when none was asked for.

    Raises:
        Refusal: The module holds no such name, or it is no mapping.
    """
    if name is None:
        return None
    found = getattr(module, name, None)
    if found is None:
        raise Refusal(NO_NAME_MESSAGE.format(module=module.__name__,
                                             name=name), ExitCode.NO_NAME)
    if not isinstance(found, Mapping):
        raise Refusal(NOT_DESCRIPTIONS.format(module=module.__name__,
                                              name=name),
                      ExitCode.NOT_DESCRIPTIONS)
    return found


def _named_module(parsed: Namespace) -> ModuleType:
    """Return the module that one command line names, or refuse to run.

    Args:
        parsed: Parsed command line of one run.

    Returns:
        That module, imported.

    Raises:
        Refusal: The module cannot be reached.
    """
    if parsed.module is not None:
        return _imported_module(parsed.module)
    return _module_from_file(_python_file(Path(parsed.file)))


def _constructed(config_type: type[Config]) -> Config:
    """Return the declared defaults of one class, or refuse to run.

    Args:
        config_type: Class that the command line named.

    Returns:
        A configuration object holding what the class declares.

    Raises:
        Refusal: The editor cannot construct that class. An application
            whose class needs constructor arguments this library knows
            nothing about names a loader with `--loader` instead.
    """
    try:
        return default_config(config_type)
    except ConfigLoadError as error:
        raise Refusal(str(error), ExitCode.NO_DEFAULTS) from error


def _loader_config(loader: ConfigLoader, name: str) -> Config:
    """Return what one loader answers with when there is no file, or refuse.

    Args:
        loader: Loader that the command line named.
        name: Name it was named under, which is what a refusal says.

    Returns:
        The configuration object that the loader constructed.

    Raises:
        Refusal: The loader cannot be called by a program, or it answered
            with nothing.
    """
    said = StringIO()
    try:
        return ask_loader(loader, stream=said)
    except TypeError as error:
        raise Refusal(explained(LOADER_ARGS_MESSAGE.format(name=name), error),
                      ExitCode.LOADER_ARGS) from error
    except DEFAULTS_ERRORS as error:
        raise Refusal(explained(NO_LOADER_CONFIG.format(name=name), error,
                                said.getvalue()),
                      ExitCode.NO_DEFAULTS) from error


def _target_config(wanted: Optional[type[Config]],
                   loader: Optional[ConfigLoader],
                   name: Optional[str]) -> Config:
    """Return the configuration object that one command line starts from.

    A class alone is constructed on the values it declares. A loader is asked
    instead, with no JSON source, which is what `ConfigLoader` says a loader
    answers. Which class that is is not checked here, because it is not settled
    yet: a loader may choose its class by looking at the input file, and the
    class of the session is the class of the object the load produced.

    Args:
        wanted: Class that `--class` named, or None when it named none. It is
            never None when there is no loader, because a command line that
            names neither is refused before this.
        loader: Loader that the command line named, or None when it named
            none.
        name: Name the loader was named under, which a refusal says.

    Returns:
        The configuration object to start the session from.

    Raises:
        Refusal: There is no configuration object to edit.
    """
    if loader is None:
        assert wanted is not None
        return _constructed(wanted)
    assert name is not None
    return _loader_config(loader=loader, name=name)


def checked_class(config: Config, wanted: Optional[type[Config]],
                  name: Optional[str]) -> None:
    """Refuse a loaded configuration that is not the class that was asked for.

    `--class` beside a `--loader` is a question rather than an instruction: is
    this the class you are prepared to go on with? It is asked of the object
    that is really going to be edited, so a loader that chose its class by
    looking at the input file is answered for that file. `isinstance` is what
    answers it, so a subclass of the class that was named is accepted.

    Args:
        config: Configuration object that the load produced.
        wanted: Class that `--class` named, or None when it named none.
        name: Name of the loader, or None when the command line named none
            and there is therefore nothing to check.

    Raises:
        Refusal: The class is not the one that was asked for.
    """
    if wanted is None or name is None or isinstance(config, wanted):
        return
    raise Refusal(WRONG_CLASS_MESSAGE.format(name=name,
                                             other=type(config).__name__,
                                             wanted=wanted.__name__),
                  ExitCode.WRONG_CLASS)


class Target(NamedTuple):
    """What one command line said is to be edited, and what explains it.

    The two doors to it answer with the same four things: the object to start
    from, what its application says about its members, and the loader and the
    class that a save and a load are checked against where the command line
    named them.
    """

    config: Config
    """Configuration object holding the values to start from."""

    descriptions: Optional[Descriptions]
    """What the application says about its own members, or None."""

    loader: Optional[ConfigLoader] = None
    """Loader the command line named, or None when it named none."""

    wanted: Optional[type[Config]] = None
    """Class that `--class` named, or None when it named none."""


def _own_target() -> Target:
    """Return the settings class of this editor as what to edit.

    Returns:
        The declared settings of the editor, and what this library says about
        each of them.

    Raises:
        Refusal: The editor cannot construct its own settings class, which
            would be a defect of this library rather than of the command line.
    """
    return Target(config=_constructed(SettingsConfig),
                  descriptions=SETTINGS_DESCRIPTIONS)


def _named_target(parsed: Namespace) -> Target:
    """Return what a command line naming a module or a file says to edit.

    Args:
        parsed: Parsed command line of one run.

    Returns:
        The object to start from, and what says what about it.

    Raises:
        Refusal: The module, the class, the loader or the descriptions
            cannot be reached.
    """
    module = _named_module(parsed)
    loader = None if parsed.loader is None \
        else _loader_in(module=module, name=parsed.loader)
    wanted = None if parsed.class_name is None \
        else _class_in(module=module, name=parsed.class_name)
    return Target(config=_target_config(wanted=wanted, loader=loader,
                                        name=parsed.loader),
                  descriptions=_descriptions_in(module=module,
                                                name=parsed.descriptions),
                  loader=loader, wanted=wanted)


def target_of(parsed: Namespace) -> Target:
    """Return what one command line says is to be edited.

    Args:
        parsed: Parsed command line of one run.

    Returns:
        The object to start from, and what says what about it.

    Raises:
        Refusal: There is no configuration object to edit.
    """
    return _own_target() if parsed.edit_settings else _named_target(parsed)
