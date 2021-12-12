#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author: Jeremy
@file:norm_vec.py
@time:2021/12/12
"""
from manimlib import *

class Opening(Scene):
    def construct(self):
        coord = NumberPlane()
        coord.add_coordinate_labels()
        vector = (4,3)
        vec = coord.get_vector(vector).set_color(RED)
        brace = Brace(coord.get_vector((5,0)), ORIGIN, color=YELLOW)\
            .rotate(angle_of_vector(vector)).align_to(vec, LEFT).shift(UP*1.5+LEFT*.1)
        vec_label = Tex(r"\vx=\begin{bmatrix}4\\3\end{bmatrix}", color=RED,)\
            .next_to(vec.get_end()).add_background_rectangle()


        mod = Tex(r"|\vx|=5", color=YELLOW, isolate='=')\
            .add_background_rectangle().rotate(angle_of_vector(vector)).move_to(brace).shift(UL*.5)
        two_norm = Tex(r"\lVert\vx\rVert_2", color=YELLOW)\
            .add_background_rectangle().rotate(angle_of_vector(vector)).move_to(mod)
        self.add(coord)
        self.wait()
        self.play(GrowArrow(vec))
        self.play(Write(vec_label))
        self.wait()
        self.play(GrowFromCenter(brace))
        self.play(Write(mod))
        self.wait()
        self.play(FadeTransform(mod, two_norm))


class Generalize(Scene):
    def construct(self):
        concept = Text("概念").scale(1.5)
        properties = Text("必要性质").scale(1.5)
        generalization = Text("推广的概念").scale(1.5)
        VGroup(concept, properties, generalization).arrange(buff=2)
        arrows = VGroup(
            Arrow(concept.get_right(), properties.get_left()),
            Arrow(properties.get_right(), generalization.get_left())
        )
        extract = Text("提取", color=YELLOW).next_to(arrows[0], UP)
        definition = Text("定义", color=YELLOW).next_to(arrows[1], UP)
        self.play(Write(concept))
        self.wait()
        self.play(GrowArrow(arrows[0]), Write(extract))
        self.play(Write(properties))
        self.wait()
        self.play(GrowArrow(arrows[1]), Write(definition))
        self.play(Write(generalization))
        self.wait()


class Norms(Scene):
    def construct(self):
        pass