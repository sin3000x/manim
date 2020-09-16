from manimlib.imports import *


class test(GraphScene, Scene):
    CONFIG = {
        "x_min": -5,
        "x_max": 5,
        "y_min": -2,
        "y_max": 2,
        "graph_origin": ORIGIN,
    }

    def construct(self):
        self.drawing()

    def drawing(self):
        self.setup_axes(animate=False)
        func_graph = self.get_graph(self.func, x_min=-4.5, x_max=4.5)
        func_lab = self.get_graph_label(func_graph, label="y={\\sin x\\over x}", direction=DOWN)
        self.play(ShowCreation(func_graph))
        self.play(Write(func_lab))
        self.wait()

        x_dots = [Dot(self.coords_to_point(self.a_n(n), 0), color=WHITE) for n in range(1, 20)]
        vert_lines = [DashedVMobject(self.get_vertical_line_to_graph(self.a_n(n), func_graph)) for n in range(1, 20)]
        func_dots = [Dot(self.coords_to_point(self.a_n(n), self.func(self.a_n(n))), color=WHITE) for n in range(1, 20)]

        for x_dot in x_dots:
            self.add(x_dot)
            self.wait(.15)

        for i, (vert_line, func_dot) in enumerate(zip(vert_lines, func_dots)):
            self.play(ShowCreation(vert_line), run_time=.1)
            self.add(func_dot)
            self.wait(.3/(i+1))
            self.remove(vert_line)
            self.wait(.1)

        # arrow = Line(RIGHT*2, ORIGIN).shift(DOWN*0.5)
        # curve_arrow = CurvedArrow(func_dots[1].get_center(), func_dots[-1].get_center())
        origin = Dot(color=YELLOW)
        label_o = TextMobject("$0$").next_to(ORIGIN, DL, buff=SMALL_BUFF)
        empty = Circle(arc_center=self.coords_to_point(0, 1), radius=.08, color=YELLOW)
        label_1 = TextMobject("$1$").next_to(empty, UL, buff=SMALL_BUFF)
        # self.play(GrowArrow(arrow))
        self.add(origin)
        self.play(Write(label_o))
        self.wait(1)
        # self.play(FadeIn(curve_arrow))
        self.add(empty)
        self.play(Write(label_1))
        self.wait()


    @staticmethod
    def func(x):
        return float(np.sinc(x / np.pi))

    @staticmethod
    def a_n(n):
        return 3/n


