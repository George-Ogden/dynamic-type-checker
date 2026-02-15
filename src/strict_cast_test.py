from typing import Any

import pytest

from .strict_cast import check_type


@pytest.mark.parametrize(
    "typ, obj, succeeds",
    [
        (bool, True, True),
        (bool, 5, False),
        (int, 6, True),
        (int, True, True),
        (int, 7.4, False),
        (int, "hello", False),
        (str, "hello", True),
        (str, 7, False),
        (str, 7.4, False),
        (str, True, False),
        (float, 96.3, True),
        (float, True, False),
        (float, 9, False),
        (float, "True", False),
        (list, ["True"], True),
        (list, True, False),
        (list, "True", False),
    ],
)
def test_check_type(typ: Any, obj: object, succeeds: bool) -> None:
    assert check_type(typ, obj) == succeeds
