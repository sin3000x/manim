from jeremy.old_shaders.frechet import NotImply
from manimlib import *


class Opening(Scene):
    def construct(self) -> None:
        axes = Axes(
            axis_config=dict(include_ticks=False, include_tip=True),
            x_range=(-2.5, 2.5)
        ).shift(LEFT_SIDE / 2)

        func = lambda x: (x + 1) ** 4 - 3 * (x + 1) ** 3 + 4 * (x + 1) - 1
        stationary = (-0.59307 - 1, 0.84307 - 1, 2 - 1)
        graph = axes.get_graph(func, color=BLUE)
        graph2 = axes.get_graph(lambda x: x ** 3, color=BLUE)
        dots = VGroup(
            *[Dot().move_to(axes.c2p(s, func(s))).set_color(YELLOW) for s in stationary]
        )
        dots2 = Dot().move_to(axes.c2p(0, 0)).set_color(YELLOW)
        lines = VGroup(
            *[Line(LEFT, RIGHT, color=YELLOW).move_to(axes.c2p(s, func(s))) for s in stationary]
        )
        lines2 = Line(LEFT, RIGHT, color=YELLOW).move_to(axes.c2p(0, 0))
        stationary_label = Tex(r"\nabla f(\vx)=0", color=RED).to_edge(DOWN, buff=1)
        saddle = VGroup(
            TexText("saddle point"),
            TexText("鞍点")
        ).arrange(DOWN).set_color(YELLOW).to_edge(UP, buff=1)
        extrema = TexText("极值点", color=YELLOW).next_to(stationary_label, UP, buff=1.5)
        notim = VGroup(Tex("\\rightarrow"), Tex("\\nleftarrow")).arrange(DOWN, buff=0).stretch(2, 0).move_to(
            mid(stationary_label.get_center(), extrema.get_center())).rotate(-PI / 2)
        for mob in [axes, graph, graph2, dots, dots2, lines, lines2, stationary_label, saddle, extrema, notim]:
            mob.fix_in_frame()

        axes3d = ThreeDAxes(z_axis_config=dict(include_ticks=False, include_tip=True), x_range=(-3, 3), y_range=(-3, 3),
                            z_range=(-2, 2))
        frame = self.camera.frame
        frame.shift(LEFT * 3.5)
        # frame.add_updater(lambda m, dt: m.increment_theta(-0.1 * dt))
        frame.set_euler_angles(
            theta=0 * DEGREES,
            phi=90 * DEGREES,
            gamma=0 * DEGREES,
        )
        graph3d = axes3d.get_graph(lambda x, y: 1 - x ** 2 - y ** 2)
        graph3d2 = axes3d.get_graph(lambda x, y: x * y, u_range=[-1.5, 1.5], v_range=[-1.5, 1.5])
        plane = axes3d.get_graph(lambda x, y: 1, color=YELLOW, opacity=.6)
        plane2 = axes3d.get_graph(lambda x, y: 0, color=YELLOW, opacity=.6)
        dot3d = Sphere(radius=0.1, opacity=1, color=YELLOW).move_to(axes3d.c2p(0, 0, 1))
        dot3d2 = Sphere(radius=0.1, opacity=1, color=YELLOW).move_to(axes3d.c2p(0, 0, 0))

        self.add(axes, axes3d)
        self.play(FadeIn(graph), FadeIn(graph3d))
        self.wait()
        self.play(
            LaggedStartMap(ShowCreation, lines), LaggedStartMap(FadeIn, dots, scale=.5),
            FadeIn(dot3d, scale=.5), ShowCreation(plane)
        )
        self.wait()
        self.play(Write(stationary_label))
        self.wait()

        self.play(*[FadeOut(mob) for mob in (dots, dot3d, lines, plane)])
        self.play(ReplacementTransform(graph, graph2), ReplacementTransform(graph3d, graph3d2), run_time=2)
        self.play(
            ShowCreation(lines2), FadeIn(dots2, scale=.5),
            FadeIn(dot3d2, scale=.5), ShowCreation(plane2)
        )
        dot3d2.add_updater(lambda x: self.add(x))
        self.wait()
        self.play(Write(saddle))
        self.wait()

        self.play(Write(extrema))
        self.play(Write(notim))
        self.wait()


class Constraint(Scene):
    def construct(self) -> None:
        t2c = {r'f(\vx)': YELLOW, r'c(\vx)': RED}
        f = Tex(r"\mathrm{minimize}~ f(\vx)", t2c=t2c, font_size=70).next_to(ORIGIN, UP, buff=1)
        equiv = Tex(r"\text{maximize}~ f(\vx)\Longleftrightarrow\text{minimize}~ -f(\vx)", t2c=t2c, font_size=70)
        c = Tex(r"\text{subject to}~c(\vx)=0", t2c=t2c, font_size=70)
        self.play(Write(f))
        self.wait()
        self.play(Write(equiv))
        self.wait()
        self.play(FadeOut(equiv))
        self.wait()
        self.play(Write(c))
        self.wait()


