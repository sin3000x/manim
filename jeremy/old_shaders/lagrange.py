from sympy import false, isolate
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
        self.play(GrowFromCenter(brace))
        self.wait()

        A = [
            ['1', '-3', '(-3)^2', '(-3)^3', '(-3)^4'],
            ['1', '-2', '(-2)^2', '(-2)^3', '(-2)^4'],
            ['1', '0', '0^2', '0^3', '0^4'],
            ['1', '1', '1^2', '1^3', '1^4'],
            ['1', '3', '3^2', '3^3', '3^4']
        ]
        A = Matrix(A,element_alignment_corner=ORIGIN, h_buff=1.5).set_color(YELLOW)
        a = np.array([f'a_{i}' for i in range(5)])
        a.shape = (-1,1)
        y = np.array([-1,1,-0.5,0,1.5])
        y.shape = (-1,1)
        va = Matrix(a).set_color(RED)
        vy = TMatrix(y).set_color(BLUE)
        system = VGroup(vy, Tex("="),A,va).arrange()
        self.play(FadeTransform(eq, system), FadeOut(brace))
        self.wait()

        vander = VGroup(TexText("Vandermonde matrix"), TexText("范德蒙(德)矩阵")).set_color(YELLOW).arrange(DOWN).next_to(A, DOWN, buff=.5)
        self.play(Write(vander))
        self.wait()
        return super().construct()


class Polynomial(Scene):
    def construct(self):
        p1 = Tex("\\frac12",r"\cdot","1","-","5",r"\cdot"," x","+","\\frac92",r"\cdot",r" x^2","+","10",r"\cdot",r" x^3").tm(cm)
        p2 = Tex("2",r"\cdot","1","+","1",r"\cdot ","x","+","3",r"\cdot","\\left(\\frac32 x^2-\\frac12\\right)","+","4",r"\cdot ","\\left(\\frac52 x^3-\\frac32 x\\right)").tm(cm)
        VGroup(p1[2], p2[2]).set_color(YELLOW)
        VGroup(
            p1[0],p1[4], p1[8], p1[12],
            p2[0], p2[4], p2[8], p2[12]
        ).set_color(RED)
        VGroup(p2,p1).arrange(DOWN, buff=1, aligned_edge=LEFT)
        # for i in range(len(p2)):
        #     p1[i].align_to(p2[i], LEFT)
        p1.save_state()
        p2.save_state()
        p1.set_color(WHITE)
        p2.set_color(WHITE)
        self.play(Write(p2))
        self.wait()
        self.play(RT(p2.copy(), p1))
        self.wait()

        space = VGroup(Tex(r"\mathcal{P}_3=\{p:\deg p\leq 3\}"), TexText("是 4 维空间")).arrange().to_edge(UP, buff=.5).set_color(BLUE)
        self.play(Write(space[0]))
        self.wait()
        self.play(Write(space[1]))
        self.wait()
        self.play(Restore(p1))
        self.wait()

        monomial = VGroup(
            TexText("monomial basis"),
            TexText("单项式基")
        ).arrange(DOWN).set_color(YELLOW).next_to(p1, DOWN, buff=.5)
        lines = VGroup(
            *[Line(p1[i].get_bottom()+DOWN*.3, monomial.get_top()+UP*.1, color=YELLOW, buff=0) for i in [2,6,10,14]]
        )
        self.play(*[ShowCreation(line) for line in lines])
        self.play(Write(monomial))
        self.wait()
        self.play(Restore(p2))
        self.wait()
        return super().construct()


# class Monomial(Scene):
#     def construct(self):
#         plane = NumberPlane()
#         self.add(plane)
#         n = [10,20,30,40,50]
#         graphs = [
#             plane.get_graph(lambda x: x**n, use_smoothing=False).set_color(YELLOW) for n in n
#         ]
#         self.play(ShowCreation(graphs[0]))
#         for i in range(1, len(graphs)):
#             self.play(RT(graphs[i-1], graphs[i]))
#         return super().construct()

