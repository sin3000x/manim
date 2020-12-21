from manimlib.imports import *


class compose(Scene):
    def construct(self):
        m = {"A": RED, "B": RED}
        self.wait()
        A = VGroup(*[TexMobject(f"{i}").scale(1.2) for i in [1, 2, 3]]).arrange(DOWN, buff=LARGE_BUFF)
        B = VGroup(Like(stroke_width=.01).scale(.25), Coin(stroke_width=0.01).scale(.3), Favo().scale(.25)).arrange(
            DOWN, buff=MED_LARGE_BUFF)
        C = VGroup(*[TextMobject(fr"\kaishu {i}").scale(1) for i in ["脱单", "高分", "好运"]]).arrange(DOWN, buff=LARGE_BUFF)
        for i in range(3):
            B[i].set_y(A[i].get_y())
            C[i].set_y(A[i].get_y())
        vset = VGroup(A, B, C).arrange(buff=3)
        B.shift(RIGHT*.2)
        Ac = A.copy()
        for i in range(3):
            Ac[i].move_to(C[i])
        Ae = SurroundingEllipse(A)
        Be = SurroundingEllipse(B).set_width(Ae.get_width()).set_height(Ae.get_height(), stretch=True)
        Ce = SurroundingEllipse(C).set_width(Ae.get_width()).set_height(Ae.get_height(), stretch=True)
        Ce2 = Ce.copy()

        Al = TexMobject("A", color=RED).scale(1.3).next_to(Ae, UP)
        AlatC = TexMobject("A", color=RED).scale(1.3).next_to(Ce, UP)
        BlatC = TexMobject("B", color=RED).scale(1.3).next_to(Ce, UP)
        Bl = TexMobject("B", color=RED).scale(1.3).next_to(Be, UP)
        Cl = TexMobject("C", color=RED).scale(1.3).next_to(Ce, UP)
        Bl2 = Bl.copy().move_to(Cl)
        B2 = B.copy().move_to(C)

        b = [0, 1, 2]
        c = [0, 1, 2]
        arrows_bc = VGroup(*[Line(B[l].get_right(), C[r].get_left(), buff=.2).add_tip(tip_length=.2) for (l, r) in
                  zip(b, c)])
        arrows_bc_bi = VGroup(*[Line(B[l].get_right(), Ac[r].get_left(), buff=.2).add_tip(tip_length=.2) for (l, r) in
                  zip(b, c)])
        arrows_ab = VGroup(*[Line(A[l].get_right(), B[r].get_left(), buff=.2).add_tip(tip_length=.2) for (l, r) in
                             zip([0,1,2], [0,1,1])])
        arrows_ab_bi = VGroup(*[Line(A[l].get_right(), B[r].get_left(), buff=.2).add_tip(tip_length=.2) for (l, r) in
                             zip([0,1,2], [0,1,2])])


        f = TexMobject("f").next_to(arrows_bc, UP)
        g = TexMobject("g").next_to(arrows_ab, UP)
        self.play(ShowCreation(Be), FadeIn(Bl))
        self.play(LaggedStartMap(Write, B, lag_ratio=.5))
        self.play(ShowCreation(Ce), FadeIn(Cl))
        self.play(LaggedStartMap(Write, C, lag_ratio=.5))
        self.play(LaggedStartMap(GrowArrow, arrows_bc, lag_ratio=.5))
        self.play(Write(f))
        self.wait()

        # A appears
        self.play(ShowCreation(Ae), FadeIn(Al))
        self.play(LaggedStartMap(Write, A, lag_ratio=.5))
        self.wait()
        self.play(LaggedStartMap(GrowArrow, arrows_ab, lag_ratio=.5))
        self.wait()
        self.play(Write(g))
        self.wait()

        # composition
        scope = TexMobject(r"f\circ g",r"\colon","A", r"\to", "C").to_edge(DOWN).tm({"A": RED, "C": RED})
        definition = TexMobject(r"f\circ g",r" (x)=f\left(g(x)\right)").to_edge(DOWN)
        values = TexMobject(r"f\circ g",r"(1)=\text{\kaishu 脱单},~",r"f\circ g",r"(2)=",r"f\circ g",r"(3)=\text{\kaishu 高分}").to_edge(DOWN)
        non_abel = TexMobject(r"\text{一般地，}", r"f\circ g\neq g\circ f").to_edge(DOWN)
        nest = TexMobject(r"f\left(\left(g\left(\cdots\right)\right)\right)").to_edge(DOWN)
        associative = TexMobject(r"(f\circ g)\circ h=f\circ (g\circ h)").to_edge(DOWN)
        associative_def = TexMobject(r"f\circ g\circ h(x)=f(g(h(x)))").to_edge(DOWN)

        x = TexMobject("x", color=BLUE).scale(1.2).move_to(A)
        fx = TexMobject(*"g ( x )".split(), color=BLUE).scale(1.2).move_to(B)
        fgx = TexMobject(*"f ( g ( x ) )".split(), color=BLUE).scale(1.2).move_to(C)
        to_fade = VGroup(A[1:], B[1:], C[1:], arrows_ab[1:], arrows_bc[1:])
        self.play(Write(scope))
        self.wait()
        self.play(ReplacementTransform(scope[0], definition[0]), FadeOut(scope[1:]))
        self.play(Write(definition[1:]), run_time=2)
        self.wait()
        self.play(FadeOut(to_fade))
        self.play(Write(x))
        self.wait()
        self.play(ReplacementTransform(x, fx[-2]))
        self.play(Write(fx[:-2]), Write(fx[-1]))
        self.wait()
        self.play(ReplacementTransform(fx, fgx[2:-1]))
        self.play(Write(fgx[:2]), Write(fgx[-1]))
        self.wait()
        self.play(FadeOut(fgx))
        self.play(FadeIn(to_fade))
        self.wait()

        self.play(FadeOut(definition))
        self.play(Write(values), run_time=3)
        self.wait()
        self.play(FadeOut(values))
        self.play(Write(non_abel))
        self.wait()

        self.play(FadeOut(non_abel))
        self.play(Write(nest))
        self.wait()

        self.play(FadeOut(nest))
        self.play(Write(associative))
        self.wait()
        self.play(ReplacementTransform(associative, associative_def))
        self.wait()

        # f o f^-1
        self.play(FadeOut(VGroup(
            arrows_bc, arrows_ab, f, g,
            C, Cl,
            associative_def
                                 )))
        f.next_to(arrows_ab, UP)
        finv = TexMobject("f^{-1}").next_to(arrows_bc, UP)
        self.play(FadeIn(AlatC))
        self.play(LaggedStartMap(Write, Ac, lag_ratio=.5))
        self.wait()
        self.play(LaggedStartMap(GrowArrow, arrows_ab_bi, lag_ratio=.5))
        self.play(Write(f))
        self.play(LaggedStartMap(GrowArrow, arrows_bc_bi, lag_ratio=.5))
        self.play(Write(finv))
        self.wait()

        finvf = TexMobject(r"f",r"^{-1}",r"\circ",r"f",r"\colon","A",r"\to","A").tm(m).to_edge(DOWN)
        idA = TexMobject(r"f",r"^{-1}",r"\circ",r"f",r"=\mathrm{id}","_A").tm(m).to_edge(DOWN)
        idB = TexMobject(r"f",r"\circ",r"f",r"^{-1}",r"=\mathrm{id}","_B").tm(m).to_edge(DOWN)
        self.play(Write(finvf))
        self.wait()
        self.play(ReplacementTransform(finvf[:4], idA[:4]), ReplacementTransform(finvf[4:], idA[4:]))
        # self.play(Write(idA[1:]))
        self.wait()

        # f^-1 o f
        distance = B.get_x()-A.get_x()
        self.play(FadeOut(VGroup(A, Al, Ae, arrows_ab_bi, f)))
        self.play(VGroup(B, Ac, Bl, AlatC, Be, Ce, arrows_bc_bi, finv).shift, LEFT*distance)
        self.wait()

        arrows_ab2 = VGroup(*[Line(Ac[l].get_right(), B2[r].get_left(), buff=.2).add_tip(tip_length=.2) for (l, r) in
                              zip([0, 1, 2], [0, 1, 2])])
        f.next_to(arrows_ab2, UP)
        self.play(FadeIn(Bl2), ShowCreation(Ce2))
        self.play(LaggedStartMap(Write, B2, lag_ratio=.5))
        self.play(LaggedStartMap(GrowArrow, arrows_ab2, lag_ratio=.5))
        self.play(Write(f))
        self.wait()
        # self.play(ReplacementTransform(idA, idB))
        self.play(ReplacementTransform(idA[1], idB[3]),
                  ReplacementTransform(idA[0], idB[0]),
                  ReplacementTransform(idA[2], idB[1]),
                  ReplacementTransform(idA[3], idB[2]),
                  ReplacementTransform(idA[4], idB[4]),
                  )
        self.play(ReplacementTransform(idA[-1], idB[-1]))
        self.wait()

        # invertible
        inv_def = TexMobject(r"\text{若有~}g\colon ","B",r"\to",r" A",r"~\text{使}~",r"g\circ f=\mathrm{id}","_A", ",~",
                             r"f\circ g=\mathrm{id}", r"_B",r"\text{,}").tm(m).to_edge(DOWN)
        inv_def2 = TextMobject(r"称$f$可逆，$g$是$f$的逆映射.",r"可证$g$的唯一性.").to_edge(DOWN)
        theorem = TexMobject(r"f\textbf{\text{\heiti ~可逆}}~\Longleftrightarrow~f\textbf{\text{\heiti ~是双射.}}", color=YELLOW).to_edge(DOWN)
        self.play(FadeOut(idB))
        self.play(Write(inv_def), run_time=3)
        self.wait()
        self.play(FadeOut(inv_def))
        self.play(Write(inv_def2[0]), run_time=2)
        self.wait()
        self.play(Write(inv_def2[1]), run_time=2)
        self.wait()
        self.play(FadeOut(inv_def2))
        self.play(Write(theorem), run_time=2)
        self.wait(3)


