#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author: Jeremy
@file:svd.py
@time:2021/07/28
"""
from manimlib import *


class TransformationDecomposition(LinearTransformationScene):
    def construct(self):
        self.wait()
        a = np.array([[1, 0], [1, 2]])
        plane = NumberPlane()
        self.add(plane)
        self.apply_matrix(a)
        # plane.apply_matrix(a)