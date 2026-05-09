import random as rdm
import utils
import pithon.ProblemGenerator as ProbGen



class AlgebraGen(ProbGen.ProblemGenerator):
    def __init__(self):
        super().__init__()

    def generate_problem(self):
        """Returns the path to an image of the generated problem"""
        solution = rdm.randint(0, 100)
        
        return utils.render_latex(r"\frac{a}{b}")
    def gen_basic_linear(self, lower: int, upper: int):
        """Generate a basic linear equation in the form y=mx+b. where y,m,x,b are all integers

        Args:
            lower (int): lower bound for answer
            upper (int): upper bound for answer
        """
        solution = rdm.randint(lower, upper)
if __name__ == "__main__":
    gen = AlgebraGen()
    gen.generate_problem()
