from manimlib.imports import *


class test(GraphScene):
    CONFIG = {
        "x_min": -5,
        "x_max": 5,
        "y_min": -2,
        "y_max": 2,
        "graph_origin": ORIGIN,
    }

    def construct(self):
        self.setup_axes(animate=False)
        func_graph = self.get_graph(self.func, x_min=-4.5, x_max=4.5)
        func_lab = self.get_graph_label(func_graph, label="y={\\sin x\\over x}", direction=DOWN)
        self.play(ShowCreation(func_graph))
        self.play(Write(func_lab))
        self.wait()

    @staticmethod
    def func(x):
        return np.sinc(x / np.pi)


