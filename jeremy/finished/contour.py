from manimlib.imports import *


class contour(GraphScene):
    CONFIG = {
        "color_map": {"varepsilon_0": RED, "s_n": TEAL, "s_{k_n}": TEAL, "t_n": BLUE, "t_{k_n}": BLUE}
    }

    def construct(self):
        self.opening()
        self.graphing()
        self.negdef()
        self.suppose()
        self.proof()

    def opening(self):
        title = self.title = TextMobject("\\textbf{\\underline{\\heiti Contour定理}}", color=YELLOW).to_corner(UL)
        theorem = self.theorem = TextMobject("$f$在$[a,b]$上", r"{连续}~", "$\\implies ~f$在$[a,b]$上", r"{一致连续}", ".") \
            .next_to(title, DOWN).set_x(0).set_color_by_tex("连续", BLUE)
        self.play(Write(title))
        self.play(Write(theorem))

    def graphing(self):
        self.x_axis_label, self.y_axis_label = None, None
        self.x_axis_width, self.y_axis_height = 4, 4
        self.x_max, self.y_max = .1, 100
        self.x_min, self.y_min = 0, 0
        self.graph_origin = 3 * DOWN + 5 * LEFT
        self.y_tick_frequency = 100
        self.x_tick_frequency = .1

        # original graph
        self.setup_axes(animate=True)
        graph_fracx = self.get_graph(lambda x: 1 / x, x_max=.1, x_min=0.01, color=BLUE)
        self.play(ShowCreation(graph_fracx))
        self.play(graph_fracx.fade, 0.6)

        # part of it
        tracker = ValueTracker(0.011)
        delta = 0.05
        graph_part = self.get_graph(lambda x: 1 / x, x_min=tracker.get_value(), x_max=tracker.get_value() + delta,
                                    color=YELLOW)

        def part_updater(part):
            new_part = self.get_graph(lambda x: 1 / x, x_min=tracker.get_value(), x_max=tracker.get_value() + delta,
                                      color=YELLOW)
            part.become(new_part)

        graph_part.add_updater(part_updater)
        lline = (self.get_vertical_line_to_graph(tracker.get_value(), graph_fracx))

        def lline_updater(line):
            new_line = (self.get_vertical_line_to_graph(tracker.get_value(), graph_fracx))
            line.become(new_line)

        lline.add_updater(lline_updater)
        rline = (self.get_vertical_line_to_graph(tracker.get_value() + delta, graph_fracx))

        def rline_updater(line):
            new_line = (self.get_vertical_line_to_graph(tracker.get_value() + delta, graph_fracx))
            line.become(new_line)

        rline.add_updater(rline_updater)
        a = TexMobject("a")
        b = TexMobject("b")

        def a_updater(a):
            a.next_to(lline, DOWN)

        def b_updater(b):
            b.next_to(rline, DOWN).align_to(a, DOWN)

        a.add_updater(a_updater)
        b.add_updater(b_updater)
        self.play(ShowCreation(lline), ShowCreation(rline), Write(a), Write(b))
        self.play(ShowCreation(graph_part))
        # self.play(Write(a), Write(b))
        self.play(tracker.set_value, 0.045, run_time=3, rate_func=there_and_back)
        self.wait()
        lline.clear_updaters()
        rline.clear_updaters()
        graph_part.clear_updaters()

        self.play(FadeOut(VGroup(a, b, lline, rline, graph_part, graph_fracx, self.axes)))

    def negdef(self):
        # ============================ negation part ===============================
        zheng = self.zheng = TextMobject("【证】").next_to(self.theorem, DOWN, buff=MED_LARGE_BUFF).align_to(self.title,
                                                                                                          LEFT)
        l1 = self.l1 = TextMobject("反证.", "假设", "$f(x)$", "在", "$[a,b]$", "上不一致连续.", "即", "否定")
        def1 = TexMobject(r"\forall ", r"\varepsilon", r">0,", r" \exists", r"\delta", r">0,",
                          r"\forall x_1,x_2\in I, ") \
            .set_color_by_tex_to_color_map({"varepsilon": RED, "delta": GREEN})
        def2 = TexMobject(r"|x_1-x_2|<", r"\delta", r"\Longrightarrow", "|f(x_1)-f(x_2)|<", r"\varepsilon", r".") \
            .set_color_by_tex_to_color_map({"varepsilon": RED, "delta": GREEN})
        dedao = TextMobject("得到：")
        neg1 = TexMobject(r"\exists ", r"\varepsilon_0", r">0,", r" \forall", r"\delta", r">0,",
                          r"\exists x_1,x_2\in I, ") \
            .set_color_by_tex_to_color_map({"varepsilon_0": RED, "delta": GREEN})
        neg2 = TexMobject(r"|x_1-x_2|<", r"\delta", r"\text{且}", r"|f(x_1)-f(x_2)|\geq", r"\varepsilon_0", r".") \
            .set_color_by_tex_to_color_map({"varepsilon_0": RED, "delta": GREEN})

        l1.next_to(zheng)
        VGroup(def1, def2, dedao, neg1, neg2).arrange(DOWN).set_x(0).next_to(l1, DOWN)
        dedao.align_to(l1, LEFT)
        neg2[:2].align_to(def2[:2], LEFT)
        neg2[2].align_to(def2[2], ORIGIN).shift(RIGHT * SMALL_BUFF)
        neg2[3:].align_to(def2[3:], LEFT)

        self.play(Write(zheng))
        self.wait()
        self.play(Write(l1[0]))
        self.wait()
        self.play(Write(l1[1:]))
        self.play(Write(def1))
        self.play(Write(def2))
        self.wait()
        self.play(Write(dedao))
        # negative
        self.play(ReplacementTransform(def1[:3].copy(), neg1[:3]))
        self.play(ReplacementTransform(def1[3:6].copy(), neg1[3:6]))
        self.play(ReplacementTransform(def1[6:].copy(), neg1[6:]))
        self.play(ReplacementTransform(def2[:2].copy(), neg2[:2]))
        self.play(ReplacementTransform(def2[2].copy(), neg2[2]))
        self.play(ReplacementTransform(def2[3:].copy(), neg2[3:]))
        self.wait()

        self.play(FadeOut(VGroup(def1, def2, l1[-1], dedao)))
        self.play(VGroup(neg1, neg2).next_to, l1, DOWN)
        # ============================ neg def part ===============================
        self.wait()
        self.play(Succession(Indicate(neg1[3:6]), Indicate(neg1[3:6])))
        l2_group = [
            TexMobject(r"\text{取}", r"\delta", "=", frac, ",").set_color_by_tex("delta", GREEN)
            for frac in [r"{1}", r"\frac 12", r"\frac 13", r"\frac 1n"]
        ]

        ndef1_group = [TexMobject(r"\exists ", r"\varepsilon_0", r">0,", r"\delta", "=", j, ","
                                                                                            fr"\exists s_{i},t_{i}\in I, ") \
            .set_color_by_tex_to_color_map(
            {"varepsilon_0": RED, "delta": GREEN}) for i, j in
            zip([1, 2, 3, "n"], [r"{1}", r"\frac 12", r"\frac 13", r"\frac 1n"])]
        ndef2_group = [
            TexMobject("|", f"s_{i}", "-", f"t_{i}", "|<", j,
                       r"\text{ 且 }", "|f(", f"s_{i}", ")-f(", f"t_{i}", r")|\geq", r"\varepsilon_0", r".") \
                .set_color_by_tex_to_color_map({"varepsilon_0": RED, "delta": GREEN})
            for i, j in zip([1, 2, 3, "n"], [r"{1}", r"\frac 12", r"\frac 13", r"\frac 1n"])]
        for l2, ndef1, ndef2 in zip(l2_group, ndef1_group, ndef2_group):
            l2.next_to(neg2, DOWN, buff=MED_LARGE_BUFF).align_to(l1, LEFT)
            ndef1.next_to(neg2, DOWN, buff=MED_LARGE_BUFF).align_to(neg1, LEFT)
            # ndef1[3:-1].align_to(neg1[3:-1], LEFT)
            # ndef1[-1].align_to(neg1[-1], LEFT)
            ndef2.next_to(ndef1, DOWN).align_to(neg2, LEFT)
            ndef2[-7:].align_to(neg2[-3:], LEFT)
            ndef2[-8].align_to(neg2[-4], LEFT)
        self.play(VGroup(neg1, neg2).fade, 0.5)
        self.play(Write(l2_group[0]))
        self.play(Write(ndef1_group[0]))
        self.play(Write(ndef2_group[0]))
        for l2, ndef1, ndef2 in zip(l2_group[1:], ndef1_group[1:], ndef2_group[1:]):
            self.play(Transform(l2_group[0], l2),
                      Transform(ndef1_group[0], ndef1),
                      Transform(ndef2_group[0], ndef2))
            self.wait(.5)

        negdef1 = self.ndef1 = TexMobject(r"\exists ", r"\varepsilon_0", r">0", ",", r"\forall", r"n\in\mathbb{N}^*",
                                          ",",
                                          r"\exists", "s_n", ",", "t_n", r"\in I, ") \
            .set_color_by_tex_to_color_map(self.color_map)
        negdef2 = self.ndef2 = TexMobject(r"|", "s_n", "-", "t_n", r"|", "<", r"\frac 1n", r"\text{ 且 }~",
                                          r"|", "f(", "s_n", ")", "-", "f(", "t_n", r")|", r"\geq", r"\varepsilon_0",
                                          r".") \
            .set_color_by_tex_to_color_map(self.color_map)
        VGroup(negdef1, negdef2).arrange(DOWN).next_to(l1, DOWN)

        self.wait(2)
        self.play(FadeOut(VGroup(neg1, neg2)),
                  ReplacementTransform(VGroup(l2_group[0], ndef1_group[0]), negdef1),
                  ReplacementTransform(ndef2_group[0], negdef2), run_time=2)
        box = SurroundingRectangle(VGroup(negdef1, negdef2), color=YELLOW)
        self.play(ShowCreation(box))
        text = TextMobject(r"{\kaishu 非一致连续的精确表述}", color=YELLOW).next_to(negdef2, DOWN)
        self.wait()
        self.play(Write(text))
        self.wait()
        self.play(FadeOut(VGroup(box, text)))

        brace1, brace2 = Brace(negdef2[:7], DOWN, color=YELLOW), Brace(negdef2[8:-1], DOWN, color=YELLOW)
        brace2.align_to(brace1, UP)
        text1, text2 = TextMobject("$s_n,t_n${\\kaishu 越来越近}", color=YELLOW).scale(.8).next_to(brace1, DOWN), \
                       TextMobject("{\\kaishu 但}$f(x_n),f(t_n)$ {\\kaishu 总有正距离}", color=YELLOW).scale(.8).next_to(
                           brace2, DOWN)
        self.play(GrowFromCenter(brace1), Write(text1))
        self.wait()
        self.play(GrowFromCenter(brace2), Write(text2))
        self.wait()

        self.play(FadeOut(VGroup(brace1, brace2, text1, text2)))

    def suppose(self):
        l1 = self.l1
        ndef1, ndef2 = self.ndef1, self.ndef2
        s1 = TexMobject(r"\text{如果}~ ", r"\lbrace", "s_n", r"\rbrace,", r"\lbrace", "t_n", r"\rbrace", r"\text{收敛},",
                        r"\text{那么}~", r"s_n", r"\to s, ", r"t_n", r"\to s.") \
            .set_color_by_tex_to_color_map(self.color_map).next_to(ndef2, DOWN).align_to(l1, LEFT)
        s1_2 = self.p1 = TexMobject(r"\text{实际上}~ ", r"\lbrace", "s_{k_n}", r"\rbrace,", r"\lbrace", "t_{k_n}",
                                    r"\rbrace", r"\text{收敛},",
                                    r"\text{那么}~", r"s_{k_n}", r"\to s, ", r"t_{k_n}", r"\to s.") \
            .set_color_by_tex_to_color_map(self.color_map).next_to(ndef2, DOWN).align_to(l1, LEFT)

        s2 = TexMobject(r"\lim_{n\to\infty}", r"|", "f", r"(", "s_n", ")", "-", "f", r"(", "t_n", r")", r"|", r"\geq",
                        r"\varepsilon_0", r".")
        s2_2 = TexMobject(r"|", r"\lim_{n\to\infty}", "f", r"(", "s_n", ")", "-", r"\lim_{n\to\infty}", "f", r"(",
                          "t_n", r")", r"|", r"\geq",
                          r"\varepsilon_0", r".")
        s2_3 = TexMobject(r"|", "f", r"(", "s", ")", "-", "f", r"(", "s", r")", r"|", r"\geq",
                          r"\varepsilon_0", r".")
        s2_4 = TexMobject("0", r"\geq", r"\varepsilon_0", r".")
        zero = TexMobject("0")
        for s in [s2, s2_2, s2_3, s2_4]:
            s.set_color_by_tex_to_color_map(self.color_map)
            s.next_to(s1, DOWN).set_x(0)
        zero.move_to(s2_4[0])

        box1 = SurroundingRectangle(ndef2[8:-1], color=YELLOW)
        box1_2 = SurroundingRectangle(ndef1[:3], color=YELLOW)
        box2 = SurroundingRectangle(s2_4[:-1], color=YELLOW)
        line = Underline(s1[1:8], color=YELLOW)
        self.play(Write(s1[:8]), run_time=2)
        self.play(ShowPassingFlashAround(ndef2[:7]))
        self.play(Write(s1[8:]), run_time=2)
        self.wait()
        self.play(ShowCreation(box1))
        self.wait()
        self.play(ReplacementTransform(ndef2[8:-1].copy(), s2))
        self.wait()
        for s in [s2_2, s2_3]:
            self.play(Transform(s2, s))
            self.wait()
        self.play(Transform(s2[:-3], zero), Transform(s2[-3:], s2_4[1:]))
        self.wait()
        self.play(ReplacementTransform(box1, box1_2), ShowCreation(box2))
        self.wait()
        self.play(FadeOut(VGroup(box1_2, box2)), ShowCreation(line))
        self.wait()
        self.play(FadeOut(line))
        self.wait()
        self.play(ReplacementTransform(s1, s1_2))
        self.wait()
        self.play(FadeOut(VGroup(self.title, self.theorem, self.zheng, self.l1[:-1], self.ndef1, self.ndef2, zero, s2)))
        self.play(s1_2.to_edge, UP, run_time=2)

    def proof(self):
        p = self.p1
        # p = TexMobject(r"\text{实际上}~ ", r"\lbrace", "s_{k_n}", r"\rbrace,", r"\lbrace", "t_{k_n}",
        #                r"\rbrace", r"\text{收敛},",
        #                r"\text{那么}~", r"s_{k_n}", r"\to s, ", r"t_{k_n}", r"\to s.") \
        #     .set_color_by_tex_to_color_map(self.color_map).to_edge(UP)
        # self.add(p)
        n = 15
        indices = [2, 4, 5, 7, 11, 12, 14]

        # ============= s part ===============================
        s_dots = VGroup(*[Dot() for _ in range(n)]) \
            .arrange(RIGHT, buff=MED_LARGE_BUFF * 1.5).next_to(p, DOWN, buff=LARGE_BUFF).set_x(0)
        s_labels = VGroup(*[TexMobject(f"s", f"_{{{i + 1}}}").next_to(s_dots[i], UP) for i in range(n)])
        s_sublabels = VGroup(
            *[TexMobject(f"s", f"_{{k_{i}}}", color=self.color_map["s_n"]).next_to(s_dots[indices[i - 1] - 1], DOWN) for
              i in range(1, len(indices) + 1)])
        tos = TexMobject(r"\to", "s").next_to(s_sublabels[-1], RIGHT)
        self.play(LaggedStartMap(GrowFromCenter, s_dots))
        self.play(FadeIn(s_labels))
        self.wait()
        for ind, sub_ind in enumerate(indices):
            self.play(FadeIn(s_sublabels[ind]), s_dots[sub_ind - 1].set_color, self.color_map["s_n"])
        self.play(Write(tos))

        box10, box20 = SurroundingRectangle(s_labels[0][-1], color=YELLOW, buff=0.07), SurroundingRectangle(
            s_sublabels[0][-1], color=YELLOW, buff=0.07)
        self.play(ShowCreation(box10), ShowCreation(box20))
        for i, s_sublabel in enumerate(s_sublabels):
            s_label = s_labels[i]
            box1, box2 = SurroundingRectangle(s_label[-1], color=YELLOW, buff=0.07), SurroundingRectangle(
                s_sublabel[-1], color=YELLOW, buff=0.07)
            self.play(Transform(box10, box1), Transform(box20, box2))

        ineq = TexMobject("k_n", "\\geq", "n").next_to(s_sublabels, DOWN, buff=MED_LARGE_BUFF).set_x(0)
        box_ineq = SurroundingRectangle(ineq, color=YELLOW)
        self.wait()
        self.play(Write(ineq))
        self.play(ReplacementTransform(VGroup(box10, box20).copy(), box_ineq))

        # ============= t part ===============================
        t_dots = VGroup(*[Dot() for _ in range(n)]) \
            .arrange(RIGHT, buff=MED_LARGE_BUFF * 1.5).next_to(ineq, DOWN, buff=LARGE_BUFF).set_x(0)
        t_labels = VGroup(*[TexMobject(f"t", f"_{{{i + 1}}}").next_to(t_dots[i], UP) for i in range(n)])
        t_sublabels = VGroup(
            *[TexMobject(f"t", f"_{{k_{i}}}", color=self.color_map["t_n"]).next_to(t_dots[indices[i - 1] - 1], DOWN) for
              i in
              range(1, len(indices) + 1)])
        self.play(LaggedStartMap(GrowFromCenter, t_dots))
        self.play(FadeIn(t_labels))
        self.wait()
        for ind, sub_ind in enumerate(indices):
            self.play(FadeIn(t_sublabels[ind]), t_dots[sub_ind - 1].set_color, self.color_map["t_n"])
        self.wait()
        # ================ proof ===============================
        box_lim = SurroundingRectangle(p[-2:])
        self.play(ReplacementTransform(VGroup(box10, box20), box_lim))
        self.wait()
        p1 = TexMobject(r"|", r"t_{k_n}", r"-", r"s", r"|", r"\leq",
                        r"|", r"t_{k_n}", r"-", r"s_{k_n}", r"|",
                        r"+", r"|", r"s_{k_n}", r"-", r"s", r"|").next_to(t_sublabels, DOWN)

        self.play(Write(p1[:5]))
        self.wait()
        self.play(Write(p1[5:]))
        xian = Line(t_sublabels[-1].get_center(), tos[-1].get_center(), color=WHITE)
        gou = Line(t_sublabels[-1].get_center(), s_sublabels[-1].get_center(), color=YELLOW)
        gu = Line(s_sublabels[-1].get_center(), tos[-1].get_center(), color=YELLOW)
        self.play(GrowArrow(xian))
        self.wait()
        self.play(GrowArrow(gou))
        self.play(GrowArrow(gu))

        p2 = TexMobject(r"<", r"{1 \over k_n}", r"+", r"|", r"s_{k_n}", r"-",
                        r"s", r"|").next_to(p1, DOWN).align_to(
            p1[5], LEFT)
        p3 = TexMobject(r"\leq",r" \frac 1n", r"+", r"|", r"s_{k_n}", r"-",
                        r"s", r"|").next_to(p2, RIGHT)
        to0 = TexMobject(r"\to","0").next_to(p3, RIGHT)
        conclusion = TexMobject(r"t_{k_n}\to s").next_to(t_sublabels, DOWN, buff=LARGE_BUFF)
        self.play(Write(p2[0]))
        self.wait()
        self.play(ReplacementTransform(p1[6:11].copy(), p2[1]))
        self.wait()
        self.play(ReplacementTransform(p1[11:].copy(), p2[2:]))
        self.play(Write(p3[0]))
        self.wait()
        self.play(Indicate(box_ineq))
        self.play(Indicate(box_ineq))
        self.play(ReplacementTransform(p2[1].copy(), p3[1]))
        self.wait()
        self.play(ReplacementTransform(p2[2:].copy(), p3[2:]))
        self.wait()
        self.play(Write(to0))
        self.wait()
        self.play(ReplacementTransform(VGroup(p1,p2,p3,to0), conclusion))


