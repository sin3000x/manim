from manimlib.imports import *

class SquareToCircle(Scene):
    def construct(self):
        l = Logo()
        self.play(ShowCreation(l), run_time=8)