import utils.tree
import utils.common_funcs as common_funcs
import pithon.ProblemGenerator as ProbGen
from copy import deepcopy

from pithon.number import FractionFactory, IntegerFactory


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
