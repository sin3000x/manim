import re

from manimlib import *
from scipy.interpolate import approximate_taylor_polynomial


class Opening(Scene):
    def construct(self) -> None:
        axes = Axes()
        sin_graph = axes.get_graph(np.sin, color=YELLOW, x_range=(-4, 4))
        sin_label = axes.get_graph_label(
            sin_graph,
            x=3,
            label="f(x)"
        )
        self.add(axes, sin_graph, sin_label)

        graph = axes.get_graph(lambda x: 0, color=RED, x_range=(-4, 4))
        p0_label = axes.get_graph_label(
            graph,
            label="p_0(x)",
            x=-2.5
        )
        self.play(ShowCreation(graph), Write(p0_label))
        for degree in range(1, 12, 2):
            sin_taylor = approximate_taylor_polynomial(
                np.sin, 0, degree, 1, order=degree + 2
            )
            sin_taylor_graph = axes.get_graph(
                sin_taylor, color=RED, x_range=(-4, 4)
            )
            label = axes.get_graph_label(
                sin_taylor_graph,
                label="p_{{%s}}(x)" % degree,
                x=-2.5
            )
            self.play(
                Transform(graph, sin_taylor_graph),
                Transform(p0_label, label)
            )
            self.wait()
        self.wait()


def f(x):
    if -2 <= x < -1:
        return x + 2
    if -1 <= x < 1:
        return 1 - np.sqrt(1 - x ** 2)
    if 1 <= x <= 2:
        return 1 - np.sqrt(1 - (x - 2) ** 2)
    return 0
    # return np.abs(x)


def gt(x, t=1e-4):
    return np.exp(- x ** 2 / (4 * t)) / np.sqrt(4 * PI * t)


def gs(x, s=1.0):
    return np.exp(-x ** 2 / (2 * s ** 2)) / (np.sqrt(2 * PI) * s)


def get_conv_graph(axes, f1, f2, dx=0.01, x_range=None, clip_to_range=None, color=TEAL):
    if x_range is None:
        x_min, x_max = axes.x_range[:2]
    else:
        x_min, x_max = x_range
    x_samples = np.arange(x_min, x_max + dx, dx)
    f_samples = np.array([f1(x) for x in x_samples])
    # f_samples = f1(x_samples)
    try:
        g_samples = f2(x_samples)
    except ValueError:
        g_samples = np.array([f2(x) for x in x_samples])
    full_conv = np.convolve(f_samples, g_samples)
    # print(f"{full_conv=}")
    x0 = len(x_samples) // 2 - 1  # TODO, be smarter about this
    # x0 = 99
    # x0 = round(len(x_samples) // 2 - 1 - (x_max - 1) / (2 * dx))
    conv_samples = full_conv[x0:x0 + len(x_samples)]
    conv_graph = VMobject()
    conv_graph.set_stroke(color, 6)
    # conv_graph.set_points_smoothly(
    #     axes.c2p(x_samples, conv_samples * dx),
    # )
    y_samples = conv_samples * dx
    if clip_to_range:
        l, r = clip_to_range
        indices = np.where((x_samples >= l) & (x_samples <= r))
        x_samples = x_samples[indices]
        y_samples = y_samples[indices]
    conv_graph.set_points_as_corners(
        axes.c2p(x_samples, y_samples),
    )
    conv_graph.x = x_samples
    conv_graph.y = y_samples

    return conv_graph


def get_convolved_self(axes, f1, f2, dx=0.01, x_range=None, clip_to_range=None, color=TEAL):
    if x_range is None:
        x_min, x_max = axes.x_range[:2]
    else:
        x_min, x_max = x_range
    x_samples = np.arange(x_min, x_max + dx, dx)
    f_samples = np.array([f1(x) for x in x_samples])
    # f_samples = f1(x_samples)
    try:
        g_samples = f2(x_samples)
    except ValueError:
        g_samples = np.array([f2(x) for x in x_samples])
    full_conv = np.convolve(f_samples, g_samples)
    # print(f"{full_conv=}")
    x0 = len(x_samples) // 2 - 1  # TODO, be smarter about this
    # x0 = 99
    # x0 = round(len(x_samples) // 2 - 1 - (x_max - 1) / (2 * dx))
    conv_samples = full_conv[x0:x0 + len(x_samples)]
    conv_graph = VMobject()
    conv_graph.set_stroke(color, 6)
    # conv_graph.set_points_smoothly(
    #     axes.c2p(x_samples, conv_samples * dx),
    # )
    y_samples = conv_samples * dx
    y_samples = np.array([f1(x) for x in x_samples])
    if clip_to_range:
        l, r = clip_to_range
        indices = np.where((x_samples >= l) & (x_samples <= r))
        x_samples = x_samples[indices]
        y_samples = y_samples[indices]
    conv_graph.set_points_as_corners(
        axes.c2p(x_samples, y_samples),
    )
    conv_graph.x = x_samples
    conv_graph.y = y_samples

    return conv_graph


