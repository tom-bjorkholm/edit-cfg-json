#! /usr/bin/env python3
"""The user interface agnostic model of one editable configuration."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from collections.abc import Mapping, Sequence
from copy import deepcopy
from typing import NamedTuple, Optional, TextIO
import json
import sys
from config_as_json import Config, ConfigPath, JsonType, ParseConverter, \
    PathOrStr
from edit_cfg_json.converting import convert_member, member_converters
from edit_cfg_json.descriptions import Descriptions, class_docstring, \
    class_summary, member_description, optional_members
from edit_cfg_json.leaf_value import text_as_value, value_as_text, \
    values_differ
from edit_cfg_json.loader import ConfigLoader, ConfigSource
from edit_cfg_json.loading import LoadReport
from edit_cfg_json.saving import NOT_VALID, NO_DESTINATION, SaveOutcome, \
    SaveState, reload_refusal, write_config
from edit_cfg_json.settings import Settings, SettingsSource, checked_file, \
    chosen_file, current_settings
from edit_cfg_json.validation import ValidationPass, ValidationVerdict, \
    validate_buffer

NOT_EDITABLE_ERROR = 'Member {name} cannot be edited by this version.'
"""Message of the error raised when a member cannot be edited."""


class MemberRow(NamedTuple):
    """One configuration member as it appears in the JSON file."""

    path: ConfigPath
    """Path that addresses this member in the model.

    Every path of a flat configuration has one step. The further steps that
    lists, dicts and nested configuration objects need arrive together with
    those, and no call site has to change when they do.
    """

    value: JsonType
    """Current value of the member in JSON space, as the user edits it."""

    original: JsonType
    """Value that this member had when the file was last agreed with.

    That is when the model was built, and again after every save: what has
    just been written is what there is no longer anything to save about, so a
    save makes the written value the one the buffer is compared against.

    It is what the current value is compared against, and it is also the only
    type information that the model has. A PEP 526 annotation on an instance
    attribute is recorded nowhere at runtime, so the value that the
    configuration object holds is the only source of the type. Reading the
    type from the current value instead would not work: a number member that
    the user has half typed holds text for as long as the text is not a
    number yet, and the member would then stop being a number member. A save
    is safe to move it to, because only a validated value is ever written.
    """

    changed_by_validator: bool = False
    """Whether a validation pass rewrote this value.

    A validation pass sets the flag and the next edit of this member clears
    it, so it always answers the same question: is the value shown here
    something a validator made of what was typed? It belongs to the model
    rather than to a backend, so that two backends cannot show it
    differently.
    """

    filled_from_default: bool = False
    """Whether the declared defaults supplied this value.

    It is set when a load that was allowed to use the defaults filled in a
    member the input file did not hold, and it stays set for the rest of the
    session: that the file did not hold this value remains true whatever the
    user then types into it. It belongs to the model for the same reason as
    the flag above, so that two backends cannot show it differently.
    """

    load_reason: str = ''
    """What reading the input file did to this member, empty when nothing.

    Reading a file is not always only reading it. A class that declares rules
    for reading an older format may have supplied this value or renamed a key
    of the file into this member, and parsing or validating may have
    normalized what the file held. The user has to be told, because the value
    shown is then not the value in the file.

    It says which of those things happened wherever the load recorded it, and
    says that the value is not the file's where it did not, which is the whole
    of what a comparison can know. It stays as it is for the rest of the
    session, exactly as the flag above does and for the same reason, and the
    two are never both there: what the declared defaults filled in is said by
    that flag, which says more than this would.
    """

    description: str = ''
    """What is said about this member, empty when nothing is.

    The application says most of it, in the description mapping, and the type
    of the member says the rest: the names an enum accepts, or what kind of
    value the member holds, and whether the class may leave it out of the file.
    It is read once, when the model is built, because it says what the member
    is for and that does not change while it is edited.

    It is empty only for a member the editor cannot edit yet, whose row says
    which kind of container it is where its value would be. Every other member
    has at least what its own type says about it.
    """

    converter: Optional[ParseConverter] = None
    """How the text of this member becomes the value that is stored in it.

    It is None for a member that holds what the file holds, which is most of
    them. It is what says that a member holds an enum, and that answers two
    questions: which names the description of the member lists, and whether
    the text the field holds means a value of this member at all.
    """

    conversion: str = ''
    """Why the text of this member means no value of it, empty when it does.

    It is answered by this member alone, which is what makes it a different
    thing from what a validation pass says about it: it stays true until this
    member is edited again, whatever happens to the rest of the buffer. It is
    set when the user leaves the field and again by every validation pass, and
    the next edit of this member clears it.
    """

    @property
    def name(self) -> str:
        """Return the name of the member, the last step of its path."""
        return self.path[-1]

    @property
    def editable(self) -> bool:
        """Return whether this member is a scalar that can be edited.

        A list or a dict value is ordinary JSON structure that needs a tree
        of fields rather than a single field, which this version of the
        model does not have. Such a member is still reported as a row, so
        that no configuration member can silently go missing.
        """
        return not isinstance(self.original, (dict, list))

    @property
    def is_text(self) -> bool:
        """Return whether this member holds text.

        This is the difference between a value that is text and a value
        whose text is a rendering of it. The text of a text member is the
        value itself, while the text of a number is how the number is
        written.
        """
        return isinstance(self.original, str)

    @property
    def edited(self) -> bool:
        """Return whether this member holds something that is not saved yet.

        A member is changed when it would now be written to the file
        differently, and not when it merely was typed in. Typing a value
        back to what it was leaves nothing to save, and an editor that still
        claimed to have changes would be telling the user something untrue.
        Saving says the same thing about every member at once.
        """
        return values_differ(self.value, self.original)


def _ordered_names(config: Config, members: dict[str, JsonType]) -> list[str]:
    """Return the serialized member names in the order they are declared.

    The declaration order is the order in which the configuration class
    assigns its members, which `vars()` preserves. That is the order the
    application thinks about its configuration in, so it is the order the
    editor shows. The JSON document cannot supply it, because
    `config_as_json` writes its keys sorted.

    A member that the class omits from JSON while its value is `None` is
    not serialized and so gets no row. A serialized name that is not an
    attribute of the object is appended instead of dropped, so that no
    member can go missing whatever a validator or a converter did.
    """
    declared = [name for name in vars(config) if name in members]
    return declared + [name for name in members if name not in declared]


def _row_of(name: str, value: JsonType, report: LoadReport, about: str,
            converter: Optional[ParseConverter]) -> MemberRow:
    """Return the row of one serialized member of a configuration.

    Args:
        name: Name of the member, which is the one step of its path while
            every member of the configuration is a scalar.
        value: JSON space value that the member holds.
        report: What reading the input file did, which says whether this
            member holds a value that came from the file.
        about: Everything there is to say about this member, empty for a
            member that nothing says anything about.
        converter: How the text of this member becomes a value, or None.

    Returns:
        The row of that member, as the model starts out holding it.
    """
    return MemberRow(path=(name,), value=value, original=value,
                     filled_from_default=name in report.filled,
                     load_reason=report.reasons.get(name, ''),
                     description=about, converter=converter)


def _about(name: str, members: Mapping[str, JsonType],
           descriptions: Descriptions,
           converters: Mapping[str, ParseConverter],
           optional: frozenset[str]) -> str:
    """Return everything there is to say about one member.

    Args:
        name: Name of the member, which is the one step of its path.
        members: One JSON space value per serialized member.
        descriptions: What the application says about its members.
        converters: One converter per member that has one.
        optional: Names of the members the class may leave out of the file.

    Returns:
        The description of that member.
    """
    return member_description(descriptions=descriptions, path=(name,),
                              converter=converters.get(name),
                              value=members[name], optional=name in optional)


def _rows_from_config(config: Config, report: LoadReport,
                      descriptions: Descriptions,
                      converters: Mapping[str, ParseConverter],
                      stderr_file: TextIO) -> dict[ConfigPath, MemberRow]:
    """Return one row per serialized member, by path, in declaration order.

    A mapping by path is what the design asks for, because every leaf is
    addressed by its path and no other name for it is needed. A dictionary
    keeps the order it was built in, so the declaration order the rows are
    shown in survives being a mapping.
    """
    members = json.loads(config.as_json_string(stderr_file=stderr_file))
    assert isinstance(members, dict)
    optional = optional_members(config)
    return {(name,): _row_of(name=name, value=members[name], report=report,
                             converter=converters.get(name),
                             about=_about(name=name, members=members,
                                          descriptions=descriptions,
                                          converters=converters,
                                          optional=optional))
            for name in _ordered_names(config=config, members=members)}


def _refreshed(row: MemberRow, members: Mapping[str, JsonType]) -> MemberRow:
    """Return one row as a validated configuration object left it.

    A member that the validated object does not serialize keeps the value
    the buffer holds. That happens when a validator sets a member the class
    leaves out of JSON while it is None, and there is then no value to read
    back rather than a value that changed.

    Args:
        row: Member as the buffer holds it.
        members: One JSON space value per member of the validated object.

    Returns:
        The row, marked as rewritten when the validation changed its value.
    """
    value = members.get(row.name, row.value)
    if not values_differ(value, row.value):
        return row
    return row._replace(value=value, changed_by_validator=True)


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

    This version of the model handles scalar members only. A member whose
    value is a list or a dict is reported as a row that is not editable.
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
                when it did not say. The model needs it for one thing only: a
                save asks it whether the application would read back the file
                that is about to be written, which is the one question the
                validation of a buffer cannot answer.
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
        self._report = report
        self._rows = _rows_from_config(config=own, report=report,
                                       descriptions=descriptions or {},
                                       converters=member_converters(own),
                                       stderr_file=stderr_file)
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
        return self._report.message

    @property
    def rows(self) -> Sequence[MemberRow]:
        """Return one row per configuration member, in declaration order.

        Declaration order is the order the configuration class assigns its
        members in, and not the sorted order that the JSON file has. How
        the file is written is an implementation detail of saving; what the
        application declared is what the user thinks about.

        The rows are a snapshot. Editing a member replaces its row, so a row
        that a caller kept is the state at the time it was read.
        """
        return tuple(self._rows.values())

    @property
    def dirty(self) -> bool:
        """Return whether the buffer holds anything that is worth saving.

        A save answers this question, so a buffer that has just been written
        is no longer dirty however much was typed into it before.
        """
        return any(row.edited for row in self._rows.values())

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
        """Set one member of the buffer from the text of an edit field.

        Text that the field already shows changes nothing, because it is not
        an edit. That is not only tidiness: a field posts a change when it is
        given its initial text, and a model that counted that as an edit
        would report unsaved changes before the user had touched anything.
        It is also what lets a backend write the buffer back into its fields
        after a validation pass without that counting as an edit.

        Args:
            path: Path of the member to set.
            text: Text that the edit field holds.

        Raises:
            KeyError: The path is not a member of this configuration.
            ValueError: The member is not one that this version can edit.
        """
        row = self._rows[path]
        if not row.editable:
            raise ValueError(NOT_EDITABLE_ERROR.format(name=row.name))
        if value_as_text(row.value) == text:
            return
        value = text_as_value(text=text, is_text_member=row.is_text)
        self._rows[path] = row._replace(value=value, conversion='',
                                        changed_by_validator=False)
        self._verdict = None
        self._saving.outcome = None

    def check_field(self, path: ConfigPath) -> None:
        """Report whether the text of one member means a value of it at all.

        This is what a backend calls when a field loses the focus, which is
        the moment at which the user has moved on from that field. It is
        deliberately not done on every change: the name of an enum member is
        no name of one for most of the time it takes to type it, and a field
        that reported that would be reporting a failure that is not one yet.

        Nor is it the validation of the whole configuration. It needs no
        candidate configuration and it answers a different question, which is
        whether this text means a value at all rather than whether the
        configuration is one the application would accept. Both are needed: a
        member this refuses is one the whole configuration would refuse too,
        but with a message about JSON that a person editing a field never
        asked about.

        Args:
            path: Path of the member to check.

        Raises:
            KeyError: The path is not a member of this configuration.
        """
        row = self._rows[path]
        converted = convert_member(converter=row.converter, value=row.value)
        self._rows[path] = row._replace(conversion=converted.message)

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
        the configuration object that was accepted, and every member the
        pass rewrote is marked: accepting the rewrite silently and showing
        the user the text they typed would be the worst available behaviour.

        Returns:
            What the pass found. It is also kept, as `verdict`.
        """
        return self._validation_pass().verdict

    def save(self) -> SaveOutcome:
        """Write the buffer to the output file, if it can be written.

        Saving is validating and then writing, and it runs the very same
        pass that `validate` does, so a validator that rewrites a value
        rewrites it here too and the member says so afterwards. What reaches
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

        A save that wrote the file leaves nothing to save, so the values
        that were written become the ones the buffer is compared against
        and the model stops reporting itself as dirty.

        Returns:
            Whether the file was written, and what to tell the user. It is
            also kept, as `save_message`.
        """
        out_file = self._saving.out_file
        if out_file is None:
            return self._record(SaveOutcome(saved=False,
                                            message=NO_DESTINATION))
        destination = checked_file(name=out_file, settings=self.settings)
        if destination.message:
            return self._record(SaveOutcome(saved=False,
                                            message=destination.message))
        candidate = self._validation_pass().candidate
        if candidate is None:
            return self._record(SaveOutcome(saved=False, message=NOT_VALID))
        refusal = reload_refusal(loader=self._source.loader, config=candidate)
        if refusal:
            return self._record(SaveOutcome(saved=False, message=refusal))
        outcome = write_config(config=candidate, out_file=destination.name)
        if outcome.saved:
            self._keep_saved(candidate)
        return self._record(outcome)

    def _validation_pass(self) -> ValidationPass:
        """Validate the buffer, refresh it, and keep what the pass found."""
        self._check_fields()
        outcome = validate_buffer(config=self._source.config,
                                  members=self._buffer())
        if outcome.verdict.valid:
            self._take_validated(outcome.members)
        self._verdict = outcome.verdict
        return outcome

    def _check_fields(self) -> None:
        """Report every member whose text means no value of that member.

        A validation pass answers this for the whole buffer at once, so the
        answer that one field gives when it is left is refreshed for all of
        them here. A member the user never visited is then reported exactly
        as one they typed into and left.
        """
        for path in tuple(self._rows):
            self.check_field(path)

    def _record(self, outcome: SaveOutcome) -> SaveOutcome:
        """Keep what one attempt to save did, and hand it back."""
        self._saving.outcome = outcome
        return outcome

    def _keep_saved(self, candidate: Config) -> None:
        """Make what was written the values that the buffer is compared to.

        The mark of a member a validator rewrote is deliberately left alone.
        That a value is not literally the one the user typed stays true after
        it has been saved, and it is the mark that says so.
        """
        self._saving.written = candidate
        self._rows = {path: row._replace(original=row.value)
                      for path, row in self._rows.items()}

    def _buffer(self) -> dict[str, JsonType]:
        """Return the buffer as one JSON space value per member.

        Every member of a flat configuration is named by the single step of
        its path. The members inside lists, dicts and nested configuration
        objects arrive together with the further steps that address them.
        """
        return {row.name: row.value for row in self._rows.values()}

    def _take_validated(self, members: Mapping[str, JsonType]) -> None:
        """Refresh the buffer from the configuration object that was built."""
        self._rows = {path: _refreshed(row=row, members=members)
                      for path, row in self._rows.items()}
