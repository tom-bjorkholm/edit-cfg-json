#! /usr/bin/env python3
"""The rows of one configuration, and what the user has done to them.

This is the edit buffer of the model: the values as the user is editing them,
one row per node, and which of the containers are folded away. It is separate
from `EditModel` because the model is a session — where it came from, what the
application decided, what a validation pass found, where a save would go — and
this is the one thing in that session which the user changes by typing.

Nothing here does any input or output, and nothing here knows what a backend
is. What a backend reads is the rows, and what it does is set the text of one
of them and fold one of them away.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from collections.abc import Mapping, Sequence
from typing import TextIO
from config_as_json import Config, ConfigPath, JsonType
from edit_cfg_json.converting import convert_member
from edit_cfg_json.descriptions import Descriptions
from edit_cfg_json.leaf_value import text_as_value
from edit_cfg_json.loading import LoadReport
from edit_cfg_json.rows import MemberRow, built_rows, member_values, stamped
from edit_cfg_json.tree import assembled, starts_folded
from edit_cfg_json.validation import SubtreeAnswer

NOT_EDITABLE_ERROR = 'Member {name} is not a value that can be edited.'
"""Message of the error raised when a node is not a value.

A list, a dict and a nested configuration object are all structure rather than
a value, and each of them is edited through the rows below it. A declared
member that holds no configuration object is refused as well, because no text
becomes one.
"""

NOT_A_CONTAINER = 'Member {name} is not a list or a dict.'
"""Message of the error raised when a node that holds none is folded."""


class EditBuffer:
    """The values of one configuration as the user is editing them.

    Leaf values are held in JSON space, so that an enum member is held as its
    name and a value being typed does not have to be a valid Python value
    yet. JSON space is about the kind of the value, not about its notation:
    a string member holds the string, and the quotes that the file format
    puts around it are added when the file is written and nowhere else.

    A member that holds a list, a dict or a nested configuration object is a
    tree of rows rather than one row, because what is inside one of those is
    edited a value at a time. Every one of them holds what its own rows hold,
    which is kept true as they are edited, so a folded node cannot hide a
    change.
    """

    def __init__(self, config: Config, report: LoadReport,
                 descriptions: Descriptions, stderr_file: TextIO) -> None:
        """Read the JSON space values of one configuration object.

        Args:
            config: Configuration object to read. It is not modified, because
                what is read is the text it writes and not the object.
            report: What reading the input file did beyond reading the values.
            descriptions: What the application says about its members.
            stderr_file: Stream used for user-facing diagnostics.

        Raises:
            InvalidConfiguration: The configuration object is not valid.
            InvalidConfigurationValue: A member of the configuration object
                does not hold a valid value.
        """
        self._report = report
        self._descriptions = descriptions
        self._folded: set[ConfigPath] = set()
        self._answers: dict[ConfigPath, SubtreeAnswer] = {}
        self._rows: dict[ConfigPath, MemberRow] = {}
        self._rebuild(config=config, previous={},
                      members=member_values(config=config,
                                            stderr_file=stderr_file))

    @property
    def report(self) -> LoadReport:
        """Return what reading the input file did beyond reading values."""
        return self._report

    @property
    def rows(self) -> Sequence[MemberRow]:
        """Return one row per node of the configuration, in the order shown.

        Every row is here whether it is folded away or not, because a backend
        creates its widgets once and hides the ones that are not shown.
        """
        return tuple(self._rows.values())

    @property
    def dirty(self) -> bool:
        """Return whether the buffer holds anything that is worth saving."""
        return any(row.edited for row in self._rows.values())

    @property
    def anything_open(self) -> bool:
        """Return whether at least one container is open."""
        return any(row.foldable and not row.folded
                   for row in self._rows.values())

    def values(self) -> dict[str, JsonType]:
        """Return the buffer as one JSON space value per member.

        A member that holds a list or a dict holds what its own rows hold,
        because every edit of a value inside one is written up into it.

        Returns:
            One value per member of the configuration.
        """
        return {row.name: row.value for row in self._rows.values()
                if row.depth == 0}

    def set_text(self, path: ConfigPath, text: str) -> bool:
        """Set one node of the buffer from the text of an edit field.

        Text that the node already shows changes nothing, because it is not
        an edit. That is not only tidiness: a field posts a change when it is
        given its initial text, and a buffer that counted that as an edit
        would report unsaved changes before the user had touched anything.
        It is also what lets a backend write the buffer back into its fields
        after a validation pass without that counting as an edit.

        Every container the node is inside is brought up to date with it, so
        that what the whole configuration holds is always what its rows say.

        Args:
            path: Path of the node to set.
            text: Text that the edit field holds.

        Returns:
            Whether that was an edit, which is what the rest of the session
            asks: a verdict and a save that were reached from this buffer
            still stand while nothing in it has changed.

        Raises:
            KeyError: The path is not a node of this configuration.
            ValueError: The node is not one that this version can edit.
        """
        row = self._rows[path]
        if not row.editable:
            raise ValueError(NOT_EDITABLE_ERROR.format(name=row.name))
        if row.value_text == text:
            return False
        value = text_as_value(text=text, is_text_member=row.is_text)
        self._rows[path] = row._replace(value=value, conversion='',
                                        changed_by_validator=False)
        self._hold_again(path)
        return True

    def check_field(self, path: ConfigPath) -> None:
        """Report whether the text of one node means a value of it at all.

        Args:
            path: Path of the node to check.

        Raises:
            KeyError: The path is not a node of this configuration.
        """
        row = self._rows[path]
        converted = convert_member(converter=row.converter, value=row.value)
        self._rows[path] = row._replace(conversion=converted.message)

    def check_all(self) -> None:
        """Report every node whose text means no value of that node."""
        for path in tuple(self._rows):
            self.check_field(path)

    def toggle_fold(self, path: ConfigPath) -> None:
        """Fold one container away, or open it again.

        Args:
            path: Path of the container to fold or open.

        Raises:
            KeyError: The path is not a node of this configuration.
            ValueError: The node is not a container.
        """
        row = self._rows[path]
        if not row.foldable:
            raise ValueError(NOT_A_CONTAINER.format(name=row.name))
        self._folded ^= {path}
        self._stamp()

    def toggle_fold_all(self) -> None:
        """Fold every container away, or open every one of them.

        One action and not two, because a user who wants the values back
        wants all of them back: which of the two it does is decided by what
        is on the screen, so a press always changes something.
        """
        self._folded = {row.path for row in self._rows.values()
                        if row.foldable} if self.anything_open else set()
        self._stamp()

    def take_subtrees(self,
                      answers: Mapping[ConfigPath, SubtreeAnswer]) -> None:
        """Keep what asking these objects about themselves found.

        Only the objects that were asked are replaced, and what every other
        one said is left exactly as it was: folding one node asks the objects
        at and inside it, and a validation pass asks all of them.

        Args:
            answers: What each of them said about itself, by the path of its
                node.
        """
        self._answers.update(answers)
        self._stamp()

    def keep_saved(self) -> None:
        """Make what was written the values that the buffer is compared to.

        The mark of a node a validator rewrote is deliberately left alone.
        That a value is not literally the one the user typed stays true after
        it has been saved, and it is the mark that says so.
        """
        self._rows = {path: row._replace(original=row.value)
                      for path, row in self._rows.items()}

    def take_validated(self, config: Config,
                       members: Mapping[str, JsonType]) -> None:
        """Rebuild the buffer from the configuration object that was built.

        The rows are built again rather than patched, because a validator
        that normalizes a list changes how many rows there are: the paths
        after such a pass are not the paths before it. What every row that
        is still there knew is carried over, so the rebuild is a refresh.

        Args:
            config: Configuration object that the pass accepted, which is
                what says in which order the members are shown and which of
                the nodes are configuration objects of their own. It is the
                object these values were read from, so it is what answers for
                them. It is not modified.
            members: One JSON space value per member of the accepted object.
        """
        self._rebuild(config=config, members=members, previous=self._rows)

    def _rebuild(self, config: Config, members: Mapping[str, JsonType],
                 previous: Mapping[ConfigPath, MemberRow]) -> None:
        """Build the rows from one set of values, keeping what was known.

        Args:
            config: Configuration object holding these values. It is not
                modified.
            members: One JSON space value per serialized member.
            previous: The rows as they were before, empty for the first build.
        """
        self._rows = built_rows(config=config, members=dict(members),
                                report=self._report,
                                descriptions=self._descriptions,
                                previous=previous)
        self._fold_new(previous)
        self._forget_gone()
        self._stamp()

    def _forget_gone(self) -> None:
        """Forget what an object that a pass left no row at all said.

        A pass can change how many nodes there are, so an object that answered
        about itself may be gone by the time the rows are built again. What it
        said is then about nothing and is dropped, exactly as the fold of a
        container that a pass removed is.
        """
        self._answers = {path: answer for path, answer in self._answers.items()
                         if path in self._rows}

    def _fold_new(self, previous: Mapping[ConfigPath, MemberRow]) -> None:
        """Decide the fold of a container that has just appeared.

        A container the user folded stays folded across a validation pass,
        because folding is what the user asked for and a pass answers a
        different question. One that a pass created is decided the way every
        container is decided when the editor opens, and one that a pass
        removed is forgotten.

        Args:
            previous: The rows as they were before, empty for the first build.
        """
        containers = {path for path, row in self._rows.items() if row.foldable}
        self._folded &= containers
        self._folded |= {path for path in containers - set(previous)
                         if starts_folded(path=path, paths=self._rows)}

    def _stamp(self) -> None:
        """Write the state of the buffer onto the rows it is about."""
        self._rows = stamped(rows=self._rows, folded=self._folded,
                             answers=self._answers)

    def _hold_again(self, path: ConfigPath) -> None:
        """Bring every container that one node is inside up to date with it.

        Args:
            path: Path of the node that was just edited.
        """
        for depth in range(len(path) - 1, 0, -1):
            parent = self._rows[path[:depth]]
            self._rows[parent.path] = parent._replace(
                value=assembled(children=self._held(parent),
                                as_list=isinstance(parent.original, list)))
        if self._forget_answers(path):
            self._stamp()

    def _forget_answers(self, path: ConfigPath) -> bool:
        """Take back what every object holding one node said about itself.

        The answer was about the values that object held, and one of them has
        just changed, so it is taken back along with everything it explained.
        An object beside it is left alone: nothing inside that one has
        changed, so what it said is as true as it was.

        It is a different lifetime from the verdict of the whole
        configuration, which any edit anywhere takes away, and that is why the
        answers are kept here rather than there.

        Args:
            path: Path of the node that was just edited.

        Returns:
            Whether anything was taken back, which is what says that the rows
            have to be written again. Every key the user types reaches this,
            and the second of them has nothing left to take back.
        """
        kept = {other: answer for other, answer in self._answers.items()
                if not (len(other) < len(path)
                        and path[:len(other)] == other)}
        if len(kept) == len(self._answers):
            return False
        self._answers = kept
        return True

    def _held(self, parent: MemberRow) -> list[tuple[str, JsonType]]:
        """Return the last step and the value of each child of one row."""
        return [(child[-1], self._rows[child].value)
                for child in parent.children or ()]