class WeierstrassTheorem1(Scene):
    def construct(self) -> None:
        title = Title(
            "Weierstrass Approximation Theorem",
            font_size=48
        ).set_color(YELLOW)
        self.add(title)

        theorem = TexText(
            r"\heiti $[a,b]$ 上的任何连续函数都可以用多项式一致逼近.",
            tex_to_color_map={
                "连续函数": RED,
                "多项式": RED
            }
        ).next_to(title, DOWN, buff=.5)
        box = SurroundingRectangle(theorem[20:24])
        self.play(Write(theorem))
        self.wait()

        image1 = ImageMobject("sinsin") \
            .to_edge(DOWN).to_edge(LEFT, buff=2)
        image2 = ImageMobject("weierstrass") \
            .to_edge(DOWN).to_edge(RIGHT, buff=2)
        f_label = Tex(
            r"f(x)=\sin \left({1 \over x}\right)\sin{1 \over \sin\left({1\over x}\right)}",
            font_size=30
        ).next_to(image1, UP).set_color(BLUE)
        w_label = Tex(
            r"w(x) = \sum_{n=0}^\infty 2^{-n}\cos(3^n x)",
            font_size=30
        ).next_to(image2, UP).set_color(BLUE)

        self.play(Write(f_label), FadeIn(image1, scale=3))
        self.wait()
        self.play(Write(w_label), FadeIn(image2, scale=3))
        self.wait()

        self.play(ShowCreation(box))
        self.wait()


class WeierstrassTheorem2(Scene):
    def construct(self) -> None:
        self.title = title = Title(
            "Weierstrass Approximation Theorem",
            font_size=48
        ).set_color(YELLOW)
        self.add(title)
        self.wait()
        self.write_theorem()

        axes = Axes(
            x_range=(-1, 1), y_range=(-0.5, 1), unit_size=3,
            num_sampled_graph_points_per_tick=100,
            axis_config={"include_ticks": False}
        ).to_edge(DOWN)
        f1 = lambda x: x * (x + 0.8) * (x - 1)
        f2 = lambda x: x ** 2
        graph1 = axes.get_graph(f1, color=RED)
        graph1.label = axes.get_graph_label(graph1, "f", x=0.8)
        graph2 = axes.get_graph(f2, color=GREEN)
        graph2.label = axes.get_graph_label(graph2, "g", x=0.8)

        x_tracker = ValueTracker(-1)
        diff_line = Line(
            start=axes.c2p(-1, f1(-1)), end=axes.c2p(-1, f2(-1)), color=YELLOW
        )

        self.play(FadeIn(axes))
        self.play(
            ShowCreation(graph1), ShowCreation(graph2)
        )
        self.play(Write(graph1.label), Write(graph2.label))
        self.play(ShowCreation(diff_line))
        shadow = diff_line.copy().set_color(WHITE).add_to_back()
        shadow.label = Tex(r"\lVert f-g\rVert\,").next_to(shadow, LEFT)
        self.add(shadow)

        diff_line.add_updater(
            lambda t: t.become(
                Line(
                    start=axes.c2p(x_tracker.get_value(), f1(x_tracker.get_value())),
                    end=axes.c2p(x_tracker.get_value(), f2(x_tracker.get_value())),
                    color=YELLOW
                )
            )
        )
        self.play(x_tracker.animate.set_value(1), run_time=3)
        self.play(Write(shadow.label))
        self.wait()

    def write_theorem(self):
        theorem = self.theorem = Tex(
            r"\forall \eps>0,~\exists p,~\text{s.t.}~\lVert f-p\rVert_\infty<\eps."
        ).next_to(self.title, DOWN, buff=.5)
        self.play(Write(theorem[:5]))
        self.wait()
        self.play(Write(theorem[5:8]))
        self.wait()
        self.play(Write(theorem[8:]))
        self.wait()


