from manimlib import *


class Vocab(Scene):
    def construct(self):
        t = Vocabulary()
        self.add(t)
        eng = ['diagonalizable', 'similar', 'eigenvalue', 'eigenvector']
        chi = ['可对角化', '相似', '特征值', '特征向量']
        eng = VGroup(*[TexText(s) for s in eng]).scale(1.2).arrange(DOWN, aligned_edge=LEFT, buff=.6)
        chi = VGroup(*[TexText(s) for s in chi]).scale(1.2).arrange(DOWN, aligned_edge=LEFT)

        for c, e in zip(chi, eng):
            c.align_to(e, DOWN)

        v = VGroup(eng, chi).arrange(buff=2).next_to(t, DOWN, buff=.8)
        box = SurroundingRectangle(v, color=GREEN, stroke_width=8, buff=.3)
        self.add(eng, chi, box)
        self.wait(5)


class pic(Scene):
    def construct(self):
        plane = NumberPlane()
        # self.add(plane)
        a = VGroup(Tex("A\\sim").scale(1.2), Matrix([[1, ''], ['', 2]], h_buff=1),).arrange().scale(2)
        self.add(a)