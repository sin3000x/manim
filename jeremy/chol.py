#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author: Jeremy
@file:chol.py
@time:2021/07/06
"""
from manimlib import *


class Symmetry(Scene):
    def construct(self):
        statement = Text("正定阵首先需要是对称的.").scale(2)
        VGroup(statement[0:3], statement[-4:-2]).set_color(YELLOW)
        self.play(Write(statement))
        self.wait()


a = [[2, -1, 0], [-1, 2, -1], [0, -1, 2]]
A = mIntegerMatrix(a).set_color(RED)


class Why(ThreeDScene):
    CONFIG = {
        "camera_class": ThreeDCamera,
    }

    def construct(self):
        title = Title("\\heiti 正定有啥用", color=YELLOW)
        self.add(title)
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
        self.play(Write(func))
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