class sets(Scene):
    def ShadeArrow(self, arrow, ratio=None):
        """
        这个函数写的真的太烂了
        """
        line = Line(arrow.get_start(), arrow.get_end(), color=RED)
        if ratio is None:
            ratio = 0.2 / line.get_length()
        tip = arrow.get_tip().copy().set_color(RED)
        # self.play(AnimationGroup(GrowArrow(line), FadeIn(tip), lag_ratio=ratio))
        return VGroup(line, tip), AnimationGroup(GrowArrow(line), FadeIn(tip), lag_ratio=ratio)

    def UnshadeArrow(self, arrow, ratio=None):
        line = Line(arrow.get_end(), arrow.get_start(), color=RED)
        if ratio is None:
            ratio = 0.5-0.2 / line.get_length()
        tip = arrow.get_tip().copy().set_color(RED)
        # self.play()
        return VGroup(line, tip), AnimationGroup(FadeIn(tip), GrowArrow(line), lag_ratio=ratio)

    def construct(self):
        # opening
        simple = TextMobject(*r"集 合 $A$ 到 集 合 $B$ 的 对 应 关 系".split()).scale(2)
        rule = TextMobject("$A$","的",r"任何",r"元素，都有",r"唯一的",r"$B$","中元素与之对应.").to_edge(DOWN)
        rule[2].set_color(YELLOW)
        rule[-3].set_color(YELLOW)
        VGroup(simple[:-4], simple[-4:]).arrange(DOWN).move_to(ORIGIN)
        self.play(Write(simple), run_time=2)
        self.wait()
        self.play(FadeOut(simple))

        # show two sets
        A = VGroup(*[TexMobject(f"{i}").scale(1.2) for i in [1,2,3]]).arrange(DOWN, buff=LARGE_BUFF)
        A4 = VGroup(*[TexMobject(f"{i}").scale(1.2) for i in [1,2,3,4]]).arrange(DOWN, buff=MED_LARGE_BUFF)
        B = VGroup(Like(stroke_width=.01).scale(.25), Coin(stroke_width=0.01).scale(.3), Favo().scale(.25)).arrange(DOWN, buff=MED_LARGE_BUFF)
        for i in range(3):
            B[i].set_y(A[i].get_y())
        VGroup(A, B).arrange(buff=3)
        A4.move_to(A)
        A.save_state()
        Ae = SurroundingEllipse(A)
        Be = SurroundingEllipse(B).set_width(Ae.get_width()).set_height(Ae.get_height(), stretch=True)
        Al = TexMobject("A", color=RED).scale(1.3).next_to(Ae, UP)
        Bl = TexMobject("B", color=RED).scale(1.3).next_to(Be, UP)
        self.play(ShowCreation(Ae),FadeIn(Al))
        self.play(LaggedStartMap(Write, A, lag_ratio=.1))
        self.wait(.5)
        self.play(ShowCreation(Be),FadeIn(Bl))
        self.play(LaggedStartMap(Write, B, lag_ratio=.1))
        self.wait()

        # show rule
        self.play(Write(rule))
        left = [0, 1, 2]
        right = [0, 1, 1]
        left2 = [2, 0]
        right2 = [0, 1]
        left4 = [0,1,2,3]
        right4 = [0,1,1,2]
        left3 = [0,1,2]
        right3 = [0,1,2]
        arrows = [Line(A[l].get_right(), B[r].get_left(), buff=.2).add_tip(tip_length=.2) for (l, r) in zip(left, right)]
        arrows4 = [Line(A4[l].get_right(), B[r].get_left(), buff=.2).add_tip(tip_length=.2) for (l, r) in zip(left4, right4)]
        arrows3 = [Line(A[l].get_right(), B[r].get_left(), buff=.2).add_tip(tip_length=.2) for (l, r) in zip(left3, right3)]
        arrows3_re = [Line(B[r].get_left(),A[l].get_right(),  buff=.2).add_tip(tip_length=.2) for (l, r) in zip(left3, right3)]
        arrows = VGroup(*arrows)
        arrows3 = VGroup(*arrows3)
        arrows3_re = VGroup(*arrows3_re)
        to_add = [Line(A[l].get_right(), B[r].get_left(), buff=.2).add_tip(tip_length=.2) for (l, r) in zip(left2, right2)]
        to_add[1].set_color(RED)
        for arrow in arrows:
            self.play(GrowArrow(arrow))
        self.wait()
        self.play(FadeOut(arrows[-1]))
        rule.save_state()
        self.play(rule[:2].fade, .7, rule[3:].fade, .7)
        self.wait()
        self.play(Restore(rule), GrowArrow(arrows[-1]))
        self.wait()
        self.play(GrowArrow(to_add[0]))
        self.play(rule[:-3].fade, .7, rule[-2:].fade, .7)
        self.wait()
        self.play(Restore(rule), FadeOut(to_add[0]))
        self.wait()

        # name the map, domain and image
        image_of_1 = TextMobject(r"\kaishu 1的像").next_to(B[0], RIGHT, buff=LARGE_BUFF)
        f1 = TexMobject("=f(1)").move_to(image_of_1)
        f23 = TexMobject("=f(2)=f(3)").next_to(B[1], RIGHT).align_to(f1, LEFT)
        x_of_like = VGroup(Like(stroke_width=.01).scale(.25), TextMobject(r"\kaishu 的原像")).arrange().next_to(A[0], LEFT, buff=LARGE_BUFF)
        idle = TextMobject(r"$A$中不能有闲置元素，而$B$可以有.").to_edge(DOWN)
        onto_words = TextMobject(r"当$B$没有闲置元素时，$f$称为满射.").to_edge(DOWN)
        inj_words = TextMobject(r"当$A$中不同元素的像不同时，$f$称为单射.").to_edge(DOWN)
        bij_words = TextMobject(r"若$f$同时是单射和满射，称$f$为双射.").to_edge(DOWN)
        self.play(Write(image_of_1))
        self.wait()
        self.play(Write(x_of_like))
        self.wait()

        f = TexMobject("f").next_to(arrows, UP)
        fc = TexMobject("f").next_to(arrows, UP)
        # f.save_state()
        finv = TexMobject("f","^{-1}").next_to(arrows, UP)
        onto = TextMobject(r"\kaishu 满射").move_to(f)
        inj = TextMobject(r"\kaishu 单射").move_to(f)
        bij = TextMobject(r"\kaishu 双射").move_to(f)
        self.play(Write(f))
        self.wait()
        self.play(ReplacementTransform(image_of_1, f1))
        self.wait()
        self.play(Write(f23), FadeOut(x_of_like), run_time=2)
        self.wait()
        self.play(FadeOut(VGroup(f1, f23, rule)))
        box = SurroundingRectangle(A[:2], color=RED, buff=MED_LARGE_BUFF)
        box2 = SurroundingRectangle(B[:2], color=RED, buff=MED_LARGE_BUFF)

        # f(E)
        self.play(ShowCreation(box))
        self.wait()
        new1, group1 = self.ShadeArrow(arrows[0], ratio=.25)
        new2, group2 = self.ShadeArrow(arrows[1], ratio=.25)
        self.play(group1, group2)
        self.wait()
        fE = VGroup(TexMobject(r"f( \{ 1,2 \} )"), TexMobject(r"= \{ X,X \}")).arrange(DOWN).scale(1.2).next_to(B[:2], RIGHT, buff=LARGE_BUFF)
        finvE = VGroup(TexMobject(r"f^{-1}( \{ X, X \} )"), TexMobject(r"= \{ 1,2,3 \}")).arrange(DOWN).scale(1.2).next_to(A, LEFT, buff=1.2)
        finvE[0][0][5].fade(1)
        finvE[0][0][7].fade(1)
        invElike = Like(stroke_width=.01).replace(finvE[0][0][5])
        invEcoin = Coin(stroke_width=.01).replace(finvE[0][0][7])
        # finvE = VGroup(*finvE, invElike, invEcoin)

        fE[1][0][2].fade(1)
        fE[1][0][4].fade(1)
        Elike = Like(stroke_width=.01).replace(fE[1][0][2])
        Ecoin = Coin(stroke_width=.01).replace(fE[1][0][4])
        fE = VGroup(*fE, Elike, Ecoin)

        #
        self.play(Write(fE))
        self.wait()
        self.play(FadeOut(VGroup(box, new1, new2)))
        self.wait()

        # f^-1(E)
        self.play(ShowCreation(box2))
        new3, group3 = self.UnshadeArrow(arrows[0], ratio=.3)
        new4, group4 = self.UnshadeArrow(arrows[1], ratio=.3)
        new5, group5 = self.UnshadeArrow(arrows[2], ratio=.3)
        self.wait()
        self.play(group3, group4, group5)
        self.wait()
        self.play(Write(VGroup(finvE[0], invElike, invEcoin)))
        self.play(Write(finvE[1]))
        self.wait()
        self.play(FocusOn(finvE[0][0][1:3]))
        self.wait()

        dom_range = TextMobject("$A$被称为$f$的","定义域","；","$f(A)$被称为$f$的","值域",".").to_edge(DOWN)
        dom_range[1].set_color(YELLOW)
        dom_range[-2].set_color(YELLOW)
        self.play(Write(dom_range[:3]), run_time=2)
        self.play(Write(dom_range[3:]), run_time=2)
        self.wait(2)
        self.play(FadeOut(VGroup(
            box2, fE, finvE, dom_range, invEcoin, invElike,
            new3, new4, new5
        )))

        # onto
        onto_comment = TextMobject("此时$A$的元素比$B$只多不少.").to_edge(DOWN)
        inj_comment = TextMobject("此时$A$的元素比$B$只少不多.").to_edge(DOWN)
        bij_comment = TextMobject("此时$A$与$B$元素一样多.").to_edge(DOWN)
        self.play(Write(idle))
        self.wait()
        self.play(ReplacementTransform(A, A4[:3]),
                  # ReplacementTransform(arrows[0], arrows4[0]),
                  ReplacementTransform(arrows[1], arrows4[1]),
                  ReplacementTransform(arrows[2], arrows4[2]),
                  # FadeOut(idle)
                  )
        self.play(Write(A4[-1]), GrowArrow(arrows4[-1]), ReplacementTransform(idle, onto_words))
        self.play(ReplacementTransform(f, onto))
        self.wait()
        self.play(ReplacementTransform(onto_words, onto_comment))
        self.play(FadeOut(VGroup(arrows4[1], arrows4[2], A4[1], A4[2])))
        self.wait()
        self.play(GrowArrow(to_add[1]))
        self.wait(2)
        self.play(FadeOut(VGroup(to_add[1], onto_comment)), ReplacementTransform(onto, inj))
        self.wait()
        # self.play(GrowArrow(arrows4[1]), GrowArrow(arrows4[2]), Write(VGroup(A4[1], A4[2])), FadeOut(to_add[1]))

        # injective
        self.play(Write(inj_words))
        self.wait()
        self.play(ReplacementTransform(inj_words, inj_comment))
        self.wait()
        arrows4[2].set_color(RED)
        self.play(Write(A4[1:3]), GrowArrow(arrows4[1]))
        self.wait()
        self.play(GrowArrow(arrows4[2]))
        self.wait()

        # bijective
        self.play(FadeOut(A4), FadeOut(VGroup(*arrows4[1:], arrows[0])), FadeOut(inj), FadeOut(inj_comment))
        A.restore()
        self.play(LaggedStartMap(Write, A, lag_ratio=.1))
        self.play(LaggedStartMap(GrowArrow, arrows3, lag_ratio=.4))
        self.wait()
        self.play(Write(bij_words))
        self.play(Write(bij))
        self.wait()
        self.play(ReplacementTransform(bij_words, bij_comment))
        self.wait()

        # inverse
        # f.restore()
        self.play(ReplacementTransform(bij, fc))
        self.wait()
        self.play(ReplacementTransform(arrows3, arrows3_re), ReplacementTransform(fc, finv))
        # self.play(ReplacementTransform(arrows3, arrows3_re), ReplacementTransform(fc, finv[0]), Write(finv[1]))
        self.wait()


