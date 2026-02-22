import typing


def check_type[T](typ: type[T] | None, obj: object, /) -> bool:
    if typ is typing.Any:
        return True
    if typ is None:
        return obj is None
    return isinstance(obj, typ)
