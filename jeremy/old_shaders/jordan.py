from manimlib import *


def get_submat_box(matrix, start, end, **kwargs):
    elements = matrix.get_entries()
    N = int(len(elements)**(1/2))
    # print("N=",N)
    diag = [elements[i] for i in range(N**2) if i%(N+1)==0]
    # print("diag=",diag)
    sub = VGroup(*diag[start-1:end])
    return SurroundingRectangle(sub, **kwargs)


def get_submat_boxes(matrix, lists, **kwargs):
    res = VGroup()
    for l in lists:
        if len(l)==2:
            res.add(get_submat_box(matrix, *l, **kwargs))
        if len(l)==1:
            res.add(get_submat_box(matrix, *l, *l, **kwargs))

    return res


class Opening(Scene):
    def construct(self):
        simpler = VGroup(Tex("n"), TexText("个", "(线性无关的)", "特征向量")).arrange().scale(2)
        simpler[1][1].set_color(YELLOW)
        lazy = Text("我懒（").to_corner(DR)
        self.add(simpler)
        self.wait(5)
        self.add(lazy)
        self.wait(1)


class Recap(Scene):
    def construct(self):
        condition = Tex(r"A\text{~可对角化}\Longleftrightarrow A\text{~有$n$个特征向量}", isolate=['A']) \
            .tm({"A": RED}).scale(1.5)

        diff = TexText(r"特征值不同$\Longrightarrow$特征向量无关").scale(1.5)
        VGroup(condition, diff).arrange(DOWN, buff=1.5)
        self.play(Write(condition))
        self.wait()
        self.play(Write(diff))
        self.wait()


class Motivation(Scene):
    def construct(self):
        a = np.array([[5, 4, 2, 1], [0, 1, -1, -1], [-1, -1, 3, 0], [1, 1, -1, 2]])
        b = a - 4*np.eye(4)
        c = [[1,'','',-1],['',1,'',0],['','',1,1],['','','',0]]
        diag = np.diag([1,2,4,4])
        jordan = [[1,0,0,0],[0,2,0,0],[0,0,4,1],[0,0,0,4]]
        A = Matrix(a, element_to_mobject=lambda x: Tex(f"{x}"))
        B = Matrix(b, element_to_mobject=lambda x: Tex(f"{int(x)}"))
        C = Matrix(c, element_to_mobject=lambda x: Tex(f"{x}"))
        D = Matrix(diag, element_to_mobject=lambda x: Tex(f"{x}"if x!=0 else ''), h_buff=1)
        J = Matrix(jordan, element_to_mobject=lambda x: Tex(f"{x}" if x!=0 else ''), h_buff=1)

        # introduce A
        A_label = VGroup(Tex("A="), A).arrange()
        values = Tex("{{\\lambda=1,2,}}{{4,4}}", color=YELLOW).scale(1.5)
        VGroup(A_label, values).arrange(buff=1).to_edge(UP)
        self.play(Write(A_label))
        self.wait()

        # give its eigenvalues
        self.play(Write(values))
        self.wait()

        # whether independent
        issue = Brace(values[1], DOWN)
        issue = VGroup(issue, TexText("2个向量？").next_to(issue, DOWN))
        only = TexText("1个向量").move_to(issue[1])
        self.play(GrowFromCenter(issue))
        self.wait()

        # recap on eigenvectors
        solve = Tex(r"Ax=4x", isolate=['x','A','4','=']).tm({'x': RED}).scale(1.5).next_to(A_label, DOWN, buff=1).set_x(0)
        solve2 = Tex(r"(A-4I)x=0", isolate=['x','(',')','A','=','-','4','0']).tm({'x': RED}).scale(1.5).move_to(solve)
        self.play(Write(solve))
        self.wait()
        self.play(TransformMatchingTex(solve, solve2, path_arc=PI/2))
        self.wait()

        self.play(FadeOut(solve2[-3:]))
        B.next_to(A, DOWN, buff=1)
        C.move_to(B)
        self.play(ReplacementTransform(solve2[:-3], B))
        self.wait()

        self.play(ReplacementTransform(B, C))
        self.wait()

        # rank-nullity
        rank = Tex("\\rank(A-4I)=3")
        nullity = Tex("\\textrm{dim}\\left(\\mathrm{null}(A-4I)\\right)=1", color=YELLOW)
        VGroup(rank, nullity).arrange(DOWN).next_to(C, buff=1)
        self.play(Write(rank))
        self.wait()
        self.play(Write(nullity))
        self.wait()

        self.play(RT(issue[1], only))
        self.wait()
        self.play(FadeOut(VGroup(C, rank, nullity)))

        # undiagonalizable
        similar = VGroup(Tex("A"), Tex("\\sim"), D).arrange().to_edge(DOWN)
        self.play(Write(similar))

        cross = Cross(similar)
        self.play(ShowCreation(cross))
        self.wait()

        # JCF
        self.play(Uncreate(cross))
        J.move_to(D)
        self.play(Transform(D, J))
        self.wait()

        # naming
        self.play(similar.shift, LEFT*2)
        self.play(D.set_color, BLUE)
        self.wait()
        box = get_submat_box(D, 3, 4)
        jcf = VGroup(TexText("Jordan Canonical Form", color=D.get_color()),
                     TexText("若尔当标准型", color=BLUE).scale(1)).arrange(DOWN)
        block = TexText("Jordan block", color=YELLOW)
        VGroup(jcf, block).arrange(DOWN, aligned_edge=LEFT, buff=.5).next_to(D, buff=.5)
        aka = TexText("(若当/约当)").scale(.8).next_to(jcf[1][0][:3], DOWN)
        self.play(Write(jcf))
        self.wait()
        self.play(Write(aka))
        self.wait()
        self.play(FadeOut(aka))
        self.wait()

        # for i, ele in enumerate(D.get_entries()):
        #     t = Text(str(i)).move_to(ele)
        #     self.add(t)

        self.play(ShowCreation(box))
        self.wait()
        self.play(Write(block))


