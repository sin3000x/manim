from manimlib import *

class svd(Scene):
    def construct(self):
        mob = VGroup()
        w = 2
        h = w*1.5
        r = w*0.6
        A = Rectangle(width=w,height=h)
        A.label = Tex("A").scale(1.5).move_to(A)
        eq = Tex("\\approx").next_to(A)

        U = Rectangle(width=h,height=h).next_to(eq)
        U.shade = Rectangle(width=r, height=h).move_to(U, aligned_edge=LEFT)
        U.label = Tex("\\hat{U}").scale(1.5).move_to(U.shade)

        S = A.copy().next_to(U)
        S.shade = Rectangle(width=r,height=r).move_to(S,aligned_edge=UL)
        S.label = Tex("\\hat{\\Sigma}").scale(1.5).move_to(S.shade)

        V = Rectangle(width=w,height=w).next_to(S, aligned_edge=UP)
        V.shade = Rectangle(width=w, height=r).move_to(V, aligned_edge=UP)
        V.label = Tex("\\hat{V}").scale(1.5).move_to(V.shade)

        mob.add(A,eq,U,S,V, U.shade, V.shade, S.shade, A.label,).set_color(BLACK).move_to(ORIGIN)
        U.shade.set_fill(color=RED,opacity=.8)
        V.shade.set_fill(color=GREEN,opacity=.8)
        S.shade.set_fill(color=BLUE, opacity=.8)
        A.set_fill(color=BLUE, opacity=.8)
        self.add(mob)

        return super().construct()


class hosvd(Scene):
    def construct(self):
        w = 2
        h = w*1.5
        b = 0.5
        r1 = 1.6
        r2 = 1.2
        r3 = 0.3
        X = VGroup(
            Polygon(ORIGIN, RIGHT*w, RIGHT*w+UR*b,RIGHT*w+UR*b+UP*h, UR*b+UP*h, UP*h),
            Line(UP*h+RIGHT*w, UP*h),
            Line(UP*h+RIGHT*w, RIGHT*w),
            Line(UP*h+RIGHT*w, UP*h+RIGHT*w+UR*b),
        )
        X.shade = VGroup(
            Polygon(ORIGIN, RIGHT*w, RIGHT*w+UP*h, UP*h).set_stroke(width=0),
            Polygon(RIGHT*w,RIGHT*w+UR*b, RIGHT*w+UR*b+UP*h, UP*h+RIGHT*w).set_stroke(width=0),
            Polygon(UP*h, UP*h+RIGHT*w, UP*h+RIGHT*w+UR*b, UP*h+UR*b).set_stroke(width=0)
        )
        X.label = Tex("\\mathcal{X}").scale(1.5).move_to(RIGHT*w/2+UP*h/2)
        eq = Tex("\\approx").next_to(X).shift(UP*.3)
        A = Rectangle(width=h, height=h).next_to(eq).align_to(X, DOWN)
        A.shade = Rectangle(width=r1, height=h).move_to(A, aligned_edge=LEFT)
        A.label = Tex("k_1").scale(.8).next_to(A.shade, UP,buff=.1)

        G = VGroup(
            Polygon(ORIGIN, RIGHT*w, RIGHT*w+UR*b,RIGHT*w+UR*b+UP*h, UR*b+UP*h, UP*h),
            Line(UP*h+RIGHT*w, UP*h),
            Line(UP*h+RIGHT*w, RIGHT*w),
            Line(UP*h+RIGHT*w, UP*h+RIGHT*w+UR*b),
        ).next_to(A, aligned_edge=DOWN)
        G.inner = VGroup(
            Polygon(UP*h, UP*(h-r1), UP*(h-r1)+RIGHT*r2, UP*(h-r1)+RIGHT*r2+UR*r3, UP*h+r2*RIGHT+UR*r3, UP*h+UR*r3),
            Line(UP*h+r2*RIGHT, UP*h+r2*RIGHT+UR*r3),
            Line(UP*h+r2*RIGHT, UP*h+r2*RIGHT+DOWN*r1),
        ).shift((G.get_x()-X.get_x())*RIGHT)
        G.shade = VGroup(
            Polygon(UP*h, UP*(h-r1), UP*(h-r1)+RIGHT*r2, UP*h+RIGHT*r2).set_stroke(width=0),
            Polygon(UP*h, UP*h+UR*r3, UP*h+UR*r3+RIGHT*r2, UP*h+RIGHT*r2).set_stroke(width=0),
            Polygon(UP*h+RIGHT*r2, UP*h+RIGHT*r2+UR*r3, UP*h+RIGHT*r2+UR*r3+DOWN*r1, UP*h+RIGHT*r2+DOWN*r1).set_stroke(width=0)
        ).shift((G.get_x()-X.get_x())*RIGHT)
        G.label = VGroup(
            Tex("k_1").scale(.8).next_to(G.shade[0].get_left(), buff=.1),
            Tex("k_2").scale(.8).next_to(G.shade[0], DOWN, buff=.1),
            Tex("k_3").scale(.8).next_to(G.shade[2], DR, buff=-0.1)
        )

        B = Square(w).next_to(G, buff=-.2, aligned_edge=UP).shift(DOWN*b)
        B.shade = Rectangle(width=w, height=r2).move_to(B).align_to(B, UP)
        B.label = Tex("k_2").scale(.8).next_to(B.shade,buff=.1)

        C = Polygon(ORIGIN, RIGHT*b*2.5, RIGHT*b*2.5+UR*b*1.2, UR*b*1.2).next_to(G, UP, aligned_edge=UP).shift(UR*.2)
        C.shade = Polygon(ORIGIN, RIGHT*b*1, RIGHT*b*1+UR*b*1.2, UR*b*1.2).move_to(C).align_to(C, LEFT)
        C.label = Tex("k_3").scale(.8).next_to(C.shade, UP, aligned_edge=RIGHT, buff=.1).shift(LEFT*.1)

        mob = VGroup(X, X.shade, X.label, eq, A, A.shade, G.inner, G.shade,G.label, A.label,  G, C, B.shade,B.label, C.shade, C.label, B).move_to(ORIGIN).set_color(BLACK)
        for i in X.shade:
            i.set_fill(color=BLUE, opacity=.8)
        for i in G.shade:
            i.set_fill(color=BLUE, opacity=.8)
        A.shade.set_fill(color=RED, opacity=.8)
        B.shade.set_fill(color=GREEN, opacity=.8)
        C.shade.set_fill(color=YELLOW, opacity=.8)
        B.set_fill(color=WHITE, opacity=1)
        self.add(mob[:-1],B,B.shade)
        return super().construct()