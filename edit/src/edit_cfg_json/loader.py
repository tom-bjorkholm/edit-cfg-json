#! /usr/bin/env python3
"""How the application says that its configuration is constructed.

Most applications say nothing: their configuration class takes the keyword
arguments that `config_as_json` documents, and the editor constructs it from
the signature it reads. An application whose class needs an argument this
library knows nothing about — a folder, a connection, the list of names its own
validators accept — has to say so, and a loader is how it says it.

**The signature of a loader is closed.** The editor passes the four things it
owns, all of them keyword arguments, and everything else is bound before the
callable reaches the editor, with a closure or `functools.partial`. That is
what keeps this protocol from growing a parameter for every application that
has one: what the editor does not know about is not the editor's to pass.

What a loader is not asked for is the hook that records what reading an old
format file changed. `Config` gives every configuration object one of its own,
and `Config.auto_change_hook` is where the editor reads it, so a loader that
was never told about it reports exactly as much as one that was.

**A loader answers a call with no JSON source**, with the configuration that
class uses when there is no file yet. The editor asks for that when it is
started on the declared values rather than on a file, so a loader that chooses
its class by looking at the JSON has to name the class it uses for a
configuration that does not exist yet.

**The class is chosen when the file is loaded.** A loader that returns
different classes for different files is supported, and this is the rule that
makes it work: the model is built on the object the load produced, and the
session then edits that class. Nothing asks the loader again while the user
types, because the rows, the descriptions and the marks are that one class's.
What a save does ask is whether the file it is about to write would still be
read as the class being edited, which is where a value that selects another
class is caught.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from collections.abc import Callable
from typing import NamedTuple, Optional, Protocol, TextIO, runtime_checkable
import sys
from config_as_json import Config, PathOrStr
from edit_cfg_json.constructing import built_config

NO_FILE_NAME = ('The editor reads its own input files, so this loader takes '
                'JSON text and not a file name.')
"""Message of the refusal of a file name given to a derived loader."""

LOADER_EXITED = ('The loader of this application ended the program instead of '
                 'saying what was wrong with the values it was given.')
"""Message of a loader that raised `SystemExit` rather than an exception.

