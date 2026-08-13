#! /usr/bin/env python3
"""Command line handling shared by all example programs.

The examples in this repository teach how an application hands its own
configuration object to `edit_cfg_json`. They are not about command line
parsing, so the parsing lives here once and every example reuses it. That
keeps each example file about the shape of a configuration instead of about
`argparse`.

One required option decides which user interface the example is shown in:

| `--ui` value | What it does                                     |
| ------------ | ------------------------------------------------ |
| `tk`         | opens the Tkinter editor in a window             |
| `textual`    | opens the Textual editor in the terminal         |
| `dump`       | prints the model once, non-interactively         |

**The first two are the editors, and they are what every example is really
about.** An example teaches what the user sees and does: which control is
pressed, what appears below which member, what changes when a field loses the
focus. Reading an example and then running it with `--ui tk` or
`--ui textual` is the intended way round.

**`--ui dump` is a very limited non-interactive user interface**, and it is
not the way to see what the editor does. It is `edit_cfg_json.DumpEditor`,
which prints the model once and returns: there is no field to type into, no
control to press, no focus to lose and nobody to answer a question. What it
is genuinely good for is the two things a non-interactive backend can do —
exercising a feature over the core and backend API without a display, which is
what the tests of these examples do, and printing what a short sequence of
editor actions left behind. The command lines below stand in for those
actions, so every example can be checked from a script and on a machine with
no display, and that is the whole of what a printout is evidence of.

The three are one option rather than a switch beside two, because they are
alternatives: there is no situation in which one run should both open a
window and print the model. Making them one option also means that `argparse`
itself refuses a missing or an unknown choice, so this module needs no hand
written check for either.

`StandInUser` below is the other kind of backend: one written by hand, in a
few lines, for this repository's own purposes. Between it and `DumpEditor`
they say what a backend really is — anything with a `run_editor` method.

The repeatable `--set member=value` option edits the buffer before anything
is shown. What it stands in for is a user typing into a field, which is where
an example's editing really happens; making the same edit from a command line
is what lets it be reached without a display. A member the user changed is
marked, so the edit is visible even when the new value looks like the old one.

A value inside a list or a dict is named by the whole path to it, with a dot
between the steps: `--set retry_delays.0=3` and `--set ports.http=8080`. A
member of the configuration has one step and is written as its own name,
which is what every example before the lists and dicts one does. The one
thing this notation cannot address is a dictionary key that holds a dot; such
a key is edited in the editor like any other.

`--fold PATH` folds one list or dict away, or opens it again if it is folded
already, in the same way that pressing its control in a window does.
`--toggle-fold` stands in for the key that folds every one of them, and is
repeatable because a key is.

`--add PATH` puts one more element into a list, and `--add PATH=KEY` puts one
more entry into a dict, which needs a key because nothing but the person
configuring the application knows what a new entry is called. `--remove PATH`
takes one element out again, and `--move PATH=up` and `--move PATH=down` make
one element of a list change places with a neighbour. All four stand in for
pressing the control on that row, and all four are applied before `--set`, so
that a value inside a new element can be typed into in the same run.

`-i/--input` names the file that the values are read from, and `--policy`
says what to do about a declared value that the file does not hold. There is
a file for every case in [examples/data/](../../data/), including the ones
that cannot be opened, so each of them can be tried without writing a file
first. A file that cannot be opened is a message and an exit, and never an
editor that quietly shows the default values instead of what was asked for.

`-o/--output` names the file that is written, and defaults to the input file,
which is what an editor is normally asked to do. With neither, there is
nowhere to write, and the two interactive backends ask for a destination when
Save is pressed.

An example that has something to say about the members it declares hands a
description mapping to `run_example`, which passes it on to `edit()`. There is
no command line option for that, because it is not the kind of thing a command
line could supply: it is what the application knows about its own
configuration, and the editor has no way of finding it out.

An example whose configuration class the editor cannot construct on its own
hands over a loader in the same way, and for the same reason: what that class
needs besides the JSON is the application's to know. There is no command line
option for that either — the two examples that have one build it in Python,
where the argument that has to be bound is.

`--toggle-explain` stands in for the key that shows or hides the explanatory
text, in the same way that `--set` stands in for a user typing into a field. It
is a key, so it can be pressed more than once: the editor starts with the
explanations shown, one of these hides them — the label of the configuration
keeps its one line summary, and the rest of the class docstring and the
description of every member go away — and two of them show them again.

A validation pass is asked for in the two editors, with a button or with a
key, because a user who is halfway through typing a value has not asked
anything yet. `--ui dump` has no later moment in which to be asked, so it
validates once before it prints — which is what having no user does to the
question, and not a second opinion about when a buffer should be validated.

`--save` is the one option that only means something for `--ui dump`, for the
same reason: the printout happens once and the run is then over, so there is
no moment at which a user could press Save. Without `--save` it says where it
would write, and with it the file is really written, which is what puts a
round trip within reach of a script. It is repeatable, because Save is a
button and a key: two of them are two presses in one session, which is what
shows that the file a save keeps is kept once and not once per press.

A save that writes over a file this session did not write keeps what that file
held, under the name the application chose, and says where it went. The two
editors ask before they do it; `--ui dump` has nobody to ask and writes, which
is the same answer a printout gives to the question about closing.

`--extension`, `--enforce-extension` and `--key` stand in for the
application the editor runs inside. A real application does not parse these
from a command line: it knows its own answers and builds one
`edit_cfg_json.Settings` from them. They are options here so that every
answer can be tried without writing a program per answer.

An example that has decided something about its own files hands over a
`Settings` object of its own instead, which is what a real application does,
and the three options above then fill in the parts they name and leave the
rest of it alone.

`--key ACTION=COMBINATIONS` names one action of the editor and the key
combinations that run it, separated by commas. `--key save=ctrl+w` moves
Save, and `--key save_as=` takes the key away from Save as altogether and
leaves the action reachable through the button and the command palette. An
action that no `--key` names keeps its default.

The settings are passed here as a `Settings` object, which is what an
application that knows its own answers does. `edit()` also accepts a
callable that answers with a `Settings`, which is worth having when the
answers are not ready at the moment of the call, and is documented at
`edit_cfg_json.SettingsSource`.

Every run ends by saying what `edit()` gave back, because "the saved object,
or `None` when nothing was saved" is the contract of this library and a
contract is better seen than read.

`embedded_parser` and `session_result` beside `run_example` are for the two
examples that mount the editor in a window an application owns. Those cannot
use `run_example` at all: every option of it is phrased against
`edit_cfg_json.EditorBackend`, and an embedded editor is deliberately not one
— it does not run to completion, so it cannot be handed to `edit()`. What
they share with the rest is the three file options, which are the core's own,
and the one setting that only an embedded editor has a reason to change; what
they say at the end is read from the model, because a widget has no moment at
which it could return anything.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import argparse
from dataclasses import fields, replace
from typing import Optional
from config_as_json import Config
from edit_cfg_json import ActionSettings, ConfigLoadError, ConfigLoader, \
    Descriptions, DumpEditor, EditModel, EditorBackend, Settings, \
    add_file_options, edit, named_policy, text_path

UI_DUMP = 'dump'
"""Value of `--ui` that prints the model instead of opening a window."""

UI_TK = 'tk'
"""Value of `--ui` that opens the Tkinter editor."""

UI_TEXTUAL = 'textual'
"""Value of `--ui` that opens the Textual editor."""

UI_CHOICES = (UI_DUMP, UI_TK, UI_TEXTUAL)
"""Every accepted value of the required `--ui` option."""

DUMP_ONLY_MESSAGE = '--save only means something together with --ui dump.'
"""Message used to refuse `--save` where a Save button or key exists."""

SAVED_MESSAGE = 'edit() returned the saved {name} object.'
"""Message that says the editor handed a written configuration back."""

NOTHING_MESSAGE = 'edit() returned None, so nothing was saved.'
"""Message that says the session ended without writing anything."""

SET_FORM_MESSAGE = '--set needs member=value, and got {setting}.'
"""Message used to refuse a `--set` value that names no member."""

NO_MEMBER_MESSAGE = '{name} is not part of this configuration.'
"""Message used to refuse a path that addresses nothing in the model."""

NOT_EDITABLE_MESSAGE = '{name} is not a value that can be edited.'
"""Message used to refuse a `--set` of a node that is not a value.

