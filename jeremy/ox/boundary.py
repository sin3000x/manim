from manimlib import *

class Boundary(Scene):
    def construct(self):
        mob = VGroup()
        plane = ComplexPlane()

        square = Polygon(*[plane.n2p(i) for i in [3+3j,-3+3j,-3-3j,3-3j]])

        bound = VGroup().set_points_smoothly([[-1,3,0],[0,1,0],[1,0.5,0],[2,0,0],[3,-1,0]], True)

        ydot = Dot([2,1,0])
        y_label = Tex("\\mathcal{Y}").next_to(ydot, )

        xstar = Dot([1,.5,0])
        xstar_label = Tex("\\mathcal{X}^*").next_to(xstar, DOWN)

        dots = VGroup(
            *[Dot([x,y,0]) for x,y in zip(
                np.linspace(-2,0.7,10),
                [-2.7/(n)+0.7 for n in range(1,11)]
            )]
        )

        labels = VGroup(
            Tex(r"\mathcal{X}^{(0)}").next_to(dots[0]), 
            Tex(r"\mathcal{X}^{(1)}").next_to(dots[1])
        )

        ranks = VGroup(
            TexText("rank 2").next_to([-2,3,0],DOWN),
            TexText("rank 3").next_to([1,3,0],DOWN)
            )

        mob.add(square, bound, ydot, y_label, xstar, xstar_label,dots,labels,ranks)
        mob.set_color(BLACK)
        self.add(mob)

        