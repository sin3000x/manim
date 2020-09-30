from manimlib.imports import *
from scipy.integrate import quad


class increasing(GraphScene, MovingCameraScene):
    CONFIG = {
        "shift_onto_screen": False,
    }

    def construct(self):
        title = TextMobject("\\heiti 严格递增且有无数个驻点.", color=YELLOW).to_edge(UL)

        def second():
            self.x_min = 0
            self.x_max = 1
            self.y_min = 0
            self.y_max = 1
            self.graph_origin = DOWN * 9 + LEFT * 4
            self.y_axis_height = 5
            self.x_axis_width = 5
            self.y_tick_frequency = 1
            l1 = TextMobject("又一个例子...")
            f2 = TexMobject(
                r"f(x)=\begin{cases}x\left(2-\sin(\log x)-\cos(\log x)\right)\quad &0<x\leq 1\\0 & x=0\end{cases}")
            f2d = TexMobject(r"x\neq 0\text{ 时 }~f'(x)=2-2\cos(\log x)\geq 0.")
            l2 = TextMobject(r"而$f'(x)=0~$", r"$\Leftrightarrow$", r"$~\cos(\log x)=1~$", r"$\Leftrightarrow$"
                             , r"$~x=\mathrm{e}^{-2\pi n}~(n=0,1,2,\cdots)$").set_color_by_tex("Leftrightarrow", RED)
            l3 = TextMobject("与前面一样，它也是严格单调递增的.")
            l4 = TextMobject("$f(x)$的图象大概是这样的...")
            VGroup(l1, f2, f2d, l2, l3, l4).arrange(DOWN).next_to(title, DOWN)
            f2.set_x(0)
            box = SurroundingRectangle(f2, color=YELLOW)
            for l in [l1, f2d, l2, l3, l4]:
                l.align_to(title, LEFT)

            self.play(Write(l1))
            self.wait()
            self.play(Write(f2))
            self.play(ShowCreation(box))
            self.wait()
            self.play(Write(f2d))
            self.wait()
            self.play(Write(l2))
            self.wait()
            self.play(Write(l3))
            self.wait()


            self.camera.frame.save_state()
            self.play(self.camera.frame.shift, DOWN * (title.get_top()[1] - l4.get_center()[1]))
            self.play(Write(l4))
            self.wait()

            self.setup_axes(animate=True)
            f = lambda x: x * (2 - np.sin(np.log(x)) - np.cos(np.log(x)))
            graph = self.get_graph(f, x_min=1e-6, x_max=1)
            self.play(ShowCreation(graph))
            self.wait()

            text = TextMobject(r"驻点$\left(\mathrm{e}^{-2\pi n},f\left(\mathrm{e}^{-2\pi n}\right)\right)$",
                               color=YELLOW) \
                .next_to(self.x_axis_label_mob, RIGHT).shift(UP * 3 + LEFT * .5)

            arrow = Arrow(self.coords_to_point(0.2, .2), self.coords_to_point(0, 0), color=GREEN)
            label = TextMobject("\\kaishu 驻点们集中在这，指数级靠近原点.", color=GREEN).next_to(arrow[0], UR)

            self.play(Write(text))
            self.wait()
            self.play(GrowArrow(arrow))
            self.play(Write(label))
            self.wait()
            self.play(Restore(self.camera.frame), run_time=2)

            # dots = [Dot(radius=.002, color=YELLOW).move_to(
            #     self.coords_to_point(np.e**(-2*np.pi*n), f(np.e**(-2*np.pi*n)))) for n in range(21)]
            #
            # self.add(VGroup(*dots))
            # self.camera.frame.save_state()
            # self.play(self.camera.frame.set_width, .08,
            #           self.camera.frame.move_to, self.coords_to_point(0, 0), run_time=10)
            # self.wait()
            # self.play(Restore(self.camera.frame), run_time=2)
            self.wait(2)

        def first():
            self.x_min = -1
            self.x_max = 1
            self.y_min = 0
            self.y_max = .8
            self.graph_origin = DOWN * 10
            self.y_axis_hight = 5.5
            self.y_tick_frequency = .8

            f1 = TexMobject(r"f(x)=\int_0^x t\cdot\left(1+\cos\frac 1t \right)~\mathrm{d}t\quad x\in\mathbb{R}")
            l1 = TextMobject(r"在$x\geq 0$时，$f'(x)=x\left(1+\cos\frac 1x \right)\geq 0$，")
            l2 = TextMobject(r"而$f'(x)=0~$", r"$\Leftrightarrow$",
                             r" $x=0\text{ 或 } ~1+\cos\frac 1x=0$").set_color_by_tex("Leftrightarrow", RED)
            l3 = TextMobject(r"$\Leftrightarrow$",
                             r"$ x=0\text{ 或 }~x=\frac{1}{(2n+1)\pi}~ (n=0,1,2,\cdots)$").set_color_by_tex(
                "Leftrightarrow", RED)
            l41 = TextMobject(r"$f'(x)\geq 0$")
            l42 = TextMobject(r"$f'(x)$不在任何一个区间上恒为$0$")
            l4 = TextMobject("$\\Rightarrow f(x)$严格单调递增.")
            l5 = TextMobject(r"$f(x)$的图象大概是这样的...")
            VGroup(title, f1, l1, l2, l3, l41, l42, l5).arrange(DOWN).to_corner(UL)
            # title.to_edge(UL)
            f1.set_x(0)
            box = SurroundingRectangle(f1, color=RED, buff=.1)

            for l in [l1, l2, l42, l5]:
                l.align_to(title, LEFT)
            l41.align_to(l42, RIGHT)
            brace = Brace(VGroup(l41, l42), RIGHT)
            l4.next_to(brace, RIGHT)
            VGroup(l41, l42, l4, brace).set_color(BLUE)

            l3.align_to(l2[1], LEFT)
            self.play(Write(title))
            self.wait()
            self.play(Write(f1))
            self.play(ShowCreation(box))
            self.play(Write(l1))
            self.wait()
            self.play(Write(l2))
            self.wait()
            self.play(Write(l3))
            self.wait()
            self.play(Write(l41))
            self.play(Write(l42))
            self.play(GrowFromCenter(brace))
            # self.wait()
            self.play(Write(l4))
            self.wait()

            # scrolling
            self.play(self.camera.frame.shift, DOWN * (title.get_top()[1] - l5.get_center()[1]), run_time=2)
            self.wait()
            self.play(Write(l5))
            self.wait()

            def f(x):
                res = quad(lambda t: t * (1 + np.cos(1 / t)), 1e-6, x)
                return res[0]

            self.setup_axes(animate=True)
            graph = self.get_graph(f, x_min=-1, x_max=1)
            self.play(ShowCreation(graph))
            dots = [Dot(radius=.01, color=YELLOW).move_to(
                self.coords_to_point(1 / ((2 * n + 1) * np.pi), f(1 / ((2 * n + 1) * np.pi)))) for n in range(-20, 21)]
            dot0 = Dot(radius=.01).move_to(self.coords_to_point(0, 0))
            self.add(VGroup(*dots), dot0)
            self.camera.frame.save_state()
            self.play(self.camera.frame.set_width, 0.8,
                      self.camera.frame.move_to, self.coords_to_point(0, 0), run_time=5)
            self.play(Restore(self.camera.frame), run_time=2)
            self.wait()
            self.play(self.camera.frame.shift, UP * (title.get_top()[1] - l5.get_center()[1]), run_time=2)

            self.play(FadeOut(VGroup(f1, box, l1, l2, l3, l41, l42, l4, brace, l5, self.axes, graph, dots, dot0)))

        first()
        second()
