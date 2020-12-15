from manimlib.imports import *


class mvt(GraphScene):
    CONFIG = {
        "map": {"a": BLUE, "b": RED, "arrow": WHITE, "kaishu": WHITE, "forall": WHITE}
    }

    def construct(self):
        self.fermat()
        self.rolle()
        self.lagrange()
        self.cauchy()

    def fermat(self):
        title = TextMobject(r"\textbf{\underline{{\heiti Fermat定理（引理）}}}", color=YELLOW).to_corner(UL)
        self.play(Write(title))
        self.wait()

        theorem = TexMobject(r"f\text{ 在极值点~}", "x_0", r"\in (a,b)", r"\text{ 处可导}",
                             r"~\Longrightarrow~", "f'(", "x_0", ")=0.") \
            .set_color_by_tex("x_0", RED).next_to(title, DOWN).set_x(0)
        self.play(Write(theorem[:4]))
        self.wait()
        self.play(Write(theorem[4:]))
        self.wait()

        # plot
        self.x_min, self.x_max = 0, 2
        self.y_min, self.y_max = 0, 1.2
        self.x_axis_width, self.y_axis_height = 4, 4
        self.x_tick_frequency, self.y_tick_frequency = 1, self.y_max
        self.setup_axes(True)
        func = lambda x: -(x - 1) ** 2 + 1
        graph = self.get_graph(func, x_min=0.2, x_max=1.8)

        prop = TexMobject("f(x)", r"\leq", "f(", "x_0", ")").set_color_by_tex("x_0", RED)
        slope = TexMobject(r"{{f(x)-f(", "x_0", r")}", r"\over", r"{x-", r"x_0}}\geq 0",
                           color=YELLOW)  # .set_color_by_tex("x_0", RED)
        left_limit = TexMobject(r"\lim_{", r"x\to", "x_0", "^-}", r"{{f(x)-f(", "x_0", r")}", r"\over", r"{x-",
                                r"x_0}}\geq 0", color=YELLOW)  # .set_color_by_tex("x_0", RED)
        right_limit = TexMobject(r"\lim_{", r"x\to", "x_0", "^+}", r"{{f(x)-f(", "x_0", r")}", r"\over", r"{x-",
                                 r"x_0}}\leq 0", color=YELLOW)  # .set_color_by_tex("x_0", RED)
        limits = VGroup(slope, right_limit).arrange(DOWN)
        VGroup(prop, limits).arrange(DOWN, buff=MED_LARGE_BUFF).next_to(graph, RIGHT).shift(RIGHT)
        box = BackgroundRoundedRectangle(VGroup(prop, limits), color=GOLD, buff=0.2, fill_opacity=0.15)
        left_limit.move_to(slope)

        self.play(ShowCreation(graph))
        self.wait()

        peak = Dot(self.coords_to_point(1, func(1)), color=RED)
        x0_label = TexMobject("x_0", color=RED).scale(.8).next_to(self.coords_to_point(1, 0), DOWN)
        self.play(GrowFromCenter(peak), FadeIn(x0_label))
        self.play(FadeIn(box))
        self.play(Write(prop))

        x = ValueTracker(0.3)
        tick = self.x_axis.get_tick(x.get_value())
        tick.add_updater(lambda tick: tick.become(self.x_axis.get_tick(x.get_value())))
        moving = Dot()
        moving.add_updater(lambda dot: dot.move_to(self.coords_to_point(x.get_value(), func(x.get_value()))))
        x_label = TexMobject("x").scale(.8).next_to(self.coords_to_point(1, 0), DOWN)
        x_label.add_updater(lambda label: label.next_to(self.coords_to_point(x.get_value(), 0), DOWN))
        line = Line()

        def line_updater(line):
            new = Line(moving.get_center(), peak.get_center(), color=YELLOW)
            new.set_length(4)
            line.become(new)
            return line

        line.add_updater(line_updater)

        self.play(GrowFromCenter(moving), FadeIn(tick), FadeIn(x_label))
        self.play(ShowCreation(line))
        self.play(Write(slope))
        self.wait()
        self.play(ReplacementTransform(slope, left_limit[4:]), Write(left_limit[:4]), x.set_value, 0.99, run_time=2)
        self.wait()

        self.play(x.set_value, 1.6, run_time=.3)
        self.wait()

        self.play(Write(right_limit), x.set_value, 1.01, run_time=2)
        self.wait(2)

        limit = TexMobject(r"\lim_{", r"x\to", "x_0}", r"{{f(x)-f(", "x_0", r")}", r"\over", r"{x-", r"x_0}}", "= 0",
                           color=YELLOW).move_to(limits)
        der = TexMobject(r"f'(x_0)", "=0", color=YELLOW).move_to(limit)
        self.play(ReplacementTransform(VGroup(left_limit, right_limit), limit))
        self.wait()
        self.play(ReplacementTransform(limit[:-1], der[:-1]), ReplacementTransform(limit[-1], der[-1]))
        self.wait()

        for to_clear in [line, moving, tick, x_label]:
            to_clear.clear_updaters()
        self.remove(peak)
        self.play(
            FadeOut(VGroup(box, line, moving, tick, x_label, der, prop, title, theorem, x0_label, graph, self.axes)))

    def rolle(self):
        self.x_min, self.x_max = 0, 2
        self.y_min, self.y_max = 0, 1.4
        self.x_axis_width, self.y_axis_height = 4, 3.5
        self.graph_origin -= [1.2, 0.5, 0]
        self.y_bottom_tick = 0
        self.x_tick_frequency, self.y_tick_frequency = self.x_max, self.y_max
        title = TextMobject(r"\textbf{\underline{{\heiti Rolle中值定理}}}", color=YELLOW).to_corner(UL)
        self.play(Write(title))
        self.wait()

        theorem1 = TexMobject(r"f\text{ 在~}", "[", "a", ",", "b", "]", r"\text{~连续,~}", r"(", "a", ",", "b", ")",
                              r"\text{~可导.~}"
                              ) \
            .set_color_by_tex_to_color_map(self.map)
        theorem2 = TexMobject(r"f(", "a", ")", "=", "f", "(", "b", ")",
                              r"~\Longrightarrow~", r"\exists", r"\xi\in ", "(", "a", ",", "b", ")", ",",
                              r"\text{~s.t.~}", "f'(", r"\xi", ")=0.").set_color_by_tex_to_color_map(self.map)
        VGroup(theorem1, theorem2).arrange(DOWN).next_to(title, DOWN).set_x(0)
        self.play(Write(theorem1))
        self.wait()
        self.play(Write(theorem2))
        self.wait()

        f = lambda x: -0.48 + 7.05 * x - 8.83333 * x ** 2 + 2.91667 * x ** 3
        self.setup_axes(True)
        a_tick, b_tick = self.x_axis.get_tick(0.2), self.x_axis.get_tick(1.8)
        a_label, b_label = TexMobject("a", color=self.map['a']).next_to(a_tick, DOWN), TexMobject("b", color=self.map[
            'b']).next_to(b_tick, DOWN)
        b_label.align_to(a_label, DOWN)
        graph = self.get_graph(f, x_min=0.2, x_max=1.8)
        self.play(ShowCreation(graph), FadeIn(VGroup(a_tick, b_tick, a_label, b_label)))
        line = DashedLine(graph.get_start(), graph.get_end(), color=YELLOW).scale_in_place(1.4)
        self.play(ShowCreation(line))
        self.wait()

        xmax = 0.547546
        xmin = 1.4715
        min_dot = Dot(self.coords_to_point(xmin, f(xmin)))
        max_dot = Dot(self.coords_to_point(xmax, f(xmax)))
        jizhi = TextMobject(r"{\kaishu 极值点}").scale(.8).move_to(self.coords_to_point(xmin, f(xmax)))
        left_arrow = Arrow(jizhi.get_left(), max_dot)
        down_arrow = Arrow(jizhi.get_bottom(), min_dot).match_style(left_arrow)
        down_arrow.get_tip().set_width(left_arrow.get_tip().get_width()).shift(UP * 0.1)

        only = TextMobject(r"{\kaishu 只需说明极值点~$\xi$~在内部取到.}")
        assumption = TextMobject(r"{\kaishu 设~$M>m$.}")
        notboth = TexMobject(r"f(", "a", ")=f(", "b", ")", r"\text{\kaishu 不能同时取到}M,m.").set_color_by_tex_to_color_map(
            self.map)
        xi = TextMobject(r"{\kaishu 必有内点~$\xi$~取到了最值.}")
        fact = TextMobject(r"{\kaishu （内部的最值点是极值点）}", color=YELLOW)
        v = VGroup(only, assumption, notboth, xi, fact).arrange(DOWN).next_to(theorem2, DOWN,
                                                                              buff=MED_LARGE_BUFF).to_edge(RIGHT)
        box = BackgroundRoundedRectangle(v, color=GOLD, buff=0.2, fill_opacity=0.15)
        # VGroup(min_dot, max_dot, jizhi, left_arrow, down_arrow).set_color(GREEN)
        self.play(FadeIn(VGroup(min_dot, max_dot, jizhi)), GrowArrow(left_arrow), GrowArrow(down_arrow))
        self.play(FadeIn(box))
        self.play(Write(only), run_time=2)
        self.wait()

        max_tick = self.y_axis.get_tick(f(xmax))
        min_tick = self.y_axis.get_tick(f(xmin))
        M_label, m_label = TexMobject('M').next_to(max_tick, LEFT), TexMobject('m').next_to(min_tick, LEFT)
        self.play(FadeOut(VGroup(jizhi, left_arrow, down_arrow)))
        self.play(FadeIn(VGroup(max_tick, min_tick, M_label, m_label)))
        self.wait()
        self.play(Write(assumption))
        self.wait()

        saving = [max_tick, min_tick, M_label, m_label, graph, max_dot, min_dot]
        for to_save in saving:
            to_save.save_state()

        constant = self.get_graph(lambda x: 0.6, x_min=0.2, x_max=1.8, color=GREEN)
        self.play(Transform(graph, constant),
                  *list(it.chain(
                      *[[i.set_y, line.get_y()] for i in [max_tick, min_tick, M_label, m_label, max_dot, min_dot]])))
        self.wait()
        self.play(AnimationGroup(*[Restore(to_restore) for to_restore in saving]))
        self.wait()
        self.play(Write(notboth))
        self.wait()
        self.play(Write(xi), FadeIn(VGroup(jizhi, left_arrow, down_arrow)), run_time=2)
        self.wait(2)
        self.play(Write(fact))
        self.wait(2)
        self.play(FadeOut(
            VGroup(jizhi, left_arrow, down_arrow, title, theorem1, theorem2, line, self.axes, box, a_tick, b_tick,
                   a_label, b_label, *saving, *v)))

    def lagrange(self):
        # self.x_min, self.x_max = 0, 2
        self.y_min, self.y_max = 0, 1.2
        # self.x_axis_width, self.y_axis_height = 4, 3.5
        self.graph_origin -= [.5, 0, 0]
        # self.y_bottom_tick = 0
        self.x_tick_frequency, self.y_tick_frequency = self.x_max, self.y_max
        title = TextMobject(r"\textbf{\underline{{\heiti Lagrange中值定理}}}", color=YELLOW).to_corner(UL)
        self.play(Write(title))
        self.wait()

        theorem1 = TexMobject(r"f\text{ 在~}", "[", "a", ",", "b", "]", r"\text{~连续,~}", r"(", "a", ",", "b", ")",
                              r"\text{~可导.~}"
                              ) \
            .set_color_by_tex_to_color_map(self.map)
        theorem2 = TexMobject(r"\Longrightarrow~", r"\exists", r"\xi\in ", "(", "a", ",", "b", ")", ",",
                              r"\text{~s.t.~}", "f'(", r"\xi", r")={{f(", "b", ")-f(", "a", r")}\over", "{b", "-",
                              "a}}", ".").set_color_by_tex_to_color_map(self.map)
        VGroup(theorem1, theorem2).arrange(DOWN, buff=SMALL_BUFF).next_to(title, DOWN).set_x(0)
        self.play(Write(theorem1))
        self.wait()
        self.play(Write(theorem2))
        self.wait()

        self.setup_axes(True)
        f = lambda x: -0.0336538 + 1.81891 * x - 0.753205 * x ** 2
        graph = self.get_graph(f, x_min=0.2, x_max=1.8, color=GREEN)
        self.play(ShowCreation(graph))

        min_dot, max_dot = Dot(self.coords_to_point(0.2, f(0.2))), Dot(self.coords_to_point(1.8, f(1.8)))
        left_tick, right_tick = self.x_axis.get_tick(0.2), self.x_axis.get_tick(1.8)
        down_tick, up_tick = self.y_axis.get_tick(f(0.2)), self.y_axis.get_tick(f(1.8))
        a_label, b_label = TexMobject("a", color=self.map['a']).next_to(left_tick, DOWN), TexMobject("b",
                                                                                                     color=self.map[
                                                                                                         'b']).next_to(
            right_tick, DOWN)
        b_label.align_to(a_label, DOWN)
        fa_label, fb_label = TexMobject("f(", "a", ")").set_color_by_tex_to_color_map(self.map).next_to(down_tick,
                                                                                                        LEFT), \
                             TexMobject("f(", "b", ")").set_color_by_tex_to_color_map(self.map).next_to(up_tick, LEFT)

        line = Line(graph.get_start(), graph.get_end(), color=YELLOW).scale_in_place(1.4)
        scale = self.coords_to_point(0, 1)[1] - self.coords_to_point(0, 0)[1]
        through_origin = line.copy().shift(DOWN * 0.2375 * scale)
        left_line = Line(self.coords_to_point(0.2, f(0.2)), self.coords_to_point(0.2, 1 / 16), color=PINK)
        right_line = Line(self.coords_to_point(1.8, f(1.8)), self.coords_to_point(1.8, 9 / 16), color=PINK)
        tangent = DashedVMobject(self.get_graph(lambda x: 5 / 16 * (x - 1) + f(1), x_min=0.2, x_max=1.7, color=YELLOW))
        xi_tick = self.x_axis.get_tick(1)
        xi_label = TexMobject(r"\xi").next_to(xi_tick, DOWN)
        self.play(GrowFromCenter(min_dot), GrowFromCenter(max_dot),
                  FadeIn(VGroup(left_tick, right_tick, down_tick, up_tick,
                                a_label, b_label, fa_label, fb_label)))
        self.play(ShowCreation(line))
        self.wait()
        self.play(FadeIn(VGroup(xi_tick, xi_label)))
        self.play(ShowCreation(tangent))
        self.wait()
        self.play(FadeOut(VGroup(xi_tick, xi_label, tangent)))

        f_label = self.get_graph_label(graph, direction=UP).next_to(graph, UP)
        l_label = TexMobject("l(x)", color=YELLOW).next_to(line.get_center(), DOWN)
        h = TexMobject(r"h(x)\coloneqq f(x)-l(x)")
        two_points = TexMobject("{{y-f(a)}\over{f(b)-f(a)}}={{x-a}\over{b-a}}", color=YELLOW)
        l1 = TexMobject(r"l(x)=", r"\frac{b-x}{b-a} f(a)+\frac{x-a}{b-a} f(b)", color=YELLOW)
        l2 = TexMobject(r"l(x)=", r"\frac{f(b)-f(a)}{b-a}x", color=YELLOW)
        both_zero = TexMobject("h(", "a", ")=h(", "b", ")", "=", "0", r"~\Longrightarrow~",
                               r"h'(\xi)=0").set_color_by_tex_to_color_map(self.map)
        equal = TexMobject("h(", "a", ")=h(", "b", ")", r"~\Longrightarrow~",
                           r"h'(\xi)=0").set_color_by_tex_to_color_map(self.map)
        result = TexMobject(r"f'(\xi)=l'(\xi)", "=", "{{f(", "b", ")-f(", "a", r")}\over", "{b", "-", "a}}",
                            ".").set_color_by_tex_to_color_map(self.map)
        v = VGroup(h, two_points, both_zero, result).arrange(DOWN).next_to(theorem2, DOWN).to_edge(RIGHT, buff=.75)
        box = BackgroundRoundedRectangle(v, color=GOLD, buff=0.2, fill_opacity=0.15)
        l1.move_to(two_points)
        l2.move_to(l1)
        equal.move_to(both_zero)
        self.play(Write(f_label))
        self.play(Write(l_label))
        self.play(FadeIn(box))
        self.play(Write(h))
        self.wait()
        self.play(ReplacementTransform(l_label.copy(), two_points))
        self.wait()
        self.play(ReplacementTransform(two_points, l1))
        self.wait()
        self.play(Write(both_zero))
        self.wait()
        self.play(Write(result[0]))
        self.wait()
        self.play(Write(result[1:]))
        self.wait(2)

        # translation
        self.play(ReplacementTransform(line, through_origin),
                  GrowArrow(left_line), GrowArrow(right_line), l_label.next_to, through_origin.get_center(), DOWN,
                  run_time=2)
        self.play(ReplacementTransform(l1[0], l2[0]), ReplacementTransform(l1[1:], l2[1:]))
        self.wait()
        self.play(ReplacementTransform(both_zero[:5], equal[:5]), ReplacementTransform(both_zero[-2:], equal[-2:]),
                  FadeOut(both_zero[5:-2]))
        self.wait(2)
        self.play(FadeOut(VGroup(title, theorem1, theorem2, self.axes,
                                 left_tick, right_tick, up_tick, down_tick,
                                 min_dot, max_dot,
                                 a_label, b_label, fa_label, fb_label, f_label, l_label,
                                 graph, through_origin, left_line, right_line,
                                 h, equal, l2, result,
                                 box)))

    def cauchy(self):
        title = TextMobject(r"\textbf{\underline{{\heiti Cauchy中值定理}}}", color=YELLOW).to_corner(UL)
        self.play(Write(title))
        self.wait()

        theorem1 = TexMobject(r"f,g", r"\text{ 在~}", "[", "a", ",", "b", "]", r"\text{~连续,~}", r"(", "a", ",", "b", ")",
                              r"\text{~可导.~}"
                              ) \
            .set_color_by_tex_to_color_map(self.map)
        theorem2 = TexMobject(r"g'(x)\neq 0,~", r"\forall", r"x\in (", r"a", ",", "b",
                              ")").set_color_by_tex_to_color_map(self.map)
        theorem3 = TexMobject(r"\Longrightarrow~", r"\exists", r"\xi\in ", "(", "a", ",", "b", ")", ",",
                              r"\text{~s.t.~}", "{{f(", "b", ")-f(", "a", r")}\over", "{g(", "b", ")", "-",
                              "g(", "a", ")}}", r"={f'(\xi)\over ",r"g'(\xi)}", ".").set_color_by_tex_to_color_map(self.map)
        VGroup(theorem1, theorem2, theorem3).arrange(DOWN, buff=SMALL_BUFF).next_to(title, DOWN).set_x(0)
        self.play(Write(theorem1))
        self.wait()
        self.play(Write(theorem2))
        self.wait()
        self.play(Write(theorem3), run_time=3)
        self.wait()
        frame = SurroundingRectangle(theorem2, color=YELLOW, buff=.1)
        frame_xi = SurroundingRectangle(theorem3[-2], color=YELLOW, buff=.1)
        frame_ab = SurroundingRectangle(theorem3[-10:-3], color=YELLOW, buff=.1)
        self.play(ShowCreation(frame))
        self.wait()
        self.play(ReplacementTransform(frame, frame_xi))
        self.wait()
        self.play(ReplacementTransform(frame_xi, frame_ab))
        self.wait()
        self.play(FadeOut(frame_ab))
        self.play(FadeOut(VGroup(theorem1, theorem2)), theorem3.move_to, theorem1)
        self.play(FadeOut(theorem3[0]))

        h = TexMobject(r"h(x)\coloneqq f(x)-l(x)")
        l1 = TexMobject(r"l_2(x)=", r"{{b", "-", r"x}", r"\over", "{b", "-", "a}}", " f(a)+", "{{x", "-", "a}",
                        r"\over", r"{b", "-", "a}}", " f(b)")
        l1g = TexMobject(r"l_2(x)=", r"{{g(b)", "-", r"g(x)}", r"\over", "{g(b)", "-", "g(a)}}", " f(a)+", "{{g(x)",
                         "-", "g(a)}", r"\over", r"{g(b)", "-", "g(a)}}", " f(b)")
        l2 = TexMobject(r"l(x)=", r"{{f(b)-f(a)}\over{", "b", "-", "a", "}}x", color=YELLOW)
        l2g = TexMobject(r"l(x)=", r"{{f(b)-f(a)}\over{", "g", "(", "b", ")", "-", "g", "(", "a", ")", "}", "}", "g",
                         "(", "x", ")", color=YELLOW)

        equal = TexMobject("h(", "a", ")=h(", "b", ")", r"~\Longrightarrow~",
                           r"h'(\xi)=0").set_color_by_tex_to_color_map(self.map)
        result = TexMobject(r"f'(\xi)=l'(\xi)", "=", "{{f(", "b", ")-f(", "a", r")}\over", "{g(", "b", ")", "-", "g(",
                            "a", ")}}", r"g'(\xi)",
                            ".").set_color_by_tex_to_color_map(self.map)

        v = VGroup(h, l2g, l1g, result).arrange(DOWN, buff=.15).next_to(theorem3, DOWN, buff=MED_LARGE_BUFF)
        l2.move_to(l2g)
        l1.move_to(l1g)
        equal.move_to(l1g)
        box = BackgroundRoundedRectangle(v, color=GOLD, buff=0.2, fill_opacity=0.15)
        self.play(FadeIn(box))
        self.play(Write(h))
        self.play(Write(l2))
        self.wait()
        self.play(ReplacementTransform(l2[:2], l2g[:2]), ReplacementTransform(l2[2], l2g[2:6]),
                  ReplacementTransform(l2[3], l2g[6]), ReplacementTransform(l2[4], l2g[7:11]),
                  ReplacementTransform(l2[-1], l2g[-4:]))
        self.wait()
        self.play(Write(l1))
        self.wait()
        self.play(AnimationGroup(*[ReplacementTransform(l1[i], l1g[i]) for i in range(17)]))
        self.wait()
        self.play(FadeOut(l1g))
        self.play(Write(equal))
        self.wait()
        self.play(Write(result[0]))
        self.wait()
        self.play(Write(result[1:]))
        self.wait(3)

        self.play(FadeOut(VGroup(box, h, l2g, equal, result)))

        self.x_min, self.x_max = 0, 2.2
        self.y_min, self.y_max = 0, 1.5
        self.x_axis_width, self.y_axis_height = 4, 3.5
        self.graph_origin = 2.5 * DOWN + 4.5 * LEFT
        self.y_bottom_tick = 0
        self.x_tick_frequency, self.y_tick_frequency = self.x_max, self.y_max
        self.x_axis_label, self.y_axis_label = "$g(t)$", "$f(t)$"
        self.setup_axes(True)
        f = lambda x: (x - 1) ** 2 + 0.3
        graph = self.get_graph(f, x_min=0.3, x_max=2, color=GREEN)
        self.play(ShowCreation(graph))
        left_tick, right_tick = self.x_axis.get_tick(0.3), self.x_axis.get_tick(2)
        down_tick, up_tick = self.y_axis.get_tick(f(0.3)), self.y_axis.get_tick(f(2))
        xi_g_tick, xi_f_tick = self.x_axis.get_tick(1.15), self.y_axis.get_tick(f(1.15))
        xi_g_label, xi_f_label = TexMobject("g(", r"\xi", ")").next_to(xi_g_tick, DOWN), \
                                 TexMobject("f(", r"\xi", ")").next_to(
                                     xi_f_tick, LEFT)
        left_label, right_label = TexMobject("g(", "a", ")").set_color_by_tex_to_color_map(self.map).next_to(left_tick,
                                                                                                             DOWN), \
                                  TexMobject("g(", "b", ")").set_color_by_tex_to_color_map(self.map).next_to(
                                      right_tick, DOWN)
        right_label.align_to(left_label, DOWN)
        down_label, up_label = TexMobject("f(", "a", ")").set_color_by_tex_to_color_map(self.map).next_to(down_tick,
                                                                                                          LEFT), \
                               TexMobject("f(", "b", ")").set_color_by_tex_to_color_map(self.map).next_to(up_tick, LEFT)
        slope_ab = TexMobject(r"k=\frac{f(b)-f(a)}{g(b)-g(a)}", color=YELLOW)
        slope_xi = TexMobject(r"k", r"=\frac{\mathrm{d}f}{\mathrm{d}g} (\xi)=\frac{\frac{\mathrm{d}f(\xi)}"
                                    r"{\mathrm{d}t}}{\frac{\mathrm{d}g(\xi)}{\mathrm{d}t}}",
                              r"=\frac{f'(\xi)}{g'(\xi)}", color=TEAL)
        VGroup(slope_ab, slope_xi).arrange(DOWN, aligned_edge=LEFT).next_to(theorem3, DOWN, buff=MED_LARGE_BUFF).to_edge(RIGHT)
        self.play(FadeIn(VGroup(left_tick, right_tick, down_tick, up_tick,
                                left_label, right_label, down_label, up_label)))
        line = Line(graph.get_start(), graph.get_end(), color=YELLOW).scale_in_place(1.4)
        tangent = self.get_graph(lambda x: 0.3 * (x - 1.15) + f(1.15), x_min=0, x_max=2.4, color=TEAL)
        self.play(ShowCreation(line))
        self.wait()
        self.play(Write(slope_ab))
        self.wait()
        self.play(FadeOut(VGroup(left_tick, right_tick, down_tick, up_tick,
                                left_label, right_label, down_label, up_label)),
                  FadeIn(VGroup(xi_f_label, xi_g_label, xi_f_tick, xi_g_tick)))
        self.play(ShowCreation(tangent))
        self.play(Write(slope_xi), run_time=3)
        self.wait(3)




class test(Scene):
    def construct(self):
        a = TexMobject(r"f'(\xi)=\frac{f(b)-f(a)}{b-a}").scale(2)
        self.add(a)
