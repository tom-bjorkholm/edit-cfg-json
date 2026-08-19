#! /usr/bin/env python3
"""What the application around the editor has already decided.

The editor does not run on its own. It runs inside an application that made
decisions before the editor was ever called: which key combinations its own
user interface has taken, and what a configuration file of that application
is called. This module is how the application says so, and it is what the
editor consults instead of deciding those things for itself.

Every attribute has a default, so an application with no opinion passes
nothing at all and gets what the editor would have chosen anyway.

Where it is the person running the application who decides rather than the
application, the same answers are `edit_cfg_json.SettingsConfig`, which is a
configuration class of their own and can be read from a file. Both classes here
stay frozen: what the editor is given it has no business changing, and the one
thing that would have wanted them unfrozen — bridging them into a `Config` —
turns out to be impossible for a reason of its own. See `settings_config`.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from collections.abc import Callable
from dataclasses import dataclass, fields
from pathlib import Path
from typing import NamedTuple, Optional
from config_as_json import PathOrStr

DUPLICATE_KEY = 'Key combination {key} is set for both {first} and {second}.'
"""Message of the refusal of one key combination given to two actions."""

NOT_AN_EXTENSION = '{value} is not a file name extension.'
"""Message of the refusal of an extension setting that names none."""

NOT_A_SUFFIX = '{value} is not a backup file name suffix.'
"""Message of the refusal of a backup suffix that names no file of its own."""

NOT_A_COUNT = '{value} is not a number of backup files to keep.'
"""Message of the refusal of a backup count that keeps no file at all.

Keeping no backup is what an empty `backup_suffix` says, and saying it twice
would leave two answers that could disagree with each other.
"""

MIN_BACKUPS = 1
"""Fewest backup files that `backup_count` may ask for."""


def names_a_file(value: str) -> bool:
    """Return whether one piece of text adds anything to a file name.

    Text that does not is neither an extension nor a backup suffix: a name
    with it added would be the name it was added to, so the file it stands for
    would be the file it was made from.

    Args:
        value: Text that is to be added to a file name.

    Returns:
        Whether adding it makes another name.
    """
    return bool(value.strip('.').strip())


def with_dot(extension: str) -> str:
    """Return one file name extension beginning with its dot.

    Args:
        extension: Extension as it was written, with or without its dot.

    Returns:
        That extension with a dot in front of it, so that `cfg` and `.cfg`
        mean the same thing.
    """
    return extension if extension.startswith('.') else f'.{extension}'


BACKUP_SUFFIX = '.bak'
"""What is added to the name of a file whose previous content is kept.

