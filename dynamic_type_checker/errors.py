from collections.abc import Collection, Iterable
from typing import TypeAliasType

from .utils import TypeAnnotation


class MalformedTypeError(TypeError):
    def __init__(self, typ: TypeAnnotation, *, extra_msg: str = "") -> None:
        self.typ = typ
        super().__init__(self.make_msg(extra_msg))

    def make_msg(self, extra_msg: str) -> str:
        msg = f"{self.typ} is not a valid type."
        if extra_msg:
            assert extra_msg == extra_msg.strip()
            assert extra_msg[-1] in ".!?"
            msg += f" {extra_msg}"
        return msg

    @classmethod
    def requires_arguments_message(cls, typ: TypeAnnotation) -> str:
        return f"{typ} requires type arguments."


class CyclicTypeError(MalformedTypeError):
    def __init__(self, typ: TypeAnnotation, cycle: Collection[TypeAliasType]) -> None:
        self.cycle = cycle
        super().__init__(typ, extra_msg=self.cycle_msg(cycle))

    @classmethod
    def cycle_msg(cls, cycle: Collection[TypeAliasType]) -> str:
        assert len(cycle) > 0
        try:
            [typ] = cycle
        except ValueError:
            return cls.mutually_recursive_aliases_msg(cycle)
        return cls.recursive_alias_msg(typ)

    @classmethod
    def recursive_alias_msg(cls, alias: TypeAliasType) -> str:
        return f"The type alias {alias} is defined in terms of itself."

    @classmethod
    def mutually_recursive_aliases_msg(cls, cycle: Collection[TypeAliasType]) -> str:
        return f"The types {cls.list_aliases(cycle)} are defined in terms of each other."

    @classmethod
    def list_aliases(cls, aliases: Iterable[TypeAliasType]) -> str:
        [*first_types, last_type] = aliases
        return f"{str.join(', ', map(str, first_types))} and {last_type}"
