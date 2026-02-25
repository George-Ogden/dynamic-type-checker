import enum
import types
import typing

from .errors import MalformedTypeError


def check_type(typ: type | typing._SpecialForm | None, obj: object, /) -> bool:
    if typ is typing.Any:
        return True
    if typ is typing.Never or typ is typing.NoReturn:
        return False
    if typ is None:
        return obj is None
    if typ is typing.Literal:
        raise MalformedTypeError(f"{typ} is not a valid type.")
    if typing.get_origin(typ) is typing.Literal:
        if any(
            not isinstance(arg, int | bool | str | bytes | enum.Enum | types.NoneType)
            for arg in typing.get_args(typ)
        ):
            raise MalformedTypeError(f"{typ} is not a valid type.")
        return obj in typing.get_args(typ)
    if isinstance(typ, type):
        return isinstance(obj, typ)
    raise NotImplementedError()
