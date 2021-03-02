from manimlib import *

m = {"z": YELLOW, "w": BLUE, "\\Longrightarrow": WHITE, }


class Def(Scene):
    def construct(self):
        prob = Tex("\\text{如何定义}~ {{\\ln}} z?", tex_to_color_map=m).to_edge(UP, buff=1)
        calc = Tex("\\text{如何计算}~ {{\\ln}} z?", tex_to_color_map=m).to_edge(UP, buff=1)
        self.play(Write(prob))
        self.wait()

        exp = Tex(r"\text{若有}~\e^w=z,", tex_to_color_map=m).next_to(prob, DOWN, buff=1)
        self.play(Write(exp))
        self.wait()

        ln = Tex(r"\text{我们说}~ w=\ln z.", tex_to_color_map=m).next_to(exp, DOWN)
        self.play(Write(ln))
        self.wait()

        issue = Tex(r"\e^{{0}}=\e^{{{2\pi\i}}}=\e^{{{4\pi\i}}}=\cdots={{1}}") \
            .tm({"0": BLUE, "pi": BLUE, "1": YELLOW}).next_to(ln, DOWN, buff=1)
        multi = Tex(r"\ln{{1}}={{0}},~{{\pm 2\pi\i}},~{{\pm 4\pi\i}},~\cdots").tm(
            {"0": BLUE, "pi": BLUE, "1": YELLOW}).next_to(issue, DOWN, buff=.5)
        comment = TexText("\\kaishu 我们不认为多值函数是函数.", color=GREEN).to_edge(DOWN, buff=.5)
        arrow = Arrow(comment.get_top(), multi.get_bottom()).set_color(GREEN)
        self.play(Write(issue))
        self.wait()
        self.play(Write(multi))
        self.wait()
        self.play(Write(comment), GrowArrow(arrow))
        self.wait()

        self.play(TransformMatchingTex(prob, calc),
                  FadeOut(VGroup(issue, multi, comment, arrow)))
        self.wait()

        notation = Tex(r"\text{记~} {{w}}={{x+\i y}},\text{~那么}").tm({"w": BLUE, "y": BLUE, }).next_to(ln, DOWN, buff=1)
        polar = Tex(r"{{z}}=\e^{{w}}=\e^{{{x+\i y}}}={{\e^x\e^{\i y}}}").tm(
            {"z": YELLOW, "w": BLUE, "x": BLUE, "\\e^x": YELLOW}).next_to(notation, DOWN)
        self.play(Write(notation))
        self.wait()
        self.play(Write(polar))
        self.wait()

        r_theta = Tex(r"r~\e^{\i\theta}", color=GREEN).next_to(polar[-1], DOWN)
        self.play(Write(r_theta))
        self.wait()

        m2 = {r"\ln": GREEN, "r": GREEN, "x": YELLOW, "y": YELLOW, "theta": GREEN, "Longrightarrow": WHITE,
              "|z|": GREEN, "arg": GREEN}
        cor = VGroup(Tex(r"\Longrightarrow {{x}}={{\ln}} {{r}},"), Tex(r"{{y}}={{\theta+2k\pi}}")).arrange(
            buff=.5).to_edge(DOWN)
        cor2 = VGroup(Tex(r"\Longrightarrow {{x}}={{\ln}} {{|z|}},").move_to(cor[0]),
                      Tex(r"{{y}}={{\arg z}}").move_to(cor[1]).align_to(cor[1], DL))

        for c in [*cor] + [*cor2]:
            c.tm(m2)

        self.play(Write(cor[0]))
        self.wait()
        self.play(Write(cor[1]))
        self.wait()
        self.play(
            TransformMatchingTex(cor[0], cor2[0], key_map={'r': '|z|', r'\theta+2k\pi': r'\arg z'}),
            TransformMatchingTex(cor[1], cor2[1]),
        )
        self.wait()
        self.play(FadeOut(VGroup(notation, exp, ln, cor2, polar, r_theta)))

        formula = Tex(r"\ln z=\ln |z|+\i\arg z", tex_to_color_map={"z": YELLOW, "\\i": BLUE}).scale(2)
        box = SurroundingRectangle(formula, buff=.5)
        self.play(Write(formula))
        self.play(ShowCreation(box))
        self.wait()


