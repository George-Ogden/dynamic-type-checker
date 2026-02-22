def check_type[T](typ: type[T] | None, obj: object, /) -> bool:
    if typ is None:
        return obj is None
    return isinstance(obj, typ)
