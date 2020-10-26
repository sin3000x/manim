from manimlib.imports import *

class contour(Scene):
    def construct(self):
        self.opening()

    def opening(self):
        title = TextMobject("\\underline{\\heiti Contour定理}", color=YELLOW).to_corner(UL)
        theorem = TextMobject("$f$在$[a,b]$上",r"{\heiti 连续}~","$\\implies ~f$在$[a,b]$上",r"{\heiti 一致连续}",".")\
            .next_to(title, DOWN).set_x(0).set_color_by_tex("连续", YELLOW)
        self.play(Write(title))
        self.play(Write(theorem))