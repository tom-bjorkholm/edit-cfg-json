#! /usr/bin/env python3
"""Tests for how much each part of the editor stands out.

What the two state dependent decisions are is tested here, because they are
the ones both backends would otherwise answer for themselves and could answer
differently. What colour each answer becomes is each backend's own and is
tested there.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from pathlib import Path
from edit_cfg_json import EXPLANATION, EditModel, Emphasis, LOAD_REMARK, \
    MEMBER_MARK, save_emphasis, verdict_emphasis
from .sample_cfg import FlatCfg, RangeCfg


def test_kinds_of_text() -> None:
    """Test each kind of text has a reason to stand out, and its own one.

    The explanations are secondary text, a mark is something that happened to
    a member, and a remark about the input file is a warning about a file that
    was not what was asked for. Three different things, so three answers.
    """
    assert EXPLANATION is Emphasis.MUTED
    assert MEMBER_MARK is Emphasis.ATTENTION
    assert LOAD_REMARK is Emphasis.WARNING


def test_verdict_unknown() -> None:
    """Test a buffer nobody validated is the third state and not a failure."""
    assert verdict_emphasis(EditModel(FlatCfg())) is Emphasis.MUTED


def test_verdict_accepted() -> None:
    """Test a buffer the application accepts is shown as accepted."""
    model = EditModel(FlatCfg())
    model.validate()
    assert verdict_emphasis(model) is Emphasis.GOOD


def test_verdict_refused() -> None:
    """Test a buffer the application refuses is shown as refused."""
    model = EditModel(RangeCfg())
    model.set_text(path=('answer',), text='500')
    model.validate()
    assert verdict_emphasis(model) is Emphasis.BAD


def test_edit_forgets_verdict() -> None:
    """Test an edit puts the validation back to the state nobody reached."""
    model = EditModel(FlatCfg())
    model.validate()
    model.set_text(path=('answer',), text='7')
    assert verdict_emphasis(model) is Emphasis.MUTED


def test_save_not_tried() -> None:
    """Test a destination that is waiting is not a state that was reached."""
    assert save_emphasis(EditModel(FlatCfg())) is Emphasis.MUTED


def test_save_wrote(tmp_path: Path) -> None:
    """Test a save that wrote the file is shown as one that did."""
    model = EditModel(FlatCfg(), out_file=tmp_path / 'out.json')
    model.save()
    assert save_emphasis(model) is Emphasis.GOOD


def test_save_refused(tmp_path: Path) -> None:
    """Test a save that could not be made is shown as refused."""
    model = EditModel(RangeCfg(), out_file=tmp_path / 'out.json')
    model.set_text(path=('answer',), text='500')
    model.save()
    assert save_emphasis(model) is Emphasis.BAD


def test_save_no_destination() -> None:
    """Test a save with nowhere to write is refused rather than pending."""
    model = EditModel(FlatCfg())
    model.save()
    assert save_emphasis(model) is Emphasis.BAD


def test_edit_forgets_save(tmp_path: Path) -> None:
    """Test an edit after a save puts the saving back to waiting."""
    model = EditModel(FlatCfg(), out_file=tmp_path / 'out.json')
    model.save()
    model.set_text(path=('answer',), text='7')
    assert save_emphasis(model) is Emphasis.MUTED


def test_save_outcome_kept(tmp_path: Path) -> None:
    """Test the model reports what the last attempt to save did.

    Whether an attempt succeeded is what a backend cannot read out of the
    message of it, and it is what decides how that message is shown.
    """
    model = EditModel(FlatCfg(), out_file=tmp_path / 'out.json')
    assert model.save_outcome is None
    outcome = model.save()
    assert model.save_outcome is outcome
    assert outcome.saved
