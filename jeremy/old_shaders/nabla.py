from sympy import factor
from manimlib import *

cm = {'f': YELLOW, 'vf': RED, 'R^m': RED}

class Opening(Scene):
    def construct(self) -> None:
        scalar = Tex(r"f",r"\colon \R^n\to",r"\R", r"\text{\ 数量值函数}").tm(cm)
        scalar[-2].set_color(cm['f'])
        vector = Tex(r"\vf",r"\colon\R^n\to",r"\R^m", r"\text{\ 向量值函数}").tm(cm)
        VGroup(
            scalar.scale(1.5), vector.scale(1.5)
            ).arrange(DOWN, buff=2, aligned_edge=LEFT)
        scalar[-1].align_to(vector[-1], LEFT)
        scalar_field = TexText("(数量场)", color=cm['f']).next_to(scalar[-1], DOWN)
        vector_field = TexText("(向量场)", color=cm['vf']).next_to(vector[-1], DOWN)

        self.play(Write(scalar)); self.wait()
        self.play(Write(vector)); self.wait()
        self.play(Write(scalar_field), Write(vector_field)); self.wait()
        return super().construct()


class ScalarField(Scene):
    def construct(self) -> None:
        plane = NumberPlane()
        plane.add_coordinate_labels()
        self.add(plane); self.wait()

        f = lambda x,y: x**2+y**2
        f_label = Tex("f(x,y)=x^2+y^2", color=YELLOW).add_background_rectangle().to_corner(UL)
        self.play(Write(f_label))

        x = ValueTracker(0); y = ValueTracker(0)
        dot = Dot().set_color(YELLOW).add_updater(lambda t: t.move_to(plane.c2p(x.get_value(), y.get_value())))
        value = DecimalNumber().add_updater(
            lambda t: t.set_value(
                f(x.get_value(), y.get_value())
                )
            ).add_updater(lambda t: t.next_to(dot, DOWN)).add_updater(lambda t: t.set_color(dot.get_color()))
        # always(dot.move_to, plane.c2p(x.get_value(), y.get_value()))

        self.play(FadeIn(dot), Write(value)); self.wait()
        self.play(x.animate.set_value(4), y.animate.set_value(2), run_time=3)
        self.play(x.animate.set_value(1), y.animate.set_value(-3), run_time=3)
        self.play(x.animate.set_value(-4), y.animate.set_value(0), run_time=3)
        self.play(x.animate.set_value(-2), y.animate.set_value(2), run_time=3)
        self.wait(2)

        # Contours
        theta = ValueTracker(PI)
        unit = plane.get_x_axis().get_unit_size()
        circles = VGroup(*[Circle(radius=r*unit) for r in [4,3,2,1]])
        labels = VGroup(*[Tex(f"{r**2}.00").scale(.7) for r in [4,3,2,1]])
        for i in range(len(circles)):
                circles[i].set_color(interpolate_color(RED, GREEN, i / len(circles)))
                labels[i].move_to(circles[i].get_right()).set_color(circles[i].get_color()).add_background_rectangle()
            
        for r, circle, label in zip([4,3,2,1], circles, labels):
            x.add_updater(lambda t: t.set_value(r*np.cos(theta.get_value())))
            y.add_updater(lambda t: t.set_value(r*np.sin(theta.get_value())))
            self.wait()
            self.play(theta.animate.increment_value(TAU), run_time=4, rate_func=linear)
            self.play(FadeIn(circle), FadeIn(label))
        self.play(FadeOut(dot), FadeOut(value))
        self.wait()

        contour = Tex(r"\{",r"\vx",r"\mid ",r"f",r"(",r"\vx",r")=c\}").tm({'x': RED, 'f': YELLOW}).add_background_rectangle()
        label = VGroup(
            TexText(r"level set", color=YELLOW),
            TexText("等值面", color=YELLOW).scale(.8)
            ).arrange(DOWN).add_background_rectangle()
        VGroup(contour, label).arrange(DOWN, buff=.5).to_corner(UR)
        self.play(Write(contour)); self.wait()
        self.play(Write(label)); self.wait()

        return super().construct()


