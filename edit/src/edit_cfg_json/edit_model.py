#! /usr/bin/env python3
"""The user interface agnostic model of one editable configuration."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from collections.abc import Sequence
from copy import deepcopy
from io import StringIO
from pathlib import Path
from typing import Optional, TextIO
import sys
from config_as_json import Config, ConfigPath, PathOrStr
from edit_cfg_json.buffer import EditBuffer
from edit_cfg_json.descriptions import Descriptions, class_docstring, \
    class_summary
from edit_cfg_json.elements import declared_values
from edit_cfg_json.loader import ConfigLoader, ConfigSource
from edit_cfg_json.loading import LoadReport
from edit_cfg_json.rows import MemberRow
from edit_cfg_json.saving import NOTHING_KEPT, NOT_VALID, NO_DESTINATION, \
    KeptFile, SaveOutcome, SaveState, keep_previous, reload_refusal, \
    write_config
from edit_cfg_json.settings import Settings, SettingsSource, checked_file, \
    chosen_file, current_settings
from edit_cfg_json.validation import ValidationPass, ValidationVerdict, \
    subtree_answers, validate_buffer


# The model is where every piece of state that both backends read lives, so
# that two user interfaces of one application cannot disagree about any of
# it. That is design section 4 rather than an accident, and it is what makes
# the count of these one more than pylint's default.
# pylint: disable-next=too-many-public-methods
class EditModel:
    """The editable state of one `config_as_json.Config` object.

    The model does no input or output of its own and owns no event loop, so
    a backend can either be run by a convenience wrapper or be mounted as a
    widget by an application that already runs its own event loop.

    Leaf values are held in JSON space, so that an enum member is held as its
    name and a value being typed does not have to be a valid Python value
    yet. JSON space is about the kind of the value, not about its notation:
    a string member holds the string, and the quotes that the file format
    puts around it are added when the file is written and nowhere else.

    A member that holds a list, a dict or a nested configuration object is a
    tree of rows rather than one row, because what is inside one of those is
    edited a value at a time. Each of those rows is addressed by its own path,
    and every one of those nodes can be folded away, which is state of this
    model so that two backends cannot fold different things.

    How many things such a member holds is editable as well, because that is
    what a member of that shape exists to let the application's user decide. A
    new element is copied from what the class declares and never invented, and
    a node the editor has nothing to copy for offers nothing and says so.

    The buffer is validated by running the application's own configuration
    class over it rather than by any rule of the editor's own, so the user
    sees the diagnostics the application would produce and the editor cannot
    accept anything the application would refuse. Saving runs that same pass
    and writes the object it accepted, so nothing reaches the file that the
    application would not read back.

    What the editor says about the values it shows comes from the application
    and from its configuration class, and never from the editor: the
    docstring of the class labels the configuration object, and the
    description mapping labels the individual members. Both are optional, and
    whether they are shown is state of this model rather than of a backend.

    A member that `nested_configs()` declares is a node with a class and a
    docstring of its own, and its members are the rows below it. It is not
    shown as the dict it serializes to, because that would be showing it as
    something it is not, and everything inside it belongs to its own class:
    the parse converters that say what a value there means, and the members
    that class may leave out of a file.

    Such an object is also asked whether it is a configuration on its own,
    which folding it and every validation pass answer. That is a different
    state from the verdict of the whole configuration and is kept apart from
    it: a rule of the class above may relate two of these objects across the
    boundary between them, so both of them can be valid on their own while the
    configuration holding them cannot be saved.
    """

    # Every argument after the configuration object is an optional keyword,
    # and each of them says one independent thing about this session. See
    # the same disable on `edit`, which passes them on.
    # pylint: disable-next=too-many-arguments
    def __init__(self, config: Config, report: LoadReport = LoadReport(), *,
                 descriptions: Optional[Descriptions] = None,
                 loader: Optional[ConfigLoader] = None,
                 out_file: Optional[PathOrStr] = None,
                 settings: SettingsSource = Settings(),
                 stderr_file: TextIO = sys.stderr) -> None:
        """Read the JSON space values of one configuration object.

        The object is deep copied before it is serialized, because
        `Config.as_json_string()` validates, and a member validator returns
        the value that is stored back into the member. Serializing the
        caller's object directly could therefore change it, and the editor
        never mutates the caller's configuration object.

        The model does no input or output of its own, so the file was read
        before this and what reading it did arrives as the report.

        Args:
            config: Configuration object to edit. It is the source of both
                the member names and their values, and is not modified.
            report: What reading the input file did beyond reading the
                values. The default says there was no file to read.
            descriptions: What the application says about the members it
                declares, or None when it says nothing. A member that no
                description reaches is shown without one, which is all that
                saying nothing costs.
            loader: How this application constructs its configuration, or None
                when it did not say. The model needs it for two things. A save
                asks it whether the application would read back the file that
                is about to be written, which is the one question the
                validation of a buffer cannot answer; and it is asked here,
                with no JSON source, for the values the class declares, which
                is what a new element of an ordinary list is copied from. A
                class the editor cannot construct answers with nothing and
                loses that offer and nothing else.
            out_file: File that saving writes, or None when the user has not
                chosen one yet and the editor has to ask before it can save.
                It is taken exactly as it is, because a destination that was
                named in this call may be the input file and reading one
                file while writing another would be a surprise. A
                destination chosen later, with `set_out_file`, gets the
                extension of the application when it has none of its own.
            settings: What the application around the editor has already
                decided, or a callable that answers with it. The default is
                an application with no opinion.
            stderr_file: Stream used for user-facing diagnostics.

        Raises:
            InvalidConfiguration: The configuration object is not valid.
            InvalidConfigurationValue: A member of the configuration object
                does not hold a valid value.
        """
        own = deepcopy(config)
        self._source = ConfigSource(config=own, loader=loader)
        declared = declared_values(source=self._source, stream=StringIO())
        self._buffer = EditBuffer(config=own, report=report,
                                  descriptions=descriptions or {},
                                  stderr_file=stderr_file, defaults=declared)
        self._verdict: Optional[ValidationVerdict] = None
        self._settings = settings
        self._saving = SaveState(out_file=out_file)
        self._explained = True

    @property
    def _config_type(self) -> type[Config]:
        """Return the class of the configuration that is being edited.

        It is the class of the object the model was built on, whatever else
        an application's loader might have made of another file: which class
        this session is about was settled when that object was loaded.
        """
        return self._source.config_type

    @property
    def config_type_name(self) -> str:
        """Return the class name of the edited configuration object."""
        return self._config_type.__name__

    @property
    def summary(self) -> str:
        """Return the one line summary of the configuration class.

        It is the first paragraph of the docstring of that class, and it is
        empty when the class has no docstring of its own. It is short enough
        to be shown on a single row, which is why it stays visible while the
        rest of the explanatory text is hidden.
        """
        return class_summary(self._config_type)

    @property
    def docstring(self) -> str:
        """Return the whole docstring of the configuration class.

        It is empty when the class has none of its own. The docstring of a
        base class is deliberately not used in its place: a label that
        describes this library rather than the configuration would be worse
        than no label at all.
        """
        return class_docstring(self._config_type)

    @property
    def explanations_shown(self) -> bool:
        """Return whether the explanatory text is being shown in full.

        The summary of the configuration is shown either way, because it is
        one line for the whole configuration. What this answers is whether
        the rest of that docstring and the description of every member are
        shown as well, which is one line per member and is what a user who
        knows this configuration wants back.

        It belongs to the model rather than to a backend, so that an
        application cannot end up with two user interfaces that disagree
        about whether they are explaining themselves.
        """
        return self._explained

    def toggle_explanations(self) -> None:
        """Show the explanatory text if it is hidden, and hide it if not."""
        self._explained = not self._explained

    def toggle_fold(self, path: ConfigPath) -> None:
        """Fold one container away, or open it again.

        Which containers are folded belongs to the model, so that an
        application cannot end up with two user interfaces that are folded
        differently. Every row says whether it is folded and whether it is
        shown, which is where a backend reads it.

        Every nested configuration object at or inside that container is asked
        whether it is a configuration on its own at the same time, and what it
        refused is kept with the answer. That is the cheap local question, it
        needs no candidate configuration, and changing how much of a node is
        on the screen is the moment at which a user is looking at it.

        Every object inside it and not only the node itself, because the
        member that holds several objects is a list or a dict and is no
        configuration of its own. Folding one of those hides every object in
        it, so folding one of those has to ask every object in it.

        Args:
            path: Path of the container to fold or open.

        Raises:
            KeyError: The path is not a node of this configuration.
            ValueError: The node is not a container.
        """
        self._buffer.toggle_fold(path)
        self._ask_subtrees(path)

    def toggle_fold_all(self) -> None:
        """Fold every container away, or open every one of them.

        One action and not two, because a user who wants the values back
        wants all of them back: which of the two it does is decided by what
        is on the screen, so a press always changes something.

        Every nested configuration object is asked about itself, for the same
        reason folding one of them asks that one.
        """
        self._buffer.toggle_fold_all()
        self._ask_subtrees()

    def open_all(self, no_more_folding: bool = False) -> None:
        """Open every container, whatever is folded now.

        It is what a backend that shows the model once asks for, and the
        toggle above is what a user interface with a control offers: the
        toggle answers what the next press does, which is a question only a
        session that goes on can ask.

        Every nested configuration object is asked about itself, for the same
        reason folding one of them asks that one.

        Args:
            no_more_folding: Whether a container that a later pass creates is
                to be open as well. A validation pass can add one, and a new
                container is folded away when it is large, so a program that
                shows the buffer once and then ends asks for this and a
                session that a user is looking at does not.
        """
        self._buffer.open_all(no_more_folding=no_more_folding)
        self._ask_subtrees()

    def _ask_subtrees(self, path: ConfigPath = ()) -> None:
        """Say what the objects at or inside one node are on their own.

        Args:
            path: Path of the node to ask about, the empty path for the whole
                configuration. A node with no configuration object at it or
                inside it is left exactly as it was, because there is nothing
                there to ask.
        """
        self._buffer.take_subtrees(
            subtree_answers(config=self._source.config,
                            members=self._buffer.values(), inside=path))

    @property
    def settings(self) -> Settings:
        """Return what the application has decided, as it is now.

        A caller that handed over a callable is asked again here, which is
        what handing one over is for. What a later answer can change is
        worth knowing exactly: the key combinations are read once, when a
        backend builds its bindings, while the file name settings are read
        at every save and at every choice of a destination.

        Both backends read the settings from here rather than being given
        them, so that the two of them cannot bind different keys or offer
        the user different file names.
        """
        return current_settings(self._settings)

    @property
    def load_message(self) -> str:
        """Return what reading the input file did, empty when nothing.

        It cannot change while the editor runs, because the file was read
        before the model was built. Both backends show it, so that neither of
        them decides on its own what the user is told about the file.
        """
        return self._buffer.report.message

    @property
    def rows(self) -> Sequence[MemberRow]:
        """Return one row per node of the configuration, in the order shown.

        The members come in declaration order, which is the order the
        configuration class assigns them in and not the sorted order that the
        JSON file has. How the file is written is an implementation detail of
        saving; what the application declared is what the user thinks about.
        What a list or a dict holds follows the member that holds it, in the
        order that container holds it in.

        Every row is here whether it is folded away or not, because a backend
        creates its widgets once and hides the ones that are not shown, and
        each row says which of the two it is.

        The rows are a snapshot. Editing a member replaces its row, and a
        validation pass replaces all of them, so a row that a caller kept is
        the state at the time it was read.
        """
        return self._buffer.rows

    @property
    def dirty(self) -> bool:
        """Return whether the buffer holds anything that is worth saving.

        A save answers this question, so a buffer that has just been written
        is no longer dirty however much was typed into it before.
        """
        return self._buffer.dirty

    @property
    def out_file(self) -> Optional[PathOrStr]:
        """Return the file that saving writes, None when there is none yet.

        There is none when the editor was started neither on an input file
        nor on an output file, which is what happens when an application
        offers to write its very first configuration file. The editor then
        has to ask for a destination before it can save anything.
        """
        return self._saving.out_file

    @property
    def overwritten_file(self) -> Optional[PathOrStr]:
        """Return the existing file that saving now would overwrite, or None.

        There is one where a destination has been chosen, a file of that name
        is really there, and this session has not written it yet. That last
        condition is what makes this a question about the user's *own* work: a
        file this session has written is the user's earlier save, and there is
        nothing to say about overwriting one of those.

        It is what says whether a backend has anything to ask before it saves,
        and what the previous content is kept as is decided at the same moment
        and for the same file.
        """
        out_file = self._saving.out_file
        if out_file is None or Path(out_file) in self._saving.written_files:
            return None
        return out_file if Path(out_file).is_file() else None

    @property
    def save_outcome(self) -> Optional[SaveOutcome]:
        """Return what the last attempt to save did, or None when none.

        None is not a kind of failure but a third state, exactly as it is for
        the verdict: nothing has been saved since the buffer last changed.
        Whether an attempt succeeded is what a backend cannot read out of the
        message, and it is what decides how that message is shown.
        """
        return self._saving.outcome

    @property
    def save_message(self) -> str:
        """Return what the last attempt to save did, empty when none.

        It is dropped as soon as the buffer changes, for the same reason as
        the verdict: what an earlier buffer did when it was saved says
        nothing true about the buffer that is there now.
        """
        outcome = self._saving.outcome
        return outcome.message if outcome is not None else ''

    @property
    def saved_config(self) -> Optional[Config]:
        """Return the configuration object that was written, or None.

        This is what `edit()` gives back to the application, so that a
        caller needs no load of its own to work with what was saved. It is
        never the caller's own object, which the editor does not modify and
        which would otherwise be stale.
        """
        return self._saving.written

    @property
    def verdict(self) -> Optional[ValidationVerdict]:
        """Return what the last validation pass found, or None.

        None is not a kind of failure but a third state: the buffer has not
        been validated since it last changed. A verdict that was reached
        from an earlier buffer would say something untrue about the buffer
        that is there now, so it is dropped rather than kept.
        """
        return self._verdict

    def set_text(self, path: ConfigPath, text: str) -> None:
        """Set one node of the buffer from the text of an edit field.

        Text that the field already shows changes nothing, because it is not
        an edit. That is not only tidiness: a field posts a change when it is
        given its initial text, and a model that counted that as an edit
        would report unsaved changes before the user had touched anything.
        It is also what lets a backend write the buffer back into its fields
        after a validation pass without that counting as an edit.

        Every container the node is inside is brought up to date with it, so
        that what the whole configuration holds is always what its rows say.

        Args:
            path: Path of the node to set.
            text: Text that the edit field holds.

        Raises:
            KeyError: The path is not a node of this configuration.
            ValueError: The node is not one that this version can edit.
        """
        if self._buffer.set_text(path=path, text=text):
            self._changed()

    def add_element(self, path: ConfigPath, key: str = '') -> None:
        """Put one more element into a node that holds them.

        A new element is what the class of the configuration said one is,
        because it is the only thing that knows: an object of the declared
        class where a class declares that every element of a list or every
        value of a dict is one, and a copy of what the class declares for the
        member itself where it declares no such thing. The editor invents no
        value that the application never mentioned, and a node it has nothing
        to copy for offers nothing and says why.

        A declared member holding no configuration object is grown by being
        given the object it is for. That is adding rather than editing, for
        the reason a field cannot do it: no text typed into a field becomes a
        configuration object.

        Which nodes offer this is on the rows, as `MemberRow.offer`, so that
        two user interfaces of one application cannot offer different things.

        Args:
            path: Path of the node to put an element into.
            key: Name of the new entry of a dict, which only the user can
                give. It is empty for everything else, because an element of a
                list is addressed by where it is.

        Raises:
            KeyError: The path is not a node of this configuration.
            ValueError: Nothing can be added there, or the key is missing,
                unwanted, or one that dict already holds.
        """
        self._buffer.add_element(config=self._source.config, path=path,
                                 key=key)
        self._changed()

    def remove_element(self, path: ConfigPath) -> None:
        """Take one element out of the node that holds it.

        A declared optional member that holds an object is put back to holding
        none, which is the other half of what adding one does. A member that
        its class leaves out of the file altogether is not offered this: it
        would then have no row at all, and a member the editor had taken off
        the screen could never be given an object again.

        Args:
            path: Path of the element to remove.

        Raises:
            KeyError: The path is not a node of this configuration.
            ValueError: That node is not one that can be removed.
        """
        self._buffer.remove_element(config=self._source.config, path=path)
        self._changed()

    def move_element(self, path: ConfigPath, later: bool) -> None:
        """Make one element of a list change places with a neighbour.

        The order of a list is part of what the file says, so it is part of
        what an editor of that file has to be able to change. A dict has no
        such question, because it is written in the sorted order of its keys.

        Args:
            path: Path of the element to move.
            later: Whether it changes places with the one after it rather than
                with the one before it.

        Raises:
            KeyError: The path is not a node of this configuration.
            ValueError: That node cannot be moved that way.
        """
        self._buffer.move_element(config=self._source.config, path=path,
                                  later=later)
        self._changed()

    def _changed(self) -> None:
        """Drop what was true of the buffer before this change.

        A verdict and a save are about the values that were there when they
        were reached, so both of them say nothing true about a buffer that has
        changed since.
        """
        self._verdict = None
        self._saving.outcome = None

    def check_field(self, path: ConfigPath) -> None:
        """Report whether the text of one node means a value of it at all.

        This is what a backend calls when a field loses the focus, which is
        the moment at which the user has moved on from that field. It is
        deliberately not done on every change: the name of an enum member is
        no name of one for most of the time it takes to type it, and a field
        that reported that would be reporting a failure that is not one yet.

        Nor is it the validation of the whole configuration. It needs no
        candidate configuration and it answers a different question, which is
        whether this text means a value at all rather than whether the
        configuration is one the application would accept. Both are needed: a
        node this refuses is one the whole configuration would refuse too,
        but with a message about JSON that a person editing a field never
        asked about.

        Args:
            path: Path of the node to check.

        Raises:
            KeyError: The path is not a node of this configuration.
        """
        self._buffer.check_field(path)

    def set_out_file(self, out_file: PathOrStr) -> None:
        """Choose the file that saving writes from now on.

        This is the whole of what a backend's "save as" does before it
        saves, so that choosing a destination and writing to it stay two
        things and an application that mounts the model in a user interface
        of its own can offer them separately.

        A name that has no extension at all gets the one the application
        uses for its configuration, because a destination that is being
        chosen does not name a file that exists yet. A name that has the
        wrong extension is kept as it is and refused by the save that
        follows, so that the refusal is reported where every other refused
        save is reported and not through a second channel of its own.

        Args:
            out_file: File to write, with whatever name and extension the
                application and its user want. The editor has an opinion
                about the extension only where the application gave it one.
        """
        self._saving.out_file = chosen_file(name=out_file,
                                            settings=self.settings).name
        self._saving.outcome = None

    def validate(self) -> ValidationVerdict:
        """Run the application's own validation over the whole buffer.

        A validation pass is not read only. `Config.validate()` documents
        that a member validator returns the value that shall be stored back
        into the member, so a validator that changes the case of a string
        rewrites what the user typed. The buffer is therefore refreshed from
        the configuration object that was accepted, and every node the pass
        rewrote is marked: accepting the rewrite silently and showing the
        user the text they typed would be the worst available behaviour.

        A validator may also change how many values a container holds, which
        one that removes the duplicates of a list does, so the rows the pass
        leaves behind are not always the rows it was given.

        Returns:
            What the pass found. It is also kept, as `verdict`.
        """
        return self._validation_pass().verdict

    def save(self) -> SaveOutcome:
        """Write the buffer to the output file, if it can be written.

        Saving is validating and then writing, and it runs the very same
        pass that `validate` does, so a validator that rewrites a value
        rewrites it here too and the node says so afterwards. What reaches
        the file is therefore always what the editor is showing.

        A configuration the application would refuse is not written, because
        an editor that produced a file its own application cannot read would
        have failed at the one thing it is for. An application that said how
        it loads is asked that once more, with the text the file would hold,
        because a loader that chooses its class by looking at the JSON is the
        one case a validation pass cannot answer for. Nor is anything written
        when no destination has been chosen; the editor asks for one instead.
        Nor when the destination is a file name that the application does not
        use for its configuration, whether it was chosen here or named in
        the call that built this model.

        What the destination held before this session reached it is kept
        first, under the name the application chose for it, so that a save
        over somebody else's configuration does not take it away from them.

        A save that wrote the file leaves nothing to save, so the values
        that were written become the ones the buffer is compared against
        and the model stops reporting itself as dirty.

        Returns:
            Whether the file was written, and what to tell the user. It is
            also kept, as `save_message`.
        """
        # The settings are resolved once and passed on, because a callable
        # that answers with them is asked again at every point of use: one
        # save asking twice could check the name against one answer and keep
        # the previous content according to another.
        settings = self.settings
        out_file = self._saving.out_file
        if out_file is None:
            return self._record(SaveOutcome(saved=False,
                                            message=NO_DESTINATION))
        destination = checked_file(name=out_file, settings=settings)
        if destination.message:
            return self._record(SaveOutcome(saved=False,
                                            message=destination.message))
        candidate = self._validation_pass().candidate
        if candidate is None:
            return self._record(SaveOutcome(saved=False, message=NOT_VALID))
        refusal = reload_refusal(loader=self._source.loader, config=candidate)
        if refusal:
            return self._record(SaveOutcome(saved=False, message=refusal))
        return self._record(self._written(candidate=candidate,
                                          name=destination.name,
                                          settings=settings))

    def _written(self, candidate: Config, name: PathOrStr,
                 settings: Settings) -> SaveOutcome:
        """Keep what the destination holds, write it, and say what came of it.

        Args:
            candidate: Configuration object that the pass accepted.
            name: File to write, as the settings of the application leave it.
            settings: What the application has decided, as this save read it.

        Returns:
            Whether the file was written, and what to tell the user.
        """
        kept = self._kept_file(name=name, settings=settings)
        if kept.message:
            return SaveOutcome(saved=False, message=kept.message)
        outcome = write_config(config=candidate, out_file=name, kept=kept.name)
        if outcome.saved:
            self._keep_saved(candidate=candidate, name=name)
        return outcome

    def _kept_file(self, name: PathOrStr, settings: Settings) -> KeptFile:
        """Keep what one destination holds, unless this session wrote it.

        Args:
            name: File that is about to be written.
            settings: What the application has decided, as this save read it.

        Returns:
            Where the previous content went, or why it could not be kept.
        """
        if Path(name) in self._saving.written_files:
            return NOTHING_KEPT
        return keep_previous(name=name, settings=settings)

    def _validation_pass(self) -> ValidationPass:
        """Validate the buffer, refresh it, and keep what the pass found.

        The buffer is refreshed from the object the pass built and not from
        the object of the session, because that is where the accepted values
        are and because the nested configuration objects inside it are the
        ones that own them.

        What each nested object is on its own is written onto the rows after
        that refresh, because a pass can leave the model with other rows than
        it had and a state written onto the rows it had would be lost.
        """
        self._buffer.check_all()
        outcome = validate_buffer(config=self._source.config,
                                  members=self._buffer.values())
        if outcome.verdict.valid:
            assert outcome.candidate is not None
            self._buffer.take_validated(config=outcome.candidate,
                                        members=outcome.members)
        self._buffer.take_subtrees(outcome.subtrees)
        self._verdict = outcome.verdict
        return outcome

    def _record(self, outcome: SaveOutcome) -> SaveOutcome:
        """Keep what one attempt to save did, and hand it back."""
        self._saving.outcome = outcome
        return outcome

    def _keep_saved(self, candidate: Config, name: PathOrStr) -> None:
        """Make what was written the values that the buffer is compared to.

        The destination joins the files this session has written, which is
        what keeps the next save over it from keeping a backup of it and from
        asking about it: both of those are about the file somebody else left
        there, and that file is gone as soon as this session has written once.

        Args:
            candidate: Configuration object that reached the file.
            name: File that it reached.
        """
        self._saving.written = candidate
        self._saving.written_files.add(Path(name))
        self._buffer.keep_saved()
