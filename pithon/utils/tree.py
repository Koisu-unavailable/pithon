from __future__ import annotations
from typing import Callable, Optional


class Node:
    def __init__(self, value, child, convert_to_latex: Callable[[Node], LatexNode]) -> None:
        self.value = value
        self.child = child
        self.parent = None
        self.convert_to_latex = convert_to_latex

    def __repr__(self) -> str:
        return f"{self.__class__.__qualname__} {{value: {self.value}, child: {self.child}}}"


class LatexNode(Node):
    def __init__(self, value):
        super().__init__(value, None, None)

class NumberNode(Node):
    def __init__(self, value):
        super().__init__(value, None, num_to_latex)


class VariableNode(Node):
    def __init__(self, value: str) -> None:
        super().__init__(value, None, lambda: value)


class OperationNode(Node):
    def __init__(
        self,
        value: Callable[[float, float], float],
        child: list[Node],
        convert_to_latex,
        priority: int
    ) -> None:
        super().__init__(value, child, convert_to_latex)
        self.priority = priority
        for child in self.child:
            child.parent = self


class UnaryOperationNode(Node):
    def __init__(
        self, value: Callable[[float], float], child: NumberNode | VariableNode, convert_to_latex
    ) -> None:
        super().__init__(value, child, convert_to_latex)  # type: ignore
        self.child.parent = self


def print_tree(node, indent="", is_last=True):
    """Pretty-print the AST as a tree."""
    branch = "└── " if is_last else "├── "
    print(indent + branch + node_label(node))

    # Prepare indentation for children
    if is_last:
        new_indent = indent + "    "
    else:
        new_indent = indent + "│   "

    # Handle leaf nodes
    if not hasattr(node, "child") or node.child is None:
        return

    # Normalize children into a list
    children = node.child if isinstance(node.child, list) else [node.child]

    # Print children
    for i, child in enumerate(children):
        print_tree(child, new_indent, i == len(children) - 1)


def node_label(node):
    """Return a readable label for each node type."""
    if isinstance(node, NumberNode):
        return f"Number({node.value})"
    if isinstance(node, VariableNode):
        return f"Var({node.value})"
    if isinstance(node, UnaryOperationNode):
        return f"UnaryOp({node.convert_to_latex.__name__})"
    if isinstance(node, OperationNode):
        return f"({node.convert_to_latex.__name__})"
    return f"Node({node.value})"


class TreeCollapser:
    """TreeCollapser.collapse is part of a class to keep track of state during recursive function calls."""

    def __init__(self) -> None:
        self.seen = []
        self.seen_ref = []
        self.start: OperationNode
        self.iters = 0

    def collapse(
        self, node: Node, previous_level: Optional[Node], first_call: bool = False
    ):
        self.iters += 1
        if node is None:
            print("Reached None node — stopping collapse")
            return None
        if first_call:
            self.seen = []
            self.start = node
        if not isinstance(node, OperationNode) and first_call:
            raise TypeError("First node must be an operation node")
        if isinstance(node, UnaryOperationNode):
            if not isinstance(node.child, NumberNode):
                return self.collapse(node.child, node)
            result = NumberNode(node.value(node.child.value), num_to_latex)
            print(result)
            if previous_level.child == node:
                previous_level.child = result
            else:  # it's a list
                index_of_node = previous_level.child.index(node)
                previous_level.child[index_of_node] = result
            if len(self.seen) < 3:
                return self.collapse(previous_level, previous_level.parent)
            else:
                return self.collapse(previous_level, previous_level.parent)
        else:  # is opeation node
            if not isinstance(node.child[0], NumberNode):
                return self.collapse(node.child[0], node)
            if not isinstance(node.child[1], NumberNode):
                return self.collapse(node.child[1], node)
            result = NumberNode(node.value(node.child[0].value, node.child[1].value), num_to_latex)
            print(result)
            
            if previous_level is None:
                return result
            if isinstance(previous_level, UnaryOperationNode):
                previous_level.child = node
            else:
                if previous_level.child[0] == node:
                    previous_level.child = [result, previous_level.child[1]]
                else:
                    previous_level.child = [previous_level.child[0], result]
            
            return self.collapse(previous_level, previous_level.parent)

    def convert_tree_to_latex(self, node: Node) -> LatexNode:
        if isinstance(node, OperationNode):
            for i in [0,1]:
                node.child[i] = self.convert_tree_to_latex(node.child[i])
            latex = node.convert_to_latex(node)
            if isinstance(node.parent, OperationNode):
                if node.priority >= node.parent.priority:
                    latex.value = r"\left(" + latex.value + r"\right)"
            return latex
        if isinstance(node, UnaryOperationNode):
            node.child = self.convert_tree_to_latex(node.child)
            return node.convert_to_latex(node)
        if isinstance(node, NumberNode) or isinstance(node, VariableNode):
            return node.convert_to_latex(node)
        if isinstance(node, LatexNode):
            return node



def num_to_latex(node):
    return LatexNode(str(node.value))


def add_to_latex(node):
    return LatexNode(f"{node.child[0].value} + {node.child[1].value}")


def mul_to_latex(node: OperationNode):
    latex = ""
    for element in node.child:
        if not isinstance(e, VariableNode) or not isinstance(e, NumberNode):
            break
    else:
        latex = f"{[child for child in node.child if isinstance(child, NumberNode )][0]}{[child for child in node.child if isinstance(child, VariableNode )][0]}"
    return LatexNode(f"{node.child[0].value} \\cdot {node.child[1].value}")


def pow_to_latex(node):
    return LatexNode(f"{node.child[0].value}^{{{node.child[1].value}}}")


def sub_to_latex(node):
    return LatexNode(f"{node.child[0].value} - {node.child[1].value}")


def sqrt_to_latex(node):
    return LatexNode(f"\\sqrt{{{node.child.value}}}")


print(isinstance(OperationNode((lambda x,y: x+y), [NumberNode(9), VariableNode("x")], mul_to_latex, 2).child , list[VariableNode | OperationNode]))

# import copy
# beginning = OperationNode(
#     lambda x, y: x + y,
#     [
#         OperationNode(
#             lambda x, y: x * y,
#             [
#                 NumberNode(9, num_to_latex),
#                 NumberNode(2, num_to_latex)
#             ],
#             mul_to_latex,
#             2
#         ),
#         OperationNode(
#             lambda x, y: x * y,
#             [
#                 OperationNode(
#                     lambda x, y: x**y,
#                     [
#                         NumberNode(2, num_to_latex),
#                         NumberNode(2, num_to_latex)
#                     ],
#                     pow_to_latex,
#                     1
#                 ),
#                 OperationNode(
#                     lambda x, y: x - y,
#                     [
#                         UnaryOperationNode(
#                             lambda x: x ** (1 / 2),
#                             NumberNode(64, num_to_latex),
#                             sqrt_to_latex
#                         ),
#                         NumberNode(2, num_to_latex),
#                     ],
#                     sub_to_latex,
#                     3
#                 ),
#             ],
#             mul_to_latex,
#             2
#         ),
#     ],
#     add_to_latex,
#     3
# )

# treeCollapser = TreeCollapser()
# print_tree(beginning)
# print("SKSK: ", treeCollapser.convert_tree_to_latex(copy.deepcopy(beginning)))
# print(treeCollapser.collapse(beginning, None, first_call=True))



