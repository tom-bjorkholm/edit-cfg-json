#! /usr/bin/env python3
"""Ways of reading one edit model that its tests share.

A test of the model asks it the same four things over and over: what one row
holds, which rows there are, which of them are on the screen, and what a save
wrote. They are here rather than in each test module, so that one test module
more does not mean one more copy of them.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from pathlib import Path
import json
from config_as_json import ConfigPath, JsonType
from edit_cfg_json import EditModel, MemberRow


def row_at(model: EditModel, path: ConfigPath) -> MemberRow:
    """Return the row of one node of one model.

    Args:
        model: Model to read.
        path: Path that addresses the node.

    Returns:
        The row of that node.

    Raises:
        KeyError: The path is not a node of this configuration.
    """
    return {row.path: row for row in model.rows}[path]


def row_paths(model: EditModel) -> list[ConfigPath]:
    """Return the path of every row of one model, in the order shown.

    Args:
        model: Model to read.

    Returns:
        The path of every node, folded away or not.
    """
    return [row.path for row in model.rows]


def shown_paths(model: EditModel) -> list[ConfigPath]:
    """Return the path of every row that is not folded away.

    Args:
        model: Model to read.

    Returns:
        The path of every node that is on the screen as things stand.
    """
    return [row.path for row in model.rows if row.shown]


def written(out_file: Path) -> JsonType:
    """Return what one output file holds, as JSON space values.

    Args:
        out_file: File that a save wrote.

    Returns:
        The values of that file.
    """
    value: JsonType = json.loads(out_file.read_text(encoding='UTF-8'))
    return value