class WeierstrassProof(Scene):
    def construct(self) -> None:
        title = Title(
            "Weierstrass, 1885", font_size=48
        ).set_color(YELLOW)
        self.add(title)
        self.wait()
        step1 = Tex(
            "1.~f\\approx \\tilde f",
            tex_to_color_map={'f': YELLOW, '\\tilde f': TEAL},
            font_size=80
        )
        step2 = Tex(
            "2.~\\tilde f \\approx p",
            tex_to_color_map={'\\tilde f': TEAL, 'p': RED},
            font_size=80
        )
        VGroup(step1, step2).arrange(DOWN, buff=1).move_to(ORIGIN)
        for s in (step1, step2):
            self.play(Write(s))
            self.wait()


class Smoothing(Scene):
    def construct(self) -> None:
        axes = Axes(
            num_sampled_graph_points_per_tick=200,
            unit_size=3
        )
        self.add(axes)
        RANGE = (-2, 2)
        graph = axes.get_graph(
            function=f,
            color=YELLOW,
            x_range=RANGE
        )
        graph.label = axes.get_graph_label(graph, 'f(x)', x=1.5)
        smooth_graph = get_conv_graph(axes, f, gt, dx=0.01, x_range=RANGE).set_stroke(opacity=.8)
        smooth_graph.label = axes.get_graph_label(smooth_graph, '\\tilde f(x)', x=1.2)
        self.play(ShowCreation(graph), Write(graph.label), run_time=2)
        self.wait()
        self.play(ShowCreation(smooth_graph), Write(smooth_graph.label), run_time=2)
        self.wait()

        arrows = VGroup(
            Arrow(ORIGIN, DOWN).next_to(axes.c2p(-1, 1), UP),
            Arrow(ORIGIN, DOWN).next_to(axes.c2p(1, 1), UP)
        )
        self.play(*[GrowArrow(a) for a in arrows])
        self.wait()

        self.remove(arrows, smooth_graph, smooth_graph.label)
        self.wait()
        gs_graph = axes.get_graph(gs, color=RED)
        # gs_graph_1 = axes.get_graph(lambda x: gs(x-1, s=0.18), color=RED)
        self.play(ShowCreation(gs_graph))

        s = ValueTracker(1)
        gs_graph.add_updater(
            lambda t: t.become(
                axes.get_graph(
                    lambda x: gs(x, s.get_value()),
                    color=RED
                )
            )
        )
        self.play(
            s.animate.set_value(0.18),
            self.frame.animate.shift(UP * 3),
            run_time=2
        )
        gs_graph.clear_updaters()
        g_label = axes.get_graph_label(
            gs_graph, r"g(x)={1\over\sqrt{2\pi}\sigma}\e^{-{x^2\over 2\sigma^2}}", x=0.2
        ).shift(RIGHT * .5 + UP * 2)
        g_label_1 = Tex("g(x-1)").match_style(g_label).move_to(g_label).align_to(g_label, LEFT).shift(RIGHT * 3)
        g_label_flipped = Tex("g(1-x)").match_style(g_label_1).move_to(g_label_1)
        self.play(Write(g_label))
        self.wait()

        ft0 = Tex(
            r"\tilde f(0)=\int_{-\infty}^{+\infty}f(x)g(x)\d x",
            tex_to_color_map={
                r"\tilde f(0)": TEAL,
                'f(x)': YELLOW,
                'g(x)': RED
            },
            font_size=40
        ).to_corner(UL).shift(UP * 3)
        ft1 = TexText(
            r"$\displaystyle\tilde f(1)=\int_{-\infty}^{+\infty}f(x)g(x-1)\d x$",
            tex_to_color_map={
                r"\tilde f(1)": TEAL,
                'f(x)': YELLOW,
                'g(x-1)': RED
            },
            font_size=40
        ).next_to(ft0, DOWN)
        self.play(Write(ft0))
        self.wait()
        f_line = axes.get_v_line_to_graph(x=1, graph=graph, stroke_width=5)
        self.play(ShowCreation(f_line))
        self.wait()
        self.play(
            gs_graph.animate.shift(3 * RIGHT),
            ReplacementTransform(g_label, g_label_1),
            # FadeOut(g_label[4:]),
            Write(ft1)
        )
        self.wait()

        general = TexText(
            r"$\displaystyle\tilde f(t)=\int_{-\infty}^{+\infty}f(x)g(x-t)\d x$",
            tex_to_color_map={"\\tilde f(t)": TEAL, "f(x)": YELLOW, "g(x-t)": RED}
        ).move_to(VGroup(ft0, ft1)).shift(RIGHT)
        convolution = TexText(
            "$=(f*g)(t)$",
            tex_to_color_map={'f': YELLOW, 'g': RED}
        ).next_to(general[5], DOWN, aligned_edge=LEFT, buff=.8)
        self.play(
            FadeTransform(VGroup(ft0, ft1), general)
        )
        self.wait()
        self.play(Write(convolution))
        self.wait()

        self.play(
            gs_graph.animate.flip(),
            ReplacementTransform(g_label_1, g_label_flipped)
        )
        self.wait()


