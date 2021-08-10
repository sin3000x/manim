# from @cigar666

"""
注：
    1. 主要用来求解两圆和多圆相交的交集部分的示意（如果是空集会出问题）
    2. Intersection_n_circle是没有基于前两个类的，其实就用它也就行了
    3. 可以用来做一些类似文氏图之类的，其他凸区域的交集可使用类似的方法写出来（如果谁有兴趣可以写一下）
"""

from manimlib import *


def Range(in_val, end_val, step=1):
    return list(np.arange(in_val, end_val + step, step))


class GetIntersections:
    def get_coord_from_proportion(self, vmob, proportion):
        return vmob.point_from_proportion(proportion)

    def get_points_from_curve(self, vmob, dx=0.005):
        coords = []
        for point in Range(0, 1, dx):
            dot = Dot(self.get_coord_from_proportion(vmob, point))
            coords.append(dot.get_center())
        return coords

    def get_intersections_between_two_vmobs(self, vmob1, vmob2,
                                            tolerance=0.05,
                                            radius_error=0.2,
                                            use_average=True,
                                            use_first_vmob_reference=False):
        coords_1 = self.get_points_from_curve(vmob1)
        coords_2 = self.get_points_from_curve(vmob2)
        intersections = []
        for coord_1 in coords_1:
            for coord_2 in coords_2:
                distance_between_points = get_norm(coord_1 - coord_2)
                if use_average:
                    coord_3 = (coord_2 - coord_1) / 2
                    average_point = coord_1 + coord_3
                else:
                    if use_first_vmob_reference:
                        average_point = coord_1
                    else:
                        average_point = coord_2
                if len(intersections) > 0 and distance_between_points < tolerance:
                    last_intersection = intersections[-1]
                    distance_between_previus_point = get_norm(average_point - last_intersection)
                    if distance_between_previus_point > radius_error:
                        intersections.append(average_point)
                if len(intersections) == 0 and distance_between_points < tolerance:
                    intersections.append(average_point)
        return intersections


class Irregular_shape(VMobject):

    def __init__(self, *curves, **kwargs):
        VMobject.__init__(self, **kwargs)
        vertices = []
        for curve in curves:
            vertices += list(curve)

        self.set_points_as_corners(
            [*vertices, vertices[0]]
        )


class Intersection_ThinRectCircle(Irregular_shape):
    """
    the shape is like a meatball pinned by a vertical stick
    """

    def __init__(self, rect, circle, num=360, **kwargs):
        left, right = rect.get_edges()[1].get_x(), rect.get_edges()[3].get_x()
        up, down = rect.get_edges()[0].get_y(), rect.get_edges()[2].get_y()

        r = circle.get_height()/2
        o = circle.get_center()

        left_side = rect.get_edges()[1]
        right_side = rect.get_edges()[3]

        left_side_points = np.array([np.ones(num)*left_side.get_x(),np.linspace(left_side.get_bottom()[1], left_side.get_top()[1], num), np.zeros(num)]).T
        right_side_points = np.array([np.ones(num)*right_side.get_x(),np.linspace(right_side.get_bottom()[1], right_side.get_top()[1], num), np.zeros(num)]).T

        def p_in_rect(p):
            return (left <= p[0] <= right) and (down <= p[1] <= up)

        def p_in_circle(p, circle_o, circle_r):
            return sum((p - circle_o) ** 2) <= circle_r ** 2

        t1 = np.linspace(0, np.pi, num)
        t2 = np.linspace(np.pi, 2 * np.pi, num)
        tarc, barc, lside, rside = [], [], [], []
        for i in range(len(t1)):
            p_on_circle = np.array([np.cos(t1[i]), np.sin(t1[i]), 0]) * r + o
            if p_in_rect(p_on_circle):
                tarc.append(p_on_circle)

        for i in range(len(t2)):
            p_on_circle = np.array([np.cos(t2[i]), np.sin(t2[i]), 0]) * r + o
            if p_in_rect(p_on_circle):
                barc.append(p_on_circle)

        for p in left_side_points:
            if p_in_circle(p, o, r):
                lside.append(p)

        for p in right_side_points:
            if p_in_circle(p, o, r):
                rside.append(p)

        Irregular_shape.__init__(self, tarc, lside, barc, reversed(rside), **kwargs)





