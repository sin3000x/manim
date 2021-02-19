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
        one_point.add_updater(lambda t: t.move_to(plane.n2p(complex(np.cos(th.get_value()), np.sin(th.get_value())))))
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
        line.add_updater(lambda t: t.become(Line(ORIGIN, one_point, color=YELLOW, stroke_width=8)))
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
        scope = Tex("-\\pi<\\arg z\\leq\\pi", color=YELLOW)\
            .to_edge(UL, buff=1).shift(RIGHT).scale(1.5).add_background_rectangle()
        self.play(Write(scope))
        self.wait()
        th.set_value(-1e-5)
        arc.add_updater(update_arc)
        self.add(arc)
        self.play(th.set_value, -PI+1e-5, run_time=3)
        self.play(th.set_value, PI-1e-5, run_time=3)
        self.wait()

        arc.clear_updaters()
        one_point.clear_updaters()
        line.clear_updaters()
        self.play(FadeOut(multi), FadeOut(ln3), FadeOut(VGroup(arc, one_point, line)))
        self.remove(bg3)
        cut = BranchCut(factor=.1, num=40)
        self.play(ShowCreation(cut))
        self.wait()

        cut_label = Arrow(ORIGIN, UP).next_to(cut, DOWN).shift(RIGHT)
        cut_label = VGroup(cut_label, TexText("Branch Cut").next_to(cut_label, DOWN).add_background_rectangle()).set_color(YELLOW)
        self.play(GrowArrow(cut_label[0]), GrowFromCenter(cut_label[1]))
        self.wait()

        i_point, m1_point, mi_point = [Dot().move_to(_) for _ in [plane.n2p('j'), plane.n2p(-1), plane.n2p('-j')]]