class Polar(Scene):
    def construct(self):
        m = {"r": GREEN, "theta": YELLOW, "sqrt": GREEN, "frac": YELLOW}

        plane = ComplexPlane().add_coordinate_labels()
        self.add(plane)
        point = Dot(plane.n2p("3+3j"), color=GREEN)
        label = Tex(r"{{r}}\e^{\i\theta}", isolate=["\\e", "\\theta"]).tm(m).next_to(point)
        bg = BackgroundRectangle(label)
        line = Line(ORIGIN, point)
        r = Brace(line, UL)
        r = VGroup(r.set_color(m['r']), r.get_tex("r").set_color(m['r']).add_background_rectangle())
        mod = VGroup(
            TexText("modulus"),
            Tex("|z|")
        ).arrange(DOWN).next_to(r[-1], LEFT, buff=1.5).set_color(r[-1].get_color())
        for mo in mod:
            mo.add_background_rectangle()
        theta = Arc(angle=PI / 4, color=m['theta'], radius=.7)
        theta = VGroup(theta, Tex(r"\theta", color=m['theta']).next_to(theta).shift(UP * .2).add_background_rectangle())
        arg = VGroup(
            TexText("argument"),
            Tex("\\arg (z)")
        ).arrange(DOWN).next_to(theta[-1], buff=1).set_color(theta[-1].get_color()).shift(UP * .3)
        for a in arg:
            a.add_background_rectangle()
        three = Tex(r"{{3\sqrt2}}\,\e^{\i{{\frac\pi 4}}}", isolate=["\\e"]).tm(m).next_to(point)

        self.play(GrowFromCenter(point))
        self.play(ShowCreation(line))
        self.wait()
        self.add(bg)
        self.play(Write(label))
        self.wait()
        self.play(GrowFromCenter(r))
        self.wait()
        self.play(GrowFromCenter(theta))
        self.wait()
        self.play(TransformMatchingTex(label, three, key_map={'r': r'3\sqrt2', r'\theta': r'\frac\pi 4'}))
        three.add_background_rectangle()
        self.wait()
        self.play(Write(mod))
        self.wait()
        self.play(Write(arg))
        self.wait()

        point2 = Dot(plane.n2p("-5"), color=RED)
        label2 = Tex(r"5\e^{\i\pi}") \
            .set_color(point2.get_color()).next_to(point2, DOWN, buff=.5).add_background_rectangle()
        self.play(GrowFromCenter(point2))
        self.play(Write(label2))
        self.wait()


