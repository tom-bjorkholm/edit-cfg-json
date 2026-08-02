
"""Repository-specific build specification for common_build_tools."""

from pathlib import Path
from typing import Optional
import sys
from build_spec import BuildSpec

CUSTOM_BUILD_TOOLS_SRC = Path(__file__).resolve().parent / 'src'
sys.path.insert(0, str(CUSTOM_BUILD_TOOLS_SRC))
# The generator lives in this repository, not in the shared build tools,
# so its folder has to be on sys.path before the import can work.
# pylint: disable-next=wrong-import-position
from create_pypi_readme import create_pypi_readme_cmd  # noqa: E402


def custom_spec() -> Optional[BuildSpec]:
    """Return custom build spec for this repository."""
    return BuildSpec(python_layout_max_name_length=25,
                     custom_after_test=[create_pypi_readme_cmd])