class LagrangeBasis(Scene):
    def construct(self):
        a = [-0.5000,-0.1833,0.6833,0.0667,-0.0667]
        plane = NumberPlane(x_range=[-4,4], y_range=[-2,2],height=FRAME_HEIGHT, width=FRAME_WIDTH)
        plane.add_coordinate_labels()

        dots = VGroup(*[Dot(color=RED).move_to(plane.c2p(*coord)) for coord in coords])
        graph = plane.get_graph(poly(coords), color=YELLOW)
        self.add(plane,dots)
        self.wait()

        monomials = VGroup(*[plane.get_graph(lambda x: x**n) for n in range(5)])
        monomials2 = VGroup(*[plane.get_graph(lambda x: an*x**n) for an,n in zip(a,range(5))])
        for i, m in enumerate(monomials):
            VGroup(m, monomials2[i]).set_color(interpolate_color(RED, YELLOW, (i) / 5))
            m.fade(0)
            self.play(ShowCreation(m))   
            self.wait()     
        self.wait()

        for i in range(len(monomials)):
            self.play(RT(monomials[i], monomials2[i]))

        self.play(*[RT(monomials2[i], graph) for i in range(5)], run_time=2)
        self.wait()

        self.play(FadeOut(VGroup(monomials2, graph)))
        #### lagrange
        # self.play(dots.fade, .6)
        dots = VGroup(
            *[VGroup(*[Cross(Dot(plane.c2p(x,0)),stroke_width=[6,6,6]).scale(1.5) for x in xs]) for i in range(5)]
        ).set_color(YELLOW)
        dots2 = dots.copy()
        cross_final = VGroup()
        for i in range(len(dots)):
            dots[i][i].shift(UP*plane.get_y_axis().get_unit_size())
            dots2[i][i].shift(UP*plane.get_y_axis().get_unit_size()*ys[i])
            cross_final.add(dots2[i][i])
        lagranges = VGroup(*[plane.get_graph(l(xs, n)) for n in range(5)])
        lagranges2 = VGroup(*[plane.get_graph(an*l(xs, n)) for an,n in zip(ys,range(5))])
        for i, m in enumerate(lagranges):
            VGroup(m, lagranges2[i]).set_color(interpolate_color(RED, YELLOW, (i) / 5))
            m.save_state()
            dots[i].save_state()
            self.play(ShowCreation(m))   
            self.wait()
            for d in dots[i]:
                self.play(FadeIn(d), Flash(d))
            self.wait()
            self.play(m.fade, 1, dots[i].fade,1)
        self.wait()
        tips = VGroup(
            TexText("1. 个数与点相同.", color=YELLOW),
            TexText("2. 次数$\leq4$.", color=YELLOW),
            TexText("3. 被点的横坐标确定.", color=YELLOW)
        ).arrange(DOWN, aligned_edge=LEFT).to_edge(UP).add_background_rectangle()
        for t in tips:
            self.play(Write(t))
            self.wait()
        self.play(FadeOut(tips))

        for i in range(len(lagranges)):
            self.play(Restore(lagranges[i]), Restore(dots[i]))
            self.wait()
            self.play(
                RT(lagranges[i], lagranges2[i]),
                RT(dots[i], dots2[i])
                )
            to_fade = list(range(5))
            to_fade.pop(i)
            self.play(
                VGroup(*[dots2[i][j] for j in to_fade]).fade, 1,
                lagranges2[i].fade, .8,
                dots2[i][i].fade, .7
                )
            self.wait()
        tmp = AnimationGroup(
            *[RT(lagranges2[i], graph) for i in range(5)], run_time=2
            # RT(dots2[-1], cross_final)
            )
        print(tmp)
        self.play(tmp)
        self.wait()
        return super().construct()


