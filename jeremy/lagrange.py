from sympy import false
from manimlib import *

def l(points, num):
    n = len(points)
    coords = []
    for i in range(n):
        if i==num:
            coords.append((points[i],1))
        else:
            coords.append((points[i],0))
    return poly(coords, n-1)

xs = [-3,-2,0,1,3]
ys = [-1,1,-0.5,0,1.5]
coords = list(zip(xs,ys))
class Opening(Scene):
    def construct(self):
        plane = NumberPlane(x_range=[-4,4], y_range=[-2,2],height=FRAME_HEIGHT, width=FRAME_WIDTH)
        plane.add_coordinate_labels()
        self.add(plane)
        self.wait()

        dots = VGroup(*[Dot(color=RED).move_to(plane.c2p(*coord)) for coord in coords])
        graph = plane.get_graph(poly(coords), color=YELLOW)
        for d in dots:
            self.play(GrowFromCenter(d), Flash(d))
        self.wait()

        self.play(ShowCreation(graph), run_time=2)
        self.wait()
        return super().construct()

cm = {'a': RED, 'x': YELLOW, 'y': BLUE}
class Vandermonde(Scene):
    def construct(self):
        to_isolate = [f'a_{i}' for i in range(4)] + ['x', '+', ':']
        func = Tex("y","=","a_0","+","a_1","x","+","a_2","x^2","+","a_3","x^3","+","a_4","x^4",":").tm(cm).to_edge(UP)
        self.play(Write(func))
        self.wait()

        eq = VGroup()
        for x,y in coords:
            e = Tex(
                f"{y}","=","a_0","+","a_1",f"({x})","+","a_2",f"({x})^2","+","a_3",f"({x})^3","+","a_4",f"({x})^4"
            ).tm(cm)
            VGroup(e[-1],e[-4],e[-7],e[-10]).set_color(YELLOW)
            e[0].set_color(BLUE)
            eq.add(e)
        eq.arrange(DOWN)
        for i,e in enumerate(eq[1:]):
            for j in range(len(e)):
                e[j].align_to(eq[i][j], RIGHT)

        
        brace = Brace(eq, LEFT)
        self.play(Write(eq[0]))
        self.wait()
        self.play(
            *[RT(eq[0].copy(), eq[i]) for i in range(1,len(eq))]
            )
        self.wait()

        A = [
            ['1', '-3', '(-3)^2', '(-3)^3', '(-3)^4'],
            ['1', '-2', '(-2)^2', '(-2)^3', '(-2)^4'],
            ['1', '0', '0^2', '0^3', '0^4'],
            ['1', '1', '1^2', '1^3', '1^4'],
            ['1', '3', '3^2', '3^3', '3^4']
        ]
        A = Matrix(A, color=YELLOW)
        self.play(Transform(eq, A))
        self.wait()
        return super().construct()