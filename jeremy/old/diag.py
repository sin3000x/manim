from manimlib.imports import *


class Opening(Scene):
    def construct(self):
        A = [[2, 1], [1, 2]]
        mat = Matrix(A).set_column_colors(X_COLOR, Y_COLOR).to_edge(UP, buff=1)
        e1 = Matrix([1,0])
        e2 = Matrix([0,1])
        c1 = Matrix([2,1]).set_color(X_COLOR)
        c2 = Matrix([1,2]).set_color(Y_COLOR)

        self.play(Write(mat))
        self.wait()

        first = VGroup(
            mat.copy(), e1, TexMobject('='), c1
        ).arrange()
        second = VGroup(
            mat.copy(), e2, TexMobject('='), c2
        ).arrange().next_to(first, DOWN, buff=.5)
        self.play(RT(mat.copy(), first[0]))
        self.play(Write(first[1:]))
        self.wait()

        self.play(RT(mat.copy(), second[0]))
        self.play(Write(second[1:]))
        self.wait()


class Symmetric(LinearTransformationScene):
    CONFIG = {
        "foreground_plane_kwargs": {
            "x_radius": FRAME_WIDTH,
            "y_radius": FRAME_WIDTH,
            "secondary_line_ratio": 0
        },
        "background_plane_kwargs": {
            "x_min": -FRAME_X_RADIUS - 4,
            "x_max": FRAME_X_RADIUS + 4,
            "y_min": -FRAME_Y_RADIUS - 4,
            "y_max": FRAME_Y_RADIUS + 4,
            "y_radius": FRAME_WIDTH + 2,
            "color": GREY,
            "background_line_style": {
                "stroke_color": GREY,
                "stroke_width": 1,
            },
        },
    }

    def construct(self):
        A = [[2, 1], [1, 2]]
        X = [[1, -1], [1, 1]]
        self.setup()
        self.wait()

        # transforming
        self.apply_matrix(A)
        self.wait()

        # writing labels
        basis_i = self.add_vector([1, 0])
        label_i = self.write_vector_coordinates(self.i_hat, color=X_COLOR)
        basis_j = self.add_vector([0, 1])
        label_j = self.write_vector_coordinates(self.j_hat, color=Y_COLOR)
        self.wait()

        # once more
        self.moving_vectors.pop()
        self.moving_vectors.pop()
        self.remove(basis_j, basis_i)
        self.apply_inverse(A, run_time=1)
        self.wait()
        self.apply_matrix(A)

        # eigenvectors
        self.moving_vectors = []
        self.remove_foreground_mobjects(label_j, label_i)
        self.play(FadeOut(
            VGroup(self.i_hat, self.j_hat, label_i, label_j)
        ))
        self.apply_inverse(A, run_time=1)
        self.wait()
        eig1 = self.add_vector([1, 1])
        self.apply_matrix(A)
        self.wait()

        self.apply_inverse(A, run_time=1)
        self.wait()
        eig1.save_state()
        self.play(eig1.scale, .5, {"about_point": ORIGIN})
        self.apply_matrix(A)
        self.wait()

        # eigen labels
        eig_label = VGroup(TextMobject("Eigenvector", color=YELLOW), TextMobject("特征向量", color=YELLOW).scale(.8)) \
            .arrange(DOWN, buff=.1).add_background_rectangle().next_to(eig1)
        eig_val = VGroup(TextMobject("Eigenvalue: 3", color=YELLOW), TextMobject("特征值", color=YELLOW).scale(.8)) \
            .arrange(DOWN, buff=.1).add_background_rectangle().next_to(eig1, LEFT)
        line = Line(DL, UR, color=YELLOW)
        line.set_length(12)
        self.play(Write(eig_label))
        self.wait()
        self.play(GrowFromCenter(line))
        self.play(FadeOut(line))
        self.wait()
        self.play(Write(eig_val))
        self.wait()
        self.play(FadeOut(eig_label), FadeOut(eig_val))
        self.apply_inverse(A, run_time=1)
        eig1.restore()
        self.wait()

        # another eig
        eig2 = self.add_vector([-1, 1], color=PINK)
        self.wait()
        self.apply_matrix(A)
        self.wait()
        self.apply_inverse(A)
        self.wait()

        # change basis
        self.play(self.background_plane.apply_matrix, X, self.plane.apply_matrix, X)
        self.wait()
        self.apply_matrix(A)
        self.wait()
        diag = Matrix([[1, 0], [0, 3]]).set_column_colors(PINK, YELLOW).add_background_rectangle().to_corner(UL)
        self.play(Write(diag))
        self.play(FocusOn(eig2))
        c1, c2 = diag.get_columns()
        self.play(ShowCreationThenDestructionAround(c1))
        self.wait()
        self.play(FocusOn(eig1))
        self.play(ShowCreationThenDestructionAround(c2))
        self.wait()

        # similarity
        eq = TexMobject("=").add_background_rectangle().next_to(diag)
        origin = Matrix([[2, 1], [1, 2]]).set_column_colors(X_COLOR, Y_COLOR).to_corner(UL)
        X_inv_label = TexMobject("X^{-1}").next_to(eq)
        origin.next_to(X_inv_label)
        X_label = TexMobject("X").next_to(origin)
        bg = BackgroundRectangle(VGroup(X_inv_label, origin, X_label))
        self.play(Write(eq))
        self.play(FadeIn(bg))
        self.play(Write(origin))
        self.wait()
        self.play(Write(X_inv_label), Write(X_label))
        self.add_foreground_mobject(diag, eq, X_inv_label, origin, X_label)
        self.apply_inverse(A)
        self.wait()

        # talk about X
        self.play(self.plane.apply_matrix, np.linalg.inv(X),
                  self.background_plane.apply_matrix, np.linalg.inv(X))
        X_mat = Matrix([[-1, 1], [1, 1]]).set_column_colors(PINK, YELLOW)
        X_equals = VGroup(
            TexMobject('X='), X_mat
        ).arrange().add_background_rectangle().to_corner(DL, buff=2)
        self.play(Write(X_equals))
        self.wait()

        # X and eigenvectors
        c1, c2 = X_mat.get_columns()
        boxes = VGroup(SurroundingRectangle(c1), SurroundingRectangle(c2)).set_color(WHITE)
        eigenvectors = VGroup(TextMobject("Eigenvectors"), TextMobject("特征向量").scale(.8)) \
            .arrange(DOWN, buff=.1).add_background_rectangle().next_to(X_mat, DOWN)
        self.play(ShowCreation(boxes))
        self.play(Write(eigenvectors))
        self.wait()
        self.play(FadeOut(eigenvectors), FadeOut(boxes))

        # swap i and j
        i1 = TexMobject("i", color=PINK).next_to(eig2, LEFT)  # .add_background_rectangle()
        j1 = TexMobject("j", color=YELLOW).next_to(eig1, RIGHT)  # .add_background_rectangle()
        i1.generate_target()
        i1.target.set_color(YELLOW).move_to(j1)
        j1.generate_target()
        j1.target.set_color(PINK).move_to(i1)
        self.play(Write(i1))
        self.play(Write(j1))
        self.wait()
        self.play(MoveToTarget(i1), MoveToTarget(j1))
        self.wait()

        # permuting matrices
        self.play(c1.move_to, c2, c2.move_to, c1)
        diag2 = Matrix([[3, 0], [0, 1]]).set_column_colors(YELLOW, PINK).add_background_rectangle().to_corner(UL)
        self.play(RT(diag, diag2))
        self.wait()
        self.play(FadeOut(i1), FadeOut(j1))
        self.apply_matrix(A)


