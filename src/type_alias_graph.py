from collections import deque
from collections.abc import Iterable, Sequence
import types
import typing
from typing import Self, TypeAliasType, cast, final

import attrs

from .utils import TypeAnnotation, is_in

type TypeAliasCycle = Sequence[TypeAliasType]


@final
@attrs.frozen
class TypeAliasNode:
    typ: TypeAliasType
    children: Sequence[Self] = attrs.field(factory=list)

    def __eq__(self, other: object) -> bool:
        return (
            isinstance(other, type(self))
            and self.typ == other.typ
            and self._child_types_set == other._child_types_set
        )

    def __hash__(self) -> int:
        return hash(self.typ)

    @property
    def _child_types_set(self) -> set[TypeAliasType]:
        return {child.typ for child in self.children}

    def find_cycle(self, history: list[Self], explored: set[Self]) -> list[Self] | None:
        try:
            return history[history.index(self) :]
        except ValueError:
            ...
        if self in explored:
            return None
        history.append(self)
        for child in self.children:
            if (cycle := child.find_cycle(history, explored)) is not None:
                return cycle
        explored.add(self)
        assert history[-1] == self
        history.pop()
        return None


@attrs.frozen
class TypeAliasGraph:
    root: TypeAliasNode

    @classmethod
    def from_type_alias_type(cls, typ: TypeAliasType) -> Self:
        type_alias_to_node: dict[TypeAliasType, TypeAliasNode] = {typ: TypeAliasNode(typ)}
        queue = deque([typ])
        while queue:
            current_typ = queue.popleft()
            for child in cls.expand_type(current_typ.__value__):
                if child in type_alias_to_node:
                    child_node = type_alias_to_node[child]
                else:
                    child_node = TypeAliasNode(child)
                    type_alias_to_node[child] = child_node
                    queue.append(child)
                cast(list[TypeAliasNode], type_alias_to_node[current_typ].children).append(
                    child_node
                )
        return cls(type_alias_to_node[typ])

    @classmethod
    def expand_type(cls, typ: TypeAnnotation) -> Iterable[TypeAliasType]:
        if isinstance(typ, typing.TypeAliasType):
            yield typ
        elif is_in(typing.get_origin(typ), (typing.Literal, typing.Union, types.UnionType)):
            for arg in typing.get_args(typ):
                yield from cls.expand_type(arg)

    @classmethod
    def find_cycle(cls, alias: TypeAliasType) -> TypeAliasCycle | None:
        graph = cls.from_type_alias_type(alias)
        cycle = graph.root.find_cycle([], set())
        if cycle is None:
            return None
        return [node.typ for node in cycle]