class Creature(PiCreatureScene):
    def construct(self):
        you = self.pi_creature
        line = NumberLine(
            x_min=-2,
            x_max=12,
            include_tip=True
        )
        line.to_edge(DOWN, buff=1.5)
        line.to_edge(LEFT, buff=-0.5)

        you.next_to(line.n2p(0), UP)

        you_label = TextMobject("you")
        you_label.next_to(you, RIGHT, MED_LARGE_BUFF)
        you_arrow = Arrow(you_label.get_left(), you.get_right() + 0.5 * LEFT, buff=0.1)

        now_label = TextMobject("Now")
        later_label = TextMobject("Later")
        now_label.next_to(line.n2p(0), DOWN)
        later_label.next_to(line.n2p(10), DOWN)

        self.add(line, now_label)
        self.add(you)
        self.play(
            FadeInFrom(you_label, LEFT),
            GrowArrow(you_arrow),
            # you.change, "pondering",
        )
        self.wait()
        you_label.add(you_arrow)
        self.play(
            # you.change, "horrified",
            you.look, DOWN,
            you.next_to, line.n2p(10), UP,
            MaintainPositionRelativeTo(you_label, you),
            FadeInFromPoint(later_label, now_label.get_center()),
        )
        self.wait()

        # Add bubble
        bubble = you.get_bubble(
            height=4,
            width=6,
        )
        bubble.set_fill(opacity=0)
        formula = TextMobject("what a beautiful formula")
        bubble.position_mobject_inside(formula)

        self.play(
            # you.change, "confused", bubble,
            ShowCreation(bubble),
        )
        self.play(FadeIn(formula))

        self.wait(2)


class test(GraphScene):
    def construct(self):
        self.setup_axes()
        x = [0, 1, 2, 3, 4, 5, 6, 7]
        y = [0, 1, 4, 9, 8, 3, 2, 10]

        coords = [[px, py] for px, py in zip(x, y)]
        # |
        # V
        points = self.get_points_from_coords(coords)

        graph = SmoothGraphFromSetPoints(points, color=GREEN)
        dots = self.get_dots_from_coords(coords)

        self.add(dots)
        self.play(ShowCreation(graph), rate_func=lambda t: smooth(1.5 * t))
