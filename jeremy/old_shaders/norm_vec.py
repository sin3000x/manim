#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author: Jeremy
@file:norm_vec.py
@time:2021/12/12
"""
from manimlib import *


class Opening(Scene):
    def construct(self):
        coord = NumberPlane()
        coord.add_coordinate_labels()
        vector = (4, 3)
        vec = coord.get_vector(vector).set_color(RED)
        brace = Brace(coord.get_vector((5, 0)), ORIGIN, color=YELLOW) \
            .rotate(angle_of_vector(vector)).align_to(vec, LEFT).shift(UP * 1.5 + LEFT * .1)
        vec_label = Tex(r"\vx=\begin{bmatrix}4\\3\end{bmatrix}", color=RED, ) \
            .next_to(vec.get_end(), buff=.5).add_background_rectangle()

        mod = Tex(r"|\vx|=5", color=YELLOW, isolate='=') \
            .add_background_rectangle().rotate(angle_of_vector(vector)).move_to(brace).shift(UL * .5)
        two_norm = Tex(r"\lVert\vx\rVert_2", color=YELLOW) \
            .add_background_rectangle().rotate(angle_of_vector(vector)).move_to(mod)
        self.add(coord)
        self.wait()
        self.play(GrowArrow(vec))
        self.play(Write(vec_label))
        self.wait()
        self.play(GrowFromCenter(brace))
        self.play(Write(mod))
        self.wait()
        self.play(FadeTransform(mod, two_norm))
        self.wait()

        self.remove(brace, two_norm)
        self.wait()

        line2 = Line(vec.get_start(), vec.get_end(), color=YELLOW)
        line1 = VGroup(
            Line(coord.c2p(0, 0), coord.c2p(4, 0), color=YELLOW),
            Line(coord.c2p(4, 0), coord.c2p(4, 3), color=YELLOW),
        )
        braces = VGroup(
            Brace(line1[0], DOWN, color=YELLOW),
            Brace(line1[1], RIGHT, color=YELLOW),
        )
        self.play(ShowCreation(line2))
        label2 = Tex(r"\lVert \vx \rVert_2=5", color=YELLOW) \
            .add_background_rectangle().next_to(line2.get_center(), UP).shift(LEFT)
        label1 = Tex(r"\lVert \vx \rVert_1=7", color=YELLOW) \
            .add_background_rectangle().next_to(coord.c2p(4, 0), DOWN)
        label_inf = Tex(r"\lVert \vx \rVert_\infty=4", color=YELLOW) \
            .add_background_rectangle().next_to(braces[0], DOWN)
        self.play(Write(label2))
        self.wait()

        self.play(FadeOut(VGroup(line2, label2)))
        self.wait()
        self.play(ShowCreation(line1))
        self.play(Write(label1))
        self.wait()

        taxicab = TexText("Taxicab / Manhattan norm").add_background_rectangle().move_to(DOWN * 2)
        self.play(Write(taxicab))
        self.wait()
        taxi = ImageMobject("taxi").scale(.2)
        self.play(FadeIn(taxi))
        self.wait()

        taxi.save_state()
        self.play(taxi.animate.rotate(angle_of_vector(vector)))
        self.play(taxi.animate.move_to(vec.get_end()), run_time=2)
        self.wait()
        taxi.restore()

        self.play(taxi.animate.move_to(line1[0].get_end()))
        taxi.rotate(PI / 2)
        self.play(taxi.animate.move_to(line1[1].get_end()))
        self.wait()
        taxi.restore()
        self.remove(line1)

        turnings = [coord.c2p(*i) for i in [(1, 0), (1, 1), (3, 1), (3, 3), (4, 3)]]
        turning_lines = VGroup(Line(ORIGIN, turnings[0], color=YELLOW))
        for i in range(1, len(turnings)):
            turning_lines.add(Line(turnings[i - 1], turnings[i], color=YELLOW))
        for i, t in enumerate(turnings):
            self.play(taxi.animate.move_to(t), ShowCreation(turning_lines[i]))
            if i < len(turnings) - 1:
                taxi.rotate(PI / 2 * (-1) ** i)
        self.wait()

        self.play(FadeOut(VGroup(turning_lines, label1, taxicab)), FadeOut(taxi))
        self.wait()
        self.play(ShowCreation(line1[0]), GrowFromCenter(braces[0]))
        self.play(ShowCreation(line1[1]), GrowFromCenter(braces[1]))
        self.play(Write(label_inf))


class Generalize(Scene):
    def construct(self):
        concept = Text("概念").scale(1.5)
        properties = Text("必要性质").scale(1.5)
        generalization = Text("推广的概念").scale(1.5)
        VGroup(concept, properties, generalization).arrange(buff=2)
        arrows = VGroup(
            Arrow(concept.get_right(), properties.get_left()),
            Arrow(properties.get_right(), generalization.get_left())
        )
        extract = Text("提取", color=YELLOW).next_to(arrows[0], UP)
        definition = Text("定义", color=YELLOW).next_to(arrows[1], UP)
        self.play(Write(concept))
        self.wait()
        self.play(GrowArrow(arrows[0]), Write(extract))
        self.play(Write(properties))
        self.wait()
        self.play(GrowArrow(arrows[1]), Write(definition))
        self.play(Write(generalization))
        self.wait()


class Norms(Scene):
    def construct(self):
        title = Title("norm (范数)", color=YELLOW)
        self.add(title)
        self.wait()
        map = Tex(r"\lVert\cdot\rVert\colon\C^n\to\R").next_to(title, DOWN, buff=.5)
        self.play(Write(map))
        self.wait()

        properties = VGroup(
            VGroup(Tex(r"1.~\lVert", r"\vx", r"\rVert\geq0").set_color_by_tex("x", RED),
                   Tex(r"\text{, 等号成立}~\iff~ ", r"\vx", r"=0").set_color_by_tex("vx", RED)).arrange(),
            VGroup(Tex(r"2.~\lVert", r"\alpha", r"\vx", r"\rVert=|", r"\alpha", r"|\lVert", r"\vx", r"\rVert")
                   .tm({"x": RED, "alpha": BLUE}),
                   ).arrange(),
            VGroup(Tex(r"3.~\lVert", r"\vx", r"+", r"\vy", r"\rVert\leq\lVert", r"\vx", r"\rVert", r"+\lVert", r"\vy",
                       r"\rVert")
                   .tm({'vx': RED, 'vy': RED}),
                   ).arrange()
        ).arrange(DOWN, aligned_edge=LEFT, buff=.5).next_to(map, DOWN, buff=1)
        for p in properties:
            for t in p:
                self.play(Write(t))
                self.wait()


class pNorm(Scene):
    def construct(self):
        title = Title(r"p-norm: $\lVert x\rVert_p$", color=YELLOW)
        self.add(title)
        self.wait()
        p_norm = Tex(r"\lVert ", r"\vx", r" \rVert_p\coloneqq\sqrt[p]{|", r"x_1", r"|^p+\cdots+|", r"x_n",
                     r"|^p},~p\geq1") \
            .set_color_by_tex('x', RED).next_to(title, DOWN, buff=.5)
        self.play(Write(p_norm))
        self.wait()

        norms = VGroup(
            Tex(r"\lVert ", r"\vx", r" \rVert_1=|", r"x_1", r"|+\cdots+|", r"x_n", r"|"),
            Tex(r"\lVert ", r"\vx", r" \rVert_2=\sqrt{|", r"x_1", r"|^2+\cdots+|", r"x_n", r"|^2}", r"=\sqrt{x^H x}"),
            Tex(r"\lVert ", r"\vx", r" \rVert_\infty=\max_{1\leq i\leq n}|", "x_i", "|"),
        ).arrange(DOWN, buff=.5, aligned_edge=LEFT).next_to(p_norm, DOWN, buff=1)
        for n in norms:
            n.tm({'x': RED, 'max': WHITE})
        # VGroup(norms[1][-1][0:3], norms[1][-1][4]).set_color(WHITE)
        norms[1][-1].set_color(YELLOW)
        self.play(Write(norms[0]))
        self.wait()
        self.play(Write(norms[1][:7]))
        self.wait()
        self.play(Write(norms[1][7:]))
        self.wait()
        self.play(Write(norms[2]))
        self.wait()


class Translation(Scene):
    def construct(self):
        title = Title("为什么叫范数", color=YELLOW)
        self.add(title)
        self.wait()


class UnitDisc(Scene):
    def construct(self):
        title = Title(r"$\lVert \vx \rVert=1$", color=YELLOW)
        self.add(title)
        axes = VGroup(*[
            Axes(height=3, width=3, x_range=[-1.5, 1.5], y_range=[-1.5, 1.5], axis_config={"include_ticks": False}) for
            i in range(3)
        ]).arrange(buff=1).next_to(title, DOWN, buff=1.5)
        self.add(axes)
        self.wait()

        norms = VGroup(
            Tex(r"\lVert\vx\rVert_1=1"),
            Tex(r"\lVert\vx\rVert_2=1"),
            Tex(r"\lVert\vx\rVert_\infty=1"),
        )

        discs = VGroup(
            Polygon(*[axes[0].c2p(*i) for i in [(1, 0), (0, 1), (-1, 0), (0, -1)]], color=RED),
            Circle(arc_center=axes[1].get_origin(), radius=axes[1].get_x_axis().get_unit_size(), color=GREEN),
            Polygon(*[axes[2].c2p(*i) for i in [(1, 1), (-1, 1), (-1, -1), (1, -1)]], color=BLUE),
        )

        equations = VGroup(
            Tex("|x|+|y|=1", color=discs[0].get_color()),
            Tex(r"\sqrt{x^2+y^2}=1", color=discs[1].get_color()),
            Tex(r"\max(|x|,|y|)=1", color=discs[2].get_color())
        )
        for i in range(len(norms)):
            norms[i].next_to(axes[i], UP, buff=.5)
            equations[i].next_to(axes[i], DOWN, buff=.5)

            self.play(Write(norms[i]))
            self.wait()
            self.play(ShowCreation(discs[i]), Write(equations[i]))
            self.wait()


class Unitary(Scene):
    def construct(self):
        title = Title(r"$\lVert Q\vx\rVert_2=\lVert \vx\rVert_2$", color=YELLOW)
        self.add(title)
        self.wait()
        condition = Tex(r"\text{If~}", r"Q", r"\text{~is unitary (酉矩阵)}: ", r"Q", r"^H", r"Q", r"=I", r",") \
            .next_to(title, DOWN, buff=.5).to_edge(LEFT, buff=1).tm({'Q': RED})
        condition[3:-1].set_color(YELLOW)
        proof = VGroup(
            Tex(r"\lVert ", "Q", r"\vx \rVert_2^2", r"=", r"(", r"Q", r"\vx)^H(", r"Q", r"\vx)").tm({'Q': RED}),
            Tex(r"=\vx^H", r"Q^HQ", r"\vx").set_color_by_tex('Q', YELLOW),
            Tex(r"=\vx^H\vx"),
            Tex(r"=\lVert \vx \rVert_2^2")
        ).arrange(DOWN, buff=.5).next_to(condition, DOWN, buff=.5).set_x(0)
        for i in proof[1:]:
            i.align_to(proof[0][3], LEFT)
        self.play(Write(condition))
        self.wait()
        self.play(Write(proof), run_time=4)
        self.wait()


class Invariant(LinearTransformationScene):
    CONFIG = {
        "show_basis_vectors": False,
        "foreground_plane_kwargs": {
            "x_range": [-8, 8],
            "y_range": [-8, 8],
            "faded_line_ratio": 0
        },
    }

    def construct(self):
        vector = Vector((3, 2)).set_color(YELLOW)
        self.add_transformable_mobject(vector)
        circle = Circle(radius=get_norm((3, 2)))
        self.play(GrowArrow(vector))
        self.play(ShowCreation(circle))
        self.wait()
        # import scipy.linalg.decomp_qr as qr
        # q, _ = qr.qr(np.random.rand(2,2))
        t = PI / 3
        m = [[np.cos(t), np.sin(t)], [-np.sin(t), np.cos(t)]]
        self.apply_matrix(m, run_time=3)
        self.wait()


class Holder(Scene):
    def construct(self):
        title = Title(r"H\"older inequality", color=YELLOW)
        self.add(title)
        condition = Tex(r"\text{若~}{1\over", r" p}", r"+{1\over", r" q}", r"=1,\text{ 则}") \
            .next_to(title, DOWN, buff=.5).to_edge(LEFT, buff=1)
        holder = Tex(r"|\vx^H\vy|\leq\lVert \vx \rVert_", r"p", r"\lVert \vy \rVert_", r"q") \
            .scale(1.2).next_to(condition, DOWN).set_x(0)
        condition2 = Tex(r"\text{当~}", "p", r"=", r"q", r"=2:") \
            .next_to(holder, DOWN, buff=.7).align_to(condition, LEFT)
        cauchy = Tex(r"|\vx^H\vy|\leq\lVert \vx \rVert_", r"2", r"\lVert \vy \rVert_", r"2") \
            .scale(1.2).next_to(condition2, DOWN).set_x(0)

        v = VGroup(condition, holder, condition2, cauchy)
        for i in v:
            i.tm({"p": RED, 'q': BLUE, 'leq': WHITE})
            self.play(Write(i))
            self.wait()
        label = TexText("Cauchy-Schwarz inequality", color=YELLOW).next_to(cauchy, DOWN, buff=.5)
        self.play(Write(label))
        self.wait()


class Proof1(Scene):
    def construct(self):
        cm = {'t': RED, 'text': WHITE, 'Vert': WHITE}
        title = Title(r"$|\langle\vx,\vy\rangle|\leq\lVert\vx\rVert_2\lVert\vy\rVert_2$", color=YELLOW)
        self.add(title)
        self.wait()
        consider = Tex(r"\text{考虑~}", r"\vx+", "t", r"\vy:").tm(cm).next_to(title, DOWN, buff=.5).to_edge(LEFT, buff=1)
        self.play(Write(consider))
        self.wait()
        proof = VGroup(
            Tex("0", r"\leq", r"\lVert \vx+", r"t", r"\vy\rVert_2^2"),
            Tex(r"=(\vx+", r"t", r"\vy)^T(\vx+", r"t", r"\vy)"),
            Tex(r"=\vx^T\vx+", r"t", r"\vx^T\vy", r"+", r"t", r"\vy^T\vx", r"+", r"t", r"^2\vy^T\vy")
                .tm({r"\vx^T\vy": BLUE, r"\vy^T\vx": BLUE}),
            Tex(r"=\lVert \vy \rVert_2^2", r"t", r"^2", r"+", r"2\vx^T\vy ", r"t", r"+\lVert\vx\rVert_2^2")
                .tm({r"\vx^T\vy": BLUE})
        ).arrange(DOWN, buff=.3).next_to(consider, DOWN, buff=.5)
        for p in proof:
            p.tm(cm)
        for p in proof[1:]:
            p.align_to(proof[0][1], LEFT)
        proof.set_x(0)
        for p in proof:
            self.play(Write(p))
            self.wait()

        delta = Tex(r"\Delta=(2\vx^T\vy)^2-4\lVert\vx\rVert_2^2\lVert\vy\rVert_2^2\leq0", color=YELLOW) \
            .next_to(proof, DOWN, buff=.5)
        self.play(Write(delta), run_time=2)
        self.wait()


class Conjugate(Scene):
    def construct(self):
        cm = {'t': RED, 'text': WHITE, 'Vert': WHITE}
        title = Tex(r"\vy^H\vx=\overline{\vx^H\vy}", color=BLUE).to_edge(UP, buff=1)
        self.add(title)
        self.wait()
        proof0 = Tex(r"\vy^H\vx=\bar{\vy}^T\vx=\vx^T\bar{\vy}=\bar{\vx}^H\bar{\vy}=\overline{\vx^H\vy}").next_to(title,
                                                                                                                 DOWN)
        self.play(Write(proof0))
        self.wait()

        line = Line(color=YELLOW).set_width(FRAME_WIDTH).next_to(proof0, DOWN, buff=.5)
        proof = VGroup(
            Tex("0", r"\leq", r"\lVert \vx+", r"t", r"\vy\rVert_2^2"),
            Tex(r"=\lVert \vy \rVert_2^2|", r"t", r"|^2", r"+", r"2\Re(\vx^H\vy ", r"t", r")+\lVert\vx\rVert_2^2")
        ).arrange(DOWN, buff=.3).next_to(proof0, DOWN, buff=1)
        proof[1].align_to(proof[0][1], LEFT)
        proof.set_x(0)
        self.play(GrowFromCenter(line))
        for p in proof:
            p.tm(cm)
            self.play(Write(p))
            self.wait()
        t = Tex(r"\text{取~}", "t", r"=-{\vy^H\vx\over\lVert\vy\rVert_2^2}:").tm(cm).next_to(proof, DOWN).to_edge(LEFT,
                                                                                                                 buff=1)
        conclusion = Tex(r"\lVert\vx\rVert_2^2-{|\vx^H\vy|^2\over\lVert\vy\rVert_2^2}\geq0", color=YELLOW)
        VGroup(t, conclusion).arrange().next_to(proof, DOWN, buff=.5)
        self.play(Write(t))
        self.wait()
        self.play(Write(conclusion))
        self.wait()


class Proof2(Scene):
    def construct(self):
        cm = {'t': RED, 'text': WHITE, 'Vert': WHITE}
        title = Title(r"$|\langle\vx,\vy\rangle|\leq\lVert\vx\rVert_2\lVert\vy\rVert_2$", color=YELLOW)
        self.add(title)
        self.wait()
        consider = Tex("\\text{考虑~}", r"A=[\vx,\vy]: ").next_to(title, DOWN, buff=.5).to_edge(LEFT, buff=1)
        self.play(Write(consider))
        self.wait()

        pos = VGroup(
            VGroup(Tex(r"A^HA", r"=\begin{bmatrix}\vx^H\vx & \vx^H\vy\\ \vy^H\vx & \vy^H\vy\end{bmatrix}", r"="
                                                                                                           r"\begin{bmatrix}\lVert\vx\rVert_2^2 & \vx^H\vy\\[5pt] \overline{\vx^H\vy} & \lVert\vy\rVert_2^2\end{bmatrix}"),
                   TexText("是", r"半正定矩阵", r":")).arrange(),
            Tex(r"\vx^H", r"A^HA", r"\vx=(A\vx)^H(A\vx)=\lVert A\vx\rVert_2^2\geq0").set_color_by_tex('A^HA', RED)
        ).arrange(DOWN).next_to(consider, DOWN).set_x(0)
        VGroup(pos[0][0][0], pos[0][0][-1]).set_color(RED)
        pos[0][1][1].set_color(YELLOW)
        self.play(Write(pos[0]))
        self.wait()
        self.play(Write(pos[1]))
        self.wait()

        imply = Tex("\\text{于是~}", r"\det(A^HA)\geq0", r":") \
            .set_color_by_tex('A', YELLOW).next_to(pos, DOWN, buff=.5).align_to(consider, LEFT)
        self.play(Write(imply))
        self.wait()

        det = Tex(r"\lVert\vx\rVert_2^2\lVert\vy\rVert_2^2-|\vx^H\vy|^2\geq0", color=YELLOW) \
            .next_to(imply, DOWN).set_x(0)
        self.play(Write(det))
        self.wait()


class Pic(Scene):
    def construct(self):
        norm = Tex(r"\lVert\vx\rVert").scale(8)
        self.add(norm)