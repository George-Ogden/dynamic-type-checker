# ruff: noqa: UP007
import sys
import typing
from typing import Any, Literal, TypeAliasType

from debug import pprint
from inline_snapshot import snapshot
import pytest

from .errors import MalformedTypeError
from .test_utils import InvalidLiteral, OneFieldClass, ZeroOrOneUnion, a_function
from .validate_type import validate_type


@pytest.mark.parametrize(
    "typ, error_cls, error_message",
    [
        (
            typing.Literal,
            MalformedTypeError,
            snapshot("typing.Literal is not a valid type. typing.Literal requires type arguments."),
        ),
        (
            typing.Literal[int],
            MalformedTypeError,
            snapshot(
                "typing.Literal[int] is not a valid type. typing.Literal types may only contain primitive values, enum values, nested literals or aliases to literal types."
            ),
        ),
        (
            typing.Literal[a_function],
            MalformedTypeError,
            snapshot(
                "typing.Literal[a_function] is not a valid type. typing.Literal types may only contain primitive values, enum values, nested literals or aliases to literal types."
            ),
        ),
        (
            typing.Union,
            MalformedTypeError,
            snapshot("typing.Union is not a valid type. typing.Union requires type arguments."),
        ),
        (
            typing.Union[bool, typing.Literal[int]],
            MalformedTypeError,
            snapshot(
                "typing.Union[bool, typing.Literal[int]] is not a valid type. typing.Literal types may only contain primitive values, enum values, nested literals or aliases to literal types."
            ),
        ),
        (
            bool | typing.Literal[float],
            MalformedTypeError,
            snapshot(
                "typing.Union[bool, typing.Literal[float]] is not a valid type. typing.Literal types may only contain primitive values, enum values, nested literals or aliases to literal types."
            ),
        ),
        (
            typing.TypeAliasType("BrokenTypeAlias", typing.Literal[float]),
            MalformedTypeError,
            snapshot(
                "BrokenTypeAlias is not a valid type. typing.Literal types may only contain primitive values, enum values, nested literals or aliases to literal types."
            ),
        ),
        (
            typing.TypeAliasType("BrokenTypeAlias", typing.Literal[float]) | None,
            MalformedTypeError,
            snapshot(
                "BrokenTypeAlias | None is not a valid type. typing.Literal types may only contain primitive values, enum values, nested literals or aliases to literal types."
            ),
        ),
        (
            typing.TypeAliasType("BrokenTypeAlias", typing.Literal) | None,
            MalformedTypeError,
            snapshot(
                "BrokenTypeAlias | None is not a valid type. typing.Literal requires type arguments."
            ),
        ),
        (
            Literal[InvalidLiteral],
            MalformedTypeError,
            snapshot(
                "typing.Literal[InvalidLiteral] is not a valid type. typing.Literal types may only contain primitive values, enum values, nested literals or aliases to literal types."
            ),
        ),
        (
            Literal[TypeAliasType("TypeAliasToClass", OneFieldClass)],
            MalformedTypeError,
            snapshot(
                "typing.Literal[TypeAliasToClass] is not a valid type. typing.Literal types may only contain primitive values, enum values, nested literals or aliases to literal types."
            ),
        ),
        (
            typing.Literal[ZeroOrOneUnion],
            MalformedTypeError,
            snapshot(
                "typing.Literal[ZeroOrOneUnion] is not a valid type. typing.Literal types may only contain primitive values, enum values, nested literals or aliases to literal types."
            ),
        ),
    ],
)
def test_validate_type(typ: Any, error_cls: type[Exception], error_message: str) -> None:
    pprint(typ, prefix="typ = ", file=sys.stderr)
    with pytest.raises(error_cls) as e:
        validate_type(typ)
    assert str(e.value) == error_message
