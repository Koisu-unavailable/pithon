import random as rdm
import utils.tree
import utils.common_funcs as common_funcs
import pithon.ProblemGenerator as ProbGen
import math
from copy import deepcopy


class AlgebraGen(ProbGen.ProblemGenerator):
    def __init__(self):
        super().__init__()

    def generate_problem(self):
        """Returns the path to an image of the generated problem"""
        solution = rdm.randint(0, 100)
        
        return utils.render_latex(r"\frac{a}{b}")
    def gen_basic_linear(self, lower_x: float, upper_x: float, lower_m: float, upper_m: float, lower_b: float, upper_b: float, ):
        """Generate a basic linear equation in the form y=mx+b. where y,m,x,b are all integers

        Args:
            lower (int): lower bound for x
            upper (int): upper bound for x
        """
        # this is the solution to x
        solution = rdm.randint(lower_x, upper_x)
        solution_node = utils.tree.NumberNode(solution)
        # the m in y=mx+b
        m = rdm.randint(lower_m, upper_m)
        mx_node = utils.tree.MultiplicationNode([utils.tree.NumberNode(m), utils.tree.NumberNode(solution)])
        b = rdm.randint(lower_b, upper_b)
        addition_node = utils.tree.AdditionNode([mx_node, utils.tree.NumberNode(b)])
        expression_result = utils.tree.TREECOLLAPSER.collapse(deepcopy(addition_node), None, True)
        # we know the mx node is first, refer to the lines above
        addition_node.child[0] = utils.tree.MultiplicationNode([utils.tree.NumberNode(m), utils.tree.VariableNode("x")])
        utils.tree.print_tree(addition_node)
        return {
            "equation": utils.tree.TREECOLLAPSER.convert_tree_to_latex(addition_node).value + f" = {expression_result.value}", \
            "answer": solution
        }
if __name__ == "__main__":
    gen = AlgebraGen()
    gen.generate_problem()