class Lagrange(Scene):
    def construct(self):
        cm = {'x': RED, 'y': BLUE, 'p': WHITE}
        to_isolate=['x_0', 'x_1', 'x_n', 'y_0', 'y_1', 'y_n', 'p_n', 'l_0', 'l_1', 'l_n', '=']
        assume = Tex("p_n(x_0)=y_0,~p_n(x_1)=y_1,~\\ldots,~p_n(x_n)=y_n",
        isolate=to_isolate).tm(cm).to_edge(UP, buff=1.5)
        box = SurroundingRectangle(assume, buff=.2)
        self.play(Write(assume))
        self.play(ShowCreation(box))
        self.wait()

        lagrange_basis = Tex("p_n(x)","=",r"y_0",r"l_0(x)","+","y_1","l_1(x)","+\\cdots+","y_n","l_n(x)").tm({'l': WHITE, 'y': BLUE, 'p': WHITE}).scale(1.3).next_to(assume, DOWN, buff=2)
        basis0=  Tex("p_n(","x_0",")","=",r"y_0",r"l_0(","x_0",")","+","y_1","l_1(","x_0",")","+\\cdots+","y_n","l_n(","x_0",")").tm({')': WHITE,'x_0': RED,'l': WHITE, 'y': BLUE, 'p': WHITE}).scale(1.2).move_to(lagrange_basis)
        basis1=  Tex("p_n(","x_1",")","=",r"y_0",r"l_0(","x_1",")","+","y_1","l_1(","x_1",")","+\\cdots+","y_n","l_n(","x_1",")").tm({')':WHITE,'x_1': RED,'l': WHITE, 'y': BLUE, 'p': WHITE}).scale(1.2).move_to(lagrange_basis)
        basisn=  Tex("p_n(","x_n",")","=",r"y_0",r"l_0(","x_n",")","+","y_1","l_1(","x_n",")","+\\cdots+","y_n","l_n(","x_n",")").tm({')': WHITE,'x_n': RED,'l': WHITE, 'y': BLUE, 'p': WHITE}).scale(1.2).move_to(lagrange_basis)
        basis0[8:].fade(.7)
        VGroup(basis1[4:9], basis1[13:]).fade(.7)
        VGroup(basisn[4:14]).fade(.7)
        self.play(Write(lagrange_basis))
        self.wait()
        brace0, brace1, bracen = [Brace(lagrange_basis[i], DOWN) for i in [3,6,9]]
        brace0.add(VGroup(Tex("l_0(","x_0",")=1").tm({'x': RED}), Tex("l_0(x_i)=0")).arrange(DOWN).next_to(brace0, DOWN))
        brace1.add(VGroup(Tex("l_1(","x_1",")=1").tm({'x': RED}), Tex("l_1(x_i)=0")).arrange(DOWN).next_to(brace1, DOWN))
        bracen.add(VGroup(Tex("l_n(","x_n",")=1").tm({'x': RED}), Tex("l_n(x_i)=0")).arrange(DOWN).next_to(bracen, DOWN))
        self.play(GrowFromCenter(brace0))
        self.wait()
        self.play(GrowFromCenter(brace1))
        self.play(GrowFromCenter(bracen))
        self.wait()
        self.play(FadeOut(VGroup(brace0, brace1, bracen)))
        self.wait()

        self.play(FadeTransform(lagrange_basis, basis0))
        self.wait()
        self.play(FadeTransform(basis0, basis1))
        self.wait()
        self.play(FadeTransform(basis1, basisn))
        self.wait()
        
        return super().construct()

class FindBasis(Scene):
    def construct(self):
        plane = NumberPlane(x_range=[-4,4], y_range=[-2,2],height=FRAME_HEIGHT, width=FRAME_WIDTH)
        plane.add_coordinate_labels()

        coords = [(-3,0),(-2,1),(-1,0),(1,0),(2,0)]
        dots = VGroup(*[Dot(color=RED).move_to(plane.c2p(*coord)) for coord in coords])
        labels = VGroup(*[Tex(s, color=RED) for s in [f"x_{i}" for i in range(len(coords))]])
        for l, d in zip(labels, dots):
            l.next_to(d, DOWN)
        graph = plane.get_graph(poly(coords), color=YELLOW)
        self.add(plane)
        for d,l in zip(dots, labels):
            self.add(d)
            self.play(Flash(d), Write(l))
        self.wait()

        self.play(ShowCreation(graph))
        self.wait()

        func = Tex("l_1(x)=c(x-x_0)(x-x_2)(x-x_3)(x-x_4)", isolate=['x_0','x_2','x_3','x_4', '=', 'x']).tm({'x': YELLOW, 'x_': RED}).to_edge(UP).add_background_rectangle()
        one = Tex("l_1(","x_1",")=1:").tm({'x': RED}).add_background_rectangle()
        c = Tex("c={1\\over(x_1-x_0)(x_1-x_2)(x_1-x_3)(x_1-x_4)}", isolate=[f"x_{i}" for i in range(5)]).tm({'x': RED}).add_background_rectangle()
        VGroup(one, c).arrange(buff=.5).next_to(func, DOWN)
        self.play(Write(func[:5]))
        self.wait()
        self.play(Write(func[5:]))
        self.wait()
        self.play(Write(one))
        self.wait()
        self.play(FadeOut(VGroup(plane, dots, labels, graph)))
        self.play(Write(c))
        self.wait()

        l1 = Tex("\\Longrightarrow~l_1(x)={(x-x_0)(x-x_2)(x-x_3)(x-x_4)\\over (x_1-x_0)(x_1-x_2)(x_1-x_3)(x_1-x_4)}", isolate=[f"x_{i}" for i in range(5)]+['x']).tm({'x': YELLOW, 'x_': RED})
        self.play(Write(l1))
        self.wait()

        lj = Tex(r"l_j(x)=\prod_{k=0,k\ne j}^n {x-x_k\over x_j-x_k}", isolate=['x_k', 'x_j', 'x']).tm({'x': YELLOW, 'x_': RED}).next_to(l1, DOWN, buff=1)
        box = SurroundingRectangle(lj, buff=.3)
        self.play(Write(lj))
        self.play(ShowCreation(box))
        self.wait()


