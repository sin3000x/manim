from manimlib.imports import *


def temperature_to_color(temp, min_temp=0, max_temp=15):
    colors = [BLUE, TEAL, GREEN, YELLOW, "#ff0000"]

    alpha = inverse_interpolate(min_temp, max_temp, temp)
    index, sub_alpha = integer_interpolate(
        0, len(colors) - 1, alpha
    )
    return interpolate_color(
        colors[index], colors[index + 1], sub_alpha
    )


class plot_uni(GraphScene):
    CONFIG = {
        "x_min": 0,
        "x_max": 1,
        "y_min": 0,
        "y_max": 1,
        "graph_origin": 3 * DOWN + 4.5 * LEFT,
        "x_labeled_nums": [0, 1],
        "y_labeled_nums": [1],
        "exclude_zero_label": False,
        "x_axis_width": 6,
        "num_rects": 500,
        "default_riemann_start_color": RED,
        "default_riemann_end_color": RED,
    }

    def construct(self):
        NUM = 20
        x_value = ValueTracker(.6)
        eps = .1

        def functions(n):
            return lambda x: x ** 2 + 1 / (x + n)

        def get_vline(x, y=1):
            return Line(self.c2p(x, 0), self.c2p(x, y), color=YELLOW)

        def get_vdots(x):
            return VGroup(*[Dot(self.c2p(x, f(x)), color=YELLOW) for f in functions])

        def tmp(f):
            return lambda t: t.move_to(self.c2p(x_value.get_value(), f(x_value.get_value())))

        functions = [functions(n) for n in range(1, NUM)]
        dot_updaters = [tmp(f) for f in functions]
        fn = TexMobject(r"f_n(x)=x^2+{1\over{x+n}}", color=BLUE)
        f = TexMobject(r"f(x)=x^2", color=RED)
        map = {"f": RED, "f_": BLUE, "地": YELLOW}
        pointwise = TexMobject(r"f_n", r"~\text{\kaishu 逐点地}", r"\text{\kaishu 收敛于}~", "f").tm(map)
        uniform = TexMobject(r"f_n", r"~\text{\kaishu 一致地}", r"\text{\kaishu 收敛于}~", "f").tm(map)
        VGroup(VGroup(fn, f).arrange(DOWN, aligned_edge=LEFT), VGroup(pointwise, uniform).arrange(DOWN)) \
            .arrange(DOWN, buff=.7, aligned_edge=LEFT).to_edge(RIGHT)

        self.setup_axes(True)
        graph = VGroup(*[self.get_graph(functions[n - 1], x_min=0, x_max=1 - 1e-3,
                                        color=interpolate_color(BLUE_E, BLUE_A, n / NUM),
                                        # color=temperature_to_color(n),
                                        )
                         for n in range(1, NUM)])
        self.play(ShowCreation(graph[0]), Write(fn), run_time=2)

        result = self.get_graph(lambda x: x ** 2, x_min=0, x_max=1, color=RED)
        curve1 = self.get_graph(lambda x: x ** 2 + eps, x_min=0, x_max=1, color=RED)
        curve2 = self.get_graph(lambda x: x ** 2 - eps, x_min=0, x_max=1, color=RED)
        area = self.get_area(curve1, 0, 1 + 1e-3, bounded=curve2)

        for i in range(1, NUM - 1):
            self.play(RT(graph[i - 1].copy(), graph[i]))
        self.wait()
        self.play(ShowCreation(result), Write(f))

        vline = get_vline(x_value.get_value()) \
            .add_updater(lambda t: t.become(get_vline(x_value.get_value(), functions[0](x_value.get_value()))))
        vdots = get_vdots(x_value.get_value())
        result_dot = Dot(color=RED) \
            .add_updater(lambda t: t.move_to(self.c2p(x_value.get_value(), x_value.get_value() ** 2)))
        for i in range(NUM - 1):
            vdots[i].add_updater(dot_updaters[i])

        self.wait()
        self.play(ShowCreation(vline))
        for dot in vdots:
            self.add(dot)
            self.wait(.2)
        self.wait()
        self.play(GrowFromCenter(result_dot))
        self.wait()
        self.play(Write(pointwise))
        self.wait()
        self.play(x_value.set_value, .9, run_time=3)
        self.wait()
        self.play(x_value.set_value, .3, run_time=3)
        self.wait()
        self.play(Write(uniform))
        self.wait()
        vline.clear_updaters()
        self.play(FadeOut(VGroup(vdots, vline, result_dot)))
        self.play(RT(result.copy(), curve1), RT(result.copy(), curve2))
        self.wait()
        self.play(ShowCreation(area))
        self.wait()

        distances = VGroup(*[Line(self.c2p(0, 0), self.c2p(0, f(0)), color=GREEN) for f in functions])
        braces = VGroup(*[Brace(d, LEFT, color=GREEN) for d in distances])
        d = VGroup(*[TexMobject(*f"d( f_{{{i + 1}}} , f )".split()).tm(map).next_to(brace, LEFT) for i, brace in
                     enumerate(braces)])
        self.play(FadeOut(VGroup(curve1, curve2, area)))
        self.play(ShowCreation(distances[0]))
        self.play(GrowFromCenter(braces[0]))
        self.play(Write(d[0]))
        self.wait()
        for i in range(1, NUM - 1):
            self.play(RT(distances[i - 1], distances[i]),
                      RT(braces[i - 1], braces[i]),
                      RT(d[i - 1], d[i]))


