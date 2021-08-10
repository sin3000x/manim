from manimlib import *

M = {"z": YELLOW, "alpha": BLUE}


class Open(Scene):
    def construct(self):
        t = Vocabulary()
        self.add(t)
        eng = ['power function', 'root of unity', 'branch cut', 'chain rule']
        chi = ['幂函数', '单位根', '支割线', '链式法则']
        eng = VGroup(*[TexText(s) for s in eng]).scale(1.2).arrange(DOWN, aligned_edge=LEFT, buff=.6)
        chi = VGroup(*[TexText(s) for s in chi]).scale(1.2).arrange(DOWN, aligned_edge=LEFT)

        for c, e in zip(chi, eng):
            c.align_to(e, DOWN)

        v = VGroup(eng, chi).arrange(buff=2).next_to(t, DOWN, buff=.8)
        box = SurroundingRectangle(v, color=GREEN, stroke_width=8, buff=.3)
        self.add(eng, chi, box)
        self.wait(5)


class Def(Scene):
    def construct(self):
        power = Tex(r"{{z}}^{{\alpha}}\coloneqq \e^{ {{\alpha}}\ln {{z}}}").to_edge(UP, buff=1).tm(M)
        self.play(Write(power))

        ln_multi = Arrow(ORIGIN, UP).next_to(power[-2], DOWN)
        ln_multi = VGroup(ln_multi, TexText("多值的").scale(.8).next_to(ln_multi, DOWN)).set_color(GREEN)
        pow_multi = ln_multi.copy().next_to(power[:2], DOWN)
        self.play(GrowArrow(ln_multi[0]), GrowFromCenter(ln_multi[1]))
        self.wait()
        self.play(GrowArrow(pow_multi[0]), GrowFromCenter(pow_multi[1]))
        self.wait()
        self.play(FadeOut(ln_multi), FadeOut(pow_multi))
        self.wait()

        calc = Tex(r"\left({{r}}\e^{\i{{\theta}} }\right)^{{\alpha}}={{r}}^{{\alpha}} \e^{\i{{\alpha}}{{\theta}} }",
                   to_isolate=['\\theta', '\\alpha']).next_to(power, DOWN, buff=.5)\
            .tm({'alpha': BLUE})
        self.play(Write(calc))
        self.wait()

        ex = VGroup(Tex(r"1^{{\frac 16}}"),
                    Tex(r"{{=}}"),
                    Tex(r"\left(\e^{\i\cdot 2k\pi}\right)^{{\frac 16}}")).arrange().next_to(calc, DOWN, buff=1)
        ex2 = Tex(r"=\e^{\i\frac k3\pi}").next_to(ex[1], DOWN, aligned_edge=LEFT, buff=.5)
        self.play(Write(ex[0:2]))
        self.wait()
        self.play(TransformMatchingTex(ex[0].copy(), ex[2]))
        self.wait()
        self.play(Write(ex2))
        self.wait()


class Unity(Scene):
    def construct(self):
        plane = ComplexPlane(axis_config={"unit_size": 3}).add_coordinate_labels()
        self.add(plane)
        circle = Circle(radius=plane.get_x_unit_size(), color=RED)
        self.add(circle)

        num0 = complex(np.cos(PI/3), np.sin(PI/3))
        dots = [Dot(color=YELLOW).move_to(plane.n2p(num0**i)) for i in range(6)]
        dots = VGroup(*dots)

        labels = VGroup()
        for i in range(6):
            label = Tex(r"\e^{\i \frac{%s}{3}\pi}" % i, color=YELLOW).scale(1.2).add_background_rectangle()
            label.move_to(dots[i].get_center()*1.25)
            labels.add(label)

        lines = [Line(dots[i].get_center(), dots[i+1].get_center(), color=YELLOW) for i in range(5)]
        lines = VGroup(*lines).add(Line(dots[5], dots[0], color=YELLOW))

        for i in range(6):
            self.play(GrowFromCenter(dots[i]), FadeIn(labels[i]))

        self.wait()
        self.play(ShowCreation(lines), run_time=3)
        self.wait()

        general = Tex(r"1^{\frac 1n}=\e^{\frac{2\pi}{n}k\i}", color=YELLOW)\
            .scale(1.5).add_background_rectangle().to_edge(UL)
        self.play(FadeOut(labels))
        self.play(Write(general))
        self.wait()

        from_center = [Line(ORIGIN, dot.get_center(), color=GREEN, stroke_width=8) for dot in dots]
        from_center = VGroup(*from_center)
        self.play(*[ShowCreation(l) for l in from_center])
        self.play(from_center[2:].fade, .8)

        arc = Arc(radius=.8, angle=PI/3 ,color=YELLOW)
        arc = VGroup(arc, Tex(r"\frac{2\pi}{n}", color=YELLOW).move_to(arc.get_center()*2).add_background_rectangle())
        self.play(GrowFromCenter(arc[0]))
        self.play(Write(arc[1]))
        self.wait()

        roots = TexText("$z^n=1$", color=YELLOW)\
            .scale(1.5).to_corner(UR, buff=.5).align_to(general, DOWN).add_background_rectangle()
        unity = TexText("单位根", color=GREEN).next_to(roots, DOWN, buff=1)
        arrow = Arrow(unity.get_top(), roots.get_bottom()).set_color(unity.get_color())
        self.play(Write(roots))
        self.wait()
        self.play(GrowFromCenter(arrow), GrowFromCenter(unity))
        self.wait()


