from manimlib.imports import *


class main(Scene):
    def construct(self):
        # a = TexMobject("a","^2")
        # self.add(a)
        # self.debugTeX(a)
        # self.wait()
        like = Like()
        coin = Coin()
        favo = Favo()
        laptop = Laptop()
        vs = VideoSeries()
        # p = PlayingCard()
        ab = AnimatedBoundary(like)
        # VGroup(laptop, vs, p, ab).arrange()
        self.play(Write(laptop))
        self.play(Write(vs))
        # self.play(Write(p))
        self.play(Write(ab))
        # like.repeat(100)
        # self.play(TransformFromCopy(like, coin))
        # self.play(FadeOut(like))
        # self.play(Write(like))
        # self.play(ReplacementTransform(like, coin))

        # coin.repeat(10)
        # self.play(ReplacementTransform(coin, favo))
        # self.play(Write(coin))
        # self.play(Write(favo))