class Example3D(Scene):
    def construct(self) -> None:
        label = Tex(r"f(x,y)=x+y", color=BLUE).to_edge(UP, buff=1).shift(LEFT*4).fix_in_frame()
        const = Tex(r"\text{s.t. } x^2+y^2=1", t2c={"x^2+y^2=1": RED}).next_to(label, DOWN).shift(LEFT*0).fix_in_frame()
        axes = ThreeDAxes(x_range=[-2, 2], y_range=[-2, 2])
        plane = axes.get_graph(lambda x, y: x + y)
        # plane.mesh = SurfaceMesh(plane, resolution=(30,30), flat_stroke=True)
        cylinder = Cylinder(height=3, color=RED, opacity=.5)
        curve = axes.get_parametric_curve(lambda t: [np.cos(t), np.sin(t), np.cos(t)+np.sin(t)], color=YELLOW, t_range=[0, TAU, .01])

        frame = self.camera.frame
        frame.set_euler_angles(
            theta=-30 * DEGREES,
            phi=80 * DEGREES,
        )

        self.add(axes)
        self.play(Write(label))
        self.play(ShowCreation(plane), run_time=2)
        self.wait()
        self.play(Write(const))
        self.wait()
        self.play(ShowCreation(cylinder))
        frame.add_updater(lambda m, dt: m.increment_theta(-0.2 * dt))
        self.wait()
        self.play(ShowCreation(curve))
        self.wait(60)


def except_for(length, exclude):
    return it.chain(range(exclude), range(exclude+1, length))


