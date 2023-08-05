"""
    formelsammlung.strcalc
    ~~~~~~~~~~~~~~~~~~~~~~

    Calculate arithmetic expressions from strings.

    :copyright: (c) 2020, Christian Riedel and AUTHORS
    :license: GPL-3.0-or-later, see LICENSE for details
"""  # noqa: D205,D208,D400
import ast
import operator
import sys

from typing import Optional, Union


NumberType = Union[int, float, complex]
NUMBERTYPES = (int, float, complex)


class StringCalculatorError(Exception):
    """Exception for the StringCalculator."""


class _StringCalculator(ast.NodeVisitor):
    """Calculate an arithmetic expression from a string using :mod:`ast`."""

    def visit_BinOp(self, node: ast.BinOp) -> NumberType:  # noqa: N802,C0103
        """Handle `BinOp` nodes."""
        return {  # type: ignore[no-any-return]
            ast.Add: operator.add,  #: a + b
            ast.Sub: operator.sub,  #: a - b
            ast.Mult: operator.mul,  #: a * b
            ast.Pow: operator.pow,  #: a ** b
            ast.Div: operator.truediv,  #: a / b
            ast.FloorDiv: operator.floordiv,  #: a // b
            ast.Mod: operator.mod,  #: a % b
        }[type(node.op)](self.visit(node.left), self.visit(node.right))

    # fmt: off
    def visit_UnaryOp(self, node: ast.UnaryOp) -> NumberType:  # noqa: N802,C0103
        """Handle `UnaryOp` nodes."""
        return {  # type: ignore[no-any-return]
            ast.UAdd: operator.pos,  #: + a
            ast.USub: operator.neg,  #: - a
        }[type(node.op)](self.visit(node.operand))
    # fmt: on

    @staticmethod
    def visit_Constant(  # noqa: N802,C0103
        node: ast.Constant,
    ) -> NumberType:  # pragma: py-lt-38
        """Handle `Constant` nodes."""
        ret_val = node.value
        if isinstance(ret_val, bool) or not isinstance(ret_val, NUMBERTYPES):
            raise ValueError(f"Extracted `Constant` is not of type {NumberType}.")
        return ret_val

    @staticmethod
    def visit_Num(node: ast.Num) -> NumberType:  # noqa: N802,C0103
        """Handle `Num` nodes.

        For backwards compatibility <3.8. Since 3.8 ``visit_Constant`` is used.
        """
        return node.n  # pragma: py-gte-38

    def visit_Expr(self, node: ast.Expr) -> NumberType:  # noqa: N802,C0103
        """Handle `Expr` nodes."""
        # safety hurdle from visist_Constant for backwards compatibility
        if sys.version_info[0:2] < (3, 8):  # pragma: py-gte-38
            ret_val = self.visit(node.value)
            if isinstance(ret_val, bool) or not isinstance(ret_val, NUMBERTYPES):
                raise ValueError(f"`Expr` did not return a {NumberType}.")
            return ret_val

        return self.visit(node.value)  # type: ignore[no-any-return]  # pragma: py-lt-38


def calculate_string(expression: str) -> Optional[NumberType]:
    """Calculate the given expression.

    The given arithmetic expression string is parsed as an :mod:`ast` and then
    handled by the :class:`ast.NodeVisitor`.

    Python exceptions are risen like with normal arithmetic expression e.g.
    :class:`ZeroDivisionError`.

    Supported number types:

        - :class:`int` ``1``
        - :class:`float` ``1.1``
        - :class:`complex` ``1+1j``

    .. warning::
        On PyPy3 only:
        When working with :class:`complex` numbers containing or resulting with
        :class:`float` numbers be aware that the result of :func:`calculate_string` and
        the equivalent arithmetic expression can divert in the decimals. The result from
        :func:`calculate_string` is then less precise.

    Supported mathematical operators:

        - Positive (:func:`operator.pos`) ``+ a``
        - Negative (:func:`operator.neg`) ``- a``
        - Addition (:func:`operator.add`) ``a + b``
        - Subtraction (:func:`operator.sub`) ``a - b``
        - Multiplication (:func:`operator.mul`) ``a * b``
        - Exponentiation (:func:`operator.pow`) ``a ** b``
        - Division (:func:`operator.truediv`) ``a / b``
        - FloorDivision (:func:`operator.floordiv`) ``a // b``
        - Modulo (:func:`operator.mod`) ``a % b``

    How to use:

    .. testsetup::

        from formelsammlung.strcalc import calculate_string

    .. doctest::

        >>> calculate_string("(1+2)/3")
        1.0

    :param expression: String with arithmetic expression.
    :raises StringCalculatorError: if given expression cannot be calculated.
    :return: Result or None
    """
    if expression == "":
        return None

    try:
        ret_val = _StringCalculator().visit(ast.parse(expression).body[0])
    except KeyError as exc:
        raise StringCalculatorError(
            f"Expression `{expression}` has unsupported node: `{exc}`."
        ) from exc
    except ValueError as exc:
        raise StringCalculatorError(
            f"Expression `{expression}` could not be calculated due to: `{exc}`."
        ) from exc
    else:
        return ret_val  # type: ignore[no-any-return]
