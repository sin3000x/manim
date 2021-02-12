from manimlib import *
# from manimlib.constants import *

m = {"z": YELLOW, r"\i": BLUE}
m2 = {"z_1": YELLOW, "z_2": BLUE}


class Def(Scene):
    def construct(self):
        exp = Tex(r"{{\e^{z} \coloneqq}}",r" {{1+z+{{{z^2\over2!}}}+{{{z^3\over3!}}}+{{{z^4\over4!}}}+{{{z^5\over5!}}}+\cdots}}"
                  , tex_to_color_map=m).to_edge(UP, buff=1)
        exp_lim = Tex(r"{{\e^{z} \coloneqq}}",r" {{\lim_{n\to\infty}}}{{\left(1+{z\over n}\right)^n}}", tex_to_color_map={"z": YELLOW}).move_to(exp)
        exp_diff = Tex(r"{{\e^{z} \coloneqq}}", r"\text{the solution to }",r"\begin{cases}f'(z) = f(z)\\f(0) = 1\end{cases}").move_to(exp)
        exp_real = Tex(r"{{\e^{x+\i y} \coloneqq}}",r"\e^x(\cos y+\i \sin y)", tex_to_color_map=m).move_to(exp)
        exp_diff[0][1].set_color(YELLOW)
        exp_diff[2][4].set_color(YELLOW)
        exp_diff[2][9].set_color(YELLOW)
        cos_x = Tex(r"\cos x = {\e^{{{\i x}}}+\e^{{{-\i x}}} \over 2}", isolate=["\\cos", "x", '\\e'],tex_to_color_map=m)
        # exp_real[2][1:3].set_color(YELLOW)
        cos_x.next_to(exp_real[2][1:3], DOWN, submobject_to_align=cos_x[2][0], aligned_edge=ORIGIN, buff=1.2)
        sin_x = Tex(r"\sin x = {\e^{{{\i x}}}-\e^{{{-\i x}}} \over 2\i}", isolate=["\\sin", "x", '\\e'], tex_to_color_map=m)
        sin_x.next_to(cos_x[0][-2], DOWN, submobject_to_align=sin_x[0][-2], aligned_edge=LEFT, buff=1.5)
        cos_z = Tex(r"\cos z \coloneqq {\e^{{{\i z}}}+\e^{{{-\i z}}} \over 2}",isolate=["\\cos", "z", '\\e'], tex_to_color_map=m)
        cos_z.next_to(exp_real[2][1], DOWN, submobject_to_align=cos_z[2], aligned_edge=LEFT, buff=1.2).set_y(cos_x.get_y())
        sin_z = Tex(r"\sin z \coloneqq {\e^{{{\i z}}}-\e^{{{-\i z}}} \over 2\i}",isolate=["\\sin", "z", '\\e'], tex_to_color_map=m)
        sin_z.next_to(exp_real[2][1], DOWN, submobject_to_align=sin_z[2], aligned_edge=LEFT, buff=1.2).set_y(sin_x.get_y())
        # for i, t in enumerate(exp_diff[2]):
        #     self.add(Text(str(i), color=YELLOW).move_to(t))
        sin = Tex(
            r"\sin z\coloneqq z-{{{z^3\over3!}}}+{{{z^5\over5!}}}-{{{z^7\over7!}}}+{{{z^9\over9!}}}-{{{z^{11}\over11!}}}+\cdots"
            , tex_to_color_map=m)
        cos = Tex(
            r"\cos z\coloneqq 1-{{{z^2\over2!}}}+{{{z^4\over4!}}}-{{{z^6\over6!}}}+{{{z^8\over8!}}}-{{{z^{10}\over10!}}}+\cdots"
            , tex_to_color_map=m)
        # exp = Tex(*r"\e^ {z} \coloneqq 1+ z + {z ^2 \over 2!} + {z ^3 \over 3!} + \cdots".split()).tm(m)
        # sin = Tex(*r"\sin z \coloneqq z- {z^3} + {z ^2 \over 2!} + {z ^3 \over 3!} + \cdots".split()).tm(m)
        sin.next_to(exp[2], DOWN, buff=1.2, aligned_edge=LEFT, submobject_to_align=sin[2])
        cos.next_to(sin[2], DOWN, buff=1.2, aligned_edge=LEFT, submobject_to_align=cos[2])
        self.play(Write(exp), run_time=2)
        self.play(Write(sin), run_time=2)
        self.play(Write(cos), run_time=2)
        self.wait()
        self.play(ShowPassingFlashAround(exp[2][:2]), ShowPassingFlashAround(sin[2][:2]), ShowPassingFlashAround(cos[2][:2]))
        self.play(ShowPassingFlashAround(exp[2][:2]), ShowPassingFlashAround(sin[2][:2]), ShowPassingFlashAround(cos[2][:2]))

        line = Line(color=RED).set_width(FRAME_WIDTH - 2).next_to(cos, DOWN).set_x(0)
        self.play(GrowFromCenter(line))
        self.wait()
        exp_ix = Tex(
            r"\e^{{{\i x}}}{{=1}}{{+\i x}}{{+{({{\i x}})^2\over2!}}}{{+{({{\i x}})^3\over3!}}}{{+{({{\i x}})^4\over4!}}}{{+{({{\i x}})^5\over5!}}}+\cdots"
            , tex_to_color_map=m).to_edge(DOWN, buff=1)
        exp_ix2 = Tex(
            r"\e^{{{\i x}}}{{=1}}{{+\i x}}{{-{x^2\over2!}}}{{-\i{{{x^3\over3!}}}}}{{+{x^4\over4!}}}{{+\i{{{x^5\over5!}}}}}+\cdots"
            , tex_to_color_map=m).move_to(exp_ix)
        exp_ix3 = Tex(
            r"\e^{{{\i x}}}{{=1}}{{-{x^2\over2!}}}{{+{x^4\over4!}}}{{+\cdots}}{{+\i x}}{{-\i{{{x^3\over3!}}}}}{{+\i{{{x^5\over5!}}}}}+\cdots"
            , tex_to_color_map=m).move_to(exp_ix)
        new3 = VGroup(Tex(r"{{\e^{\i x}=}}", tex_to_color_map=m).move_to(exp_ix3[:3]).align_to(exp_ix3, LEFT), Tex(
            r"{{1-{x^2\over2!}+{x^4\over4!}+\cdots}}{{+\i}} x-{{\i}}{{{x^3\over3!}}}+{{\i}}{{{x^5\over5!}}}+\cdots"
            , tex_to_color_map=m).move_to(exp_ix3).align_to(exp_ix3, RIGHT))
        exp_ix4 = VGroup(Tex(r"{{\e^{\i x}=}}", tex_to_color_map=m), Tex(
            r"{{\left({{1-{x^2\over2!}+{x^4\over4!}+\cdots}}\right)}} + \i {{\left({{x-{{{x^3\over3!}}}+{{{x^5\over5!}}}+\cdots}}\right)}}"
            , tex_to_color_map=m)).arrange().move_to(new3)
        new4 = VGroup(Tex(r"{{\e^{\i x}=}}", tex_to_color_map=m), Tex(
            r"{{\left(1-{x^2\over2!}+{x^4\over4!}+\cdots\right)}} + \i {{\left(x-{x^3\over3!}+{x^5\over5!}+\cdots\right)}}"
            , tex_to_color_map=m)).arrange().move_to(new3)
        euler = VGroup(Tex(r"{{\e^{\i x}=}}", tex_to_color_map=m), Tex(r"{{\cos x}} + \i {{\sin x}}"
                                                                       , tex_to_color_map=m)).arrange().move_to(new3)
        euler_conj = VGroup(Tex(r"{{\e^{- \i x}=}}", tex_to_color_map=m), Tex(r"{{\cos x}} - \i {{\sin x}}"
                                                                       , tex_to_color_map=m))\
            .arrange()
        euler_conj.next_to(euler[0], DOWN, submobject_to_align=euler_conj[0], aligned_edge=RIGHT)
        
        euler[1].shift(DOWN * .05)
        euler_conj[1].shift(DOWN * .05)
        self.play(Write(exp_ix), run_time=2)
        self.wait()
        self.play(RT(exp_ix[:3], exp_ix2[:3]),
                  RT(exp_ix[3:], exp_ix2[3:]))
        self.wait()
        self.play(
            TransformMatchingTex(exp_ix2, exp_ix3,
                                 path_arc=90 * DEGREES,
                                 transform_mismatches=True),
            run_time=2)
        self.wait()
        self.remove(exp_ix3)
        self.add(new3)
        self.play(RT(new3[0], exp_ix4[0]), TransformMatchingTex(new3[1], exp_ix4[1]), run_time=2)
        self.wait()
        self.remove(exp_ix4)
        self.add(new4)
        self.play(RT(new4[0], euler[0]),
                  TransformMatchingTex(new4[1], euler[1],
                                       key_map={r"\left(1-{x^2\over2!}+{x^4\over4!}+\cdots\right)": r"\cos x",
                                                r"\left(x-{x^3\over3!}+{x^5\over5!}+\cdots\right)": r"\sin x"},
                                       # fade_transform_mismatches=True
                                       ),
                  run_time=2)
        self.wait()
        self.play(euler.next_to, line, {"direction": DOWN, "buff": .5})
        box = SurroundingRectangle(euler)
        self.play(ShowCreation(box))
        self.wait()
        euler_label = TexText("Euler's formula", color=YELLOW).next_to(box, DOWN, buff=MED_LARGE_BUFF)
        self.play(Write(euler_label))
        self.wait()
        comment = TexText("绝对收敛的级数可以重排.", color=YELLOW)
        self.play(FadeOut(VGroup(sin, cos)))
        self.play(Write(comment))
        self.wait()
        self.remove(comment)
        self.wait()
        self.play(RT(exp[0:5], exp_lim[0:5]), RT(exp[5:], exp_lim[5:]))
        self.wait()
        self.play(TransformMatchingTex(exp_lim, exp_diff))
        self.wait()
        self.play(TransformMatchingTex(exp_diff, exp_real))
        self.wait()
        self.play(FadeOut(box), FadeOut(euler_label))
        self.wait()
        self.play(RT(euler[0].copy(), euler_conj[0]),
                  TransformMatchingTex(euler[1].copy(), euler_conj[1]),
                  run_time=2)
        self.wait()
        self.play(Write(cos_x))
        self.play(Write(sin_x))
        self.play(FadeOut(VGroup(line, euler, euler_conj)))
        self.wait()
        self.play(TransformMatchingTex(cos_x, cos_z, key_map={'x': 'z', '=': '\\coloneqq'}, transform_mismatches=True),
                  TransformMatchingTex(sin_x, sin_z, key_map={'x': 'z', '=': '\\coloneqq'}, transform_mismatches=True),
                  run_time=2)
        self.wait()
        line.next_to(sin_z, DOWN).set_x(0)
        self.play(GrowFromCenter(line))

        cos_ex = Tex(r"\cos {{(10\i)}}={\e^{-10}+\e^{10}\over 2}=\cosh(10)\approx 11013.2",
                     tex_to_color_map=m)\
            .next_to(line, DOWN, buff=.5)
        unbounded = TexText("$\\sin z, \\cos z$ 无界.", color=YELLOW).next_to(cos_ex, DOWN, buff=MED_LARGE_BUFF)
        self.play(Write(cos_ex))
        self.wait()
        self.play(Write(unbounded))
        self.wait()