class Contour(Scene):
    def construct(self) -> None:
        numbers = np.arange(-3, 3.5, 0.5)
        UNIT = 4
        plane = NumberPlane(x_range=(-8, 8, UNIT), y_range=(-4, 4, UNIT))
        lines = VGroup(*[plane.get_graph(lambda x: num*UNIT - x) for num in numbers])
        labels = VGroup(*[Tex(str(num)).move_to(plane.c2p((num + 0.8)*UNIT, -0.8*UNIT)) for num in numbers])
        circle = Circle(radius=UNIT, stroke_color=BLUE)
        for i in range(len(lines)):
            lines[i].set_color(interpolate_color(GREEN, RED, i/len(lines)))
            labels[i].set_color(lines[i].get_color()).add_background_rectangle()
        f_label = Tex("f(x,y)=x+y", color=YELLOW).add_background_rectangle().to_edge(UR)
        c_label = Tex("c(x,y)=x^2+y^2-1=0", color=circle.get_color()).add_background_rectangle().to_edge(UL)
        grad_f = Tex(r"\nabla f=(1, 1)^T", color=f_label.get_color()).add_background_rectangle().next_to(f_label, DOWN, aligned_edge=RIGHT)
        grad_c = Tex(r"\nabla c=(2x,2y)^T", color=c_label.get_color()).add_background_rectangle().next_to(c_label, DOWN, aligned_edge=LEFT)
        self.add(plane)
        self.wait()
        self.play(LaggedStartMap(ShowCreation, lines), Write(f_label))
        self.play(FadeIn(labels))
        self.wait()

        # explain lines
        for i in range(len(numbers)):
            lines[i].save_state()
            labels[i].save_state()
        self.play(
            *[lines[i].animate.set_opacity(0.2) for i in except_for(len(numbers), 6)],
            *[labels[i].animate.set_opacity(0.2) for i in except_for(len(numbers), 6)]
        )
        xy0 = Tex("x+y=0", color=YELLOW).move_to(UL * 3)
        self.play(Write(xy0))
        self.wait()
        xy_1 = Tex("x+y=-1", color=YELLOW).next_to(xy0, LEFT, buff=.5)
        self.play(Restore(lines[4]), Restore(labels[4]), TransformMatchingTex(xy0, xy_1))
        self.wait()

        self.play(FadeOut(xy_1), *[Restore(line) for line in lines], *[Restore(label) for label in labels])
        self.wait()

        # circle and gradient
        self.play(ShowCreation(circle), FadeOut(labels), lines.animate.set_opacity(.4))
        self.wait()
        self.play(Write(c_label))
        self.wait()
        self.play(Write(grad_f))
        self.play(Write(grad_c))
        self.wait()
        grad_f_vector = Vector((1, 1), stroke_color=YELLOW)
        grad_c_vector = Arrow(
            start=(UNIT*np.cos(-30*DEGREES), UNIT*np.sin(-30*DEGREES)),
            end=(6*np.cos(-30*DEGREES), 6*np.sin(-30*DEGREES)),
            stroke_color=BLUE,
            buff=0
        )
        self.play(GrowArrow(grad_f_vector))
        self.play(GrowArrow(grad_c_vector))
        self.wait()

        vec_start = grad_c_vector.get_start()
        dot = Dot().move_to(vec_start)
        self.play(FadeIn(dot))
        self.wait()

        ascent_vectors = VGroup(
            *[Arrow(vec_start, vec_start+RIGHT, buff=0).set_angle(angle * DEGREES) for angle in np.linspace(-110, 50, 10)]
        )
        self.play(LaggedStartMap(GrowArrow, ascent_vectors))
        self.wait()

        descent_vectors = VGroup(
            *[Arrow(vec_start, vec_start+RIGHT, buff=0).set_angle(angle * DEGREES) for angle in np.linspace(70, 230, 10)]
        )
        self.play(FadeOut(ascent_vectors))
        self.play(LaggedStartMap(GrowArrow, descent_vectors))
        self.wait()

        tangent_vectors = VGroup(
            *[Arrow(vec_start, vec_start+RIGHT, buff=0).set_angle(angle * DEGREES) for angle in (60, 240)]
        )
        grad_f_vector1 = Arrow(vec_start, vec_start+UR, buff=0, stroke_color=YELLOW)
        self.play(FadeOut(descent_vectors))
        self.play(LaggedStartMap(GrowArrow, tangent_vectors))
        self.wait()

        taylor = Tex(r"f(\vx+\vdelta)\approx f(\vx)+\nabla f(\vx)^T\vdelta", color=YELLOW).add_background_rectangle().shift(DOWN)
        self.play(Write(taylor))
        self.wait()
        self.play(FadeOut(taylor))
        self.wait()

        # investigate two points
        self.play(ShowCreation(grad_f_vector1))
        self.wait()
        self.play(WiggleOutThenIn(tangent_vectors[1], scale_value=2, n_wiggles=12, run_time=3))
        self.play(WiggleOutThenIn(tangent_vectors[1], scale_value=2, n_wiggles=12, run_time=3))
        self.wait()

        self.play(FadeOut(tangent_vectors), FadeOut(grad_f_vector1))
        grad_c_vector1 = Arrow(LEFT * UNIT, LEFT * (UNIT + 2), buff=0, stroke_color=BLUE)
        self.play(
            dot.animate.move_to(UNIT * LEFT),
            ReplacementTransform(grad_c_vector, grad_c_vector1),
            run_time=2
        )
        self.wait()
        tangent_vectors = VGroup(
            Arrow(LEFT * 4, LEFT * 4 + UP, buff=0),
            Arrow(LEFT * 4, LEFT * 4 + DOWN, buff=0),
        )
        grad_f_vector1 = Arrow(LEFT * 4, LEFT * 4 + UR, stroke_color=YELLOW, buff=0)
        self.play(LaggedStartMap(GrowArrow, tangent_vectors))
        self.wait()
        self.play(GrowArrow(grad_f_vector1))
        self.wait()
        self.play(WiggleOutThenIn(tangent_vectors[1], scale_value=2, n_wiggles=12, run_time=3))
        self.play(WiggleOutThenIn(tangent_vectors[1], scale_value=2, n_wiggles=12, run_time=3))
        self.wait()

        # explain what we need
        statement = TexText(r"$\perp\nabla c$的方向，不能与$\nabla f$夹锐角或钝角.", t2c={'\\nabla c': BLUE, '\\nabla f': YELLOW}).to_edge(DOWN, buff=1)#.add_background_rectangle()
        statement_perp = TexText(r"$\perp\nabla c$的方向，也$\perp\nabla f$.", t2c={'\\nabla c': BLUE, '\\nabla f': YELLOW}).to_edge(DOWN, buff=1)#.add_background_rectangle()
        parallel = Tex(r"\nabla f~/\kern -0.8em /~\nabla c", t2c={'\\nabla c': BLUE, '\\nabla f': YELLOW}, font_size=72).to_edge(DOWN, buff=1).add_background_rectangle()
        self.play(Write(statement))
        self.wait()

        self.play(ReplacementTransform(statement[:7], statement_perp[:7]), ReplacementTransform(statement[7:], statement_perp[7:]))
        self.wait()

        self.play(FadeOut(statement_perp))
        self.play(Write(parallel))
        self.wait()

        self.play(
            *[FadeOut(mob) for mob in (parallel, grad_f_vector, grad_f_vector1, tangent_vectors, grad_c_vector1, dot,
                                       f_label, grad_f, c_label, grad_c)]
        )
        dot1 = Dot(UNIT/np.sqrt(2) * DL)
        dot2 = Dot(UNIT/np.sqrt(2) * UR)
        grad_c_vector1 = Arrow(dot1.get_center(), dot1.get_center() + DL * 1.2, buff=0, stroke_color=BLUE)
        grad_c_vector2 = Arrow(dot2.get_center(), dot2.get_center() + UR * 1.2, buff=0, stroke_color=BLUE)
        grad_f_vector1 = Arrow(dot1.get_center(), dot1.get_center()+UR, buff=0, stroke_color=YELLOW)
        grad_f_vector2 = Arrow(dot2.get_center(), dot2.get_center()+UR, buff=0, stroke_color=YELLOW)
        tangent_vectors1 = VGroup(Arrow(dot1.get_center(), dot1.get_center() + UL, buff=0), Arrow(dot1.get_center(), dot1.get_center() + DR, buff=0))
        tangent_vectors2 = VGroup(Arrow(dot2.get_center(), dot2.get_center() + UL, buff=0), Arrow(dot2.get_center(), dot2.get_center() + DR, buff=0))
        self.play(FadeIn(dot1, scale=2), FadeIn(dot2, scale=2))
        self.play(GrowArrow(grad_c_vector1), GrowArrow(grad_f_vector1), GrowArrow(grad_c_vector2), GrowArrow(grad_f_vector2))
        self.wait()
        self.play(LaggedStartMap(GrowArrow, tangent_vectors1), LaggedStartMap(GrowArrow, tangent_vectors2))
        self.wait()
        self.play(
            *[FadeOut(mob) for mob in (dot1, dot2,grad_c_vector1, grad_c_vector2, grad_f_vector1, grad_f_vector2, tangent_vectors1, tangent_vectors2)]
        )

        # another perspective: tangent contours
        value = ValueTracker()
        line = always_redraw(
            plane.get_graph, lambda x: value.get_value() * UNIT - x, color=YELLOW
        )
        line1 = plane.get_graph(lambda x: np.sqrt(2) * UNIT - x, color=line.get_color())
        value_label = DecimalNumber(color=line.get_color()).add_updater(lambda t: t.set_value(value.get_value()))
        value_label.add_updater(lambda t: t.next_to(RIGHT * value.get_value() * UNIT, buff=.5))
        self.play(FadeIn(line))
        self.play(Write(value_label))
        self.wait()
        self.play(value.animate.set_value(.1))
        self.wait()
        self.play(value.animate.set_value(-.1))
        self.wait()
        self.play(value.animate.set_value(np.sqrt(2)), run_time=3)
        self.add(line1)
        self.play(value.animate.set_value(-np.sqrt(2)), run_time=3)
        self.wait()

        self.play(
            FadeIn(grad_c_vector1), FadeIn(grad_f_vector1), FadeIn(dot1),
            FadeIn(grad_c_vector2), FadeIn(grad_f_vector2), FadeIn(dot2),
        )
        self.wait()

        coord1 = Tex(r"\left({\sqrt2\over2}, {\sqrt2\over2}\right)").next_to(dot2, DL, buff=.1)
        coord2 = Tex(r"\left(-{\sqrt2\over2}, -{\sqrt2\over2}\right)").next_to(dot1, LEFT)
        self.play(Write(coord1), Write(coord2))
        self.wait()


