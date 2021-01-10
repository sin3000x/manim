from manimlib.imports import *


class opening(GraphScene):
    CONFIG = {
        "x_min": 0,
        "x_max": 4,
        "x_tick_frequency": 4,
        "y_min": -2,
        "y_max": 4.5,
        "y_tick_frequency": 6.5,
        "x_axis_width": 5,
        "y_axis_height": 6,
        "graph_origin": 1.8 * DOWN + 5 * LEFT,
    }

    def construct(self):
        map = {"f": RED, "gamma": YELLOW, "xi": BLUE, "exists": WHITE, "Fermat": YELLOW, "x_0": YELLOW}
        title = myTitle("Darboux中值定理", color=YELLOW).to_corner(UL)
        pre = TextMobject("$f$", "在$[a,b]$可导，那么").tm(map)
        th1 = TextMobject("(1)~", "$f'$", "可取到", r"$f'$", "$(a)$", r"与", r"$f'$", "$(b)$", r"间的一切值.")
        th2 = TextMobject("(2)~", "$f'$", "无第一类间断点.")
        th = VGroup(pre, th1, th2).arrange(DOWN, aligned_edge=LEFT).next_to(title, DOWN, aligned_edge=LEFT)
        pre.set_x(0)

        func = VGroup(TexMobject(r"x^2 \sin \left(\tfrac 1x \right)\quad", r"x\neq 0"),
                      TexMobject(r"0\quad", r"x=0")).arrange(DOWN, aligned_edge=LEFT).next_to(th, DOWN, buff=1)
        # func = TexMobject(r"f(x)=\left\{\begin{array}{ll} x^{2} \sin \left(\frac{1}{x}\right) & x \neq 0 \\0 & x=0\end{array}\right.").next_to(th, DOWN)
        func[1][1].align_to(func[0][1], LEFT)
        func_label = VGroup(TexMobject("f", "(x)=").tm(map), Brace(func, LEFT, width_multiplier=3))
        func_label[0].next_to(func_label[1], LEFT)
        self.play(Write(title))
        self.wait()
        for t in th:
            t.tm(map)
            self.play(Write(t), run_time=2)
            self.wait()

        self.play(GrowFromCenter(func_label))
        self.wait()
        self.play(Write(func[0]))
        self.play(Write(func[1]))
        # self.play(Write(func))
        self.wait()
        plot = ImageMobject('plot').scale(2).next_to(func, RIGHT, buff=1)
        fdash = TexMobject("f'", "(x)").tm(map).next_to(plot, DOWN)
        self.add_sound('pop')
        self.add(plot, fdash)
        self.wait()

        # first part start
        th1.save_state()
        th2.save_state()
        self.play(FadeOut(VGroup(fdash, func, func_label,
                                 title, pre, th2)),
                  FadeOut(plot),
                  th1.to_edge, UP)
        self.wait()
        self.setup_axes(True)
        f = lambda x: (x - 1) ** 3 - 2 * (x - 1) ** 2 + 3
        graph = self.get_graph(f, x_min=0.1, x_max=3.2, color=RED)

        f_label = TexMobject(*r"f'(x) - \gamma = 0".split()).scale(1.5).to_edge(RIGHT, buff=2)
        f_label2 = TexMobject(*r"f'(x) = \gamma".split()).scale(1.5).move_to(f_label)
        f_label[0].set_color(RED)
        f_label[2].set_color(YELLOW)
        f_label2[0].set_color(RED)
        f_label2[2].set_color(YELLOW)

        self.play(ShowCreation(graph), Write(f_label[0]))

        x_ticks = VGroup(
            self.x_axis.get_tick(0.1), self.x_axis.get_tick(3.2),
        )
        y_lines = VGroup(
            DashedLine(self.coords_to_point(0, f(.1)), self.coords_to_point(.1, f(.1))),
            DashedLine(self.coords_to_point(0, f(3.2)), self.coords_to_point(3.2, f(3.2))),
        )
        labels = VGroup(
            TexMobject("f'", "(a)").tm(map).next_to(y_lines[0], LEFT),
            TexMobject("f'", "(b)").tm(map).next_to(y_lines[1], LEFT),
            # TexMobject("a").next_to(x_ticks[0], DOWN),
            # TexMobject("b").next_to(x_ticks[1], DOWN),
        )

        # labels[-1].align_to(labels[-2], DOWN)
        gamma_value = .3
        gamma = VGroup(
            DashedLine(self.coords_to_point(0, f(gamma_value)), self.coords_to_point(gamma_value, f(gamma_value)),
                       color=YELLOW),
            self.x_axis.get_tick(gamma_value).set_color(YELLOW)
        )
        gamma_label = TexMobject(r"\gamma", color=YELLOW).next_to(gamma[0], LEFT)

        self.play(ShowCreation(y_lines[0]), ShowCreation(y_lines[1]))
        self.play(FadeIn(labels))
        self.wait()
        self.play(Write(gamma_label))
        self.play(ShowCreation(gamma[0]))
        self.wait()

        to_move = VGroup(graph, y_lines, gamma[0],
                         labels, gamma_label)
        y_unit = self.coords_to_point(0, 1) - self.coords_to_point(0, 0)
        self.play(to_move.shift, -f(gamma_value) * y_unit, Write(f_label[1:3]), run_time=2)
        labels2 = VGroup(
            TexMobject("f'", "(a)", "-", r"\gamma").tm(map).scale(.9).next_to(y_lines[0], LEFT),
            TexMobject("f'", "(b)", "-", r"\gamma").tm(map).scale(.9).next_to(y_lines[1], LEFT),
        )
        gamma_label2 = TexMobject(r"0", color=YELLOW).next_to(gamma[0], LEFT)
        self.wait()
        self.play(Write(f_label[3:]))
        self.wait()
        self.play(
            RT(f_label[0], f_label2[0]),
            RT(f_label[3], f_label2[1]),
            FadeOut(f_label[1]),
            FadeOut(f_label[4]),
            RT(f_label[2], f_label2[2], path_arc=np.pi),
        )
        self.wait()
        self.play(FadeOut(f_label2))

        suffice_map = {"f": RED, "gamma": YELLOW}
        suffice = VGroup(
            TextMobject('只需证明', '``零点定理",'),
            TexMobject(r"\text{再构造~}", "F(x)=", r"f(x)", r"-", r"\gamma", " x", r"\text{~即可.}").tm(suffice_map),
            TexMobject(r"\Longrightarrow", "F'(x)=", *r"f'(x) - \gamma".split(), r"\text{~,就有}").tm(suffice_map),
            TexMobject(*r"F'(a) = f' (a) - \gamma".split()).tm(map),
            TexMobject(*r"F'(b) = f' (b) - \gamma".split()).tm(map),
            TexMobject(*r"\Longrightarrow F'( \xi )= f' ( \xi ) - \gamma = 0".split()).tm(map),
            TexMobject(*r"\Longrightarrow f' ( \xi ) = \gamma".split()).tm(map),
        ).arrange(DOWN, aligned_edge=LEFT).to_edge(RIGHT)
        bg = BackgroundRectangle(suffice)
        differ = VGroup(Brace(suffice[3:5], RIGHT), TextMobject("异号").tm(map))
        differ[1].next_to(differ[0], RIGHT)
        xi = TexMobject(r"\xi", color=BLUE) \
            .next_to(self.coords_to_point(gamma_value, 0), DOWN).shift(UR * .1)
        F_label = TexMobject("F'(x)").scale(1.5).next_to(self.x_axis, DOWN, buff=1).shift(LEFT * .3)
        self.play(FadeIn(bg))
        for line in suffice[:2]:
            self.play(Write(line), run_time=2)
            self.wait()
        self.play(Write(suffice[2]), Write(F_label))
        self.wait()
        self.play(Write(suffice[3]))
        self.play(Write(suffice[4]))
        self.play(
            RT(labels[0][:2], labels2[0][:2]),
            RT(labels[1][:2], labels2[1][:2]),
            Write(labels2[0][2:]),
            Write(labels2[1][2:]),
            RT(gamma_label, gamma_label2),
        )
        self.wait()
        self.play(GrowFromCenter(differ))
        self.wait()
        self.play(Write(suffice[5]), Write(xi))
        self.wait()
        self.play(Write(suffice[6]))
        self.wait()

        self.play(FadeOut(VGroup(
                                 suffice[1:], differ)),
            bg.set_opacity, 0
                  )
        self.play(FadeOut(VGroup(self.axes, F_label, gamma_label2, labels2, graph, xi,
                                 y_lines, gamma[0])),
                  suffice[0].align_to, th1[1], LEFT,run_time=2)
        self.wait()

        # zero theorem
        ##################  0   1  2   3  4 5         6           7      8          9              10
        th0 = TexMobject(
            *r"f' (a) f' (b) < 0 ~\Longrightarrow~ \exists \xi \in(a,b),~\text{s.t.}~ f' ( \xi )=0".split()) \
            .tm(map).next_to(suffice[0], DOWN).set_x(0)
        self.play(RT(suffice[0][1], th0))
        self.wait()
        self.play(WiggleOutThenIn(th0[:6]))
        self.wait()
        self.play(WiggleOutThenIn(th0[10:]))
        self.wait()

        wlog = TexMobject(r"\text{【证】}", r"\text{不妨设~} ", r"f'", r" (a)", ">", "0", r", ", r"f'", r" (b)<0", ".").tm(
            map).next_to(th0, DOWN, buff=.5).align_to(suffice[0], LEFT)
        self.play(Write(wlog))
        self.wait()

        box = SurroundingRectangle(wlog[2:6], color=YELLOW)
        box_b = SurroundingRectangle(wlog[-3:-1])
        self.play(ShowCreation(box))
        self.wait()
        imply = VGroup(TexMobject(r"\text{在~}a\text{~的右邻域内：}"), TexMobject(*"f (x)> f (a)".split()).tm(map)) \
            .arrange().next_to(wlog, DOWN).align_to(wlog[1], LEFT)
        imply2 = TexMobject(r"\text{在~}b\text{~的左邻域内：}", *"f (x) > f (b)") \
            .tm(map).next_to(imply, DOWN, aligned_edge=LEFT)
        imply2[1:].align_to(imply[1], LEFT)
        box_con = SurroundingRectangle(imply[1])
        mono = TexMobject("f", "(x)", r"\text{~单调递增}").tm(map).next_to(imply[1], DOWN, aligned_edge=LEFT)
        cro = Cross(mono)
        self.play(Write(imply[0]))
        self.wait()
        self.play(Write(imply[1:]))
        self.wait()
        self.play(Write(mono))
        self.play(ShowCreation(cro))
        self.wait()

        self.play(FadeOut(VGroup(cro, mono)))

        ####################  0        1   2    3   4  5    6      7
        fa = TexMobject(*r"\lim_{x\to a^+} {{f (x)- f (a)} \over {x-a}} > 0".split()) \
            .tm(map).next_to(imply, DOWN).set_x(box.get_x())
        box_whole = SurroundingRectangle(fa[2:])
        box_de = SurroundingRectangle(fa[7])
        box_nu = SurroundingRectangle(fa[2:6])
        self.play(
            RT(wlog[2:6].copy()[:-2], fa[:-2]),
            RT(wlog[2:6].copy()[-2:], fa[-2:]),
        )
        self.wait()
        self.play(ShowCreation(box_whole))
        self.wait()
        self.play(RT(box_whole, box_de))
        self.wait()
        self.play(RT(box_de, box_nu))
        self.wait()
        self.play(RT(box_nu, box_con))
        self.wait()
        self.play(FadeOut(VGroup(box_con, fa)))

        self.x_min, self.x_max = 0, 2.2
        self.y_min, self.y_max = 0, 2.5
        self.y_bottom_tick = 0
        self.x_tick_frequency, self.y_tick_frequency = self.x_max, self.y_max
        self.graph_origin = 2.5 * DOWN + 3 * RIGHT
        self.x_axis_width, self.y_axis_height = 3, 3
        self.setup_axes(True)
        f = lambda x: -(x - 1.5) ** 2 + 2
        graph1 = self.get_graph(f, x_min=0.2, x_max=.3, color=RED)
        graph2 = self.get_graph(f, x_min=0.3, x_max=1.8, color=RED)
        graph3 = self.get_graph(f, x_min=1.8, x_max=2, color=RED)
        ticks = VGroup(self.x_axis.get_tick(.2), self.x_axis.get_tick(2))
        labels = VGroup(
            TexMobject("a").next_to(ticks[0], DOWN),
            TexMobject("b").next_to(ticks[1], DOWN),
        )
        labels[1].align_to(labels[0], DOWN)
        self.play(FadeIn(ticks))
        self.play(FadeIn(labels))
        self.play(ShowCreation(graph1))
        self.wait()

        self.play(RT(box, box_b))
        self.play(Write(imply2))
        self.play(ShowCreation(graph3))
        self.wait()

        not_max = TexMobject(*r"\Longrightarrow~ f (a), f (b)".split(), r"\text{~都不是最大值.}") \
            .tm(map).next_to(imply2, DOWN, aligned_edge=LEFT)
        at_xi = TexMobject(r"\Longrightarrow~", r"\text{最大值于内点~}", r"\xi", r"\text{~上取到.}") \
            .tm(map).next_to(not_max, DOWN, aligned_edge=LEFT)
        xi_dot = Dot(self.coords_to_point(1.5, f(1.5)), color=BLUE)
        xi.next_to(xi_dot, UP)
        conclusion = TexMobject(*r"\Longrightarrow f' ( \xi )=0\quad".split(), r"\text{(Fermat)}") \
            .tm(map).next_to(at_xi, DOWN, aligned_edge=LEFT)
        self.play(Write(not_max), FadeOut(box_b))
        self.wait()
        self.play(Write(at_xi), run_time=2)
        self.play(ShowCreation(graph2))
        self.play(FadeIn(xi_dot))
        self.play(Write(xi))
        self.wait()
        self.play(Write(conclusion))
        self.wait()

        # second part
        th2.move_to(th1).align_to(th1, LEFT)
        to_fade = list(self.mobjects)
        to_fade.remove(th1)
        self.play(*[FadeOut(mob) for mob in to_fade])
        self.play(
            RT(th1[0], th2[0]),
            RT(th1[1], th2[1]),
            RT(th1[2:], th2[2:]),
        )
        self.wait()

        proof = TextMobject("反证.", "假设", "$x_0$", "是", "$f'$", "的第一类间断点.").tm(map).next_to(th2[1:], DOWN,
                                                                                           aligned_edge=LEFT)
        self.play(Write(proof[0]))
        self.play(Write(proof[1:]))
        self.wait()
        ie = TexMobject(*r"\text{则~} f' ( x_0 +),~ f' ( x_0 -)\text{~存在.}".split()).tm(map).next_to(proof, DOWN,
                                                                                                    aligned_edge=LEFT)
        self.play(Write(ie))
        self.wait()

        fx0 = TexMobject(*r"f' ( x_0 ) = \lim_ {x \to x_0} {{f (x) - f ( x_0 )} \over {x - x_0}}".split()) \
            .tm(map).next_to(ie, DOWN).set_x(0)
        lim_pos = TexMobject(*r"\lim_ {x \to x_0 ^+}".split()) \
            .move_to(fx0[5:9])
        fxi = TexMobject(*r"f' ( \xi )".split()).tm(map) \
            .next_to(fx0[8], RIGHT).align_to(fx0[:4], UP).shift(UP * .05 + LEFT * .1)
        fxi_pos = TexMobject(*r"f' ( x_0 + )".split()).tm(map).next_to(fx0[4], RIGHT)
        fxi_neg = TexMobject(*r"= f' ( x_0 - )".split()).tm(map).next_to(fxi_pos, RIGHT)
        self.play(Write(fx0))
        self.wait()
        # self.add(lim_pos)
        # self.debugTeX(lim_pos)
        VGroup(lim_pos[3][0], lim_pos[4]).set_color(YELLOW)
        self.play(
            Transform(fx0[5], lim_pos[0]),
            Transform(fx0[6], lim_pos[1]),
            Transform(fx0[7], lim_pos[2]),
            Transform(fx0[8][0], lim_pos[3][0]),
            Transform(fx0[8][1], lim_pos[4]),
            # Transform(fx0[8][1:], lim_pos[3][1:]),
            Write(lim_pos[3][1])
        )
        self.wait()

        self.play(Transform(fx0[9:], fxi))
        interval = UnitInterval(tick_frequency=1).shift(DOWN)
        x0 = VGroup(interval.get_tick(.2), TexMobject("x_0", color=YELLOW))
        x = VGroup(interval.get_tick(.8), TexMobject("x"))
        xi = VGroup(interval.get_tick(.6), TexMobject(r"\xi", color=BLUE))
        for t in [x0, x, xi]:
            t[1].next_to(t[0], DOWN)
        xi[1].align_to(x0[1], DOWN)
        self.play(FadeIn(interval), FadeIn(x0), FadeIn(x))
        self.play(FadeIn(xi))
        self.wait()

        self.play(x.shift, LEFT * 3, xi.shift, LEFT * 2.1, run_time=2)
        self.wait()
        self.play(Transform(fx0[5:], fxi_pos), FadeOut(lim_pos[3][1]))
        self.wait()
        self.play(Write(fxi_neg))
        self.wait()
        self.play(FadeOut(VGroup(interval, x, xi, x0)))

        cont = TexMobject(*r"\text{即~} f' \text{~在~} x_0 \text{~处连续.~}".split(), r"\text{矛盾.}").tm(map)
        cont.next_to(fx0, DOWN, buff=.5).align_to(ie, LEFT)
        self.play(Write(cont[:-1]))
        self.play(Write(cont[-1]))
        self.wait()

        to_fade = [proof, fx0, fxi_neg, cont, ie]
        # to_fade.remove(th2)
        self.play(*[FadeOut(mob) for mob in to_fade])
        th1.restore()
        self.play(Restore(th2))
        self.play(FadeIn(VGroup(title, th1, pre)))
        self.wait()

        D = TexMobject(r"D(x)=\begin{cases}1,\quad x\in\mathbb{Q}\\0,\quad x\notin\mathbb{Q}\end{cases}", color=YELLOW)
        not_pri = TextMobject("\\kaishu 没有原函数.", color=YELLOW)
        d = VGroup(D, not_pri).arrange(buff=MED_LARGE_BUFF).next_to(th2, DOWN, buff=.75).set_x(0)
        otherwise = TextMobject("\\kaishu 若~$f'(x)=D(x)$,~$D(x)$~应该有介值性.").next_to(d, DOWN, buff=.5)
        self.play(Write(D))
        self.play(Write(not_pri))
        self.wait()
        self.play(Write(otherwise))
        self.wait()
