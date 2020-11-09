from manimlib.imports import *

class LA(Scene):
    def construct(self):
        self.transpose()

    def transpose(self):
        a = np.array([[1,2,3],[4,5,6]])
        at = a.T
        A = Matrix(a, h_buff=0.8)
        A.set_row_colors(YELLOW, BLUE).shift(UP)
        Ac = A[0].copy()
        At = Matrix(at).next_to(A, DOWN, buff=MED_LARGE_BUFF)
        At.set_column_colors(YELLOW, BLUE)
        self.play(Write(A))
        self.wait()
        self.play(
            Ac.shift, DOWN*(A.get_y()-At.get_y()),
            Ac.flip, UP+LEFT
        )
        brackets = self.add_brackets(Ac)
        self.play(
            *list(it.chain(*[[Ac[i].flip, DOWN+RIGHT] for i in range(a.size)])),
            Write(brackets)
            )

        # def flip_without_ele(m):
        #     m.shift(DOWN*(A.get_y()-At.get_y()))
        #     m.flip(LEFT+UP)
        #     for i in range(a.size):
        #         m[i].flip(DOWN+RIGHT)
        #     return m
        # self.play(ApplyFunction(flip_without_ele, Ac))

    @staticmethod
    def add_brackets(m):
        bracket_pair = TexMobject("\\left(", "\\right)")
        bracket_pair.scale(2)
        bracket_pair.stretch_to_fit_height(
            m.get_height() + 2 * SMALL_BUFF
        )
        l_bracket, r_bracket = bracket_pair.split()

        l_bracket.next_to(m, LEFT, SMALL_BUFF)
        r_bracket.next_to(m, RIGHT, SMALL_BUFF)
        return VGroup(l_bracket, r_bracket)