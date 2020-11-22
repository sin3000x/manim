from manimlib.imports import *


class dots(Scene):
    def construct(self):
        dots = VGroup(*[Dot() for _ in range(10)]).arrange()
        # self.add(dots)

        def update_dot(d):
            d.scale(3)
            d.set_color(RED)
            return d

        self.play(AnimationGroup(*[
            ApplyFunction(update_dot, dot, rate_func=there_and_back) for dot in dots
        ], lag_ratio=.1))

        self.play(LaggedStartMap(GrowFromCenter, dots))