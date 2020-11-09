from manimlib.imports import *

class contour(GraphScene):
    def construct(self):
        self.opening()
        self.graphing()
        self.proof()

    def opening(self):
        title = self.title = TextMobject("\\underline{\\heiti Contour定理}", color=YELLOW).to_corner(UL)
        theorem = self.theorem = TextMobject("$f$在$[a,b]$上",r"{连续}~","$\\implies ~f$在$[a,b]$上",r"{一致连续}",".")\
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
        graph_part = self.get_graph(lambda x: 1 / x, x_min=tracker.get_value(), x_max=tracker.get_value()+delta, color=YELLOW)
        def part_updater(part):
            new_part = self.get_graph(lambda x: 1 / x, x_min=tracker.get_value(), x_max=tracker.get_value()+delta, color=YELLOW)
            part.become(new_part)
        graph_part.add_updater(part_updater)
        lline = (self.get_vertical_line_to_graph(tracker.get_value(), graph_fracx))
        def lline_updater(line):
            new_line = (self.get_vertical_line_to_graph(tracker.get_value(), graph_fracx))
            line.become(new_line)
        lline.add_updater(lline_updater)
        rline = (self.get_vertical_line_to_graph(tracker.get_value()+delta, graph_fracx))
        def rline_updater(line):
            new_line = (self.get_vertical_line_to_graph(tracker.get_value()+delta, graph_fracx))
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
        self.play(ShowCreation(lline), ShowCreation(rline),Write(a), Write(b))
        self.play(ShowCreation(graph_part))
        # self.play(Write(a), Write(b))
        self.play(tracker.set_value, 0.045, run_time=3, rate_func=there_and_back)
        self.wait()
        lline.clear_updaters()
        rline.clear_updaters()
        graph_part.clear_updaters()

        self.play(FadeOut(VGroup(a,b,lline, rline, graph_part, graph_fracx, self.axes)))


    def proof(self):
        # ============================ negative part ===============================
        zheng = TextMobject("【证】").next_to(self.theorem, DOWN).align_to(self.title, LEFT)
        l1 = TextMobject("反证.","假设","$f(x)$","在","$[a,b]$","上不一致连续.","即","否定")
        def1 = TexMobject(r"\forall ", r"\varepsilon", r">0,", r" \exists", r"\delta", r">0,",
                           r"\forall x_1,x_2\in I, ") \
            .set_color_by_tex_to_color_map({"varepsilon": RED, "delta": GREEN})
        def2 = TexMobject(r"|x_1-x_2|<", r"\delta", r"\Longrightarrow","|f(x_1)-f(x_2)|<", r"\varepsilon", r".") \
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
        neg2[2].align_to(def2[2], ORIGIN)
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

        self.play(FadeOut(VGroup(def1, def2,l1[-1], dedao)))
        self.play(VGroup(neg1, neg2).next_to, l1, DOWN)
        # ============================ neg def part ===============================
        self.wait()
        self.play(Succession(Indicate(neg1[3:6]),Indicate(neg1[3:6])))


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
        self.play(ShowCreation(graph),rate_func=lambda t: smooth(1.5*t))