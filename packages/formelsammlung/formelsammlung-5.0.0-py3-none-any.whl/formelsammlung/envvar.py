"""
    formelsammlung.envvar
    ~~~~~~~~~~~~~~~~~~~~~

    Get environment variables and transform their type.

    :copyright: (c) 2020, Christian Riedel and AUTHORS
    :license: GPL-3.0-or-later, see LICENSE for details
"""  # noqa: D205,D208,D400
import os
import re

from typing import Any, Iterable, NoReturn, Optional, Pattern, Set, Union


#: Default values to convert to ``True`` for environment variables.
TRUE_BOOL_VALUES = ("1", "y", "yes", "t", "True")
#: Default values to convert to ``False`` for environment variables.
FALSE_BOOL_VALUES = ("0", "n", "no", "f", "False")
#: Default regex to check if a string could be an :class:`int`.
INT_REGEX = r"^[\d]+(_\d+)*$"
#: Default regex to check if a string could be an :class:`float`.
FLOAT_REGEX = r"^[\d]+(_\d+)*\.\d+$"


class EnvVarGetter:  # noqa: R0903
    """Class containing the config for :meth:`EnvVarGetter.getenv_typed`."""

    def __init__(  # noqa: R0913
        self,
        *,
        raise_error_if_no_value: bool = False,
        true_bool_values: Optional[Iterable] = None,
        false_bool_values: Optional[Iterable] = None,
        int_regex: Optional[str] = None,
        float_regex: Optional[str] = None,
    ) -> None:
        """Initialize :class:`EnvVarGetter` with config values.

        Use the :class:`EnvVarGetter` instance to call :meth:`EnvVarGetter.getenv_typed`
        with the set config.

        .. Note:: Parameters below are all keyword only.

        :param raise_error_if_no_value: If ``True`` raises an :exc:`KeyError` when no
            value is found by :meth:`EnvVarGetter.getenv_typed` for ``var_name`` and
            ``default`` is ``None``.

            Default: ``False``
        :param true_bool_values: Set of objects whose string representations are
            matched case-insensitive against the environment variable's value to check
            if the value is a ``True`` bool.

            Default: :const:`TRUE_BOOL_VALUES`
        :param false_bool_values: Set of objects whose string representations are
            matched case-insensitive against the environment variable's value to check
            if the value is a ``False`` bool.

            Default: :const:`FALSE_BOOL_VALUES`
        :param int_regex: Regex string to identify integers.

            Default: :const:`INT_REGEX`
        :param float_regex: Regex string to identify floats.

            Default: :const:`FLOAT_REGEX`
        """
        self.raise_error_if_no_value = raise_error_if_no_value
        self._true_bool_values = set(true_bool_values or TRUE_BOOL_VALUES)
        self._false_bool_values = set(false_bool_values or FALSE_BOOL_VALUES)
        self._int_regex = int_regex or INT_REGEX
        self._int_regex_pattern = re.compile(self._int_regex)
        self._float_regex = float_regex or FLOAT_REGEX
        self._float_regex_pattern = re.compile(self._float_regex)

    @property
    def true_bool_values(self) -> Set[str]:
        """Set of objects to identify a ``True`` boolean.

        See parameters of :class:`EnvVarGetter`.
        """
        # Get value for ``_true_bool_values``.
        return self._true_bool_values

    @true_bool_values.setter
    def true_bool_values(self, value: Iterable) -> None:
        """Set new value for ``_true_bool_values``."""
        self._true_bool_values = set(value)

    @property
    def false_bool_values(self) -> Set[str]:
        """Set of objects to identify a ``False`` boolean.

        See parameters of :class:`EnvVarGetter`.
        """
        # Get value for ``_false_bool_values``.
        return self._false_bool_values

    @false_bool_values.setter
    def false_bool_values(self, value: Iterable) -> None:
        """Set new value for ``_false_bool_values``."""
        self._false_bool_values = set(value)

    @property
    def int_regex(self) -> str:
        """Regex string used for checking if a string is an :class:`int`.

        See parameters of :class:`EnvVarGetter`.
        """
        # Get value for ``_int_regex``.
        return self._int_regex

    @int_regex.setter
    def int_regex(self, value: str) -> None:
        """Set new value for ``int_regex`` and update ``int_regex_pattern``."""
        self._int_regex = value
        self._int_regex_pattern = re.compile(self._int_regex)

    @property
    def int_regex_pattern(self) -> Pattern[str]:
        """Regex pattern of :meth:`EnvVarGetter.int_regex`.

        Cannot be set. Set via :meth:`EnvVarGetter.int_regex`.
        """
        return self._int_regex_pattern

    @int_regex_pattern.setter
    def int_regex_pattern(self, value: Any) -> NoReturn:  # noqa: R0201
        """Error if called."""
        raise AttributeError(
            "`int_regex_pattern` cannot be set directly. "
            "Set as string via `int_regex`."
        )

    @property
    def float_regex(self) -> str:
        """Regex string used for checking if a string is a :class:`float`.

        See parameters of :class:`EnvVarGetter`.
        """
        # Get value for ``_float_regex``.
        return self._float_regex

    @float_regex.setter
    def float_regex(self, value: str) -> None:
        """Set new value for ``float_regex`` and update ``float_regex_pattern``."""
        self._float_regex = value
        self._float_regex_pattern = re.compile(self._float_regex)

    @property
    def float_regex_pattern(self) -> Pattern[str]:
        """Regex pattern of :meth:`EnvVarGetter.float_regex`.

        Cannot be set. Set via :meth:`EnvVarGetter.float_regex`.
        """
        return self._float_regex_pattern

    @float_regex_pattern.setter
    def float_regex_pattern(self, value: Any) -> NoReturn:  # noqa: R0201
        """Error if called."""
        raise AttributeError(
            "`float_regex_pattern` cannot be set directly. "
            "Set as string via `float_regex`."
        )

    def _guess_bool(self, value: str) -> Optional[bool]:
        """Guess if value is a ``bool``."""
        #: Guess if `True`
        if value.casefold() in (str(b).casefold() for b in self._true_bool_values):
            return True
        #: Guess if `False`
        if value.casefold() in (str(b).casefold() for b in self._false_bool_values):
            return False
        return None

    def _guess_num(self, value: str) -> Optional[Union[int, float]]:
        """Guess if value is an ``int`` or ``float``."""
        #: Guess if `int`
        if self._int_regex_pattern.fullmatch(value):
            return int(value)
        #: Guess if `float`
        if self._float_regex_pattern.fullmatch(value):
            return float(value)
        return None

    def getenv_typed(
        self,
        var_name: str,
        default: Any = None,
        rv_type: Optional[type] = None,
    ) -> Any:
        """Wrap :func:`os.getenv` to adjust the type of the return values.

        Instead of returning the environments variable's value as :class:`str` like
        :func:`os.getenv` you can set ``rv_type`` to a :class:`type` to convert the
        value into. If ``rv_type`` is not set the :class:`type` gets guessed and used
        for conversion.

        **Guessable types are (checked in this order):**

            - :class:`bool`
            - :class:`int`
            - :class:`float`
            - :class:`str` (fallback)

        For :class:`bool` guessing the value returned by :func:`os.getenv` is compared
        against :meth:`EnvVarGetter.true_bool_values` and
        :meth:`EnvVarGetter.false_bool_values` and if a match is found returns the
        corresponding boolean.

        For :class:`int` guessing the value returned by :func:`os.getenv` is checked by
        the regex :meth:`EnvVarGetter.int_regex_pattern` which can be changed by setting
        :meth:`EnvVarGetter.int_regex`.

        For :class:`float` guessing the value returned by :func:`os.getenv` is checked
        by the regex :meth:`EnvVarGetter.float_regex_pattern` which can be changed by
        setting :meth:`EnvVarGetter.float_regex`.

        .. Warning:: Because :class:`bool` is guessed before :class:`int` ``0`` and
            ``1`` are converted into :class:`bool` instead of :class:`int` when
            ``rv_type`` is not set.

        **How to use:**

        .. testsetup::

            import os
            from formelsammlung.envvar import EnvVarGetter

        .. doctest::

            >>> os.environ["TEST_ENV_VAR"] = "2"
            >>> getter = EnvVarGetter()
            >>> getter.getenv_typed("TEST_ENV_VAR", 1, int)
            2

        .. testcleanup::

            os.environ["TEST_ENV_VAR"] = ""

        :param var_name: Name of the environment variable.
        :param default: Default value if no value is found for ``var_name``.

            Default: ``None``.
        :param rv_type: Type the value of the environment variable should be changed
            into. If not set or set to ``None`` the type gets guessed.

            Default: ``None``.
        :raises KeyError: If ``raise_error_if_no_value`` is ``True`` and no value is
            found for ``var_name`` and ``default`` is ``None``.
        :raises KeyError: If ``rv_type`` is set to :class:`bool` and value from
            ``var_name`` or ``default`` is not found in ``true_bool_values`` or
            ``false_bool_values``.
        :return: Value for ``var_name`` or ``default`` converted to ``rv_type``
            or guessed type.
        """
        env_var = os.getenv(var_name, default)

        if not env_var and default is None:
            if self.raise_error_if_no_value:
                raise KeyError(
                    f"Environment variable '{var_name}' not set "
                    "or empty and no default."
                ) from None
            return None

        #: Convert to given `rv_type` if set.
        if rv_type and rv_type is not bool:
            return rv_type(env_var)

        env_var = str(env_var)

        #: Guess bool value
        bool_val = self._guess_bool(env_var)
        if bool_val is not None:
            return bool_val

        if rv_type:
            raise KeyError(
                f"Environment variable '{var_name}' has an invalid Boolean value.\n"
                f"For true use any of: {self._true_bool_values}\n"
                f"For false use any of: {self._false_bool_values}"
            ) from None

        #: Guess num value
        num_val = self._guess_num(env_var)
        if num_val is not None:
            return num_val

        return env_var


def getenv_typed(
    var_name: str, default: Any = None, rv_type: Optional[type] = None, **kwargs: Any
) -> Any:
    """Shortcut for ``EnvVarGetter(...).getenv_typed(...)``.

    **How to use:**

    .. testsetup::

        import os
        from formelsammlung.envvar import getenv_typed

    .. doctest::

        >>> os.environ["TEST_ENV_VAR"] = "2"
        >>> getenv_typed("TEST_ENV_VAR", 1, int)
        2

    .. testcleanup::

        os.environ["TEST_ENV_VAR"] = ""

    :param var_name: Same argument as for and gets given to
        :meth:`EnvVarGetter.getenv_typed`.
    :param default: Same argument as for and gets given to
        :meth:`EnvVarGetter.getenv_typed`.
    :param rv_type: Same argument as for and gets given to
        :meth:`EnvVarGetter.getenv_typed`.
    :param kwargs: Arguments taken by :class:`EnvVarGetter`
    :return: Return value of :meth:`EnvVarGetter.getenv_typed`.
    """  # noqa: D402
    return EnvVarGetter(**kwargs).getenv_typed(var_name, default, rv_type)
