from enum import Enum
from fractions import Fraction

import utils.tree
import pithon.ProblemGenerator as ProbGen
from copy import deepcopy

from pithon.number import FractionFactory, IntegerFactory


class QuadraticForm(Enum):
    PURE_SQUARE = "pure_square"
    SQUARE_PLUS_CONSTANT = "square_plus_constant"
    SQUARE_PLUS_LINEAR = "square_plus_linear"
    GENERAL = "general"
    FACTORED = "factored"


class AlgebraGen(ProbGen.ProblemGenerator):
    def __init__(self):
        super().__init__()

    @staticmethod
    def _fraction_node(numerator: int, denominator: int):
        if denominator == 1:
            return utils.tree.NumberNode(numerator)
        return utils.tree.DivisionNode([
            utils.tree.NumberNode(numerator),
            utils.tree.NumberNode(denominator),
        ])

    @staticmethod
    def _format_number(value: int | Fraction) -> str:
        if isinstance(value, Fraction):
            if value.denominator == 1:
                return str(value.numerator)
            return rf"\left(\frac{{{value.numerator}}}{{{value.denominator}}}\right)"
        return str(value)

    @staticmethod
    def _create_number(factory: IntegerFactory | FractionFactory) -> int | Fraction:
        value = factory.create()
        if isinstance(value, Fraction):
            return value
        return value

    @staticmethod
    def _format_factored_term(value: int | Fraction) -> str:
        formatted = AlgebraGen._format_number(value)
        if value >= 0:
            return f" + {formatted}"
        return f" - {abs(value) if isinstance(value, int) else abs(value.numerator) if value.denominator == 1 else AlgebraGen._format_number(abs(value))}"

    def gen_quadratic(
        self,
        form: QuadraticForm,
        solution_factory: IntegerFactory | FractionFactory,
        factory_map: dict[str, IntegerFactory | FractionFactory],
    ):
        """Generate a quadratic equation where the answer is constructed from the chosen solution."""
        solution = self._create_number(solution_factory)

        if form == QuadraticForm.PURE_SQUARE:
            rhs = solution**2
            return {
                "equation": rf"x^2 = {self._format_number(rhs)}",
                "answer": solution,
            }

        if form == QuadraticForm.SQUARE_PLUS_CONSTANT:
            k = self._create_number(factory_map["k"])
            rhs = solution**2 + k
            return {
                "equation": rf"x^2 + {self._format_number(k)} = {self._format_number(rhs)}",
                "answer": solution,
            }

        if form == QuadraticForm.SQUARE_PLUS_LINEAR:
            b = self._create_number(factory_map["b"])
            rhs = solution**2 + b * solution
            return {
                "equation": rf"x^2 + {self._format_number(b)}x = {self._format_number(rhs)}",
                "answer": solution,
            }

        if form == QuadraticForm.GENERAL:
            a = self._create_number(factory_map["a"])
            b = self._create_number(factory_map["b"])
            c = self._create_number(factory_map["c"])
            rhs = a * solution**2 + b * solution + c
            return {
                "equation": rf"{self._format_number(a)}x^2 + {self._format_number(b)}x + {self._format_number(c)} = {self._format_number(rhs)}",
                "answer": solution,
            }

        if form == QuadraticForm.FACTORED:
            h = self._create_number(factory_map["h"])
            k = self._create_number(factory_map["k"])
            rhs = (solution + h) * (solution + k)
            return {
                "equation": rf"\left(x{self._format_factored_term(h)}\right)\left(x{self._format_factored_term(k)}\right) = {self._format_number(rhs)}",
                "answer": solution,
            }

        raise ValueError(f"Unsupported quadratic form: {form}")

    def generate_problem(self):
        """Returns the path to an image of the generated problem"""
        return utils.render_latex(r"\frac{a}{b}")

    def gen_basic_linear(self, solution_factory: IntegerFactory, m_factory: IntegerFactory, b_factory: IntegerFactory):
        """Generate a basic linear equation in the form y=mx+b where y, m, x, and b are integers."""
        solution = solution_factory.create()
        m = m_factory.create()
        b = b_factory.create()

        mx_node = utils.tree.MultiplicationNode([utils.tree.NumberNode(m), utils.tree.NumberNode(solution)])
        addition_node = utils.tree.AdditionNode([mx_node, utils.tree.NumberNode(b)])
        expression_result = utils.tree.TREECOLLAPSER.collapse(deepcopy(addition_node), None, True)
        # we know the mx node is first, refer to the lines above
        addition_node.child[0] = utils.tree.MultiplicationNode([utils.tree.NumberNode(m), utils.tree.VariableNode("x")])
        utils.tree.print_tree(addition_node)
        return {
            "equation": utils.tree.TREECOLLAPSER.convert_tree_to_latex(addition_node).value + f" = {expression_result.value}",
            "answer": solution,
        }

    def gen_basic_linear_fractional(
        self,
        solution_factory: FractionFactory,
        m_factory: FractionFactory,
        b_factory: FractionFactory,
    ):
        """Generate a linear equation where the solution, slope, and intercept are fractional values."""
        solution = solution_factory.create()
        m = m_factory.create()
        b = b_factory.create()

        result = m * solution + b

        m_node = self._fraction_node(m.numerator, m.denominator)
        b_node = self._fraction_node(b.numerator, b.denominator)
        result_node = self._fraction_node(result.numerator, result.denominator)

        equation_node = utils.tree.AdditionNode([
            utils.tree.MultiplicationNode([m_node, utils.tree.VariableNode("x")]),
            b_node,
        ])

        return {
            "equation": utils.tree.TREECOLLAPSER.convert_tree_to_latex(equation_node).value + f" = {utils.tree.TREECOLLAPSER.convert_tree_to_latex(result_node).value}",
            "answer": solution,
        }


if __name__ == "__main__":
    gen = AlgebraGen()
    gen.generate_problem()
