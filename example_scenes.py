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
class Sao(Scene):
    def construct(self):
        j = TextMobject('【解】')
        z = TextMobject('【证明】')
        # ========== title ==============================
        title = TextMobject('那些蜜汁数学操作（')
        title.scale(2)
        self.add(title)
        # self.play(Write(title))
        self.wait()
        self.play(FadeOut(title))

        # ============= 1. (a+b)^n ===========================
        q1 = TextMobject(r"1. 展开",r"$(a+b)^n$",".", color=YELLOW)
        q1.to_edge(TOP).shift(UP)
        self.play(Write(q1))
        self.wait()
        j.next_to(q1, DOWN).to_edge(LEFT, buff=1.5)
        s1_l = [TextMobject('$(a+b)^n$'), TexMobject('(~a~+~b~)^n'),
                TexMobject('(~~a~~+~~b~~)^n'), TexMobject('(~~~a~~~+~~~b~~~)^{~n}'),
                TexMobject('(~~~~~a~~~~~+~~~~~b~~~~~)^{~~~n}')]
        # s1_l[0].next_to(j, DOWN).move_to(ORIGIN)
        self.play(Write(j))
        self.play(ReplacementTransform(q1[1].copy(), s1_l[0]))
        for i in range(1, 5):
            # s1_l[i].scale(1.5)
            # s1_l[i].next_to(j, DOWN).move_to(ORIGIN)
            self.play(ReplacementTransform(s1_l[i - 1], s1_l[i]))

        self.wait(2)
        r1 = TextMobject(r'\textit{展得真开...}', color=BLUE)
        r1.to_edge(BOTTOM)
        framebox = SurroundingRectangle(r1, buff=.1, color=BLUE)
        self.play(ShowCreation(framebox), Write(r1))
        self.wait(2)
        self.play(FadeOut(q1), FadeOut(j), FadeOut(s1_l[4]), FadeOut(r1), FadeOut(framebox))

        # ============= 2. 不等号 ===========================
        q2 = TextMobject('2. 已知$0<x<y<1$，填入不等号：', color=YELLOW)
        q2.to_edge(TOP).shift(UP)

        s2 = TextMobject(r'$\frac{1}{\ln{(1-x^2)}}~~~$', r'$\neq$', r'$~~~\frac{1}{\ln{(1-y^2)}}$')
        s2.scale(1.5)
        s2[0].set_color(YELLOW)
        s2[2].set_color(YELLOW)
        s2_line = Underline(s2[1])
        s2_line.set_length(1.2)
        s2_line.set_color(YELLOW)
        self.play(Write(q2), run_time=3)
        self.play(Write(s2[0]), Write(s2[2]), Write(s2_line))
        self.wait(2)
        self.play(Write(s2[1]))
        self.wait(2)

        r2 = TextMobject(r'\textit{真·不等号}', color=BLUE)
        r2.to_edge(BOTTOM)
        framebox = SurroundingRectangle(r2, buff=.1, color=BLUE)
        self.play(ShowCreation(framebox), Write(r2))
        self.wait(2)
        self.play(FadeOut(q2), FadeOut(s2), FadeOut(s2_line), FadeOut(r2), FadeOut(framebox))

        # ============= 3. 求x ===========================
        q3 = TextMobject("3. 已知$x^2-x-1=0$，求$x$.", color=YELLOW)
        q3.to_edge(TOP).shift(UP)
        self.play(Write(q3))
        self.wait(1)

        j.next_to(q3, DOWN).to_edge(LEFT, buff=1.5)
        s3 = TexMobject(r'x\text{，求你了.}')
        # s3.next_to(j, DOWN).move_to(ORIGIN)
        self.play(Write(j))
        self.wait()
        self.play(Write(s3))
        self.wait(2)

        r3 = TextMobject(r'\textit{大丈夫能屈能伸！}', color=BLUE)
        r3.to_edge(BOTTOM)
        framebox = SurroundingRectangle(r3, buff=.1, color=BLUE)
        self.play(ShowCreation(framebox), Write(r3))
        self.wait(2)
        self.play(FadeOut(q3), FadeOut(s3), FadeOut(r3), FadeOut(j), FadeOut(framebox))

        # ============= 4. 666666 ===========================
        q4 = TextMobject(r'4. 判断',r'$\sum_{n=1}^\infty\frac{\sin x}{n}$','的敛散性.', color=YELLOW)
        q4.to_edge(TOP).shift(UP)
        j.next_to(q4, DOWN).to_edge(LEFT, buff=1.5)

        s4_1 = TexMobject(r'\sum\limits_{n=1}^\infty\frac{\mathrm{sin}~x}{n}').shift(UP)
        s4_2 = TexMobject(r'\sum\limits_{n=1}^\infty\frac{\mathrm{si\cancel{n}}~x}{\cancel{n}}').shift(UP)
        s4_3 = TexMobject(r'\sum\limits_{n=1}^\infty\frac{\mathrm{si\cancel{n}}~x}{\cancel{n}}',
                          r'=', '\sum\limits_{n=1}^\infty', r'\text{six}').shift(UP)
        s4_4 = TexMobject(r'\sum\limits_{n=1}^\infty\frac{\mathrm{si\cancel{n}}~x}{\cancel{n}}',
                          r'=', r'\sum\limits_{n=1}^\infty', '~6').shift(UP)

        s4_5 = TexMobject(r'=', r'6+6+6+\cdots').align_to(s4_4[1], LEFT).shift(DOWN*0.7)
        self.play(Write(q4))
        self.wait(1)

        self.play(Write(j))
        self.play(ReplacementTransform(q4[1].copy(), s4_1))
        self.play(FadeIn(s4_2))
        self.remove(s4_1)
        self.play(ReplacementTransform(s4_2, s4_3), run_time=1)
        self.wait()
        self.play(ReplacementTransform(s4_3, s4_4))
        self.wait()
        self.play(Write(s4_5))

        s4 = TextMobject('故发散.')
        s4.next_to(s4_5, DOWN).align_to(q4, LEFT)
        self.play(Write(s4))
        self.wait(2)

        r4 = TextMobject(r'\texttt{66666666...}', color=BLUE)
        r4.to_edge(BOTTOM).shift(DOWN)
        framebox = SurroundingRectangle(r4, buff=.1, color=BLUE)
        self.play(ShowCreation(framebox), Write(r4))
        self.wait(2)

        self.play(FadeOut(s4_4), FadeOut(j), FadeOut(s4_5), FadeOut(r4), FadeOut(q4), FadeOut(s4), FadeOut(framebox))
        # ============= 5. 1/0 ===========================
        q5 = TextMobject(r'5. 已知',r'$\frac 10=\infty$',r'，证明$\frac 1\infty=0$.', color=YELLOW).to_edge(TOP).shift(UP)
        z.next_to(q5, DOWN).to_edge(buff=1.5)
        self.play(Write(q5))
        self.wait()
        self.play(Write(z))

        s5_1 = TexMobject(r'{','1','\\over','0',r'}', '=', r'\infty')
        s5_2 = TexMobject(r'{','1','\\over','0',r'}', '=', r'\infty').rotate(PI/2)
        s5_31 = TexMobject('8').move_to(s5_2[-1])
        s5_32 = TexMobject('8','-8').move_to(s5_31)
        s5_33 = TexMobject('0').move_to(s5_32)
        s5_41 = TexMobject('-10').move_to(s5_2[2])
        s5_42 = TexMobject('-10','-8').move_to(s5_41)
        s5_43 = TexMobject('-18').move_to(s5_42)

        self.play(ReplacementTransform(q5[1].copy(),s5_1))
        self.wait()
        self.play(ReplacementTransform(s5_1, s5_2))
        self.wait()
        self.play(Transform(s5_2[-1], s5_31))   # inf -> 8
        self.wait()
        self.play(Transform(s5_2[0:5], s5_41))   # 1/0 -> -10
        self.wait()
        self.play(Transform(s5_2[-1], s5_32), Transform(s5_2[0:5], s5_42))
        self.wait()
        self.play(Transform(s5_2[-1], s5_33), Transform(s5_2[0:5], s5_43))
        self.wait()
        self.play(Transform(s5_2, s5_2.copy().rotate(-PI/2)))
        self.wait()

        s5_51 = TexMobject('{','1','\\over','\\infty').move_to(s5_2[0:5])
        s5_52 = TexMobject('0').move_to(s5_2[-1])
        self.play(Transform(s5_2[0:5], s5_51))
        self.wait()
        self.play(Transform(s5_2[-1], s5_52))
        self.wait()

        s5 = TextMobject('证毕.').next_to(s5_2, DOWN).align_to(q5, LEFT)
        self.play(Write(s5))
        self.wait(2)

        r5 = TextMobject('\\textit{步\\quad 步\\quad 惊 \\quad 心}', color=BLUE).to_edge(BOTTOM).shift(DOWN)
        framebox = SurroundingRectangle(r5, buff=.1, color=BLUE)
        self.play(ShowCreation(framebox), Write(r5), run_time=2)
        self.wait(2)
        self.play(FadeOut(q5), FadeOut(r5), FadeOut(s5), FadeOut(s5_2), FadeOut(framebox), FadeOut(z))

        # ============6. lim 5===================================================
        q6 = TextMobject(r'6. 已知$$\lim\limits_{x\to8}{1\over{x-8}}=\infty,$$那么', color=YELLOW).to_edge(TOP).shift(UP)
        s6 = TexMobject(r'\lim\limits_{x\to5}{1\over{x-5}}=','~5').next_to(q6, DOWN)
        s6[0].set_color(YELLOW)
        s6[1].scale(1.3)
        self.play(Write(q6), run_time=4)
        self.play(Write(s6[0]))
        self.wait(2)
        s6[1].rotate(PI/2)
        self.play(Write(s6[1]))
        self.wait()

        r6 = TextMobject('\\textit{我也想躺会...}', color=BLUE).to_edge(BOTTOM).shift(DOWN)
        framebox = SurroundingRectangle(r6, buff=.1, color=BLUE)
        self.play(ShowCreation(framebox), Write(r6), run_time=2)
        self.wait(2)

        self.play(FadeOut(s6), FadeOut(q6), FadeOut(r6), FadeOut(framebox))

        # =======7. 3*9===============================================================
        q7 = TextMobject(r'7. 求$3\times 9.$', color=YELLOW).to_edge(TOP).shift(UP)
        self.play(Write(q7))
        self.wait()
        j.next_to(q7, DOWN).to_edge(buff=1.5)
        self.play(Write(j))

        s7_1 = TexMobject(r"3\times 9=",r"3", r"\times", r"\sqrt", r"{81}").shift(UP)
        s7_2 = TexMobject(r"3", r"\sqrt", r"{", '8', '1', "}").move_to(s7_1[1:])
        s7_2_2 = TexMobject(r"3", r"\sqrt", r"{81}").move_to(s7_1[1:])
        self.play(Write(s7_1))
        self.play(ReplacementTransform(s7_1[1:], s7_2_2))
        self.add(s7_2)
        self.remove(s7_2_2)
        self.wait(0.5)

        s7_3 = TexMobject('2').next_to(s7_2, UP).align_to(s7_2[3], LEFT)
        self.play(Write(s7_3))

        s7_4 = TexMobject('6').next_to(s7_2, DOWN).align_to(s7_2[3], LEFT)
        self.play(Write(s7_4))
        self.wait(0.5)

        line7 = Line().move_to(s7_4).shift(DOWN*0.3)
        line7.set_length(1.5)
        line7.set_stroke(width=2)
        self.play(ShowCreation(line7), run_time=0.3)
        self.wait(0.5)

        s7_5 = TexMobject('21').next_to(line7, DOWN, buff=0.2).align_to(s7_4, LEFT)
        self.play(Write(s7_5))

        s7_6 = TexMobject('27').next_to(s7_2, UP).align_to(s7_2[3], LEFT)
        self.play(Transform(s7_3, s7_6))

        s7_7 = s7_5.copy().next_to(s7_5, DOWN)
        self.play(Write(s7_7))

        line7_2 = Line().move_to(s7_7).shift(DOWN*0.3)
        line7_2.set_length(1.5)
        line7_2.set_stroke(width=2)
        self.play(ShowCreation(line7_2), run_time=0.3)

        s7_8 = TexMobject('0').next_to(line7_2, DOWN, buff=0.2).align_to(s7_7, RIGHT)
        self.play(Write(s7_8))

        box = SurroundingRectangle(s7_6, color=YELLOW)
        s7 = TextMobject('即为所求.').next_to(box, RIGHT)
        s7.scale(0.8)
        self.play(ShowCreation(box))
        self.play(Write(s7))
        self.wait(2)

        r7 = TextMobject('\\textit{居然对了才是最骚的}', color=BLUE).to_edge(BOTTOM).shift(DOWN)
        framebox = SurroundingRectangle(r7, buff=.1, color=BLUE)
        self.play(ShowCreation(framebox), Write(r7), run_time=2)
        self.wait(2)
        self.play(FadeOut(s7_1),FadeOut(s7_2),FadeOut(s7_3),FadeOut(s7_4),
                  FadeOut(s7_5),FadeOut(s7_6),FadeOut(s7_7),FadeOut(s7_8),FadeOut(s7),
                  FadeOut(line7),FadeOut(line7_2),FadeOut(r7),FadeOut(framebox),FadeOut(j),
                  FadeOut(box), FadeOut(q7))

        # ================ end =======================
        end = TextMobject(r'感谢收看(￣$\nabla$￣)$\~{}$*')
        end.scale(2)
        self.add(end)
        self.wait(2)

