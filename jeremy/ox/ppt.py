from manimlib import *

class MatFun(Scene):
    def construct(self):
        num = 16
        length = .2
        size = num*length
        LEFT_CENTER = LEFT*FRAME_X_RADIUS/2
        RIGHT_CENTER = RIGHT*FRAME_X_RADIUS/2
        square = Square(side_length=size).set_fill(opacity=.2, color=BLACK).set_stroke(color=BLACK, width=2).move_to(LEFT_CENTER)
        dot = Dot().set_color(RED)
        f = Tex("f(x,y)").set_color(BLACK)
        always(f.next_to, dot, DOWN)


        pts = [i/2 for i in range(-2,3)]
        row = VGroup(*[Square(length).set_stroke(width=1) for i in range(num)]).arrange(buff=0)
        mat = VGroup(*[row.copy() for i in range(num)]).arrange(DOWN, buff=0).set_color(BLACK).next_to(square, buff=1)
        
        ele = (10,7)
        mat[ele[0]][ele[1]].set_fill(opacity=1, color=RED)
        shift = mat[ele[0]][ele[1]].get_x()-mat.get_left()
        dot.set_x(square.get_left()[0]+shift[0])
        dot.set_y(mat[ele[0]][ele[1]].get_y())

        fi = Tex("f(x_i, y_i)").set_color(BLACK).next_to(mat[ele[0]][ele[1]], DOWN).add_background_rectangle(color=WHITE, opacity=1)


        self.add(square, dot, f, mat, fi)
        return super().construct()


class UniFun(Scene):
    def construct(self):
        num = 16
        length = .2
        size = num*length
        LEFT_CENTER = LEFT*FRAME_X_RADIUS/2
        RIGHT_CENTER = RIGHT*FRAME_X_RADIUS/2
        square = Square(side_length=size).set_fill(opacity=.2, color=BLACK).set_stroke(color=BLACK, width=2).move_to(LEFT_CENTER)
        dot = Line(UP, DOWN).set_height(size).set_color(RED)
        f = Tex("f(x_i,y)").set_color(BLACK)
        always(f.next_to, dot, DOWN)


        pts = [i/2 for i in range(-2,3)]
        row = VGroup(*[Square(length).set_stroke(width=1) for i in range(num)]).arrange(buff=0)
        mat = VGroup(*[row.copy() for i in range(num)]).arrange(DOWN, buff=0).set_color(BLACK).next_to(square, buff=1)
        
        ele = (10,7)
        for r in mat:
            r[ele[1]].set_fill(color=RED, opacity=1)
        shift = mat[ele[0]][ele[1]].get_x()-mat.get_left()
        dot.set_x(square.get_left()[0]+shift[0])
        # dot.set_y(mat[ele[0]][ele[1]].get_y())

        fi = Tex("f(x_i, y)").set_color(BLACK).set_x(mat[ele[0]][ele[1]].get_x()).align_to(f, DOWN)#.add_background_rectangle(color=WHITE, opacity=1)


        self.add(square, dot, f, mat, fi)
        return super().construct()


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
        A.add(Tex("\\times_1", color=BLACK).next_to(A))
        G = Cuboid(1, .33, label='X').next_to(A).align_to(A, DOWN).shift(UP).set_stroke(color=BLACK)
        B = Rectangle(width=2, height=1).next_to(G,aligned_edge=DOWN,buff=1).set_fill(color=WHITE, opacity=1).set_stroke(color=BLACK)
        B.add(Tex("\\times_2", color=BLACK).next_to(B, LEFT))

        C = Polygon(ORIGIN, RIGHT, RIGHT+UR*1, UR*1).next_to(G,UP, aligned_edge=LEFT, buff=.6).set_stroke(color=BLACK).shift(RIGHT*.33)
        C.add(Tex("\\times_3", color=BLACK).next_to(C, DOWN))
        tucker = VGroup(A,G,B,C)
        mob.add(
            tucker
        ).move_to(ORIGIN).scale(1.3)
        A[-1].align_to(G[-1], UP)
        B[-1].align_to(G[-1], UP)
        C[-1].align_to(G[-1], LEFT).shift(RIGHT*.4+UP*.1)
        
        self.add(A,G,B,C)