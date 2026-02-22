"""This file is for the type checker to test on (not to be run directly)."""

from collections.abc import Sequence
import types
from typing import assert_type, cast

from . import strict_cast

assert_type(strict_cast(int, 10), int)
assert_type(strict_cast(str, ["a", "b"]), str)
assert_type(strict_cast(float, 10.0), float)
assert_type(strict_cast(list, cast(Sequence, [])), list)


class CustomClass: ...


assert_type(strict_cast(CustomClass, CustomClass()), CustomClass)
assert_type(strict_cast(CustomClass, ()), CustomClass)

assert_type(strict_cast(None, 0), None)
assert_type(strict_cast(None, None), None)
assert_type(strict_cast(types.NoneType, ()), None)
