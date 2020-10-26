from manimlib.imports import *

class LA(Scene):
    def construct(self):
        A = Matrix([[1,2],[3,4]])
        A.set_row_colors(YELLOW, RED).shift(LEFT)
        At = Matrix([[1,3],[2,4]]).next_to(A, RIGHT)
        At.set_column_colors(YELLOW, RED)
        self.play(Write(A))
        self.wait()
        self.play(ReplacementTransform(A.copy(), At))