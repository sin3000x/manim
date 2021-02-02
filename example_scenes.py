from manimlib.imports import *
import math


# To watch one of these scenes, run the following:
# python -m manim example_scenes.py SquareToCircle
# Use -s to skip to the end and just save the final frame
# Use -w to write the animation to a file
# Use -o to write it to a file and open it once done
# Use -n <number> to skip ahead to the n'th animation of a scene.


class OpeningManimExample(Scene):
    def construct(self):
        title = TexText("This is some \\LaTeX")
        basel = Tex(
            "\\sum_{n=1}^\\infty "
            "\\frac{1}{n^2} = \\frac{\\pi^2}{6}"
        )
        VGroup(title, basel).arrange(DOWN)
        self.play(
            Write(title),
            FadeIn(basel, UP),
        )
        self.wait()

        transform_title = Text("That was a transform")
        transform_title.to_corner(UL)
        self.play(
            Transform(title, transform_title),
            LaggedStartMap(FadeOut, basel, shift=DOWN),
        )
        self.wait()

        fade_comment = Text(
            """
            You probably don't want to overuse
            Transforms, though, a simple fade often
            looks nicer.
            """,
            font_size=36,
            color=GREY_B,
        )
        fade_comment.next_to(
            transform_title, DOWN,
            buff=LARGE_BUFF,
            aligned_edge=LEFT
        )
        self.play(FadeIn(fade_comment, shift=DOWN))
        self.wait(3)

        grid = NumberPlane((-10, 10), (-5, 5))
        grid_title = Text(
            "But manim is for illustrating math, not text",
        )
        grid_title.to_edge(UP)
        grid_title.add_background_rectangle()

        self.add(grid, grid_title)  # Make sure title is on top of grid
        self.play(
            FadeOut(title, shift=LEFT),
            FadeOut(fade_comment, shift=LEFT),
            FadeIn(grid_title),
            ShowCreation(grid, run_time=3, lag_ratio=0.1),
        )
        self.wait()

        matrix = [[1, 1], [0, 1]]
        linear_transform_title = VGroup(
            Text("This is what the matrix"),
            IntegerMatrix(matrix, include_background_rectangle=True),
            Text("looks like")
        )
        linear_transform_title.arrange(RIGHT)
        linear_transform_title.to_edge(UP)

        self.play(
            FadeOut(grid_title),
            FadeIn(linear_transform_title),
        )
        self.play(grid.apply_matrix, matrix, run_time=3)
        self.wait()

        grid_transform_title = Text(
            "And this is a nonlinear transformation"
        )
        grid_transform_title.set_stroke(BLACK, 5, background=True)
        grid_transform_title.to_edge(UP)
        grid.prepare_for_nonlinear_transform(100)
        self.play(
            ApplyPointwiseFunction(
                lambda p: p + np.array([np.sin(p[1]), np.sin(p[0]), 0]),
                grid,
                run_time=5,
            ),
            FadeOut(linear_transform_title),
            FadeIn(grid_transform_title),
        )
        self.wait()


class SquareToCircle(Scene):
    def construct(self):
        circle = Circle()
        circle.set_fill(BLUE, opacity=0.5)
        circle.set_stroke(BLUE_E, width=4)
        square = Square()

        self.play(ShowCreation(square))
        self.wait()
        self.play(ReplacementTransform(square, circle))
        self.wait()

        # This opens an iPython termnial where you can keep writing
        # lines as if they were part of this construct method
        self.embed()
        # Try typing the following lines
        # self.play(circle.stretch, 4, {"dim": 0})
        # self.play(Rotate(circle, TAU / 4))
        # self.play(circle.shift, 2 * RIGHT, circle.scale, 0.25)
        # circle.insert_n_curves(10)
        # self.play(circle.apply_complex_function, lambda z: z**2)


class AnimatingMethods(Scene):
    def construct(self):
        grid = Tex(r"\pi").get_grid(10, 10, height=4)
        self.add(grid)

        # If you pass in a mobject method to the scene's "play" function,
        # it will apply an animation interpolating between the mobject's
        # initial state and whatever happens when you apply that method.
        # For example, calling grid.shift(2 * LEFT) would shift it two units
        # to the left, but the following line animates that motion.
        self.play(grid.shift, 2 * LEFT)
        # The same applies for any method, including those setting colors.
        self.play(grid.set_submobject_colors_by_gradient, BLUE, GREEN)
        self.play(grid.set_height, TAU - MED_SMALL_BUFF)
        self.wait()

        # The method Mobject.apply_complex_function lets you apply arbitrary
        # complex functions, treating the points defining the mobject as
        # complex numbers.
        self.play(grid.apply_complex_function, np.exp, run_time=5)
        self.wait()

        # Even more generally, you could apply Mobject.apply_function,
        # which takes in functions form R^3 to R^3
        self.play(
            grid.apply_function,
            lambda p: [
                p[0] + 0.5 * math.sin(p[1]),
                p[1] + 0.5 * math.sin(p[0]),
                p[2]
            ],
            run_time=5,
        )
        self.wait()


