from manimlib import *

class fiber1(VGroup):
    def __init__(self):
        super().__init__()
        h = 8
        self.add(Polygon(ORIGIN, RIGHT, RIGHT*1.5+UP*.5, RIGHT*1.5+UP*(h+.5),RIGHT*.5+UP*(h+.5),UP*h).set_stroke(color=BLACK))
        self.add(
            Line(RIGHT+UP*h, UP*h, color=BLACK), 
            Line(RIGHT+UP*h, RIGHT*1.5+UP*(h+.5), color=BLACK), 
            Line(RIGHT+UP*h, RIGHT, color=BLACK), 
            )
        self.add(
            Polygon(ORIGIN, RIGHT, RIGHT+UP*h,UP*h, color=WHITE).set_fill(WHITE, opacity=1).set_stroke(opacity=0)
            )
        self.add(
            Polygon(RIGHT+UP*h,UP*h,0.5*RIGHT+(h+0.5)*UP,1.5*RIGHT+(h+0.5)*UP, color=WHITE).set_fill(WHITE, opacity=1).set_stroke(opacity=0)
            )
        self.add(
            Polygon(RIGHT, 1.5*RIGHT+0.5*UP, 1.5*RIGHT+(h+0.5)*UP,RIGHT+UP*h).set_fill(WHITE, opacity=1).set_stroke(opacity=0)
            )    
        # self.add(Square().set_fill(color=BLUE, opacity=1))

class Fibers1(Scene):
    def construct(self):
        cuboid = fiber1().scale(.5)
        # cuboid.stretch(1.5,1)
        row = VGroup(*[cuboid.copy() for i in range(5)]).arrange()
        row2 = row.copy().shift(LEFT*.5+DOWN*.5)
        row3 = row2.copy().shift(LEFT*.5+DOWN*.5)
        row4 = row3.copy().shift(LEFT*.5+DOWN*.5)
        row5 = row4.copy().shift(LEFT*.5+DOWN*.5)
        array = VGroup(row, row2, row3, row4, row5).move_to(ORIGIN)
        self.add(row, row2, row3, row4, row5)

class fiber2(VGroup):
    def __init__(self, *vmobjects, **kwargs):
        super().__init__(*vmobjects, **kwargs)
        self.add(
            Polygon(ORIGIN, 8*RIGHT, [8.5,0.5,0], [8.5,1.5,0],[0.5,1.5,0], UP).set_fill(color=WHITE, opacity=1).set_stroke(color=BLACK)
        )
        self.add(
            Line([8,1,0],UP,color=BLACK),
            Line([8,1,0],[8.5,1.5,0],color=BLACK),
            Line([8,1,0],8*RIGHT,color=BLACK),
        )



class Fibers2(Scene):
    def construct(self):
        cuboid = fiber2().scale(.5)
        # cuboid.stretch(1.5,1)
        row = VGroup(*[cuboid.copy() for i in range(5)]).arrange(DOWN)
        row2 = row.copy().shift(LEFT*.5+DOWN*.5)
        row3 = row2.copy().shift(LEFT*.5+DOWN*.5)
        row4 = row3.copy().shift(LEFT*.5+DOWN*.5)
        row5 = row4.copy().shift(LEFT*.5+DOWN*.5)
        array = VGroup(row, row2, row3, row4, row5).move_to(ORIGIN)
        self.add(row, row2, row3, row4, row5)

class fiber3(VGroup):
    def __init__(self, *vmobjects, **kwargs):
        super().__init__(*vmobjects, **kwargs)
        self.add(
            Polygon(ORIGIN, RIGHT, [4.5,4.5,0], [4.5,5.5,0],[3.5,5.5,0], UP).set_fill(color=WHITE, opacity=1).set_stroke(color=BLACK)
        )
        self.add(
            Line([1,1,0],RIGHT,color=BLACK),
            Line([1,1,0],[4.5,5.5,0],color=BLACK),
            Line([1,1,0],UP,color=BLACK),
        )

