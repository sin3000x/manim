from manimlib.imports import *

class ChangePositionAndSize(MovingCameraScene):
    def construct(self):
        text = TexMobject("\\nabla\\textbf{u}").scale(3)
        square = Square()
        VGroup(text, square).arrange_submobjects(RIGHT, buff=3)

        self.add(square, text)
        self.camera.frame.save_state()
        # self.play(self.camera.frame.set_width, text.get_width()*1.2,
        #           self.camera.frame.move_to, text)
        self.play(self.camera.frame.move_to, DOWN*2)
        self.wait()

        self.play(Restore(self.camera.frame))
        self.wait()


class ChangePositionAndSizeCameraInAnotherScene(GraphScene,MovingCameraScene):
    CONFIG = {
        "y_max" : 50,
        "y_min" : 0,
        "x_max" : 7,
        "x_min" : 0,
        "y_tick_frequency" : 5,
        "x_tick_frequency" : 0.5,
    }

    def construct(self):
        self.setup_axes(animate=False)
        graph = self.get_graph(lambda x : x**2,
                                    color = GREEN,
                                    x_min = 0,
                                    x_max = 7
                                    )
        print(graph.points)
        dot_at_start_graph=Dot().move_to(graph.points[0])
        dot_at_end_grap=Dot().move_to(graph.points[-1])

        self.add(graph,dot_at_end_grap,dot_at_start_graph)
        self.camera.frame.save_state()
        self.play(
            self.camera.frame.scale,0.5,
            self.camera.frame.move_to,dot_at_start_graph
        )
        self.wait()
        self.play(
            self.camera.frame.move_to,dot_at_end_grap, run_time = 2
        )
        self.play(Restore(self.camera.frame))
        self.wait()