class TextExample(Scene):
    def construct(self):
        # To run this scene properly, you should have "Consolas" font in your computer
        # for full usage, you can see https://github.com/3b1b/manim/pull/680
        text = Text("Here is a text", font="Consolas", font_size=90)
        difference = Text(
            """
            The most important difference between Text and TexText is that\n
            you can change the font more easily, but can't use the LaTeX grammar
            """,
            font="Arial", font_size=24,
            # t2c is a dict that you can choose color for different text
            t2c={"Text": BLUE, "TexText": BLUE, "LaTeX": ORANGE}
        )
        VGroup(text, difference).arrange(DOWN, buff=1)
        self.play(Write(text))
        self.play(FadeIn(difference, UP))
        self.wait(3)

        fonts = Text(
            "And you can also set the font according to different words",
            font="Arial",
            t2f={"font": "Consolas", "words": "Consolas"},
            t2c={"font": BLUE, "words": GREEN}
        )
        slant = Text(
            "And the same as slant and weight",
            font="Consolas",
            t2s={"slant": ITALIC},
            t2w={"weight": BOLD},
            t2c={"slant": ORANGE, "weight": RED}
        )
        VGroup(fonts, slant).arrange(DOWN, buff=0.8)
        self.play(FadeOut(text), FadeOut(difference, shift=DOWN))
        self.play(Write(fonts))
        self.wait()
        self.play(Write(slant))
        self.wait()


class TexTransformExample(Scene):
    def construct(self):
        to_isolate = ["B", "C", "=", "(", ")"]
        lines = VGroup(
            # Surrounding substrings with double braces
            # will ensure that those parts are separated
            # out in the Tex.  For example, here the
            # Tex will have 5 submobjects, corresponding
            # to the strings [A^2, +, B^2, =, C^2]
            Tex("{{A^2}} + {{B^2}} = {{C^2}}"),
            Tex("{{A^2}} = {{C^2}} - {{B^2}}"),
            # Alternatively, you can pass in the keyword argument
            # "isolate" with a list of strings that should be out as
            # their own submobject.  So both lines below are equivalent
            # to what you'd get by wrapping every instance of "B", "C"
            # "=", "(" and ")" with double braces
            Tex("{{A^2}} = (C + B)(C - B)", isolate=to_isolate),
            Tex("A = \\sqrt{(C + B)(C - B)}", isolate=to_isolate)
        )
        lines.arrange(DOWN, buff=LARGE_BUFF)
        for line in lines:
            line.set_color_by_tex_to_color_map({
                "A": BLUE,
                "B": TEAL,
                "C": GREEN,
            })

        play_kw = {"run_time": 2}
        self.add(lines[0])
        # The animation TransformMatchingTex will line up parts
        # of the source and target which have matching tex strings.
        # Here, giving it a little path_arc makes each part sort of
        # rotate into their final positions, which feels appropriate
        # for the idea of rearranging an equation
        self.play(
            TransformMatchingTex(
                lines[0].copy(), lines[1],
                path_arc=90 * DEGREES,
            ),
            **play_kw
        )
        self.wait()

        # Now, we could try this again on the next line...
        self.play(
            TransformMatchingTex(lines[1].copy(), lines[2]),
            **play_kw
        )
        self.wait()
        # ...and this looks nice enough, but since there's no tex
        # in lines[2] which matches "C^2" or "B^2", those terms fade
        # out to nothing while the C and B terms fade in from nothing.
        # If, however, we want the C^2 to go to C, and B^2 to go to B,
        # we can specify that with a key map.
        self.play(FadeOut(lines[2]))
        self.play(
            TransformMatchingTex(
                lines[1].copy(), lines[2],
                key_map={
                    "C^2": "C",
                    "B^2": "B",
                }
            ),
            **play_kw
        )
        self.wait()

        # And to finish off, a simple TransformMatchingShapes would work
        # just fine.  But perhaps we want that exponent on A^2 to transform into
        # the square root symbol.  At the moment, lines[2] treats the expression
        # A^2 as a unit, so we might create a new version of the same line which
        # separates out just the A.  This way, when TransformMatchingTex lines up
        # all matching parts, the only mismatch will be between the "^2" from
        # new_line2 and the "\sqrt" from the final line.  By passing in,
        # transform_mismatches=True, it will transform this "^2" part into
        # the "\sqrt" part.
        new_line2 = Tex("{{A}}^2 = (C + B)(C - B)", isolate=to_isolate)
        new_line2.replace(lines[2])
        new_line2.match_style(lines[2])

        self.play(
            TransformMatchingTex(
                new_line2, lines[3],
                transform_mismatches=True,
            ),
            **play_kw
        )
        self.wait(3)
        self.play(FadeOut(lines, RIGHT))

        # Alternatively, if you don't want to think about breaking up
        # the tex strings deliberately, you can TransformMatchingShapes,
        # which will try to line up all pieces of a source mobject with
        # those of a target, regardless of the submobject hierarchy in
        # each one, according to whether those pieces have the same
        # shape (as best it can).
        source = Text("the morse code", height=1)
        target = Text("here come dots", height=1)

        self.play(Write(source))
        self.wait()
        kw = {"run_time": 3, "path_arc": PI / 2}
        self.play(TransformMatchingShapes(source, target, **kw))
        self.wait()
        self.play(TransformMatchingShapes(target, source, **kw))
        self.wait()