class Stationary(Scene):
    def construct(self) -> None:
        cm = {'\\nabla c(\\vx)': BLUE, '\\nabla f(\\vx)': YELLOW}
        parallel = Tex(r"\nabla f(\vx)~/\kern -0.8em /~\nabla c(\vx)", t2c=cm, font_size=70)
        lamb = Tex(r"\nabla f(\vx)=\lambda\nabla c(\vx)", t2c=cm, font_size=70)
        constraint = Tex(r"c(\vx)=0", font_size=70, t2c={'c(\\vx)': BLUE})
        stationary = TexText(r"$f(\vx)$在约束$c(\vx)=0$下的``驻点''.", t2c={'f(\\vx)': YELLOW, 'c(\\vx)': BLUE}, font_size=70)
        VGroup(VGroup(parallel, constraint).arrange(DOWN, buff=.5), stationary).arrange(DOWN, buff=1)
        lamb.move_to(parallel)
        constraint.align_to(lamb, LEFT)
        brace = Brace(VGroup(lamb, constraint), LEFT)
        self.play(Write(parallel))
        self.wait()
        self.play(TransformMatchingTex(parallel, lamb))
        self.wait()
        self.play(Write(constraint))
        self.play(GrowFromCenter(brace))
        self.wait()
        self.play(Write(stationary))
        self.wait()