class UnitCircle(Scene):
    def construct(self):
        plane = ComplexPlane(axis_config={
            "unit_size": 3
        },
            # x_range=[-8,8,3],
            # y_range=[-4,4,3]
        )
        plane.add_coordinate_labels()
        self.add(plane)
        x_unit = plane.get_x_unit_size()
        circle = Circle(radius=x_unit)
        self.add(circle)
        tracker = ValueTracker(30)
        deg = DecimalNumber(30, color=YELLOW, unit="^\\circ").add_background_rectangle()
        f_always(deg.set_value, tracker.get_value)
        always(deg.set_color, YELLOW)
        theta_eq = Tex("\\theta=").to_corner(UL, buff=1.5).add_background_rectangle()
        point = Dot(color=YELLOW)
        radius = Line()
        arc = Arc()
        theta = Tex("\\theta").add_background_rectangle()
        euler = Tex("\\e^{\\i\\theta}")
        always(deg.next_to, theta_eq)
        point.add_updater(
            lambda t: t.move_to(
                plane.n2p(
                    complex(np.cos(deg.get_value() * DEGREES), np.sin(deg.get_value() * DEGREES))
                )
            )
        )
        radius.add_updater(lambda t: t.become(Line(ORIGIN, point.get_center(), color=YELLOW)))
        coord = Tex("({{\\cos\\theta}}, {{\\sin\\theta}})").next_to(point)
        coord_complex = Tex("{{\\cos\\theta}}+{{\\i}}{{\\sin\\theta}}").next_to(point)
        bg = BackgroundRectangle(coord)
        arc.add_updater(lambda t: t.become(Arc(angle=deg.get_value() * DEGREES, radius=.6)))
        theta.add_updater(lambda t: t.move_to(
            plane.n2p(
                complex(np.cos(deg.get_value() * DEGREES / 2) / 3, np.sin(deg.get_value() * DEGREES / 2) / 3)
            )
        ))

        # animation part
        self.play(FadeIn(point), FadeIn(radius))
        self.play(Write(coord))
        self.wait()
        self.play(FadeIn(arc), FadeIn(theta))
        self.add(bg)
        self.play(TransformMatchingTex(coord, coord_complex, transform_mismatches=True))
        self.wait()
        euler.move_to(1.2*point.get_center())
        self.play(TransformMatchingShapes(coord_complex, euler))
        euler.add_background_rectangle()
        euler.add_updater(lambda t: t.move_to(1.2*point.get_center()))
        self.remove(bg)
        self.wait()
        self.play(Write(VGroup(theta_eq, deg)))

        self.play(tracker.increment_value, 260, run_time=6)
        self.play(tracker.set_value, 180, run_time=3)
        self.wait()

        identity = Tex("\\e^{\\i\\pi}+1=0", color=YELLOW).to_edge(LEFT, buff=1).shift(DOWN).add_background_rectangle()
        id_label = TexText("Euler's identity").next_to(identity, DOWN).add_background_rectangle()
        self.play(Write(identity))
        self.play(Write(id_label))
        self.wait()

        tracker.set_value(30)
        self.wait()
        self.play(tracker.increment_value, 360, run_time=5)
        arc.clear_updaters()
        theta.clear_updaters()
        self.play(FadeOut(arc), FadeOut(theta))
        self.wait()
        period_i = Tex(r"\e^{\i\theta}=\e^{\i(\theta+2k\pi)}", color=YELLOW).to_edge(RIGHT).shift(DOWN).add_background_rectangle()
        period = TexText(r"$e^z$~以~$2\pi\i$~为周期.",).scale(.9).add_background_rectangle().next_to(period_i, DOWN)
        self.play(Write(period_i))
        self.wait()
        self.play(Write(period))
        self.wait()

        polar = Tex("\\to r{{\\e^{\\i\\theta}}}", color=YELLOW).next_to(euler).add_background_rectangle()
        self.play(Write(polar))

