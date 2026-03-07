# mypy: disable-error-code="return"
# ruff: noqa: RET503
import enum
import types
import typing

from .errors import MalformedTypeError
from .utils import TypeAnnotation

type SubChecker = typing.Callable[[TypeAnnotation, object], bool | None]
_type_sub_checkers: list[SubChecker] = []


def check_type(typ: TypeAnnotation, obj: object, /) -> bool:
    for sub_checker in _type_sub_checkers:
        if (type_check_result := sub_checker(typ, obj)) is not None:
            return type_check_result
    raise NotImplementedError()


def register_sub_checker(sub_checker: SubChecker) -> SubChecker:
    _type_sub_checkers.append(sub_checker)
    return sub_checker


@register_sub_checker
def check_any_type(typ: TypeAnnotation, obj: object, /) -> bool | None:
    if typ is typing.Any:
        return True


@register_sub_checker
def check_never_type(typ: TypeAnnotation, obj: object, /) -> bool | None:
    if typ is typing.Never or typ is typing.NoReturn:
        return False


@register_sub_checker
def check_none_type(typ: TypeAnnotation, obj: object, /) -> bool | None:
    if typ is None:
        return obj is None


@register_sub_checker
def check_literal_type(typ: TypeAnnotation, obj: object, /) -> bool | None:
    if typ is typing.Literal:
        raise MalformedTypeError(typ, requires_arguments=True)
    if typing.get_origin(typ) is typing.Literal:
        if not all(
            isinstance(arg, int | bool | str | bytes | enum.Enum | types.NoneType)
            for arg in typing.get_args(typ)
        ):
            raise MalformedTypeError(
                typ, extra_msg=f"{typing.Literal} types may only contain primitive or enum values."
            )
        return any(literal_equal(arg, obj) for arg in typing.get_args(typ))


def literal_equal(literal_arg: int | bool | str | bytes | enum.Enum | None, obj: object) -> bool:
    if type(literal_arg) is type(obj):
        if isinstance(literal_arg, enum.Enum | types.NoneType):
            return literal_arg is obj
        return literal_arg == obj
    return False


@register_sub_checker
def check_type_type(typ: TypeAnnotation, obj: object, /) -> bool | None:
    if isinstance(typ, type):
        return isinstance(obj, typ)


@register_sub_checker
def check_union_type(typ: TypeAnnotation, obj: object, /) -> bool | None:
    if typ is typing.Union:
        raise MalformedTypeError(typ, requires_arguments=True)
    if typing.get_origin(typ) is typing.Union:
        return any(check_type(arg, obj) for arg in typing.get_args(typ))
