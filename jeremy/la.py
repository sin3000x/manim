from manimlib.imports import *


class LA2(Scene):
    CONFIG = {
        "color_map": {"A": RED, "B": BLUE, "x": RED, "y": BLUE, "z": GREEN, "O": RED, "I": BLUE, "unit": YELLOW},
        "x": RED, "y": BLUE
    }

    def construct(self):
        # self.opening()
        self.matrices_vectors()
        self.zero_identity()
        self.transposition()
        self.inner()
        self.addition()
        self.scalar_mul()
        self.mat_mul()
        self.special()
        self.ele_op()
        self.linear_combination()
        self.linear_dep()
        self.rank()
        self.range_null()
        self.det()
        self.inv()
        self.theorem()
        self.eigen()
    @staticmethod
    def myTitle(string, underline=True):
        title = TextMobject(f"\\textbf{{\\heiti{{{string}}}}}", color=YELLOW).to_edge(UP)
        if not underline:
            return title
        underline = Line(LEFT, RIGHT, color=YELLOW).next_to(title, DOWN, buff=MED_SMALL_BUFF).set_width(FRAME_WIDTH - 2)
        return VGroup(title, underline)

    @staticmethod
    def mT(*strings, underline=False):
        title = VGroup(*[TextMobject(f"\\textbf{{\\heiti{{{string}}}}}", color=YELLOW) for string in strings]).arrange(
            DOWN)
        if underline:
            title.to_edge(UP)
            underline = Line(LEFT, RIGHT, color=YELLOW).next_to(title, DOWN, buff=MED_SMALL_BUFF).set_width(
                FRAME_WIDTH - 2)
            return VGroup(title, underline)
        title.scale(.8)
        return title

    def mt(self, *strings, mob=None):
        brace = Brace(mob, DOWN, color=YELLOW)
        title = self.mT(*strings).next_to(brace, DOWN)
        return VGroup(brace, title)

    def runTitle(self, title):
        self.play(Write(title[0]))
        self.play(GrowFromCenter(title[1]))

    def runLabel(self, label, time=None):
        self.play(GrowFromCenter(label[0]))
        if time is None:
            self.play(Write(label[1]))
        else:
            self.play(Write(label[1]), run_time=time)

    def fadeout(self):
        self.play(*[FadeOut(mob) for mob in self.mobjects])

    def opening(self):
        l1 = TextMobject("本视频作复习/入门用")
        l2 = TextMobject("本意非教学")
        l3 = TextMobject("(￣$\\nabla$￣)$\\sim$*")
        VGroup(l1, l2, l3).arrange(DOWN, buff=MED_LARGE_BUFF).scale(1.5)
        self.add(l1, l2, l3)
        self.wait(3)
        self.remove(l1, l2, l3)

    def matrices_vectors(self):
        title = self.myTitle("1. Matrix (矩阵), Vector (向量)")
        A = VGroup(TexMobject("A="), Matrix([["a_{11}", "a_{12}", r"\cdots", "a_{1n}"],
                                             ["a_{21}", "a_{22}", r"\cdots", "a_{2n}"],
                                             ["\\vdots", "\\vdots", r"\ddots", "\\vdots"],
                                             ["a_{m1}", "a_{m2}", r"\cdots", "a_{mn}"]])).arrange(RIGHT).to_edge(LEFT)
        fields = [TexMobject("\\in", f"\\mathbb{{{f}}}^{{m \\times n}}") for f in ['F', 'R', 'C']]
        for f in fields:
            f.next_to(A, RIGHT)
        Aex = Matrix(np.array([[1, 2, 3], [4, 5, 6]]), h_buff=.8).set_color(BLUE).next_to(fields[0], RIGHT,
                                                                                          buff=LARGE_BUFF)
        Aex2 = Matrix(np.array([[1, r"2+\mathrm{i}", 3], [r"4\mathrm{i}", 5, 6]]), h_buff=1.1).set_color(BLUE).next_to(
            fields[0], RIGHT, buff=LARGE_BUFF)
        square = Matrix(np.array([[1, r"2+\mathrm{i}"], [r"4\mathrm{i}", 5]]), h_buff=1.1).set_color(BLUE).next_to(
            fields[0], RIGHT, buff=LARGE_BUFF)
        square_label = VGroup(self.myTitle("square matrix", False), self.myTitle("(方阵)", False)).arrange(DOWN).scale(
            .8).next_to(square, DOWN, buff=MED_LARGE_BUFF)
        self.runTitle(title)
        # field
        self.play(Write(A[0]))
        self.wait()
        self.play(Write(A[1]), run_time=3)
        self.wait()
        self.play(Write(fields[0]))
        self.wait()
        self.play(ReplacementTransform(fields[0], fields[1]))
        self.wait()
        self.play(Write(Aex))
        self.wait()
        self.play(ReplacementTransform(fields[1], fields[2]), ReplacementTransform(Aex, Aex2))
        self.wait(2)

        # square
        self.play(ReplacementTransform(Aex2, square))
        self.wait()
        self.play(Write(square_label))
        self.wait()

        # block
        array = A[1].get_entries()

        box11 = SurroundingRectangle(VGroup(array[0], array[5]), color=RED)
        box12 = SurroundingRectangle(VGroup(array[2], array[7]), color=RED).set_height(box11.get_height()).align_to(
            box11, UP)
        box13 = SurroundingRectangle(VGroup(array[8], array[13]), color=RED).set_width(box11.get_width()).align_to(
            box11, LEFT)
        box14 = SurroundingRectangle(VGroup(array[10], array[15]), color=RED).set_height(box13.get_height(),
                                                                                         stretch=True).set_width(
            box12.get_width(), stretch=True).align_to(box12, LEFT).align_to(box13, DOWN)
        block1 = Matrix([["A_{11}", "A_{12}"], ["A_{21}", "A_{22}"]]).move_to(square)
        block2 = Matrix([["A_{11}", "A_{12}", "\\cdots", "A_{1n}"]], h_buff=1).move_to(block1)
        block1_entries = block1.get_entries()
        block1_entries.set_color(RED)
        block2.get_entries().set_color(RED)
        block_label = VGroup(self.myTitle("block matrix", False), self.myTitle("(分块矩阵)", False)).arrange(DOWN).scale(
            .8).move_to(square_label)

        boxes = [SurroundingRectangle(column, color=RED) for column in A[1].get_columns()]
        boxes[2].set_height(boxes[0].get_height())

        self.play(FadeOut(fields[2]))
        for box in [box11, box12, box13, box14]:
            self.play(ShowCreation(box))
        self.wait()
        self.play(ReplacementTransform(box11.copy(), block1_entries[0]),
                  ReplacementTransform(box12.copy(), block1_entries[1]),
                  ReplacementTransform(box13.copy(), block1_entries[2]),
                  ReplacementTransform(box14.copy(), block1_entries[3]),
                  FadeOut(square.get_entries()),
                  ReplacementTransform(square.get_brackets(), block1.get_brackets()),
                  ReplacementTransform(square_label, block_label))
        self.wait(2)
        self.play(ReplacementTransform(box11, boxes[0]),
                  ReplacementTransform(box12, boxes[1]),
                  ReplacementTransform(box13, boxes[2]),
                  ReplacementTransform(box14, boxes[3]),
                  ReplacementTransform(block1_entries, block2.get_entries()),
                  ReplacementTransform(block1.get_brackets(), block2.get_brackets()),
                  )
        self.wait()

        # vector
        row = Matrix([[1, 2, 3, 4]], h_buff=.8)
        row_space = TexMobject("\\in", "\\mathbb{R}^{1\\times 4}").next_to(row, RIGHT).shift(UP * .1)
        row_label = VGroup(self.myTitle("row vector", False), self.myTitle("(行向量)", False)).arrange(DOWN).scale(
            .8).next_to(row, DOWN)
        column = Matrix([1, 2, 3, 4])
        column_space = TexMobject("\\in", "\\mathbb{R}^{4\\times 1}").next_to(column, RIGHT)
        vspace = TexMobject("\\in", "\\mathbb{R}^{4}").next_to(column, RIGHT)
        column_label = VGroup(self.myTitle("column vector", False), self.myTitle("(列向量)", False)).arrange(DOWN).scale(
            .8).next_to(column, DOWN)

        self.play(FadeOut(A), FadeOut(VGroup(*boxes)),
                  ReplacementTransform(block2, row),
                  ReplacementTransform(block_label, row_label), run_time=2)
        self.wait()
        self.play(Write(row_space))
        self.wait()
        self.play(ReplacementTransform(row, column),
                  ReplacementTransform(row_label, column_label),
                  ReplacementTransform(row_space, column_space))
        self.wait()
        self.play(ReplacementTransform(column_space, vspace))
        self.wait(2)
        self.play(FadeOut(VGroup(title, column, column_label, vspace)))

    def zero_identity(self):
        m, n = 2, 3
        N = 3
        title = self.mT("2. zero/identity matrix (零/单位阵)", underline=True)
        self.runTitle(title)
        self.wait()
        identity = np.identity(N, dtype=int)
        # identity2 = identity.copy().astype(object)
        # identity2[identity2 == 0] = np.nan
        # identity2 = [[1,None,None],[None,1,None],[None,None,1]]
        zero = VGroup(TexMobject("O", fr"_{{{m} \times {n}}}", "=").set_color_by_tex_to_color_map(self.color_map),
                      Matrix(np.zeros((m, n), dtype=int), h_buff=.8, v_buff=.6)).arrange()
        I = VGroup(TexMobject("I", fr"_{{{N}}}", "=").set_color_by_tex_to_color_map(self.color_map),
                   Matrix(identity, h_buff=.8, v_buff=.6)).arrange()
        # I2 = VGroup(TexMobject("I", fr"_{{{N}}}", "=").set_color_by_tex_to_color_map(self.color_map),
        #            Matrix(identity2, h_buff=.8, v_buff=.6)).arrange()
        VGroup(zero, I).arrange(DOWN).next_to(title[-1], DOWN)
        # I2.move_to(I)
        self.play(Write(zero), run_time=2)
        self.wait()
        self.play(Write(I), run_time=2)
        self.wait()

        zero_prop = TexMobject("A", "+", "O", "=", "O", "+", "A", "=", "A").set_color_by_tex("O", self.color_map['O'])
        i_prop = TexMobject("A", "I", "=", "I", "A", "=", "A").set_color_by_tex("I", self.color_map['I'])
        VGroup(zero_prop, i_prop).arrange(DOWN).next_to(I, DOWN, buff=LARGE_BUFF)
        self.play(Write(zero_prop))
        self.wait()
        self.play(Write(i_prop))
        self.wait()

        boxes = VGroup(*[SurroundingRectangle(col, color=self.color_map['unit']) for col in I[-1].get_columns()])
        # for box in boxes:
        #     self.play(ShowCreation(box))
        # self.wait()

        units = VGroup(*[TexMobject(f"e_{i + 1}", color=self.color_map['unit']) for i in range(N)])
        for i, unit in enumerate(units):
            unit.next_to(boxes[i], DOWN).scale(.8)
            self.play(ShowCreation(boxes[i]))
            self.play(Write(unit))

        label = self.mT("the $i$-th unit vector").next_to(units[-1], RIGHT, buff=MED_LARGE_BUFF)
        self.wait()
        self.play(Write(label))
        self.wait()

        self.play(FadeOut(VGroup(boxes, units, label)))
        self.wait()
        # self.play(ReplacementTransform(I, I2))
        to_fade = []
        for i, ele in enumerate(I[-1].get_entries()):
            if i % (N + 1):
                to_fade.append(ele)
        self.play(VGroup(*to_fade).fade, 1)
        self.wait()
        self.play(FadeOut(VGroup(title, zero, I, zero_prop, i_prop)))

    def transposition(self):
        title = self.mT("3. Transposition (转置运算)", underline=True)
        self.runTitle(title)
        self.wait()

        trans = TexMobject(r"\mathbb{R}^{m\times n}\to\mathbb{R}^{n\times m}", ":")
        notation = TexMobject(r"A^T, ", r"A'")
        VGroup(trans, notation).arrange(RIGHT, buff=MED_LARGE_BUFF).next_to(title[-1], DOWN)
        self.play(Write(trans))
        self.wait()
        self.play(Write(notation))
        self.wait()
        a = np.array([[1, 2, 3], [4, 5, 6]])
        at = a.T
        A = Matrix(a, h_buff=0.8)
        A.set_row_colors(RED, BLUE)  # .shift(UP)
        At = Matrix(at)
        At.set_column_colors(RED, BLUE)
        Aeq = TexMobject("A=")
        Ateq = TexMobject("A^T=")
        VGroup(Aeq, A).arrange(RIGHT).next_to(trans, DOWN, buff=MED_LARGE_BUFF).set_x(0)
        VGroup(Ateq, At).arrange(RIGHT).next_to(A, DOWN, buff=MED_LARGE_BUFF).set_x(0)
        Ac = A[0].copy()
        trans_label = self.mT("transpose", "(转置)").next_to(At, RIGHT).shift(DOWN * .2)
        self.play(Write(Aeq))
        self.play(Write(A))
        self.wait()
        self.play(Write(Ateq))
        self.wait()
        self.play(
            Ac.shift, DOWN * (A.get_y() - At.get_y()) + RIGHT * (At.get_x() - A.get_x()),
            Ac.flip, UP + LEFT
        )
        brackets = self.add_brackets(Ac)
        self.play(
            *list(it.chain(*[[Ac[i].flip, DOWN + RIGHT] for i in range(a.size)])),
            Write(brackets)
        )
        self.wait()
        self.play(Write(trans_label))
        self.wait()

        # conjugate
        self.play(VGroup(A, brackets, Ac, trans_label, Aeq, Ateq).fade, 0.6)
        self.wait()
        c_trans = TexMobject(r"\mathbb{C}^{m\times n}\to\mathbb{C}^{n\times m}", ":")
        c_notation = TexMobject(r"A^H, ", r"A^*")
        VGroup(c_trans, c_notation).arrange(RIGHT, buff=MED_LARGE_BUFF).next_to(title[-1], DOWN)
        self.play(ReplacementTransform(trans, c_trans))
        self.wait()
        self.play(ReplacementTransform(notation[0], c_notation[0]), ReplacementTransform(notation[1], c_notation[1]))
        self.wait()
        self.play(Indicate(c_notation[1]))
        self.play(Indicate(c_notation[1]))
        self.wait()

        c_A = MobjectMatrix([[TexMobject("1"), TexMobject("2", "+", "\\mathrm{i}"), TexMobject("3")],
                             [TexMobject("4"), TexMobject("5"), TexMobject("6", "-", "2\\mathrm{i}")]],
                            element_alignment_corner=ORIGIN, h_buff=1.6)
        c_A.set_row_colors(RED, BLUE)
        c_At = MobjectMatrix(
            [[TexMobject("1"), TexMobject("4")], [TexMobject("2", r"-", r"\mathrm{i}"), TexMobject("5")],
             [TexMobject("3"), TexMobject("6", r"+", r"2\mathrm{i}")]], element_alignment_corner=ORIGIN, h_buff=1.6)
        c_At.set_column_colors(RED, BLUE)
        c_Aeq = TexMobject("A=")
        c_Ateq = TexMobject("A^*=")
        VGroup(c_Aeq, c_A).arrange(RIGHT).next_to(trans, DOWN, buff=MED_LARGE_BUFF).set_x(0)
        VGroup(c_Ateq, c_At).arrange(RIGHT).next_to(c_A, DOWN, buff=MED_LARGE_BUFF).set_x(0)
        for i in [1, 5]:
            c_A.get_entries()[i].set_color_by_tex_to_color_map({"+": GREEN, "-": GREEN})
        for i in [2, 5]:
            c_At.get_entries()[i].set_color_by_tex_to_color_map({"+": GREEN, "-": GREEN})

        c_trans_label = self.mT("conjugate transpose", "(共轭转置)").next_to(c_At, RIGHT).shift(DOWN * .2)

        self.play(ReplacementTransform(Aeq, c_Aeq), ReplacementTransform(A, c_A))
        self.wait()
        self.play(ReplacementTransform(Ateq, c_Ateq),
                  ReplacementTransform(Ac[0], c_At.get_entries()[0]),
                  ReplacementTransform(Ac[3], c_At.get_entries()[1]),
                  ReplacementTransform(Ac[1], c_At.get_entries()[2]),
                  ReplacementTransform(Ac[4], c_At.get_entries()[3]),
                  ReplacementTransform(Ac[2], c_At.get_entries()[4]),
                  ReplacementTransform(Ac[5], c_At.get_entries()[5]),
                  ReplacementTransform(brackets, c_At.get_brackets()),
                  ReplacementTransform(trans_label, c_trans_label))
        self.wait(3)
        # proposition
        trans_prop = VGroup(TexMobject("(", r"A", r"^T)^T=", r"A"),
                            TexMobject(r"(\alpha ", r"A", r")^T=\alpha ", r"A", r"^T"),
                            TexMobject("(", r"A", r"+", r"B", r")^T=", r"A", r"^T+", r"B", r"^T"),
                            TexMobject("(", r"A", r"B", r")^T=", r"B", r"^T ", r"A", r"^T"),
                            ).arrange(DOWN)
        ctrans_prop = VGroup(TexMobject("(", r"A", r"^H)^H=", r"A"),
                             TexMobject(r"(\alpha ", r"A", r")^H=\overline{\alpha} ", r"A", r"^H"),
                             TexMobject("(", r"A", r"+", r"B", r")^H=", r"A", r"^H+", r"B", r"^H"),
                             TexMobject("(", r"A", r"B", r")^H=", r"B", r"^H ", r"A", r"^H"),
                             ).arrange(DOWN)
        for prop in [*trans_prop] + [*ctrans_prop]:
            prop.set_color_by_tex_to_color_map(self.color_map)

        VGroup(trans_prop, ctrans_prop).arrange(RIGHT, buff=LARGE_BUFF).next_to(c_trans, DOWN, buff=LARGE_BUFF).set_x(0)
        self.play(FadeOut(VGroup(c_Aeq, c_A, c_Ateq, c_At, c_trans_label)))
        self.play(Write(trans_prop), run_time=5)
        self.wait()
        self.play(Write(ctrans_prop), run_time=5)
        self.wait(3)

        self.play(FadeOut(VGroup(title, c_trans, c_notation, trans_prop, ctrans_prop)))

    def inner(self):
        title = self.mT("4. inner product (内积)", underline=True)

        self.runTitle(title)
        self.wait()
        inner_def = TexMobject(r"x", r"^T ", r"y", r"=", r"x_1", r" y_1",
                               r"+", r"x_2", r" y_2", r" +", r"\cdots ", r"+",
                               r"x_n", r" y_n", ",", r"\quad x", r",",
                               r"y", r"\in\mathbb{R}^n").set_color_by_tex_to_color_map(self.color_map).next_to(
            title[-1], DOWN)
        c_inner_def = TexMobject(r"x", r"^H ", r"y", r"=", r"\overline{x_1}", r" y_1",
                                 r"+", r"\overline{x_2}", r" y_2", r" +", r"\cdots ", r"+",
                                 r"\overline{x_n}", r" y_n", ",", r"\quad x", r",",
                                 r"y", r"\in\mathbb{C}^n").set_color_by_tex_to_color_map(self.color_map).move_to(
            inner_def)
        x_arr = np.array([1, 2, -1, 0])
        y_arr = np.array([2, 2, 3, 1])
        x = Matrix(x_arr)
        xT = Matrix([x_arr], h_buff=.8)
        xT.get_entries().set_color(self.color_map['x'])
        xT2 = xT.copy()

        # row = [TexMobject("\\mathrm{i}"), TexMobject("2\\mathrm{i}"), TexMobject("-\\mathrm{i}"), TexMobject("0")]
        xTc = MobjectMatrix([[TexMobject("\\mathrm{i}"), TexMobject("2", "\\mathrm{i}"), TexMobject("-", "\\mathrm{i}"),
                              TexMobject("0")]], h_buff=.8, bracket_h_buff=SMALL_BUFF)
        xTc2 = MobjectMatrix([[TexMobject("-", "\\mathrm{i}"), TexMobject("-", "2\\mathrm{i}"),
                               TexMobject("+", "\\mathrm{i}"), TexMobject("0")], ], h_buff=1, bracket_h_buff=SMALL_BUFF)
        xTc.get_entries().set_color(self.color_map['x'])
        xTc2.get_entries().set_color(self.color_map['x'])
        for i in [0, 1, 2]:
            xTc2.get_entries()[i][0].set_color(WHITE)

        y = Matrix(y_arr)
        y.get_entries().set_color(self.color_map['y'])
        y2 = Matrix(x_arr, bracket_h_buff=SMALL_BUFF)
        y2.get_entries().set_color(self.color_map['x'])
        yc = MobjectMatrix(
            [[TexMobject("\\mathrm{i}")], [TexMobject("2", "\\mathrm{i}")], [TexMobject("-", "\\mathrm{i}")],
             [TexMobject("0")]], bracket_h_buff=SMALL_BUFF)
        yc.get_entries().set_color(self.color_map['x'])
        yc2 = MobjectMatrix(
            [[TexMobject("\\mathrm{i}")], [TexMobject("2", "\\mathrm{i}")], [TexMobject("-", "\\mathrm{i}")],
             [TexMobject("0")]], bracket_h_buff=SMALL_BUFF)
        yc2.get_entries().set_color(self.color_map['x'])

        xT_entry = xT.get_entries()
        y_entry = y.get_entries()
        xTc_entry = xTc.get_entries()
        yc_entry = yc.get_entries()
        yc2_entry = yc.get_entries()
        xTc2_entry = xTc2.get_entries()

        expansion = VGroup(TexMobject("="),
                           TexMobject(str(x_arr[0]), color=self.color_map['x']), TexMobject("\\cdot"),
                           TexMobject(str(y_arr[0]), color=self.color_map['y']), TexMobject("+"),
                           TexMobject(str(x_arr[1]), color=self.color_map['x']), TexMobject("\\cdot"),
                           TexMobject(str(y_arr[1]), color=self.color_map['y']), TexMobject("+"),
                           TexMobject(str(x_arr[2]), color=self.color_map['x']), TexMobject("\\cdot"),
                           TexMobject(str(y_arr[2]), color=self.color_map['y']), TexMobject("+"),
                           TexMobject(str(x_arr[3]), color=self.color_map['x']), TexMobject("\\cdot"),
                           TexMobject(str(y_arr[3]), color=self.color_map['y']),
                           ).arrange()
        VGroup(xT, y, expansion).arrange().next_to(inner_def, DOWN, buff=MED_LARGE_BUFF)
        result = TexMobject("=", str(x_arr.dot(y_arr))).next_to(expansion, DOWN, aligned_edge=LEFT,
                                                                buff=MED_LARGE_BUFF * 3)

        expansion2 = VGroup(TexMobject("="),
                            TexMobject(str(x_arr[0]), color=self.color_map['x']), TexMobject("\\cdot"),
                            TexMobject(str(x_arr[0]), color=self.color_map['x']), TexMobject("+"),
                            TexMobject(str(x_arr[1]), color=self.color_map['x']), TexMobject("\\cdot"),
                            TexMobject(str(x_arr[1]), color=self.color_map['x']), TexMobject("+"),
                            TexMobject(str(x_arr[2]), color=self.color_map['x']), TexMobject("\\cdot"),
                            TexMobject(str(x_arr[2]), color=self.color_map['x']), TexMobject("+"),
                            TexMobject(str(x_arr[3]), color=self.color_map['x']), TexMobject("\\cdot"),
                            TexMobject(str(x_arr[3]), color=self.color_map['x']),
                            ).arrange()
        VGroup(xT2, y2, expansion2).arrange().next_to(inner_def, DOWN, buff=MED_LARGE_BUFF)
        result2 = TexMobject("=", str(x_arr.dot(x_arr))).next_to(expansion2, DOWN, aligned_edge=LEFT,
                                                                 buff=MED_LARGE_BUFF * 3)

        expansionc = VGroup(TexMobject("="),
                            xTc_entry[0].copy(), TexMobject("\\cdot"),
                            yc_entry[0].copy(), TexMobject("+"),
                            xTc_entry[1].copy(), TexMobject("\\cdot"),
                            yc_entry[1].copy(), TexMobject("+"),
                            xTc_entry[2].copy(), TexMobject("\\cdot"),
                            yc_entry[2].copy(), TexMobject("+"),
                            xTc_entry[3].copy(), TexMobject("\\cdot"),
                            yc_entry[3].copy(),
                            ).arrange()
        VGroup(xTc, yc, expansionc).arrange().next_to(inner_def, DOWN, buff=MED_LARGE_BUFF)
        resultc = TexMobject("=", "-6").next_to(expansionc, DOWN, aligned_edge=LEFT,
                                                buff=MED_LARGE_BUFF * 3)

        expansionc2 = VGroup(TexMobject("="),
                             xTc2_entry[0].copy(), TexMobject("\\cdot"),
                             yc2_entry[0].copy(), TexMobject("+"),
                             xTc2_entry[1].copy(), TexMobject("\\cdot"),
                             yc2_entry[1].copy(), TexMobject("+"),
                             xTc2_entry[2][-1].copy(), TexMobject("\\cdot"),
                             yc2_entry[2].copy(), TexMobject("+"),
                             xTc2_entry[3].copy(), TexMobject("\\cdot"),
                             yc2_entry[3].copy(),
                             ).arrange()
        VGroup(xTc2, yc2, expansionc2).arrange().next_to(inner_def, DOWN, buff=MED_LARGE_BUFF)
        resultc2 = TexMobject("=", "6").next_to(expansionc2, DOWN, aligned_edge=LEFT,
                                                buff=MED_LARGE_BUFF * 3)

        self.play(Write(inner_def))
        self.wait()
        self.play(Write(xT))
        self.play(Write(y))
        self.wait()
        self.play(Write(expansion[0]))
        self.play(ReplacementTransform(xT_entry[0].copy(), expansion[1]),
                  ReplacementTransform(y_entry[0].copy(), expansion[3]), Write(expansion[2]))
        self.play(Write(expansion[4]))
        self.play(ReplacementTransform(xT_entry[1].copy(), expansion[5]),
                  ReplacementTransform(y_entry[1].copy(), expansion[7]), Write(expansion[6]))
        self.play(Write(expansion[8]))
        self.play(ReplacementTransform(xT_entry[2].copy(), expansion[9]),
                  ReplacementTransform(y_entry[2].copy(), expansion[11]), Write(expansion[10]))
        self.play(Write(expansion[12]))
        self.play(ReplacementTransform(xT_entry[3].copy(), expansion[13]),
                  ReplacementTransform(y_entry[3].copy(), expansion[15]), Write(expansion[14]))
        self.wait()
        self.play(Write(result))
        self.wait()

        # length
        self.play(ReplacementTransform(xT, xT2), ReplacementTransform(y, y2))
        self.play(ReplacementTransform(expansion, expansion2))
        self.play(ReplacementTransform(result, result2))
        length = TexMobject(fr"\sqrt{{{x_arr.dot(x_arr)}}}", color=YELLOW).next_to(result2, RIGHT, buff=LARGE_BUFF * 2)
        self.wait()
        self.play(Write(length))
        length_label = self.mT("length", "(长度)").next_to(length, DOWN)
        self.play(Write(length_label))
        self.wait()

        self.play(VGroup(xT2, y2, expansion2, result2, length, length_label).fade, 0.6)
        self.wait(2)
        self.play(ReplacementTransform(inner_def, c_inner_def), run_time=1.5)
        self.wait()

        self.play(FadeOut(VGroup(length, length_label)))
        self.play(ReplacementTransform(xT2, xTc), ReplacementTransform(y2, yc))
        self.play(ReplacementTransform(expansion2, expansionc))
        self.play(ReplacementTransform(result2, resultc))

        self.wait(2)
        self.play(ReplacementTransform(xTc, xTc2), ReplacementTransform(yc, yc2))
        self.play(ReplacementTransform(expansionc, expansionc2))
        self.play(ReplacementTransform(resultc, resultc2))
        self.wait()

        length_formula = TexMobject(r"\Vert", r" x", r"\Vert", r"_2", r"=", r"\sqrt", r"{x", r"^H ", r"x}") \
            .next_to(c_inner_def, DOWN, aligned_edge=LEFT)
        for i in [1, 6, 8]:
            length_formula[i].set_color(self.color_map['x'])
        self.play(ReplacementTransform(VGroup(xTc2, yc2, expansionc2, resultc2), length_formula))
        self.wait()

        other_form = TexMobject("x", "\\cdot", "y", "=", r"\langle", r" x", r",", r"y", r" \rangle") \
            .set_color_by_tex_to_color_map(self.color_map).next_to(c_inner_def[3], RIGHT)

        e1 = Matrix([1, 1, -2], bracket_h_buff=SMALL_BUFF)
        e1_norm = Matrix([r"\tfrac{1}{\sqrt{6}}", r"\tfrac{1}{\sqrt{6}}", r"-\tfrac{2}{\sqrt{6}}"],
                         bracket_h_buff=SMALL_BUFF, v_buff=1)
        e2 = Matrix([0, 2, 1])
        e2_norm = Matrix([0, r"\tfrac{2}{\sqrt{5}}", r"\tfrac{1}{\sqrt{5}}"], v_buff=1)
        e1_norm.get_brackets().set_height(e2_norm.get_brackets().get_height())
        dot = Dot()
        dot2 = Dot()
        eq0 = TexMobject("=0")
        eq02 = eq0.copy()
        v1 = VGroup(e1, dot, e2, eq0).arrange().next_to(length_formula, DOWN).set_x(0)
        v2 = VGroup(e1_norm, dot2, e2_norm, eq02).arrange().next_to(length_formula, DOWN).set_x(0)
        brace1 = Brace(VGroup(e1, e2), DOWN, color=YELLOW)
        brace2 = Brace(VGroup(e1_norm, e2_norm), DOWN, color=YELLOW)
        orthogonal_label = self.mT("orthogonal", "(正交)").next_to(brace1, DOWN)
        orthonormal_label = self.mT("orthonormal", "(标准正交)").next_to(brace2, DOWN)
        self.play(Transform(c_inner_def[4:-4], other_form))
        self.wait()
        self.play(Write(v1))
        self.wait()
        self.play(GrowFromCenter(brace1))
        self.play(Write(orthogonal_label))
        self.wait()
        self.play(FadeOut(VGroup(brace1, orthogonal_label)))
        self.play(ReplacementTransform(v1, v2))
        self.wait()
        self.play(GrowFromCenter(brace2))
        self.play(Write(orthonormal_label))
        self.wait(2)

        self.play(FadeOut(VGroup(title, c_inner_def, length_formula, v2, brace2, orthonormal_label)))

    def addition(self):
        title = self.mT("5. Addition (加法)", underline=True)
        self.runTitle(title)
        self.wait()

        trans = TexMobject(r"\mathbb{R}^{m\times n}\times\mathbb{R}^{m\times n}\to\mathbb{R}^{m\times n}")
        trans.next_to(title[-1], DOWN)
        self.play(Write(trans))
        self.wait(2)

        a = np.array([[1, 1], [1, 2], [1, 3]])
        b = np.array([[0, 0], [0, 1], [1, 2]])
        A = Matrix(a, h_buff=1)
        A.get_entries().set_color(self.color_map['x'])
        B = Matrix(b, h_buff=1)
        B.get_entries().set_color(self.color_map['y'])
        beginning = VGroup(A, TexMobject("+"), B, TexMobject("=")).arrange()
        mob_matrix = np.array([VGroup(TexMobject("a"))], dtype=object).repeat(6).reshape(3, 2)
        for i in range(3):
            for j in range(2):
                mob_matrix[i][j] = TexMobject(str(a[i][j]), "+", str(b[i][j]))
                mob_matrix[i][j][0].set_color(self.color_map['A'])
                mob_matrix[i][j][2].set_color(self.color_map['B'])
        C = MobjectMatrix(mob_matrix, h_buff=1.5)
        VGroup(beginning, C).arrange()  # .next_to(trans, DOWN, buff=MED_LARGE_BUFF)

        self.play(Write(beginning))
        self.wait()
        A_entries, B_entries, C_entries = A.get_entries(), B.get_entries(), C.get_entries()

        def update_matrices(entries):
            A_entries, B_entries, C_entries = entries
            for A_entry, B_entry, C_entry in zip(A_entries, B_entries, C_entries):
                A_entry.copy().become(C_entry[0])
            return C_entries

        self.play(AnimationGroup(*[ReplacementTransform(A_entries[i].copy(), C_entries[i][0]) for i in range(a.size)],
                                 lag_ratio=0),
                  AnimationGroup(*[ReplacementTransform(B_entries[i].copy(), C_entries[i][2]) for i in range(b.size)],
                                 lag_ratio=0),
                  AnimationGroup(*[Write(C_entries[i][1]) for i in range(a.size)], lag_ratio=0),
                  Write(C.get_brackets()), run_time=3)

        self.wait()
        result = Matrix(a + b, h_buff=1).next_to(beginning, RIGHT)
        for ele in result.get_entries():
            ele.set_color_by_gradient([RED, BLUE])
        beginning_c = beginning.copy()
        VGroup(beginning_c, result).arrange()
        self.play(ReplacementTransform(beginning, beginning_c), ReplacementTransform(C, result))
        self.wait()
        self.play(FadeOut(VGroup(title, beginning_c, C, trans, result)))

    def scalar_mul(self):
        title = self.mT("6. Scalar-Matrix Multiplication (数量乘法)", underline=True)
        self.runTitle(title)
        self.wait()

        trans = TexMobject(r"\mathbb{R}\times\mathbb{R}^{m\times n}\to\mathbb{R}^{m\times n}")
        trans.next_to(title[-1], DOWN)
        self.play(Write(trans))
        self.wait(2)

        a = np.array([[1, 1], [1, 2], [1, 3]])
        A = Matrix(a, h_buff=1)
        A.get_entries().set_color(self.x)
        two = TexMobject("2", color=self.y)
        eq = TexMobject("=")
        mob_matrix = np.array([VGroup(TexMobject("a"))], dtype=object).repeat(6).reshape(3, 2)
        for i in range(3):
            for j in range(2):
                mob_matrix[i][j] = TexMobject("2", r"\cdot", str(a[i][j]))
                mob_matrix[i][j][0].set_color(self.y)
                mob_matrix[i][j][2].set_color(self.x)
        R = MobjectMatrix(mob_matrix, h_buff=1.5)
        v = VGroup(two, A, eq, R).arrange()
        # self.play(Write(two))
        # self.play(Write(A))
        # self.play(Write(eq))
        self.play(Write(v[:3]))
        self.wait()
        Rs = R.get_entries()
        As = A.get_entries()
        self.play(Write(R.get_brackets()),
                  AnimationGroup(*[ReplacementTransform(As[i].copy(), Rs[i][2]) for i in range(a.size)]), )
        self.play(
            AnimationGroup(*[ReplacementTransform(two.copy(), Rs[i][0]) for i in range(a.size)]),
            AnimationGroup(*[Write(Rs[i][1]) for i in range(a.size)]),
            run_time=2
        )
        self.wait()
        result = Matrix(2 * a, h_buff=1)
        for ele in result.get_entries():
            ele.set_color_by_gradient([self.y, self.x])
        A_c = A.copy()
        twoc = two.copy()
        eqc = eq.copy()
        VGroup(twoc, A_c, eqc, result).arrange()
        self.play(
            ReplacementTransform(A, A_c),
            ReplacementTransform(two, twoc),
            ReplacementTransform(eq, eqc),
            ReplacementTransform(R, result)
        )
        self.wait()
        self.play(FadeOut(VGroup(title, A_c, R, trans, result, twoc, eqc)))
        # for a, r in zip(A.get_entries(), R.get_entries()):
        #     ReplacementTransform(a.copy(), r[0])

    def mat_mul(self):
        title = self.mT("7. Matrix-Matrix Multiplication (矩阵乘法)", underline=True)
        self.runTitle(title)
        self.wait()

        trans = TexMobject(r"\R^{m\times r}\times\R^{r\times n}\to\R^{m\times n}")
        trans.next_to(title[-1], DOWN)
        box = SurroundingRectangle(VGroup(trans[0][3], trans[0][6]), color=RED)
        a = np.array([[1, 1], [1, 2], [1, 3], [1, 4]])
        b = np.array([[1, 2, 3], [4, 5, 6]])
        c = a.dot(b)
        A = Matrix(a).set_column_colors(self.x, self.y)
        B = Matrix(b).set_row_colors(self.x, self.y)
        C = Matrix(c)
        for ele in C.get_entries():
            ele.set_color_by_gradient([RED, BLUE])
        formula = VGroup(A, B, TexMobject("="), C).arrange()
        sizes = VGroup(TexMobject(r"4\times 2"), TexMobject(r"2\times 3"), TexMobject(r"4\times 3"))
        for s, m in zip(sizes, [A, B, C]):
            s.next_to(m, DOWN)
        for s in sizes[1:]:
            s.align_to(sizes[0], UP)
        rows = VGroup(*[SurroundingRectangle(row, buff=.2) for row in A.get_rows()])
        columns = VGroup(*[SurroundingRectangle(c, buff=.2) for c in B.get_columns()])
        # rows.save_state()
        columns[0].save_state()
        A1 = Matrix([a[0]]).set_column_colors(RED, BLUE)
        B1 = Matrix([[1], [4]]).set_row_colors(RED, BLUE)
        ex1 = VGroup(A1, B1, TexMobject(*r"= 1 \cdot 1 + 1 \cdot 4 = 5".split())).arrange().to_edge(DOWN)
        for ind, color in zip([1, 3, 5, 7], [RED, BLUE, RED, BLUE]):
            ex1[2][ind].set_color(color)
        ex1[2][-1].set_color_by_gradient([RED, BLUE])

        self.play(Write(trans))
        self.wait(2)
        self.play(ShowCreationThenDestruction(box))
        # self.add(box)
        self.wait()
        self.play(Write(A), run_time=2)
        self.play(Write(B), run_time=2)
        self.play(Write(formula[2]))
        self.play(Write(C.get_brackets()))
        self.wait()
        for size in sizes:
            self.play(Write(size))
            # self.wait()
        self.play(FadeOut(sizes))
        self.wait()
        self.play(ShowCreation(rows[0]))
        self.play(ShowCreation(columns[0]))
        self.wait()
        self.play(Write(A1.get_brackets()),
                  Write(B1.get_brackets()),
                  ReplacementTransform(A.get_rows()[0].copy(), ex1[0].get_rows()[0]),
                  ReplacementTransform(B.get_columns()[0].copy(), ex1[1].get_columns()[0]),
                  )
        self.play(Write(ex1[2:]), run_time=2)
        self.wait()
        self.play(ReplacementTransform(ex1[2][-1].copy(), C.get_entries()[0]))
        self.play(FadeOut(ex1))
        for i in [1, 2]:
            self.play(Transform(columns[0], columns[i]))
            self.play(ReplacementTransform(VGroup(A.get_rows()[0], B.get_columns()[i]).copy(),
                                           C.get_entries()[i]))
        self.play(Restore(columns[0]), Transform(rows[0], rows[1]))
        for row in range(1, 4):
            for column in range(3):
                if column > 0:
                    self.play(Transform(columns[0], columns[column]))
                self.play(ReplacementTransform(VGroup(A.get_rows()[row], B.get_columns()[column]).copy(),
                                               C.get_rows()[row][column]))
            if row < 3:
                self.play(Restore(columns[0]),
                          Transform(rows[0], rows[row + 1]))
        self.play(FadeOut(rows[0]),
                  FadeOut(columns[0]),
                  FadeIn(sizes))
        self.wait()
        complexity = VGroup(TexMobject("O(n^3)"),
                            TexMobject(r"\to", "O(n^{2.8074})"),
                            TexMobject(r"\to", "O(n^{2.3728596})")).arrange().to_edge(DOWN, buff=1.5)
        strassen_brace = Brace(complexity[1][1], DOWN, color=YELLOW)
        strassen_label = self.mT("Strassen算法").next_to(strassen_brace, DOWN)
        now_brace = Brace(complexity[2][1], DOWN, color=YELLOW)
        now_label = self.mT("2020最新进展").next_to(now_brace, DOWN)
        self.play(FadeOut(sizes))
        self.play(Write(complexity[0]))
        self.wait()
        self.play(Write(complexity[1]))
        self.play(GrowFromCenter(strassen_brace))
        self.play(Write(strassen_label))
        self.wait()
        self.play(Write(complexity[2]))
        self.play(GrowFromCenter(now_brace))
        self.play(Write(now_label))
        self.wait()
        self.play(FadeOut(VGroup(strassen_brace, strassen_label,
                                 now_brace, now_label,
                                 complexity)))
        non_abel = TexMobject(r"AB\neq BA",r",\quad (AB)C=A(BC)", color=YELLOW).to_edge(DOWN, buff=1)
        zero_factor = TexMobject(r"AB=O~\centernot\Longrightarrow~ A=O",r"~\text{或}~","B=O", color=YELLOW).move_to(non_abel)
        self.play(Write(non_abel[0]))
        self.wait()
        self.play(Write(non_abel[1:]))
        self.wait()
        self.play(FadeOut(non_abel))
        self.play(Write(zero_factor))
        self.wait()

        self.play(*[FadeOut(mob) for mob in self.mobjects])

    def special(self):
        title = self.mT("8. Special Matrices (特殊矩阵)", underline=True)
        self.runTitle(title)
        self.wait()

        # powers
        equations = VGroup(
            *[TexMobject(f"{i}") for i in [r"A^2=I\colon", r"A^2=A\colon", r"A^k=O,~k\in\mathbb{N}^*\colon"]]) \
            .arrange(DOWN, buff=LARGE_BUFF, aligned_edge=LEFT).to_edge(LEFT, buff=LARGE_BUFF)
        defs = VGroup(*[self.mT(f"{i}") for i in
                        ["involutory matrix（乘方矩阵）", "idempotent matrix（幂等矩阵）", "nilpotent matrix（幂零矩阵）"]]) \
            .arrange(DOWN, buff=LARGE_BUFF, aligned_edge=LEFT).shift(RIGHT * 2)
        for i in range(3):
            defs[i].scale(1.2)  # .next_to(equations[i])
            self.play(Write(equations[i]))
            self.play(Write(defs[i]))
            self.wait()
        self.play(FadeOut(VGroup(equations, defs)))

        # diagonal
        diag = [[1, -2, 1], [0, 2, 3], [1, 2, -1]]
        diag = Matrix(diag)
        diag.save_state()
        # self.remove(*[diag.get_entries()[i] for i in [1,2,3,5,6,7]])
        VGroup(*[diag.get_entries()[i] for i in [1, 2, 3, 5, 6, 7]]).fade(1)
        diag_b = Brace(diag, DOWN, color=YELLOW)
        diag_l = self.mT("diagonal matrix", "(对角矩阵)").next_to(diag_b, DOWN)
        upper_l = self.mT("upper triangular matrix", "(上三角矩阵)").next_to(diag_b, DOWN)
        lower_l = self.mT("lower triangular matrix", "(下三角矩阵)").next_to(diag_b, DOWN)
        self.play(Write(diag), run_time=2)
        self.play(GrowFromCenter(diag_b))
        self.play(Write(diag_l))
        self.wait()
        # self.play(FadeIn(VGroup(*[diag.get_entries()[i] for i in [1,2,5]])))
        self.play(ReplacementTransform(diag_l, upper_l),
                  VGroup(*[diag.get_entries()[i] for i in [1, 2, 5]]).set_opacity, 1)
        self.wait()
        self.play(ReplacementTransform(upper_l, lower_l),
                  VGroup(*[diag.get_entries()[i] for i in [3, 6, 7]]).set_opacity, 1,
                  VGroup(*[diag.get_entries()[i] for i in [1, 2, 5]]).set_opacity, 0)
        self.wait()
        self.play(FadeOut(VGroup(lower_l, diag_b, diag)))

        # symmetric
        a = [[0, 1, 2], [1, 3, 5], [2, 5, -1]]
        A = Matrix(a, h_buff=1.6)

        Ae = A.get_entries()
        # for i, e in enumerate(Ae):
        #     if i == 0:
        #         e.set_color(RED)
        #     if i in [1,3]:
        #         e.set_color(YELLOW)
        #     if i in [2, 6]:
        #         e.set_color(BLUE)
        #     if i in [4]:
        #         e.set_color(RED)
        #     if i in [5,7]:
        #         e.set_color(GREEN)
        #     if i in [8]:
        #         e.set_color(RED)
        self.play(Write(A))
        self.play(
            VGroup(Ae[1], Ae[3]).set_color, RED, )
        self.play(
            VGroup(Ae[2], Ae[6]).set_color, BLUE, )
        self.play(
            VGroup(Ae[5], Ae[7]).set_color, GREEN,
        )
        Ah = A.deepcopy()
        Ah.get_entries()[1].become(TexMobject(r"1+\i", color=RED).move_to(Ae[1]).align_to(Ae[1], LEFT))
        Ah.get_entries()[3].become(TexMobject(r"1-\i", color=RED).move_to(Ae[3]).align_to(Ae[3], LEFT))
        # self.play(Ae.flip, DOWN+RIGHT, rate_func = lambda x: there_and_back(smooth(x/2)))
        sym_b = Brace(A, DOWN, color=YELLOW)
        sym_l = self.mT("symmetric matrix", "(对称矩阵)").next_to(sym_b, DOWN)
        herm_l = self.mT("Hermitian matrix", "(埃尔米特矩阵)").next_to(sym_b, DOWN)
        self.play(GrowFromCenter(sym_b))
        self.play(Write(sym_l))
        self.wait()
        self.play(ReplacementTransform(A, Ah),
                  ReplacementTransform(sym_l, herm_l), run_time=2)
        self.wait()
        self.play(FadeOut(VGroup(Ah, herm_l, sym_b)))

        # definite
        pre = TextMobject("对任何", "非零", "向量", "$x$", "$=(x_1,x_2,x_3)^T$").next_to(title[1], DOWN)
        pre_semi = TextMobject("对任何", "向量", "$x$", r"$=(x_1,\ldots,x_n)^T$").next_to(title[1], DOWN)
        pre_ind = TextMobject("存在", r"$x,y\in\R^n$").next_to(title[1], DOWN)
        a = [[1, -1, -1], [-1, 2, 0], [-1, 0, 3]]
        A = Matrix(a, h_buff=1.2)
        xt = Matrix([['x_1', 'x_2', 'x_3']], h_buff=1.1)
        x = Matrix([['x_1'], ['x_2'], ['x_3']])
        def_mat = VGroup(xt, A, x).arrange().next_to(pre, DOWN)
        def_res = TexMobject(*"= 1 x_1 ^2 + 2 x_2 ^2 + 3 x_3 ^2 - 2 x_1 x_2 - 2 x_1 x_3 + 0 x_2 x_3".split())
        ###################### 0 1  2   3 4 5  6   7 8 9  10 11 1213 14  15 1617 18 19 20 21 22 23
        def_res.next_to(def_mat, DOWN, submobject_to_align=def_res[1], aligned_edge=LEFT, buff=MED_SMALL_BUFF)
        labels = VGroup(TexMobject("x^T"), TexMobject("A"), TexMobject("x"))
        for i, (d, l) in enumerate(zip(def_mat, labels)):
            l.set_color(YELLOW).next_to(d, DOWN)
        for i in [0, 2]:
            labels[i].align_to(labels[1], DOWN)
        self.play(Write(pre))
        self.wait()
        for m, l in zip(def_mat, labels):
            self.play(Write(m), FadeIn(l))
        # self.play(Write(def_mat))
        self.wait()
        self.play(FadeOut(labels))
        self.play(Write(def_res))
        self.wait()
        Ae = A.get_entries()
        self.play(VGroup(def_res[1], def_res[5], def_res[9]).set_color, RED,
                  VGroup(Ae[0], Ae[4], Ae[8]).set_color, RED)
        self.wait()
        a12_21 = TexMobject("a_{12}+a_{21}", color=BLUE).scale(.8).next_to(def_res[12:14], DOWN, buff=MED_LARGE_BUFF)
        a13_31 = TexMobject("a_{13}+a_{31}", color=YELLOW).scale(.8).next_to(def_res[16:18], DOWN, buff=MED_LARGE_BUFF)
        a23_32 = TexMobject("a_{23}+a_{32}", color=GREEN).scale(.8).next_to(def_res[21], DOWN, buff=MED_LARGE_BUFF)
        self.play(def_res[12:14].set_color, BLUE,
                  VGroup(Ae[1], Ae[3]).set_color, BLUE)
        self.play(Write(a12_21))
        self.wait()
        self.play(def_res[16:18].set_color, YELLOW,
                  VGroup(Ae[2], Ae[6]).set_color, YELLOW)
        self.play(Write(a13_31))
        self.wait()
        self.play(def_res[21].set_color, GREEN,
                  VGroup(Ae[5], Ae[7]).set_color, GREEN)
        self.play(Write(a23_32))
        self.wait()
        quadra_b = Brace(def_res, DOWN, color=YELLOW)
        quadra_l = self.mT("quadratic form", "(二次型)").next_to(quadra_b, DOWN)
        self.play(FadeOut(VGroup(a12_21, a13_31, a23_32)))
        self.play(GrowFromCenter(quadra_b))
        self.play(Write(quadra_l))
        self.wait()
        self.play(FadeOut(VGroup(quadra_b, quadra_l)))
        g0 = TexMobject(">", "0").next_to(def_res, DOWN, aligned_edge=LEFT, buff=MED_LARGE_BUFF)
        geq0 = TexMobject(r"\geq", "0").next_to(def_res, DOWN, aligned_edge=LEFT)
        self.play(Write(g0))
        self.wait()
        self.play(FadeOut(VGroup(def_res, g0)))
        self.play(def_mat.move_to, LEFT)
        posdef = self.mt("positive definite（正定）", mob=def_mat[1])  # .next_to(g0, RIGHT, buff=MED_LARGE_BUFF)
        self.play(GrowFromCenter(posdef[0]))
        self.play(Write(posdef[1]))
        self.wait()

        semi = TexMobject("x^T", "A", "x", r"\geq", "0")
        ind = TexMobject("(", "x^T", "A", "x", ")(y^T A y)", r"<", "0")
        self.play(FadeOut(posdef))
        self.play(*[ReplacementTransform(def_mat[i], semi[i]) for i in range(3)])
        self.wait()
        self.play(Write(semi[3:]))
        semidef = self.mt("positive semi-definite（半正定）", mob=semi[1])
        indef = self.mt("indefinite（不定）", mob=ind[2])
        self.wait()
        self.play(GrowFromCenter(semidef[0]))
        self.play(Write(semidef[1]))
        self.wait()
        self.play(ReplacementTransform(pre, pre_semi))
        self.wait()
        self.play(ReplacementTransform(pre_semi, pre_ind),
                  ReplacementTransform(semi, ind),
                  ReplacementTransform(semidef[0], indef[0]),
                  ReplacementTransform(semidef[1], indef[1]),
                  )
        self.wait()
        to_herm = TexMobject(r"x^T A x\to x^H A x", color=YELLOW).to_edge(DOWN, buff=LARGE_BUFF)
        self.play(Write(to_herm))
        self.wait()
        self.play(FadeOut(VGroup(pre_ind, indef, ind, to_herm)))

        # orthogonal
        q = [["\\sqrt 2\\over 2", "\\sqrt 2\\over 2"], ["-{\\sqrt 2\\over 2}", "\\sqrt 2\\over 2"]]
        u = [["{1+\\i}\\over 2", "{1-\\i}\\over 2"], ["{{1-\\i}}\\over 2}", "{1+\\i}\\over 2"]]
        ut = [["{1-\\i}\\over 2", "{1+\\i}\\over 2"], ["{{1+\\i}}\\over 2}", "{1-\\i}\\over 2"]]
        q = np.array(q)
        u = np.array(u)
        Q = Matrix(q, v_buff=1.5, h_buff=1.5)
        Qt = Matrix(q.T, v_buff=1.5, h_buff=1.5)
        U = Matrix(u, v_buff=1.5, h_buff=1.5)
        Ut = Matrix(ut, v_buff=1.5, h_buff=1.5)
        I = Matrix([[1, 0], [0, 1]])
        ortho = VGroup(Q, Qt, TexMobject("="), I).arrange()
        uni = VGroup(U, Ut, TexMobject("="), I.copy()).arrange()
        self.play(Write(ortho[0]))
        self.wait()
        self.play(Write(ortho[1:]))
        self.wait()
        orth_label = self.mt("orthogonal matrix", "(正交矩阵)", mob=Q)
        uni_label = self.mt("unitary matrix", "(酉矩阵)", mob=U)
        self.play(GrowFromCenter(orth_label[0]))
        self.play(Write(orth_label[1]))
        self.wait()
        self.play(*[ReplacementTransform(ortho[i], uni[i]) for i in range(4)],
                  ReplacementTransform(orth_label[0], uni_label[0]),
                  ReplacementTransform(orth_label[1], uni_label[1]),
                  )
        self.wait()
        self.play(*[FadeOut(mob) for mob in self.mobjects])

    def ele_op(self):
        title = self.mT("9. Elementary Row Operations (初等行变换)", underline=True)
        self.runTitle(title)
        self.wait()
        row_switching = self.mT("row switching","(交换两行)")
        row_mul = self.mT("row multiplication","(乘非0数)")
        row_add = self.mT("row addition","(倍加)")
        a = np.array([[1, 0, 1], [0, 2, 1], [1, 1, 1]])
        a1 = np.array([[0, 2, 1], [1, 0, 1], [1, 1, 1]])
        a2 = np.array([[1, 0, 1], [0, 2, 1], [2, 2, 2]])
        a3 = np.array([[1, 0, 1], [0, 2, 1], [0, 1, 0]])

        A1, A2, A3 = Matrix(a, v_buff=.6, h_buff=.9), Matrix(a, v_buff=.6, h_buff=.9), Matrix(a, v_buff=.6, h_buff=.9)
        A11, A21, A31 = Matrix(a1, v_buff=.6, h_buff=.9), Matrix(a2, v_buff=.6, h_buff=.9), Matrix(a3, v_buff=.6, h_buff=.9)
        A1.set_row_colors(RED, BLUE, WHITE)
        A11.set_row_colors(BLUE, RED, WHITE)
        A2.set_row_colors(WHITE, WHITE, RED)
        A21.set_row_colors(WHITE, WHITE, RED)
        A3.set_row_colors(RED, WHITE, BLUE)
        A31.set_row_colors(RED, WHITE, BLUE)
        for ele in A31.get_rows()[2]:
            ele.set_color_by_gradient([RED, BLUE])

        for mat in [A1, A2, A3, A11, A21, A31]:
            mat.scale(.95)
        matrices = VGroup(A1, A2, A3).arrange(DOWN).next_to(title[1], DOWN)
        matrices_changed = VGroup(A11, A21, A31)
        labels = VGroup(row_switching, row_mul, row_add).arrange(DOWN,).to_edge(LEFT)
        for label, mat in zip(labels, matrices):
            label.set_y(mat.get_y())
        # for ch in [ row_mul[1], row_add[1]]:
        #     ch.align_to(row_switching[1],LEFT)
        matrices.shift(LEFT*0.5)
        for mat, change in zip(matrices, matrices_changed):
            change.next_to(mat, RIGHT, buff=LARGE_BUFF*2)
        arrows = VGroup(*[Line(mat.get_right(), change.get_left(), buff=.3).add_tip(tip_length=.2) for mat, change in zip(matrices, matrices_changed)])
        row_labels = VGroup(*[TexMobject(f"{i}", color=YELLOW) for i in [r"r_1\leftrightarrow r_2", "2r_3","r_3-r_1"]])
        for label, arrow in zip(row_labels, arrows):
            label.next_to(arrow, UP)

        self.play(Write(labels[0]))
        self.wait()
        self.play(Write(matrices[0]))
        # self.wait()
        self.play(GrowArrow(arrows[0]), Write(row_labels[0]))
        # self.wait()
        self.play(Write(matrices_changed[0].get_brackets()),
                  Write(matrices_changed[0].get_rows()[2]))
        self.play(ReplacementTransform(matrices[0].get_rows()[0].copy(),
                                       matrices_changed[0].get_rows()[1]),
                  ReplacementTransform(matrices[0].get_rows()[1].copy(),
                                       matrices_changed[0].get_rows()[0]),
                  run_time=2)
        self.wait()

        self.play(Write(labels[1]))
        self.wait()
        self.play(Write(matrices[1]))
        self.play(GrowArrow(arrows[1]), Write(row_labels[1]))
        self.play(Write(matrices_changed[1].get_brackets()),
                  Write(matrices_changed[1].get_rows()[:2]))
        self.play(ReplacementTransform(matrices[1].get_rows()[2].copy(),
                                       matrices_changed[1].get_rows()[2]), run_time=2)
        self.wait()

        self.play(Write(labels[2]))
        self.wait()
        self.play(Write(matrices[2]))
        self.play(GrowArrow(arrows[2]), Write(row_labels[2]))
        self.play(Write(matrices_changed[2].get_brackets()),
                  Write(matrices_changed[2].get_rows()[:2]))
        self.play(ReplacementTransform(VGroup(matrices[2].get_rows()[0],
                                              matrices[2].get_rows()[2]).copy(),
                                       matrices_changed[2].get_rows()[2]), run_time=2)
        self.wait()
        self.play(*[FadeOut(mob) for mob in self.mobjects])

    def linear_combination(self):
        title = self.mT("10. Linear Combination（线性组合）", underline=True)
        self.runTitle(title)
        self.wait()
        alpha_val = ValueTracker(1)
        alpha = DecimalNumber(0.1).add_updater(lambda x: x.set_value(alpha_val.get_value()))
        beta_val = ValueTracker(1)
        beta = DecimalNumber(0).add_updater(lambda x: x.set_value(beta_val.get_value()))
        a_vec = lVector([3,0], tip_length=.2).set_color(RED)
        b_vec = lVector([3,3], tip_length=.2).set_color(BLUE)
        c_vec = lVector([6,3], tip_length=.2).set_color_by_gradient(PURPLE)
        VGroup(a_vec, b_vec, c_vec).shift(LEFT*4+DOWN*2)
        a_label = TexMobject("a", color=RED)#.next_to(a_vec.get_end(), DOWN)
        b_label = TexMobject("b", color=BLUE)#.next_to(b_vec.get_end(), UP)
        c_label = TexMobject("c", color=PURPLE)#.next_to(c_vec.get_end(), UP)
        # self.play(Write(b_label))
        # self.play(Write(c_label))
        a_label.add_updater(lambda x: x.next_to(a_vec.get_end(), DOWN))
        b_label.add_updater(lambda x: x.next_to(b_vec.get_end(), UP))
        c_label.add_updater(lambda x: x.next_to(c_vec.get_end(), UP))
        # self.play()
        A = Matrix([[1],[0]]).set_color(RED)
        B = Matrix([[1],[1]]).set_color(BLUE)
        lc = VGroup(TexMobject(r"c","=").set_color_by_tex("c", PURPLE), alpha, A, TexMobject("+"), beta, B).arrange(buff=.5).to_edge(RIGHT)
        self.play(GrowArrow(a_vec), GrowArrow(b_vec),Write(a_label), Write(b_label), )
        self.play(GrowArrow(c_vec),Write(c_label),Write(lc), run_time=3)
        brace = Brace(lc, DOWN, color=YELLOW)
        linear = self.mt("a,b的线性组合", mob=lc[1:])
        # self.play()
        a_vec.add_updater(lambda x: x.become(lVector([3*alpha_val.get_value(), 0], tip_length=.2).set_color(RED).shift(LEFT*4+DOWN*2)))
        b_vec.add_updater(lambda x: x.become(lVector([3*beta_val.get_value(), 3*beta_val.get_value()], tip_length=.2).set_color(BLUE).shift(LEFT*4+DOWN*2)))
        c_vec.add_updater(lambda x: x.become(lVector([3*(alpha_val.get_value()+beta_val.get_value()), 3*beta_val.get_value()], tip_length=.2).set_color(PURPLE).shift(LEFT*4+DOWN*2)))

        self.play(alpha_val.set_value, 1.4, beta_val.set_value, -0.2, run_time=2)
        # self.play(GrowFromCenter(brace))
        # self.play(Write(span))
        self.play(alpha_val.set_value, -0.5, beta_val.set_value, 1.2, run_time=3)
        self.wait()
        self.play(GrowFromCenter(linear[0]))
        self.play(Write(linear[1]))
        self.wait()
        self.play(FadeOut(linear))
        span = TexMobject(r"\{c\}",r"=",r"\mathrm{span}(",r"a",r",",r"b",r")").next_to(lc, DOWN, buff=LARGE_BUFF, aligned_edge=LEFT)
        span.tm({"a": RED, "b": BLUE, "span": WHITE})
        span[0][1].set_color(PURPLE)
        span_label = self.mt("a,b张成的空间", mob=span[2:])
        self.play(ReplacementTransform(lc[0][0].copy(),span[0][1]),
                  Write(span[0][0]),
                  Write(span[0][2]))
        self.play(Write(span[1:]))
        self.wait()
        self.play(GrowFromCenter(span_label[0]))
        self.play(Write(span_label[1]))
        self.wait()
        for arrow in [a_vec, b_vec, c_vec]:
            arrow.clear_updaters()
        self.play(*[FadeOut(mob) for mob in self.mobjects])

    def linear_dep(self):
        title = self.mT("11. Linearly (In)dependent（线性相关/无关）", underline=True)
        self.runTitle(title)
        self.wait()
        e1 = Matrix([[1],[0],[0]])
        e2 = Matrix([[0],[1],[0]])
        e3 = Matrix([[0],[0],[-1]])
        e = Matrix([[1],[-2],[0]])
        zero = Matrix([[0],[0],[0]])
        indept = VGroup(TexMobject("0",r"\cdot"),e1,
                        TexMobject("+"),TexMobject("0",r"\cdot"),e2,
                        TexMobject("+"),TexMobject("0",r"\cdot"),e3,
                        TexMobject("="), zero
                        ).arrange()
        dept = VGroup(TexMobject("-1",r"\cdot"),e1.copy(),
                        TexMobject("+"),TexMobject("2",r"\cdot"),e2.copy(),
                        TexMobject("+"),TexMobject("1",r"\cdot"),e,
                        TexMobject("="), zero.copy()
                        ).arrange()
        indept_label = self.mt("linearly independent","(线性无关)", mob=indept[:-2])
        dept_label = self.mt("linearly dependent","(线性相关)", mob=indept[:-2])
        for zero in [indept[i] for i in [0,3,6]]+[dept[i] for i in [0,3,6]]:
            zero[0].set_color(RED)
        self.play(Write(indept))
        self.wait()
        self.play(GrowFromCenter(indept_label[0]))
        self.play(Write(indept_label[1]))
        self.wait()
        self.play(ReplacementTransform(indept, dept),
                  ReplacementTransform(indept_label, dept_label))
        self.wait()
        self.fadeout()

    def rank(self):
        title = self.mT("12. Rank（秩）", underline=True)
        self.runTitle(title)
        self.wait()
        a = np.array([[1,0,1],[0,1,2],[0,0,0]])
        A = Matrix(a)
        A_mat = VGroup(TexMobject("A="),A).arrange()
        cols = VGroup(*[SurroundingRectangle(col, buff=.2) for col in A.get_columns()])
        rows = VGroup(*[SurroundingRectangle(row, color=RED) for row in A.get_rows()])
        rank = TexMobject(r"\mathrm{rank}(A)=2").next_to(A_mat, DOWN, buff=MED_LARGE_BUFF)
        self.play(Write(A_mat))
        self.wait()
        self.play(ShowCreation(cols), run_time=2)
        self.wait()
        self.play(Write(rank))
        self.wait()
        self.play(ReplacementTransform(cols, rows))
        self.wait()
        self.fadeout()

    def range_null(self):
        title = self.mT("13. Range（值域）, Null Space（零空间）", underline=True)
        self.runTitle(title)
        self.wait()
        a = np.array([[1,0,-1],[2,1,0]])
        zero = Matrix([[0],[0]])
        A = Matrix(a)
        A_blo = Matrix([['a_1','a_2','a_3']])
        A_blo.set_column_colors(BLUE, YELLOW, GREEN)
        A.set_column_colors(BLUE, YELLOW, GREEN)
        A_cols = VGroup(*[
            Matrix([[1],[2]]).set_column_colors(BLUE),
            Matrix([[0],[1]]).set_column_colors(YELLOW),
            Matrix([[-1],[0]]).set_column_colors(GREEN),
        ])
        X = Matrix([['x_1'],['x_2'],['x_3']])
        X.set_column_colors(RED)
        AX = VGroup(A, X).arrange()
        AX_blo = VGroup(A_blo, X.copy(), TexMobject(*"= x_1 a_1 + x_2 a_2 + x_3 a_3".split())
        ############################################## 0 1   2  3  4   5  6  7   8
                        .tm({"a_1": BLUE, 'a_2': YELLOW, 'a_3': GREEN, "x": RED})).arrange()
        A_span = VGroup(Matrix(a, h_buff=1).set_column_colors(BLUE, YELLOW, GREEN), X.copy(), TexMobject("="),
                        TexMobject("x_1", color=RED),A_cols[0],
                        TexMobject("+"),TexMobject("x_2", color=RED),A_cols[1],
                        TexMobject("+"),TexMobject("x_3", color=RED),A_cols[2],
                        ).arrange()
        A_null = VGroup(Matrix(a, h_buff=1).set_column_colors(BLUE, YELLOW, GREEN), X.copy(),
                        TexMobject("="), zero).arrange()

        labels = VGroup(TexMobject("A"), TexMobject("x"))
        labels[0].next_to(A, DOWN, buff=LARGE_BUFF)
        labels[1].next_to(X, DOWN).align_to(labels[0], DOWN)
        Range = self.mt("所有向量构成了",r"$\mathrm{range}(A)$", mob=AX)
        range_span = TexMobject(r"\mathrm{range}(A)=\mathrm{span}(a_1,a_2,a_3)", color=YELLOW).next_to(AX, DOWN, buff=MED_LARGE_BUFF)
        dim_range = TexMobject(r"\mathrm{dim}(\mathrm{range}(A))",r"=\mathrm{rank}(A)", color=YELLOW).next_to(range_span, DOWN)
        self.play(Write(A), FadeIn(labels[0]))
        self.play(Write(X), FadeIn(labels[1]))
        self.wait()
        self.play(FadeOut(labels))
        self.runLabel(Range)
        self.wait()
        self.play(FadeOut(Range))
        self.play(
            ReplacementTransform(AX[1], AX_blo[1]),
            ReplacementTransform(AX[0].get_brackets(), AX_blo[0].get_brackets()),
            ReplacementTransform(AX[0].get_columns()[0], AX_blo[0].get_columns()[0]),
            ReplacementTransform(AX[0].get_columns()[1], AX_blo[0].get_columns()[1]),
            ReplacementTransform(AX[0].get_columns()[2], AX_blo[0].get_columns()[2]),
        )
        self.play(Write(AX_blo[2:]))
        self.wait()
        self.play(
            ReplacementTransform(AX_blo[0].get_brackets(), A_span[0].get_brackets()),
            ReplacementTransform(AX_blo[0].get_columns()[0], A_span[0].get_columns()[0]),
            ReplacementTransform(AX_blo[0].get_columns()[1], A_span[0].get_columns()[1]),
            ReplacementTransform(AX_blo[0].get_columns()[2], A_span[0].get_columns()[2]),
            ReplacementTransform(AX_blo[1], A_span[1]),
            ReplacementTransform(AX_blo[2][0], A_span[2]),
            ReplacementTransform(AX_blo[2][2], A_span[4]),
            ReplacementTransform(AX_blo[2][5], A_span[7]),
            ReplacementTransform(AX_blo[2][8], A_span[10]),
            ReplacementTransform(AX_blo[2][1], A_span[3]),
            ReplacementTransform(AX_blo[2][4], A_span[6]),
            ReplacementTransform(AX_blo[2][7], A_span[9]),
            ReplacementTransform(AX_blo[2][3], A_span[5]),
            ReplacementTransform(AX_blo[2][6], A_span[8]), run_time=2
        )
        self.wait()
        self.play(Write(range_span))
        self.wait()
        self.play(Write(dim_range[0]))
        self.wait()
        self.play(Write(dim_range[1:]))
        self.wait()
        self.play(FadeOut(range_span), FadeOut(dim_range))

        # null space
        self.play(RT(A_span, A_null))
        self.wait()
        null_label = self.mt("所有解构成了",r"$\mathrm{null}(A)$",mob=A_null[1])
        self.runLabel(null_label, time=2)
        self.wait()
        self.play(FadeOut(null_label))
        rank_nullity = TexMobject(r"\mathrm{rank}(A)",r"+",r"\mathrm{dim}(\mathrm{null}(A))",r"=",r"3").to_edge(DOWN, buff=1.5)
        self.play(Write(rank_nullity))
        china = TextMobject("秩",r"$+$",r"基础解系个数",r"$=$",r"列数").move_to(rank_nullity)
        self.wait()
        self.play(RT(rank_nullity, china))
        self.wait()
        rn_label = self.mt("rank-nullity theorem（秩-零化度定理）",mob=china)
        self.runLabel(rn_label, time=2)
        self.wait()
        self.fadeout()

    def det(self):
        title = self.mT("14. Determinant（行列式）", underline=True)
        self.runTitle(title)
        self.wait()
        notation = VGroup(TexMobject(r"\C^{n\times n}\to\C\colon"), TexMobject(r"\quad |A|,~\det(A)")).arrange(buff=MED_LARGE_BUFF).next_to(title[1], DOWN)
        a = [[1,0,2],[-2,1,3],[0,4,1]]
        A = Matrix(a).next_to(notation, DOWN)
        self.play(Write(notation[0]))
        self.wait()
        self.play(Write(notation[1]))
        self.wait()
        line_h = Line(color=BLUE).replace(A.get_rows()[0])
        row1 = TextMobject("\\kaishu 行",r"1").next_to(line_h, LEFT, buff=LARGE_BUFF)
        line_v = Line(UP, DOWN, color=BLUE).replace(A.get_columns()[1])
        col2 = TextMobject("\\kaishu 列","2").next_to(line_v, DOWN)
        VGroup(row1[1], col2[1]).set_color(BLUE)
        minor = VGroup(TexMobject("M",r"_{12}",r"=").set_color_by_tex("12", BLUE),Matrix([[-2,3],[0,1]], bracket='v')).arrange()
        cofactor = VGroup(TexMobject("A",r"_{12}",r"=","(-1)","^",r"{1","+","2}").tm({"1": BLUE, "2": BLUE, "-1": WHITE}),Matrix([[-2,3],[0,1]], bracket='v')).arrange()
        minor[1].get_entries().set_color(RED)
        cofactor[1].get_entries().set_color(RED)
        minor_label = self.mT("minor（余子式）")
        cofactor_label = self.mT("cofactor（代数余子式）")
        VGroup(minor, minor_label).arrange(buff=MED_LARGE_BUFF).next_to(A, DOWN, buff=LARGE_BUFF)
        VGroup(cofactor, cofactor_label).arrange(buff=MED_LARGE_BUFF).next_to(A, DOWN, buff=LARGE_BUFF)
        expansion = VGroup(Matrix(a, bracket='v'),TexMobject(r"= ",r"1",r"\cdot A_{11}+",r"0",r"\cdot A_{12}+",r"2",r"\cdot A_{13}")).arrange().move_to(A)
        VGroup(expansion[0].get_rows()[0], expansion[1][1],expansion[1][3],expansion[1][5]).set_color(RED)
        column_exp = TexMobject(r"=",r"0",r"\cdot A_{12}+",r"1",r"\cdot A_{22}+",r"4",r"\cdot A_{32}").next_to(expansion[1], DOWN, aligned_edge=LEFT, buff=LARGE_BUFF)
        for i in [1,3,5]:
            column_exp[i].set_color(BLUE)
        one = TexMobject(r"\det(a)=a")
        two = VGroup(Matrix([['a','b'],['c', 'd']], bracket='v',element_alignment_corner=DL), TexMobject("="," ad","-","bc").tm({'ad': RED, 'bc': BLUE})).arrange()
        for ele, color in zip(two[0].get_entries(), [RED, BLUE, BLUE, RED]):
            ele.set_color(color)
        VGroup(one, two).arrange(buff=LARGE_BUFF).next_to(column_exp, DOWN, buff=MED_LARGE_BUFF).set_x(0)
        self.play(Write(A))
        self.wait()
        self.play(ShowCreation(line_h))
        self.play(Write(row1))
        self.play(ShowCreation(line_v))
        self.play(Write(col2))
        self.play(VGroup(*[A.get_entries()[i] for i in [3,5,6,8]]).set_color, RED)
        self.wait()
        self.play(*[RT(A.get_entries()[i].copy(), minor[1].get_entries()[j]) for i, j in zip([3,5,6,8],[0,1,2,3])],
                  Write(minor[1].get_brackets()))
        self.play(Write(minor[0]))
        self.play(Write(minor_label))
        self.wait()
        self.play(RT(minor, cofactor), RT(minor_label, cofactor_label))
        self.wait()
        self.play(FadeOut(VGroup(cofactor, cofactor_label, line_h, line_v, row1, col2)))
        self.play(RT(A, expansion[0]))
        self.wait()
        self.play(Write(expansion[1]))
        self.wait()
        self.play(Write(column_exp), VGroup(expansion[0].get_entries()[1],expansion[0].get_entries()[4],expansion[0].get_entries()[7]).set_color, BLUE)
        self.wait()
        self.play(Write(one))
        self.wait()
        self.play(Write(two))
        self.wait()
        self.fadeout()

    def inv(self):
        title = self.mT("15. Inverse（逆）", underline=True)
        self.runTitle(title)
        self.wait()
        a = [[1,2],[1,1]]
        ainv = [[-1,2],[1,-1]]
        i = [[1,0],[0,1]]
        A = Matrix(a)
        Ainv = Matrix(ainv)
        I = Matrix(i)
        equation = VGroup(A,Ainv,TexMobject("="),I).arrange().next_to(title[1], DOWN)
        # equation2 = VGroup(Ainv.copy(),A.copy(),TexMobject("="),I).arrange()
        A_label = self.mt("$A$", mob=A)
        # A_label.add_updater(lambda x: x.next_to(A, DOWN))
        Ainv_label = self.mt("$A^{-1}$", mob=Ainv)
        adj_equation = TexMobject(r"A^{-1}={",r"{\mathrm{adj}(A)}",r"\over",r"{\det(A)}}")
        adj_equation[1].set_color(BLUE)
        adj = Matrix([['A_{11}','A_{21}',r'\cdots','A_{n1}'],
                      ['A_{12}','A_{22}',r'\cdots','A_{n2}'],
                      [r'\vdots',r'\vdots',r'\ddots',r'\vdots'],
                      ['A_{1n}','A_{2n}',r'\cdots','A_{nn}'],]).set_color(BLUE)
        adj_def = VGroup(adj,TexMobject("="),TexMobject("A^*")).arrange()
        VGroup(adj_equation, adj_def).arrange(buff=LARGE_BUFF).next_to(A_label, DOWN).set_x(0)
        adj_label = self.mt("adjugate","(伴随矩阵)",mob=adj_def[-1])
        adj_label[1].shift(UP*.1)
        self.play(Write(equation))
        self.runLabel(A_label)
        self.runLabel(Ainv_label)
        self.wait()
        self.play(A.move_to, Ainv, Ainv.move_to, A,
                  A_label.move_to, Ainv_label, Ainv_label.move_to, A_label, rate_func=there_and_back, run_time=2)
        self.wait()
        self.play(Write(adj_equation))
        self.wait()
        self.play(Write(adj_def[0]))
        self.wait()
        self.play(Write(adj_def[1:]))
        self.wait()
        self.runLabel(adj_label, time=2)
        self.wait()
        self.play(ShowPassingFlashAround(adj_equation[-1]))
        self.play(ShowPassingFlashAround(adj_equation[-1]))
        self.wait()
        self.fadeout()

    def theorem(self):
        title = self.mT("16. Theorem（定理）", underline=True)
        self.runTitle(title)
        self.wait()
        pre = TexMobject(r"\text{设}~",r"A\in\C^{n\times n},",r"~\text{那么以下命题等价.}").next_to(title[1], DOWN)
        tmp = [r"1.~ \det(A)\neq 0",
               r"2.~ A^{-1}~\text{存在.}",
               r"3.~ \mathrm{rank}(A)=n",
               r"4.~ \mathrm{null}(A)=\{0\}",
               r"5.~ A~\text{的特征值都不为}~0."]
        conditions = VGroup(*[TexMobject(condition) for condition in tmp]).arrange(DOWN, buff=.5, aligned_edge=LEFT)\
            .next_to(pre, DOWN, buff=MED_LARGE_BUFF)
        self.play(Write(pre))
        self.wait()
        for c in conditions:
            self.play(Write(c))
            self.wait()
        brace = Brace(conditions, LEFT, color=YELLOW)
        label = self.mT("nonsingular","(非奇异)").scale(1.1).next_to(brace, LEFT)
        self.runLabel(VGroup(brace, label))
        self.wait()
        self.fadeout()

    def eigen(self):
        title = self.mT("17. Eigenvalue（特征值）", underline=True)
        self.runTitle(title)
        self.wait()
        pre = TexMobject(r"A\in\C^{n\times n},\quad 0\neq x\in\C^n").next_to(title[1], DOWN)
        a = np.array([[2,1],[1,2]])
        first = ValueTracker(2.5)
        second = ValueTracker(-1.4)
        origin = LEFT*5+DOWN*2
        x = lVector([first.get_value(), second.get_value()], tip_length=.2).set_color(RED).shift(origin)
        Ax = lVector(np.dot(a, np.array([[first.get_value()], [second.get_value()]]).flatten()), tip_length=.2).set_color(BLUE).shift(origin)
        x_label = TexMobject("x", color=RED).add_updater(lambda t: t.next_to(x.get_end()))
        Ax_label = TexMobject("Ax", color=BLUE).add_updater(lambda t: t.next_to(Ax.get_end()))
        self.play(Write(pre))
        self.wait()
        self.play(GrowArrow(x), Write(x_label))
        self.play(GrowArrow(Ax), Write(Ax_label))
        self.wait()
        x.add_updater(lambda x: x.become(lVector([first.get_value(), second.get_value()], tip_length=.2).set_color(RED)).shift(origin))
        Ax.add_updater(lambda x: x.become(lVector(np.dot(a, np.array([[first.get_value()], [second.get_value()]])).flatten(), tip_length=.2).set_color(BLUE)).shift(origin))
        self.play(first.set_value, 1, second.set_value, 1, run_time=3)
        self.wait()

        eigen_equation = TexMobject(*r"A x = \lambda x".split()).set_color_by_tex("x", RED).to_edge(RIGHT, buff=5)
        eigenval = self.mt("eigenvalue","(特征值)", mob=eigen_equation[3])
        eigenvec = self.mt("eigenvector","(特征向量)",mob=eigen_equation[1])
        self.play(Write(eigen_equation))
        self.wait()
        self.runLabel(eigenval)
        self.wait()
        self.play(RT(eigenval, eigenvec))
        self.wait()
        self.play(first.set_value, -.5, second.set_value, -.5, run_time=3)
        self.play(first.set_value, 1.5, second.set_value, 1.5, run_time=3)
        self.wait()

    @staticmethod
    def add_brackets(m):
        bracket_pair = TexMobject("\\left(", "\\right)")
        bracket_pair.scale(2)
        bracket_pair.stretch_to_fit_height(
            m.get_height() + 2 * SMALL_BUFF
        )
        l_bracket, r_bracket = bracket_pair.split()

        l_bracket.next_to(m, LEFT, SMALL_BUFF)
        r_bracket.next_to(m, RIGHT, SMALL_BUFF)
        return VGroup(l_bracket, r_bracket)
