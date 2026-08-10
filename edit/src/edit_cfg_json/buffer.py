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
from copy import deepcopy
from io import StringIO
from typing import Optional, TextIO
from config_as_json import Config, ConfigPath, JsonType
from edit_cfg_json.converting import convert_member
from edit_cfg_json.descriptions import Descriptions
from edit_cfg_json.elements import NOT_EXTENDABLE, NOT_MOVABLE, \
    NOT_REMOVABLE, checked_key, grown, kept_order, moved_paths, object_added, \
    object_moved, object_removed, refused, shrunk, swapped
from edit_cfg_json.leaf_value import text_as_value
from edit_cfg_json.loading import LoadReport
from edit_cfg_json.rows import MemberRow, built_rows, stamped
from edit_cfg_json.tree import assembled, member_values, starts_folded
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


def _swapped_order(count: int, index: int, later: bool) -> list[int]:
    """Return the order of one list with one element moved by one place.

    Args:
        count: How many elements the list holds.
        index: Where the element that moves is now.
        later: Whether it changes places with the one after it.

    Returns:
        The index each element of the new list had in the old one.
    """
    order = list(range(count))
    other = index + 1 if later else index - 1
    order[index], order[other] = order[other], order[index]
    return order


def _renamed(rows: Mapping[ConfigPath, MemberRow],
             moved: Mapping[ConfigPath, ConfigPath]
             ) -> dict[ConfigPath, MemberRow]:
    """Return the rows under the paths that they have after a change.

    A row whose path has not changed keeps it. A row that has moved is put
    under its new path, which is what takes the place of the row that used to
    be there, and the path an element vacated is left to whatever moved into
    it or to nothing at all.

    Args:
        rows: The rows as they were before the change.
        moved: The new path of every row whose path has changed.

    Returns:
        Those rows by the path each of them has now, which is what the next
        build compares against.
    """
    kept = {path: row for path, row in rows.items() if path not in moved}
    kept.update({new: rows[old] for old, new in moved.items()})
    return kept


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
                 descriptions: Descriptions, stderr_file: TextIO,
                 defaults: Mapping[str, JsonType]) -> None:
        """Read the JSON space values of one configuration object.

        Args:
            config: Configuration object to read. It is not modified, because
                what is read is the text it writes and not the object.
            report: What reading the input file did beyond reading the values.
            descriptions: What the application says about its members.
            stderr_file: Stream used for user-facing diagnostics.
            defaults: The values that the class declares, which is what a new
                element of an ordinary list is copied from. They are empty for
                a class the editor could not construct at all, which costs
                that configuration the offer to grow such a list and nothing
                else.

        Raises:
            InvalidConfiguration: The configuration object is not valid.
            InvalidConfigurationValue: A member of the configuration object
                does not hold a valid value.
        """
        self._report = report
        self._descriptions = descriptions
        self._defaults = defaults
        self._folded: set[ConfigPath] = set()
        self._folds_new = True
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
        if not self.anything_open:
            self.open_all()
            return
        self._folded = {row.path for row in self._rows.values()
                        if row.foldable}
        self._stamp()

    def open_all(self, no_more_folding: bool = False) -> None:
        """Open every container of the buffer, whatever is folded now.

        Args:
            no_more_folding: Whether a container that appears later is to be
                open as well. It stays on once it has been asked for, because
                what asks for it is a program that shows the buffer once: a
                validation pass can create a container, and the rule that
                decides the fold of a new one would fold a big one away again
                after the only moment at which anything is shown.
        """
        self._folded = set()
        self._folds_new = self._folds_new and not no_more_folding
        self._stamp()

    def add_element(self, config: Config, path: ConfigPath,
                    key: str = '') -> None:
        """Put one more element into a node that holds them.

        A new element is what the class of the configuration said one is: an
        object of the declared class where the class declares one, and a copy
        of what it declares for the member where it does not. A declared member
        that holds no object is grown by being given the object it is for,
        which is what design section 4.1 of `doc/design.md` calls adding.

        Args:
            config: Configuration object of the session. It is modified where
                the new element is a configuration object, because the tree
                finds those objects by walking the real ones. It is the
                editor's own copy and never the caller's.
            path: Path of the node to put an element into.
            key: Name of the new entry of a dict, empty for everything else.

        Raises:
            KeyError: The path is not a node of this configuration.
            ValueError: Nothing can be added there, or the key is missing,
                unwanted or one that dict already holds.
        """
        row = self._rows[path]
        refused(offered=row.offer.extend, form=NOT_EXTENDABLE, path=path)
        checked_key(offer=row.offer, value=row.value, key=key, path=path)
        object_added(config=config, path=path, key=key, stream=StringIO())
        made = grown(value=row.value, key=key, template=row.offer.template) \
            if row.foldable else deepcopy(row.offer.template)
        self._restructured(config=config, path=path, value=made, moved={})

    def remove_element(self, config: Config, path: ConfigPath) -> None:
        """Take one element out of the node that holds it.

        Args:
            config: Configuration object of the session, modified as above.
            path: Path of the element to remove, or of the declared optional
                member to put back to holding no object.

        Raises:
            KeyError: The path is not a node of this configuration.
            ValueError: That node is not one that can be removed.
        """
        row = self._rows[path]
        refused(offered=row.offer.remove, form=NOT_REMOVABLE, path=path)
        object_removed(config=config, path=path)
        held = self._container_of(path)
        if held is None:
            self._restructured(config=config, path=path, value=None, moved={})
            return
        self._restructured(config=config, path=held.path,
                           value=shrunk(value=held.value, step=path[-1]),
                           moved=self._moved(held=held, path=path,
                                             removing=True))

    def move_element(self, config: Config, path: ConfigPath,
                     later: bool) -> None:
        """Make one element of a list change places with a neighbour.

        Args:
            config: Configuration object of the session, modified as above.
            path: Path of the element to move.
            later: Whether it changes places with the one after it rather than
                with the one before it.

        Raises:
            KeyError: The path is not a node of this configuration.
            ValueError: That node cannot be moved that way.
        """
        row = self._rows[path]
        refused(offered=row.offer.later if later else row.offer.earlier,
                form=NOT_MOVABLE, path=path)
        object_moved(config=config, path=path, later=later)
        held = self._rows[path[:-1]]
        order = swapped(value=held.value, index=int(path[-1]), later=later)
        self._restructured(config=config, path=held.path, value=order,
                           moved=self._moved(held=held, path=path,
                                             removing=False, later=later))

    def _container_of(self, path: ConfigPath) -> Optional[MemberRow]:
        """Return the row of the container one node is an element of.

        Args:
            path: Path of the node to ask about.

        Returns:
            The row of the list or the dict holding it, and None for a
            declared member, which is held by a configuration object and not
            by a container.
        """
        parent = self._rows.get(path[:-1])
        if parent is None or parent.config_type is not None or \
                not parent.foldable:
            return None
        return parent

    def _moved(self, held: MemberRow, path: ConfigPath, removing: bool,
               later: bool = False) -> dict[ConfigPath, ConfigPath]:
        """Return where each node under one container goes after a change.

        Every node inside the container and not only its elements, because an
        element of a list holds nodes of its own and all of them are addressed
        through the index that has just changed.

        A dictionary entry keeps its key whatever happens to the entries
        beside it, so only a list moves anything.

        Args:
            held: Row of the container that changed.
            path: Path of the element that was removed or moved.
            removing: Whether the element was taken out rather than moved.
            later: Whether it changed places with the one after it.

        Returns:
            The new path of every node whose path has changed.
        """
        if not isinstance(held.value, list):
            return {}
        index = int(path[-1])
        order = kept_order(count=len(held.value), without=index) if removing \
            else _swapped_order(count=len(held.value), index=index,
                                later=later)
        return moved_paths(paths=self._rows, container=held.path, order=order)

    def _restructured(self, config: Config, path: ConfigPath, value: JsonType,
                      moved: Mapping[ConfigPath, ConfigPath]) -> None:
        """Give one node a new value and build the rows around it again.

        Everything the buffer holds about a node is held under the path of
        that node, and an element of a list is addressed by where it is, so
        the fold state, what each object said about itself and what each row
        is compared against all move with the values.

        Args:
            config: Configuration object of the session, which now holds the
                objects that this change made or removed.
            path: Path of the node whose value changed.
            value: The value it holds now.
            moved: The new path of every node whose path has changed.
        """
        self._rows[path] = self._rows[path]._replace(value=value)
        self._hold_again(path)
        self._folded = {moved.get(other, other) for other in self._folded}
        self._answers = {moved.get(other, other): answer
                         for other, answer in self._answers.items()}
        self._rebuild(config=config, members=self.values(),
                      previous=_renamed(rows=self._rows, moved=moved))

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
        self._rebuild(config=config, members=members, previous=self._rows,
                      refreshing=True)

    def _rebuild(self, config: Config, members: Mapping[str, JsonType],
                 previous: Mapping[ConfigPath, MemberRow],
                 refreshing: bool = False) -> None:
        """Build the rows from one set of values, keeping what was known.

        Args:
            config: Configuration object holding these values. It is not
                modified.
            members: One JSON space value per serialized member.
            previous: The rows as they were before, empty for the first build.
            refreshing: Whether these values are what a validation pass
                accepted, which is what decides whether a node it changed is
                marked as one a validator wrote.
        """
        self._rows = built_rows(config=config, members=dict(members),
                                report=self._report,
                                descriptions=self._descriptions,
                                previous=previous, defaults=self._defaults,
                                refreshing=refreshing)
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
        removed is forgotten. A buffer that was opened for good decides
        nothing: everything in it is open, including whatever has just
        appeared.

        Args:
            previous: The rows as they were before, empty for the first build.
        """
        containers = {path for path, row in self._rows.items() if row.foldable}
        self._folded &= containers
        if not self._folds_new:
            return
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

        The object *at* the node is taken back as well, which only a change of
        structure reaches: an editable node is never a configuration object,
        and a member that has just been given one has an object that nothing
        has asked anything of yet.

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
                if not (len(other) <= len(path)
                        and path[:len(other)] == other)}
        if len(kept) == len(self._answers):
            return False
        self._answers = kept
        return True

    def _held(self, parent: MemberRow) -> list[tuple[str, JsonType]]:
        """Return the last step and the value of each child of one row."""
        return [(child[-1], self._rows[child].value)
                for child in parent.children or ()]
