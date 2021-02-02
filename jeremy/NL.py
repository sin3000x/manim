from manimlib.imports import *

LEFT_DIST = 4
FUNC_LABEL_FACT = 1.2
VERT_DIST = 4
L = 0.5
R = 3
NUM_SECT = 3
SECT2 = 6
SECT3 = 12
DX = (R-L)/NUM_SECT
DX2 = (R-L)/SECT2
DX3 = (R-L)/SECT3
xi = 2.64064
class graphs(GraphScene, ZoomedScene):
    CONFIG = {
        "y_max": 15,
        "y_min": 0,
        "x_max": 3.5,
        "x_min": 0,
        "y_tick_frequency": 15,
        "x_tick_frequency": 3.5,
        "x_axis_width": 6,
        "y_axis_height": 3,
        "axes_color": GRAY,
        "num_rects": 1000,
        "area_opacity": 0.8,
        "num_graph_anchor_points": 3000,
        "zoom_factor": 0.3,
        "zoomed_display_height": 3.2,
        "zoomed_display_width": 6,
        "image_frame_stroke_width": 3,
        "zoomed_camera_config": {
            "default_frame_stroke_width": 3,
        },
        "zoomed_camera_image_mobject_config": {
            "default_display_frame_config": {
                "stroke_width": 3,
                "stroke_color": WHITE,
                "buff": 0,
            }
        },
    }

    def construct(self):
        ZoomedScene.setup(self)
        f = lambda x: (x-1)**3-3*x+7
        F = lambda x: (x-1)**4/4-3*x**2/2+7*x
        x = ValueTracker(0)

        self.graph_origin = -0.5 * DOWN + LEFT_DIST * LEFT
        self.setup_axes(animate=True)
        y_unit = (self.c2p(0,1)-self.c2p(0,0))[1]
        F_graph = self.get_graph(F,
                                  color=GREEN,
                                  x_min=0,
                                  x_max=3.3
                                  )
        F_part = self.get_graph(F,
                                  color=RED,
                                  x_min=L,
                                  x_max=R
                                  )
        F_diff = Line(F_part.get_start(),
                      F_part.get_start()+UP*(F_part.get_end()[1]-F_part.get_start()[1]),
                      color=RED).to_edge(RIGHT, buff=2.5)

        self.graph = self.get_graph(lambda t: F(t)*2/3, x_min=0, x_max=3.3)
        # F_line = Line().add_updater(
        #     lambda t: t.become(
        #         Line(self.c2p(x.get_value(), 0), self.c2p(x.get_value(), F(x.get_value())*2/3)).shift(UP*VERT_DIST)
        #     )
        # )
        F_tangent = Line().add_updater(
            lambda t: t.become(
                self.get_tangent_line(x.get_value()).shift(UP*VERT_DIST)
            )
        )

        # Dashed lines for F
        F_lines = VGroup()
        F_lines2 = VGroup()
        F_lines3 = VGroup()
        for lines,dx, ran in zip([F_lines, F_lines2, F_lines3],[DX, DX2, DX3],[range(NUM_SECT+1), range(SECT2+1), range(SECT3+1)]):
            for i in ran:
                lines.add(DashedLine(self.c2p(L+dx*i, 0), self.c2p(L+dx*i, F(L+dx*i))))

        xi_line = (DashedLine(self.c2p(xi, F(xi)), self.c2p(xi, 0), color=BLUE))
        xi_label = TexMobject("\\xi").next_to(xi_line, DOWN).set_color(xi_line.get_color())

        f1 = TexMobject(r"F(x)", color=F_graph.get_color())
        f1.scale(1.2)
        f1.next_to(self.y_axis, LEFT)
        self.play(ShowCreation(F_graph))
        self.play(Write(f1))

        # f part
        self.graph_origin = (-0.5+VERT_DIST) * DOWN + LEFT_DIST * LEFT
        self.y_max=10
        self.y_tick_frequency = self.y_max
        self.setup_axes(animate=True)
        f_graph = self.get_graph(f,
                                    color=BLUE_D,
                                    x_min=0,
                                    x_max=3.3
                                    )
        f_lines = VGroup()
        f_lines2 = VGroup()
        f_lines3 = VGroup()
        for lines,dx, ran in zip([f_lines, f_lines2, f_lines3],[DX, DX2, DX3],[range(NUM_SECT+1), range(SECT2+1), range(SECT3+1)]):
            for i in ran:
                lines.add(DashedLine(self.c2p(L+dx*i, 0), self.c2p(L+dx*i, f(L+dx*i))))
        # for i in range(NUM_SECT+1):
        #     f_lines.add(DashedLine(self.c2p(L+DX*i, 0), self.c2p(L+DX*i, f(L+DX*i))))
        f2 = TexMobject(r"f(x)", color=BLUE_D)
        f2.scale(FUNC_LABEL_FACT).next_to(self.y_axis, LEFT).align_to(f1, LEFT)
        f_line = Line().add_updater(
            lambda t: t.become(
                self.get_vertical_line_to_graph(
                    x.get_value(),
                    f_graph,
                    color=YELLOW)
            )
        )

        self.play(Write(f2))

        xi_line_f = DashedLine(self.c2p(xi, 0), self.c2p(xi, f(xi)), color=BLUE)

        # show F and f
        self.play(ShowCreation(f_line), ShowCreation(F_tangent))
        self.play(ShowCreation(f_graph), x.set_value, 3.3, run_time=5)
        f_line.clear_updaters()
        F_tangent.clear_updaters()
        self.play(FadeOut(VGroup(f_line, F_tangent)))

        # show area and F(b)-F(a)
        area = self.get_area(f_graph, t_min=L, t_max=R)
        self.play(ShowCreation(area), ShowCreation(F_part), run_time=3)
        self.wait()
        small_area = area.copy().scale(.6).next_to(F_diff, DOWN, buff=2.5)
        eq = TexMobject("=").rotate(np.pi/2).scale(2.5).next_to(F_diff, DOWN, buff=1)
        self.play(RT(area.copy(), small_area), run_time=2)
        self.play(RT(F_part.copy(), F_diff), run_time=2)
        self.play(Write(eq))
        self.wait()

        # show division
        self.play(ShowCreation(F_lines[0]), ShowCreation(F_lines[-1]),
                  ShowCreation(f_lines[0]), ShowCreation(f_lines[-1]),
                  FadeOut(VGroup(area, F_part)))
        self.wait()
        self.play(*[ShowCreation(F_lines[i]) for i in range(1,NUM_SECT)],
                  *[ShowCreation(f_lines[i]) for i in range(1,NUM_SECT)],
                  FadeOut(VGroup(small_area, eq, F_diff)))

        # small partial lines
        sec_lines = VGroup(
            *[Line(F_lines[i].get_end(),
                   F_lines[i+1].get_end(),
                   ).set_color_by_gradient([RED, YELLOW]) for i in range(0, NUM_SECT)]
        )

        dys = VGroup(
            *[Line((F_lines[i].get_end()[0],F_lines[i-1].get_end()[1], 0),
                   F_lines[i].get_end(),
                   color=RED) for i in range(1, NUM_SECT+1)]
        )
        dys2 = VGroup(
            *[Line((F_lines2[i].get_end()[0],F_lines2[i-1].get_end()[1], 0),
                   F_lines2[i].get_end(),
                   color=RED) for i in range(1, SECT2+1)]
        )
        dys3 = VGroup(
            *[Line((F_lines3[i].get_end()[0],F_lines3[i-1].get_end()[1], 0),
                   F_lines3[i].get_end(),
                   color=RED) for i in range(1, SECT3+1)]
        )
        dy_label = Brace(dys[-1], RIGHT, color=RED)
        dy_label = VGroup(dy_label, dy_label.get_tex("\\Delta y").set_color(RED))
        tan = TexMobject("=","\\Delta x","\\cdot","\\tan\\alpha").next_to(dy_label).tm(
            {"x": YELLOW}
        )
        Fxi = TexMobject("F'(\\xi)", color=BLUE).move_to(tan[-1])
        fxi = TexMobject(r"f(\xi)", color=BLUE).next_to(tan[-2])

        dxs = VGroup(
            *[Line(l.get_start(), r.get_start(), color=YELLOW) for l, r in zip(sec_lines, dys)]
        )
        dx_label = Brace(dxs[-1], DOWN, color=YELLOW)
        dx_label = VGroup(dx_label, dx_label.get_tex("\\Delta x").set_color(YELLOW))
        arc = Arc(arc_center=dxs[-1].get_start(), angle=sec_lines[-1].get_angle(), radius=.4)
        alpha = TexMobject("\\alpha").scale(.7).next_to(dxs[-1], UP, buff=.05).shift(LEFT*.1)
        arc = VGroup(arc, alpha).set_color(WHITE)

        self.play(ShowCreation(dys[-1]),GrowFromCenter(dy_label))
        self.wait()
        # self.add(dys, sec_lines, dxs)

        self.play(ShowCreation(dxs[-1]), GrowFromCenter(dx_label))
        self.wait()
        self.play(ShowCreation(sec_lines[-1]), Write(tan), FadeIn(arc))



        # Set camera
        zoomed_camera = self.zoomed_camera
        zoomed_display = self.zoomed_display
        frame = zoomed_camera.frame.set_color(PURPLE).move_to(sec_lines[-1])
        zoomed_display_frame = zoomed_display.display_frame.set_color(PURPLE)

        zoomed_display.move_to(f1).shift(RIGHT)

        # brackground zoomed_display
        zd_rect = BackgroundRectangle(
            zoomed_display,
            fill_opacity=0,
            buff=MED_SMALL_BUFF,
        )

        self.add_foreground_mobject(zd_rect)
        # animation of unfold camera
        unfold_camera = UpdateFromFunc(
            zd_rect,
            lambda rect: rect.replace(zoomed_display)
        )

        self.play(
            ShowCreation(frame),
        )

        # Activate zooming
        self.activate_zooming()

        self.play(
            # You have to add this line
            self.get_zoomed_display_pop_out_animation(),
            unfold_camera
        )

        self.play(FadeOut(arc))
        self.play(sec_lines[-1].shift, DOWN*0.407997*y_unit)
        self.wait()
        self.play(FadeOut(dx_label), FadeOut(dxs[-1]))
        self.wait()
        self.play(ShowCreation(xi_line))
        self.play(Write(xi_label))
        self.wait()
        self.play(Transform(tan[-1], Fxi))
        self.wait()
        # self.play(
        #     FadeOut(zoomed_display_frame),
        #     FadeOut(frame),
        # )
        self.remove(zoomed_display_frame, frame)
        self.wait()
        self.play(Transform(tan[-1], fxi), ShowCreation(xi_line_f), run_time=2)
        self.wait()
        f_dx = Line(self.c2p(R-DX, 0), self.c2p(R, 0))
        delta_x = Brace(f_dx, DOWN, color=YELLOW, buff=0)
        f_xi = Brace(xi_line_f, RIGHT, color=BLUE, buff=0)
        self.play(GrowFromCenter(delta_x))
        self.play(GrowFromCenter(f_xi))
        self.wait()

        f_rect = self.get_riemann_rectangles(
            f_graph, x_min=L, x_max=R, dx=DX,input_sample_type="center"
        )
        f_rect2 = self.get_riemann_rectangles(
            f_graph, x_min=L, x_max=R, dx=DX2,input_sample_type="center"
        )
        f_rect3 = self.get_riemann_rectangles(
            f_graph, x_min=L, x_max=R, dx=DX3,input_sample_type="center"
        )
        f_rect[2].stretch(f(xi)/f(R-DX/2), 1, about_edge=DOWN)
        bar = f_rect[2].copy().scale(.8).next_to(tan[0])
        self.play(DrawBorderThenFill(f_rect[2]))
        self.play(FadeOut(delta_x))
        self.remove(f_xi)
        self.wait()
        self.play(FadeOut(tan[1:]), RT(f_rect[2].copy(), bar), run_time=2)
        self.wait()
        # zd_rect.clear_updaters()

        self.play(FadeOut(sec_lines[-1]),
            FadeOut(xi_line),
            FadeOut(xi_label))
        self.wait()
        for i in [1,0]:
            self.play(ShowCreation(dys[i]))
            self.play(Indicate(dys[i]), scale_factor=1.5)
            self.play(DrawBorderThenFill(f_rect[i]))
            self.wait()
        self.play(FadeOut(VGroup(dy_label, tan[0], bar)))
        to_res = [dys[0], dys[1]]
        for re in to_res:
            re.save_state()
        self.play(
            dys[1].set_x, dys[-1].get_x(),
            dys[0].set_x, dys[-1].get_x(), lag_ratio=.2
        )
        self.play(ApplyWave(f_rect))
        self.wait()
        self.play(*[Restore(re) for re in to_res])
        self.wait()

        # self.transform_between_riemann_rects(f_rect, f_rect2,
        #                                      added_anims=[RT(F_lines, F_lines2, run_time=2),
        #                                      RT(dys, dys2, run_time=2),])
        # self.wait()
        # self.transform_between_riemann_rects(f_rect2, f_rect3,
        #                                      added_anims=[RT(F_lines2, F_lines3, run_time=2),
        #                                      RT(dys2, dys3, run_time=2),])
        self.play(RT(F_lines, F_lines2),RT(dys, dys2), RT(f_rect, f_rect2))
        self.wait()
        self.play(RT(F_lines2, F_lines3),RT(dys2, dys3), RT(f_rect2, f_rect3))
        self.wait()
        self.play(*list(it.chain(*[[i.set_x, dys3[-1].get_x()] for i in dys3[:-1]])))
        self.wait()
        self.play(ApplyWave(f_rect3, amplitude=.5))
        self.wait()

        self.play(FadeOut(F_lines3[1:-1]))
        self.remove(xi_line_f, f_lines[1], f_lines[2])
        # self.play(RT(f_rect3, area))
        self.transform_between_riemann_rects(f_rect3, area, rate_func=linear)
        self.wait()
        # self.add(f_rect[:2])

    def get_tangent_line(self, x, color=YELLOW):
        tangent_line = Line(LEFT, RIGHT).scale(3)
        tangent_line.set_color(color)
        self.make_line_tangent(tangent_line, x)
        return tangent_line

    def make_line_tangent(self, line, x):
        graph = self.graph
        line.rotate(self.angle_of_tangent(x, graph) - line.get_angle())
        line.move_to(self.input_to_graph_point(x, graph))


