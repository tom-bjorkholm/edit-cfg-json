# Configuration files for the examples

These are input files for the `-i` option of the
[example programs](../src/example/README.md). Some of them can be opened for
editing and some of them cannot, because being told clearly why a file cannot
be opened is as much a part of an editor as editing is.

They live outside [examples/src/](../src/) because they are data and not
Python. Nothing in this folder is part of the installed packages.

None of them is ever written to. An example that is asked to save writes the
file that `-o` names, or the file that `-i` names when there is no `-o`, so
copy one of these somewhere else first if you want to try the round trip over
its own input file.

## Files for `e01_flat_config.py`

`FlatConfig` declares one text member `name` and one number member `answer`,
and `answer` has to be a whole number between 0 and 100.

| File | What happens |
| --- | --- |
| [e01_complete.json](e01_complete.json) | Opens. Both values come from the file, so no member is marked. |
| [e01_incomplete.json](e01_incomplete.json) | Opens under the default policy and under `--policy defaults`: `answer` is filled in from the declared default and marked as such. Refused under `--policy strict`. |
| [e01_unknown_key.json](e01_unknown_key.json) | Refused under every policy. `colour` is not a member of this configuration, and dropping it would lose whatever the file meant by it. |
| [e01_not_json.json](e01_not_json.json) | Refused under every policy. The file is not JSON at all, which the diagnostics below the message say. |
| [e01_bad_value.json](e01_bad_value.json) | Refused under every policy. The keys are right and `answer` is outside the allowed range. |

## Files for `e02_enum_config.py`

`EnumConfig` declares two enum members, `needed` and `available`, both of
which are written to the file as the name of an enum member.

| File | What happens |
| --- | --- |
| [e02_complete.json](e02_complete.json) | Opens with both names from the file. |
| [e02_incomplete.json](e02_incomplete.json) | Opens under the default policy: `available` is filled in from the declared default and marked. Refused under `--policy strict`. |
| [e02_bad_enum.json](e02_bad_enum.json) | Refused under every policy. `ELECT` is the beginning of both `ELECTRICAL` and `ELECTRONIC`, so it names no member, and the diagnostics list the three names that exist. |

## Files for `e03_described_config.py`

`DescribedConfig` declares two text members, one number member and one enum
member, and the mapping of that example describes three of the four.

| File | What happens |
| --- | --- |
| [e03_complete.json](e03_complete.json) | Opens with every value from the file. The descriptions are text about the members and not part of them, so a file holds exactly what the other examples' files hold. |

## Files for `e04_validated_config.py`

`ValidatedConfig` declares one text member and two number members, with a
rule about each of them and one further rule about how long the whole job can
take.

| File | What happens |
| --- | --- |
| [e04_complete.json](e04_complete.json) | Opens with every value from the file, and every rule is satisfied: two attempts of 300 seconds is 600, which is under the 900 that all the attempts together may take. |

## Files for `e05_old_format_config.py`

`OldFormatConfig` reads files written by an older version of its application,
which renamed one member, dropped one key and added one. `NoHookConfig` beside
it in that example is the same configuration by a class that cannot report what
the reading did.

| File | What happens |
| --- | --- |
| [e05_old_format.json](e05_old_format.json) | Opens under every policy, and reading it changes it: `title` becomes `report_name`, `debug_trace` is dropped, `format_version` is supplied, and the case of `owner` is corrected by a validator. Every member that is not what the file holds is marked, and the message names the older keys. |
| [e05_current.json](e05_current.json) | Opens with every value from the file and nothing said about the load, because nothing happened to it. It is the same configuration as the file above, in the shape that saving that file writes. |

## Files for `e06_factory_config.py`

`TeamConfig` is told which teams exist when it is constructed, so the editor
cannot construct it and reads its files through a loader instead.

| File | What happens |
| --- | --- |
| [e06_teams.json](e06_teams.json) | Opens through the loader of that example, with both values from the file. Without a loader the same file is refused, because the editor knows nothing about the list of teams that the class needs. |

## Files for `e07_chosen_class.py`

`Cad2DConfig` and `Cad3DConfig` hold the same three members and differ in the
finest grid each of them allows. The loader of that example looks at `mode` to
decide which of the two a file holds.