class JordanBlock(Scene):
    def construct(self):
        j = [['\\lambda','1','',''],['','\\lambda','\\ddots',''],['','','\\ddots','1'],['','','','\\lambda']]
        j_other = [['\\lambda','','',''],['1','\\lambda','',''],['','\\ddots','\\ddots',''],['','','1','\\lambda']]
        j1 = [[1,0,0,0],[0,2,0,0],[0,0,4,1],[0,0,0,4]]
        diag = np.diag([1,2,4,4])
        J = Matrix(j, h_buff=1)
        J_other = Matrix(j_other, h_buff=1)
        J1 = Matrix(j1, element_to_mobject=lambda x: Tex(f"{x}" if x != 0 else ''), h_buff=1, v_buff=.8)
        D = Matrix(diag, element_to_mobject=lambda x: Tex(f"{x}" if x != 0 else ''), h_buff=1)
        VGroup(*[J.get_entries()[i] for i in [0,5,10,15]]).set_color(RED)
        VGroup(*[J_other.get_entries()[i] for i in [0,5,10,15]]).set_color(RED)
        self.add(J)

        values = TexText("1. 特征值是$\\lambda$.")
        values[0][-2].set_color(RED)
        vectors = TexText("2. 只有一个特征向量.")
        v = VGroup(values, vectors).arrange(DOWN, buff=.5, aligned_edge=LEFT)
        VGroup(J, v).arrange(buff=1.5).to_edge(UP, buff=.5)
        self.play(Write(values))
        self.wait()
        self.play(Write(vectors))
        self.wait()

        VGroup(J1, D).arrange(buff=1.5).to_edge(DOWN, buff=.5)#.set_color()
        boxes1 = get_submat_boxes(J1, [[1, 1], [2, 2], [3, 4]])
        boxes2 = get_submat_boxes(D, [[1, 1], [2, 2], [3, 3], [4, 4]])
        self.play(Write(J1))
        self.wait()
        self.play(ShowCreation(boxes1), run_time=2)
        self.wait()
        self.play(Write(D))
        self.wait()
        self.play(ShowCreation(boxes2), run_time=2)
        self.wait()

        # other definition
        J_other.move_to(J)
        self.play(RT(J, J_other))
        self.wait()

        # propositions
        J1 = VGroup(J1, boxes1)
        self.play(FadeOut(VGroup(J_other, v, D, boxes2)))
        self.play(J1.move_to, LEFT*4)

        p1 = TexText("(a) 有几块，就有几个特征向量.")
        p2 = TexText("(b) 4的代数重数$=4$出现的次数.")
        p3 = TexText("(c) 4的几何重数=含4的块数.")
        p2[0][5:9].set_color(RED)
        p2[0][-3:-1].set_color(RED)
        p3[0][5:9].set_color(BLUE)
        p3[0][-3:-1].set_color(BLUE)
        p = VGroup(p1, p2, p3).arrange(DOWN, aligned_edge=LEFT, buff=.5).next_to(J1, buff=1)
        for i in p:
            self.play(Write(i))
            self.wait()

        dim = Tex(r"\mathrm{dim}\left(\mathrm{null}(A-4I)\right)", color=BLUE).next_to(p3, DOWN)
        self.play(Write(dim))
        self.wait()


class Theorem(Scene):
    def construct(self):
        theorem = TexText("任何复方阵都相似于其Jordan标准型.", color=YELLOW).scale(1.5).shift(UP)
        self.play(Write(theorem))
        self.wait()

        r1 = TexText(r"[1] Roger A. Horn and Charles R. Johnson. Matrix Analysis.")
        r2 = TexText(r"[2] James M. Ortega. Matrix Theory: A Second Course.")
        r3 = TexText(r"[3] Gilbert Strang. Linear Algebra and Its Applications.")
        r = VGroup(r1, r2, r3).arrange(DOWN, aligned_edge=LEFT).to_edge(DOWN)
        self.play(Write(r))
        self.wait(5)