class StationaryCompare(Scene):
    def construct(self) -> None:
        cm = {'f(\\vx)': YELLOW, '\\nabla f(\\vx)': YELLOW, 'c(\\vx)': RED, '\\nabla c(\\vx)': RED, }
        unconstr = TexText(r"$f(\vx)$ 的驻点：$\nabla f(\vx)=0$.", t2c=cm).to_edge(UP, buff=1)
        unconstr_explain = TexText("\\kaishu $f(\\vx)$沿各个方向的导数$=0$.", color=BLUE).next_to(unconstr, DOWN, buff=.5)

        constr = TexText(r"$f(\vx)$ s.t. $c(\vx)=0$ 的驻点："
                         r"$\begin{cases}\nabla f(\vx)=\lambda \nabla c(\vx)\\c(\vx)=0\end{cases}$", t2c=cm).next_to(unconstr_explain, DOWN, buff=1)
        constr_explain = TexText("\\kaishu $f(\\vx)$沿可行方向的导数$=0$.", color=BLUE).next_to(constr, DOWN, buff=.5)
        brace1 = Brace(constr_explain[:5], DOWN)
        brace1.text = Tex(r"\nabla f~/\kern -0.8em /~\nabla c", t2c={'\\nabla f': YELLOW, '\\nabla c': RED}).next_to(brace1, DOWN)
        brace2 = Brace(constr_explain[6:10], DOWN).align_to(brace1, DOWN)
        brace2.text = Tex(r"\perp\nabla c", t2c={'\\nabla c': RED}).next_to(brace2, DOWN)
        self.play(Write(unconstr))
        self.wait()
        self.play(Write(constr))
        self.wait()
        self.play(Write(unconstr_explain))
        self.wait()
        self.play(Write(constr_explain))
        self.wait()
        self.play(GrowFromCenter(brace1))
        self.play(Write(brace1.text))
        self.wait()
        self.play(GrowFromCenter(brace2))
        self.play(Write(brace2.text))
        self.wait()


class LagrangeFunction(Scene):
    def construct(self) -> None:
        cm = {'f(\\vx)': YELLOW, '\\nabla f(\\vx)': YELLOW, 'c(\\vx)': RED, '\\nabla c(\\vx)': RED, r'L(\vx,\lambda)': BLUE, r'\nabla L=0': BLUE}
        L = Tex(r"L(\vx,\lambda)=f(\vx)-\lambda c(\vx)", t2c=cm).to_edge(UP, buff=1)
        grad = Tex(r"\nabla L=0\Longleftrightarrow\begin{cases}\nabla f(\vx)=\lambda \nabla c(\vx)\\c(\vx)=0\end{cases}", t2c=cm).shift(DOWN)
        L_arrow = Arrow(ORIGIN, UP).next_to(L[:7], DOWN)
        lambda_arrow = Arrow(ORIGIN, UP).next_to(L[14], DOWN).align_to(L_arrow, DOWN)
        lambda_arrow.text = TexText(r"Lagrange\\multiplier").next_to(lambda_arrow, DOWN)
        L_arrow.text = TexText(r"Lagrange\\function").next_to(L_arrow, DOWN)
        method = TexText("拉格朗日乘数/乘子法").next_to(grad, DOWN, buff=.5)
        self.play(Write(L))
        self.wait()
        self.play(ShowCreationThenDestructionAround(L[13], stroke_width=5))
        self.play(ShowCreationThenDestructionAround(L[13], stroke_width=5))
        self.wait()
        self.play(Write(grad))
        self.wait()
        self.play(GrowArrow(L_arrow))
        self.play(Write(L_arrow.text))
        self.wait()
        self.play(GrowArrow(lambda_arrow))
        self.play(Write(lambda_arrow.text))
        self.wait()
        self.play(Write(method))
        self.wait()


class SolveExample(Scene):
    def construct(self) -> None:
        cm = {'f(x,y)': YELLOW, '\\nabla f(x,y)': YELLOW, 'c(x,y)': RED, '\\nabla c(x,y)': RED,}
        prob = TexText(r"minimize $f(x,y)=x+y$, s.t. $c(x,y)=x^2+y^2-1=0$",
                       t2c={'f(x,y)=x+y': YELLOW, 'c(x,y)=x^2+y^2-1=0': RED}).to_edge(UP, buff=1)
        condition = Tex(r"\begin{cases}\nabla f(x,y)=\lambda \nabla c(x,y)\\c(x,y)=0\end{cases}", t2c=cm).next_to(prob, DOWN, buff=.5)
        this_condition = Tex(r"\begin{cases}\begin{bmatrix}1\\1\end{bmatrix}="
                             r"\lambda \begin{bmatrix}2x\\2y\end{bmatrix}\\[3ex]x^2+y^2=1\end{cases}",
                             t2c={r'\begin{bmatrix}1\\1\end{bmatrix}': YELLOW,
                                  r"\begin{bmatrix}2x\\2y\end{bmatrix}": RED,
                                  r'x^2+y^2=1': RED
                                  }).next_to(condition, DOWN, buff=.5).align_to(condition, LEFT)
        solution = Tex(r"\Longrightarrow\begin{bmatrix}x\\y\end{bmatrix}="
                       r"\pm\begin{bmatrix}{\sqrt2\over2}\\[0.7em]{\sqrt2\over2}\end{bmatrix}", color=BLUE)\
            .next_to(this_condition, buff=.5)
        self.play(Write(prob))
        self.wait()
        self.play(Write(condition))
        self.wait()
        self.play(ReplacementTransform(condition.copy(), this_condition))
        self.wait()
        self.play(Write(solution))
        self.wait()


