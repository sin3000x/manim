from manimlib.imports import *


class Coins(VGroup):
    def __init__(self, num=8, *vmobjects, **kwargs):
        # coins = [Coin(stroke_width=.1).scale(.5).shift(UP*np.random.random()*4-2+RIGHT*np.random.random()*4-2) for i in range(num)]
        coins = [Coin(stroke_width=.1).scale(.5) for i in range(num)]
        super().__init__(*coins, **kwargs)
        self.arrange()


class Integers(VGroup):
    def __init__(self, low=-4, high=4, step=1, buff=MED_SMALL_BUFF, **kwargs):
        integers = list(range(low, high + 1, step))
        integers = [TexMobject(str(i)) for i in integers]
        super().__init__(*integers, **kwargs)
        self.arrange(buff=buff)


class opening(Scene):
    def construct(self):
        series = VideoSeries(num_videos=8, gradient_colors=[PINK_A, PINK_B], ).set_width(FRAME_WIDTH - 3).to_edge(UP,
                                                                                                                  buff=LARGE_BUFF)
        coins = Coins().to_edge(BOTTOM)
        brace_s, brace_c = Brace(series, DOWN), Brace(coins, DOWN)
        label_s, label_c = Heiti(r"8个", color=PINK_B).next_to(brace_s, DOWN), Heiti("8个", color=BLUE_COIN).next_to(
            brace_c, DOWN)
        arrows = VGroup(
            *[Line(coin.get_top(), serie.get_bottom(), buff=MED_SMALL_BUFF, color=YELLOW).add_tip(tip_length=.2) for
              coin, serie in zip(coins, series)])
        one2one = TextMobject(r"\kaishu 一一对应", color=YELLOW).scale(1.3).to_edge(DOWN)
        one2multi = VGroup(*[Line(coins[i].get_top(), series[j].get_bottom(), buff=MED_SMALL_BUFF)
                           .add_tip(tip_length=.2) for i, j in zip([3, 3], [3, 4])]).set_color(YELLOW)
        injective = VGroup(*[Line(coins[i].get_top(), series[j].get_bottom(), buff=MED_SMALL_BUFF)
                           .add_tip(tip_length=.2) for i, j in zip([3, 4], [3, 4])]).set_color(YELLOW)

        cross = Cross(series[0]).move_to(one2multi.get_center()).shift(LEFT * .1)
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
        self.play(GrowArrow(one2multi[0]), GrowArrow(one2multi[1]), )
        self.play(ShowCreation(cross))
        self.wait()
        self.play(FadeOut(VGroup(cross, one2multi)))
        self.wait()

        self.play(RT(demands[0], demands[1]),
                  GrowArrow(injective[0]),
                  GrowArrow(injective[1]),
                  )
        self.wait()
        # self.play(FadeOut(injective))
        self.play(RT(demands[1], demands[2]),
                  *[GrowArrow(i) for i in arrows[:3]],
                  *[GrowArrow(i) for i in arrows[5:]],
                  )
        self.wait()
        self.play(RT(demands[2], one2one))
        self.wait()


