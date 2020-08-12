#!/usr/bin/env python

from manimlib.imports import *
import math


# To watch one of these scenes, run the following:
# python -m manim example_scenes.py SquareToCircle -pl
#
# Use the flat -l for a faster rendering at a lower
# quality.
# Use -s to skip to the end and just save the final frame
# Use the -p to have the animation (or image, if -s was
# used) pop up once done.
# Use -n <number> to skip ahead to the n'th animation of a scene.
# Use -r <number> to specify a resolution (for example, -r 1080
# for a 1920x1080 video)


class OpeningManimExample(Scene):
    def construct(self):
        title = TextMobject("This is some \\LaTeX")
        basel = TexMobject(
            "\\sum_{n=1}^\\infty "
            "\\frac{1}{n^2} = \\frac{\\pi^2}{6}"
        )
        VGroup(title, basel).arrange(DOWN)
        self.play(
            Write(title),
            FadeInFrom(basel, UP),
        )
        self.wait()

        transform_title = TextMobject("That was a transform")
        transform_title.to_corner(UP + LEFT)
        self.play(
            Transform(title, transform_title),
            LaggedStart(*map(FadeOutAndShiftDown, basel)),
        )
        self.wait()

        grid = NumberPlane()
        grid_title = TextMobject("This is a grid")
        grid_title.scale(1.5)
        grid_title.move_to(transform_title)

        self.add(grid, grid_title)  # Make sure title is on top of grid
        self.play(
            FadeOut(title),
            FadeInFromDown(grid_title),
            ShowCreation(grid, run_time=3, lag_ratio=0.1),
        )
        self.wait()

        grid_transform_title = TextMobject(
            "That was a non-linear function \\\\"
            "applied to the grid"
        )
        grid_transform_title.move_to(grid_title, UL)
        grid.prepare_for_nonlinear_transform()
        self.play(
            grid.apply_function,
            lambda p: p + np.array([
                np.sin(p[1]),
                np.sin(p[0]),
                0,
            ]),
            run_time=3,
        )
        self.wait()
        self.play(
            Transform(grid_title, grid_transform_title)
        )
        self.wait()


class SquareToCircle(Scene):
    def construct(self):
        circle = Circle()
        square = Square()
        square.flip(RIGHT)
        square.rotate(-3 * TAU / 8)
        circle.set_fill(PINK, opacity=0.5)

        self.play(ShowCreation(square))
        self.play(Transform(square, circle))
        self.play(FadeOut(square))


class WarpSquare(Scene):
    def construct(self):
        square = Square()
        self.play(ApplyPointwiseFunction(
            lambda point: complex_to_R3(np.exp(R3_to_complex(point))),
            square
        ))
        self.wait()


class WriteStuff(Scene):
    def construct(self):
        example_text = TextMobject(
            "This is a some text",
            tex_to_color_map={"text": YELLOW}
        )
        example_tex = TexMobject(
            "\\sum_{k=1}^\\infty {1 \\over k^2} = {\\pi^2 \\over 6}",
        )
        group = VGroup(example_text, example_tex)
        group.arrange(DOWN)
        group.set_width(FRAME_WIDTH - 2 * LARGE_BUFF)

        self.play(Write(example_text))
        self.play(Write(example_tex))
        self.wait()


class UpdatersExample(Scene):
    def construct(self):
        decimal = DecimalNumber(
            0,
            show_ellipsis=True,
            num_decimal_places=3,
            include_sign=True,
        )
        square = Square().to_edge(UP)

        decimal.add_updater(lambda d: d.next_to(square, RIGHT))
        decimal.add_updater(lambda d: d.set_value(square.get_center()[1]))
        self.add(square, decimal)
        self.play(
            square.to_edge, DOWN,
            rate_func=there_and_back,
            run_time=5,
        )
        self.wait()


