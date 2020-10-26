from manimlib.imports import *


class Bound(MovingCameraScene):
    def construct(self):
        # opening
        title = TextMobject("\\underline{\\heiti 有界性定理}", color=YELLOW).to_corner(UL)
        theorem = TextMobject("连续函数在有限闭区间上有界.", color=YELLOW) \
            .next_to(title, DOWN).set_x(0)
        self.play(Write(title))
        self.play(Write(theorem), run_time=2)
        self.wait(2)

        # proof
        zheng = TextMobject("【证】~ 反证法.").next_to(theorem, DOWN, buff=MED_LARGE_BUFF).align_to(title, LEFT)
        # l1 = TextMobject("反证法。",).next_to(zheng, RIGHT)
        l1 = TextMobject("设$f(x)$在$[a,b]$上连续，我们否定$f(x)${\\heiti 有界}.", "即，否定").next_to(zheng, DOWN, aligned_edge=LEFT)
        #                       0          1      2      3      4         5       6      7      8       9        10
        bounded = TexMobject(r"\exists ", r"M", r"\geq", r"0", ",", r"\forall", r" x", r":", r"a\leq ", r"x", r"\leq b",
                             #     11           12     13     14    15        16
                             r"\Rightarrow", r" |f(", r"x", r")|", r"\leq", r" M") \
            .set_color_by_tex_to_color_map({'M': RED}).next_to(l1, DOWN)
        tmp = TextMobject("得到了：").next_to(bounded, DOWN).align_to(zheng, LEFT)
        negation = TexMobject(r"\forall ", r"M", r"\geq", r"0", ",", r"\exists", r" x", r":", r"a\leq ", r"x",
                              r"\leq b",
                              r"\text{ 且 }~", r" |f(", r"x", r")|", r">", r" M") \
            .set_color_by_tex_to_color_map({'M': RED}).next_to(tmp, DOWN).align_to(bounded, LEFT)

        self.play(Write(zheng))
        self.wait()
        self.play(Write(l1))
        self.wait()
        self.play(Write(bounded))
        self.wait()
        self.play(Write(tmp))
        self.play(ReplacementTransform(bounded.copy()[:5], negation[:5]))
        # self.wait()
        self.play(ReplacementTransform(bounded.copy()[5:8], negation[5:8]))
        # self.wait()
        self.play(ReplacementTransform(bounded.copy()[8:12], negation[8:12]))
        # self.wait()
        self.play(ReplacementTransform(bounded.copy()[12:], negation[12:]))
        self.wait()

        # scrolling down
        self.camera.frame.save_state()
        self.play(self.camera.frame.move_to, DOWN * (title.get_top()[1] - tmp.get_y()), run_time=2)
        l2 = TextMobject("既然", "$M$", "是任意的，我们让它越来越大直到无穷.").set_color_by_tex_to_color_map({"M": RED}) \
            .next_to(negation, DOWN).align_to(tmp, LEFT)
        l3 = TextMobject("不妨令", "$M$", "$=1,2,3,\\cdots$").set_color_by_tex_to_color_map({"M": RED}) \
            .next_to(l2, DOWN).align_to(zheng, LEFT)
        l4 = TextMobject("对于每个给定的", "$M$", ",总有一个对应的", "$x$", ".").set_color_by_tex_to_color_map({"M": RED, "x": BLUE}) \
            .next_to(l3, DOWN, aligned_edge=LEFT)
        negation0 = negation.copy().next_to(l4, DOWN).set_x(0)
        negation1 = TexMobject(r"M", "=", "1", ",", r"\exists", r" x_1", r":", r"a\leq ", r"x_1", r"\leq b",
                               r"\text{ 且 }~", r" |f(", r"x_1", r")|", r">", r" 1") \
            .set_color_by_tex_to_color_map({'1': BLUE}).next_to(l4, DOWN).set_x(0)
        negation2 = TexMobject(r"M", "=", "2", ",", r"\exists", r" x_2", r":", r"a\leq ", r"x_2", r"\leq b",
                               r"\text{ 且 }~", r" |f(", r"x_2", r")|", r">", r" 2") \
            .set_color_by_tex_to_color_map({'2': BLUE}).next_to(l4, DOWN).set_x(0)
        negation3 = TexMobject(r"M", "=", "3", ",", r"\exists", r" x_3", r":", r"a\leq ", r"x_3", r"\leq b",
                               r"\text{ 且 }~", r" |f(", r"x_3", r")|", r">", r" 3") \
            .set_color_by_tex_to_color_map({'3': BLUE}).next_to(l4, DOWN).set_x(0)
        negationn = TexMobject(r"M", "=", "n", ",", r"\exists", r" x_n", r":", r"a\leq ", r"x_n", r"\leq b",
                               r"\text{ 且 }~", r" |f(", r"x_n", r")|", r">", r" n") \
            .set_color_by_tex_to_color_map({'n': BLUE}).next_to(l4, DOWN).set_x(0)
        for neg in [negation1, negation2, negation3, negationn]:
            neg[2].set_color(RED)
            neg[-1].set_color(RED)

        line = Underline(negationn[-5:], color=YELLOW)

        self.play(Write(l2))
        self.wait()
        self.play(Write(l3))
        self.wait()
        self.play(Write(l4))
        self.play(ReplacementTransform(negation.copy(), negation0))
        self.wait(.5)
        self.play(ReplacementTransform(negation0, negation1))
        self.wait(.5)
        self.play(ReplacementTransform(negation1, negation2))
        self.wait(.5)
        self.play(ReplacementTransform(negation2, negation3))
        self.wait(.5)
        self.play(ReplacementTransform(negation3, negationn))
        self.wait()

        l5 = TextMobject("由此得到了一个特殊的数列", r"$\{x_n\}$.").next_to(negationn, DOWN).align_to(l4, LEFT)
        label = TextMobject("$x_n$的性质", color=YELLOW).scale(.8).next_to(line, DOWN)
        l6 = TextMobject(r"如果它收敛于$x^*$，那我们一取极限就有矛盾$f(x^*)=\infty$~!").next_to(l5, DOWN, aligned_edge=LEFT)
        l7 = TextMobject(r"遗憾的是$\{x_n\}$并不一定收敛...").next_to(l6, DOWN, aligned_edge=LEFT)
        l8 = TextMobject(r"但是别怕！它有收敛子列$\{x_{n_k}\}$!").next_to(l7, DOWN, aligned_edge=LEFT)
        l9 = TextMobject(r"依据是", "Bolzano-Weierstrass定理", "（见往期视频）...").next_to(l8, DOWN, aligned_edge=LEFT)
        l9[1].set_color(YELLOW)

        self.play(Write(l5))
        self.wait()
        self.play(ShowCreation(line))
        self.play(Write(label))
        self.wait()
        self.play(Write(l6), run_time=3)
        self.wait(2)
        self.play(Write(l7))
        self.wait()

        # scrolling down, again
        self.play(self.camera.frame.shift, DOWN * (tmp.get_top()[1] - l7.get_top()[1]), run_time=3)
        self.wait()
        self.play(Write(l8))
        self.wait()
        self.play(Write(l9))
        self.wait()

        l10 = TextMobject("这样就有").next_to(l9, DOWN, aligned_edge=LEFT)
        series = TexMobject("x_{n_k}", r"\xrightarrow{k\to\infty}", "x^*").next_to(l10, DOWN).set_x(0)
        series[1].set_color(BLUE)

        l11 = TextMobject("由于$f(x)$连续：").next_to(series, DOWN).align_to(l10, LEFT)
        continuous = TexMobject(r"\lim_", r"{k\to\infty}", r"f", r"(", r"x_{n_k}", r")", r"=",
                                r"\lim\limits_{k\to\infty}", r"f", r"(", r"x_{n_k}", r")",
                                r"=f(x^*)").next_to(l11, DOWN).set_x(0)
        continuous[1].set_color(BLUE)
        t = TexMobject(r"f", r"(", r"\lim\limits_{k\to\infty}", r"x_{n_k}", r")").move_to(continuous[7:12])
        self.play(Write(l10))
        self.play(Write(series))
        self.wait()

        self.play(Write(l11))
        self.wait()
        self.play(Write(continuous[:12]))
        self.play(Transform(continuous[7:12], t))
        self.wait()
        self.play(Write(continuous[-1]))
        self.wait()

        # scrolling down, once again
        self.play(self.camera.frame.shift, DOWN * (l7.get_top()[1] - l11.get_top()[1]), run_time=2)
        self.wait()

        l12 = TextMobject("同时，当", r"$k\to\infty$", '时有', r"$n_k\to\infty$.")\
            .next_to(continuous, DOWN).align_to(l11, LEFT)
        l12[1].set_color(BLUE)
        l12[-1].set_color(RED)
        l13 = TextMobject(r"（这是因为$\{x_{n_k}\}$是跳着选的子列，有$n_k\geq k$.）").next_to(l12, DOWN, aligned_edge=LEFT)
        l14 = TextMobject(r"又根据",r"$|f(x_{n_k})|>n_k$",r"（这是$\{x_n\}$的性质），").next_to(l13, DOWN, aligned_edge=LEFT)
        l14[1].set_color(RED)
        l15 = TextMobject(r"可知", r"$\{f(x_{n_k})\}_k$发散", r".").next_to(l14, DOWN, aligned_edge=LEFT)

        self.play(Write(l12), run_time=2)
        self.wait()
        self.play(Write(l13), run_time=2)
        self.wait()
        self.play(Write(l14), run_time=2)
        self.wait()
        self.play(Write(l15))
        self.wait()
        box1 = SurroundingRectangle(continuous, color=YELLOW, buff=.1)
        box2 = SurroundingRectangle(l15[1], color=YELLOW, buff=.1)
        self.play(ShowCreation(box1), ShowCreation(box2))
        self.wait(2)
        end = TextMobject("得到了一个矛盾.",r"故假设不成立，$f(x)$有界.").next_to(l15, DOWN, aligned_edge=LEFT)
        qed = TexMobject("\\blacksquare").next_to(end, DOWN).to_edge(RIGHT)
        self.play(Write(end[0]))
        self.wait()
        self.play(Write(end[1:]))
        self.play(Write(qed))
        self.wait()
        self.play(Restore(self.camera.frame), run_time=5)
        self.wait()