class z2z(Scene):
    def construct(self):
        integers = Integers(1, 10, buff=LARGE_BUFF).set_color(PINK_B).scale(1.2).to_edge(UP, buff=2)
        integers2 = Integers(2, 20, 2, buff=MED_LARGE_BUFF).set_color(BLUE_COIN).scale(1.2).to_edge(DOWN, buff=2)
        for i2, i in zip(integers2, integers):
            i2.set_x(i.get_x())

        integers[-1].become(TexMobject(r"\cdots", color=PINK_B).scale(1.2).next_to(integers[-2], buff=LARGE_BUFF))
        integers2[-1].become(
            TexMobject(r"\cdots", color=BLUE_COIN).scale(1.2).next_to(integers2[-2]).align_to(integers[-1], LEFT))

        arrows = [Arrow(up.get_bottom(), down.get_top(), buff=.5, color=YELLOW) for up, down in
                  zip(integers[:-1], integers2[:-1])]
        arrows2 = [Arrow(down.get_top(), up.get_bottom(), buff=.5, color=YELLOW) for up, down in
                   zip(integers[:-1], integers2[:-1])]
        arrows = VGroup(*arrows)
        arrows2 = VGroup(*arrows2)
        map_label = TexMobject(*" f ( n ) = 2 n".split(), color=YELLOW).to_edge(UP)
        invmap_label = TexMobject(*"f ^ {-1} ( n ) = {n \\over 2}".split(), color=YELLOW).to_edge(UP)
        comment = VGroup(TexMobject(r"\mathbb{N}^*", r"~\text{\kaishu 与}~", r"2\mathbb{N}^*", r"~\text{\kaishu 有相同的}"),
                         TextMobject("\\kaishu 元素个数.")).arrange(buff=0.1).to_edge(DOWN)
        comment[0][0].set_color(PINK_B)
        comment[0][2].set_color(BLUE_COIN)
        equinumerous = TexMobject(r"\mathbb{N}^*", r"\sim", r"2\mathbb{N}^*").scale(1.2).to_edge(DOWN)
        equinumerous[0].set_color(PINK_B)
        equinumerous[2].set_color(BLUE_COIN)
        # bg = BackgroundRectangle(map_label)
        # bg2 = BackgroundRectangle(invmap_label)
        self.play(Write(integers), run_time=3)
        self.play(Write(integers2), run_time=3)
        self.wait()
        self.play(LaggedStartMap(GrowArrow, arrows, lag_ratio=.2))
        self.wait()
        # self.play(FadeIn(bg2))
        self.play(Write(map_label))
        self.wait()
        self.play(RT(arrows, arrows2), RT(map_label, invmap_label), )
        self.wait()
        self.play(Write(comment))
        self.wait()
        self.play(Transform(comment[1], TextMobject("\\kaishu 势（基数）.").next_to(comment[0], buff=.1)))
        self.wait()
        self.play(RT(comment, equinumerous))
        self.wait()
        self.play(FadeOut(VGroup(integers, integers2, arrows2, invmap_label)),
                  )
        self.play(FocusInto(equinumerous, fade=0))
        self.wait()


