#! /usr/bin/env python3
"""Tests for the program that opens the editor this machine can run.

**Nothing here opens a window or a screen**, and what stands in for the
registrations of the two editors is what makes that possible: a made up user
interface answers what a test wants it to answer and its backend shows
nothing. A test that used the real registrations would open whichever editor
the machine the tests run on happens to have.

The other three programs of this repository are one table in
`test_programs.py`, because they differ in the backend and in nothing else.
This one is not in that table: it has no backend of its own, so what it hands
over depends on the machine, and what is worth testing about it is exactly
what the table cannot say.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from pathlib import Path
from typing import Optional
import pytest
from edit_cfg_json import EditModel, ExitCode, UiBackend
from edit_cfg_json.launcher import PROGRAM, main
from edit_cfg_json.ui_choice import NO_EDITOR

CLASS_ARGS = ('--module', 'test_edit_cfg_json.sample_cfg',
              '--class', 'FlatCfg')
"""What says which class to edit, for a run that is to reach the editor."""


class RecordingEditor:  # pylint: disable=too-few-public-methods
    """A backend that records the model it was given and shows nothing."""

    def __init__(self) -> None:
        """Make a backend that has been given nothing yet."""
        self.shown: Optional[EditModel] = None

    def run_editor(self, model: EditModel) -> None:
        """Record the model instead of showing it."""
        self.shown = model


SHOWN: list[RecordingEditor] = []
"""Every backend that a made up user interface has been asked for."""


def _recording() -> RecordingEditor:
    """Return one backend, and remember that it was asked for.

    Returns:
        A backend that records what it is given.
    """
    made = RecordingEditor()
    SHOWN.append(made)
    return made


def made_up(ui_name: str, priority: int, can_run: bool = True,
            interactive: bool = True) -> UiBackend:
    """Return one registration that answers what a test wants it to answer.

    Args:
        ui_name: What `--ui` calls it.
        priority: How good an editor it says it is.
        can_run: What it answers about being able to run here.
        interactive: Whether it says the user gets a session.

    Returns:
        A registration of a user interface that does not exist.
    """
    def answer() -> bool:
        """Answer what this registration was made to answer."""
        return can_run
    return UiBackend(ui_name=ui_name, priority=priority, can_run=answer,
                     backend=_recording, interactive=interactive,
                     home_settings=f'.{ui_name}.cfg')


WINDOW = made_up('window', 10)
"""A registration standing in for the editor of a machine with a display."""

SCREEN = made_up('screen', 5)
"""One standing in for the editor of a machine with a terminal."""

PRINTOUT = made_up('printout', 0, interactive=False)
"""One standing in for what is not an editor and is never chosen."""

NO_DISPLAY = made_up('window', 10, can_run=False)
"""The window editor on a machine that has no display."""


@pytest.fixture(autouse=True)
def _nothing_shown_yet() -> None:
    """Give one test a record of shown models that is empty."""
    SHOWN.clear()


def registry(monkeypatch: pytest.MonkeyPatch, *found: UiBackend) -> None:
    """Make these registrations the ones this installation has.

    Args:
        monkeypatch: What the replacement is undone by.
        found: The registrations that discovery is to answer with.
    """
    monkeypatch.setattr('edit_cfg_json.ui_choice.discovered_uis',
                        lambda: list(found))


def test_opens_best_editor(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test the editor with the highest priority is the one that is run."""
    registry(monkeypatch, WINDOW, SCREEN, PRINTOUT)
    assert main(list(CLASS_ARGS)) is ExitCode.OK
    assert len(SHOWN) == 1
    assert isinstance(SHOWN[0].shown, EditModel)


