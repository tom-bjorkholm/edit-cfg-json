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

## Why a file with a bad value cannot be opened

An editor that refused to open the very file that has to be repaired would
be unhelpful, so this is a deliberate decision and not an oversight. A member
validator returns the value that is stored back into the member, so a load
that stopped part way through leaves it unknown which values were already
rewritten and which were not. Showing that half converted state as if it were
the file would be worse than saying plainly that the file has to be corrected
in a text editor first.
