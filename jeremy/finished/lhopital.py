from manimlib.imports import *
from jeremy.ref.VideoProgressBar import VideoProgressBar


class main(Scene):
    CONFIG = {
        "map": {"f": RED, "g": BLUE, "infty": WHITE, "forall": WHITE,"frac": WHITE,"left":WHITE, "right": WHITE, "inf": WHITE},
        "infmap": {"limsup": RED, "liminf": GREEN}
    }

    def construct(self):
        self.opening()
        self.other_limit()
        self.remark1()
        self.remark2()
        self.remark3()

    def opening(self):
        self.title = title = TextMobject(r"\textbf{\underline{{\heiti l'H\^{o}pital法则}}}", color=YELLOW).to_corner(UL)
        title_00 = TextMobject(r"$\boldsymbol{\dfrac{0}{0}}$\textbf{{\heiti 型}}", color=YELLOW).move_to(title)
        title_inf = TextMobject(r"$\boldsymbol{\dfrac{*}{\infty}}$\textbf{{\heiti 型}}", color=YELLOW).move_to(title)
        title_limit = TextMobject(r"\textbf{{\heiti 上下极限}}", color=YELLOW).move_to(title)
        self.play(Write(title))
        self.wait()
        zero_zero = TexMobject(r"{0\over 0}")
        infty_infty = TexMobject(r"\infty", r" \over", r" \infty")
        star_infty = TexMobject(r"*", r"\over", r"\infty")
        VGroup(zero_zero, infty_infty, star_infty).scale(2.5)
        VGroup(zero_zero, infty_infty).arrange(buff=LARGE_BUFF * 3)
        star_infty.move_to(infty_infty)
        self.play(Write(zero_zero))
        self.wait()
        self.play(Write(infty_infty))
        self.wait()
        self.play(ReplacementTransform(infty_infty, star_infty))
        self.wait()

        zero_zero.generate_target()
        zero_zero.target.set_x(0).scale(4)
        zero_zero.target.fade(1)
        self.play(FadeOut(star_infty), MoveToTarget(zero_zero))

        t1 = TexMobject(*r"f , g \text{~在~}(a,b)\text{~上可导~}".split())
        t2 = TexMobject(*r"g '(x) \neq 0,\quad\forall x\in(a,b)".split())
        t3 = TexMobject(*r"\lim_{ x\to a^+} f (x) = \lim_{x\to "
        #    0    1    2   3  4  5     6
                         r"a^+} g (x) = 0".split())
        ###################  7  8  9 10 11
        t3_inf = TexMobject(*r"\lim_{x\to "
        #    0
                             r"a^+} g (x) = \infty".split()).set_color_by_tex_to_color_map(self.map)
        ###################  1  2  3  4    5
        t4 = TexMobject(*r"\lim_{ x\to a^+} {f '(x)\over g"
                         r" '(x)} \text{~存在，或为~}\infty".split())
        tmain = TexMobject(*r"\Longrightarrow \lim_{ x\to a^+} {f (x) "
        #       0            1    2     3  4   5
                            r"\over g (x)} = \lim_{ x\to a^+} {f '(x)\over g '(x)}".split())
        ######################  6   7  8   9   10
        v = VGroup(t1, t2, t3, t4, tmain).arrange(DOWN, buff=0.4).next_to(title, DOWN).set_x(0)
        t3_inf.move_to(t3)
        for t in v:
            t.set_color_by_tex_to_color_map(self.map)
        tmain[1:].set_x(0)
        tmain[0].next_to(tmain[1:], LEFT)
        tmp = tmain[1:].copy().scale(1.5).move_to(ORIGIN)
        box = SurroundingRectangle(tmain[1:], color=YELLOW)
        box1, box2 = SurroundingRectangle(tmp[2], buff=.05), SurroundingRectangle(tmp[11], buff=.05)
        # bg = BackgroundRectangle(tmain[1:], color=GOLD, fill_opacity=.15, buff=.1)
        question2 = TextMobject(r"{\kaishu 过分吗？}", color=YELLOW).move_to(t2).to_edge(LEFT)
        question4 = question2.copy().move_to(t4).to_edge(LEFT)
        # arrow2 = Arrow(question2.get_right(), t2.get_left())
        arrow4 = Arrow(question4.get_right(), t4.get_left(), color=YELLOW)
        arrow2 = arrow4.copy().set_y(t2.get_y())
        self.play(Write(tmp))
        self.wait()
        self.play(ShowCreation(box1), ShowCreation(box2))
        self.wait()
        self.play(FadeOut(VGroup(box1, box2)))
        self.play(ReplacementTransform(tmp, tmain[1:]))
        self.play(Write(tmain[0]))
        self.play(ShowCreation(box))
        # self.play(ReplacementTransform(box1, box), ReplacementTransform(box2, box))
        self.wait()
        self.play(ReplacementTransform(tmain[4:6].copy(), t3[3:5]),
                  ReplacementTransform(tmain[7:9].copy(), t3[8:10]),
                  Write(t3[:3]), Write(t3[5:8]), Write(t3[10:]), run_time=2)
        self.wait()
        self.play(ReplacementTransform(tmain[10:].copy(), t4[:7]))
        self.play(Write(t4[7:]), run_time=2)
        self.wait()
        self.play(GrowArrow(arrow4))
        self.wait()
        self.play(Write(t1))
        self.wait()
        self.play(ReplacementTransform(tmain[-2:].copy(), t2[:2]), run_time=2)
        self.play(Write(t2[2:]), run_time=2)
        self.wait()
        self.play(GrowArrow(arrow2))
        self.wait()
        t = tmain.deepcopy()
        self.play(FadeOut(VGroup(t1, t2, t3, t4, box, arrow2, arrow4, tmain[0])),
                  tmain[1:].move_to, t1, Transform(title, title_00),run_time=2)
        self.wait()

        # proving start
        number_line = NumberLine(x_min=-2, x_max=2, tick_frequency=4,
                                 leftmost_tick=-2, numbers_with_elongated_ticks=[-2, 2]) \
            .next_to(tmain[1:], DOWN, buff=MED_LARGE_BUFF)
        a, b = TexMobject("a"), TexMobject("b")
        a.next_to(number_line.get_left(), DOWN, buff=MED_LARGE_BUFF)
        b.next_to(number_line.get_right(), DOWN, buff=MED_LARGE_BUFF)
        a.align_to(b, DOWN)
        left_r, right_r = TexMobject("(", color=TEAL, stroke_width=3).scale(1.2).move_to(
            number_line.get_left()).align_to(number_line, LEFT), \
                          TexMobject(")", color=TEAL, stroke_width=3).scale(1.2).move_to(
                              number_line.get_right()).align_to(number_line, RIGHT)
        left_s, right_s = TexMobject("[", color=YELLOW, stroke_width=3).scale(1.2).move_to(
            number_line.n2p(-2)).align_to(number_line, LEFT), \
                          TexMobject("]", color=YELLOW, stroke_width=3).scale(1.2).move_to(number_line.n2p(1.5))
        xi = number_line.get_tick(.4)
        x_label, xi_label = TexMobject("x"), TexMobject(r"\xi")
        x_label.add_updater(lambda x: x.next_to(right_s, DOWN).align_to(b, DOWN))
        xi_label.add_updater(lambda x: x.next_to(xi, DOWN).align_to(b, DOWN))
        cauchy = TexMobject(*r"{f (x) \over g (x)} = {{f "
        #                       0   1    2   3  4   5   6
                             r"(x) - f (a)} \over {g"
        #                     7   8 9  10    11   12
                             r" (x) - g (a)}} = "
        #                       13  1415 16   17
                             r"{f '( \xi )\over g '( \xi )}".split()) \
            .set_color_by_tex_to_color_map(self.map).next_to(number_line, DOWN, buff=LARGE_BUFF*1.2)
        #                       18  19    20   21    22
        conclusion = TexMobject(*r"\lim_{ x \to a^+} {f (x) "
        #   0    1  2   3    4  5
                                 r"\over g (x)} = \lim_{ \xi \to a^+} {f '( \xi )\over g '( \xi )}"
                                #                            6   7   8  9   10    11  12  13  14 15  16 17     18 19 20 21
                                .split()).set_color_by_tex_to_color_map(self.map).next_to(cauchy, DOWN)
        conclusion2 = TexMobject(*r"\lim_{ x \to a^+} {f (x) "
        #   0    1  2   3    4  5
                                  r"\over g (x)} = \lim_{ x \to a^+} {f '( x )\over g '( x )}"
                                 #                            6   7   8  9   10    11  12  13  14 15  16 17     18 19 20 21
                                 .split()).set_color_by_tex_to_color_map(self.map).next_to(cauchy, DOWN)
        bg = BackgroundRoundedRectangle(VGroup(cauchy, conclusion2), buff=.3)
        r1 = TexMobject(r"f , g \text{{\kaishu ~在~}}[a,x]\text{{\kaishu ~上连续}}")
        r2 = TexMobject(r"(a,x)\text{{\kaishu ~上可导}}")
        r3 = TexMobject(r"g '(t)\neq0,~~\forall t\in(a,x)")
        v1 = VGroup(r1, r2, r3).arrange(DOWN).scale(.8).next_to(number_line, LEFT, buff=LARGE_BUFF)
        box2 = SurroundingRectangle(v1, color=PINK)
        self.play(FadeIn(bg), run_time=1.5)
        self.play(Write(cauchy[:6]))
        self.wait()
        self.play(ReplacementTransform(cauchy[:2].copy(), cauchy[6:8]),
                  ReplacementTransform(cauchy[3:5].copy(), cauchy[12:14]),
                  Write(cauchy[11]), run_time=1.5)
        self.play(Write(cauchy[8:11]), Write(cauchy[14:17]), run_time=2)
        self.wait()

        # number line
        self.play(FadeIn(VGroup(number_line, a, b)))
        self.play(Write(left_r), Write(right_r))
        self.wait(2)
        self.play(ReplacementTransform(left_r, left_s))
        self.wait(2)
        self.play(FadeIn(VGroup(right_s, x_label)))
        self.wait()
        self.play(Write(cauchy[17:]))
        self.play(FadeIn(VGroup(xi, xi_label)))
        cauchy_label = BraceLabel(cauchy, r"{\heiti $[a,x]$上的Cauchy中值定理}", label_constructor=TextMobject,
                                  label_scale=.8)
        cauchy_label.label.set_color(YELLOW)
        self.play(GrowFromCenter(cauchy_label.brace))
        self.play(Write(cauchy_label.label))
        self.wait()
        self.play(Write(r1))
        self.play(Write(r2))
        self.play(Write(r3))
        self.play(ShowCreation(box2))
        self.wait()

        # x to a+
        self.play(right_s.move_to, number_line.n2p(-1.6), xi.move_to, number_line.n2p(-1.8), run_time=2)

        self.wait()
        self.play(FadeOut(cauchy_label))
        self.play(ReplacementTransform(cauchy[:5].copy(), conclusion[4:9]), Write(conclusion[:4]), run_time=2)
        self.play(Write(conclusion[9:14]), ReplacementTransform(cauchy[18:].copy(), conclusion[14:]), run_time=2)
        self.wait()
        self.play(Transform(conclusion, conclusion2))
        self.wait(2)
        x_label.clear_updaters()
        xi_label.clear_updaters()

        # finishing 0/0
        self.play(FadeOut(VGroup(box2, v1, conclusion, cauchy, bg,
                                 number_line, x_label, xi_label, xi, a, b, left_s, right_s, right_r)))
        tmain[0].become(t[0])
        self.play(Transform(tmain[1:], t[1:]), run_time=2)
        self.wait()

        # inf/inf starts
        self.play(FadeIn(VGroup(t1, t2, t3, t4, arrow2, arrow4, tmain[0])), ShowCreation(box))
        self.wait()

        self.play(FadeOut(t3[:6]), ReplacementTransform(t3[6:11], t3_inf[:5]),
                  ReplacementTransform(t3[-1], t3_inf[-1]), Transform(title, title_inf), )
        self.wait()
        self.play(FadeOut(VGroup(t1, t2, t3_inf, t4, box, arrow2, arrow4)),
                  FadeOut(tmain[0]),
                  tmain[1:].move_to, t1, run_time=2)
        self.wait()

        # proof starts: strip
        right_box = SurroundingRectangle(tmain[10:], color=YELLOW)
        l = TextMobject(r'\kaishu 记为~$l$', color=YELLOW).next_to(right_box, RIGHT)
        self.play(ShowCreation(right_box))
        self.play(Write(l))
        self.wait()

        strip = TexMobject(r"\text{{\kaishu 区间内有~}}",*r"l-\varepsilon< {f '(x)\over g '(x)} < l+\varepsilon.".split()).set_color_by_tex_to_color_map(self.map).scale(.9)
        #######################################################   1       2      3     4   5
        VGroup(number_line, strip).arrange(buff=LARGE_BUFF*1).next_to(tmain[1:], DOWN)

        left_r, right_r = TexMobject("(", color=TEAL, stroke_width=3).scale(1.2).move_to(
            number_line.get_left()).align_to(number_line, LEFT), \
                          TexMobject(")", color=TEAL, stroke_width=3).scale(1.2).move_to(
                              number_line.get_right()).align_to(number_line, RIGHT)
        left_s, right_s = TexMobject("[", color=YELLOW, stroke_width=3).scale(1.2).move_to(
            number_line.n2p(-0.5)), \
                          TexMobject("]", color=YELLOW, stroke_width=3).scale(1.2).move_to(number_line.n2p(0.5))
        a, a_delta, x, c = [TexMobject(f"{s}").scale(.9) for s in ["a",r"a+\delta","x","c"]]
        a.next_to(left_r, DOWN)
        a_delta.next_to(right_r, DOWN).align_to(a, DOWN).shift(DOWN*.048)
        x.add_updater(lambda u: u.next_to(left_s, DOWN))
        c.add_updater(lambda u: u.next_to(right_s, DOWN))
        xi_arrow = Arrow(UP, DOWN).next_to(number_line.n2p(0), DOWN)
        xi_label2 = TexMobject(r"\xi")
        xi_label2.scale(.9).next_to(xi_arrow, DOWN)

        # number line shows
        self.play(FadeIn(VGroup(number_line, left_r, right_r, a, a_delta)))
        self.play(Write(strip))
        self.wait()
        self.play(FadeIn(VGroup(left_s, right_s, x, c)))
        self.wait()

        cauchy2 = TexMobject(*r"{{f "
        #                       0
                              r"( x ) - f ( c )} \over {g"
        #                       1 2 3 4 5 6 7 8    9   10
                              r" ( x ) - g ( c )}} = "
        #                       11 12131415161718  19
                              r"{f '( \xi )\over g '( \xi )}".split()).tm(self.map).next_to(number_line, DOWN, buff=LARGE_BUFF).set_x(0)
        #                       20  21 22  23    24 25 26 27
        cauchy2_ineq = TexMobject(*r"l-\varepsilon < {{f "
        #                                 0        1   2
                                   r"( x ) - f ( c )} \over {g"
        #                       3 4 5 6 7 8 9 10   11   12
                                   r" ( x ) - g ( c )}} "
        #                       13 14151617181920   
                                   r"< l+\varepsilon".split()).tm(self.map).next_to(number_line, DOWN,
                                                                                    buff=LARGE_BUFF).set_x(
            0)
        #                       21  22
        cauchy2_gx = TexMobject(*r"l-\varepsilon < {{{f "
        #                                 0      1    2  
                                 r"( x ) \over g (x)} - {f ( c ) \over g (x)}} \over {{g"
        #                          3 4 5  6    7  8   9 10 111213  14  15 16     17   18
                                 r" ( x ) \over g (x)} - {g ( c ) \over g (x)}}} "
        #                           192021  22 23 24   25 26272829  30  31 32   
                                 r"< l+\varepsilon".split()).tm(self.map).next_to(number_line, DOWN,
                                                                                  buff=LARGE_BUFF).set_x(
            0)
        #                            33  34
        cauchy2_res = TexMobject(*r"l-\varepsilon < {{{f "
        #                                 0      1    2  
                                 r"( x ) \over g (x)} - {f ( c ) \over g (x)}} \over {1 "
        #                         3  4 5  6     7  8  9  10111213  14  15 16     17   18
                                 r"- {g ( c ) \over g (x)}}} "
        #                         19  2021  22 23 24   25 26272829  30  31 32   
                                 r"< l+\varepsilon".split()).tm(self.map).next_to(number_line, DOWN,
                                                                                  buff=LARGE_BUFF).set_x(
            0)
        #                            33  34
        question = TexMobject(r"\text{\kaishu 如何出现~}\frac{f(x)}{g(x)}?",color=YELLOW).scale(.9)

        clock = Clock().scale(.9)
        VGroup(question, clock).arrange(buff=LARGE_BUFF).next_to(cauchy2_ineq, DOWN)
        limit = TexMobject(*r"l-\varepsilon \leq \lim_{x\to a^+} {f (x) \over g (x)}\leq l+\varepsilon".split())\
            .tm(self.map).next_to(cauchy2_gx, DOWN)
        imply = CurvedArrow(cauchy2_gx.get_left()+LEFT*.5, limit.get_left()+LEFT*.5, color=YELLOW)
        error = VGroup(TextMobject(r"\kaishu 默认了"),
                       TexMobject(r"\lim_{x\to a^+}\frac{f(x)}{g(x)}\text{\kaishu 存在}"))\
            .arrange(DOWN).set_color(YELLOW).scale(.8).next_to(imply, LEFT)
        cross = Cross(limit)
        # proof continues
        self.play(Write(cauchy2))
        self.wait()
        self.play(GrowArrow(xi_arrow))
        self.play(Write(xi_label2))
        self.wait()
        self.play(ShowPassingFlashAround(cauchy2[20:]), ShowPassingFlashAround(strip[2:6]))
        self.play(ShowPassingFlashAround(cauchy2[20:]), ShowPassingFlashAround(strip[2:6]))
        self.wait()
        # xi_label.clear_updaters()
        self.play(FadeOut(cauchy2[19:]), ReplacementTransform(cauchy2[:19], cauchy2_ineq[2:21]),
                  FadeOut(VGroup(xi_arrow, xi_label2)))
        self.play(Write(cauchy2_ineq[:2]), Write(cauchy2_ineq[21:]))
        self.wait()

        # think about how to relate to f/g
        self.play(Write(question))
        self.wait()
        self.play(FadeIn(clock))
        self.play(ClockPassesTime(clock))
        self.play(FadeOut(clock), FadeOut(question))
        self.wait()

        # super dirty transformation
        self.play(ReplacementTransform(cauchy2_ineq[:2], cauchy2_gx[:2]),
              ReplacementTransform(cauchy2_ineq[2], cauchy2_gx[2]),
              ReplacementTransform(cauchy2_ineq[3], cauchy2_gx[3]),
              ReplacementTransform(cauchy2_ineq[4], cauchy2_gx[4]),
              ReplacementTransform(cauchy2_ineq[5], cauchy2_gx[5]),
              ReplacementTransform(cauchy2_ineq[6], cauchy2_gx[9]),
              ReplacementTransform(cauchy2_ineq[7], cauchy2_gx[10]),
              ReplacementTransform(cauchy2_ineq[8], cauchy2_gx[11]),
              ReplacementTransform(cauchy2_ineq[9], cauchy2_gx[12]),
              ReplacementTransform(cauchy2_ineq[10], cauchy2_gx[13]),
              ReplacementTransform(cauchy2_ineq[11], cauchy2_gx[17]),
              ReplacementTransform(cauchy2_ineq[12], cauchy2_gx[18]),
              ReplacementTransform(cauchy2_ineq[13], cauchy2_gx[19]),
              ReplacementTransform(cauchy2_ineq[14], cauchy2_gx[20]),
              ReplacementTransform(cauchy2_ineq[15], cauchy2_gx[21]),
              ReplacementTransform(cauchy2_ineq[16], cauchy2_gx[25]),
              ReplacementTransform(cauchy2_ineq[17], cauchy2_gx[26]),
              ReplacementTransform(cauchy2_ineq[18], cauchy2_gx[27]),
              ReplacementTransform(cauchy2_ineq[19], cauchy2_gx[28]),
              ReplacementTransform(cauchy2_ineq[20], cauchy2_gx[29]),
              ReplacementTransform(cauchy2_ineq[21:], cauchy2_gx[33:]),
              )
        self.play(
            Write(cauchy2_gx[6:9]),
            Write(cauchy2_gx[14:17]),
            Write(cauchy2_gx[22:25]),
            Write(cauchy2_gx[30:33]),
        )
        # self.play(ReplacementTransform(cauchy2_gx, cauchy2_res))
        self.play(Transform(cauchy2_gx[18:25], cauchy2_res[18]),
                  Transform(cauchy2_gx[25], cauchy2_res[19]),
                  Transform(cauchy2_gx[26:33], cauchy2_res[20:-2])
                  )

        # two parts to 0 as x-> a+
        bg1 = SurroundingRectangle(cauchy2_gx[10:17], color=GOLD, buff=0.05)
        bg2 = SurroundingRectangle(cauchy2_gx[26:33], color=GOLD, buff=0.05)
        to0 = TexMobject(r"\to 0", color=GOLD).next_to(bg1, buff=.1).scale(.8)
        to02 = TexMobject(r"\to 0", color=GOLD).next_to(bg2, buff=.1).scale(.8)

        self.wait()
        self.play(left_s.move_to, number_line.n2p(-1.7), run_time=2)
        self.wait()
        self.play(ShowCreation(bg1))
        self.play(ShowCreation(bg2))
        self.play(Write(to0), Write(to02))
        self.wait()
        self.play(Write(limit))
        self.wait()

        # but there's an error
        self.play(GrowArrow(imply))
        self.wait()
        self.play(Write(error[0]))
        self.play(Write(error[1]))
        self.wait()
        self.play(ShowCreation(cross))
        self.wait()

        # go over upper/lower limits
        self.play(FadeOut(VGroup(
            tmain[1:], right_box, l,
            number_line, left_r, left_s, right_s, right_r, a, a_delta, x, c,
            strip,
            cauchy2_gx, bg1, bg2, to0, to02,
            imply, error, limit, cross
        )), Transform(title, title_limit))
        self.wait()

        prop1 = TexMobject(*r"1.~\lim_{x\to0}\sin \left(\frac{1}{x}\right) ".split(),r"\text{\kaishu 不存在}",*r",~ \varlimsup_{x\to0} \sin\left(\frac{1}{x}\right)"
                            r"=1,~ \varliminf_{x\to0} \sin\left(\frac{1}{x}\right) =-1".split())\
            .tm(self.infmap).scale(.9).next_to(title_limit, DOWN).set_x(0)
        prop2 = TexMobject(*r"2.~ \varliminf \leq \varlimsup ,~".split(),r"\text{\kaishu 等号成立}",*r"\Longleftrightarrow~ \lim= \varliminf = \varlimsup".split())\
            .tm(self.infmap).next_to(prop1, DOWN, aligned_edge=LEFT, buff=LARGE_BUFF)
        prop3 = TexMobject(*r"3.~ f\leq g ~\Longrightarrow~ \varliminf f \leq \varliminf g,~ \varlimsup f \leq \varlimsup g".split())\
            .tm({"limsup": RED, "liminf": GREEN}).next_to(prop2, DOWN, aligned_edge=LEFT, buff=LARGE_BUFF*1.3)
        self.play(Write(prop1[:3]))
        self.wait()
        self.play(Write(prop1[3:]))
        self.wait()
        self.play(Write(prop2[:4]))
        self.wait()
        self.play(Write(prop2[4:]))
        self.wait()
        self.play(Write(prop3[:3]))
        self.wait()
        self.play(Write(prop3[3:]))
        self.wait(2)

        # go back
        self.play(FadeOut(VGroup(prop1, prop2, prop3)),
                  Transform(title, title_inf))
        VGroup(
            cauchy2_gx, bg1, bg2, to0, to02,
        ).shift(UP)
        VGroup(bg1, bg2, to0, to02).set_color(YELLOW)

        brace1 = Brace(cauchy2_gx[:33], DOWN)
        liminf = TexMobject(*r"l - \varepsilon \leq \varliminf_{x\to a^+} {f (x)\over g (x)}".split())\
            .tm(self.map).scale(1).next_to(brace1, DOWN)
        brace2 = Brace(cauchy2_gx[2:], DOWN)
        limsup = TexMobject(*r"\varlimsup_{x\to a^+} {f (x)\over g (x)} \leq l + \varepsilon".split())\
            .tm(self.map).scale(1).next_to(brace2, DOWN)
        liminfsup = TexMobject(*r"l - \varepsilon \leq \varliminf_{x\to a^+} {f (x)\over g (x)} \leq \varlimsup_{x\to a^+} {f (x)\over g (x)} \leq l + \varepsilon".split())\
            .tm(self.map).scale(1).next_to(brace1, DOWN).set_x(0)
        lim0eps = TexMobject(
            *r"l \leq \varliminf_{x\to a^+} {f (x)\over g (x)} \leq \varlimsup_{x\to a^+} {f (x)\over g (x)} \leq l".split()) \
            .tm(self.map).scale(1).next_to(brace1, DOWN).set_x(0)
        limeq = TexMobject(
            *r"l = \varliminf_{x\to a^+} {f (x)\over g (x)} = \varlimsup_{x\to a^+} {f (x)\over g (x)} = l".split()) \
            .tm(self.map).scale(1).next_to(brace1, DOWN).set_x(0)
        limres = TexMobject(
            *r"\lim_{x\to a^+} {f (x)\over g (x)}= l".split()) \
            .tm(self.map).scale(1).next_to(brace1, DOWN).set_x(0)
        bg_inf = BackgroundRoundedRectangle(VGroup(cauchy2_gx, lim0eps)).set_width(FRAME_WIDTH-2, stretch=True)
        self.play(FadeIn(VGroup(
            tmain[1:], right_box, l,
            cauchy2_gx, bg1, bg2, to0, to02,
            bg_inf
        )))
        self.wait()

        # braces
        self.play(GrowFromCenter(brace1))
        self.play(Write(liminf))
        self.wait()
        self.play(FadeOut(brace1), liminf.shift, LEFT*3)

        self.play(GrowFromCenter(brace2))
        self.play(Write(limsup))
        self.wait()
        # self.play(FadeOut(brace2))
        self.play(FadeOut(brace2), ReplacementTransform(liminf, liminfsup[:10]),
                  ReplacementTransform(limsup, liminfsup[11:]))
        self.play(Write(liminfsup[10]))
        self.wait()
        self.play(ReplacementTransform(liminfsup[3:-3], lim0eps[1:-1]),
                  ReplacementTransform(liminfsup[:3], lim0eps[0]),
                  ReplacementTransform(liminfsup[-3:], lim0eps[-1]),
                  )
        self.wait()
        self.play(ReplacementTransform(lim0eps, limeq))
        self.wait()
        self.play(ReplacementTransform(limeq, limres))
        self.wait()
        self.play(FadeOut(VGroup(
            tmain[1:], right_box, l,
            cauchy2_gx, bg1, bg2, to0, to02,
            bg_inf,
            limres, title
        )))

    def other_limit(self):
        minus = TexMobject(r"x\to ",r"a^-",r"~\text{时，证明类似.}")
        minus[1].set_color(YELLOW)
        a = TexMobject(r"x\to ","a",r"~\text{时，转化为单侧极限.}")
        a[1].set_color(YELLOW)
        inf = TexMobject(r"x\to ",r"\pm\infty",r"~\text{时，作}~",r"t=\frac 1x",r"~\text{化为}~",r"t\to 0^+/0^-.")
        inf[1].set_color(YELLOW)
        VGroup(minus, a, inf).arrange(DOWN, buff=LARGE_BUFF)
        self.play(Write(minus))
        self.wait()
        self.play(Write(a))
        self.wait()
        self.play(Write(inf))
        self.wait()
        self.play(FadeOut(VGroup(minus, a, inf)))

    def remark1(self):
        q = TexMobject("1.~",r"\lim_{x\to 0} {\sin x \over x} = 1",r"~\text{可以用l'H\^{o}pital法则吗？}").to_edge(UP)
        q[1].set_color(YELLOW)
        clock = Clock()
        sol = TexMobject(*r"\lim_{x\to 0} {(\sin x)' \over x'} =\lim_{x\to 0} {\cos x \over 1} =\cos 0=1.".split()).next_to(q, DOWN)
        ########################   0   1      2  3     4    5           6  7    8   9    10 11   12   13
        derdef = VGroup(TexMobject(r"(\sin x)'",r"=",r"\lim_{h\to 0} {{\sin (x+h)-\sin x}\over h}"),
                        TexMobject(r"=\lim_{h\to 0} {{2\cos\left(x+\frac{h}{2}\right)\sin\left(\frac{h}{2}\right)} \over h}"),
                        TexMobject(r"=",r"\cos x\cdot",r"\lim_{h\to 0} {{\sin\left(\frac{h}{2}\right)} \over {\frac{h}{2}}}")).arrange(DOWN).next_to(sol, DOWN)
        derdef[1].align_to(derdef[0][1], LEFT)
        derdef[2].align_to(derdef[0][1], LEFT)
        derdef[2][-1].set_color(YELLOW)

        taylor_sin = TexMobject(r"\sin x=x-\frac{x^3}{3!}+\frac{x^5}{5!}-\cdots")
        taylor_cos = TexMobject(r"\cos x=1-\frac{x^2}{2!}+\frac{x^4}{4!}-\cdots")
        taylor_v = VGroup(taylor_sin, taylor_cos).arrange(DOWN).scale(.9).set_color(RED)

        euler_sin = TexMobject(r"\sin x=\frac{\e^{\i x}-\e^{-\i x}}{2\i}")
        euler_cos = TexMobject(r"\cos x=\frac{\e^{\i x}+\e^{-\i x}}{2}")
        euler_v = VGroup(euler_sin, euler_cos).arrange(DOWN).scale(.9).set_color(BLUE)

        other_v = VGroup(taylor_v, euler_v).arrange(buff=LARGE_BUFF*1.5).next_to(sol, DOWN, buff=MED_LARGE_BUFF)
        taylor_brace = Brace(VGroup(taylor_sin, taylor_cos), LEFT)
        euler_brace = Brace(VGroup(euler_sin, euler_cos), LEFT)
        bg_other = BackgroundRectangle(other_v)
        use_derdef = TexMobject(r"\text{没有必要.}~",r"\lim_{x\to 0}\frac{\sin x-\sin 0}{x-0}",r"=\sin'(0)=\cos 0=1.").next_to(other_v, DOWN)
        use_derdef[1].set_color(YELLOW)
        self.play(Write(q))
        self.wait()
        self.play(FadeIn(clock))
        self.play(ClockPassesTime(clock))
        self.play(FadeOut(clock))
        self.play(Write(sol))
        self.wait()
        box_der = SurroundingRectangle(VGroup(sol[2:4], sol[8:10]), color=RED)
        self.play(ShowCreation(box_der))
        self.wait()
        self.play(Write(derdef[0]))
        self.play(Write(derdef[1]))
        self.play(Write(derdef[2]))
        self.wait()
        self.play(Transform(box_der, SurroundingRectangle(derdef[2][-1], color=RED)))
        self.wait()

        # other def
        self.play(FadeOut(box_der), FadeOut(derdef))
        self.play(Write(taylor_sin))
        self.play(Write(taylor_cos))
        self.play(GrowFromCenter(taylor_brace))
        self.wait()
        self.play(Write(euler_sin))
        self.play(Write(euler_cos))
        self.play(GrowFromCenter(euler_brace))
        self.wait()
        self.play(Write(use_derdef[0]))
        self.wait()
        self.play(Write(use_derdef[1:]))
        self.wait()
        self.play(FadeOut(VGroup(
            q, sol, taylor_v, euler_v, taylor_brace, euler_brace, use_derdef
        )))

    def remark2(self):
        remark = TexMobject("2.~",r"\text{关于要求}\,",*r"\lim_{x\to a^+} {f '(x) \over g '(x)}".split(),r"~\text{存在.}").to_edge(UP).tm(self.map)
        p = TexMobject(r"\lim_{x\to\infty}{{x+\sin x}\over x}=\lim_{x\to\infty} 1+\lim_{x\to\infty}{\sin x \over x}=1+0=1")#.next_to(remark, DOWN)
        lhospital = TexMobject(r"\lim_{x\to\infty}{(x+\sin x)' \over x'}=\lim_{x\to\infty} (1+\cos x)",r"~\text{不存在.}")#.next_to(p, DOWN, buff=MED_LARGE_BUFF)
        VGroup(p, lhospital).arrange(DOWN, buff=LARGE_BUFF).next_to(remark, DOWN, buff=MED_LARGE_BUFF)
        self.play(Write(remark))
        self.wait()
        self.play(Write(p), run_time=3)
        self.wait()
        self.play(Write(lhospital), run_time=3)
        self.wait()
        self.play(FadeOut(VGroup(remark, p, lhospital)))

    def remark3(self):
        remark = TexMobject(r"3.~",r"\text{关于要求}~",r"g",r"'(x)",r"~\text{在去心邻域内恒不为0.}").tm(self.map).to_edge(UP)
        example = TexMobject(r"\lim_{x\to\infty}",r"{{x+\sin x\cos x}",r"\over {\e^{\sin x}\left(",r"x+\sin x\cos x",r"\right)}}","=",
                             r"\lim_{x\to\infty}{1\over \e^{\sin x}}",r"~\text{不存在.}").next_to(remark, DOWN)
        lhospital = VGroup(TexMobject(r"{{\left(",r"x+\sin x\cos x",r"\right)'}",r"\over {\left(\e^{\sin x}\left(",r"x+\sin x\cos x",r"\right)\right)'}}"),
                           TexMobject("="),
                           TexMobject(r"{{2\cos^2 x} \over {\e^{\sin x}",r"\cos x",r" (2\cos x+x+\sin x\cos x)}}"),
                           ).scale(.95).arrange().next_to(example, DOWN, buff=MED_LARGE_BUFF)
        # lhospital[2].next_to(lhospital[0], DOWN).align_to(lhospital[0], LEFT)
        # lhospital[1].next_to(lhospital[2], LEFT)
        lhospital2 = TexMobject("=",r"{{2\cos x} \over {\e^{\sin x}",r" (2\cos x+x+\sin x\cos x)}}").next_to(lhospital, DOWN).align_to(lhospital[1], LEFT)
        lhospital3 = TexMobject(r"\to 0").next_to(lhospital2, DOWN, buff=MED_LARGE_BUFF, aligned_edge=LEFT)

        for i in [1,3]:
            example[i].set_color(YELLOW)
        lhospital[0][1].set_color(YELLOW)
        lhospital[0][4].set_color(YELLOW)
        lhospital[2][-2].set_color(RED)
        self.play(Write(remark))
        self.wait()
        self.play(Write(example[:5]))
        self.wait()
        self.play(Write(example[5:]))
        self.wait()
        self.play(Write(lhospital[0]))
        self.wait()
        self.play(Write(lhospital[1:]))
        self.wait()
        self.play(Write(lhospital2))
        self.wait()
        self.play(Write(lhospital3))
        self.wait(4)








