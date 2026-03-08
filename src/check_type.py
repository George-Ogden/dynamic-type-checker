# mypy: disable-error-code="return"
# ruff: noqa: RET503
import enum
import types
import typing

from .utils import TypeAnnotation, is_in
from .validate_type import validate_type

type SubChecker = typing.Callable[[TypeAnnotation, object], bool | None]
_type_sub_checkers: list[SubChecker] = []


def check_type(typ: TypeAnnotation, obj: object, /) -> bool:
    validate_type(typ)
    for sub_checker in _type_sub_checkers:
        if (type_check_result := sub_checker(typ, obj)) is not None:
            return type_check_result
    raise NotImplementedError()


def register_sub_checker[T: SubChecker](sub_checker: T) -> T:
    _type_sub_checkers.append(sub_checker)
    return sub_checker


@register_sub_checker
def check_any_type(typ: object, obj: object, /) -> bool | None:
    if typ is typing.Any:
        return True


@register_sub_checker
def check_never_type(typ: object, obj: object, /) -> bool | None:
    if is_in(typ, (typing.NoReturn, typing.Never)):
        return False


@register_sub_checker
def check_none_type(typ: object, obj: object, /) -> bool | None:
    if typ is None:
        return obj is None


@register_sub_checker
def check_literal_type(typ: object, obj: object, /) -> bool | None:
    if typing.get_origin(typ) is typing.Literal:
        return any(literal_equal(arg, obj) for arg in typing.get_args(typ))


def literal_equal(
    literal_arg: int | bool | str | bytes | enum.Enum | typing.TypeAliasType | None, obj: object
) -> bool:
    if (type_alias_result := check_type_alias(literal_arg, obj)) is not None:
        return type_alias_result
    if type(literal_arg) is type(obj):
        if isinstance(literal_arg, enum.Enum | types.NoneType):
            return literal_arg is obj
        return literal_arg == obj
    return False


@register_sub_checker
def check_type_type(typ: object, obj: object, /) -> bool | None:
    if isinstance(typ, type):
        return isinstance(obj, typ)


@register_sub_checker
def check_union_type(typ: object, obj: object, /) -> bool | None:
    if is_in(typing.get_origin(typ), (typing.Union, types.UnionType)):
        return any(check_type(arg, obj) for arg in typing.get_args(typ))


@register_sub_checker
def check_type_alias(typ: object, obj: object, /) -> bool | None:
    if isinstance(typ, typing.TypeAliasType):
        return check_type(typ.__value__, obj)