class Cor(Scene):
    def construct(self):
        thm = TexText("过 $n+1$ 个(横坐标互异)点确定了唯一的$p_n$.", color=YELLOW).to_edge(UP, buff=.5).add_to_front().add_background_rectangle()
        self.play(Write(thm))
        self.wait()

        plane = NumberPlane(x_range=[-4,4], y_range=[-2,2],height=FRAME_HEIGHT, width=FRAME_WIDTH)
        plane.add_coordinate_labels()

        coords = [(-3,1),(-2,1),(-1,1),(1,1),(2,1)]
        dots = VGroup(*[Dot(color=RED).move_to(plane.c2p(*coord)) for coord in coords])
        labels = VGroup(*[Tex(s, color=RED) for s in [f"x_{i}" for i in range(len(coords))]])
        for l, d in zip(labels, dots):
            l.next_to(d, DOWN)
        graph = plane.get_graph(poly(coords), color=RED)
        self.play(FadeIn(plane))
        thm.add_background_rectangle()
        for d,l in zip(dots, labels):
            self.add(d)
            self.play(Flash(d), Write(l))
        self.wait()
        interp = Tex(r"l_0(x)+l_1(x)+\cdots+l_4(x)", "=", "1", color=YELLOW).scale(1.5).shift(DOWN).add_background_rectangle()
        self.play(Write(interp[:2]))
        self.wait()
        self.play(Write(interp[-1]), ShowCreation(graph))
        self.wait()
        self.play(Write(interp[-2]))
        self.wait()

        # zero = Tex(r"l_0(x)+l_1(x)+\cdots+l_4(x)-1\text{ 在5个点取0.}").next_to(interp, DOWN).add_background_rectangle()
        # self.play(Write(zero))
        return super().construct()