class continuum(Scene):
    def construct(self):
        prob = TextMobject("无限集", r"与它的某", "真子集", "对等.").scale(1.5)
        prob[0].set_color(YELLOW)
        prob[2].set_color(RED)
        self.play(Write(prob[1:]))
        self.wait()
        self.play(Write(prob[0]))
        self.wait()
        self.play(prob.to_edge, TOP)
        sets = TexMobject(
            *r"\mathbb{N}^* \sim 2\mathbb{N}^* \sim \mathbb{Z} \sim \mathbb{N}\times\mathbb{N} \sim \mathbb{Q} \sim \cdots".split()) \
            .tm({'mathbb': YELLOW}).scale(1.5).next_to(prob, DOWN, buff=1.5)
        self.play(Write(sets))
        self.wait()
        brace = Brace(sets, DOWN, color=WHITE)
        label = TextMobject(r"\kaishu 可数集（可列集）", color=YELLOW).next_to(brace, DOWN)
        aleph0 = TextMobject(r"$\aleph_0$").scale(1.5)
        # aleph0[0].set_color(YELLOW)
        self.play(GrowFromCenter(brace))
        self.play(Write(label))
        self.wait()
        self.play(FadeOut(prob), VGroup(sets, brace, label).to_edge, UP, run_time=2)
        self.wait()
        aleph0.move_to(label)

        N = TexMobject(r"1,2,3,4,5,6,7,8,9,\cdots").scale(1.5)
        N2 = TexMobject(r"2,4,6,8,10,12,14,16,\cdots").scale(1.5)
        Z = TexMobject(r"0,1,-1,2,-2,3,-3,4,-4,\cdots").scale(1.5)
        v = VGroup(N, N2, Z).arrange(DOWN, buff=0.8).next_to(label, DOWN, buff=LARGE_BUFF)
        for set in v:
            self.play(Write(set))
            self.wait()

        uncountable = TexMobject(*r"(0,1) \sim [0,1] \sim \mathbb{R} \sim \mathbb{C} \sim \cdots".split()).tm(
            {"0": YELLOW, "mathbb": YELLOW}).scale(1.5).next_to(label, DOWN, buff=1)
        uncountable_brace = Brace(uncountable, DOWN)
        aleph1 = TexMobject(r"\aleph_1").scale(1.5).next_to(uncountable_brace, DOWN)

        no_biggest = TextMobject("\\heiti 无最大基数定理：没有最多，只有更多.", color=YELLOW).scale(1.2).to_edge(DOWN,
                                                                                                buff=MED_LARGE_BUFF)
        chain = TexMobject(r"\aleph_0<", r"\aleph_1", r"<\aleph_2<\aleph_3<\cdots").scale(1.5).move_to(no_biggest)

        self.play(FadeOut(v))
        self.play(Write(uncountable))
        self.wait()
        self.play(RT(label, aleph0))
        self.wait()
        self.play(GrowFromCenter(uncountable_brace))
        self.play(Write(aleph1))
        self.wait()
        self.play(Write(no_biggest))
        self.wait()
        self.play(RT(no_biggest, chain))
        self.wait()
        self.play(Indicate(chain[1]))
        self.wait()
        self.play(FadeOut(VGroup(sets, uncountable, brace, uncountable_brace, aleph0, aleph1, chain[2:])),
                  chain[:2].move_to, ORIGIN + UP * 2, run_time=2)
        hypo = TextMobject("\\kaishu 没有中间的基数", color=YELLOW).next_to(chain[0][-1], UP, buff=LARGE_BUFF)
        arrow = Arrow(hypo.get_bottom(), chain[0][-1].get_top())
        title = TextMobject("\\underline{\\textbf{\\heiti 连续统假设}}", color=YELLOW).to_corner(UL)
        self.play(GrowArrow(arrow))
        self.play(Write(hypo))
        self.wait()
        self.play(Write(title))
        self.wait()

        timeline = NumberLine(x_min=1870, x_max=1970, unit_size=0.1, tick_frequency=50, include_ticks=False,
                              include_tip=True).shift(DOWN * 2 + LEFT * 192)
        self.play(ShowCreation(timeline))
        ticks = VGroup(*[timeline.get_tick(i) for i in [1878, 1900, 1940, 1963]])
        # self.add(ticks)
        # timeline.add_numbers(1878,1900,1940,1963)
        images = [ImageMobject('cantor'), ImageMobject('hilbert'), ImageMobject('godel'), ImageMobject('cohen')]
        names = [TextMobject("Georg Cantor"), TextMobject("David Hilbert"), TextMobject("Kurt Gödel"),
                 TextMobject("Paul Cohen")]
        years = [TextMobject(f"{i}") for i in [1878, 1900, 1940, 1963]]
        contents = [TextMobject(f"\\kaishu {i}", color=YELLOW) for i in ["提出", "第一问", "相容性", "独立性"]]
        for i in range(4):
            images[i].next_to(ticks[i], UP, buff=1)
            names[i].scale(.62).next_to(images[i], DOWN)
            years[i].scale(.8).next_to(ticks[i], DOWN)
            contents[i].next_to(years[i], DOWN, buff=.5)

            self.play(FadeIn(VGroup(years[i], ticks[i])))
            self.play(FadeInFrom(images[i], UP), Write(names[i]))
            self.wait()
            self.play(Write(contents[i]))
            self.wait()

        independence = TextMobject("与ZFC公理系统是独立的.").shift(UP * 2)
        cannot = TextMobject("我们证明了这个问题是不可证明的.").move_to(independence)
        self.play(RT(VGroup(chain[:2], hypo, arrow), independence))
        self.wait()
        self.play(RT(independence, cannot))
        self.wait()