class Prop(Scene):
    def construct(self):
        # to_isolate = [r"\e", "z"]
        one = Tex("1.").to_corner(UL, buff=1).shift(RIGHT)
        derivative = VGroup(
            Tex(r"(\e^z)'=\e^z", tex_to_color_map=m),
            Tex(r"(\sin z)'=\cos z", tex_to_color_map=m),
            Tex(r"(\cos z)'=-\sin z", tex_to_color_map=m),
        ).arrange(DOWN).align_to(one, UP)
        # self.play(Write(one))
        for t in derivative:
            self.play(Write(t))
        self.wait()

        two = Tex("2.").next_to(derivative, DOWN, buff=1).align_to(one, LEFT)
        identity = Tex("\\sin^2 z+\\cos^2 z=1", tex_to_color_map=m).align_to(two, UP)
        # self.play(Write(two))
        self.play(Write(identity))
        self.wait()

        three = Tex("3.").next_to(identity, DOWN, buff=1).align_to(one, LEFT)
        degrees = VGroup(
            Tex(r"\sin{{(z_1\pm z_2)}}=\sin z_1 \cos z_2 \pm \cos z_1 \sin z_2", tex_to_color_map=m2),
            Tex(r"\cos{{(z_1\pm z_2)}}=\cos z_1 \cos z_2 \mp \sin z_1 \sin z_2", tex_to_color_map=m2),
        ).arrange(DOWN).align_to(three, UP)
        # self.play(Write(three))
        for deg in degrees:
            self.play(Write(deg))
        self.wait()

        self.play(*[FadeOut(mob) for mob in self.mobjects])
        sin = VGroup(
            TexText("the zeros of {{$\\sin z$}}:"),
            Tex("z=k\\pi\\quad (k\\in\\mathbb{Z})")
        ).arrange(buff=.5).to_edge(UP, buff=2)

        cos = VGroup(
            TexText("the zeros of {{$\\cos z$}}:"),
            Tex("z=k\\pi+{\\pi \\over 2}\\quad (k\\in\\mathbb{Z})")
        ).arrange(buff=.5)
        sin[0][1].set_color(YELLOW)
        sin[1].shift(DOWN*.05)
        cos[0][1].set_color(YELLOW)
        cos[1].shift(DOWN*.05)
        self.play(Write(sin[0]))
        self.wait()
        self.play(Write(sin[1:]))
        self.wait()

        # proof part
        proofs = VGroup(
            Tex(r"{{\sin z}} {{=}} {{0}}"),
            Tex(r"{{{ {{\e^{{{ {{\i}} z}}}-\e^{{{- {{\i}} z}}}}} \over 2 {{\i}} }}} {{=}} {{0}}"),
            Tex(r"{{{{\e^{{{ {{\i}} z}}}-\e^{{{- {{\i}} z}}}}}}} {{=}} {{0}}"),
            Tex(r"\e^{{{ {{\i}} z}}} {{=}} \e^{{{- {{\i}} z}}}"),
            Tex(r"{{\e^{{{ {{2}} {{\i}} {{z}} }}}}} {{=}} {{1}}"),
        )
        proofs2 = VGroup(
            Tex(r"{{{{2}} {{\i}} {{z}}}} {{=}} {{0?}}"),
            Tex(r"{{2}} {{\i}} {{z}} {{=}} {{2 k\pi \i}}"),
            Tex(r"{{2}} {{\i}} {{z}} {{=}} {{2}} {{k\pi}} {{\i}}}}"),
            Tex(r"{{z}} {{=}} {{k\pi}}"),
        ).next_to(proofs, DOWN)
        for tex in proofs:
            tex.tm({r"\i": BLUE})
        for tex in proofs2:
            tex.tm({r"\i": BLUE})
        proofs2[1][-1].set_color(WHITE)
        proofs2[1][-1][-1].set_color(BLUE)
        self.play(Write(proofs[0]))
        for i in range(len(proofs)-1):
            if i == 0:
                self.play(TransformMatchingTex(proofs[i], proofs[i + 1]),
                          key_map={r"\sin z": r"{\e^{{{ {{\i}} z}}}-\e^{{{- {{\i}} z}}} \over 2 {{\i}} }"})
                self.wait()
            elif i == 1:
                self.play(TransformMatchingShapes(proofs[i], proofs[i + 1]), )
                self.wait()
            elif i == 2:
                self.play(TransformMatchingShapes(proofs[i], proofs[i + 1], path_arc = 90*DEGREES))
                self.wait()

            elif i == 4:
                self.play(TransformMatchingShapes(proofs[i], proofs[i + 1]),
                          key_map={r"1": r"0?", r"\e^{{{ {{2}} {{\i}} {{z}} }}}": r"{{2}} {{\i}} {{z}}"},
                          # fade_transform_mismatches=True
                          )
                self.wait()
            else:
                self.play(TransformMatchingTex(proofs[i], proofs[i+1]), transform_mismatches=True)
                self.wait()
        self.play(TransformMatchingTex(proofs[-1].copy(), proofs2[0]))
        self.wait()
        self.play(TransformMatchingTex(proofs2[0], proofs2[1]))
        self.wait()
        self.remove(proofs2[1])
        self.add(proofs2[2])
        self.play(TransformMatchingTex(proofs2[2], proofs2[3]))
        self.wait()

        self.play(FadeOut(proofs[-1]), FadeOut(proofs2[-1]))
        self.play(Write(cos[0]))
        self.wait()
        self.play(Write(cos[1]))
        self.wait()

class CexpPic(Scene):
    def construct(self):
        one = Tex(r"\e^{{{\i\pi}}}=\e^{{{3\i\pi}}}", tex_to_color_map=m).scale(3)
        two = Tex(r"\cos{(?)}>10,000", tex_to_color_map={"?": YELLOW}).scale(3)
        v = VGroup(one, two).arrange(DOWN, buff=1.5)
        self.add(v)