class plot_not_uni(GraphScene):
    CONFIG = {
        "x_min": 0,
        "x_max": 1,
        "y_min": 0,
        "y_max": 1,
        "x_axis_width": 8,
        "graph_origin": 3 * DOWN + 5 * LEFT,
        "x_labeled_nums": [0, 1],
        "y_labeled_nums": [1],
        "exclude_zero_label": False,
        "num_rects": 500,
        "default_riemann_start_color": RED,
        "default_riemann_end_color": RED,
    }

    def construct(self):
        NUM = 15
        x_value = ValueTracker(.6)
        eps = .1

        def functions(n):
            return lambda x: x ** n

        def get_vline(x):
            return Line(self.c2p(x, 0), self.c2p(x, 1), color=YELLOW)

        def get_vdots(x):
            return VGroup(*[Dot(self.c2p(x, f(x)), color=YELLOW) for f in functions])

        def tmp(f):
            return lambda t: t.move_to(self.c2p(x_value.get_value(), f(x_value.get_value())))

        functions = [functions(n) for n in range(1, NUM)]
        dot_updaters = [tmp(f) for f in functions]
        conv = TexMobject(*r"x^n \to 0".split()).tm({"n": BLUE, "0": RED}).scale(1.2)
        scope = TexMobject(r"x \in [0,1)")
        v = VGroup(conv, scope).arrange(DOWN, buff=MED_LARGE_BUFF).to_edge(RIGHT, buff=1)

        self.setup_axes()
        self.wait()
        result = self.get_graph(lambda x: 0, x_min=0, x_max=1, color=RED)
        curve1 = self.get_graph(lambda x: 0 + eps, x_min=0, x_max=1, color=RED)
        curve2 = self.get_graph(lambda x: 0 - eps, x_min=0, x_max=1, color=RED)
        area = self.get_area(curve1, 0, 1 + 1e-3, bounded=curve2)

        graph = VGroup(*[self.get_graph(functions[n - 1], x_min=0, x_max=1,
                                        color=interpolate_color(BLUE_E, BLUE_A, n / NUM),
                                        # color=temperature_to_color(n),
                                        )
                         for n in range(1, NUM)])
        self.play(ShowCreation(graph[0]))
        for i in range(1, NUM - 1):
            self.play(RT(graph[i - 1].copy(), graph[i]))

        vline = get_vline(x_value.get_value()).add_updater(lambda t: t.become(get_vline(x_value.get_value())))
        vdots = get_vdots(x_value.get_value())
        for i in range(NUM - 1):
            vdots[i].add_updater(dot_updaters[i])
        # for i in range(NUM-1):
        #     vdots[i].add_updater(lambda t: t.become(get_vdots(x_value.get_value())[i]))
        self.play(ShowCreation(vline))
        for dot in vdots:
            self.add(dot)
            self.wait(.2)
        self.wait()
        self.play(Write(conv))
        self.play(Write(scope))
        self.wait()
        self.play(x_value.set_value, .9, run_time=3)
        self.wait()
        self.play(x_value.set_value, .6, run_time=3)
        vline.clear_updaters()
        self.play(FadeOut(VGroup(vline, vdots)))
        self.play(ShowCreation(result))
        self.play(RT(result.copy(), curve1), RT(result.copy(), curve2))
        self.play(ShowCreation(area))
        self.wait()

        self.play(FadeOut(VGroup(area, curve1, curve2)))
        distance = Line(self.c2p(1, 0), self.c2p(1, 1), color=GREEN)
        # brace = Brace(distance, RIGHT, color=GREEN)
        # d = TexMobject(*"d ( f_n , f )=1".split()).tm({"f_": BLUE,"f": RED}).next_to(brace, RIGHT)
        self.play(ShowCreation(distance))
        # self.play(GrowFromCenter(brace), RT(v, d))


