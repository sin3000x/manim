#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author: Jeremy
@file:svd.py
@time:2021/07/28
"""
from manimlib.imports import *


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
        t1 = PI/4
        u = np.array(
            [[np.cos(t1), -np.sin(t1)],
             [np.sin(t1), np.cos(t1)]]
        )
        title = VGroup(
            TextMobject("Rotation:", color=YELLOW).add_background_rectangle(),
            Matrix([["\\cos\\theta", "-\\sin\\theta"], ["\\sin\\theta", "\\cos\\theta"]], h_buff=1.5).add_background_rectangle()
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
        self.apply_inverse(u)



class TransformationDecomposition(LinearTransformationScene):
    CONFIG = {
        "show_basis_vectors": False,
        "foreground_plane_kwargs": {
            "x_range": np.array([-16.0, 16.0, 1.0]),
            "y_range": np.array([-10.0, 10.0, 1.0]),
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


class test(LinearTransformationScene):
    def construct(self):
        t1, t2 = PI / 4, PI / 4
        u = np.array(
            [[np.cos(t1), -np.sin(t1)],
             [np.sin(t1), np.cos(t1)]]
        )
        v = np.array(
            [[-np.cos(t2), np.sin(t2)],
             [np.sin(t2), np.cos(t2)]]
        )
        self.apply_matrix(u)
        self.wait()
        self.apply_matrix(v)
        self.wait()
