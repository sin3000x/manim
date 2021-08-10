#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author: Jeremy
@file:svd.py
@time:2021/07/28
"""
import os.path
import pickle

import numpy as np

from manimlib.imports import *


class Opening(Scene):
    def construct(self):
        real = TexMobject("\\text{We assume }","A\\in\\R^{m\\times n}",".").scale(1.5).set_color_by_tex('A', YELLOW)
        complex = TexMobject("\\text{For }","A\\in\\C^{m\\times n}","\\colon","A^T\\to A^H=\\overline{A^T}.").scale(1.5)
        complex[1].set_color(YELLOW)
        VGroup(real, complex).arrange(DOWN, buff=1.5)
        self.play(Write(real))
        self.wait()
        self.play(Write(complex[0:3]))
        self.wait()
        self.play(Write(complex[3:]))
        self.wait()

class Compare(Scene):
    def construct(self):
        line = Line(UP * FRAME_Y_RADIUS, DOWN * FRAME_Y_RADIUS, color=YELLOW)
        self.add(line)
        self.wait(10)


class Rotation(LinearTransformationScene):
    CONFIG = {
        "show_basis_vectors": True,
        "foreground_plane_kwargs": {
            # "x_range": np.array([-16.0, 16.0, 1.0]),
            # "y_range": np.array([-10.0, 10.0, 1.0]),
            "x_max": 16,
            "x_min": -16,
            "y_max": 10,
            "y_min": -10,
            "faded_line_ratio": 0
        },
    }

    def construct(self):
        t1 = PI / 4
        u = np.array(
            [[np.cos(t1), -np.sin(t1)],
             [np.sin(t1), np.cos(t1)]]
        )
        title = VGroup(
            TextMobject("Rotation:", color=YELLOW, stroke_width=2).add_background_rectangle(),
            Matrix([["\\cos\\theta", "-\\sin\\theta"], ["\\sin\\theta", "\\cos\\theta"]],
                   h_buff=1.8).add_background_rectangle()
        ).arrange(buff=.5).to_edge(UP)
        for ele in title[1].get_entries()[:4]:
            ele[0][-1].set_color(YELLOW)

        # vectors = VGroup(self.add_vector([1,0]), self.add_vector([0, 1]))
        # for i, c in zip(vectors, [GREEN, RED]):
        #     i.set_color(c)
        # vectors.add_updater(lambda x: self.add(x))
        # self.add(vectors)
        self.play(Write(title))

        # self.play(
        #     self.plane.apply_matrix, u,
        #     vectors.apply_matrix, u,
        #     run_time=3
        # )
        self.apply_matrix(u)
        self.wait()
        # self.apply_inverse(u)

        arc = Arc(angle=t1, color=YELLOW, radius=0.5)  # .add_tip(tip_length=0.1)
        theta = TexMobject("\\theta", color=YELLOW).add_background_rectangle().next_to(arc)
        self.play(GrowArrow(arc), Write(theta))
        self.wait()


class Scaling(LinearTransformationScene):
    CONFIG = {
        "show_basis_vectors": True,
        "foreground_plane_kwargs": {
            # "x_range": np.array([-16.0, 16.0, 1.0]),
            # "y_range": np.array([-10.0, 10.0, 1.0]),
            "x_max": 16,
            "x_min": -16,
            "y_max": 12,
            "y_min": -12,
            "faded_line_ratio": 0
        },
    }

    def construct(self):
        a = np.diag([2, 0.5])
        title = VGroup(
            TextMobject("Scaling:", color=YELLOW, stroke_width=2).add_background_rectangle(),
            Matrix([["2", "0"], ["0", "0.5"]], h_buff=1).set_column_colors(X_COLOR, Y_COLOR).add_background_rectangle()
        ).arrange(buff=.3).to_edge(UP)

        self.play(Write(title))
        self.apply_matrix(a)
        self.wait()

        stretch = TextMobject("stretch", "/", "compress", " along the axes...", stroke_width=2) \
            .tm({'stretch': YELLOW, 'compress': YELLOW}).to_edge(BOTTOM).add_background_rectangle()
        self.play(Write(stretch))
        self.wait()


class TransformationDecomposition(LinearTransformationScene):
    CONFIG = {
        "show_basis_vectors": False,
        "include_background_plane": False,
        "foreground_plane_kwargs": {
            # "x_range": np.array([-16.0, 16.0, 1.0]),
            # "y_range": np.array([-10.0, 10.0, 1.0]),
            "x_max": 16,
            "x_min": -16,
            "y_max": 10,
            "y_min": -10,
            "faded_line_ratio": 0
        },
    }

    def construct(self):
        t1, t2 = PI / 4, PI / 2
        u = np.array(
            [[np.cos(t1), -np.sin(t1)],
             [np.sin(t1), np.cos(t1)]]
        )
        v = np.array(
            [[np.cos(t2), -np.sin(t2)],
             [np.sin(t2), np.cos(t2)]]
        )
        d = np.diag([0.8, 0.5])
        a = u.dot(d).dot(v.T)
        # dots = VGroup(*[Dot(i, color=c) for i,c in zip([LEFT, UP, RIGHT, DOWN], [BLUE_A, BLUE_B, BLUE_C, BLUE_D])])
        pic = SVGMobject("pi.svg", color=YELLOW).scale(2)
        self.add(pic)
        self.wait()
        self.add_transformable_mobject(pic)
        self.apply_matrix(a)
        self.wait()
        self.apply_inverse(a, run_time=.2)
        self.wait()

        for matrix in [v.T, d, u]:
            self.apply_matrix(matrix)


class Orthogonal(LinearTransformationScene):
    CONFIG = {
        "show_basis_vectors": True,
        "foreground_plane_kwargs": {
            # "x_range": np.array([-16.0, 16.0, 1.0]),
            # "y_range": np.array([-10.0, 10.0, 1.0]),
            "x_max": 16,
            "x_min": -16,
            "y_max": 10,
            "y_min": -10,
            "faded_line_ratio": 0
        },
    }

    def construct(self):
        t1 = PI / 4
        u = np.array(
            [[-np.cos(t1), np.sin(t1)],
             [np.sin(t1), np.cos(t1)]]
        )
        # title = VGroup(
        #     TextMobject("Rotation:", color=YELLOW, stroke_width=2).add_background_rectangle(),
        #     Matrix([["\\cos\\theta", "-\\sin\\theta"], ["\\sin\\theta", "\\cos\\theta"]], h_buff=1.8).add_background_rectangle()
        # ).arrange(buff=.5).to_edge(UP)
        # for ele in title[1].get_entries()[:4]:
        #     ele[0][-1].set_color(YELLOW)
        #
        # self.play(Write(title))

        self.apply_matrix(u)
        self.wait()


class Definition(Scene):
    def construct(self):
        # np.set_printoptions(precision=3)
        a = np.array([[1, 0, 1], [0, 1, 0], [0, 0, 1]])
        u, s, v = np.linalg.svd(a)
        u = np.round(u, 2)
        s = np.round(s, 2)
        v = np.round(v, 2)
        v = v.T
        v[0, 1] = 0

        A = Matrix(a, h_buff=.8).set_color(YELLOW)
        S = Matrix([['1.62', '', ''], ['', '1.00', ''], ['', '', '0.62']], h_buff=1).set_color(YELLOW)
        U = Matrix(u, h_buff=1.2).set_color(RED)
        V = Matrix(v, h_buff=1.2).set_color(GREEN)
        for mat in [A, S, U, V]:
            mat.scale(0.8)

        v = VGroup(A, TexMobject("="), U, S, V).arrange().to_edge(UP, buff=1.5)
        v.add(TexMobject("^T", color=V.get_color()).move_to(v[-1].get_corner(UR)).shift(RIGHT * .2))
        self.play(Write(v))
        self.wait()

        labels = A_label, U_label, S_label, V_label = [TexMobject(i) for i in ["A", "U", "\\Sigma", "V^T"]]
        for label, c, mat in zip(labels, [YELLOW, RED, YELLOW, GREEN], [A, U, S, V]):
            label.scale(2).set_color(c)
            label.next_to(mat, DOWN, buff=.7)
        for label in labels[1:]:
            label.align_to(A_label, DOWN)

        labels = VGroup(A_label, TexMobject("=").next_to(A_label, RIGHT).align_to(v[1], LEFT), U_label, S_label,
                        V_label)
        self.play(Write(labels))
        self.wait()

        ortho1 = Brace(U_label, DOWN)
        ortho1 = VGroup(ortho1, TextMobject("orthogonal").next_to(ortho1, DOWN))
        ortho2 = Brace(V_label[0][0], DOWN)
        ortho2 = VGroup(ortho2, TextMobject("orthogonal").next_to(ortho2, DOWN))

        def1 = TexMobject("UU^T=U^TU=I", color=RED).next_to(ortho1, DOWN)
        def2 = TexMobject("VV^T=V^TV=I", color=GREEN).next_to(ortho2, DOWN)
        self.play(GrowFromCenter(ortho1))
        self.play(GrowFromCenter(ortho2))
        self.wait()
        self.play(Write(def1), Write(def2))
        self.wait()

        arrows = VGroup(*[Line(ORIGIN, DOWN * 0.3).add_tip(tip_length=.2) for _ in range(3)])
        for arrow, i in zip(arrows, [0, 4, 8]):
            arrow.next_to(S.get_entries()[i], UP, buff=.1)
        self.play(LaggedStartMap(GrowArrow, arrows, lag_ratio=.3))
        singular = TextMobject("singular values").next_to(S, UP, buff=.5)
        self.play(Write(singular))
        self.wait()

        self.play(FadeOut(
            VGroup(ortho1, ortho2, def1, def2)
        ))
        svd = TextMobject("Singular", " Value", " Decomposition", stroke_width=3).scale(1.5).to_edge(DOWN, buff=1.5)
        for i in svd:
            self.add(i)
            self.wait(.5)


def get_svd(a, u, s, v, A_buff=.8, S_buff=1, U_buff=1.2, V_buff=1.2, scale_factor=0.8):
    A = Matrix(a, h_buff=A_buff).set_color(YELLOW)
    S = Matrix(s, h_buff=S_buff).set_color(YELLOW)
    U = Matrix(u, h_buff=U_buff).set_color(RED)
    V = Matrix(v, h_buff=V_buff).set_color(GREEN)
    for mat in [A, S, U, V]:
        mat.scale(scale_factor)

    v = VGroup(A, TexMobject("="), U, S, V).arrange()
    V.add(TexMobject("^T", color=V.get_color()).move_to(v[-1].get_corner(UR)).shift(RIGHT * .2))
    return v


class Rectangular(Scene):
    def construct(self):
        a = np.array([[1, 0], [1, 1], [0, 1]])
        u, s_, v = np.linalg.svd(a)
        s = np.zeros_like(a, dtype=np.float)
        s[[0, 1], [0, 1]] = s_
        v = v.T

        u = np.round(u, 2)
        s = np.round(s, 2)
        v = np.round(v, 2)

        v1 = get_svd(a, u, [['1.73', ''], ['', '1.00'], ['0', '0']], v, U_buff=1.5, V_buff=1.5).to_edge(TOP, buff=.3)
        v1[3].get_entries()[4:6].fade(.6)

        a = np.array([[1, 0, 1], [1, 1, 0]])
        u, s_, v = np.linalg.svd(a)
        s = np.zeros_like(a, dtype=np.float)
        s[[0, 1], [0, 1]] = s_
        v = v.T

        u = np.round(u, 2)
        s = np.round(s, 2)
        v = np.round(v, 2)
        v2 = get_svd(a, u, [['1.73', '', '0'], ['', '1.00', '0']], v, U_buff=1.5, V_buff=1.5).to_edge(BOTTOM, buff=.3)
        VGroup(v2[3].get_entries()[2], v2[3].get_entries()[5]).fade(.6)
        columns = VGroup(Brace(v1[0], LEFT), Brace(v2[0], LEFT)).set_color(RED)
        rows = VGroup(Brace(v1[0], UP), Brace(v2[0], UP)).set_color(GREEN)

        shapes = VGroup(
            *[TexMobject(i, stroke_width=2) for i in ['m\\times n', 'm\\times m', 'm\\times n', 'n\\times n']]) \
            .next_to(v1, DOWN, buff=.5)
        for shape, color, mat in zip(shapes, [YELLOW, RED, YELLOW, GREEN], [v1[0], v1[2], v1[3], v1[4]]):
            shape.set_color(color).set_x(mat.get_x())

        self.play(Write(v1[:2]), Write(v2[:2]))
        self.play(Write(shapes[0]))
        self.wait()
        self.play(Write(v1[3]), Write(v2[3]))
        self.play(Write(shapes[2]))
        self.wait()
        self.play(
            Write(v1[2]),
            GrowFromCenter(columns[0], run_time=3),
            Write(v2[2]),
            GrowFromCenter(columns[1], run_time=3),
        )
        self.play(Write(shapes[1]))
        self.wait()
        self.play(
            Write(v1[4]),
            GrowFromCenter(rows[0], run_time=3),
            Write(v2[4]),
            GrowFromCenter(rows[1], run_time=3),
        )
        self.play(Write(shapes[3]))
        self.wait()
        # self.play(Write(shapes))
        # self.wait()


class RankDeficient(LinearTransformationScene):
    CONFIG = {
        "show_basis_vectors": False,
        "include_background_plane": False,
        "foreground_plane_kwargs": {
            # "x_range": np.array([-16.0, 16.0, 1.0]),
            # "y_range": np.array([-10.0, 10.0, 1.0]),
            "x_max": 18,
            "x_min": -18,
            "y_max": 14,
            "y_min": -14,
            "faded_line_ratio": 0
        },
    }

    def construct(self):
        t1, t2 = PI / 4, PI / 2
        u = np.array(
            [[np.cos(t1), -np.sin(t1)],
             [np.sin(t1), np.cos(t1)]]
        )
        v = np.array(
            [[np.cos(t2), -np.sin(t2)],
             [np.sin(t2), np.cos(t2)]]
        )
        d = np.diag([1.0, 0.0001])
        a = u.dot(d).dot(v.T)
        # dots = VGroup(*[Dot(i, color=c) for i,c in zip([LEFT, UP, RIGHT, DOWN], [BLUE_A, BLUE_B, BLUE_C, BLUE_D])])
        pic = SVGMobject("pi.svg", color=YELLOW).scale(2)
        self.add(pic)
        self.wait()
        self.add_transformable_mobject(pic)
        self.plane.save_state()
        pic.save_state()
        self.apply_matrix(a)
        self.wait()
        self.plane.restore()
        pic.restore()

        self.wait()

        for matrix in [v.T, d, u]:
            self.apply_matrix(matrix)


def get_s(a, s, A_buff=.8, S_buff=1, scale_factor=0.8):
    A = Matrix(a, h_buff=A_buff).set_color(YELLOW)
    S = Matrix(s, h_buff=S_buff).set_color(YELLOW)
    U = TexMobject("U").set_color(RED)
    V = TexMobject("V^T").set_color(GREEN)
    for mat in [A, S]:
        mat.scale(scale_factor)

    v = VGroup(A, TexMobject("="), U, S, V).arrange()
    return v


class SingularValuesRank(Scene):
    def construct(self):
        title = Title("More on Singular Values...", stroke_width=2)
        self.add(title)
        self.wait()

        a1 = np.array([[1, 1, 0], [0, 1, 0], [0, 0, 1]])
        a2 = np.ones_like(a1, dtype=int)
        v1 = VGroup(
            TexMobject("\\text{rank}=", "2", ":").set_color_by_tex('2', BLUE),
            get_s(a1, np.diag(['2', '1', '0']))
        ).arrange(buff=.5).next_to(title, DOWN)
        arrows1 = VGroup(
            *[Line(ORIGIN, UP * 0.4).add_tip(tip_length=0.2).next_to(v1[1][-2].get_entries()[i], DOWN, buff=.1)
              for _, i in zip(range(2), [0, 4])]
        ).set_color(BLUE)
        v2 = VGroup(
            TexMobject("\\text{rank}=", "1", ":").set_color_by_tex('1', BLUE),
            get_s(a2, np.diag(['3', '0', '0']))
        ).arrange(buff=.5).next_to(v1, DOWN, buff=.5)
        arrows2 = Line(ORIGIN, UP * 0.4).add_tip(tip_length=0.2) \
            .next_to(v2[1][-2].get_entries()[0], DOWN, buff=.1).set_color(BLUE)
        self.play(Write(v1))
        self.wait()

        self.play(Write(v2))
        self.wait()

        self.play(LaggedStartMap(GrowArrow, arrows1, lag_ratio=.2))
        self.wait()
        self.play(GrowArrow(arrows2))
        self.wait()

        braces = VGroup(Brace(v2[1][0], DOWN), Brace(v2[1][-2], DOWN)).set_color(BLUE)
        self.play(GrowFromCenter(braces[0]))
        self.play(GrowFromCenter(braces[1]))
        same_rank = TextMobject("should have the same rank", color=BLUE).next_to(braces, DOWN)
        self.play(Write(same_rank))
        self.wait()

        self.play(FadeOut(braces), FadeOut(same_rank))
        self.wait()

        conclusions = VGroup(
            TexMobject(r"\operatorname{rank}(A)+\operatorname{dim}(\operatorname{null}(A))=n"),
            TexMobject(r"\operatorname{rank}(A)=\operatorname{rank}(A^TA)=\operatorname{rank}(AA^T)"),
        ).arrange(DOWN).to_edge(DOWN).set_color(BLUE)
        self.play(Write(conclusions))
        self.wait()


class SingularValuesNorm(Scene):
    def construct(self):
        title = Title("More on Singular Values...", stroke_width=2)
        self.add(title)
        self.wait()

        decomp = VGroup(
            TexMobject("A", "=", "U").tm({'A': YELLOW, 'U': RED}),
            Matrix(np.diag(['\\sigma_1', '\\sigma_2', '\\ddots', '\\sigma_n'])).set_color(YELLOW),
            TexMobject("V^T", color=GREEN)
        ).arrange().next_to(title, DOWN)
        self.play(Write(decomp))
        self.wait()

        norms = VGroup(
            TexMobject(r"\lVert ", "A", r" \rVert_2=", r"\sigma_1").tm({'A': YELLOW, 'sigma': YELLOW}),
            TexMobject(r"\lVert", r" A", r" \rVert_F=", r"\sqrt{\sigma_1^2+\sigma_2^2+\cdots+\sigma_n^2}").tm(
                {'A': YELLOW, 'sigma': YELLOW})
        ).arrange(DOWN, aligned_edge=LEFT).to_edge(DOWN, buff=1)
        self.play(Write(norms))


class Expansion(Scene):
    def construct(self):
        m = {'A': YELLOW, 'U': RED, 'u': RED, 'Sigma': YELLOW, 'V': GREEN, 'v': GREEN, '^T': GREEN, 'sigma': YELLOW}
        origin = TexMobject("A", "=", "U~", "\\Sigma", "~V", "^T").tm(m)
        columns = TexMobject("=", "[u_1, u_2, \\cdots, u_m]~", "\\Sigma", "~[v_1, v_2, \\cdots, v_n]", "^T").tm(m)
        origin.to_edge(UP).to_edge(LEFT, buff=1)
        columns.next_to(origin[1], DOWN, aligned_edge=LEFT, buff=.5)
        transposed = VGroup(
            TexMobject("="),
            columns[1].copy(),
            Matrix(np.diag(['\\sigma_1', '\\ddots', '\\sigma_r', '0', '\\ddots', '0']), h_buff=.8, v_buff=.6).set_color(
                YELLOW),
            Matrix(np.array(['v_1^T', 'v_2^T', '\\vdots', 'v_n^T']), bracket_h_buff=.1, v_buff=1).set_color(GREEN)
        ).arrange().next_to(columns, DOWN, aligned_edge=LEFT)
        # transposed[-1].add(TexMobject("^T", color=GREEN).move_to(transposed[-1].get_corner(UR)+RIGHT*.2))
        self.play(Write(origin))
        self.wait()
        self.play(Write(columns[0]))
        anims = AnimationGroup(
            *[RT(origin[i].copy(), columns[i - 1]) for i in range(2, 6)],
            lag_ratio=.8,
            run_time=3
        )
        self.play(
            anims,
        )
        self.wait()

        anims = AnimationGroup(
            *[RT(columns[i].copy(), transposed[i]) for i in range(4)],
            lag_ratio=.8,
            run_time=4
        )
        self.play(anims)
        self.wait()

        arrow = Line(ORIGIN, UP * 0.4).add_tip(tip_length=.2).next_to(transposed[-2].get_entries()[14], DOWN)
        self.play(GrowArrow(arrow))
        self.wait()

        expansion = TexMobject(r"=", r"\sigma_1", r"u_1", r"v_1^T", r"+", r"\cdots+", r"\sigma_r", r"u_r", r"v_r^T") \
            .tm(m).next_to(transposed, DOWN, aligned_edge=LEFT)
        self.play(Write(expansion))
        self.wait()


class ExpansionExample(Scene):
    def construct(self):
        # a = np.arange(1, 10).reshape(3, 3)
        a = np.array([[1, 0, 1], [0, 1, 0], [0, 0, 1]])
        u_, s_, v_ = np.linalg.svd(a)
        v_ = v_.T
        u = np.round(u_, 2)
        s = np.round(s_, 2)
        s = np.diag(s).astype(object)
        s[s == 0] = ''
        v = np.round(v_, 2)
        v[0, 1] = 0
        u_columns = [u[:, i] for i in range(a.shape[0])]
        v_columns = [v[:, i] for i in range(a.shape[1])]
        U_columns = [Matrix(col, bracket_h_buff=.1).scale(.8).set_color(RED) for col in u_columns]
        V_columns = [Matrix(col, bracket_h_buff=.1).scale(.8).set_color(GREEN) for col in v_columns]
        for col in V_columns:
            col.add(TexMobject("^T", color=GREEN).move_to(col.get_corner(UR) + RIGHT * .2))
        svd = get_svd(a, u, s, v).to_edge(UP, buff=.2)
        U, S, V = svd[-3], svd[-2], svd[-1]
        diag = [svd[-2].get_entries()[i] for i in [0, 4, 8]]
        self.play(Write(svd))
        self.wait()

        # claim part
        expansion = VGroup(
            TexMobject("="),
        )
        for i in range(3):
            expansion.add(
                diag[i].copy(),
                U_columns[i],
                V_columns[i],
                TexMobject("+")
            )
        expansion.remove(expansion[-1])
        expansion.arrange(buff=.1).next_to(svd[1], DOWN, aligned_edge=LEFT, buff=1.5)
        expansion[4:8].shift(LEFT * .3)
        expansion[8:].shift(LEFT * .6)

        # animate part
        def transform_matrix_to_column(mat, col, col_num, transpose=False):
            mat_col = mat.get_columns()[col_num]
            if transpose:
                return AnimationGroup(
                    RT(mat_col.copy(), col.get_entries()),
                    Write(VGroup(col.get_brackets(), col[-1])),
                    lag_ratio=.4,
                    run_time=2
                )
            return AnimationGroup(
                RT(mat_col.copy(), col.get_entries()),
                Write(col.get_brackets()),
                lag_ratio=.4,
                run_time=2
            )

        def animate_a_term(num, diag_index):
            return AnimationGroup(
                RT(diag[num].copy(), expansion[diag_index]),
                transform_matrix_to_column(U, U_columns[num], num),
                transform_matrix_to_column(V, V_columns[num], num, True),
                lag_ratio=.8
            )

        # for i, n in enumerate([])
        self.play(Write(expansion[0]))
        self.play(animate_a_term(0, 1))
        self.play(Write(expansion[4]))
        self.play(animate_a_term(1, 5))
        self.play(Write(expansion[8]))
        self.play(animate_a_term(2, 9))
        self.wait()

        braces = VGroup(*[Brace(VGroup(expansion[i], expansion[i + 1][:-1]), DOWN) for i in [2, 6, 10]])
        self.play(LaggedStartMap(GrowFromCenter, braces, lag_ratio=.2))
        self.wait()
        outer_product = TextMobject("outer product").next_to(braces[0], DOWN)
        self.play(Write(outer_product))
        self.wait()

        arrows = VGroup(
            *[Line(ORIGIN, UP * .6).add_tip(tip_length=0.2).next_to(expansion[i], DOWN, buff=.5) for i in [1, 5, 9]])
        importance = VGroup(
            TextMobject("most\\\\important"),
            TextMobject("important"),
            TextMobject("less\\\\important")
        )
        for i, a in zip(importance, arrows):
            i.next_to(a, DOWN, buff=.4)
        importance[1].set_y(importance[0].get_y())
        self.play(FadeOut(braces), FadeOut(outer_product), LaggedStartMap(GrowArrow, arrows, lag_ratio=.2))
        self.play(Write(importance))
        self.wait()

        self.play(FadeOut(arrows), FadeOut(importance))
        self.wait()

        approx = [
            s_[0] * np.outer(u_[:, 0], v_[:, 0]),
            s_[0] * np.outer(u_[:, 0], v_[:, 0]) + s_[1] * np.outer(u_[:, 1], v_[:, 1]),
            s_[0] * np.outer(u_[:, 0], v_[:, 0]) + s_[1] * np.outer(u_[:, 1], v_[:, 1]) + s_[2] * np.outer(u_[:, 2],
                                                                                                           v_[:, 2])
        ]
        # for i in range(len(approx)):
        #     approx[i] = np.round(approx[i], 2)

        Approx = VGroup(
            *[
                VGroup(
                    DecimalMatrix(mat, element_to_mobject_config= {"num_decimal_places": 2})
                        .scale(.8).set_color(YELLOW),
                    TexMobject(":~", "\\text{rank}=%d" % (i + 1)).set_color_by_tex(':', YELLOW)
                ).arrange()
                for i, mat in enumerate(approx)
            ]
        ).to_edge(DOWN)

        braces = VGroup(
            Brace(VGroup(expansion[1:3], expansion[3][:-1])),
            Brace(VGroup(expansion[1], expansion[7][:-1])),
            Brace(VGroup(expansion[1], expansion[11][:-1])),
        )  # .set_color(YELLOW)
        for app, bra in zip(Approx, braces):
            # app.next_to(bra, DOWN)
            bra.save_state()

        self.play(GrowFromCenter(braces[0]))
        self.play(Write(Approx[0]))
        self.wait()

        def change_dec_matrix(mat1, mat2):
            braces1 = mat1.get_brackets()
            braces2 = mat2.get_brackets()
            return AnimationGroup(
                *[ChangeDecimalToValue(ele1, ele2.number) for (ele1, ele2) in zip(mat1.get_entries(), mat2.get_entries())],
                # *[ApplyMethod(ele1.move_to, ele2) for (ele1, ele2) in zip(mat1.get_entries(), mat2.get_entries())],
                Transform(braces1, braces2)
            )
        # first_approx = Approx[0][0]
        # first_approx.generate_target()
        for i in range(1, 3):
            self.play(
                RT(braces[i - 1], braces[i]),
                change_dec_matrix(Approx[0][0], Approx[i][0]),
                RT(Approx[i - 1][1], Approx[i][1]),
                run_time=2)
            self.wait()
        self.play(FadeOut(Approx[-1][1]), FadeOut(braces[-1]), FadeOut(Approx[0][0]))
        for bra in braces:
            bra.restore()
        self.play(GrowFromCenter(braces[0]))
        for i in range(1, 3):
            self.play(RT(braces[i - 1], braces[i]), run_time=1)
            self.wait()


class InnerOuter(Scene):
    def construct(self):
        inner_label = TextMobject("inner product:", stroke_width=2).to_corner(UL).shift(DOWN * .4)
        self.play(Write(inner_label))
        self.wait()

        a, b, c = np.array([1, 2]), np.array([3, 4]), np.array([3, 4, 5])
        ac = np.outer(a, c)
        A_row = Matrix(a.reshape(-1, 1).T, h_buff=1).set_color(X_COLOR)
        A_col = Matrix(a).set_color(X_COLOR)
        B = Matrix(b).set_color(Y_COLOR)
        C = Matrix(c.reshape(-1, 1).T, h_buff=.8).set_color(Y_COLOR)
        AC = Matrix(ac, h_buff=1).set_color_by_gradient([X_COLOR, Y_COLOR])

        inner = VGroup(
            A_row, B, TexMobject("="),
            TexMobject("1", "\\times", "3", "+", "2", "\\times", "4").tm({
                '1': X_COLOR,
                '2': X_COLOR,
                '3': Y_COLOR,
                '4': Y_COLOR
            }),
            TexMobject("="), TexMobject(str(a.dot(b))).set_color_by_gradient([X_COLOR, Y_COLOR])
        ).arrange().next_to(inner_label, DOWN, buff=.3).set_x(0)
        self.play(Write(inner[:3]))
        self.wait()
        self.play(
            AnimationGroup(
                RT(A_row.get_entries()[0].copy(), inner[3][0], path_arc=-PI),
                Write(inner[3][1]),
                RT(B.get_entries()[0].copy(), inner[3][2], path_arc=-PI),
                lag_ratio=.1,
                run_time=2
            )
        )
        self.play(Write(inner[3][3]))
        self.play(
            AnimationGroup(
                RT(A_row.get_entries()[1].copy(), inner[3][4], path_arc=PI),
                Write(inner[3][5]),
                RT(B.get_entries()[1].copy(), inner[3][6], path_arc=PI),
                lag_ratio=0.1,
                run_time=2
            )
        )
        self.play(Write(inner[4:]))
        self.wait()

        outer_label = TextMobject("outer product:", stroke_width=2) \
            .next_to(inner, DOWN, buff=.5).align_to(inner_label, LEFT)
        self.play(Write(outer_label))
        self.wait()

        temp = np.zeros_like(ac).astype(object)
        for i in range(len(a)):
            for j in range(len(c)):
                temp[i, j] = TexMobject(f"{a[i]}", "\\cdot ", f"{c[j]}").tm(
                    {
                        '1': X_COLOR, '2': X_COLOR, '3': Y_COLOR, '4': Y_COLOR, '5': Y_COLOR
                    }
                )
        temp = Matrix(temp, element_to_mobject=lambda x: x)
        temp.get_brackets()[0].set_color(X_COLOR)
        temp.get_brackets()[1].set_color(Y_COLOR)

        outer = VGroup(
            A_col, C, TexMobject("="),
            temp,
            TexMobject("="),
            AC
        ).arrange().next_to(outer_label, DOWN, buff=.5).set_x(0)

        def animate_row(A_ele, B_row, temp_row):
            return AnimationGroup(
                *[RT(A_ele.copy(), temp_row[i][0]) for i in range(3)],
                *[Write(temp_row[i][1]) for i in range(3)],
                *[RT(B_row[i].copy(), temp_row[i][2]) for i in range(3)]
            )

        self.play(Write(outer[:3]))
        self.wait()
        self.play(
            animate_row(A_col.get_entries()[0], C.get_rows()[0], temp.get_rows()[0]),
            Write(temp.get_brackets()),
            run_time=2
        )
        self.play(animate_row(A_col.get_entries()[1], C.get_rows()[0], temp.get_rows()[1]), run_time=2)
        self.wait()

        self.play(Write(outer[4:]))
        self.wait()

        brace = Brace(outer[-1], DOWN, color=YELLOW)
        brace = VGroup(brace, TexMobject("\\text{rank}=1", color=brace.get_color()).next_to(brace, DOWN))
        self.play(GrowFromCenter(brace))
        self.wait()


class LowRankApprox(Scene):
    def construct(self):
        m = {
            'A': YELLOW, 'sigma': YELLOW,
            'u': RED,
            'v': GREEN,
            'sum': WHITE,
            'X': BLUE,
            'solution': WHITE
        }
        Ak = VGroup(
            TexMobject("A_k", "=", "\\sum_{i=1}^k", "\\sigma_i", "u_i", "v_i^T").tm(m),
            TextMobject("has rank $k$", "~$(k<r)$,"),
        ).arrange().to_edge(UP)
        self.play(Write(Ak[0]))
        self.wait()
        self.play(Write(Ak[1][0]))
        self.wait()
        self.play(Write(Ak[1][1]))
        self.wait()

        nearest = TextMobject(r"and it's the", r" ``nearest''", r" matrix to $A$ in rank $k$.") \
            .set_color_by_tex('near', YELLOW).next_to(Ak, DOWN)
        self.play(Write(nearest))
        self.wait()

        line = Line(color=BLUE).set_width(FRAME_WIDTH).next_to(nearest, DOWN, buff=.5)
        self.play(ShowCreation(line))
        self.wait()

        prob = VGroup(
            TexMobject(r"\underset{X}{\operatorname{minimize}}~", r"\lVert ", r"A", r"-", r"X", r"\rVert_2") \
                .tm({'X': BLUE, 'underset': WHITE}),
            TexMobject("\\text{subject to }", "\\text{rank}(", r"X", r")=k").set_color_by_tex('X', BLUE)
        ).arrange(DOWN).next_to(line, DOWN, buff=.5)

        prob[0][0][8].set_color(BLUE)
        self.play(Write(prob[0]))
        self.wait()
        self.play(Write(prob[1]))
        self.wait()

        sol = TexMobject("\\Longrightarrow~", "X", "=", "A_k", "\\text{~ is a solution.}").tm(m).next_to(prob, DOWN,
                                                                                                         buff=.5)
        self.play(Write(sol))
        self.wait()

        frobenius = VGroup(
            Arrow(ORIGIN, LEFT).set_color(YELLOW).next_to(prob[0], RIGHT).shift(UP * .1),
        )
        frobenius.add(TexMobject("\\lVert A-X \\rVert_F", color=YELLOW).next_to(frobenius))
        self.play(Indicate(prob[0][1:]))
        self.wait()

        self.play(GrowArrow(frobenius[0]))
        self.play(Write(frobenius[1]))
        self.wait()

        name = TextMobject("low-rank approximation", color=YELLOW, stroke_width=2).scale(1.2).to_edge(DOWN, buff=.7)
        box = SurroundingRectangle(name, buff=.2)
        self.play(Write(name), )
        self.play(ShowCreation(box))
        self.wait()


def figure_and_numbers(array, height=6, direction=RIGHT):
    array[array>1] = 1
    array[array<0] = 0
    fig = ImageMobject(layer_to_image_array(array.flatten()))
    figure = PixelsAsSquares(fig).set_height(height).next_to(ORIGIN, direction)

    numbers = VGroup()
    for square in figure:
        rgb = square.fill_rgb
        num = DecimalNumber(
            square.fill_rgb[0],
            num_decimal_places=1
        )
        num.set_stroke(width=1)
        color = rgba_to_color(1 - (rgb + 0.2) / 1.2)
        num.set_color(color)
        num.set_width(0.7 * square.get_width())
        num.move_to(square)
        numbers.add(num)

    return VGroup(figure, numbers)

def get_figure(array, height=5):
    array[array > 1] = 1
    array[array < 0] = 0
    fig = ImageMobject(layer_to_image_array(array.flatten()))
    figure = PixelsAsSquares(fig).set_height(height)
    return figure

class Visualize(Scene):

    def construct(self):
        with open(os.path.join(os.getcwd(), "jeremy/ref/train.data"), 'rb') as f:
            data = pickle.load(f)
        array = data[12] / 255
        origin = figure_and_numbers(array, direction=LEFT)
        title1 = TexMobject("\\text{rank}=20").next_to(origin, UP)

        self.play(Write(origin[0]))
        self.play(Write(origin[1]))
        self.wait()
        self.play(Write(title1))

        u, s, v = np.linalg.svd(array)
        ranks = range(1, 11)

        def get_approx(rank):
            res = np.zeros([28, 28])
            for i in range(rank):
                res += s[i] * np.outer(u[:, i], v[i, :])
            # print(res)
            return res

        images = VGroup()
        sigmas = VGroup()
        ranks_label = VGroup()
        for rank in ranks:
            images.add(figure_and_numbers(get_approx(rank)))
            sigmas.add(TexMobject(f"\\sigma_{{{rank}}}={round(s[rank-1], 2)}", color=YELLOW))
            ranks_label.add(TexMobject("\\text{rank}=%d" % rank))

        sigmas.next_to(images, DOWN)
        ranks_label.next_to(images, UP)

        self.play(Write(images[0][0]))
        self.play(Write(images[0][1]))
        self.play(Write(ranks_label[0]))
        self.play(Write(sigmas[0]))
        self.wait()

        for i in range(1, len(ranks)):
            self.play(
                RT(images[i-1], images[i]),
                RT(ranks_label[i-1], ranks_label[i]),
                RT(sigmas[i-1], sigmas[i]),
                run_time=2
            )
            self.wait()


class Calc(Scene):
    def construct(self):
        m = {
            'A': YELLOW,
            'U': RED,
            'V': GREEN,
            'Sigma': YELLOW,
        }
        title = Title("The Calculation of SVD", stroke_width=2)
        self.add(title)
        self.wait()

        A_and_AT = VGroup(
            TexMobject("A","=","U","\\Sigma"," V^T", ",").tm(m),
            TexMobject("A^T", "=", "V", "\\Sigma^T", "U^T").tm(m)
        ).arrange(buff=.5, aligned_edge=UP).next_to(title, DOWN, buff=.5)
        # A_and_AT[1].align_to(A_and_AT)

        A_AT = TexMobject("AA^T", "=", "U", "\\Sigma^2", "U^T","=", "U", "\\Sigma^2", "U^{-1}").tm(m)
        AT_A = TexMobject("A^TA", "=", "V", "\\Sigma^2", "V^T","=", "V", "\\Sigma^2", "V^{-1}").tm(m)

        VGroup(A_AT, AT_A).arrange(DOWN).next_to(A_and_AT, DOWN, buff=.5, aligned_edge=LEFT)
        implies = TexMobject("\\Longrightarrow", color=BLUE).next_to(A_AT, LEFT, buff=.3)

        for i in A_and_AT:
            self.play(Write(i))
            self.wait()
        self.play(Write(implies))
        self.wait()
        self.play(Write(A_AT))
        self.wait()
        self.play(Write(AT_A))
        self.wait()
        self.play(VGroup(
            A_and_AT, A_AT[1:5], AT_A[1:5]
        ).fade, .5)
        self.wait()

        results = VGroup(
            TexMobject("\\sigma_i", "=", "\\sqrt{\\text{eigenvalues of $AA^T$ or $A^TA$}}").set_color_by_tex('sigma', YELLOW),
            TexMobject("u_i", "=", "\\text{orthonormal eigenvectors of $AA^T$}").set_color_by_tex('u_i', RED),
            TexMobject("v_i", "=", "\\text{orthonormal eigenvectors of $A^TA$}").set_color_by_tex('v_i', GREEN),
        ).arrange(DOWN, aligned_edge=LEFT).next_to(AT_A, DOWN, buff=.8, aligned_edge=LEFT)
        VGroup(
            results[0][-1][-8:-5],results[0][-1][-3:], results[1][-1][-3:], results[2][-1][-3:]
        ).set_color(YELLOW)

        implies2 = implies.copy().next_to(results[0], LEFT).align_to(implies, LEFT)
        self.play(ShowCreation(implies2))
        for i in results:
            self.play(Write(i))
            self.wait()


class Ending(Scene):
    def construct(self):
        thanks = TextMobject("Thanks for watching!").scale(2.5)
        self.play(Write(thanks))
        self.wait()


class Pic(Scene):
    # def construct(self):
    #     width=2
    #     svd = VGroup(
    #         TextMobject("Singular", stroke_width=width),
    #         TextMobject("Value", stroke_width=width),
    #         TextMobject("Decomposition", stroke_width=width),
    #     )
    #     for i in svd:
    #         i[0][0].set_color(YELLOW)
    #         i.scale(3)
    #     svd.arrange(DOWN, aligned_edge=LEFT, buff=.5)
    #     svd[1].shift(LEFT*.2)
    #     svd[2].shift(LEFT*.1+DOWN*.1)
    #     self.add(svd)
    def construct(self):
        with open(os.path.join(os.getcwd(), "jeremy/ref/train.data"), 'rb') as f:
            data = pickle.load(f)
        array = data[12] / 255
        origin = get_figure(array)


        u, s, v = np.linalg.svd(array)
        rank = 4

        def get_approx(rank):
            res = np.zeros([28, 28])
            for i in range(rank):
                res += s[i] * np.outer(u[:, i], v[i, :])
            return res

        approx = get_figure(get_approx(rank))
        VGroup(origin, approx).arrange(buff=2).shift(DOWN*.4)
        title1 = TexMobject("\\text{rank}=20").scale(1.5).next_to(origin, UP).shift(DL*.5+UP*.3)
        title2 = TexMobject("\\text{rank}=4").scale(1.5).next_to(approx, UP).shift(DL*.5+UP*.3)
        arrow = Arrow(origin.get_right(), approx.get_left(), buff=-1).set_color(YELLOW)
        svd = TextMobject("SVD", color=YELLOW).scale(1.5).next_to(arrow, UP)
        self.add(origin, approx, title1, title2, arrow, svd)