class Structure(Scene):
    def construct(self):
        a = [[2,0,0,0],[-3,2,0,1],[0,0,2,1],[0,0,0,2]]
        A = Matrix(a, element_to_mobject=lambda t: Tex(str(t)), h_buff=1)
        j1 = [[2,0,0,0],
              [0,2,1,0],
              [0,0,2,1],
              [0,0,0,2]]
        j2 = [[2,1,0,0],
              [0,2,0,0],
              [0,0,2,1],
              [0,0,0,2]]
        J1 = Matrix(j1, element_to_mobject=lambda t: Tex(str(t) if t!=0 else ''), h_buff=1)
        J2 = Matrix(j2, element_to_mobject=lambda t: Tex(str(t) if t!=0 else ''), h_buff=1)
        Aequals = VGroup(Tex("A="), A).arrange()

        values = Tex("\\lambda=2,2,2,2")
        vectors = TexText("2个特征向量.")
        v = VGroup(values, vectors).arrange(DOWN, buff=.5).set_color(YELLOW)

        VGroup(Aequals, v).arrange(buff=2).to_edge(UP)
        self.add(Aequals)
        self.wait()

        self.play(Write(values))
        self.wait()
        self.play(Write(vectors))
        self.wait()

        VGroup(J1, J2).arrange(buff=1).to_edge(DOWN)
        boxes1 = get_submat_boxes(J1, [[1],[2,4]])
        boxes2 = get_submat_boxes(J2, [[1,2],[3,4]])
        self.play(Write(J1))
        self.play(ShowCreation(boxes1))
        self.wait()
        self.play(Write(J2))
        self.play(ShowCreation(boxes2))
        self.wait()
        J1 = VGroup(J1, boxes1)
        J2 = VGroup(J2, boxes2)

        # size
        self.play(FadeOut(VGroup(J1, J2)))
        self.wait()
        num = VGroup(TexText("$k$阶Jordan块的个数："),
                     Tex(r"\mathrm{rank}(A-\lambda I)^{k-1}+\mathrm{rank}(A-\lambda I)^{k+1}-2\,\mathrm{rank}(A-\lambda I)^{k}")
                     ).arrange(DOWN).next_to(Aequals, DOWN, buff=.5).set_x(0).set_color(BLUE)
        self.play(Write(num[0]))
        self.wait()
        self.play(Write(num[1]))
        self.wait()

        one_order = VGroup(TexText("1阶Jordan块数："),
                           Tex(r"\mathrm{rank}(A-2 I)^{0}+\mathrm{rank}(A-2 I)^{2}-2\,\mathrm{rank}(A-2 I)^{1}"))\
            .arrange(DOWN).next_to(num, DOWN)
        self.play(Write(one_order))
        self.wait()

        equals = VGroup(Tex("="), Tex(r"4+0-2\times2"), Tex("=0")).arrange()
        equals.next_to(one_order, DOWN, index_of_submobject_to_align=1, submobject_to_align=equals[1], aligned_edge=LEFT)
        self.play(Write(equals[:2]))
        self.wait()

        self.play(Write(equals[2]))
        self.wait()

        self.play(FadeOut(VGroup(num, one_order, equals)))
        self.play(FadeIn(VGroup(J1,J2)))
        cross = Cross(J1)
        self.play(ShowCreation(cross))


class Meaning(Scene):
    def construct(self):
        title = Title("Jordan标准型的意义", color=YELLOW)
        self.add(title)

        sim = Tex(r"1.~A\sim B~\iff~ J_A=J_B", isolate=['A','J','B']).tm({'A': RED, 'J': BLUE, 'B': RED})
        C_H = TexText(r"2. Cayley–Hamilton 定理：$p(A)=O$.")
        C_H[0][-5].set_color(RED)
        minimal = TexText(r"3. 极小多项式")
        calc = Tex(r"4.~A=XJX^{-1}~\implies~ A^n=XJ^nX^{-1},~\e^{A}=X\e^{J}X^{-1}")
        v = VGroup(sim, C_H, minimal, calc).arrange(DOWN, aligned_edge=LEFT, buff=.5)

        for i, j in zip([2,11,12,21,22],[5,15,16,25,26]):
            calc[0][i].set_color(RED)
            calc[0][j].set_color(BLUE)

        for i in v:
            self.play(Write(i))
            self.wait()

        # for i, t in enumerate(calc[0]):
        #     self.add(Text(str(i), color=PINK).scale(.5).move_to(t))


class Pic(Scene):
    def construct(self):
        jordan = [[1, 0, 0, 0], [0, 2, 0, 0], [0, 0, 4, 1], [0, 0, 0, 4]]
        J = Matrix(jordan, element_to_mobject=lambda x: Tex(f"{x}" if x != 0 else ''), h_buff=1)
        boxes = get_submat_boxes(J, [[1],[2],[3,4]], buff=.2).set_stroke(width=10)
        J = VGroup(J, boxes).scale(1.5).to_edge(UP)
        t = TexText("Jordan标准型").scale(2.8).to_edge(DOWN, buff=.8)
        self.add(J,t)





