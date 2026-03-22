from collections import deque
from collections.abc import Iterable, Sequence
import types
import typing
from typing import Self, TypeAliasType, cast, final

import attrs

from .utils import TypeAnnotation, is_in


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

    @property
    def _child_types_set(self) -> set[TypeAliasType]:
        return {child.typ for child in self.children}

    def __hash__(self) -> int:
        return hash(self.typ)


@attrs.frozen
class TypeAliasGraph:
    nodes: Sequence[TypeAliasNode]

    @classmethod
    def from_nodes(cls, nodes: Iterable[TypeAliasNode]) -> Self:
        return cls(tuple(nodes))

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
        return cls.from_nodes(type_alias_to_node.values())

    @classmethod
    def expand_type(cls, typ: TypeAnnotation) -> Iterable[TypeAliasType]:
        if isinstance(typ, typing.TypeAliasType):
            yield typ
        elif is_in(typing.get_origin(typ), (typing.Literal, typing.Union, types.UnionType)):
            for arg in typing.get_args(typ):
                yield from cls.expand_type(arg)

    def __eq__(self, other: object) -> bool:
        return isinstance(other, type(self)) and set(self.nodes) == set(other.nodes)
