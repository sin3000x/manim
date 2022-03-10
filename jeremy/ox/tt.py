from manimlib import *

class TT(Scene):
    def construct(self):
        w = 3
        h = w
        b = w/4
        u = w/3
        ub = u/4
        X = VGroup(
            Polygon(ORIGIN, RIGHT*w, RIGHT*w+UR*b,RIGHT*w+UR*b+UP*h, UR*b+UP*h, UP*h),
            Line(UP*h+RIGHT*w, UP*h),
            Line(UP*h+RIGHT*w, RIGHT*w),
            Line(UP*h+RIGHT*w, UP*h+RIGHT*w+UR*b),
        )
        X.shade = VGroup(
            Polygon(UR*w, UR*w+UR*ub, UR*w+UR*ub+LEFT*u, UR*w+LEFT*u).set_stroke(width=0),
            Polygon(UR*w, UR*w+LEFT*u, UR*w+DL*u, UR*w+DOWN*u).set_stroke(width=0),
            Polygon(UR*w, UR*w+UR*ub, UR*w+UR*ub+DOWN*u, UR*w+DOWN*u).set_stroke(width=0),
            Line(UR*w+UR*ub+LEFT*u,UR*w+UR*ub),
            Line(UR*w+UR*ub+LEFT*u,UR*w+LEFT*u),
            Line(UR*w+DL*u, UR*w+DOWN*u),
            Line(UR*w+DL*u, UR*w+LEFT*u),
            Line(UR*w+UR*ub+DOWN*u,UR*w+UR*ub),
            Line(UR*w+UR*ub+DOWN*u,UR*w+DOWN*u),
        )
        X.label = Tex("\\mathcal{X}").scale(1.5).move_to(RIGHT*w/2+UP*h/2)

        # x = VGroup(
        #     Polygon(ORIGIN, RIGHT*u, RIGHT*u+UR*ub,RIGHT*u+UR*ub+UP*u, UR*ub+UP*u, UP*u),
        #     Line(UP*u+RIGHT*u, UP*u),
        #     Line(UP*u+RIGHT*u, RIGHT*u),
        #     Line(UP*u+RIGHT*u, UP*u+RIGHT*u+UR*ub),
        # ).next_to(X, buff=.5)
        
        # x.shade = VGroup(
        #     Polygon(ORIGIN, RIGHT*u, UR*u, UP*u).set_stroke(width=0),
        #     Polygon(RIGHT*u, RIGHT*u+UR*ub, RIGHT*u+UR*ub+UP*u, UR*u).set_stroke(width=0),
        #     Polygon(UP*u, UR*u, UR*u+ub*UR, UP*u+UR*ub).set_stroke(width=0)
        # ).move_to(x)
        
        u = u*.9
        r0 = r3 = u
        r1 = r2 = 3*r0
        x = Square(u).next_to(X, buff=1)
        eq = Tex("=").next_to(x)
        x.label = Tex("x_{ijk}").scale(.8).move_to(x)

        f = .7
        G1 = Rectangle(height=r0, width=r1).next_to(eq)
        G1.label = Tex("G_1(i)").scale(f).move_to(G1)
        G2 = Rectangle(height=r1, width=r2).next_to(G1)
        G2.label = Tex("G_2(j)").scale(f).move_to(G2)
        G3 = Rectangle(height=r2, width=r3).next_to(G2)
        G3.label = Tex("G_3(k)").scale(f).move_to(G3)

        arrow = Arrow(X.shade.get_right(), x.get_left())

        mob = VGroup(X, X.shade, X.label,x,eq, G1, G1.label, G2, G2.label, G3, G3.label, x.label, arrow).move_to(ORIGIN).set_color(BLACK)
        for i in X.shade[:3]:
            i.set_fill(color=BLUE, opacity=.8)
        x.set_fill(color=BLUE, opacity=.8)
        self.add(mob)
        return super().construct()