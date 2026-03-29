"""This file is for the type checker to test on (not to be run directly)."""

import types
import typing
from typing import assert_type

from . import check_type

assert_type(check_type(int, 0), bool)
assert_type(check_type(float, 0), bool)
assert_type(check_type(list, ()), bool)
assert_type(check_type(None, ()), bool)
assert_type(check_type(types.NoneType, None), bool)
assert_type(check_type(typing.Any, str), bool)
