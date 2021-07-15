#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author: Jeremy
@file:chol.py
@time:2021/07/06
"""
import numpy as np

from manimlib import *

M = {
    "A": RED,
    "R": YELLOW
}

class Symmetry(Scene):
    def construct(self):
        statement = Text("正定阵首先需要是对称的.").scale(2)
        VGroup(statement[0:3], statement[-4:-2]).set_color(YELLOW)
        self.play(Write(statement))
        self.wait()


a = np.array([[2, -1, 0], [-1, 2, -1], [0, -1, 2]])
A = mIntegerMatrix(a).set_color(RED)


class Why(ThreeDScene):
    CONFIG = {
        "camera_class": ThreeDCamera,
    }

    def construct(self):
        title = Title("\\heiti 正定有啥用", color=YELLOW)
        self.add(title)
        self.wait()

        # quadratic function
        xT = Matrix(["x_1", "x_2"], h_buff=.8)
        bT = mIntegerMatrix([2,1], h_buff=.8)
        x = Matrix([["x_1"], ["x_2"]])
        aa = [[1, -1], [-1, 1]]
        AA = mIntegerMatrix(aa).set_color(RED)

        ex_func = Tex("f(x)", "=", "(x_1-x_2)^2+2x_1+x_2+3").next_to(title, DOWN, buff=0.3).shift(LEFT*2)
        ex_func_mat = VGroup(Tex("="), xT, AA, x, Tex("+"), bT, x.copy(), Tex("+3")).arrange()\
            .next_to(ex_func[1], DOWN, aligned_edge=LEFT, buff=.5)
        ex_func_mat[1:].set_color(RED)
        self.play(Write(ex_func))
        self.wait()
        self.play(Write(ex_func_mat))
        self.wait()

        # quadratic form
        func, grad, hess = quad = VGroup(
            Tex("\\text{对于~}", "f(x)=\\frac12x^TAx+b^Tx+c", ",").next_to(title, DOWN),
            Tex(r"\\\nabla f(x)=Ax+b, "),
            Tex(r"\\\nabla^2f(x)=A")
        )
        # grad.next_to(func[1], DOWN, aligned_edge=LEFT)
        # hess.next_to(grad, DOWN, aligned_edge=LEFT)
        VGroup(func[1], hess).set_color(RED)
        VGroup(grad, hess).arrange().next_to(func, DOWN)
        # self.play(Write(func))
        self.play(FadeTransform(VGroup(ex_func, ex_func_mat), func))
        self.wait()
        self.play(Write(grad))
        self.play(Write(hess))
        self.wait()

        explanations = VGroup(
            TexText("正定：唯一全局最小值").scale(.8),
            TexText("半正定：最小值不唯一").scale(.8),
            TexText("不定：无最小值").scale(.8)
        ).to_edge(LEFT).shift(DOWN*2).set_color(YELLOW).fix_in_frame()

        # axes = ThreeDAxes()
        # s1 = axes.get_graph(lambda x,y: (x,y,x**2+2*y**2))
        to_fix = VGroup(*[i for i in self.mobjects])
        to_fix.fix_in_frame()

        surfaces = [
            ParametricSurface(
                lambda x, y: (x, y, x ** 2 + 2 * y ** 2),
                u_range=(-1, 1),
                v_range=(-1, 1),
                color=BLUE,
                opacity=.5,
                gloss=.3,
                shadow=0,
            ),
            ParametricSurface(
                lambda x, y: (x, y, x ** 2 +  y ** 2+2*x*y),
                u_range=(-1, 1),
                v_range=(-1, 1),
                color=BLUE,
                opacity=.5,
                gloss=.3,
                shadow=0,
            ),
            ParametricSurface(
                lambda x, y: (x, y, 3*x ** 2 - y ** 2),
                u_range=(-1, 1),
                v_range=(-1, 1),
                color=BLUE,
                opacity=.5,
                gloss=.3,
                shadow=0,
            ),
        ]
        for s in surfaces:
            s.shift(IN*3)
            s.mesh = SurfaceMesh(s, resolution=(15,15,))
            s.mesh.set_stroke(YELLOW, 1, opacity=.5)
            s.add(s.mesh)
        # s1.mesh = SurfaceMesh(s1)
        # s1.mesh.set_stroke(BLUE, 1, opacity=.5)

        frame = self.camera.frame
        frame.save_state()
        frame.set_euler_angles(
            theta=30 * DEGREES,
            phi=90 * DEGREES,
        )

        surface = surfaces[0]
        surface.save_state()

        # self.move_camera(phi=0*DEGREES, theta=0*DEGREES)
        # self.play(ShowCreation(axes))
        self.play(ShowCreation(surface, run_time=3, lag_ratio=.01), Write(explanations[0]))
        self.play(frame.animate.increment_theta(DEGREES))

        frame.add_updater(lambda m, dt: m.increment_theta(0.2 * dt))
        self.wait(10)

        for i, s in enumerate(surfaces[1:]):
            self.play(
                Transform(surface, s),
                ReplacementTransform(explanations[i], explanations[i+1])
            )
            self.wait(3)

        self.play(Restore(surface), FadeOut(explanations[2]))
        self.wait(5)
        # self.play(ShowCreation(s1.mesh))
        self.play(FadeOut(surface))
        self.wait()
        frame.clear_updaters()
        frame.to_default_state()

        equiv = Tex("\\text{minimize~}","f(x)","~\\Longleftrightarrow~Ax+b=0").shift(DOWN*.5)
        equiv[1].set_color(RED)
        self.play(Write(equiv))
        self.wait()

        inner = TexText("还可以定义内积：", r"$\langle x,y\rangle\coloneqq x^TAy$", "~~(SVM)").to_edge(DOWN, buff=1.5)
        inner[1].set_color(YELLOW)
        for i in inner:
            self.play(Write(i))
            self.wait()


class CompleteSquare(Scene):
    def construct(self):
        title = Title("\\heiti{1. 傻fufu地配方}", color=YELLOW)
        self.add(title)
        self.wait()

        definition = Tex(r"x^T", "A", r"x>0,~\forall x\in\R^n\quad(x\neq0)").next_to(title, DOWN)
        definition[1].set_color(RED)
        self.play(Write(definition))

        xT = Matrix(["x_1", "x_2", "x_3"], h_buff=.8)
        x = Matrix([["x_1"], ["x_2"], ["x_3"]])
        quadratic = VGroup(xT, A, x).arrange().next_to(definition, DOWN, buff=.5)

        self.play(Write(A))
        self.wait()
        self.play(Write(xT))
        self.play(Write(x))
        self.wait()

        expand = Tex("=", "2x_1^2+2x_2^2+2x_3^2-2x_1x_2-2x_1x_3")
        squares = Tex("=", "x_1^2+x_3^2+(x_1-x_2)^2+(x_2-x_3)^2")
        positive = Tex(">", "0")
        expand.next_to(quadratic, DOWN, aligned_edge=LEFT, submobject_to_align=expand[1])
        squares.next_to(expand, DOWN, aligned_edge=LEFT)
        positive.next_to(squares, DOWN, aligned_edge=LEFT)

        self.play(Write(expand))
        self.wait()
        self.play(Write(squares))
        self.play(Write(positive))
        self.wait()


class Eigenvalues(Scene):
    def construct(self):
        title = Title("2. \\heiti 特征值都大于0", color=YELLOW)
        self.add(title)
        self.wait()
        eigens = VGroup(A, Tex("\\text{的特征值：}", "2,~2+\\sqrt2,~2-\\sqrt2")).arrange(buff=.3).next_to(title, DOWN,
                                                                                                     buff=.3)
        self.play(Write(eigens), run_time=3)
        self.wait()

        proof = VGroup(
            TexText("$A$", "正定：").set_color_by_tex('A', RED),
            TexText("取$x$为特征向量，则"),
            Tex("x^T", "A", "x=x^T(\\lambda x)", "=\\lambda ", "x^Tx", ">0").set_color_by_tex('A', RED)
        ).arrange().next_to(eigens, DOWN, buff=.5)
        for p in proof[:-1]:
            self.play(Write(p))
            self.wait()
        self.play(Write(proof[2][:3]))
        self.wait()
        self.play(Write(proof[2][3:5]))
        self.wait()
        self.play(Write(proof[2][5:]))
        self.wait()

        brace = Brace(proof[2][-2], DOWN)
        two_norm = Tex("x_1^2+\\cdots+x_n^2").scale(.8).next_to(brace, DOWN, buff=.1)
        brace = VGroup(brace, two_norm).set_color(YELLOW)
        self.play(GrowFromCenter(brace))
        self.wait()

        converse = VGroup(
            TexText(r"$\lambda_i>0$："),
            Tex("\\quad x^T", "A", "x", "=x^T", "Q^T\\Lambda Q", "x").set_color_by_tex_to_color_map(
                {"A": RED, "Q": RED}),
            Tex("=(", "Qx", ")^T", "\\Lambda", "(Qx)"),
            Tex(">0")
        ).arrange().next_to(proof, DOWN, buff=1.2, aligned_edge=LEFT)
        # converse[1][-1][4:-1].set_color(RED)
        for c in converse[:-1]:
            self.play(Write(c))
            self.wait()

        brace1 = Brace(converse[2][1], UP)
        nonzero = Tex("Qx\\neq0").scale(.8).next_to(brace1, UP, buff=.1)
        brace1 = VGroup(brace1, nonzero).set_color(YELLOW)
        self.play(GrowFromCenter(brace1))
        self.wait()

        brace2 = Brace(converse[2][-2], DOWN)
        diag = Tex("\\mathrm{diag}(\\lambda_1,\\cdots,\\lambda_n)").next_to(brace2, DOWN)
        brace2 = VGroup(brace2, diag).set_color(YELLOW)
        self.play(GrowFromCenter(brace2))
        self.wait()

        self.play(Write(converse[-1]))
        self.wait()


def get_box(mat, order, **kwargs):
    entries = mat.get_entries()
    n = int(np.sqrt(len(entries)))
    mul = n+1
    return SurroundingRectangle(VGroup(entries[0], entries[mul*(order-1)]), **kwargs)


class Sylvester(Scene):
    def construct(self):
        title = Title("3. \\heiti 各阶顺序主子式都大于0", color=YELLOW)
        self.add(title)
        self.wait()

        A.next_to(title, DOWN).to_edge(LEFT, buff=1)
        self.play(Write(A))
        self.wait()

        boxes = VGroup()
        colors = [YELLOW, GREEN, BLUE]
        for i, color in zip(range(1, 4), colors):
            box = get_box(A, i, color=color, buff=.3)
            boxes.add(box)

        minors = VGroup(
            VGroup(Det(a[np.ix_([0], [0])]), Tex(">0")).arrange().scale(.9),
            VGroup(Det(a[np.ix_([0,1], [0,1])]), Tex(">0")).arrange().scale(.9),
            VGroup(Det(a[np.ix_([0,1,2], [0,1,2])]), Tex(">0")).arrange().scale(.9),
        ).arrange(buff=.4).next_to(A, buff=.5)
        for m, c in zip(minors, colors):
            m.set_color(c)

        self.play(ShowCreation(boxes[0]))
        self.wait()
        self.play(Write(minors[0]))
        self.wait()

        for i in range(1, 3):
            self.play(
                TransformFromCopy(boxes[i-1], boxes[i]),
                Write(minors[i])
            )
            self.wait()

        sylvester = Title("Sylvester's Criterion", color=YELLOW)
        self.play(Transform(title, sylvester))
        self.wait()

        ## prove part
        necessary = TexText("假设$A$正定.").next_to(A, DOWN, buff=.5, aligned_edge=LEFT)
        self.play(Write(necessary))
        divide = VGroup(
            Tex("\\text{记~}","A=").set_color_by_tex("A", RED),
            Matrix([["A_k", "*"], ["*", '*']], h_buff=1).set_color(RED),
            TexText(", 要证$|A_k|>0$.")
        ).arrange().next_to(necessary)
        self.wait()
        self.play(Write(divide[:2]))
        self.wait()
        self.play(Write(divide[2]))
        self.wait()

        nonzero = VGroup(
            Tex("\\text{对非零向量~}x_k,~x_k^TA_kx_k="),
            Matrix(["x_k^T", 0], h_buff=.9),
            Matrix([["A_k", "*"], ["*", '*']], h_buff=1).set_color(RED),
            Matrix([["x_k"], [0]]),
            Tex(">0")
        ).arrange().next_to(necessary, DOWN, aligned_edge=LEFT, buff=.5)
        brace = Brace(nonzero[1], DOWN, color=YELLOW)
        brace = VGroup(brace, TexText("非零", color=YELLOW).next_to(brace, DOWN))
        conclusion = Tex("A_k\\text{正定}","\\Longrightarrow |A_k|>0.").next_to(nonzero, DOWN, aligned_edge=LEFT)
        self.play(Write(nonzero[0]))
        self.wait()

        self.play(Write(nonzero[1:4]))
        self.wait()

        self.play(GrowFromCenter(brace))
        self.wait()

        self.play(Write(nonzero[4:]))
        self.wait()

        for c in conclusion:
            self.play(Write(c))
            self.wait()

        to_fade = list(self.mobjects)
        to_fade.remove(title)
        self.play(FadeOut(VGroup(*to_fade)))

        sufficient = VGroup(
            TexText("\\heiti 各顺序主子式$>0$","~$\\Longrightarrow$~","$A$","正定").tm(M),
            Tex("?")
        ).next_to(title, DOWN, buff=.5)
        sufficient[1].next_to(sufficient[0][1], UP, buff=0)
        self.play(Write(sufficient))
        self.wait()

        base = TexText("\\heiti 对一阶方阵，结论成立.").next_to(sufficient, DOWN, buff=.4).align_to(title, LEFT)
        self.play(Write(base))
        self.wait()

        assumption = TexText("\\heiti 假设对$n-1$阶方阵成立.").next_to(base, DOWN, aligned_edge=LEFT)
        An = TexText("\\heiti 那么对$n$阶方阵","$A$",",").tm(M).next_to(assumption)
        self.play(Write(assumption))
        self.wait()
        self.play(Write(An))
        self.wait()

        blocks = VGroup(
            Tex("A="),
            Matrix([["A_{n-1}", r"\mathbf\alpha"], [r"\mathbf\alpha^T", "a_{nn}"]], h_buff=1),
        ).set_color(RED).arrange().next_to(assumption, DOWN, aligned_edge=LEFT, buff=1.5)
        a00 = blocks[1].get_entries()[0]
        a00.set_color(YELLOW)
        self.play(Write(blocks))
        self.wait()

        brace = Brace(a00, UP, color=YELLOW)
        brace = VGroup(brace, TexText("正定","，合同于单位阵", color=brace.get_color()).scale(.7).next_to(brace, UP))
        self.play(Indicate(assumption))
        self.wait()
        self.play(GrowFromCenter(brace))
        self.wait()

        elementary = Matrix([["A_{n-1}", '0'], ['0', "b"]], h_buff=1).set_color(RED).next_to(blocks, buff=2)
        elementary.get_entries()[0].set_color(YELLOW)
        b = elementary.get_entries()[3].set_color(YELLOW)
        arrow = Arrow(blocks.get_right(), elementary.get_left())
        elem_comment = TexText("合同变换").scale(.7).next_to(arrow, UP)
        self.play(GrowArrow(arrow), Write(elem_comment))
        self.play(Write(elementary))
        self.wait()

        brace2 = Brace(b, DOWN, color=YELLOW).stretch(1.5, 0)
        brace2 = VGroup(brace2, Tex("b>0", color=YELLOW).scale(.8).next_to(brace2, DOWN))
        det = Tex("|A|=|A_{n-1}|\\,b", color=BLUE).scale(.8).next_to(elementary, UP)
        self.play(Write(det))
        self.wait()
        self.play(GrowFromCenter(brace2))
        self.wait()

        diag = Matrix([["I_{n-1}", '0'], ['0', "b"]], h_buff=1).set_color(RED).next_to(elementary, buff=2)
        diag.get_entries()[0].set_color(YELLOW)
        diag.get_entries()[3].set_color(YELLOW)
        arrow2 = Arrow(elementary.get_right(), diag.get_left())
        diag_comment = elem_comment.copy().next_to(arrow2, UP)
        self.play(GrowArrow(arrow2), Write(diag_comment))
        self.play(Write(diag))
        self.wait()


class Cholesky(Scene):
    def construct(self):
        title = Title("\\heiti Cholesky分解", color=YELLOW)
        self.add(title)
        self.wait()

        chol = Tex("A","=","R^TR").tm(M).next_to(title, DOWN, buff=.5)
        self.play(Write(chol))
        self.wait()

        constraints = TexText("$R$","是上三角阵","，且对角元大于$0$.").tm(M).next_to(chol, DOWN, buff=1)
        Lambda = Matrix(np.diag(["1", "-1", "-1", "\\ddots", "1"]), h_buff=1, v_buff=.6).scale(.8)
        self.play(Write(constraints[:2]))
        self.wait()

        ## positive diag
        L2 = VGroup(
            Tex("\\Lambda="), Lambda, Tex(",","~\\Lambda^2=I").set_color_by_tex("Lambda", BLUE)
        ).arrange().to_edge(DOWN)
        another = Tex("A","=","(\\Lambda R)^T(\\Lambda R)").tm(
            {'A': RED, "Lambda": BLUE}
        ).next_to(chol, DOWN)
        self.play(Write(L2[:2]))
        self.wait()
        self.play(Write(L2[2]))
        self.wait()

        self.play(Write(another))
        self.wait()

        self.play(Write(constraints[2]), FadeOut(VGroup(another, L2)))
        self.wait()

        ## LLT
        LL = Tex("LL^T", color=BLUE).next_to(chol[-1], DOWN)
        rT = np.array([
            ['\\scriptstyle +', '', '', ''],
            ['*', '\\scriptstyle +', '', ''],
            ['*', '*', '\\scriptstyle +', ''],
            ['*', '*', '*', '\\scriptstyle +']
        ])
        RT = Matrix(rT, h_buff=1)
        R = Matrix(rT.T, h_buff=1)
        factor = VGroup(RT, R).set_color(BLUE).arrange().to_edge(DOWN, buff=.5)

        self.play(Write(LL))
        self.wait()
        self.play(Write(factor))
        self.wait()


def get_sub(mat, order):
    entries = mat.get_entries()
    n = int(np.sqrt(len(entries)))
    res = VGroup()
    for i in range(order):
        res.add(*[entries[_+i] for _ in [n*j for j in range(order)]])
    return res

class CholeskyExample(Scene):
    def construct(self):
        title = Title("\\heiti Cholesky分解", color=YELLOW)
        self.add(title)
        self.wait()

        a = np.array(
            [[1,1,3],
            [1,5,3],
            [3,3,10]]
        )
        A = mIntegerMatrix(a)

        r0 = np.array(
            [["r_{11}", "r_{12}", "r_{13}"],
             ["", "r_{22}", "r_{23}"],
             ["", "", "r_{33}"]]
        )
        r = np.array(
            [['1', '1', '3'],
             ['', '2', '0'],
             ['', '', '1']]
        )
        r1 = r2 = r3 = None
        r_list = [r0,0,0,0]
        for i in range(1, len(r_list)):
            r_list[i] = r_list[i-1].copy()
            r_list[i][:,i-1] = r[:,i-1]
        r0, r1, r2, r3 = r_list

        R_list = []
        Rt_list = []
        for r in r_list:
            R_list.append(Matrix(r, h_buff=1))
            Rt_list.append(Matrix(r.T, h_buff=1))
        R0, R1, R2, R3 = R_list
        R0t, R1t, R2t, R3t = Rt_list

        Rresult = Matrix(
            np.array(
            [['r_{11}^2', 'r_{11}r_{12}', 'r_{11}r_{13}'],
             ['r_{11}r_{12}', 'r_{12}^2+r_{22}^2', 'r_{12}r_{13}+r_{22}r_{23}'],
             ['r_{11}r_{13}', 'r_{12}r_{13}+r_{22}r_{23}', 'r_{13}^2+r_{23}^2+r_{33}^2']]
        ),
            h_buff=2.8,
            element_alignment_corner=DOWN,
            element_to_mobject = lambda i: Tex(i).scale(.8) if len(i)>20 else Tex(i)
        )

        raw = VGroup(
            A, Tex("="), R0t, R0
        ).arrange().next_to(title, DOWN)
        raw_result = VGroup(
            Tex("="), Rresult
        ).arrange().next_to(raw[1], DOWN, aligned_edge=LEFT, buff=1.5)
        for i in R_list[1:]:
            i.move_to(raw[-1])
        for i in Rt_list[1:]:
            i.move_to(raw[-2])
        self.play(Write(raw))
        self.wait()
        self.play(Write(raw_result))
        self.wait()

        A_boxes = VGroup()
        R_boxes = VGroup()
        for i, color in zip([1,2,3], [YELLOW, RED, BLUE]):
            A_boxes.add(get_box(A, i, color=color))
            R_boxes.add(get_box(Rresult, i, color=color, buff=.3).shift(LEFT*.2))
        self.play(
            ShowCreation(VGroup(A_boxes[0])),
            get_sub(Rresult, 1).animate.set_color(YELLOW)
        )
        self.wait()

        factor = 0.7
        r11 = Tex("r_{11}=\\sqrt{1}", color=YELLOW).scale(factor).next_to(raw, DOWN).to_edge(LEFT)
        r12 = Tex("r_{12}=1/r_{11}", color=RED).scale(factor).next_to(r11, DOWN, aligned_edge=LEFT)
        r22 = Tex("r_{22}=\\sqrt{5-r_{12}^2}", color=RED).scale(factor).next_to(r12, DOWN, aligned_edge=LEFT)
        r13 = Tex("r_{13}=3/r_{11}", color=BLUE).scale(factor).next_to(r22, DOWN, aligned_edge=LEFT)
        r23 = Tex("r_{23}=\\left(3-r_{12}r_{13}\\right)/r_{22}", color=BLUE).scale(factor).next_to(r13, DOWN, aligned_edge=LEFT)
        r33 = Tex("r_{33}=\\sqrt{10-r_{13}^2-r_{23}^2}", color=BLUE).scale(factor).next_to(r23, DOWN, aligned_edge=LEFT)

        self.play(Write(r11))
        self.play(RT(R0t, R1t), RT(R0, R1))
        self.wait()

        self.play(
            RT(A_boxes[0], A_boxes[1]),
            get_sub(Rresult, 2).animate.set_color(RED)
        )
        self.wait()
        self.play(Write(r12))
        self.wait()
        self.play(Write(r22))
        self.wait()
        self.play(RT(R1t, R2t), RT(R1, R2))
        self.wait()

        self.play(
            RT(A_boxes[1], A_boxes[2]),
            get_sub(Rresult, 3).animate.set_color(BLUE)
        )
        self.wait()
        self.play(Write(r13))
        self.play(Write(r23))
        self.play(Write(r33))
        self.wait()
        self.play(RT(R2t, R3t), RT(R2, R3))
        self.wait()

        self.play(
            Flash(r11[0][5], color=WHITE),
            Flash(r22[0][5], color=WHITE),
            Flash(r33[0][5], color=WHITE),
        )
        self.wait()

        self.play(FadeOut(
            VGroup(
                raw_result, r11, r12, r13, r22, r23, r33, A_boxes[2], raw[:2], R3, R3t
            )
        ))

        algorithm = VGroup(
            VGroup(TexText("for"), Tex("j=1\\,..\\,n")).arrange(buff=.5, aligned_edge=UP),
            VGroup(TexText("for"), Tex("i=1\\,..\\,j-1")).arrange(buff=.5, aligned_edge=UP),
            Tex(r"r_{i j}=\left(a_{i j}-\sum_{k=1}^{i-1} r_{k i} r_{k j}\right) /"," r_{i i}"),
            Tex(r"r_{j j}=\sqrt{a_{j j}-\sum_{k=1}^{j-1} r_{k j}^{2}}")
        ).arrange(DOWN, aligned_edge=LEFT).next_to(title, DOWN, buff=.5)#.to_edge(LEFT, buff=1)
        VGroup(algorithm[1], algorithm[3]).shift(RIGHT)
        algorithm[2].shift(RIGHT*2)
        VGroup(algorithm[1], algorithm[2]).set_color(RED)

        flops = Tex("\\frac {n^3}{3}~\\text{flops}", color=YELLOW).next_to(algorithm, LEFT)
        box = SurroundingRectangle(flops)
        self.play(Write(algorithm))
        self.wait()
        self.play(Write(flops))
        self.play(ShowCreation(box))
        self.wait()

        arrows = VGroup(
            Arrow(ORIGIN, DOWN, color=YELLOW).next_to(algorithm[2][-1], UP),
            Arrow(ORIGIN, LEFT, color=YELLOW).next_to(algorithm[-1]),
        ).set_color(YELLOW)
        for a in arrows:
            self.play(GrowArrow(a))
            self.wait()


class App(Scene):
    def construct(self):
        title = Title("\\heiti 应用: 解方程组", color=YELLOW)
        self.add(title)
        self.wait()

        a = np.array(
            [[1, 1, 3],
             [1, 5, 3],
             [3, 3, 10]]
        )
        r = np.array(
            [['1', '1', '3'],
             ['', '2', '0'],
             ['', '', '1']]
        )
        A = mIntegerMatrix(a)
        R = Matrix(r, h_buff=1)
        Rt = Matrix(r.T, h_buff=1)
        VGroup(A, R, Rt).set_color(RED)
        b = mIntegerMatrix(np.array([[1],[1],[1]]))
        x = Matrix(np.array([['x_1'], ['x_2'], ['x_3']]), h_buff=1).set_color(YELLOW)
        y = Matrix(np.array([['y_1'], ['y_2'], ['y_3']]), h_buff=1).set_color(BLUE)

        eq = VGroup(
            A, x.copy(), Tex('='), b.copy()
        ).arrange().next_to(title, DOWN)
        eq_r = VGroup(
            Rt, R, x, Tex('='), b
        ).arrange().next_to(title, DOWN)
        eq_y = VGroup(
            Rt.copy(), y, Tex('='), b.copy()
        ).arrange().next_to(title, DOWN)
        subs = VGroup(
            R.copy(), x.copy(), Tex('='), y.copy(),
        ).arrange().next_to(eq_y, DOWN, buff=.5)
        self.play(Write(eq))
        self.wait()

        self.play(RT(eq, eq_r))
        self.wait()

        self.play(TransformFromCopy(eq_r[1:3], subs[:2]))
        self.play(Write(subs[2:]))
        self.play(
            RT(eq_r[0], eq_y[0]),
            RT(eq_r[1:3], eq_y[1]),
            RT(eq_r[3:], eq_y[2:]),
        )
        self.wait()


class Cauchy(Scene):
    def construct(self):
        title = Title("\\heiti 应用：度量矩阵", color=YELLOW)
        self.add(title)
        self.wait()

        prob = VGroup(
            TexText("给定正定矩阵$A\\in\\R^{n\\times n}$， 证明:").next_to(title, DOWN).to_edge(LEFT, buff=1),
            Tex("|a_{ij}|<\\sqrt{a_{ii}a_{jj}}").scale(1.1),
            Tex("(i\\ne j).")
        )
        prob[1][0].set_color(YELLOW)
        prob[1].next_to(prob[0], DOWN).set_x(0)
        prob[2].next_to(prob[1], buff=.5)
        self.play(Write(prob))
        self.wait()

        R = Matrix(["r_1", "r_2", "\\cdots", "r_n"], h_buff=.8,element_alignment_corner=ORIGIN)\
            .set_color(BLUE)
        Rt = Matrix([["r_1^T"], ["r_2^T"], ["\\vdots"], ["r_n^T"]]).set_color(BLUE).scale(.8)
        inner = VGroup(
            Tex("A","=","R^TR","=").tm({'A': RED, 'R': BLUE}),
            Rt,
            R,
            Tex("\\Longrightarrow", " a_{ij}","=","r_i^Tr_j=\\langle r_i, r_j\\rangle")
                .tm({'a': RED, 'r': BLUE, 'right': YELLOW})
        ).arrange().next_to(prob, DOWN, buff=.5).set_x(0)
        self.play(Write(inner[0]))
        self.wait()

        self.play(Write(inner[1:3]))
        self.wait()
        self.play(Write(inner[3:]))
        self.wait()

        cauchy = Tex(
            "\\left|\\langle r_i,r_j \\rangle\\right|< \\lVert r_i \\rVert\\lVert r_j \\rVert",
            color=YELLOW
        ).next_to(inner, DOWN).set_x(0)
        comment = TexText("Cauchy–Schwarz不等式").scale(.8).next_to(cauchy, DOWN)
        self.play(Write(cauchy))
        self.wait()

        self.play(Write(comment))
        self.wait()


class Pic(Scene):
    def construct(self):
        A = mIntegerMatrix(a, h_buff=1).scale(2).to_edge(LEFT, buff=1)
        title = Text("正 定").scale(4)
        trans = TexText("pos.~ def.").scale(2)
        VGroup(title, trans).set_color(YELLOW).arrange(DOWN).to_edge(RIGHT, buff=1)
        boxes = VGroup(*[get_box(A, i, color=c, stroke_width=10, buff=.5) for i, c in zip(range(1,4), [GREEN, RED, BLUE])])
        self.add(A, boxes, title, trans)