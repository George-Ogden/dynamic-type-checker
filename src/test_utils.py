# ruff: noqa: UP040
# mypy: disable-error-code="misc,valid-type"
from collections.abc import Iterable
import enum
import inspect
from typing import TYPE_CHECKING, Any, Literal, TypeAlias, TypeAliasType, final

import pytest

if TYPE_CHECKING:
    from mypy_pytest_plugin_types import ParameterSet


def cases[Self: type](cls: Self) -> Iterable["ParameterSet[Self]"]:
    for name, method in inspect.getmembers(cls, predicate=inspect.ismethod):
        if name != "cases" and not name.startswith("_"):
            yield pytest.param(method(), id=name)


@pytest.mark.typed
def test_case[T: type](cls: T) -> T:
    cls.cases = classmethod(cases)  # type: ignore [attr-defined]
    return final(cls)


test_case.__test__ = False


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


class EqualityError:
    def __eq__(self, other: object) -> bool:
        raise NotImplementedError()


Bull = enum.IntEnum("Bull", [("Twoo", 1), ("Faws", 0)])
Colors = enum.Enum("Colors", ["RED", "GREEN", "BLUE"])
Rotations = enum.Flag("Rotations", ["ROT90", "ROT180"])


def a_function(a: int) -> int:
    return a


type IntAlias = int
type UnionAlias = int | str | OneFieldClass
type IntAliasAlias = IntAlias
ClassAlias: TypeAlias = OneFieldClass
AClassAlias = TypeAliasType("AClassAlias", OneFieldClass)

type Zero = Literal[False, 0]
type One = Literal[True, 1]
type ZeroOrOneLiteral = Literal[Zero, One]
type ZeroOrOneUnion = Zero | One

type InvalidLiteral = Literal

type RecursiveTypeAlias = RecursiveTypeAlias
type MutuallyRecursiveTypeAlias1 = MutuallyRecursiveTypeAlias2
type MutuallyRecursiveTypeAlias2 = MutuallyRecursiveTypeAlias1
type BigMutuallyRecursiveTypeAlias1 = BigMutuallyRecursiveTypeAlias2
type BigMutuallyRecursiveTypeAlias2 = BigMutuallyRecursiveTypeAlias3
type BigMutuallyRecursiveTypeAlias3 = BigMutuallyRecursiveTypeAlias1
type RecursiveUnionType = RecursiveUnionType | int
type RecursiveLiteralType = Literal[RecursiveLiteralType]

type DiamondType = IntAlias | IntAliasAlias