class Shear(LinearTransformationScene):
    CONFIG = {
        "foreground_plane_kwargs": {
            "x_max": FRAME_WIDTH,
            "x_min": -FRAME_WIDTH,
            "y_max": FRAME_WIDTH,
            "y_min": -FRAME_WIDTH,
        },
    }
    def construct(self):
        A = [[1,1], [0,1]]
        self.setup()
        self.apply_matrix(A)
        self.wait()
        i_lab = self.write_vector_coordinates(self.i_hat, color=X_COLOR, nudge=DOWN*.5)
        j_lab = self.write_vector_coordinates(self.j_hat, color=Y_COLOR)
        self.wait()

        # introduce the matrix
        A_label = Matrix(A).set_column_colors(X_COLOR, Y_COLOR).to_edge(UP)
        bg = BackgroundRectangle(A_label)
        c1, c2 = A_label.get_columns()
        brack = A_label.get_brackets()
        self.add(bg)
        self.play(AnimationGroup(RT(i_lab[1].copy(), c1), RT(j_lab[1].copy(), c2), lag_ratio=.5))
        self.play(Write(brack))
        self.wait()

        # cleaning
        self.remove_foreground_mobjects(i_lab, j_lab, A_label)
        self.remove(bg)
        self.play(FadeOut(i_lab), FadeOut(j_lab), FadeOut(A_label))
        self.apply_inverse(A, run_time=1)
        self.wait()

        # eigenvectors
        self.apply_matrix(A)
        line = Line(color=YELLOW, stroke_width=5)
        line.set_length(FRAME_WIDTH)
        self.wait()
        self.play(GrowFromCenter(line))
        self.wait()

        no = TextMobject("\\kaishu 只有一个线性无关的特征向量", color=YELLOW).scale(1.3)\
            .add_background_rectangle().next_to(line, DOWN, buff=.8)
        self.play(Write(no))
        self.wait()
        A_label.add_background_rectangle()
        self.play(Write(A_label))
        self.wait()