class UpdatersExample(Scene):
    def construct(self):
        square = Square()
        square.set_fill(BLUE_E, 1)

        # On all all frames, the constructor Brace(square, UP) will
        # be called, and the mobject brace will set its data to match
        # that of the newly constructed object
        brace = always_redraw(Brace, square, UP)

        text, number = label = VGroup(
            Text("Width = "),
            DecimalNumber(
                0,
                show_ellipsis=True,
                num_decimal_places=2,
                include_sign=True,
            )
        )
        label.arrange(RIGHT)

        # This ensures that the method deicmal.next_to(square)
        # is called on every frame
        always(label.next_to, brace, UP)
        # You could also write the following equivalent line
        # label.add_updater(lambda m: m.next_to(brace, UP))

        # If the argument itself might change, you can use f_always,
        # for which the arguments following the initial Mobject method
        # should be functions returning arguments to that method.
        # The following line ensures thst decimal.set_value(square.get_y())
        # is called every frame
        f_always(number.set_value, square.get_width)
        # You could also write the following equivalent line
        # number.add_updater(lambda m: m.set_value(square.get_width()))

        self.add(square, brace, label)

        # Notice that the brace and label track with the square
        self.play(
            square.scale, 2,
            rate_func=there_and_back,
            run_time=2,
        )
        self.wait()
        self.play(
            square.set_width, 5, {"stretch": True},
            run_time=3,
        )
        self.wait()
        self.play(
            square.set_width, 2,
            run_time=3
        )
        self.wait()

<<<<<<< HEAD


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


