from manimlib import *


class ImplictIntro(Scene):
    def construct(self):
        eq1 = Tex("x^2+y-1=0", color=YELLOW, isolate=list("x^2+y-1=0")).scale(1.2).to_edge(UP, buff=1)
        xy1 = Tex("x=1", "\\quad\\Longrightarrow\\quad ", "y=0").next_to(eq1, DOWN, buff=.5)
        implicit_label = VGroup(TexText("Implicit Equation"), TexText("隐式方程")).arrange(DOWN).scale(.8).next_to(eq1,
                                                                                                               DOWN)
        what_we_cares = TexText("是否给出了函数$y=f(x)$?")
        another_way = TexText("给定$x$，", "确定了唯一的$y$.", color=BLUE)
        eq1_ex = Tex(r"y=1-x^2", isolate=list("y=1-x^2"), color=YELLOW).scale(1.2).move_to(eq1)
        eq2 = Tex(r"\sin x+\ln y-xy^3=0", color=YELLOW).scale(1.2).next_to(what_we_cares, DOWN, buff=.5)
        xy2 = Tex("x=1", "\\quad\\Longrightarrow\\quad ", "y=0.48").next_to(eq2, DOWN, buff=.5)
        for i, j in zip(xy1, xy2):
            j.align_to(i, LEFT)
        y_add = Tex("y=0.91").next_to(xy2[-1], DOWN)
        v = VGroup(xy2, y_add)
        cross = Cross(v, stroke_width=[6, 6, 6])

        self.play(Write(eq1))
        self.wait()
        self.play(Write(implicit_label))
        self.wait()

        self.play(Write(what_we_cares))
        self.wait()

        self.play(TransformMatchingShapes(eq1, eq1_ex, path_arc=PI / 2))
        self.wait()

        self.play(Write(eq2))
        self.wait()

        self.play(FadeTransform(eq1_ex, eq1), FadeOut(implicit_label))
        self.wait()
        self.play(FadeOut(what_we_cares))
        self.wait()
        self.play(Write(another_way[0]), Write(xy1[0]))
        self.wait()
        self.play(Write(another_way[1]), Write(xy1[1:]))
        self.wait()

        self.play(Write(xy2))
        self.play(Write(y_add))
        self.wait()
        self.play(ShowCreation(cross))
        self.wait()


