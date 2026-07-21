from __future__ import annotations

from typing import Callable, Literal


class Node():
    def __init__(self, value, child, beginning=False) -> None:
        self.value = value
        self.child = child
        self.beginning = beginning

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__qualname__} {{value: {self.value}, child: {self.child}, beginning: {self.beginning}}}"
        )


class NumberNode(Node):
    def __init__(
        self, value: float, child: OperationNode | None, beginning=False
    ) -> None:
        super().__init__(value, child, beginning)


class OperationNode(Node):
    def __init__(
        self,
        value: Callable[[float, float], float],
        child: VariableNode | NumberNode | UnaryOperationNode,
        beginning=False,
    ) -> None:
        super().__init__(value, child, beginning)

    def __call__(self, parent: NumberNode) -> NumberNode:
        return NumberNode(self.value(parent.value, self.child.value), self.child.child)


class UnaryOperationNode(Node):
    def __init__(
        self, value: Callable[[float], float], child: NumberNode, beginning=False
    ) -> None:
        super().__init__(value, child, beginning)

    def __call__(self) -> NumberNode:
        return NumberNode(self.value(self.child), self.child.child)


class VariableNode(Node):
    def __init__(self, value: str, child: OperationNode, beginning=False) -> None:
        super().__init__(value, child, beginning)


def collapse(node, first_call: bool = False):
    print("running")
    print(node)
    if not node.beginning and first_call:
        raise ValueError("Node is not the start.")
    print(node)
    if not node.child:
        return node

    child = node.child
    result = None
    print("child is: ", child)
    result = child(node)
    collapse(result)


start = NumberNode(
        1,
        OperationNode(
            lambda x, y: x + y,
            NumberNode(
                1,
                OperationNode(
                    lambda x, y: x / y,
                    UnaryOperationNode(lambda x: x**2, NumberNode(2, None)),
                ),
            ),
        ),
        True
    )
    

collapse(start, True)
