from manimlib.imports import *

class Coins(VGroup):
    def __init__(self, num=8, *vmobjects, **kwargs):
        # coins = [Coin(stroke_width=.1).scale(.5).shift(UP*np.random.random()*4-2+RIGHT*np.random.random()*4-2) for i in range(num)]
        coins = [Coin(stroke_width=.1).scale(.5) for i in range(num)]
        super().__init__(*coins, **kwargs)
        self.arrange()


class main(Scene):
    def construct(self):
        series = VideoSeries(num_videos=8, gradient_colors=[PINK_A, PINK_B],).set_width(FRAME_WIDTH-3).to_edge(UP, buff=LARGE_BUFF)
        coins = Coins().to_edge(BOTTOM)
        brace_s, brace_c = Brace(series, DOWN), Brace(coins, DOWN)
        label_s, label_c = Heiti(r"8个", color=PINK_B).next_to(brace_s, DOWN), Heiti("8个", color=BLUE_COIN).next_to(brace_c, DOWN)
        arrows = VGroup(*[Line(coin.get_top(), serie.get_bottom(), buff=MED_SMALL_BUFF, color=YELLOW).add_tip(tip_length=.2) for coin, serie in zip(coins, series)])
        one2one = TextMobject(r"\kaishu 一一对应", color=YELLOW).scale(1.3).to_edge(DOWN)
        one2multi = VGroup(*[Line(coins[i].get_top(), series[j].get_bottom(), buff=MED_SMALL_BUFF).add_tip(tip_length=.2) for i, j in zip([3,3],[3,4])])
        cross = Cross(series[0]).move_to(one2multi.get_center()).shift(LEFT*.1)
        demands = VGroup(
            TextMobject(r"\kaishu 1. 映射：每个硬币都对应了唯一视频."),
            TextMobject(r"\kaishu 2. 单射：不同硬币投给了不同视频."),
            TextMobject(r"\kaishu 3. 满射：所有视频都被投币了."),
        )
        for d in demands:
            d.scale(1.2).to_edge(DOWN).set_color(YELLOW)
        coin_add = Coin(stroke_width=.1).scale(.5).next_to(coins, RIGHT)

        self.play(Write(series))
        self.wait()
        self.play(Write(coins))
        self.wait()
        self.play(GrowFromCenter(brace_s))
        self.play(Write(label_s))
        self.play(GrowFromCenter(brace_c))
        self.play(Write(label_c))
        self.wait()
        self.play(FadeOut(VGroup(brace_c, brace_s, label_c, label_s)))
        self.play(LaggedStartMap(GrowArrow, arrows, lag_ratio=.3))
        self.wait()
        self.play(Write(one2one))
        self.wait()
        self.play(FadeOut(one2one))

        # 3 demands
        self.play(Write(demands[0]))
        self.wait()
        self.play(Write((coin_add)))
        self.wait()
        self.play(FadeOut(coin_add), FadeOut(arrows))
        self.play(LaggedStartMap(GrowArrow, one2multi, lag_ratio=.5))
        self.play(ShowCreation(cross))
        self.wait()