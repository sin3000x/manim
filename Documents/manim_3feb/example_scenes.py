#!/usr/bin/env python

from big_ol_pile_of_manim_imports import *

# To watch one of these scenes, run the following:
# python -m manim example_scenes.py SquareToCircle -pl
#
# Use the flat -l for a faster rendering at a lower
# quality.
# Use -s to skip to the end and just save the final frame
# Use the -p to have the animation (or image, if -s was
# used) pop up once done.
# Use -n <number> to skip ahead to the n'th animation of a scene.


class OpeningManimExample(Scene):
    def construct(self):
        title = TextMobject("This is some \\LaTeX")
        basel = TexMobject(
            "\\sum_{n=1}^\\infty "
            "\\frac{1}{n^2} = \\frac{\\pi^2}{6}"
        )
        VGroup(title, basel).arrange_submobjects(DOWN)
        self.play(
            Write(title),
            FadeInFrom(basel, UP),
        )
        self.wait()

        transform_title = TextMobject("That was a transform")
        transform_title.to_corner(UP + LEFT)
        self.play(
            Transform(title, transform_title),
            LaggedStart(FadeOutAndShiftDown, basel),
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
            Write(grid),
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
        group.arrange_submobjects(DOWN)
        group.set_width(FRAME_WIDTH - 2 * LARGE_BUFF)

        self.play(Write(example_text))
        self.play(Write(example_tex))
        self.wait()


class UdatersExample(Scene):
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

class Check1(CheckFormulaByTXT):
    CONFIG={
    "text": TextMobject("TEST")
}


class PythagoreanProof(Scene):
    CONFIG = {
        "square_scale": 2,
    }
    def construct(self):
        left_square, right_square =  Square(), Square()
        VGroup(left_square,right_square)\
                .scale(self.square_scale)\
                .arrange_submobjects(RIGHT,buff=2)

        # LEFT SQUARE SETTINGS
        dots = [
            left_square.point_from_proportion(i * 1/4 + 1/16)
            for i in range(4)
        ]
        dots_corners = [
            left_square.point_from_proportion(i * 1/4)
            for i in range(4)
        ]
        triangles = VGroup(*[
            Polygon(
                dots[i],
                dots_corners[i],
                dots[i-1],
                stroke_width=0,
                fill_opacity=0.7
            )
            for i in range(4)
        ])
        # RIGHT SQUARE SETTINGS
        dots2 = [
            right_square.point_from_proportion(i * 1/4 + j * 1/16)
            for i,j in zip(range(4),[1,3,3,1])
        ]
        dots_corners2 = [
            right_square.point_from_proportion(i * 1/4)
            for i in range(4)
        ]
        middle = np.array([
            dots2[0][0],
            dots2[1][1],
            0
        ])

        all_rectangles = VGroup(*[
            Polygon(
                dots_corners2[i],
                dots2[i],
                middle,
                dots2[i-1],
            )
            for i in range(4)
        ])
        # rectancles: rectangles of the triangles
        rectangles = all_rectangles[0::2]
        # Big and small squares
        squares = all_rectangles[1::2]
        # IMPORTANT
        # use total_points = 3 if you are using the 3/feb release
        # use total_points = 4 if you are using the most recent release
        total_points = 3
        rect_dot = [
            [
                rectangles[i].points[total_points*j]
                for j in range(4)
            ]
            for i in range(2)
        ]
        triangles2 = VGroup(*[
            Polygon(
                rect[i+1],
                rect[i],
                rect[i-1],
                fill_opacity=0.7
            )
            for rect in rect_dot
            for i in [0,2]
        ])
        # FORMULAS
        theorem = TexMobject("c^2","=","a^2","+","b^2",color=BLUE).to_edge(DOWN)
        parts_theorem = VGroup(
            TexMobject("a^2").move_to(left_square),
            TexMobject("b^2").move_to(squares[0]),
            TexMobject("c^2").move_to(squares[1])
        )
        #print(len(triangles2))

        self.play(
            *list(map(
                DrawBorderThenFill,
                [left_square,right_square,triangles.copy()
            ]))
        )
        #"""
        self.play(
            *[
                ApplyMethod(
                    triangles[i].move_to,
                    triangles2[i].get_center()
                )
                for i in range(len(triangles))
            ]
        )
        self.play(
                Rotate(triangles[1],-PI/2),
                Rotate(triangles[2],PI/2),
        )
        self.play(
            ShowCreation(squares),
            Write(parts_theorem)
        )
        #"""

        self.play(
            *[
                ReplacementTransform(
                    t_.copy()[:],r_,
                    run_time=4
                )
                for t_,r_ in zip(parts_theorem,[theorem[2],theorem[-1],theorem[0]])
            ],
            Write(theorem[1]),Write(theorem[-2])
        )

        self.wait(3)
# See old_projects folder for many, many more