ma = {"a": RED, "b": BLUE}
class Proof(Scene):
    def construct(self):
        title = Heiti("Newton-Leibniz公式").to_corner(UL)
        self.play(Write(title))
        self.wait()
        division = TexMobject("a","=x_0<x_1<\\cdots<x_n=","b")\
            .tm(ma).next_to(title, DOWN).set_x(0)
        trans = TexMobject(*"F( b )-F( a ) = F(x_n)-F(x_0)".split()).tm(ma)\
            .next_to(division, DOWN, buff=MED_LARGE_BUFF).align_to(title, LEFT)
        terms = TexMobject("=\\Delta y_n+\\cdots+\\Delta y_1")
        pairs = TexMobject("=\\left(F(x_n)-F(x_{n-1})\\right)+\\cdots+\\left(F(x_1)-F(x_0)\\right)")
        lagrange = TexMobject(*"= F' (\\xi_n)\\Delta x_n+\\cdots+ F' (\\xi_1)\\Delta x_1".split())
        tof = TexMobject(*"= f (\\xi_n)\\Delta x_n+\\cdots+ f (\\xi_1)\\Delta x_1".split())
        res = TexMobject(*"\\to \\int_ {a }^b f(x)\\d x".split())
        res[2].set_color(BLUE)
        res[3].set_color(RED)
        formula = TexMobject(*"F( b )-F( a ) = \\int_ {a }^b f(x)\\d x".split()).tm(ma)
        formula[7].set_color(BLUE)
        formula[8].set_color(RED)
        box = SurroundingRectangle(formula, color=YELLOW)

        VGroup(terms, pairs, lagrange, res).arrange(DOWN, aligned_edge=LEFT)\
            .next_to(trans, DOWN).align_to(trans[5], LEFT)
        tof.move_to(lagrange).align_to(pairs, LEFT)

        self.play(Write(division))
        self.wait()
        self.play(Write(trans))
        self.wait()
        self.play(Write(terms))
        self.wait()
        self.play(Write(pairs))
        self.wait()
        self.play(Write(lagrange))
        self.wait()
        self.play(*[RT(lagrange[i], tof[i]) for i in range(len(tof))])
        self.wait()
        self.play(Write(res))
        self.wait()

        self.play(FadeOut(VGroup(division, trans[5:], terms, pairs, tof)),
                  RT(trans[:5], formula[:5]),
                  RT(res, formula[5:]))
        self.play(ShowCreation(box))
        self.wait()

        self.play(VGroup(formula, box).shift, DOWN)

        c1 = TextMobject("1.\\quad ","$F'=f$")
        c2 = TextMobject("2.\\quad","$f$","~在~","$[a,b]$","~上可积")
        VGroup(c1, c2).arrange(DOWN, aligned_edge=LEFT)\
            .next_to(title, DOWN, buff=.7, aligned_edge=LEFT).set_x(0)
        extra = TexMobject(",~ x\\in [a,b]").next_to(c1, RIGHT, buff=0)
        extra2 = TexMobject(",~ x\\in (a,b)").next_to(c1, RIGHT, buff=0)

        c3 = TextMobject("3.\\quad","$F$","~在~","$[a,b]$","~上连续").next_to(c2, DOWN, )
        self.play(Write(c1))
        self.wait()
        self.play(Write(c2))
        self.wait(2)
        self.play(Write(extra))
        self.wait()
        self.play(RT(extra, extra2))
        self.wait()
        self.play(Write(c3))
        self.wait(2)

class pic(GraphScene):
    CONFIG = {
        "y_max": 4,
        "x_max": 2,
        "x_min": 0,
        "y_min": 0,
        "y_axis_height": 7,
        "graph_origin": 3.2 * DOWN + 4 * LEFT,
    }
    def construct(self):
        self.setup_axes()
        graph = self.get_graph(lambda x: x**2, x_min=0,x_max=1.9)
        self.add(graph)
        rec = self.get_riemann_rectangles(graph, x_min=0.2, x_max=1.8)
        self.add(rec)
        label = TexMobject("\\int_a^b f(x)\\d x").next_to(graph, UP).scale(2).shift(DOWN*2+LEFT*.5)
        self.add(label)

