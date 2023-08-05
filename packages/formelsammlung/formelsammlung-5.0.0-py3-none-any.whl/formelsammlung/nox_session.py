"""
    formelsammlung.nox_session
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

    Monkypatched ``nox`` session object.

    :copyright: (c) 2020, Christian Riedel and AUTHORS
    :license: GPL-3.0-or-later, see LICENSE for details
"""  # noqa: D205,D208,D400
from typing import Any, Callable, Dict, Optional

from nox.sessions import CondaEnv, PassthroughEnv
from nox.sessions import Session as _Session
from nox.sessions import VirtualEnv

from formelsammlung.venv_utils import where_installed


def _monkeypatch_session(session_func: Callable) -> Callable:
    """Decorate nox session functions to add ``poetry_install`` method.

    :param session_func: decorated function with commands for nox session
    """

    def switch_session_class(session: "Session", **kwargs: Dict[str, Any]) -> None:
        """Call session function with session object overwritten by custom one.

        :param session: nox session object
        :param kwargs: keyword arguments from e.g. parametrize
        """
        session = Session(session._runner)  # noqa: W0212
        session_func(session=session, **kwargs)

    #: Overwrite name and docstring to imitate decorated function for nox
    switch_session_class.__name__ = session_func.__name__
    switch_session_class.__doc__ = session_func.__doc__

    return switch_session_class


session_w_poetry = _monkeypatch_session
session_w_poetry.__doc__ = """Decorator function for ``nox`` session fcuntions.

The decorator replaces ``nox``'s own :class:`nox.sessions.Session` class with
``formelsammlung``'s :class:`Session` class. The later introduces the
:meth:`Session.poetry_install` method for easier usage of ``nox`` with ``poetry``
managed projects.

The decorator **must** come after ``nox``'s :func:`nox.session` decorator as it takes
the :class:`nox.sessions.Session` object given by :func:`nox.session` as its argument
to change it.

Example::

    import nox
    from formelsammlung.nox_session import session_w_poetry

    @nox.session
    @session_w_poetry
    def some_nox_session(session):
        ...

:param session_func: decorated function with commands for nox session. This argument is
    automatically provided by python. You must not provide it yourself.
"""


class Session(_Session):  # noqa: R0903
    """Subclass of nox's Session class to add ``poetry_install`` method."""

    def poetry_install(
        self,
        extras: Optional[str] = None,
        *,
        no_root: bool = False,
        no_dev: bool = False,
        pip_require_venv: bool = False,
        **kwargs: Any,
    ) -> None:
        """Wrap ``poetry install`` command for usage in  ``nox`` sessions.

        :param extras: string of space separated extras to install
        :param no_dev: if ``--no-dev`` should be set

            Default: ``False``
        :param no_root: if ``--no-root`` should be set

            Default: ``False``
        :param pip_require_venv: if ``True`` sets environment variable
            ``PIP_REQUIRE_VIRTUALENV`` to ``true`` for this call. ``pip`` then requires
            to be run inside a venv. ``pip`` is used to install ``poetry`` inside the
            venv, if no ``poetry`` executable can be found.
        :param kwargs: same kwargs as :meth:`nox.sessions.Session.install` (see ``nox``
            docs)
        """
        #: Safety hurdle copied from nox.sessions.Session.install()
        if not isinstance(self._runner.venv, (CondaEnv, VirtualEnv, PassthroughEnv)):
            raise ValueError("A session w/o a virtualenv can not install dependencies.")

        env = {"PIP_DISABLE_VERSION_CHECK": "1"}
        req_venv = {"PIP_REQUIRE_VIRTUALENV": "true"}

        if pip_require_venv:
            env.update(req_venv)
            if "env" in kwargs:
                kwargs["env"].update(req_venv)
            else:
                kwargs["env"] = req_venv

        if where_installed("poetry")[0] == 0:
            self.install("poetry>=1", env=env)

        no_root_flag = ["--no-root"] if no_root else []
        no_dev_flag = ["--no-dev"] if no_dev else []
        extra_deps = ["--extras", extras] if extras else []
        install_args = no_root_flag + no_dev_flag + extra_deps

        if "silent" not in kwargs:
            kwargs["silent"] = True

        self._run("poetry", "install", *install_args, external="error", **kwargs)