class Condition(Scene):
    def construct(self):
        diagonal = TexMobject(r"A", r"\text{~可以}", r"\text{相似对角化}",
                              r"~\Longleftrightarrow~",
                              "A", r"\text{~的}", r"\text{特征向量构成一组基}") \
            .tm({'A': RED, '相似': YELLOW, '特征': YELLOW})  # .to_edge(UP, buff=2)
        indept = TexMobject("A", r"\text{~有}", r'~n~\text{个线性无关的特征向量}') \
            .tm({'A': RED}).move_to(diagonal).align_to(diagonal[4], LEFT)
        indept[2:].set_color(YELLOW)
        self.play(Write(diagonal[:4]))
        self.wait()
        self.play(Write(diagonal[4:]))
        self.wait()
        self.play(
            Transform(diagonal[4], indept[0]),
            Transform(diagonal[5:], indept[1:])
        )
        self.play(diagonal.set_x, 0)
        self.wait()

        conclusion = TextMobject(r"``\kaishu 不同的特征值对应的特征向量线性无关''", color=BLUE).to_edge(UP, buff=2)
        self.play(Write(conclusion))
        self.wait()

        distinct = TextMobject("$n$ 个互异的特征值").next_to(diagonal[5:], DOWN, buff=1.5)
        self.play(Write(distinct))
        self.wait()

        implies = TexMobject("\\Longrightarrow").rotate(PI/2).scale(1.2).next_to(distinct, UP)
        self.play(Write(implies))


class Example(Scene):
    def construct(self):
        A = VGroup(TexMobject("A="),
            Matrix(np.array(['*' for _ in range(9)]).reshape((3,3)), h_buff=.8)
        ).arrange().to_edge(UP).set_color(BLUE)
        self.play(Write(A))
        self.wait()

        distinct = VGroup(TexMobject("\\lambda=1,2,3:", color=YELLOW), TextMobject('可对角化')).arrange(buff=.5)
        self.play(Write(distinct[0]))
        self.wait()
        self.play(Write(distinct[1]))
        self.wait()

        not_distinct = VGroup(TexMobject("\\lambda=1,", "2,2", ":", color=YELLOW), TextMobject('It depends.'))\
            .arrange(buff=.5).next_to(distinct, DOWN, aligned_edge=LEFT)
        self.play(Write(not_distinct[0]))
        self.wait()
        self.play(Write(not_distinct[1]))
        self.wait()

        brace = Brace(not_distinct[0][1])
        self.play(GrowFromCenter(brace))
        indept = VGroup(Matrix(np.array([1,0,0])), TexMobject(','), Matrix(np.array([0,1,0])))\
            .arrange().scale(.8).next_to(brace, DOWN)
        self.play(Write(indept))
        self.wait()

        dept = VGroup(Matrix(np.array([1,0,0])), TexMobject(','), Matrix(np.array([-1,0,0])))\
            .arrange().scale(.8).next_to(brace, DOWN)

        t = TexMobject("\\sqrt{}", color=GREEN).next_to(indept, buff=1)
        f = TexMobject("\\times", color=RED).scale(1.2).next_to(dept, buff=1)

        self.play(Write(t))
        self.wait()
        self.play(FadeOut(VGroup(indept, t)))
        self.play(Write(dept))
        self.wait()
        self.play(Write(f))
        self.wait()



class Watch3b1b(Scene):
    def construct(self):
        logo = Logo().scale(.8)
        logo = VGroup(logo, TextMobject("3Blue1Brown").scale(1.5)) \
            .arrange(DOWN, buff=.5).to_edge(LEFT, buff=1.8)
        self.play(FadeInFrom(logo, LEFT))

        arrow = Arrow(RIGHT, LEFT).set_color(YELLOW).next_to(logo[0], buff=.8)
        watch = TextMobject("\\kaishu 看他的", color=YELLOW).scale(2).next_to(arrow, buff=.5)
        self.play(GrowArrow(arrow), Write(watch))
        self.wait()

