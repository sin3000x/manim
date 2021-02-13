from manimlib import *

m = {"z": YELLOW, "w": BLUE, "\\Longrightarrow": WHITE,}
class Def(Scene):
    def construct(self):
        prob = Tex("\\text{如何定义}~ {{\\ln}} z?", tex_to_color_map = m).to_edge(UP, buff=1)
        calc = Tex("\\text{如何计算}~ {{\\ln}} z?", tex_to_color_map = m).to_edge(UP, buff=1)
        self.play(Write(prob))
        self.wait()

        exp = Tex(r"\text{若有}~\e^w=z,", tex_to_color_map=m).next_to(prob, DOWN, buff=1)
        self.play(Write(exp))
        self.wait()

        ln = Tex(r"\text{我们说}~ w=\ln z.", tex_to_color_map=m).next_to(exp, DOWN)
        self.play(Write(ln))
        self.wait()

        issue = Tex(r"\e^{{0}}=\e^{{{2\pi\i}}}=\e^{{{4\pi\i}}}=\cdots={{1}}")\
            .tm({"0": BLUE, "pi": BLUE, "1": YELLOW}).next_to(ln, DOWN, buff=1)
        multi = Tex(r"\ln{{1}}={{0}},~{{\pm 2\pi\i}},~{{\pm 4\pi\i}},~\cdots").tm({"0": BLUE, "pi": BLUE, "1": YELLOW}).next_to(issue, DOWN, buff=.5)
        comment = TexText("\\kaishu 我们不认为多值函数是函数.", color=GREEN).to_edge(DOWN, buff=.5)
        arrow = Arrow(comment.get_top(), multi.get_bottom()).set_color(GREEN)
        self.play(Write(issue))
        self.wait()
        self.play(Write(multi))
        self.wait()
        self.play(Write(comment),GrowArrow(arrow))
        self.wait()

        self.play(TransformMatchingTex(prob, calc),
                FadeOut(VGroup(issue, multi, comment, arrow)))
        self.wait()

        notation = Tex(r"\text{记~} {{w}}={{x+\i y}},\text{~那么}").tm({"w": BLUE, "y": BLUE,}).next_to(ln, DOWN, buff=1)
        polar = Tex(r"{{z}}=\e^{{w}}=\e^{{{x+\i y}}}={{\e^x\e^{\i y}}}").tm({"z": YELLOW, "w": BLUE, "x": BLUE, "\\e^x": YELLOW}).next_to(notation, DOWN)
        self.play(Write(notation))
        self.wait()
        self.play(Write(polar))
        self.wait()

class Polar(Scene):
    def construct(self):
        m = {"r": GREEN, "theta": YELLOW}

        plane = ComplexPlane().add_coordinate_labels()
        self.add(plane)
        point = Dot(plane.n2p("3+3j"), color=GREEN)
        label = Tex(r"r\e^{\i\theta}", isolate=["\\e", "\\theta"]).tm(m).next_to(point).add_background_rectangle()
        line = Line(ORIGIN, point)
        r = Brace(line, UL)
        r = VGroup(r.set_color(m['r']), r.get_tex("r").set_color(m['r']).add_background_rectangle())
        theta = Arc(angle=PI/4, color=m['theta'], radius=.7)
        theta = VGroup(theta, Tex(r"\theta", color=m['theta']).next_to(theta).shift(UP*.2).add_background_rectangle())
        self.play(GrowFromCenter(point))
        self.play(ShowCreation(line))
        self.wait()
        self.play(Write(label))
        self.wait()
        self.play(GrowFromCenter(r))
        self.wait()
        self.play(GrowFromCenter(theta))
        self.wait()