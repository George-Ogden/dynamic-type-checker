from typing import Any, overload

from .check_type import check_type
from .errors import TypeCheckError


@overload
def strict_cast[T](typ: type[T], obj: object, /) -> T: ...


@overload
def strict_cast(typ: None, obj: object, /) -> None: ...


@overload
def strict_cast(typ: Any, obj: object, /) -> Any: ...


def strict_cast(typ: Any, obj: object, /) -> Any:
    """
    Raises a TypeCheckError if obj is not of type T.
    Otherwise, return obj.
    """
    if check_type(typ, obj):
        return obj
    raise generate_type_error(typ, obj)


def generate_type_error(typ: Any, obj: object, /) -> TypeError:
    return TypeCheckError(f"{obj!r} is not an instance of {typ.__name__!r}.")