class countable(Scene):
    def construct(self):
        title = TextMobject(r"\underline{\textbf{\heiti 一些定理...}}", color=YELLOW).to_corner(UL)
        self.play(Write(title))
        theorems = VGroup(
            TextMobject("\\heiti 定理1：", r"任意", r"无限集", r"都包含一个", r"可数的子集", r".").tm({"无限": YELLOW, "子集": YELLOW}),
            TextMobject("\\heiti 定理2：", r"可数集", r"的", r"无限子集", r"都是", r"可数集", r".").tm({"无限": YELLOW, "可数集": YELLOW, }),
            TextMobject("\\heiti 定理3：", r"加上（去掉）", "至多可数", "个元素", "不改变", "无限集的基数.").tm({"至多可数": YELLOW, "不": YELLOW}),
        ).arrange(DOWN, aligned_edge=LEFT, buff=2).align_to(title, LEFT)
        self.play(Write(theorems[0]))
        self.wait()
        proof1 = TexMobject(r"\{a_1,a_2,a_3,\cdots\}").next_to(theorems[0][2], DOWN)
        self.play(Write(proof1[0][0]))
        self.play(RT(theorems[0][2].copy(), proof1[0][1:3]))
        self.wait()
        self.play(Write(proof1[0][3]))
        self.play(RT(theorems[0][2].copy(), proof1[0][4:6]))
        self.wait()
        self.play(Write(proof1[0][6]))
        self.play(RT(theorems[0][2].copy(), proof1[0][7:9]))
        self.wait()
        self.play(Write(proof1[0][9:]))
        self.wait()

        self.play(Write(theorems[1]))
        self.wait()
        ex2 = TexMobject(r"\mathbb{Z}~\Longrightarrow~", r"\mathbb{N},\mathbb{N}^*,2\mathbb{Z},\cdots") \
            .next_to(theorems[1], DOWN, buff=.5).set_x(0)
        proof2 = VGroup(*[TexMobject("a_{%d}" % i) for i in range(1, 11)], TexMobject("\\cdots")).arrange(
            buff=.5).scale(1.2) \
            .next_to(ex2, DOWN, buff=.5)
        self.play(Write(ex2[0]))
        self.wait()
        self.play(Write(ex2[1:]))
        self.wait()
        self.play(Write(proof2))
        self.wait()
        for i in [0, 2, 3, 5, 7, 8, 10]:
            self.play(proof2[i].set_color, YELLOW)
        self.play(FadeOut(VGroup(proof1, proof2, ex2)))
        self.play(theorems[1].next_to, theorems[0], {"direction": DOWN, "aligned_edge": LEFT})
        aleph0 = TextMobject(r'$\aleph_0$是``最少的"无穷多.').scale(1.5)
        self.wait()
        self.play(Write(aleph0))
        self.wait()
        self.play(FadeOut(aleph0))
        theorems[2].next_to(theorems[1], DOWN, aligned_edge=LEFT)
        self.play(Write(theorems[2]), theorems[:2].fade, 0.7)
        self.wait()
        ex3 = TexMobject(r"\mathbb{N}\sim\mathbb{N}^*", ",~(0,1)\\sim [0,1]").next_to(theorems, DOWN)
        self.play(Write(ex3[0]))
        self.play(Write(ex3[1]))
        self.wait()
        self.play(FadeOut(ex3))
        theorem = TextMobject("\\heiti 定理4：可数个", r"可数集的并", r"还是", r"可数集", ".").tm({"可数集": YELLOW}) \
            .next_to(theorems, DOWN, aligned_edge=LEFT)
        self.play(Write(theorem), theorems[2].fade, 0.7)
        self.wait()
        elements = VGroup()
        for i in range(1, 5):
            elements.add(VGroup(*[TexMobject("a_{%d %d}" % (i, j)) for j in range(1, 5)], TexMobject("\\cdots")).scale(
                1.1).arrange(buff=.5))
        elements.add(VGroup(*[TexMobject("\\vdots") for _ in range(5)]).scale(1.1).arrange())
        elements.arrange(DOWN, buff=.3).next_to(theorem, DOWN, buff=.5).set_x(0)
        for i, vdot in enumerate(elements[-1]):
            vdot.set_x(elements[-2][i].get_x())
        # self.add(elements)
        # self.add(theorem_s)
        self.play(Write(elements[0]))
        self.wait()
        self.play(Write(elements[1]))
        self.wait()
        self.play(Write(elements[2:]))
        self.wait()

        h_arrows = VGroup()
        for i in range(4):
            h_arrows.add(Line(elements[i].get_left(), elements[i].get_right(), color=YELLOW).add_tip(tip_length=.2))
            self.play(GrowArrow(h_arrows[i]))
        endless = TextMobject("\\kaishu 写不完鸭", color=YELLOW).next_to(h_arrows[0], RIGHT, buff=LARGE_BUFF)
        self.wait()
        self.play(Write(endless))
        self.wait()
        self.play(FadeOut(VGroup(h_arrows, endless)))

        arrows = VGroup()
        for i in range(5):
            if i < 4:
                arrows.add(Line(elements[i][0].get_left() + [-0.1, -0.1, 0], elements[0][i].get_top() + [0.2, 0.2, 0],
                                color=YELLOW).add_tip(tip_length=.2).shift(DOWN * .1))
            else:
                arrows.add(Line(elements[i][0].get_left() + [-0.25, -0.05, 0], elements[0][i].get_top() + [0.2, 0.3, 0],
                                color=YELLOW).add_tip(tip_length=.2).shift(DOWN * .1))

            self.play(GrowArrow(arrows[i]))
        self.wait()


