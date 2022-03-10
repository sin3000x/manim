from manimlib import *

class Cuboid(VMobject):
    def __init__(self, length, bias=None, **kwargs):
        super().__init__(**kwargs)
        if bias is None:
            bias == length/2
        self.add(Polygon(ORIGIN, length*RIGHT, length*RIGHT+UR*bias, length*RIGHT+UR*bias+UP*length, UR*bias+UP*length, UP*length))
        self.add(
            Line(length*UR, UP*length),
            Line(length*UR, length*UR+bias*UR),
            Line(length*UR, RIGHT*length)
        )
        self.add(Tex("\\mathcal{X}").move_to(UR*length/2))
        self.set_color(BLACK)

class Product(VGroup):
    def __init__(self, width, height, bias=1, buff=.15, label='1', **kwargs):
        super().__init__(**kwargs)
        a = Rectangle(width=width, height=height)
        b = Rectangle(width=height, height=width).next_to(a, RIGHT, buff=buff).align_to(a, UP)
        c = Polygon(ORIGIN, width*RIGHT, width*RIGHT+UR*bias, UR*bias).next_to(a, UP, buff=buff).align_to(a, LEFT)
        self.add(a,b,c)
        a_label = Tex("\\va_{%s}" % label).next_to(a, DOWN)
        b_label = Tex("\\vb_{%s}" % label).next_to(b, DOWN)
        c_label = Tex("\\vc_{%s}" % label).next_to(c, buff=.1)
        self.add(a_label, b_label, c_label)
        self.a = a

class Factor(VGroup):
    def __init__(self, width, height, bias=1, buff=.15, **kwargs):
        super().__init__(**kwargs)
        a = Rectangle(width=width, height=height)
        b = Rectangle(width=height, height=width).next_to(a, RIGHT, buff=buff).align_to(a, UP)
        c = Polygon(ORIGIN, width*RIGHT, width*RIGHT+UR*bias, UR*bias).next_to(a, UP, buff=buff).align_to(a, LEFT)
        self.add(a,b,c)
        a_label = Tex("A").move_to(a)
        b_label = Tex("B").move_to(b)
        c_label = Tex("C").move_to(c)
        self.add(a_label, b_label, c_label)

class CP(Scene):
    def construct(self):
        mob = VGroup()
        mob.add(
            Cuboid(2, .66), 
            Tex("="), 
            Product(width=0.25, height=2),
            Tex("+\\cdots+"),
            Product(width=0.25, height=2, label='R'),
            Tex("="), 
            Factor(width=1, height=2)
            )
        
        mob.arrange().set_color(BLACK).scale(.9)
        mob[-1].align_to(mob[2].a, DOWN)
        self.add(mob.move_to(ORIGIN))