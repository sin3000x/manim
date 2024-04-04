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
    if x < -1:
        return x + 2
    if x < 1:
        return 1 - np.sqrt(1 - x ** 2)
    if x <= 2:
        return 1 - np.sqrt(1 - (x - 2) ** 2)
    return 0
    # return np.abs(x)


def gt(x, t=1e-4):
    return np.exp(- x ** 2 / (4 * t)) / np.sqrt(4 * PI * t)


def get_conv_graph(axes, f1, f2, dx=0.01, x_range=None, clip_to_range=None):
    if x_range is None:
        x_min, x_max = axes.x_range[:2]
    else:
        x_min, x_max = x_range
    x_samples = np.arange(x_min, x_max + dx, dx)
    f_samples = np.array([f1(x) for x in x_samples])
    # f_samples = f1(x_samples)
    g_samples = f2(x_samples)
    # g_samples = np.array([f2(x) for x in x_samples])
    full_conv = np.convolve(f_samples, g_samples)
    # print(f"{full_conv=}")
    x0 = len(x_samples) // 2 - 1  # TODO, be smarter about this
    # x0 = 99
    # x0 = round(len(x_samples) // 2 - 1 - (x_max - 1) / (2 * dx))
    conv_samples = full_conv[x0:x0 + len(x_samples)]
    conv_graph = VMobject()
    conv_graph.set_stroke(TEAL, 6)
    # conv_graph.set_points_smoothly(
    #     axes.c2p(x_samples, conv_samples * dx),
    # )
    if clip_to_range:
        l, r = clip_to_range
        indices = np.where((x_samples >= l) & (x_samples <= r))
        x_samples = x_samples[indices]
        y_samples = (conv_samples * dx)[indices]
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
            tex_to_color_map = {'\\tilde f': TEAL, 'p': RED},
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

class Average(Scene):
    def construct(self) -> None:
        title = Title(
            "\\heiti 被环境同化", font_size=48, underline_buff=.3
        ).set_color(YELLOW)
        self.add(title)
        self.wait()

        axes = Axes()#.shift(DOWN)
        graph = axes.get_graph(np.abs, x_range=(-2, 2))
        smoothed_graph = get_conv_graph(
            axes=axes,
            f1=np.abs,
            f2=lambda x: gt(x, 0.1),
            x_range=(-5, 5),
            clip_to_range=(-2, 2)
        )
        graph.point = Dot(axes.get_origin(), fill_color=YELLOW)
        graph.dotlabel = Tex("f(0)")\
            .set_color(graph.point.get_color())\
            .next_to(graph.point, DOWN)
        smoothed_graph.point = Dot(
            axes.c2p(0, smoothed_graph.y[len(smoothed_graph.y) // 2]),
            fill_color=smoothed_graph.get_color()
        )
        smoothed_graph.dotlabel = Tex("\\tilde f(0)")\
            .set_color(smoothed_graph.get_color()).next_to(smoothed_graph.point, UP)
        self.play(ShowCreation(graph))
        self.play(FadeIn(graph.point, scale=.5), Write(graph.dotlabel))
        self.wait()
        self.play(
            RT(graph.copy(), smoothed_graph),
            RT(graph.point.copy(), smoothed_graph.point),
        )
        self.play(Write(smoothed_graph.dotlabel))
        self.wait()

        even_avg = Tex(
            r"\tilde f(0)=\frac13 f(0) + \frac13 f(-0.1) + \frac13 f(0.1)",
            tex_to_color_map={'\\frac13': RED}
        ).to_edge(DOWN, buff=1)
        weighted_avg = Tex(
            r"\tilde f(0)=90\%f(0)+4\%f(\pm 0.1)+1\%f(\pm 0.2)",
            tex_to_color_map={r'90\%': RED, r'4\%': RED, r'1\%': RED}
        ).move_to(even_avg)
        g_avg = Tex(
            "1==1",
            # r"\tilde f(0) = \sum_i f(x_i)g(x_i)",
            # tex_to_color_map={"g(x_i)": RED},
            isolate=['=']
        )
        self.play(Write(even_avg))
        self.wait()
        self.play(
            RT(even_avg[:6], weighted_avg[:6]),
            RT(even_avg[6:], weighted_avg[6:]),
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
        # self.play(Write(g_avg))
        self.add(g_avg)