class Graph(Scene):
    def construct(self) -> None:
        f = lambda x,y: x**2+y**2
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
        surface.mesh = SurfaceMesh(surface, resolution=(30, 30), normal_nudge=-1e-2)
        surface.mesh.set_stroke(WHITE, 1, opacity=0.5)
        frame = self.camera.frame
        frame.set_euler_angles(
            theta=-30 * DEGREES,
            phi=80 * DEGREES,
        )

        self.add(axes)
        # frame.add_updater(lambda m, dt: m.increment_theta(-0.1 * dt))
        self.play(
            FadeIn(surface), 
            # ShowCreation(surface.mesh, lag_ratio=.01, run_time=3)
            )

        x = ValueTracker(); y = ValueTracker()
        line = Line(ORIGIN, UP).add_updater(
            lambda m: m.become(
                Line(
                    axes.c2p(x.get_value(), y.get_value(), 0),
                    axes.c2p(x.get_value(), y.get_value(), f(x.get_value(), y.get_value()))
                ).set_color(RED)
            )
        )
        ballxy = Sphere(radius=.1, color=RED, gloss=0).add_updater(lambda t:t.move_to(line.get_start()))
        ballz = Sphere(radius=.1, color=RED, gloss=0).add_updater(lambda t:t.move_to(line.get_end()))
        value = DecimalNumber().add_updater(lambda t: t.set_value(f(x.get_value(), y.get_value()))).add_updater(lambda t: t.next_to(line).rotate(angle=-PI/2, axis=LEFT).rotate(angle=-PI/6, axis=OUT))

        self.add(line, ballxy, ballz, value)
        self.play(x.animate.set_value(2), y.animate.set_value(-1), run_time=3)
        self.play(x.animate.set_value(-2), y.animate.set_value(-1.5), run_time=3)
        self.play(x.animate.set_value(-2), y.animate.set_value(1), run_time=3)

        graph = Tex(r"\{\left(",r"\vx",r",",r"f",r"(",r"\vx",r")\right)\mid",r"\vx",r"\in D\}").tm({'x': RED, 'f': YELLOW, 'left': WHITE})
        graph_label = TexText("graph\ (图象)").set_color(YELLOW)
        VGroup(graph, graph_label).arrange(DOWN, buff=.5).fix_in_frame().to_edge(RIGHT, buff=.5)
        self.play(Write(graph)); self.wait()
        self.play(Write(graph_label)); self.wait()
        return super().construct()

class VectorFunction(Scene):
    def construct(self):
        plane = NumberPlane()
        plane.add_coordinate_labels()
        self.add(plane); self.wait()
        f = lambda x,y: (x,y)
        f_label = Tex(r"\vf(x,y)=\begin{bmatrix}x\\y\end{bmatrix}", color=YELLOW).add_background_rectangle().to_corner(UL)
        self.play(Write(f_label)); self.wait()
        f_label.add_updater(lambda t: self.add(t))

        x = ValueTracker(); y=ValueTracker()
        vector = Arrow(ORIGIN, UP).add_updater(
            lambda t: t.become(
                Arrow(
                    plane.c2p(x.get_value(), y.get_value()),
                    plane.c2p(
                        x.get_value()+f(x.get_value(), y.get_value())[0], y.get_value()+f(x.get_value(), y.get_value())[1]
                    ),
                    buff=0
                ).set_color(YELLOW)
            )
        )
        dot = Dot().set_color(RED).add_updater(lambda t: t.move_to(vector.get_start()))
        self.add(vector, dot)
        self.play(x.animate.set_value(3), y.animate.set_value(1), run_time=2)
        self.play(x.animate.set_value(-3), y.animate.set_value(-2), run_time=3)
        self.play(x.animate.set_value(2), y.animate.set_value(-1), run_time=3)
        vector.clear_updaters()
        self.play(FadeOut(vector), FadeOut(dot))
        field = VF(func=f, coordinate_system=plane, factor=.1, step_multiple=.5)
        self.play(FadeIn(field)); self.wait()
        
        div = Tex(r"\nabla\cdot\vf=\frac{\partial x}{\partial x}+\frac{\partial y}{\partial y}=2", color=YELLOW).next_to(f_label, buff=1).add_background_rectangle()
        self.play(Write(div)); self.wait()

        name = VGroup(TexText("divergence"), TexText("散度")).arrange(DOWN).set_color(RED).add_background_rectangle().next_to(div, DOWN)
        self.play(Write(name)); self.wait()

        self.play(FadeOut(VGroup(name)))
        dot = Dot(plane.c2p(2,-1)).set_color(RED)
        flux = TexText("``通量的局部描述''", color=RED).next_to(div, DOWN).add_background_rectangle()
        density = TexText("散度是通量的体密度", color=RED).add_background_rectangle().move_to(flux)
        self.play(FadeIn(dot, scale=2))
        self.play(Write(flux))
        self.wait()

        circle = Circle(arc_center=dot.get_center(), radius=1, color=RED)
        self.play(ShowCreation(circle))

        lines = StreamLines(
            coordinate_system=plane,
            func=lambda x, y: (x,y),
        )
        self.add(AnimatedStreamLines(
            lines,
            # line_anim_class=ShowPassingFlash
        ))
        self.wait(30)
        self.play(FadeOut(lines)); self.wait()
        self.play(circle.animate.scale(.1), run_time=3); self.wait()
        self.play(RT(flux, density)); self.wait()
        # return super().construct()