class Computing(Scene):
    def construct(self):
        to_isolate=['x_0', 'x_1', 'x_j', 'x_k', 'x_n', 'x', 'y_j']
        cm = {'x': YELLOW,'x_': RED, 'y': BLUE}
        p = Tex(r"p(x)=\sum_{j=0}^n y_j l_j(x)", isolate=to_isolate).tm(cm)
        lj = Tex(r"l_j(x)={\prod_{k=0,k\ne j}^n(x-x_k)\over\prod_{k=0,k\ne j}^n(x_j-x_k)}",isolate=to_isolate).tm(cm)
        
        VGroup(p, lj).arrange(buff=1).to_edge(UP, buff=.5)
        lj2 = Tex(r"=w_j\cdot{l(x)\over x-x_j}", isolate=to_isolate).tm(cm).next_to(lj[2][1], DOWN, aligned_edge=LEFT, buff=1)
        self.play(Write(p))
        self.play(Write(lj))
        numerator = VGroup(lj[2][2:], lj[3:6], lj[6][0])
        box = SurroundingRectangle(numerator, buff=.1, color=GREEN)
        self.wait()

        short = VGroup(
            TexText("1. $O(n^2)$次加法和乘法."),
            TexText("2. 加入新点要重新计算.")
        ).arrange(DOWN, aligned_edge=LEFT, buff=.5)
        for s in short:
            self.play(Write(s))
            self.wait()
        self.play(FadeOut(short))
        
        ell = Tex("l(x)=(x-x_0)(x-x_1)\\cdots (x-x_n)", isolate=to_isolate).tm(cm).shift(DOWN)
        wj = Tex(r"w_j={1\over\prod_{k=0,k\ne j}^n(x_j-x_k)}", isolate=to_isolate).tm(cm).move_to(ell)
        self.play(Write(ell))
        self.wait()
        self.play(ShowCreation(box))
        self.wait()
        self.play(Write(lj2[0][0]))   ## =
        self.play(Write(lj2[0][4:]), Write(lj2[1:]))  ## numerator
        self.wait()
        self.play(Write(lj2[0][1:4]))  ## wj
        self.wait()
        self.play(RT(ell, wj))
        self.wait()
        self.play(FadeOut(wj))

        p2 = Tex(r"=l(x)\sum_{j=0}^n{w_j\over x-x_j}y_j", isolate=to_isolate).tm(cm).next_to(p[2][1], DOWN, aligned_edge=LEFT, buff=1)
        self.play(Write(p2))
        self.play(lj2.fade, .7)
        self.wait()
        p3 = Tex(r"={l(x)\sum_{j=0}^n{w_j\over x-x_j}y_j\over\sum_{j=0}^n l_j(x)}", isolate=to_isolate).tm(cm).next_to(p2, DOWN, aligned_edge=LEFT, buff=.5)
        p32 = Tex(r"={l(x)\sum_{j=0}^n{w_j\over x-x_j}y_j\over\sum_{j=0}^n w_j\cdot{l(x)\over x-x_j}}", isolate=to_isolate).tm(cm).next_to(p2, DOWN, aligned_edge=LEFT, buff=.5).move_to(p3).align_to(p3, LEFT)
        p33 = Tex(r"={\sum_{j=0}^n{w_j\over x-x_j}y_j\over\sum_{j=0}^n {w_j\over x-x_j}}", isolate=to_isolate).tm(cm).next_to(p32, DOWN, aligned_edge=LEFT, buff=.5)
        self.play(Write(p3))
        self.wait()
        self.play(FadeTransform(p3, p32,))
        self.wait()
        self.play(Write(p33))
        self.wait()

        self.play(FadeOut(VGroup(p32, p2, p[2][1:], p[3:],lj, lj2, box)))
        peq = VGroup(p[:2], p[2][0])
        peq.generate_target()
        p33.generate_target()
        # print(peq.target)
        # print(p33.target)
        VGroup(peq.target, p33.target).arrange().to_edge(UP, buff=.5)
        self.play(MoveToTarget(peq), MoveToTarget(p33))
        self.wait()

        label = VGroup(TexText("Barycentric formula"), TexText("质心公式")).set_color(YELLOW).arrange(DOWN).next_to(peq.target, DOWN, buff=1).set_x(0)
        self.play(Write(label))
        self.wait()

        points = Tex("(","-1",",","1",")~(","0",
        ",","2",")~(","\\frac12",",",
        "3",")~(","1",",","4",
        "):").next_to(label, DOWN).to_edge(LEFT)
        VGroup(*[points[i] for i in [1,5,9,13]]).set_color(RED)
        VGroup(*[points[i] for i in [3,7,11,15]]).set_color(BLUE)
        self.play(Write(points))
        self.wait()

        p = Tex(r"p(x)={{-\frac13\over x+1}\cdot1+{2\over x-0}\cdot2+{-\frac83\over x-\frac12}\cdot3+{1\over x-1}\cdot 4\over{-\frac13\over{x+1}}+{2\over x-0}+{-\frac83\over x-\frac12}+{1\over x-1}}").next_to(points, DOWN).set_x(0)
        # self.add(Debug(p[0]))
        VGroup(*[p[0][i] for i in [2,10,18,29,39,50,56,65,73]]).set_color(YELLOW)
        VGroup(*[p[0][i] for i in [14,22,35,43]]).set_color(BLUE)
        VGroup(*[p[0][i] for i in [11,12,19,20,30,31,32,33,40,41,51,52,57,58,66,67,68,69,74,75]]).set_color(RED)
        self.play(Write(p))
        self.wait()
        return super().construct()