class ex(GraphScene):
    def construct(self):
        cm = {"R": RED, "[0": BLUE}
        f = TexMobject("f(x)=x^2").to_edge(UP)
        box = SurroundingRectangle(f)

        # explaining injection and surjection
        r2r = VGroup(TexMobject(r"\R",r"\to",r" \R",r"\colon",r"~\text{不是单射，不是满射.}"),
                     TexMobject("f(-1)=f(1)=1",r",\quad","-1",r"~\text{\kaishu 在~}\R\text{~\kaishu 中没有原像.}", color=YELLOW)).arrange(DOWN)
        r2p = VGroup(TexMobject(r"\R",r"\to",r" [0,+\infty)",r"\colon",r"~\text{不是单射，是满射.}"),
                     TextMobject(r"\kaishu 任给~$y\geq 0$，都有原像~$\sqrt{y}$.", color=YELLOW)).arrange(DOWN)
        p2p = VGroup(TexMobject(r"[0,+\infty)",r"\to",r" [0,+\infty)",r"\colon",r"~\text{是单射，也是满射}",r"~\Longrightarrow~",r"\text{是双射.}"),
                     TexMobject(r"x_1\neq x_2 ~\Longrightarrow~ f(x_1)\neq f(x_2).", color=YELLOW),
                     TextMobject(r"\kaishu 有逆~", r"$f^{-1}(x)=\sqrt{x}$.", color=YELLOW)).arrange(DOWN)
        v = VGroup(r2r, r2p, p2p).arrange(DOWN, buff=MED_LARGE_BUFF).next_to(f, DOWN, buff=MED_LARGE_BUFF)
        self.wait()
        self.play(Write(f))
        self.play(ShowCreation(box))
        self.wait()
        for i, group in enumerate(v):
            group[0].tm(cm)
            if i == 0:
                self.play(Write(group[0]), run_time=2)
                self.wait()
                self.play(Write(group[1][0]), run_time=2)
                self.wait()
                self.play(Write(group[1][1:]), run_time=2)
                self.wait()
            else:
                for t in group:
                    self.play(Write(t), run_time=2)
                    self.wait()
                self.wait()
        self.play(FadeOut(VGroup(v[1:], v[0][1:])))
        self.wait()

        # plot part
        self.x_min, self.x_max = -2.2, 2.2
        self.y_min, self.y_max = -0.2, 4.2
        self.x_leftmost_tick, self.y_bottom_tick = -2, 0
        self.x_axis_width, self.y_axis_height = 6, 4.5
        self.graph_origin = LEFT*3+DOWN*3
        self.exclude_zero_label = False
        self.x_labeled_nums = [-2,-1,0,1,2]
        self.y_labeled_nums = [1,2,3,4]
        self.setup_axes(True)

        fE = TexMobject(r"f\left([-1,2]\right)=[0,4]")
        finvE = TexMobject(r"f^{-1}\left([0,4]\right)=[-2,2]")
        VGroup(fE, finvE).arrange(DOWN, buff=LARGE_BUFF).next_to(v[0], DOWN).to_edge(RIGHT, buff=LARGE_BUFF)
        graph_fE = self.get_graph(lambda x: x**2, x_min=-1, x_max=2, color=GREEN)
        graph_finvE = self.get_graph(lambda x: x**2, x_min=-2, x_max=2, color=GREEN)
        graph_part = self.get_graph(lambda x: x**2, x_min=1, x_max=2, color=GREEN).flip().shift(LEFT*(self.coords_to_point(2,0)[0]-self.coords_to_point(-1,0)[0]))

        self.play(ShowCreation(graph_fE))
        self.wait()
        self.play(Write(fE))
        self.wait()

        # self.play(ReplacementTransform(graph_fE, graph_finvE))
        self.play(ShowCreation(graph_part))
        self.wait()
        self.play(Write(finvE))
        self.wait()

class pic(Scene):
    def construct(self):
        a = VGroup(TexMobject("f(2)=").scale(4), Coin().scale(1.4)).arrange(buff=.9)
        self.add(a)