class Multi(Scene):
    def construct(self):
        title = TexText("\\heiti $z^\\alpha$ 多值个数", color=YELLOW).to_edge(UP)
        box = SurroundingRectangle(title)
        # title[0][1].set_color(BLUE)
        self.play(Write(title))
        self.play(ShowCreation(box))
        self.wait()

        pq = Tex("{{\\alpha}}={{\\frac pq}}\\quad(p,q~\\text{互质且}~q>0):~q\\text{~个值.}")\
            .tm({"pq": YELLOW, "alpha": BLUE}).next_to(title, DOWN, buff=.5)
        sqrt = Tex(r"4^{\frac12}=\left(4\e^{2k\pi\i}\right)^{\frac 12}=2\e^{k\pi\i}=\pm2", color=GREEN).next_to(pq, DOWN)

        self.play(Write(pq))
        self.wait()
        self.play(Write(sqrt), run_time=3)
        self.wait()

        integer = Tex("{{\\alpha}}={{n}}:~\\text{一个值.}")\
            .tm({"n": YELLOW, "alpha": BLUE}).next_to(sqrt, DOWN, buff=.5).align_to(pq, LEFT)
        square = Tex(r"3^2=\left(3\e^{2k\pi\i}\right)^2=9\e^{4k\pi\i}=9", color=GREEN).next_to(integer, DOWN).set_x(0)
        self.play(Write(integer))
        self.wait()
        self.play(Write(square))
        self.wait()

        other = Tex("{{\\alpha}}={{\\text{无理数/非实数}}}:~\\text{无数个值.}")\
            .tm({"无理数": YELLOW, "alpha": BLUE}).next_to(square, DOWN, buff=.5).align_to(pq, LEFT)
        self.play(Write(other))
        self.wait()
        ii = Tex(r"\i^\i=\left(\e^{\i(\frac \pi2+2k\pi)}\right)^\i=\e^{-(\frac \pi2+2k\pi)}", color=GREEN)\
            .next_to(other, DOWN).set_x(0)
        self.play(Write(ii))
        self.wait()


class Branch(Scene):
    def construct(self):
        plane = ComplexPlane().add_coordinate_labels()
        cut = BranchCut()
        self.add(plane)
        self.play(ShowCreation(cut))
        self.wait()

        sqrt = Tex(r"4^{\frac 12}=\e^{\frac 12\ln4}=\e^{\frac 12(\ln|4|+\i\arg(4))}=\e^{\ln2}=2", color=GREEN) \
            .scale(1.2).to_edge(UP, buff=1).add_background_rectangle()
        self.play(Write(sqrt), run_time=3)
        # for i, s in enumerate(sqrt[1]):
        #     self.add(Text(str(i), color=PINK).move_to(s).scale(.5))

        arrow = Arrow(ORIGIN, UP).set_color(YELLOW).next_to(sqrt[1][9:11], DOWN)
        arrow2 = arrow.copy().next_to(sqrt[1][34:36], DOWN)
        C = Tex("\\mathbb{C}", color=YELLOW).next_to(arrow, DOWN)
        R = Tex("\\mathbb{R}", color=YELLOW).next_to(arrow2, DOWN)
        self.play(GrowArrow(arrow))
        self.play(Write(C))
        # self.wait()
        self.play(GrowArrow(arrow2))
        self.play(Write(R))
        self.wait()

        diff = Tex(r"(z^{\alpha})'=\left(\e^{\alpha \ln z}\right)'=\e^{\alpha \ln z}(\alpha \ln z)'"
                   r"=\alpha z^{\alpha}\frac 1z", color=YELLOW).to_edge(DOWN, buff=2).add_background_rectangle()
        self.play(Write(diff), run_time=3)
        self.wait()
        # for i, s in enumerate(diff[1]):
        #     self.add(Text(str(i), color=PINK).move_to(s).scale(.5))
        arrow3 = arrow.copy().next_to(diff[1][-1], DOWN)
        self.play(GrowArrow(arrow3))
        self.wait()
        self.play(FadeOut(arrow3))
        cube = Tex(r"{{z^3}}\coloneqq z\cdot z\cdot z", color=GREEN).next_to(diff, DOWN).add_background_rectangle(buff=.3)
        self.play(FadeIn(cube[0]))
        self.play(Write(cube[1]))
        self.wait()
        # for i, s in enumerate(cube[1]):
        #     self.add(Text(str(i), color=PINK).move_to(s).scale(.5))
        self.play(Write(cube[2:]))
        self.wait()

class Pic(Scene):
    def construct(self):
        t = Tex("2^{\\i}").scale(6)
        self.add(t)