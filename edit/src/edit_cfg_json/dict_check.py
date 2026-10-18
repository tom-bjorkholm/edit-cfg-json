#! /usr/bin/env python3
"""Where `config_as_json` checks the dicts of a file, and what it demands.

`Config.check_dict_parse` is applied once per member of a configuration
object, with what that object holds in the member and what the file holds for
it. It refuses a dict where the object holds something else and anything else
where the object holds a dict, then matches the keys of the two dicts, and
then does the same for the value at every key the object's dict holds. So what
it demands of one node of a file is answered by walking the object down the
path of that node, and it stops where the recursion stops:

- at a member that `nested_configs()` names, which `config_as_json` reads
  whole instead, so nothing anywhere inside it is checked;
- below a place whose last step names an entry of `_unchecked_dicts`: the
  check returns there after asking whether it is a dict at all, and it asks by
  the name of the step, so a key deeper inside another member that happens to
  have such a name stops it as well, exactly as it stops it in the class;
- at anything that is not a dict, a list among them, and at a key the
  object's dict does not hold, because neither is recursed into.

**The object asked is the one the rows are built from.** Validation parses the
buffer into a copy of the object the model was built on, and a nested object
into a new one of its class, so those are what the file is matched against.
The rows are built from the model's own object, or from what a validation pass
accepted, and an accepted object holds a dict at exactly the checked places
where the object it was matched against does: a pass that held anything else
there was refused. So the answer does not change while the editor is open, and
nothing the user typed can change it.

**One walk answers two questions.** Whether a type that is a dict, or one that
is not, may be chosen at a node (`dict_shape`), and whether the keys of a dict
are matched, which is what decides whether it can gain or lose one
(`keys_checked`). They are one walk because they are one check.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from collections.abc import Container, Mapping
from typing import NamedTuple, Optional
from config_as_json import ConfigPath
from edit_cfg_json.tree import ConfigNode, member_nestings, owner_path, \
    unchecked_members


class DictCheck(NamedTuple):
    """What says where the dict-shape check of one tree reaches."""

    nodes: Mapping[ConfigPath, ConfigNode]
    """Every configuration object of the tree, by its path."""

    nested: Container[ConfigPath]
    """The path of every member that `nested_configs()` names."""

    unchecked: Container[ConfigPath]
    """Each object's path and one name of its `_unchecked_dicts`, as a path.
    """


def dict_check(nodes: Mapping[ConfigPath, ConfigNode]) -> DictCheck:
    """Return what says where the dict-shape check of one tree reaches.

    Args:
        nodes: Every configuration object of the tree, by its path.

    Returns:
        What `dict_shape` and `keys_checked` ask about that tree.
    """
    return DictCheck(nodes=nodes, nested=frozenset(member_nestings(nodes)),
                     unchecked=unchecked_members(nodes))


def dict_shape(path: ConfigPath, check: DictCheck) -> Optional[bool]:
    """Return whether the dict-shape check demands a dict at one node.

    Args:
        path: Path of the node to answer for.
        check: What says where the check of that tree reaches.

    Returns:
        True where only a dict is accepted, False where a dict is refused, and
        None where the check does not reach that node at all.
    """
    owner = owner_path(path=path, nodes=check.nodes)
    member = path[:len(owner) + 1]
    config = check.nodes[owner].config
    if config is None or member in check.nested:
        return None
    held: object = getattr(config, member[-1], None)
    for depth in range(len(member), len(path)):
        if not isinstance(held, dict) or path[depth] not in held or \
                _stops(path=path[:depth], owner=owner, check=check):
            return None
        held = held[path[depth]]
    return isinstance(held, dict)


def keys_checked(path: ConfigPath, check: DictCheck) -> bool:
    """Return whether the keys of the dict at one node are matched.

    They are where the check demands a dict there and goes on past it, and a
    dict whose keys are matched cannot gain or lose one: a file holding one
    with other keys is refused.

    Args:
        path: Path of the dict to answer for.
        check: What says where the check of that tree reaches.

    Returns:
        Whether the class refuses that dict holding other keys than it does.
    """
    owner = owner_path(path=path, nodes=check.nodes)
    return dict_shape(path=path, check=check) is True and \
        not _stops(path=path, owner=owner, check=check)


def _stops(path: ConfigPath, owner: ConfigPath, check: DictCheck) -> bool:
    """Return whether the check returns at one place instead of recursing."""
    return (*owner, path[-1]) in check.unchecked
