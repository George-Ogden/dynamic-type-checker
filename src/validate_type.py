import enum
import types
import typing

from .errors import MalformedTypeError
from .utils import TypeAnnotation, is_in


def validate_type(typ: TypeAnnotation) -> None:
    _validate_type(typ, typ)


def _validate_type(typ: TypeAnnotation, original_typ: TypeAnnotation) -> None:
    if is_in(typ, (typing.Literal, typing.Union)):
        raise MalformedTypeError(original_typ, requires_arguments=True)
    if typing.get_origin(typ) is typing.Literal and not all(
        isinstance(arg, int | bool | str | bytes | enum.Enum | types.NoneType)
        for arg in typing.get_args(typ)
    ):
        raise MalformedTypeError(
            original_typ,
            extra_msg=f"{typing.Literal} types may only contain primitive or enum values.",
        )
    if typing.get_origin(typ) is typing.Union:
        for arg in typing.get_args(typ):
            _validate_type(arg, original_typ)
