from fractions import Fraction

from pithon.algebra import AlgebraGen, QuadraticForm
from pithon.number import FractionFactory, IntegerFactory


class StubIntegerFactory(IntegerFactory):
    def __init__(self, value: int):
        self.value = value

    def create(self) -> int:
        return self.value


class StubFractionFactory(FractionFactory):
    def __init__(self, value: Fraction):
        self.value = value

    def create(self) -> Fraction:
        return self.value


def test_basic_linear_generation_is_mathematically_sound():
    generator = AlgebraGen()
    solution = 4
    slope = 3
    intercept = 5

    problem = generator.gen_basic_linear(
        StubIntegerFactory(solution),
        StubIntegerFactory(slope),
        StubIntegerFactory(intercept),
    )

    assert problem["answer"] == solution
    assert problem["equation"] == r"3 \cdot x + 5 = 17"


def test_fractional_linear_generation_is_mathematically_sound():
    generator = AlgebraGen()
    solution = Fraction(1, 2)
    slope = Fraction(2, 3)
    intercept = Fraction(3, 4)
    expected_rhs = slope * solution + intercept

    problem = generator.gen_basic_linear_fractional(
        StubFractionFactory(solution),
        StubFractionFactory(slope),
        StubFractionFactory(intercept),
    )

    assert problem["answer"] == solution
    assert problem["equation"] == r"\left(\frac{2}{3}\right) \cdot x + \frac{3}{4} = \frac{13}{12}"
    assert expected_rhs == Fraction(13, 12)



