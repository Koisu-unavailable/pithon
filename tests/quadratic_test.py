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


def test_quadratic_pure_square_generation_is_mathematically_sound():
    generator = AlgebraGen()
    solution = 4

    problem = generator.gen_quadratic(
        QuadraticForm.PURE_SQUARE,
        StubIntegerFactory(solution),
        {},
    )

    assert problem["answer"] == solution
    assert problem["equation"] == r"x^2 = 16"


def test_quadratic_square_plus_constant_generation_is_mathematically_sound():
    generator = AlgebraGen()
    solution = 4
    k = 3

    problem = generator.gen_quadratic(
        QuadraticForm.SQUARE_PLUS_CONSTANT,
        StubIntegerFactory(solution),
        {"k": StubIntegerFactory(k)},
    )

    assert problem["answer"] == solution
    assert problem["equation"] == r"x^2 + 3 = 19"


def test_quadratic_square_plus_linear_generation_is_mathematically_sound():
    generator = AlgebraGen()
    solution = 4
    b = 2

    problem = generator.gen_quadratic(
        QuadraticForm.SQUARE_PLUS_LINEAR,
        StubIntegerFactory(solution),
        {"b": StubIntegerFactory(b)},
    )

    assert problem["answer"] == solution
    assert problem["equation"] == r"x^2 + 2x = 24"


def test_quadratic_general_generation_is_mathematically_sound():
    generator = AlgebraGen()
    solution = 4
    a = 2
    b = 3
    c = 5

    problem = generator.gen_quadratic(
        QuadraticForm.GENERAL,
        StubIntegerFactory(solution),
        {
            "a": StubIntegerFactory(a),
            "b": StubIntegerFactory(b),
            "c": StubIntegerFactory(c),
        },
    )

    assert problem["answer"] == solution
    assert problem["equation"] == r"2x^2 + 3x + 5 = 49"


def test_quadratic_factored_generation_is_mathematically_sound():
    generator = AlgebraGen()
    solution = 4
    h = 1
    k = 2

    problem = generator.gen_quadratic(
        QuadraticForm.FACTORED,
        StubIntegerFactory(solution),
        {
            "h": StubIntegerFactory(h),
            "k": StubIntegerFactory(k),
        },
    )

    assert problem["answer"] == solution
    assert problem["equation"] == r"\left(x + 1\right)\left(x + 2\right) = 30"
