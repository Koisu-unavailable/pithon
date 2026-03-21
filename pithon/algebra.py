import random as rdm
import utils
import satmathbot.genmath.ProblemGenerator as ProbGen
import sympy


class AlgebraGen(ProbGen.ProblemGenerator):
    def __init__(self):
        super().__init__()

    def generate_problem(self):
        """Returns the path to an image of the generated problem"""
        solution = rdm.randint(0, 100)
        sympy.
        return utils.render_latex(r"\frac{a}{b}")


if __name__ == "__main__":
    gen = AlgebraGen()
    gen.generate_problem()