It is added to the whole name rather than put in place of the extension, so
that a configuration called `xx.cfg` is kept as `xx.cfg.bak` and the name still
says what kind of file it was. That is also what lets one attribute express
every shape an application may want, `.old` and `~` among them.
"""

WRONG_EXTENSION = ('File {name} does not have the {extension} extension '
                   'that this application uses for its configuration.')
"""Message of the refusal of a file name an enforced extension forbids."""


def _duplicate(key: str, first: str, second: str) -> ValueError:
    """Return the refusal of one key combination given to two actions.

    Args:
        key: The combination that both of them hold.
        first: Name of the action that was seen holding it first.
        second: Name of the other action that holds it.

    Returns:
        The failure to raise where the settings were built.
    """
    return ValueError(DUPLICATE_KEY.format(key=key, first=first,
                                           second=second))


# One attribute per action of the editor, which is what section 9.1 of
# doc/design.md asks for: an action the application says nothing about keeps
# the default of its own attribute, so there is no merge rule to explain, and
# a misspelled action name is refused where the mistake was made. That is what
# makes the count of these more than pylint's default.
@dataclass(frozen=True)
class ActionSettings:  # pylint: disable=too-many-instance-attributes
    """The key combinations of every action of the editor.

    One attribute per action, so that an action the application says nothing
    about keeps the default of its own attribute and there is no merge rule
    to explain, and so that a misspelled action name is refused where the
    mistake was made rather than becoming a setting nobody reads.

    Each attribute holds every combination that runs its action. The first
    of them is the one a footer or a menu names, and the rest work without
    being named, because naming one action twice would suggest that they
    were two actions. An empty tuple takes the key away and not the action:
    a button and a command palette entry reach it whatever the keys say.

    Combinations are written the way Textual names keys, in lower case: the
    modifiers `ctrl`, `shift`, `alt` and `meta` joined with `+`, and then a
    single character, `f1` to `f12`, or a name such as `escape`, `enter`,
    `tab`, `space`, `backspace`, `delete`, `insert`, `home`, `end`,
    `pageup`, `pagedown`, `up`, `down`, `left` or `right`. The Tk backend
    translates them into the notation of its own toolkit, and leaves an
    action it cannot translate without that key rather than without a
    button.
    """

    quit: tuple[str, ...] = ('ctrl+q',)
    """Keys that end the editor.

    Quitting writes nothing of its own. It is the "cancel" of this design;
    saving leaves the editor open, and what has been saved has been saved.

    A single unmodified letter cannot be used for this or for any other
    action here, now that the value of a member is edited in a field: an
    unmodified letter belongs to whichever field has the focus, and a user
    who typed it would expect to see it appear.
    """

    validate: tuple[str, ...] = ('ctrl+r', 'f5')
    """Keys that ask the application what it makes of these values.

    `ctrl+r` because a field claims most of the other control letters:
    Textual's `Input` already reads `ctrl+a`, `ctrl+c`, `ctrl+d`, `ctrl+e`,
    `ctrl+k`, `ctrl+u`, `ctrl+v`, `ctrl+w` and `ctrl+x`, and the terminal
    itself claims `ctrl+c` and the four that are Backspace, Tab, Return and
    Escape. Of what is left, `r` is the one that means something: re-check.

    `f5` because a function key is what other editors use to ask a tool to
    check what has been written. It is the second of the two, so it works
    without being named, which is what it deserves: a function key is the
    one of the two that a keyboard or a terminal is most likely not to
    deliver.
    """

    save: tuple[str, ...] = ('ctrl+s',)
    """Keys that write the output file.

    The key every application uses for this, and it does reach a terminal
    application: Textual's driver clears `IXON` and `IXOFF` when it puts the
    terminal into raw mode, so neither `ctrl+s` nor `ctrl+q` is taken for
    flow control any more.
    """

    save_as: tuple[str, ...] = ('ctrl+shift+s', 'f12')
    """Keys that choose an output file and then write it.

    The key every application uses for this as well, but unlike the one
    above it is not delivered everywhere. A legacy terminal encodes a
    control letter as a single byte with nowhere to put the shift, so this
    combination arrives as the save key and the wrong action runs. That is
    why the action is offered without a key as well.

    `f12` because a function key is what other editors use to ask a tool to
    write the output file. It is the second of the two, so it works without
    being named, which is what it deserves: a function key is the one of the
    two that a keyboard or a terminal is most likely not to deliver.
    """

    cancel: tuple[str, ...] = ('escape',)
    """Keys that leave a question of the editor unanswered.

    The question about the output file is the only one so far. The Tk
    backend binds nothing for this, because the only question it asks is the
    toolkit's own file dialog, which answers this key itself.
    """

    explain: tuple[str, ...] = ('f1', 'ctrl+g')
    """Keys that show or hide what the application says about the values.

    `f1` because a function key is what asks for help everywhere else, and
    because it is free: of the keys an editor would want, a field claims most
    of the control letters and the application itself claims the rest.

    `ctrl+g` because a terminal or a keyboard that does not deliver a function
    key would otherwise leave this action to the button and the command
    palette. It is one of the few control letters that Textual's own field
    does not read for itself.
    """

    fold: tuple[str, ...] = ('f2', 'ctrl+t')
    """Keys that fold every list and dict away, or open every one of them.

    One action for all of them and not one per container: a container is
    folded and opened where it is, with a control on its own row, and what a
    key is worth is getting the whole configuration back at once.

    `f2` because it is the function key beside the one that explains, and the
    two actions are the same kind of thing: both of them decide how much of
    the configuration is on the screen.

    `ctrl+t` for the same reason `explain` has a control letter as well, which
    is a terminal or a keyboard that does not deliver a function key, and `t`
    because the tree is what this action is about. It is deliberately not
    `ctrl+f`, which is the `find` action below.

    An application whose configuration has no list and no dict in it is never
    offered this action at all, because there would be nothing for it to do.
    """

    find: tuple[str, ...] = ('ctrl+f',)
    """Keys that put the cursor in the field a search is typed into.

    `ctrl+f` because it is what opens a search everywhere else, and it was kept
    free from the first version of this editor for exactly this action: an
    action added later is an added attribute here and breaks no application,
    but a *key* that moved would break every user who had learnt it, and no
    version number protects a habit.

    It puts the cursor in the field rather than asking a question, because the
    field is part of the editor and stays: a user who has found one member and
    wants another comes back to text that is already there.
    """

    find_next: tuple[str, ...] = ('f3',)
    """Keys that go to the next node the search reaches.

    `f3` because it is what finds the next one everywhere else, and it was kept
    free for this action beside `ctrl+f` and for the same reason.

    A function key is the one a keyboard or a terminal is most likely not to
    deliver, and this action is reached without it in both backends: this one
    is the whole tuple rather than the second of two because the control
    letters a field does not claim are spoken for, and because the button and
    the command palette entry are what an action without its key still has.
    """

    def __post_init__(self) -> None:
        """Refuse one key combination that two actions would both run.

        Only one of the two can ever run, which one it is depends on the
        toolkit, and the symptom is an action that mysteriously does
        nothing. The case of a combination is ignored here, because it is
        ignored where the combination is used.

        Raises:
            ValueError: Two actions hold the same key combination.
        """
        taken: dict[str, str] = {}
        for field in fields(self):
            keys: tuple[str, ...] = getattr(self, field.name)
            for key in keys:
                first = taken.setdefault(key.lower(), field.name)
                if first != field.name:
                    raise _duplicate(key=key, first=first, second=field.name)


@dataclass(frozen=True)
class Settings:
    """What the application around the editor has already decided.

    Which keys its own user interface has taken and how hard the editor may
    hold them, what one of its configuration files is called, and how the file
    that is about to be overwritten is looked after. The last of those is the
    application's for the same reason as the others: whether an old
    configuration is worth keeping, and under what name, is something an
    application knows about its own files and the editor cannot find out.

    Both this class and `ActionSettings` are frozen: the editor is given
    what an application decided and has no business changing it.
    """

    actions: ActionSettings = ActionSettings()
    """The key combinations of every action of the editor."""

    file_extension: Optional[str] = None
    """What a configuration file of this application is called, or None.

    None is no opinion, and it is the default: some applications use `.cfg`,
    some use `.json`, and others use something else again. A value is
    normalized to begin with a dot, so `cfg` and `.cfg` mean the same thing.
    """

    extension_enforced: bool = False
    """Whether a file name with another extension is refused.

    It says nothing at all while `file_extension` is None, because there is
    then no extension to enforce.
    """

    backup_suffix: Optional[str] = BACKUP_SUFFIX
    """What the file that is about to be overwritten is kept as, or None.

    It is added to the whole file name, so `.bak` keeps `xx.cfg` as
    `xx.cfg.bak`, `.old` keeps it as `xx.cfg.old` and `~` keeps it as
    `xx.cfg~`. It is taken exactly as it is given, unlike `file_extension`,
    because a suffix that is not an extension is one of the shapes an
    application may want.

    None keeps nothing, for an application that looks after its own files in
    some other way. The default keeps one, because overwriting a file the user
    has not written in this session is the one moment at which the previous
    content is about to stop existing, and an editor that has it in its hands
    is the cheapest place there will ever be to keep it.
    """

    backup_count: int = 1
    """How many of them are kept, the newest first.

    One is kept under the plain name that `backup_suffix` gives, because a
    number in it would say that there are others when there are not. Two or
    more are numbered from `_1`, which is the file that was overwritten last,
    and each save moves every one of them one number further back until the
    oldest falls off the end.
    """

    priority_keys: bool = True
    """Whether the keys of the editor are offered the key press first.

    True is what an editor that owns its window wants: a key of the editor is
    acted on before the field that has the focus is offered it, so that the
    action runs wherever the user was typing. It is also what an editor
    mounted in an application's own window wants most of the time, because
    the keys of such an editor reach only the part of the window the editor
    was given.

    False is for an application that has already taken one of these
    combinations for a widget of its own inside that part. The widget with
    the focus is then offered the key first and the editor gets what is left
    of it, which is the other way of answering the question that emptying one
    tuple of `ActionSettings` answers by taking the key away altogether.
    """

    confirm_overwrite: bool = True
    """Whether the user is asked before an existing file is overwritten.

    They are asked once per destination per session, at the same moment as the
    previous content would be kept, because that is the moment at which the
    file on disk stops being what it was. A session that has already written
    that file is not asked again: it is the user's own earlier save that is
    being overwritten, and asking about it would be asking about nothing.

    The two interactive editors put the question. A backend that prints once
    and returns has nobody to answer it and writes what it was asked to write,
    which is the same answer such a backend gives to the question about
    closing.
    """

    def __post_init__(self) -> None:
        """Normalize the extension, and refuse what names no file at all.

        Raises:
            ValueError: The extension or the backup suffix is text that names
                no file, or fewer than one backup is to be kept.
        """
        self._normalize_extension()
        self._check_backups()

    def _normalize_extension(self) -> None:
        """Add the dot of the extension, and refuse text that is not one.

        The dot is added here rather than everywhere the extension is read,
        so that every user of a `Settings` sees one form of it. Writing to a
        frozen instance is what normalizing in place costs, and it is done
        the one way a frozen dataclass allows.

        Raises:
            ValueError: The extension is text that names no extension.
        """
        extension = self.file_extension
        if extension is None:
            return
        if not names_a_file(extension):
            raise ValueError(NOT_AN_EXTENSION.format(value=repr(extension)))
        object.__setattr__(self, 'file_extension', with_dot(extension))

    def _check_backups(self) -> None:
        """Refuse a suffix that names no file and a count that keeps none.

        The suffix is not normalized in any way, because a suffix that begins
        with a dot and one that does not are both shapes an application asks
        for. What it may not be is text that adds nothing to a name, since the
        backup would then be the file it was made from.

        Raises:
            ValueError: The suffix names no file, or the count is below one.
        """
        suffix = self.backup_suffix
        if suffix is not None and not names_a_file(suffix):
            raise ValueError(NOT_A_SUFFIX.format(value=repr(suffix)))
        if self.backup_count < MIN_BACKUPS:
            raise ValueError(NOT_A_COUNT.format(value=self.backup_count))


type SettingsSource = Settings | Callable[[], Settings]
"""The settings of the application, or a way to ask for them.

