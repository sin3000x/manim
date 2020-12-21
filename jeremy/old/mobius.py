from manimlib.imports import *

class linear(LinearTransformationScene):
    def construct(self):
        # square = Square().scale(2)
        function = lambda point: complex_to_R3((2*R3_to_complex(point)+5)/(-3*R3_to_complex(point)-1))
        elliptic = lambda z:(2*z+5)/(-3*z-1)

        # self.add_transformable_mobject(square)

        self.apply_nonlinear_transformation(function)

        # self.wait()
        # self.play(self.apply_complex_function, lambda z: (2*z+5)/(-3*z-1), run_time=5, rate_func=there_and_back)
        # self.play(grid.apply_complex_function, lambda z: 7*z+6, run_time=5, rate_func=there_and_back)
        # self.play(grid.apply_complex_function, lambda z: z/(z+1), run_time=5, rate_func=there_and_back)

class mobius(Scene):
    def construct(self):
        underplane = ComplexPlane(color=WHITE).fade(0.6)
        plane = ComplexPlane(y_min=0)
        plane.add_coordinates()
        plane.add_coordinates(0)
        plane.prepare_for_nonlinear_transform()
        self.add(plane, underplane)
        funcs = [lambda z: 3*z+2, lambda z: (2*z+1)/2,lambda z: (2*z+5)/(-3*z-1) if z != -1/3 else 1e12]
        gammas = VGroup(*[TexMobject(f"{gamma}") for gamma in [r"3*z+2 \colon", r"{{2z+1} \over 2}\colon",r"{{2z+5} \over {-3z-1}}\colon "]])
        labels = VGroup(*[TextMobject(f"{label}") for label in ["hyperbolic", "parabolic","elliptic"]])
        trans = VGroup(*[TextMobject(f"{tr}", color=YELLOW) for tr in ["dilation", "translation", "rotation"]])

        v1 = VGroup(gammas, labels).arrange().to_edge(BOTTOM)
        trans.next_to(v1, DOWN)
        bg = BackgroundRectangle(VGroup(v1, trans))
        self.play(FadeIn(bg))
        fix = Dot(plane.n2p(-1),color=YELLOW)
        infty = TexMobject("\\infty", color=YELLOW).to_edge(UP)
        for i, (fun, gamma, label, tran) in enumerate(zip(funcs, gammas, labels, trans)):
            if i == 0:
                self.play(Write(gamma))
                self.play(Write(label))
                self.play(Write(tran))
                self.play(FadeIn(fix), FadeIn(infty))
                self.wait()
            if i == 1:
                self.play(ReplacementTransform(gammas[i-1], gamma),
                          ReplacementTransform(labels[i-1], label),
                          ReplacementTransform(trans[i-1], tran),
                          FadeOut(fix))
                self.wait()
            if i == 2:
                self.play(ReplacementTransform(gammas[i-1], gamma),
                          ReplacementTransform(labels[i-1], label),
                          ReplacementTransform(trans[i-1], tran),
                          ReplacementTransform(infty, Dot(plane.n2p(-0.5+1.19j), color=YELLOW)))
                self.wait()
            self.play(plane.apply_complex_function, fun, run_time=5, rate_func=there_and_back)


class test(ComplexTransformationScene):
    def construct(self):
        self.add_transformable_plane()
        self.apply_complex_function(lambda x: x**2)

