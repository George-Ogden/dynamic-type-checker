from typing import NamedTuple, Self, TypeAliasType, cast

import pytest
from utils.test_utils import test_case

from .test_utils import (
    DiamondType,
    IntAlias,
    IntAliasAlias,
    MutuallyRecursiveTypeAlias1,
    MutuallyRecursiveTypeAlias2,
    One,
    RecursiveLiteralType,
    RecursiveTypeAlias,
    RecursiveUnionType,
    Zero,
    ZeroOrOneLiteral,
    ZeroOrOneUnion,
)
from .type_alias_graph import TypeAliasCycle, TypeAliasGraph, TypeAliasNode


@test_case
class TypeAliasGraphFromTypeAliasTestCase(NamedTuple):
    type_alias: TypeAliasType
    expected: TypeAliasGraph

    @classmethod
    def trivial_type_alias_graph(cls) -> Self:
        type_alias = IntAlias
        node = TypeAliasNode(type_alias, [])
        return cls(type_alias, TypeAliasGraph(node))

    @classmethod
    def recursive_type_alias_graph(cls) -> Self:
        type_alias = RecursiveTypeAlias
        node = TypeAliasNode(type_alias, [])
        cast(list[TypeAliasNode], node.children).append(node)
        return cls(type_alias, TypeAliasGraph(node))

    @classmethod
    def literal_aliases_type_alias_graph(cls) -> Self:
        zero_child = TypeAliasNode(Zero, [])
        one_child = TypeAliasNode(One, [])
        type_alias = ZeroOrOneLiteral
        parent = TypeAliasNode(type_alias, [zero_child, one_child])
        return cls(type_alias, TypeAliasGraph(parent))

    @classmethod
    def union_of_aliases_type_alias_graph(cls) -> Self:
        zero_child = TypeAliasNode(Zero, [])
        one_child = TypeAliasNode(One, [])
        type_alias = ZeroOrOneUnion
        parent = TypeAliasNode(type_alias, [zero_child, one_child])
        return cls(type_alias, TypeAliasGraph(parent))

    @classmethod
    def diamond_type_alias_graph(cls) -> Self:
        int_alias_child = TypeAliasNode(IntAlias, [])
        int_alias_alias_child = TypeAliasNode(IntAliasAlias, [int_alias_child])
        type_alias = DiamondType
        diamond_node = TypeAliasNode(type_alias, [int_alias_child, int_alias_alias_child])
        return cls(type_alias, TypeAliasGraph(diamond_node))

    @classmethod
    def recursive_union_type_alias_graph(cls) -> Self:
        type_alias = RecursiveUnionType
        node = TypeAliasNode(type_alias, [])
        cast(list[TypeAliasNode], node.children).append(node)
        return cls(type_alias, TypeAliasGraph(node))

    @classmethod
    def mutually_recursive_type_alias_graph(cls) -> Self:
        left_type_alias = MutuallyRecursiveTypeAlias1
        right_type_alias = MutuallyRecursiveTypeAlias2
        left_node = TypeAliasNode(left_type_alias, [])
        right_node = TypeAliasNode(right_type_alias, [])
        cast(list[TypeAliasNode], left_node.children).append(right_node)
        cast(list[TypeAliasNode], right_node.children).append(left_node)
        return cls(left_type_alias, TypeAliasGraph(left_node))


@pytest.mark.parametrize("case", TypeAliasGraphFromTypeAliasTestCase.cases())
def test_type_alias_graph_from_type_alias(case: TypeAliasGraphFromTypeAliasTestCase) -> None:
    TypeAliasGraph.from_type_alias_type(case.type_alias)._assert_test_eq(case.expected)


@test_case
class TypeAliasGraphEqualityTestCases(NamedTuple):
    left: TypeAliasNode
    right: TypeAliasNode

    @classmethod
    def different_aliases(cls) -> Self:
        return cls(TypeAliasNode(IntAlias, []), TypeAliasNode(IntAliasAlias, []))

    @classmethod
    def different_child_lengths(cls) -> Self:
        return cls(
            TypeAliasNode(IntAliasAlias, []),
            TypeAliasNode(IntAliasAlias, [TypeAliasNode(IntAlias, [])]),
        )

    @classmethod
    def nested_failure(cls) -> Self:
        type_alias = RecursiveTypeAlias
        single_node = TypeAliasNode(type_alias, [])
        cast(list[TypeAliasNode], single_node.children).append(single_node)
        first_double_node = TypeAliasNode(type_alias, [])
        second_double_node = TypeAliasNode(type_alias, [])
        cast(list[TypeAliasNode], first_double_node.children).append(second_double_node)
        cast(list[TypeAliasNode], second_double_node.children).append(first_double_node)
        return cls(single_node, second_double_node)

    @classmethod
    def mutually_recursive_type_alias_graph(cls) -> Self:
        left_type_alias = MutuallyRecursiveTypeAlias1
        right_type_alias = MutuallyRecursiveTypeAlias2
        left_node = TypeAliasNode(left_type_alias, [])
        right_node = TypeAliasNode(right_type_alias, [])
        cast(list[TypeAliasNode], left_node.children).append(right_node)
        cast(list[TypeAliasNode], right_node.children).append(left_node)
        return cls(left_node, right_node)


@pytest.mark.parametrize("case", TypeAliasGraphEqualityTestCases.cases())
def test_type_aliases_not_equal(case: TypeAliasGraphEqualityTestCases) -> None:
    left = TypeAliasGraph(case.left)
    right = TypeAliasGraph(case.right)
    with pytest.raises(AssertionError):
        left._assert_test_eq(right)
    with pytest.raises(AssertionError):
        right._assert_test_eq(left)


@pytest.mark.parametrize(
    "alias, cycle",
    [
        (IntAlias, None),
        (IntAliasAlias, None),
        (ZeroOrOneLiteral, None),
        (ZeroOrOneUnion, None),
        (RecursiveTypeAlias, [RecursiveTypeAlias]),
        (MutuallyRecursiveTypeAlias1, [MutuallyRecursiveTypeAlias1, MutuallyRecursiveTypeAlias2]),
        (RecursiveLiteralType, [RecursiveLiteralType]),
        (DiamondType, None),
    ],
)
def test_graph_find_cycle(alias: TypeAliasType, cycle: TypeAliasCycle | None) -> None:
    assert TypeAliasGraph.find_cycle(alias) == cycle