class Average(Scene):
    def construct(self) -> None:
        title = Title(
            "\\heiti 被环境同化", font_size=48, underline_buff=.3
        ).set_color(YELLOW)
        self.add(title)
        self.wait()

        axes = Axes()  # .shift(DOWN)
        graph = axes.get_graph(np.abs, x_range=(-2, 2), color=YELLOW)
        smoothed_graph = get_conv_graph(
            axes=axes,
            f1=np.abs,
            f2=lambda x: gt(x, 0.1),
            x_range=(-5, 5),
            clip_to_range=(-2, 2)
        )
        graph.point = Dot(axes.get_origin(), fill_color=YELLOW)
        graph.dotlabel = Tex("f(0)") \
            .set_color(graph.point.get_color()) \
            .next_to(graph.point, DOWN)
        smoothed_graph.point = Dot(
            axes.c2p(0, smoothed_graph.y[len(smoothed_graph.y) // 2]),
            fill_color=smoothed_graph.get_color()
        )
        smoothed_graph.dotlabel = Tex("\\tilde f(0)") \
            .set_color(smoothed_graph.get_color()).next_to(smoothed_graph.point, UP)
        self.play(ShowCreation(graph))
        self.play(FadeIn(graph.point, scale=.5), Write(graph.dotlabel))
        self.wait()
        self.play(
            TransformFromCopy(graph, smoothed_graph),
            TransformFromCopy(graph.point, smoothed_graph.point),
        )
        self.add(smoothed_graph, smoothed_graph.point)
        self.play(Write(smoothed_graph.dotlabel))
        self.wait()

        even_avg = Tex(
            r"{\tilde f}(0)=\frac13 f(0) + \frac13 f(-0.1) + \frac13 f(0.1)",
            tex_to_color_map={
                '\\frac13': RED, **{f'f({i})': YELLOW for i in (0, -0.1, 0.1)}, r'{\tilde f}(0)': TEAL
            }
        ).to_edge(DOWN, buff=1)
        weighted_avg = Tex(
            r"{\tilde f}(0)=90\%f(0)+4\%f(\pm 0.1)+1\%f(\pm 0.2)",
            tex_to_color_map={
                **{f'f({i})': YELLOW for i in (0, r"\pm 0.1", r"\pm 0.2")},
                r'90\%': RED, r'4\%': RED, r'1\%': RED, r'{\tilde f}(0)': TEAL
            }
        ).move_to(even_avg)
        self.play(Write(even_avg))
        self.wait()
        self.play(
            ReplacementTransform(even_avg[:6], weighted_avg[:6]),
            ReplacementTransform(even_avg[6:], weighted_avg[6:]),
        )
        self.wait()
        self.play(
            FadeOut(
                VGroup(
                    graph, smoothed_graph,
                    graph.point, smoothed_graph.point,
                    graph.dotlabel, smoothed_graph.dotlabel
                )
            )
        )
        g_avg = TexText(
            r"$\tilde f(0) = \sum_i f(x_i)w(x_i)$", font_size=60,
            tex_to_color_map={"w(x_i)": RED, '\\tilde f(0)': TEAL, 'f(x_i)': YELLOW},
        ).next_to(title, DOWN)
        condition = TexText(
            r"满足 $\sum_i w(x_i)=1$，且$w(x)$集中在0附近.",
            tex_to_color_map={'w(x_i)': RED, 'w(x)': RED}
        ).next_to(g_avg, DOWN)
        continuous = Tex(
            r"\tilde f(0)=\int_{-\infty}^{+\infty}f(x)g(x)\d x",
            font_size=60,
            tex_to_color_map={
                '\\tilde f(0)': TEAL,
                'f(x)': YELLOW,
                'g(x)\\d x': RED
            }
        ).next_to(condition, DOWN, buff=1)
        condition2 = Tex(
            r"\int_{-\infty}^{+\infty}g(x)\d x=1",
            tex_to_color_map={"g(x)\\d x": RED}
        ).next_to(continuous, DOWN)
        self.play(Write(g_avg))
        self.wait()
        self.play(Write(condition))
        self.wait()
        self.play(ReplacementTransform(weighted_avg, continuous))
        self.wait()
        self.play(Write(condition2))
        self.wait()


class Convolution(Scene):
    def construct(self) -> None:
        idea = Text("卷积是一种滑动的加权求和.", font_size=90)
        self.play(Write(idea))
        self.wait()


class Smoothing2(Scene):
    def construct(self) -> None:
        axes = Axes(
            num_sampled_graph_points_per_tick=200,
            unit_size=3
        )
        self.add(axes)
        RANGE = (-2, 2)
        graph = axes.get_graph(
            function=f,
            color=YELLOW,
            x_range=RANGE
        )
        graph.label = axes.get_graph_label(graph, 'f(x)', x=1.5)
        smooth_graph = get_conv_graph(
            axes, f, lambda x: gt(x, t=0.1), dx=0.01, x_range=RANGE
        ).set_stroke(opacity=.8)
        smooth_graph.label = axes.get_graph_label(
            smooth_graph, '(f*g)(x)', x=1.2
        ).shift(UP)

        t = ValueTracker(0.1)
        smooth_graph.add_updater(
            lambda m: m.become(
                get_conv_graph(
                    axes, f, lambda x: gt(x, t=t.get_value()), x_range=RANGE
                ).set_stroke(opacity=.8)
            )
        )

        convolution = Tex(
            r"(f*g)(x)=\int_{-\infty}^{+\infty}f(t)g(x-t)\d t",
            tex_to_color_map={'f': YELLOW, 'g': RED}
        ).next_to(ORIGIN, DOWN, buff=1).add_background_rectangle()

        self.add(graph, graph.label)
        self.wait()
        self.play(ShowCreation(smooth_graph))
        self.wait()
        self.play(t.animate.set_value(1e-4), run_time=2)
        smooth_graph.clear_updaters()
        self.play(Write(smooth_graph.label))
        self.wait()
        self.play(FadeIn(convolution))
        self.wait()

        self.play(FadeOut(VGroup(smooth_graph, smooth_graph.label)))
        self.wait()

        line1 = Line(
            axes.c2p(-2, 0), axes.c2p(-3, 0), color=YELLOW
        ).shift(UP * 0.03)
        line2 = Line(
            axes.c2p(2, 0), axes.c2p(3, 0), color=YELLOW
        )
        self.play(
            ShowCreation(line1), ShowCreation(line2)
        )
        self.wait()


class Extension(Scene):
    def construct(self) -> None:
        axes = Axes()
        general_f = lambda x: 0.5 * x + np.cos(x)
        graph = axes.get_graph(
            general_f,
            color=YELLOW,
            x_range=(-3, 3)
        )
        graph.label = axes.get_graph_label(
            graph, "f(x)", x=2
        )
        line1 = Line(
            axes.c2p(-3, general_f(-3)),
            axes.c2p(-4, 0),
            color=YELLOW
        )
        line2 = Line(
            axes.c2p(3, general_f(3)),
            axes.c2p(4, 0),
            color=YELLOW
        )
        hline1 = Line(4 * LEFT, 8 * LEFT, color=YELLOW).shift(UP * 0.03)
        hline2 = Line(4 * RIGHT, 8 * RIGHT, color=YELLOW)
        self.add(axes, graph, graph.label)
        self.wait()
        self.play(ShowCreation(line1), ShowCreation(line2))
        self.wait()
        self.play(ShowCreation(hline1), ShowCreation(hline2))
        self.wait()


class HeatEquation(Scene):
    def construct(self) -> None:
        axes = Axes(
            num_sampled_graph_points_per_tick=200,
            unit_size=3
        )
        self.add(axes)
        RANGE = (-3, 3)
        t = ValueTracker(1e-4)

        graph = get_convolved_self(
            axes, f, gs, dx=0.01, x_range=RANGE,
            color=YELLOW
        )
        smooth_graph = get_conv_graph(
            axes, f, lambda x: gt(x, t=1e-4),
            dx=0.01, x_range=RANGE
        ).set_stroke(opacity=.8)
        self.add(graph)
        self.wait()
        graph.save_state()
        self.play(
            ReplacementTransform(graph, smooth_graph)
        )
        self.wait()

        name = TexText(
            "Weierstrass transformation / Gaussian blur",
            font_size=60
        ).next_to(ORIGIN, DOWN, buff=1).add_background_rectangle()
        self.play(FadeIn(name))
        self.wait()

        self.play(
            ReplacementTransform(smooth_graph, graph)
        )
        self.wait()
        self.remove(smooth_graph)
        u_label = TexText(
            "$u(x,0)=f(x)$", fill_color=YELLOW
        ).move_to((5, 2, 0))
        self.play(Restore(graph), Write(u_label))
        self.wait()
        # smooth_graph.set_color(YELLOW)
        # self.play(Transform(graph, smooth_graph), run_time=.5, rate_func=linear)
        graph.add_updater(
            lambda m: m.become(
                get_conv_graph(
                    axes, f, lambda x: gt(x, t=t.get_value()),
                    dx=0.01, x_range=RANGE, color=YELLOW
                )
            )
        )
        self.play(t.animate.set_value(1), run_time=10, rate_func=linear)
        self.wait()
        equation = TexText("$u_t'=u_{xx}''$", font_size=70, fill_color=YELLOW) \
            .next_to(name, DOWN).add_background_rectangle()
        self.play(FadeIn(equation))
        self.wait()

        graph.clear_updaters()
        self.play(Restore(graph))
        # smooth_graph.set_stroke(opacity=.5)
        self.play(ShowCreation(smooth_graph), run_time=2)
        ft_label = TexText(
            r"$u(x,10^{-4})$", fill_color=TEAL
        ).move_to((-1.5, 2, 0))
        self.play(Write(ft_label))
        self.wait()


comb = {}


def binomial(n, p, k):
    if (n, k) in comb:
        coef = comb[n, k]
    else:
        coef = math.comb(n, k)
        comb[n, k] = coef
    return coef * (p ** k) * ((1 - p) ** (n - k))


class BernsteinProof(Scene):
    def construct(self) -> None:
        title = Title(
            "Bernstein, $1912$", font_size=48
        ).set_color(YELLOW)
        self.add(title)
        self.wait()

        cm = {
            "x": YELLOW,
            "x_i": RED
        }
        avg = Tex(
            r"f(x) \approx \sum_{i=0}^n f(x_i)w(x_i)",
            tex_to_color_map=cm
        ).next_to(title, DOWN)
        condition = TexText(
            r"满足 $\sum_i w(x_i)=1$，且越靠近$x$，$w(x_i)$越大.",
            tex_to_color_map=cm
        ).next_to(avg, DOWN)
        self.play(Write(avg))
        self.wait()
        self.play(Write(condition))
        self.wait()

        n = 10
        p = 1 / 3
        values = [binomial(n, p, i) for i in range(1 + n)]
        bar = BarChart(
            values,
            max_value=0.3,
            bar_names=['x_{{%s}}' % i for i in range(1 + n)],
            height=3,
        ).to_edge(DOWN, buff=.25).shift(LEFT * 2)
        bar.bars.shift(UP * 0.02)
        bar.bar_labels.shift(DOWN * .2).set_color(cm['x_i'])
        xk = TexText(r"($x_i=\frac in$)", font_size=30, fill_color=BLUE) \
            .next_to(bar.bar_labels)
        self.play(
            ShowCreation(bar.x_axis), ShowCreation(bar.y_axis),
            ShowCreation(bar.x_ticks)
        )
        tick3, tick4 = bar.x_ticks[3:5]
        width = tick4.get_x() - tick3.get_x()
        line = DashedLine(DOWN, UP * 2, color=YELLOW) \
            .set_x(tick3.get_x() + width / 3).align_to(bar.x_axis, DOWN)
        line.label = Tex("x", fill_color=YELLOW, font_size=40).next_to(line, UP)
        X = Tex(
            r"X\sim \mathrm{Bin}(n,x)",
            tex_to_color_map=cm
        ).next_to(bar, RIGHT, aligned_edge=UP)
        Xn = Tex(
            r"x\approx \frac Xn",
            tex_to_color_map=cm
        ).next_to(X, DOWN)

        weight = TexText(r"$w(x_i)=P(\frac Xn=x_i)$", tex_to_color_map=cm).move_to(Xn)
        weight2 = TexText(r"$=P(X=i)$").next_to(weight[5], DOWN, aligned_edge=LEFT, buff=.5)
        self.play(ShowCreation(line))
        self.play(Write(line.label))
        self.wait()

        self.play(Write(X))
        self.wait()

        self.play(Write(Xn))
        self.wait()

        self.play(FadeIn(bar.bar_labels), FadeIn(bar.y_axis_labels))
        self.play(Write(xk))
        self.wait()
        self.play(
            DrawBorderThenFill(bar.bars)
        )
        self.wait()

        self.play(ReplacementTransform(Xn, weight))
        self.wait()
        self.play(Write(weight2))
        self.wait()


class BernsteinProof2(Scene):
    def construct(self) -> None:
        title = Title(
            "Bernstein, $1912$", font_size=48
        ).set_color(YELLOW)
        self.add(title)

        cm = {
            'x': YELLOW,
            'X': YELLOW,
            'n': BLUE,
            'Bin': WHITE
        }
        X = Tex(
            r"X\sim \mathrm{Bin}(n,x)",
            tex_to_color_map=cm
        ).next_to(title, DOWN, buff=.5)
        self.add(X)
        self.wait()

        B = TexText(
            r"$\displaystyle B_n(x)=\sum_{i=0}^n f\left({i\over n}\right) P(X=i)$",
            tex_to_color_map=cm
        ).next_to(X, DOWN)
        B_full = Tex(
            r"=\sum_{i=0}^n f\left({i\over n}\right) {n\choose i}x^i (1-x)^{n-i}",
            tex_to_color_map=cm
        ).next_to(B[5], DOWN, aligned_edge=LEFT, buff=1)

        expectation = Tex(
            r"=E\left[f\left({X\over n}\right)\right]",
            tex_to_color_map=cm
        ).next_to(B_full, DOWN, aligned_edge=LEFT, buff=.5)

        convergence = Tex(
            r"\rightrightarrows f(x)",
            tex_to_color_map=cm
        ).next_to(expectation)
        self.play(Write(B))
        self.wait()
        # self.add(Debug(B))
        self.play(
            ReplacementTransform(B[5:17].copy(), B_full[:12]),
            FadeTransform(B[17:].copy(), B_full[12:])
        )
        self.wait()

        self.play(Write(expectation))
        self.wait()

        self.play(Write(convergence))
        self.wait()

        x_range = TexText(
            r"($x\in[0, 1]$)",
            fill_color=GREEN
        ).to_corner(DL, buff=1)
        self.play(Write(x_range))
        self.wait()


class OtherProofs(Scene):
    def construct(self) -> None:
        # title = Title("\\heiti 其他数学家的证明", font_size=48).set_color(YELLOW)
        # self.add(title)

        lebesgue = TexText(
            "\\underline {Lebesgue, 1898}", fill_color=YELLOW
        ).to_corner(UL, buff=.5)

        cm = {
            'f(x)': YELLOW,
            '|x|': BLUE
        }
        lebesgue_proof = VGroup(
            TexText(r"1. $f(x)\approx$折线.", tex_to_color_map=cm),
            TexText("2. 归结为逼近$|x|$.", tex_to_color_map=cm),
            TexText(r"3. 展开$|x|=\left(1+(x^2-1)\right)^{\frac12}$.", tex_to_color_map=cm)
        ).arrange(DOWN, aligned_edge=LEFT).next_to(lebesgue, DOWN).set_x(0)
        self.play(Write(lebesgue))
        self.wait()

        for p in lebesgue_proof:
            self.play(Write(p))
            self.wait()

        fejer = TexText(
            r"\underline{Fej\'er, $1900$}",
            fill_color=YELLOW
        ).next_to(lebesgue_proof, DOWN).align_to(lebesgue, LEFT)
        self.play(Write(fejer))
        self.wait()
        fejer_proof = TexText(
            r"$f$的Chebyshev级数在Ces\`aro意义下$\rightrightarrows f$.",
            tex_to_color_map={'f': YELLOW}
        ).next_to(fejer, DOWN).set_x(0)

        self.play(Write(fejer_proof))
        self.wait()

        ref = TexText("Pinkus, Allan. ``Weierstrass and approximation theory.'' \\\\ \\textit{Journal of Approximation "
                      "Theory} 107.1(2000): 1-66.", fill_color=RED).to_edge(DOWN, buff=1)
        self.play(Write(ref))
        self.wait()


class App(Scene):
    def construct(self) -> None:
        cm = {
            'f(x)': YELLOW,
            'p_n(x)': BLUE,
            'f^2(x)': YELLOW
        }
        prob = TexText(
            r"$f(x)\in$ $C[0,1]$满足$\int_0^1f(x)x^n\d x=0$，那么$f(x)=0$.",
            tex_to_color_map={'f(x)': YELLOW}
        ).to_edge(UP)
        self.add(prob)
        self.wait()

        proof = VGroup(
            TexText(
                r"\textit{\underline{Proof}}\quad 设 $|| f-p_n || < \eps$，有$\int_0^1f(x) p_n(x)\d x=0$.",
                tex_to_color_map={**cm, 'f': YELLOW, 'p_n': BLUE, 'Proof': WHITE}
            ),
            TexText(
                r"$\displaystyle\int_0^1 f^2(x)\d x=\int_0^1 f^2(x)\d x-\int_0^1 f(x) p_n(x)\d x$",
                tex_to_color_map=cm
            ),
            TexText(
                r"$\displaystyle=\int_0^1 f(x)\cdot \left(f(x)-p_n(x)\right)\d x$",
                tex_to_color_map=cm
            ),
            Tex(
                r"\leq\int_0^1 |f(x)|\cdot|f(x)-p_n(x)|\d x",
                tex_to_color_map=cm
            ),
            Tex(r"\to0")
        ).arrange(DOWN).next_to(prob, DOWN)
        for v in proof[-3:]:
            v.align_to(proof[1][10], LEFT)
        proof[-1].shift(DOWN * .25)

        for v in proof:
            self.play(Write(v))
            self.wait()


class Pic(Scene):
    def construct(self) -> None:
        axes = Axes(
            num_sampled_graph_points_per_tick=200,
            unit_size=3
        ).shift(DOWN * 2)
        self.add(axes)
        RANGE = (-2, 2)
        stroke = 10
        graph = axes.get_graph(
            function=f,
            color=YELLOW,
            x_range=RANGE,
        ).set_stroke(width=stroke)
        graph.label = axes.get_graph_label(graph, 'f(x)', x=1.5)
        smooth_graphs = VGroup(
            [
                get_conv_graph(axes, f, lambda x: gt(x, t=t), dx=0.01, x_range=RANGE).set_stroke(opacity=.8)
                for t in np.linspace(1e-3, 0.1, 5)
            ]
        )
        smooth_graphs.set_color_by_gradient(YELLOW, WHITE)
        for i, g in enumerate(smooth_graphs):
            op = (5 - i) / 8
            print(op)
            g.set_stroke(opacity=.7, width=stroke)

        text = TexText(
            r"\textbf{ 多项式 $\rightrightarrows$ 连续函数}",
            font_size=120,
            stroke_width=2,
            tex_to_color_map={
                '多项式': BLUE,
                '连续': YELLOW
            }
        ).add_background_rectangle().to_edge(UP, buff=1)
        self.add(
            axes, graph, smooth_graphs, text
        )