class HC(Scene):
    def construct(self):
        # theorem
        theorem_name = TextMobject(r'\underline{\textbf{Hamilton-Cayley定理}}').set_color(YELLOW)\
            .to_corner(LEFT+TOP).shift(UP*1.5)
        theorem_content = TextMobject(r'设矩阵$A_{n\times n}$的特征多项式$f(\lambda)=|\lambda E-A|$, ', r'则$f(A)=O.$')\
            .set_color(YELLOW).next_to(theorem_name, DOWN).align_to(theorem_name, LEFT).shift(DOWN*0.5)
        self.play(Write(theorem_name))
        self.wait()
        self.play(Write(theorem_content[0]))
        self.wait()
        self.play(Write(theorem_content[1]))
        self.wait()

        # example
        li = TextMobject('【例】').align_to(theorem_content, LEFT).shift(UP * 0.5)
        mA = TexMobject(r'A', '=', r'\begin{pmatrix} 1 & 2 \\ 3 & 4 \end{pmatrix}').shift(UP * 0.5)
        self.play(Write(li))
        self.play(Write(mA))
        self.wait()

        eig = TexMobject(r'|\lambda E-A|', r'=', r'\begin{vmatrix} \lambda-1 & -2 \\ -3 & \lambda-4 \end{vmatrix}',
                         r'=', r'\lambda^2-5\lambda-2') \
            .next_to(mA, DOWN)
        # eig_poly = TexMobject(r'=',r'\lambda^2-5\lambda-2').next_to(eig, DOWN).align_to(eig[1], LEFT)
        self.play(Write(eig))
        self.wait()
        poly_A = TexMobject(r'A', '^2-5', 'A', '-2', 'E', '=',
                            r'\begin{pmatrix} 1 & 2 \\ 3 & 4 \end{pmatrix}^2',
                            r'-5\begin{pmatrix} 1 & 2 \\ 3 & 4 \end{pmatrix}'
                            r'-2\begin{pmatrix} 1 & 0 \\ 0 & 1 \end{pmatrix}').next_to(eig, DOWN) \
            .align_to(eig, LEFT).set_color_by_tex('A', BLUE).set_color_by_tex('E', BLUE)
        poly = TexMobject(r'\lambda', '^2-5', r'\lambda', '-2', r'\cdot 1').move_to(poly_A[:5]). \
            set_color_by_tex_to_color_map({r'\lambda': RED, r'\cdot 1': RED})
        poly_O = TexMobject(r'\begin{pmatrix} 0 & 0 \\ 0 & 0 \end{pmatrix}').move_to(poly_A[6])
        self.play(ReplacementTransform(eig[-1].copy(), poly))
        self.wait()
        self.play(Transform(poly, poly_A[:5]))
        self.wait()
        self.play(Write(poly_A[5:]))
        self.play(Transform(poly_A[6:], poly_O))
        self.wait()
        self.play(FadeOut(VGroup(li, mA, eig, poly, poly_O, poly_A)))

        # proof1
        zheng = TextMobject('【证】').next_to(theorem_content, DOWN).align_to(theorem_content, LEFT)
        l1 = TexMobject(r'\text{记}',r'~B(',r'\lambda',r')=(',r'\lambda',r'E-A)^*',r'\text{ 为 }~',r'\lambda',r'E-A\text{ 的}\underline{\textbf{\textit{伴随阵}}}','~,')\
            .set_color_by_tex(r'\lambda', RED).next_to(theorem_content, DOWN)
        self.play(Write(zheng))
        self.play(Write(l1))
        self.wait()

        # flash back
        shan = TextMobject(r'\textbf{闪回！}').to_corner(LEFT+TOP).scale(1.2).set_color(YELLOW)
        self.play(FadeOut(VGroup(theorem_content, theorem_name, zheng, l1)))
        self.add(shan)
        self.wait()

        s1 = TextMobject(r'矩阵$A=\left(a_{i j}\right)_{n \times n}$的伴随矩阵'
                         r'$$A^*=\left(\begin{array}{cccc} A_{11} & A_{21} & \cdots & A_{n 1} \\'
                         r'A_{12} & A_{22} & \cdots & A_{n 2} \\ '
                         r'\vdots & \vdots & & \vdots \\'
                         r'A_{1 n} & A_{2 n} & \cdots & A_{n n}\end{array}\right)$$').shift(UP)
        s2 = TextMobject(r'其中$A_{ij}$是$a_{ij}$的\underline{\textit{代数余子式}}.').next_to(s1, DOWN)
        s3 = TextMobject(r'满足',r'$AA^*=|A|E$', '.').next_to(s2, DOWN, buff=1.0)
        s3[-2].set_color(YELLOW)
        self.play(Write(s1), runtime=4)
        self.wait()
        self.play(Write(s2))
        self.wait()
        self.play(Write(s3))
        self.wait(3)

        self.play(FadeOut(VGroup(shan, s1, s2, s3)), FadeIn(VGroup(theorem_content, theorem_name, zheng, l1)))

        # proof2
        l2 = TexMobject(r'\text{那么有 }~','B(',r'\lambda',r')(',r'\lambda',r'E-A)=', r'|',r'\lambda',r'E','-','A', r'|', 'E.')\
            .set_color_by_tex(r'\lambda', RED).next_to(l1, DOWN).align_to(l1, LEFT)
        l2_2 = TexMobject('f(',r'\lambda',')','E.').set_color_by_tex('\\lambda', RED).next_to(l2[5],RIGHT)
        self.play(Write(l2))
        self.wait(2)
        self.play(Transform(l2[6:], l2_2))

        # find B(lambda)
        b0_0 = [TexMobject('\\lambda','-2').set_color_by_tex('\\lambda', RED),TexMobject('1'),TexMobject('0')]
        b0_1 = [TexMobject('-2'),TexMobject('\\lambda','+1').set_color_by_tex('\\lambda', RED),TexMobject('3')]
        b0_2 = [TexMobject('-4'),TexMobject('2'),TexMobject('\\lambda','-4').set_color_by_tex('\\lambda', RED)]
        m1 = Matrix([b0_0,b0_1, b0_2], element_to_mobject=lambda x: x,element_alignment_corner=ORIGIN)
        b1 = VGroup(TexMobject('B(',r'\lambda',')','=').set_color_by_tex('\\lambda', RED), m1)\
            .arrange(RIGHT).next_to(l2, DOWN).shift(LEFT)
        star = TexMobject('*').move_to(b1.get_corner(UR))
        line_1 = Line(b1[1][0].get_left()+UP*0.8, b1[1][0].get_right()+UP*0.8).set_color(BLUE)
        line_2 = Line(b1[1][0].get_top()+LEFT*1.4, b1[1][0].get_bottom()+LEFT*1.4).set_color(BLUE)
        self.play(Write(b1))
        self.play(Write(star))
        self.play(ShowCreation(line_1))
        self.play(ShowCreation(line_2))
        self.wait()
        row1 = [TexMobject('\\lambda','+1').set_color_by_tex('\\lambda', RED),TexMobject('3')]
        row2 = [TexMobject('2'),TexMobject('\\lambda','-4').set_color_by_tex('\\lambda', RED)]
        det = Matrix([row1, row2], element_to_mobject=lambda x: x, bracket='v', element_alignment_corner=ORIGIN)\
            .next_to(b1, RIGHT, buff=.8)
        b2 = TexMobject(r'=',r'\lambda',r'^2-3',r'\lambda',r'-10').set_color_by_tex('\\lambda', RED).next_to(det, DOWN)
        self.play(FadeInFrom(det, LEFT))
        self.play(Write(b2))

        ro1 = [TexMobject(r'\lambda',r'^2-3',r'\lambda',r'-10').set_color_by_tex('\\lambda', RED), TexMobject(r'-',r'\lambda','+4').set_color_by_tex('\\lambda', RED), TexMobject('3')]
        ro2 = [TexMobject('2', r'\lambda','-20').set_color_by_tex('\\lambda', RED), TexMobject(r'\lambda',r'^2-6',r'\lambda',r'+8').set_color_by_tex('\\lambda', RED), TexMobject(r'-3',r'\lambda',r'+6').set_color_by_tex('\\lambda', RED)]
        ro3 = [TexMobject('4', r'\lambda').set_color_by_tex('\\lambda', RED), TexMobject('-2',r'\lambda').set_color_by_tex('\\lambda', RED), TexMobject(r'\lambda',r'^2-',r'\lambda').set_color_by_tex('\\lambda', RED)]
        m2 = Matrix([ro1, ro2, ro3], element_to_mobject=lambda x: x, h_buff=3).next_to(b1[0],RIGHT)
        self.play(FadeOut(VGroup(b1[1], star, det, line_1, line_2, b2[0])))
        self.play(Transform(b2[1:], m2[0][0][0:]))
        self.play(FadeIn(m2))
        self.wait()
        b3 = TextMobject(r'$\phi$(>$\omega$<*) 每个元素的次数最高是$n-1$.').next_to(m2, DOWN, buff=.2).scale(1)
        self.play(Write(b3))

        B0 = Matrix([[1,0,0],[0,1,0],[0,0,1]], h_buff=.8, v_buff=.6).scale(.8)
        B1 = Matrix([[-3,-1,0],[2,-6,-3],[4,-2,-1]], h_buff=.8, v_buff=.6).scale(.8)
        B2 = Matrix([[-10,4,3],[-20,8,6],[0,0,0]], h_buff=.8, v_buff=.6).scale(.8)
        b4 = VGroup(TexMobject(r'\lambda','^2').set_color_by_tex('\\lambda', RED), B0, TexMobject('+',r'\lambda')
                    .set_color_by_tex('\\lambda', RED), B1,TexMobject('+'), B2).arrange(RIGHT).next_to(b1[0],RIGHT)
        b5 = b4.copy()
        starts = []
        for i in [1,3,5]:
            b5[i].set_color(BLUE)
            starts.append(b5[i].get_bottom())
        self.play(FadeOut(b2[1:]))
        self.play(ReplacementTransform(m2, b4))
        self.wait()
        self.play(Transform(b4, b5))

        arrows = [Line(start, b3.get_top(), stroke_width=3, preserve_tip_size_when_scaling=True).set_color(BLUE) for start in starts]
        self.play(GrowArrow(arrows[0]), GrowArrow(arrows[1]), GrowArrow(arrows[2]), Transform(b3, TextMobject('\\textit{数字矩阵}').move_to(b3).set_color(BLUE)))

        b6 = TexMobject(r'\lambda',r'^{n-1}',r'B_0',r'+',r'\lambda',r'^{n-2}',r'B_1',r'+',r'\cdots',r'+',r'B_{n-1}').set_color_by_tex("\\lambda", RED).next_to(b1[0], RIGHT)
        self.play(FadeOut(VGroup(*arrows, b3)))
        self.play(ReplacementTransform(b4, b6))
        self.wait()

        ## proof3
        l3 = TexMobject(r'f(',r'\lambda',r')','=',r'\lambda',r'^n+a_1',r'\lambda',r'^{n-1}+\cdots+a_n').set_color_by_tex('\\lambda', RED).next_to(b6, DOWN)
        l3[3].align_to(b1[0][-1], LEFT)
        l3[:3].align_to(b1, LEFT)
        l3[4:].align_to(b6, LEFT)
        self.play(Write(l3))
        self.wait()

        box = SurroundingRectangle(l2[1:], buff=.1).set_color(YELLOW)
        self.play(ShowCreation(box))

        l4 = TexMobject(r'\left(',r'\lambda',r'^{n-1}',r'B_0',r'+',r'\lambda',r'^{n-2}',r'B_1',r'+',r'\cdots',r'+',r'B_{n-1}',r'\right)',r'(',r'\lambda','E-A)').set_color_by_tex("\\lambda", RED).move_to(b6)
        l5 = TexMobject(r'\left(',r'\lambda',r'^n+a_1',r'\lambda',r'^{n-1}+\cdots+a_n',r'\right)','E').set_color_by_tex('\\lambda', RED).move_to(l3)

        # self.play(FadeOut(b1[0]), FadeOut(l3[:4]))
        self.play(FadeOut(b1[0]), FadeOut(l3[:4]), ReplacementTransform(b6, l4[1:12]), ReplacementTransform(l3[4:], l5[1:5]))
        self.play(FadeIn(VGroup(l4[0], l4[12:], l5[0], l5[5:])))
        self.wait()

        # l6 = TexMobject(r'\lambda',r'^n B_0','+',r'\lambda',r'^{n-1}(B_1-B_0 A)','+',r'\lambda',r'^{n-2}(B_2-B_1
        # A)+\cdots+',r'\lambda',r'(B_{n-1}-B_{n-2}A)-B_{n-1}A').set_color_by_tex('\\lambda', RED).move_to(l4)
        l6 = TexMobject(r'\lambda',r'^n',' B_0','+',r'\lambda',r'^{n-1}','(B_1-B_0 A)','+','\cdots','+',r'\lambda',r'(B_{n-1}-B_{n-2}A)','-','B_{n-1}','A').set_color_by_tex('\\lambda', RED).move_to(l4)
        #                  0         1      2    3       4         5           6        7    8       9      10         11                 12      13     14
        l7 = TexMobject(r'\lambda',r'^n',' E','+','a_1 ',r'\lambda',r'^{n-1}','E','+','\cdots','+','a_{n-1}',r'\lambda',r' E','+','a_n E').set_color_by_tex('\\lambda', RED).move_to(l5).align_to(ORIGIN, ORIGIN)
        #                  0        1      2   3    4          5        6      7   8     9      10    11           12      13  14   15
        l7[:3].align_to(l6[:3], LEFT)
        l7[3].align_to(l6[3], LEFT)
        l7[4:8].align_to(l6[4:7], LEFT)
        l7[8].align_to(l6[7], LEFT)
        l7[9].align_to(l6[8], LEFT)
        l7[10].align_to(l6[9], LEFT)
        l7[11:14].align_to(l6[10:12], LEFT)
        l7[14].align_to(l6[12], LEFT)
        l7[15].align_to(l6[13:], LEFT)

        # match color
        first, second, third, fourth = YELLOW, GREEN, BLUE, PURPLE
        l6_1 = l6.copy()
        tmp = l6.copy()
        l7_1 = l7.copy()
        l6_1[2].set_color(first)
        l7_1[2].set_color(first)
        l6_1[6].set_color(second)
        l7_1[4].set_color(second)
        l7_1[7].set_color(second)
        l6_1[11].set_color(third)
        l7_1[11].set_color(third)
        l7_1[13].set_color(third)
        l6_1[12:].set_color(fourth)
        l7_1[14:].set_color(fourth)

        self.play(ReplacementTransform(l4, l6))
        self.play(ReplacementTransform(l5, l7))
        self.play(ReplacementTransform(l6, l6_1), ReplacementTransform(l7, l7_1))

        # brace
        l8_1 = VGroup(l6_1[2].copy(), TexMobject('='), l7_1[2].copy()).arrange(RIGHT).to_edge(TOP).shift(UP)
        # l8_2 = VGroup(l6_1[6].copy(), TexMobject('='), l7_1[4].copy(), l7_1[7].copy()).arrange(RIGHT).next_to(l8_1, DOWN)
        l8_2 = VGroup(l6_1[6].copy(), TexMobject('='), TexMobject('a_1','E').set_color(second)).arrange(RIGHT).next_to(l8_1, DOWN)
        # l8_3 = VGroup(l6_1[11].copy(), TexMobject('='), l7_1[11].copy(), l7_1[13].copy()).arrange(RIGHT).next_to(l8_2, DOWN)
        l8_0 = TexMobject('\\vdots').next_to(l8_2, DOWN).align_to(l8_1[1].get_center(), LEFT)

        l8_3 = VGroup(l6_1[11].copy(), TexMobject('='), TexMobject('a_{n-1}','E').set_color(third)).arrange(RIGHT).next_to(l8_0, DOWN)
        l8_4 = VGroup(l6_1[12:].copy(), TexMobject('='), l7_1[15].copy()).arrange(RIGHT).next_to(l8_3, DOWN)
        for l in [l8_2, l8_3, l8_4]:
            l[0].align_to(l8_1[0], RIGHT)
            l[1].align_to(l8_1[1], LEFT)
            l[2].align_to(l8_1[2], LEFT)

        br = Brace(VGroup(l8_1, l8_2, l8_0, l8_3, l8_4), LEFT)


        self.play(FadeOut(VGroup(theorem_name, theorem_content, zheng, box, l1, l2)))
        self.play(ReplacementTransform(VGroup(l6_1[2], l7_1[2]), l8_1))
        self.play(ReplacementTransform(VGroup(l6_1[6], l7_1[4], l7_1[7]), l8_2))
        self.play(Write(l8_0))
        self.play(ReplacementTransform(VGroup(l6_1[11], l7_1[11], l7_1[13]), l8_3))
        self.play(ReplacementTransform(VGroup(l6_1[12:], l7_1[14:]), l8_4))

        self.play(GrowFromCenter(br), FadeOut(VGroup(l6_1[:2],l6_1[3:6],l6_1[7:11], l7_1[:2], l7_1[3], l7_1[5:7], l7_1[8:11], l7_1[12])))

        # change color
        dest = TexMobject(r'\text{要证}','f(','A',')=','A','^n+','a_1','A','^{n-1}+\cdots+','a_{n-1}','A','+','a_n', 'E=O.').set_color_by_tex_to_color_map({'A': RED, 'a_1': second, 'a_{n-1}': third, 'a_n': fourth}).to_edge(BOTTOM).shift(DOWN)
        self.play(Write(dest))
        l8_11 = VGroup(TexMobject('B_0').move_to(l8_1[0]), TexMobject('=').move_to(l8_1[1]), TexMobject('E').move_to(l8_1[2]))
        l8_21 = VGroup(TexMobject('(','B_1-B_0','A',')').set_color_by_tex('A', RED).move_to(l8_2[0]), TexMobject('=').move_to(l8_2[1]), TexMobject('a_1','E').set_color_by_tex('a_1', second).move_to(l8_2[2]))
        l8_31 = VGroup(TexMobject('(','B_{n-1}-B_{n-2}','A',')').set_color_by_tex('A', RED).move_to(l8_3[0]), TexMobject('=').move_to(l8_3[1]), TexMobject('a_{n-1}', 'E').set_color_by_tex('a_{n-1}', third).move_to(l8_3[2]))
        tmp.set_color(WHITE)
        tmp[-1].set_color(RED)
        l8_41 = VGroup(tmp[12:].move_to(l8_4[0]), TexMobject('=').move_to(l8_4[1]), TexMobject('a_n','E').set_color_by_tex('a_n', fourth).move_to(l8_4[2]))
        self.play(FadeIn(VGroup(l8_11, l8_21, l8_31, l8_41)))
        self.remove(l8_1, l8_2, l8_3, l8_4)
        self.wait()

        # times A^...
        l9_1 = VGroup(TexMobject('B_0','A','^n').set_color_by_tex('A', RED).move_to(l8_11).align_to(l8_11[0], RIGHT),TexMobject('E','A','^n').set_color_by_tex('A', RED).move_to(l8_11).align_to(l8_11[2], LEFT))
        l9_2 = VGroup(TexMobject('(','B_1-B_0','A',')','A','^{n-1}').set_color_by_tex('A', RED).move_to(l8_21).align_to(l8_21[0], RIGHT), TexMobject('a_1','E','A','^{n-1}').set_color_by_tex('a_1', second).set_color_by_tex('A', RED).move_to(l8_21).align_to(l8_21[2], LEFT))
        l9_3 = VGroup(TexMobject('(','B_{n-1}-B_{n-2}','A',')','A').set_color_by_tex('A', RED).move_to(l8_31).align_to(l8_31[0], RIGHT), TexMobject('a_{n-1}','E','A').set_color_by_tex('a_{n-1}', third).set_color_by_tex('A', RED).move_to(l8_31).align_to(l8_31[2], LEFT))

        self.play(ReplacementTransform(l8_11[0], l9_1[0][0]), FadeIn(l9_1[0][1:]), ReplacementTransform(l8_11[2], l9_1[1][0]), FadeIn(l9_1[1][1:]))
        self.play(ReplacementTransform(l8_21[0], l9_2[0][:4]), FadeIn(l9_2[0][4:]), ReplacementTransform(l8_21[2], l9_2[1][:2]), FadeIn(l9_2[1][2:]))
        br2 = br.copy().shift(LEFT*0.3)
        self.play(ReplacementTransform(br, br2), ReplacementTransform(l8_31[0], l9_3[0][:4]), FadeIn(l9_3[0][4:]), ReplacementTransform(l8_31[2], l9_3[1][:2]), FadeIn(l9_3[1][2:]))
        self.wait()

        # processing
        l10_1_1 = TexMobject('A','^n').set_color_by_tex('A',RED).next_to(l8_11[1], RIGHT)
        l10_2_0 = TexMobject('B_1','A','^{n-1}','-','B_0','A','^n').set_color_by_tex('A',RED).next_to(l8_21[1], LEFT)
        l10_2_1 = TexMobject('a_1','A','^{n-1}').set_color_by_tex('a_1', second).set_color_by_tex('A', RED).next_to(l8_21[1], RIGHT)
        l10_3_0 = TexMobject('B_{n-1}','A','-','B_{n-2}','A','^2').set_color_by_tex('A',RED).next_to(l8_31[1], LEFT)
        l10_3_1 = TexMobject('a_{n-1}','A').set_color_by_tex('a_{n-1}', third).set_color_by_tex('A', RED).next_to(l8_31[1], RIGHT)
        self.play(ReplacementTransform(l9_1[1], l10_1_1))
        self.play(ReplacementTransform(l9_2[0], l10_2_0), ReplacementTransform(l9_2[1], l10_2_1))
        self.play(ReplacementTransform(l9_3[0], l10_3_0), ReplacementTransform(l9_3[1], l10_3_1))
        self.wait()

        # sum
        line_3 = Line(br2.get_corner(DL), br2.get_corner(DL)+RIGHT*8).shift(DOWN*0.5).set_color(YELLOW)
        plus = TexMobject('+').set_color(YELLOW).move_to(br2.get_bottom())
        equal = TexMobject('=').next_to(line_3, DOWN, buff=0.4).align_to(l8_31[1], LEFT)
        self.play(ShowCreation(line_3), Transform(l9_1[0], l9_1[0].copy().align_to(l10_2_0, LEFT)))
        self.play(ReplacementTransform(br2, plus))
        self.play(ReplacementTransform(l8_41[1].copy(), equal))
        self.wait()

        O = TexMobject('O').next_to(equal, LEFT)
        rhs = TexMobject('f(','A',')').set_color_by_tex('A', RED).next_to(equal, RIGHT)
        diag1 = Line(l9_1[0].get_center(), l10_2_0[3:].get_center()).set_color(YELLOW)
        delta = -(l10_2_0[3:].get_center() - l9_1[0].get_center())[1]

        diag2 = diag1.copy().shift(DOWN*delta)
        diag3 = diag2.copy().shift(DOWN*delta)
        diag4 = diag3.copy().shift(DOWN*delta)

        self.play(ReplacementTransform(VGroup(l10_1_1.copy(), l10_2_1.copy(), l10_3_1.copy(), l8_41[-1].copy()), rhs))
        self.wait()
        for diag in [diag1, diag2, diag3, diag4]:
            self.play(ShowCreation(diag))
        self.play(ReplacementTransform(VGroup(l9_1[0].copy(), l10_2_0.copy(), l10_3_0.copy(), l8_41[0].copy()), O))
        self.wait()
        t = TextMobject("(￣$\\nabla$￣) /").next_to(rhs, RIGHT, buff=1)
        self.play(Write(t))
        self.wait()
        self.play(FadeOut(VGroup(l9_1[0], l8_11[1], l10_1_1, l10_2_0, l8_21[1], l10_2_1,
                                 l8_0, l10_3_0, l8_31[1], l10_3_1, l8_4,l8_41,
                                 diag1, diag2, diag3, diag4, line_3, plus,
                                 O, equal, rhs, dest, t)),
                  FadeIn(VGroup(theorem_name,theorem_content, l1, l2, box, zheng)))
        self.wait()


