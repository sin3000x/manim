from big_ol_pile_of_manim_imports import *

class Formula(Scene):
    def construct(self):
        formula_tex = TexMobject(r"""
        \left[\begin{array}{ll}
a & a \\
a & a \\
a & a
\end{array}\right]
""")
        formula_tex.scale(2)
        self.play(Write(formula_tex))
        self.wait()