class DivConstant(Scene):
    def construct(self) -> None:
        plane = NumberPlane()
        field = VF(lambda x,y:(1.0,0), plane)
        f = Tex(r"\vf(x,y)=\begin{bmatrix}1\\0\end{bmatrix}", color=YELLOW).to_corner(UL).add_background_rectangle()
        div = Tex(r"\nabla\cdot\vf=0", color=YELLOW).next_to(f, buff=1).add_background_rectangle()
        self.add(field); self.wait()
        self.play(Write(f)); self.wait()
        self.play(Write(div)); self.wait()

        lines = StreamLines(
            coordinate_system=plane,
            magnitude_range=(0,3.0),
            func=lambda x, y: (1.0,0),
        )
        self.add(AnimatedStreamLines(
            lines,
            # line_anim_class=ShowPassingFlash
        ))
        dot = Dot(plane.c2p(2,0), color=RED)
        circle = Circle(arc_center=dot.get_center(), color=RED)
        self.play(FadeIn(dot, scale=2))
        self.play(ShowCreation(circle))
        self.wait()
        self.play(circle.animate.scale(.2), run_time=3)
        self.wait(10)
        return super().construct()


class DivPoint(Scene):
    def construct(self) -> None:
        plane = NumberPlane()
        def func(x,y):
            if get_norm([x,y]) > 0:
                return (x/(get_norm([x,y])), y/(get_norm([x,y])))
            else:
                return (0,0)
        field = VF(func, plane)
        self.add(field); self.wait()

        f = Tex(r"\vf(\vx)={\vx \over \lVert \vx \rVert ^2}", color=YELLOW).to_corner(UL).add_background_rectangle()
        div = Tex(r"\nabla\cdot\vf=0~(\vx\ne\vec{0})", color=YELLOW).next_to(f, buff=1).add_background_rectangle()
        self.add(field); self.wait()
        self.play(Write(f)); self.wait()
        self.play(Write(div)); self.wait()

        lines = StreamLines(
            coordinate_system=plane,
            magnitude_range=(0,0.5),
            func=func,
        )
        self.add(AnimatedStreamLines(
            lines,
            # line_anim_class=ShowPassingFlash
        ))
        self.wait(10)
        return super().construct()

class Nabla(Scene):
    def construct(self) -> None:
        nabla = Tex(r"\nabla=\left[{\partial\over\partial x_1},~ {\partial\over\partial x_2},~\ldots,~{\partial\over\partial x_n}\right]^T", color=YELLOW).to_edge(UP, buff=.5)
        self.play(Write(nabla))
        self.wait()

        image = ImageMobject("nabla", height=3).to_edge(LEFT, buff=3)
        self.play(FadeIn(image))
        self.wait()

        name = TexText("nabla / del").next_to(image, DOWN)
        self.play(Write(name))
        self.wait()

        grad = Tex(r"\nabla f=\begin{bmatrix}{\partial f\over\partial x_1}\\[5pt] {\partial f\over\partial x_2}\\ \vdots \\ {\partial f\over \partial x_n}\end{bmatrix}").scale(1.2).next_to(image, buff=1).align_to(name, DOWN)
        grad[0][0].set_color(YELLOW)
        VGroup(*[grad[0][i] for i in [1,10,16,25]]).set_color(RED)
        # self.add(Debug(grad[0]))
        self.play(Write(grad)); self.wait()
        return super().construct()