class Branch(Scene):
    def construct(self):
        th = ValueTracker(1e-5)

        plane = ComplexPlane(axis_config={"unit_size": 2}).add_coordinate_labels()
        self.add(plane)

        one_point = Dot(plane.n2p(1), color=YELLOW)
        self.add(one_point)

        ln = Tex("\\ln1={{\\ln |1|}}+\\i\\arg (1)", color=YELLOW).next_to(one_point, UP, buff=.5)
        ln2 = Tex("\\ln1={{0}}+\\i\\arg (1)").set_color(ln.get_color()).move_to(ln)
        ln3 = Tex("\\ln1=\\i{{\\arg (1)}}").set_color(ln.get_color()).move_to(ln)

        arg_0 = Tex("\\ln1=\\i{{0}}").set_color(ln.get_color()).move_to(ln)
        arg_2pi = Tex("\\ln1=\\i{{(2\\pi)}}").set_color(ln.get_color()).move_to(ln).tm({"pi": GREEN})
        arg_m2pi = Tex("\\ln1=\\i{{(-2\\pi)}}").set_color(ln.get_color()).move_to(ln).tm({"pi": RED})
        bg = BackgroundRectangle(ln)
        bg2 = BackgroundRectangle(ln2)
        bg3 = BackgroundRectangle(ln3)
        line = Line(ORIGIN, one_point, color=YELLOW, stroke_width=8)

        def update_point(a):
            return a.move_to(plane.n2p(complex(np.cos(th.get_value()), np.sin(th.get_value()))))

        one_point.add_updater(update_point)
        arc = Arc().add_tip(fill_opacity=0)

        def update_arc(a):
            a.become(
                Arc(radius=0.4, angle=th.get_value())
                    .add_tip(reset=False, length=.2, width=.2))
            if th.get_value() > 0:
                a.set_color(GREEN)
            if th.get_value() < 0:
                a.set_color(RED)

        self.add(bg)
        self.play(Write(ln))
        self.wait()
        self.play(RT(bg, bg2),
                  TransformMatchingTex(ln, ln2, key_map={"\\ln |1|": "0"}),
                  )
        self.play(RT(bg2, bg3),
                  TransformMatchingShapes(ln2, ln3),
                  )
        self.wait()

        self.play(GrowArrow(line))

        def update_line(a):
            return a.become(Line(ORIGIN, one_point, color=one_point.get_color(), stroke_width=8))

        line.add_updater(update_line)
        arc.add_updater(
            # lambda t: t.become(
            #     Arc(radius=0.4, angle=th.get_value())
            #         .add_tip(reset=False, length=.2, width=.2).set_color(GREEN)
            # )
            update_arc
        )
        self.play(TransformMatchingTex(ln3, arg_0, key_map={"\\arg (1)": "0"}))
        self.wait()
        self.add(arc)
        self.play(
            TransformMatchingTex(arg_0, arg_2pi, key_map={"0": "2\\pi"}),
            th.increment_value, TAU,
            run_time=2,
        )
        self.wait()

        # self.remove(arc)
        # arc.clear_updaters()
        th.set_value(-1e-5)
        # arc.add_updater(
        #     # lambda t: t.become(
        #     #     Arc(radius=0.4, angle=th.get_value())
        #     #         .add_tip(reset=False, length=.2, width=.2).set_color(RED)
        #     # )
        #     update_arc
        # )
        self.play(
            TransformMatchingTex(arg_2pi, arg_m2pi, key_map={"(2\\pi)": "(-2\\pi)"}),
            th.increment_value, -TAU,
            run_time=2,
        )

        self.wait()
        arc.clear_updaters()
        self.play(
            TransformMatchingTex(arg_m2pi, ln3, key_map={"(-2\\pi)": "\\arg (1)"}),
            FadeOut(arc)
        )

        multi = Arrow(ORIGIN, DOWN).next_to(ln3[-1], UP)
        multi = VGroup(multi, TexText("多值的").next_to(multi, UP)).set_color(WHITE)
        self.play(GrowArrow(multi[0]), GrowFromCenter(multi[1]))
        self.wait()

        # -pi < arg <= pi
        scope = Tex("-\\pi<\\arg z\\leq\\pi", color=YELLOW) \
            .to_edge(UL, buff=1).shift(RIGHT).scale(1.5).add_background_rectangle()
        self.play(Write(scope))
        self.wait()
        th.set_value(-1e-5)
        arc.add_updater(update_arc)
        self.add(arc)
        self.play(th.set_value, -PI + 1e-5, run_time=3)
        self.play(th.set_value, PI - 1e-5, run_time=3)
        self.wait()

        # introduce branch cut
        arc.clear_updaters()
        one_point.clear_updaters()
        line.clear_updaters()
        self.play(FadeOut(multi), FadeOut(ln3), FadeOut(VGroup(arc, one_point, line)))
        self.remove(bg3)
        cut = BranchCut(factor=.1, num=40)
        cut.save_state()
        self.play(ShowCreation(cut))
        self.wait()

        cut_label = Arrow(ORIGIN, UP).next_to(cut, DOWN).shift(RIGHT)
        cut_label = VGroup(cut_label, TexText("branch cut").next_to(cut_label, DOWN)).set_color(YELLOW)
        cut_label[1].add_background_rectangle()
        self.play(GrowArrow(cut_label[0]), GrowFromCenter(cut_label[1]))
        self.wait()

        # three examples
        i_point, m1_point, mi_point = points = [Dot().move_to(_) for _ in
                                                [plane.n2p('j'), plane.n2p(-1), plane.n2p('-j')]]
        for i, c in zip([i_point, m1_point, mi_point], [PINK, TEAL, GOLD]):
            i.set_color(c)
        lines = [Line(ORIGIN, p, stroke_width=8).set_color(p.get_color()) for p in points]
        self.play(FadeOut(cut_label))
        self.play(cut.fade, .7)
        self.play(AnimationGroup(*[GrowFromCenter(i) for i in points]))
        self.play(AnimationGroup(*[ShowCreation(l) for l in lines], lag_ratio=.3))
        self.wait()

        lni = Tex(r"{{\ln(\i)=}}{{\ln(|\i|)+}}{{\i\arg(\i)}}").set_color(i_point.get_color()).next_to(i_point, )
        bg = BackgroundRectangle(lni)
        lni2 = Tex(r"{{\ln(\i)=}}{{\i\arg(\i)}}").set_color(i_point.get_color()).next_to(i_point)
        lni22 = Tex(r"\ln(\i)=\i{{\arg(\i)}}").set_color(i_point.get_color()).replace(lni2)
        lni3 = Tex(r"\ln(\i)=\i{{\frac \pi2}}").set_color(i_point.get_color()).next_to(i_point)
        bg2 = BackgroundRectangle(lni2)
        bg3 = BackgroundRectangle(lni3)
        # self.add(bg)
        self.play(Write(VGroup(bg, lni)))
        self.wait()
        self.play(RT(bg, bg2), TransformMatchingTex(lni, lni2))
        self.add(lni22)
        self.remove(lni2)
        self.wait()

        lnm1 = Tex(r"\ln(-1)=\i{{\arg(-1)}}").set_color(m1_point.get_color()).next_to(m1_point, UP).shift(LEFT * .1)
        lnm12 = Tex(r"\ln(-1)=\i{{\pi}}").set_color(m1_point.get_color()).move_to(lnm1)
        bgm1 = BackgroundRectangle(lnm1)
        bgm2 = BackgroundRectangle(lnm12)

        lnmi = Tex(r"\ln(-\i)=\i{{\arg(-\i)}}").set_color(mi_point.get_color()).next_to(mi_point)
        lnmi2 = Tex(r"\ln(-\i)=\i{{\left(-\frac \pi2\right)}}").set_color(mi_point.get_color()).next_to(mi_point)
        bgmi = BackgroundRectangle(lnmi)
        bgmi2 = BackgroundRectangle(lnmi2)

        self.play(Write(VGroup(bgm1, lnm1)))
        self.play(Write(VGroup(bgmi, lnmi)))
        self.wait()

        self.play(RT(bg2, bg3), TransformMatchingTex(lni22, lni3))
        self.play(RT(bgm1, bgm2), TransformMatchingTex(lnm1, lnm12))
        self.play(RT(bgmi, bgmi2), TransformMatchingTex(lnmi, lnmi2))
        self.wait()

        # not equal
        not_i = Tex(r"\ln{{(-\i)}}\neq\ln{{(-1)}}+\ln{{(\i)}}", color=YELLOW).scale(1.2).to_edge(DOWN)
        not_all = Tex(r"\ln{{(zw)}}\neq\ln{{(z)}}+\ln{{(w)}}", color=YELLOW).scale(1.2).to_edge(DOWN)
        bg_not = BackgroundRectangle(not_i)
        bg_not2 = BackgroundRectangle(not_all)
        box = SurroundingRectangle(not_all, buff=.2)
        self.play(Write(VGroup(bg_not, not_i)))
        self.play(ShowCreation(box))
        self.wait()
        self.play(RT(bg_not, bg_not2),
                  TransformMatchingTex(not_i, not_all,
                                       key_map={r"(-\i)": "(zw)",
                                                r"(-1)": "(z)",
                                                r"(\i)": "(w)"
                                                }))
        # self.play(ShowCreation(box))
        self.wait()

        # discuss about continuity
        self.remove(bg3, bgm2, bgmi2, bg_not2)
        self.play(
            FadeOut(VGroup(
                VGroup(*points), VGroup(*lines),
                lni3, lnm12, lnmi2,
                not_all, box
            )),
            Restore(cut)
        )
        th.set_value(-1e-5)
        arc.add_updater(update_arc)
        one_point.add_updater(update_point)
        line.add_updater(update_line)
        VGroup(one_point, line).set_color(PINK)
        self.add(one_point, line, arc)
        self.wait()

        thetaeq = Tex("\\theta=").to_corner(UR, buff=1).shift(LEFT * 2).scale(1.2).add_background_rectangle()
        theta = DecimalNumber(0, unit="^\\circ").add_background_rectangle().next_to(thetaeq)
        self.play(Write(VGroup(thetaeq, theta)))
        theta.add_updater(lambda t: t.set_value(th.get_value() / DEGREES))
        theta.add_updater(lambda t: t.next_to(thetaeq))
        self.play(th.set_value, -PI + 1e-5, run_time=3, rate_func=linear)
        th.set_value(PI - 1e-5)
        self.play(th.set_value, PI * .95, run_time=1, rate_func=linear)
        self.play(th.set_value, PI - 1e-5, run_time=1, rate_func=linear)
        th.set_value(-PI + 1e-5)
        self.play(th.set_value, -0.95 * PI, run_time=1, rate_func=linear)
        self.play(th.set_value, -PI + 1e-5, run_time=1, rate_func=linear)
        th.set_value(PI-1e-5)
        self.play(th.set_value, PI*.95, run_time=1, rate_func=linear)
        self.wait()

        to_clear = [arc, one_point, line, theta]
        for c in to_clear:
            c.clear_updaters()
        self.play(FadeOut(VGroup(scope, thetaeq, *to_clear)))

        cut_plane = TexText("在去掉了负实轴(和0)的复平面上,", color=YELLOW).to_edge(UP).add_background_rectangle()
        analytic = TexText("$\\ln z$解析,且$(\\ln z)'=\\frac 1z$", color=YELLOW).next_to(cut_plane, DOWN).add_background_rectangle()
        self.play(Write(cut_plane))
        self.wait()
        self.play(Write(analytic))
        self.wait()

        # other cuts
        self.play(FadeOut(cut_plane), FadeOut(analytic))
        self.wait()
        self.play(Rotating(cut, angle=PI, run_time=1))
        two_pi = Tex(r"0\leq\arg z<2\pi", color=YELLOW).scale(1.5).move_to(scope)
        pi_3 = Tex(r"\frac \pi3<\arg z\leq\frac 73\pi", color=YELLOW).scale(1.5).move_to(scope)
        bg = BackgroundRectangle(two_pi)
        self.play(Write(VGroup(bg, two_pi)))
        self.wait()
        self.play(Rotating(cut, angle=PI/3, run_time=1))
        self.play(TransformMatchingTex(two_pi, pi_3))
        self.wait()

        self.remove(bg)
        self.play(FadeOut(pi_3), FadeOut(cut))
        cut1 = BranchCut(factor=.1, num=40, color=RED).shift(LEFT*plane.get_x_unit_size())
        cut2 = BranchCut(factor=.1, num=50, color=YELLOW, reverse=True).shift(RIGHT*plane.get_x_unit_size())
        cut2.rotate(PI).fade(.3)
        # cut2.reverse_points()
        self.wait()
        f = Tex(r"f(z)=\ln(z+1)-\ln(z-1)", color=YELLOW).add_background_rectangle().to_edge(UP, buff=1)
        self.play(Write(f))
        self.wait()
        self.play(ShowCreation(cut1),
                  ShowCreation(cut2)
                  )
        self.wait()
        # for i, c in enumerate(cut2[0]):
        #     self.add(Text(str(i), color=PINK).scale(.5).move_to(c))
        self.play(FadeOut(cut1), FadeOut(cut2[0][20:]))
        self.wait()


