import random as rdm
from fractions import Fraction


class IntegerFactory:
    def __init__(self, lower: int, upper: int):
        self.lower = lower
        self.upper = upper

    def create(self) -> int:
        return rdm.randint(self.lower, self.upper)


class FractionFactory:
    def __init__(self, num: IntegerFactory, den: IntegerFactory):
        self.num = num
        self.den = den

    def create(self) -> Fraction:
        numerator = self.num.create()
        denominator = self.den.create()
        return Fraction(numerator, denominator)