class Tone(Scene):
    def construct(self) -> None:
        div = ImageMobject("div", height=2).to_edge(UP)
        self.add(div); self.wait()

        san3 = ImageMobject("san3").next_to(ORIGIN, LEFT, buff=-0.1)
        san4 = ImageMobject("san4").next_to(ORIGIN, RIGHT, buff=-0.1)
        self.add(san3); self.wait()
        self.add(san4); self.wait()

        words = TexText(r"曲线\quad 曲面\quad 曲率", color=YELLOW).scale(1.5).next_to(san3, DOWN).set_x(0)
        dots = VGroup(*[Dot().next_to(words[0][i], DOWN) for i in [0,2,4]])
        # self.add(Debug(words[0]))
        self.play(FadeIn(words), FadeIn(dots))
        return super().construct()


class TestVectorField(Scene):
    def construct(self):
        plane = NumberPlane()
        self.add(plane); self.wait()
        lines = StreamLines(
            coordinate_system=plane,
            func=lambda x, y: (x,y),
        )
        self.add(AnimatedStreamLines(
            lines,
            line_anim_class=ShowPassingFlash
        ))
        self.wait(10)


class Gradient(Scene):
    def construct(self) -> None:
        plane = NumberPlane()
        plane.add_coordinate_labels()
        self.add(plane)

        f = lambda x,y: x**2+y**2
        f_label = Tex("f(x,y)=x^2+y^2", color=YELLOW).add_background_rectangle().to_corner(UL)
        self.add(f_label)
        unit = plane.get_x_axis().get_unit_size()
        circles = VGroup(*[Circle(radius=r*unit) for r in [4,3,2,1]])
        labels = VGroup(*[Tex(f"{r**2}.00").scale(.7) for r in [4,3,2,1]])
        for i in range(len(circles)):
                circles[i].set_color(interpolate_color(RED, GREEN, i / len(circles)))
                labels[i].move_to(circles[i].get_right()).set_color(circles[i].get_color()).add_background_rectangle()
        self.add(circles, labels)
        self.wait()

        gradient = Tex(r"\nabla f=\begin{bmatrix}2x\\2y\end{bmatrix}", color=YELLOW).add_background_rectangle().next_to(f_label, DOWN, aligned_edge=LEFT)
        self.play(Write(gradient))
        self.wait()

        x = ValueTracker(np.cos(PI/4)); y = ValueTracker(np.sin(PI/4))
        dot = Dot(color=YELLOW).add_updater(lambda t: t.move_to(plane.c2p(x.get_value(), y.get_value())))
        arrow = Arrow(dot.get_center(),
            plane.c2p(x.get_value()+2*x.get_value(), y.get_value()+2*y.get_value()),
            buff=0).set_color(YELLOW)
        self.play(FadeIn(dot))
        self.play(GrowArrow(arrow))
        arrow.add_updater(lambda t: t.become(
            Arrow(
            dot.get_center(),
            plane.c2p(x.get_value()+2*x.get_value(), y.get_value()+2*y.get_value()),
            buff=0
        ).set_color(YELLOW)
            )
        )
        self.wait()

        name = VGroup(TexText("gradient"), TexText("梯度")).arrange(DOWN).next_to(gradient, DOWN).add_background_rectangle()
        self.play(Write(name))
        self.wait()

        self.play(x.animate.set_value(2), y.animate.set_value(0), run_time=2)
        self.play(x.animate.set_value(np.cos(-3*PI/4)), y.animate.set_value(np.sin(-3*PI/4)), run_time=2)

        # field = VF(lambda x,y: (2*x,2*y), NumberPlane(x_range=(-3,3)), factor=.1, step_multiple=1).set_color(YELLOW)
        # self.play(FadeOut(arrow), FadeOut(dot), FadeIn(field))


        return super().construct()