class opening(PiCreatureScene):
    CONFIG = {
        "pi_creatures_start_on_screen": True,
    }

    def construct(self):
        seq = VGroup(TexMobject(*r"1 , ~\frac12 , ~\frac13 , ~\frac14 , ~\frac15 , \cdots".split()) \
                     .set_color_by_gradient(BLUE, GREEN).set_color_by_tex(',', WHITE),
                     TexMobject(*r"\to 0".split(), color=GREEN)).arrange()
        seq_fun = VGroup(TexMobject(*r"1 , ~1+x , ~1+x+\frac{x^2}{2!} , ~1+x+\frac{x^2}{2!}+\frac{x^3}{3!}"
                                     r" \cdots".split())
                         .set_color_by_gradient(BLUE, GREEN).set_color_by_tex(',', WHITE),
                         TexMobject(r"\to \e^x", color=GREEN)).arrange()
        VGroup(seq, seq_fun).arrange(DOWN, buff=MED_LARGE_BUFF).to_edge(UP)
        self.play(Write(seq[0]))
        self.wait()
        self.play(Write(seq[1]))
        self.wait()
        self.play(Write(seq_fun[0]))
        self.wait()
        self.play(Write(seq_fun[1]))
        self.wait()

        you = self.pi_creature
        question = TextMobject(r"\kaishu 如何刻画一个函数列收敛？").scale(1.5).next_to(you, RIGHT, buff=1).shift(UP * .5)
        self.play(Write(question), you.change_mode, 'question', run_time=2)
        # self.play()
        self.wait()


class definition(Scene):
    def construct(self):
        cmap = {"f": RED, "f_": BLUE, "textbf": WHITE, "N": YELLOW, "mathbb": WHITE, "forall": WHITE}
        point_label = TexMobject("f_n(x)", r"~\textbf{\text{\heiti 在}}~", r"I",
                                 r"~\textbf{\text{\heiti 上逐点收敛到}}}~", "f(x)", r"\colon").tm(cmap).to_edge(UL)
        point_label[-3][1:5].set_color(YELLOW)
        point = VGroup(
            TexMobject(*r"\forall x\in I, \forall \varepsilon >0, \exists N \in\mathbb{N^*},".split()).tm(cmap),
            TexMobject(*r"n> N ~\Longrightarrow~ | f_n(x) - f(x) |< \varepsilon".split()).tm(cmap)) \
            .arrange(DOWN) \
            .next_to(point_label, DOWN, buff=.5).set_x(0)
        box1 = SurroundingRectangle(point[0][6:], color=GREEN)
        c1 = TexMobject(*r"N ( x,\varepsilon)".split()).tm(cmap).next_to(point_label, RIGHT)
        self.play(Write(point_label))
        self.wait()
        self.play(Write(point[0][:3]))
        self.wait()
        self.play(Write(point[0][3:6]))
        self.wait()
        self.play(Write(point[0][6:]))
        self.wait()
        self.play(Write(point[1][:3]))
        self.wait()
        self.play(Write(point[1][3:]))
        self.wait()

        uni_label = TexMobject("f_n(x)", r"~\textbf{\text{\heiti 在}}~", r"I",
                               r"~\textbf{\text{\heiti 上一致收敛到}}}~", "f(x)", r"\colon").tm(cmap) \
            .next_to(point, DOWN, buff=1).align_to(point_label, LEFT)
        uni_label[-3][1:5].set_color(YELLOW)
        uni = VGroup(
            TexMobject(*r"\forall \varepsilon >0, \exists N \in\mathbb{N^*}, \forall x\in I,".split()).tm(cmap),
            TexMobject(*r"n> N ~\Longrightarrow~ | f_n(x) - f(x) |< \varepsilon".split()).tm(cmap)).arrange(DOWN) \
            .next_to(uni_label, DOWN, buff=.5).set_x(0)
        box2 = SurroundingRectangle(uni[0][3:6], color=GREEN)
        c2 = TexMobject("N", r"(\varepsilon)").tm(cmap).next_to(uni_label, RIGHT)
        self.play(Write(uni_label))
        self.play(Write(uni[0][:3]))
        self.wait()
        self.play(Write(uni[0][3:6]))
        self.wait()
        self.play(Write(uni[0][6:]))
        self.wait()
        self.play(Write(uni[1][:3]))
        self.wait()
        self.play(Write(uni[1][3:]))
        self.wait()

        self.play(ShowCreation(box1), ShowCreation(box2))
        self.wait()
        self.play(Write(c1))
        self.wait()
        self.play(Write(c2))
        self.wait()

        strip = VGroup(Brace(uni[1][3:], DOWN),
                       TexMobject(*r"f(x) - \varepsilon < f_n(x) < f(x) +\varepsilon".split()).tm(cmap))
        strip[1].next_to(strip[0], DOWN)
        self.play(GrowFromCenter(strip[0]))
        self.play(Write(strip[1]))
        self.wait()

        dsup = TexMobject(*r"d( f_n , f ) \to 0".split()).tm(cmap).move_to(uni)
        dsup_def = TexMobject(*r"\sup _{x\in I} | f_n(x) - f(x) | \to 0".split()).tm(cmap).move_to(dsup)
        self.play(RT(VGroup(uni, strip, box2), dsup))
        self.wait()
        self.play(RT(dsup, dsup_def))
        self.wait()


