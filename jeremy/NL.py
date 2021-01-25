from manimlib.imports import *

LEFT_DIST = 4
FUNC_LABEL_FACT = 1.2
VERT_DIST = 4
L = 0.5
R = 3
NUM_SECT = 3
DX = (R-L)/NUM_SECT
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
        "zoomed_display_height": 3,
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

        F_lines = VGroup()
        for i in range(NUM_SECT+1):
            F_lines.add(DashedLine(self.c2p(L+DX*i, 0), self.c2p(L+DX*i, F(L+DX*i))))

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
        for i in range(NUM_SECT+1):
            f_lines.add(DashedLine(self.c2p(L+DX*i, 0), self.c2p(L+DX*i, f(L+DX*i))))
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
        dy_label = Brace(dys[-1], RIGHT, color=RED)
        dy_label = VGroup(dy_label, dy_label.get_tex("\\Delta y").set_color(RED))
        tan = TexMobject("=","\\Delta x","\\cdot","\\tan\\alpha").next_to(dy_label).tm(
            {"x": YELLOW}
        )

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

        f_rect = self.get_riemann_rectangles(
            f_graph, x_min=L, x_max=R, dx=DX,
        )
        self.play(ShowCreation(f_rect[2]))
        self.wait()

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

    def get_tangent_line(self, x, color=YELLOW):
        tangent_line = Line(LEFT, RIGHT).scale(3)
        tangent_line.set_color(color)
        self.make_line_tangent(tangent_line, x)
        return tangent_line

    def make_line_tangent(self, line, x):
        graph = self.graph
        line.rotate(self.angle_of_tangent(x, graph) - line.get_angle())
        line.move_to(self.input_to_graph_point(x, graph))