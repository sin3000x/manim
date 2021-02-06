from manimlib.imports import *

m = {"z": YELLOW, r"\i": BLUE}

class Series(Scene):
    def construct(self):
        exp = Tex(r"\e^{z} \coloneqq 1+z+{{{z^2\over2!}}}+{{{z^3\over3!}}}+{{{z^4\over4!}}}+{{{z^5\over5!}}}+\cdots", tex_to_color_map=m).to_edge(UP, buff=1)
        sin = Tex(r"\sin z\coloneqq z-{{{z^3\over3!}}}+{{{z^5\over5!}}}-{{{z^7\over7!}}}+{{{z^9\over9!}}}-{{{z^{11}\over11!}}}+\cdots", tex_to_color_map=m)
        cos = Tex(r"\cos z\coloneqq 1-{{{z^2\over2!}}}+{{{z^4\over4!}}}-{{{z^6\over6!}}}+{{{z^8\over8!}}}-{{{z^{10}\over10!}}}+\cdots", tex_to_color_map=m)
        # exp = Tex(*r"\e^ {z} \coloneqq 1+ z + {z ^2 \over 2!} + {z ^3 \over 3!} + \cdots".split()).tm(m)
        # sin = Tex(*r"\sin z \coloneqq z- {z^3} + {z ^2 \over 2!} + {z ^3 \over 3!} + \cdots".split()).tm(m)
        sin.next_to(exp[2], DOWN, buff=1.2, aligned_edge=LEFT, submobject_to_align=sin[2])
        cos.next_to(sin[2], DOWN, buff=1.2, aligned_edge=LEFT, submobject_to_align=cos[2])
        self.play(Write(exp))
        self.play(Write(sin))
        self.play(Write(cos))
        self.wait()

        line = Line(color=RED).set_width(FRAME_WIDTH-2).next_to(cos, DOWN).set_x(0)
        self.play(GrowFromCenter(line))
        self.wait()
        exp_ix = Tex(r"\e^{{{\i x}}} = 1+{{\i x}}+{{{({{\i x}})^2\over2!}}}+{{{({{\i x}})^3\over3!}}}+{{{({{\i x}})^4\over4!}}}+{{{({{\i x}})^5\over5!}}}+\cdots", tex_to_color_map=m).to_edge(DOWN, buff=1)
        exp_ix2 = Tex(r"\e^{{{\i x}}} = 1+{{\i x}}-{{{x^2\over2!}}}-\i{{{x^3\over3!}}}+{{{x^4\over4!}}}+\i{{{x^5\over5!}}}\cdots", tex_to_color_map=m).move_to(exp_ix)
        self.play(Write(exp_ix))
        self.wait()
        self.play(RT(exp_ix[:3], exp_ix2[:3]), RT(exp_ix[3:], exp_ix2[3:]))