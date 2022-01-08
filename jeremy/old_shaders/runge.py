#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author: Jeremy
@file:runge.py
@time:2021/12/25
"""
import numpy as np

from manimlib import *
from numpy import interp

class Charge(Circle):
    CONFIG = {
        "radius": 1.0,
        "color": YELLOW,
        "sign": '-',
        "opacity": 0.8,
        "factor": 0.5,
        "sign_kwargs": {
            'color': BLACK,
        }
    }

    def __init__(self):
        super(Charge, self).__init__()
        symbol = Tex('+', color=self.sign_kwargs['color']) if self.sign == '+' else Tex('-',
                                                                                        color=self.sign_kwargs['color'])
        self.surround(symbol, buff=0.1)
        self.set_opacity(self.opacity)
        self.add(symbol)
        self.scale(self.factor)


class Opening(Scene):
    def construct(self):
        plane = NumberPlane()
        self.add(plane)
        self.wait()
        coords = [
            [(-3,2), (1,-2), (4,1)],
            [(-3,-3.5), (1,0.5), (4,3.5)],
            [(-3,0), (1,0), (4,0)],
        ]
        dots = [VGroup(*[Dot(plane.c2p(*i)) for i in coord]).set_color(YELLOW) for coord in coords]
        self.play(LaggedStartMap(GrowFromCenter, dots[0]))
        self.wait()

        graph = [plane.get_graph(poly(coord, 2), color=RED) for coord in coords]
        self.play(ShowCreation(graph[0]))
        self.wait()
        for i in range(2):
            self.play(RT(dots[i], dots[i+1]), RT(graph[i], graph[i+1]))
            self.wait()
        conclusion = TexText(r"$n+1$个(横坐标互异)点确定唯一的至多$n$次多项式.", color=YELLOW)\
            .to_edge(UP, buff=1).add_background_rectangle()
        self.play(Write(conclusion))
        self.wait()


class Interpolation(Scene):
    CONFIG = {
        "f": lambda x: np.sin(x)
    }
    def construct(self):
        plane = NumberPlane()
        self.add(plane)
        graph = plane.get_graph(self.f, color=RED)
        self.play(ShowCreation(graph), run_time=2)
        self.wait()

        xx = [-6,-5,-3.5,-1,1,2,4,5.5]
        dots = VGroup(*[Dot(plane.c2p(xj, self.f(xj))).set_color(YELLOW) for xj in xx])
        for x, dot in zip(xx, dots):
            always(dot.move_to, plane.c2p(x, self.f(x)))
        self.play(LaggedStartMap(GrowFromCenter, dots, lag_ratio=.4))
        self.wait()
        graph = plane.get_graph(poly(list(zip(xx, self.f(xx))), 7), color=GREEN)
        self.play(ShowCreation(graph), run_time=2)
        self.wait()
        title = VGroup(TexText("Polynomial Interpolation"), TexText("多项式插值"))\
            .arrange(DOWN).set_color(YELLOW).to_edge(UP, buff=.5).add_background_rectangle()
        self.play(Write(title))
        self.wait()
        self.play(FadeOut(graph), FadeOut(dots))

        MAX_DEG = 20
        dots = [
            VGroup(*[Dot(plane.c2p(xj, self.f(xj))) for xj in np.linspace(-7,7,i)]).set_color(YELLOW)
            for i in range(2, MAX_DEG)
        ]
        graphs = [
            plane.get_graph(poly(list(zip(np.linspace(-7,7,i), self.f(np.linspace(-7,7,i)))), i-1), color=GREEN)
            for i in range(2,MAX_DEG)
        ]
        self.wait()
        self.play(LaggedStartMap(GrowFromCenter, dots[0]))
        self.wait()
        self.play(ShowCreation(graphs[0]))
        self.wait()
        for i in range(len(graphs)-1):
            self.play(RT(dots[i], dots[i+1]), RT(graphs[i], graphs[i+1]))
            # self.wait()

class Weierstrass(Scene):
    def construct(self):
        title = Title("Weierstrass逼近定理", color=YELLOW)
        theorem = TexText("$[a,b]$上的","连续函数","都能被","多项式","一致逼近.").next_to(title, DOWN, buff=.5)
        theorem.tm({'连续': RED, '多项式': RED})
        self.add(title)
        self.wait()
        self.play(Write(theorem))
        self.wait()

        formula = Tex(r"\forall\eps>0,~", r"\exists p,~", r"\text{s.t.}~\lVert f-p\rVert<\eps.", color=YELLOW)\
            .next_to(theorem, DOWN, buff=.5)
        for i in formula:
            self.play(Write(i))
            self.wait()
        norm = Tex(r"\lVert f-p\rVert_\infty=\sup|f-p|").next_to(formula[-1], DOWN, buff=1)
        arrow = Arrow(ORIGIN, UP).next_to(norm, UP)
        self.play(GrowArrow(arrow))
        self.wait()
        self.play(Write(norm))
        self.wait()

        problem = TexText("并没有保证","多项式插值","能一致收敛到$f$.").to_edge(DOWN, buff=2)
        problem[1].set_color(RED)
        self.play(Write(problem))
        self.wait()

class Abs(Scene):
    def construct(self):
        plane = NumberPlane(x_range=[-2, 2], y_range=[-1, 1], height=FRAME_HEIGHT, width=FRAME_WIDTH)
        numbers = VGroup(Tex("-1").next_to(plane.c2p(-1), DOWN), Tex("1").next_to(plane.c2p(1), DOWN))
        abs = plane.get_graph(lambda x: np.abs(x), color=RED, use_smoothing=False)
        self.add(plane, numbers)
        self.play(ShowCreation(abs), run_time=2)
        self.wait()

        MAX_DEG = 20
        dots = [
            VGroup(*[Dot(plane.c2p(xj, np.abs(xj))) for xj in np.linspace(-1,1,i)]).set_color(YELLOW)
            for i in range(3, MAX_DEG)
        ]
        graphs = [
            plane.get_graph(poly(list(zip(np.linspace(-1,1,i), np.abs(np.linspace(-1,1,i)))), i-1), color=GREEN)
            for i in range(3,MAX_DEG)
        ]
        self.wait()
        self.play(LaggedStartMap(GrowFromCenter, dots[0]))
        self.wait()
        self.play(ShowCreation(graphs[0]))
        self.wait()
        for i in range(len(graphs)-1):
            self.play(RT(dots[i], dots[i+1]), RT(graphs[i], graphs[i+1]))


class Runge(Scene):
    def construct(self):
        f = lambda x: 1/(1+25*x**2)
        plane = NumberPlane(x_range=[-2, 2], y_range=[-1, 1], height=FRAME_HEIGHT, width=FRAME_WIDTH)
        numbers = VGroup(Tex("-1").next_to(plane.c2p(-1), DOWN), Tex("1").next_to(plane.c2p(1), DOWN))
        abs = plane.get_graph(f, color=RED)
        self.add(plane, numbers)
        self.play(ShowCreation(abs), run_time=2)
        f_label = Tex(r"f(x)={1\over 1+25x^2}", isolate=['x', '=']).tm({'x': RED})\
            .add_background_rectangle().next_to(ORIGIN, DOWN)
        taylor = Tex(r"=1-25 x^2+625 x^4-15625 x^6+\cdots", isolate=['x'])\
            .tm({'x': RED}).next_to(f_label[4], DOWN, aligned_edge=LEFT, buff=1).add_background_rectangle()
        self.play(Write(f_label))
        self.wait()
        self.play(Write(taylor))
        self.wait()

        analytic = TexText("analytic 解析的", color=YELLOW).to_edge(DOWN, buff=.75).add_background_rectangle()
        self.play(Write(analytic))
        self.wait()
        self.play(FadeOut(VGroup(analytic, taylor)))

        MAX_DEG = 20
        dots = [
            VGroup(*[Dot(plane.c2p(xj, f(xj))) for xj in np.linspace(-1,1,i)]).set_color(YELLOW)
            for i in range(3, MAX_DEG)
        ]
        graphs = [
            plane.get_graph(poly(list(zip(np.linspace(-1,1,i), f(np.linspace(-1,1,i)))), i-1), color=GREEN)
            for i in range(3,MAX_DEG)
        ]
        self.play(LaggedStartMap(GrowFromCenter, dots[0]))
        self.wait()
        self.play(ShowCreation(graphs[0]))
        self.wait()
        for i in range(len(graphs)-1):
            self.play(RT(dots[i], dots[i+1]), RT(graphs[i], graphs[i+1]))
        self.wait()

        runge_label = TexText("Runge function", color=YELLOW).add_background_rectangle().next_to(f_label, DOWN, buff=.5)
        self.play(Write(runge_label))

class Soccer(Scene):
    def construct(self):
        plane = ComplexPlane(x_range=[-2, 2], y_range=[-1, 1], height=FRAME_HEIGHT, width=FRAME_WIDTH)
        numbers = VGroup(Tex("-1").next_to(plane.n2p(-1), DOWN), Tex("1").next_to(plane.n2p(1), DOWN))
        self.add(plane, numbers)

        interval = Line(plane.n2p(-1), plane.n2p(1), color=RED)
        self.play(ShowCreation(interval))
        self.wait()

        contour1 = ComplexContour(lambda z: ((z+1)*np.log(z+1)-(z-1)*np.log(z-1)).real, 2*np.log(2),
                                  x=np.linspace(-1.1, 1.1, 2000),
                                  y=np.linspace(0,0.53,2000),
                                  tol=1e-4,
                                  x_unit=plane.get_x_axis().get_unit_size(),
                                  y_unit=plane.get_y_axis().get_unit_size())\
            .set_color(RED).reverse_points()
        points = contour1.points
        contour2 = ComplexContour(lambda z: ((z+1)*np.log(z+1)-(z-1)*np.log(z-1)).real, 2*np.log(2),
                                  y=np.linspace(-1, 0, 2000),
                                  x_unit=plane.get_x_axis().get_unit_size(),
                                  y_unit=plane.get_y_axis().get_unit_size()
                                  ).set_color(RED)
        self.play(RT(interval, contour1), RT(interval.copy(), contour2))
        self.wait()

        dot = Dot(plane.n2p(0.52552491457j), color=YELLOW)
        self.play(FadeIn(dot, scale=.5))
        label = Tex(r"0.52552491457\,\i", color=YELLOW).next_to(dot, UP).add_background_rectangle()
        self.play(Write(label))
        self.wait()

        f_label = Tex(r"f(x)={1\over 1+25x^2}", isolate=['x', '=']).tm({'x': GREEN}) \
            .add_background_rectangle().to_corner(UL)
        self.play(Write(f_label))
        self.wait()
        cross = Cross(dot).set_color(GREEN).scale(1.5).move_to(plane.n2p(0.2j))
        cross2 = Cross(dot).set_color(GREEN).scale(1.5).move_to(plane.n2p(-0.2j))
        self.play(ShowCreation(cross), ShowCreation(cross2))
        self.wait()


class Hermite(Scene):
    def construct(self):
        cm = {'x': BLUE, 't': RED, 'dots': WHITE, 'int': WHITE, 'x_': YELLOW, 'sqrt': WHITE, 'right': WHITE,}
        pre = TexText(r"插值节点",r"$x_0,\ldots,x_n$",r":").to_corner(UL)
        pre[1].set_color(cm['x_'])
        hermite = Tex(r"f(",r"x",r")-p(",r"x",r")=","{1\over2\pi\i}\int_\Gamma","{l(",
                      r"x",r")\over l(",r"t",r")}","{f(",r"t",
                      r")\over ","t","-",r"x",r"}\d ",r"t")\
            .next_to(pre, DOWN).set_x(0).tm(cm)
        hermite_label = TexText("Hermite Integral Formula", color=YELLOW).next_to(hermite, DOWN, buff=.5)
        box = SurroundingRectangle(hermite_label, color=YELLOW)
        ell = Tex(r"l(","x",")=(","x","-",r"x_0",")\cdots(",r"x",r"-",r"x_n",r")")\
            .tm(cm).next_to(hermite_label, DOWN, buff=.5)
        self.play(Write(pre))
        self.wait()
        self.play(Write(hermite[:5]))
        self.wait()
        self.play(Write(hermite[5:]))
        self.wait()
        self.play(Write(hermite_label))
        self.play(ShowCreation(box))
        self.wait()
        self.play(Write(ell))
        self.wait()
        self.play(FadeOut(VGroup(ell, box, hermite_label)))

        xjs = VGroup(
            Dot(ORIGIN+UP*.5), Dot(DOWN*.5+LEFT*2), Dot(DOWN*2.5+LEFT), Dot(DOWN*1+RIGHT*2), Dot(DOWN*2+RIGHT*.5)
        )
        xj_labels = VGroup(*[Tex(f"x_{i}", color=YELLOW) for i in range(5)])
        x = Dot(DOWN).set_color(cm['x'])
        x_label = Tex('x', color=cm['x']).add_updater(lambda t: t.next_to(x, DOWN))

        for xj, xj_label in zip(xjs, xj_labels):
            xj.set_color(YELLOW)
            xj_label.next_to(xj, DOWN)
        self.play(LaggedStartMap(GrowFromCenter, xjs), LaggedStartMap(GrowFromCenter, xj_labels))
        self.wait()
        self.play(GrowFromCenter(x), GrowFromCenter(x_label))
        self.play(x.animate.move_to(LEFT*2+UP))
        self.play(x.animate.move_to(LEFT*2+DOWN))
        self.play(x.animate.move_to(DOWN*2+RIGHT))
        self.play(x.animate.move_to(DOWN))
        self.wait()

        contour = VGroup().set_points_smoothly(
            [UP, LEFT*3, LEFT*3+DOWN*2, DOWN*3.5, RIGHT*2+DOWN*2, RIGHT*3+DOWN, UP],
            true_smooth=True).set_color(RED)
        tip = ArrowTip(angle=-0.8).set_color(RED).scale(.7).move_to(LEFT*3+DOWN*2)
        gamma = Tex(r"\Gamma", color=RED).next_to(contour, LEFT)
        region = contour.copy().scale(1.2).set_fill(GREEN, opacity=0.4).set_stroke(width=0)
        self.play(ShowCreation(contour))
        self.play(Write(gamma))
        self.play(ShowCreation(tip))
        self.wait()
        self.play(FadeIn(region))
        self.wait()
        self.play(FadeOut(VGroup(contour, tip, gamma, region, xjs, x,xj_labels, x_label)))
        self.wait()

        box = SurroundingRectangle(hermite[6:11])
        self.play(ShowCreation(box))
        self.wait()
        ratio = Tex(r"{(","x","-",r"x_0",r")\cdots(","x","-",r"x_n",r")\over(",
                    "t","-",r"x_0",r")\cdots(","t",r"-",r"x_n)}").tm(cm).next_to(hermite, DOWN, buff=.5)
        bars = VGroup(
            Line(ORIGIN, UP).set_height(ratio.get_height()).next_to(ratio, LEFT),
            Line(ORIGIN, UP).set_height(ratio.get_height()).next_to(ratio, RIGHT),
        )
        self.play(RT(hermite[6:11].copy(), ratio))
        self.wait()
        self.play(ShowCreation(bars))
        self.wait()
        mean = Tex(r"=",r"\left({\sqrt[n+1]{|","x","-",r"x_0",r"|\cdots|","x","-",r"x_n",r"|}\over","\sqrt[n+1]{|",
                    "t","-",r"x_0",r"|\cdots|","t",r"-",r"x_n",r"|}}\right)^{n+1}")\
            .tm(cm).next_to(ratio, DOWN, aligned_edge=LEFT).shift(LEFT)
        comment = TexText("$\Gamma$足够大$\Longrightarrow$ ","$t$","比","$x$","平均离","节点","更远")\
            .tm({'t': RED, 'x': BLUE, '节点': YELLOW, 'right': WHITE}).next_to(mean, DOWN)
        exp = Tex(r"\leq","0.9^{n+1}").next_to(mean, DOWN, aligned_edge=LEFT)
        self.play(Write(mean))
        self.wait()
        self.play(Write(comment))
        self.wait()
        self.play(FadeOut(comment))
        self.play(Write(exp))
        self.wait()

        limit = Tex('\\to0').next_to(exp)
        self.play(Write(limit))
        self.wait()


class Analysis(Scene):
    def construct(self):
        cm = {'x': BLUE, 't': RED, 'dots': WHITE, 'int': WHITE, 'x_': YELLOW, 'sqrt': WHITE, 'right': WHITE, }
        hope = TexText("希望").to_corner(UL)
        self.add(hope)
        self.wait()

        mean = Tex(r"{\sqrt[n+1]{|", "x", "-", r"x_0", r"|\cdots|", "x", "-", r"x_n", r"|}\over",
                   "\sqrt[n+1]{|",
                   "t", "-", r"x_0", r"|\cdots|", "t", r"-", r"x_n", r"|}}<1") \
            .tm(cm).next_to(hope, DOWN).set_x(0)
        self.play(Write(mean))
        self.wait()

        log = TexText("取对数:").next_to(mean, DOWN).align_to(hope, LEFT)
        self.play(Write(log))
        self.wait()
        logged = Tex(r"{1\over n+1}\sum_{j=0}^n\ln |t-x_j|",">",r"{1\over n+1}\sum_{j=0}^n\ln |x-x_j|", isolate=['t','x_j', 'x'])\
            .tm(cm).next_to(log, DOWN).set_x(0)
        simplified = Tex(r"u_n(t)",">","u_n(x)", isolate=['x', 't']).tm(cm).move_to(logged)
        self.play(Write(logged))
        self.wait()
        self.play(TransformMatchingTex(logged, simplified, transform_mismatches=True))
        self.wait()
        where = TexText("其中").next_to(simplified, DOWN).align_to(log, LEFT)
        un = Tex(r"u_n(z)={1\over n+1}\sum_{j=0}^n\ln |z-x_j|", isolate=['z', 'x_j'])\
            .tm({'z': BLUE, 'x_': YELLOW}).next_to(where, DOWN).set_x(0)
        self.play(Write(where))
        self.play(Write(un))
        self.wait()
        box = SurroundingRectangle(simplified)
        self.play(ShowCreation(box))
        self.wait()


class Potential(Scene):
    def construct(self):
        un = Tex(r"u_n(z)={1\over n+1}\sum_{j=0}^n\ln |z-x_j|", isolate=['z', 'x_j']) \
            .tm({'z': BLUE, 'x_': YELLOW}).move_to([ 0.,        -2.2348687,  0.       ] )
        self.add(un)
        self.play(un.animate.to_corner(UL))

        plane = ComplexPlane(x_range=[-2, 2], y_range=[-1, 1], height=FRAME_HEIGHT, width=FRAME_WIDTH)
        numbers = VGroup(Tex("-1").next_to(plane.c2p(-1), DOWN), Tex("1").next_to(plane.c2p(1), DOWN))
        self.play(FadeIn(VGroup(plane, numbers)))
        self.wait()

        def func(x, n):
            s = 0
            for j in range(n):
                s += np.log(np.abs(x - xj[j]))
            return s / n

        xj = np.linspace(-1, 1, 8)
        charges = VGroup(*[Charge().move_to(plane.c2p(num)) for _, num in enumerate(xj)])
        self.play(LaggedStartMap(GrowFromCenter, charges))
        z = ValueTracker(0.2j, value_type=np.complex)
        z_dot = Dot(color=BLUE).add_updater(lambda x: x.move_to(plane.n2p(z.get_value())))
        z_label = DecimalNumber(unit='V', num_decimal_places=4, include_sign=True).add_updater(lambda x: x.set_value(func(z.get_value(), 8)))\
            .add_updater(lambda x: x.next_to(z_dot, UP))
        self.play(GrowFromCenter(z_dot))
        self.play(Write(z_label))
        self.play(z.set_value, 1+0.5j, run_time=4)
        self.play(z.set_value, -0.8j, run_time=5)
        self.play(z.set_value, -1+0.2j, run_time=5)
        self.play(z.set_value, xj[2], run_time=3)
        self.wait()


class Physics(Scene):
    def construct(self):
        line = Line(UP*FRAME_Y_RADIUS, DOWN*FRAME_Y_RADIUS)
        title1 = TexText("电势").to_edge(UP).set_x(-FRAME_X_RADIUS/2).set_color(YELLOW)
        title2 = TexText("我们的势").to_edge(UP).set_x(FRAME_X_RADIUS/2).set_color(YELLOW)
        self.add(line, title1, title2)
        self.wait()

        phy = VGroup(Tex(r"F\propto {1\over ","r",r"^2}"), Tex(r"u\propto {1\over ",r"r",r"}"))\
            .arrange(DOWN, buff=1.5, aligned_edge=LEFT).set_x(-FRAME_X_RADIUS/2)
        ours = VGroup(Tex(r"F\propto {1\over ",r"r}"), Tex(r"u\propto \ln ",r"r"))\
            .arrange(DOWN, buff=1.5, aligned_edge=LEFT).set_x(FRAME_X_RADIUS/2)
        for i in phy:
            i.tm({'r': RED, 'over': WHITE})
            i.scale(1.5)
            self.play(Write(i))
            self.wait()
        for i in ours:
            i.tm({'r': RED, 'over': WHITE, 'prop': WHITE})
            i.scale(1.5)
            self.play(Write(i))
            self.wait()


class Contours(Scene):
    def construct(self):
        cm = {'z': BLUE, 'x_j': YELLOW}
        formula = Tex(r"u_n(z)={1\over n+1}\sum_{j=0}^n\ln |z-x_j|", isolate=['z', 'x_j']) \
            .tm({'z': BLUE, 'x_': YELLOW}).move_to([0., -2.2348687, 0.])
        self.add(formula)
        self.play(formula.animate.scale(.7).to_corner(UL))
        formula.add_updater(lambda x: self.add(x))
        self.wait()

        plane = ComplexPlane(x_range=[-2, 2], y_range=[-1, 1], height=FRAME_HEIGHT, width=FRAME_WIDTH)
        numbers = VGroup(Tex("-1").next_to(plane.c2p(-1), DOWN), Tex("1").next_to(plane.c2p(1), DOWN))
        self.play(FadeIn(VGroup(plane, numbers)))
        self.wait()

        def func(x, n):
            s = 0
            for j in range(n):
                s += np.log(np.abs(x - xj[j]))
            return s / n

        levels = np.log((np.arange(1.25, 3.25, 0.25) / np.e))

        levels[2] = -0.45
        xj = np.linspace(-1, 1, 8)
        charges8 = VGroup(*[Charge().move_to(plane.c2p(num)) for _, num in enumerate(xj)])
        tols = [1 * 1e-5, 9e-5, 1e-5, 1e-4, 1e-4, 1e-4, 1e-4, 1e-4]
        xs = [np.linspace(-2, 2, 2000)] * 8
        ys = [np.linspace(-1, 1, 2000)] * 8
        xs[0] = np.linspace(-0.3, 0.3, 2000)
        ys[0] = np.linspace(-0.1, 0.1, 2000)
        xs[1] = np.linspace(-0.8, 0.8, 1000)
        xs[2] = np.linspace(-1, 1, 2000)
        ys[2] = np.linspace(-0.4, 0.4, 1000)
        contours8 = VGroup(*[ComplexContour(
            lambda x: func(x, 8),
            level,
            x_unit=plane.get_x_axis().get_unit_size(),
            y_unit=plane.get_y_axis().get_unit_size(),
            x=xs[i],
            y=ys[i],
            tol=tols[i],
            close=True
        ) for i, level in enumerate(levels)])

        xj = np.linspace(-1, 1, 12)
        xs[0] = np.linspace(-0.5, 0.5, 1000)
        tols[0] = 2e-5
        tols[1] = 2e-5
        xs[1] = np.linspace(-0.8, 0.8, 2000)
        charges12 = VGroup(*[Charge().move_to(plane.c2p(num)) for _, num in enumerate(xj)])
        contours12 = VGroup(*[ComplexContour(
            lambda x: func(x, 12),
            level,
            x_unit=plane.get_x_axis().get_unit_size(),
            y_unit=plane.get_y_axis().get_unit_size(),
            x=xs[i],
            y=ys[i],
            tol=tols[i],
            close=True
        ) for i, level in enumerate(levels)])

        xj = np.linspace(-1, 1, 16)
        xs[0] = np.linspace(-0.6, 0.6, 1000)
        xs[2] = np.linspace(-1.2, 1.2, 2000)
        tols[0] = 5e-6
        tols[1] = 1e-4
        tols[2] = 2e-5
        charges16 = VGroup(*[Charge().move_to(plane.c2p(num)) for _, num in enumerate(xj)])
        contours16 = VGroup(*[ComplexContour(
            lambda x: func(x, 16),
            level,
            x_unit=plane.get_x_axis().get_unit_size(),
            y_unit=plane.get_y_axis().get_unit_size(),
            x=xs[i],
            y=ys[i],
            tol=tols[i],
            close=True
        ) for i, level in enumerate(levels)])

        xj = np.linspace(-1, 1, 20)
        xs[0] = np.linspace(-0.8, 0.8, 2000)
        ys[0] = np.linspace(-0.2, 0.2, 2000)
        xs[1] = np.linspace(-0.85, 0.85, 2000)
        xs[2] = np.linspace(-1.2, 1.2, 2000)
        # xs[3] = np.linspace(-1.2, 1.2, 2000)
        tols[0] = 2e-6
        tols[1] = 2e-4
        tols[2] = 2e-4
        tols[3] = 2e-4
        charges20 = VGroup(*[Charge().move_to(plane.c2p(num)) for _, num in enumerate(xj)])
        contours20 = VGroup(*[ComplexContour(
            lambda x: func(x, 20),
            level,
            x_unit=plane.get_x_axis().get_unit_size(),
            y_unit=plane.get_y_axis().get_unit_size(),
            x=xs[i],
            y=ys[i],
            tol=tols[i],
            close=True
        ) for i, level in enumerate(levels)])
        contours = [contours8, contours12, contours16, contours20]
        charges = [charges8, charges12, charges16, charges20]
        for contour in contours:
            for i, c in enumerate(contour):
                c.set_color(interpolate_color(GREEN, RED, i / 8))

        self.play(LaggedStartMap(GrowFromCenter, charges8, lag_ratio=.2))
        self.wait()
        self.play(FadeIn(contours8))
        self.wait()
        for i in range(3):
            self.play(
                RT(charges[i], charges[i + 1]),
                AnimationGroup(*[FadeTransform(contours[i][j], contours[i + 1][j]) for j in range(8)]),
            )
            self.wait()


class Limit(Scene):
    def construct(self):
        cm = {'z': BLUE, 'x': YELLOW}
        limit = Tex(r"\lim_{n\to\infty}{1\over n+1}\sum_{j=0}^n\ln |z-x_j|", isolate=['z', 'x_j']) \
            .tm(cm).to_edge(UP)
        integrate = Tex(r"=\frac12\int_{-1}^1\ln |z-x|\d x", isolate=['z', 'x'])\
            .tm(cm).next_to(limit, DOWN, aligned_edge=LEFT).shift(LEFT*.5)
        steps = VGroup(
            MTex(r"=\frac12\int_{-1}^1\ln\sqrt{(z-x)(\overline{z-x})}\d x", isolate=['z', 'x']).tm(cm),
            MTex(r"=\frac14\int_{-1}^1\ln(z-x)+\ln(\overline{z-x})\d x", isolate=['z', 'x']).tm(cm),
            MTex(r"=\frac12\Re\int_{-1}^1\ln(z-x)\d x", isolate=['z', 'x']).tm(cm)
        ).arrange(DOWN, aligned_edge=LEFT).next_to(integrate, DOWN, aligned_edge=LEFT)
        res = Tex(r"=-1+\frac12\Re\left[(z+1)\ln(z+1)-(z-1)\ln(z-1)\right]")\
            .next_to(integrate, DOWN).set_x(0)
        VGroup(res[0][11], res[0][18], res[0][24], res[0][31]).set_color(BLUE)
        # self.add(Debug(res[0]))
        self.add(limit)
        self.wait()
        self.play(Write(integrate))
        self.wait()
        for s in steps:
            self.play(Write(s))
            self.wait()
        self.play(RT(steps, res))
        self.wait()


class LimitContour(Scene):
    def construct(self):
        plane = ComplexPlane(x_range=[-2, 2], y_range=[-1, 1], height=FRAME_HEIGHT, width=FRAME_WIDTH)
        numbers = VGroup(Tex("-1").next_to(plane.c2p(-1), DOWN), Tex("1").next_to(plane.c2p(1), DOWN))
        self.add(plane, numbers)
        self.wait()
        line = Line(plane.n2p(-1), plane.n2p(1)).set_color(YELLOW)
        self.play(ShowCreation(line))
        self.wait()

        xs = [np.linspace(-2,2,2000)]*8
        ys = [np.linspace(-1,1,2000)]*8
        tols = [1e-4]*8

        xs[0] = np.linspace(-0.8, 0.8, 3000)
        ys[0] = np.linspace(-0.2, 0.2, 2000)
        xs[1] = np.linspace(-0.85, 0.85, 2000)
        xs[2] = np.linspace(-1.2, 1.2, 2000)
        # xs[3] = np.linspace(-1.2, 1.2, 2000)
        tols[0] = 2e-5
        tols[1] = 2e-4
        tols[2] = 2e-4
        tols[3] = 2e-4
        levels = np.log((np.arange(1.25, 3.25, 0.25) / np.e))
        contours = VGroup(*[ComplexContour(
            lambda z: -1+((z+1)*np.log(z+1)-(z-1)*np.log(z-1)).real/2,
            level,
            x_unit=plane.get_x_axis().get_unit_size(),
            y_unit=plane.get_y_axis().get_unit_size(),
            x=xs[i],
            y=ys[i],
            tol=tols[i],
            close=True
        ) for i, level in enumerate(levels)])
        for i, c in enumerate(contours):
            c.set_color(interpolate_color(GREEN, RED, i / 8))

        self.play(FadeIn(contours))
        self.wait()
        self.play(VGroup(contours[0:3], contours[4:]).fade, .9)
        self.wait()

        res = Tex(r"-1+\frac12\Re\left[(z+1)\ln(z+1)-(z-1)\ln(z-1)\right]=-1+\ln2").to_edge(UP)
        VGroup(res[0][10], res[0][17], res[0][23], res[0][30]).set_color(BLUE)
        self.play(Write(res))
        self.wait()


class Solve(Scene):
    def construct(self):
        N = 4
        axes1 = NumberLine(x_range=[-1,1], width=8).move_to(UP)
        chebpts = [
            VGroup(*[Dot(axes1.n2p(i)).set_color(YELLOW) for i in np.cos(np.linspace(0,PI, N))])
            for N in range(3, 20)
        ]


        axes2 = NumberLine(x_range=[-1,1], width=8).move_to(DOWN*2)
        # x,y = np.polynomial.legendre.leggauss(N)
        legpts = [
            VGroup(*[Dot(axes2.n2p(i)).set_color(RED) for i in np.polynomial.legendre.leggauss(N)[0]])
            for N in range(3,20)
                  ]
        label1 = TexText("Chebyshev points", color=YELLOW).next_to(axes1, UP, buff=.5)
        label2 = TexText("Legendre points", color=RED).next_to(axes2, UP, buff=.5)
        self.add(axes1, axes2, chebpts[0], legpts[0], label1, label2)
        for i in range(len(chebpts)-1):
            self.play(
                RT(chebpts[i], chebpts[i+1]),
                RT(legpts[i], legpts[i+1]),
            )

class Pic(Scene):
    def construct(self):
        f = lambda x: 1 / (1 + 25 * x ** 2)
        plane = Axes(x_range=[-1.5, 1.5], y_range=[-1.5,1.5], height=FRAME_HEIGHT, width=FRAME_WIDTH-2).shift(DOWN*2)
        numbers = VGroup(Tex("-1").next_to(plane.c2p(-1), DOWN), Tex("1").next_to(plane.c2p(1), DOWN))
        abs = plane.get_graph(f, color=RED)
        self.add(plane, numbers, abs)
        f_label = Tex(r"f(x)={1\over 1+25x^2}", isolate=['x', '=']).tm({'x': RED}) \
            .add_background_rectangle().next_to(ORIGIN, DOWN)

        MAX_DEG = 20
        dots = [
            VGroup(*[Dot(plane.c2p(xj, f(xj))) for xj in np.linspace(-1, 1, i)]).set_color(YELLOW)
            for i in range(3, MAX_DEG)
        ]
        graphs = [
            plane.get_graph(poly(list(zip(np.linspace(-1, 1, i), f(np.linspace(-1, 1, i)))), i - 1), color=GREEN)
            for i in range(3, MAX_DEG)
        ]

        # runge_label = TexText("Runge function", color=YELLOW).add_background_rectangle().next_to(f_label, DOWN, buff=.5)
        self.add(dots[10], graphs[10])

        title = TexText("Runge现象", color=YELLOW, stroke_width=5).scale(3).to_edge(UP)
        self.add(title)