class RoughTheorem(Scene):
    def construct(self):
        title = Title(r"\heiti 隐函数定理（大概？）", color=YELLOW, underline_color=YELLOW)
        theorem = VGroup(TexText("$F(x,y)=0$", r"局部", "确定了函数", "$y=y(x)$", "，且"),
                         Tex(r"{\d y \over \d x}", r"=-{F'_x \over F'_y}")).arrange(DOWN).next_to(title, DOWN, buff=.5)
        partial = Tex(r"F'_x\coloneqq{\partial F\over\partial x}", color=BLUE).next_to(theorem[1], RIGHT, buff=1)
        issues = VGroup(*[TexText(i, color=YELLOW) for i in ["什么样的？", "哪儿？", "什么样的？"]])
        arrows = VGroup()
        for i, (issue, index) in enumerate(zip(issues, [0, 1, 3])):
            issue.next_to(theorem[0][index], DOWN, buff=1)
            if i > 0:
                issue.align_to(issues[0], DOWN)
            arrows.add(Arrow(theorem[0][index].get_bottom(), issue.get_top()).set_color(YELLOW))

        self.add(title)
        self.wait()
        self.play(Write(theorem[0]))
        self.wait()
        self.play(Write(theorem[1]))
        self.wait()
        self.play(Write(partial))
        self.wait()
        self.play(FadeOut(partial))
        self.wait()

        self.play(Indicate(theorem[1]))
        self.wait()

        # seems to be easy
        method = TexText(r"对$F\left(x,y(x)\right)$求导：", color=BLUE).next_to(theorem, DOWN, buff=.5)
        Fx = Tex(r"F'_x+F'_y\cdot y'=0", r"~\Longrightarrow~", r"y'=-{F'_x\over F'_y}", color=BLUE).next_to(method,
                                                                                                            DOWN)
        self.play(Write(method))
        self.wait()
        self.play(Write(Fx[0]))
        self.wait()
        self.play(Write(Fx[1:]))
        self.wait()

        box1 = SurroundingRectangle(theorem[1][0])
        box2 = SurroundingRectangle(theorem[0][-2])
        local_box = SurroundingRectangle(theorem[0][1])
        self.play(ShowCreation(box1))
        self.wait()
        self.play(ShowCreation(box2))
        self.wait()
        self.play(FadeOut(VGroup(method, Fx)))
        self.play(ShowCreation(local_box), FadeOut(VGroup(box1, box2)))
        self.wait()

        # draw the circle
        axes = Axes(
            x_range=[-1.5, 1.5],
            y_range=[-1.5, 1.5],
            axis_config={"include_tip": True, "include_ticks": False},
            height=5,
            width=5
        ).to_corner(DL)
        circle = Circle(radius=axes.x_axis.get_unit_size(), color=RED).move_to(axes.get_origin())
        self.play(FadeIn(axes), ShowCreation(circle))
        circle_label = Tex("x^2+y^2=1", color=RED).scale(.8).next_to(circle, UL, buff=-.4).shift(UP * .6 + RIGHT)
        F_label = Tex("F(x,y)=x^2+y^2-1", color=RED).next_to(axes, buff=1)
        self.play(Write(circle_label))
        self.wait()
        self.play(Write(F_label))
        self.wait()

        # locally
        point1 = Dot(axes.c2p(np.cos(PI / 3), np.sin(PI / 3))).set_color(YELLOW)
        point0 = Dot(axes.c2p(-1, 0)).set_color(YELLOW)
        point00 = Dot(axes.c2p(1, 0)).set_color(BLUE)
        self.play(FadeIn(point1, scale=.5))
        self.wait()
        graph1 = axes.get_graph(lambda t: np.sqrt(1 - t ** 2), x_range=[0.3, 0.7], color=YELLOW)
        graph0 = axes.get_graph(lambda t: np.sqrt(1 - t ** 2), x_range=[-0.3, 0.3], color=YELLOW) \
            .rotate(angle=PI / 2, about_point=axes.get_origin())
        line = Line(axes.c2p(-0.97, -np.sqrt(1 - 0.97 ** 2)), axes.c2p(-0.97, np.sqrt(1 - 0.97 ** 2)),
                    color=BLUE).set_stroke(width=3)
        self.play(GrowFromCenter(graph1))
        self.wait()

        # but not every point
        self.play(FadeIn(point0, scale=0.5))
        self.wait()
        self.play(GrowFromCenter(graph0))
        self.wait()

        frame = self.camera.frame
        frame.save_state()
        self.play(frame.animate.move_to(point0.get_center() + RIGHT * .5).scale(.2), run_time=2)
        self.play(GrowFromCenter(line))
        self.wait()
        self.play(Restore(frame), run_time=2)
        self.play(FadeOut(line))

        # partial y
        Fynot0 = Tex(r"F'_y\neq0", color=BLUE).next_to(theorem[1][-1][-2:], buff=1)
        arrow = Arrow(Fynot0.get_left(), theorem[1][-1][-2:].get_right(), color=BLUE)
        self.play(FadeIn(Fynot0, LEFT), GrowArrow(arrow))
        self.wait()

        Fy = Tex("F'_y=2y", color=BLUE).next_to(F_label, DOWN, aligned_edge=LEFT)
        Fyis0 = Tex(r"F'_y(\pm1,0)=0", color=BLUE).next_to(Fy, DOWN, aligned_edge=LEFT)
        self.play(Write(Fy))
        self.wait()

        self.play(FadeToColor(VGroup(graph0, point0), BLUE))
        self.play(FadeIn(point00))
        self.play(Write(Fyis0))
        self.wait()

        self.play(FadeOut(
            VGroup(
                axes, circle, circle_label, point0, point1, point00, graph1, graph0,
                F_label, Fy, Fyis0,
                arrow, Fynot0,
                local_box
            )
        ))
        self.play(theorem[1].animate.shift(DOWN * 2))
        self.wait()

        # conditions
        for issue, arrow in zip(issues, arrows):
            self.play(FadeIn(issue, UP), GrowArrow(arrow))
            self.wait()


