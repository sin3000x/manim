from manimlib.imports import *
import matplotlib.pyplot as plt

class pi(TeacherStudentsScene):
    def construct(self):
        # you = self.pi_creature.move_to(ORIGIN)
        # a = [Coin().to_edge(i) for i in [LEFT, UP, RIGHT, DOWN]]
        # for i in a:
        #     self.play(FadeIn(i))
        #     self.wait()

        # self.play(you.change, "question")
        t = self.teacher_says("hello")
        self.wait(4)


class Cut(Scene):
    def construct(self):
        plane = NumberPlane()
        self.add(plane)
        cut = BranchCut()
        self.play(ShowCreation(cut))
        # self.play(Wave(cut))

class ZoomedSceneExample(ZoomedScene):
    CONFIG = {
        "zoom_factor": 0.3,
        "zoomed_display_height": 3,
        "zoomed_display_width": 6,
        "image_frame_stroke_width": 20,
        "zoomed_camera_config": {
            "default_frame_stroke_width": 3,
        },
    }

    def construct(self):
        # Set objects
        dot = Dot().shift(UL*2)
        plane = NumberPlane().add_coordinates()
        graph = plane.get_graph(lambda x: np.sin(x), color=YELLOW)
        graph2 = plane.get_graph(lambda x: np.cos(x), color=YELLOW)

        # image=ImageMobject(np.uint8([[ 0, 100,30 , 200],
        #                              [255,0,5 , 33]]))
        # image.set_height(7)
        frame_text=TextMobject("Frame",color=PURPLE).scale(1.4).add_background_rectangle()
        zoomed_camera_text=TextMobject("Zommed camera",color=RED).scale(1.4).add_background_rectangle()

        self.add(plane, dot, graph)

        # Set camera
        zoomed_camera = self.zoomed_camera
        zoomed_display = self.zoomed_display
        frame = zoomed_camera.frame.move_to(dot).set_color(PURPLE)
        zoomed_display_frame = zoomed_display.display_frame.set_color(RED)

        zoomed_display.shift(DOWN)

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

        frame_text.next_to(frame,DOWN)

        self.play(
            ShowCreation(frame),
            FadeInFromDown(frame_text)
        )

        # Activate zooming
        self.activate_zooming()

        self.play(
            # You have to add this line
            self.get_zoomed_display_pop_out_animation(),
            unfold_camera
        )

        zoomed_camera_text.next_to(zoomed_display_frame,DOWN)
        self.play(FadeInFromDown(zoomed_camera_text))

        # Scale in     x   y  z
        scale_factor=[0.5,1.5,0]

        # Resize the frame and zoomed camera
        # self.play(
        #     frame.scale,                scale_factor,
        #     zoomed_display.scale,       scale_factor,
        #     FadeOut(zoomed_camera_text),
        #     FadeOut(frame_text)
        # )

        # Resize the frame
        self.play(
            # frame.scale,.5,
            frame.shift,2.5*DOWN
        )
        self.play(RT(graph, graph2))
        self.play(FadeOut(frame_text))

        # Resize zoomed camera
        # self.play(
        #     ScaleInPlace(zoomed_display,2)
        # )
        #
        #
        # self.wait()

        # self.play(
        #     self.get_zoomed_display_pop_out_animation(),
        #     unfold_camera,
        #     # -------> Inverse
        #     rate_func=lambda t: smooth(1-t),
        # )
        # self.play(
        #     Uncreate(zoomed_display_frame),
        #     FadeOut(frame),
        # )
        self.wait()

class AreaTest(GraphScene, Scene):
    CONFIG = {
    "x_min": 0,
    "x_max": 10,
    "x_axis_width": 10, #change the width of the step in x
    "x_tick_frequency": 1,
    "x_axis_label": "$time$",
    "y_min": 0,
    "y_max": 10,
    "y_axis_height": 6,
    "y_tick_frequency": 1,
    "y_bottom_tick": None,
    "y_labeled_nums": None,
    "y_axis_label": "$velocity$",
    "axes_color": BLUE,
    "graph_origin": LEFT*6+DOWN*3, #Change the position of the origin
    "exclude_zero_label": True,
    "default_graph_colors": [BLUE, GREEN, YELLOW],
    "default_derivative_color": GREEN,
    "default_input_color": YELLOW,
    "default_riemann_start_color": BLUE,
    "default_riemann_end_color": GREEN,
    "area_opacity": 0.8,
    "num_rects": 50,
    "num_graph_anchor_points" : 3000,
    "function_color" : WHITE,
    }

    def func1(self, x):
        return (x)

class T(GraphScene):
    CONFIG = {
        "x_min": 0,
        "x_max": 1.2,
        "y_max": 1.2,
        "graph_origin": ORIGIN
    }
    def construct(self):
        self.setup_axes(animate = True)
        graph = self.get_graph(lambda t: np.sin(1000/t), x_min=1e-6, x_max=1)
        self.add(graph)
        label = TexMobject("\\sin\\frac 1x").next_to(graph, LEFT, buff=1)
        self.add(label)