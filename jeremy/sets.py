from manimlib import *


class Opening(Scene):
    def construct(self):
        origin = Square(color=BLACK).to_edge(UP).set_fill(BLUE, opacity=1)
        edges = origin.get_edges().set_color(WHITE)

        self.add(origin, *edges[:2])