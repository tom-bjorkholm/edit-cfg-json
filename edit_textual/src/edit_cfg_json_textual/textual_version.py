#! /usr/bin/env python3
"""What `edit-cfg-json-textual` answers `--version` with.

The report of this package is the report of the core with this distribution in
front of it, because that is the package whoever runs this program installed
and the one an upgrade instruction has to name. `textual` is added at the end,
which is the one dependency this package has that the core has not, and
everything between the two is inherited rather than written again.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from edit_cfg_json import EcajVersionReporter

MAIN_PACKAGE = 'edit-cfg-json-textual'
"""Distribution that this program is installed from."""


class TextualVersionReporter(EcajVersionReporter):
    """Report what this package and everything below it are."""

    def package_names(self) -> list[str]:
        """Return the distributions whose versions are reported.

        Returns:
            This distribution first, then the ones the core lists, and last
            the user interface library that only this package needs.
        """
        return [MAIN_PACKAGE, *super().package_names(), 'textual']

    @classmethod
    def get_main_package_name(cls) -> str:
        """Return the distribution that the upgrade instructions name.

        Returns:
            What to install to upgrade the program that is running.
        """
        return MAIN_PACKAGE
