from typing import Any, overload


@overload
def strict_cast[T](typ: type[T], obj: object, /) -> T: ...


@overload
def strict_cast(typ: Any, obj: object, /) -> Any: ...


def strict_cast(typ: Any, obj: object, /) -> Any:
    """
    Raises a TypeError if obj is not of type T.
    Otherwise, return obj.
    """
    if check_type(typ, obj):
        return obj
    raise generate_type_error(typ, obj)


def generate_type_error(typ: Any, obj: object, /) -> TypeError:
    return TypeError(f"{obj!r} is not an instance of {typ.__name__!r}.")


def check_type[T](typ: type[T], obj: object, /) -> bool:
    return isinstance(obj, typ)