| File | What happens |
| --- | --- |
| [e07_drawing.json](e07_drawing.json) | Opens as `Cad2DConfig`, on a grid finer than a model may use. Editing `mode` to `3D` and saving is refused, because the model class would not read this grid back. |
| [e07_model.json](e07_model.json) | Opens as `Cad3DConfig`. Editing `mode` to `2D` and saving is refused as well, and for the other reason: that file would be read as the drawing class, which is not the class this session is about. |

## Files for `e08_lists_and_dicts.py`

`ContainerConfig` declares one text member and four members that hold a list
or a dict of values, which the editor shows as a tree of rows.

| File | What happens |
| --- | --- |
| [e08_complete.json](e08_complete.json) | Opens with every value from the file. `many_labels` holds two elements here rather than the twelve the class declares, so it opens unfolded: how many rows a container would add is what decides that, and not which member it is. |
| [e08_short_list.json](e08_short_list.json) | Opens with the declared values of every member but `many_labels`, which holds one element. It is the file to try `--fold` and `--toggle-fold` against, because nothing in it starts folded. |

## Files for `e09_nested_config.py`

`CourseExportConfig` holds one plain member and two nested `Config` objects of
the same class, one of which may be absent altogether.

| File | What happens |
| --- | --- |
| [e09_with_audit.json](e09_with_audit.json) | Opens with both nested objects present, so the optional one is a node with rows of its own rather than the `no TableOutputConfig` that the declared defaults show. Its format and its encoding differ from the other output's, which is what two objects of one class are for. |

## Files for `e10_config_containers.py`

`CourseReportsConfig` holds one plain member, a list whose elements are
`ReportOutputConfig` objects and a dict whose values are more of them.

| File | What happens |
| --- | --- |
| [e10_reports.json](e10_reports.json) | Opens with two reports in the list and three in the dict, rather than the three and two the class declares. That folds the other one of the two containers: how many rows opening a container would add is what decides which of them opens folded, and neither the member nor the declared default has anything to do with it. |

## Files for `e11_add_remove.py`

`PipelineConfig` holds every shape a member that has several of something can
have, so that what can be added to each of them can be read side by side.

| File | What happens |
| --- | --- |
| [e11_pipeline.json](e11_pipeline.json) | Opens with two machines in `extra_hosts`, which the declared defaults leave empty. That is what makes the member extendable: nothing declares what one host looks like, so the editor has nothing to copy until the file gives it one. It also holds three stages rather than two and an `audit` stage rather than none. |

## Files for `e12_backup_files.py`

`ArchiveConfig` declares one text member, one number member and one true or
false member. That example is not about them: it is about what becomes of the
file when a save writes over it.

| File | What happens |
| --- | --- |
| [e12_archive.cfg](e12_archive.cfg) | Opens with every value from the file. It is the one data file with another extension, because that application uses `.cfg` for its configuration. Copy it somewhere else before saving over it, which is what the example says to do: the round trip is what keeps the previous content beside the file as `archive.cfg.old_1`. |

## Files for the four examples that mount the editor

`PipelineConfig` declares one text member and one number member.
`e13_embedded_tk.py`, `e14_embedded_textual.py`, `e15_window_tk.py` and
`e16_screen_textual.py` are not about them either: they are about where the
editor is in an application that already runs a user interface.

| File | What happens |
| --- | --- |
| [e13_pipeline.json](e13_pipeline.json) | Opens with both values from the file. It is one file for all four examples, because they are two applications in two toolkits each and the point of reading it at all is that the editor is told which file to read in the same call that says where it goes. It keeps its name from the example it was written for. |

## Files for `e17_settings_config.py`

`ToolConfig` declares one text member, one true-or-false member and one member
holding a whole `edit_cfg_json.SettingsConfig`.

| File | What happens |
| --- | --- |
| [e17_tool.json](e17_tool.json) | Opens with every value from the file, including a whole settings block: another backup suffix, three of them kept, an extension for this tool's files and `ctrl+w` for Save. It holds every member of `SettingsConfig` because a nested configuration object is read whole whatever policy the parse around it was given, which is the one thing about this example that a shorter file would have hidden. |

## Why a file with a bad value cannot be opened

An editor that refused to open the very file that has to be repaired would
be unhelpful, so this is a deliberate decision and not an oversight. A member
validator returns the value that is stored back into the member, so a load
that stopped part way through leaves it unknown which values were already
rewritten and which were not. Showing that half converted state as if it were
the file would be worse than saying plainly that the file has to be corrected
in a text editor first.
