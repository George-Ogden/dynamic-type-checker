def check_type[T](typ: type[T], obj: object, /) -> bool:
    return isinstance(obj, typ)