class Div(Scene):
    def construct(self) -> None:
        nabla = Tex(r"\nabla=\begin{bmatrix}\frac{\partial}{\partial x_1}\\ \vdots \\ \frac{\partial}{\partial x_n}\end{bmatrix}", color=YELLOW)
        f = Tex(r"\vf=\begin{bmatrix}f_1\\ \vdots \\ f_n\end{bmatrix}", color=RED)
        VGroup(nabla, f).arrange(buff=.5).to_edge(UP, buff=1)
        self.play(Write(nabla)); self.wait()
        self.play(Write(f)); self.wait()

        div = Tex(r"\nabla",r"\cdot",r"\vf",r"={\partial f_1\over\partial x_1}+\cdots+{\partial f_n\over\partial x_n}").next_to(nabla, DOWN, buff=1).set_x(0).tm({'nabla': YELLOW, 'vf': RED})
        self.play(Write(div))
        return super().construct()


class Gauss(Scene):
    def construct(self) -> None:
        title = Title("散度是通量的体密度", color=YELLOW)
        self.add(title); self.wait()
        formula = Tex(r"\oiint_{\partial V} \vf\cdot\vn\d S",r"=",r"\iiint_V\nabla\cdot\vf\d V").scale(1.5)
        VGroup(formula[0][1:3], formula[-1][1]).set_color(RED)
        VGroup(formula[0][3:5], formula[-1][2:6]).set_color(YELLOW)

        brace1 = Brace(formula[0], DOWN)
        brace1.add(TexText("流过",r"边界的通量").tm({'V': RED}).next_to(brace1, DOWN))

        brace2 = Brace(formula[-1], DOWN)
        brace2.add(TexText(r"内部所有散度的贡献").tm({'V': RED}).next_to(brace2, DOWN))
        self.play(Write(formula[0])); self.wait()
        self.play(GrowFromCenter(brace1)); self.wait()

        self.play(Write(formula[1:])); self.wait()
        self.play(GrowFromCenter(brace2)); self.wait()
        # self.add(Debug(formula[0]), Debug(formula[-1]))
        gauss = TexText("Gauss公式", color=YELLOW).scale(1.3).next_to(formula, UP, buff=.5)
        self.play(Write(gauss)); self.wait()
        return super().construct()


class Curl(Scene):
    def construct(self) -> None:
        nabla = Tex(r"\nabla=\begin{bmatrix}\frac{\partial}{\partial x}\\[2mm] \frac{\partial}{\partial y} \\[2mm] \frac{\partial}{\partial z}\end{bmatrix}", color=YELLOW)
        f = Tex(r"\vf=\begin{bmatrix}f_1\\[2mm] f_2 \\[2mm] f_3\end{bmatrix}", color=RED)
        VGroup(nabla, f).arrange(buff=.5).to_edge(UP, buff=1)
        self.play(Write(nabla)); self.wait()
        self.play(Write(f)); self.wait()

        curl = VGroup(
            Tex(r"\nabla", r"\times", r"\vf", "=").tm({'nabla': YELLOW, 'f': RED}),
            Det(
                [['\\vi', '\\vj', '\\vk'],
                [r'\partial\over\partial x', r'\partial\over\partial y', r'\partial\over\partial z'],
                ['f_1', 'f_2', 'f_3']],
                v_buff = 1,
                element_alignment_corner = UP,
            ).set_row_colors(WHITE, YELLOW, RED),
            Tex(r"=\begin{bmatrix}\frac{\partial f_3}{\partial y}-\frac{\partial f_2}{\partial z}\\[2mm] \frac{\partial f_1}{\partial z}-\frac{\partial f_3}{\partial x}\\[2mm] \frac{\partial f_2}{\partial x}-\frac{\partial f_1}{\partial y}\end{bmatrix}")
            ).arrange().next_to(f, DOWN, buff=.5).set_x(0)
        row = curl[1].get_rows()[1]
        for ele in row:
            ele.scale(.8).shift(UP*.2)
        self.play(Write(curl[:-1])); self.wait()
        self.play(Write(curl[-1])); self.wait()
        self.wait()


