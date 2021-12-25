#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author: Jeremy
@file:norm_mat.py
@time:2021/12/16
"""
import numpy as np

from manimlib import *


class Norms(Scene):
    def construct(self):
        title = Title("norm (范数)", color=YELLOW)
        self.add(title)
        self.wait()
        map = Tex(r"\lVert\cdot\rVert\colon\C^{m\times n}\to\R").next_to(title, DOWN, buff=.7)
        self.play(Write(map))
        self.wait()

        properties = VGroup(
            VGroup(Tex(r"1.~\lVert", r" A", r"\rVert\geq 0").set_color_by_tex("A", RED),
                   Tex(r"\text{, 等号成立}~\iff~ ", r"A", r"=O").set_color_by_tex("A", RED)).arrange(),
            VGroup(Tex(r"2.~\lVert", r"\alpha", r" A", r"\rVert=|", r"\alpha", r"|\lVert", r" A", r"\rVert")
                   .tm({"A": RED, "alpha": BLUE}),
                   ).arrange(),
            VGroup(Tex(r"3.~\lVert", r" A", r"+", r"B", r"\rVert\leq\lVert", r" A", r"\rVert", r"+\lVert", r" B",
                       r"\rVert")
                   .tm({'A': RED, 'B': RED}),
                   ).arrange()
        ).arrange(DOWN, aligned_edge=LEFT, buff=.5).next_to(map, DOWN, buff=1)
        self.add(properties)
        self.wait(3)


a = np.array([[2, 1], [-2, 1]])


class Trans(LinearTransformationScene):
    CONFIG = {
        "show_basis_vectors": False,
        "foreground_plane_kwargs": {
            "x_range": [-8, 8],
            "y_range": [-8, 8],
            "faded_line_ratio": 0
        },
    }

    def construct(self):
        self.apply_matrix(a)
        self.wait()
        self.apply_inverse(a)
        self.wait()
        vectors = VGroup(
            *[self.get_vector(self.plane.c2p(np.cos(t), np.sin(t))) for t in np.linspace(0, TAU, 20)[:-1]]
        ).set_color(GREEN)  # .add(self.get_vector(self.plane.c2p(-1,0)).set_color(YELLOW))
        circle = Circle(color=RED, radius=1)
        maximizer = self.get_vector(self.plane.c2p(-1, 0)).set_color(YELLOW).set_opacity(0)
        self.add_transformable_mobject(circle, vectors, maximizer)
        self.play(ShowCreation(circle), LaggedStartMap(GrowArrow, vectors, lag_ratio=.2))
        self.apply_matrix(a)
        self.wait()

        maximizer.set_opacity(1)
        self.play(GrowArrow(maximizer))
        self.wait()


class Induced(Scene):
    def construct(self):
        cm = {'A': RED}
        title = Title("induced norm (诱导范数)", color=YELLOW)
        self.add(title)
        self.wait()
        definition = Tex(r"\lVert ", r"A", r"\rVert\coloneqq\max_{\lVert \vx\rVert=1}\lVert ", r"A",
                         r"\vx\rVert", r"=\max_{\vx\ne0}{\lVert ", r"A", r"\vx\rVert\over\lVert\vx\rVert}") \
            .tm(cm).next_to(title, DOWN, buff=.5)
        self.play(Write(definition[:5]))
        self.wait()
        self.play(Write(definition[5:]))
        self.wait()

        p_norm = Tex("\lVert ", r"A", r"\rVert_p=", r"\max_{\vx\ne0}{\lVert ", r"A",
                     r"\vx\rVert_p\over\lVert\vx\rVert_p}") \
            .tm(cm).scale(1.5).next_to(definition, DOWN, buff=1)
        box = SurroundingRectangle(p_norm, buff=.3)
        self.play(Write(p_norm))
        self.play(ShowCreation(box))
        self.wait()


class TwoNorm(Scene):
    def construct(self):
        cm = {'A': RED, 'A^HA': BLUE, 'Q': BLUE, '\\vy': BLUE}
        title = Title(r"$\lVert A\rVert_2=\sigma_1=\sqrt{\lambda_{\max}(A^HA)}$", color=YELLOW)
        self.add(title)
        self.wait()

        A = VGroup(Tex("A", color=RED), Tex("="), mIntegerMatrix(a)).arrange().next_to(title, DOWN, buff=.5)
        self.play(Write(A))
        self.wait()
        AHA = VGroup(Tex("\Longrightarrow ", "A^TA", "=").tm(cm), mIntegerMatrix(a.T @ a)) \
            .arrange().next_to(A, DOWN).shift(LEFT * .8)
        self.play(Write(AHA))
        self.wait()
        eig = Tex(r"\Longrightarrow\lambda(", r"A^TA", r")=8,~2").tm(cm).next_to(AHA, DOWN, aligned_edge=LEFT)
        self.play(Write(eig))
        self.wait()
        sigma1 = Tex(r"\Longrightarrow\lVert", r" A", r"\rVert_2=\sqrt{\lambda_{\max}}=\sqrt{8}") \
            .tm(cm).next_to(eig, DOWN, aligned_edge=LEFT, buff=.5)
        self.play(Write(sigma1))
        self.wait()
        self.play(FadeOut(VGroup(A, AHA, eig, sigma1)))
        self.wait()

        # proof
        definition = VGroup(Tex("\lVert ", r"A", r"\rVert_2").tm(cm), Tex(r"=", r"\max_{\vx\ne0}{\lVert ", r"A",
                                                                          r"\vx\rVert_2\over\lVert\vx\rVert_2}").tm(
            cm)).arrange() \
            .next_to(title, DOWN, buff=.5).to_edge(LEFT, buff=1)
        proof = VGroup(
            Tex(r"=\max_{\vx\ne0}{\sqrt{\vx^H ", r"A^HA", r"\vx}\over\lVert\vx\rVert_2}")
                .tm(cm).next_to(definition[1], DOWN, aligned_edge=LEFT, buff=1),
            Tex(r"=\max_{\vx\ne0}{\sqrt{\vx", r"^H ", r"Q", r"^H\Lambda ", r"Q", r"\vx}", r"\over",
                r"\lVert\vx\rVert_2}"),
            Tex(r"=\max_{\vx\ne0}{\sqrt{(", r"Q", r"\vx", r")", r"^H\Lambda ", r"(", r"Q", r"\vx", r")}", r"\over",
                r"\lVert\vx\rVert_2}"),
            Tex(r"=\max_{\vx\ne0}{\sqrt{(", r"Q", r"\vx", r")", r"^H\Lambda ", r"(", r"Q", r"\vx", r")}", r"\over",
                r"\lVert Q\vx\rVert_2}"),
            Tex(r"=\max_{\vy\ne0}{\sqrt{\vy", r"^H\Lambda ", r"\vy", r"}", r"\over", r"\lVert ", r"\vy", r"\rVert_2}"),
            Tex(r"=\max_{\vy\ne0}", r"\sqrt{\lambda_1|y_1|^2+\cdots+\lambda_n|y_n|^2\over |y_1|^2+\cdots+|y_n|^2}"),
            Tex(r"\leq\sqrt{\lambda_{\max}}\max_{\vy\ne0}",
                r"\sqrt{|y_1|^2+\cdots+|y_n|^2\over |y_1|^2+\cdots+|y_n|^2}=\sqrt{\lambda_{\max}}"),
        )

        hermitian = VGroup(TexText("Hermitian matrix (埃尔米特矩阵)").scale(.8), Tex("B^H=B")) \
            .arrange(DOWN).set_color(BLUE).next_to(proof[0], buff=1)
        self.play(Write(definition))
        self.wait()
        self.play(Write(proof[0]))
        self.wait()
        self.play(Write(hermitian))
        self.wait()
        self.play(
            VGroup(proof[0], hermitian).animate.shift(UP * (definition.get_y() - proof[0].get_y() + 0.05)),
            FadeOut(definition[1:])
        )
        self.wait()

        proof[1].next_to(proof[0], DOWN, aligned_edge=LEFT, buff=.5)
        proof[1][2:5].set_color(BLUE)
        # self.add(Debug(proof[1]))
        eigenvalue = Tex(r"\lambda_i\geq0", color=BLUE).next_to(proof[1], buff=.5).set_x(hermitian.get_x())
        invariant = Tex(r"\lVert Q\vx\rVert_2=\lVert\vx\rVert_2", color=BLUE).move_to(eigenvalue)
        proof[2].move_to(proof[1]).align_to(proof[1], LEFT)
        VGroup(proof[2][1:3], proof[2][6:8]).set_color(BLUE)
        proof[3].move_to(proof[2]).align_to(proof[2], LEFT)
        VGroup(proof[3][1:3], proof[3][6:8], proof[3][-1][1:3]).set_color(BLUE)
        proof[4].next_to(proof[3], DOWN, aligned_edge=LEFT, buff=.5)
        VGroup(proof[4][0][-1], proof[4][2], proof[4][5]).set_color(BLUE)
        # self.add(Debug(proof[4][0]))
        self.play(Write(proof[1]))
        self.wait()
        self.play(Write(eigenvalue))
        self.wait()
        self.play(FadeTransform(proof[1], proof[2]))
        self.wait()
        self.play(TransformMatchingTex(proof[2], proof[3]), RT(eigenvalue, invariant))
        self.wait()
        self.play(Write(proof[4]))
        self.wait()
        self.play(
            proof[4].animate.move_to(proof[0]).align_to(proof[0], LEFT),
            FadeOut(VGroup(proof[0], proof[3], hermitian, invariant))
        )
        self.wait()
        proof[5].next_to(proof[4], DOWN, aligned_edge=LEFT, buff=.5)
        proof[6].next_to(proof[5], DOWN, aligned_edge=LEFT, buff=.5)
        VGroup(
            proof[5][1][2:4], proof[5][1][14:16],
            proof[6][0][1:7], proof[6][1][34:]
        ).set_color(RED)
        # self.add(Debug(proof[6][1]))
        self.play(Write(proof[5]))
        self.wait()
        self.play(Write(proof[6]))
        self.wait()

        attain = VGroup(Tex("\\lambda_k=\\lambda_{\\max}:"), TexText(r"取 $y_k=1$,"), TexText("其余 $y_i=0$.")) \
            .arrange(DOWN).set_color(BLUE).scale(.8).next_to(proof[5], buff=1)
        self.play(Write(attain[0]))
        self.wait()
        self.play(Write(attain[1:]))
        self.wait()


class OneNorm(Scene):
    def construct(self):
        cm = {'A': RED, '4': YELLOW, '\\vx': BLUE, 'x_': BLUE, '\\va': RED, }
        title = Title(r"$\lVert A\rVert_1=\max_j\sum_i|a_{ij}|$", color=YELLOW)
        self.add(title)
        self.wait()

        A = VGroup(Tex("A", color=RED), Tex("="), mIntegerMatrix(a)).arrange().next_to(title, DOWN, buff=.5)
        self.play(Write(A))
        self.wait()

        boxes = VGroup(
            *[SurroundingRectangle(c, buff=.2).set_color(col) for c, col in zip(A[-1].get_columns(), [YELLOW, BLUE])])
        self.play(ShowCreation(boxes))
        self.wait()

        sums = VGroup(Tex('4').set_color(YELLOW), Tex('2').set_color(BLUE))
        for s, b in zip(sums, boxes):
            s.next_to(b, DOWN)
        self.play(Write(sums))
        self.wait()

        norm = Tex(r"\Longrightarrow", r"\lVert", " A", r"\rVert_1", r"=", "4").tm(cm).next_to(A, DOWN, buff=1.2)
        self.play(Write(norm))
        self.wait()

        self.play(FadeOut(VGroup(A, boxes, sums, norm)))
        self.wait()

        proofs = VGroup(
            VGroup(
                Tex(r"A", r"\vx", r"=", r"[\va_1,\cdots,\va_n]").tm(cm),
                Matrix(np.array(['x_1', r'\vdots', 'x_n'], ndmin=2).T).set_color(BLUE)
            ).arrange().next_to(title, DOWN, buff=.5),
            Tex("=", r"\va_1", "x_1", r"+\cdots+", r"\va_n", "x_n").tm(cm),
            Tex(r"\Longrightarrow", r"\lVert ", r"A", r" \vx", r"\rVert_1", r"\leq", r"|", r"x_1", r"|\cdot\lVert",
                r"\va_1",
                r"\rVert_1+\cdots+|", r"x_n", r"|\cdot\lVert", r"\va_n", r"\rVert_1"),
            Tex(r"\leq", r"\max_j\,\lVert\va_j\rVert_1", r"\cdot", r"\left(", r"|x_1|+\cdots+|x_n|", r"\right)").tm(cm),
            Tex(r"\leq", r"\max_j\,\lVert\va_j\rVert_1", r"\cdot", r"\lVert", r"\vx", r"\rVert_1").tm(cm),
            Tex(r"{\lVert ", r"A", r"\vx", r"\rVert_1\over\lVert", r"\vx", r"\rVert_1}\leq",
                r"\max_j\,\lVert\va_j\rVert_1").tm(cm),
            Tex(r"\Longrightarrow", r"\lVert ", r"A", r"\rVert_1\leq", r"\max_j\,\lVert\va_j\rVert_1").tm(cm)
        )
        proofs[1].next_to(proofs[0][0][2], DOWN, aligned_edge=LEFT, buff=1.5)
        proofs[2].next_to(proofs[1], DOWN, buff=.5).set_x(0).tm(cm)
        proofs[3].next_to(proofs[2][5], DOWN, aligned_edge=LEFT, buff=.5)
        proofs[4].move_to(proofs[3]).align_to(proofs[3], LEFT)
        proofs[5].next_to(title, DOWN, buff=.5)
        proofs[6].next_to(proofs[5], DOWN, buff=.5).shift(LEFT * .2)
        brace = Brace(proofs[6][-1], DOWN)
        brace = VGroup(brace, Tex(r"\lVert\va_k\rVert_1").next_to(brace, DOWN)).set_color(YELLOW)
        x = Tex("\\text{取~}", r"x_k", "=1,~\\text{其余~}", r"x_i", "=0:").tm(cm).next_to(brace, DOWN, buff=.5)
        attain = Tex(r"\lVert ", r"A", r"\vx", r"\rVert_1=", r"\lVert\va_k\rVert_1").tm(cm).next_to(x, DOWN)
        attain[-1].set_color(YELLOW)
        for p in proofs[:4]:
            self.play(Write(p))
            self.wait()
        self.play(TransformMatchingTex(proofs[3], proofs[4]))
        self.wait()
        self.play(FadeOut(proofs[:2]))
        self.play(Write(proofs[5]))
        self.wait()

        self.play(FadeOut(VGroup(proofs[2], proofs[4])))
        self.play(Write(proofs[6]))
        self.wait()

        self.play(GrowFromCenter(brace))
        self.wait()

        self.play(Write(x))
        self.wait()
        self.play(Write(attain))
        self.wait()


class InfNorm(Scene):
    def construct(self):
        cm = {'A': RED, '3': BLUE, '\\vx': BLUE, 'x_': BLUE, '\\va': RED, }
        title = Title(r"$\lVert A\rVert_\infty=\max_i\sum_j|a_{ij}|$", color=YELLOW)
        self.add(title)
        self.wait()

        A = VGroup(Tex("A", color=RED), Tex("="), mIntegerMatrix(a)).arrange().next_to(title, DOWN, buff=.5)
        self.play(Write(A))
        self.wait()

        boxes = VGroup(
            *[SurroundingRectangle(c, buff=.1).set_color(col) for c, col in zip(A[-1].get_rows(), [BLUE, BLUE])])
        boxes[0].set_width(boxes[1].get_width(), stretch=True).align_to(boxes[1], LEFT)
        self.play(ShowCreation(boxes))
        self.wait()

        sums = VGroup(Tex('3').set_color(BLUE), Tex('3').set_color(BLUE))
        for s, b in zip(sums, boxes):
            s.next_to(b, buff=.5)
        self.play(Write(sums))
        self.wait()

        norm = Tex(r"\Longrightarrow", r"\lVert", " A", r"\rVert_\infty", r"=", "3").tm(cm).next_to(A, DOWN, buff=.5)
        self.play(Write(norm))
        self.wait()

        transpose = Tex(r"\lVert A\rVert_\infty=\lVert A^T\rVert_1", color=YELLOW).next_to(norm, DOWN, buff=.5)
        self.play(Write(transpose))
        self.wait()

        self.play(FadeOut(VGroup(A, boxes, sums, norm, transpose)))

        one_label = Tex(r"\lVert A\rVert_", r"1", r":")
        inf_label = Tex(r"\lVert A\rVert_", r"\infty", r":")
        A_one, A_inf = VGroup(Tex("A", color=RED), Tex("="), mIntegerMatrix(a)).arrange(), VGroup(Tex("A", color=RED),
                                                                                                  Tex("="),
                                                                                                  mIntegerMatrix(
                                                                                                      a)).arrange()
        VGroup(one_label, inf_label).arrange(DOWN, aligned_edge=LEFT, buff=2).next_to(ORIGIN, LEFT, buff=1.5)
        A_one.next_to(one_label, buff=1)
        A_inf.next_to(inf_label).align_to(A_one, LEFT)
        boxes1 = VGroup(*[SurroundingRectangle(c) for c in A_one[-1].get_columns()]).set_color(YELLOW)
        boxes_inf = VGroup(*[SurroundingRectangle(r) for r in A_inf[-1].get_rows()]).set_color(BLUE)
        boxes_inf[0].set_width(boxes_inf[1].get_width(), stretch=True).align_to(boxes_inf[1], LEFT)

        box1 = SurroundingRectangle(one_label[-2], color=YELLOW)
        box_inf = SurroundingRectangle(inf_label[-2], color=BLUE)

        arrow1 = Arrow(UP, DOWN).set_color(YELLOW).next_to(A_one, RIGHT, buff=.5)
        arrow2 = Arrow(LEFT, RIGHT).scale(1.5).set_color(BLUE).next_to(A_inf[-1], DOWN, buff=.5)
        self.play(Write(one_label), Write(inf_label))
        self.play(Write(A_one), Write(A_inf))
        self.play(ShowCreation(boxes1), ShowCreation(boxes_inf))
        self.wait()

        self.play(ShowCreation(box1))
        self.wait()
        self.play(GrowArrow(arrow1))
        self.wait()
        self.play(ShowCreation(box_inf))
        self.wait()
        self.play(GrowArrow(arrow2))
        self.wait()


class Tree(Scene):
    def construct(self):
        induced = VGroup(
            TexText("$p$-范数").scale(1.2),
            Tex("\\cdots").scale(1.2)
        ).arrange(DOWN, buff=1, aligned_edge=LEFT).to_corner(UR, buff=3).shift(UP * 1.5)
        brace_induced = Brace(induced, LEFT, buff=.5)
        norms = VGroup(
            TexText("诱导范数").scale(1.2),
            TexText("Frobenius 范数", color=YELLOW).scale(1.2),
            Tex("\\cdots").scale(1.2)
        )
        norms[0].next_to(brace_induced, LEFT, buff=.5)
        norms[1].next_to(norms[0], DOWN, aligned_edge=LEFT, buff=1.5)
        norms[2].next_to(norms[1], DOWN, aligned_edge=LEFT, buff=1.5)
        brace_norm = Brace(norms, LEFT, buff=.5)
        norm_label = TexText("矩阵范数").scale(1.2).next_to(brace_norm, LEFT, buff=.5)
        self.play(Write(norm_label), GrowFromCenter(brace_norm))
        self.play(Write(norms[0]), GrowFromCenter(brace_induced))
        self.play(Write(induced))
        self.wait()
        self.play(Write(norms[1:]))
        self.wait()


class Frobenius(Scene):
    def construct(self):
        cm = {'A': RED, 'a_': RED, 'P': YELLOW, 'Q': YELLOW}
        title = Title("Frobenius norm", color=YELLOW)
        self.add(title)
        self.wait()

        A = VGroup(Tex("A", color=RED), Tex("="), mIntegerMatrix(a)).arrange().next_to(title, DOWN, buff=.5)
        self.play(Write(A))
        self.wait()

        frob = Tex(r"\lVert ", r"A", r"\rVert_F=\sqrt{2^2+1^2+(-2)^2+1^2}=\sqrt{10}").tm(cm).next_to(A, DOWN, buff=.5)
        self.play(Write(frob))
        self.wait()

        induced_i = Tex(r"\lVert I\rVert=",
                        r"\max_{\vx\ne0}{\lVert I\vx\rVert\over\lVert\vx\rVert}=",
                        r"\max_{\vx\ne0}{\lVert \vx\rVert\over\lVert\vx\rVert}=1", color=BLUE) \
            .next_to(frob, DOWN, buff=1)
        frob_i = Tex(r"\lVert I_n\rVert_F=\sqrt{n}", color=YELLOW).next_to(induced_i, DOWN)

        formula = Tex(r"\lVert ", "A", r"\rVert_F=\sqrt{\sum_{i,j}|", r"a_{ij}", r"|^2}",
                      r"=\sqrt{\mathrm{trace\,}(", r"A^HA", r")}").tm(cm).next_to(title, DOWN, buff=.5)
        self.play(Write(induced_i))
        self.wait()
        self.play(Write(frob_i))
        self.wait()

        self.play(FadeOut(VGroup(A, frob)))
        self.play(Write(formula[:5]))
        self.wait()
        self.play(Write(formula[5:]))
        self.wait()

        invariant = VGroup(
            Tex(r"\lVert ", "P ", "A", r" Q", r"\rVert_F=\lVert ", r"A", r" \rVert_F,").tm(cm),
            Tex(r"\lVert ", "P ", "A", r" Q", r"\rVert_2=\lVert ", r"A", r" \rVert_2").tm(cm),
        ).arrange(buff=.5)
        self.play(Write(invariant[0]))
        self.wait()
        self.play(Write(invariant[1]))
        self.wait()


class Consistent(Scene):
    def construct(self):
        cm = {'A': RED, 'B': BLUE, '\\va': RED, '\\vb': BLUE, '\\vx': BLUE, 'M': GOLD}
        title = Title(r"consistent (相容): $\lVert AB\rVert\leq\lVert A\rVert\lVert B\rVert$", color=YELLOW)
        self.add(title)
        self.wait()

        theorem = TexText("Frobenius norm and all induced norms are consistent.").next_to(title, DOWN, buff=.5)
        self.play(Write(theorem))
        self.wait()

        frob = VGroup(
            Tex(r"\lVert ", r"A", r"B", r"\rVert_F^2", r"=", r"\sum_{i,j}|", r"{\va_i}", r"^T", r"\vb_j", r"|^2")
                .next_to(theorem, DOWN, buff=.5).shift(LEFT),
            Tex(r"\leq\sum_{i,j}\lVert", r"\va_i", r"\rVert_2^2\lVert", r"\vb_j", r"\rVert_2^2"),
            Tex(r"=\left(\sum_i\lVert", r"\va_i", r"\rVert_2^2\right)", r"\left(", r"\sum_j\lVert", r"\vb_j",
                r"\rVert_2^2\right)"),
            Tex(r"=\lVert ", "A", r"\rVert_F^2\lVert ", "B", r"\rVert_F^2")
        )
        Frob = Tex(r"\lVert ", r"A", r"B", r"\rVert_F", r"\leq\lVert", " A", r"\rVert_F\lVert ", "B", r"\rVert_F") \
            .tm(cm).next_to(theorem, DOWN, buff=.5)
        frob_2 = Tex(r"\lVert ", "A", r"\vx", r"\rVert_2\leq\lVert ", r"A", r"\rVert_F\lVert", r"\vx", r"\rVert_2") \
            .tm(cm).next_to(Frob, DOWN)
        for f in frob:
            f.tm(cm)
        frob[1].next_to(frob[0], DOWN).align_to(frob[0][4], LEFT)
        frob[2].next_to(frob[1], DOWN, aligned_edge=LEFT)
        frob[3].next_to(frob[2], DOWN, aligned_edge=LEFT)

        self.play(Write(frob[0]))
        self.wait()
        self.play(Write(frob[1:]))
        self.wait()

        self.play(RT(frob, Frob))
        self.wait()

        self.play(Write(frob_2))
        self.wait()

        induced = VGroup(TexText("对诱导范数:").next_to(frob_2, DOWN, buff=1).align_to(theorem, LEFT),
                         Tex(r"\lVert ", "M", r"\vx", r"\rVert\leq\lVert ", r"M", r"\rVert\lVert", r"\vx", r"\rVert")
                         .tm({'M': GOLD}).next_to(frob_2, DOWN, buff=1).set_x(0),
                         TexText(r"($\lVert M\rVert$的定义)", color=YELLOW).scale(.8)
                         )
        induced[2].next_to(induced[1], buff=1)
        self.play(Write(induced[0]))
        self.wait()
        self.play(Write(induced[1]))
        self.play(Write(induced[2]))
        self.wait()

        proofs = VGroup(
            Tex(r"\lVert ", "A", r" B", r"\rVert=\max_{\vx\ne0}{\lVert ", "A", r"(", "B",
                r"\vx)\rVert\over\lVert\vx\rVert}"),
            Tex(r"\leq", r"\lVert ", "A", r"\rVert", r"\max_{\vx\ne0}{", r"\lVert ", "B",
                r"\vx\rVert\over\lVert\vx\rVert}"),
            Tex(r"=\lVert ", "A", r"\rVert\lVert ", "B", r"\rVert")
        ).arrange().next_to(induced, DOWN, buff=.5).set_x(0)
        for p in proofs:
            p.tm({'A': RED, 'B': BLUE})
            self.play(Write(p))
            self.wait()



class NotConsistent(Scene):
    def construct(self):
        cm = {'A': RED, 'B': BLUE, 'a_': RED, '\\vb': BLUE, '\\vx': BLUE, 'M': GOLD}
        title = Title(r"consistent (相容): $\lVert AB\rVert\leq\lVert A\rVert\lVert B\rVert$", color=YELLOW)
        self.add(title)
        self.wait()

        max_norm = Tex(r"\lVert ", "A", r"\rVert_{\max}\coloneqq \max_{i,j}|", "a_{i,j}", "|") \
            .next_to(title, DOWN, buff=.5).tm(cm)
        self.play(Write(max_norm))
        self.wait()

        example = Tex(r"A", "=", "B", r"=\begin{bmatrix}1&1\\1&1\end{bmatrix},~", r"A", "B", "=",
                      r"\begin{bmatrix}2&2\\2&2\end{bmatrix}").next_to(max_norm, DOWN, buff=.5).tm(cm)
        self.play(Write(example))
        self.wait()

        norms = Tex(r"\lVert ", "A", "B", r" \rVert=2,~\lVert ", "A", r"\rVert=\lVert ", "B", r"\rVert=1") \
            .tm(cm).next_to(example, DOWN, buff=.5)
        self.play(Write(norms))
        self.wait()

        note = TexText("\\kaishu 注:某些教材定义范数时要求相容性.", color=YELLOW).next_to(norms, DOWN, buff=1)
        self.play(Write(note))
        self.wait()


class Radius(Scene):
    def construct(self):
        cm = {'A': RED, '\\vx': BLUE, 'X': BLUE, '\\lambda': RED}
        title = Title(r"$\rho(A)\leq\lVert A\rVert$", color=YELLOW)
        self.add(title)
        self.wait()

        radius = Tex(r"\rho(", "A", r")\coloneqq\max|\lambda|").next_to(title, DOWN, buff=.5).tm({'A': RED})
        self.play(Write(radius))
        self.wait()

        proofs = VGroup(
            VGroup(
                Tex(r"A", r"\vx", r"=", r"\lambda", r"\vx", ",").tm(cm),
                Tex(r"\text{考虑~}", r"X","=", r"[", r"\vx", r",", r"\vx", ",", r"\cdots,", r"\vx", r"]:").tm(cm)
            ).arrange(buff=.5).next_to(radius, DOWN, buff=1),
            Tex(r"A","X","=","A","[",r"\vx",r",\cdots,",r"\vx",r"]=[",r"A",r"\vx",r", \cdots, ",r"A",r"\vx",
                r"]=[",r"\lambda",r"\vx",r", \cdots,",r"\lambda",r"\vx",r"]=",r"\lambda ","X").tm(cm),
            Tex(r"|",r"\lambda",r"|\lVert ",r"X",r"\rVert","=",r"\lVert",r"\lambda",r" X",
                r"\rVert=\lVert ",r"A",r"X",r"\rVert",r"\leq\lVert ",r"A",r"\rVert\lVert ",r"X",r"\rVert").tm(cm),
            Tex(r"\Longrightarrow",r"|",r"\lambda",r"|\leq\lVert ",r"A",r"\rVert").tm(cm)
        )
        proofs[1].next_to(proofs[0], DOWN, buff=.5)
        proofs[2].next_to(proofs[1], DOWN, buff=.5)
        proofs[3].next_to(proofs[2], DOWN, buff=.5)
        self.play(Write(proofs[0][0]))
        self.wait()
        self.play(Write(proofs[0][1]))
        self.wait()
        self.play(Write(proofs[1]))
        self.wait()
        self.play(Write(proofs[2][6:13]))
        self.wait()
        self.play(Write(proofs[2][:6]))
        self.wait()
        self.play(Write(proofs[2][13:]))
        self.wait()
        self.play(Write(proofs[3]))
        self.wait()


class Properties(Scene):
    def construct(self):
        cm = {'A': RED, 'vx': BLUE, 'vy': BLUE, 'k': YELLOW}
        properties = VGroup(
            Tex(r"{1\over\sqrt{n}}\lVert A \rVert_\infty\leq\lVert A\rVert_2\leq\sqrt{m}\lVert A\rVert_\infty", isolate=['A']),
            Tex(r"{1\over\sqrt{m}}\lVert A \rVert_1\leq\lVert A\rVert_2\leq\sqrt{n}\lVert A\rVert_1", isolate=['A']),
            Tex(r"\lVert A\rVert_2\leq\lVert A\rVert_F\leq\sqrt{r}\lVert A\rVert_2", isolate=['A']),
            Tex(r"\lVert A\rVert_2\leq\sqrt{\lVert A\rVert_1\lVert A\rVert_\infty}", isolate=['A']),
            Tex(r"\lVert A^HA\rVert_2=\lVert AA^H\rVert_2=\lVert A\rVert_2^2", isolate=['A']),
            Tex(r"\lVert A\rVert_F=\sqrt{\sigma_1^2+\cdots+\sigma_r^2}", isolate=['A']),
            Tex(r"\rho(A)=\lim_{k\to\infty}\lVert A^k\rVert^{1\over k}", isolate=['A', 'k']),
            Tex(r"\lVert\vx\vy^H\rVert_F=\lVert\vx\vy^H\rVert_2=\lVert\vx\rVert_2\lVert\vy\rVert_2", isolate=['A', '\\vx', '\\vy']),
        )
        for p in properties:
            p.tm(cm).scale(.9)
        properties.arrange(DOWN)
        self.add(properties)
        self.wait()


class Pic(Scene):
    def construct(self):
        norm = Tex(r"\lVert A\rVert").scale(9)
        self.add(norm)