class test(Scene):
    def construct(self):
        mat = Matrix([[1,''], ['', 1]])
        self.add(mat)
        self.wait()


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
        func_graph = self.get_graph(np.sin, self.function_color)
        graph_lab = self.get_graph_label(func_graph, label="\\sin x")

        func_graph_2 = self.get_graph(np.cos, self.function_color)
        graph_lab_2 = self.get_graph_label(func_graph_2, label="\\cos x")

        vert_line = self.get_vertical_line_to_graph(1, func_graph, color=YELLOW)

        x = self.coords_to_point(1, np.sin(1))
        y = self.coords_to_point(0, np.cos(1))
        horz_line = Line(x, y, color=YELLOW)

        point = Dot(self.coords_to_point(1, np.sin(1)))

        # Display graph
        self.play(ShowCreation(func_graph), Write(graph_lab))
        self.wait(1)
        self.play(ShowCreation(vert_line))
        self.play(ShowCreation(horz_line))
        self.add(point)
        self.wait(1)
        self.play(Transform(func_graph, func_graph_2), Transform(graph_lab, graph_lab_2))
        self.wait(2)
=======
        # In general, you can alway call Mobject.add_updater, and pass in
        # a function that you want to be called on every frame.  The function
        # should take in either one argument, the mobject, or two arguments,
        # the mobject and the amount of time since the last frame.
        now = self.time
        w0 = square.get_width()
        square.add_updater(
            lambda m: m.set_width(w0 * math.cos(self.time - now))
        )
        self.wait(4 * PI)