class meaning(Scene):
    def construct(self):
        cmap = {"f": RED, "f_n": BLUE, }
        pre = TexMobject(*r"f_n \to f".split()).tm(cmap).scale(1.2).to_edge(UP, buff=.5)
        question = TexMobject("f_n", r"~\text{连续}", r"~\Longrightarrow~", "f", r"~\text{连续?}").tm(cmap).next_to(pre,
                                                                                                                DOWN)
        counter = TexMobject(r"x^n\to\begin{cases}0,\quad x\in[0,1)\\1,\quad x=1\end{cases}", color=YELLOW) \
            .next_to(question, DOWN, buff=.5)
        self.play(Write(pre))
        self.wait()
        self.play(Write(question))
        self.wait()
        self.play(Write(counter))
        self.wait()

        smap = {"lim": BLUE, "int": RED, "sum": BLUE, "x": RED}

        li = TexMobject(r"\lim", r"\int")
        li_ = TexMobject(r"\int", r"\lim")
        ld = TexMobject(r"\lim", r"\frac{\mathrm{d}}{\mathrm{d}x}")
        ld_ = TexMobject(r"\frac{\mathrm{d}}{\mathrm{d}x}", r"\lim").move_to(ld)
        ls = TexMobject(r"\int", r"\sum")
        ls_ = TexMobject(r"\sum", r"\int")
        ds = TexMobject(r"\frac{\mathrm{d}}{\mathrm{d}x}", r"\sum")
        ds_ = TexMobject(r"\sum", r"\frac{\mathrm{d}}{\mathrm{d}x}")

        VGroup(li, ld, ls, ds).arrange(buff=1).next_to(counter, DOWN, buff=1)
        for i in [li, li_, ld, ld_, ls, ls_, ds, ds_]:
            i.tm(smap)

        for i, j in zip([li, ld, ls, ds], [li_, ld_, ls_, ds_]):
            j.move_to(i)

        for i, j in zip([li, ld, ls, ds], [li_, ld_, ls_, ds_]):
            self.play(Write(i))
            self.play(
                RT(i[0], j[1], ),
                RT(i[1], j[0], path_arc=-np.pi),
                rate_func=there_and_back, run_time=2
            )
            j.become(i)

        self.wait()


class pic(Scene):
    def construct(self):
        a = TexMobject(r"f_n\rightrightarrows f").scale(4)
        self.add(a)