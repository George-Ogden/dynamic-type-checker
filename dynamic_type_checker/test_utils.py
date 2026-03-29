# ruff: noqa: UP040
# mypy: disable-error-code="misc,valid-type"
import enum
from typing import Any, Literal, NoReturn, TypeAlias, TypeAliasType


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


def no_argument_function() -> None: ...


def positional_only_arg_fn(x: int, /) -> int:
    return x + 1


def positional_keyword_arg_fn(x: int, y: int) -> int:
    return x**y


def keyword_arg_fn(*, seq: tuple, idx: int) -> float:
    return seq[idx]


def type_error_function() -> NoReturn:
    raise TypeError()


def variadic_arg_function(*args: bool) -> tuple[bool, ...]:
    return args


def variadic_kwarg_function(**kwargs: str) -> dict[str, str]:
    return kwargs


def fully_mixed_function(
    pos_one: str, pos_two: str, /, mixed: int, *args: bool, keyword: float, **kwargs: tuple
) -> tuple:
    return pos_one, pos_two, mixed, *args, keyword, *kwargs.values()


class CallableClass:
    def __call__(self, x: int) -> int:
        return x


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
