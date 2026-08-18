#! /usr/bin/env python3
"""Tests for example e12_backup_files.

What this example adds is what becomes of the file that a save overwrites. So
what is asserted here is that it is kept under the name this application chose,
that the kept files are numbered and rotate the way it asked for, that one
session keeps one of them however often the user presses Save, and that a save
which writes nothing keeps nothing either.

Every one of these runs `--ui dump`, which has nobody to answer the question
that the two editors put before they overwrite anything. That question is
tested in the core and in each of the two backends, where it exists.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from pathlib import Path
import json
import shutil
import pytest
from example import e12_backup_files
from example.e12_backup_files import ArchiveConfig, FILE_SETTINGS
from .helpers import data_file, dump, head, open_tk_ui, saved_tail, \
    textual_titles

HEAD = head(ArchiveConfig())
"""The lines that every dump of this example begins with."""

DATA_NAME = 'e12_archive.cfg'
"""Input file of this example, which is copied before it is written over."""

FILE_VALUES = {'archive_folder': '/srv/collector/archive', 'compress': False,
               'keep_days': 30}
"""What that input file holds, which is what the first save keeps."""


def _dump(capsys: pytest.CaptureFixture[str], *settings: str) -> str:
    """Run this example with `--ui dump` and return what it printed."""
    return dump(e12_backup_files.main, capsys, *settings)


def _copied(tmp_path: Path) -> Path:
    """Return a copy of the input file, which is what a save writes over.

    The data files of the examples are never written to, so a round trip over
    one of them is a round trip over a copy.
    """
    out_file = tmp_path / 'archive.cfg'
    shutil.copyfile(data_file(DATA_NAME), out_file)
    return out_file


def _held(name: Path) -> object:
    """Return what one file holds, as JSON space values."""
    return json.loads(name.read_text(encoding='UTF-8'))


def _days(keep_days: int) -> dict[str, object]:
    """Return the values of the input file with another number of days.

    Args:
        keep_days: How long the archive is kept, which is the one member
            that these tests edit.

    Returns:
        What a file written after that edit holds.
    """
    return {**FILE_VALUES, 'keep_days': keep_days}


def test_example_decides() -> None:
    """Test the answers of this application are its own and not options.

    A real application knows what it has decided about its files and says so
    in one object, which is what this example is here to show.
    """
    assert FILE_SETTINGS.backup_suffix == '.old'
    assert FILE_SETTINGS.backup_count == 3
    assert FILE_SETTINGS.confirm_overwrite


def test_dump(capsys: pytest.CaptureFixture[str]) -> None:
    """Test the three declared members are shown with their defaults."""
    assert _dump(capsys) == (
        f'{HEAD}\narchive_folder = /var/lib/collector\n    Text.\n'
        'keep_days = 30\n    A whole number.\n'
        'compress = true\n    True or false.\n'
        'validation: valid\nsave to: no file chosen yet\n'
        'edit() returned None, so nothing was saved.')


@pytest.mark.parametrize('typed, row',
                         [('f', 'compress = false (edited)'),
                          ('F', 'compress = false (edited)'),
                          ('tr', 'compress = true'),
                          ('TRUE', 'compress = true')])
def test_flag_typed(typed: str, row: str,
                    capsys: pytest.CaptureFixture[str]) -> None:
    """Test the member holding true or false takes a beginning of a word.

    This application says nothing at all about that member, so what accepts
    the beginning is the editor reading the type of the member from the value
    it holds. The two beginnings of the value it already holds leave nothing
    to save, because what would be written is what the file holds.
    """
    shown = _dump(capsys, '--set', f'compress={typed}')
    assert f'\n{row}\n' in shown
    assert 'validation: valid' in shown


def test_flag_refused(capsys: pytest.CaptureFixture[str]) -> None:
    """Test a text that means neither word is refused at that member."""
    shown = _dump(capsys, '--set', 'compress=yes')
    assert 'yes is not one of: true, false' in shown
    assert 'validation: invalid, see compress' in shown


def test_previous_kept(tmp_path: Path,
                       capsys: pytest.CaptureFixture[str]) -> None:
    """Test a save over the input file keeps what that file held."""
    out_file = _copied(tmp_path)
    kept = tmp_path / 'archive.cfg.old_1'
    printed = _dump(capsys, '-i', str(out_file), '--set', 'keep_days=60',
                    '--save')
    assert printed.endswith(saved_tail(out_file, 'ArchiveConfig', kept))
    assert _held(kept) == FILE_VALUES
    assert _held(out_file) == _days(60)


def test_kept_files_rotate(tmp_path: Path,
                           capsys: pytest.CaptureFixture[str]) -> None:
    """Test each run moves the kept files one number further back.

    Three runs over one file, by an application that keeps three of them, so
    the oldest of the three is the one the first run wrote over.
    """
    out_file = _copied(tmp_path)
    for days in ('60', '90', '120'):
        _dump(capsys, '-i', str(out_file), '--set', f'keep_days={days}',
              '--save')
    kept = [_held(tmp_path / f'archive.cfg.old_{number}')
            for number in (1, 2, 3)]
    assert kept == [_days(90), _days(60), FILE_VALUES]
    assert _held(out_file) == _days(120)


def test_kept_once_a_session(tmp_path: Path,
                             capsys: pytest.CaptureFixture[str]) -> None:
    """Test pressing Save twice in one session keeps one file and not two.

    What a second press would keep is the first press of the same session,
    and keeping that would push the configuration that was really there one
    number further from being found.
    """
    out_file = _copied(tmp_path)
    printed = _dump(capsys, '-i', str(out_file), '--set', 'keep_days=60',
                    '--save', '--save')
    assert printed.endswith(saved_tail(out_file, 'ArchiveConfig'))
    assert _held(tmp_path / 'archive.cfg.old_1') == FILE_VALUES
    assert not (tmp_path / 'archive.cfg.old_2').exists()


def test_refused_save_keeps(tmp_path: Path,
                            capsys: pytest.CaptureFixture[str]) -> None:
    """Test a save that writes nothing leaves the kept files alone.

    Saving is validating and then writing, and what the file holds is kept
    between the two, so a refused save costs neither the file nor the oldest
    of the kept ones.
    """
    out_file = _copied(tmp_path)
    _dump(capsys, '-i', str(out_file), '--set', 'keep_days=60', '--save')
    printed = _dump(capsys, '-i', str(out_file), '--set', 'keep_days=soon',
                    '--save')
    assert 'These values are not valid, so they cannot be saved.' in printed
    assert _held(tmp_path / 'archive.cfg.old_1') == FILE_VALUES
    assert not (tmp_path / 'archive.cfg.old_2').exists()
    assert _held(out_file) == _days(60)


def test_new_file_keeps_none(tmp_path: Path,
                             capsys: pytest.CaptureFixture[str]) -> None:
    """Test a destination that holds no file is nothing to keep."""
    out_file = tmp_path / 'first.cfg'
    printed = _dump(capsys, '-o', str(out_file), '--save')
    assert printed.endswith(saved_tail(out_file, 'ArchiveConfig'))
    assert list(tmp_path.iterdir()) == [out_file]


def test_extension_completed(tmp_path: Path,
                             capsys: pytest.CaptureFixture[str]) -> None:
    """Test the extension of this application reaches a name that has none.

    It is one `Settings` object, so the answer this example gives about its
    file names arrives with the answers it gives about keeping them.
    """
    out_file = tmp_path / 'chosen'
    assert f'Saved to {out_file}.cfg.' in _dump(capsys, '-o', str(out_file),
                                                '--save')


def test_tk_ui_opens(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test --ui tk builds the window and returns when it is closed."""
    open_tk_ui(e12_backup_files.main, monkeypatch, '-i', data_file(DATA_NAME))


def test_textual_ui_opens(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test --ui textual starts the application named after the class."""
    assert textual_titles(e12_backup_files.main, monkeypatch, '-i',
                          data_file(DATA_NAME)) == ['ArchiveConfig']