class rational(Scene):
    def construct(self):
        title = TextMobject(r"\underline{\textbf{\heiti $\mathbb{Q}$是可数集}}", color=YELLOW).to_corner(UL)
        self.play(Write(title))
        numberline = NumberLine(unit_size=2.5, include_numbers=True)
        zero_one = Line(numberline.n2p(0), numberline.n2p(1), color=YELLOW)
        one_two = Line(numberline.n2p(1), numberline.n2p(2), color=RED)
        neg = Line(numberline.n2p(-1), numberline.n2p(0), color=RED)
        all_l = Line(numberline.n2p(-1), numberline.n2p(-FRAME_X_RADIUS), color=RED)
        all_r = Line(numberline.n2p(2), numberline.n2p(FRAME_X_RADIUS), color=RED)
        zero_one_int = TexMobject("[0,1)", color=YELLOW).scale(1.2).next_to(numberline, UP, buff=LARGE_BUFF).shift(
            LEFT * 1.7)
        one_two_int = TexMobject("[1,2)", color=RED).scale(1.2).next_to(numberline, UP, buff=LARGE_BUFF).shift(
            RIGHT * 1.7)
        arrow = Arrow(zero_one_int.get_right(), one_two_int.get_left())
        neg_int = TexMobject("[-1,0)", color=RED).scale(1.2).next_to(arrow, RIGHT)
        n_int = TexMobject("[n,n+1)", color=RED).scale(1.2).next_to(arrow, RIGHT)
        f = TexMobject("x", "+", "1").next_to(arrow, UP)
        neg_f = TexMobject("x", "-", "1").next_to(arrow, UP)
        fn = TexMobject("x", "+", "n").next_to(arrow, UP)
        self.play(FadeIn(numberline))
        self.play(ShowCreation(zero_one), Write(zero_one_int))
        self.wait()
        self.play(RT(zero_one.copy(), one_two, path_arc=np.pi), Write(one_two_int))
        self.play(GrowArrow(arrow), Write(f))
        self.wait()
        self.play(RT(zero_one.copy(), neg, path_arc=-np.pi), RT(one_two_int, neg_int), RT(f, neg_f))
        self.wait()

        self.play(ShowCreation(all_l), ShowCreation(all_r), RT(neg_int, n_int), RT(neg_f, fn), run_time=2)
        self.wait()
        Q0_1 = TexMobject(r"\mathbb{Q}_", "{", "[0,1)", "}", color=YELLOW).scale(1.2).next_to(zero_one, UP,
                                                                                              buff=MED_LARGE_BUFF)
        labels = VGroup()
        for i in range(-3, 3):
            if i == 0:
                continue
            labels.add(TexMobject(r"\mathbb{Q}", r"_{[%d, %d)}" % (i, i + 1), color=RED).scale(1.2).next_to(
                numberline.n2p(i + 0.5), UP, buff=MED_LARGE_BUFF))
        # for lab in labels:
        #     lab[1].set_width(Q0_1[1:].get_width(), stretch=True)
        self.play(RT(VGroup(arrow, fn, n_int, zero_one_int), Q0_1))
        self.wait()
        self.play(Write(labels))
        self.play(VGroup(labels, Q0_1, numberline, zero_one, one_two, neg, all_r, all_l).shift, UP)

        rationals = VGroup(TexMobject("0"))
        for i in range(2, 6):
            tmp = VGroup()
            for j in range(1, i):
                tmp.add(TexMobject(rf"\tfrac {j}{i}").scale(1.2))
            tmp.arrange(buff=.5)
            rationals.add(tmp)
        rationals.arrange(DOWN, aligned_edge=LEFT).next_to(numberline, DOWN, buff=0).set_color(YELLOW)

        arrows = VGroup(
            *[Line(i.get_left() + LEFT * .2, i.get_right() + RIGHT * .3).add_tip(tip_length=.2) for i in rationals])
        self.play(RT(Q0_1.copy(), rationals))
        self.wait()
        for arrow in arrows:
            self.play(GrowArrow(arrow))
        self.wait()

        self.play(FadeOut(arrows))
        for _ in range(2):
            self.play(ShowPassingFlashAround(rationals[1]),
                      ShowPassingFlashAround(rationals[3][1]))
        self.wait()
        cross = Cross(rationals[3][1])
        self.play(ShowCreation(cross))

class real(Scene):
    def construct(self):
        title = myTitle(r"$\mathbb{R}$不是可数集").to_corner(UL)
        self.play(Write(title))