class Fibers3(Scene):
    def construct(self):
        cuboid = fiber3().scale(.6)
        # cuboid.stretch(1.5,1)
        row = VGroup(*[cuboid.copy() for i in range(5)]).arrange(RIGHT,buff=-1.7)
        column = VGroup(*[cuboid.copy() for i in range(5)]).arrange(UP, buff=-2.5)
        b = .8
        row2 = row.copy().shift(DOWN*b)
        row3 = row2.copy().shift(DOWN*b)
        row4 = row3.copy().shift(DOWN*b)
        row5 = row4.copy().shift(DOWN*b)

        columns = VGroup(*[column.copy() for i in range(5)]).arrange(buff=-1.8)
        array = VGroup(row, row2, row3, row4, row5).move_to(ORIGIN)
        for i in range(5):
            self.add(*[columns[i][j] for j in range(5)])


class slice1(VGroup):
    def __init__(self, *vmobjects, **kwargs):
        super().__init__(*vmobjects, **kwargs)
        bias = np.array([])
        self.add(
            Polygon(ORIGIN, 8*RIGHT, [8+4,4,0], [8+4,4.5,0],[4,4.5,0], 0.5*UP).set_fill(color=WHITE, opacity=1).set_stroke(color=BLACK)
        )
        self.add(
            Line([8,0.5,0],8*RIGHT,color=BLACK),
            Line([8,0.5,0],[8+4,4.5,0],color=BLACK),
            Line([8,0.5,0],0.5*UP,color=BLACK),
        )

class Slices1(Scene):
    def construct(self):
        row = slice1().scale(.6)
        # cuboid.stretch(1.5,1)
        b = 1
        row2 = row.copy().shift(DOWN*b)
        row3 = row2.copy().shift(DOWN*b)
        row4 = row3.copy().shift(DOWN*b)
        row5 = row4.copy().shift(DOWN*b)
        array = VGroup(row, row2, row3, row4, row5).move_to(ORIGIN)
        self.add(row5, row4, row3, row2, row)


class slice2(VGroup):
    def __init__(self, *vmobjects, **kwargs):
        super().__init__(*vmobjects, **kwargs)
        self.add(
            Polygon(ORIGIN, [4,4,0], [4,10,0], [3.5,10,0], [-0.5,6,0],[-0.5,0,0]).set_fill(color=WHITE, opacity=1).set_stroke(color=BLACK)
        )
        self.add(
            Line([0,6,0],[-0.5,6,0],color=BLACK),
            Line([0,6,0],[4,10,0],color=BLACK),
            Line([0,6,0],ORIGIN,color=BLACK),
        )

class Slices2(Scene):
    def construct(self):
        row = slice2().scale(.7)
        # cuboid.stretch(1.5,1)
        b = 1
        row2 = row.copy().shift(LEFT*b)
        row3 = row2.copy().shift(LEFT*b)
        row4 = row3.copy().shift(LEFT*b)
        row5 = row4.copy().shift(LEFT*b)
        array = VGroup(row, row2, row3, row4, row5).move_to(ORIGIN)
        self.add(row5, row4, row3, row2, row)


class slice3(VGroup):
    def __init__(self, *vmobjects, **kwargs):
        super().__init__(*vmobjects, **kwargs)
        self.add(
            Polygon(ORIGIN, [8,0,0], [8.3,0.3,0], [8.3,8.3,0], [0.3,8.3,0],[0,8,0]).set_fill(color=WHITE, opacity=1).set_stroke(color=BLACK)
        )
        self.add(
            Line([8,8,0],[8.3,8.3,0],color=BLACK),
            Line([8,8,0],[0,8,0],color=BLACK),
            Line([8,8,0],RIGHT*8,color=BLACK),
        )

class Slices3(Scene):
    def construct(self):
        row = slice3().scale(.6)
        # cuboid.stretch(1.5,1)
        b = .5
        row2 = row.copy().shift(UR*b)
        row3 = row2.copy().shift(UR*b)
        row4 = row3.copy().shift(UR*b)
        row5 = row4.copy().shift(UR*b)
        array = VGroup(row, row2, row3, row4, row5).move_to(ORIGIN)
        self.add(row5, row4, row3, row2, row)