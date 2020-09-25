from manimlib.imports import *


class attain(GraphScene, MovingCameraScene):
    CONFIG = {
        "x_min": 0,
        "x_max": 1.1,
        "y_min": 0,
        "y_max": 1.1,
        "x_axis_width": 3,
        "y_axis_height": 3,
        "graph_origin": 3.2 * DOWN + 5.8 * LEFT,
    }

    def construct(self):
        # opening
        title = TextMobject("\\underline{\\heiti 最值定理}", color=YELLOW).to_corner(UL)
        theorem = TextMobject("连续函数在闭区间上可取到最大值与最小值.", color=YELLOW).next_to(title, DOWN).set_x(0)
        self.play(Write(title))
        self.play(Write(theorem), run_time=2)
        self.wait(2)

        # explain
        e1 = TexMobject("\\text{【解释】~}", "f(x)\\text{在}", "[a,b]\\text{上有最大值点}", "\\xi", "\\text{，最小值点}", "\\eta",
                        "\\text{，}", ) \
            .set_color_by_tex_to_color_map({"xi": RED, "eta": BLUE}) \
            .next_to(theorem, DOWN, buff=MED_LARGE_BUFF).align_to(title, LEFT)
        e1_1 = TexMobject("\\text{使 }", "f(", "\\eta", ")", "\\leq f(x)\\leq f(", "\\xi", ")", "\\text{ 恒成立.}") \
            .set_color_by_tex_to_color_map({"xi": RED, "eta": BLUE}) \
            .next_to(e1, DOWN).align_to(e1[1], LEFT)
        self.play(Write(e1), run_time=2)
        self.wait()
        self.play(Write(e1_1))
        self.wait()

        # plotting
        self.setup_axes(animate=True)
        f1 = lambda x: x ** 2 - 0.5 * x + 0.5
        f2 = lambda x: x
        f3_1 = lambda x: 2 * x
        f3_2 = lambda x: 0.5

        graphs = [self.get_graph(f, x_max=1, x_min=0) for f in [f1, f2]]
        graph3_1 = self.get_graph(f3_1, x_min=0, x_max=0.5, color=YELLOW)
        graph3_2 = self.get_graph(f3_2, x_max=1, x_min=0.5, color=YELLOW)
        dots1 = VGroup(Dot().move_to(graphs[0].points[0]), Dot().move_to(graphs[0].points[-1]))
        dots2 = VGroup(Circle(radius=DEFAULT_DOT_RADIUS).move_to(graphs[1].points[0]),
                       Circle(radius=DEFAULT_DOT_RADIUS).move_to(graphs[1].points[-1]))
        dots3 = VGroup(Dot().move_to(graph3_1.points[0]),
                       Circle(radius=DEFAULT_DOT_RADIUS).move_to(self.coords_to_point(0.5, 1)),
                       Dot().move_to(self.coords_to_point(0.5, 0.5)), Dot().move_to(graph3_2.points[-1]))

        # first
        self.play(ShowCreation(graphs[0]))
        self.play(FadeIn(dots1))
        # self.wait()
        extreme = Dot().move_to(self.coords_to_point(0.25, f1(0.25)))
        lineh = DashedLine(self.coords_to_point(0, f1(.25)), self.coords_to_point(.25, f1(.25)))
        linev = DashedLine(self.coords_to_point(.25, f1(.25)), self.coords_to_point(.25, 0))

        lineh2 = DashedLine(self.coords_to_point(0, f1(1)), self.coords_to_point(1, f1(1)))
        linev2 = DashedLine(self.coords_to_point(1, f1(1)), self.coords_to_point(1, 0))

        M = TexMobject("f", "(", "\\xi", ")").set_color_by_tex("xi", RED).next_to(lineh2[0], LEFT)
        m = TexMobject("f", "(", "\\eta", ")").set_color_by_tex("eta", BLUE).next_to(lineh[0], LEFT)
        xi = TexMobject("\\xi", color=RED).next_to(linev2[-1], DOWN)
        eta = TexMobject("\\eta", color=BLUE).next_to(linev[-1], DOWN)

        self.play(GrowArrow(lineh))
        self.play(FadeIn(extreme))
        self.play(Write(m))
        self.play(GrowArrow(linev))
        self.play(Write(eta))
        # self.wait()

        self.play(GrowArrow(lineh2))
        self.play(Write(M))
        self.play(GrowArrow(linev2))
        self.play(Write(xi))
        self.wait()

        self.play(FadeOut(graphs[0]), FadeOut(dots1),
                  FadeOut(VGroup(M, m, xi, eta, linev, lineh, linev2, lineh2, extreme)))

        # second
        self.play(ShowCreation(graphs[1]))
        self.play(FadeIn(dots2))
        second = TextMobject("{\\kaishu 这个上确界取不到，因为不是\\underline{闭区间}}.", color=RED).next_to(dots2[-1], RIGHT,
                                                                                             buff=MED_LARGE_BUFF)
        self.play(Write(second))
        self.wait(2)
        self.play(FadeOut(graphs[1]), FadeOut(dots2), FadeOut(second))

        # third
        self.play(ShowCreation(graph3_1))
        self.play(ShowCreation(graph3_2))
        self.play(FadeIn(dots3))
        third = TextMobject("\\kaishu 这个上确界取不到，因为不是\\underline{连续函数}.", color=RED).next_to(self.coords_to_point(0.5, 1),
                                                                                           RIGHT, buff=MED_LARGE_BUFF)
        self.play(Write(third))
        self.wait(2)
        self.play(FadeOut(graph3_1), FadeOut(graph3_2), FadeOut(dots3), FadeOut(third), FadeOut(self.axes))

        # proof start
        l1 = TextMobject("【证明】~", "由于$f(x)$的值域非空有界，故有上下确界.")
        l2 = TextMobject("依据是", "确界原理", ".")
        l2[1].set_color(YELLOW)
        l3 = TextMobject(r"反证.", r"首先假设$f(x)$取不到", r"$\sup f$", "这个数：").set_color_by_tex("sup", GREEN)
        l4 = TexMobject(r"f(x)<", r"\sup f", r",~\forall x\in [a,b]").set_color_by_tex("sup", GREEN)
        l5 = TextMobject("然而实际上$f(x)$可以无限接近", r"$\sup f$", "...").set_color_by_tex("sup", GREEN)
        l6 = TextMobject("怀着看热闹不嫌事大的心态，我们构造函数")
        l7 = TexMobject(r"{1 \over{", r"\sup", r"f", r"-", "f(x)}}", r",~x\in [a,b]")
        l7[1:3].set_color(GREEN)
        l8 = TextMobject("由假设它也是一个连续函数，于是有上界$M>0$：")
        l9 = TexMobject(r"{1 \over{", r"\sup", r"f", r"-", "f(x)}}", r"\leq", "M")
        l9[1:3].set_color(GREEN)
        l10 = TextMobject(r"整理一下：")
        l11 = TexMobject("f(x)", r"\leq", r"\sup", " f", "-", "{", "1", r"\over", "M", "}")
        l11[2:4].set_color(GREEN)
        v = VGroup(l1, l2, l3, l4, l5, l6, l7, l8, l9, l10, l11).arrange(DOWN).next_to(e1_1, DOWN)
        for i, _ in enumerate(v):
            if i == 0:
                _.align_to(e1, LEFT)
            else:
                _.align_to(e1[1], LEFT)
        l4.set_x(0)
        l7.set_x(0)
        l9.set_x(0)
        l11.set_x(0)

        self.play(Write(l1))
        self.wait()
        self.play(Write(l2))
        self.wait()
        self.play(Write(l3[0]))
        self.wait()
        self.play(Write(l3[1:]))
        self.wait()
        self.play(Write(l4))
        self.wait()

        # scroll down
        self.camera.frame.save_state()
        self.play(self.camera.frame.shift, DOWN * (title.get_top()[1] - l3.get_center()[1]), run_time=2)
        self.wait()

        self.play(Write(l5))
        self.wait()
        self.play(Write(l6), run_time=2)
        self.wait()
        self.play(Write(l7))
        self.wait()
        self.play(Write(l8), run_time=2)
        self.wait()
        self.play(Write(l9))
        self.wait()

        # scroll down, again
        self.play(self.camera.frame.shift, DOWN * (l3.get_top()[1] - l8.get_top()[1]), run_time=2)
        self.wait()

        self.play(Write(l10))
        self.wait()
        self.play(ReplacementTransform(l9.copy(), l11))
        self.wait()

        l12 = TextMobject("这样，我们就找到了一个比", r"$\sup f$", "还要小的上界.")
        l13 = TextMobject("这与上确界的定义矛盾.", r"故$f(x)$取到最大值.")
        l14 = TextMobject("另一方面，推出$-f(x)$也取到最大值.")
        l15 = TextMobject("即$f(x)$取到最小值.")
        end = TexMobject(r"\blacksquare")
        v2 = VGroup(l12, l13, l14, l15, end).arrange(DOWN).next_to(l11, DOWN)
        for _ in v2:
            _.align_to(l10, LEFT)
        end.to_edge(RIGHT).shift(UP * .5)

        self.play(Write(l12))
        self.wait()
        self.play(Write(l13[0]), run_time=2)
        self.wait()
        self.play(Write(l13[1]), run_time=2)
        self.wait()
        self.play(Write(l14), run_time=3)
        self.wait(2)
        self.play(Write(l15), run_time=2)
        self.wait()
        self.play(Write(end))
        self.wait(2)

        self.play(Restore(self.camera.frame), run_time=3)
        self.wait()


class test(Scene):
    def construct(self):
        t = TexMobject(r"{1 \over{", r"\sup", r"f", r"-", "f(x)}}", )
        # t[4:6].set_color(GREEN)
        t2 = TexMobject(r"{ 1 \over { \sup f - f(x) } } \leq M")
        t3 = TexMobject(r"{1 \over {\sup f-f(x)}}~x\in[a,b]")
        self.play(Write(t))
        self.wait()
