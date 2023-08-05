"""
    formelsammlung.venv_utils
    ~~~~~~~~~~~~~~~~~~~~~~~~~

    Utility function for working with virtual environments.

    :copyright: (c) 2020, Christian Riedel and AUTHORS
    :license: GPL-3.0-or-later, see LICENSE for details
"""  # noqa: D205,D208,D400
import contextlib
import os
import shutil
import sys

from pathlib import Path
from typing import Optional, Tuple, Union


OS_BIN = "Scripts" if sys.platform == "win32" else "bin"


def get_venv_path() -> Path:
    """Get path to the venv from where the python executable runs.

    :raises FileNotFoundError: when no calling venv can be detected.
    :return: Return venv path
    """
    if hasattr(sys, "real_prefix"):
        return Path(
            sys.real_prefix  # type: ignore[no-any-return,attr-defined]  # noqa: E1101
        )
    if sys.base_prefix != sys.prefix:
        return Path(sys.prefix)
    raise FileNotFoundError("No calling venv could be detected.")


def get_venv_bin_dir(venv_path: Union[str, Path]) -> Path:
    """Return path to bin/Scripts dir of given venv.

    :param venv_path: Path to venv
    :raises FileNotFoundError: when no bin/Scripts dir can be found for given venv.
    :return: Path to bin/Scripts dir
    """
    bin_dir = Path(venv_path) / OS_BIN
    if bin_dir.is_dir():
        return bin_dir

    raise FileNotFoundError(f"Given venv has no '{OS_BIN}' directory.")


def get_venv_tmp_dir(
    venv_path: Union[str, Path],
    search_tmp_dirs: Optional[Tuple[str]] = None,
    create_if_missing: bool = False,
    create_dir_name: Optional[str] = None,
) -> Path:
    """Return path to tmp/temp dir of given venv.

    :param venv_path: Path to venv
    :param search_tmp_dirs: List of temp dir names to look for;
        defaults to ("tmp", "temp", ".tmp", ".temp")
    :param create_if_missing: Create a temp dir in the given venv if non exists;
        defaults to ``False``
    :param create_dir_name: Name of the venv to create; defaults to ``tmp``
    :raises FileNotFoundError: when no tmp/temp dir can be found for given venv.
    :return: Path to tmp/temp dir
    """
    tmp_dirs = search_tmp_dirs if search_tmp_dirs else ("tmp", "temp", ".tmp", ".temp")
    for tmp_dir in tmp_dirs:
        tmp_path = Path(venv_path) / tmp_dir
        if tmp_path.is_dir():
            return tmp_path

    if create_if_missing:
        tmp_path = Path(venv_path) / (create_dir_name if create_dir_name else "tmp")
        tmp_path.mkdir(exist_ok=True)
        return tmp_path

    raise FileNotFoundError(f"Given venv has non of theses directories: {tmp_dirs}.")


def get_venv_site_packages_dir(venv_path: Union[str, Path]) -> Path:
    """Return path to site-packages dir of given venv.

    :param venv_path: Path to venv
    :raises FileNotFoundError: when no site-packages dir can be found for given venv.
    :return: Path to site-packages dir
    """
    paths = list(Path(venv_path).glob("**/site-packages"))
    if paths:
        return paths[0]

    raise FileNotFoundError("Given venv has no 'site-packages' directory.")


def where_installed(program: str) -> Tuple[int, Optional[str], Optional[str]]:
    """Find installation locations for given program.

    Return exit code and locations based on found installation places.
    Search in current venv and globally.

    Exit codes:

    - 0 = nowhere
    - 1 = venv
    - 2 = global
    - 3 = both

    :param program: Program to search
    :return: Exit code, venv executable path, glob executable path
    """
    exit_code = 0

    glob_exe = exe = shutil.which(program)
    if not exe:
        return exit_code, None, None

    venv_path = None
    with contextlib.suppress(FileNotFoundError):
        venv_path = get_venv_path()

    if venv_path is not None:
        path = os.pathsep.join(
            p
            for p in os.environ["PATH"].split(os.pathsep)
            if Path(p) != venv_path / OS_BIN
        )
        glob_exe = shutil.which(program, path=path)

    if glob_exe is None:
        exit_code += 1
    elif exe == glob_exe:
        exit_code += 2
        exe = None
    else:
        exit_code += 3

    return exit_code, exe, glob_exe