class Note(Scene):
    def construct(self):
        title = TexText(r"\textbf{\heiti 关于记号...}", color=YELLOW).to_edge(UP, buff=.5)
        self.play(Write(title))
        self.wait()

        arg = VGroup(Tex("\\mathrm{Arg}"), Tex("\\arg"), ).arrange(DOWN, buff=.5).next_to(title, DOWN, buff=1).shift(
            LEFT * 3)
        ln = VGroup(Tex("\\mathrm{Ln}"), Tex("\\ln")).arrange(DOWN, buff=.5).next_to(arg, DOWN, buff=1)
        self.play(Write(arg))
        self.play(Write(ln))

        label_arg = VGroup(TexText("多值的").next_to(arg[0], buff=1),
                           TexText("单值的 (principal value)").next_to(arg[1], buff=1))
        label_ln = label_arg.copy().next_to(ln, buff=1)
        self.play(Write(label_arg[0]), Write(label_ln[0]))
        self.play(Write(label_arg[1]), Write(label_ln[1]))
        self.wait()
        self.play(
            label_arg[0].set_y, label_arg[1].get_y(),
            label_arg[1].set_y, label_arg[0].get_y(),
            label_ln[0].set_y, label_ln[1].get_y(),
            label_ln[1].set_y, label_ln[0].get_y(),
        )
        self.wait()

        self.play(FadeOut(VGroup(arg, ln, label_arg, label_ln)))
        my = TexText("\\heiti 视频中只采用$\\ln$的写法.", color=YELLOW).next_to(title, DOWN, buff=1.5)
        multi = TexText("在给出支割线之前是多值的,").next_to(my, DOWN, buff=1)
        single = TexText("之后是单值的.").next_to(multi, DOWN)
        self.play(Write(my))
        self.wait()
        self.play(Write(multi))
        self.play(Write(single))
        self.wait()