class Error(Scene):
    def construct(self):
        to_isolate=['x_0', 'x_n', 'f', 'x', 't', 'p_n']
        cm = {'x': WHITE,'x_': WHITE, 'f': BLUE, 'xi': GREEN, 't': YELLOW, 'ldots': WHITE, 'p': RED, 'phi': YELLOW}
        interp = Tex(r"p_n",r"(",r"x_0",r")=",r"f","(",r"x_0",r"),\ \ldots,\ ",r"p_n",r"(","x_n",r")=",r"f",r"(",r"x_n",r")").tm(cm).to_edge(UP, buff=.5)
        self.play(Write(interp))
        self.wait()

        error = Tex(r"f",r"(",r"x",r")",r"-",r"p_n",r"(",r"x",r")",r"=",r"{f^{(n+1)}",r"(",r"\xi",r")\over (n+1)!}",r"l",r"(",r"x",r")").tm(cm).next_to(interp, DOWN, buff=.5)
        box = SurroundingRectangle(error, buff=.1)
        # self.add(Debug(error))
        self.play(Write(error[:10]))
        self.wait()
        self.play(Write(error[10:]))
        self.play(ShowCreation(box))
        self.wait()
        condition = Tex(r"f",r"\in C^{n+1}([a,b])").tm(cm)#.next_to(error, DOWN)
        self.play(Write(condition))
        self.wait()

        phi = Tex(r"\phi(t)",r"=",r"f",r"(",r"t",r")",r"-",r"p_n",r"(",r"t",r")",r"-{",r"f",r"(",r"x",r")-",r"p_n",r"(",r"x",r")\over ",r"l",r"(",r"x",r")}",r"l",r"(",r"t",r")").tm(cm).next_to(box, DOWN, buff=.5)
        phix = Tex(r"\phi(x)",r"=",r"f",r"(",r"x",r")",r"-",r"p_n",r"(",r"x",r")",r"-{",r"f",r"(",r"x",r")-",r"p_n",r"(",r"x",r")\over ",r"l",r"(",r"x",r")}",r"l",r"(",r"x",r")=0").tm(cm).next_to(phi, DOWN)

        self.play(FadeOut(condition))
        self.play(Write(phi))
        self.wait()

        # self.add(Debug(phi))
        brace1 = Brace(phi[2:11], DOWN)
        brace1.add(Tex("0").next_to(brace1, DOWN)).set_color(YELLOW)
        brace2 = Brace(phi[24:], DOWN)
        brace2.add(Tex("0").next_to(brace2, DOWN)).set_color(YELLOW)
        # nodes = Tex("\\text{当 }x=x_0,\\ldots,x_n", color=WHITE).next_to(phi, DOWN, buff=1.5)
        # self.play(Write(nodes))
        self.play(GrowFromCenter(brace1))
        self.play(GrowFromCenter(brace2))
        self.wait()
        self.play(FadeOut(brace1), FadeOut(brace2))
        self.play(Write(phix))
        self.wait()
        zeros = TexText("有 $x_0,x_1,\\ldots,x_n,x$ 共 $n+2$ 个零点:").move_to(phix)
        self.play(FadeTransform(phix, zeros))
        self.wait()

        rolle = Tex(r"\phi^{(n+1)}",r"(",r"\xi",r")",r"=",r"f^{(n+1)}",r"(",r"\xi",r")",r"-{",r"f",r"(",r"x",r")-",r"p_n",r"(",r"x",r")\over ",r"l",r"(",r"x",r")}",r"(n+1)!=0").tm(cm).next_to(zeros, DOWN, buff=.5)
        self.play(Write(rolle))
        self.wait()
        self.play(FadeOut(VGroup(rolle, zeros, phi)))
        self.wait()
        comment = TexText(r"让",r" $|l(x)|=|(x-x_0)\cdots(x-x_n)|$",r" 足够小.").next_to(box, DOWN, buff=.5)
        comment[1].set_color(YELLOW)
        self.play(Write(comment))
        self.wait()

        ax1 = Axes(x_range=[-1.5,1.5],y_range=[-0.005,0.005],height=3,width=4, axis_config={"include_ticks": False})
        ax2 = ax1.deepcopy()
        VGroup(ax1, ax2).arrange(buff=1).to_edge(DOWN, buff=.5)
        num = 12
        rad = 0.05
        equi = np.linspace(-1,1,num)
        cheb = np.cos(np.linspace(0,PI, num))
        pts_equi = VGroup(*[Dot(ax2.c2p(j,0), radius=rad).set_color(YELLOW) for j in equi])
        pts_cheb = VGroup(*[Dot(ax1.c2p(i,0), radius=rad).set_color(YELLOW) for i in cheb])
        graph_equi = ax2.get_graph(lambda x: math.prod(x-equi), x_range=[-1,1], use_smoothing=False, epsilon=1e-12)
        graph_cheb = ax1.get_graph(lambda x: math.prod(x-cheb), x_range=[-1,1], use_smoothing=True, epsilon=1e-12)
        cheb_label = TexText("Chebyshev", color=YELLOW).next_to(graph_cheb, UP,  buff=.5)
        equi_label = TexText("Equispace", color=YELLOW).next_to(graph_equi, UP).align_to(cheb_label, DOWN)

        self.play(ShowCreation(ax1), ShowCreation(ax2))
        self.play(FadeIn(pts_cheb), FadeIn(pts_equi))
        self.play(ShowCreation(graph_cheb))
        self.wait()
        self.play(FadeIn(cheb_label), FadeIn(equi_label))
        self.play(ShowCreation(graph_equi))
        self.wait()
        # self.add(ax1,ax2,pts_cheb, pts_equi, graph_cheb, graph_equi)
        return super().construct()


