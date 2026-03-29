from collections.abc import Callable
from typing import Any

from inline_snapshot import snapshot
import pytest
from utils.test_utils import check_for_errors

from .test_utils import (
    CallableClass,
    fully_mixed_function,
    keyword_arg_fn,
    no_argument_function,
    positional_keyword_arg_fn,
    positional_only_arg_fn,
    type_error_function,
    variadic_arg_function,
    variadic_kwarg_function,
)
from .type_check import type_check


@pytest.mark.parametrize(
    "obj, error_msg",
    [
        # callable class
        (
            CallableClass(),
            snapshot(
                "Currently, only functions are supported by `type_check`, got <dynamic_type_checker.test_utils.CallableClass object at [ID]>."
            ),
        ),
        # arbitrary object
        (4, snapshot("Currently, only functions are supported by `type_check`, got 4.")),
        # type
        (
            bool,
            snapshot(
                "Currently, only functions are supported by `type_check`, got <class 'bool'>."
            ),
        ),
    ],
)
def test_type_check_non_function(obj: Any, error_msg: str) -> None:
    with pytest.raises(TypeError) as e:
        type_check(obj)
    assert str(e.value).replace(hex(id(obj)), "[ID]") == error_msg


@pytest.mark.parametrize(
    """fn, inputs, expected""",
    [
        (no_argument_function, ((), {}), None),
        (positional_only_arg_fn, ((3,), {}), 4),
        (positional_keyword_arg_fn, ((2, 3), {}), 8),
        (positional_keyword_arg_fn, ((2,), dict(y=3)), 8),
        (positional_keyword_arg_fn, ((), dict(y=2, x=3)), 9),
        (keyword_arg_fn, ((), dict(idx=-2, seq=(1, 2, 4))), 2),
        (keyword_arg_fn, ((), dict(idx=3, seq=(1, 2, 4))), IndexError),
        (type_error_function, ((), {}), TypeError),
        pytest.param(type_error_function, ((), {}), None, marks=pytest.mark.xfail(strict=True)),
        (variadic_arg_function, ((), {}), ()),
        (variadic_arg_function, (("a",), {}), ("a",)),
        (variadic_arg_function, (("a", "b"), {}), ("a", "b")),
        (variadic_kwarg_function, ((), {}), {}),
        (variadic_kwarg_function, ((), dict(a="b")), dict(a="b")),
        (variadic_kwarg_function, ((), dict(a="b", b="c")), dict(b="c", a="b")),
        (
            fully_mixed_function,
            (("pos_one", "pos_two"), dict(keyword=4.0, mixed=3)),
            ("pos_one", "pos_two", 3, 4.0),
        ),
        (
            fully_mixed_function,
            (("pos_one", "pos_two", 3, False, True), dict(kwarg=(), keyword=6.0, kwarg2=((),))),
            ("pos_one", "pos_two", 3, False, True, 6.0, (), ((),)),
        ),
    ],
)
def test_type_check_function_valid_cases(
    fn: Callable, inputs: tuple[tuple[Any, ...], dict[str, Any]], expected: Any
) -> None:
    args, kwargs = inputs
    with check_for_errors(expected):
        assert type_check(fn)(*args, **kwargs) == expected