class test(Scene):
    def construct(self):
        # theorem
        theorem_name = TextMobject(r'\underline{\textbf{Hamilton-Cayley定理}}').set_color(YELLOW)\
            .to_corner(LEFT+TOP).shift(UP*1.5)
        theorem_content = TextMobject(r'设矩阵$A$的特征多项式$f(\lambda)=|\lambda E-A|$, ', r'则有$f(A)=O.$')\
            .set_color(YELLOW).next_to(theorem_name, DOWN).align_to(theorem_name, LEFT).shift(DOWN*0.5)
        self.play(Write(theorem_name))
        self.wait()
        self.play(Write(theorem_content[0]))
        self.wait()
        self.play(Write(theorem_content[1]))
        self.wait()

        # example
        li = TextMobject('【例】').align_to(theorem_content, LEFT).shift(UP*0.5)
        mA = TexMobject(r'A','=',r'\begin{pmatrix} 1 & 2 \\ 3 & 4 \end{pmatrix}').shift(UP*0.5)
        self.play(Write(li))
        self.play(Write(mA))
        self.wait()

        eig = TexMobject(r'|\lambda E-A|',r'=',r'\begin{vmatrix} \lambda-1 & -2 \\ -3 & \lambda-4 \end{vmatrix}',
                         r'=',r'\lambda^2-5\lambda-2')\
            .next_to(mA, DOWN)
        # eig_poly = TexMobject(r'=',r'\lambda^2-5\lambda-2').next_to(eig, DOWN).align_to(eig[1], LEFT)
        self.play(Write(eig))
        self.wait()
        poly = TexMobject(r'\lambda','^2-5',r'\lambda','-2').next_to(eig, DOWN)\
            .align_to(eig, LEFT).set_color_by_tex(r'\lambda', RED)
        poly_A = TexMobject(r'A','^2-5','A','-2','E','=',
                            r'\begin{pmatrix} 1 & 2 \\ 3 & 4 \end{pmatrix}^2'
                            r'-5\begin{pmatrix} 1 & 2 \\ 3 & 4 \end{pmatrix}'
                            r'-2\begin{pmatrix} 1 & 0 \\ 0 & 1 \end{pmatrix}').next_to(eig, DOWN)\
            .align_to(eig, LEFT).set_color_by_tex('A', BLUE).set_color_by_tex('E', BLUE)
        poly = TexMobject(r'\lambda','^2-5',r'\lambda','-2',r'\cdot 1').move_to(poly_A[:5]).set_color_by_tex(r'\lambda', RED)
        poly_O = TexMobject(r'A','^2-5','A','-2','E','=',
                             r'\begin{pmatrix} 0 & 0 \\ 0 & 0 \end{pmatrix}').next_to(eig, DOWN)\
            .align_to(eig, LEFT).set_color_by_tex('A', BLUE).set_color_by_tex('E', BLUE)
        self.play(ReplacementTransform(eig[-1].copy(), poly))
        self.wait()
        self.play(Transform(poly, poly_A[:5]))
        self.wait()
        self.play(Write(poly_A[5:]))
        self.play(Transform(poly_A, poly_O))




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