A callable is asked again at each point where the answer is used, which is
what an application gets for passing one. What that can change is worth
knowing exactly: the key combinations are read once, when a backend builds
its bindings, and the file name settings are read at every save and at every
choice of a destination. The gain that matters is neither of those, but that
an application need not have its settings ready at the moment it calls: a
model can be built long before the editor is shown, and a callable defers
the answer to the moment it is used.
"""


def current_settings(source: SettingsSource) -> Settings:
    """Return the settings of the application as they are now.

    Args:
        source: The settings, or a callable that answers with them.

    Returns:
        The settings to use for what is about to be done.
    """
    return source() if callable(source) else source


class CheckedFile(NamedTuple):
    """One file name as the settings of the application leave it."""

    name: PathOrStr
    """The file to use, which is the given name unless an extension was
    added to it."""

    message: str
    """Why this file cannot be used, empty when it can be."""


def _matches(name: PathOrStr, extension: str) -> bool:
    """Return whether one file name already has one extension.

    The comparison ignores the case of both, because the file systems of
    Windows and of macOS do not distinguish it either, and refusing `.CFG`
    while accepting `.cfg` would be a difference that the file the name
    stands for does not make.

    Args:
        name: File name to look at.
        extension: Extension of the application, beginning with its dot.

    Returns:
        Whether the name ends with that extension.
    """
    return Path(name).suffix.lower() == extension.lower()


def _refused(name: PathOrStr, extension: str) -> CheckedFile:
    """Return the refusal of one file name an extension forbids.

    Args:
        name: File name that the application cannot use.
        extension: Extension that this application enforces.

    Returns:
        That name, and why it cannot be used.
    """
    return CheckedFile(name=name,
                       message=WRONG_EXTENSION.format(name=name,
                                                      extension=extension))


def checked_file(name: PathOrStr, settings: Settings) -> CheckedFile:
    """Return one file name, or say why this application cannot use it.

    The name is never changed here. An extension that is a default says
    nothing about a name that already exists, and an extension that is
    enforced can only refuse one: opening or overwriting a different file
    because two names differ by an extension would be a surprise, and a
    surprise about which file was written is the expensive kind.

    Args:
        name: File the editor was asked to read or to write.
        settings: What the application has decided about file names.

    Returns:
        That name, and why it cannot be used when it cannot.
    """
    extension = settings.file_extension
    if extension is None or not settings.extension_enforced:
        return CheckedFile(name=name, message='')
    if _matches(name=name, extension=extension):
        return CheckedFile(name=name, message='')
    return _refused(name=name, extension=extension)


def chosen_file(name: PathOrStr, settings: Settings) -> CheckedFile:
    """Return one newly chosen destination, with the extension it needs.

    A name that has no extension at all gets the one the application uses,
    because a destination that is being chosen does not name a file that
    exists yet and completing it is a service rather than a substitution.
    Everything else is what `checked_file` makes of it.

    This is for a destination the user or the application chooses while the
    editor runs. A destination that was inherited, which is the input file
    when the caller named no output file, is only checked and never
    completed.

    Args:
        name: File the user or the application has just chosen to write.
        settings: What the application has decided about file names.

    Returns:
        The name to write, and why it cannot be used when it cannot.
    """
    extension = settings.file_extension
    if extension is not None and not Path(name).suffix:
        return checked_file(name=f'{name}{extension}', settings=settings)
    return checked_file(name=name, settings=settings)
