#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author: Jeremy
@file:frechet.py
@time:2021/09/14
"""
from manimlib import *

CM = {'x': RED, 'a': RED, 'h': BLUE, 'right': WHITE, '|': BLUE, 'left': WHITE}
ONED_POS = [2.55252092, 2.04724764, 0.]


class Introduction(Scene):
    def construct(self):
        # one-variable
        cubed = lambda t: t ** 3
        cube = Tex("f(x)=x^3", isolate=['x'], color=YELLOW).scale(1.2).to_edge(UP)
        self.play(Write(cube))
        self.wait()

        # draw a graph
        axes = Axes(
            x_range=[-0.5, 2, 0.5],
            y_range=[-1, 4],
            height=6,
            width=7,
            # num_sampled_graph_points_per_tick=50,
        ).next_to(cube, DOWN).to_edge(LEFT, buff=0.2)
        graph = axes.get_graph(lambda t: t ** 3, x_range=[-0.5, 1.5], use_smoothing=False, color=YELLOW)
        self.play(Write(axes, lag_ratio=.01))
        self.play(ShowCreation(graph))
        self.wait()

        # the original limit
        oned_limit = Tex(r"f'(a)", "=", r"\lim_{h\to0}", "{f(a+h)-f(a)\over h}", isolate=list('ah')) \
            .tm(CM).next_to(cube, DOWN).to_edge(RIGHT, buff=1.5)
        limit_continue = VGroup(
            Tex(r"=\lim_{h\to0}", "{(a+h)^3-a^3\over h}", isolate=['a', 'h']).tm(CM),
            Tex(r"=\lim_{h\to0}", "{3a^2h+3ah^2+h^3\over h}", isolate=['a', 'h']).tm(CM),
            Tex(r"=\lim_{h\to0}", "(3a^2+3ah+h^2)", isolate=['a', 'h']).tm(CM),
            Tex(r"=3a^2", isolate=['a', 'h']).tm(CM),
        ).arrange(DOWN, aligned_edge=LEFT).next_to(oned_limit, DOWN).align_to(oned_limit[3], LEFT)
        self.play(Write(oned_limit[4:]))
        self.wait()

        # animating on the graph
        a = 0.5
        h = ValueTracker(0.9)
        dot_a = Dot(
            axes.c2p(a, cubed(a)),
            color=CM['a'])
        a_label = Tex(r"\left(a, f(a)\right)", isolate=['a']).tm(CM).next_to(dot_a, UP).shift(LEFT * .3)

        dot_h = Dot(
            axes.c2p(a + h.get_value(), cubed(a + h.get_value())),
            color=CM['a'])
        self.play(FadeIn(dot_a, scale=.5), FadeIn(a_label, shift=DOWN))
        self.play(FadeIn(dot_h, scale=.5))
        dot_h.add_updater(lambda t: t.become(Dot(
            axes.c2p(a + h.get_value(), cubed(a + h.get_value())),
            color=CM['a'])))
        line = always_redraw(self.get_secant, dot_a, dot_h)
        self.play(ShowCreation(line))
        self.wait()

        vert1 = DashedLine(dot_a, axes.c2p(a, 0))
        vert2 = DashedLine(dot_h, axes.c2p(a + h.get_value(), 0))
        h_label = Tex("h", color=BLUE).next_to(axes.c2p(mid(a, a + h.get_value()), 0), DOWN)
        self.play(ShowCreation(vert1), ShowCreation(vert2))
        self.play(Write(h_label))

        h_label.add_updater(lambda t: t.next_to(axes.c2p(mid(a, a + h.get_value()), 0), DOWN))
        vert2.add_updater(lambda t: t.become(DashedLine(dot_h, axes.c2p(a + h.get_value(), 0))))

        self.play(h.set_value, .01, run_time=5)
        self.wait()

        # calculate the limit
        self.play(Write(limit_continue), run_time=4)
        self.wait()
        self.play(Write(oned_limit[:4]))
        self.wait()

        # ONED_POS = oned_limit.get_center()
        # print(ONED_POS)
        # generalize
        self.play(FadeOut(limit_continue))
        limits = VGroup(
            Tex(r"f'(a)", "=", r"\lim_{h\to0}", "{f(a+h)-f(a)\over h}").move_to(oned_limit),
            Tex(r"0", "=", r"\lim_{h\to0}", "{f(a+h)-f(a)\over h}", "-f'(a)"),
            Tex(r"0", "=", r"\lim_{h\to0}", "{f(a+h)-f(a)\over h}", "-{f'(a)h\over h}", isolate=list('ah')).tm(CM),
            Tex(r"0", "=", r"\lim_{h\to0}", "{f(a+h)-f(a)-f'(a)h\over h}", isolate=list('ah')).tm(CM)
        )
        VGroup(limits[0][0][-2], limits[0][3][2], limits[0][3][9]).set_color(RED)
        VGroup(limits[1][-1][-2], limits[1][-2][2], limits[1][-2][9]).set_color(RED)
        VGroup(limits[0][2][-3], limits[0][3][4], limits[0][3][12]).set_color(BLUE)
        VGroup(limits[1][2][-3], limits[1][3][4], limits[1][3][12]).set_color(BLUE)

        # self.add(Debug(limits[0][3]))
        for l in limits[1:]:
            l.next_to(limits[0], DOWN)
        # self.add(Debug(limits[2]))
        self.play(TransformMatchingTex(limits[0], limits[1], path_arc=PI / 2))
        self.wait()
        self.play(
            TransformMatchingShapes(limits[1][:-1], limits[2][:13]),
            TransformMatchingShapes(limits[1][-1], limits[2][13:]),
        )
        self.wait()
        self.play(FadeTransform(limits[2], limits[3]))
        # limit_zero = Tex(r"0", "=", r"\lim_{h\to0}", "{f(a+h)-f(a)-f'(a)h\over h}", isolate=list('ah'))\
        #     .tm(CM).next_to(oned_limit, DOWN)
        # self.play(Write(limit_zero))
        self.wait()

        drop_limit = Tex(r"f(a+h)-f(a)-f'(a)h=o(h)", isolate=['a', 'h']).tm(CM).next_to(limits, DOWN)
        final = Tex(r"f(a+h)-f(a)=f'(a)h+o(h)", isolate=['a', 'h', '=', 'o']).tm(CM).next_to(drop_limit, DOWN)

        self.play(
            TransformMatchingShapes(limits[-1][5:15].copy(), drop_limit[:10]),
            TransformMatchingShapes(limits[-1][16].copy(), drop_limit[10:]),
        )
        self.wait()
        self.play(FadeTransform(drop_limit.copy(), final))
        self.wait()

        self.play(FadeOut(VGroup(oned_limit, limits[-1], drop_limit)))
        self.play(final.shift, UP * 3)
        self.play(h.set_value, .8)
        self.wait()

        # linear part
        arrow1 = Arrow(ORIGIN, DOWN).set_color(BLUE).next_to(line.get_center(), UP, buff=.3) \
            .set_x(axes.c2p(a + h.get_value() / 2)[0])
        arrow2 = f_always(Arrow(ORIGIN, UP).set_color(YELLOW).move_to,
                          lambda: axes.c2p(a + h.get_value() / 2, cubed(a + h.get_value() / 2) - .5))
        h_label.clear_updaters()
        self.play(GrowArrow(arrow1), GrowArrow(arrow2), FadeOut(h_label), FadeOut(a_label))
        self.wait()
        arrow1.add_updater(
            lambda t: t.next_to(line.get_center(), UP, buff=.3).set_x(axes.c2p(a + h.get_value() / 2)[0]))

        self.play(h.set_value, .1, run_time=3)
        self.wait()

        # interpret
        factor = .8
        brace1 = Brace(final[:7], DOWN)
        brace1 = VGroup(brace1, TexText("函数增量").scale(factor).next_to(brace1, DOWN))
        brace2 = Brace(final[8:12], DOWN)
        brace2 = VGroup(brace2, TexText(r"线性\\函数").scale(factor).next_to(brace2, DOWN))
        brace3 = Brace(final[13:], DOWN)
        brace3 = VGroup(brace3, TexText(r"高阶\\无穷小").scale(factor).next_to(brace3, DOWN))
        for b in [brace1, brace2, brace3]:
            self.play(GrowFromCenter(b))
            self.wait()
        # self.add(Debug(final))

        arrow3 = Arrow(ORIGIN, DOWN).next_to(final[8:11], UP).set_color(YELLOW)
        self.play(GrowArrow(arrow3))
        self.wait()

        # higher dimension
        vector = Tex(r"f(\va+\vh)-f(\va)=L(\vh)+o(|\vh|)", isolate=[r'\va', r'\vh', '=', 'o', '|', '+']) \
            .tm(CM).next_to(final, DOWN, buff=2)
        self.play(Write(vector))
        self.wait()
        # self.add(Debug(vector))

        # h->0
        brace_ovh = Brace(vector[12:], DOWN)
        h_to_0 = Tex("\\vh\\to\\vnull", isolate=['\\vh']).tm(CM).next_to(brace_ovh, DOWN)
        h_len_to_0 = Tex("|\\vh|\\to0", isolate=['|']).tm(CM).next_to(h_to_0, DOWN)
        self.play(GrowFromCenter(brace_ovh))
        self.wait()
        self.play(Write(h_to_0))
        self.wait()
        self.play(Write(h_len_to_0))
        self.wait()

        # linear part
        brace_L = Brace(vector[8:11], DOWN)
        linear_prop = VGroup(
            Tex(r"L(\va+\vb)=L(\va)+L(\vb)\\", color=YELLOW).scale(.8),
            Tex(r"L(\lambda\va)=\lambda L(\va)", color=YELLOW).scale(.8)
        ).arrange(DOWN).next_to(brace_L, DOWN)
        self.play(FadeOut(VGroup(brace_ovh, h_to_0, h_len_to_0)))
        self.play(GrowFromCenter(brace_L))
        self.wait()
        self.play(Write(linear_prop[0]))
        self.play(Write(linear_prop[1]))
        self.wait()

        note = TexText(r"注: $L(\vnull)=0$.").scale(.8).next_to(linear_prop, DOWN)
        self.play(Write(note))
        self.wait()

        # well-defined
        well_def = TexText("全微分").scale(.8).next_to(brace_L, DOWN)
        self.play(RT(VGroup(linear_prop, note), well_def))
        self.wait()

    @staticmethod
    def get_secant(dota, dotb, length=5):
        line = Line(dota, dotb, color=CM['h'])
        line.set_length(length)
        return line


class NaiveWay(Scene):
    def construct(self):
        oned_limit = Tex(r"f'(a)", "=", r"\lim_{h\to0}", "{f(a+h)-f(a)\over h}", isolate=list('ah0')) \
            .tm(CM).move_to(ONED_POS)
        # oned_limit.save_state()
        self.add(oned_limit)
        self.wait()
        oned_limit.generate_target()
        oned_limit.target.scale(1.5).set_x(0).to_edge(UP, buff=1)
        self.play(MoveToTarget(oned_limit))
        self.wait()

        ex = Tex(r"f\left(\begin{bmatrix}x\\y\end{bmatrix}\right)=x^2y",
                 r"\text{~在~}", r"\va=\begin{bmatrix}1\\2\end{bmatrix}", r"?").tm({'x^2y': YELLOW, 'va': RED}) \
            .scale(1.2).next_to(oned_limit, DOWN, buff=1)
        self.play(Write(ex))
        self.wait()

        nd_limit = Tex(r"f'(\va)", "=", r"\lim_{\vh\to\vnull}", r"{f(\va+\vh)-f(\va)\over \vh}", isolate=['\\va', '\\vh', '\\vnull']) \
            .tm(CM).scale(1.5).move_to(oned_limit)
        self.play(TransformMatchingTex(oned_limit, nd_limit, key_map={'a': '\\va', 'h': '\\vh', '0': '\\vnull'}), run_time=1)
        self.wait()

        cr = Cross(nd_limit)
        self.play(ShowCreation(cr))
        self.wait()

        self.play(Uncreate(cr), FadeOut(ex))
        self.wait()


class TwoD(Scene):
    CONFIG = {
        "camera_class": ThreeDCamera,
    }
    def construct(self):
        axes = ThreeDAxes(
            x_range=[-5, 5],
            y_range=[-5, 5],
            z_range=[-2, 6]
        ).shift(IN*2)

        surface = ParametricSurface(
            lambda x, y: [x, y, x**2+y**2],
            u_range=[-3, 3],
            v_range=[-3,3],
            color=YELLOW,
            opacity=0.7,
        ).shift(IN*2)
        surface.mesh = SurfaceMesh(surface, resolution=(30, 30))
        surface.mesh.set_stroke(WHITE, 1, opacity=0.5)
        frame = self.camera.frame
        frame.set_euler_angles(
            theta=-30 * DEGREES,
            phi=80 * DEGREES,
        )

        self.add(axes)
        # self.wait()
        self.play(FadeIn(surface), ShowCreation(surface.mesh, lag_ratio=.01, run_time=3))

        f = lambda s,t: s**2+t**2
        a = [-1, -1]
        s = ValueTracker(.2)
        t = ValueTracker(0)
        dot1 = Sphere(radius=.1, color=RED, gloss=0).move_to(axes.c2p(*a, f(*a)))
        dot2 = f_always(Sphere(radius=.1, color=RED, gloss=0).move_to,
                        lambda: axes.c2p(a[0]+s.get_value(), a[1]+t.get_value(), f(a[0]+s.get_value(), a[1]+t.get_value())))
        plane = ParametricSurface(
            lambda x,y: [x, y, -2*x-2*y-2],
            u_range=[-1.5, -0.5],
            v_range=[-1.5, -0.5],
            color=BLUE,
            opacity=.8,
        ).shift(IN*2)
        # plane.mesh = SurfaceMesh(plane)
        self.play(GrowFromCenter(dot1))
        self.play(GrowFromCenter(dot2))

        self.play(t.animate.set_value(0.2),s.animate.set_value(0), rate_func=smooth)
        self.play(t.animate.set_value(0),s.animate.set_value(-0.2), rate_func=smooth)

        self.play(FadeIn(plane))
        frame.add_updater(lambda m, dt: m.increment_theta(-0.1 * dt))
        self.play(t.animate.set_value(-0.2),s.animate.set_value(0), rate_func=smooth, run_time=2)
        self.play(t.animate.set_value(0),s.animate.set_value(0.2), rate_func=smooth, run_time=2)
        self.play(t.animate.set_value(0.1), rate_func=smooth, run_time=2)
        self.play(s.animate.set_value(-0.1), rate_func=smooth, run_time=2)
        self.wait(10)


class LinearMap(Scene):
    def construct(self):
        L_vec = Tex(r"\vL\colon",r"\R^2",r"\to",r"\R^3")\
            .to_edge(UP).tm({'\\R^2': RED, '\\R^3': BLUE})
        L_vec_ex = VGroup(
            Matrix(np.array([['y_1'], ['y_2'], ['y_3']])).scale(.9).set_color(BLUE),
            Tex("="),
            mIntegerMatrix(np.arange(1, 7).reshape(3, 2)).scale(.9),
            Matrix(np.array([['x_1'], ['x_2']])).scale(.9).set_color(RED)
        ).arrange().next_to(L_vec, DOWN, buff=.5)
        self.play(Write(L_vec))
        self.wait()
        self.play(Write(L_vec_ex))
        self.wait()

        L = Tex(r"L\colon",r"\R^2",r"\to",r"\R")\
            .tm({'\\R': BLUE, '\\R^2': RED}).next_to(L_vec_ex, DOWN, buff=1)
        L_ex = VGroup(
            Tex('y').set_color(BLUE),
            Tex("="),
            mIntegerMatrix(np.arange(1, 3).reshape(1, 2)),
            Matrix(np.array([['x_1'], ['x_2']])).set_color(RED)
        ).arrange().next_to(L, DOWN, buff=.5)
        self.play(Write(L))
        self.wait()
        self.play(Write(L_ex))
        self.wait()

        gradient = TexText("gradient",r"$^T$", color=YELLOW).next_to(L_ex, DOWN)
        Jacobian = TexText("Jacobian matrix", color=YELLOW).next_to(L_vec_ex, DOWN)
        self.play(L_ex[2].animate.set_color(YELLOW), Write(gradient[0]))
        self.wait()
        self.play(Write(gradient[1]))
        self.wait()
        self.play(L_vec_ex[2].animate.set_color(YELLOW), Write(Jacobian))
        self.wait()


class CalcExample(Scene):
    def construct(self):
        title = TexText(r"$f(\vx)=xy^2$", "在", r"$\va=(2,-1)^T$", r"处可微.")\
            .tm({'f': YELLOW, 'va': RED}).to_edge(UP)
        self.play(Write(title))
        self.wait()

        h = TexText(r"记",r"$\vh=(s,t)^T$.").tm(CM).next_to(title, DOWN, buff=.5).to_edge(LEFT)
        self.play(Write(h))
        self.wait()

        diff = VGroup(
            Tex(r"f(",r"\va", "+", r"\vh", r")-f(", r"\va", r")",r"=",
                r"f\left(\begin{bmatrix}2+s\\-1+t\end{bmatrix}\right)", r"-", r"f\left(\begin{bmatrix}2\\-1\end{bmatrix}\right)",
                ).tm(CM),
            Tex(r"=(2+s)(-1+t)^2-2", isolate=['=', 's', 't']).tm({'s': BLUE, 't': BLUE}),
            Tex(r"=s-4t+2t^2-2st+st^2", isolate=['=', 's', 't', '+']).tm({'s': BLUE, 't': BLUE}),
        ).arrange(DOWN).next_to(h, DOWN).set_x(0)
        for i in diff[1:]:
            i.align_to(diff[0][7], LEFT)
        VGroup(diff[0][-3][5], diff[0][-3][9]).set_color(BLUE)
        VGroup(diff[0][-3][3], diff[0][-3][6], diff[0][-3][7], diff[0][-1][3:6]).set_color(RED)
        # self.add(Debug(diff[0][-1]), Debug(diff[0][-3]))
        # self.add(Debug(diff[2]))
        for i in diff:
            self.play(Write(i))
            self.wait()
        self.wait()

        brace1 = Brace(diff[2][1:4])
        brace1 = VGroup(brace1, TexText("线性函数", color=YELLOW).scale(.8).next_to(brace1, DOWN))
        brace2 = Brace(diff[2][5:])
        brace2 = VGroup(brace2, Tex("o(|\\vh|)", color=YELLOW).next_to(brace2, DOWN))
        limit = Tex(r"\lim_{(s,t)\to(0,0)}{2t^2-2st+st^2\over\sqrt{s^2+t^2}}=0")\
            .next_to(brace2, DOWN)
        # self.add(Debug(limit[0]))
        for i in [4, 6, 15, 19, 20, 22, 23, 28, 31]:
            limit[0][i].set_color(BLUE)
        self.play(GrowFromCenter(brace1))
        self.wait()
        self.play(GrowFromCenter(brace2))
        self.wait()
        self.play(Write(limit))
        self.wait()

        self.play(FadeOut(limit))
        partial = VGroup(
            Tex(r"{\partial f\over \partial x}(2,-1)=1"),
            Tex(r"{\partial f\over \partial y}(2,-1)=-4")
        ).scale(.9).set_color(YELLOW).arrange(DOWN, aligned_edge=LEFT).to_edge(LEFT, buff=1).shift(DOWN)
        box = SurroundingRectangle(partial, color=BLUE, buff=.3)
        self.play(Write(partial[0]))
        self.play(Write(partial[1]))
        self.play(ShowCreation(box))
        self.wait()


class Partial(Scene):
    def construct(self):
        title = Tex(r"f(\va+\vh)-f(\va)=L(\vh)+o(|\vh|)", isolate=[r'\va', r'\vh', '=', 'o', '|', '+']) \
            .tm(CM).to_edge(UP)
        i_direc = VGroup(
            TexText(r"取", r"$\vh=t\vei$", r":").set_color_by_tex('vh', BLUE),
            Tex(r"f(\va+t\vei)-f(\va)", "=", r"L(", r"t\vei", r")+o(", r"t", r")").tm({'t': BLUE}),
            Tex(r"{f(\va+t\vei)-f(\va)\over t}", r"=", r"L(", r"\vei", r")+o(1)").tm({'t': BLUE, 'vei': BLUE}),
            Tex("\\text{令~}", r"t", "\\to0\\colon"),
            Tex(r"{\partial f\over\partial x_i}(\va)=L(\vei)"),
            TexText("此时任何方向导数都存在$\\sim$", color=YELLOW)
        ).arrange(DOWN).next_to(title, DOWN)
        i_direc[3][1].set_color(BLUE)
        i_direc[0].to_edge(LEFT)
        i_direc[3].to_edge(LEFT)
        i_direc[1][0].set_color(WHITE)
        i_direc[2][0].set_color(WHITE)
        VGroup(i_direc[1][0][5:9], i_direc[2][0][5:9], i_direc[2][0][17]).set_color(BLUE)
        VGroup(i_direc[1][0][2:4],i_direc[1][0][13:15], i_direc[2][0][2:4], i_direc[2][0][13:15]).set_color(RED)
        i_direc[4][0][7:9].set_color(RED)
        i_direc[-1].to_edge(DOWN)
        self.add(title)
        self.wait()
        # self.add(Debug(i_direc[-1][0]))

        for i in i_direc:
            self.play(Write(i))
            self.wait()


class Continuous(Scene):
    def construct(self):
        title = Tex(r"f(\va+\vh)-f(\va)=L(\vh)+o(|\vh|)", isolate=[r'\va', r'\vh', '=', 'o', '|', '+']) \
            .tm(CM).to_edge(UP)
        cont = VGroup(
            Tex(r"\text{令~}", r"\vh",r"\to",r"\vnull", r":").tm({**CM, 'vnull': YELLOW}),
            Tex(r"\lim_{\vh\to\vnull}\left(f(\va+\vh)-f(\va)\right)= L(\vnull)=0", isolate=['\\va', '\\vh', '\\vnull'])
                .tm({**CM, 'vnull': YELLOW}),
            Tex(r"\lim_{\vh\to\vnull}f(\va+\vh)=f(\va)", isolate=['\\va', '\\vh', '\\vnull'])
                .tm({**CM, 'vnull': YELLOW})
        ).arrange(DOWN).next_to(title, DOWN)
        cont[0].to_edge(LEFT)
        self.add(title)
        self.wait()

        for i in cont:
            self.play(Write(i))
            self.wait()

        implies_cont = TexText(r"可微",r"~$\Longrightarrow$~连续").next_to(cont[-1], DOWN, buff=1)
        implies_partial = VGroup(
            Tex("\\Longrightarrow").rotate(-PI/2),
            TexText("各偏导存在")
        ).arrange(DOWN).next_to(implies_cont[0], DOWN)
        self.play(Write(implies_cont))
        self.wait()
        self.play(Write(implies_partial))
        self.wait()

        notim = NotImply().stretch(2, 0)\
            .rotate(PI/4).move_to(
            mid(implies_cont[0].get_center(), implies_partial[1].get_center()))\
            .shift(RIGHT*1.8)
        self.play(Write(notim))


class Frechet(Scene):
    def construct(self):
        lim = Tex(r"\lim_{\lVert h\rVert\to0}", r"{\lVert f(x+h)-f(x)-Lh\rVert\over \lVert h\rVert}", r"=0",
                  isolate=['x', 'h'])\
            .scale(1.2).to_edge(UP, buff=2).tm({'x': RED, 'h': BLUE})
        frechet = TexText(r"称", r"$f$", "在", r"$x$", r"处", r"Fr\'echet differentiable", ".")\
            .scale(1.2).next_to(lim, DOWN, buff=1)
        frechet[3].set_color(RED)
        frechet[-2].set_color(YELLOW)
        self.play(Write(lim))
        self.wait()
        self.play(Write(frechet))
        self.wait()


class NotImply(VGroup):
    def __init__(self, *vmobjects, **kwargs):
        super().__init__(*vmobjects, **kwargs)
        self.add(Tex("\\nrightarrow"), Tex("\\nleftarrow"))
        self.arrange(DOWN, buff=0)


class Pic(Scene):
    def construct(self):
        title = VGroup(
            Tex("f(x,y)", isolate=list('xy'), stroke_width=8).tm({'x': RED, 'y': RED}),
            TexText("可微?", color=YELLOW, stroke_width=8)
        ).arrange(DOWN).scale(4)
        self.add(title)