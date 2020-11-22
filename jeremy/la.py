from manimlib.imports import *


class LA(Scene):
    CONFIG = {
        "color_map": {"A": RED, "B": BLUE, "x": RED, "y": BLUE, "O": RED, "I": BLUE, "unit": YELLOW}
    }

    def construct(self):
        self.opening()
        # self.matrices_vectors()
        self.zero_identity()
        # self.transposition()
        # self.inner_outer()

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

    def runTitle(self, title):
        self.play(Write(title[0]))
        self.play(GrowFromCenter(title[1]))

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
        self.play(Write(square_label))
        self.wait()

        # block
        array = A[1].get_entries()

        box11 = SurroundingRectangle(VGroup(array[0], array[5]), color=RED)
        box12 = SurroundingRectangle(VGroup(array[2], array[7]), color=RED).set_height(box11.get_height()).align_to(
            box11, UP)
        box13 = SurroundingRectangle(VGroup(array[8], array[13]), color=RED).set_width(box11.get_width()).align_to(
            box11, LEFT)
        box14 = SurroundingRectangle(VGroup(array[10], array[15]), color=RED).set_height(box13.get_height()).set_width(
            box12.get_width()).align_to(box12, LEFT)
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
        self.play(Write(zero))
        self.wait()
        self.play(Write(I))
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

        units = VGroup(*[TexMobject(f"e_{i+1}", color=self.color_map['unit']) for i in range(N)])
        for i,unit in enumerate(units):
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
            if i%(N+1):
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
        ctrans_prop = VGroup(TexMobject("(", r"A", r"^*)^*=", r"A"),
                             TexMobject(r"(\alpha ", r"A", r")^*=\overline{\alpha} ", r"A", r"^*"),
                             TexMobject("(", r"A", r"+", r"B", r")^*=", r"A", r"^*+", r"B", r"^*"),
                             TexMobject("(", r"A", r"B", r")^*=", r"B", r"^* ", r"A", r"^*"),
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

    def inner_outer(self):
        title = self.mT("4. inner product (内积)", underline=True)

        self.runTitle(title)
        self.wait()
        inner_def = TexMobject(r"x", r"^T ", r"y", r"=", r"x_1", r" y_1",
                               r"+", r"x_2", r" y_2", r" +", r"\cdots ", r"+",
                               r"x_n", r" y_n", ",", r"\quad x", r",",
                               r"y", r"\in\mathbb{R}^n").set_color_by_tex_to_color_map(self.color_map).next_to(
            title[-1], DOWN)
        c_inner_def = TexMobject(r"x", r"^* ", r"y", r"=", r"\overline{x_1}", r" y_1",
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

        length_formula = TexMobject(r"\Vert", r" x", r"\Vert", r"_2", r"=", r"\sqrt", r"{x", r"^* ", r"x}") \
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
        pass

    def scalar_mul(self):
        pass

    def mat_mul(self):
        pass

    def powers(self):
        pass

    def special(self):
        pass

    def linear_combination(self):
        pass

    def rank(self):
        pass

    def range_null(self):
        pass

    def det(self):
        pass

    def inv(self):
        pass

    def eigen(self):
        pass

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
