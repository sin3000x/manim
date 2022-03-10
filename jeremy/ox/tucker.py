from manimlib import *

class Cuboid(VMobject):
    def __init__(self, length, bias=None, label='X', **kwargs):
        super().__init__(**kwargs)
        if bias is None:
            bias == length/2
        self.add(Polygon(ORIGIN, length*RIGHT, length*RIGHT+UR*bias, length*RIGHT+UR*bias+UP*length, UR*bias+UP*length, UP*length))
        self.add(
            Line(length*UR, UP*length),
            Line(length*UR, length*UR+bias*UR),
            Line(length*UR, RIGHT*length)
        )
        self.add(Tex(f"\\mathcal{{{label}}}").move_to(UR*length/2))
        self.set_color(BLACK)

class Tucker(Scene):
    def construct(self):
        mob = VGroup()
        X = Cuboid(2, .66).to_edge(LEFT).set_stroke(color=BLACK)
        eq = Tex("=").next_to(X).set_color(BLACK).scale(1.4)
        A = Rectangle(width=1, height=2)\
            .next_to(eq).align_to(X,DOWN).set_stroke(color=BLACK)
        A.add(Tex("A", color=BLACK).move_to(A))
        G = Cuboid(1, .33, label='G').next_to(A).align_to(A, DOWN).shift(UP).set_stroke(color=BLACK)
        B = Rectangle(width=2, height=1).next_to(G,aligned_edge=DOWN,buff=-.1).set_fill(color=WHITE, opacity=1).set_stroke(color=BLACK)
        B.add(Tex("B", color=BLACK).move_to(B))

        C = Polygon(ORIGIN, RIGHT, RIGHT+UR*1, UR*1).next_to(G,UP, aligned_edge=LEFT).set_stroke(color=BLACK).shift(RIGHT*.33)
        C.add(Tex("C", color=BLACK).move_to(C))
        tucker = VGroup(A,G,B,C)
        mob.add(
            X,eq,tucker
        ).arrange(buff=.3).move_to(ORIGIN).scale(1.3)
        
        self.add(X,eq,A,G,B,C)