class Theorem(Scene):
    def construct(self):
        boxes = VGroup()
        m = {"x_0": RED, "F": BLUE}
        title = TexText("\\underline{\\heiti 隐函数定理}", color=YELLOW).to_corner(UL)
        self.add(title)
        pre = Tex(r"F\colon D\to\R, ~ D\subset\R^2", r"\text{ 是开集}", color=BLUE).scale(.8).align_to(title, DOWN)
        self.play(Write(pre))
        arrow = Arrow(ORIGIN, UP).set_color(BLUE).next_to(pre[-1], DOWN)
        self.wait()
        self.play(GrowArrow(arrow))
        self.wait()
        self.play(FadeOut(arrow))
        self.wait()

        # conditions
        conditions = VGroup(
            Tex(r"(1)~", "F", r"\in C^1(D)"),
            Tex(r"(2)~", "F", "(x_0,y_0)", r"=0,\text{ 其中 }", "(x_0,y_0)", r"\in D").tm(m),
            Tex(r"(3)~", r"F'_y", "(x_0,y_0)", r"\neq0").tm(m)
        ).arrange(DOWN, aligned_edge=LEFT, buff=.3).next_to(pre, DOWN, buff=.3, aligned_edge=LEFT)

        boxes.add(
            SurroundingRectangle(conditions[1][2][1:3]),
            SurroundingRectangle(conditions[1][-2][1:3]),
            SurroundingRectangle(conditions[2][2][1:3]),
        )
        comments = VGroup(
            TexText("（光滑）").next_to(conditions[0], LEFT, buff=.8),
            TexText("（上面有个点）").next_to(conditions[1], LEFT),
            TexText("（偏导的要求）").next_to(conditions[2], LEFT)
        ).set_color(YELLOW)
        comments[1].align_to(comments[0], RIGHT)
        comments[2].align_to(comments[0], RIGHT)

        self.play(Write(conditions[0]))
        self.wait()
        self.play(Write(comments[0]))
        self.wait()
        self.play(Write(conditions[1]))
        self.wait()
        self.play(Write(comments[1]))
        self.wait()
        self.play(Write(conditions[2]))
        self.wait()
        self.play(Write(comments[2]))
        self.wait()

        # longbar = DashedLine(color=GREEN).set_width(FRAME_WIDTH).next_to(comments, DOWN, buff=.3).set_x(0)
        # self.play(GrowFromCenter(longbar))
        # self.wait()

        local = TexText(r"那么存在一个包含$(x_0,y_0)$的开矩形，$I\times J\subset D$，使得：", color=BLUE) \
            .scale(.8).next_to(conditions, DOWN, buff=.7).set_x(1.5)
        # self.add(Debug(local[0]))
        boxes.add(SurroundingRectangle(local[0][9:11]))
        local_label = TexText("（局部）", color=YELLOW).next_to(local, LEFT, buff=.8).align_to(comments, LEFT)
        self.play(Write(local))
        self.wait()
        self.play(Write(local_label))
        self.wait()

        conclusions = VGroup(
            TexText(r"(1)~给定$x\in I$, $F(x,y)=0$确定唯一$f(x)\in J$"),
            TexText(r"(2)~$y_0=f(x_0)$"),
            TexText(r"(3)~$f\in C^1(I)$, 且$f'(x)=-{F_x'\over F_y'}$"),
        ).arrange(DOWN, aligned_edge=LEFT).next_to(local, DOWN, aligned_edge=LEFT)
        # self.add(Debug(conclusions[0][0]),Debug(conclusions[1][0]),Debug(conclusions[2][0]))
        boxes.add(
            SurroundingRectangle(conclusions[0][0][5]),
            SurroundingRectangle(conclusions[0][0][11]),
            SurroundingRectangle(conclusions[0][0][23]),
            SurroundingRectangle(conclusions[1][0][8:10]),
            # SurroundingRectangle(conclusions[2][0][15]),
        )

        comments2 = VGroup(
            TexText("（存在性）", color=YELLOW).next_to(conclusions[0], LEFT).align_to(local_label, LEFT),
            TexText("（过点）", color=YELLOW).next_to(conclusions[1], LEFT),
            TexText("（连续可导）", color=YELLOW).next_to(conclusions[2], LEFT)
        )
        comments2[1].align_to(local_label, LEFT)
        comments2[2].align_to(local_label, LEFT)

        for conclusion, comment in zip(conclusions, comments2):
            self.play(Write(conclusion))
            self.wait()
            self.play(Write(comment))
            self.wait()

        Rn = Tex("\\R^{n+1}", color=YELLOW).next_to(conditions[0], buff=.5)
        self.play(Write(Rn))
        self.wait()
        partial = Tex(r"{\partial f\over \partial x_i}=-{F'_{x_i}\over F'_y}", color=YELLOW)\
            .next_to(conclusions[2], buff=.5)
        self.play(ShowCreation(boxes))
        self.wait()
        self.play(Write(partial))
        self.wait()


