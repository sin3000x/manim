from manimlib.imports import *
# from jeremy.ref.debugTex import debugTeX

# 函数的上下极限
class fun(GraphScene):
    CONFIG = {"upper": BLUE, "middle": RED, "lower": GREEN,"color_map": {r"\sup": BLUE, r"k\geq": BLUE, "a_k": BLUE},
              "color_map_down": {r"\inf": GREEN, r"k\geq": GREEN, "a_k": GREEN},
              "color_map_limit": {"limsup": BLUE, "liminf": GREEN,"大": BLUE,"小": GREEN},
              "x_min": -15,
              "x_max": 15,
              "y_min": -1.2,
              "y_max": 1.2,
              "x_axis_width": 12,
              "y_axis_height": 3,
              "y_tick_frequency": 1.2,
              "graph_origin": ORIGIN,
              }

    def debugTeX(self, texm, scale_factor=0.6, text_color=PURPLE):
        for i, j in enumerate(texm):
            tex_id = Text(str(i), font="Consolas").scale(scale_factor).set_color(text_color)
            tex_id.move_to(j)
            self.add(tex_id)

    def construct(self):
        self.opening()
        self.plot()
        self.prop()
        self.an()

    def opening(self):
        lsup_an = TexMobject(r"\varlimsup_{n\to\infty} a_n", "=", r"\sup", r"\{ \text{{\kaishu 极限点}} \}").set_color_by_tex(
            "limsup", self.upper)
        linf_an = TexMobject(r"\varliminf_{n\to\infty} a_n", "=", r"\inf", r"\{ \text{{\kaishu 极限点}} \}").set_color_by_tex(
            "liminf", self.lower)
        self.lsup=lsup = TexMobject(r"\varlimsup_{x\to a} f(x)", "=", r"\sup",
                             r"\{ \text{{\kaishu 极限点}} \}").set_color_by_tex(
            "limsup", self.upper)
        linf = TexMobject(r"\varliminf_{x\to a} f(x)", "=", r"\inf",
                             r"\{ \text{{\kaishu 极限点}} \}").set_color_by_tex(
            "liminf", self.lower)
        lim = self.lim = linf[-1]

        VGroup(lsup_an, linf_an).arrange(DOWN, aligned_edge=LEFT)
        VGroup(lsup, linf).arrange(DOWN, aligned_edge=LEFT)
        self.linf = linf.copy()
        self.play(Write(lsup_an))
        self.play(Write(linf_an))
        self.wait()
        self.play(ReplacementTransform(lsup_an, lsup))
        self.play(ReplacementTransform(linf_an, linf))
        self.wait()
        self.play(ShowPassingFlashAround(lsup[-1]), ShowPassingFlashAround(linf[-1]))
        self.play(FadeOut(VGroup(lsup, linf[:-1])), lim.to_edge, UP, lim.set_x, 0)

    def plot(self):
        self.setup_axes(animate=True)
        fun = lambda x: np.sin(x)
        graph = self.get_graph(fun, x_min=-15, x_max=15)
        self.play(ShowCreation(graph), run_time=3)

        # all ones
        dots_x = [Dot(self.coords_to_point(np.pi/2+2*n*np.pi, 0), color=YELLOW) for n in range(-2,4)]
        dots_y = [Dot(self.coords_to_point(np.pi/2+2*n*np.pi, 1), color=GREEN) for n in range(-2,4)]
        coords_x = [np.pi/2+2*n*np.pi for n in range(-2,4)]
        x_tend = TexMobject(r"x\to +\infty").to_edge(DOWN, buff=LARGE_BUFF)
        self.play(Write(x_tend))
        self.wait()
        for dot in dots_x:
            self.add(dot)
            self.wait(.5)
        x_label = TexMobject(r"\to +\infty", color=YELLOW).next_to(self.x_axis, DOWN).to_edge(RIGHT)
        self.play(Write(x_label))
        self.wait()

        lines = [DashedLine(self.coords_to_point(x, 0), self.coords_to_point(x, 1), color=GREEN) for x in coords_x]
        for line, dot in zip(lines, dots_y):
            self.play(GrowArrow(line), run_time=.4)
            self.add(dot)
        y_label = TexMobject(r"\to"," 1", color=GREEN).move_to(self.y_axis_label_mob).align_to(x_label, LEFT)
        lip = y_label[-1].copy()
        self.play(Write(y_label))
        self.wait()
        self.play(lip.fade, 1, lip.move_to, self.lim, run_time=2)
        self.wait()

        self.play(FadeOut(VGroup(x_label, y_label, *dots_x, *dots_y, *lines)))

        # all zeros
        dots_x2 = [Dot(self.coords_to_point(n * np.pi, 0), color=YELLOW) for n in range(-4, 5)]
        dots_y2 = [Dot(self.coords_to_point(n * np.pi, 0), color=RED) for n in range(-4, 5)]
        # coords_x2 = [np.pi / 2 + 2 * n * np.pi for n in range(-2, 4)]
        self.wait()
        for dot in dots_x2:
            self.add(dot)
            self.wait(.3)
        x_label2 = TexMobject(r"\to +\infty", color=YELLOW).next_to(self.x_axis, DOWN).to_edge(RIGHT)
        self.play(Write(x_label2))
        self.wait()

        # lines2 = [DashedLine(self.coords_to_point(x, 0), self.coords_to_point(x, 1), color=GREEN) for x in coords_x2]
        for dot in dots_y2:
            # self.play(GrowArrow(line), run_time=.4)
            self.add(dot)
            self.wait(.3)
        y_label2 = TexMobject(r"\to", " 0", color=RED).next_to(self.x_axis, UP, buff=.1).align_to(x_label2, LEFT)
        lip2 = y_label2[-1].copy()
        bg = BackgroundRectangle(y_label2)
        self.play(FadeIn(bg))
        self.play(Write(y_label2))
        self.wait()
        self.play(lip2.fade, 1, lip2.move_to, self.lim, run_time=2)
        self.wait()

        ex_fun = TexMobject(r"f(x)=\sin\left(\frac 1x \right)",",~",r"x\to 0")
        upper = TexMobject(r"\varlimsup_{x\to 0}f(x)=1", color=YELLOW)
        zero_up = TexMobject(r"{1 \over {{\pi \over 2}+2n\pi}}",r"\to",r"0^+",",~",r"-{1 \over {-{\pi \over 2}+2n\pi}}",r"\to","0^-")
        zero_up[0].set_color(self.upper)
        zero_up[-3].set_color(self.middle)
        value_up = TexMobject(r"f\left(",r"{1 \over {{\pi \over 2}+2n\pi}}",r"\right)",r"=\sin\left({\pi \over 2}+2n\pi\right)=1")
        value_down = TexMobject(r"f\left(",r"-{1 \over {-{\pi \over 2}+2n\pi}}",r"\right)",r"=-\sin\left(-{\pi \over 2}+2n\pi\right)=1")
        value_up[1].set_color(self.upper)
        value_down[1].set_color(self.middle)


        VGroup(ex_fun, upper, zero_up, value_up, value_down).arrange(DOWN)
        tend = TexMobject(r"\exists x_n\to 0^+\text{{\kaishu 或~}}0^-,\text{{\kaishu 使~}} f(x_n)\to 1.", color=self.upper).next_to(upper, DOWN)
        self.play(ReplacementTransform(VGroup(self.lim, self.axes, bg, VGroup(*dots_x2), VGroup(*dots_y2), x_tend, x_label2, y_label2, graph), ex_fun))
        self.wait()
        self.play(Write(upper))
        self.wait()
        self.play(Write(zero_up))
        self.wait()
        self.play(ReplacementTransform(zero_up.copy()[0], value_up[1]), Write(value_up[0]), Write(value_up[2]))
        self.play(Write(value_up[3:]))
        self.play(ReplacementTransform(zero_up.copy()[-3], value_down[1]), Write(value_down[0]), Write(value_down[2]))
        self.play(Write(value_down[3:]))
        self.wait(2)

        self.play(ReplacementTransform(VGroup(zero_up, value_up, value_down), tend))
        lower = TexMobject(r"\varliminf_{x\to 0}f(x)=-1", color=YELLOW).next_to(tend, DOWN, buff=MED_LARGE_BUFF).align_to(upper, LEFT)
        tend2 = TexMobject(r"\exists y_n\to 0^+\text{{\kaishu 或~}}0^-,\text{{\kaishu 使~}} f(y_n)\to -1.", color=self.upper).next_to(lower, DOWN)
        self.wait()
        self.play(Write(lower))
        self.play(Write(tend2))
        self.wait()

        self.play(FadeOut(VGroup(ex_fun, upper, lower, tend, tend2)))

    def prop(self):
        # definition of limit point
        VGroup(self.lsup, self.linf).to_edge(TOP)
        self.play(FadeIn(VGroup(self.lsup, self.linf)))
        self.wait()
        limit_point = TexMobject(r"\{l\in\overline{\mathbb{R}}\colon \text{{\kaishu 存在}}a\text{{\kaishu 去心邻域内的数列}}x_n,"
                                 r"\\x_n\to a,\text{{\kaishu 使得}}f(x_n)\to l\}").next_to(self.linf, DOWN, buff=MED_LARGE_BUFF)
        # self.add(limit_point)
        # self.debugTeX(limit_point[0])
        for i in [1, 33]:
            limit_point[0][i].set_color(RED)
        for i in [17,18,20,21,29,30]:
            limit_point[0][i].set_color(YELLOW)
        # for i in [8,9,24,25]:
        #     limit_point[0][i].set_color(WHITE)
        #
        self.play(Write(limit_point[0][20:34]))
        self.play(Write(limit_point[0][1:6]), run_time=2)
        self.play(Write(limit_point[0][0]), Write(limit_point[0][34]))
        self.wait()
        self.play(Write(limit_point[0][6:20]), run_time=2)
        self.wait()
        self.play(FadeOut(VGroup(self.linf, self.lsup, limit_point)))


        # sup and inf prop
        sup_prop = VGroup(
            TexMobject("a^*", r"\in", r"\{ \text{{\kaishu {极限点}}} \}").set_color_by_tex("a^*", self.upper),
            TexMobject("y>", r"a^*", r"~\Longrightarrow~", "y>","a_n", r"~(",r"\text{{\kaishu 从某项}}",")").set_color_by_tex("a^*",
                                                                                                                 self.upper)).arrange(
            DOWN, aligned_edge=LEFT)
        sup_change = TexMobject("y>", r"a^*", r"~\Longrightarrow~", "y>","f(x)", r"~~(",r"\text{{\kaishu 当~}}",r"0<|x-a|<\delta",")").set_color_by_tex("a^*",
                                                                                                                 self.upper)
        sup_brace = Brace(sup_prop, LEFT)
        sup_prop_label = TextMobject(r"{\kaishu 上极限}", "$a^*$").set_color_by_tex("a^*", self.upper).next_to(sup_brace,
                                                                                                            LEFT)
        sup_v = VGroup(sup_prop, sup_brace, sup_prop_label)
        sup_v.set_x(0)
        sup_good = TextMobject("{\\kaishu 上极限是满足这两个性质的唯一数.}", color=YELLOW).next_to(sup_v, DOWN)

        inf_prop = VGroup(
            TexMobject("a_*", r"\in", r"\{ \text{{\kaishu {极限点}}} \}").set_color_by_tex("a_*", self.lower),
            TexMobject("y<", r"a_*", r"~\Longrightarrow~", "y<","a_n", r"~(",r"\text{{\kaishu 从某项}}",")").set_color_by_tex("a_*",
                                                                                                                 self.lower)).arrange(
            DOWN, aligned_edge=LEFT)
        inf_change = TexMobject("y<", r"a_*", r"~\Longrightarrow~", "y<","f(x)", r"~~(",r"\text{{\kaishu 当~}}",r"0<|x-a|<\delta",r")").set_color_by_tex("a_*",
                                                                                                                 self.lower)
        inf_brace = Brace(inf_prop, LEFT)
        inf_prop_label = TextMobject(r"{\kaishu 下极限}", "$a_*$").set_color_by_tex("a_*", self.lower).next_to(inf_brace,
                                                                                                            LEFT)
        inf_v = VGroup(inf_prop, inf_brace, inf_prop_label)
        inf_v.set_x(0)
        inf_good = TextMobject("{\\kaishu 下极限是满足这两个性质的唯一数.}", color=YELLOW).next_to(inf_v, DOWN)

        VGroup(VGroup(sup_v, sup_good), VGroup(inf_v, inf_good)).arrange(DOWN, buff=LARGE_BUFF)
        sup_change.move_to(sup_prop[1])
        inf_change.move_to(inf_prop[1])
        self.play(FadeIn(VGroup(sup_prop, sup_brace, sup_prop_label, sup_good,
                                inf_prop, inf_brace, inf_prop_label, inf_good)))
        self.wait(2)
        self.play(ReplacementTransform(sup_prop[1][:4], sup_change[:4]), ReplacementTransform(inf_prop[1][:4], inf_change[:4]),
                  ReplacementTransform(sup_prop[1][4], sup_change[4]), ReplacementTransform(inf_prop[1][4], inf_change[4]),
                  ReplacementTransform(sup_prop[1][5], sup_change[5]), ReplacementTransform(inf_prop[1][5], inf_change[5]),
                  ReplacementTransform(sup_prop[1][-1], sup_change[-1]), ReplacementTransform(inf_prop[1][-1], inf_change[-1]),
                  ReplacementTransform(sup_prop[1][6:-1], sup_change[6:-1]), ReplacementTransform(inf_prop[1][6:-1], inf_change[6:-1]),
                  VGroup(sup_prop[0], inf_prop[0], sup_brace, inf_brace, sup_prop_label, inf_prop_label).shift,
                  LEFT*(sup_change.get_x()-sup_prop[0].get_x()), run_time=2)
        self.wait(2)

        self.play(FadeOut(VGroup(sup_prop[0], sup_change, sup_brace, sup_prop_label, sup_good,
                                 inf_prop[0], inf_change, inf_brace, inf_prop_label, inf_good)))

        # another def
        sup_an = TexMobject(r"\limsup_{n\to\infty}",r" a_n\coloneqq \lim_{n\to\infty}\sup_{k\geq n} \{a_k\}")\
            .set_color_by_tex_to_color_map(self.color_map_limit)
        sup_f = TexMobject(r"\limsup_{x\to a}",r" f(x)\coloneqq \lim_{\delta\to 0^+}\sup_{0<|x-a|<\delta} f(x)")\
            .set_color_by_tex_to_color_map(self.color_map_limit)
        inf_an = TexMobject(r"\liminf_{n\to\infty}",r" a_n\coloneqq \lim_{n\to\infty}\inf_{k\geq n} \{a_k\}")\
            .set_color_by_tex_to_color_map(self.color_map_limit)
        inf_f = TexMobject(r"\liminf_{x\to a}", r" f(x)\coloneqq \lim_{\delta\to 0^+}\inf_{0<|x-a|<\delta} f(x)") \
            .set_color_by_tex_to_color_map(self.color_map_limit)
        v1 = VGroup(sup_an, sup_f).arrange(DOWN)
        v2 = VGroup(inf_an, inf_f).arrange(DOWN)
        VGroup(v1, v2).arrange(DOWN, buff=LARGE_BUFF)
        self.play(Write(sup_an))
        self.play(Write(inf_an))
        self.wait()
        self.play(Write(sup_f))
        self.play(Write(inf_f))
        self.wait(2)
        self.play(FadeOut(VGroup(v1, v2)))


        # propositiono part
        leq = TexMobject(r"\varliminf_{n\to\infty}", "a_n", r"\leq", r"\varlimsup_{n\to\infty}",
                         "a_n").set_color_by_tex_to_color_map(self.color_map_limit)
        leq2 = TexMobject(r"\varliminf_{x\to a}", "f(x)", r"\leq", r"\varlimsup_{x\to a}",
                         "f(x)").set_color_by_tex_to_color_map(self.color_map_limit)
        eq = TexMobject(r"\varliminf_{n\to\infty}", "a_n", r"=", r"\varlimsup_{n\to\infty}", "a_n", "=", "a",
                        r"~\Longleftrightarrow~", r"\lim_{n\to\infty} a_n=a").set_color_by_tex_to_color_map(
            self.color_map_limit)
        eq2 = TexMobject(r"\varliminf_{x\to a}", "f(x)", r"=", r"\varlimsup_{x\to a}", "f(x)", "=", "l",
                        r"~\Longleftrightarrow~", r"\lim_{x\to a} f(x)=l").set_color_by_tex_to_color_map(
            self.color_map_limit)
        v1 = VGroup(leq, eq).arrange(DOWN)

        pre = TexMobject("a_n", r"\leq", "b_n", r"~(\text{{\kaishu 从某项}})")
        pre2 = TexMobject("f(x)", r"\leq", "g(x)", r"~(\text{{\kaishu 某区间}})")

        ineq_inf = TexMobject(r"\varliminf_{n\to\infty}", "a_n", r"\leq", r"\varliminf_{n\to\infty}",
                              "b_n").set_color_by_tex_to_color_map(self.color_map_limit)
        ineq_sup = TexMobject(r"\varlimsup_{n\to\infty}", "a_n", r"\leq", r"\varlimsup_{n\to\infty}",
                              "b_n").set_color_by_tex_to_color_map(self.color_map_limit)
        ineq_inf2 = TexMobject(r"\varliminf_{x\to a}", "f(x)", r"\leq", r"\varliminf_{x\to a}",
                              "g(x)").set_color_by_tex_to_color_map(self.color_map_limit)
        ineq_sup2 = TexMobject(r"\varlimsup_{x\to a}", "f(x)", r"\leq", r"\varlimsup_{x\to a}",
                              "g(x)").set_color_by_tex_to_color_map(self.color_map_limit)
        v2 = VGroup(pre, ineq_inf, ineq_sup).arrange(DOWN)

        VGroup(v1, v2).arrange(DOWN, buff=LARGE_BUFF)
        leq2.move_to(leq)
        eq2.move_to(eq)
        pre2.move_to(pre)
        ineq_inf2.move_to(ineq_inf)
        ineq_sup2.move_to(ineq_sup)

        self.play(FadeIn(VGroup(v1, v2)))
        self.wait(2)
        self.play(ReplacementTransform(leq, leq2))
        self.play(ReplacementTransform(eq, eq2))
        self.play(ReplacementTransform(pre, pre2))
        self.play(ReplacementTransform(ineq_inf, ineq_inf2))
        self.play(ReplacementTransform(ineq_sup, ineq_sup2))
        self.wait(3)

        self.play(FadeOut(VGroup(leq2, eq2, pre2, ineq_inf2, ineq_sup2)))
    def an(self):
        self.x_min, self.x_max=0, 1.1
        self.y_min, self.y_max=-1, 1
        self.graph_origin = LEFT*5
        self.x_axis_width = 10
        self.y_axis_height = 6
        self.y_tick_frequency = 1
        self.y_bottom_tick = -1
        # self.default_graph_colors = [YELLOW, RED, PURPLE]
        self.setup_axes(animate=True)

        colors = it.cycle([YELLOW, RED, PINK])

        zero = TexMobject("0").next_to(self.coords_to_point(0,0), DL, buff=.1)
        one = TexMobject("1").next_to(self.coords_to_point(1,0), DOWN)

        # a_n = lambda n: np.sin(n)
        def f(x):
            n = math.floor(1/x)
            return np.sin(n)

        # fs = [f(x) for n in range(1, 5)]
        N = 7

        ticks = [self.x_axis.get_tick(1/(i+2)) for i in range(N)]
        xlabels = [TexMobject(f"\\tfrac{1}{{{i+2}}}").scale(.8).next_to(self.coords_to_point(1/(i+2), 0), DOWN) for i in range(N)]
        self.play(FadeIn(zero), FadeIn(one), FadeIn(VGroup(*ticks)), FadeIn(VGroup(*xlabels)))
        for i in range(N):
            graph = self.get_graph(f, x_min=1/(i+2)+1e-4, x_max=1/(i+1)-1e-4, color=next(colors))
            label = TexMobject(f"a_{{{i+1}}}", color=graph.get_color()).scale(0.8).next_to(graph, UP)
            # self.add(tick)
            # self.play(Write(xlabel))
            if i == 5:
                # graph.shift(DOWN)
                label.next_to(graph, DOWN)
            self.play(ShowCreation(graph), run_time=.6)
            self.play(Write(label), run_time=.6)

        cdots = TexMobject(r"\cdots").next_to(self.coords_to_point(1/16, 0), DOWN)
        self.play(Write(cdots))
        definition = TexMobject("f(x)=a_n,\\quad x\\in \\left[\\frac{1}{n+1},\\frac 1n \\right)").scale(.8)
        sup = TexMobject(r"\varlimsup_{n\to\infty}", "a_n", r"=", r"\varlimsup_{x\to 0^+}",
                              "f(x)").set_color_by_tex_to_color_map(self.color_map_limit)
        inf = TexMobject(r"\varliminf_{n\to\infty}", "a_n", r"=", r"\varliminf_{x\to 0^+}",
                              "f(x)").set_color_by_tex_to_color_map(self.color_map_limit)
        v0 = VGroup(sup, inf).arrange(DOWN)
        v = VGroup(definition, v0).arrange(DOWN, buff=MED_LARGE_BUFF).to_edge(RIGHT)
        bg = BackgroundRectangle(v)
        self.play(FadeIn(bg))
        self.play(Write(definition))
        self.wait()
        self.play(Write(sup))
        self.wait()
        self.play(Write(inf))
        self.wait()

class test(Scene):
    def construct(self):
        a = TexMobject(r"\varlimsup_{x\to a}","f(x)").scale(3)
        self.add(a)





