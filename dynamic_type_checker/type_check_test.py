from typing import Any

from inline_snapshot import snapshot
import pytest

from .test_utils import CallableClass
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