A list, a dict and a nested configuration object are each edited through the
values inside them, so the path of one of those is not a path `--set` can be
given. Neither is a declared member that holds no configuration object.
"""

NOT_A_CONTAINER_MESSAGE = '{name} is not a list or a dict.'
"""Message used to refuse a `--fold` of something that holds nothing."""

MOVE_FORM_MESSAGE = ('--move needs PATH={up} or PATH={down}, and got '
                     '{value}.')
"""Message used to refuse a `--move` that says no direction."""

MOVE_UP = 'up'
"""What `--move` is told to make an element change places with the one
before it."""

MOVE_DOWN = 'down'
"""What it is told to make it change places with the one after it."""

KEY_FORM_MESSAGE = ('--key needs one of {names} followed by =combinations, '
                    'and got {value}.')
"""Message used to refuse a `--key` that names no action of the editor."""

SESSION_SAVED = 'The session saved a {name} object.'
"""What an example that mounts the editor says about what was written."""

SESSION_NOTHING = 'The session saved nothing.'
"""What it says when the session ended without writing anything."""

ORDINARY_KEYS_HELP = ('Offer the editor a key after the widget that has the '
                      'focus, rather than before it.')
"""What `--ordinary-keys` says it does."""


def embedded_parser(example_name: str) -> argparse.ArgumentParser:
    """Return the command line that the two embedding examples share.

    They cannot use the parser below, because every option of it is phrased
    against `edit_cfg_json.EditorBackend` and an editor mounted in an
    application's own window is deliberately not one: it does not run to
    completion, so it cannot be handed to `edit()` at all. What is left is
    the three file options, which are the core's own and mean here what they
    mean in every program of this library, and the one setting that only an
    embedded editor has a reason to change.

    There is no `--ui`, because each of those two examples is one toolkit,
    and no `--ui dump`, because what they teach is where the editor is in a
    window and a printout has no window to be one part of.

    Args:
        example_name: Name of the example, used in help and error text.

    Returns:
        A parser for `--ordinary-keys`, `--policy`, `-i/--input` and
        `-o/--output`.
    """
    parser = argparse.ArgumentParser(prog=example_name)
    parser.add_argument('--ordinary-keys', action='store_true',
                        help=ORDINARY_KEYS_HELP)
    add_file_options(parser)
    return parser


def session_result(saved: Optional[Config]) -> str:
    """Return what one embedded editing session gave back, as a line.

    An editor mounted in a window an application owns has no moment at which
    it could return anything, so what the application reads is
    `edit_cfg_json.EditModel.saved_config`. This is how the two examples that
    do that say what they found there.

    Args:
        saved: What the model of the session holds as its saved object.

    Returns:
        A line naming the saved configuration class, or saying there is none.
    """
    if saved is None:
        return SESSION_NOTHING
    return SESSION_SAVED.format(name=type(saved).__name__)


def _create_parser(example_name: str) -> argparse.ArgumentParser:
    """Return the argument parser that all example programs share.

    Args:
        example_name: Name of the example, used in help and error text.

    Returns:
        A parser for `--ui`, `--set`, `--add`, `--remove`, `--move`,
        `--toggle-explain`, `--toggle-fold`, `--fold`, `--policy`, `--save`,
        `--extension`, `--enforce-extension`, `--key`, `-i/--input` and
        `-o/--output`.
    """
    # The last three of those are added by the core, in `add_file_options`,
    # because the programs the core installs have the very same three options
    # and they have to mean the same thing here as they do there.
    parser = argparse.ArgumentParser(prog=example_name)
    parser.add_argument('--ui', required=True, choices=UI_CHOICES,
                        help='How to show the configuration.')
    parser.add_argument('--set', action='append', dest='edits',
                        metavar='MEMBER=VALUE',
                        help='Edit one member before showing it. Repeatable.')
    parser.add_argument('--toggle-explain', action='count', default=0,
                        help='Press the explain key. Repeatable, as a key '
                             'is.')
    parser.add_argument('--toggle-fold', action='count', default=0,
                        help='Press the fold key. Repeatable, as a key is.')
    parser.add_argument('--fold', action='append', dest='folds',
                        metavar='PATH',
                        help='Fold or open one list or dict. Repeatable.')
    parser.add_argument('--add', action='append', dest='adds',
                        metavar='PATH[=KEY]',
                        help='Add one element or entry. Repeatable.')
    parser.add_argument('--remove', action='append', dest='removes',
                        metavar='PATH',
                        help='Remove one element or entry. Repeatable.')
    parser.add_argument('--move', action='append', dest='moves',
                        metavar='PATH=up|down',
                        help='Move one element of a list. Repeatable.')
    parser.add_argument('--extension', default=None,
                        help='File name extension this application uses.')
    parser.add_argument('--enforce-extension', action='store_true',
                        help='Refuse a file with another extension.')
    parser.add_argument('--key', action='append', dest='keys',
                        metavar='ACTION=COMBINATIONS',
                        help='Keys of one action of the editor. Repeatable.')
    parser.add_argument('--save', action='count', default=0,
                        help='Press Save. Repeatable, as a press is. Only '
                             'with --ui dump.')
    add_file_options(parser)
    return parser


def _refuse_save(parser: argparse.ArgumentParser,
                 parsed: argparse.Namespace) -> None:
    """Refuse `--save` where the user interface has a Save of its own.

    An option that looked as if it worked and quietly did nothing would be
    worse than no option.

    Args:
        parser: Parser used to report the error and exit.
        parsed: Parsed command line of one example run.
    """
    if parsed.save and parsed.ui != UI_DUMP:
        parser.error(DUMP_ONLY_MESSAGE)


def _set_member(parser: argparse.ArgumentParser, model: EditModel, name: str,
                text: str) -> None:
    """Edit one value of the buffer, or say why it cannot be edited.

    The model is addressed by the path of a node, and a value inside a list
    or a dict is named by the whole path to it, with a dot between the steps:
    `retry_delays.0` is the first element of that list and `ports.http` is
    that key of that dict. A member of the configuration is one step and is
    therefore written as its own name, exactly as it was before there were
    lists and dicts to address.

    The model tells the two failures apart, and so does this: a name that
    addresses nothing at all is a different mistake from one that addresses
    something this version of the editor cannot edit.

    Args:
        parser: Parser used to report the error and exit.
        model: Model whose buffer is edited.
        name: Path of the value to edit, with a dot between its steps.
        text: Text to set the value to, exactly as a field would hold it.
    """
    try:
        model.set_text(path=text_path(name), text=text)
    except KeyError:
        parser.error(NO_MEMBER_MESSAGE.format(name=name))
    except ValueError:
        parser.error(NOT_EDITABLE_MESSAGE.format(name=name))


def _apply_edits(parser: argparse.ArgumentParser, model: EditModel,
                 edits: Optional[list[str]]) -> None:
    """Apply every `--set member=value` of one command line to the buffer.

    Args:
        parser: Parser used to report the error and exit.
        model: Model whose buffer is edited.
        edits: The `--set` values, or None when the option was not used.
    """
    for setting in edits or []:
        name, separator, text = setting.partition('=')
        if not separator:
            parser.error(SET_FORM_MESSAGE.format(setting=setting))
        _set_member(parser=parser, model=model, name=name, text=text)


def _apply_adds(parser: argparse.ArgumentParser, model: EditModel,
                adds: Optional[list[str]]) -> None:
    """Put one more element into every node that one command line names.

    A list is named on its own and a dict is named with the key of the new
    entry after an equals sign, because a new entry of a dict has to be
    called something and nothing but the person configuring the application
    knows what. It is the same notation as `--set`, for the same reason: what
    follows the equals sign is what the user would have typed.

    Args:
        parser: Parser used to report the error and exit.
        model: Model whose buffer is edited.
        adds: The `--add` values, or None when the option was not used.
    """
    for value in adds or []:
        name, _, key = value.partition('=')
        try:
            model.add_element(path=text_path(name), key=key)
        except KeyError:
            parser.error(NO_MEMBER_MESSAGE.format(name=name))
        except ValueError as error:
            parser.error(str(error))


def _apply_removes(parser: argparse.ArgumentParser, model: EditModel,
                   removes: Optional[list[str]]) -> None:
    """Take one element out of what holds it, for every name of one run.

    Args:
        parser: Parser used to report the error and exit.
        model: Model whose buffer is edited.
        removes: The `--remove` values, or None when unused.
    """
    for name in removes or []:
        try:
            model.remove_element(text_path(name))
        except KeyError:
            parser.error(NO_MEMBER_MESSAGE.format(name=name))
        except ValueError as error:
            parser.error(str(error))


def _apply_moves(parser: argparse.ArgumentParser, model: EditModel,
                 moves: Optional[list[str]]) -> None:
    """Move one element of a list by one place, for every name of one run.

    Args:
        parser: Parser used to report the error and exit.
        model: Model whose buffer is edited.
        moves: The `--move` values, or None when the option was not used.
    """
    for value in moves or []:
        name, separator, direction = value.partition('=')
        if not separator or direction not in (MOVE_UP, MOVE_DOWN):
            parser.error(MOVE_FORM_MESSAGE.format(value=value, up=MOVE_UP,
                                                  down=MOVE_DOWN))
        try:
            model.move_element(path=text_path(name),
                               later=direction == MOVE_DOWN)
        except KeyError:
            parser.error(NO_MEMBER_MESSAGE.format(name=name))
        except ValueError as error:
            parser.error(str(error))


def _apply_folds(parser: argparse.ArgumentParser, model: EditModel,
                 folds: Optional[list[str]]) -> None:
    """Fold away every container that one command line names.

    Args:
        parser: Parser used to report the error and exit.
        model: Model whose containers are folded.
        folds: The `--fold` values, or None when the option was not used.
    """
    for name in folds or []:
        try:
            model.toggle_fold(text_path(name))
        except KeyError:
            parser.error(NO_MEMBER_MESSAGE.format(name=name))
        except ValueError:
            parser.error(NOT_A_CONTAINER_MESSAGE.format(name=name))


def _action_keys(parser: argparse.ArgumentParser, values: Optional[list[str]],
                 given: ActionSettings) -> ActionSettings:
    """Return the key combinations that every `--key` of one run asks for.

    The names that are accepted are the attributes of `ActionSettings`
    itself, so this cannot fall behind the actions the editor has.

    Args:
        parser: Parser used to report the error and exit.
        values: The `--key` values, or None when the option was not used.
        given: What the example itself decided about the keys.

    Returns:
        The keys of every action, with what the example decided for each
        action the command line said nothing about.
    """
    names = {field.name for field in fields(ActionSettings)}
    chosen: dict[str, tuple[str, ...]] = {}
    for value in values or []:
        name, separator, keys = value.partition('=')
        if not separator or name not in names:
            parser.error(KEY_FORM_MESSAGE.format(
                value=value, names=', '.join(sorted(names))))
        chosen[name] = tuple(key for key in keys.split(',') if key)
    try:
        actions = replace(given, **chosen)
    except ValueError as error:
        # `parser.error` writes the message and ends the process, so nothing
        # below this runs when two actions were given the same key.
        parser.error(str(error))
    return actions


def _settings(parser: argparse.ArgumentParser, parsed: argparse.Namespace,
              given: Settings) -> Settings:
    """Return what this run says the application has already decided.

    A real application does not build this from a command line. It knows
    its own answers, and either passes one object like this one or a
    callable that answers with one. That is what `given` is: an example that
    has decided something about its own files says so in Python, and each
    option here fills in the one thing it names and leaves the rest of it.

    Args:
        parser: Parser used to report the error and exit.
        parsed: Parsed command line of one example run.
        given: What the example itself decided, which is nothing at all for
            an example that has no opinion about keys or about files.

    Returns:
        The settings that this run hands to the editor.
    """
    try:
        settings = replace(
            given,
            actions=_action_keys(parser=parser, values=parsed.keys,
                                 given=given.actions),
            file_extension=parsed.extension or given.file_extension,
            extension_enforced=(parsed.enforce_extension
                                or given.extension_enforced))
    except ValueError as error:
        # `parser.error` writes the message and ends the process, so nothing
        # below this runs when the extension is text that names none.
        parser.error(str(error))
    return settings


class StandInUser:  # pylint: disable=too-few-public-methods
    """A backend that does what a user would, and then runs another one.

    What it does belongs on this side of `edit()` rather than before it,
    because `edit()` owns the model: it reads the file and builds the model
    itself, which is what gives a load its policy and its change reporting.
    `--set` stands in for a user typing, `--add`, `--remove` and `--move` for a
    user pressing the controls of a row, `--toggle-explain` for a user pressing
    the explain key, and `--save` for a user pressing Save, and every one of
    those happens in an editor that is already open.

    How many elements there are is changed before anything is typed, so that a
    value inside a new element can be set in the same run. That is also the
    order a user would work in.

    Saving is here rather than in `DumpEditor` for the same reason as the other
    two: the dump prints the model it is given, and pressing Save is not
    printing. A dump does print once and return, though, so `--save` is the
    only way a user could ever ask it for one, which is why the command line
    accepts the option for `--ui dump` alone. It presses Save once per time it
    was given, because a second press of Save is a thing a user does and does
    not do the same as the first: the file it would write over is the one the
    first press wrote.
    """

    def __init__(self, inner: EditorBackend, parser: argparse.ArgumentParser,
                 parsed: argparse.Namespace) -> None:
        """Remember what to do to the model and what to run afterwards.

        Args:
            inner: Backend that shows the model once it has been edited.
            parser: Parser used to report a bad `--set` and exit.
            parsed: Parsed command line of one example run.
        """
        self._inner = inner
        self._parser = parser
        self._parsed = parsed

    def run_editor(self, model: EditModel) -> None:
        """Act as the user would, and hand the model to the real backend.

        Args:
            model: Model to edit and then to show.
        """
        _apply_adds(parser=self._parser, model=model, adds=self._parsed.adds)
        _apply_removes(parser=self._parser, model=model,
                       removes=self._parsed.removes)
        _apply_moves(parser=self._parser, model=model,
                     moves=self._parsed.moves)
        _apply_edits(parser=self._parser, model=model,
                     edits=self._parsed.edits)
        for _ in range(self._parsed.toggle_explain):
            model.toggle_explanations()
        for _ in range(self._parsed.toggle_fold):
            model.toggle_fold_all()
        _apply_folds(parser=self._parser, model=model,
                     folds=self._parsed.folds)
        for _ in range(self._parsed.save):
            model.save()
        self._inner.run_editor(model)


def _tk_editor() -> EditorBackend:
    """Return the Tkinter backend, imported only when it is needed.

    The import is inside this function on purpose. `tkinter` cannot be
    installed from PyPI, so a machine can have a perfectly good Python
    without it. An example that imported the Tkinter backend at module level
    would then fail even for `--ui textual`.

    Returns:
        A backend that satisfies the `EditorBackend` protocol.
    """
    # pylint: disable-next=import-outside-toplevel
    from edit_cfg_json_tk import TkEditor
    return TkEditor()


def _textual_editor() -> EditorBackend:
    """Return the Textual backend, imported only when it is needed.

    Returns:
        A backend that satisfies the `EditorBackend` protocol.
    """
    # pylint: disable-next=import-outside-toplevel
    from edit_cfg_json_textual import TextualEditor
    return TextualEditor()


def _selected_backend(parsed: argparse.Namespace) -> EditorBackend:
    """Return the backend that the `--ui` value of one run asks for.

    Args:
        parsed: Parsed command line of one example run.

    Returns:
        A backend that satisfies the `EditorBackend` protocol.
    """
    if parsed.ui == UI_DUMP:
        return DumpEditor()
    return _tk_editor() if parsed.ui == UI_TK else _textual_editor()


def _result_text(saved: Optional[Config]) -> str:
    """Return what one editing session gave back, as a line of text.

    Args:
        saved: What `edit()` returned.

    Returns:
        A line naming the saved configuration class, or saying there is none.
    """
    if saved is None:
        return NOTHING_MESSAGE
    return SAVED_MESSAGE.format(name=type(saved).__name__)


# One argument per thing that an example hands over, which is what makes this
# the whole of what an application does. See the same disable on `edit` in the
# core, which these arguments are passed on to.
# pylint: disable-next=too-many-arguments
def _run_editor(*, parser: argparse.ArgumentParser, config: Config,
                backend: EditorBackend, parsed: argparse.Namespace,
                descriptions: Optional[Descriptions],
                loader: Optional[ConfigLoader],
                settings: Settings) -> Optional[Config]:
    """Run one editing session, or say why the input file cannot be opened.

    This is the whole of what an application does: it hands over its own
    configuration object, what it says about the members of it, how that
    object is constructed when the editor cannot work it out for itself, the
    files it wants read and written, the policy it wants applied, what it has
    already decided about keys and file names, and the user interface to use.
    The editor does the rest, and gives back what it wrote.

    Args:
        parser: Parser used to report the error and exit.
        config: Configuration object of the example. It is not modified.
        backend: User interface to run the session in.
        parsed: Parsed command line of one example run.
        descriptions: What the example says about its members, or None.
        loader: How the example constructs its configuration, or None.
        settings: What the example has already decided about keys and files.

    Returns:
        The configuration object that was saved, or None when the session
        ended without writing anything.
    """
    try:
        saved = edit(config=config, backend=backend, in_file=parsed.input,
                     descriptions=descriptions, loader=loader,
                     out_file=parsed.output,
                     policy=named_policy(parsed.policy),
                     settings=_settings(parser=parser, parsed=parsed,
                                        given=settings))
    except ConfigLoadError as error:
        # `parser.error` writes the message and ends the process, so nothing
        # below this runs when the input file cannot be opened.
        parser.error(str(error))
    return saved


# One argument per thing that an example hands over, which is the whole of
# what an application says about a session. Each of them is an independent
# keyword, as the arguments of `edit` in the core are and for the same reason,
# and that core function carries the same disable.
# pylint: disable-next=too-many-arguments
def run_example(example_name: str, config: Config, *,
                args: Optional[list[str]] = None,
                descriptions: Optional[Descriptions] = None,
                loader: Optional[ConfigLoader] = None,
                settings: Settings = Settings()) -> None:
    """Run one example program from the command line.

    This is the whole contract between an example and this module: the
    example says what it is called, hands over the configuration object it
    wants to edit, says what it has to say about the members of it, says
    how that object is constructed if the editor cannot construct it itself,
    and says what it has already decided about keys and about its own files.

    Args:
        example_name: Name of the example, used in help and error text.
        config: Configuration object that the example wants to edit. The
            editor never modifies it.
        args: Optional replacement for `sys.argv[1:]`, mainly for tests.
        descriptions: What this example says about the members it declares,
            or None for an example that says nothing about them.
        loader: How this example constructs its configuration, or None for a
            class that the editor can construct on its own, which is what
            every example but two is.
        settings: What this example has already decided about the keys of the
            editor and about the files it reads and writes. The default is an
            application with no opinion, which is what every example but one
            is; the command line then fills in what its own options name.
    """
    parser = _create_parser(example_name)
    parsed = parser.parse_args(args)
    _refuse_save(parser=parser, parsed=parsed)
    backend = StandInUser(inner=_selected_backend(parsed), parser=parser,
                          parsed=parsed)
    print(_result_text(_run_editor(parser=parser, config=config,
                                   backend=backend, parsed=parsed,
                                   descriptions=descriptions, loader=loader,
                                   settings=settings)))
