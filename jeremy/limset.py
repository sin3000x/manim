#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author: Jeremy
@file:limset.py
@time:2021/06/04
"""
from manimlib import *

LMID = -FRAME_X_RADIUS / 2
RMID = FRAME_X_RADIUS / 2


class Test(Scene):
    def construct(self):
        r = Rectangle(width=1, height=5)
        c = Circle(radius=2)
        # side = r.get_edges()[1]
        # self.add(side)
        #
        # points = np.array([np.ones(10)*side.get_x(),np.linspace(side.get_bottom()[1], side.get_top()[1], 10), np.zeros(10)]).T
        # # points = side.get_all_points()
        # print(points)
        self.add(r, c)

        inter = Intersection_ThinRectCircle(r, c, color=YELLOW, fill_color=YELLOW)
        inter.set_opacity(1)
        self.add(inter)


class SetScene(Scene):
    def construct(self):
        sets = A, B = VGroup(Circle(), Circle()).arrange(buff=-1)
        self.add(sets)
        self.wait()

        inter = Intersection_2circle(A, B, color=BLACK, fill_color=YELLOW)
        inter.set_opacity(.8)

        union = sets.copy().set_color(YELLOW).set_opacity(1)

        whole = FullScreenRectangle(fill_color=YELLOW).set_opacity(.8)
        whole = Rectangle(width=1).set_height(inter.get_height())
        self.play(FadeIn(union))
        self.wait()
        self.play(FadeTransform(union, whole))

        # intersect = self.get_intersections_between_two_vmobs(A,B)
        # for point in intersect:
        #     self.add(Dot(radius=0.05, color=YELLOW).move_to(point))


class Opening(Scene):
    def construct(self):
        vert = Line(UP, DOWN).set_height(FRAME_HEIGHT)
        self.add(vert)

        # compare numbers
        numbers = VGroup(
            Tex('-1'), Tex('<'), Tex('2')
        ).arrange(buff=.5).set_x(LMID).to_edge(UP, buff=.5).set_color(YELLOW)
        numbers[1].shift(DOWN * 0).set_color(WHITE)  # nudge < down a little?
        num_underline = Underline(numbers[1], color=YELLOW).stretch(2.3, 0)
        numberline = NumberLine(
            x_range=[-3, 3, 1],
            include_tip=True,
            include_numbers=True
        ).next_to(numbers, DOWN, buff=2)
        dots = VGroup(Dot(numberline.n2p(-1), color=YELLOW), Dot(numberline.n2p(2), color=YELLOW))
        self.play(Write(numbers[0]), Write(numbers[2]), Write(num_underline), ShowCreation(numberline))
        self.play(RT(numbers[0].copy(), dots[0]), RT(numbers[2].copy(), dots[1]))
        self.play(Write(numbers[1]))
        self.wait()

        # compare sets
        sets = VGroup(
            Tex(r'\{0,1\}'), Tex(r'?'), Tex(r'\{1,2\}')
        ).arrange(buff=.5).set_x(RMID).to_edge(UP, buff=.5).set_color(YELLOW)
        singleton = Tex(r"\{1\}", color=YELLOW).move_to(sets[0]).align_to(sets[0], RIGHT)
        subset = Tex(r"\subseteq").move_to(sets[1])
        sets[1].set_color(WHITE)
        set_underline = Underline(sets[1], color=YELLOW).stretch(4, 0)
        A, B = circles = VGroup(Circle(), Circle()).arrange(buff=-1).next_to(sets, DOWN, buff=1).set_color(WHITE)
        A_label, B_label = labels = VGroup(Tex("A").move_to(A).shift(LEFT * .5),
                                           Tex("B").move_to(B).shift(RIGHT * .5)).set_color(YELLOW)
        self.play(Write(sets[0]), Write(sets[2]), Write(set_underline), ShowCreation(circles), Write(labels))
        self.play(Write(sets[1]))
        self.wait()

        # subset
        to_move = [A, B, A_label, B_label]
        for i in to_move:
            i.generate_target()
        A.target.scale(.8)
        B.target.scale(1.5)
        VGroup(A.target, B.target).set_x(RMID)
        A.target.move_to(B.target).shift(LEFT * .3)
        A_label.target.move_to(A.target)
        B_label.target.shift(RIGHT * .2)
        animations = [MoveToTarget(i) for i in to_move]
        self.play(*animations, TransformMatchingTex(sets[0], singleton), TransformMatchingTex(sets[1], subset))
        self.wait()

        # # remark
        # remark = TexText("$\\subseteq$: 包含于，\\\\$\\subset$: 真包含于").scale(1.1).next_to(B, DOWN, buff=.5)
        # self.play(Write(remark), run_time=2)
        # self.wait()

        ############## sup part ###############
        ### numbers
        # add some dots
        self.play(numberline.animate.set_y(0), FadeOut(dots))
        np.random.seed(1)
        n_points = VGroup(
            *[Dot(numberline.n2p(i)) for i in np.random.random(9) * (-3)], Dot(numberline.n2p(0.5))
        ).set_color(YELLOW)
        lm = min([numberline.p2n(d.get_x()) for d in n_points])
        # print(lm)
        for d in n_points:
            self.add(d)
            self.wait(.1)
        self.wait()

        # upper bound and sup
        upper = Line(UP, DOWN, color=RED).set_stroke(width=8).move_to(numberline.n2p(.5))
        self.play(ShowCreation(upper))
        self.wait()
        self.play(upper.animate.move_to(numberline.n2p(2.8)))
        self.wait()
        self.play(upper.animate.move_to(numberline.n2p(.5)))
        self.wait()

        sup_label = Tex(r"\sup_{1\leqslant i\leqslant n}a_i", color=RED).next_to(upper, DOWN)
        self.play(Write(sup_label))
        self.wait()

        ### sets
        self.play(FadeOut(VGroup(
            circles, labels,  # remark
        )))
        n_sets = VGroup(
            Circle(color=YELLOW, fill_color=RED),
            Circle(arc_center=[-.5, -1, 0], color=YELLOW, fill_color=RED),
            Circle(arc_center=[.5, -1, 0], color=YELLOW, fill_color=RED)
        ).move_to([RMID, 0.5, 0])
        self.play(ShowCreation(n_sets))
        self.wait()
        union = n_sets.copy().set_stroke(width=0).set_opacity(1)
        self.play(FadeIn(union))
        self.wait()

        whole = FullScreenRectangle(fill_color=RED).set_width(FRAME_X_RADIUS, stretch=True).set_x(RMID).set_opacity(.7)
        self.play(FadeTransform(union, whole))
        self.wait()
        self.play(FadeTransform(whole, union))
        self.wait()

        self.play(union.animate.set_opacity(.8))
        union_label = Tex(r"\bigcup_{i=1}^n A_i", color=RED).next_to(union, DOWN)
        self.play(Write(union_label))
        self.wait()

        ############## inf part ###############
        ### numbers
        self.play(FadeOut(VGroup(upper, sup_label)))
        self.wait()
        lower = Line(UP, DOWN, color=BLUE).set_stroke(width=8).move_to(numberline.n2p(lm))
        self.play(ShowCreation(lower))
        self.wait()
        self.play(lower.animate.move_to(numberline.n2p(-3)))
        self.wait()
        self.play(lower.animate.move_to(numberline.n2p(lm)))
        self.wait()

        inf_label = Tex(r"\inf_{1\leqslant i\leqslant n}a_i", color=BLUE).next_to(lower, DOWN)
        self.play(Write(inf_label))
        self.wait()

        ### sets
        self.play(FadeOut(union), FadeOut(union_label))
        self.wait()
        intersection = Intersection_n_circle(*n_sets, color=BLUE, fill_color=BLUE).set_opacity(1)
        self.play(FadeIn(intersection))
        self.wait()

        intersection.save_state()
        self.play(intersection.animate.scale(.01))
        self.wait()
        self.play(Restore(intersection))
        self.play(intersection.animate.set_opacity(.8))
        inter_label = Tex(r"\bigcap_{i=1}^n A_i", color=BLUE).next_to(union, DOWN)
        self.play(Write(inter_label))
        self.wait()

        ###### limit for monotonic sequences
        # number part
        self.play(FadeOut(VGroup(
            n_points, numberline, inf_label, lower
        )))

        increasing_dots = VGroup(
            *[Dot() for _ in range(10)]
        ).arrange(buff=.3).set_x(LMID)

        for i, d in enumerate(increasing_dots):
            d.shift(UP * (1 - 3 / (i + 1)))
            self.add(d)
            self.wait(.1)

        lim_sup = Line(color=RED).set_width(FRAME_X_RADIUS - 2).set_y(increasing_dots[-1].get_y() + 0.2).set_x(LMID)
        self.play(ShowCreation(lim_sup))

        lim_sup_label = Tex(r"\lim_{n\to\infty}a_n=\sup_{n\geqslant1}a_n", color=RED).next_to(lim_sup, UP)
        self.play(Write(lim_sup_label))
        self.wait()

        # set part
        self.play(FadeOut(VGroup(
            n_sets, intersection, inter_label
        )))
        self.wait()

        increasing_sets = VGroup(
            *[Circle(radius=(i + 1) / 3, color=WHITE, arc_center=(1 - i / 6) * LEFT, fill_color=RED) for i in range(5)]
        ).set_x(RMID)
        for s in increasing_sets:
            self.add(s)
            self.wait(.1)

        lim_union = increasing_sets[-1].copy().set_stroke(width=0).set_opacity(.8).scale(1.05)
        lim_inter = increasing_sets[0].copy().set_stroke(width=0).set_fill(color=BLUE).set_opacity(.8).scale(.8)
        lim_union_label = Tex(r"\lim_{n\to\infty}A_n=\bigcup_{n=1}^\infty A_n", color=RED).next_to(lim_union, DOWN)
        lim_inter_label = Tex(r"\lim_{n\to\infty}A_n=\bigcap_{n=1}^\infty A_n", color=BLUE).next_to(lim_union, DOWN)
        self.play(FadeIn(lim_union))
        self.play(Write(lim_union_label))
        self.wait()

        self.play(FadeOut(VGroup(
            lim_union, lim_union_label, increasing_sets
        )))
        self.wait()
        for s in reversed(increasing_sets):
            self.add(s)
            self.wait(.1)

        self.play(FadeIn(lim_inter))
        self.play(Write(lim_inter_label))
        self.wait()

        ### limsup and liminf
        # number part
        self.play(FadeOut(VGroup(
            increasing_dots, lim_sup, lim_sup_label
        )))
        self.wait()

        limsup = Tex(r"\varlimsup_{n\to\infty}a_n=\inf_{n\geqslant1}", r"\sup_{k\geqslant n}a_k", color=RED)
        liminf = Tex(r"\varliminf_{n\to\infty}a_n=\sup_{n\geqslant1}", r"\inf_{k\geqslant n}a_k", color=BLUE)
        limsup[-1].set_color(YELLOW)
        liminf[-1].set_color(YELLOW)
        VGroup(limsup, liminf).arrange(DOWN).set_x(LMID).shift(UP)
        frame = PictureInPictureFrame().set_x(LMID).to_edge(DOWN, buff=.5)
        self.play(ShowCreation(frame))
        self.wait()

        self.play(Write(limsup))
        self.wait()

        self.play(Write(liminf))
        self.wait()

        brace = Brace(limsup[-1], UP)
        decrease = TexText("递减的").scale(0.8).next_to(brace, UP)
        self.play(GrowFromCenter(VGroup(brace, decrease)))
        self.wait()

        # set part
        self.play(FadeOut(VGroup(
            increasing_sets, lim_inter, lim_inter_label
        )))
        self.wait()

        limsup_set = Tex(r"\varlimsup_{n\to\infty}A_n=\bigcap_{n=1}^\infty", r"\bigcup_{k=n}^\infty A_k", color=RED)
        liminf_set = Tex(r"\varliminf_{n\to\infty}A_n=\bigcup_{n=1}^\infty", r"\bigcap_{k=n}^\infty A_k", color=BLUE)
        limsup_set[-1].set_color(YELLOW)
        liminf_set[-1].set_color(YELLOW)
        VGroup(limsup_set, liminf_set).arrange(DOWN).set_x(RMID).shift(UP)
        self.play(Write(limsup_set))
        self.play(Write(liminf_set))
        self.wait()

        # converge
        equal = Tex(r"\text{若}\varlimsup_{n\to\infty}A_n=\varliminf_{n\to\infty}A_n,")
        lim = Tex(r"\text{可记}\lim_{n\to\infty}A_n.")
        VGroup(equal, lim).arrange(DOWN).next_to(liminf_set, DOWN, buff=.5)
        self.play(Write(equal))
        self.wait()
        self.play(Write(lim))
        self.wait()


class Example1(Scene):
    def construct(self):
        An = Tex(r"""
        A_n=
        \begin{cases}
        (-\frac 1n,1] &n\text{ 为奇}\\
        (-1,\frac 1n] &n\text{ 为偶}
        \end{cases}
        """)

        limsup = Tex(r"\varlimsup_{n\to\infty}A_n=(-1,1]", color=RED)
        liminf = Tex(r"\varliminf_{n\to\infty}A_n=\{0\}", color=BLUE)
        VGroup(An, VGroup(limsup, liminf).arrange(DOWN, aligned_edge=LEFT)).arrange(buff=1).to_edge(UP)

        limsup_calc = Tex(r"\varlimsup_{n\to\infty}A_n=\bigcap_{n=1}^\infty", r"\bigcup_{k=n}^\infty A_k",
                          r"=\bigcap_{n=1}^\infty", "(-1,1]",
                          r"=(-1, 1]", color=RED)
        liminf_calc = Tex(r"\varliminf_{n\to\infty}A_n=\bigcup_{n=1}^\infty", r"\bigcap_{k=n}^\infty A_k",
                          r"=\bigcup_{n=1}^\infty", r"\{0\}",
                          r"=\{0\}", color=BLUE)
        VGroup(limsup_calc[1], limsup_calc[3], liminf_calc[1], liminf_calc[3]).set_color(YELLOW)
        limsup_calc.next_to(An, DOWN).set_x(0)
        liminf_calc.next_to(An, DOWN).set_x(0)
        # self.add(limsup_calc)
        self.play(Write(An))
        self.wait()

        # draw the bars
        intervals = []
        N = 10
        for n in range(1, N + 1):
            if n % 2 == 0:
                intervals.append((-1, 1 / n))
            else:
                intervals.append((-1 / n, 1))

        chart = IntervalChart(
            intervals,
            bar_names=[f"A_{{{i}}}" for i in range(1, N + 1)],
            width=10, height=1.5, depth=1.5,
            bar_colors=[BLUE, GREEN],
        ).to_edge(DOWN)
        self.play(ShowCreation(chart.axes), Write(chart.y_axis_labels), run_time=1)
        animations = []
        for bar, bottom in zip(chart.bars, chart.bottoms):
            animations.append(DrawBorderThenFill(bar))
            animations.append(ShowCreation(bottom))
            # self.bring_to_front(bottom)

        self.play(AnimationGroup(*animations, lag_ratio=.1), run_time=3)
        self.play(Write(chart.bar_labels))
        self.wait()

        # calculate
        self.play(Write(limsup_calc[:2]))
        self.wait()

        # limsup: change color
        for bar in chart.bars:
            bar.save_state()
        chart.bottoms.add_updater(lambda m: self.bring_to_front(m))
        self.play(FadeToColor(chart.bars, YELLOW))
        for bar in chart.bars[:-1]:
            self.play(Restore(bar), run_time=.5)
        # self.bring_to_front(chart.bottoms)

        self.play(Write(limsup_calc[2:4]), Restore(chart.bars[-1]))
        self.wait()
        self.play(Write(limsup_calc[4:]))
        self.wait()

        self.play(Write(limsup))
        self.wait()
        self.play(FadeOut(limsup_calc))
        self.wait()

        # liminf
        self.play(Write(liminf_calc[:2]))

        upperline = chart.x_axis.copy().set_color(YELLOW).set_y(chart.bars[1].get_edges()[0].get_y())
        lowerline = chart.x_axis.copy().set_color(YELLOW).set_y(chart.bars[2].get_edges()[2].get_y())
        self.play(ShowCreation(upperline), ShowCreation(lowerline))
        self.wait()
        self.play(upperline.animate.move_to(chart.x_axis), lowerline.animate.move_to(chart.x_axis), run_time=2)
        self.wait()

        self.play(Write(liminf_calc[2:4]))
        self.wait()
        self.play(Write(liminf_calc[4:]))
        self.wait()
        self.play(Write(liminf))
        self.wait()
        self.play(FadeOut(liminf_calc))
        self.wait()

        # relationship
        contain = Tex(r"\varliminf_{n\to\infty}A_n", r"\subseteq", r"\varlimsup_{n\to\infty}A_n") \
            .tm({"liminf": BLUE, "sup": RED, "subset": YELLOW})
        leq = Tex(r"\varliminf_{n\to\infty}a_n", r"\leqslant", r"\varlimsup_{n\to\infty}a_n") \
            .tm({"liminf": BLUE, "sup": RED, "leq": YELLOW})
        VGroup(contain, leq).arrange(buff=1).move_to(limsup_calc)
        self.play(Write(contain))
        self.wait()
        self.play(Write(leq))
        self.wait()

        # using proposition
        self.play(FadeOut(VGroup(lowerline, upperline)))
        self.wait()
        upperline.save_state()
        upperline.shift(UP*.2)
        self.play(ShowCreation(upperline))
        self.wait()

        self.play(upperline.animate.set_y(chart.bars[0].get_top()[1]))
        self.play(upperline.animate.set_y(chart.bars[0].get_bottom()[1]+.05), run_time=2)
        self.wait()

        self.play(Restore(upperline))
        self.wait()


class Example2(Scene):
    def construct(self):
        An = Tex(r"""
        A_n=
        \begin{cases}
        (-\frac 1n,1+\frac1n] &n\text{ 为奇}\\
        (\frac1n,1-\frac 1n] &n\text{ 为偶}
        \end{cases}
        """)

        # definitions and calculations
        limsup = Tex(r"\varlimsup_{n\to\infty}A_n=[0,1]", color=RED)
        liminf = Tex(r"\varliminf_{n\to\infty}A_n=(0,1)", color=BLUE)
        VGroup(An, VGroup(limsup, liminf).arrange(DOWN, aligned_edge=LEFT)).arrange(buff=1).to_edge(UP)

        limsup_calc = Tex(r"\varlimsup_{n\to\infty}A_n=\bigcap_{n=1}^\infty", r"\bigcup_{k=n}^\infty A_k",
                          r"=\bigcap_{n=1}^\infty", r"\left(-{1\over 2n-1},1+{1\over 2n-1}\right]",
                          r"=[0,1]", color=RED)
        liminf_calc = Tex(r"\varliminf_{n\to\infty}A_n=\bigcup_{n=1}^\infty", r"\bigcap_{k=n}^\infty A_k",
                          r"=\bigcup_{n=1}^\infty", r"\left({1\over2n},1-{1\over 2n}\right]",
                          r"=(0,1)", color=BLUE)
        VGroup(limsup_calc[1], limsup_calc[3], liminf_calc[1], liminf_calc[3]).set_color(YELLOW)
        limsup_calc.next_to(An, DOWN).set_x(0)
        liminf_calc.next_to(An, DOWN).set_x(0)
        self.play(Write(An))
        self.wait()

        # draw bars
        intervals = []
        N = 10
        for n in range(1, N + 1):
            if n % 2 == 0:
                if n == 2:
                    intervals.append((1 / 2, 1 / 2 + .05))
                else:
                    intervals.append((1 / n, 1 - 1 / n))
            else:
                intervals.append((-1 / n, 1 + 1 / n))
        # print(intervals)

        chart = IntervalChart(
            intervals,
            bar_names=[f"A_{{{i}}}" for i in range(1, N + 1)],
            width=10, height=2, depth=1,
            max_value=2,
            min_value=-1,
            n_ticks=3,
            bar_colors=[BLUE, GREEN],
        ).to_edge(DOWN)
        self.play(ShowCreation(chart.axes), Write(chart.y_axis_labels), run_time=1)
        animations = []
        for bar, bottom in zip(chart.bars, chart.bottoms):
            animations.append(DrawBorderThenFill(bar))
            animations.append(ShowCreation(bottom))
            # self.bring_to_front(bottom)

        self.play(AnimationGroup(*animations, lag_ratio=.1), run_time=3)
        self.play(Write(chart.bar_labels))
        self.wait()

        self.play(Write(limsup_calc[:2]))
        self.wait()

        # limsup: change color
        for bar in chart.bars:
            bar.save_state()
        chart.bottoms.add_updater(lambda m: self.bring_to_front(m))
        self.play(FadeToColor(chart.bars, YELLOW))
        self.wait()
        arrow = Arrow(ORIGIN, DOWN).set_color(YELLOW).next_to(chart.bars[0], UP)
        self.play(GrowArrow(arrow))

        odd = VGroup(chart.bars[0])
        for i, bar in enumerate(chart.bars):
            if (i > 0) and i % 2 == 0:
                self.play(arrow.animate.next_to(bar, UP), run_time=.5)
                self.wait(.5)
                if i<N-2:
                    self.play(Restore(bar), run_time=.5)
                else:
                    self.play(Restore(bar), FadeOut(arrow), run_time=.5)
                odd.add(bar)
            else:
                self.wait(.5)
                self.play(Restore(bar), run_time=.5)


        # self.bring_to_front(chart.bottoms)
        self.play(FadeToColor(odd, YELLOW))
        self.wait()
        self.play(Write(limsup_calc[2:4]))
        self.wait()
        self.play(Write(limsup_calc[4:]))
        self.wait()

        self.play(Write(limsup))
        self.wait()
        self.play(*[Restore(i) for i in odd], FadeOut(limsup_calc))
        self.wait()

        # liminf
        self.play(Write(liminf_calc[:2]))
        self.wait()
        self.play(FadeToColor(chart.bars, YELLOW))
        self.wait()
        arrow = Arrow(ORIGIN, DOWN).set_color(YELLOW).next_to(chart.bars[1], UP)

        even = VGroup(chart.bars[1])
        self.play(Restore(chart.bars[0]))
        self.wait(.5)
        self.play(GrowArrow(arrow))
        for i, bar in enumerate(chart.bars):
            if i % 2 == 1 and i > 1:
                self.play(arrow.animate.next_to(bar, UP), run_time=.5)
                self.wait(0.5)
                if i<N-1:
                    self.play(Restore(bar), run_time=.5)
                else:
                    self.play(Restore(bar), FadeOut(arrow), run_time=.5)
                even.add(bar)
            else:
                self.wait(.5)
                self.play(Restore(bar), run_time=.5)

        # self.bring_to_front(chart.bottoms)
        self.play(FadeToColor(even, YELLOW))
        self.wait()
        self.play(Write(liminf_calc[2:4]))
        self.wait()
        self.play(Write(liminf_calc[4:]))
        self.wait()

        self.play(Write(liminf))
        self.wait()
        self.play(FadeOut(liminf_calc))
        self.play(*[Restore(i) for i in even])
        self.wait()

        # using proposition
        line = chart.x_axis.copy().set_color(YELLOW)
        lower = line.copy().set_color(RED).shift(UP*.3)
        self.play(line.animate.shift(UP*chart.y_unit), run_time=2)
        self.wait()
        self.play(line.animate.shift(DOWN*chart.y_unit))
        self.play(line.animate.shift(UP*chart.y_unit))
        self.wait()
        self.play(ShowCreation(lower))
        self.wait()
        self.play(line.copy().animate.shift(DOWN*chart.y_unit), FadeOut(lower))
        self.wait()


class Prop(Scene):
    def construct(self):
        m = {"limsup": RED, "liminf": BLUE}
        sup = Tex(r"\varlimsup_{n\to\infty}A_n", "=", r"\{\textbf{\heiti 频繁}\text{出现的元素}\}").tm(m)
        sup[2][1:3].set_color(RED)
        supdef = Tex("=", r"\{x\colon \forall j\in\mathbb{N},\exists n\geqslant j,\text{ s.t. }x\in A_n\}")
        supdef[1].set_color(RED)
        inf = Tex(r"\varliminf_{n\to\infty}A_n", "=", r"\{\textbf{\heiti 最终}\text{出现的元素}\}").tm(m)
        inf[2][1:3].set_color(BLUE)
        infdef = Tex("=", r"\{x\colon\exists j_0\in\mathbb{N},n\geqslant j_0~\Longrightarrow~ x\in A_n\}")
        infdef[1].set_color(BLUE)
        VGroup(
            VGroup(sup, supdef).arrange(DOWN),
            VGroup(inf, infdef).arrange(DOWN)
        ).arrange(DOWN, buff=2).shift(LEFT+UP*.5)
        supdef.align_to(sup[1], LEFT)
        infdef.align_to(inf[1], LEFT)
        # self.add(Debug(sup[2]))

        for i in [sup, supdef, inf, infdef]:
            self.play(Write(i))
            self.wait()

        supex = Tex(r"1,-1,1,-1,1,-1,\cdots", color=YELLOW).next_to(supdef, DOWN, buff=.5).set_x(0)
        infex = Tex(r"2,3,3,3,3,3,\cdots", color=YELLOW).next_to(infdef, DOWN, buff=.5).set_x(0)
        self.play(Write(supex))
        self.wait()
        self.play(Write(infex))
        self.wait()


class ByTurns(Scene):
    def construct(self):
        w, h, r = .5, 3, 1
        rect_c, circ_c = BLUE, RED
        Sequence = VGroup(
            Rectangle(width=w, height=h, fill_color=rect_c, color=rect_c),
            Circle(radius=r, fill_color=circ_c, color=circ_c),
            Rectangle(width=w, height=h, fill_color=rect_c, color=rect_c),
            Circle(radius=r, fill_color=circ_c, color=circ_c),
            Rectangle(width=w, height=h, fill_color=rect_c, color=rect_c),
            Circle(radius=r, fill_color=circ_c, color=circ_c),
            Rectangle(width=w, height=h, fill_color=rect_c, color=rect_c),
            Tex(r"\cdots")
        ).arrange(buff=.5).to_edge(UP)
        for s in Sequence:
            s.set_opacity(.8)
            self.play(DrawBorderThenFill(s))

        limsup = Tex(r"\varlimsup A_n", "=")
        liminf = Tex(r"\varliminf A_n", "=")
        VGroup(limsup[0], liminf[0]).set_color(YELLOW)
        group = VGroup(
            Rectangle(width=w, height=h, fill_color=YELLOW, color=YELLOW).set_opacity(1),
            Circle(radius=r, fill_color=YELLOW, color=YELLOW).set_opacity(1),
        )
        group2 = VGroup(
            Rectangle(width=w, height=h, fill_color=rect_c, color=rect_c),
            Circle(radius=r, fill_color=circ_c, color=circ_c),
        )
        VGroup(
            VGroup(limsup, group).arrange(),
            VGroup(liminf, group2).arrange()
        ).arrange(buff=2).next_to(Sequence, DOWN, buff=1)
        intersection = Intersection_ThinRectCircle(group2[0], group2[1], color=YELLOW, fill_color=YELLOW).set_opacity(1)
        self.play(Write(limsup))
        self.wait()
        self.play(FadeIn(group))
        self.wait()

        self.play(Write(liminf))
        self.wait()
        self.play(ShowCreation(group2))
        self.play(FadeIn(intersection))
        self.wait()


class Pic(Scene):
    def construct(self):
        increasing_sets = VGroup(
            *[Circle(radius=(i + 1) / 3, color=WHITE, arc_center=(1 - i / 6) * LEFT, fill_color=YELLOW) for i in range(5)]
        ).scale(1.5)
        lim_inter_label = Tex(r"\lim_{n\to\infty} A_n", color=YELLOW).scale(3)
        title = Text("上下限集", color=WHITE).scale(2).to_edge(UP)

        for i,s in enumerate(increasing_sets):
            s.fade(i/5)

        # lim_union = increasing_sets[-1].copy().set_stroke(width=0).set_opacity(.8).scale(1.05)
        VGroup(increasing_sets, lim_inter_label).arrange(buff=1).shift(DOWN*.7)
        # lim_inter = increasing_sets[0].copy()\
        #     .set_stroke(width=0).set_fill(color=BLUE).set_opacity(.8).scale(.8).set_color(YELLOW)
        # lim_union_label = Tex(r"\lim_{n\to\infty}A_n=\bigcup_{n=1}^\infty A_n", color=RED).next_to(lim_union, DOWN)

        self.add(increasing_sets, lim_inter_label, title)
        # VGroup(lim_inter, lim_inter_label).set_color(YELLOW)

        # self.play(FadeIn(lim_inter))
        self.play(Write(lim_inter_label))