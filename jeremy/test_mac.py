from manimlib import *


class Flip(Scene):
    def construct(self) -> None:
        axes = Axes()
        self.add(axes)
        line = axes.get_graph(lambda x: x, color=YELLOW)
        cos = axes.get_graph(np.cos, x_range=[0, PI], color=BLUE)
        self.add(cos, line)
        self.wait()
        self.play(cos.animate.flip(axis=UR, about_point=ORIGIN))
        self.wait()


class RotateThenFlip(Scene):
    def construct(self) -> None:
        axes = Axes()
        self.add(axes)
        line = axes.get_graph(lambda x: x, color=YELLOW)
        cos = axes.get_graph(np.cos, x_range=[0, PI], color=BLUE)
        self.add(cos, line)
        self.wait()
        self.play(Rotate(cos, PI/2, about_point=ORIGIN))
        self.wait()
        self.play(cos.animate.flip())
        self.wait()