class SurfaceExample(Scene):
    CONFIG = {
        "camera_class": ThreeDCamera,
    }

    def construct(self):
        surface_text = Text("For 3d scenes, try using surfaces")
        surface_text.fix_in_frame()
        surface_text.to_edge(UP)
        self.add(surface_text)
        self.wait(0.1)

        torus1 = Torus(r1=1, r2=1)
        torus2 = Torus(r1=3, r2=1)
        sphere = Sphere(radius=3, resolution=torus1.resolution)
        # You can texture a surface with up to two images, which will
        # be interpreted as the side towards the light, and away from
        # the light.  These can be either urls, or paths to a local file
        # in whatever you've set as the image directory in
        # the custom_defaults.yml file

        # day_texture = "EarthTextureMap"
        # night_texture = "NightEarthTextureMap"
        day_texture = "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4d/Whole_world_-_land_and_oceans.jpg/1280px-Whole_world_-_land_and_oceans.jpg"
        night_texture = "https://upload.wikimedia.org/wikipedia/commons/thumb/b/ba/The_earth_at_night.jpg/1280px-The_earth_at_night.jpg"

        surfaces = [
            TexturedSurface(surface, day_texture, night_texture)
            for surface in [sphere, torus1, torus2]
        ]

        for mob in surfaces:
            mob.shift(IN)
            mob.mesh = SurfaceMesh(mob)
            mob.mesh.set_stroke(BLUE, 1, opacity=0.5)

        # Set perspective
        frame = self.camera.frame
        frame.set_euler_angles(
            theta=-30 * DEGREES,
            phi=70 * DEGREES,
        )

        surface = surfaces[0]

        self.play(
            FadeIn(surface),
            ShowCreation(surface.mesh, lag_ratio=0.01, run_time=3),
        )
        for mob in surfaces:
            mob.add(mob.mesh)
        surface.save_state()
        self.play(Rotate(surface, PI / 2), run_time=2)
        for mob in surfaces[1:]:
            mob.rotate(PI / 2)

        self.play(
            Transform(surface, surfaces[1]),
            run_time=3
        )

        self.play(
            Transform(surface, surfaces[2]),
            # Move camera frame during the transition
            frame.increment_phi, -10 * DEGREES,
            frame.increment_theta, -20 * DEGREES,
            run_time=3
        )
        # Add ambient rotation
        frame.add_updater(lambda m, dt: m.increment_theta(-0.1 * dt))

        # Play around with where the light is
        light_text = Text("You can move around the light source")
        light_text.move_to(surface_text)
        light_text.fix_in_frame()

        self.play(FadeTransform(surface_text, light_text))
        light = self.camera.light_source
        self.add(light)
        light.save_state()
        self.play(light.move_to, 3 * IN, run_time=5)
        self.play(light.shift, 10 * OUT, run_time=5)

        drag_text = Text("Try moving the mouse while pressing d or s")
        drag_text.move_to(light_text)
        drag_text.fix_in_frame()

        self.play(FadeTransform(light_text, drag_text))
        self.wait()


class ControlsExample(Scene):
    def setup(self):
        self.textbox = Textbox()
        self.checkbox = Checkbox()
        self.color_picker = ColorSliders()
        self.panel = ControlPanel(
            Text("Text", size=0.5), self.textbox, Line(),
            Text("Show/Hide Text", size=0.5), self.checkbox, Line(),
            Text("Color of Text", size=0.5), self.color_picker
        )
        self.add(self.panel)

    def construct(self):
        text = Text("", size=2)

        def text_updater(old_text):
            assert(isinstance(old_text, Text))
            new_text = Text(self.textbox.get_value(), size=old_text.size)
            # new_text.align_data_and_family(old_text)
            new_text.move_to(old_text)
            if self.checkbox.get_value():
                new_text.set_fill(
                    color=self.color_picker.get_picked_color(),
                    opacity=self.color_picker.get_picked_opacity()
                )
            else:
                new_text.set_opacity(0)
            old_text.become(new_text)

        text.add_updater(text_updater)

        self.add(MotionMobject(text))

        self.textbox.set_value("Manim")
        # self.wait(60)
        # self.embed()


# See https://github.com/3b1b/videos for many, many more
>>>>>>> fbb0d76f4f3db46c1374e29eba30433e5dbfa9c1
