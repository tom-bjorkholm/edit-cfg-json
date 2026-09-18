#! /usr/bin/env python3
"""Tests for example a03_chosen_ui.

**Every test here names the user interface it wants**, and that is what makes
them tests of this example rather than of the machine they run on: with no
`--ui` the example opens whichever editor is installed and can run, which is a
window on one machine and a terminal screen on another. `--ui dump`, which the
`dump` helper adds, is the one answer that is the same everywhere, and what it
prints is the same evidence that the `e` series of examples is checked by.

That backend has nobody to press Save, so the three tests that need a session
which does something replace what this installation registers with a user
interface made up here. Two of them are about a machine that can open no
editor, which cannot be reached on a machine that can.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from pathlib import Path
import pytest
from edit_cfg_json import EditModel, UiBackend
from example import a03_chosen_ui
from example._shared_pipeline import PipelineConfig, RUN_UNCHANGED, \
    SESSION_NOTHING, SESSION_SAVED
from .helpers import PIPELINE_FILE, data_file, dump, head, refusal_of, \
    written_json

NOT_HERE = 'window'
"""A user interface that the tests make unable to run in this context."""

SAVING = 'saver'
"""A user interface whose stand-in user edits one member and saves."""


class _Saver:  # pylint: disable=too-few-public-methods
    """A backend standing in for a user who typed a value and saved.

    The one user interface every machine has is the backend that prints, and
    it has nobody to press Save. So a session that really writes something is
    a user interface made up here, which is also what says that anything
    registered is opened: this one is no part of the library at all.
    """

    def run_editor(self, model: EditModel) -> None:
        """Type into the number member and save."""
        model.set_text(path=('workers',), text='8')
        model.save()


def _registered(monkeypatch: pytest.MonkeyPatch, *found: UiBackend) -> None:
    """Make these registrations the ones this installation has.

    Args:
        monkeypatch: What the replacement is undone by.
        found: The registrations that discovery is to answer with.
    """
    monkeypatch.setattr('edit_cfg_json.ui_choice.discovered_uis',
                        lambda: list(found))


def _unavailable(ui_name: str) -> UiBackend:
    """Return a registration of a user interface that cannot run here.

    Args:
        ui_name: What `--ui` would call it.

    Returns:
        A registration answering that this context is not one it can run in.
    """
    def answer() -> bool:
        """Answer that this user interface cannot run here."""
        return False
    return UiBackend(ui_name=ui_name, priority=10, can_run=answer,
                     backend=_Saver)


def _saving() -> UiBackend:
    """Return a registration whose backend edits one member and saves.

    Returns:
        A registration of a user interface that does not exist.
    """
    return UiBackend(ui_name=SAVING, priority=10, can_run=lambda: True,
                     backend=_Saver)


def test_prints_the_config(capsys: pytest.CaptureFixture[str]) -> None:
    """Test the editor is opened in the user interface that was named.

    `--ui dump` is not an editor and is the one user interface every machine
    has, which is why this example's own test is written against it. What it
    prints is the configuration the example handed over, with what the example
    says about each member.
    """
    printed = dump(a03_chosen_ui.main, capsys)
    assert printed.startswith(head(PipelineConfig()))
    assert 'What this pipeline is called in the logs.' in printed


def test_reads_the_file(capsys: pytest.CaptureFixture[str]) -> None:
    """Test the file options reach the editor as they do in a01 and a02."""
    named = data_file(PIPELINE_FILE)
    printed = dump(a03_chosen_ui.main, capsys, '-i', named)
    assert 'release-candidate' in printed


def test_nothing_saved(capsys: pytest.CaptureFixture[str]) -> None:
    """Test a session that wrote nothing leaves the command as it was.

    Nothing saved is an ordinary outcome and not an error, and this backend
    has nobody to press Save, so it is what every run of it reports.
    """
    printed = dump(a03_chosen_ui.main, capsys)
    assert SESSION_NOTHING in printed
    assert RUN_UNCHANGED in printed


def test_ui_offers_what_runs(monkeypatch: pytest.MonkeyPatch,
                             capsys: pytest.CaptureFixture[str]) -> None:
    """Test the option accepts exactly what this machine can really run.

    The choices are asked of the library rather than written out, so a user
    interface that cannot run here is not offered and asking for it is
    refused by `argparse` beside the ones that would have worked.
    """
    _registered(monkeypatch, _unavailable(NOT_HERE))
    with pytest.raises(SystemExit):
        a03_chosen_ui.main(['--ui', NOT_HERE])
    assert NOT_HERE in capsys.readouterr().err


def test_no_editor_message(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test a machine with no editor at all is told, and not given a trace.

    This example names no toolkit, so it could not catch an exception of one.
    What it catches instead is the one refusal of this library, which says the
    same thing whatever the user interfaces of the machine happen to be.
    """
    _registered(monkeypatch, _unavailable(NOT_HERE))
    said = refusal_of(lambda: a03_chosen_ui.main([]))
    assert 'No editor' in said


def test_saved_comes_back(monkeypatch: pytest.MonkeyPatch,
                          capsys: pytest.CaptureFixture[str],
                          tmp_path: Path) -> None:
    """Test what the session saved is handed back to the command.

    The command goes on with the object the call answered with, which is what
    the last line says: the object the example constructed is untouched, so
    the values named there can only have come from the return value.
    """
    _registered(monkeypatch, _saving())
    out_file = tmp_path / 'pipeline.json'
    a03_chosen_ui.main(['--ui', SAVING, '-i', data_file(PIPELINE_FILE),
                        '-o', str(out_file)])
    printed = capsys.readouterr().out
    assert SESSION_SAVED.format(name='PipelineConfig') in printed
    assert 'Running release-candidate with 8 workers.' in printed
    assert written_json(out_file) == {'name': 'release-candidate',
                                      'workers': 8}