class Hermite(Scene):
    def construct(self):
        to_isolate=['x_0', 'x_1', 'x_j', 'x_k', 'x_n', 'x', 'y_j']
        cm = {'x': YELLOW,'x_': RED, 'y': BLUE, 't': BLUE, 'right': WHITE, 'left': WHITE, 'dot': WHITE, 'int': WHITE}
        p = Tex(r"p(x)",r"=",r"\sum_{j=0}^n f(x_j) l_j(x)", isolate=to_isolate).tm(cm)
        lj = Tex(r"l_j(x)={\prod_{k=0,k\ne j}^n(x-x_k)\over\prod_{k=0,k\ne j}^n(x_j-x_k)}",isolate=to_isolate).tm(cm)
        
        VGroup(p, lj).arrange(buff=2).to_edge(UP, buff=.5)
        lj2 = Tex(r"=w_j\cdot{l(x)\over x-x_j}", isolate=to_isolate).tm(cm).next_to(lj[2][1], DOWN, aligned_edge=LEFT, buff=1)
        lj3 = Tex(r"={l(x)\over l'(x_j)(x-x_j)}", isolate=to_isolate).tm(cm).move_to(lj2).align_to(lj2, LEFT)
        pre = Tex(r"=",r"l",r"(",r"x",r")",r"\cdot",r" {1\over l'(x_j)(x-x_j)}", isolate=to_isolate).tm(cm).next_to(lj3, DOWN, aligned_edge=LEFT)
        residue = Tex(r"=",r"l",r"(",r"x",r")",r"\cdot",r"\mathrm{Res}\left({1\over l(",r"t",r")(x-",r"t",r")}",r";","t",r"=x_j\right)", isolate=to_isolate).tm(cm).next_to(pre, DOWN, aligned_edge=LEFT).shift(LEFT*1.8)

        int_j = Tex(r"={1\over 2\pi\i}\int_{\Gamma_j}{l(",r"x",r")\over l(",r"t",")(",r"x",r"-",r"t",r")}",r"\d ",r"t").tm(cm).next_to(residue, DOWN).align_to(pre, LEFT)

        gamma_j = TexText("$\\Gamma_j$ 只包围 $x_j$.", color=BLUE).next_to(int_j, LEFT, buff=1)

        note = Tex(r"\mathrm{Res}\left({1\over g(x)};x_0\right)={1\over g'(x_0)}", color=BLUE).scale(.8).next_to(residue, LEFT, buff=1)
        box = SurroundingRectangle(note, color=BLUE)

        # numerator = VGroup(lj[2][2:], lj[3:6], lj[6][0])
        # box = SurroundingRectangle(numerator, buff=.1, color=GREEN)
        
        ell = Tex("l(x)=(x-x_0)(x-x_1)\\cdots (x-x_n)", isolate=to_isolate).tm(cm).shift(DOWN)
        wj = Tex(r"w_j={1\over\prod_{k=0,k\ne j}^n(x_j-x_k)}",r"=",r"{1\over l'(x_j)}", isolate=to_isolate).tm(cm).next_to(ell, DOWN)

        # self.add(Debug(wj))
        p2 = Tex(r"={1\over2\pi\i}\int_{\Gamma'}{l(x)",r"f(","t",r")",r"\over l(",r"t",r")(x-",r"t",r")}",r"\d ",r"t", isolate=to_isolate).tm(cm).next_to(p[3], DOWN, aligned_edge=LEFT, buff=1)
        gamma_p = TexText("$\\Gamma'$ 只包围 $x_0,\\ldots,x_n$.", color=BLUE).next_to(p2, DOWN, buff=.5)

        self.add(p,lj,lj2)
        self.wait()
        self.play(Write(ell))
        self.play(Write(wj[:6]))
        self.wait()
        self.play(Write(wj[6:]))
        self.wait()
        self.play(FadeTransform(lj2, lj3))
        self.play(FadeOut(VGroup(ell,wj)))
        self.wait()

        self.play(Write(pre))
        self.wait()
        self.play(TransformMatchingTex(pre.copy(), residue))
        self.wait()
        self.play(Write(note))
        self.play(ShowCreation(box))
        self.wait()

        self.play(Write(int_j))
        self.wait()
        self.play(FadeOut(note), FadeOut(box), Write(gamma_j))
        self.wait()

        self.play(Write(p2), VGroup(lj3, pre, residue, gamma_j).fade, .7)
        self.wait()
        self.play(Write(gamma_p))
        self.wait()
        self.play(Indicate(VGroup(p2[:3], p2[6:])), run_time=2)
        self.wait()
        self.play(Indicate(p2[3:6]), run_time=2)
        self.wait()

        self.play(FadeOut(VGroup(lj3, pre, residue, gamma_j, lj, int_j)))
        res_x = Tex(r"\mathrm{Res}\left({l(x)f(t)\over l(t)(x-t)};t=x\right)=-f(x)", color=YELLOW).scale(.8).next_to(gamma_p, buff=1)
        self.play(Write(res_x))
        self.wait()

        total = Tex("p(x)-f(x)=",r"{1\over2\pi\i}\int_{\Gamma}{l(x)",r"f(","t",r")",r"\over l(",r"t",r")(x-",r"t",r")}",r"\d ",r"t", isolate=to_isolate).next_to(res_x, DOWN, buff=.5).tm(cm).set_x(0)
        gamma = TexText("$\\Gamma$ 包围 $x_0,\\ldots,x_n,x$.", color=BLUE).next_to(total, DOWN)
        self.play(Write(total))
        self.wait()
        self.play(Write(gamma))
        self.wait()
        self.play(FadeOut(VGroup(p,p2,gamma_p, gamma, res_x)))

        hermite = Tex("f(x)-p(x)=",r"{1\over2\pi\i}\int_{\Gamma}{l(x)",r"f(","t",r")",r"\over l(",r"t",r")(",r"t",r"-",r"x",r")}",r"\d ",r"t", isolate=to_isolate).tm(cm).to_edge(UP, buff=.5)
        hermite_label = TexText("Hermite integral formula", color=YELLOW).next_to(hermite, DOWN, buff=.5)
        self.play(Write(hermite))
        self.play(FadeOut(total), Write(hermite_label))
        self.wait()

        smoother = TexText(r"``$f$ 解析区域越大, 插值收敛越快.''")
        self.play(Write(smoother))
        self.wait()
        # self.add(Debug(p2))

        # self.play(FadeOut(VGroup()))


class Pic(Scene):
    def construct(self):
        plane = Axes(x_range=[-4,4], y_range=[-2,2],height=FRAME_HEIGHT, width=FRAME_WIDTH).shift(DOWN+LEFT*.4)
        dots = VGroup(*[Dot(color=RED, radius=0.2).move_to(plane.c2p(*coord)) for coord in coords])
        graph = plane.get_graph(poly(coords), color=YELLOW, stroke_width=8)
        text = TexText("Lagrange",r"插值", stroke_width=5, color=YELLOW).scale(3).to_edge(UP, buff=.5).add_background_rectangle(opacity=1)
        self.add(plane, graph, dots, text)
        return super().construct()