def test_falls_to_can_run(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test a machine with no display is given the editor it can run."""
    registry(monkeypatch, NO_DISPLAY, SCREEN)
    assert main(list(CLASS_ARGS)) is ExitCode.OK
    assert len(SHOWN) == 1


def test_named_ui_is_opened(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test `--ui` opens the one it names and not the better one."""
    registry(monkeypatch, WINDOW, SCREEN)
    assert main(['--ui', 'screen', *CLASS_ARGS]) is ExitCode.OK
    assert len(SHOWN) == 1


def test_no_editor_refused(monkeypatch: pytest.MonkeyPatch,
                           capsys: pytest.CaptureFixture[str]) -> None:
    """Test a machine that can open no editor says so and opens nothing.

    The one that can run is not an editor, so it is not what a run that asked
    for nothing is given, and the refusal names it because that is what the
    user can do instead.
    """
    registry(monkeypatch, NO_DISPLAY, PRINTOUT)
    assert main(list(CLASS_ARGS)) is ExitCode.NO_EDITOR
    assert not SHOWN
    printed = capsys.readouterr()
    assert printed.err.startswith(NO_EDITOR)
    assert 'printout' in printed.err


def test_version_no_editor(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test what is installed can be asked where no editor can be opened.

    Whoever is about to report that they have no editor is the one person who
    most needs this answered, so the refusal waits until the command line has
    been read.
    """
    registry(monkeypatch, NO_DISPLAY)
    asked: list[int] = []
    monkeypatch.setattr('versionreporter.VersionReporter.print',
                        lambda self: asked.append(1))
    assert main(['--version']) is ExitCode.OK
    assert asked


def test_help_without_editor(monkeypatch: pytest.MonkeyPatch,
                             capsys: pytest.CaptureFixture[str]) -> None:
    """Test the help is answered where no editor can be opened.

    It is what says that `--ui` exists at all, so a user who has just been
    told that no editor can be opened finds the alternative in it.
    """
    registry(monkeypatch, NO_DISPLAY, PRINTOUT)
    with pytest.raises(SystemExit) as ended:
        main(['--help'])
    assert ended.value.code == ExitCode.OK
    printed = capsys.readouterr()
    assert f'usage: {PROGRAM}' in printed.out
    assert '--ui' in printed.out


def test_choices_can_run(monkeypatch: pytest.MonkeyPatch,
                         capsys: pytest.CaptureFixture[str]) -> None:
    """Test `--ui` accepts exactly the user interfaces that can run here.

    A name that cannot run is refused by `argparse` beside the names that
    would have worked, which is the answer that says what to type instead.
    """
    registry(monkeypatch, NO_DISPLAY, SCREEN)
    with pytest.raises(SystemExit) as ended:
        main(['--ui', 'window', *CLASS_ARGS])
    assert ended.value.code == ExitCode.USAGE
    printed = capsys.readouterr()
    assert 'screen' in printed.err
    assert not SHOWN


def test_save_with_printout(monkeypatch: pytest.MonkeyPatch,
                            tmp_path: Path) -> None:
    """Test the options of a backend with no user appear when it is chosen.

    Which options the parser has depends on the editor, which is why the
    command line is read twice. `--save` belongs to a backend that prints once
    and returns, and asking for it by name is how this program reaches one.
    """
    registry(monkeypatch, WINDOW, PRINTOUT)
    written = tmp_path / 'saved.json'
    assert main(['--ui', 'printout', '--save', '-o', str(written),
                 *CLASS_ARGS]) is ExitCode.OK
    assert written.is_file()


def test_save_refused(monkeypatch: pytest.MonkeyPatch,
                      capsys: pytest.CaptureFixture[str]) -> None:
    """Test `--save` is not even an option where the user could press Save."""
    registry(monkeypatch, WINDOW, PRINTOUT)
    with pytest.raises(SystemExit) as ended:
        main(['--ui', 'window', '--save', *CLASS_ARGS])
    assert ended.value.code == ExitCode.USAGE
    assert '--save' in capsys.readouterr().err


def test_priority_file(monkeypatch: pytest.MonkeyPatch,
                       tmp_path: Path) -> None:
    """Test a settings file decides which editor this program opens.

    It is the shared file of the home folder that decides it, and not one
    belonging to either editor: which editor is opened cannot be decided by
    the settings of one of them, because that one has not been chosen yet.
    """
    registry(monkeypatch, WINDOW, SCREEN)
    named = tmp_path / 'prefer_screen.cfg'
    named.write_text('{"ui_priorities": {"screen": 20}}', encoding='utf-8')
    assert main(['-c', str(named), *CLASS_ARGS]) is ExitCode.OK
    model = SHOWN[0].shown
    assert isinstance(model, EditModel)
    assert model.settings.ui_priorities == {'screen': 20}


def test_home_of_editor(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test the session reads the settings file of the editor that was chosen.

    What the two editors differ about is their keys and their questions, and
    those belong to the user interface rather than to the program that opened
    it, so a session this program opens in one of them behaves like the
    program of that editor.
    """
    registry(monkeypatch, WINDOW, SCREEN)
    (Path.home() / '.window.cfg').write_text('{"backup_count": 4}',
                                             encoding='utf-8')
    assert main(list(CLASS_ARGS)) is ExitCode.OK
    model = SHOWN[0].shown
    assert isinstance(model, EditModel)
    assert model.settings.backup_count == 4


def test_missing_settings(monkeypatch: pytest.MonkeyPatch, tmp_path: Path,
                          capsys: pytest.CaptureFixture[str]) -> None:
    """Test a settings file that was named and is not there is refused once.

    The lookup is made twice, once to decide the editor and once by the
    session, and a user is told about it once: running with other settings
    than the ones that were asked for is what the refusal exists to stop, and
    saying it twice would suggest two faults.
    """
    registry(monkeypatch, WINDOW)
    missing = tmp_path / 'not_here.cfg'
    assert main(['-c', str(missing), *CLASS_ARGS]) is ExitCode.NO_SETTINGS
    assert capsys.readouterr().err.count(str(missing)) == 1


def test_no_class_is_usage(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test this program refuses a command line exactly as the others do."""
    registry(monkeypatch, WINDOW)
    with pytest.raises(SystemExit) as ended:
        main(['--module', 'test_edit_cfg_json.sample_cfg'])
    assert ended.value.code == ExitCode.USAGE


def test_shows_the_class(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test what reaches the editor is the class the command line named."""
    registry(monkeypatch, WINDOW)
    assert main(list(CLASS_ARGS)) is ExitCode.OK
    model = SHOWN[0].shown
    assert isinstance(model, EditModel)
    assert model.config_type_name == 'FlatCfg'