class Intersection_2circle(Irregular_shape):

    def __init__(self, Mcircle_1, Mcircle_2, num=360, **kwargs):
        def p_in_circle(p, circle_o, circle_r):
            return (sum((p - circle_o) ** 2) <= circle_r ** 2)

        r1, r2 = Mcircle_1.get_height() / 2, Mcircle_2.get_height() / 2
        o1, o2 = Mcircle_1.get_center(), Mcircle_2.get_center()
        arc1, arc2 = [], []
        t = np.linspace(0, 2 * np.pi, num)
        # for p in [np.array([np.cos(t[i]), np.sin(t[i]), 0]) * r1 + o1 for i in range(len(t))]:
        #     if p_in_circle(p, o2, r2):
        #         arc1.append(p)
        # for p in [np.array([np.cos(t[i]), np.sin(t[i]), 0]) * r2 + o2 for i in range(len(t))]:
        #     if p_in_circle(p, o1, r1):
        #         arc2.append(p)
        for i in range(len(t)):
            p1 = np.array([np.cos(t[i]), np.sin(t[i]), 0]) * r1 + o1
            if p_in_circle(p1, o2, r2):
                arc1.append(p1)
            p2 = np.array([np.cos(t[i]), np.sin(t[i]), 0]) * r2 + o2
            if p_in_circle(p2, o1, r1):
                arc1.append(p2)
        Irregular_shape.__init__(self, arc1, arc2, **kwargs)


class Union_2circle(Irregular_shape):

    def __init__(self, Mcircle_1, Mcircle_2, num=360, **kwargs):
        def p_in_circle(p, circle_o, circle_r):
            return (sum((p - circle_o) ** 2) <= circle_r ** 2)

        r1, r2 = Mcircle_1.get_height() / 2, Mcircle_2.get_height() / 2
        o1, o2 = Mcircle_1.get_center(), Mcircle_2.get_center()
        arc1, arc2 = [], []
        t = np.linspace(0, 2 * np.pi, num)
        # for p in [np.array([np.cos(t[i]), np.sin(t[i]), 0]) * r1 + o1 for i in range(len(t))]:
        #     if p_in_circle(p, o2, r2):
        #         arc1.append(p)
        # for p in [np.array([np.cos(t[i]), np.sin(t[i]), 0]) * r2 + o2 for i in range(len(t))]:
        #     if p_in_circle(p, o1, r1):
        #         arc2.append(p)
        for i in range(len(t)):
            p1 = np.array([np.cos(t[i]), np.sin(t[i]), 0]) * r1 + o1
            if not p_in_circle(p1, o2, r2):
                arc1.append(p1)
            p2 = np.array([np.cos(t[i]), np.sin(t[i]), 0]) * r2 + o2
            if not p_in_circle(p2, o1, r1):
                arc1.append(p2)
        Irregular_shape.__init__(self, arc1, arc2, **kwargs)