class Theorem(Scene):
    def construct(self) -> None:
        cm = {'f': YELLOW, 'f(\\vx)': YELLOW, '\\nabla f(\\vx^*)': YELLOW, '\\nabla c(\\vx^*)': RED, 'c(\\vx)': RED, 'c(\\vx^*)': RED}
        condition = TexText(r"设$f,c\in C^1$, $f(\vx)$ s.t. $c(\vx)=0$在$\vx^*$处取到极值,", t2c=cm).to_edge(UP, buff=1)
        condition[3].set_color(RED)
        condition2 = TexText(r"并且\_\_\_\_\_\_\_").next_to(condition, DOWN, aligned_edge=LEFT, buff=.5)
        condition_true = TexText(r"并且$\nabla c(\vx^*)\ne0$,", t2c=cm).move_to(condition2).align_to(condition2, LEFT)
        conclusion = TexText(r"那么存在一个常数 $\lambda\in\R$, s.t. "
                             r"$\begin{cases}\nabla f(\vx^*)=\lambda \nabla c(\vx^*)\\c(\vx^*)=0\end{cases}$.", t2c=cm)\
            .next_to(condition2, DOWN, aligned_edge=LEFT)
        span = Tex(r'\nabla f(\vx^*)=\lambda_1 \nabla c_1(\vx^*)+\cdots+\lambda_n \nabla c_n(\vx^*)', color=BLUE).next_to(conclusion, DOWN, buff=1)
        licq = TexText(r'$\nabla c_1(\vx^*),\ldots,\nabla c_n(\vx^*)$线性无关', color=BLUE).next_to(condition_true)
        self.play(Write(condition))
        self.wait()
        self.play(Write(conclusion), run_time=2)
        self.wait()
        self.play(Write(condition2))
        self.wait()
        self.play(TransformMatchingStrings(condition2, condition_true, matched_keys=['并且']))
        self.wait()
        self.play(ShowCreationThenDestructionAround(condition_true[2:-1], stroke_width=5))
        self.play(ShowCreationThenDestructionAround(condition_true[2:-1], stroke_width=5))
        self.wait()

        self.play(Write(span))
        self.wait()
        self.play(Write(licq))
        self.wait()


class Proof(Scene):
    def construct(self) -> None:
        cm = {'c(x,y)': RED, 'f(x,y)': YELLOW, 'f(x,y(x))': YELLOW, "f'(x^*)": YELLOW, 'y=y(x)': RED}
        constraint = Tex(r"c(x,y)=0\Longrightarrow y=y(x)", t2c=cm).to_edge(UP, buff=1)
        implicit = Tex(r"c(x,y)=0\Longrightarrow y=y(x)\text{ 在~} (x^*,y^*) \text{ 附近存在,}", t2c=cm).move_to(constraint)
        y_dash = Tex(r"\text{隐函数定理:~~}y'=-{c_x'\over c_y'}", t2c={r"y'=-{c_x'\over c_y'}": RED}).next_to(implicit, DOWN)
        univariate = Tex(r"f(x,y)=f(x,y(x))\Longrightarrow f'(x^*)=0", t2c=cm).next_to(y_dash, DOWN)
        partial = TexText(r"再利用$\displaystyle{\partial f\over\partial x}=f_x'+f_y'\cdot y'(x)$, 在$(x^*,y^*)$处",
                      t2c={"y'(x)": RED, r"{\partial f\over\partial x}": YELLOW, "f_x'": YELLOW, "f_y'": YELLOW})\
            .next_to(univariate, DOWN)
        partial2 = Tex(r"f_x'-f_y'\cdot{c_x'\over c_y'}=0\Longrightarrow\begin{cases}f_x'=\lambda c_x'\\f_y'=\lambda c_y'\end{cases}",
                       t2c={"f_x'": YELLOW, "f_y'": YELLOW, "c_x'": RED, "c_y'": RED}).next_to(partial, DOWN)
        arrow = Arrow(ORIGIN, LEFT, stroke_color=BLUE).next_to(y_dash[14:])
        arrow.text = Tex(r"c_y'(x^*,y^*)\ne0", color=BLUE).next_to(arrow)
        x_y = Tex(r"x=x(y)", color=BLUE).next_to(implicit[10:16], UP)
        self.play(Write(constraint))
        self.wait()
        self.play(Write(univariate))
        self.wait()
        self.play(Indicate(constraint[10:]))
        self.wait()
        self.play(TransformMatchingStrings(constraint, implicit, matched_keys=[r"c(x,y)=0\Longrightarrow y=y(x)"]))
        self.wait()
        self.play(Write(y_dash))
        self.wait()
        self.play(Write(partial[:23]))
        self.wait()
        self.play(Write(partial[23:]))
        self.wait()
        self.play(Write(partial2[:17]))
        self.wait()
        self.play(Write(partial2[17:]))
        self.wait()
        self.play(GrowArrow(arrow))
        self.play(Write(arrow.text))
        self.wait()
        self.play(Write(x_y))
        self.wait()


