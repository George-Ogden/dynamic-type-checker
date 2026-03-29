from __future__ import annotations

from collections import deque
from collections.abc import Iterable, Sequence
import contextlib
import types
import typing
from typing import TYPE_CHECKING, Self, TypeAliasType, cast, final

import attrs

from .utils import TypeAnnotation, is_in

type TypeAliasCycle = Sequence[TypeAliasType]

if TYPE_CHECKING:
    from bidict import bidict


@final
@attrs.frozen
class TypeAliasNode:
    typ: TypeAliasType
    children: Sequence[Self] = attrs.field(factory=list, eq=False, hash=False)

    def find_cycle(self, history: list[Self], explored: set[Self]) -> list[Self] | None:
        with contextlib.suppress(ValueError):
            return history[history.index(self) :]
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

    def _assert_test_eq(self, other: Self, equality: bidict) -> None:
        assert self.typ == other.typ
        if id(self) in equality:
            assert equality[id(self)] == id(other)
            return
        equality[id(self)] = id(other)
        for self_child, other_child in zip(self.children, other.children, strict=True):
            self_child._assert_test_eq(other_child, equality)


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

    def _assert_test_eq(self, other: Self) -> None:
        from bidict import bidict

        try:
            return self.root._assert_test_eq(other.root, bidict())
        except Exception as e:
            raise AssertionError(f"{self} != {other}") from e
