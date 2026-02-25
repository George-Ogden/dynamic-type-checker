import enum
import sys
import types
import typing
from typing import Any

from debug import pprint
from inline_snapshot import snapshot
import pytest

from .check_type import check_type
from .errors import MalformedTypeError


class EmptyClass: ...


class OneFieldClass:  # noqa: B903
    def __init__(self, x: Any) -> None:
        self.x = x


class MetaclassIsInstance(type):
    def __instancecheck__(cls, instance: object) -> bool:
        return cls.is_instance(instance)

    @classmethod
    def is_instance(cls, x: object) -> bool:
        return issubclass(type(x), cls)


class CustomMetaclassIsInstance(metaclass=MetaclassIsInstance):
    @classmethod
    def is_instance(cls, x: object) -> bool:
        return isinstance(x, int) and x > 0


class CustomMetaclassSubclassIsInstance(CustomMetaclassIsInstance): ...


Bull = enum.IntEnum("Bull", [("Twoo", 1), ("Faws", 0)])
Colors = enum.Enum("Colors", ["RED", "GREEN", "BLUE"])
Rotations = enum.Flag("Rotations", ["ROT90", "ROT180"])


def a_function(a: int) -> int:
    return a


@pytest.mark.parametrize(
    "typ, obj, succeeds",
    [
        # primitive types
        (bool, True, True),
        (bool, 5, False),
        (bool, None, False),
        (int, 6, True),
        (int, True, True),
        (int, 7.4, False),
        (int, "hello", False),
        (int, None, False),
        (str, "hello", True),
        (str, 7, False),
        (str, 7.4, False),
        (str, True, False),
        (float, 96.3, True),
        (float, True, False),
        (float, 9, False),
        (float, "True", False),
        (list, ["True"], True),
        (list, True, False),
        (list, "True", False),
        (tuple, (), True),
        (tuple, ((),), True),
        (tuple, (3), False),
        (tuple, [2], False),
        (tuple, None, False),
        # classes
        (EmptyClass, EmptyClass(), True),
        (EmptyClass, EmptyClass, False),
        (EmptyClass, 5, False),
        (EmptyClass, OneFieldClass("no"), False),
        (OneFieldClass, OneFieldClass("no"), True),
        (OneFieldClass, OneFieldClass(10), True),
        (OneFieldClass, OneFieldClass, False),
        (OneFieldClass, None, False),
        # custom metaclasses
        pytest.param(
            CustomMetaclassIsInstance,
            CustomMetaclassIsInstance(),
            False,
            marks=pytest.mark.xfail,  # see https://github.com/python/cpython/issues/144873
        ),
        (CustomMetaclassIsInstance, CustomMetaclassSubclassIsInstance(), False),
        (CustomMetaclassSubclassIsInstance, 2, True),
        (CustomMetaclassIsInstance, 5, True),
        (CustomMetaclassIsInstance, 1, True),
        (CustomMetaclassIsInstance, 0, False),
        (CustomMetaclassIsInstance, -5, False),
        (CustomMetaclassIsInstance, 1.0, False),
        (CustomMetaclassIsInstance, True, True),
        (CustomMetaclassIsInstance, False, False),
        # None type hint
        (None, None, True),
        (None, 1, False),
        (None, (), False),
        (types.NoneType, None, True),
        (types.NoneType, 3.1, False),
        # Any type hint
        (typing.Any, 1, True),
        (typing.Any, None, True),
        (typing.Any, OneFieldClass(1), True),
        (typing.Any, OneFieldClass, True),
        # Never/NoReturn type hint
        (typing.Never, 1, False),
        (typing.Never, object, False),
        (typing.NoReturn, 1, False),
        (typing.NoReturn, RuntimeError(), False),
        # Literal type hint
        (typing.Literal[2], 2, True),
        (typing.Literal[2], 3, False),
        (typing.Literal[1, 2], 3, False),
        (typing.Literal[1, 3], 3, True),
        pytest.param(typing.Literal[True], 1, False, marks=pytest.mark.xfail),
        pytest.param(typing.Literal[False], 0, False, marks=pytest.mark.xfail),
        (typing.Literal[False], False, True),
        (typing.Literal[False], True, False),
        (typing.Literal["abcd"], True, False),
        (typing.Literal["abcd", "ef"], "e", False),
        (typing.Literal["abcd", "ef"], "abcd", True),
        (typing.Literal["abcd", "ef"], "ef", True),
        (typing.Literal[Bull.Twoo], Bull.Twoo, True),
        (typing.Literal[Bull.Twoo], Bull.Faws, False),
        pytest.param(typing.Literal[Bull.Twoo], 1, False, marks=pytest.mark.xfail),
        (typing.Literal[Bull.Twoo], 0, False),
        pytest.param(typing.Literal[Bull.Twoo], True, False, marks=pytest.mark.xfail),
        (typing.Literal[Bull.Twoo], False, False),
        (typing.Literal[Colors.BLUE], Colors.BLUE, True),
        (typing.Literal[Colors.BLUE], Colors.RED, False),
        (typing.Literal[Colors.BLUE], 2, False),
        (typing.Literal[Colors.BLUE], "BLUE", False),
        (typing.Literal[Colors.BLUE], "RED", False),
        (typing.Literal[Rotations.ROT90], Rotations.ROT90, True),
        (typing.Literal[Rotations.ROT90], Rotations.ROT180, False),
        (typing.Literal[Rotations.ROT90], Rotations.ROT90 | Rotations.ROT180, False),
        (typing.Literal[Rotations.ROT90], Rotations.ROT90 | Rotations.ROT90, True),
        (
            typing.Literal[Rotations.ROT90 | Rotations.ROT180],
            Rotations.ROT180 | Rotations.ROT90,
            True,
        ),
        (typing.Literal[Rotations.ROT90 | Rotations.ROT180], Rotations.ROT90, False),
        (typing.Literal[Rotations.ROT90, Rotations.ROT180], Rotations.ROT90, True),
        (typing.Literal[Rotations.ROT90], 1, False),
        (typing.Literal[Rotations.ROT180], 2, False),
        (typing.Literal[Rotations(0)], Rotations(0), True),
        (typing.Literal[Rotations(0)], Rotations(1), False),
        (typing.Literal[None], None, True),  # noqa: PYI061
        (typing.Literal[None], 1, False),  # noqa: PYI061
        (typing.Literal[b"1234"], b"1234", True),
        (typing.Literal[b"1234"], "1234", False),
        (typing.Literal[b"1234"], int.from_bytes(b"1234"), False),
        (typing.Literal[b"1234"], 1234, False),
    ],
)
def test_check_type(typ: Any, obj: object, succeeds: bool) -> None:
    pprint(typ, prefix="typ = ", file=sys.stderr)
    pprint(obj, prefix="obj = ", file=sys.stderr)
    assert check_type(typ, obj) == succeeds


@pytest.mark.parametrize(
    "typ, obj, error_cls, error_message",
    [
        (
            typing.Literal,
            "blah",
            MalformedTypeError,
            snapshot("typing.Literal is not a valid type."),
        ),
        (
            typing.Literal[int],
            int,
            MalformedTypeError,
            snapshot("typing.Literal[int] is not a valid type."),
        ),
        (
            typing.Literal[a_function],
            a_function,
            MalformedTypeError,
            snapshot("typing.Literal[a_function] is not a valid type."),
        ),
    ],
)
def test_check_type_errors(
    typ: Any, obj: object, error_cls: type[Exception], error_message: str
) -> None:
    pprint(typ, prefix="typ = ", file=sys.stderr)
    pprint(obj, prefix="obj = ", file=sys.stderr)
    with pytest.raises(error_cls) as e:
        check_type(typ, obj)
    assert str(e.value) == error_message
