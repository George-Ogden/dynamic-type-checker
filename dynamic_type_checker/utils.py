import types
import typing
from typing import Any, TypeGuard

type TypeAnnotation = type | typing._SpecialForm | typing.TypeAliasType | types.UnionType | None


def is_in[T](item: Any, container: tuple[T, ...]) -> TypeGuard[T]:
    """Check whether an item is in a container using `is` instead of `==`."""
    return any(item is element for element in container)
