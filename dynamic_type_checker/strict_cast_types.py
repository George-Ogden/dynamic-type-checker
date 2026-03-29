"""This file is for the type checker to test on (not to be run directly)."""

from collections.abc import Sequence
import sys
import types
import typing
from typing import Any, assert_type, cast

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

# Unclear why this fails. See https://github.com/python/mypy/issues/20859.
assert_type(strict_cast(typing.Any, "abc"), Any)  # type: ignore [assert-type]

assert_type(strict_cast(typing.NoReturn, lambda: None), typing.Any)
assert_type(strict_cast(typing.Never, sys.exit()), typing.Any)