class CircleInterpretation(Scene):
    def construct(self):
        axes = Axes(
            x_range=[-1.5, 1.5, 1],
            y_range=[-1.5, 1.5, 1],
            height=8,
            axis_config={"include_ticks": False},
            width=8,
        )
        # circle = Circle(radius=, color=BLUE)
        # f_always(circle.move_to, lambda:)
        circle = always_redraw(lambda: Circle(
            arc_center=axes.get_origin(),
            radius=(axes.c2p(1, 0) - axes.c2p(0, 0))[0],
            color=BLUE)
                               )
        self.add(axes, circle)

        F = Tex("F(x,y)=x^2+y^2-1", color=BLUE).to_corner(UL)
        self.play(Write(F))
        self.wait()

        point = Dot(color=RED)
        f_always(point.move_to, lambda: axes.c2p(np.cos(PI / 3), np.sin(PI / 3)))
        point_label = Tex("(x_0,y_0)", color=point.get_color())
        always(point_label.next_to, point)
        self.play(FadeIn(point, scale=.5))
        self.play(Write(point_label))
        self.wait()

        rect = DashedRectangle(dash_length=0.15, width=1.5).move_to(point)
        # always(rect.move_to, point)
        self.play(ShowCreation(rect))
        self.wait()

        # print(axes.p2c(point))

        # graph =
        graph = axes.get_graph(
            lambda t: np.sqrt(1 - t ** 2),
            x_range=[
                np.cos(PI / 3) - (rect.get_width() / 2) / axes.x_axis.unit_size,
                np.cos(PI / 3) + (rect.get_width() / 2) / axes.x_axis.unit_size,
                ],
            color=YELLOW
        )
        self.play(ShowCreation(graph))
        self.wait()
        # graph.add_updater(lambda t: t.become(axes.get_graph(
        #     lambda t: np.sqrt(1 - t ** 2),
        #     x_range=[
        #         np.cos(PI / 3) - (rect.get_width() / 2) / axes.x_axis.unit_size,
        #         np.cos(PI / 3) + (rect.get_width() / 2) / axes.x_axis.unit_size,
        #     ],
        #     color=YELLOW
        # )))
        graph_label = Tex("y=f(x)", color=graph.get_color())
        passing = Tex("f(x_0)=y_0", color=graph.get_color())
        derivative = Tex("f'(x)", r"=-{F'_x\over F'_y}", color=graph.get_color())
        result = Tex(r"=-{x\over y}", color=graph.get_color())
        v = VGroup(graph_label, passing, derivative, result) \
            .arrange(DOWN, aligned_edge=LEFT).next_to(F, DOWN, buff=.5, aligned_edge=LEFT)
        result.align_to(derivative[-1], LEFT)

        for i in v:
            self.play(Write(i))
            self.wait()

        self.play(
            FadeOut(VGroup(F, v, rect, graph)),
            axes.animate.shift(DOWN * 3 + LEFT * 5), run_time=2
        )
        self.wait()

        # ====== proof start =========
        assume = TexText("不妨设", "$F'_y(x_0,y_0)>0$", r"~$\Longrightarrow$~", "邻域内", "$F'_y(x,y)>0$", ".") \
            .tm({"x_0": RED, "(x,y)": BLUE}).to_edge(UP).shift(LEFT)
        IJ_ = DashedRectangle(dash_length=0.15).move_to(point)
        self.play(Write(assume[:2]))
        self.wait()
        self.play(Write(assume[2:4]), ShowCreation(IJ_))
        self.wait()
        self.play(Write(assume[4:]))
        self.wait()

        # we have to shrink the I interval
        arrow = Arrow(ORIGIN, UP * 2).set_color(GREEN).next_to(IJ_, DOWN).shift(RIGHT * 1.5)
        self.play(GrowArrow(arrow))
        self.wait()
        self.play(FadeOut(arrow))
        self.wait()

        # increasing w.r.t y
        increasing_y = Arrow(ORIGIN, IJ_.get_height() * UP, buff=0).set_color(YELLOW).next_to(IJ_, buff=.5)
        increasing_ylabel = TexText("$F(x,y)$关于$y$递增", color=YELLOW).next_to(increasing_y)
        self.play(GrowArrow(increasing_y))
        self.wait()
        self.play(Write(increasing_ylabel))
        self.wait()

        # setting x to x_0
        passing = Line(ORIGIN, IJ_.get_height() * UP, color=YELLOW).move_to(point)
        self.play(ShowCreation(passing))
        self.wait()

        # closed interval [c,d]\in J
        dline = Line(ORIGIN, IJ_.get_width() * RIGHT).move_to(IJ_[0])
        dlabel = Tex("d").next_to(dline, LEFT)
        cline = Line(ORIGIN, IJ_.get_width() * RIGHT).move_to(IJ_[2])
        clabel = Tex("c").next_to(cline, LEFT)
        self.play(FadeTransform(IJ_[2], cline))
        self.play(Write(clabel))
        self.wait()
        self.play(FadeTransform(IJ_[0], dline))
        self.play(Write(dlabel))
        self.wait()

        # F(x_0, c) and F(x_0, d)
        F_point_label = Tex("F(x_0,y_0)=0", color=RED).scale(.7).next_to(point).add_background_rectangle()
        cpoint = Dot(passing.get_start(), color=BLUE)
        cpoint_label = Tex("F(x_0,c)<0", color=BLUE).next_to(cpoint, DOWN).add_background_rectangle()
        cinterval_label = Tex("F(x,c)<0", color=YELLOW).next_to(cpoint, DOWN).add_background_rectangle()
        dpoint = Dot(passing.get_end(), color=BLUE)
        dpoint_label = Tex("F(x_0,d)>0", color=BLUE).next_to(dpoint, UP).add_background_rectangle()
        dinterval_label = Tex("F(x,d)>0", color=YELLOW).next_to(dpoint, UP).add_background_rectangle()
        self.play(FadeTransform(point_label, F_point_label))
        self.wait()
        self.play(GrowFromCenter(cpoint), Write(cpoint_label))
        self.wait()
        self.play(GrowFromCenter(dpoint), Write(dpoint_label))
        self.wait()

        # continuous w.r.t x
        continuous_x = Arrow(ORIGIN, IJ_.get_width() * RIGHT, buff=0).set_color(YELLOW).next_to(IJ_, buff=2)
        continuous_x_label = TexText("$F(x,y)$关于$x$连续", color=YELLOW).next_to(continuous_x, DOWN)
        self.play(
            FadeOut(increasing_y),
            FadeOut(increasing_ylabel),
            FadeTransform(F_point_label, point_label)
        )
        self.play(GrowArrow(continuous_x))
        self.wait()
        self.play(Write(continuous_x_label))
        self.wait()

        # from point to open interval
        self.play(FadeToColor(VGroup(cpoint, cpoint_label[1]), YELLOW))
        copen = VGroup(Tex("("), Tex(")")).set_color(YELLOW).arrange(buff=1).move_to(cpoint)
        dopen = VGroup(Tex("("), Tex(")")).set_color(YELLOW).arrange(buff=1.5).move_to(dpoint)
        self.wait()
        self.play(FadeIn(copen))
        self.wait()

        self.play(FadeToColor(VGroup(dpoint, dpoint_label[1]), YELLOW))
        self.play(FadeIn(dopen))
        self.wait()

        IJ = DashedRectangle(dash_length=0.15, width=copen.get_width()).set_color(YELLOW).move_to(point)
        self.play(FadeIn(IJ))
        self.wait()
        self.play(FadeOut(VGroup(copen, dopen, passing, cpoint, dpoint)))
        self.play(
            FadeOut(VGroup(IJ_[1], IJ_[3], cline, dline))
        )
        self.wait()

        self.play(
            FadeTransform(cpoint_label, cinterval_label),
            FadeTransform(dpoint_label, dinterval_label),
        )
        self.play(FadeOut(VGroup(point, point_label, continuous_x, continuous_x_label)))
        zero = TexText("零点定理", "、严格单调", color=YELLOW).move_to(continuous_x)
        self.wait()
        self.play(Write(zero[0]))
        self.wait()

        # fix x
        xval = ValueTracker(np.cos(PI / 3))
        xmin = np.cos(PI / 3) - (IJ.get_width() / 2) / axes.x_axis.unit_size
        xmax = np.cos(PI / 3) + (IJ.get_width() / 2) / axes.x_axis.unit_size
        passing.set_color(WHITE)
        f_always(passing.set_x, lambda: axes.c2p(xval.get_value(), 0)[0])
        self.play(ShowCreation(passing))
        self.wait()
        dot = point.copy().set_color(YELLOW)
        self.play(GrowFromCenter(dot))
        self.wait()
        self.play(Write(zero[1]))
        self.wait()
        self.remove(dot)
        xval.set_value(xmin + 0.01)
        graph_part = axes.get_graph(np.cos)
        graph_part.add_updater(lambda m: m.become(
            axes.get_graph(
                lambda t: np.sqrt(1 - t ** 2),
                x_range=[xmin, xval.get_value(), 0.01],
                color=YELLOW,
                use_smoothing=False
            )
        ))
        self.add(graph_part)
        self.play(xval.animate.set_value(xmax - 1e-3), run_time=3)
        self.play(FadeOut(passing))
        self.wait()

        # locally exists
        local = TexText("$y=f(x)$局部存在，", "且满足$y_0=f(x_0)$.").next_to(assume, DOWN, aligned_edge=LEFT)
        self.play(Write(local[0]))
        self.wait()
        self.play(FadeIn(VGroup(point, point_label)))
        self.wait()
        self.play(Write(local[1]))
        self.wait()

        # what we want next
        self.play(FadeOut(VGroup(
            cinterval_label, dinterval_label, zero,
            clabel, dlabel
        )))
        IJlabel = VGroup(
            Tex("I").next_to(IJ, DOWN),
            Tex("J").next_to(IJ, LEFT)
        ).set_color(YELLOW)
        self.play(Write(IJlabel))
        self.wait()
        differentiable = TexText("还需证$f(x)$在$I$上有连续的导函数", "，且", "$f'(x)=-{F'_x\\over F'_y}$.") \
            .next_to(local, DOWN, aligned_edge=LEFT)
        self.play(Write(differentiable[0]))
        self.wait()
        self.play(Write(differentiable[1:]))
        self.wait()

        # only need the second part
        self.play(FadeToColor(differentiable[-1], YELLOW))
        FxyContinuous = VGroup(
            TexText("连续").scale(.7).next_to(differentiable[-1], UP).shift(RIGHT),
            TexText("连续，非零").scale(.7).next_to(differentiable[-1], DOWN).shift(RIGHT)
        )  # .arrange(DOWN, aligned_edge=LEFT).next_to(differentiable)
        self.wait()
        self.play(Write(FxyContinuous[0]))
        self.wait()
        self.play(Write(FxyContinuous[1]))
        self.wait()

        # scene transformation
        self.play(FadeOut(FxyContinuous),
                  FadeOut(VGroup(IJ, IJlabel)))
        self.play(axes.animate.shift(LEFT * 3 + DOWN * 5.5).scale(3),
                  VGroup(assume, local, differentiable).animate.shift(UP * 2),
                  run_time=2)
        self.wait()

        # continuous
        continuous = TexText("先证", "$f(x)$在$I$连续", "：").next_to(differentiable, DOWN, aligned_edge=LEFT)
        self.play(Write(continuous))
        self.wait()

        # two steps
        cont_at_x0 = TexText(r"\textbullet~$f$在$x_0$处连续：", "收缩$x$范围.")
        cont_at_x1 = TexText(r"\textbullet~$f$在$x_1\in I$处连续：", "存在$g$在$x_1$处连续", "，而$g=f$.")
        VGroup(cont_at_x0, cont_at_x1) \
            .arrange(DOWN, aligned_edge=LEFT) \
            .next_to(continuous, DOWN, aligned_edge=LEFT).shift(RIGHT)
        VGroup(cont_at_x0[0], cont_at_x1[0]).set_color(BLUE)
        VGroup(cont_at_x0[1:], cont_at_x1[1:]).set_color(YELLOW)
        self.play(Write(cont_at_x0[0]))
        self.wait()
        self.play(Write(cont_at_x1[0]))
        self.wait()

        # at x_0
        IJ_2 = DashedRectangle(dash_length=0.15, height=1.2).move_to(point)
        IJ2 = DashedRectangle(dash_length=0.15, height=1.2, width=1).move_to(point).set_color(RED)
        cont_def = Tex("|x-x_0|<\\delta", "~\\Longrightarrow~", "|f(x)-y_0|<\\varepsilon", color=YELLOW) \
            .next_to(cont_at_x0[0])
        self.play(Write(cont_def))
        self.wait()
        self.play(ShowCreation(IJ_2))
        self.wait()
        self.play(RT(IJ_2.copy(), IJ2), FadeOut(point_label))
        self.wait()

        self.play(cont_def[-1].animate.next_to(IJ_2, buff=.5), run_time=2)
        self.wait()
        self.play(cont_def[0].animate.next_to(IJ2, DOWN), FadeOut(cont_def[1]), run_time=2)
        self.wait()

        self.play(Write(cont_at_x0[1:]))
        self.wait()

        self.play(
            FadeOut(VGroup(
                IJ_2, IJ2, cont_def[0], cont_def[2]
            )),
            FadeIn(point_label))
        self.wait()

        # at x1
        point1 = Dot(axes.c2p(np.cos(.9), np.sin(.9)), color=PINK)
        point1_label = Tex("(x_1,y_1)", color=point1.get_color()).next_to(point1)
        self.play(FadeIn(VGroup(point1, point1_label), scale=0.5))
        self.wait()

        same_condition = VGroup(TexText("$F(x_1,y_1)=0$"),
                                TexText("$F'_y(x_1,y_1)>0$")) \
            .arrange(DOWN).next_to(point1_label, buff=1)
        self.play(Write(same_condition[0]))
        self.wait()
        self.play(Write(same_condition[1]))
        self.wait()

        self.play(FadeOut(VGroup(point, point_label)))
        self.wait()

        graph1 = axes.get_graph(
            lambda t: np.sqrt(1-t**2),
            x_range=[np.cos(.9)-.1, np.cos(.9)+.1, .01],
            use_smoothing=False,
            color=point1.get_color()
        )
        self.play(ShowCreation(graph1))
        self.wait()

        graph1_label = Tex("y=g(x)", color=point1.get_color()).next_to(graph1, LEFT).shift(DR+UP*.5)
        self.play(Write(graph1_label))
        self.wait()

        self.play(Indicate(cont_at_x0[0]))
        self.wait()
        self.play(Write(cont_at_x1[1]))
        self.wait()
        self.play(Write(cont_at_x1[2]))
        self.wait()

        self.play(FadeOut(VGroup(graph1, graph1_label)))
        self.wait()

        self.play(FadeOut(VGroup(point1, point1_label, same_condition)))
        self.wait()

        # derivative
        cm = {'k': RED, 'h': RED, 'right': WHITE, 'alpha': WHITE}
        point_x = Dot(axes.c2p(np.cos(1.2), np.sin(1.2)), color=WHITE)
        x_label = Tex("(x,","f(x)",")", color=point_x.get_color()).next_to(point_x)
        point_xh = Dot(axes.c2p(np.cos(0.9), np.sin(0.9)), color=WHITE)
        xh_label = Tex("\\left(x+","h",",","f(x+","h",")","\\right)").next_to(point_xh).tm(cm)
        xh_label2 = Tex("\\left(x+","h",",","f(x)","+","k","\\right)") \
            .next_to(point_xh).tm(cm)
        self.play(GrowFromCenter(point_x))
        self.play(Write(x_label))
        self.wait()

        self.play(GrowFromCenter(point_xh))
        self.play(Write(xh_label))
        self.wait()
        self.play(TransformMatchingTex(xh_label, xh_label2, key_map={"f(x+h)": "f(x)+k"}))
        self.wait()

        xh = Dot().set_x(point_x.get_x()).set_y(point_xh.get_y())
        vert = Line(point_x, xh.get_center(), color=RED)
        vert_label = Tex("k", color=RED).next_to(vert, LEFT)
        horizon = Line(point_xh, xh.get_center(), color=RED)
        horizon_label = Tex("h", color=RED).next_to(horizon, DOWN)
        self.play(ShowCreation(vert), ShowCreation(horizon))
        self.play(Write(vert_label), Write(horizon_label))
        self.wait()

        # formula begins
        derivative_def = Tex(r"\lim_{h\to0}{f(x+h)-f(x) \over h}", color=YELLOW).next_to(xh_label2, buff=.5).shift(UP)
        derivative_defk = Tex(r"\lim_{h\to0}",r"{k \over h}", color=YELLOW).move_to(derivative_def)
        self.play(Write(derivative_def))
        self.wait()
        self.play(TransformMatchingTex(derivative_def, derivative_defk))
        self.wait()

        self.play(derivative_defk.animate.to_corner(DL),
                  VGroup(differentiable, continuous, cont_at_x0, cont_at_x1).animate.shift(UP*3.3),
                  run_time=2)

        # Frechet
        self.wait()
        frechet = TexText(r"$F$可微：", ) \
            .next_to(cont_at_x1, DOWN).align_to(continuous, LEFT)
        frechet1 = Tex(
            r"F(x+h,y+k)-F(x,y)=F'_x h+F'_y k+o(\sqrt{h^2+k^2})",
        ) \
            .next_to(frechet, DOWN).set_x(0)
        hk20 = Tex("(h\\to0,k\\to0)", color=YELLOW).next_to(frechet1, DOWN, aligned_edge=RIGHT)
        frechet2 = Tex(
            r"F(x+h,y+k)-F(x,y)=F'_x h+F'_y k+\alpha h+\beta k",
        ).next_to(hk20, DOWN).set_x(0)
        ab20 = Tex("(h\\to0,k\\to0\\text{~时~}\\alpha\\to0, \\beta\\to0)", color=YELLOW)\
            .next_to(frechet2, DOWN).align_to(hk20, RIGHT)

        for i in [4,8,21,26]+list(range(30,37)):
            frechet1[0][i].set_color(RED)
        for i in [4,8,21,26, -1, -4]:
            frechet2[0][i].set_color(RED)
        self.play(Write(frechet))
        self.wait()
        self.play(Write(frechet1))
        self.wait()

        # self.add(Debug(frechet1[0]))
        self.play(Write(hk20))
        self.wait()

        self.play(RT(frechet1[0][:28].copy(), frechet2[0][:28]))
        self.wait()
        self.play(FadeTransform(frechet1[0][28:].copy(), frechet2[0][28:]))
        self.wait()

        self.play(Write(ab20))
        self.wait()

        self.play(FadeOut(VGroup(frechet1, hk20)), VGroup(frechet2, ab20).animate.shift(UP*1.6))
        # self.add(Debug(frechet2[0], scale=.5))
        self.wait()
        VGroup(frechet2[0][12:17], point_x, x_label).set_color(BLUE)
        self.play(Indicate(VGroup(frechet2[0][12:17], x_label), color=BLUE,),
                  # FadeToColor(frechet2[0][12:17], BLUE), FadeToColor(VGroup(point_x, x_label), BLUE)
                  )
        # self.play(FadeToColor(frechet2[0][12:17], BLUE), FadeToColor(VGroup(point_x, x_label), BLUE))
        self.wait()
        VGroup(frechet2[0][1:10], point_xh, xh_label2).set_color(BLUE)
        self.play(Indicate(VGroup(frechet2[0][1:10], xh_label2), color=BLUE,),
                  # FadeToColor(frechet2[0][1:10], BLUE), FadeToColor(VGroup(point_xh, xh_label2), BLUE)
                  )
        # self.play(FadeToColor(frechet2[0][1:10], BLUE), FadeToColor(VGroup(point_xh, xh_label2), BLUE))
        self.wait()

        zero = VGroup(
            Tex(r"0-0","=",r"F'_x ","h",r"+F'_y ",r"k",r"+\alpha ",r"h",r"+\beta",r" k").tm(cm),
            Tex(r"0","=",r"F'_x ","h",r"+F'_y ",r"k",r"+\alpha ",r"h",r"+\beta",r" k").tm(cm),
            Tex(r"0","=",r"F'_x ",r"+F'_y ",r"{k \over h}",r"+\alpha ",r"+\beta",r" {k \over h}").tm(cm),
                      )\
            .next_to(ab20, DOWN, buff=.5)
        for i in range(3):
            zero[i].align_to(frechet2, RIGHT)
        zero[0][0].set_color(BLUE)
        zero[1][0].set_color(BLUE)
        self.play(Write(zero[0]))
        self.wait()

        self.play(TransformMatchingTex(zero[0], zero[1], key_map={'0-0': '0'}))
        self.wait()

        # mention k
        k = VGroup(Tex("k=f(x+h)-f(x):"), TexText("$h\\to0$时$k\\to0$"))\
            .arrange(DOWN).set_color(YELLOW).next_to(zero, DOWN)
        ab202 = Tex("(h\\to0\\text{~时~}k\\to0, \\alpha\\to0, \\beta\\to0)", color=YELLOW) \
            .next_to(zero, DOWN).align_to(hk20, RIGHT)
        self.play(Write(k[0]))
        self.wait()
        self.play(Write(k[1:]))
        self.wait()
        self.play(FadeTransform(k, ab202))
        self.wait()

        # derive k/h
        self.play(TransformMatchingTex(zero[1], zero[2], key_map={'k': r'{k \over h}'}))
        self.wait()

        derivative_defk.generate_target()
        derivative_defk.target[1].set_color(RED)
        derivative_defk.target[0].set_color(WHITE)
        limk = VGroup(
            derivative_defk.target,
            Tex(r"=\lim_{h\to0}\left(-{F'_x+\alpha\over F'_y+\beta}\right)"),
            Tex(r"=-{F'_x\over F'_y}"),
        ).arrange().next_to(ab202, DOWN)
        self.play(FadeOut(VGroup(x_label, xh_label2)), MoveToTarget(derivative_defk))
        self.wait()
        self.play(Write(limk[1]))
        self.wait()
        self.play(Write(limk[2]))
        self.wait()

        fp = Tex("f'(x)").next_to(limk[1], LEFT)
        self.play(FadeTransform(derivative_defk, fp))
        self.wait()

        qed = TexText("Q.E.D.", color=YELLOW).to_corner(DR, buff=.5)
        self.play(Write(qed))
        self.wait()


