from typing import Any, TypeGuard, _SpecialForm

type TypeAnnotation = type | _SpecialForm | None


def is_in[T](item: Any, container: tuple[T, ...]) -> TypeGuard[T]:
    """Check whether an item is in a container using `is` instead of `==`."""
    return any(item is element for element in container)
