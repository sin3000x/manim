from manimlib.imports import *

# Heine定理
class Heine(GraphScene):
    CONFIG = {
        "x_min": -5,
        "x_max": 5,
        "y_min": -2,
        "y_max": 2,
        "graph_origin": ORIGIN,
        "theorem": VGroup(
            TexMobject(r"\lim\limits_{x\to a}f(x)=L", "\Longleftrightarrow").set_color_by_tex("\Longleftrightarrow",
                                                                                              RED),
            TextMobject(r"$ \forall x_n\to a$", r",",r"$\lim\limits_{n\to\infty}f(x_n)=L$")).arrange(RIGHT),
        "title": TextMobject("\\underline{\\textbf{Heine}\\heiti 定理}").set_color(YELLOW).to_corner(
            LEFT + TOP),
    }

    # def __init__(self, **kwargs):
    #     super().__init__(**kwargs)
    #     self.theorem = VGroup(
    #         TexMobject(r"\lim\limits_{x\to a}f(x)=L", "\Longleftrightarrow").set_color_by_tex("\Longleftrightarrow",
    #                                                                                           RED),
    #         TextMobject(r"$ \forall x_n\to a,$", r"$\lim\limits_{n\to\infty}f(x_n)=L$")).arrange(RIGHT)
    #     self.title = TextMobject("\\underline{\\textbf{Heine}\\heiti 定理}").set_color(YELLOW).to_corner(
    #         LEFT + TOP)

    def construct(self):
        self.opening()
        self.drawing()
        # self.proof()
        self.proof1()
        self.proof2()

    def opening(self):
        theorem = self.theorem
        title = self.title
        self.play(Write(title))
        self.play(Write(theorem[0]))
        self.wait()
        self.play(Write(theorem[1][0]))
        self.wait()
        self.play(Write(theorem[1][1:]))
        self.wait()
        self.play(FadeOut(VGroup(title, *theorem)))

    def drawing(self):
        func = lambda x: np.sinc(x / np.pi)
        a_n = lambda n: 3 / (n)
        points_num = 15
        lim = TexMobject(r"\lim", r"_{x\to", "0}", r"{\sin x\over x}", "=", "1") \
            .set_color_by_tex_to_color_map({"0": RED, r"{\sin x\over x}": BLUE, "1": YELLOW}).to_corner(UL)

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
        curve_arrow = CurvedArrow(func_dots[1].get_center(), func_dots[-1].get_center(), angle=PI / 4,
                                  color=WHITE).shift(
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
        self.play(Write(origin))
        self.play(Write(label_o))

        for i, (vert_line, func_dot) in enumerate(zip(vert_lines, func_dots)):
            self.play(ShowCreation(vert_line), run_time=.08)
            self.add(func_dot)
            self.wait(.1)
            self.remove(vert_line)
            self.wait(.1)

        self.play(GrowArrow(curve_arrow), FadeInFrom(curve_lab, DOWN))
        # self.play(Write(curve_lab))
        self.play(Write(empty))
        self.play(Write(label_1))
        self.wait()

        self.play(
            FadeOut(VGroup(lim, func_lab, func_graph,
                           arrow, arrow_lab, curve_arrow, curve_lab,
                           origin, label_o, empty, label_1,
                           *x_dots, *func_dots, self.axes)),
            FadeIn(VGroup(self.title, self.theorem))
        )


        self.play(Transform(self.title, self.title.copy().to_corner(UL)),
                  Transform(self.theorem, self.theorem.copy().to_corner(UL).shift(DOWN).align_to(self.title, LEFT)))

        first = TexMobject(r"\{x_n\} \subset f\text{的定义域}", color=BLUE).scale(0.8) \
            .move_to(self.theorem[1][-1].get_center()).shift(DOWN * 1.5)
        second = TexMobject(r"x_n\neq a", color=BLUE).scale(0.8) \
            .move_to(self.theorem[1][0].get_center()).shift(DOWN * 1.5).align_to(first, UP)
        arrow1 = Arrow(self.theorem[1][-1].get_bottom(), first.get_top(), color=BLUE)
        arrow2 = Arrow((self.theorem[1][0].get_bottom()[0], self.theorem[1][-1].get_bottom()[1], 0),
                       second.get_top(), color=BLUE)
        self.play(ShowCreation(arrow1))
        self.play(Write(first))
        self.play(ShowCreation(arrow2))
        self.play(Write(second))
        self.wait()
        self.play(FadeOut(VGroup(first, second, arrow1, arrow2)))

    def proof1(self):
        right = TexMobject(r"(\Rightarrow)", color=RED).next_to(self.theorem, DOWN).align_to(self.theorem, LEFT)
        self.play(Write(right))
        self.wait()
        l1 = TexMobject(r"\text{已知}", r"\lim\limits_{x\to a}f(x)=L.").next_to(right, RIGHT)
        #                     0          1                2           3       4            5        6               7
        l1_1 = TexMobject(r"\forall", r"\varepsilon", r">0, \exists", r"\delta", r">0,", r"0<|x-a|<", r"\delta",
                          r"\Rightarrow |f(x)-L|<", r"\varepsilon", ".") \
            .set_color_by_tex_to_color_map({"\\delta": GREEN, r"\varepsilon": BLUE}).next_to(l1[0], RIGHT)
        self.play(Write(l1))
        self.wait()
        self.play(Transform(l1[1], l1_1))
        self.wait()

        box = SurroundingRectangle(self.theorem[1][0], buff=.1).set_color(YELLOW)
        self.play(ShowCreation(box))
        self.wait()
        #                       0                   1     2            3           4       5          6                7                   8         9
        l2 = TexMobject(r"\exists N\in \mathbb{N}", ",", r"n\geq N", r"\Rightarrow", "0<", "|x_n-a|<", r"\delta",
                        r"\Rightarrow |f(x_n)-L|<", r"\varepsilon", ".") \
            .set_color_by_tex_to_color_map({"\\delta": GREEN, r"\varepsilon": BLUE}).next_to(l1_1, DOWN)
        l2[4:7].align_to(l1_1[5:7], RIGHT)
        l2[:4].next_to(l2[4], LEFT)
        l2[7:].align_to(l1_1[7:], LEFT)
        self.play(Write(l2[5]))
        self.wait()
        self.play(Write(l2[6]))
        self.wait()
        self.play(Write(l2[:4]))
        self.wait()
        self.play(Write(l2[4]))
        self.wait()
        self.play(Write(l2[7:]))
        self.wait()

        self.play(FadeOut(VGroup(box, right, l1, l1_1, l2)))

    def proof2(self):
        left = TexMobject(r"(\Leftarrow)", color=RED).next_to(self.theorem, DOWN).align_to(self.theorem, LEFT)
        self.play(Write(left))
        self.wait()

        # neg
        fan = TextMobject("反证。", "否定", r"$\lim\limits_{x\to a}f(x)=L$", ":").next_to(left, RIGHT)
        jia = TextMobject("假设").move_to(fan[1])
        self.play(Write(fan))
        self.wait()
        l1_1 = TexMobject(r"\forall", r"\varepsilon", r">0, ", r"\exists", r"\delta", r">0,",r"\forall","x",":", r"0<|",
                          "x","-a|<", r"\delta", r"\Rightarrow",r" |f(","x",")-L|", "<", r"\varepsilon:") \
            .set_color_by_tex_to_color_map({"\\delta": GREEN, r"\varepsilon": BLUE}).shift(UP * fan.get_y() - UP)
        self.play(ReplacementTransform(fan[2:], l1_1))
        self.wait()
        #                   0            1             2           3           4        5       6        7   8      9
        l2 = TexMobject(r"\exists", r"\varepsilon_0", r">0, ", r"\forall", r"\delta", r">0,",r"\exists","x",":", r"0<|",
                        #10  11       12             13         14   15   16      17           18
                        "x","-a|<", r"\delta", r"\Rightarrow",r" |f(","x",")-L|", "\geq", r"\varepsilon_0") \
            .set_color_by_tex_to_color_map({"\\delta": GREEN, r"\varepsilon_0": BLUE}).next_to(l1_1, DOWN)
        self.play(ReplacementTransform(l1_1.copy()[:3], l2[:3]))
        self.play(ReplacementTransform(l1_1.copy()[3:6], l2[3:6]))
        self.play(ReplacementTransform(l1_1.copy()[6:9], l2[6:9]))
        self.play(ReplacementTransform(l1_1.copy()[9:14], l2[9:14]))
        self.play(ReplacementTransform(l1_1.copy()[14:], l2[14:]))

        # proof
        self.play(Transform(fan[1], jia), FadeOut(l1_1))
        self.play(l2.shift, UP)

        # explain
        c1 = Brace(l2[9:13], DOWN, buff=SMALL_BUFF)
        c2 = Brace(l2[6:13], DOWN, buff=SMALL_BUFF)
        c3 = Brace(l2[14:], DOWN, buff=SMALL_BUFF)
        t1 = TextMobject("不论与$a$多近", color=YELLOW).scale(.8).next_to(c1, DOWN)
        t2 = TextMobject("总存在$x$", color=YELLOW).scale(.8)
        t3 = TextMobject("使$f(x)$与$L$有正距离", color=YELLOW).scale(.8).next_to(c3, DOWN)

        self.play(GrowFromCenter(c1))
        self.play(Write(t1))
        self.play(ReplacementTransform(c1, c2))
        self.play(Transform(t1, t1.copy().next_to(c2, DOWN)))
        t2.next_to(t1, DOWN)
        self.play(Write(t2))
        self.wait()
        self.play(GrowFromCenter(c3))
        self.play(Write(t3))
        self.wait()

        self.play(FadeOut(VGroup(c2, c3, t1, t2, t3)))

        # continue
        l3 = TexMobject("1",",","\\frac 12",",","\\frac 13",",","\\cdots", color=GREEN).scale(.8).next_to(l2[4], DOWN*1.5)
        self.play(Write(l3))
        #                   0            1             2           3           4        5       6        7   8      9
        l41 = TexMobject(r"\exists", r"\varepsilon_0", r">0, ", r"\forall", r"\delta", r">0,", r"\exists", "x_1", ":",
                        r"0<|",
                        # 10  11       12             13         14   15   16      17           18
                        "x_1", "-a|<", r"1", r"\Rightarrow", r" |f(", "x_1", ")-L|", "\geq", r"\varepsilon_0") \
            .set_color_by_tex_to_color_map({"\\delta": GREEN,r"\varepsilon_0": BLUE}).move_to(l2)
        l41[12].set_color(GREEN)
        #                   0            1             2           3           4        5       6        7   8      9
        l42 = TexMobject(r"\exists", r"\varepsilon_0", r">0, ", r"\forall", r"\delta", r">0,", r"\exists", "x_2", ":",
                        r"0<|",
                        # 10  11       12             13         14   15   16      17           18
                        "x_2", "-a|<", r"\frac 12", r"\Rightarrow", r" |f(", "x_2", ")-L|", "\geq", r"\varepsilon_0") \
            .set_color_by_tex_to_color_map({"\\delta": GREEN,r"\varepsilon_0": BLUE}).move_to(l2)
        l42[12].set_color(GREEN)
        #                   0            1             2           3           4        5       6        7   8      9
        l43 = TexMobject(r"\exists", r"\varepsilon_0", r">0, ", r"\forall", r"\delta", r">0,", r"\exists", "x_3", ":",
                        r"0<|",
                        # 10  11       12             13         14   15   16      17           18
                        "x_3", "-a|<", r"\frac 13", r"\Rightarrow", r" |f(", "x_3", ")-L|", "\geq", r"\varepsilon_0") \
            .set_color_by_tex_to_color_map({"\\delta": GREEN,r"\varepsilon_0": BLUE}).move_to(l2)
        l43[12].set_color(GREEN)
        #                   0            1             2           3           4        5       6           7      8
        l44 = TexMobject(r"\exists", r"\varepsilon_0", r">0, ", r"\forall", r"\delta", r">0,", r"\exists", "x_n", ":",
                        # 9
                        r"0<|",
                        # 10       11       12             13         14         15   16      17           18
                        "x_n", "-a|<", r"\frac 1n", r"\Rightarrow", r" |f(", "x_n", ")-L|", "\geq", r"\varepsilon_0") \
            .set_color_by_tex_to_color_map({"\\delta": GREEN,r"\varepsilon_0": BLUE}).move_to(l2)
        l44[12].set_color(GREEN)
        self.play(ReplacementTransform(l2, l41))
        self.wait()
        self.play(ReplacementTransform(l41, l42))
        self.wait()
        self.play(ReplacementTransform(l42, l43))
        self.wait()
        self.play(ReplacementTransform(l43, l44))
        self.wait()

        b = Brace(l44[9:13], DOWN, buff=SMALL_BUFF)
        t4 = TexMobject(r"x_n\to a").next_to(b, DOWN)
        box = SurroundingRectangle(self.theorem[1][-1], buff=SMALL_BUFF, color=YELLOW)
        self.play(GrowFromCenter(b))
        self.play(Write(t4))
        self.play(ShowCreation(box))

        l5 = TexMobject(r"\Rightarrow",r" |f(", "x_n", ")-L|", "<", r"{\varepsilon_0 \over 2}")\
            .move_to(t4)
        l5[-1].set_color(BLUE)
        l5[0].align_to(l44[13], LEFT)
        l5[1:4].align_to(l44[14:17], LEFT)
        l5[4].align_to(l44[17], LEFT)
        l5[5].align_to(l44[-1], LEFT)
        self.play(Write(l5[:-1]))
        self.wait()
        self.play(Write(l5[-1]))

        l6 = TextMobject(r"当$n\gg 1$.").next_to(l5, DOWN)
        self.play(Write(l6))

        box2 = SurroundingRectangle(VGroup(l44[14:], l5[1:]), color=YELLOW, buff=SMALL_BUFF)
        self.play(ReplacementTransform(box, box2))
        self.wait()

