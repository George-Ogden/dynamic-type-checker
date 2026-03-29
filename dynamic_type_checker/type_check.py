from collections.abc import Callable
import inspect


def type_check[**P, R](f: Callable[P, R], /) -> Callable[P, R]:
    if not inspect.isfunction(f):
        raise TypeError(f"Currently, only functions are supported by `type_check`, got {f!r}.")
    return f