class CounterExample(Scene):
    def construct(self) -> None:
        cm = {'f(x,y)': YELLOW, '\\nabla f(0,0)': YELLOW, 'c(x,y)': RED, '\\nabla c(0,0)': RED, }
        prob = TexText(r"minimize $f(x,y)=x+y$, s.t. $c(x,y)=x^2+y^2=0$",
                       t2c={'f(x,y)=x+y': YELLOW, 'c(x,y)=x^2+y^2=0': RED}).to_edge(UP, buff=1)
        x_star = Tex(r"(x^*,y^*)=(0,0)").next_to(prob, DOWN)
        lag = Tex(r"\nabla f(0,0)\ne\lambda\nabla c(0,0)", t2c=cm).next_to(x_star, DOWN, buff=.5)
        gradf = Tex(r"\begin{bmatrix}1\\1\end{bmatrix}", color=YELLOW).next_to(lag[1:7], DOWN)
        gradc = Tex(r"\begin{bmatrix}0\\0\end{bmatrix}", color=RED).next_to(lag[11:], DOWN)

        self.play(Write(prob))
        self.wait()
        self.play(Write(x_star))
        self.wait()
        self.play(Write(lag))
        self.wait()
        self.play(Write(gradf))
        self.wait()
        self.play(Write(gradc))
        self.wait()


class CounterExample2(Scene):
    def construct(self) -> None:
        prob = TexText(r"minimize $f(x,y)=x$, s.t. $c(x,y)=y^2+x^4-x^3=0$",
                       t2c={'f(x,y)=x': YELLOW, 'c(x,y)=y^2+x^4-x^3=0': RED}).to_edge(UP, buff=1)
        axes = Axes(
            x_range=(0, 1.2),
            y_range=(-0.5, 0.5),
            width=4,
            height=4,
            axis_config=dict(include_tip=True),
        ).next_to(prob, DOWN, buff=1).to_edge(LEFT, buff=1.5)
        zero = Tex('0').next_to(axes.c2p(0,0), LEFT, buff=.1).scale(.8)
        one = Tex('1').next_to(axes.c2p(1,0), LEFT, buff=.1).scale(.8)
        dot = Dot(axes.c2p(0,0), fill_color=YELLOW)
        dot2 = Dot(axes.c2p(1,0), fill_color=BLUE)
        graph = VGroup(
            axes.get_graph(lambda x: np.sqrt(x**3-x**4), x_range=(0, 1, .01)),
            axes.get_graph(lambda x: -np.sqrt(x**3-x**4), x_range=(0, 1, .01))
        ).set_color(RED)
        grad = Tex(r"\nabla f=\begin{bmatrix}1\\0\end{bmatrix},"
                   r"~\nabla c=\begin{bmatrix}4x^3-3x^2\\2y\end{bmatrix}",
                   t2c={r'\nabla f=\begin{bmatrix}1\\0\end{bmatrix}': YELLOW,
                        r'\nabla c=\begin{bmatrix}4x^3-3x^2\\2y\end{bmatrix}': RED})\
            .next_to(prob, DOWN, buff=1).to_edge(RIGHT, buff=1.5)
        equation = Tex(r"\begin{cases}"
                       r"\nabla f(x^*,y^*)=\lambda\nabla c(x^*,y^*)\\"
                       r"c(x^*,y^*)=0"
                       r"\end{cases}",
                       t2c={r'\nabla f(x^*,y^*)': YELLOW,
                            r'\nabla c(x^*,y^*)': RED,
                            r'c(x^*,y^*)': RED})\
            .next_to(grad, DOWN, buff=.5)
        sol = Tex(r'\Longrightarrow (x^*,y^*)=(1,0)', color=BLUE).next_to(equation, DOWN).shift(LEFT)
        arrow = Arrow(ORIGIN, UP, stroke_color=YELLOW).next_to(dot, DOWN)
        gradc = Tex(r'\nabla c(0,0)=0', color=RED).next_to(arrow, DOWN)
        self.play(Write(prob))
        self.wait()
        self.play(ShowCreation(axes))
        self.play(Write(zero), Write(one), ShowCreation(graph))
        self.wait()

        self.play(FadeIn(dot, scale=2))
        self.wait()
        self.play(Write(grad))
        self.wait()
        self.play(Write(equation))
        self.wait()
        self.play(Write(sol))
        self.wait()
        self.play(FadeIn(dot2, scale=2))
        self.wait()
        self.play(GrowArrow(arrow), Write(gradc))
        self.wait()


