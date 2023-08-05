"""
    formelsammlung.tox_env_exe_runner
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Call tools from tox environments.

    :copyright: (c) 2020, Christian Riedel and AUTHORS
    :license: GPL-3.0-or-later, see LICENSE for details
"""  # noqa: D205,D208,D400
import subprocess  # noqa: S404
import sys

from pathlib import Path
from typing import List, Optional


IS_WIN = sys.platform == "win32"
EXE = "Scripts/{tool}.exe" if IS_WIN else "bin/{tool}"


def _check_runner_envs(venv_runner: str, envs: List[str], tool: str) -> Optional[Path]:
    """Check if executable is found in any of the envs for given env runner."""
    for env in envs:
        path = Path(f".{venv_runner}") / env / EXE.format(tool=tool)
        if path.is_file():
            return path
    return None


def _check_venv(venv: str, tool: str) -> Optional[Path]:
    """Check if executable is found in venv."""
    path = Path(venv) / EXE.format(tool=tool)
    if path.is_file():
        return path
    return None


def env_exe_runner(
    venv_runner: List[str],
    envs: List[str],
    tool: str,
    tool_args: Optional[List[str]] = None,
) -> int:
    """Call given ``tool`` from given `tox` or `nox` or `virtual` env considering OS.

    :param venv_runner: List containing: 'nox' and/or 'tox' and/or one or more
        'virtual environment's
    :param envs: List of environments to search the ``tool`` in when 'tox' or 'nox' is
        in venv_runner. If neither 'tox' nor 'nox' is in ``venv_runner`` you may pass
        an empty list.
    :param tool: Name of the executable to run.
    :param tool_args: Arguments to give to the ``tool``.
    :return: Exit code 127 if no executable is found or the exit code of the called cmd.
    """
    cmd_path = None
    error_msgs = []

    for runner in venv_runner:

        if runner in ("tox", "nox"):
            error_msgs.append(f"- '{runner}' envs: {envs}")
            cmd_path = _check_runner_envs(runner, envs, tool)
        else:
            error_msgs.append(f"- virtual env: ['{runner}']")
            cmd_path = _check_venv(runner, tool)

        if cmd_path is not None:
            break

    if cmd_path is None:
        print(f"No '{tool}' executable found. Searched in:")
        for msg in error_msgs:
            print(msg)
        return 127

    return subprocess.call([str(cmd_path), *(tool_args or [])])  # noqa: S603


def cli_caller() -> int:
    """Warp ``env_exe_runner`` to be callable by cli.

    Script to call executables in `tox`/`nox`/`virtual` envs considering OS.

    The script takes three mandatory arguments:

    1. A string with comma separated runner (`tox` and/or `nox`) and/or virtual envs.
    2. A string with comma separated `tox`/`nox` envs to check for the executable.
       The envs are checked in given order. If `tox`/`nox` are not part of the first arg
       you may pass a '-' as second arg.
    3. The executable to call like e.g. `pylint`.

    All other arguments after are passed to the tool on call.

    :return: Exit code from ``env_exe_runner``
    """
    return env_exe_runner(
        sys.argv[1].split(","), sys.argv[2].split(","), sys.argv[3], sys.argv[4:]
    )  # pragma: no cover


if __name__ == "__main__":
    sys.exit(cli_caller())