class Intersection_n_circle(VMobject):

    def __init__(self, *Mcircle, num=360, **kwargs):

        def p_in_circle(p, circle_o, circle_r):
            return (sum((p - circle_o) ** 2) <= circle_r ** 2)

        r_list = [c.get_height() / 2 for c in Mcircle]
        o_list = [c.get_center() for c in Mcircle]
        arc_list = [[] for c in Mcircle]

        t = np.linspace(0, 2 * np.pi, num)
        for i in range(len(t)):
            for j in range(len(arc_list)):
                p = np.array([np.cos(t[i]), np.sin(t[i]), 0]) * r_list[j] + o_list[j]
                p_in = True
                for k in range(len(arc_list)):
                    p_in = p_in and p_in_circle(p, o_list[k], r_list[k])
                if p_in:
                    arc_list[j].append(p)

        vertices = []
        for arc in arc_list:
            vertices += arc

        VMobject.__init__(self, **kwargs)

        n_v = len(vertices)
        v_arr = np.array(vertices)
        center = sum(v_arr) / n_v
        angle = []

        def get_angle(vector):
            if vector[1] >= 0:
                return np.arccos(vector[0] / np.sqrt(sum(vector ** 2)))
            else:
                return 2 * np.pi - np.arccos(vector[0] / np.sqrt(sum(vector ** 2)))

        for v in vertices:
            angle_i = get_angle(v - center)
            angle.append(angle_i)
        order = np.argsort(np.array(angle))

        vertices_in_order = list(np.zeros((n_v, 3)))
        for i in range(n_v):
            vertices_in_order[i] = vertices[order[i]]

        self.set_points_as_corners(
            [*vertices_in_order, vertices_in_order[0]]
        )


## some tests ##
class Test_2cirlces(Scene):

    def construct(self):
        circle_1 = Circle().scale(2).shift(LEFT * 1.5)
        circle_2 = Circle().scale(1.5).shift(RIGHT * 1 + DOWN * 1.2)

        intersection = Intersection_2circle(circle_1, circle_2, color=YELLOW, fill_color=YELLOW)

        self.play(ShowCreation(circle_1))
        self.play(ShowCreation(circle_2))
        self.wait()
        self.play(ShowCreation(intersection), run_time=2)
        self.wait(0.5)
        self.play(ApplyMethod(intersection.set_opacity, 0.8))
        self.wait(2)
        self.play(FadeOut(intersection))
        self.wait(0.5)

        circle_3 = Circle().scale(1.8).shift(UP * 1. + LEFT * 0.4)
        intersection_3c = Intersection_n_circle(circle_1, circle_2, circle_3, color=YELLOW, fill_color=YELLOW)
        self.play(ShowCreation(circle_3))
        self.wait()
        self.play(ShowCreation(intersection_3c), run_time=2)
        self.wait()
        self.play(ApplyMethod(intersection_3c.set_opacity, 1))
        self.wait(4)


class N_circles(Scene):

    def construct(self):
        circles = VGroup()

        circles.add(Circle(radius=2).shift(LEFT * 2))
        circles.add(Circle(radius=1.5).shift(LEFT * 1))
        circles.add(Circle(radius=2).shift(UP * 1.8 + RIGHT * 0.5))
        circles.add(Circle(radius=3).shift(RIGHT * 2 + DOWN * 0.5))
        circles.add(Circle(radius=2).shift(DOWN * 1))
        circles.add(Circle(radius=2.4).shift(LEFT * 1.2 + UP * 2.4))

        for i in range(len(circles)):
            self.play(ShowCreation(circles[i]), run_time=1)
            self.wait(0.5)
        intersection = Intersection_n_circle(*circles, color=YELLOW)
        self.wait(0.5)
        self.play(ShowCreation(intersection), run_time=2)
        self.wait()
        self.play(ApplyMethod(intersection.set_opacity, 0.8))
        self.wait(4)


class Four_circles(Scene):

    def construct(self):
        circle_1 = Circle(radius=2).shift(UP + LEFT)
        circle_2 = Circle(radius=2).shift(-UP + LEFT)
        circle_3 = Circle(radius=2).shift(UP - LEFT)
        circle_4 = Circle(radius=2).shift(-UP - LEFT)

        intersection_1234 = Intersection_n_circle(circle_1, circle_2, circle_3, circle_4,
                                                  color=YELLOW, fill_opacity=0.6, fill_color=YELLOW)

        intersection_14 = Intersection_n_circle(circle_1, circle_4, color=YELLOW, fill_opacity=0.6, fill_color=YELLOW)

        self.add(circle_1, circle_2, circle_3, circle_4)
        self.wait()
        self.play(ShowCreation(intersection_14))
        self.wait()
        self.play(ReplacementTransform(intersection_14, intersection_1234))

        self.wait(2)