# See old_projects folder for many, many more
class MyScene(Scene):
    def construct(self):
        j = TextMobject('【解】')
        # ========== title ==============================
        title = TextMobject('那些蜜汁数学操作（')
        title.scale(2)
        self.add(title)
        # self.play(Write(title))
        self.wait()
        self.play(FadeOut(title))

        # ============= 1. (a+b)^n ===========================
        q1 = TextMobject(r"1. 展开$(a+b)^n$.", color=YELLOW)
        q1.to_edge(TOP)
        self.play(Write(q1))
        self.wait()
        j.next_to(q1, DOWN).to_edge(LEFT, buff=1.5)
        s1_l = [TexMobject('(a+b)^n'), TexMobject('(~a~+~b~)^n'),
                TexMobject('(~~a~~+~~b~~)^n'), TexMobject('(~~~a~~~+~~~b~~~)^{~n}'),
                TexMobject('(~~~~~a~~~~~+~~~~~b~~~~~)^{~~~n}')]
        s1_l[0].scale(1.5)
        # s1_l[0].next_to(j, DOWN).move_to(ORIGIN)
        self.play(Write(j))
        self.play(Write(s1_l[0]))
        for i in range(1, 5):
            s1_l[i].scale(1.5)
            # s1_l[i].next_to(j, DOWN).move_to(ORIGIN)
            self.play(ReplacementTransform(s1_l[i - 1], s1_l[i]))

        self.wait(2)
        r1 = TextMobject(r'\textbf{展得真开...}', color=BLUE)
        r1.to_edge(BOTTOM)
        self.play(Write(r1))
        self.wait()
        self.play(FadeOut(q1), FadeOut(j), FadeOut(s1_l[4]), FadeOut(r1))

        # ============= 2. 不等号 ===========================
        q2 = TextMobject('2. 已知$0<x<y<1$，填入不等号：', color=YELLOW)
        q2.to_edge(TOP)

        s2 = TextMobject(r'$\frac{1}{\ln{(1-x^2)}}~~~$', r'$\neq$', r'$~~~\frac{1}{\ln{(1-y^2)}}$')
        s2.scale(1.5)
        s2[0].set_color(YELLOW)
        s2[2].set_color(YELLOW)
        s2_line = Underline(s2[1])
        s2_line.set_length(1.2)
        s2_line.set_color(YELLOW)
        self.play(Write(q2), run_time=3)
        self.play(Write(s2[0]), Write(s2[2]), Write(s2_line))
        self.wait()
        self.play(Write(s2[1]))
        self.wait(2)

        r2 = TextMobject(r'\textbf{真·不等号}', color=BLUE)
        r2.to_edge(BOTTOM)
        self.play(Write(r2))
        self.wait()
        self.play(FadeOut(q2), FadeOut(s2), FadeOut(s2_line), FadeOut(r2))

        # ============= 3. 求x ===========================
        q3 = TextMobject("3. 已知$x^2-x-1=0$，求$x$.", color=YELLOW)
        q3.to_edge(TOP)
        self.play(Write(q3))
        self.wait(1)

        j.next_to(q3, DOWN).to_edge(LEFT, buff=1.5)
        s3 = TextMobject('$x$，求你了。').scale(1.5)
        # s3.next_to(j, DOWN).move_to(ORIGIN)
        self.play(Write(j))
        self.play(Write(s3))
        self.wait(2)

        r3 = TextMobject(r'\textbf{...你咋那么听话呢}', color=BLUE)
        r3.to_edge(BOTTOM)
        self.play(Write(r3))
        self.wait()
        self.play(FadeOut(q3), FadeOut(s3), FadeOut(r3), FadeOut(j))

        # ============= 4. 666666 ===========================
        q4 = TextMobject(r'4. 判断$\sum_{n=1}^\infty\frac{\sin x}{n}$的敛散性.', color=YELLOW)
        q4.to_edge(TOP)
        j.next_to(q4, DOWN).to_edge(LEFT, buff=1.5)

        s4_1 = TexMobject(r'\sum\limits_{n=1}^\infty\frac{\mathrm{sin}~x}{n}')
        s4_2 = TexMobject(r'\sum\limits_{n=1}^\infty\frac{\mathrm{si\cancel{n}}~x}{\cancel{n}}')
        s4_3 = TexMobject(r'\sum\limits_{n=1}^\infty\frac{\mathrm{si\cancel{n}}~x}{\cancel{n}}',
                          r'=', '\sum\limits_{n=1}^\infty', r'\text{six}')
        s4_4 = TexMobject(r'\sum\limits_{n=1}^\infty\frac{\mathrm{si\cancel{n}}~x}{\cancel{n}}',
                          r'=', r'\sum\limits_{n=1}^\infty', '~6')

        s4_5 = TexMobject(r'=', r'6+6+6+\cdots').align_to(s4_4[1], LEFT)
        s4_5.shift(DOWN * 1.5)
        self.play(Write(q4))
        self.wait(1)

        self.play(Write(j))
        self.play(Write(s4_1))
        self.play(FadeIn(s4_2))
        self.remove(s4_1)
        self.play(ReplacementTransform(s4_2, s4_3), run_time=1)
        self.wait()
        self.play(ReplacementTransform(s4_3, s4_4))
        self.wait()
        self.play(Write(s4_5))

        s4 = TextMobject('故发散。')
        s4.next_to(s4_5, DOWN).align_to(q4, LEFT)
        self.play(Write(s4))
        self.wait(2)

        r4 = TextMobject(r'\textbf{66666666}', color=BLUE)
        r4.to_edge(DOWN)
        self.play(Write(r4))
        self.wait()

        self.play(FadeOut(s4_4), FadeOut(j), FadeOut(s4_5), FadeOut(r4), FadeOut(q4), FadeOut(s4))


class test(Scene):
    def construct(self):
        j = TextMobject('【解】')
        q5 = TextMobject(r'已知$\frac 10=\infty$，证明$\frac 1\infty=0$.', color=YELLOW).to_edge(TOP)
        j.next_to(q5, DOWN).to_edge(buff=1.5)
        self.play(Write(q5))
        self.play(Write(j))


class Graphing(GraphScene):
    CONFIG = {
        "x_min": -5,
        "x_max": 5,
        "y_min": -4,
        "y_max": 4,
        "graph_origin": ORIGIN,
        "function_color": WHITE,
        "axes_color": BLUE
    }

    def construct(self):
        # Make graph
        self.setup_axes(animate=True)
        func_graph = self.get_graph(func_to_graph, self.function_color)
        graph_lab = self.get_graph_label(func_graph, label="x^{2}")

        func_graph_2 = self.get_graph(func_to_graph_2, self.function_color)
        graph_lab_2 = self.get_graph_label(func_graph_2, label="x^{3}")

        vert_line = self.get_vertical_line_to_graph(1, func_graph, color=YELLOW)

        x = self.coords_to_point(1, func_to_graph(1))
        y = self.coords_to_point(0, func_to_graph(1))
        horz_line = Line(x, y, color=YELLOW)

        point = Dot(self.coords_to_point(1, func_to_graph(1)))

        # Display graph
        self.play(ShowCreation(func_graph), Write(graph_lab))
        self.wait(1)
        self.play(ShowCreation(vert_line))
        self.play(ShowCreation(horz_line))
        self.add(point)
        self.wait(1)
        self.play(Transform(func_graph, func_graph_2), Transform(graph_lab, graph_lab_2))
        self.wait(2)

    def func_to_graph(x):
        return x ** 2

    def func_to_graph_2(x):
        return x ** 3