class DLog(Scene):
    def construct(self):
        lim1 = Tex(r"{{f'(z_0)}} {{=}} {{\lim_{ {{z}}\to {{z_0}} } }} {\ln {{z}}-\ln {{z_0}} \over {{z}}-{{z_0}}}",
                   ).tm({'z': YELLOW, 'z_0': WHITE}).to_edge(UP, buff=1).shift(LEFT)
        lim2 = Tex(r"\xlongequal{ w =\ln z} \lim_{w\to w_0} {w-w_0\over \e^w-\e^{w_0}}")\
            .tm({'w': BLUE, 'w_0': WHITE}).next_to(lim1[4], DOWN, buff=1).shift(RIGHT*1)

        VGroup(lim2[0][0], lim2[0][14], lim2[0][18], lim2[0][24]).set_color(BLUE)
        lim2[0][4].set_color(YELLOW)
        lim3 = Tex(r"=\lim_{w\to w_0}\frac{1}{\frac{\e^w-\e^{w_0} }{w-w_0} }")\
            .next_to(lim2, DOWN, buff=.5).align_to(lim1[1], LEFT)
        # for i, l in enumerate(lim3[0]):
        #     i = Text(str(i), color=PINK).scale(.5).move_to(l)
        #     self.add(i)
        VGroup(lim3[0][4],lim3[0][11],lim3[0][17]).set_color(BLUE)
        lim4 = Tex(r"={1\over \exp'(w_0)}").next_to(lim3, DOWN, aligned_edge=LEFT)
        lim5 = Tex(r"={1\over \e^{w_0} } ={1\over z_0}").next_to(lim4, buff=.2)

        self.play(Write(lim1))
        self.wait()
        self.play(Write(lim2))
        self.wait()
        self.play(Write(lim3))
        self.wait()
        self.play(Write(lim4))
        self.wait()
        self.play(Write(lim5))
        self.wait()


class pic(Scene):
    def construct(self):
        l = Tex("\\ln(\\i)").scale(7)
        self.add(l)


class exp(Scene):
    def construct(self):
        e = Tex("\\e^{\\i\\pi}").scale(7)
        self.add(e)

