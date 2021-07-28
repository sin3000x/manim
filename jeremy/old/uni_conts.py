from manimlib.imports import *

# 一致连续性
class continuous(GraphScene):
    def construct(self):
        title = TextMobject("\\underline{\\heiti 函数的一致连续性}", color=YELLOW).to_corner(UL)
        def1 = TextMobject("$f(x)$在区间$I$上{\\heiti 一致连续}：")
        def11 = TexMobject(r"\forall ", r"\varepsilon", r">0,", r" \exists", r"\delta", r">0,",
                           r"\forall x_1,x_2\in I, ") \
            .set_color_by_tex_to_color_map({"varepsilon": RED, "delta": GREEN})
        replace1 = TexMobject(r"\delta", r"(", r"\varepsilon", r")") \
            .set_color_by_tex_to_color_map({"varepsilon": RED, "delta": GREEN})

        def12 = TexMobject(r"|x_1-x_2|<", r"\delta", r"\Rightarrow |f(x_1)-f(x_2)|<", r"\varepsilon", r".") \
            .set_color_by_tex_to_color_map({"varepsilon": RED, "delta": GREEN})
        e1 = TextMobject("\\kaishu 图象可以一笔画出来~$+$~不能太陡峭", color=YELLOW)

        def2 = TextMobject("$f(x)$在区间$I$上{\\heiti 连续}：")
        def21 = TexMobject(r"\forall", r" x_0", r"\in I,", r" \forall", r"\varepsilon", r">0, ",
                           r"\exists", r"\delta", r">0, ", r"\forall x\in I,") \
            .set_color_by_tex_to_color_map({"varepsilon": RED, "delta": GREEN, "x_0": BLUE})
        replace2 = TexMobject(r"\delta", r"(", r"\varepsilon", ",", "x_0", r")") \
            .set_color_by_tex_to_color_map({"varepsilon": RED, "delta": GREEN, "x_0": BLUE})
        def22 = TexMobject(r"|x-", r"x_0", r"|<", r"\delta", r"\Rightarrow |f(x)-f(", r"x_0", r")|<", r"\varepsilon",
                           ".") \
            .set_color_by_tex_to_color_map({"varepsilon": RED, "delta": GREEN, "x_0": BLUE})
        e2 = TextMobject("\\kaishu 图象可以一笔画出来", color=YELLOW)
        v1 = VGroup(def1, def11, def12).arrange(DOWN).next_to(title, DOWN)
        v2 = VGroup(def2, def21, def22).arrange(DOWN).next_to(v1, DOWN, buff=LARGE_BUFF)
        for defs in [*v1] + [*v2]:
            defs.set_x(0)

        def1.align_to(title, LEFT)
        def2.align_to(title, LEFT)
        line1 = Underline(def11[3:6], color=YELLOW)
        line2 = Underline(def21[6:9], color=YELLOW)
        replace1.next_to(def1, RIGHT)
        replace2.next_to(def2, RIGHT)
        e1.move_to(VGroup(def11, def12).get_center())
        e2.move_to(VGroup(def21, def22).get_center())
        arrow = TexMobject("\\Longrightarrow").rotate(-PI/2).scale(2).shift(UP+LEFT*2)
        bg_arrow = BackgroundRectangle(arrow)

        def frac():
            self.x_axis_width, self.y_axis_height = 6.5, 6.5
            self.x_max, self.y_max = .1, 100
            self.x_min, self.y_min = 0, 0
            self.graph_origin = 3 * DOWN + 5 * LEFT
            self.y_tick_frequency = 100
            self.x_tick_frequency = .1

            self.setup_axes(animate=True)
            graph_fracx = self.get_graph(lambda x: 1/x, x_max=.1, x_min=0.01)
            label_fracx = self.get_graph_label(graph_fracx, label="y=\\frac 1x", direction=UP)
            self.play(ShowCreation(graph_fracx))
            self.play(Write(label_fracx))
            y_up = ValueTracker(22)
            epsilon = 10
            vepsilon = TexMobject("\\varepsilon", color=RED).next_to(
                self.coords_to_point(0, y_up.get_value() - epsilon / 2), LEFT)
            vepsilon.add_updater(lambda obj: obj.next_to(self.coords_to_point(0, y_up.get_value() - epsilon / 2), LEFT))
            delta = TexMobject("\\delta", color=GREEN).next_to(self.coords_to_point(y_up.get_value() - epsilon / 2, 0),
                                                               DOWN)
            delta.add_updater(
                lambda obj: obj.next_to(self.coords_to_point(0.5*(1/(y_up.get_value() - epsilon)+1/y_up.get_value()), 0), DOWN))

            l_up = DashedLine(self.coords_to_point(0, y_up.get_value()),
                              self.coords_to_point(1/y_up.get_value(), y_up.get_value()))

            def update_lup(line):
                new_line = DashedLine(self.coords_to_point(0, y_up.get_value()),
                                      self.coords_to_point(1/y_up.get_value(), y_up.get_value()))
                line.become(new_line)

            l_up.add_updater(update_lup)

            l_right = DashedLine(self.coords_to_point(1/y_up.get_value(), y_up.get_value()),
                                 self.coords_to_point(1/y_up.get_value(), 0))

            def update_lright(line):
                new_line = DashedLine(self.coords_to_point(1/y_up.get_value() , y_up.get_value()),
                                      self.coords_to_point(1/y_up.get_value() , 0))
                line.become(new_line)

            l_right.add_updater(update_lright)

            l_down = DashedLine(self.coords_to_point(0, y_up.get_value() - epsilon),
                                self.coords_to_point(1/(y_up.get_value() - epsilon) , y_up.get_value() - epsilon))

            def update_ldown(line):
                new_line = DashedLine(self.coords_to_point(0, y_up.get_value() - epsilon),
                                      self.coords_to_point(1/(y_up.get_value() - epsilon) ,
                                                           y_up.get_value() - epsilon))
                line.become(new_line)

            l_down.add_updater(update_ldown)

            l_left = DashedLine(self.coords_to_point(1/(y_up.get_value() - epsilon), y_up.get_value() - epsilon),
                                self.coords_to_point(1/(y_up.get_value() - epsilon), 0))

            def update_lleft(line):
                new_line = DashedLine(
                    self.coords_to_point(1/(y_up.get_value() - epsilon), y_up.get_value() - epsilon),
                    self.coords_to_point(1/(y_up.get_value() - epsilon), 0))
                line.become(new_line)

            l_left.add_updater(update_lleft)

            self.play(ShowCreation(l_up), ShowCreation(l_down))
            self.play(Write(vepsilon))
            self.play(ShowCreation(l_right), ShowCreation(l_left))
            self.play(Write(delta))
            self.play(y_up.set_value, 99, run_time=4)
            self.wait()

            qaq = TexMobject("\\mathrm{QAQ?}", color=YELLOW).next_to(delta, RIGHT, buff=MED_LARGE_BUFF)
            self.play(Write(qaq))
            l1 = TextMobject("$\\frac 1x$在$(0,1)$上不一致连续.")
            l2 = TextMobject("但在$[\\sigma, +\\infty)$上一致连续.")
            v5 = VGroup(l1, l2).arrange(DOWN, aligned_edge=LEFT).to_edge(RIGHT).shift(UP)
            self.play(Write(l1))
            self.wait()
            self.play(Write(l2))
            self.wait()
            l_up.remove_updater(update_lup)
            l_down.remove_updater(update_ldown)
            l_left.remove_updater(update_lleft)
            l_right.remove_updater(update_lright)
            self.play(FadeOut(VGroup(*v5, qaq, self.axes, graph_fracx, label_fracx, l_up, l_down, l_left, l_right, vepsilon, delta)))

        def sqrtx():
            self.x_axis_width, self.y_axis_height = 6.5, 6.5
            self.x_max, self.y_max = 16, 6
            self.x_min, self.y_min = 0, 0
            self.graph_origin = 3 * DOWN + 5 * LEFT

            self.setup_axes(animate=True)
            graph_sqrtx = self.get_graph(np.sqrt, x_max=15.5, x_min=0)
            label_sqrtx = self.get_graph_label(graph_sqrtx, label="y=\\sqrt{x}", direction=RIGHT)
            self.play(ShowCreation(graph_sqrtx))
            self.play(Write(label_sqrtx))
            y_up = ValueTracker(3)
            epsilon = 1
            vepsilon = TexMobject("\\varepsilon", color=RED).next_to(
                self.coords_to_point(0, y_up.get_value() - epsilon / 2), LEFT)
            vepsilon.add_updater(lambda obj: obj.next_to(self.coords_to_point(0, y_up.get_value() - epsilon / 2), LEFT))
            delta = TexMobject("\\delta", color=GREEN).next_to(self.coords_to_point(y_up.get_value() - epsilon / 2, 0),
                                                               DOWN)
            delta.add_updater(lambda obj: obj.next_to(self.coords_to_point((y_up.get_value() - epsilon / 2)**2, 0), DOWN))

            l_up = DashedLine(self.coords_to_point(0, y_up.get_value()),
                              self.coords_to_point(y_up.get_value()**2, y_up.get_value()))

            def update_lup(line):
                new_line = DashedLine(self.coords_to_point(0, y_up.get_value()),
                                      self.coords_to_point(y_up.get_value()**2, y_up.get_value()))
                line.become(new_line)

            l_up.add_updater(update_lup)

            l_right = DashedLine(self.coords_to_point(y_up.get_value()**2, y_up.get_value()),
                                 self.coords_to_point(y_up.get_value()**2, 0))

            def update_lright(line):
                new_line = DashedLine(self.coords_to_point(y_up.get_value()**2, y_up.get_value()),
                                      self.coords_to_point(y_up.get_value()**2, 0))
                line.become(new_line)

            l_right.add_updater(update_lright)

            l_down = DashedLine(self.coords_to_point(0, y_up.get_value() - epsilon),
                                self.coords_to_point((y_up.get_value() - epsilon)**2, y_up.get_value() - epsilon))

            def update_ldown(line):
                new_line = DashedLine(self.coords_to_point(0, y_up.get_value() - epsilon),
                                      self.coords_to_point((y_up.get_value() - epsilon)**2, y_up.get_value() - epsilon))
                line.become(new_line)

            l_down.add_updater(update_ldown)

            l_left = DashedLine(self.coords_to_point((y_up.get_value() - epsilon)**2, y_up.get_value() - epsilon),
                                self.coords_to_point((y_up.get_value() - epsilon)**2, 0))

            def update_lleft(line):
                new_line = DashedLine(self.coords_to_point((y_up.get_value() - epsilon)**2, y_up.get_value() - epsilon),
                                      self.coords_to_point((y_up.get_value() - epsilon)**2, 0))
                line.become(new_line)

            l_left.add_updater(update_lleft)

            self.play(ShowCreation(l_up), ShowCreation(l_down))
            self.play(Write(vepsilon))
            self.play(ShowCreation(l_right), ShowCreation(l_left))
            self.play(Write(delta))
            self.play(y_up.set_value, 3.9)
            self.play(y_up.set_value, 1.5, run_time=2)
            self.play(y_up.set_value, 3, run_time=1)
            self.wait()
            ps = TextMobject("\\kaishu 注：我们不必找到图中这个最精确的$\\delta$.", color=YELLOW).next_to(delta, RIGHT, buff=.1).scale(.7).shift(LEFT)
            self.play(Write(ps))
            self.wait()

            l1 = TexMobject("\\text{取}", r"\delta", "=", r"\varepsilon","^2", ".").set_color_by_tex_to_color_map(
                {"varepsilon": RED, "delta": GREEN})
            l2 = TexMobject("\\text{那么}", "|x_1-x_2|<", r"\delta", "\\text{ 时，}").set_color_by_tex("delta", GREEN)
            l3 = TexMobject(r"|f(x_2)-f(x_1)|","=",r"|\sqrt{x_2}-\sqrt{x_1}|")
            l4 = TexMobject("=",r"{|x_2-x_1| \over {\sqrt{x_2}+\sqrt{x_1}}}")
            l5 = TexMobject(r"\leq", "{|x_2-x_1|\over\sqrt{|x_2-x_1|}}")
            l6 = TexMobject(r"=",r"\sqrt{|x_2-x_1|}")
            l7 = TexMobject(r"<",r"\sqrt",r"{\delta}").set_color_by_tex_to_color_map(
                {"varepsilon": RED, "delta": GREEN})
            l8 = TexMobject(r"=",r"\varepsilon").set_color_by_tex_to_color_map(
                {"varepsilon": RED, "delta": GREEN})
            v4 = VGroup(l1, l2, l3, l4, l5, l6, l7, l8).arrange(DOWN, aligned_edge=LEFT).to_edge(RIGHT).scale(.8)
            bg = BackgroundRectangle(v4)
            for _ in v4[3:]:
                _.align_to(l3[1], LEFT)
            self.play(ShowCreation(bg))
            for l in v4:
                self.play(Write(l))
            self.wait()
            l_up.remove_updater(update_lup)
            l_down.remove_updater(update_ldown)
            l_left.remove_updater(update_lleft)
            l_right.remove_updater(update_lright)
            self.play(FadeOut(v4), FadeOut(bg))
            self.play(FadeOut(VGroup(ps,  l_left, l_right, l_up, l_down, vepsilon, delta, self.axes, graph_sqrtx, label_sqrtx)))

        def x():
            self.x_axis_width, self.y_axis_height = 6.5, 6.5
            self.x_max, self.y_max = 6, 6
            self.x_min, self.y_min = 0, 0
            self.graph_origin = 3 * DOWN + 5 * LEFT

            self.setup_axes(animate=True)
            graph_x = self.get_graph(lambda x: x, x_max=5.5, x_min=0)
            label_x = self.get_graph_label(graph_x, label="y=x")
            self.play(ShowCreation(graph_x))
            self.play(Write(label_x))
            y_up = ValueTracker(4)
            epsilon = 1
            vepsilon = TexMobject("\\varepsilon", color=RED).next_to(
                self.coords_to_point(0, y_up.get_value() - epsilon / 2), LEFT)
            vepsilon.add_updater(lambda obj: obj.next_to(self.coords_to_point(0, y_up.get_value() - epsilon / 2), LEFT))
            delta = TexMobject("\\delta", color=GREEN).next_to(self.coords_to_point(y_up.get_value() - epsilon / 2, 0),
                                                               DOWN)
            delta.add_updater(lambda obj: obj.next_to(self.coords_to_point(y_up.get_value() - epsilon / 2, 0), DOWN))
            l_up = DashedLine(self.coords_to_point(0, y_up.get_value()),
                              self.coords_to_point(y_up.get_value(), y_up.get_value()))

            def update_lup(line):
                new_line = DashedLine(self.coords_to_point(0, y_up.get_value()),
                                      self.coords_to_point(y_up.get_value(), y_up.get_value()))
                line.become(new_line)

            l_up.add_updater(update_lup)

            l_right = DashedLine(self.coords_to_point(y_up.get_value(), y_up.get_value()),
                                 self.coords_to_point(y_up.get_value(), 0))

            def update_lright(line):
                new_line = DashedLine(self.coords_to_point(y_up.get_value(), y_up.get_value()),
                                      self.coords_to_point(y_up.get_value(), 0))
                line.become(new_line)

            l_right.add_updater(update_lright)

            l_down = DashedLine(self.coords_to_point(0, y_up.get_value() - epsilon),
                                self.coords_to_point(y_up.get_value() - epsilon, y_up.get_value() - epsilon))

            def update_ldown(line):
                new_line = DashedLine(self.coords_to_point(0, y_up.get_value() - epsilon),
                                      self.coords_to_point(y_up.get_value() - epsilon, y_up.get_value() - epsilon))
                line.become(new_line)

            l_down.add_updater(update_ldown)

            l_left = DashedLine(self.coords_to_point(y_up.get_value() - epsilon, y_up.get_value() - epsilon),
                                self.coords_to_point(y_up.get_value() - epsilon, 0))

            def update_lleft(line):
                new_line = DashedLine(self.coords_to_point(y_up.get_value() - epsilon, y_up.get_value() - epsilon),
                                      self.coords_to_point(y_up.get_value() - epsilon, 0))
                line.become(new_line)

            l_left.add_updater(update_lleft)

            l1 = TexMobject("\\text{取}", r"\delta", "=", r"\varepsilon", ".").set_color_by_tex_to_color_map(
                {"varepsilon": RED, "delta": GREEN})
            l2 = TexMobject("\\text{那么}", "|x_1-x_2|<", r"\delta", "\\text{ 时，}").set_color_by_tex("delta", GREEN)
            l3 = TexMobject("|f(x_1)-f(x_2)|=|x_1-x_2|<", r"\delta", "=", r"\varepsilon").set_color_by_tex_to_color_map(
                {"varepsilon": RED, "delta": GREEN})
            v3 = VGroup(l1, l2, l3).arrange(DOWN, aligned_edge=LEFT).to_edge(RIGHT)
            bg = BackgroundRectangle(v3, opacity=1)
            self.play(ShowCreation(l_up), ShowCreation(l_down))
            self.play(Write(vepsilon))
            self.play(ShowCreation(l_right), ShowCreation(l_left))
            self.play(Write(delta))
            self.play(y_up.set_value, 5.4)
            self.play(y_up.set_value, 1.2, run_time=2)
            self.play(y_up.set_value, 4, run_time=2)
            self.wait()

            line_up = Line(self.coords_to_point(y_up.get_value() - .4, y_up.get_value() - .4),
                                 self.coords_to_point(0, y_up.get_value() - .4), color=YELLOW)
            line_down = Line(self.coords_to_point(y_up.get_value() - .8, y_up.get_value() - .8),
                                   self.coords_to_point(0, y_up.get_value() - .8), color=YELLOW)
            line_left = Line(self.coords_to_point(y_up.get_value() - .8, 0),
                                   self.coords_to_point(y_up.get_value() - .8, y_up.get_value() - .8), color=YELLOW)
            line_right = Line(self.coords_to_point(y_up.get_value() - .4, 0),
                                    self.coords_to_point(y_up.get_value() - .4, y_up.get_value() - .4), color=YELLOW)

            self.play(ShowCreation(line_left), ShowCreation(line_right))
            self.wait()
            self.play(ShowCreation(line_down), ShowCreation(line_up))
            self.wait()
            self.play(FadeOut(VGroup(line_left, line_right, line_up, line_down)), ShowCreation(bg))
            self.play(Write(l1))
            self.play(Write(l2))
            self.play(Write(l3))
            self.wait()
            l_up.remove_updater(update_lup)
            l_down.remove_updater(update_ldown)
            l_left.remove_updater(update_lleft)
            l_right.remove_updater(update_lright)
            self.play(FadeOut(v3), FadeOut(bg))
            self.play(FadeOut(VGroup(vepsilon, delta, l_down, l_up, l_right, l_left, self.axes, graph_x, label_x)))

        def first():
            self.play(Write(title))
            self.wait()
            # uniform continuous
            self.play(Write(def1))
            self.wait()
            self.play(Write(def11[:3]))
            self.wait()
            self.play(Write(def11[3:6]))
            self.wait()
            self.play(Write(def11[6:]))
            self.wait()
            self.play(Write(def12[:2]))
            self.wait()
            self.play(Write(def12[2:]))
            self.wait(2)
            # continuous
            self.play(Write(def2))
            self.wait()
            self.play(Write(def21[:3]))
            self.wait()
            self.play(Write(def21[3:6]))
            self.wait()
            self.play(Write(def21[6:9]))
            self.wait()
            self.play(Write(def21[9:]))
            self.wait()
            self.play(Write(def22[:4]))
            self.wait()
            self.play(Write(def22[4:]))
            self.wait()

            # explain
            self.play(ShowCreation(line1))
            self.play(ShowCreation(line2))
            self.wait()
            self.play(Write(replace1))
            self.wait()
            self.play(Write(replace2))
            self.wait(2)
            self.play(FadeOut(VGroup(title, *v1, *v2, line1, line2, replace1, replace2)))

        def second():
            l1 = TextMobject("\\heiti 对于可导函数，", color=BLUE).to_edge(TOP).shift(UP)
            l2 = TextMobject("导数有界~$\\Longrightarrow$~一致连续：", color=YELLOW)
            l3 = TexMobject(r"|f(x_1)-f(x_2)|=|f'(\xi)|\cdot|x_1-x_2|\leq M|x_1-x_2|\leq M\delta")
            l4 = TextMobject("一致连续~$\\centernot\\Longrightarrow$~导数有界：", color=YELLOW)
            l5 = TexMobject(r"(\sqrt{x})'={1\over {2\sqrt{x}}}\text{ 于}~(0, +\infty)~\text{上无界}.")
            v = VGroup(l2, l3, l4, l5).arrange(DOWN).next_to(l1, DOWN, buff=MED_LARGE_BUFF)
            l2.to_edge(LEFT)
            l4.to_edge(LEFT).shift(DOWN*.8)
            l5.shift(DOWN*.8)
            for l in [l1, *v]:
                self.play(Write(l))
                self.wait()
            self.play(FadeOut(VGroup(l1, *v)), FadeIn(VGroup(title, *v1, *v2, line1, line2, replace1, replace2)), run_time=2)

        def last():
            self.wait()
            self.play(ReplacementTransform(VGroup(def21, def22, line2), e2))
            self.wait()
            self.play(ReplacementTransform(VGroup(def11, def12, line1), e1))
            self.wait()
            self.play(FadeIn(bg_arrow))
            self.play(Write(arrow))
            self.wait(2)
            
            
        first()
        x()
        sqrtx()
        frac()
        second()
        last()