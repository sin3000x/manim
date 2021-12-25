from manimlib import *


class Chang(Scene):
    def construct(self):
        hello = Text("你好")
        self.play(Write(hello))
        self.wait()
        self.embed()


class Tu(Scene):
    def construct(self):
        v = Vocabulary()
        self.add(v)


class Test(Scene):
    def construct(self):
        plane = NumberPlane()
        self.add(plane)
        line = Line(LEFT, RIGHT).set_color(RED)
        self.add(line)
        self.wait()
        x = np.linspace(-1, 1, 1000)
        y = np.linspace(0, 1, 1000)

        curve = ComplexContour(
            lambda zz: np.abs(((zz+1)*np.log(zz+1) - (zz-1)*np.log(zz-1)).real),
            2*np.log(2),
            x_unit = 3,
            y_unit = 3
        ).set_color(RED)
        self.play(RT(line, curve))
        self.wait()

