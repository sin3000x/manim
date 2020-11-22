from manimlib.imports import *


class limsup(PiCreatureScene):
    CONFIG = {"upper": BLUE, "middle": RED, "lower": GREEN,"color_map": {r"\sup": BLUE, r"k\geq": BLUE, "a_k": BLUE},
              "color_map_down": {r"\inf": GREEN, r"k\geq": GREEN, "a_k": GREEN},
              "color_map_limit": {"limsup": BLUE, "liminf": GREEN,"大": BLUE,"小": GREEN}}

    def construct(self):
        self.opening()
        self.limit_points()
        self.lim_sup()
        self.closing()

    def opening(self):
        # three convergent sequences
        you = self.pi_creature
        self.remove(you)
        self.N = N = 20
        a1, a2, a3 = [lambda n: 2 / n, lambda n: (1 + 1 / n) ** n, lambda n: np.sin(n) / n]
        self.a3 = lambda n: np.sin(n) / n

        dots_1 = VGroup(*[Dot() for n in range(1, N + 1)]).arrange(RIGHT, buff=MED_LARGE_BUFF).shift(DOWN)
        dots_2 = VGroup(*[Dot() for n in range(1, N + 1)]).arrange(RIGHT, buff=MED_LARGE_BUFF).shift(DOWN * 2)
        dots_3 = VGroup(*[Dot() for n in range(1, N + 1)]).arrange(RIGHT, buff=MED_LARGE_BUFF).shift(DOWN)
        self.dots_3 = VGroup(*[Dot() for n in range(1, N + 1)]).arrange(RIGHT, buff=MED_LARGE_BUFF).shift(DOWN)
        self.dots = dots_ex = VGroup(*[Dot() for n in range(1, N + 1)]).arrange(RIGHT, buff=MED_LARGE_BUFF)
        self.unbounded = dots_unbounded = VGroup(*[Dot() for n in range(1, N + 1)]).arrange(RIGHT,
                                                                                            buff=MED_LARGE_BUFF).to_edge(
            DOWN)

        label1, label2, label3 = [TexMobject("a_n", "=", i) for i in
                                  [r"{1\over n}", r"\left(1+\frac 1n\right)^n", r"{{\sin n} \over n}"]]
        VGroup(label1, label2, label3).to_edge(DOWN)
        self.limits = limits = VGroup(*[DashedLine(color=YELLOW).set_width(FRAME_WIDTH - 2) for _ in range(3)]).shift(
            DOWN)
        for n, dot in enumerate(dots_1):
            dot.shift(UP * a1(n + 1) * 4.5)

        for n, dot in enumerate(dots_2):
            dot.shift(UP * a2(n + 1))
        limits[1].shift(UP * np.e + DOWN)

        for n, dot in enumerate(dots_3):
            dot.shift(UP * a3(n + 1) * 3)
        self.dots3 = dots_3

        limits_label = VGroup(TexMobject("0"), TexMobject("\\mathrm{e}"), TexMobject("0")).set_color(YELLOW).scale(1.2)
        for i, label, limit in zip(range(3), limits_label, limits):
            if i == 1:
                label.next_to(limit, UP).to_edge(RIGHT, buff=LARGE_BUFF)
            else:
                label.next_to(limit, DOWN).to_edge(RIGHT, buff=LARGE_BUFF)

        self.play(LaggedStartMap(ShowCreation, dots_1))
        self.play(Write(label1))
        # self.wait()
        self.play(ShowCreation(limits[0]))
        self.play(Write(limits_label[0]))

        self.wait()
        self.remove(limits[0], limits_label[0])
        self.play(ReplacementTransform(dots_1, dots_2), ReplacementTransform(label1, label2))
        self.play(ShowCreation(limits[1]))
        self.play(Write(limits_label[1]))
        self.wait()

        self.remove(limits[1], limits_label[1])
        self.play(ReplacementTransform(dots_2, dots_3), ReplacementTransform(label2, label3))
        self.play(ShowCreation(limits[2]))
        self.play(Write(limits_label[2]))
        self.wait()

        # prop
        prop = TextMobject("{\\kaishu 任何子列都收敛到相同极限.}", color=YELLOW).to_edge(TOP)
        sub_sequence_index = [2 * i for i in range(N // 2)]
        sub_dots = []
        # sub_sequence_index2 = sorted(np.random.choice(N, 10, replace=False))
        # sub_dots2 = []
        dots_3c = dots_3.copy().set_color(GREEN)
        for i in sub_sequence_index:
            sub_dots.append(dots_3[i].get_center())
            self.play(GrowFromCenter(dots_3[i], rate_func=lambda t: smooth(1 - t)), run_time=.2)
            self.play(GrowFromCenter(dots_3c[i]), run_time=.2)
            dots_3[i].become(dots_3c[i])
            self.remove(dots_3c[i])
        sub_dots.append(limits[-1].get_right())
        graph = SmoothGraphFromSetPoints(sub_dots, color=GREEN)
        # self.play(dots_3[i].set_color, GREEN)
        self.play(ShowCreation(graph), Write(prop), run_time=2)
        self.wait(2)

        # for i in sub_sequence_index2:
        #     self.play(dots_3[i].set_color, BLUE)
        #     sub_dots2.append(dots_3[i].get_center())
        # graph2 = SmoothGraphFromSetPoints(sub_dots2, color=BLUE)
        # self.play(ShowCreation(graph2))

        # an example
        def ex(n):
            if n % 3 == 1:
                return 1 + 1 / n
            elif n % 3 == 2:
                return 0
            else:
                return -1 - 1 / n

        def ub(n):
            if n % 2 == 1:
                return 0
            if n % 2 == 0:
                return n / 3

        for n, dot in enumerate(dots_ex):
            dot.shift(UP * ex(n + 1))

        for n, dot in enumerate(dots_unbounded):
            dot.shift(UP * ub(n + 1))

        self.remove(limits[-1], limits_label[-1], graph)
        self.play(FadeOut(VGroup(prop, label3)), ReplacementTransform(dots_3, dots_ex))
        # pi creature
        bubble = you.get_bubble(height=3, width=6)
        question = TextMobject("{\\kaishu 不同子列有不同极限？}")
        bubble.position_mobject_inside(question)
        self.play(FadeIn(you))
        self.play(ShowCreation(bubble))
        self.play(Write(question))
        self.wait(4)

        self.play(FadeOut(VGroup(you, bubble, question)))

    def limit_points(self):
        dots, N, unbounded_dots = self.dots, self.N, self.unbounded
        upper_dots = VGroup(*[dots[i] for i in range(N) if i % 3 == 0])
        middle_dots = VGroup(*[dots[i] for i in range(N) if i % 3 == 1])
        lower_dots = VGroup(*[dots[i] for i in range(N) if i % 3 == 2])

        unbounded_sub = VGroup(*[unbounded_dots[i] for i in range(N) if i % 2 == 1])

        # def update_upper(d):
        #     d.set_color(self.upper)
        #     return d
        #
        # def update_lower(d):
        #     d.set_color(self.lower)
        #     return d

        # upper_coords = [dot.get_center() for dot in upper_dots]
        # upper_coords.append(upper_dots[-1].get_right())
        # upper_graph = SmoothGraphFromSetPoints(upper_coords, color=self.upper)
        # self.play(ShowCreation(upper_graph))
        upper_limit = DashedLine(color=self.upper).set_width(FRAME_WIDTH - 2).shift(UP)
        middle_limit = DashedLine(color=self.middle).set_width(FRAME_WIDTH - 2)
        lower_limit = DashedLine(color=self.lower).set_width(FRAME_WIDTH - 2).shift(DOWN)

        upper_label = TextMobject("{\\kaishu 上极限}", color=self.upper).next_to(upper_limit, UP).to_edge(RIGHT,
                                                                                                       buff=LARGE_BUFF)
        lower_label = TextMobject("{\\kaishu 下极限}", color=self.lower).next_to(lower_limit, DOWN).to_edge(RIGHT,
                                                                                                         buff=LARGE_BUFF)
        limit_point_labels = VGroup(*[TextMobject("{\\kaishu 极限点}") for i in range(3)])
        limit_point_labels[0].move_to(upper_label)
        limit_point_labels[2].move_to(lower_label)
        limit_point_labels[1].next_to(middle_limit, UP).to_edge(RIGHT, buff=LARGE_BUFF)
        # self.play(AnimationGroup(*[ApplyFunction(update_upper,dot) for dot in upper_dots], lag_ratio=.6))
        # for dot in upper_dots:
        #     Indicate(dot, color=self.upper)
        #     dot.set_color(self.upper)
        # animations = it.chain(*[[Indicate(dot, color=self.upper), ApplyFunction(update_upper, dot)] for dot in upper_dots])
        # print(list(animations))
        # self.play(AnimationGroup(*animations, lag_ratio=.6))

        # upper limit
        for dot in upper_dots:
            dot.set_color(self.upper)
            self.play(Indicate(dot, color=self.upper, scale_factor=1.5), run_time=.6)
        self.play(ShowCreation(upper_limit))
        self.wait()
        self.play(Write(upper_label))

        # lower limit
        self.wait()
        for dot in lower_dots:
            dot.set_color(self.lower)
            self.play(Indicate(dot, color=self.lower, scale_factor=1.5), run_time=.6)
        self.play(ShowCreation(lower_limit))
        self.wait()
        self.play(Write(lower_label))
        self.wait(2)

        # extra: unbounded
        self.remove(dots)
        self.play(FadeOut(VGroup(upper_limit, upper_label, lower_limit, lower_label)),
                  ReplacementTransform(dots.copy(), unbounded_dots))
        self.wait()
        self.play(unbounded_sub.set_color, self.upper)
        unbounded_label = TextMobject(r"{\kaishu 上极限}", "$=+\infty$", color=self.upper).to_edge(UP).shift(DOWN)
        self.play(Write(unbounded_label))
        self.wait(2)
        self.play(ReplacementTransform(unbounded_dots, dots), ReplacementTransform(unbounded_label, upper_label),
                  FadeIn(VGroup(upper_limit, lower_label, lower_limit)))
        self.wait()

        # limit points and def
        for dot in middle_dots:
            dot.set_color(self.middle)
            self.play(Indicate(dot, color=self.middle, scale_factor=1.5), run_time=.6)
        self.play(ShowCreation(middle_limit))
        self.wait(2)

        self.play(Write(limit_point_labels[1]), ReplacementTransform(upper_label, limit_point_labels[0]),
                  ReplacementTransform(lower_label, limit_point_labels[2]))
        self.wait()

        E = TexMobject(r"\{ \text{{\kaishu 极限点}} \}").to_edge(TOP)
        # E = VGroup(Text("{", font=""),limit_point_labels[0].copy(), Brace(limit_point_labels[0], RIGHT)).arrange().to_edge(TOP)
        lsup = TexMobject(r"\varlimsup_{n\to\infty} a_n", "=", r"\sup", r"\{ \text{{\kaishu 极限点}} \}").set_color_by_tex(
            "limsup", self.upper)
        lmax = TexMobject(r"\varlimsup_{n\to\infty} a_n", "=", r"\max", r"\{ \text{{\kaishu 极限点}} \}").set_color_by_tex(
            "limsup", self.upper)
        linf = TexMobject(r"\varliminf_{n\to\infty} a_n", "=", r"\inf", r"\{ \text{{\kaishu 极限点}} \}").set_color_by_tex(
            "liminf", self.lower)
        lmin = TexMobject(r"\varliminf_{n\to\infty} a_n", "=", r"\min", r"\{ \text{{\kaishu 极限点}} \}").set_color_by_tex(
            "liminf", self.lower)

        # lsup = TextMobject(r"$\varlimsup_{n\to\infty}$", "$=$", r"$\sup$", "$\\{$","{\\kaishu 极限点}","$\\}$").set_color_by_tex("limsup", self.upper)
        # linf = TextMobject(r"$\varliminf_{n\to\infty}$", "$=$", r"$\inf$", "$\\{$","{\\kaishu 极限点}","$\\}$").set_color_by_tex("limsup", self.lower)
        #
        lsup.next_to(E, DOWN)
        linf.move_to(lower_limit).align_to(lsup, LEFT)
        self.play(ReplacementTransform(limit_point_labels, E))
        # self.remove(upper_limit)
        self.play(ReplacementTransform(VGroup(upper_dots, upper_limit), lsup[2:]))
        self.play(Write(lsup[:2]))
        self.wait()

        self.play(FadeOut(VGroup(middle_dots, middle_limit)),
                  ReplacementTransform(VGroup(lower_dots, lower_limit), linf[2:]))
        self.play(Write(linf[:2]))
        self.wait()

        # to max and min
        # ma = TexMobject("\\max").move_to(lsup[2]).scale(.9)
        # mi = TexMobject("\\min").move_to(linf[2]).scale(.9)
        lmax.next_to(E, DOWN)
        lmin.move_to(linf).align_to(lmax, LEFT)
        self.play(ReplacementTransform(lsup, lmax))
        self.play(ReplacementTransform(linf, lmin))
        self.wait()

        # prop of limit
        dots3, limit3 = self.dots_3, self.limits[2]
        for n, dot in enumerate(dots3):
            dot.shift(UP * self.a3(n + 1) * 3)

        self.play(FadeOut(VGroup(lmax, lmin, E)), FadeIn(VGroup(dots3, limit3)))
        self.wait()
        pos = Line(color=RED).replace(limit3).shift(UP * 0.4)
        neg = Line(color=RED).replace(limit3).shift(DOWN * 0.4)
        self.play(ReplacementTransform(limit3.copy(), pos), ReplacementTransform(limit3.copy(), neg))
        self.wait()

        pos_label = TexMobject(r"\text{ {\kaishu {大于}} } a_n,", r"\text{ {\kaishu {当}} } n\gg 1").add_updater(lambda x: x.next_to(pos,
                                                                                                                                  UP).to_edge(
            RIGHT))
        neg_label = TexMobject(r"\text{ {\kaishu {小于}} } a_n,", r"\text{ {\kaishu {当}} } n\gg 1").add_updater(lambda x: x.next_to(neg,
                                                                                                                                  DOWN).to_edge(
            RIGHT))
        self.play(FocusOn(pos))
        self.play(Write(pos_label))
        self.wait()
        self.play(FocusOn(neg))
        self.play(Write(neg_label))
        self.wait(2)

        # generalize to upper&lower
        fresh_dots = self.dots3
        self.fresh = fresh_dots
        limit3c = limit3.copy()
        # upper_dots =
        self.play(ReplacementTransform(dots3, fresh_dots),
                  limit3c.shift, UP * (upper_limit.get_y() - limit3.get_y()), limit3.shift,
                  UP * (lower_limit.get_y() - limit3.get_y()),
                  pos.shift, UP * (upper_limit.get_y() - limit3.get_y()- [0,0.1,0]), neg.shift,
                  UP * (lower_limit.get_y() - limit3.get_y() + [0, 0.1, 0]))
        self.wait(3)
        pos_label.clear_updaters()
        neg_label.clear_updaters()


        sup_prop = VGroup(TexMobject("a^*",r"\in",r"\{ \text{{\kaishu {极限点}}} \}").set_color_by_tex("a^*", self.upper),
                          TexMobject("x>",r"a^*",r"~\Longrightarrow~","x>a_n",r"~(\text{{\kaishu 从某项}})").set_color_by_tex("a^*", self.upper)).arrange(DOWN, aligned_edge=LEFT)
        sup_brace = Brace(sup_prop, LEFT)
        sup_prop_label = TextMobject(r"{\kaishu 上极限}","$a^*$").set_color_by_tex("a^*", self.upper).next_to(sup_brace, LEFT)
        sup_v = VGroup(sup_prop, sup_brace, sup_prop_label)
        sup_v.set_x(0)
        sup_good = TextMobject("{\\kaishu 上极限是满足这两个性质的唯一数.}", color=YELLOW).next_to(sup_v, DOWN)


        inf_prop = VGroup(TexMobject("a_*",r"\in",r"\{ \text{{\kaishu {极限点}}} \}").set_color_by_tex("a_*", self.lower),
                          TexMobject("x<",r"a_*",r"~\Longrightarrow~","x<a_n",r"~(\text{{\kaishu 从某项}})").set_color_by_tex("a_*", self.lower)).arrange(DOWN, aligned_edge=LEFT)
        inf_brace = Brace(inf_prop, LEFT)
        inf_prop_label = TextMobject(r"{\kaishu 下极限}","$a_*$").set_color_by_tex("a_*", self.lower).next_to(inf_brace, LEFT)
        inf_v = VGroup(inf_prop, inf_brace, inf_prop_label)
        inf_v.set_x(0)
        inf_good = TextMobject("{\\kaishu 下极限是满足这两个性质的唯一数.}", color=YELLOW).next_to(inf_v, DOWN)

        VGroup(VGroup(sup_v, sup_good), VGroup(inf_v, inf_good)).arrange(DOWN, buff=LARGE_BUFF)

        self.play(FadeOut(VGroup(pos_label, neg_label, pos, neg, limit3c, limit3, fresh_dots)))
        self.play(Write(sup_prop_label), GrowFromCenter(sup_brace))
        self.wait()
        self.play(Write(sup_prop[0]))
        self.wait()
        self.play(Write(sup_prop[1]))
        self.wait()
        self.play(Write(sup_good))
        self.wait()


        self.play(Write(inf_prop_label), GrowFromCenter(inf_brace))
        self.wait()
        self.play(Write(inf_prop[0]))
        self.wait()
        self.play(Write(inf_prop[1]))
        self.wait()
        self.play(Write(inf_good))
        self.wait()

        self.play(FadeOut(sup_v),FadeOut(inf_v), FadeOut(VGroup(inf_good, sup_good)))

    def lim_sup(self):
        dots = self.fresh
        upper_dots = [dots[i] for i in range(self.N) if i%3==0]
        lower_dots = [dots[i] for i in range(self.N) if i%3==2]
        labels = VGroup(*[TexMobject(f"a_{{{i+1}}}") for i in range(self.N)])
        for label, dot in zip(labels, dots):
            label.next_to(dot, DOWN)
        self.play(FadeIn(dots))
        self.play(FadeIn(labels))
        self.wait()

        # all_xs = [dot.get_x() for dot in dots]
        # target_xs = [(all_xs[i]+all_xs[i+1])/2 for i in range(self.N-1)]
        target_ys = [dot.get_y() for dot in upper_dots]
        target_ys_down = [dot.get_y() for dot in lower_dots]
        # vline = Line(DOWN, UP, color=YELLOW).set_height(FRAME_HEIGHT-2).next_to(dots, LEFT, buff=MED_LARGE_BUFF/2).set_y(0)
        hline = DashedLine(color=self.upper).set_width(FRAME_WIDTH-1.5).set_y(target_ys[0])
        hlabel = TexMobject(r"\sup",r"\{ a_1,a_2,a_3,\cdots \}", color=self.upper).add_updater(lambda x: x.next_to(hline, UP))
        # self.play(GrowFromCenter(vline))
        self.wait()
        self.play(FadeIn(hline))
        self.play(Write(hlabel))
        self.wait()

        # self.play(vline.set_x, target_xs[0],VGroup(dots[0], labels[0]).fade, 0.6)
        self.play(Indicate(VGroup(dots[0], labels[0]), scale_factor=1.4), run_time=.6)
        self.play(VGroup(dots[0], labels[0]).fade, 0.6)
        self.wait()
        self.play(Transform(hlabel, TexMobject(r"\sup",r"\{ a_2,a_3,a_4,\cdots \}", color=self.upper).next_to(target_ys[1]*UP, UP)), hline.set_y, target_ys[1])
        self.wait()

        self.play(Indicate(VGroup(dots[1], labels[1]), scale_factor=1.4), run_time=.6)
        self.play(VGroup(dots[1], labels[1]).fade, 0.6)
        # self.play(vline.set_x, target_xs[1],VGroup(dots[1], labels[1]).fade, 0.6)
        self.wait()
        self.play(Transform(hlabel, TexMobject(r"\sup",r"\{ a_3,a_4,a_5,\cdots \}", color=self.upper).next_to(target_ys[1]*UP, UP)))
        self.wait()

        self.play(Indicate(VGroup(dots[2], labels[2]), scale_factor=1.4), run_time=.6)
        self.play(VGroup(dots[2], labels[2]).fade, 0.6)
        # self.play(vline.set_x, target_xs[1],VGroup(dots[1], labels[1]).fade, 0.6)
        self.wait()
        self.play(Transform(hlabel, TexMobject(r"\sup",r"\{ a_4,a_5,a_6,\cdots \}", color=self.upper).next_to(hline, UP)))
        self.wait()

        self.play(Transform(hlabel, TexMobject(r"\sup",r"_{k\geq 4}",r"\{ a_k \}", color=self.upper).next_to(hline, UP)))
        self.wait()

        delta_y = hlabel.get_y() - hline.get_y()
        for i in range(3, self.N-2):
            target_index = 2
            self.play(VGroup(dots[i], labels[i]).fade, 0.6, run_time=.3)
            if i%3 == 0:
                self.play(Transform(hlabel, TexMobject(r"\sup",fr"_{{k\geq {i+2}}}",r"\{ a_k \}", color=self.upper).set_y(target_ys[i//3]+delta_y)), hline.set_y, target_ys[i//3], run_time=.3)
                # target_index += 1
            else:
                self.play(Transform(hlabel, TexMobject(r"\sup", fr"_{{k\geq {i + 2}}}", r"\{ a_k \}", color=self.upper).move_to(hlabel)), run_time=.3)

        self.wait()
        self.play(Transform(hlabel, TexMobject(r"\sup", r"_{k\geq n}", r"\{ a_k \}", color=self.upper).move_to(hlabel)), run_time=1)
        self.wait(5)

        lim_sup = TexMobject(r"\lim_{n\to\infty}",r"\sup", r"_{k\geq n}", r"\{ a_k \}").set_color_by_tex_to_color_map(self.color_map).move_to(hlabel)
        infsup = TexMobject(r"\lim_{n\to\infty}",r"\sup", r"_{k\geq n}", r"\{ a_k \}","=",r"\inf_{n\geq 1}",r"\sup", r"_{k\geq n}", r"\{ a_k \}").set_color_by_tex_to_color_map(self.color_map).move_to(hlabel)
        limsup_def = TexMobject(r"\lim_{n\to\infty}",r"\sup", r"_{k\geq n}", r"\{ a_k \}","=",r"\limsup_{n\to\infty}","a_n").set_color_by_tex_to_color_map(self.color_map).move_to(hlabel)
        liminf_def = TexMobject(r"\lim_{n\to\infty}",r"\inf", r"_{k\geq n}", r"\{ a_k \}","=",r"\liminf_{n\to\infty}","a_n")
        for i in [1,2,3]:
            liminf_def[i].set_color(self.lower)
        self.play(ReplacementTransform(hlabel, lim_sup[1:]), )
        self.play(Write(lim_sup[0]))
        self.wait()
        self.play(ReplacementTransform(lim_sup, infsup[:4]), )
        self.play(Write(infsup[4:]))
        self.wait()
        self.play(ReplacementTransform(infsup[:5], limsup_def[:5]),ReplacementTransform(infsup[5:], limsup_def[5:]))
        self.wait()

        hline_down = DashedLine(color=self.lower).set_width(FRAME_WIDTH-1.5).set_y(target_ys_down[0])
        liminf_def.next_to(hline_down,DOWN, buff=SMALL_BUFF)
        bg = BackgroundRectangle(liminf_def)
        self.play(FadeIn(hline_down))
        for target in target_ys_down[1:]:
            self.play(hline_down.set_y, target)
        self.play(FadeIn(bg))
        self.play(Write(liminf_def))
        self.wait()

        limupper = TexMobject(r"\varlimsup_{n\to\infty} a_n").next_to(limsup_def[4], LEFT).shift(DOWN*.05)
        limlower = TexMobject(r"\varliminf_{n\to\infty} a_n").next_to(liminf_def[4], LEFT).shift(DOWN*.1)
        self.play(Transform(limsup_def[:4], limupper), Transform(liminf_def[:4], limlower))
        self.wait()

        self.remove(bg)
        self.play(FadeOut(VGroup(dots, hline, hline_down, limsup_def, liminf_def, labels)))

    def closing(self):
        you = self.pi_creature
        self.remove(you)
        leq = TexMobject(r"\varliminf_{n\to\infty}","a_n",r"\leq",r"\varlimsup_{n\to\infty}","a_n").set_color_by_tex_to_color_map(self.color_map_limit)
        eq = TexMobject(r"\varliminf_{n\to\infty}","a_n",r"=",r"\varlimsup_{n\to\infty}","a_n","=","a",
                        r"~\Longleftrightarrow~",r"\lim_{n\to\infty} a_n=a").set_color_by_tex_to_color_map(self.color_map_limit)
        v1 = VGroup(leq, eq).arrange(DOWN)

        pre = TexMobject("a_n",r"\leq","b_n",r"~(\text{{\kaishu 从某项}})")
        ineq_inf = TexMobject(r"\varliminf_{n\to\infty}","a_n",r"\leq", r"\varliminf_{n\to\infty}","b_n").set_color_by_tex_to_color_map(self.color_map_limit)
        ineq_sup = TexMobject(r"\varlimsup_{n\to\infty}","a_n",r"\leq", r"\varlimsup_{n\to\infty}","b_n").set_color_by_tex_to_color_map(self.color_map_limit)
        v2 = VGroup(pre, ineq_inf, ineq_sup).arrange(DOWN)

        VGroup(v1, v2).arrange(DOWN, buff=LARGE_BUFF)

        for prop in [leq, eq, pre, ineq_inf, ineq_sup]:
            self.play(Write(prop))
            self.wait()

        add_inf = TexMobject(r"\varliminf_{n\to\infty}","a_n","+",r"\varliminf_{n\to\infty}","b_n",
                             r"\leq",r"\varliminf_{n\to\infty}","(a_n+b_n)",
                             r"\leq",r"\varliminf_{n\to\infty}","a_n","+",r"\varlimsup_{n\to\infty}","b_n")\
            .set_color_by_tex_to_color_map(self.color_map_limit).move_to(leq)
        add_sup = TexMobject(r"\varliminf_{n\to\infty}","a_n","+",r"\varlimsup_{n\to\infty}","b_n",
                             r"\leq",r"\varlimsup_{n\to\infty}","(a_n+b_n)",
                             r"\leq",r"\varlimsup_{n\to\infty}","a_n","+",r"\varlimsup_{n\to\infty}","b_n")\
            .set_color_by_tex_to_color_map(self.color_map_limit).move_to(eq)

        pos_pre = TexMobject("a_n",",","b_n",r"~\text{{\kaishu 非负}}").move_to(pre)
        mul_inf = TexMobject(r"\varliminf_{n\to\infty}","a_n",r"\cdot",r"\varliminf_{n\to\infty}","b_n",
                             r"\leq",r"\varliminf_{n\to\infty}",r"(a_n \cdot b_n)",
                             r"\leq",r"\varliminf_{n\to\infty}","a_n",r"\cdot",r"\varlimsup_{n\to\infty}","b_n")\
            .set_color_by_tex_to_color_map(self.color_map_limit).move_to(ineq_inf)
        mul_sup = TexMobject(r"\varliminf_{n\to\infty}","a_n",r"\cdot",r"\varlimsup_{n\to\infty}","b_n",
                             r"\leq",r"\varlimsup_{n\to\infty}",r"(a_n \cdot b_n)",
                             r"\leq",r"\varlimsup_{n\to\infty}","a_n",r"\cdot",r"\varlimsup_{n\to\infty}","b_n")\
            .set_color_by_tex_to_color_map(self.color_map_limit).move_to(ineq_sup)

        self.play(ReplacementTransform(leq, add_inf), ReplacementTransform(eq, add_sup))
        self.wait()
        self.play(ReplacementTransform(pre, pos_pre), ReplacementTransform(ineq_inf, mul_inf), ReplacementTransform(ineq_sup, mul_sup))
        self.wait()


        lim_compre = TexMobject(r"\lim_{n\to\infty}","a_n",r"\colon","a_n",r"\text{{\kaishu 在无穷远处的值}}").set_color_by_tex_to_color_map(self.color_map_limit)
        limsup_compre = TexMobject(r"\varlimsup_{n\to\infty}","a_n",r"\colon","a_n",r"\text{{\kaishu 在无穷远处的}}",r"\text{{\kaishu 最大值}}").set_color_by_tex_to_color_map(self.color_map_limit)
        liminf_compre = TexMobject(r"\varliminf_{n\to\infty}","a_n",r"\colon","a_n",r"\text{{\kaishu 在无穷远处的}}",r"\text{{\kaishu 最小值}}").set_color_by_tex_to_color_map(self.color_map_limit)
        v3 = VGroup(limsup_compre, liminf_compre)
        v3.arrange(DOWN)
        VGroup(lim_compre, v3).arrange(DOWN, aligned_edge=LEFT).shift(RIGHT*.5)

        self.play(FadeOut(VGroup(add_inf, add_sup, pos_pre, mul_inf, mul_sup)), FadeIn(you))
        for lim in [lim_compre, limsup_compre, liminf_compre]:
            self.play(Write(lim))
            self.wait(2)




class test(Scene):
    def construct(self):
        a = TexMobject(r"\varlimsup_{n\to\infty}","a_n").scale(3)
        b = TexMobject(r"\limsup_{n\to\infty}","a_n")
        # bg = BackgroundRectangle(b)
        # VGroup(a,b).arrange(DOWN, buff=MED_LARGE_BUFF).scale(2)
        self.add(a)