class Multi(Scene):
    def construct(self):
        func = TexText(r"$\sin z-xyz=0$","局部确定了隐函数","$z=z(x,y).$").to_edge(UP)
        func[0].set_color(YELLOW)
        self.add(func)
        self.wait(2)

        zx = Tex(r"{\partial z\over\partial x}",r"=",r"-{F'_x\over F'_z}").next_to(func, DOWN, buff=1)
        res0 = Tex("=",r"-{-yz\over \cos z-xy}").next_to(zx, DOWN).align_to(zx[1], LEFT)
        res = Tex("=",r"{yz\over \cos z-xy}").next_to(res0, DOWN, aligned_edge=LEFT)
        zx[0].set_color(YELLOW)
        self.play(Write(zx))
        self.wait()
        self.play(Write(res0))
        self.wait()
        self.play(Write(res))
        self.wait()


class pic(Scene):
    def construct(self):
        axes = Axes(
            x_range=[-1.5, 1.5, 1],
            y_range=[-1.5, 1.5, 1],
            height=8,
            axis_config={"include_ticks": False},
            width=8,
        ).to_edge(LEFT, buff=-2)
        # circle = Circle(radius=, color=BLUE)
        # f_always(circle.move_to, lambda:)
        circle = always_redraw(lambda: Circle(
            arc_center=axes.get_origin(),
            radius=(axes.c2p(1, 0) - axes.c2p(0, 0))[0],
            color=BLUE,
            stroke_width=15
        ),
                               )
        point = Dot(color=RED)
        f_always(point.move_to, lambda: axes.c2p(np.cos(PI / 3), np.sin(PI / 3)))
        rect = DashedRectangle(dash_length=0.15, width=1.5).move_to(point)

        graph = axes.get_graph(
            lambda t: np.sqrt(1 - t ** 2),
            x_range=[
                np.cos(PI / 3) - (rect.get_width() / 2) / axes.x_axis.unit_size,
                np.cos(PI / 3) + (rect.get_width() / 2) / axes.x_axis.unit_size,
            ],
            color=YELLOW,
            stroke_width=15
        )

        implicit = VGroup(TexText("\\heiti 隐函数").scale(3),
                          Tex(r"{\d y\over\d x}=-{F'_x\over F'_y}", color=YELLOW).scale(3))\
            .arrange(DOWN, buff=.5).to_edge(RIGHT, buff=1)
        self.add(axes, circle, rect, graph, implicit)
