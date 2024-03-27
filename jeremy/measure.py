from manimlib import *
from math import gcd

class OpenInterval(VGroup):
    def __init__(self, center_point=ORIGIN, width=2, scale=2):
        VGroup.__init__(self)
        left = Tex("(").scale(scale).align_to(LEFT * width/2, LEFT)
        right = Tex(")").scale(scale).align_to(RIGHT * width/2, RIGHT)
        self.add(left, right)
        self.shift(center_point)

class Fraction:
    def __init__(self, num, denom) -> None:
        self.numerator = num
        self.denominator = denom

    def __str__(self) -> str:
        return f"{self.numerator}/{self.denominator}"
    
    def __repr__(self) -> str:
        return self.__str__()

def rationals():
    curr = Fraction(1, 2)
    while True:
        yield curr
        if curr.numerator < curr.denominator - 1:
            new_numerator = curr.numerator + 1
            while gcd(new_numerator, curr.denominator) != 1:
                new_numerator += 1
            curr = Fraction(new_numerator, curr.denominator)
        else:
            curr = Fraction(1, curr.denominator + 1)
    
def fraction_mobject(fraction):
    n, d = fraction.numerator, fraction.denominator
    return Tex("\\frac{%d}{%d}"%(n, d))
           

class Opening(Scene):
    def construct(self) -> None:
        number_line = self.number_line = NumberLine(
            # x_range=(-1, 7),
            include_numbers=True,
            # include_tip=True
        ).next_to(ORIGIN, UP, buff=2)
        self.add(number_line)
        zero2one = self.get_line(0, 1)

        lengths = VGroup(
            *[VGroup(Tex(s, color=YELLOW), TexText("的长度: "), Tex(str(num))).arrange()
            for s, num in zip(["(0,1)", "(0,1)\\cup(2,4)", r"\{1\}", r"\mathbb{Z}", r"\{x\in[0,1]\mid \pi-x\not\in\mathbb{Q}\}"], [1, 3, 0, '?', '?'])]
        ).arrange(DOWN, buff=.25).shift(DOWN*.5)
        for i in range(1, len(lengths)):
            lengths[i][0].align_to(lengths[0][0], RIGHT)
            for j in range(1, len(lengths[i])):
                lengths[i][j].align_to(lengths[0][j], LEFT)
        lengths.set_x(-1)
        self.play(ShowCreation(zero2one))
        self.add(lengths)
        return super().construct()
    
    def get_line(self, start, end):
        return Line(
            self.number_line.n2p(start), 
            self.number_line.n2p(end),
            color=YELLOW,
            stroke_width=8
            )