class Curl1(Scene):
    def construct(self) -> None:
        plane = NumberPlane()
        # self.add(plane)
        f = Tex(r"\vf(x,y,z)=\begin{bmatrix}y\\-x\\0\end{bmatrix}", color=YELLOW).to_corner(UL).add_background_rectangle()
        curl = Tex(r"\nabla\times\vf=\begin{bmatrix}0\\0\\-2\end{bmatrix}", color=YELLOW).add_background_rectangle().next_to(f, buff=1)
        name = TexText(r"curl\ (旋度)").set_color(RED).add_background_rectangle().next_to(curl, buff=1)

        describe = TexText("``环量的局部描述''", color=RED).add_background_rectangle().next_to(curl, DOWN)

        # draw field
        field = VF(lambda x,y: (y,-x), plane)
        self.add(field, f); self.wait()
        self.play(Write(curl)); self.wait()
        self.play(Write(name)); self.wait()

        self.play(Write(describe)); self.wait()

        dot = Dot((2,-1,0)).set_color(GREEN)
        circle = Circle(radius=1, arc_center=dot.get_center(), color=GREEN)
        self.play(FadeIn(dot, scale=2))
        self.play(ShowCreation(circle))
        # lines
        lines = StreamLines(
            coordinate_system=plane,
            # magnitude_range=(0,0.5),
            func=lambda x,y:(y,-x),
        )
        self.add(AnimatedStreamLines(
            lines,
            # line_anim_class=ShowPassingFlash
        ))
        self.wait(20)
        self.play(circle.animate.scale(.1), run_time=3)
        self.wait(5)
        return super().construct()


class Curl2(Scene):
    def construct(self) -> None:
        plane = NumberPlane()
        # self.add(plane)
        f = Tex(r"\vf(x,y,z)=\begin{bmatrix}0\\-x^2\\0\end{bmatrix}", color=YELLOW).to_corner(UL).add_background_rectangle()
        curl = Tex(r"\nabla\times\vf=\begin{bmatrix}0\\0\\-2x\end{bmatrix}", color=YELLOW).add_background_rectangle().next_to(f, buff=1)

        # draw field
        field = VF(lambda x,y: (0,-x**2), plane).set_opacity(.5)
        self.add(field, f); self.wait()
        self.play(Write(curl)); self.wait()

        # dot = Dot((2,-1,0)).set_color(GREEN)
        # circle = Circle(radius=1, arc_center=dot.get_center(), color=GREEN)
        # self.play(FadeIn(dot, scale=2))
        # self.play(ShowCreation(circle))
        # lines
        lines = StreamLines(
            coordinate_system=plane,
            # magnitude_range=(0,0.5),
            func=lambda x,y:(0,-x**2),
        )
        self.add(AnimatedStreamLines(
            lines,
            # line_anim_class=ShowPassingFlash
        ))

        fac=.5
        coins = VGroup(*[
            Coin().scale(fac).move_to((i,0,0)).add_updater(lambda x,dt: x.rotate(0)) for i in range(-6,7,2)
            ])
        # for i in range(len(coins)):
        #     coins[i].add_updater(lambda x,dt: x.rotate(-2*coins[i].get_x()*PI*dt))
        coins[0].add_updater(lambda x,dt: x.rotate(3*dt*PI))
        coins[1].add_updater(lambda x,dt: x.rotate(2*dt*PI))
        coins[2].add_updater(lambda x,dt: x.rotate(dt*PI))
        # coins[3].add_updater(lambda x,dt: x.rotate(-dt*PI))
        coins[4].add_updater(lambda x,dt: x.rotate(-dt*PI))
        coins[5].add_updater(lambda x,dt: x.rotate(-2*dt*PI))
        coins[6].add_updater(lambda x,dt: x.rotate(-3*dt*PI))
        # for coin in coins:
        #     coin.add_updater(lambda x,dt: x.rotate(-2*coin.get_x()*dt*PI))
        # self.wait()
        # self.play(FadeIn(coin0))
        self.play(FadeIn(coins))
        self.wait(50)

        # coin1 = Coin().scale(fac).move_to((4,0,0)).add_updater(lambda x,dt: x.rotate(-4*dt*PI))
        # self.play(FadeIn(coin1))
        # self.wait(5)


