import enum
import types
import typing

from .errors import CyclicTypeError, MalformedTypeError
from .type_alias_graph import TypeAliasGraph
from .utils import TypeAnnotation, is_in


def validate_type(typ: TypeAnnotation) -> None:
    _validate_type(typ, typ)


def _validate_type(typ: TypeAnnotation, original_typ: TypeAnnotation) -> None:
    if isinstance(typ, typing.TypeAliasType):
        if (cycle := TypeAliasGraph.find_cycle(typ)) is not None:
            raise CyclicTypeError(original_typ, cycle)
        _validate_type(typ.__value__, original_typ)
    if is_in(typ, (typing.Literal, typing.Union)):
        raise MalformedTypeError(
            original_typ, extra_msg=MalformedTypeError.requires_arguments_msg(typ)
        )
    if typing.get_origin(typ) is typing.Literal:
        for type_arg in typing.get_args(typ):
            _validate_literal_arg(type_arg, original_typ)
    if is_in(typing.get_origin(typ), (typing.Union, types.UnionType)):
        for arg in typing.get_args(typ):
            _validate_type(arg, original_typ)


def _validate_literal_arg(typ: TypeAnnotation, original_typ: TypeAnnotation) -> None:
    if isinstance(typ, typing.TypeAliasType):
        _validate_literal_arg(typ.__value__, original_typ)
    elif typing.get_origin(typ) is typing.Literal:
        for type_arg in typing.get_args(typ):
            _validate_literal_arg(type_arg, original_typ)
    elif not isinstance(typ, int | bool | str | bytes | enum.Enum | types.NoneType):
        raise MalformedTypeError(
            original_typ,
            extra_msg=f"{typing.Literal} types may only contain primitive values, enum values, nested literals or aliases to literal types.",
        )
