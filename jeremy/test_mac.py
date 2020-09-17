from manimlib.imports import *


class Heine(GraphScene):
    CONFIG = {
        "x_min": -5,
        "x_max": 5,
        "y_min": -2,
        "y_max": 2,
        "graph_origin": ORIGIN,
    }

    def construct(self):
        self.opening()
        self.drawing()

    def opening(self):
        title = TextMobject("\\underline{\\textbf{Heine}\\heiti 定理}").set_color(YELLOW).to_corner(LEFT+TOP)
        self.play(Write(title))
        theorem = VGroup(TexMobject(r"\lim\limits_{x\to a}f(x)=L","\Longleftrightarrow").set_color_by_tex("\Longleftrightarrow", RED),
                         TextMobject(r"$ \forall x_n\to a,$",r"$\lim\limits_{n\to\infty}f(x_n)=L$")).arrange(RIGHT)
        self.play(Write(theorem[0]))
        self.wait()
        self.play(Write(theorem[1][0]))
        self.wait()
        self.play(Write(theorem[1][1:]))
        self.play(FadeOut(VGroup(title, *theorem)))

    def drawing(self):
        func = lambda x: np.sinc(x/np.pi)
        a_n = lambda n: 3 / (n)
        points_num = 15
        lim = TexMobject(r"\lim",r"_{x\to","0}",r"{\sin x\over x}","=","1")\
            .set_color_by_tex_to_color_map({"0": RED, r"{\sin x\over x}": BLUE, "1":YELLOW}).to_corner(UL)

        self.play(Write(lim))
        self.setup_axes(animate=True)
        func_graph = self.get_graph(func, x_min=-4.5, x_max=4.5)
        func_lab = self.get_graph_label(func_graph, label="y={\\sin x\\over x}", direction=DOWN)
        self.play(ShowCreation(func_graph))
        self.play(Write(func_lab))
        self.wait()

        x_dots = [Dot(self.coords_to_point(a_n(n), 0), color=RED) for n in range(1, points_num)]
        vert_lines = [DashedVMobject(self.get_vertical_line_to_graph(a_n(n), func_graph)) for n in range(1, points_num)]
        func_dots = [Dot(self.coords_to_point(a_n(n), func(a_n(n))), color=YELLOW) for n in range(1, points_num)]

        arrow = Arrow(RIGHT * 2, ORIGIN, color=WHITE).shift(DOWN * 0.5)
        arrow_lab = TexMobject(r"x_n", color=RED).next_to(arrow, DOWN, buff=SMALL_BUFF)
        curve_arrow = CurvedArrow(func_dots[1].get_center(), func_dots[-1].get_center(), angle=PI / 4, color=WHITE).shift(
            UP * 0.2)
        curve_lab = TexMobject(r"f\left(x_n\right)", color=YELLOW).next_to(curve_arrow, UP, buff=SMALL_BUFF)
        origin = Dot(color=WHITE)
        label_o = TextMobject("$0$", color=WHITE).next_to(ORIGIN, DL, buff=SMALL_BUFF)
        empty = Circle(arc_center=self.coords_to_point(0, 1), radius=.08, color=WHITE)
        label_1 = TextMobject("$1$", color=WHITE).next_to(empty, UL, buff=SMALL_BUFF)

        for x_dot in x_dots:
            self.add(x_dot)
            self.wait(.15)

        self.play(GrowArrow(arrow), FadeInFrom(arrow_lab, UP))
        # self.play(Write(arrow_lab))
        self.add(origin)
        self.play(Write(label_o))

        for i, (vert_line, func_dot) in enumerate(zip(vert_lines, func_dots)):
            self.play(ShowCreation(vert_line), run_time=.08)
            self.add(func_dot)
            self.wait(.1)
            self.remove(vert_line)
            self.wait(.1)

        self.play(GrowArrow(curve_arrow), FadeInFrom(curve_lab, DOWN))
        # self.play(Write(curve_lab))
        self.add(empty)
        self.play(Write(label_1))
        self.wait()
