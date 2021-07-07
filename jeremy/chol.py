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


class CompleteSquare(Scene):
    def construct(self):
        title = Title("\\heiti{1. 傻fufu地配方}", color=YELLOW)
        self.add(title)
        self.wait()

        definition = Tex(r"x^T","A",r"x>0,~\forall x\in\R^n\quad(x\neq0)").next_to(title, DOWN)
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
        positive = Tex(">","0")
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
        eigens = VGroup(A, Tex("\\text{的特征值：}", "2,~2+\\sqrt2,~2-\\sqrt2")).arrange(buff=.3).next_to(title, DOWN, buff=.3)
        self.play(Write(eigens), run_time=3)
        self.wait()

        proof = VGroup(
            TexText("$A$","正定：").set_color_by_tex('A', RED),
            TexText("取$x$为特征向量，则"),
            Tex("x^T","A","x=x^T(\\lambda x)","=\\lambda ", "x^Tx",">0").set_color_by_tex('A', RED)
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
            Tex("\\quad x^T","A","x", "=x^T","Q^T\\Lambda Q","x").set_color_by_tex_to_color_map({"A": RED, "Q": RED}),
            Tex("=(","Qx",")^T","\\Lambda","(Qx)"),
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