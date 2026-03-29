from typing import Any

from inline_snapshot import snapshot
import pytest

from .errors import TypeCheckError
from .strict_cast import generate_type_error, strict_cast


@pytest.mark.parametrize(
    "typ, obj, succeeds",
    [
        (bool, True, True),
        (float, 1.0, True),
        (float, "str", False),
        (bool, 10, False),
        (object, type, True),
    ],
)
def test_strict_cast(typ: Any, obj: object, succeeds: bool) -> None:
    if succeeds:
        assert strict_cast(typ, obj) is obj
    else:
        with pytest.raises(TypeError) as e:
            strict_cast(typ, obj)
        assert str(e.value) == str(generate_type_error(typ, obj))
        assert isinstance(e.value, TypeCheckError)


@pytest.mark.parametrize(
    "typ, obj, error_msg",
    [
        (float, "str", snapshot("'str' is not an instance of 'float'.")),
        (bool, 10, snapshot("10 is not an instance of 'bool'.")),
        (list, (), snapshot("() is not an instance of 'list'.")),
        (tuple, [], snapshot("[] is not an instance of 'tuple'.")),
        (int, 1.5, snapshot("1.5 is not an instance of 'int'.")),
    ],
)
def test_generate_type_error(typ: Any, obj: object, error_msg: str) -> None:
    error = generate_type_error(typ, obj)
    assert isinstance(error, TypeError)
    assert isinstance(error, TypeCheckError)
    assert str(error) == error_msg
