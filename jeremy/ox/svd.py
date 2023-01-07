from manimlib import *

class SVD(Scene):
    def construct(self) -> None:
        a = np.arange(24).reshape(6,4)
        A = IntegerMatrix(a)
        [u,s,vt] = np.linalg.svd(a)

        a1 = np.outer(u[:,0], vt[0,:])*s[0]
        A1 = DecimalMatrix(a1)

        group = VGroup(A, Tex("\\approx"), A1).arrange().set_color(BLACK)
        self.add(group)
        return super().construct()