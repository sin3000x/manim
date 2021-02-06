from manimlib.imports import *

m = {"z": YELLOW}

class Series(Scene):
    def construct(self):
        exp = Tex(r"\e^{z} \coloneqq 1+ z + {z ^2 \over 2!} + {z ^3 \over 3!} + \cdots", isolate="z").set_color_by_tex_to_color_map(m)
        self.add(exp)