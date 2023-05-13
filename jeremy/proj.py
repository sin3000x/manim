from manimlib import *


class NotProj(Scene):
    def construct(self) -> None:
        bg = NumberPlane(faded_line_style={'stroke_opacity': 0},
                         background_line_style={'stroke_opacity': .5,
                                                'stroke_color': BLUE_D})
        plane = NumberPlane(faded_line_style={'stroke_opacity': 0})
        dot = Dot(plane.c2p(1, 0), fill_color=YELLOW)
        self.add(plane, bg, dot)

        A = np.array([[1, 1], [1, 1]])
        P = np.array([[1/5, 2/5], [2/5, 4/5]])

        self.play(plane.animate.apply_matrix(A), dot.animate.move_to(bg.c2p(1, 1)))
        self.wait()
        self.play(plane.animate.apply_matrix(A), dot.animate.move_to(bg.c2p(2, 2)))
        self.wait()


class Proj(Scene):
    def construct(self) -> None:
        bg = NumberPlane(faded_line_style={'stroke_opacity': 0},
                         background_line_style={'stroke_opacity': .5,
                                                'stroke_color': BLUE_D})
        plane = NumberPlane(faded_line_style={'stroke_opacity': 0})
        dot = Dot(plane.c2p(1, 0), fill_color=YELLOW)
        self.add(plane, bg, dot)

        A = np.array([[1, 1], [1, 1]])
        P = np.array([[1/5, 2/5], [2/5, 4/5]])

        self.play(plane.animate.apply_matrix(P), dot.animate.move_to(bg.c2p(1/5, 2/5)))
        self.wait()
        self.play(plane.animate.apply_matrix(P))
        self.wait()


class ComplementProj(Scene):
    def construct(self) -> None:
        bg = NumberPlane(faded_line_style={'stroke_opacity': 0},
                         background_line_style={'stroke_opacity': .5,
                                                'stroke_color': BLUE_D})
        plane = NumberPlane(faded_line_style={'stroke_opacity': 0})
        dot = Dot(plane.c2p(1, 0), fill_color=YELLOW)
        self.add(plane, bg, dot)

        A = np.array([[1, 1], [1, 1]])
        IP = np.eye(2) - np.array([[1/5, 2/5], [2/5, 4/5]])
        x = [1, 0]
        print(IP)
        print(IP@x)

        self.play(plane.animate.apply_matrix(IP), dot.animate.move_to(bg.c2p(*IP@x)))
        self.wait()
        self.play(plane.animate.apply_matrix(IP))
        self.wait()


class BG(Scene):
    def construct(self) -> None:
        bg = FullScreenRectangle().set_color(WHITE)
        self.add(bg)