class Stokes(Scene):
    def construct(self) -> None:
        title = Title("旋度是环量的面密度", color=YELLOW)
        self.add(title); self.wait()
        formula = Tex(r"\oint_{\partial S} \vf\cdot\d \vec{\bm{r}}",r"=",r"\iint_S\nabla\times\vf\cdot\d \vec{\bm{S}}").scale(1.5)
        VGroup(formula[0][1:3], formula[-1][1]).set_color(RED)
        VGroup(formula[0][3:5], formula[-1][2:6]).set_color(YELLOW)

        brace1 = Brace(formula[0], DOWN)
        brace1.add(TexText(r"围绕边界的环量").tm({'V': RED}).next_to(brace1, DOWN))

        brace2 = Brace(formula[-1], DOWN)
        brace2.add(TexText(r"曲面上旋度的贡献").tm({'V': RED}).next_to(brace2, DOWN))
        self.play(Write(formula[0])); self.wait()
        self.play(GrowFromCenter(brace1)); self.wait()

        self.play(Write(formula[1:])); self.wait()
        self.play(GrowFromCenter(brace2)); self.wait()
        # self.add(Debug(formula[0]), Debug(formula[-1]))
        stokes = TexText("Stokes公式", color=YELLOW).scale(1.3).next_to(formula, UP, buff=.5)
        self.play(Write(stokes)); self.wait()


class Laplace(Scene):
    def construct(self) -> None:
        nabla = Tex(r"\nabla=\begin{bmatrix}\frac{\partial}{\partial x_1}\\ \vdots \\ \frac{\partial}{\partial x_n}\end{bmatrix}", color=YELLOW)
        squared = Tex(r"\nabla^T\nabla=\frac{\partial^2}{\partial x_1^2}+\cdots+\frac{\partial^2}{\partial x_n^2}")
        VGroup(nabla, squared).arrange(buff=1).to_edge(UP)

        f = MTex(r"\nabla^2 f ={\partial^2 f \over\partial x_1^2}+\cdots+{\partial^2 f\over\partial x_n^2}", isolate=['f']).tm({'f': RED, 'nabla': YELLOW}).next_to(nabla, DOWN).set_x(0)
        f[0:2].set_color(YELLOW)
        self.play(Write(nabla)); self.wait()
        self.play(Write(squared)); self.wait()
        self.play(Write(f)); self.wait()

        hessian = Tex(r"\nabla^2",r"=",r"\nabla\nabla^T",r"=\begin{bmatrix}\frac{\partial^2}{\partial x_1^2}&\cdots&\frac{\partial^2}{\partial x_1\partial x_n}\\ \vdots & \ddots & \vdots \\ \frac{\partial^2}{\partial x_n \partial x_1}&  \cdots & \frac{\partial^2}{\partial x_n^2}\end{bmatrix}").next_to(f, DOWN, buff=.5).tm({'nabla': YELLOW})
        hessian_label = TexText("Hessian", color=YELLOW).next_to(hessian, buff=.5)
        self.play(Write(hessian)); self.wait()
        self.play(Write(hessian_label)); self.wait()

        laplace = Tex(r"\Delta=\nabla\cdot\nabla", color=GREEN).next_to(f[0], LEFT, buff=1, aligned_edge=UP)
        box = SurroundingRectangle(laplace, color=GREEN)
        laplace_label = TexText("Laplace算子", color=GREEN).next_to(box, DOWN, buff=.2)
        self.play(Write(laplace)); self.play(ShowCreation(box)); self.wait()
        self.play(Write(laplace_label)); self.wait()

        return super().construct()


class Pic(Scene):
    def construct(self) -> None:
        plane = NumberPlane()
        f = lambda x,y: (x,y)
        field = VF(func=f, coordinate_system=plane, factor=.1, step_multiple=.5)

        div = Tex(r"\nabla\cdot\vf=2", color=YELLOW, stroke_width=5).scale(4.5).add_background_rectangle(opacity=1)
        self.add(field,div)