Ending the process is never the right answer inside an editor: it costs the
user the whole session. `config_as_json` does it in more than one place, so a
loader written around one of those does it too, and `ask_loader` is where it
becomes a refusal like any other.
"""


@runtime_checkable
class ConfigLoader(Protocol):  # pylint: disable=too-few-public-methods
    """Construct the application's configuration object for the editor.

    This is `config_as_json.ConfigFactory` with one parameter added and one
    left out, so a factory an application already has is nearly one of these.
    The one that is added is the thing a load has to be told and a
    construction does not: whether the declared defaults may fill in what the
    file leaves out. The one left out is `member_name`, which says where a
    nested object is, because what a loader is asked for is the whole
    configuration and that is a member of nothing.

    It is checkable at runtime because a program of this library is told the
    name of one on a command line, and a name that turns out to be something
    else has to be refused rather than called. What that check can see is that
    the object can be called at all; whether it takes these four keyword
    arguments is answered by calling it.
    """

    def __call__(self, *, from_json_data_text: Optional[str] = None,
                 from_json_filename: Optional[PathOrStr] = None,
                 ok_to_use_defaults: bool = False,
                 stderr_file: TextIO = sys.stderr) -> Config:
        """Construct one configuration object from the given JSON source.

        Args:
            from_json_data_text: JSON text to apply, or None for the values
                that the configuration class declares.
            from_json_filename: File to read. The editor reads its own input
                files and never passes this, and it is here so that a callable
                written for `config_as_json` fits without being rewritten.
            ok_to_use_defaults: Whether the declared defaults may fill in the
                members that the JSON text does not hold.
            stderr_file: Stream used for user-facing diagnostics.

        Returns:
            One configuration object holding the values of that source.
        """
        raise NotImplementedError


def derived_loader(factory: Callable[..., Config]) -> ConfigLoader:
    """Return a loader that constructs one configuration with one callable.

    This is what the editor does for a class it is given no loader for, offered
    to an application that needs the same thing with an argument of its own
    bound into it:

    ````python
    loader = derived_loader(partial(TeamConfig, KNOWN_TEAMS))
    ````

    The callable is asked for a configuration holding its declared values, and
    the JSON text is then applied with `Config.parse_json`. Constructing and
    parsing are two steps because the load policy belongs to the second of
    them: `Config.__init__` takes no `ok_to_use_defaults` at all.

    A loader written by hand is the door for anything this cannot express, and
    a class chosen by looking at the JSON is what that means in practice.

    Args:
        factory: Class to construct, or a callable that constructs it with
            arguments of its own already bound.

    Returns:
        A loader for that callable, which satisfies `ConfigLoader`.
    """
    def load(*, from_json_data_text: Optional[str] = None,
             from_json_filename: Optional[PathOrStr] = None,
             ok_to_use_defaults: bool = False,
             stderr_file: TextIO = sys.stderr) -> Config:
        """Construct the configuration and apply the JSON text to it.

        Raises:
            ValueError: A file name was given. It is refused rather than
                quietly ignored, because a caller that named a file means to
                have it read.
        """
        if from_json_filename is not None:
            raise ValueError(NO_FILE_NAME)
        config = built_config(factory, stream=stderr_file)
        if from_json_data_text is not None:
            config.parse_json(from_json_text=from_json_data_text,
                              ok_to_use_defaults=ok_to_use_defaults,
                              stderr_file=stderr_file)
        return config
    return load


def ask_loader(loader: ConfigLoader, *, stream: TextIO,
               text: Optional[str] = None,
               ok_to_use_defaults: bool = False) -> Config:
    """Ask one loader for one configuration object of this application.

    Every call the editor makes to a loader goes through here, so that a loader
    that ends the process is turned into a refusal in one place rather than in
    four. It becomes a `ValueError`, which is what every caller already reports
    as values the configuration class would not accept.

    Args:
        loader: How this application constructs its configuration.
        stream: Stream that collects what the loader says.
        text: JSON text to apply, or None for the declared values.
        ok_to_use_defaults: Whether the declared defaults may fill in what the
            text does not hold.

    Returns:
        The configuration object that the loader made.

    Raises:
        ValueError: The loader ended the program, or refused the values.
        KeyError: The keys of the text do not match the declared members.
        TypeError: The loader cannot construct the configuration this way.
        AttributeError: The class declares no public member at all.
    """
    try:
        return loader(from_json_data_text=text,
                      ok_to_use_defaults=ok_to_use_defaults,
                      stderr_file=stream)
    except SystemExit as error:
        raise ValueError(LOADER_EXITED) from error


class ConfigSource(NamedTuple):
    """The configuration of one session, and how it is constructed.

    The two belong together because each of them answers what the other cannot.
    The object says which class is being edited and is what an edit buffer is
    applied to; the loader is how a further object of that class is made, which
    only reading a file needs and only an application can say.
    """

    config: Config
    """An object of the class being edited, which is never modified."""

    loader: Optional[ConfigLoader] = None
    """How the application constructs it, None when it did not say.

    None does not mean that nothing can be constructed: it means the class is
    constructed from the signature it declares, which is what almost every
    class allows. It is kept apart from a loader that was given, because a save
    checks what it is about to write against a loader the application named and
    has nothing to check it against otherwise.
    """

    @property
    def config_type(self) -> type[Config]:
        """Return the class of the configuration that is being edited."""
        return type(self.config)

    def made(self, *, stream: TextIO, text: Optional[str] = None,
             ok_to_use_defaults: bool = False) -> Config:
        """Return one configuration object of this session's class.

        Args:
            stream: Stream that collects what the construction says.
            text: JSON text to apply, or None for the declared values.
            ok_to_use_defaults: Whether the declared defaults may fill in what
                the text does not hold.

        Returns:
            The configuration object that was constructed.

        Raises:
            ValueError: The values are ones the configuration refuses.
            KeyError: The keys of the text do not match the declared members.
            TypeError: The configuration cannot be constructed this way.
            AttributeError: The class declares no public member at all.
        """
        loader = self.loader if self.loader is not None \
            else derived_loader(self.config_type)
        return ask_loader(loader, stream=stream, text=text,
                          ok_to_use_defaults=ok_to_use_defaults)