class MultiConstraints(Scene):
    def construct(self) -> None:
        title = Title("\\heiti 推广到多个约束", color=YELLOW, font_size=50,)
        cm = {r'\nabla c_1,\ldots,\nabla c_n': RED, r'\nabla f': YELLOW}
        self.add(title)
        self.wait()
        prob = TexText(r"minimize $f(\vx)$, s.t. $\begin{cases}c_1(\vx)=0\\\cdots\\c_n(\vx)=0\end{cases}$",
                       t2c={r'f(\vx)': YELLOW, r'\begin{cases}c_1(\vx)=0\\\cdots\\c_n(\vx)=0\end{cases}': RED})\
            .next_to(title, DOWN, buff=.5)
        interp0 = TexText(r"和$\nabla c$垂直的方向，也和$\nabla f$垂直.", t2c={r'\nabla c': RED, r'\nabla f': YELLOW})\
            .next_to(prob, DOWN, buff=.5)
        interp = TexText(r"和$\nabla c_1,\ldots,\nabla c_n$垂直的方向，也和$\nabla f$垂直.",
                         t2c=cm)\
            .move_to(interp0)
        brace1 = Brace(interp[:17], DOWN)
        brace1.text = Tex(r"\mathrm{span}\,\{\nabla c_1,\ldots,\nabla c_n\}^\perp",
                          t2c=cm).next_to(brace1, DOWN)
        conclusion = Tex(r"\Longrightarrow \nabla f\in\mathrm{span}\,\{\nabla c_1,\ldots,\nabla c_n\}", t2c=cm)\
            .next_to(brace1.text, DOWN, buff=.5).set_x(0)
        self.play(Write(prob))
        self.wait()
        self.play(Write(interp0))
        self.wait()
        self.play(
            TransformMatchingShapes(interp0[0], interp[0]),
            TransformMatchingShapes(interp0[3:], interp[12:]),
            TransformMatchingShapes(interp0[1:3], interp[1:12]),
        )
        self.wait()
        self.play(GrowFromCenter(brace1))
        self.play(Write(brace1.text))
        self.wait()
        self.play(Write(conclusion))
        self.wait()


class KKT(Scene):
    def construct(self) -> None:
        title = Title("\\heiti 推广到不等号约束", color=YELLOW, font_size=50, )
        self.add(title)
        self.wait()
        cm = {r'\nabla c_1,\ldots,\nabla c_n': RED, r'\nabla f': YELLOW}
        prob = TexText(r"minimize $f(\vx)$, s.t. $c_i(\vx)=0~(i\in E),~ c_j(\vx)\ge0~(j\in I)$",
                       t2c={r'f(\vx)': YELLOW, r'c_i(\vx)=0~(i\in E)': RED, r'c_j(\vx)\ge0~(j\in I)': BLUE}) \
            .next_to(title, DOWN, buff=.5)
        self.play(Write(prob))
        self.wait()
        kkt = Tex(r"\text{KKT条件: }\begin{cases}"
                  r"\displaystyle\nabla f(\vx^*)=\sum_{i\in E\cup I}\lambda_i\nabla c_i(\vx^*)\\"
                  r"c_i(\vx^*)=0,~i\in E\\"
                  r"c_j(\vx^*)\ge0,~j\in I\\"
                  r"\lambda_j\ge0,~j\in I\\"
                  r"\lambda_j c_j(\vx^*)=0,~j\in I"
                  r"\end{cases}",
                  t2c={r'\nabla f(\vx^*)': YELLOW,
                       r'c_i(\vx^*)': RED,
                       r'\nabla c_i(\vx^*)': YELLOW,
                       r'c_j(\vx^*)': BLUE,
                       }).next_to(prob, DOWN, buff=.5)
        self.play(Write(kkt), run_time=3)
        self.wait()


class Pic(Scene):
    def construct(self) -> None:
        title = TexText("Lagrange乘数法", color=YELLOW, font_size=150, stroke_width=7)
        formula = Tex(r"\nabla f(\vx)=\lambda\nabla c(\vx)", font_size=120, stroke_width=5,
                      t2c={'\\nabla f(\\vx)': BLUE, '\\nabla c(\\vx)': RED})
        VGroup(title, formula).arrange(DOWN, buff=1)
        self.add(title, formula)
