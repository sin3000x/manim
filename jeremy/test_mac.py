from manimlib.imports import *


class main(Scene):
    def ShadeArrow(self, arrow, ratio=None):
        line = Line(arrow.get_start(), arrow.get_end(), color=RED)
        if ratio is None:
            ratio = 0.2 / line.get_length()
        tip = arrow.get_tip().copy().set_color(RED)
        # self.play()
        return VGroup(line, tip), AnimationGroup(GrowArrow(line), FadeIn(tip), lag_ratio=ratio)

    def UnshadeArrow(self, arrow, ratio=None):
        line = Line(arrow.get_end(), arrow.get_start(), color=RED)
        if ratio is None:
            ratio = 0.5-0.2 / line.get_length()
        tip = arrow.get_tip().copy().set_color(RED)
        self.play(AnimationGroup(FadeIn(tip), GrowArrow(line), lag_ratio=ratio))
        return VGroup(line, tip)

    def construct(self):
        arrow = Line(ORIGIN, RIGHT+UP).add_tip(tip_length=.2)
        # line = Line(color=RED)
        self.add(arrow)
        new = self.ShadeArrow(arrow)
        self.play(FadeOut(new))
        new = self.UnshadeArrow(arrow)
        self.play(FadeOut(new))


class attain(GraphScene):
    CONFIG = {"y_max": 4.5, "x_max": 3.5, "x_tick_frequency": 4.5, "x_leftmost_tick": -1, "y_tick_frequency": 5.5}
    def construct(self):
        self.setup_axes()
        graph = self.get_graph(lambda x: (x-1)**2+.2, x_min=0, x_max=3, stroke_width=16)
        self.add(graph)
        line_min, line_max = DashedLine(self.coords_to_point(1, 0.2), self.coords_to_point(0, 0.2), color=YELLOW),\
                             DashedLine(self.coords_to_point(0, 4.2), self.coords_to_point(3, 4.2), color=YELLOW)
        self.add(line_min, line_max)
        m, M = TextMobject(r"\textbf{\heiti 最小值}", color=YELLOW).scale(1.2).next_to(line_min, LEFT), \
               TextMobject(r"\textbf{\heiti 最大值}", color=YELLOW).scale(1.2).next_to(line_max, LEFT)
        bg = BackgroundRectangle(m)
        self.add(bg)
        self.add(m, M)


class bound(GraphScene):
    CONFIG = {"y_max": 4.5, "x_max": 3.5, "x_tick_frequency": 4.5, "x_leftmost_tick": -1, "y_tick_frequency": 5.5}
    def construct(self):
        self.setup_axes()
        f = lambda x: np.sin(5*x)/x+1
        graph = self.get_graph(lambda x: np.sin(5*x)/x+1, x_min=.3, x_max=3, stroke_width=16)
        self.add(graph)
        line_left, line_right = DashedLine(self.coords_to_point(0.3, 0), self.coords_to_point(0.3, f(0.3)), color=YELLOW),\
                                DashedLine(self.coords_to_point(3, 0), self.coords_to_point(3, f(3)), color=YELLOW)

        bound=TextMobject(r"\textbf{\heiti 有界}", color=YELLOW).scale(3).shift(LEFT*0.5+UP)
        self.add(bound)
        self.add(line_left, line_right)