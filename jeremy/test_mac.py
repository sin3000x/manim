from manimlib import *


class Chang(Scene):
    def construct(self):
        hello = Text("妈妈")
        self.play(Write(hello))
        self.wait()
        self.embed()

class Tu(Scene):
    def construct(self):
        v = Vocabulary()
        self.add(v)


class Test(Scene):
    def construct(self):
        plane = NumberPlane(axis_config={"unit_size": 2})
        self.add(plane)
        self.play(plane.apply_matrix, [[1,1],[0,1]], run_time=2)
        self.wait()
