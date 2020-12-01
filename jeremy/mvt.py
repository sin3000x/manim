from manimlib.imports import *

class mvt(Scene):
    def construct(self):
        a = TexMobject(r"{{f(b)-f(a)}\over ","{","b","-","a","}","}")
        b = TexMobject(r"{{f(b)-f(a)}\over ","{","g","(","b",")","-","g","(","a",")","}","}")
        self.add(a)
        self.play(ReplacementTransform(a,b))