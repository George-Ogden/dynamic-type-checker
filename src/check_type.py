import typing


def check_type(typ: type | typing._SpecialForm | None, obj: object, /) -> bool:
    if typ is typing.Any:
        return True
    if typ is typing.Never or typ is typing.NoReturn:
        return False
    if typ is None:
        return obj is None
    if typing.get_origin(typ) is typing.Literal:
        return obj in typing.get_args(typ)
    if isinstance(typ, type):
        return isinstance(obj, typ)
    raise NotImplementedError()
